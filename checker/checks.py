"""Individual rule-based checks. Each check returns a CheckResult."""

import json
from dataclasses import dataclass


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""


def _parse_json(text):
    """Return (data, error_message). error_message is None when parsing works."""
    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        return None, f"Invalid JSON: {exc.msg} (line {exc.lineno}, column {exc.colno})"


def check_valid_json(text):
    _, error = _parse_json(text)
    if error:
        return CheckResult("valid_json", False, error)
    return CheckResult("valid_json", True)


def check_required_keys(text, keys):
    data, error = _parse_json(text)
    if error:
        return CheckResult("required_keys", False, error)
    if not isinstance(data, dict):
        return CheckResult("required_keys", False, "Top-level JSON value is not an object")
    missing = [key for key in keys if key not in data]
    if missing:
        return CheckResult("required_keys", False, "Missing keys: " + ", ".join(missing))
    return CheckResult("required_keys", True)


def check_max_words(text, max_words):
    count = len(text.split())
    if count > max_words:
        return CheckResult("max_words", False, f"{count} words, limit is {max_words}")
    return CheckResult("max_words", True, f"{count} words")


def check_must_include(text, phrases):
    lowered = text.lower()
    missing = [p for p in phrases if p.lower() not in lowered]
    if missing:
        return CheckResult("must_include", False, "Missing phrases: " + ", ".join(missing))
    return CheckResult("must_include", True)


def check_must_not_include(text, phrases):
    lowered = text.lower()
    found = [p for p in phrases if p.lower() in lowered]
    if found:
        return CheckResult("must_not_include", False, "Forbidden phrases found: " + ", ".join(found))
    return CheckResult("must_not_include", True)
