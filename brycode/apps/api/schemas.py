from __future__ import annotations
from pydantic import BaseModel


# ── Problem models ──────────────────────────────────────────────

class Example(BaseModel):
    id: int
    input: str
    output: str
    explanation: str | None = None


class TestCase(BaseModel):
    input: str
    expected: str


class ProblemSummary(BaseModel):
    id: int
    slug: str
    title: str
    difficulty: str


class ProblemDetail(BaseModel):
    id: int
    slug: str
    title: str
    difficulty: str
    description: str
    examples: list[Example]
    constraints: list[str]
    starter_code: str


# ── Runner models ───────────────────────────────────────────────

class RunRequest(BaseModel):
    slug: str
    code: str
    test_indices: list[int] | None = None


class TestCaseResult(BaseModel):
    index: int
    input: str
    expected: str
    actual: str | None = None
    passed: bool
    error: str | None = None
    stdout: str | None = None


class RunResponse(BaseModel):
    passed: int
    total: int
    results: list[TestCaseResult]
