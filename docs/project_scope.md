# ResearchOps 项目范围定义

## 1. 项目背景

HPC（High Performance Computing，高性能计算）作业失败后，真正的故障原因往往无法通过单一错误信息确定。

用于判断故障原因的信息可能分散在多个位置，包括：

- Slurm 调度系统中的作业状态
- 标准输出 `stdout`
- 标准错误 `stderr`
- CPU、内存、GPU 等资源使用情况
- 作业提交脚本
- 软件运行环境
- 存储空间和用户配额
- HPC 集群相关文档

例如，程序日志中只出现：

```text
Killed
```

并不能直接证明该任务一定发生了内存溢出。

还需要进一步结合 Slurm 状态、实际内存使用情况以及提交脚本中的资源申请配置进行判断。

因此，ResearchOps 的目标不是简单解释错误信息，而是：

> **主动获取与当前故障相关的运行证据，并基于这些证据完成可追溯的 HPC 作业根因诊断。**

---

## 2. 核心任务

### 输入

ResearchOps 第一版的主要输入为：

```text
job_id
```

即一个 HPC 作业的唯一编号。

### 输出

系统最终输出：

```text
fault_type
root_cause
confidence
evidence
recommendation
risk_level
```

含义如下：

- `fault_type`：故障类别
- `root_cause`：故障根本原因
- `confidence`：诊断置信度
- `evidence`：支持诊断结果的证据
- `recommendation`：建议采取的解决措施
- `risk_level`：建议操作的风险等级

---

## 3. MVP 支持范围

第一版 MVP 只支持以下 8 类故障：

1. `CPU_OUT_OF_MEMORY`
   - CPU 内存不足

2. `CUDA_OUT_OF_MEMORY`
   - GPU 显存不足

3. `TIMEOUT`
   - Job 超过申请的最大运行时间

4. `MISSING_DEPENDENCY`
   - 缺少 Python 包、软件模块或其他依赖

5. `WRONG_FILE_PATH`
   - 输入文件不存在或路径错误

6. `DISK_FULL`
   - 磁盘空间不足或用户存储配额超限

7. `PERMISSION_DENIED`
   - 文件或目录权限不足

8. `PENDING_RESOURCES`
   - 因资源不足等原因导致 Job 长时间处于等待状态

在 MVP 完成之前，不增加新的故障类型。

---

## 4. Evidence 证据来源

ResearchOps 第一版计划使用以下证据来源：

```text
scheduler_state
stdout
stderr
resource_usage
submit_script
environment
storage_info
cluster_documentation
```

具体含义：

### scheduler_state

包括：

- Job 当前状态
- Job 历史状态
- ExitCode
- Pending Reason
- Elapsed Time

### stdout

程序运行过程中产生的标准输出。

### stderr

程序运行过程中产生的错误输出。

### resource_usage

包括：

- CPU 使用情况
- 内存使用情况
- MaxRSS
- GPU 显存使用情况
- 实际运行时间

### submit_script

用户提交 Job 时使用的 `sbatch` 脚本，例如：

```bash
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=02:00:00
```

### environment

包括：

- Python 版本
- Conda 环境
- 已安装 Package
- Environment Variables
- module 信息

### storage_info

包括：

- 可用磁盘空间
- 用户 Quota
- 目录状态

### cluster_documentation

包括：

- Slurm 使用说明
- Job State 定义
- 集群资源规则
- 常见错误处理方法

---

## 5. 核心设计原则

### 5.1 基于证据进行诊断

Agent 不能在没有足够证据的情况下直接猜测故障原因。

最终诊断必须能够追溯到真实获得的 Evidence。

---

### 5.2 主动获取证据

系统不应该每次固定读取所有信息。

正确流程应该是：

```text
已有 Evidence
↓
判断是否足够
↓
如果不足
↓
判断缺少什么信息
↓
调用对应 Diagnostic Tool
↓
获得新 Evidence
↓
继续判断
```


---

### 5.3 最小权限原则

诊断阶段默认只允许执行只读操作。

例如：

```text
读取日志
查看 Job 状态
查看资源使用情况
查看环境信息
```

不允许 Agent 随意执行：

```text
删除文件
取消 Job
覆盖脚本
重新提交任务
```

---

### 5.4 结构化诊断

最终结果不能只是一段自由文本。

必须按照统一 Schema 输出：

```text
Fault Type
Root Cause
Confidence
Evidence
Recommendation
Risk Level
```

---

### 5.5 Evaluation First

项目使用统一 Benchmark 对不同方法进行客观评估。

---

## 6. MVP 明确不做的内容

第一版 ResearchOps 不尝试：

- 解决所有 HPC 故障
- 支持所有 HPC Scheduler
- 管理 Kubernetes
- 自动修改任意科研代码
- 允许 LLM 执行任意 Shell 命令
- 建设生产级 HPC 管理平台
- Fine-tuning 大语言模型
- 自动执行高风险系统操作
- 构建复杂 Multi-Agent 系统

这些能力可以在后续版本中逐步增加。

---

## 7. 后续研究方向

后续项目可以进一步研究：

> 主动、基于 Tool 的证据获取是否能够比仅依赖错误日志的 LLM 方法更准确地诊断 HPC 作业故障？

对应英文研究问题：

> Can active, tool-guided evidence acquisition improve HPC failure diagnosis over passive log-based LLM methods?

未来可以比较以下方法：

```text
LLM-only
RAG
Fixed-all-evidence
Active Diagnostic Agent
```

其中：

```text
LLM-only
= 只向模型提供错误日志

RAG
= 错误日志 + HPC 文档检索

Fixed-all-evidence
= 一次性提供所有运行证据

Active Diagnostic Agent
= Agent 自己决定下一步获取什么证据
```