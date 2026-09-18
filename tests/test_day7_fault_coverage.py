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
# Build Shared Components
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
# Remaining Fault Types
# ============================================================

TEST_CASES = {
    "1002": "CUDA_OUT_OF_MEMORY",
    "1009": "WRONG_FILE_PATH",
    "1011": "DISK_FULL",
    "1013": "PERMISSION_DENIED",
    "1015": "PENDING_RESOURCES",
}


# ============================================================
# Run
# ============================================================

results = []


for job_id, expected_fault in TEST_CASES.items():

    print()
    print("=" * 70)
    print(
        f"DIAGNOSING JOB {job_id}"
    )
    print("=" * 70)


    try:

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
            result[
                "evidence_validation"
            ]
        )


        predicted_fault = (
            diagnosis.fault_type
        )


        fault_correct = (
            predicted_fault
            ==
            expected_fault
        )


        evidence_valid = (
            validation.valid
        )


        passed = (
            fault_correct
            and
            evidence_valid
        )


        results.append(
            {
                "job_id": job_id,
                "expected": expected_fault,
                "predicted": predicted_fault,
                "fault_correct": fault_correct,
                "evidence_valid": evidence_valid,
                "unsupported": (
                    validation
                    .unsupported_count
                ),
                "passed": passed,
            }
        )


        print(
            f"Expected:  "
            f"{expected_fault}"
        )


        print(
            f"Predicted: "
            f"{predicted_fault}"
        )


        print(
            f"Fault Correct: "
            f"{fault_correct}"
        )


        print(
            f"Evidence Valid: "
            f"{evidence_valid}"
        )


        print(
            f"Unsupported Evidence: "
            f"{validation.unsupported_count}"
        )


        print(
            "Result:",
            "PASS"
            if passed
            else "FAIL",
        )


        print()
        print(
            "Evidence:"
        )


        for evidence in (
            diagnosis.evidence
        ):

            print(
                f"- "
                f"{evidence.source}"
                f".{evidence.field}: "
                f"{evidence.value}"
            )


    except Exception as error:

        print(
            f"ERROR: {error}"
        )


        results.append(
            {
                "job_id": job_id,
                "expected": expected_fault,
                "predicted": "ERROR",
                "fault_correct": False,
                "evidence_valid": False,
                "unsupported": -1,
                "passed": False,
            }
        )


# ============================================================
# Summary
# ============================================================

print()
print("=" * 90)
print("DAY 7 FAULT COVERAGE SUMMARY")
print("=" * 90)


print(
    f"{'Job':<8}"
    f"{'Expected':<25}"
    f"{'Predicted':<25}"
    f"{'Evidence':<12}"
    f"{'Result'}"
)


print("-" * 90)


for item in results:

    print(
        f"{item['job_id']:<8}"
        f"{item['expected']:<25}"
        f"{item['predicted']:<25}"
        f"{str(item['evidence_valid']):<12}"
        f"{'PASS' if item['passed'] else 'FAIL'}"
    )


passed_count = sum(
    item["passed"]
    for item in results
)


print()
print(
    f"Passed: "
    f"{passed_count} / "
    f"{len(results)}"
)