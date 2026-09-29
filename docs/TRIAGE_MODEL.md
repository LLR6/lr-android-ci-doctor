# Triage Model

Android CI Doctor 的目标不是“猜一个根因”，而是把几千行构建日志缩小为可以人工核对的证据集合。

## Ordering

v0.2 的 finding 同时包含：

- `first_line`：第一次命中的日志行；
- `occurrences`：同规则命中次数；
- `priority`：规则级排查优先度；
- `evidence`：去敏后的证据。

输出优先按 **日志首次出现位置** 排序，再用 priority 处理同位置冲突。

原因是构建日志中后续错误常常只是前面失败的连锁结果。最早出现的强信号通常更值得先看。

## Priority

Priority 是排查顺序提示，不是根因置信度。

例如签名文件不存在通常比“最终找不到 APK artifact”更靠近因果链上游，但这并不意味着每次签名错误都一定是唯一根因。

## Context

`--context N` 会给每条证据保留前后 N 行。

上下文同样经过 token / password / GitHub token 脱敏，再进入 Markdown 或 JSON 输出。

这对下面情况有帮助：

- Gradle 打印多行异常；
- `Caused by` 与任务名分开；
- artifact 错误之前有实际 build failure；
- signing 错误附近包含 variant 信息。

## Non-goals

Android CI Doctor 不会：

- 自动修改 Gradle 文件；
- 自动替换签名配置；
- 上传日志；
- 把“未命中规则”解释为构建成功；
- 把 priority 当成概率。

长期方向是做因果链排序，而不是不断堆更多正则。
