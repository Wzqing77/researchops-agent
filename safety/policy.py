from safety.schemas import (
    RecoveryAction,
    RiskLevel,
    SafetyAssessment,
    SafetyDecision,
)


# ============================================================
# Action Policy
# ============================================================

ACTION_POLICY = {

    # --------------------------------------------------------
    # Read-only diagnostic actions
    # --------------------------------------------------------

    "get_job_status": {
        "risk":
            RiskLevel.LOW,

        "decision":
            SafetyDecision.ALLOW,
    },

    "get_job_accounting": {
        "risk":
            RiskLevel.LOW,

        "decision":
            SafetyDecision.ALLOW,
    },

    "read_stdout": {
        "risk":
            RiskLevel.LOW,

        "decision":
            SafetyDecision.ALLOW,
    },

    "read_stderr": {
        "risk":
            RiskLevel.LOW,

        "decision":
            SafetyDecision.ALLOW,
    },

    "get_resource_usage": {
        "risk":
            RiskLevel.LOW,

        "decision":
            SafetyDecision.ALLOW,
    },

    "read_submit_script": {
        "risk":
            RiskLevel.LOW,

        "decision":
            SafetyDecision.ALLOW,
    },

    "get_environment": {
        "risk":
            RiskLevel.LOW,

        "decision":
            SafetyDecision.ALLOW,
    },

    "check_storage": {
        "risk":
            RiskLevel.LOW,

        "decision":
            SafetyDecision.ALLOW,
    },


    # --------------------------------------------------------
    # State-changing recovery actions
    # --------------------------------------------------------

    "modify_submit_script": {
        "risk":
            RiskLevel.MEDIUM,

        "decision":
            SafetyDecision.REQUIRE_APPROVAL,
    },

    "resubmit_job": {
        "risk":
            RiskLevel.MEDIUM,

        "decision":
            SafetyDecision.REQUIRE_APPROVAL,
    },

    "modify_environment": {
        "risk":
            RiskLevel.MEDIUM,

        "decision":
            SafetyDecision.REQUIRE_APPROVAL,
    },    

    "cancel_job": {
        "risk":
            RiskLevel.HIGH,

        "decision":
            SafetyDecision.REQUIRE_APPROVAL,
    },

    "delete_file": {
        "risk":
            RiskLevel.HIGH,

        "decision":
            SafetyDecision.REQUIRE_APPROVAL,
    },


    # --------------------------------------------------------
    # Dangerous actions
    # --------------------------------------------------------

    "delete_directory_recursive": {
        "risk":
            RiskLevel.CRITICAL,

        "decision":
            SafetyDecision.BLOCK,
    },

    "run_arbitrary_shell": {
        "risk":
            RiskLevel.CRITICAL,

        "decision":
            SafetyDecision.BLOCK,
    },
}


# ============================================================
# Safety Assessment
# ============================================================

def assess_action(
    action: RecoveryAction,
) -> SafetyAssessment:

    policy = ACTION_POLICY.get(
        action.action
    )


    # Unknown action:
    # 默认不信任
    if policy is None:

        return SafetyAssessment(
            risk_level=
                RiskLevel.CRITICAL,

            decision=
                SafetyDecision.BLOCK,

            approval_required=
                False,

            reason=(
                "Unknown action is not "
                "present in the safety policy."
                "and is blocked by default"
            ),
        )


    decision = (
        policy["decision"]
    )


    return SafetyAssessment(
        risk_level=
            policy["risk"],

        decision=
            decision,

        approval_required=(
            decision
            ==
            SafetyDecision.REQUIRE_APPROVAL
        ),

        reason=(
            f"Action '{action.action}' "
            f"is classified as "
            f"{policy['risk'].value} risk."
        ),
    )