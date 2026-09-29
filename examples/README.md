# Example logs

All files in this directory are synthetic and contain no real credentials.

| File | Expected signal |
|---|---|
| `build.log` | signing + artifact path findings |
| `jdk-mismatch.log` | `JDK-01` |
| `dependency-resolution.log` | `GRADLE-01` |
| `test-failure.log` | `TEST-01` |

Try:

```bash
android-ci-doctor examples/jdk-mismatch.log --context 1
android-ci-doctor examples/dependency-resolution.log --format json
android-ci-doctor examples/test-failure.log --fail-on-findings
```

The examples are intentionally small so the expected finding can be checked by eye.
