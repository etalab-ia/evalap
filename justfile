set quiet

work_dir := `pwd`

default:
  just --list

alembic-init:
  alembic -c api/alembic.ini revision --autogenerate -m "Table Initialization"

alembic-upgrade:
  alembic -c api/alembic.ini upgrade head

alembic-history:
  alembic -c api/alembic.ini history

[no-cd]
drop-database db_name="eg1_dev":
  #!/usr/bin/env python
  # Does not work !
  import sys, os; sys.path.append("{{work_dir}}")
  from api.config import DATABASE_URI

  DB_NAME = "{{db_name}}"
  PGURI = DATABASE_URI.replace("+psycopg2", "")
  command = f'psql {PGURI} -c "DROP DATABASE {DB_NAME} WITH (FORCE);"'
  os.system(command)

[no-cd]
drop-table table_name:
  #!/usr/bin/env python
  import sys, os; sys.path.append("{{work_dir}}")
  from api.config import DATABASE_URI

  TABLE_NAME = "{{table_name}}"
  PGURI = DATABASE_URI.replace("+psycopg2", "")
  command = f'psql "{PGURI}" -c "DROP TABLE IF EXISTS {TABLE_NAME};"'
  exit_status = os.system(command)

rainfrog:
  rainfrog --url postgres://postgres:changeme@localhost:5432/eg1_dev

