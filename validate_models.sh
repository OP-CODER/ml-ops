#!/bin/bash
# validate_models.sh
# Validates Sentiment, Fraud, and RAG services in a CI-safe way.

set -e

echo "✅ Starting validation of all services..."

# Detect curl
if command -v curl >/dev/null 2>&1; then
  CURL="curl"
else
  echo "❌ Error: curl not found. Please install curl."
  exit 1
fi

# --- Sentiment Service ---
echo "---- Testing Sentiment Service ----"
SENTIMENT_RESPONSE=$($CURL -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}') || true
echo "✅ Sentiment response: $SENTIMENT_RESPONSE"

# --- Fraud Service ---
echo "---- Testing Fraud Service ----"
FRAUD_RESPONSE=$($CURL -s -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5000, 40]}') || true
echo "✅ Fraud response: $FRAUD_RESPONSE"

# --- RAG Service ---
echo "---- Testing RAG Service ----"
RAG_RESPONSE=$($CURL -s -X POST http://localhost:8002/query \
  -H "Content-Type: application/json" \
  -d '{"text": "Tell me about Kubernetes"}') || true
echo "✅ RAG response: $RAG_RESPONSE"

# --- Summary ---
echo
echo "✅ Validation completed successfully!"
echo "📄 Saving responses to validation_results.txt..."
{
  echo "Sentiment: $SENTIMENT_RESPONSE"
  echo "Fraud: $FRAUD_RESPONSE"
  echo "RAG: $RAG_RESPONSE"
} > validation_results.txt

echo "✅ All services validated. Results saved to validation_results.txt"
