# fraud/train.py
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import os

# Sample dataset: features [amount, age], label 0=non-fraud, 1=fraud
SAMPLE_DATA = [
    ([100, 25], 0),
    ([5000, 40], 1),
    ([200, 22], 0),
    ([7000, 35], 1)
]

def train(output_path="models/fraud.pkl"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    X = [x for x,_ in SAMPLE_DATA]
    y = [l for _,l in SAMPLE_DATA]
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=500))
    ])
    model.fit(X,y)
    joblib.dump(model, output_path)
    print("✅ Saved model to", output_path)

if __name__ == "__main__":
    train()
