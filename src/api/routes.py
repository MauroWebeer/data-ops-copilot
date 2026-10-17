from fastapi import APIRouter, HTTPException
from langfuse.langchain import CallbackHandler

from src.api.schemas import ChatRequest, ChatResponse
from src.agent.graph import run_agent_query

router = APIRouter(prefix="/api/v1", tags=["Data Ops Copilot"])


@router.post("/chat", response_model=ChatResponse)
async def chat_with_copilot(payload: ChatRequest):
    """Envia uma mensagem para o Agente Data Ops Copilot com suporte a sessão e tracing via LangFuse."""
    try:
        # Inicializa o callback handler do LangFuse sem argumentos no __init__
        langfuse_handler = CallbackHandler()
        langfuse_handler.session_id = payload.session_id
        
        # Executa o agente passando a session_id e o callback do LangFuse
        response_text = run_agent_query(
            user_input=payload.message,
            session_id=payload.session_id,
            callbacks=[langfuse_handler]
        )
        
        return ChatResponse(
            session_id=payload.session_id,
            response=response_text
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao processar a mensagem com o agente: {str(e)}"
        )