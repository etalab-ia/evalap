#!/usr/bin/env python
import json
import sys
from pathlib import Path

import psycopg2

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from evalap.api.config import DATABASE_URI

if len(sys.argv) < 2:
    print("Usage: get_experiment.py <expid>")
    sys.exit(1)

expid = sys.argv[1]

try:
    conn = psycopg2.connect(DATABASE_URI.replace("+psycopg2", ""))
    cur = conn.cursor()

    query = """
      SELECT json_agg(row_to_json(t)) FROM (
        SELECT *
        FROM experiments
        WHERE id = %s
      ) t;
    """
    cur.execute(query, (expid,))
    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    if result:
        print(json.dumps(result, indent=2))
    else:
        print("[]")

except Exception as e:
    print(f"Error getting experiment: {e}")
    sys.exit(1)
