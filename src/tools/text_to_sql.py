import os
import duckdb
from langchain_core.tools import tool

DB_PATH = "data/operational.duckdb"


def init_operational_db():
    """Inicializa um banco DuckDB de exemplo com tabelas de logs e status de pipelines."""
    os.makedirs("data", exist_ok=True)
    conn = duckdb.connect(DB_PATH)
    
    # Criando tabela de status de pipelines de dados
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pipeline_runs (
            pipeline_name VARCHAR,
            status VARCHAR,
            execution_date TIMESTAMP,
            rows_processed INTEGER,
            error_message VARCHAR
        )
    """)
    
    # Inserindo dados mockados iniciais se a tabela estiver vazia
    res = conn.execute("SELECT COUNT(*) FROM pipeline_runs").fetchone()
    if res[0] == 0:
        conn.execute("""
            INSERT INTO pipeline_runs VALUES
            ('ingest_sales_parquet', 'SUCCESS', '2026-10-15 08:00:00', 15420, NULL),
            ('ingest_customers_api', 'SUCCESS', '2026-10-15 08:30:00', 1250, NULL),
            ('transform_gold_orders', 'FAILED', '2026-10-15 09:00:00', 0, 'Timeout connecting to source warehouse'),
            ('sync_metrics_databricks', 'SUCCESS', '2026-10-15 10:00:00', 43100, NULL)
        """)
    conn.close()


@tool
def query_operational_pipelines_db(sql_query: str) -> str:
    """Executa uma consulta SQL (Text-to-SQL) no banco de dados operacional DuckDB para verificar status de pipelines, logs e métricas de execução.
    
    Args:
        sql_query: A consulta SQL válida compatível com DuckDB a ser executada na tabela 'pipeline_runs'.
    """
    try:
        # Garante que o banco existe antes de consultar
        init_operational_db()
        conn = duckdb.connect(DB_PATH, read_only=True)
        
        # Validação básica de segurança (opcional, focado em SELECT)
        if not sql_query.strip().lower().startswith("select"):
            return "Erro: Apenas comandos SELECT são permitidos por motivos de segurança."
            
        result_df = conn.execute(sql_query).fetchdf()
        conn.close()
        
        if result_df.empty:
            return "A consulta retornou zero registros."
            
        return result_df.to_markdown(index=False)
    except Exception as e:
        return f"Erro ao executar a consulta SQL no DuckDB: {str(e)}"