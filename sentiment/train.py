# sentiment/train.py
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import os

SAMPLE_DATA = [
    ("I love this product", 1),
    ("I hate this", 0),
    ("This is great", 1),
    ("This is awful", 0),
]

def train(output_path="models/sentiment.pkl"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    X = [t for t,_ in SAMPLE_DATA]
    y = [l for _,l in SAMPLE_DATA]
    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=500))
    ])
    model.fit(X,y)
    joblib.dump(model, output_path)
    print("✅ Saved model to", output_path)

if __name__ == "__main__":
    train()
