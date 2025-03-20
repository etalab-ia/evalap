import threading

from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from eg1.api.config import (
    API_PREFIX,
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    BACKEND_CORS_ORIGINS,
    CONTACT,
)
from eg1.api.endpoints import router as router_v1

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    contact=CONTACT,
    docs_url=API_PREFIX + "/docs",
    redoc_url=API_PREFIX + "/redoc",
    openapi_url=API_PREFIX + "/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Api rooter
app.include_router(router_v1, prefix=API_PREFIX + "/v1")
