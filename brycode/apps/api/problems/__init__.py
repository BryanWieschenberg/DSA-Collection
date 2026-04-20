"""Problem registry — import all problem modules here."""

from problems.two_sum import TWO_SUM

# Master list of all problems, keyed by slug
PROBLEM_REGISTRY: dict[str, dict] = {
    p["slug"]: p for p in [TWO_SUM]
}
