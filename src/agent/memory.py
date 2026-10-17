# Dicionário em memória para armazenar o histórico de mensagens por session_id
sessions_db = {}
MAX_HISTORY_MESSAGES = 10  # Limita para evitar estouro de tokens


def get_session_messages(session_id: str) -> list:
    """Retorna a lista de mensagens da sessão aplicando uma janela deslizante (rolling window)."""
    if session_id not in sessions_db:
        sessions_db[session_id] = []
    
    # Retorna apenas as últimas mensagens para controlar o consumo de tokens
    return sessions_db[session_id]


def add_message_to_session(session_id: str, role: str, content: str):
    """Adiciona uma mensagem e garante que o histórico não ultrapasse o limite."""
    if session_id not in sessions_db:
        sessions_db[session_id] = []
        
    sessions_db[session_id].append({"role": role, "content": content})
    
    # Se passar do limite, remove as mensagens mais antigas (preservando o contexto recente)
    if len(sessions_db[session_id]) > MAX_HISTORY_MESSAGES:
        sessions_db[session_id] = sessions_db[session_id][-MAX_HISTORY_MESSAGES:]