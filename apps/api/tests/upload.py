import sys
import os
import json
import inspect
import boto3
from urllib.parse import urlparse
from botocore.client import Config
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from tests.testgen import TestGen


def main():
    generator = TestGen()
    problem_id = generator.id

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, ".."))
    project_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))

    load_dotenv(dotenv_path=os.path.join(workspace_root, ".env"))

    if "class " in generator.code:
        method_name = generator.code.split("class ")[1].split(":")[0].split("(")[0].strip()
    else:
        method_name = generator.code.split("(")[0].strip()
    solution_class = None
    is_class_design = False


    for attr_name in dir(generator):
        attr = getattr(generator, attr_name)
        if isinstance(attr, type) and attr.__name__ == method_name:
            solution_class = attr
            is_class_design = True
            break

    if not solution_class:
        for attr_name in dir(generator):
            attr = getattr(generator, attr_name)
            if isinstance(attr, type) and hasattr(attr, method_name):
                solution_class = attr
                break

    if not solution_class:
        solution_class = getattr(
            generator, "Solution", getattr(TestGen, "Solution", None)
        )

    if is_class_design:
        oracle_method = None
        params = []
    else:
        oracle = solution_class()
        oracle_method = getattr(oracle, method_name)
        sig = inspect.signature(oracle_method)
        params = list(sig.parameters.values())

    def run_case(case):
        if is_class_design:
            results = []
            obj = None
            for m_name, args in case:
                if obj is None:
                    obj = solution_class(*args)
                    results.append(None)
                else:
                    method = getattr(obj, m_name)
                    results.append(method(*args))
            return results

        if isinstance(case, dict):
            return oracle_method(**case)
        if len(params) > 1:
            if isinstance(case, (list, tuple)):
                return oracle_method(*case)
        return oracle_method(case)

    def format_input(case):
        if is_class_design:
            return json.dumps(case)

        if isinstance(case, dict):
            return ", ".join(f"{k} = {json.dumps(v)}" for k, v in case.items())
        if len(params) > 1 and isinstance(case, (list, tuple)):
            return ", ".join(
                f"{p.name} = {json.dumps(val)}" for p, val in zip(params, case)
            )
        param_name = params[0].name if params else "input"
        return f"{param_name} = {json.dumps(case)}"

    public_inputs = generator.get_public_cases()
    private_inputs = generator.get_private_cases()

    examples = []
    for case in public_inputs:
        formatted_input = format_input(case)
        output = run_case(case)
        examples.append({"input": formatted_input, "output": json.dumps(output)})

    time_limit = getattr(generator, "timeLimit", getattr(generator, "time_limit", None))
    memory_limit = getattr(
        generator, "memoryLimit", getattr(generator, "memory_limit", None)
    )

    problems_json_path = os.path.join(
        project_root, "apps", "web", "src", "lib", "problems.json"
    )
    if os.path.exists(problems_json_path):
        with open(problems_json_path, "r") as f:
            try:
                problems = json.load(f)
            except Exception:
                problems = []
    else:
        problems = []

    problem_idx = -1
    for idx, prob in enumerate(problems):
        if prob.get("id") == problem_id:
            problem_idx = idx
            break

    problem_obj = {
        "id": problem_id,
        "name": generator.name,
        "difficulty": generator.difficulty,
        "code": generator.code,
        "description": generator.description,
        "constraints": generator.constraints,
        "examples": examples,
    }

    if time_limit is not None:
        problem_obj["timeLimit"] = time_limit
    if memory_limit is not None:
        problem_obj["memoryLimit"] = memory_limit

    if problem_idx != -1:
        problems[problem_idx] = problem_obj
    else:
        problems.append(problem_obj)

    with open(problems_json_path, "w") as f:
        json.dump(problems, f, indent=4)

    private_tests = []
    for case in private_inputs:
        formatted_input = format_input(case)
        output = run_case(case)
        private_tests.append(
            {"input": formatted_input, "expected": json.dumps(output)}
        )

    hidden_data = {"tests": private_tests}

    hidden_dir = os.path.join(script_dir, "hidden")
    os.makedirs(hidden_dir, exist_ok=True)
    local_file = os.path.join(hidden_dir, f"hiddenTests-{problem_id}.json")
    with open(local_file, "w") as f:
        json.dump(hidden_data, f, indent=4)

    full_endpoint = os.getenv("R2_ENDPOINT_URL")
    aws_access_key_id = os.getenv("R2_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("R2_SECRET_KEY")

    if not all([full_endpoint, aws_access_key_id, aws_secret_access_key]):
        return

    parsed = urlparse(full_endpoint)
    bucket_name = parsed.path.strip("/")
    endpoint_url = f"{parsed.scheme}://{parsed.netloc}"
    object_name = f"hiddenTests-{problem_id}.json"

    try:
        s3_client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=Config(signature_version="s3v4"),
        )
        s3_client.upload_file(local_file, bucket_name, object_name)
    except Exception:
        pass


if __name__ == "__main__":
    main()
