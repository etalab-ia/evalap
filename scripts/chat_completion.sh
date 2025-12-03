#!/usr/bin/env sh

MODEL="$1"
PROVIDER="${2:-albert}"

if [ "$PROVIDER" = "albert" ]; then
  URL="https://albert.api.etalab.gouv.fr/v1"
  API_KEY=$ALBERT_API_KEY
elif [ "$PROVIDER" = "albert-staging" ]; then
  URL="https://albert.api.staging.etalab.gouv.fr/v1"
  API_KEY=$ALBERT_API_KEY_STAGING
elif [ "$PROVIDER" = "openai" ]; then
  URL="https://api.openai.com/v1"
  API_KEY=$OPENAI_API_KEY
elif [ "$PROVIDER" = "anthropic" ]; then
  URL="https://api.anthropic.com/v1"
  API_KEY=$ANTHROPIC_API_KEY
elif [ "$PROVIDER" = "mistral" ]; then
  URL="https://api.mistral.ai/v1"
  API_KEY=$MISTRAL_API_KEY
fi

curl "$URL/chat/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $API_KEY" \
    -d '{
      "model": "'"$MODEL"'",
      "messages": [
        {"role": "system", "content": "Answer dramatically and with emojis."},
        {"role": "user", "content": "Combien de fois '\''p'\'' dans développer ? Combien font 2*10+50-20 ?"}
      ]
    }'
