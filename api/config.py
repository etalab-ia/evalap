import os
import tempfile

import dotenv

os.environ["DEEPEVAL_TELEMETRY_OPT_OUT"] = "YES"

dotenv.load_dotenv()

#######################################################################
### App metadata
#######################################################################

APP_NAME = "EG1"
APP_DESCRIPTION = "Albert Evaluations API"
APP_VERSION = os.getenv("APP_VERSION", "0.0.0")
CONTACT = {
    "name": "Etalab - Datalab",
    "url": "https://www.etalab.gouv.fr/",
    "email": "etalab@modernisation.gouv.fr",
}


#######################################################################
### Commons
#######################################################################

ENV = os.getenv("ENV", "dev")
assert ENV in ["unittest", "dev", "prod"], "wrong ENV value"
BACKEND_CORS_ORIGINS = ["*"]
ALBERT_API_URL = os.getenv("ALBERT_API_URL")
ALBERT_API_KEY = os.getenv("ALBERT_API_KEY")
API_PREFIX = ""

# Runners
MAX_CONCURRENT_TASKS = 4  # 8 ok, 16 hard !

#######################################################################
### Environment specific
#######################################################################

if ENV == "unittest":
    API_BASE_URL = "http://localhost:8000" + API_PREFIX
    DB_NAME = "eg1-unittest"
    DATABASE_URI = "sqlite:///" + os.path.join(tempfile.gettempdir(), f"{DB_NAME}-sqlite3.db")
elif ENV == "dev":
    API_BASE_URL = "http://localhost:8000" + API_PREFIX
    DB_NAME = "eg1_dev"
    DATABASE_URL = os.getenv("POSTGRES_URL", "postgresql+psycopg2://postgres:changeme@localhost:5432")
    DATABASE_URI = DATABASE_URL.rstrip("/") + "/" + DB_NAME
else:
    API_BASE_URL = "http://localhost:8000" + API_PREFIX
    DB_NAME = os.getenv("DB_NAME", "eg1")
    DATABASE_URL = os.getenv("POSTGRES_URL")
    if not DATABASE_URL:
        raise ValueError("You need to provid a valid POSTGRES_URL env variable.")
    DATABASE_URI = DATABASE_URL.rstrip("/") + "/" + DB_NAME
