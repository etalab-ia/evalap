#!/usr/bin/env python
import sys
from pathlib import Path

import psycopg2
from psycopg2 import sql

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from evalap.api.config import DATABASE_URI

if len(sys.argv) < 2:
    print("Usage: drop_database.py <db_name>")
    sys.exit(1)

DB_NAME = sys.argv[1]

try:
    conn = psycopg2.connect(DATABASE_URI.replace("+psycopg2", ""))
    conn.autocommit = True
    cur = conn.cursor()

    # Use sql.Identifier to safely quote the database name
    cur.execute(sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(DB_NAME)))

    cur.close()
    conn.close()
    print(f"Database {DB_NAME} dropped successfully.")
except Exception as e:
    print(f"Error dropping database: {e}")
    sys.exit(1)
