import flet as ft

# Página que mostra os tickets após o login do administrador
def show_tickets_view(page):
    # Simulação de tickets recuperados do banco de dados (ou de uma API)
    tickets = [
        {"id": 1, "nome": "João", "setor": "TI", "status": "Aberto"},
        {"id": 2, "nome": "Maria", "setor": "Financeiro", "status": "Em andamento"},
        {"id": 3, "nome": "Carlos", "setor": "RH", "status": "Concluído"},
    ]
    
    # Criar uma lista visual com os tickets
    ticket_list = ft.ListView(
        controls=[
            ft.ListTile(
                title=ft.Text(f"Ticket #{ticket['id']} - {ticket['nome']} ({ticket['setor']})"),
                subtitle=ft.Text(f"Status: {ticket['status']}"),
            )
            for ticket in tickets
        ]
    )

    page.controls.clear()
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Lista de Tickets", size=28, weight="bold", text_align=ft.TextAlign.CENTER),
                    ft.Container(ticket_list, padding=ft.padding.all(10)),
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
