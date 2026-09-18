from safety.approval import (
    approval_gate,
)

from safety.policy import (
    assess_action,
)

from safety.schemas import (
    ActionSafetyReview,
    RecoveryAction,
)


def review_action(
    action: RecoveryAction,
    approved: bool = False,
) -> ActionSafetyReview:
    """
    对一个 Recovery Action 完成：

    Policy Assessment
    +
    Approval Gate

    默认 approved=False。
    """

    assessment = assess_action(
        action
    )

    gate = approval_gate(
        action=action,
        assessment=assessment,
        approved=approved,
    )

    return ActionSafetyReview(
        action=action,

        risk_level=(
            assessment.risk_level
        ),

        decision=(
            assessment.decision
        ),

        approval_required=(
            assessment.approval_required
        ),

        executable=(
            gate.executable
        ),

        waiting_for_approval=(
            gate.waiting_for_approval
        ),

        blocked=(
            gate.blocked
        ),

        reason=(
            assessment.reason
        ),
    )


def review_actions(
    actions: list[RecoveryAction],
) -> list[ActionSafetyReview]:
    """
    Agent 新提出的 Action
    默认一律视为尚未获得人工批准。
    """

    return [
        review_action(
            action=action,
            approved=False,
        )
        for action in actions
    ]