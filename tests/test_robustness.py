import unittest

from ci_doctor.cli import analyze, redact


class RobustnessTests(unittest.TestCase):
    def test_arbitrary_text_is_safe_no_finding(self):
        self.assertEqual(analyze("\x00random text\nnot a build log"), [])

    def test_empty_input_is_safe(self):
        self.assertEqual(analyze(""), [])

    def test_repeated_secret_patterns_are_redacted(self):
        value = "token=secret-one password=secret-two Authorization: Bearer secret-three"
        cleaned = redact(value)
        self.assertNotIn("secret-one", cleaned)
        self.assertNotIn("secret-two", cleaned)
        self.assertNotIn("secret-three", cleaned)


if __name__ == "__main__":
    unittest.main()
