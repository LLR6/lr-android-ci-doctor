import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from importlib.metadata import PackageNotFoundError, version

def package_version():
    try:
        return version("lr-android-ci-doctor")
    except PackageNotFoundError:
        return "dev"



@dataclass(frozen=True)
class Rule:
    code: str
    title: str
    pattern: str
    fix: str


PRIORITY = {
    "SIGN-02": 100,
    "SIGN-01": 95,
    "JDK-01": 90,
    "SDK-01": 85,
    "GRADLE-01": 75,
    "TEST-01": 70,
    "CACHE-01": 55,
    "APK-01": 45,
}

RULES = (
    Rule("JDK-01", "Java 与 Gradle 不兼容", r"Unsupported class file major version|invalid source release|requires Java (\d+)", "核对 Gradle、Android Gradle Plugin 与 JDK 版本矩阵，在 CI 中固定 setup-java 版本。"),
    Rule("SDK-01", "Android SDK 缺失", r"SDK location not found|Failed to find (?:Build Tools|Platform SDK)|licenses have not been accepted", "安装项目要求的 SDK/Build Tools，并在 CI 中确认 ANDROID_HOME 与 licenses。"),
    Rule("GRADLE-01", "依赖无法解析", r"Could not resolve|Could not find .*?:.*?:|No matching variant of", "检查仓库源、版本、网络及 variant 属性；优先查看日志中的首个依赖坐标。"),
    Rule("SIGN-01", "签名配置缺失", r"Keystore file .* not found|No signing config|Missing keystore|Cannot recover key", "确认签名文件和密钥仅通过 CI Secrets 注入，核对路径与 alias；不要将密钥写入仓库。"),
    Rule("SIGN-02", "签名口令或别名错误", r"Keystore was tampered with|password was incorrect|No key with alias|Alias .* does not exist", "检查 keystore 与 alias 是否匹配，并在安全环境核对口令；不要把真实口令贴到 Issue。"),
    Rule("CACHE-01", "Gradle 缓存或锁异常", r"Timeout waiting to lock|Could not lock|corrupt (?:zip|cache)|ZipException", "先重跑一次确认是否瞬时故障；再定位具体缓存，避免直接清空所有构建缓存。"),
    Rule("TEST-01", "测试失败", r"There were failing tests|Tests failed|Execution failed for task '.*[Tt]est.*'", "打开测试报告定位首个失败用例，保存堆栈与输入，再修复代码或测试环境。"),
    Rule("APK-01", "产物路径不匹配", r"No files were found with the provided path|Artifact .* not found|Unable to find.*\.apk", "检查 assemble 任务、变体名与实际 APK/AAB 路径，再修改上传 artifact 的 glob。"),
)


def redact(value: str) -> str:
    value = re.sub(r"(?i)(authorization\s*[:=]\s*bearer\s+)\S+", r"\1[REDACTED]", value)
    value = re.sub(r"(?i)\b((?:api[_-]?key|token|password|storePassword|keyPassword)\s*[:=]\s*)\S+", r"\1[REDACTED]", value)
    return re.sub(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b", "[REDACTED]", value)


def analyze(log: str, context: int = 0) -> list[dict]:
    if context < 0:
        raise ValueError("context must be >= 0")

    lines = log.splitlines()
    findings = []
    for rule in RULES:
        matches = [(i, redact(line.strip())) for i, line in enumerate(lines, 1) if re.search(rule.pattern, line, re.I)]
        if not matches:
            continue

        evidence = []
        for line_no, text in matches[:3]:
            item = {"line": line_no, "text": text[:400]}
            if context:
                start = max(1, line_no - context)
                end = min(len(lines), line_no + context)
                item["context"] = [
                    {"line": n, "text": redact(lines[n - 1].strip())[:400]}
                    for n in range(start, end + 1)
                ]
            evidence.append(item)

        findings.append({
            "id": rule.code,
            "title": rule.title,
            "fix": rule.fix,
            "priority": PRIORITY.get(rule.code, 50),
            "first_line": matches[0][0],
            "evidence": evidence,
            "occurrences": len(matches),
        })

    return sorted(findings, key=lambda x: (x["first_line"], -x["priority"], x["id"]))


def markdown(path: str, findings: list[dict]) -> str:
    out = ["# Android CI Doctor", "", f"输入：`{Path(path).name}`", ""]
    if not findings:
        out += ["未命中内置规则。请检查日志中最早的 `Caused by:` 或 `FAILURE:`；这不代表构建成功。"]
    for item in findings:
        out += [
            f"## {item['id']} · {item['title']}",
            "",
            f"- priority: **{item['priority']}**",
            f"- first evidence: **L{item['first_line']}**",
            f"- occurrences: **{item['occurrences']}**",
            "",
            f"建议：{item['fix']}",
            "",
            "证据：",
        ]
        for e in item["evidence"]:
            out.append(f"- L{e['line']}: `{e['text'].replace('`', '’')}`")
            if e.get("context"):
                for row in e["context"]:
                    prefix = ">" if row["line"] == e["line"] else " "
                    out.append(f"  - {prefix} L{row['line']}: `{row['text'].replace('`', '’')}`")
        out += [""]
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="离线分析 Android / Gradle CI 构建日志")
    parser.add_argument("--version", action="version", version=f"%(prog)s {package_version()}")
    parser.add_argument("log", help="UTF-8 日志路径；使用 - 从 stdin 读取")
    parser.add_argument("--format", choices=("md", "json"), default="md")
    parser.add_argument("--fail-on-findings", action="store_true", help="发现规则命中时返回退出码 2")
    parser.add_argument("--context", type=int, default=0, help="每条证据附带前后 N 行上下文")
    args = parser.parse_args(argv)
    try:
        log = sys.stdin.read() if args.log == "-" else Path(args.log).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        parser.error(str(exc))
    try:
        findings = analyze(log, args.context)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps({"schema": "lr-ci-doctor/v1", "findings": findings}, ensure_ascii=False, indent=2)
          if args.format == "json" else markdown(args.log, findings), end="")
    return 2 if args.fail_on_findings and findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
