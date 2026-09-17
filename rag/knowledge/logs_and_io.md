# HPC 中的 stdout、stderr 与日志

## stdout

`stdout` 是 Standard Output，即标准输出。

程序正常运行过程中产生的信息通常会输出到 stdout，例如：

```text
程序启动信息
数据加载进度
训练进度
计算结果
普通状态信息
```

例如 Python：

```python
print("Loading dataset...")
```

通常会进入 stdout。

---

## Slurm stdout

在 Slurm 中，可以通过：

```bash
#SBATCH --output=job_%j.out
```

指定 stdout 文件。

其中：

```text
%j
```

会被替换成当前 Job ID。

例如：

```text
Job ID = 18342
```

则可能生成：

```text
job_18342.out
```

---

## stderr

`stderr` 是 Standard Error，即标准错误输出。

程序执行过程中出现的错误、异常和部分警告通常会进入 stderr。

常见内容包括：

```text
Python Traceback
ModuleNotFoundError
FileNotFoundError
PermissionError
CUDA Error
Runtime Error
System Error
```

---

## Slurm stderr

Slurm 中可以通过：

```bash
#SBATCH --error=job_%j.err
```

指定 stderr 文件。

例如：

```text
Job ID = 18342
```

则可能生成：

```text
job_18342.err
```

---

## stdout 和 stderr 的区别

可以粗略理解：

```text
stdout
→ 程序主要输出

stderr
→ 错误和异常信息
```

但是需要注意：

```text
stdout ≠ 一定正确
stderr ≠ 一定是 Root Cause
```

某些程序可能把 Warning 写到 stderr。

也有程序会把错误描述直接打印到 stdout。

因此不能仅仅根据输出通道判断信息的重要程度。

---

## stderr 的诊断价值

stderr 通常是 HPC 故障诊断中非常重要的 Evidence。

例如：

```text
ModuleNotFoundError: No module named 'torch'
```

对：

```text
MISSING_DEPENDENCY
```

是非常强的证据。

又例如：

```text
torch.cuda.OutOfMemoryError: CUDA out of memory
```

对：

```text
CUDA_OUT_OF_MEMORY
```

也是非常强的证据。

---

## 模糊错误信息

某些 stderr 信息存在明显歧义。

例如：

```text
Killed
```

这只能说明进程被终止。

可能原因包括：

```text
CPU 内存耗尽
Scheduler 终止
用户操作
管理员操作
其他系统原因
```

因此：

```text
stderr = Killed
```

不能单独证明：

```text
CPU_OUT_OF_MEMORY
```

应该进一步查看：

```text
Scheduler State
ExitCode
Resource Usage
Requested Memory
MaxRSS
```

---

## Slurm 日志信息

部分 Slurm 系统信息可能由：

```text
slurmstepd
```

写入日志。

常见内容包括：

```text
OOM kill
TIME LIMIT
Job cancellation
Step termination
```

例如：

```text
slurmstepd: error: Detected 1 oom_kill event
```

或者：

```text
JOB 1003 CANCELLED DUE TO TIME LIMIT
```

这些信息具有较高诊断价值。

但仍然建议与：

```text
Scheduler State
Resource Usage
Submit Script
```

结合使用。

---

## Evidence Strength

不同日志信息具有不同诊断强度。

例如：

```text
Killed
```

属于较弱、存在歧义的 Evidence。

而：

```text
torch.cuda.OutOfMemoryError
```

属于相对明确的 Evidence。

因此 ResearchOps 不应该只判断：

```text
有没有日志？
```

还需要判断：

```text
这个 Evidence 有多明确？
是否需要额外证据进行验证？
```

---

## 总结

日志诊断的核心原则是：

```text
Error Message
≠
Root Cause
```

更合理的过程是：

```text
Log Evidence
↓
判断是否存在歧义
↓
获取其他 Evidence
↓
交叉验证
↓
Root Cause Diagnosis
```