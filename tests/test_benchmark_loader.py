from pathlib import Path

from eval.benchmark_loader import (
    BenchmarkLoader
)


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


loader = BenchmarkLoader(

    benchmark_root=(
        PROJECT_ROOT
        / "benchmark"
    )
)


cases = (
    loader.load_all()
)


print(
    "\n================================"
)

print(
    "BENCHMARK CASES"
)

print(
    "================================"
)


for case in cases:

    print(

        case["case_id"],
        "|",
        case["fault_type"],
        "|",
        case["difficulty"]
    )


print(
    "\nTotal Cases:",
    len(cases)
)