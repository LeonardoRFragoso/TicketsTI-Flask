import flet as ft
from ticket_view import ticket_view

# Função principal que controla a navegação
def main(page: ft.Page):
    page.title = "Sistema de Tickets"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    ticket_view(page)  # Inicializa com a página de submissão de tickets

ft.app(target=main)
