from flask import Flask
from flask_login import LoginManager,UserMixin
from py2neo import Graph
from config import URI2,PWD,tipo,conexao,user,local,dbname,port
import secrets
graph= Graph('bolt://{}:{}@{}:{}'.format(user,PWD,local,port))