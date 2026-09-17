# 整个 Graph 在节点之间共享的运行状态

from typing_extensions import NotRequired

from langgraph.graph import MessagesState


class DiagnosticState(MessagesState):
    """
    ResearchOps LangGraph State。

    messages:
        Agent 与 Tool 的消息历史。

    job_id:
        当前正在诊断的 HPC Job ID。

    initial_evidence:
        initial_inspection 阶段获取的最小初始证据。

    knowledge_context:
        RAG 检索得到的 HPC Domain Knowledge。
    """

    job_id: str

    initial_evidence: NotRequired[str]

    knowledge_context: NotRequired[str]