#!/usr/bin/env sh

ENV="${1:-dev}"

if [ "$ENV" = "dev" ]; then
  curl -u elastic:$ELASTICSEARCH_PASSWORD -X GET "$ELASTICSEARCH_URL/_cat/indices?v"
elif [ "$ENV" = "staging" ]; then
  curl -u elastic:$ELASTICSEARCH_PASSWORD -X GET "$ELASTICSEARCH_URL/_cat/indices?v"
elif [ "$ENV" = "prod" ]; then
  curl -u elastic:$ELASTICSEARCH_PASSWORD -X GET "$ELASTICSEARCH_URL/_cat/indices?v"
fi
