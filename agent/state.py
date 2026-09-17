# 整个 Graph 在节点之间共享的运行状态

from typing import (
    Any,
)

from typing_extensions import (
    NotRequired,
)

from langgraph.graph import (
    MessagesState,
)

from agent.schemas import (
    DiagnosisResult,
    EvidenceValidationReport,
)


class DiagnosticState(
    MessagesState
):
    """
    ResearchOps LangGraph State。
    """

    job_id: str

    initial_evidence: NotRequired[
        str
    ]

    initial_evidence_data: NotRequired[
        dict[
            str,
            Any,
        ]
    ]

    knowledge_context: NotRequired[
        str
    ]

    diagnosis: NotRequired[
        DiagnosisResult
    ]

    evidence_validation: NotRequired[
        EvidenceValidationReport
    ]