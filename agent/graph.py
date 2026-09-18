import os

from dotenv import load_dotenv

from langchain_core.messages import (
    SystemMessage,
    ToolMessage,
)

from langchain_openai import ChatOpenAI

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.prebuilt import ToolNode

from agent.state import DiagnosticState

from agent.prompts import (
    REASON_SYSTEM_PROMPT,
    FINAL_DIAGNOSIS_PROMPT,
)

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from agent.schemas import (
    DiagnosisResult,
)

from agent.evidence import (
    build_evidence_store,
    validate_evidence,
)

from safety.review import (
    review_actions,
)

# ============================================================
# Model
# ============================================================

def build_model(
    thinking: bool = True,
):

    load_dotenv()

    api_key = os.getenv(
        "DEEPSEEK_API_KEY"
    )

    if not api_key:

        raise RuntimeError(
            "DEEPSEEK_API_KEY is missing."
        )


    model_kwargs = {

        "model":
            os.getenv(
                "DEEPSEEK_MODEL",
                "deepseek-flash",
            ),

        "api_key":
            api_key,

        "base_url":
            os.getenv(
                "DEEPSEEK_BASE_URL",
                "https://api.deepseek.com",
            ),

        "timeout":
            60,

        "extra_body": {

            "thinking": {

                "type": (
                    "enabled"
                    if thinking
                    else "disabled"
                )
            }
        },
    }


    # Thinking Mode 下 temperature
    # 不起实际作用，所以只在非 Thinking
    # Structured Output 模型中设置。
    if not thinking:

        model_kwargs[
            "temperature"
        ] = 0


    return ChatOpenAI(
        **model_kwargs
    )


# ============================================================
# Knowledge Formatting
# ============================================================

def _format_knowledge(
    results: list[dict],
) -> str:

    blocks = []

    for result in results:

        blocks.append(

            (
                f"Source: {result['source']}\n"
                f"Score: {result['score']:.4f}\n"
                f"{result['text']}"
            )
        )

    return "\n\n---\n\n".join(
        blocks
    )

# ============================================================
# extract Tool Evidence
# ============================================================

def _collect_tool_evidence(
    state: DiagnosticState,
) -> str:

    observations = []

    for message in state["messages"]:

        if isinstance(
            message,
            ToolMessage,
        ):

            observations.append(
                (
                    f"Tool: {message.name}\n"
                    f"Result: {message.content}"
                )
            )

    if not observations:

        return "No additional tool evidence."

    return "\n\n".join(
        observations
    )

# ============================================================
# 格式化诊断
# ============================================================


def _render_diagnosis(
    diagnosis,
    validation,
    safety_reviews,
) -> str:

    lines = []

    lines.append(
        "===== STRUCTURED DIAGNOSIS ====="
    )

    lines.append(
        f"Fault Type: "
        f"{diagnosis.fault_type}"
    )

    lines.append(
        f"\nRoot Cause:\n"
        f"{diagnosis.root_cause}"
    )

    lines.append(
        "\nEvidence:"
    )


    for index, evidence in enumerate(
        diagnosis.evidence,
        start=1,
    ):

        field_text = (

            evidence.field

            if evidence.field

            else "TEXT"
        )


        lines.append(

            (
                f"{index}. "
                f"[{evidence.source}] "
                f"{field_text} = "
                f"{evidence.value}\n"
                f"   Supports: "
                f"{evidence.supports}"
            )
        )


    lines.append(
        "\nRecommendations:"
    )


    for recommendation in (
        diagnosis.recommendations
    ):

        lines.append(
            f"- {recommendation}"
        )


    lines.append(
        (
            "\nUncertainty:\n"
            f"{diagnosis.uncertainty}"
        )
    )


    lines.append(
        "\n===== EVIDENCE VALIDATION ====="
    )


    lines.append(
        (
            f"Valid: "
            f"{validation.valid}"
        )
    )


    lines.append(
        (
            "Unsupported Evidence: "
            f"{validation.unsupported_count}"
        )
    )


    for check in validation.checks:

        status = (
            "PASS"
            if check.grounded
            else "FAIL"
        )


        lines.append(

            (
                f"[{status}] "
                f"Evidence {check.index}: "
                f"{check.reason}"
            )
        )

    lines.append(
        "\n===== RECOVERY ACTION SAFETY ====="
    )


    if not safety_reviews:

        lines.append(
            "No executable recovery actions proposed."
        )


    for index, review in enumerate(
        safety_reviews,
        start=1,
    ):

        lines.append(
            (
                f"\nAction {index}: "
                f"{review.action.action}"
            )
        )

        lines.append(
            (
                f"Target: "
                f"{review.action.target}"
            )
        )

        lines.append(
            (
                f"Risk: "
                f"{review.risk_level.value}"
            )
        )

        lines.append(
            (
                f"Decision: "
                f"{review.decision.value}"
            )
        )

        lines.append(
            (
                f"Approval Required: "
                f"{review.approval_required}"
            )
        )

        lines.append(
            (
                f"Executable Now: "
                f"{review.executable}"
            )
        )

        lines.append(
            (
                f"Blocked: "
                f"{review.blocked}"
            )
        )

    return "\n".join(
        lines
    )

# ============================================================
# Build Graph
# ============================================================

def build_diagnostic_graph(
    tools,
    retriever,
    model=None,
):
    
    if model is None:

        model = build_model(
            thinking=True
        )


    # LLM 可以选择这些 Tools
    model_with_tools = (
        model.bind_tools(
            tools
        )
    )

    # ============================================================
    # Structured Diagnosis Model
    #
    # DeepSeek Thinking Mode 不支持
    # function_calling structured output
    # 所需要的 forced tool_choice。
    #
    # 因此最终结构化输出单独使用
    # non-thinking model。
    # ============================================================

    structured_model = (

        build_model(
            thinking=False
        )

        .with_structured_output(

            DiagnosisResult,

            method="function_calling",
        )
    )


    # 方便 initial_inspection
    # 直接按 Tool Name 调用
    tool_map = {

        tool.name: tool

        for tool in tools
    }


    # --------------------------------------------------------
    # Node 1: Initial Inspection
    # --------------------------------------------------------

    def initial_inspection(
        state: DiagnosticState,
    ):

        job_id = state["job_id"]


        status = tool_map[
            "get_job_status"
        ].invoke(
            {
                "job_id": job_id
            }
        )


        stderr = tool_map[
            "read_stderr"
        ].invoke(
            {
                "job_id": job_id
            }
        )


        initial_evidence = (

            "=== Initial Evidence ===\n\n"

            "get_job_status:\n"
            f"{status}\n\n"

            "read_stderr:\n"
            f"{stderr}"
        )


        # 工程分层，initial_evidence给 LLM 看，initial_evidence_data给 Runtime Validator 用

        return {

            "initial_evidence":
                initial_evidence,

            "initial_evidence_data": {

                "get_job_status":
                    status,

                "read_stderr":
                    stderr,
            },
        }


    # --------------------------------------------------------
    # Node 2: Reason
    # --------------------------------------------------------

    def reason(
        state: DiagnosticState,
    ):

        # 收集已经获得的 Tool Evidence
        tool_observations = []

        for message in state["messages"]:

            if isinstance(
                message,
                ToolMessage,
            ):

                tool_observations.append(

                    (
                        f"{message.name}:\n"
                        f"{message.content}"
                    )
                )


        evidence_for_retrieval = (

            state.get(
                "initial_evidence",
                "",
            )

            + "\n\n"

            + "\n\n".join(
                tool_observations
            )
        )


        # 每一轮 Reason 都根据
        # 当前 Evidence 更新知识检索
        knowledge_results = (
            retriever.search(

                evidence_for_retrieval,

                top_k=2,
            )
        )


        knowledge_context = (
            _format_knowledge(
                knowledge_results
            )
        )


        system_prompt = (
            REASON_SYSTEM_PROMPT.format(

                job_id=
                    state["job_id"],

                initial_evidence=
                    state.get(
                        "initial_evidence",
                        "",
                    ),

                knowledge_context=
                    knowledge_context,
            )
        )


        response = (
            model_with_tools.invoke(

                [
                    SystemMessage(
                        content=
                            system_prompt
                    ),
                    *state["messages"],
                ]
            )
        )


        return {

            "messages": [
                response
            ],

            "knowledge_context":
                knowledge_context,
        }


    # --------------------------------------------------------
    # Conditional Route
    # --------------------------------------------------------

    def route_after_reason(
        state: DiagnosticState,
    ):

        last_message = (
            state["messages"][-1]
        )


        tool_calls = getattr(

            last_message,

            "tool_calls",

            None,
        )


        if tool_calls:

            return "tools"


        return "diagnosis"


    # --------------------------------------------------------
    # Node 4: Final Diagnosis
    # --------------------------------------------------------

    def diagnosis(
        state: DiagnosticState,
    ):

        # ========================================================
        # Collect Real Tool Evidence
        # ========================================================

        tool_evidence = (
            _collect_tool_evidence(
                state
            )
        )


        # ========================================================
        # Build Final Prompt
        # ========================================================

        final_prompt = (
            FINAL_DIAGNOSIS_PROMPT.format(

                job_id=
                    state["job_id"],

                initial_evidence=
                    state.get(
                        "initial_evidence",
                        "",
                    ),

                tool_evidence=
                    tool_evidence,

                knowledge_context=
                    state.get(
                        "knowledge_context",
                        "",
                    ),
            )
        )


        # ========================================================
        # Structured LLM
        # ========================================================


        diagnosis_result = (
            structured_model.invoke(

                [
                    SystemMessage(
                        content=
                            final_prompt
                    ),

                    HumanMessage(
                        content=(
                            "请根据以上真实 Evidence "
                            "生成最终结构化诊断。"
                        )
                    ),
                ]
            )
        )

        # ============================================================
        # Safety Review
        # ============================================================

        safety_reviews = (
            review_actions(
                diagnosis_result.recovery_actions
            )
        )        

        # ========================================================
        # Runtime Evidence Store
        # ========================================================

        evidence_store = (
            build_evidence_store(

                initial_evidence_data=
                    state.get(
                        "initial_evidence_data",
                        {},
                    ),

                messages=
                    state["messages"],
            )
        )


        # ========================================================
        # Deterministic Evidence Validation
        # ========================================================

        validation_report = (
            validate_evidence(

                diagnosis=
                    diagnosis_result,

                evidence_store=
                    evidence_store,
            )
        )

        # ============================================================
        # Safety Review
        # ============================================================

        safety_reviews = (
            review_actions(
                diagnosis_result.recovery_actions
            )
        )


        # ========================================================
        # Human-readable Output
        # ========================================================

        final_text = (
            _render_diagnosis(

                diagnosis=
                    diagnosis_result,

                validation=
                    validation_report,

                safety_reviews=
                    safety_reviews,
            )
        )


        return {

            "diagnosis":
                diagnosis_result,

            "evidence_validation":
                validation_report,

            "safety_reviews":
                safety_reviews,

            "messages": [

                AIMessage(
                    content=
                        final_text
                )
            ],
        }

    # ========================================================
    # Graph
    # ========================================================

    builder = StateGraph(
        DiagnosticState
    )


    builder.add_node(

        "initial_inspection",

        initial_inspection,
    )


    builder.add_node(

        "reason",

        reason,
    )


    builder.add_node(

        "tools",

        ToolNode(
            tools
        ),
    )


    builder.add_node(

        "diagnosis",

        diagnosis,
    )


    builder.add_edge(

        START,

        "initial_inspection",
    )


    builder.add_edge(

        "initial_inspection",

        "reason",
    )


    builder.add_conditional_edges(

        "reason",

        route_after_reason,

        {
            "tools":
                "tools",

            "diagnosis":
                "diagnosis",
        },
    )


    builder.add_edge(

        "tools",

        "reason",
    )


    builder.add_edge(

        "diagnosis",

        END,
    )


    return builder.compile()