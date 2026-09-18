from pydantic import (
    BaseModel,
)

from safety.schemas import (
    RecoveryAction,
    SafetyAssessment,
    SafetyDecision,
)


class ApprovalResult(
    BaseModel
):
    executable: bool

    waiting_for_approval: bool

    blocked: bool

    message: str


def approval_gate(
    action: RecoveryAction,
    assessment: SafetyAssessment,
    approved: bool = False,
) -> ApprovalResult:

    # ========================================================
    # Safe
    # ========================================================

    if (
        assessment.decision
        ==
        SafetyDecision.ALLOW
    ):

        return ApprovalResult(
            executable=True,
            waiting_for_approval=False,
            blocked=False,
            message=(
                "Action is safe and "
                "may execute directly."
            ),
        )


    # ========================================================
    # Permanently blocked
    # ========================================================

    if (
        assessment.decision
        ==
        SafetyDecision.BLOCK
    ):

        return ApprovalResult(
            executable=False,
            waiting_for_approval=False,
            blocked=True,
            message=(
                "Action is blocked by "
                "ResearchOps safety policy."
            ),
        )


    # ========================================================
    # Requires human approval
    # ========================================================

    if not approved:

        return ApprovalResult(
            executable=False,
            waiting_for_approval=True,
            blocked=False,
            message=(
                "Human approval is required "
                "before execution."
            ),
        )


    return ApprovalResult(
        executable=True,
        waiting_for_approval=False,
        blocked=False,
        message=(
            "Human approval received. "
            "Action may execute."
        ),
    )