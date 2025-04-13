set quiet

work_dir := `pwd`

default:
  just --list

clean:
  rm -rf build/ eg1.egg-info/

#
# Openai API utils
#

list-model provider="albert":
  #!/usr/bin/env sh
  if [ "{{provider}}" = "albert" ]; then
    URL="https://albert.api.etalab.gouv.fr/v1"
    API_KEY=$ALBERT_API_KEY
  elif [ "{{provider}}" = "albert-staging" ]; then
    URL="https://albert.api.staging.etalab.gouv.fr/v1"
    API_KEY=$ALBERT_API_KEY_STAGING
  elif [ "{{provider}}" = "openai" ]; then
    URL="https://api.openai.com/v1"
    API_KEY=$OPENAI_API_KEY
  elif [ "{{provider}}" = "anthropic" ]; then
    URL="https://api.anthropic.com/v1"
    API_KEY=$ANTHROPIC_API_KEY
  elif [ "{{provider}}" = "mistral" ]; then
    URL="https://api.mistral.ai/v1"
    API_KEY=$MISTRAL_API_KEY
  fi

  curl -XGET -H "Authorization: Bearer $API_KEY" $URL/models | jq '[.data.[] | {id, type, owned_by, aliases}]'

chat-completion model="mistralai/Mistral-Small-3.1-24B-Instruct-2503" provider="albert":
  #!/usr/bin/env sh
  if [ "{{provider}}" = "albert" ]; then
    URL="https://albert.api.etalab.gouv.fr/v1"
    API_KEY=$ALBERT_API_KEY
  elif [ "{{provider}}" = "albert-staging" ]; then
    URL="https://albert.api.staging.etalab.gouv.fr/v1"
    API_KEY=$ALBERT_API_KEY_STAGING
  elif [ "{{provider}}" = "openai" ]; then
    URL="https://api.openai.com/v1"
    API_KEY=$OPENAI_API_KEY
  elif [ "{{provider}}" = "anthropic" ]; then
    URL="https://api.anthropic.com/v1"
    API_KEY=$ANTHROPIC_API_KEY
  elif [ "{{provider}}" = "mistral" ]; then
    URL="https://api.mistral.ai/v1"
    API_KEY=$MISTRAL_API_KEY
  fi

  curl  "$URL/chat/completions" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $API_KEY" \
      -d '{
        "model": "{{model}}",
        "messages": [
          {"role": "system", "content": "Answer dramatically and with emojis."},
          {"role": "user", "content": "Combien de fois 'p' dans développer ? Combien font 2*10+50-20 ?"}
        ]
      }' 

chat-completion-cortex:
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
             {"role": "user", "content": "Combien de fois 'p' dans développer ? Combien font 2*10+50-20 ?"}
           ]
           }' | jq
    done


#
# Alembic commands
#

alembic-init:
  alembic -c eg1/api/alembic.ini revision --autogenerate -m "Table Initialization"

alembic-generate-revision name:
  alembic -c eg1/api/alembic.ini upgrade head
  alembic -c eg1/api/alembic.ini revision --autogenerate -m "{{name}}"

alembic-upgrade:
  alembic -c eg1/api/alembic.ini upgrade head

alembic-downgrade hash:
  alembic -c eg1/api/alembic.ini downgrade {{hash}}

alembic-history:
  alembic -c eg1/api/alembic.ini history

#
# Search engine
#

list-indexes env="dev":
  #!/usr/bin/env sh
  if [ "{{env}}" = "dev" ]; then
    curl -u elastic:$ELASTICSEARCH_PASSWORD -X GET "$ELASTICSEARCH_URL/_cat/indices?v"
  elif [ "{{env}}" = "staging" ]; then
    curl -u elastic:$ELASTICSEARCH_PASSWORD -X GET "$ELASTICSEARCH_URL/_cat/indices?v"
  elif [ "{{env}}" = "prod" ]; then
    curl -u elastic:$ELASTICSEARCH_PASSWORD -X GET "$ELASTICSEARCH_URL/_cat/indices?v"
  fi


#
# DB Queries
#

[no-cd]
drop-database db_name="eg1_dev":
  #!/usr/bin/env python
  # Does not work !
  import sys, os; sys.path.append("{{work_dir}}")
  from eg1.api.config import DATABASE_URI

  DB_NAME = "{{db_name}}"
  PGURI = DATABASE_URI.replace("+psycopg2", "")
  command = f'psql {PGURI} -c "DROP DATABASE {DB_NAME} WITH (FORCE);"'
  os.system(command)

[no-cd]
drop-table table_name:
  #!/usr/bin/env python
  import sys, os; sys.path.append("{{work_dir}}")
  from eg1.api.config import DATABASE_URI

  TABLE_NAME = "{{table_name}}"
  PGURI = DATABASE_URI.replace("+psycopg2", "")
  command = f'psql "{PGURI}" -c "DROP TABLE IF EXISTS {TABLE_NAME};"'
  exit_status = os.system(command)

[no-cd]
reset-experiment-status *expids:
  #!/usr/bin/env python
  import sys, os; sys.path.append("{{work_dir}}")
  from eg1.api.config import DATABASE_URI

  PGURI = DATABASE_URI.replace("+psycopg2", "")
  expids = "{{expids}}".split()
  req = f"""
    UPDATE experiments
    SET experiment_status = 'finished'
    WHERE id IN ({", ".join(expids)});
  """.strip().replace("\n", " ")
  command = f'psql "{PGURI}" -c "{req}"'
  exit_status = os.system(command)

[no-cd]
get-experiment expid:
  #!/usr/bin/env python
  import sys, os; sys.path.append("{{work_dir}}")
  from eg1.api.config import DATABASE_URI

  PGURI = DATABASE_URI.replace("+psycopg2", "")
  expid = "{{expid}}"
  req = f"""
    SELECT json_agg(row_to_json(t)) FROM (
      SELECT *
      FROM experiments
      WHERE id = {expid}
    ) t;
  """.strip()
  command = f'psql "{PGURI}" -t -P pager=off -c "{req}" | jq'
  exit_status = os.system(command)

rainfrog:
  rainfrog --url postgres://postgres:changeme@localhost:5432/eg1_dev

