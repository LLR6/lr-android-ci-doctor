# Known Failure Modes

- A downstream artifact error hides the earlier root signal.
  - Findings preserve first evidence line.
- A regex matches a harmless line.
  - Add a synthetic negative fixture.
- A new rule collides with an old Rule ID.
  - Rule IDs are compatibility-sensitive.
- Context leaks a credential.
  - All context must pass redaction before output.
- No rule matches a failing build.
  - Report no finding; never claim the build succeeded.
- Log format changes across AGP/Gradle versions.
  - Add versioned synthetic fixtures before broadening patterns.
