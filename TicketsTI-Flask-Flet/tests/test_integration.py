import pytest
import flet as ft
from flet_frontend.views.login_view import login_view

def test_flet_login(client):
    # Simula a tela de login do Flet e interage com a API Flask
    page = ft.Page()

    def submit_form(e):
        username = username_field.value
        password = password_field.value

        # Simula uma requisição à API
        response = client.post('/api/login', json={
            'username': username,
            'password': password
        })
        assert response.status_code == 200

    username_field = ft.TextField(label="Usuário")
    password_field = ft.TextField(label="Senha", password=True)
    login_button = ft.ElevatedButton("Login", on_click=submit_form)

    page.add(username_field, password_field, login_button)
    page.update()

    # Simula a interação com a tela de login
    username_field.value = 'testuser'
    password_field.value = 'testpassword'
    submit_form(None)  # Simula o clique no botão de login
