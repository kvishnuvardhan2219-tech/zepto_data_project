import os
from fastapi import FastAPI
from schemas import AskRequest, AskResponse
from graph import build_graph


app = FastAPI(title="Zepto support assistant", version="1.0")
graph = build_graph()


@app.get("/")
def health():
    return {"status": "ok", "message": "Zepto support assistant is running"}

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    """
    Main endpoint.
    Accepts: {"query": "your question"}
    Returns: {"answer": "___", "sources": [___], "confidence": 1.0}}
    """
    
    result = graph.invoke({"query": request.query})
    
    return AskResponse(
        answer = result["answer"],
        sources=result["sources"],
        confidence=result["confidence"]
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=True)
