from py2neo import Graph
from flask import Flask
from flask_login import LoginManager
import os
app = Flask(__name__, template_folder='temp')
username = "neo4j"
password = "123"
url = f'bolt://{username}:{password}@localhost:7687'
graph = Graph(url)
app.secret_key = os.urandom (24)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
import appl.view





