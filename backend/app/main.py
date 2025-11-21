from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.salas import router as salas_router
from app.routers.sanciones import router as sanciones_router
from app.routers.admin import router as admin_router
from app.routers.analytics import router as analytics_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
