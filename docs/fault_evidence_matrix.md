# ResearchOps Fault × Evidence Matrix

## 1. 文档目的

本文档用于定义 ResearchOps MVP 中 8 类 HPC 故障与不同 Evidence Source 之间的关系。

该矩阵将用于：

- Benchmark Case 设计
- Diagnostic Tool 设计
- Agent Prompt 设计
- Evaluation Ground Truth 设计

---

## 2. Evidence 类型

第一版 ResearchOps 使用：

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

---

## 3. Fault × Evidence Matrix

| Fault Type | Scheduler | stderr | Resource Usage | Submit Script | Environment | Storage | Documentation |
|---|---|---|---|---|---|---|---|
| CPU_OUT_OF_MEMORY | 高 | 中 | 高 | 高 | 低 | 低 | 中 |
| CUDA_OUT_OF_MEMORY | 中 | 高 | 高 | 中 | 中 | 低 | 中 |
| TIMEOUT | 高 | 中 | 高 | 高 | 低 | 低 | 中 |
| MISSING_DEPENDENCY | 低 | 高 | 低 | 中 | 高 | 低 | 中 |
| WRONG_FILE_PATH | 低 | 高 | 低 | 中 | 中 | 中 | 低 |
| DISK_FULL | 低 | 高 | 低 | 低 | 低 | 高 | 中 |
| PERMISSION_DENIED | 低 | 高 | 低 | 中 | 低 | 中 | 中 |
| PENDING_RESOURCES | 高 | 低 | 中 | 高 | 低 | 低 | 中 |

其中：

- 高：通常属于关键诊断证据
- 中：在部分 Case 中有帮助
- 低：通常不是首要证据

---

## 4. CPU_OUT_OF_MEMORY

典型现象：

```text
OUT_OF_MEMORY
oom-kill
Killed
```

主要 Evidence：

```text
scheduler_state
resource_usage
submit_script
stderr
```

典型 Evidence Chain：

```text
State = OUT_OF_MEMORY
+
RequestedMem = 32 GB
+
MaxRSS ≈ 32 GB
+
stderr contains oom-kill
```

注意：

```text
stderr = Killed
```

单独不能作为 CPU OOM 的充分证据。

---

## 5. CUDA_OUT_OF_MEMORY

典型错误：

```text
CUDA out of memory
torch.cuda.OutOfMemoryError
```

主要 Evidence：

```text
stderr
GPU resource usage
submit_script
environment
```

需要重点区分：

```text
CPU Memory
≠
GPU Memory
```


## 6. TIMEOUT

典型 Evidence：

```text
State = TIMEOUT
Elapsed ≈ Requested Time
```

主要 Evidence：

```text
scheduler_state
resource_usage
submit_script
```

例如：

```text
Requested Time = 01:00:00
Elapsed = 01:00:03
State = TIMEOUT
```

---

## 7. MISSING_DEPENDENCY

典型错误：

```text
ModuleNotFoundError
command not found
shared library not found
```

主要 Evidence：

```text
stderr
environment
submit_script
```

需要检查：

```text
Python Environment
Conda Environment
module
PATH
Installed Packages
```

---

## 8. WRONG_FILE_PATH

典型错误：

```text
FileNotFoundError
No such file or directory
```

主要 Evidence：

```text
stderr
submit_script
environment
storage_info
```

不能看到 `FileNotFoundError` 就立即判断一定是用户把路径写错。

也可能涉及：

```text
Working Directory
Filesystem Mount
Environment Variable
```

---

## 9. DISK_FULL

典型错误：

```text
No space left on device
Disk quota exceeded
```

主要 Evidence：

```text
stderr
storage_info
```

例如：

```text
Disk Usage = 100%
```

或者：

```text
User Quota Exceeded
```

---

## 10. PERMISSION_DENIED

典型错误：

```text
Permission denied
Operation not permitted
```

主要 Evidence：

```text
stderr
filesystem permission
submit_script
```

后续可以通过只读 Tool 检查：

```text
ownership
file mode
directory permission
```

---

## 11. PENDING_RESOURCES

典型状态：

```text
State = PENDING
```

但：

```text
PENDING
```

本身并不表示 Job 出错。

需要进一步查看：

```text
Pending Reason
Requested Resources
Partition
```

例如：

```text
State = PENDING
Reason = Resources
GPU Requested = 4
```

说明 Job 很可能只是正在等待满足资源要求的 Node。

---

## 12. Benchmark 设计原则

Benchmark 不应该让所有 Case 都能够通过一个明显的错误字符串完成判断。

应该包含：

```text
Easy
Medium
Ambiguous
```

并允许存在：

```text
Distractor Evidence
```

目标是测试 Agent 是否真正能够：

```text
判断 Evidence 是否充分
↓
选择下一步 Tool
↓
获得关键 Evidence
↓
形成 Root Cause Diagnosis
```