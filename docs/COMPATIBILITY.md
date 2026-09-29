# Compatibility

## Runtime

- Python: **3.10+**
- CI target: **3.10 / 3.11 / 3.12**
- CLI: `android-ci-doctor`

## Input

Plain-text Android / Gradle / GitHub Actions logs.

## Output

Markdown and JSON findings preserve:

- Rule ID
- first evidence line
- occurrence count
- redacted evidence/context

Rule IDs are compatibility-sensitive identifiers. Existing Rule IDs should not be reused for unrelated failure modes.
