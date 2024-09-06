import pytest
from app import create_app, db
from app.models.user import User
from flask import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_login(client):
    # Cria um usuário de teste
    user = User(username='testuser', email='testuser@example.com')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    # Testa o login
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    json_data = json.loads(response.data)
    assert response.status_code == 200
    assert json_data['success'] is True

def test_create_ticket(client):
    # Testa a criação de um ticket
    response = client.post('/api/tickets', json={
        'nome': 'Leonardo Fragoso',
        'email': 'leonardo@example.com',
        'setor': 'Suporte',
        'categoria': 'Hardware',
        'descricao': 'Problema com o computador',
        'patrimonio': '12345'
    })
    json_data = json.loads(response.data)
    assert response.status_code == 200
    assert json_data['success'] is True

def test_get_tickets(client):
    # Testa a obtenção de tickets
    response = client.get('/api/tickets')
    json_data = json.loads(response.data)
    assert response.status_code == 200
    assert 'tickets' in json_data
