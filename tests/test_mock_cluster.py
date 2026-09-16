from pathlib import Path

from tools.mock_cluster import (
    MockCluster
)


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


cluster = MockCluster(

    benchmark_root=(
        PROJECT_ROOT
        / "benchmark"
    )
)


# ============================================================
# JOB 1001
# CPU OOM
# ============================================================

print(
    "\n================================"
)

print(
    "JOB 1001"
)

print(
    "================================"
)


print(
    "\n[STATUS]"
)

print(
    cluster.get_job_status(
        "1001"
    )
)


print(
    "\n[ACCOUNTING]"
)

print(
    cluster.get_job_accounting(
        "1001"
    )
)


print(
    "\n[STDERR]"
)

print(
    cluster.read_stderr(
        "1001"
    )
)


print(
    "\n[STDOUT]"
)

print(
    cluster.read_stdout(
        "1001"
    )
)


print(
    "\n[RESOURCE]"
)

print(
    cluster.get_resource_usage(
        "1001"
    )
)


print(
    "\n[SUBMIT SCRIPT]"
)

print(
    cluster.read_submit_script(
        "1001"
    )
)


print(
    "\n[ENVIRONMENT]"
)

print(
    cluster.get_environment(
        "1001"
    )
)


print(
    "\n[STORAGE]"
)

print(
    cluster.check_storage(
        "1001"
    )
)