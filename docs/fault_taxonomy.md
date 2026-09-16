# ResearchOps Fault Taxonomy

## 1. CPU_OUT_OF_MEMORY

含义：Job 使用的系统 RAM 超过可用或申请的内存。

常见证据：

- Slurm State = OUT_OF_MEMORY
- oom-kill
- MaxRSS 接近 RequestedMem
- `--mem` 申请过低

容易混淆：

- CUDA_OUT_OF_MEMORY
- 普通进程被 Killed
- Node / application crash

---

## 2. CUDA_OUT_OF_MEMORY

含义：GPU 显存 VRAM 不足。

常见证据：

- `torch.cuda.OutOfMemoryError`
- CUDA allocation failure
- GPU Memory Peak 接近 GPU Memory Total

容易混淆：

- CPU_OUT_OF_MEMORY
- CUDA driver / runtime error
- GPU unavailable

---

## 3. TIMEOUT

含义：Job 达到了 Slurm 允许的最大 Walltime。

常见证据：

- State = TIMEOUT
- Elapsed 接近 Requested Time
- `DUE TO TIME LIMIT`

容易混淆：

- 用户手动 CANCELLED
- 程序自身超时
- Node failure

---

## 4. MISSING_DEPENDENCY

含义：运行环境缺少程序需要的软件、Python Package、动态库或命令。

常见证据：

- ModuleNotFoundError
- ImportError
- command not found
- shared library not found

需要结合：

- Conda Environment
- Installed Packages
- module
- PATH

---

## 5. WRONG_FILE_PATH

含义：程序引用的输入文件或目录不存在，或者当前 Working Directory 与预期不同。

常见证据：

- FileNotFoundError
- No such file or directory
- Path does not exist

容易混淆：

- 文件系统未挂载
- Relative Path 问题
- 环境变量展开错误

---

## 6. DISK_FULL

含义：程序无法继续写入数据，因为磁盘空间或用户 Quota 已耗尽。

常见证据：

- No space left on device
- Disk quota exceeded
- Disk Usage = 100%
- User Quota reached

注意：

磁盘整体有空闲空间，不代表用户自己的 Quota 还有空间。

---

## 7. PERMISSION_DENIED

含义：当前用户对文件、目录或可执行文件没有必要权限。

常见证据：

- Permission denied
- Operation not permitted
- 文件 ownership / mode 不允许当前操作

需要结合：

- 文件权限
- 用户 / 用户组
- Submit Script 中的操作

---

## 8. PENDING_RESOURCES

含义：Job 已成功提交，但当前没有满足资源申请条件的计算资源。

常见证据：

- State = PENDING
- Reason = Resources
- ReqNodeNotAvail
- Requested GPU / Memory / Node 过于稀缺

注意：

PENDING 本身不是 Failure。

必须进一步检查：

- Pending Reason
- Partition
- Requested Resources