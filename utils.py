from db_graph import Neo4jConexao as Conexao
def criar_db(conn,nome):
    conn.execute(f"CREATE OR REPLACE DATABASE {nome}")
