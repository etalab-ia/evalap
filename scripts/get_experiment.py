#!/usr/bin/env python
import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from evalap.api.config import DATABASE_URI

if len(sys.argv) < 2:
    print("Usage: get_experiment.py <expid>")
    sys.exit(1)

PGURI = DATABASE_URI.replace("+psycopg2", "")
expid = sys.argv[1]
req = f"""
  SELECT json_agg(row_to_json(t)) FROM (
    SELECT *
    FROM experiments
    WHERE id = {expid}
  ) t;
""".strip()
command = f'psql "{PGURI}" -t -P pager=off -c "{req}" | jq'
exit_status = os.system(command)
sys.exit(exit_status)
