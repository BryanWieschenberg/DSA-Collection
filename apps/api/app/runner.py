import os
import json
import traceback
import boto3
from urllib.parse import urlparse
from botocore.client import Config

from dotenv import load_dotenv
from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel
from concurrent.futures import ProcessPoolExecutor, TimeoutError
import multiprocessing

from app.executor import execute_case
from app.dsa import truncate_str_repr

load_dotenv()

router = APIRouter()

pool_size = max(2, min(4, multiprocessing.cpu_count()))
executor = ProcessPoolExecutor(max_workers=pool_size)


def warm_up():
    try:
        futures = [executor.submit(abs, 0) for _ in range(pool_size)]
        for f in futures:
            f.result()
    except Exception as e:
        print(f"Error warming up executor: {e}")


warm_up()


def reset_executor():
    global executor
    try:
        executor.shutdown(wait=False)
    except Exception:
        pass
    executor = ProcessPoolExecutor(max_workers=pool_size)
    warm_up()


class CaseItem(BaseModel):
    input: str
    expected: str
    hidden: bool


class RunRequest(BaseModel):
    userCode: str
    functionName: Optional[str] = None
    isClass: bool
    cases: List[CaseItem]
    timeLimitMs: int = 1000
    memLimitMb: int = 128
    isSubmit: bool = False
    problemId: Optional[int] = None


def fetch_hidden_tests(problem_id: int):
    try:
        full_endpoint = os.getenv("R2_ENDPOINT_URL")
        aws_access_key_id = os.getenv("R2_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("R2_SECRET_KEY")
        if not all([full_endpoint, aws_access_key_id, aws_secret_access_key]):
            return []
        parsed = urlparse(full_endpoint)
        bucket_name = parsed.path.strip("/")
        endpoint_url = f"{parsed.scheme}://{parsed.netloc}"
        object_name = f"hiddenTests-{problem_id}.json"
        s3_client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=Config(signature_version="s3v4"),
        )
        response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
        data = json.loads(response["Body"].read().decode("utf-8"))
        if isinstance(data, dict) and "tests" in data:
            return data["tests"]
        elif isinstance(data, list):
            for item in data:
                if item.get("id") == problem_id:
                    return item.get("tests", [])
    except Exception as e:
        print(f"Error loading hidden tests from R2: {e}")
    return []


@router.post("/run")
def run_code(req: RunRequest):
    global executor

    if req.isSubmit and req.problemId is not None:
        hidden_tests = fetch_hidden_tests(req.problemId)
        for ht in hidden_tests:
            req.cases.append(
                CaseItem(
                    input=ht["input"],
                    expected=ht.get("expected") or ht.get("output") or "",
                    hidden=True,
                )
            )

    results = []

    try:
        compile(req.userCode, "<string>", "exec")
    except Exception as e:
        err_msg = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        for i, c in enumerate(req.cases):
            results.append(
                {
                    "caseNum": i + 1,
                    "status": "RE",
                    "error": err_msg,
                    "stdout": "",
                    "output": None,
                    "timeMs": 0.0,
                    "memMb": 0.0,
                    "input": truncate_str_repr(c.input),
                    "expected": truncate_str_repr(c.expected),
                }
            )
        return results

    futures = []
    for i, c in enumerate(req.cases):
        f = executor.submit(
            execute_case,
            req.userCode,
            req.functionName,
            req.isClass,
            c.input,
            c.expected,
            req.timeLimitMs,
            req.memLimitMb,
        )
        futures.append((f, i, c))

    tle_occurred = False
    timeout_sec = (req.timeLimitMs + 200) / 1000.0

    results = [None] * len(req.cases)

    for f, i, c in futures:
        if tle_occurred:
            results[i] = {
                "caseNum": i + 1,
                "status": "TLE",
                "error": "Time Limit Exceeded",
                "stdout": "",
                "output": None,
                "timeMs": float(req.timeLimitMs),
                "memMb": 0.0,
                "input": truncate_str_repr(c.input),
                "expected": truncate_str_repr(c.expected),
            }
            continue

        try:
            res = f.result(timeout=timeout_sec)
            res["caseNum"] = i + 1
            res["input"] = truncate_str_repr(c.input)
            res["expected"] = truncate_str_repr(c.expected)
            results[i] = res
            if res["status"] in ("TLE", "MLE"):
                tle_occurred = True
        except TimeoutError:
            tle_occurred = True
            results[i] = {
                "caseNum": i + 1,
                "status": "TLE",
                "error": "Time Limit Exceeded",
                "stdout": "",
                "output": None,
                "timeMs": float(req.timeLimitMs),
                "memMb": 0.0,
                "input": truncate_str_repr(c.input),
                "expected": truncate_str_repr(c.expected),
            }
            reset_executor()
        except Exception as e:
            is_oom = (
                "BrokenProcessPool" in type(e).__name__
                or "BrokenExecutor" in type(e).__name__
            )
            if is_oom:
                reset_executor()
            results[i] = {
                "caseNum": i + 1,
                "status": "MLE" if is_oom else "RE",
                "error": "Memory Limit Exceeded (Process terminated)"
                if is_oom
                else f"Internal Runner Error: {str(e)}",
                "stdout": "",
                "output": None,
                "timeMs": 0.0,
                "memMb": 0.0,
                "input": truncate_str_repr(c.input),
                "expected": truncate_str_repr(c.expected),
            }

    return results


@router.get("/solution/{problem_id}")
def get_solution(problem_id: int):
    from fastapi import HTTPException

    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "solutions.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Solutions file not found")
    with open(path, "r") as f:
        solutions = json.load(f)
    sol = solutions.get(str(problem_id))
    if sol is None:
        raise HTTPException(status_code=404, detail="Solution not found")
    return {"solution": sol}
