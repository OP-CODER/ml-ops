import os
import joblib
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Optional MLflow logging if you have MLflow: wrap gracefully
try:
    import mlflow
    mlflow_available = True
except Exception:
    mlflow_available = False

def main():
    X, y = load_breast_cancer(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=1000)
    if mlflow_available:
        mlflow.start_run()
        mlflow.log_param("model", "LogisticRegression")

    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print("Test accuracy:", acc)
    print(classification_report(y_test, preds))

    if mlflow_available:
        mlflow.log_metric("accuracy", float(acc))
        mlflow.end_run()

    os.makedirs("model", exist_ok=True)
    joblib.dump(model, "model/model.joblib")
    print("Saved model to model/model.joblib")

if __name__ == "__main__":
    main()
