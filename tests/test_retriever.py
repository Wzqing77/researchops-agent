from pathlib import Path

from rag.retriever import LocalRetriever


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

retriever = LocalRetriever(
    knowledge_dir=(
        PROJECT_ROOT
        / "rag"
        / "knowledge"
    )
)


queries = [
    "Slurm 中 OUT_OF_MEMORY 表示什么？",

    "ExitCode 0:9 是什么意思？",

    "为什么 Job 是 PENDING，并且 Reason=Resources？",

    "CUDA out of memory 是 CPU 内存不足吗？",
]


for query in queries:

    print(
        "\n"
        "================================"
    )

    print(
        f"QUERY: {query}"
    )

    print(
        "================================"
    )

    results = retriever.search(
        query=query,
        top_k=3,
    )

    for rank, result in enumerate(
        results,
        start=1,
    ):
        print(
            f"\n--- TOP {rank} ---"
        )

        print(
            "Source:",
            result["source"],
        )

        print(
            "Chunk:",
            result["chunk_id"],
        )

        print(
            "Score:",
            round(
                result["score"],
                4,
            ),
        )

        print(
            "\nText:"
        )

        print(
            result["text"]
        )