// script.js

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    var columnId = ev.target.id;
    updateTicketStatus(data, columnId);
}

function updateTicketStatus(ticketId, columnId) {
    // Implementação da chamada AJAX usando jQuery
    $.ajax({
        type: "POST",
        url: "/update_ticket_status",
        data: {
            ticket_id: ticketId,
            new_status: columnId
        },
        success: function(response) {
            if (response.success) {
                console.log("Ticket atualizado com sucesso!");
                // Mover o elemento do ticket para a nova coluna
                var ticketElement = document.getElementById(ticketId);
                var newColumn = document.getElementById(columnId);
                var ticketList = newColumn.querySelector(".ticket-list");
                ticketList.appendChild(ticketElement);
            } else {
                console.error("Falha ao atualizar o ticket:", response.error);
            }
        },
        error: function(xhr, status, error) {
            console.error("Erro na requisição AJAX:", error);
        }
    });
}

// Função para exibir o conteúdo do ticket ao dar dois cliques
function showTicketContent(ticketId) {
    // Implementação da chamada AJAX para obter o conteúdo do ticket
    $.ajax({
        type: "POST",
        url: "/get_ticket_content",
        data: {
            ticket_id: ticketId
        },
        success: function(response) {
            if (response.success) {
                // Exibir o conteúdo do ticket em um modal, por exemplo
                alert(response.content);
            } else {
                console.error("Falha ao obter o conteúdo do ticket:", response.error);
            }
        },
        error: function(xhr, status, error) {
            console.error("Erro na requisição AJAX:", error);
        }
    });
}

// Adicionar chamada para carregar tickets no carregamento da página
$(document).ready(function () {
    loadTickets();
});

// Função para carregar os tickets
function loadTickets() {
    $.ajax({
        type: "GET",
        url: "/load_tickets",
        success: function(response) {
            if (response.success) {
                // Adicionar os tickets nas colunas correspondentes
                updateColumns(response.tickets);
            } else {
                console.error("Falha ao carregar os tickets:", response.error);
            }
        },
        error: function(xhr, status, error) {
            console.error("Erro na requisição AJAX:", error);
        }
    });
}

// Função para atualizar as colunas com os tickets carregados
function updateColumns(tickets) {
    // Iterar sobre os tickets e adicionar ou atualizar nas colunas corretas
    tickets.forEach(function (ticket) {
        var ticketElement = createTicketElement(ticket);
        var columnId = ticket.status.toLowerCase().replace(' ', '-');
        var column = document.getElementById(columnId);
        var ticketList = column.querySelector(".ticket-list");

        // Verificar se o ticket já existe na coluna
        var existingTicket = document.getElementById(ticket.id);
        if (existingTicket) {
            existingTicket.parentNode.removeChild(existingTicket);
        }

        ticketList.appendChild(ticketElement);
    });
}

// Função para criar um elemento de ticket
function createTicketElement(ticket) {
    var ticketElement = document.createElement("li");
    ticketElement.className = "ticket";
    ticketElement.draggable = true;
    ticketElement.id = ticket.id;
    ticketElement.setAttribute("ondragstart", "drag(event)");
    ticketElement.setAttribute("ondblclick", "showTicketContent('" + ticket.id + "')");

    var ticketContent = "<h3>" + ticket.nome + "</h3><p>" + ticket.descricao + "</p>";
    ticketElement.innerHTML = ticketContent;

    return ticketElement;
}
