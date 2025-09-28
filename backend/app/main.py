from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .config import FRONTEND_DIR
from .routes import login, user, data

app = FastAPI(
    title="Monks Case API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Rotas
app.include_router(login.router)
app.include_router(user.router)
app.include_router(data.router)

# Frontend
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
