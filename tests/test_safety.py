from safety.approval import (
    approval_gate,
)

from safety.policy import (
    assess_action,
)

from safety.schemas import (
    RecoveryAction,
)


def run_case(
    name: str,
    action_name: str,
    approved: bool = False,
):

    action = RecoveryAction(
        action=action_name,
        target="job_1001",
        description=name,
    )


    assessment = assess_action(
        action
    )


    gate = approval_gate(
        action=action,
        assessment=assessment,
        approved=approved,
    )


    print()
    print(
        "=" * 60
    )

    print(name)

    print(
        "=" * 60
    )

    print(
        "Action:",
        action.action,
    )

    print(
        "Risk:",
        assessment.risk_level.value,
    )

    print(
        "Decision:",
        assessment.decision.value,
    )

    print(
        "Approval Required:",
        assessment.approval_required,
    )

    print(
        "Approved:",
        approved,
    )

    print(
        "Executable:",
        gate.executable,
    )

    print(
        "Waiting Approval:",
        gate.waiting_for_approval,
    )

    print(
        "Blocked:",
        gate.blocked,
    )


# ============================================================
# Tests
# ============================================================

run_case(
    name="Read diagnostic status",
    action_name="get_job_status",
)


run_case(
    name="Modify submit script",
    action_name="modify_submit_script",
)


run_case(
    name="Modify submit script after approval",
    action_name="modify_submit_script",
    approved=True,
)


run_case(
    name="Cancel running job",
    action_name="cancel_job",
)


run_case(
    name="Dangerous recursive delete",
    action_name="delete_directory_recursive",
)


run_case(
    name="Unknown action",
    action_name="do_something_unknown",
)