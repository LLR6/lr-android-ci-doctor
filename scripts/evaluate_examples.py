import argparse
import json
from pathlib import Path

from ci_doctor.cli import analyze


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate Android CI Doctor example fixtures")
    parser.add_argument("benchmark", type=Path)
    parser.add_argument("--examples", type=Path, default=Path("examples"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fail-on-regression", action="store_true")
    args = parser.parse_args()

    data = json.loads(args.benchmark.read_text(encoding="utf-8"))
    if data.get("schema") != "lr-ci-doctor-example-benchmark/v1":
        parser.error("unsupported benchmark schema")

    results = []
    passed = 0
    for case in data.get("cases", []):
        path = args.examples / case["file"]
        found = [item["id"] for item in analyze(path.read_text(encoding="utf-8", errors="replace"))]
        expected = list(case["expected"])
        ok = found == expected
        passed += int(ok)
        results.append({"file": case["file"], "expected": expected, "observed": found, "passed": ok})

    total = len(results)
    report = {
        "schema": "lr-ci-doctor-example-report/v1",
        "passed": passed,
        "total": total,
        "accuracy": round(passed / total, 4) if total else 0.0,
        "results": results,
    }
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 2 if args.fail_on_regression and passed != total else 0


if __name__ == "__main__":
    raise SystemExit(main())
