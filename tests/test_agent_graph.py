import sys
from pathlib import Path

from langchain_core.messages import (
    AIMessage,
    ToolMessage,
)

from agent.graph import build_diagnostic_graph
from rag.retriever import LocalRetriever
from tools.mock_cluster import MockCluster
from tools.diagnostic_tools import (
    build_diagnostic_tools,
)


# ============================================================
# Project Paths
# ============================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

BENCHMARK_ROOT = (
    PROJECT_ROOT
    / "benchmark"
)

KNOWLEDGE_ROOT = (
    PROJECT_ROOT
    / "rag"
    / "knowledge"
)


# ============================================================
# Build Components
# ============================================================

cluster = MockCluster(
    benchmark_root=BENCHMARK_ROOT
)

tools = build_diagnostic_tools(
    cluster
)

retriever = LocalRetriever(
    knowledge_dir=KNOWLEDGE_ROOT
)

graph = build_diagnostic_graph(
    tools=tools,
    retriever=retriever,
)


# ============================================================
# Job ID
# ============================================================

if len(sys.argv) > 1:
    job_id = sys.argv[1]
else:
    job_id = "1001"


print()
print("=" * 70)
print("ResearchOps Diagnostic Agent")
print("=" * 70)

print(
    f"Job ID: {job_id}"
)


# ============================================================
# Run Graph
# ============================================================

result = graph.invoke(
    {
        "job_id": job_id,
        "messages": [],
    },
    config={
        "recursion_limit": 20
    },
)


# ============================================================
# Print Initial Evidence
# ============================================================

print()
print("=" * 70)
print("INITIAL EVIDENCE")
print("=" * 70)

print(
    result.get(
        "initial_evidence",
        "No initial evidence.",
    )
)


# ============================================================
# Print Agent Trace
# ============================================================

print()
print("=" * 70)
print("AGENT TRACE")
print("=" * 70)


for index, message in enumerate(
    result["messages"],
    start=1,
):

    print()
    print(
        f"[Step {index}] "
        f"{type(message).__name__}"
    )


    # --------------------------------------------------------
    # AI Message
    # --------------------------------------------------------

    if isinstance(
        message,
        AIMessage,
    ):

        if message.content:

            print(
                "Content:"
            )

            print(
                message.content
            )


        if message.tool_calls:

            print(
                "Tool Calls:"
            )

            for tool_call in (
                message.tool_calls
            ):

                print(
                    f"  - Tool: "
                    f"{tool_call['name']}"
                )

                print(
                    f"    Args: "
                    f"{tool_call['args']}"
                )


    # --------------------------------------------------------
    # Tool Message
    # --------------------------------------------------------

    elif isinstance(
        message,
        ToolMessage,
    ):

        print(
            f"Tool Result: "
            f"{message.name}"
        )

        print(
            message.content
        )


    # --------------------------------------------------------
    # Other Message
    # --------------------------------------------------------

    else:

        print(
            message.content
        )


# ============================================================
# Final Diagnosis
# ============================================================

print()
print("=" * 70)
print("FINAL DIAGNOSIS")
print("=" * 70)

print(
    result["messages"][-1].content
)