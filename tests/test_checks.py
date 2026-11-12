import unittest

from checker import checks


class CheckValidJsonTests(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(checks.check_valid_json('{"a": 1}').passed)

    def test_invalid_reports_position(self):
        result = checks.check_valid_json('{"a": 1,}')
        self.assertFalse(result.passed)
        self.assertIn("line 1", result.detail)


class CheckRequiredKeysTests(unittest.TestCase):
    def test_all_keys_present(self):
        self.assertTrue(checks.check_required_keys('{"a": 1, "b": 2}', ["a", "b"]).passed)

    def test_missing_key_is_named(self):
        result = checks.check_required_keys('{"a": 1}', ["a", "b"])
        self.assertFalse(result.passed)
        self.assertIn("b", result.detail)

    def test_non_object_fails(self):
        result = checks.check_required_keys("[1, 2]", ["a"])
        self.assertFalse(result.passed)

    def test_invalid_json_fails(self):
        self.assertFalse(checks.check_required_keys("not json", ["a"]).passed)


class CheckMaxWordsTests(unittest.TestCase):
    def test_under_limit(self):
        self.assertTrue(checks.check_max_words("one two three", 3).passed)

    def test_over_limit(self):
        result = checks.check_max_words("one two three four", 3)
        self.assertFalse(result.passed)
        self.assertIn("4 words", result.detail)


class CheckPhraseTests(unittest.TestCase):
    def test_must_include_is_case_insensitive(self):
        self.assertTrue(checks.check_must_include("Long BATTERY life", ["battery"]).passed)

    def test_must_include_missing(self):
        self.assertFalse(checks.check_must_include("no match", ["battery"]).passed)

    def test_must_not_include_found(self):
        result = checks.check_must_not_include("As an AI language model, hi", ["as an ai language model"])
        self.assertFalse(result.passed)

    def test_must_not_include_clean(self):
        self.assertTrue(checks.check_must_not_include("clean text", ["forbidden"]).passed)


if __name__ == "__main__":
    unittest.main()
