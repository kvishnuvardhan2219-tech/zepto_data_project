import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END 
import chromadb 
from sentence_transformers import SentenceTransformer
from prompt_template import PROMPT_TEMPLATE

MOCK_LLM = os.environ.get("MOCK_LLM", "1")

POLICY_KEYWORDS = ["delivery", "return", "refund", "membership", "tracking", "cancel", "gift card", "support hours"]

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="zepto_policies")

class GraphState(TypedDict):
    query: str
    intent: str
    answer: str
    sources: List[str]
    confidence: float


def classify_intent(state: GraphState) -> GraphState:
    query_lower = state["query"].lower()

    if MOCK_LLM != "0":

        if any(keyword in query_lower for keyword in POLICY_KEYWORDS):
            intent = "policy_question"
        else:
            intent = "general_question"

    else:

        if any(keyword in query_lower for keyword in POLICY_KEYWORDS):
            intent = "policy_question"

        else:
            intent = "general_question"

    state["intent"] = intent
    return state

def retrieve_and_answer(state: GraphState) -> GraphState:
    query = state["query"]

    query_embedding = embed_model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=3)

    retrieved_ids = results["ids"][0]
    retrieved_docs = results["documents"][0]

    top_chunk = retrieved_docs[0]
    top_chunk_snippet = top_chunk[:200]

    if MOCK_LLM != "0":

        answer = f"Based on the retrieved context: {top_chunk_snippet}"

    else:

        context = "\n".join(retrieved_docs)
        prompt = PROMPT_TEMPLATE.format(context=context, question=query)
        answer = f"[Real LLM call would use this prompt]: {prompt[:200]}"


    state["answer"] = answer
    state["sources"] = retrieved_ids
    state["confidence"]  = 1.0
    return state


def direct_answer(state: GraphState) -> GraphState:
    if MOCK_LLM !="0":
        answer = " I can only answer questions about Zepto policies right now."
    else:
        answer = " I can only answer questions about Zepto policies right now."


    state["answer"] = answer
    state["sources"] = []
    state["confidence"] = 1.0
    return state


def route_by_intent(state: GraphState) -> str:
    if state["intent"] == "policy_question":
        return "retrieve_and_answer"
    else:
        return "direct_answer"


def build_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("classify_intent", classify_intent)
    workflow.add_node("retrieve_and_answer", retrieve_and_answer)
    workflow.add_node("direct_answer", direct_answer)

    workflow.set_entry_point("classify_intent")

    workflow.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "retrieve_and_answer": "retrieve_and_answer",
            "direct_answer": "direct_answer"
        }
    )

    workflow.add_edge("retrieve_and_answer", END)
    workflow.add_edge("direct_answer", END)

    return workflow.compile()