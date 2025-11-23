import os
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware

from .routers.auth import router as auth_router
from .routers.salas import router as salas_router, get_mis_reservas
from .routers.sanciones import router as sanciones_router
from .routers.admin import router as admin_router
from .routers.analytics import router as analytics_router
from .utils.jwt import get_current_user

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


@app.get("/mis-reservas", include_in_schema=False)
def alias_mis_reservas(
    user_id: int | None = Query(None),
    user = Depends(get_current_user)
):
    """Alias sin prefijo para compatibilidad con clientes antiguos."""
    return get_mis_reservas(user_id=user_id, user=user)
