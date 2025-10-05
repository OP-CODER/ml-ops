# rag/serve.py
from fastapi import FastAPI
import faiss
import numpy as np
import pickle
from prometheus_fastapi_instrumentator import Instrumentator  # ✅ Added

app = FastAPI(title="RAG Service")

# Load FAISS index and documents
index = faiss.read_index("index/faiss.index")
with open("index/docs.pkl", "rb") as f:
    docs = pickle.load(f)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query")
def query(payload: dict):
    text = payload.get("text", "")
    # Fake query embedding for demo purposes
    query_vec = np.random.rand(1, 128).astype("float32")
    D, I = index.search(query_vec, k=1)
    return {"query": text, "result": docs[I[0][0]]}

# ✅ Expose Prometheus metrics endpoint
Instrumentator().instrument(app).expose(app)

