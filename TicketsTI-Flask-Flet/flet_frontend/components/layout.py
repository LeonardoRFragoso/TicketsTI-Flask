import flet as ft

def app_layout(content):
    """
    Gera um layout padrão para a aplicação com um cabeçalho fixo e conteúdo variável.
    O parâmetro `content` é o conteúdo que será exibido no corpo da página.
    """
    return ft.Column(
        [
            ft.Text("Sistema de Tickets - Cabeçalho", size=32, weight="bold"),
            content,
            ft.Text("Rodapé © 2024", size=14, weight="light", color="gray"),
        ],
        spacing=20
    )
