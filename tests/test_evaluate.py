import json
import os
import unittest

from checker.cli import main
from checker.evaluate import evaluate

EXAMPLES = os.path.join(os.path.dirname(__file__), "..", "examples")


def read(name):
    with open(os.path.join(EXAMPLES, name), encoding="utf-8") as handle:
        return handle.read()


class EvaluateTests(unittest.TestCase):
    def setUp(self):
        self.rubric = json.loads(read("rubric.json"))

    def test_good_response_passes_everything(self):
        result = evaluate(read("response_good.json"), self.rubric)
        self.assertTrue(result["passed"])
        self.assertEqual(result["score"], 1.0)

    def test_bad_response_fails_expected_checks(self):
        result = evaluate(read("response_bad.json"), self.rubric)
        failed = {c["name"] for c in result["checks"] if not c["passed"]}
        self.assertFalse(result["passed"])
        self.assertEqual(failed, {"required_keys", "must_include", "must_not_include"})

    def test_unknown_check_raises(self):
        with self.assertRaises(ValueError):
            evaluate("{}", {"checks": {"not_a_check": True}})

    def test_false_boolean_check_is_skipped(self):
        result = evaluate("not json", {"checks": {"valid_json": False}})
        self.assertEqual(result["checks"], [])
        self.assertTrue(result["passed"])


class CliTests(unittest.TestCase):
    def test_exit_code_zero_for_good_response(self):
        code = main(["--rubric", os.path.join(EXAMPLES, "rubric.json"),
                     "--response", os.path.join(EXAMPLES, "response_good.json")])
        self.assertEqual(code, 0)

    def test_exit_code_one_for_bad_response(self):
        code = main(["--rubric", os.path.join(EXAMPLES, "rubric.json"),
                     "--response", os.path.join(EXAMPLES, "response_bad.json")])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
