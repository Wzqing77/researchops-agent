# Exit Code 与 Linux Signal

## ExitCode

程序结束时通常会返回一个 Exit Code（退出码）。

最简单的理解：

```text
Exit Code = 0
→ 通常表示程序正常结束

Exit Code ≠ 0
→ 通常表示程序执行过程中出现异常
```

但是：

```text
Non-zero Exit Code
```

只能说明程序发生了异常，不能直接说明具体 Root Cause。

---

## Slurm 中的 ExitCode

Slurm Accounting 中常见格式为：

```text
exit_code:signal
```

例如：

```text
0:0
```

通常表示：

```text
Application Exit Code = 0
Signal = 0
```

程序正常结束。

---

## 1:0

例如：

```text
ExitCode = 1:0
```

表示：

```text
Application Exit Code = 1
Signal = 0
```

说明程序主动以非零状态退出。

可能原因包括：

```text
Python Exception
Missing Dependency
Wrong File Path
Permission Error
Application Error
```

因此仍然需要进一步查看：

```text
stderr
stdout
environment
```

---

## 什么是 Signal？

Linux Signal 可以理解为：

> 操作系统或其他进程发送给当前程序的一种控制信号。

Signal 可以：

```text
要求程序停止
强制杀死程序
通知程序发生异常
```

在 HPC 故障诊断中，Signal 是非常重要的系统级 Evidence。

---

## Signal 9：SIGKILL

```text
Signal = 9
SIGKILL
```

表示进程被立即强制终止。

程序无法捕获或拒绝 SIGKILL。

例如：

```text
ExitCode = 0:9
```

说明程序最终受到了：

```text
SIGKILL
```

但是需要特别注意：

```text
SIGKILL
≠
CPU OOM
```

SIGKILL 可能来自：

```text
Linux OOM Killer
Slurm Scheduler
管理员
用户
其他系统机制
```

因此：

```text
ExitCode = 0:9
```

不能单独证明发生了 CPU 内存溢出。

---

## Signal 15：SIGTERM

```text
Signal = 15
SIGTERM
```

表示：

> 请求程序终止。

与 SIGKILL 不同，程序通常可以捕获 SIGTERM。

程序收到 SIGTERM 后，可以有机会：

```text
保存结果
关闭文件
释放资源
执行清理工作
```

然后再退出。

Scheduler 在停止 Job 时可能首先发送 SIGTERM。

---

## Signal 11：SIGSEGV

```text
Signal = 11
SIGSEGV
```

通常表示：

```text
Segmentation Fault
```

即程序进行了非法内存访问。

常见原因可能包括：

```text
Native Code Bug
Invalid Pointer
C / C++ Library Error
Compiled Library Failure
```

需要注意：

```text
SIGSEGV
≠
OUT_OF_MEMORY
```

Segmentation Fault 与内存容量不足是两种不同类型的问题。

---

## Exit Code 与 Signal 的区别

可以简单理解：

```text
Exit Code
→ 程序自己如何结束

Signal
→ 程序是否受到外部或系统级信号终止
```

例如：

```text
1:0
```

更偏向：

```text
程序自己报错退出
```

而：

```text
0:9
```

说明：

```text
程序受到 SIGKILL
```

---

## 诊断原则

ExitCode 和 Signal 都属于重要 Evidence。

但是：

```text
ExitCode
≠
Root Cause

Signal
≠
Root Cause
```

例如：

```text
ExitCode = 0:9
stderr = Killed
```

仍然不足以直接判断 CPU OOM。

如果继续发现：

```text
State = OUT_OF_MEMORY
RequestedMem = 32 GB
MaxRSS = 31.9 GB
```

则 CPU OOM 的证据链才会明显增强。

---

## 总结

ResearchOps 应该使用：

```text
ExitCode
+
Signal
+
Scheduler State
+
Logs
+
Resource Usage
```

进行综合诊断，而不是依靠单一 ExitCode 或 Signal 猜测 Root Cause。