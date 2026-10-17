from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(
        ..., 
        description="Identificador único da sessão de chat para manter o histórico multi-turn.", 
        examples=["sessao-123"]
    )
    message: str = Field(
        ..., 
        description="Mensagem ou pergunta direcionada ao Data Ops Copilot.", 
        examples=["Quais pipelines falharam hoje e qual o runbook para resolver?"]
    )


class ChatResponse(BaseModel):
    session_id: str
    response: str