# Contributing

Contributions should improve evidence-first build triage rather than simply add broad regex patterns.

For a new rule:

1. Add a minimal synthetic log fixture.
2. Add expected Rule IDs to the benchmark where appropriate.
3. Test redaction when the surrounding log can contain credentials.
4. Explain why the signal is useful and where it may mislead.
5. Prefer an upstream-cause signal over a downstream symptom.

## Checks

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/evaluate_examples.py benchmarks/examples.json --fail-on-regression
```
