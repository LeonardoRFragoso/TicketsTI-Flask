import flet as ft
from show_tickets_view import show_tickets_view

# Página de login para o administrador
def login_view(page):
    def verify_login(e):
        # Simples validação de usuário e senha
        if username_field.value == "admin" and password_field.value == "123456":
            page.snack_bar = ft.SnackBar(ft.Text("Login bem-sucedido!"))
            page.snack_bar.open = True
            show_tickets_view(page)  # Redirecionar para a página de tickets
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Credenciais incorretas!"), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
        
        page.update()

    username_field = ft.TextField(label="Usuário", prefix_icon=ft.icons.PERSON)
    password_field = ft.TextField(label="Senha", prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True)
    login_button = ft.ElevatedButton("Login", on_click=verify_login)

    page.controls.clear()
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Login do Administrador", size=28, weight="bold", text_align=ft.TextAlign.CENTER),
                    ft.Container(username_field, padding=ft.padding.all(10)),
                    ft.Container(password_field, padding=ft.padding.all(10)),
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
