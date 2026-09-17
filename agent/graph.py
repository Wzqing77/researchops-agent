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


# ============================================================
# Model
# ============================================================

def build_model():

    load_dotenv()

    api_key = os.getenv(
        "DEEPSEEK_API_KEY"
    )

    if not api_key:

        raise RuntimeError(
            "DEEPSEEK_API_KEY is missing."
        )

    return ChatOpenAI(

        model=os.getenv(
            "DEEPSEEK_MODEL",
            "deepseek-flash",
        ),

        api_key=api_key,

        base_url=os.getenv(
            "DEEPSEEK_BASE_URL",
            "https://api.deepseek.com",
        ),

        temperature=0,

        timeout=60,
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
# Build Graph
# ============================================================

def build_diagnostic_graph(
    tools,
    retriever,
    model=None,
):

    if model is None:

        model = build_model()


    # LLM 可以选择这些 Tools
    model_with_tools = (
        model.bind_tools(
            tools
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


        return {

            "initial_evidence":
                initial_evidence
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

        tool_evidence = (
            _collect_tool_evidence(
                state
            )
        )

        final_prompt = (
            FINAL_DIAGNOSIS_PROMPT.format(
                job_id=state["job_id"],

                initial_evidence=state.get(
                    "initial_evidence",
                    "",
                ),

                tool_evidence=tool_evidence,

                knowledge_context=state.get(
                    "knowledge_context",
                    "",
                ),
            )
        )


        response = model.invoke(

            [
                SystemMessage(
                    content=
                        final_prompt
                ),

                *state["messages"],
            ]
        )


        return {

            "messages": [
                response
            ]
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