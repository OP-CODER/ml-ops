# rag/buildindex.py
import faiss
import numpy as np
import os
import pickle

# Sample documents
docs = [
    "FastAPI is a modern web framework",
    "Docker helps containerize applications",
    "Kubernetes manages container orchestration",
]

# Simple vectorization using random embeddings (for demo purposes)
dim = 128
embeddings = np.random.rand(len(docs), dim).astype('float32')

# Create FAISS index
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

os.makedirs("index", exist_ok=True)
faiss.write_index(index, "index/faiss.index")

# Save docs
with open("index/docs.pkl", "wb") as f:
    pickle.dump(docs, f)

print("✅ RAG index and docs saved to index/")
