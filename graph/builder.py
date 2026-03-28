from langgraph.graph import StateGraph
from graph.state import State

from nodes.preprocess import preprocess_node
from nodes.detection import detection_node
from nodes.gradcam import gradcam_node
from nodes.context import context_node
from nodes.reasoning import reasoning_node
from nodes.policy import policy_node
from nodes.doctor import senior_doctor_node, junior_doctor_node
from nodes.report import final_report_node
from nodes.merge_node import merge_node

def build_graph():

    builder = StateGraph(State)

    builder.add_node("preprocess", preprocess_node)
    builder.add_node("detect", detection_node)
    builder.add_node("gradcam", gradcam_node)
    builder.add_node("context", context_node)
    builder.add_node("reasoning", reasoning_node)
    builder.add_node("policy", policy_node)
    builder.add_node("senior", senior_doctor_node)
    builder.add_node("junior", junior_doctor_node)
    builder.add_node("final", final_report_node)
    builder.add_node("merge", merge_node)

    builder.set_entry_point("preprocess")

    builder.add_edge("preprocess", "detect")
    builder.add_edge("detect", "gradcam")
    builder.add_edge("gradcam", "merge")
    builder.add_edge("merge", "context")
    builder.add_edge("context", "reasoning")
    builder.add_edge("reasoning", "policy")

    builder.add_conditional_edges(
        "policy",
        lambda s: "senior" if s["decision"] == "SENIOR" else "junior",
        {
            "senior": "senior",
            "junior": "junior"
        }
    )

    builder.add_edge("senior", "final")
    builder.add_edge("junior", "final")

    builder.set_finish_point("final")

    return builder.compile()