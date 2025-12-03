#!/usr/bin/env python
import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from evalap.api.config import DATABASE_URI

if len(sys.argv) < 2:
    print("Usage: drop_database.py <db_name>")
    sys.exit(1)

DB_NAME = sys.argv[1]
PGURI = DATABASE_URI.replace("+psycopg2", "")
command = f'psql {PGURI} -c "DROP DATABASE {DB_NAME} WITH (FORCE);"'
os.system(command)
