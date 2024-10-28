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
drop-database:
  #!/usr/bin/env python
  import sys, os; sys.path.append("{{work_dir}}")
  from api.config import DATABASE_URI

  DB_NAME = "eg1_dev"
  command = f'psql {DATABASE_URI} -c "DROP DATABASE {DB_NAME} WITH (FORCE);"'
  os.system(command)
  print(f"Database '{DB_NAME}' has been dropped.")

rainfrog:
  rainfrog --url postgres://postgres:changeme@localhost:5432/eg1_dev

