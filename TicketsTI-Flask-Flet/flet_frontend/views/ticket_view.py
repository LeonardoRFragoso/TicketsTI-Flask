import flet as ft
from login_view import login_view

# Página inicial de submissão de tickets
def ticket_view(page):
    def submit_ticket(e):
        # Simples exemplo de validação de ticket
        if not nome_field.value or not email_field.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, preencha todos os campos obrigatórios!"), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            return

        page.snack_bar = ft.SnackBar(ft.Text("Ticket enviado com sucesso!"))
        page.snack_bar.open = True
        page.update()

    # Função para abrir a página de login
    def open_login(e):
        login_view(page)  # Abre a página de login

    # Campos de entrada
    nome_field = ft.TextField(label="Qual seu nome?", prefix_icon=ft.icons.PERSON)
    email_field = ft.TextField(label="Qual seu e-mail?", prefix_icon=ft.icons.EMAIL)

    submit_button = ft.ElevatedButton("Enviar Ticket", on_click=submit_ticket)
    login_button = ft.TextButton("Login Administrador", on_click=open_login)

    page.controls.clear()
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Submeter um Ticket", size=28, weight="bold", text_align=ft.TextAlign.CENTER),
                    ft.Container(nome_field, padding=ft.padding.all(10)),
                    ft.Container(email_field, padding=ft.padding.all(10)),
                    ft.Container(submit_button, alignment=ft.alignment.center, padding=ft.padding.only(top=20)),
                    ft.Container(login_button, alignment=ft.alignment.center, padding=ft.padding.only(top=20)),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.all(50),
            padding=ft.padding.all(30),
            width=550,
            border_radius=20,
            shadow=ft.BoxShadow(spread_radius=5, blur_radius=15, color=ft.colors.with_opacity(0.2, ft.colors.BLACK)),
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_GREY_900),
        )
    )
    page.update()
