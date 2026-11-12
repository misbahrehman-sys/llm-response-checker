"""Command line interface: python -m checker.cli --rubric R.json --response X.txt"""

import argparse
import json
import sys

from .evaluate import evaluate


def build_parser():
    parser = argparse.ArgumentParser(
        description="Check an LLM response against a rubric of simple rules."
    )
    parser.add_argument("--rubric", required=True, help="Path to rubric JSON file")
    parser.add_argument("--response", required=True, help="Path to the response text file")
    parser.add_argument("--json", action="store_true", help="Print the result as JSON")
    return parser


def format_report(result):
    lines = [f"Rubric: {result['rubric']}"]
    for check in result["checks"]:
        status = "PASS" if check["passed"] else "FAIL"
        detail = f" - {check['detail']}" if check["detail"] else ""
        lines.append(f"  [{status}] {check['name']}{detail}")
    lines.append(f"Score: {result['score']:.2f} ({'PASSED' if result['passed'] else 'FAILED'})")
    return "\n".join(lines)


def main(argv=None):
    args = build_parser().parse_args(argv)
    with open(args.rubric, encoding="utf-8") as handle:
        rubric = json.load(handle)
    with open(args.response, encoding="utf-8") as handle:
        response_text = handle.read()

    result = evaluate(response_text, rubric)
    print(json.dumps(result, indent=2) if args.json else format_report(result))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
