from pathlib import Path

from tools.mock_cluster import (
    MockCluster
)

from tools.diagnostic_tools import (
    build_diagnostic_tools
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


tools = (
    build_diagnostic_tools(
        cluster
    )
)


print(
    "\n================================"
)

print(
    "DIAGNOSTIC TOOLS"
)

print(
    "================================"
)


for item in tools:

    print(
        "\nTool:",
        item.name
    )


    print(
        "Description:",
        item.description
    )


    print(
        "Args:",
        item.args
    )