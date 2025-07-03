from flask import Flask

app = Flask(__name__)  # Cria uma instância do Flask
# Mantenha as configurações de segurança
app.secret_key = 'sua_chave_secreta_aqui'

from app import routes #Importa as rotas para que o aplicativo possa acessar o html ***

