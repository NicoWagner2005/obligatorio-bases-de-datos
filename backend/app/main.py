import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.auth import router as auth_router
from .routers.salas import router as salas_router
from .routers.sanciones import router as sanciones_router
from .routers.admin import router as admin_router
from .routers.analytics import router as analytics_router

app = FastAPI()

origins_env = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
)
allowed_origins = [origin.strip() for origin in origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth_router)
app.include_router(salas_router)
app.include_router(sanciones_router)
app.include_router(admin_router)
app.include_router(analytics_router)
