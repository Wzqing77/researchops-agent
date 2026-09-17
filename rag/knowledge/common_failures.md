# HPC 常见故障模式

## CPU Out of Memory

CPU Out-of-Memory 表示系统 RAM 不足。

这里的 Memory 指：

```text
System Memory
CPU Memory
RAM
```

而不是 GPU 显存。

常见 Evidence 包括：

```text
State = OUT_OF_MEMORY
RequestedMem
MaxRSS
oom-kill
sbatch --mem
```

例如，当发现：

RequestedMem 与 MaxRSS 非常接近，
并且 Scheduler State = OUT_OF_MEMORY

可以较强地支持：

CPU_OUT_OF_MEMORY

---

## CUDA Out of Memory

CUDA Out-of-Memory 表示 GPU 显存不足。

GPU 显存也称：

```text
GPU Memory
VRAM
```

常见错误包括：

```text
CUDA out of memory
```

或者：

```text
torch.cuda.OutOfMemoryError
```

有价值的 Evidence 包括：

```text
GPU Memory Total
GPU Memory Peak
stderr
GPU Resource Configuration
```

需要注意：

```text
CPU RAM
≠
GPU VRAM
```

因此增加：

```bash
#SBATCH --mem=128G
```

并不会直接增加 GPU 的显存容量。

---

## Walltime / TIMEOUT

TIMEOUT 表示 Job 超过 Slurm 允许的最大运行时间。

重要 Evidence 包括：

```text
State = TIMEOUT
Requested Walltime
Elapsed Time
Slurm Time Limit Message
```

例如：

```text
Requested Time = 01:00:00
Elapsed = 01:00:04
State = TIMEOUT
```

说明 Job 达到了申请的时间限制。

---

## Missing Dependency

Missing Dependency 表示运行环境缺少程序所需要的软件、Python Package、动态库或命令。

常见错误包括：

```text
ModuleNotFoundError
ImportError
command not found
shared library not found
```

例如：

```text
ModuleNotFoundError: No module named 'torch'
```

诊断时应该检查：

```text
Conda Environment
Python Version
Installed Packages
module
PATH
Shared Libraries
```

---

## Wrong File Path

Wrong File Path 表示程序访问的文件或目录不存在，或者路径解析与预期不同。

常见错误包括：

```text
FileNotFoundError
No such file or directory
```

可能原因包括：

```text
绝对路径错误
相对路径错误
Working Directory 不正确
环境变量展开错误
文件系统未挂载
```

因此：

```text
FileNotFoundError
```

不一定意味着用户简单地“把文件名写错了”。

还需要结合：

```text
Working Directory
Submit Script
Path Information
Filesystem State
```

进行判断。

---

## Disk Full

Disk Full 表示程序无法继续向存储系统写入数据。

常见错误：

```text
No space left on device
```

可能发现：

```text
Disk Usage = 100%
Free Space = 0
```

这种情况属于文件系统空间耗尽。

---

## Disk Quota Exceeded

用户还可能看到：

```text
Disk quota exceeded
```

这种情况与整个磁盘空间耗尽不同。

例如：

```text
Filesystem Free Space = 640 GB
```

但是：

```text
User Quota = 100 GB
User Usage = 100 GB
```

此时整个文件系统仍然有空间，但当前用户已经达到个人配额。

因此：

```text
Filesystem Capacity
≠
User Quota
```

---

## Permission Denied

Permission Denied 表示当前用户没有执行某项文件操作所需的权限。

常见错误包括：

```text
Permission denied
Operation not permitted
```

可能涉及：

```text
Read Permission
Write Permission
Execute Permission
Ownership
Group Membership
```

有价值的信息包括：

```text
File Owner
File Group
Permission Mode
Current User
User Groups
```

例如：

```text
mode = 0644
```

意味着普通文件通常没有 execute permission。

如果用户执行：

```bash
./run_analysis.sh
```

但文件没有执行权限，则可能得到：

```text
Permission denied
```

---

## PENDING Resources

Job 处于：

```text
PENDING
```

并不意味着 Job 已经失败。

如果：

```text
State = PENDING
Reason = Resources
```

说明当前没有满足该 Job 资源要求的可用 Node。

需要查看：

```text
Partition
CPU Request
Memory Request
GPU Request
Node Requirement
```

例如：

```text
GPU Requested = 4
```

但是当前没有具有 4 块空闲 GPU 的节点，则 Job 可能继续处于 PENDING。

因此：

```text
PENDING
≠
FAILED
```

---

## 故障诊断原则

HPC 中很多错误现象并不唯一对应某个 Root Cause。

例如：

```text
Killed
```

可能由多种原因产生。

因此 ResearchOps 不应该采用：

```text
Error String
↓
直接匹配 Fault Type
```

而应该采用：

```text
Initial Evidence
↓
判断是否存在歧义
↓
获取新的 Evidence
↓
交叉验证
↓
Root Cause Diagnosis
```

---

## Evidence 与 Knowledge

需要区分两个概念。

### Evidence

Evidence 描述：

> 当前这个具体 Job 实际发生了什么。

例如：

```text
State = OUT_OF_MEMORY
MaxRSS = 31.9 GB
```

### Knowledge

Knowledge 描述：

> HPC 系统中这些现象通常意味着什么。

例如：

```text
OUT_OF_MEMORY 通常表示 Job 超出了系统内存限制。
```

RAG 提供的是：

```text
Knowledge
```

Diagnostic Tool 提供的是：

```text
Evidence
```

最终诊断应该：

```text
Evidence
+
Domain Knowledge
↓
Root Cause Diagnosis
```

而不能使用 Knowledge 凭空构造不存在的 Evidence。