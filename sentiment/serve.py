from fastapi import FastAPI
import joblib
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Sentiment Analysis API")

# Load model
model = joblib.load("models/sentiment.pkl")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: dict):
    text = payload.get("text", "")
    pred = model.predict([text])[0]
    return {"label": "positive" if pred == 1 else "negative"}

# ✅ Enable Prometheus metrics
Instrumentator().instrument(app).expose(app)
