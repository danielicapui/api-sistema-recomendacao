from neo4j import GraphDatabase

class Neo4jConexao:
    def __init__(self,uri,user,pwd,port='7474'):
        self.uri=uri
        self.user=user
        self.pwd=pwd
        self.port=port
        self.driver=None
        try:
            self.driver=GraphDatabase.driver(f"{self.uri}/{self.port}", auth=(self.user, self.pwd))
        except Exception as e:
            print(f"Erro:Falha ao criar o driver:\nLogs:{e}")
    def feche(self):
        if self.driver!=None:
            self.driver.close()
    def execute(self,comando,dbname=None):
        assert self.driver!= None, "Driver não inicializado"
        session=None
        response=None
        
        try:
            session=self.driver.session(database=dbname) if dbname!=None else self.driver.session()
            response=list(session.run(comando))
        except Exception as e:
            print(f"Falha na executação de comando:\nLogs:{e}")
        finally:
            if session!=None:
                session.close()
        return response