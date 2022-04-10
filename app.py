from flask import Flask
from flask_login import LoginManager
from py2neo import Graph
from models import Usuario
from py2neo_conexao import Py2Neo
import os
db=Py2Neo()
def create_app():
    app = Flask(__name__, template_folder='templates')
    #modifique com o 'tipo+conexão://user:senha@local/nomedatabase' do banco de dados-
    key=os.urandom(24)
    app.config['SECRET_KEY'] =key   
    app.config.from_object('config.Config')
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    from api import api as api_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint)
    #db.graph.schema.create_uniqueness_constraint("Usuario", "username")
    @login_manager.user_loader
    def load_user(user_id):
        if user_id is not None:
            query = 'match (n:usuario) where ID(n)='+user_id+' return n'
            user = db.graph.run(query, parameters={'ID': user_id}).evaluate()
            user2 = Usuario(user['nome'], user['email'], user['senha'], user['empresa'])
            user2.id=user2.getId()
            return user2
        return None
    return app
