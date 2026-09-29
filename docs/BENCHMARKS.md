# Benchmarks

Fixture index: `benchmarks/examples.json`

Synthetic logs currently cover:

- release signing failure;
- missing APK artifact;
- JDK / class-version mismatch;
- dependency resolution failure;
- unit-test failure.

Run:

```bash
python scripts/evaluate_examples.py benchmarks/examples.json --fail-on-regression
```

The evaluator compares ordered observed Rule IDs with expected Rule IDs. This guards both missed matches and accidental new matches on known fixtures.

The fixture set is intentionally synthetic and credential-free.
