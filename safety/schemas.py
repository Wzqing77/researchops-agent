from enum import Enum

from pydantic import (
    BaseModel,
    Field,
)

# 风险不由LLM自行决定
# 模型只能提出action和target，由Runtime Safety Policy决定风险等级和是否需要请求

# ============================================================
# Risk Level
# ============================================================

class RiskLevel(
    str,
    Enum,
):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# ============================================================
# Safety Decision
# ============================================================

class SafetyDecision(
    str,
    Enum,
):
    ALLOW = "ALLOW"

    REQUIRE_APPROVAL = (
        "REQUIRE_APPROVAL"
    )

    BLOCK = "BLOCK"


# ============================================================
# Recovery Action
# ============================================================

class RecoveryAction(
    BaseModel
):
    """
    Agent 希望执行的一个恢复操作。
    """

    action: str

    target: str

    description: str

    parameters: dict = Field(
        default_factory=dict
    )


# ============================================================
# Safety Assessment
# ============================================================

class SafetyAssessment(
    BaseModel
):
    """
    Runtime 对 RecoveryAction
    做出的确定性安全判断。
    """

    risk_level: RiskLevel

    decision: SafetyDecision

    approval_required: bool

    reason: str


class ActionSafetyReview(
    BaseModel
):
    """
    一个 Recovery Action
    经过 Safety Policy + Approval Gate
    后的完整审核结果。
    """

    action: RecoveryAction

    risk_level: RiskLevel

    decision: SafetyDecision

    approval_required: bool

    executable: bool

    waiting_for_approval: bool

    blocked: bool

    reason: str