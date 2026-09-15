# ResearchOps Benchmark Schema

## 1. Benchmark 目标

Benchmark 用于系统评价不同方法对 HPC Job Failure 的诊断能力。

主要比较：

```text
LLM-only
RAG
Active Diagnostic Agent
```

---

## 2. Fault Categories

第一版包含：

```text
CPU_OUT_OF_MEMORY
CUDA_OUT_OF_MEMORY
TIMEOUT
MISSING_DEPENDENCY
WRONG_FILE_PATH
DISK_FULL
PERMISSION_DENIED
PENDING_RESOURCES
```

---

## 3. Difficulty

每个 Case 设置难度：

```text
easy
medium
ambiguous
```

### easy

单个强证据已经可以基本确定故障。

### medium

需要结合两个或多个 Evidence。

### ambiguous

初始证据具有明显歧义，Agent 必须主动查询新的 Evidence 才能可靠诊断。

---

## 4. Case 文件结构

每个 Case 可以包含：

```text
ground_truth.json
scheduler.json
stdout.log
stderr.log
submit.sh
resource_usage.json
environment.json
storage.json
```

并不是所有 Case 都必须包含全部 Evidence。

---

## 5. Ground Truth Schema

每个 Case 至少保存：

```text
case_id
fault_type
root_cause
difficulty
required_evidence
minimal_evidence
expected_tools
```

---

## 6. 字段含义

### required_evidence

能够支持正确诊断的重要 Evidence 集合。

### minimal_evidence

完成可靠诊断所需的最小 Evidence 集合。

### expected_tools

在该 Case 中合理调用的诊断 Tool。

注意：

Agent 不一定必须严格按照唯一顺序调用 Tool。

Evaluation 应允许多个合理的诊断路径。

---

## 7. Example

```json
{
  "case_id": "case_001",
  "fault_type": "CPU_OUT_OF_MEMORY",
  "root_cause": "The job exceeded its requested CPU memory.",
  "difficulty": "ambiguous",
  "required_evidence": [
    "scheduler_state",
    "resource_usage"
  ],
  "minimal_evidence": [
    "scheduler_state",
    "resource_usage"
  ],
  "expected_tools": [
    "get_job_accounting",
    "get_resource_usage"
  ]
}
```

---

## 8. Benchmark 原则

Benchmark 应尽量避免：

```text
错误文本
=
直接写出标准答案
```

例如不能让所有 CPU OOM Case 都包含：

```text
ERROR: CPU_OUT_OF_MEMORY
```

应该加入：

```text
Ambiguous Logs
Distractor Evidence
Multiple Evidence Sources
```

从而真正测试 Agent 的诊断过程。