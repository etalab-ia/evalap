from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.config import APP_DESCRIPTION, APP_NAME, APP_VERSION, BACKEND_CORS_ORIGINS, CONTACT
from api.endpoints import router as router_v1

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    contact=CONTACT,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router_v1, prefix="/api/v1")
