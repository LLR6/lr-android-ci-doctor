import unittest
from ci_doctor.cli import analyze, redact


class TriageTests(unittest.TestCase):
    def test_signing_and_artifact_are_distinct(self):
        log = "Keystore file '/tmp/release.jks' not found\nNo files were found with the provided path: app.apk"
        self.assertEqual([x["id"] for x in analyze(log)], ["SIGN-01", "APK-01"])
        self.assertEqual(analyze(log)[0]["evidence"][0]["line"], 1)

    def test_no_fabricated_success(self):
        self.assertEqual(analyze("BUILD FAILED for an unknown reason"), [])

    def test_redacts_tokens_in_evidence(self):
        self.assertNotIn("secret-value", redact("Authorization: Bearer secret-value"))
        self.assertNotIn("secret-value", redact("storePassword=secret-value"))

    def test_findings_follow_log_order_and_keep_priority(self):
        log = "No files were found with the provided path: app.apk\nKeystore file '/tmp/release.jks' not found"
        findings = analyze(log)
        self.assertEqual([x["id"] for x in findings], ["APK-01", "SIGN-01"])
        self.assertGreater(findings[1]["priority"], findings[0]["priority"])
        self.assertEqual(findings[0]["first_line"], 1)

    def test_context_is_redacted(self):
        log = "token=secret-value\nKeystore file '/tmp/release.jks' not found\nnext line"
        finding = analyze(log, context=1)[0]
        joined = str(finding["evidence"][0]["context"])
        self.assertNotIn("secret-value", joined)
        self.assertIn("next line", joined)


if __name__ == "__main__":
    unittest.main()
