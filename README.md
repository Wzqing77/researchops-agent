# ResearchOps

> 基于多源运行证据的 HPC 作业智能诊断 Agent

ResearchOps 是一个面向 HPC（高性能计算）场景的智能故障诊断 Agent。

与仅根据错误日志进行解释的普通大语言模型不同，ResearchOps 会主动从调度系统状态、运行日志、资源使用情况、提交脚本、软件环境、存储状态以及 HPC 文档中获取证据，并基于这些证据完成结构化的 Root Cause Diagnosis。

> 当前状态：MVP 开发中

---

## 为什么要做 ResearchOps？

HPC 作业失败后，真正的故障原因往往无法通过一条错误信息确定。

例如：

```text
Killed
```

单独看到这条信息，并不能直接判断 Job 是否发生了内存溢出。

还需要进一步查看：

```text
Slurm Job State
Resource Usage
stderr
Submit Script
```

例如：

```text
State = OUT_OF_MEMORY
RequestedMem = 32 GB
MaxRSS = 31.9 GB
stderr = oom-kill detected
```

结合这些证据后，才能更加可靠地判断：

```text
Root Cause = CPU Memory Exhaustion
```

因此 ResearchOps 关注的问题不是：

> 大模型能否解释 HPC 报错？

而是：

> Agent 能否在信息不完整的情况下，主动获取有价值的运行证据，并基于这些证据完成可靠的 HPC 根因诊断？

---

## MVP 故障范围

第一版支持以下 8 类常见 HPC 故障：

```text
CPU Out-of-Memory
CUDA Out-of-Memory
TIMEOUT
Missing Dependency
Wrong File Path
Disk Full / Quota Exceeded
Permission Denied
Pending Resources
```

---

## 系统工作流程

```text
Job ID
  ↓
ResearchOps Agent
  ↓
分析当前 Evidence
  ↓
Evidence 是否充分？
  ↓
如果不足
  ↓
调用 Diagnostic Tool
  ↓
获得新的 Evidence
  ↓
继续 Reasoning
  ↓
Structured Root Cause Diagnosis
```

---

## Evidence 来源

ResearchOps 计划使用：

```text
Scheduler State
stdout
stderr
Resource Usage
Submit Script
Environment
Storage Information
HPC Documentation
```

---

## 最终输出

系统最终输出：

```text
Fault Type
Root Cause
Confidence
Evidence
Recommendation
Risk Level
```

---

## MVP 技术栈

计划使用：

```text
Python
DeepSeek
LangGraph
Tool Calling
RAG
Pydantic
Agent Evaluation
```

技术只有在项目真正使用后才会加入列表。

---

## Evaluation

项目将使用统一 Benchmark 进行评估，而不是只展示少量 Demo。

计划比较：

```text
LLM-only

RAG-based Diagnosis

Active Tool-using Diagnostic Agent
```

主要评价指标：

```text
Root Cause Accuracy
Fault Type Accuracy
Evidence Accuracy
Tool Selection Accuracy
Average Tool Calls
Average Diagnostic Steps
Latency
Unsafe Action Rate
```

---



## 后续研究方向



> 主动、基于 Tool 的 Evidence Acquisition 是否能够提高 LLM 在 HPC 故障根因诊断中的准确性和诊断效率？

未来可能比较：

```text
LLM-only
RAG
Fixed-all-evidence
Active Diagnostic Agent
```