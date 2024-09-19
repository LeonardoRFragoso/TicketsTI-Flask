from app import create_app, db
from flask_migrate import Migrate

# Cria a instância do aplicativo Flask
app = create_app()

# Configura as migrações para o banco de dados
migrate = Migrate(app, db)

if __name__ == "__main__":
    # Executa a aplicação Flask no modo debug e especifica o host e a porta
    app.run(debug=True, host='0.0.0.0', port=8005)
