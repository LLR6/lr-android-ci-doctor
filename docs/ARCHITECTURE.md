# Android CI Doctor Architecture

```text
local build log
      ↓
line-oriented rules
      ↓
evidence extraction
      ↓
redaction
      ↓
finding enrichment
(priority / first_line / occurrences / context)
      ↓
Markdown / JSON report
      ↓
fixture benchmark in CI
```

## Design principle

The tool narrows a long log into auditable evidence. It does not claim to infer a guaranteed root cause.

## Ordering

Earliest strong evidence is favored because later failures are often cascading symptoms.

## Safety invariant

Evidence and optional context are redacted before they are written to reports.

## Non-goals

- editing Gradle files automatically;
- replacing signing configuration;
- uploading logs;
- treating a rule priority as a probability.
