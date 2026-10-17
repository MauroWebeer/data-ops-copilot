from fastapi import FastAPI

import src.services.tracing  # noqa: F401
from src.config import settings
from src.api.routes import router as api_router

app = FastAPI(
    title="Data Ops Copilot API",
    description="API REST com Agente Inteligente para Engenharia de Dados e Observabilidade.",
    version="0.1.0",
)

app.include_router(api_router)


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {
        "status": "healthy",
        "service": "data-ops-copilot-api",
        "langfuse_host": settings.langfuse_host,
    }