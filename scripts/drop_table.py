#!/usr/bin/env python
import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from evalap.api.config import DATABASE_URI

if len(sys.argv) < 2:
    print("Usage: drop_table.py <table_name>")
    sys.exit(1)

TABLE_NAME = sys.argv[1]
PGURI = DATABASE_URI.replace("+psycopg2", "")
command = f'psql "{PGURI}" -c "DROP TABLE IF EXISTS {TABLE_NAME};"'
exit_status = os.system(command)
sys.exit(exit_status)
