from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from py2neo import  Node,NodeMatcher
from py2neo.ogm import GraphObject, Property
class Usuario(UserMixin, GraphObject):
    __primarylabel__="usuario"
    __primarykey__="email"
    id=Property()
    nome = Property()
    email = Property()
    senha = Property()
    hashed_senha=Property()
    empresa = Property()
    def __init__(self,nome, email, senha,empresa):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.empresa =empresa
        #self.id= self.getId()
    def find(self):
        from app import db
        matcher=NodeMatcher(db.graph)
        user=matcher.match('usuario',email=self.email).first()
        #user = db.graph.run('usuario',email=self.email)
        return user
    def getId(self):
        from app import db
        query = 'match (n:usuario{email:"'+self.email+'"}) return ID(n)'
        user = self.find()
        id = db.graph.run(query, parameters={'email': user['email']}).evaluate()
        return id
    def setSenha(self, senha):
        #muda a senha
        from app import db
        self.senha = generate_password_hash(senha, method='sha256')
        if not self.find():
            user = Node('Usuario', nome=self.nome, email=self.email, senha=self.senha, created_on=self.created_on)
            db.graph.create(user)
            return True
        else:
            return False
    def is_active(self):
        return True
    def checkSenha(self, senha):
        user = self.find()
        if user:
            return check_password_hash(user['senha'], senha)
        else:
            return False