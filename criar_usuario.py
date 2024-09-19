from app import db, create_app
from app.models import User

# Inicializa a aplicação Flask para acessar o contexto do banco de dados
app = create_app()
app.app_context().push()

def criar_usuario(username, email, password, is_admin=False):
    # Criação de um novo usuário
    novo_usuario = User(
        username=username,
        email=email,
        password=password,  # Certifique-se que o modelo User gere o hash da senha
        is_admin=is_admin
    )
    db.session.add(novo_usuario)
    db.session.commit()
    print(f"Usuário {username} criado com sucesso!")

# Exemplo de criação de usuário
criar_usuario('Leonardo', 'leonardorfragoso@gmail.com', '123456', is_admin=True)
