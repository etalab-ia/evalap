import importlib.metadata
import json
import logging
import os
import tempfile

import dotenv

os.environ["DEEPEVAL_TELEMETRY_OPT_OUT"] = "YES"

dotenv.load_dotenv()

#######################################################################
### App metadata
#######################################################################

APP_NAME = "evalap"  # redundant wuth pyproject.name
APP_DESCRIPTION = "Evaluations API and Platform"
CONTACT = {
    "name": "Etalab - Datalab",
    "url": "https://www.etalab.gouv.fr/",
    "email": "etalab@modernisation.gouv.fr",
}

try:
    APP_VERSION = importlib.metadata.version(APP_NAME)
except importlib.metadata.PackageNotFoundError:
    logging.warning(f"Package {APP_NAME} is not installed.")
    APP_VERSION = "0.0"


#######################################################################
### Commons
#######################################################################

ENV = os.getenv("ENV", "dev")
assert ENV in ["unittest", "dev", "prod"], "wrong ENV value"
BACKEND_CORS_ORIGINS = ["*"]
API_PREFIX = ""

# Runners / data sampling
MAX_CONCURRENT_TASKS = 8  # 8 ok, 16 hard !
DEFAULT_JUDGE_MODEL = "gpt-4o-mini"
MCP_BRIDGE_URL = os.getenv("MCP_BRIDGE_URL", "http://172.18.0.1:9092")
ZMQ_WORKER_URL = "tcp://localhost:5556"
ZMQ_SENDER_URL = "tcp://localhost:5555"
DATASET_SAMPLE_LIMIT = int(os.getenv("DATASET_SAMPLE_LIMIT", "10" if ENV == "dev" else "0"))

# Soon obsolete
MFS_API_KEY_V2 = os.getenv("MFS_API_KEY_V2")

#######################################################################
### Auth
#######################################################################

ADMIN_TOKENS = [os.getenv("ADMIN_TOKEN")] if os.getenv("ADMIN_TOKEN") else []
USER_TOKENS = json.loads(os.getenv("USER_API_KEYS", "null"))
if USER_TOKENS:
    USER_TOKENS = {v: k for k, v in USER_TOKENS.items()}


#######################################################################
### Environment specific
#######################################################################

if ENV == "unittest":
    API_BASE_URL = "http://localhost:8000" + API_PREFIX
    DB_NAME = "evalap-unittest"
    DATABASE_URI = "sqlite:///" + os.path.join(tempfile.gettempdir(), f"{DB_NAME}-sqlite3.db")
    ZMQ_WORKER_URL = "tcp://localhost:5576"
    ZMQ_SENDER_URL = "tcp://localhost:5575"
elif ENV == "dev":
    API_BASE_URL = "http://localhost:8000" + API_PREFIX
    DB_NAME = "evalap_dev"
    DATABASE_URL = os.getenv("POSTGRES_URL", "postgresql+psycopg2://postgres:changeme@localhost:5432")
    DATABASE_URI = DATABASE_URL.rstrip("/") + "/" + DB_NAME
else:
    API_BASE_URL = "http://localhost:8000" + API_PREFIX
    DB_NAME = os.getenv("DB_NAME", "evalap")
    DATABASE_URL = os.getenv("POSTGRES_URL")
    if not DATABASE_URL:
        raise ValueError("You need to provid a valid POSTGRES_URL env variable.")
    DATABASE_URI = DATABASE_URL.rstrip("/") + "/" + DB_NAME
