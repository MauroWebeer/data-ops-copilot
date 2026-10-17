from fastapi import FastAPI

from src.config import settings

app = FastAPI(
    title="Data Ops Copilot API",
    description="API REST com Agente Inteligente para Engenharia de Dados e Observabilidade.",
    version="0.1.0",
)


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {
        "status": "healthy",
        "service": "data-ops-copilot-api",
        "langfuse_host": settings.langfuse_host,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)