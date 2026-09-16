from langchain_core.tools import (
    tool
)


def build_diagnostic_tools(
    cluster
):

    # ========================================================
    # Tool 1
    # ========================================================

    @tool
    def get_job_status(
        job_id: str
    ) -> dict:
        """
        查询指定 HPC Job 当前的调度状态。

        适合用于判断 Job 是否处于
        PENDING、RUNNING、FAILED、
        OUT_OF_MEMORY、TIMEOUT 等状态。
        """

        return (
            cluster.get_job_status(
                job_id
            )
        )


    # ========================================================
    # Tool 2
    # ========================================================

    @tool
    def get_job_accounting(
        job_id: str
    ) -> dict:
        """
        查询指定 HPC Job 的历史运行记录。

        返回 Job State、ExitCode、
        Elapsed Time 等信息。
        适合诊断已经结束或失败的 Job。
        """

        return (
            cluster.get_job_accounting(
                job_id
            )
        )


    # ========================================================
    # Tool 3
    # ========================================================

    @tool
    def read_stdout(
        job_id: str
    ) -> str:
        """
        读取指定 HPC Job 的标准输出 stdout。
        """

        return (
            cluster.read_stdout(
                job_id
            )
        )


    # ========================================================
    # Tool 4
    # ========================================================

    @tool
    def read_stderr(
        job_id: str
    ) -> str:
        """
        读取指定 HPC Job 的标准错误 stderr。

        可用于发现 Traceback、CUDA OOM、
        ModuleNotFoundError、Permission denied
        等错误信息。
        """

        return (
            cluster.read_stderr(
                job_id
            )
        )


    # ========================================================
    # Tool 5
    # ========================================================

    @tool
    def get_resource_usage(
        job_id: str
    ) -> dict:
        """
        查询指定 HPC Job 的资源使用情况。

        可能包含 Requested Memory、
        MaxRSS、CPU Efficiency、
        GPU Memory 等信息。
        """

        return (
            cluster.get_resource_usage(
                job_id
            )
        )


    # ========================================================
    # Tool 6
    # ========================================================

    @tool
    def read_submit_script(
        job_id: str
    ) -> str:
        """
        读取指定 HPC Job 的 sbatch 提交脚本。

        可用于检查 CPU、Memory、GPU、
        Walltime、Partition 等资源申请配置。
        """

        return (
            cluster.read_submit_script(
                job_id
            )
        )


    # ========================================================
    # Tool 7
    # ========================================================

    @tool
    def get_environment(
        job_id: str
    ) -> dict:
        """
        查询指定 HPC Job 的软件运行环境。

        可能包含 Python 版本、Conda 环境、
        已安装 Package、CUDA 版本等信息。
        """

        return (
            cluster.get_environment(
                job_id
            )
        )


    # ========================================================
    # Tool 8
    # ========================================================

    @tool
    def check_storage(
        job_id: str
    ) -> dict:
        """
        查询指定 HPC Job 相关的存储信息。

        可用于诊断 Disk Full、
        Quota Exceeded 等存储问题。
        """

        return (
            cluster.check_storage(
                job_id
            )
        )


    return [

        get_job_status,
        get_job_accounting,
        read_stdout,
        read_stderr,
        get_resource_usage,
        read_submit_script,
        get_environment,
        check_storage,
    ]