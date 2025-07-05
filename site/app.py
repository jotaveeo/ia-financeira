# Arquivo principal para rodar o app Flask
from flask import Flask
from app.routes import main

app = Flask(__name__)

# Registrando as rotas
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
