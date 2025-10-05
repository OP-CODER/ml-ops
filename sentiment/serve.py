# sentiment/serve.py
from fastapi import FastAPI
import joblib
from pydantic import BaseModel

class Payload(BaseModel):
    text: str

app = FastAPI()
model = joblib.load("models/sentiment.pkl")  # Ensure this exists via train.py

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/predict")
def predict(payload: Payload):
    pred = model.predict([payload.text])
    return {"label": int(pred[0]), "score": 0.99}
