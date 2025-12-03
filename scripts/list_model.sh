#!/usr/bin/env sh

PROVIDER="${1:-albert}"

if [ "$PROVIDER" = "albert" ]; then
  URL="https://albert.api.etalab.gouv.fr/v1"
  API_KEY=$ALBERT_API_KEY
elif [ "$PROVIDER" = "albert-staging" ]; then
  URL="https://albert.api.staging.etalab.gouv.fr/v1"
  API_KEY=$ALBERT_API_KEY_STAGING
elif [ "$PROVIDER" = "albert-dev" ]; then
  URL="https://albert.api.dev.etalab.gouv.fr/v1"
  API_KEY=$ALBERT_API_KEY_DEV
elif [ "$PROVIDER" = "anthropic" ]; then
  URL="https://api.anthropic.com/v1"
  API_KEY=$ANTHROPIC_API_KEY
  curl -XGET -H "x-api-key: $API_KEY" -H "anthropic-version: 2023-06-01" $URL/models | jq '[.data.[] | {id, type, owned_by, aliases}]'
  exit 0
elif [ "$PROVIDER" = "openai" ]; then
  URL="https://api.openai.com/v1"
  API_KEY=$OPENAI_API_KEY
elif [ "$PROVIDER" = "mistral" ]; then
  URL="https://api.mistral.ai/v1"
  API_KEY=$MISTRAL_API_KEY
elif [ "$PROVIDER" = "xai" ]; then
  URL="https://api.x.ai/v1"
  API_KEY=$XAI_API_KEY
elif [ "$PROVIDER" = "mammouth" ]; then
  URL="https://api.mammouth.ai/v1"
  API_KEY=$MAMMOUTH_API_KEY
fi

curl -XGET -H "Authorization: Bearer $API_KEY" $URL/models | jq '[.data.[] | {id, type, owned_by, aliases}]'
