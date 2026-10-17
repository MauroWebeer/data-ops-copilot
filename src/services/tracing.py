import os
from langfuse import Langfuse
from src.config import settings

# Configura as variáveis de ambiente que o LangChain / LangFuse Callback Handler espera automaticamente
os.environ["LANGFUSE_PUBLIC_KEY"] = settings.langfuse_public_key
os.environ["LANGFUSE_SECRET_KEY"] = settings.langfuse_secret_key
os.environ["LANGFUSE_HOST"] = settings.langfuse_host


def get_langfuse_client() -> Langfuse:
    """Retorna uma instância cliente do LangFuse para gerenciamento avançado se necessário."""
    return Langfuse(
        public_key=settings.langfuse_public_key,
        secret_key=settings.langfuse_secret_key,
        host=settings.langfuse_host,
    )