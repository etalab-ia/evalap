from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from evalap.api.config import (
    API_PREFIX,
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    BACKEND_CORS_ORIGINS,
    CONTACT,
    ENV,
)
from evalap.api.endpoints import router as router_v1

docs_url_val = API_PREFIX + "/docs" if ENV != "prod" else None
redoc_url_val = API_PREFIX + "/redoc" if ENV != "prod" else None
openapi_url_val = API_PREFIX + "/openapi.json" if ENV != "prod" else None

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    contact=CONTACT,
    docs_url=docs_url_val,
    redoc_url=redoc_url_val,
    openapi_url=openapi_url_val,
)

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Api rooter
app.include_router(router_v1, prefix=API_PREFIX + "/v1")
