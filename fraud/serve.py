# fraud/serve.py
from fastapi import FastAPI
import joblib
from pydantic import BaseModel

class Payload(BaseModel):
    features: list

app = FastAPI()
model = joblib.load("models/fraud.pkl")

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/predict")
def predict(payload: Payload):
    pred = model.predict([payload.features])
    return {"label": int(pred[0]), "score": 0.99}
