# Android CI Doctor

<!-- LR-LAB-CHROME:START -->
<p align="center">
  <a href="https://github.com/LLR6"><img alt="LR Lab" src="https://img.shields.io/badge/LR_LAB-0x4C52-0D1117?style=for-the-badge&logo=github&logoColor=white"></a>
  <img alt="DEV TOOL" src="https://img.shields.io/badge/DEV_TOOL-3B82F6?style=for-the-badge">
</p>
<p align="center"><strong>Make build failures legible.</strong><br><sub>Local Android / Gradle / CI log diagnosis</sub></p>
<p align="center"><a href="https://github.com/LLR6/lr-android-ci-doctor/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/LLR6/lr-android-ci-doctor?style=flat-square&logo=github&label=stars"></a>
  <img alt="Last commit" src="https://img.shields.io/github/last-commit/LLR6/lr-android-ci-doctor?style=flat-square"> <img alt="Maintained" src="https://img.shields.io/badge/status-active-success?style=flat-square"></p>
<p align="center"><a href="https://github.com/LLR6">Profile</a> · <a href="https://github.com/LLR6?tab=repositories">All projects</a> · <a href="https://github.com/LLR6/lr-android-ci-doctor/issues">Issues</a></p>
<!-- LR-LAB-CHROME:END -->

<!-- LR-FAMILY-NAV:START -->
<p align="center"><a href="#30-秒试玩">30-second demo</a> · <a href="./examples">Examples</a> · <a href="./src">Source</a> · <a href="./tests">Tests</a></p>
<!-- LR-FAMILY-NAV:END -->


<p align="center"><img src="./docs/media/social-preview.svg" alt="Android CI Doctor — Make build failures legible" width="100%"></p>

<p align="center"><img src="./docs/media/cli-demo.gif" alt="真实示例：读取构建日志、定位签名错误与 APK 产物路径" width="100%"></p>
<p align="center"><sub>示例来自仓库自带的 build.log；画面为便于阅读的节选。</sub></p>

<p align="center"><strong>构建失败时，先找到哪一行、为什么、下一步查什么。</strong></p>
<p align="center">本地分析 Android / Gradle / GitHub Actions 日志；保留证据行号，不上传日志。</p>
<p align="center"><a href="#30-秒看懂">30 秒看懂</a> · <a href="#5-分钟开始">5 分钟开始</a> · <a href="#能力与边界">能力与边界</a></p>
<p align="center"><img alt="Test" src="https://github.com/LLR6/lr-android-ci-doctor/actions/workflows/test.yml/badge.svg"> <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-blue"> <img alt="MIT" src="https://img.shields.io/badge/license-MIT-green"> <img alt="Version 0.1.0" src="https://img.shields.io/badge/version-0.1.0-8b5cf6"></p>

## 30 秒看懂

当 CI 只给你几千行日志时，直接搜索 `Keystore file not found` 或 `No files were found with the provided path` 往往还要手工猜根因。这个工具把常见信号整理成 **规则 ID → 原日志行号 → 去敏证据 → 检查建议**。

```text
本地日志 → 规则扫描 → 带行号的证据 → Markdown / JSON
```

## 30 秒试玩

在仓库根目录运行，无需模型 API：

```bash
python -m pip install -e .
android-ci-doctor examples/build.log
```

示例输出节选（来自 `examples/build.log`）：

```text
SIGN-01 · 签名配置缺失
L3: Keystore file '/home/runner/work/app/release.jks' not found

APK-01 · 产物路径不匹配
L4: No files were found with the provided path: app/build/outputs/apk/release/*.apk
```

## 三个值得看的点

- **证据回溯**：规则命中保留原行号，让你能回到完整日志核对上下文。
- **本地与去敏**：离线运行，输出遮盖常见 Token 与口令；公开前仍需人工检查。
- **接入 CI**：`--format json` 方便脚本处理；`--fail-on-findings` 命中时退出码为 2。

## 5 分钟开始

要求 Python 3.10+。

```bash
git clone https://github.com/LLR6/lr-android-ci-doctor.git
cd lr-android-ci-doctor
python -m pip install -e .
android-ci-doctor examples/build.log
android-ci-doctor examples/build.log --format json --fail-on-findings
cat examples/build.log | android-ci-doctor -
```

最后一条是 Linux / macOS 的管道示例；Windows 可直接传入文件路径。`--fail-on-findings` 的退出码 2 表示命中线索，并不代表程序崩溃。

## 能力与边界

识别 JDK、SDK、依赖、签名、缓存、测试与 APK 路径等常见失败信号。**规则匹配不是自动修复，也不能替代对最早失败信息的检查**。根因与连带错误可能同时命中；不要把每条命中都当作独立故障。脱敏不是安全边界；不会执行日志里的命令，也不会访问网络。

## 参与 / Help Wanted

欢迎提交**已经去敏**的失败片段，并标注预期规则和误报反例。下一步可做 Gradle 版本矩阵核验、因果链排序与 SARIF 输出。验证代码：`python -m unittest discover -s tests`。

作者：LLR6 · MIT License

<!-- LR-RELATED:START -->
### Related LR Lab projects
- [LR-Tablet](https://github.com/LLR6/LR-Tablet) — Android tablet project with reproducible CI builds.
- [CTF Tracebook](https://github.com/LLR6/lr-ctf-tracebook) — another small evidence-first local CLI tool.
- [LR-Agent](https://github.com/LLR6/LR-agent) — broader automation and reliability experiments.
<!-- LR-RELATED:END -->

<!-- LR-LAB-FOOTER:START -->
---
<p align="center"><sub>Part of <a href="https://github.com/LLR6">LR Lab</a> · Security × AI × Android × Automation</sub><br><sub>Build things that are useful, inspectable, and reproducible.</sub></p>
<!-- LR-LAB-FOOTER:END -->

