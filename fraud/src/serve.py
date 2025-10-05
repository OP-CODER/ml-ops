from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Fraud/Churn Demo")
model = joblib.load("model/model.joblib")

class Input(BaseModel):
    features: list  # e.g. [0.1, 1.2, ...]

@app.post("/predict")
def predict(inp: Input):
    x = np.array(inp.features).reshape(1, -1)
    pred = int(model.predict(x)[0])
    prob = None
    if hasattr(model, "predict_proba"):
        prob = float(model.predict_proba(x).max())
    return {"prediction": pred, "probability": prob}
