# Releasing Android CI Doctor

## Checklist

1. CI green on supported Python versions.
2. Example-log benchmark matches expected Rule IDs.
3. New rules include a synthetic fixture and regression test.
4. Context output remains redacted.
5. CLI smoke test passes.
6. Update `CHANGELOG.md`, `pyproject.toml` and `CITATION.cff`.
7. Review `docs/TRIAGE_MODEL.md`, `docs/BENCHMARKS.md` and `docs/ROADMAP.md`.

A priority value is a triage hint, not a root-cause probability.
