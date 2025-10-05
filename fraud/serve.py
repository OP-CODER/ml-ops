# fraud/serve.py
from fastapi import FastAPI
import joblib
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator  # ✅ Added

class Payload(BaseModel):
    features: list

app = FastAPI(title="Fraud Detection API")

# Load model
model = joblib.load("models/fraud.pkl")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: Payload):
    pred = model.predict([payload.features])
    return {"label": int(pred[0]), "score": 0.99}

# ✅ Enable Prometheus metrics endpoint
Instrumentator().instrument(app).expose(app)
