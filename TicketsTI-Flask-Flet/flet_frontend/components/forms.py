import flet as ft

def login_form(on_submit):
    """
    Gera um formulário de login reutilizável.
    O parâmetro `on_submit` é uma função que será chamada quando o formulário for enviado.
    """
    username_field = ft.TextField(label="Usuário", autofocus=True)
    password_field = ft.TextField(label="Senha", password=True, can_reveal_password=True)
    login_button = ft.ElevatedButton("Login", on_click=on_submit)
    
    return ft.Column([username_field, password_field, login_button])
