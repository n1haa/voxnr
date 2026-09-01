from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.projects import router as projects_router
from app.api.rbac import router as rbac_router
from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    health_router,
    prefix="/api",
    tags=["Health"],
)


app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Auth"],
)


app.include_router(
    rbac_router,
    prefix="/api/v1/rbac",
    tags=["RBAC"],
)


app.include_router(
    projects_router,
    prefix="/api/v1/projects",
    tags=["Projects"],
)