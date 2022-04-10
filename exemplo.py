from utils import criar_db
from db_graph import Neo4jConexao as Conexao
from config import URI2,USER,PWD
conn=Conexao(URI2,USER,PWD)
criar_db(conn,"exemplo")
query_string = '''
USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM
'https://raw.githubusercontent.com/ngshya/datasets/master/cora/cora_content.csv'
AS line FIELDTERMINATOR ','
CREATE (:Paper {id: line.paper_id, class: line.label})
'''
conn.execute(query_string, dbname='exemplo')

query_string = '''
USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM
'https://raw.githubusercontent.com/ngshya/datasets/master/cora/cora_cites.csv'
AS line FIELDTERMINATOR ','
MATCH (citing_paper:Paper {id: line.citing_paper_id}),(cited_paper:Paper {id: line.cited_paper_id})
CREATE (citing_paper)-[:CITES]->(cited_paper)
'''
conn.execute(query_string, dbname='exemplo')