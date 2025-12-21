#!/usr/bin/env python
import sys
from pathlib import Path

import psycopg2

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from evalap.api.config import DATABASE_URI

if len(sys.argv) < 2:
    print("Usage: reset_experiment_status.py <expid1> [expid2 ...]")
    sys.exit(1)

expids = sys.argv[1:]

try:
    conn = psycopg2.connect(DATABASE_URI.replace("+psycopg2", ""))
    conn.autocommit = True
    cur = conn.cursor()

    # Use parameterized query to safely update experiments
    query = "UPDATE experiments SET experiment_status = 'finished' WHERE id = ANY(%s)"
    cur.execute(query, (expids,))

    cur.close()
    conn.close()
    print(f"Updated status for experiments: {', '.join(expids)}")
except Exception as e:
    print(f"Error updating experiment status: {e}")
    sys.exit(1)
