#!/usr/bin/env python
import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from evalap.api.config import DATABASE_URI

if len(sys.argv) < 2:
    print("Usage: reset_experiment_status.py <expid1> [expid2 ...]")
    sys.exit(1)

PGURI = DATABASE_URI.replace("+psycopg2", "")
expids = sys.argv[1:]
req = f"""
  UPDATE experiments
  SET experiment_status = 'finished'
  WHERE id IN ({", ".join(expids)});
""".strip().replace("\n", " ")
command = f'psql "{PGURI}" -c "{req}"'
exit_status = os.system(command)
sys.exit(exit_status)
