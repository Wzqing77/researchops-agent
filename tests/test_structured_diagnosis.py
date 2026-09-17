import json
import sys
from pathlib import Path

from agent.graph import (
    build_diagnostic_graph,
)

from rag.retriever import (
    LocalRetriever,
)

from tools.mock_cluster import (
    MockCluster,
)

from tools.diagnostic_tools import (
    build_diagnostic_tools,
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


retriever = LocalRetriever(

    knowledge_dir=(

        PROJECT_ROOT
        / "rag"
        / "knowledge"
    )
)


graph = build_diagnostic_graph(

    tools=tools,

    retriever=retriever,
)


job_id = (

    sys.argv[1]

    if len(sys.argv) > 1

    else "1001"
)


result = graph.invoke(

    {
        "job_id":
            job_id,

        "messages":
            [],
    },

    config={
        "recursion_limit":
            20
    },
)


diagnosis = (
    result["diagnosis"]
)


validation = (
    result[
        "evidence_validation"
    ]
)


print()
print(
    "=" * 70
)

print(
    "STRUCTURED DIAGNOSIS"
)

print(
    "=" * 70
)


print(

    json.dumps(

        diagnosis.model_dump(),

        indent=2,

        ensure_ascii=False,
    )
)


print()
print(
    "=" * 70
)

print(
    "EVIDENCE VALIDATION"
)

print(
    "=" * 70
)


print(

    json.dumps(

        validation.model_dump(),

        indent=2,

        ensure_ascii=False,
    )
)