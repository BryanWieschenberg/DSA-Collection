from fastapi import APIRouter, HTTPException

from problems import PROBLEM_REGISTRY
from schemas import RunRequest, RunResponse, TestCaseResult
from executor import execute_solution

router = APIRouter(prefix="/run", tags=["runner"])


@router.post("/", response_model=RunResponse)
async def run_code(req: RunRequest):
    """Run user code against test cases for a problem."""
    problem = PROBLEM_REGISTRY.get(req.slug)
    if not problem:
        raise HTTPException(status_code=404, detail=f"Problem '{req.slug}' not found")

    all_cases = problem["test_cases"]
    display_cases = problem["test_cases_display"]

    if req.test_indices is not None:
        indices = [i for i in req.test_indices if 0 <= i < len(all_cases)]
    else:
        indices = list(range(len(all_cases)))

    results: list[TestCaseResult] = []

    for idx in indices:
        tc = all_cases[idx]
        disp = display_cases[idx]

        actual, error, stdout = execute_solution(
            code=req.code,
            method_name="twoSum",
            args=tc["args"],
            timeout=5,
        )

        if error:
            results.append(
                TestCaseResult(
                    index=idx,
                    input=disp["input"],
                    expected=disp["expected"],
                    actual=None,
                    passed=False,
                    error=error,
                    stdout=stdout,
                )
            )
        else:
            passed = normalize(actual) == normalize(tc["expected"])
            results.append(
                TestCaseResult(
                    index=idx,
                    input=disp["input"],
                    expected=disp["expected"],
                    actual=str(actual),
                    passed=passed,
                    error=None,
                    stdout=stdout,
                )
            )

    passed_count = sum(1 for r in results if r.passed)
    return RunResponse(passed=passed_count, total=len(results), results=results)


def normalize(value):
    """Normalize a value for comparison (sort lists, etc.)."""
    if isinstance(value, list):
        return sorted(value)
    return value
