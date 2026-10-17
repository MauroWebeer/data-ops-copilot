import os
from langchain_core.tools import tool

DOCS_DIR = "data/docs"


@tool
def search_technical_runbooks(query: str) -> str:
    """Busca em arquivos Markdown locais de runbooks técnicos e documentações de engenharia de dados por termos relevantes.
    
    Args:
        query: Termo ou palavra-chave técnica para buscar nos documentos (ex: 'Timeout', 'Schema Drift', 'transform_gold_orders').
    """
    try:
        if not os.path.exists(DOCS_DIR):
            return "Nenhum diretório de documentação encontrado."
            
        matching_snippets = []
        query_lower = query.lower()
        
        for filename in os.listdir(DOCS_DIR):
            if filename.endswith(".md"):
                file_path = os.path.join(DOCS_DIR, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Busca simples por linhas ou blocos contendo a query
                    if query_lower in content.lower():
                        matching_snippets.append(f"### Arquivo: {filename}\n{content}")
                        
        if not matching_snippets:
            return f"Nenhuma documentação encontrada para o termo: '{query}'."
            
        return "\n\n".join(matching_snippets)
    except Exception as e:
        return f"Erro ao pesquisar nas documentações: {str(e)}"