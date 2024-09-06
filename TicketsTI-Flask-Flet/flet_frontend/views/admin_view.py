import flet as ft
import requests

def admin_view(page):
    def load_tickets():
        response = requests.get("http://localhost:5000/api/tickets")
        result = response.json()

        if result.get("success"):
            tickets = result.get("tickets", [])
            ticket_list.controls.clear()
            for ticket in tickets:
                ticket_list.controls.append(
                    ft.Row(
                        [
                            ft.Text(f"Ticket ID: {ticket['id']} - {ticket['nome']} - {ticket['status']}"),
                            ft.ElevatedButton(
                                "Atualizar Status",
                                on_click=lambda e, t_id=ticket['id']: update_status(t_id)
                            ),
                            ft.ElevatedButton(
                                "Deletar",
                                on_click=lambda e, t_id=ticket['id']: delete_ticket(t_id)
                            ),
                        ]
                    )
                )
            page.update()

    def update_status(ticket_id):
        new_status = ft.TextField(label="Novo Status").value
        response = requests.put(
            f"http://localhost:5000/api/tickets/{ticket_id}",
            json={"status": new_status}
        )
        if response.json().get("success"):
            load_tickets()
            page.snack_bar = ft.SnackBar(ft.Text("Status do ticket atualizado com sucesso!"))
            page.snack_bar.open = True
            page.update()

    def delete_ticket(ticket_id):
        response = requests.delete(f"http://localhost:5000/api/tickets/{ticket_id}")
        if response.json().get("success"):
            load_tickets()
            page.snack_bar = ft.SnackBar(ft.Text("Ticket deletado com sucesso!"))
            page.snack_bar.open = True
            page.update()

    ticket_list = ft.Column()

    load_tickets()

    page.controls.clear()
    page.add(
        ft.Column(
            [
                ft.Text("Administração de Tickets", size=24),
                ticket_list,
            ]
        )
    )
    page.update()
