import os
import tempfile

import dotenv

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

#######################################################################
### Environment specific
#######################################################################

if ENV == "unittest":
    API_BASE_URL = "http://localhost:8000" + API_PREFIX
    DB_NAME = "eg1-unittest"
    DATABASE_URI = "sqlite:///" + os.path.join(tempfile.gettempdir(), f"{DB_NAME}-sqlite3.db")
elif ENV == "dev":
    API_BASE_URL = "http://localhost:8000" +API_PREFIX
    DB_NAME = "eg1_dev"
    DATABASE_URI = os.getenv(
        "POSTGRES_URI", "postgresql+psycopg2://postgres:changeme@localhost:5432/eg1_dev"
    )
else:
    API_BASE_URL = "http://localhost:8000" + API_PREFIX
    DB_NAME = "eg1"
    DATABASE_URI = os.getenv(
        "POSTGRES_URI", "postgresql+psycopg2://postgres:changeme@localhost:5432/eg1"
    )

