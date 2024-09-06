import flet as ft
from flet_frontend.views.login_view import login_view
from flet_frontend.views.ticket_view import ticket_view
from flet_frontend.views.admin_view import admin_view

def main(page: ft.Page):
    page.title = "Sistema de Tickets"
    
    def route_change(route):
        if page.route == "/login":
            login_view(page)
        elif page.route == "/tickets":
            ticket_view(page)
        elif page.route == "/admin":
            admin_view(page)

    page.on_route_change = route_change
    page.go("/login")  # Inicia na página de login

ft.app(target=main)
