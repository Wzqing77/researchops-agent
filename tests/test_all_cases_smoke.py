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


job_ids = [

    str(job_id)

    for job_id in range(
        1001,
        1031
    )
]


print(
    "\n================================"
)

print(
    "ALL CASES SMOKE TEST"
)

print(
    "================================"
)


passed = 0


for job_id in job_ids:

    try:

        status = (
            cluster.get_job_status(
                job_id
            )
        )


        print(

            job_id,
            "|",
            status["state"],
            "| PASS"
        )


        passed += 1


    except Exception as exc:

        print(

            job_id,
            "| FAIL |",
            exc
        )


print(
    "\nPassed:",
    passed,
    "/",
    len(job_ids)
)