# Roadmap

## Near term

- Add AGP/Kotlin compatibility fixtures.
- Add multi-line `Caused by` chain extraction.
- Separate upstream-cause findings from downstream symptoms.
- Add clean-log negative fixtures from more build phases.

## Medium term

- Build causal chains between findings.
- Add structured environment metadata extraction.
- Support Gradle configuration-cache and dependency-lock diagnostics.

## Non-goals

No automatic mutation of Gradle files, signing credentials or CI secrets.
