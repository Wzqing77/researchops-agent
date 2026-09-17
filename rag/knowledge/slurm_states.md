# Slurm 作业状态（Slurm Job States）

## PENDING

`PENDING` 表示 Job 已经成功提交到 Slurm，但是还没有开始运行。

常见原因包括：

- `Resources`：当前没有满足资源要求的计算节点
- `Priority`：当前 Job 优先级不足
- `Dependency`：正在等待其他 Job 完成
- `QOS`：受到 Quality of Service 策略限制
- `Reservation`：受到集群资源预留规则限制

需要注意：

```text
PENDING ≠ FAILED
```

Job 处于 `PENDING` 状态，并不表示程序发生了错误。

诊断 PENDING Job 时，应进一步检查：

```text
Pending Reason
Partition
Requested CPU
Requested Memory
Requested GPU
```

---

## RUNNING

`RUNNING` 表示 Slurm 已经为 Job 分配了计算资源，并且 Job 当前正在 Compute Node 上运行。

常见缩写：

```text
R
```

此时可以通过：

```bash
squeue
```

查看 Job 的当前状态。

---

## COMPLETED

`COMPLETED` 通常表示 Job 已经正常完成。

常见缩写：

```text
CD
```

正常完成的 Job 通常会看到：

```text
State = COMPLETED
ExitCode = 0:0
```

其中：

```text
0:0
```

通常表示：

```text
程序退出码 = 0
Signal = 0
```

即程序正常结束，并且没有受到 Signal 强制终止。

---

## FAILED

`FAILED` 表示 Job 执行失败。

常见缩写：

```text
F
```

但是：

```text
State = FAILED
```

本身并不能确定 Root Cause。

导致 FAILED 的原因可能包括：

```text
Python Exception
Missing Dependency
Wrong File Path
Permission Denied
Application Crash
Library Error
```

因此还需要进一步检查：

```text
stderr
ExitCode
Environment
Submit Script
```

---

## OUT_OF_MEMORY

`OUT_OF_MEMORY` 表示 Job 超出了系统允许的内存限制。

这种情况主要涉及：

```text
CPU / System Memory / RAM
```

诊断时常用 Evidence 包括：

```text
State = OUT_OF_MEMORY
RequestedMem
MaxRSS
stderr
Submit Script
```

例如：

```text
RequestedMem = 32 GB
MaxRSS = 31.9 GB
State = OUT_OF_MEMORY
```

这些证据组合起来，可以较强地支持：

```text
CPU_OUT_OF_MEMORY
```

需要注意：

```text
CPU Memory
≠
GPU Memory
```

Slurm 的 `OUT_OF_MEMORY` 不应该直接与 CUDA GPU 显存不足混为一谈。

---

## TIMEOUT

`TIMEOUT` 表示 Job 达到了允许的最大运行时间（Walltime），但是任务还没有完成，因此被 Slurm 终止。

常见证据包括：

```text
State = TIMEOUT
Requested Time
Elapsed Time
Slurm termination message
```

例如：

```text
Requested Time = 01:00:00
Elapsed = 01:00:03
State = TIMEOUT
```

说明 Job 达到了申请的运行时间上限。

---

## CANCELLED

`CANCELLED` 表示 Job 被取消。

可能的原因包括：

```text
用户主动取消
管理员取消
Scheduler Policy
Dependency Failure
其他系统策略
```

因此：

```text
State = CANCELLED
```

只能说明 Job 被取消，不能单独说明为什么被取消。

仍然需要结合其他运行证据判断 Root Cause。

---

## 总结

Slurm Job State 是非常重要的诊断 Evidence，但很多 State 本身并不能独立确定 Root Cause。

ResearchOps 应遵循：

```text
Job State
+
Logs
+
Resource Usage
+
Submit Configuration
↓
Root Cause Diagnosis
```