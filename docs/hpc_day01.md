# HPC Day 01

## 1. What is HPC?

高性能计算，包含很多计算节点、高速网络、共享存储、任务调度系统

其目的是利用大量计算资源完成普通单台计算机难以高效完成的大规模计算任务

## 2. Login Node vs Compute Node

### Login Node

Login Node = 用户登录集群后的入口节点

主要用于：文件管理、代码编辑、环境准备、编译、提交 Job、查看 Job

Login Node 通常由很多用户共同使用，因此一般不应该直接在上面执行长时间、大规模计算任务

### Compute Node

Compute Node 是真正执行计算任务的节点

Compute Node 通常提供：

```text
CPU
Memory
GPU
```

等计算资源。

---

## 3. 什么是 Scheduler？

HPC 集群中的计算资源通常由多个用户共同使用。

Scheduler 负责：

```text
任务排队
资源分配
任务调度
```

例如用户可以申请：

```text
CPU = 8
Memory = 32 GB
GPU = 1
Time = 4 hours
```

Scheduler 根据当前集群资源情况决定 Job 什么时候运行以及在哪个 Compute Node 上运行。

---

## 4. What does Slurm do?

Slurm 是 HPC 中常见的任务调度系统。

Job Scheduling + Resource Allocation + Job State Management

## 5. What is a Job?

Job 是用户提交给 Scheduler 的一次计算任务

## 6. sbatch vs squeue vs sacct

sbatch用于提交任务和需求提出

squeue是用于查看job现在的任务状态

sacct是用于查看job的历史和资源记录,即使 Job 已经结束，也可以通过 `sacct` 查看

## 7. Job Lifecycle

准备代码和数据---写sbatch脚本---sbatch提交--->
                 ┌→ COMPLETED
PENDING → RUNNING
                 ├→ FAILED
                 ├→ OUT_OF_MEMORY
                 ├→ TIMEOUT
                 └→ CANCELLED

## 8.Why does ResearchOps need multiple evidence sources?

一个证据不足以证明结论的可靠性，多重证据能从多个角度验证，得出准确的错误信息和出错原因

单一现象可能对应多个原因，所以要综合 Scheduler、日志、资源使用、脚本和环境等证据才能做更可靠的 Root Cause Diagnosis。

## 9. 为什么不能只根据 stderr 判断故障？

单独的一条错误信息可能存在多种解释。

例如：

```text
Killed
```

并不能直接证明一定发生了内存溢出。

应该进一步结合：

```text
Scheduler State
Resource Usage
stderr
Submit Script
```

例如：

```text
State = OUT_OF_MEMORY

RequestedMem = 32 GB

MaxRSS = 31.9 GB
```

结合这些信息以后，才能更加可靠地判断：

```text
CPU_OUT_OF_MEMORY
```

因此：

```text
一个 Evidence
≠
Root Cause
```

更合理的是：

```text
Multiple Evidence
↓
Root Cause Diagnosis
```

这也是 ResearchOps 需要主动获取多个 Evidence Source 的原因。