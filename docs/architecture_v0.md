# ResearchOps 系统架构 v0

## 1. 系统整体流程

ResearchOps 的基本工作流程如下：

```text
                     用户
                      |
                    Job ID
                      |
                      v
              +----------------+
              |  ResearchOps   |
              |      Agent     |
              +----------------+
                      |
                      v
               分析已有 Evidence
                      |
                      v
            +---------------------+
            | 当前证据是否充分？  |
            +---------------------+
                |             |
               否             是
                |             |
                v             v
         选择 Diagnostic Tool    生成诊断
                |
                v
             Tool Call
                |
                v
            Observation
                |
                v
             更新 Evidence
                |
                └──────────→ Agent
```

---

## 2. Agent 层

Agent 主要负责三个任务：

### 判断已有证据

Agent 首先判断目前已经掌握了哪些 Evidence。

### 判断是否需要更多证据

如果当前信息不足以可靠判断 Root Cause，Agent 应继续获取证据。

### 决定调用哪个 Tool

Agent 根据当前故障情况选择最有价值的 Diagnostic Tool。

例如：

```text
发现 Job = OUT_OF_MEMORY
↓
下一步可能调用 get_resource_usage
↓
再读取 submit_script
↓
判断实际内存和申请内存之间的关系
```

---

## 3. Diagnostic Tools

第一版计划实现以下 Tool：

```text
get_job_status
get_job_accounting
read_stdout
read_stderr
get_resource_usage
read_submit_script
get_environment
check_storage
```

### get_job_status

查看 Job 当前状态，例如：

```text
PENDING
RUNNING
COMPLETED
FAILED
```

主要对应 Slurm 中的当前 Job 状态查询。

---

### get_job_accounting

查看 Job 的历史执行信息，例如：

```text
State
ExitCode
Elapsed
```

后续可以模拟 Slurm：

```bash
sacct
```

的部分功能。

---

### read_stdout

读取 Job 的标准输出。

---

### read_stderr

读取 Job 的标准错误输出。

---

### get_resource_usage

获取 Job 的资源使用信息，例如：

```text
CPU Usage
Requested Memory
MaxRSS
GPU Memory
Elapsed Time
```

---

### read_submit_script

读取用户提交 Job 时使用的 `sbatch` 脚本。

例如：

```bash
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=02:00:00
```

Agent 可以比较：

```text
申请资源
vs
实际资源需求
```

---

### get_environment

读取 Job 运行环境，例如：

```text
Python Version
Conda Environment
Installed Packages
module
PATH
```

---

### check_storage

检查：

```text
Available Disk Space
User Quota
Storage Status
```

---

## 4. HPC Knowledge / RAG 层

后续将建立 HPC 文档知识库。

知识内容包括：

```text
Slurm Job State
Exit Code
CPU Memory
GPU Memory
Walltime
Pending Reason
Conda
module
Storage
Linux Permission
```

Agent 可以根据当前问题检索相应文档。

例如：

```text
State = OUT_OF_MEMORY
↓
检索 Memory / Slurm OOM 文档
```

---

## 5. Evidence 层

系统保存 Agent 已经获取的 Evidence。

例如：

```text
E1:
State = OUT_OF_MEMORY

E2:
RequestedMem = 32 GB

E3:
MaxRSS = 31.9 GB

E4:
stderr contains oom-kill
```

最终诊断必须能够引用这些证据。

---

## 6. Structured Diagnosis

最终诊断采用统一格式：

```text
fault_type
root_cause
confidence
evidence
recommendation
risk_level
```

示例：

```text
Fault Type:
CPU_OUT_OF_MEMORY

Root Cause:
申请的 CPU 内存不足。

Confidence:
0.94

Evidence:
1. State = OUT_OF_MEMORY
2. RequestedMem = 32 GB
3. MaxRSS = 31.9 GB
4. stderr 中出现 oom-kill

Recommendation:
提高 Job 的内存申请量。

Risk Level:
SAFE_WRITE
```

---

## 7. Safety Layer

ResearchOps 中的操作按照风险进行分类。

### READ_ONLY

只读取信息，例如：

```text
查看 Job 状态
读取日志
查看资源使用情况
检查环境
```

### SAFE_WRITE

可能生成新内容，但不会直接破坏原始数据，例如：

```text
生成新的 sbatch 脚本
生成修改建议
```

### HIGH_RISK

可能改变真实集群状态，例如：

```text
sbatch
scancel
删除文件
覆盖文件
```

高风险操作未来必须经过：

```text
Safety Policy
+
Human Approval
```

---

## 8. Runtime 层

后续 ResearchOps Runtime 将加入：

```text
Session
Turn
Step
Attempt
Event
Retry
MAX_STEPS
Tool Error Handling
Model Error Handling
```

用于：

```text
Tracing
Debugging
Evaluation
Replay
Failure Recovery
```

---

## 9. Evaluation 层

后续项目将统一运行 Benchmark。

比较：

```text
LLM-only
RAG
Active Diagnostic Agent
```

评价指标包括：

```text
Root Cause Accuracy
Fault Type Accuracy
Evidence Accuracy
Tool Selection Accuracy
Trajectory Accuracy
Average Tool Calls
Average Steps
Latency
Unsafe Action Rate
```

---

## 10. 核心架构原则

ResearchOps 不采用：

```text
Error Message
↓
LLM
↓
Answer
```

而采用：

```text
Incomplete Evidence
↓
Reason
↓
Acquire Evidence
↓
Observation
↓
Reason Again
↓
Evidence-Grounded Diagnosis
```

系统真正的核心能力不是“解释错误”，而是：

> **主动寻找能够支持 Root Cause Diagnosis 的证据。**