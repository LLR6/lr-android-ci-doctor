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


if __name__ == "__main__":
    unittest.main()
