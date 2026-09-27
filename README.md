# Android CI Doctor 🩺

> 把一大段 Android / Gradle / GitHub Actions 构建日志压缩成**带行号的故障线索**。本地运行、无模型 API、无日志上传。

**搜这个问题的人通常刚遇到：** `Keystore file not found`、`No files were found with the provided path`、`Unsupported class file major version`。这个工具把它们分别定位到签名、产物上传、JDK 兼容性，并保留原日志证据。

```bash
python -m pip install -e .
android-ci-doctor examples/build.log
android-ci-doctor examples/build.log --format json --fail-on-findings
```

示例会命中 `SIGN-01` 和 `APK-01`，显示原始行号、脱敏后的日志片段和下一步检查建议。`--fail-on-findings` 在命中时退出码为 2，方便放在 CI 中做检查。也能通过 `cat build.log | android-ci-doctor -` 使用。

## 设计边界

- 只做规则匹配，**不声称自动修复**或诊断所有 Gradle 失败；同一日志可能有根因和连带错误，建议从最早失败处查起。
- 自动遮盖常见 Bearer Token、口令赋值和 GitHub token；脱敏不是安全边界，公开日志前仍需人工检查。
- 不执行日志中的命令，不访问网络。可用 `python -m unittest discover -s tests` 运行测试。

## 适合参与的改进

欢迎提交**已经去敏**的失败片段、预期规则和实际结果。新增规则请给一段会命中的样例和一段不应误报的反例。路线图：Gradle 版本矩阵核验、因果链排序、SARIF 输出。

作者：LLR6 · MIT License
