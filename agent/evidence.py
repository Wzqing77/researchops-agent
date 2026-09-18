import json
import re
from typing import Any

from langchain_core.messages import (
    ToolMessage,
)

from agent.schemas import (
    DiagnosisResult,
    EvidenceCheck,
    EvidenceValidationReport,
)


# ============================================================
# Parse Tool Output
# ============================================================

def _parse_observation(
    value: Any,
) -> Any:

    if not isinstance(
        value,
        str,
    ):
        return value

    text = value.strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        return text


# ============================================================
# Build Evidence Store
# ============================================================

def build_evidence_store(
    initial_evidence_data: dict,
    messages: list,
) -> dict[str, list[Any]]:
    """
    把真正观察到的 Evidence 整理成：

    {
        "get_job_status": [
            {...}
        ],

        "read_stderr": [
            "Killed"
        ],

        "get_resource_usage": [
            {...}
        ]
    }
    """

    store: dict[
        str,
        list[Any]
    ] = {}


    # --------------------------------------------------------
    # Initial Evidence
    # --------------------------------------------------------

    for source, value in (
        initial_evidence_data.items()
    ):

        store.setdefault(
            source,
            [],
        ).append(
            value
        )


    # --------------------------------------------------------
    # Tool Evidence
    # --------------------------------------------------------

    for message in messages:

        if not isinstance(
            message,
            ToolMessage,
        ):
            continue


        source = message.name

        observation = (
            _parse_observation(
                message.content
            )
        )


        store.setdefault(
            source,
            [],
        ).append(
            observation
        )


    return store


# ============================================================
# Normalize
# ============================================================

def _normalize(
    value: Any,
) -> str:
    """
    统一文本格式，降低因为：
    - 大小写
    - 换行
    - Tab
    - 转义换行 \\n
    - 多余空格

    导致的误判。
    """

    text = str(
        value
    )

    # 模型有时会返回字面量 "\n"
    # 而 Tool Result 中是真实换行。
    text = text.replace(
        "\\n",
        "\n",
    )

    text = text.replace(
        "\\t",
        "\t",
    )

    text = (
        text
        .strip()
        .lower()
    )

    # 所有连续空白统一成一个空格
    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text


# ============================================================
# Numeric Comparison
# ============================================================

def _to_number(
    value: Any,
) -> float | None:

    try:
        return float(
            str(value).strip()
        )

    except (
        ValueError,
        TypeError,
    ):
        return None

# ============================================================
# 让Validator 真正支持 list / dict
# ============================================================

def _parse_expected_structure(
    value: Any,
) -> Any:
    """
    如果模型输出的是 JSON 字符串形式的
    list / dict，则尝试恢复成真正的数据结构。
    """

    if not isinstance(
        value,
        str,
    ):
        return value

    text = value.strip()

    try:
        return json.loads(
            text
        )

    except json.JSONDecodeError:
        return value
    

    # ========================================================
    # Structured Value
    # list / dict
    # ========================================================

    if isinstance(
        actual_value,
        (
            list,
            dict,
        ),
    ):

        parsed_expected = (
            _parse_expected_structure(
                expected_value
            )
        )


        if isinstance(
            parsed_expected,
            type(actual_value),
        ):

            return (
                actual_value
                ==
                parsed_expected
            )


        return False


    # ========================================================
    # Numeric Value
    # ========================================================

    actual_number = (
        _to_number(
            actual_value
        )
    )

    expected_number = (
        _to_number(
            expected_value
        )
    )


    if (
        actual_number is not None
        and
        expected_number is not None
    ):

        return (
            abs(
                actual_number
                -
                expected_number
            )
            < 1e-9
        )


    # ========================================================
    # Normal String Value
    # ========================================================

    return (
        _normalize(
            actual_value
        )
        ==
        _normalize(
            expected_value
        )
    )

# ============================================================
# Compare Structured Field
# ============================================================

def _field_matches(
    observation: Any,
    field: str,
    expected_value: str,
) -> bool:

    if not isinstance(
        observation,
        dict,
    ):
        return False


    if field not in observation:
        return False


    actual_value = (
        observation[field]
    )


    # ========================================================
    # Structured Value
    # list / dict
    # ========================================================

    if isinstance(
        actual_value,
        (
            list,
            dict,
        ),
    ):

        parsed_expected = (
            _parse_expected_structure(
                expected_value
            )
        )


        if isinstance(
            parsed_expected,
            type(actual_value),
        ):

            return (
                actual_value
                ==
                parsed_expected
            )


        return False


    # ========================================================
    # Numeric Value
    # ========================================================

    actual_number = (
        _to_number(
            actual_value
        )
    )

    expected_number = (
        _to_number(
            expected_value
        )
    )


    if (
        actual_number is not None
        and
        expected_number is not None
    ):

        return (
            abs(
                actual_number
                -
                expected_number
            )
            < 1e-9
        )


    # ========================================================
    # Normal String Value
    # ========================================================

    return (
        _normalize(
            actual_value
        )
        ==
        _normalize(
            expected_value
        )
    )


# ============================================================
# Compare Text Evidence
# ============================================================

def _text_matches(
    observation: Any,
    expected_value: str,
) -> bool:

    observation_text = (
        _normalize(
            observation
        )
    )

    expected_text = (
        _normalize(
            expected_value
        )
    )

    # 空字符串不能作为有效 Evidence
    if not expected_text:
        return False

    return (
        expected_text
        in
        observation_text
    )


# ============================================================
# Validate One Evidence
# ============================================================

def _validate_one(
    evidence,
    evidence_store,
) -> tuple[
    bool,
    str,
]:

    source = evidence.source


    if source not in evidence_store:

        return (
            False,
            (
                f"Evidence source "
                f"'{source}' "
                f"was never observed."
            ),
        )


    observations = (
        evidence_store[source]
    )


    # --------------------------------------------------------
    # Structured Evidence
    # --------------------------------------------------------

    if evidence.field:

        for observation in observations:

            if _field_matches(
                observation,
                evidence.field,
                evidence.value,
            ):

                return (
                    True,
                    (
                        f"Verified "
                        f"{source}."
                        f"{evidence.field} "
                        f"= {evidence.value}"
                    ),
                )


        return (
            False,
            (
                f"Field/value not found: "
                f"{source}."
                f"{evidence.field} "
                f"= {evidence.value}"
            ),
        )


    # --------------------------------------------------------
    # Text Evidence
    # --------------------------------------------------------

    for observation in observations:

        if _text_matches(
            observation,
            evidence.value,
        ):

            return (
                True,
                (
                    f"Verified text "
                    f"from {source}."
                ),
            )


    return (
        False,
        (
            f"Text '{evidence.value}' "
            f"was not found in "
            f"{source}."
        ),
    )


# ============================================================
# Validate Diagnosis
# ============================================================

def validate_evidence(
    diagnosis: DiagnosisResult,
    evidence_store: dict[
        str,
        list[Any],
    ],
) -> EvidenceValidationReport:

    checks = []


    for index, evidence in enumerate(
        diagnosis.evidence,
        start=1,
    ):

        grounded, reason = (
            _validate_one(
                evidence,
                evidence_store,
            )
        )


        checks.append(
            EvidenceCheck(
                index=index,
                source=evidence.source,
                grounded=grounded,
                reason=reason,
            )
        )


    unsupported_count = sum(

        not check.grounded

        for check in checks
    )


    return EvidenceValidationReport(

        valid=(
            unsupported_count
            ==
            0
        ),

        unsupported_count=(
            unsupported_count
        ),

        checks=checks,
    )