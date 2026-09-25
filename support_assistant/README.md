# Zepto Support Assistant (Module 3)

A complete offline-first RAG + LangGraph + FastAPI service that answers Zepto policy questions grounded in Zepto's own documents.

## Setup

```bash
cd support_assistant
pip install -r requirements.txt
```

ONE-time setup (create documents+embed them):
```bash
python create_docs.py
python ingest.py
```

RUN the API locally:
```bash

uvicorn main:app --host 0.0.0.0 --port 8000

```

## Example calls(MOCK_LLM default = MOCK mode)
### 1.policy question(triggers retrieval)

Request:
```bash
curl -X POST "http://127.0.0.1:8000/ask" -H "content-Type: application/json"  -d '{"query": "What is the delivery fee?"}'
```

response:
```json

{
    "answer": "Based on the retrived context: Zepto delivers grocery and household essentials to serviceable pin codes within 10 to 30 minutes of order confirmation, depending on the customer's delivery zone and current order volume. standard del",
    "sources": ["doc_01","doc_05","doc_02"],
    "confidence": 1.0
}
```

### 2. General question( no retrieval)
```bash
curl -X POST "http://127.0.0.1:8000/ask" -H "content-Type: application/json"  -d "{\"query\": \"What is the weather today?\"}"
```

reponse:
```json
{
    "answer": "I can only answer questions about Zepto policies right now.",
    "sources": [],
    "confidence": 1.0
}
```

# Architecture (RAG pipeline)
1. **ingestion** -> create_docs.py writes the 8 exact policy documents into doc/
2. **Embedding** -> ingest.py loads the documents, embeds them the all-MiniLM-L6-v2, and stores vectors in ChromaDB collection zepto_policies.
3. **Retrieval** -> LangGraph node retrieve_and_answer embeds the query and fetches top-3 chunks via cosine similarity (always runs, no API key needed).
4. **Generation** ->
    - classify_intent uses a keyword heuristic (MOCK_LLM default).
    - routes to retrieve_and_answer or direct_answer.
    - Mock mode returns canned answers; optional MOCK_LLM=0 path is prepared for a real LLM.

The only stage that branches on MOCK_LLM is the final answer generation inside the two answer nodes.


# Docker(local)

```bash
docker build -t zepto-support .
docker run -p 7860:7860 zepto-support 
```

Then call the same /ask endpoint on http://localhost:7860/ask .