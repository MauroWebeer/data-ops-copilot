from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

import src.services.tracing
from src.config import settings
from src.tools.text_to_sql import query_operational_pipelines_db
from src.tools.rag_docs import search_technical_runbooks
from src.agent.memory import get_session_messages, add_message_to_session

# 1. Instancia o LLM da Groq
llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0.1,
    api_key=settings.groq_api_key
)


# 2. Dicionário e lista de ferramentas disponíveis
tools_dict = {
    "query_operational_pipelines_db": query_operational_pipelines_db,
    "search_technical_runbooks": search_technical_runbooks
}
tools = list(tools_dict.values())
llm_with_tools = llm.bind_tools(tools)

# 3. Prompt do Sistema direto e objetivo
system_message = """
Você é um Data Ops Copilot especialista em Engenharia de Dados e SRE. 
Sua tarefa é ajudar engenheiros a diagnosticar falhas em pipelines consultando o banco de dados DuckDB (via ferramenta SQL) ou os runbooks (via RAG).
Sempre analise os dados retornados pelas ferramentas e redija uma resposta final clara, técnica e explicativa em texto para o usuário.
"""


def run_agent_query(user_input: str, session_id: str, callbacks: list = None) -> str:
    """Executa a query do usuário com loop de tool-calling e fallback forçado de texto."""
    messages = get_session_messages(session_id)
    
    # Constrói o histórico de mensagens
    langchain_messages = [SystemMessage(content=system_message)]
    for m in messages:
        if m["role"] == "user":
            langchain_messages.append(HumanMessage(content=m["content"]))
        elif m["role"] == "assistant":
            langchain_messages.append(AIMessage(content=m["content"]))
            
    langchain_messages.append(HumanMessage(content=user_input))
    add_message_to_session(session_id, "user", user_input)

    config = {}
    if callbacks:
        config["callbacks"] = callbacks

    try:
        answer = ""
        # Loop controlado de tool-calling (até 3 iterações)
        for _ in range(3):
            response = llm_with_tools.invoke(langchain_messages, config=config)
            
            if hasattr(response, "tool_calls") and response.tool_calls:
                langchain_messages.append(response)
                
                for tc in response.tool_calls:
                    tool_name = tc["name"]
                    tool_args = tc["args"]
                    tool_id = tc["id"]
                    
                    if tool_name in tools_dict:
                        tool_fn = tools_dict[tool_name]
                        tool_result = tool_fn.invoke(tool_args)
                    else:
                        tool_result = f"Erro: Ferramenta {tool_name} não encontrada."
                        
                    langchain_messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_id))
            else:
                answer = getattr(response, "content", "")
                if answer.strip():
                    break
        
        # Fallback de Segurança: Se o modelo executou as ferramentas mas não gerou texto,
        # forçamos uma chamada final pedindo explicitamente o resumo técnico.
        if not answer.strip():
            fallback_prompt = HumanMessage(content="Com base nos dados retornados pelas ferramentas acima, forneça o diagnóstico técnico completo e a solução para o usuário.")
            summary_response = llm.invoke(langchain_messages + [fallback_prompt], config=config)
            answer = getattr(summary_response, "content", "Diagnóstico executado, mas não foi possível gerar o texto descritivo.")

        # Salva e retorna
        add_message_to_session(session_id, "assistant", answer)
        return answer
        
    except Exception as e:
        return f"Erro na execução do agente: {str(e)}"