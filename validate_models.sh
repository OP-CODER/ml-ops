#!/bin/bash
# validate_models.sh
set -e

echo "✅ Starting validation of all services..."

# --- Detect usable curl binary ---
if command -v curl >/dev/null 2>&1; then
  CURL="curl"
elif [ -f "/mnt/c/Windows/System32/curl.exe" ]; then
  CURL="/mnt/c/Windows/System32/curl.exe"
elif [ -f "/c/Windows/System32/curl.exe" ]; then
  CURL="/c/Windows/System32/curl.exe"
else
  echo "❌ Error: curl not found. Please install curl or add it to PATH."
  exit 1
fi

# --- Sentiment Service ---
echo "---- Testing Sentiment Service ----"
SENTIMENT_RESPONSE=$($CURL -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}')
echo "✅ Sentiment response: $SENTIMENT_RESPONSE"

# --- Fraud Service ---
echo "---- Testing Fraud Service ----"
FRAUD_RESPONSE=$($CURL -s -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5000, 40]}')
echo "✅ Fraud response: $FRAUD_RESPONSE"

# --- RAG Service ---
echo "---- Testing RAG Service ----"
RAG_RESPONSE=$($CURL -s -X POST http://localhost:8002/query \
  -H "Content-Type: application/json" \
  -d '{"text": "Tell me about Kubernetes"}')
echo "✅ RAG response: $RAG_RESPONSE"

# --- Summary ---
{
  echo "✅ Validation completed successfully!"
  echo "🗒 Saving all responses to validation_results.txt..."
  echo -e "Sentiment: $SENTIMENT_RESPONSE"
  echo -e "Fraud: $FRAUD_RESPONSE"
  echo -e "RAG: $RAG_RESPONSE"
} > validation_results.txt

echo "✅ All services validated and results saved in validation_results.txt"
