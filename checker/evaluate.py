"""Run a rubric (a set of checks) against one response."""

from . import checks

SUPPORTED_CHECKS = {
    "valid_json": lambda text, value: checks.check_valid_json(text),
    "required_keys": checks.check_required_keys,
    "max_words": checks.check_max_words,
    "must_include": checks.check_must_include,
    "must_not_include": checks.check_must_not_include,
}


def evaluate(response_text, rubric):
    """Evaluate response_text against rubric and return a result dictionary.

    rubric looks like:
        {"name": "My task", "checks": {"valid_json": true, "max_words": 80}}
    A check set to false (for boolean checks) is skipped.
    """
    configured = rubric.get("checks", {})
    unknown = [name for name in configured if name not in SUPPORTED_CHECKS]
    if unknown:
        raise ValueError("Unknown check(s) in rubric: " + ", ".join(unknown))

    results = []
    for name, value in configured.items():
        if value is False:
            continue
        results.append(SUPPORTED_CHECKS[name](response_text, value))

    total = len(results)
    passed = sum(1 for r in results if r.passed)
    return {
        "rubric": rubric.get("name", "unnamed rubric"),
        "score": round(passed / total, 2) if total else 1.0,
        "passed": passed == total,
        "checks": [
            {"name": r.name, "passed": r.passed, "detail": r.detail} for r in results
        ],
    }
