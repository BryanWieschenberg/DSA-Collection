from fastapi import APIRouter, HTTPException

from problems import PROBLEM_REGISTRY
from schemas import ProblemSummary, ProblemDetail

router = APIRouter(prefix="/problems", tags=["problems"])


@router.get("/", response_model=list[ProblemSummary])
async def list_problems():
    """Return a summary list of all available problems."""
    return [
        ProblemSummary(
            id=p["id"],
            slug=p["slug"],
            title=p["title"],
            difficulty=p["difficulty"],
        )
        for p in sorted(PROBLEM_REGISTRY.values(), key=lambda x: x["id"])
    ]


@router.get("/{slug}", response_model=ProblemDetail)
async def get_problem(slug: str):
    """Return full details for a single problem."""
    problem = PROBLEM_REGISTRY.get(slug)
    if not problem:
        raise HTTPException(status_code=404, detail=f"Problem '{slug}' not found")

    return ProblemDetail(
        id=problem["id"],
        slug=problem["slug"],
        title=problem["title"],
        difficulty=problem["difficulty"],
        description=problem["description"],
        examples=problem["examples"],
        constraints=problem["constraints"],
        starter_code=problem["starter_code"],
    )
