# Data Ops Copilot

API REST robusta construída com **FastAPI** que expõe um Agente Inteligente (`LangChain` / `LangGraph`), atuando como um **Data Ops Copilot** especializado em Engenharia de Dados, SRE e operações de plataforma. O agente integra capacidades avançadas de *Text-to-SQL*, *RAG* local, gestão de memória por sessão e observabilidade completa em tempo real.

---

## 🚀 Funcionalidades Principais

1. **Text-to-SQL com DuckDB**: Permite consultar métricas, logs e o estado de execução de pipelines de dados estruturados num banco analítico DuckDB local.
2. **RAG Técnico em Markdown**: Pesquisa inteligente em runbooks e documentações técnicas armazenadas localmente na pasta `data/docs/` para resolução automatizada de falhas (*schema drift*, timeouts, etc.).
3. **Memória Multi-Turn por Sessão**: Mantém o contexto conversacional isolado e gerido por identificador de sessão (`session_id`).
4. **Observabilidade com LangFuse**: Rastreamento detalhado de cada requisição da API, chamadas de ferramentas, consumo de tokens, latência e custos.

---

## 🛠️ Stack Tecnológica

* **Linguagem**: Python 3.12+
* **Framework Backend**: FastAPI & Uvicorn
* **Orquestração de Agentes**: LangChain & LangGraph
* **LLM Provider**: Groq (`llama-3.3-70b-versatile`)
* **Armazenamento e Dados**: DuckDB (relacional e local)
* **Observabilidade**: LangFuse
* **Gestor de Pacotes**: `uv`

---

## 📁 Estrutura de Pastas

```text
data-ops-copilot/
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
├── data/
│   ├── docs/              # Ficheiros Markdown (.md) para RAG técnico
│   └── operational.duckdb # Base de dados DuckDB operacional
├── src/
│   ├── __init__.py
│   ├── main.py            # Ponto de entrada da aplicação FastAPI
│   ├── config.py          # Validação de variáveis de ambiente (Pydantic Settings)
│   ├── api/               # Camada de rotas e esquemas REST
│   │   ├── routes.py      # Endpoint POST /api/v1/chat
│   │   └── schemas.py     # Modelos de request/response Pydantic
│   ├── agent/             # Lógica do agente e gestão de memória
│   │   ├── graph.py       # Orquestração do loop de tool-calling
│   │   └── memory.py      # Gestão de histórico multi-turn por sessão
│   ├── tools/             # Ferramentas customizadas do Agente
│   │   ├── text_to_sql.py # Tool DuckDB para métricas e pipelines
│   │   └── rag_docs.py    # Tool de pesquisa em runbooks Markdown
│   └── services/          # Serviços de suporte e integrações
│       └── tracing.py     # Configuração do cliente LangFuse
└── tests/                 # Testes unitários e de integração
```

---

## ⚙️ Configuração e Instalação

### 1. Clonar o Repositório e Instalar Dependências

Certifique-se de que tem o utilitário **`uv`** instalado no seu ambiente Linux/WSL.

```bash
git clone [https://github.com/SEU_UTILIZADOR/data-ops-copilot.git](https://github.com/SEU_UTILIZADOR/data-ops-copilot.git)
cd data-ops-copilot

# Instalar dependências com o uv
uv sync
```

### 2. Configurar as Variáveis de Ambiente

Duplique o ficheiro de exemplo `.env.example` para `.env` e preencha com as suas chaves de API reais:

```bash
cp .env.example .env
```

Edite o ficheiro `.env`:

```env
GROQ_API_KEY=a_sua_chave_groq_aqui
LANGFUSE_PUBLIC_KEY=a_sua_chave_publica_langfuse
LANGFUSE_SECRET_KEY=a_sua_chave_secreta_langfuse
LANGFUSE_HOST=[https://cloud.langfuse.com](https://cloud.langfuse.com)
LANGFUSE_BASE_URL=[https://cloud.langfuse.com](https://cloud.langfuse.com)
```

---

## 🏃‍♂️ Como Executar o Projeto

Para iniciar o servidor de desenvolvimento FastAPI com recarregamento automático:

```bash
uv run uvicorn src.main:app --reload
```

O servidor estará ativo em: **`http://localhost:8000`**

---

## 🧪 Documentação Interativa & Testes

* **Swagger UI**: Aceda a `http://localhost:8000/docs` para testar os endpoints diretamente no navegador.
* **Health Check**: `GET /health`

### Exemplo de Requisição (`POST /api/v1/chat`)

**Payload JSON:**

```json
{
  "session_id": "sessao-123",
  "message": "Quais pipelines falharam recentemente e qual é o runbook para resolver?"
}
```

**Resposta Esperada:**
O agente invocará automaticamente a ferramenta DuckDB para inspecionar os logs operacionais, cruzará com o runbook técnico via RAG e devolverá o diagnóstico e a solução corretiva detalhada.

---

## 📊 Observabilidade

Todas as interações são automaticamente rastreadas no painel do **LangFuse**, permitindo auditar:

* O fluxo de raciocínio e selecção de ferramentas.
* O consumo preciso de *tokens* de input e output por requisição.
* A latência e o custo de execução por sessão.

---

## 🤝 Contribuição

Contribuições, sugestões de melhoria e novas ferramentas para o agente são bem-vindas. Sinta-se à vontade para abrir uma *pull request* ou reportar *issues*.

---

## 📄 Licença

Este projeto está licenciado sob a licença [MIT](https://www.google.com/search?q=LICENSE).

---

Pode copiar este conteúdo, guardá-lo num ficheiro chamado `README.md` na raiz do seu repositório, e versioná-lo com:

```bash
git add README.md
git commit -m "docs: add comprehensive professional README.md"
git push origin main

```