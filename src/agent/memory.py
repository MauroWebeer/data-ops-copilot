from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Dicionário em memória para armazenar o histórico por session_id
# Em produção, você poderia substituir facilmente por Redis ou PostgreSQL.
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Retorna ou cria o histórico de mensagens para uma sessão específica."""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]