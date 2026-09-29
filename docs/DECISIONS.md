# Engineering Decisions

## D1 — Earliest evidence before loudest error

Build failures often cascade. Findings are ordered primarily by the first matching log line.

## D2 — Rules are evidence extractors, not root-cause probabilities

Priority helps triage but is not a confidence score.

## D3 — Context must be redacted too

Adding surrounding lines is only useful if they pass through the same secret-redaction path.

## D4 — Every new rule needs a fixture

Rule coverage grows through small synthetic logs and benchmark expectations rather than ad-hoc regex additions.
