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


tools = build_diagnostic_tools(
    cluster
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
        "job_id": job_id,
        "messages": [],
    },
    config={
        "recursion_limit": 20
    },
)


diagnosis = (
    result["diagnosis"]
)


validation = (
    result["evidence_validation"]
)


reviews = (
    result["safety_reviews"]
)


print()
print("=" * 70)
print("DIAGNOSIS")
print("=" * 70)

print(
    "Fault Type:",
    diagnosis.fault_type,
)

print(
    "Evidence Valid:",
    validation.valid,
)


print()
print("=" * 70)
print("RECOVERY ACTIONS")
print("=" * 70)


if not diagnosis.recovery_actions:

    print(
        "No recovery actions proposed."
    )


for index, action in enumerate(
    diagnosis.recovery_actions,
    start=1,
):

    print()
    print(
        f"Action {index}"
    )

    print(
        "Name:",
        action.action,
    )

    print(
        "Target:",
        action.target,
    )

    print(
        "Description:",
        action.description,
    )

    print(
        "Parameters:",
        action.parameters,
    )


print()
print("=" * 70)
print("SAFETY REVIEWS")
print("=" * 70)


for index, review in enumerate(
    reviews,
    start=1,
):

    print()
    print(
        f"Review {index}"
    )

    print(
        "Action:",
        review.action.action,
    )

    print(
        "Risk:",
        review.risk_level.value,
    )

    print(
        "Decision:",
        review.decision.value,
    )

    print(
        "Approval Required:",
        review.approval_required,
    )

    print(
        "Executable Now:",
        review.executable,
    )

    print(
        "Waiting Approval:",
        review.waiting_for_approval,
    )

    print(
        "Blocked:",
        review.blocked,
    )