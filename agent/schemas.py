from typing import Literal

from pydantic import (
    BaseModel,
    Field,
)


# ============================================================
# Standard Fault Types
# ============================================================

FaultType = Literal[
    "CPU_OUT_OF_MEMORY",
    "CUDA_OUT_OF_MEMORY",
    "TIMEOUT",
    "MISSING_DEPENDENCY",
    "WRONG_FILE_PATH",
    "DISK_FULL",
    "PERMISSION_DENIED",
    "PENDING_RESOURCES",
]


# ============================================================
# Evidence Item
# ============================================================

class EvidenceItem(BaseModel):
    """
    一条可以被程序验证的诊断证据。
    """

    source: str = Field(
        description=(
            "证据来源，例如 get_job_status、"
            "read_stderr、get_resource_usage。"
        )
    )

    field: str | None = Field(
        default=None,
        description=(
            "如果来源是 JSON / dict，填写字段名。"
            "例如 state、max_rss_gb。"
            "纯文本证据填写 null。"
        ),
    )

    value: str = Field(
        description=(
            "从真实 Evidence 中直接读取的值。"
            "不得编造或改写成不存在的值。"
        )
    )

    supports: str = Field(
        description=(
            "说明这条 Evidence 为什么支持当前诊断。"
        )
    )


# ============================================================
# Structured Diagnosis
# ============================================================

class DiagnosisResult(BaseModel):
    """
    ResearchOps 最终结构化诊断结果。
    """

    fault_type: FaultType

    root_cause: str

    evidence: list[EvidenceItem] = Field(
        min_length=1
    )

    recommendations: list[str] = Field(
        min_length=1
    )

    uncertainty: str


# ============================================================
# Evidence Validation
# ============================================================

class EvidenceCheck(BaseModel):

    index: int

    source: str

    grounded: bool

    reason: str


class EvidenceValidationReport(BaseModel):

    valid: bool

    unsupported_count: int

    checks: list[EvidenceCheck]