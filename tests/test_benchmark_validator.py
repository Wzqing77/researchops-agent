from pathlib import Path

from eval.benchmark_validator import (
    BenchmarkValidator
)


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


validator = BenchmarkValidator(

    benchmark_root=(
        PROJECT_ROOT
        / "benchmark"
    )
)


errors = (
    validator.validate_all()
)


print(
    "\n================================"
)

print(
    "BENCHMARK VALIDATION"
)

print(
    "================================"
)


if not errors:

    print(
        "PASS"
    )


    print(
        "All benchmark cases are valid."
    )


else:

    print(
        "FAIL"
    )


    for error in errors:

        print(
            "-",
            error
        )