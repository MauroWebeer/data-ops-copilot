import os
from langfuse import Langfuse
from src.config import settings

# Define explicitamente no os.environ para garantir que qualquer SDK interno pegue
os.environ["LANGFUSE_PUBLIC_KEY"] = settings.langfuse_public_key
os.environ["LANGFUSE_SECRET_KEY"] = settings.langfuse_secret_key
os.environ["LANGFUSE_HOST"] = settings.langfuse_host
os.environ["LANGFUSE_BASE_URL"] = settings.langfuse_base_url


def get_langfuse_client() -> Langfuse:
    """Retorna uma instância cliente do LangFuse."""
    return Langfuse(
        public_key=settings.langfuse_public_key,
        secret_key=settings.langfuse_secret_key,
        host=settings.langfuse_host,
    )