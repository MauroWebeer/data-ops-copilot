from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory

from src.config import settings
from src.tools.text_to_sql import query_operational_pipelines_db
from src.tools.rag_docs import search_technical_runbooks
from src.agent.memory import get_session_history

# 1. Instancia o LLM da Groq com o modelo especificado
llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0.1,
    api_key=settings.groq_api_key
)

# 2. Lista de ferramentas disponíveis para o Data Ops Copilot
tools = [query_operational_pipelines_db, search_technical_runbooks]

# 3. Prompt do Sistema definindo a persona do Agente
system_message = """
Você é um Data Ops Copilot especialista em Engenharia de Dados, SRE e Operações de Plataforma.
Sua missão é ajudar engenheiros a diagnosticar falhas em pipelines, analisar status de execuções via DuckDB (Text-to-SQL) 
e consultar runbooks técnicos de documentação (RAG).

Diretrizes:
- Seja objetivo, técnico e direto ao ponto nas respostas.
- Quando houver erro em pipelines, consulte os dados operacionais e cruze com os runbooks técnicos correspondentes para sugerir a ação corretiva exata.
- Sempre valide se os resultados das consultas SQL retornaram dados antes de responder.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_message),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 4. Criação do Agente com suporte a Tool Calling
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. Envolve o executor com histórico de mensagens baseado em session_id
agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)


def run_agent_query(user_input: str, session_id: str) -> str:
    """Executa a query do usuário no agente mantendo o contexto da sessão informada."""
    config = {"configurable": {"session_id": session_id}}
    
    response = agent_with_chat_history.invoke(
        {"input": user_input},
        config=config
    )
    
    return response.get("output", "Desculpe, não consegui processar a resposta.")