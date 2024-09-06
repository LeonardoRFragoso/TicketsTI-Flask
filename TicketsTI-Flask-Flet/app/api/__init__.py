from flask import Blueprint

# Cria um blueprint para a API
api = Blueprint('api', __name__)

# Importa as rotas do arquivo routes.py
from app.api import routes
