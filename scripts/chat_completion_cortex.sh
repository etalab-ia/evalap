#!/usr/bin/env bash

models_and_urls=(
  "https://model1.multivacplatform.org/v1|$CORTEX_API_KEY|meta-llama/Llama-3.2-3B-Instruct"
  "https://model2.multivacplatform.org/v1|$CORTEX_API_KEY|deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
  "https://model4.multivacplatform.org/v1|$CORTEX_API_KEY|meta-llama/Llama-3.3-70B-Instruct"
)

for entry in "${models_and_urls[@]}"; do
  IFS='|' read -r url key model <<< "$entry"

  curl "$url/chat/completions" \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer $key" \
       -d '{
         "model": "'"$model"'",
         "messages": [
           {"role": "system", "content": "Answer dramatically and with emojis."},
           {"role": "user", "content": "Combien de fois '\''p'\'' dans développer ? Combien font 2*10+50-20 ?"}
         ]
         }' | jq
  done
