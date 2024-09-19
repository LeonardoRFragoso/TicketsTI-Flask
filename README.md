
# Sistema de Tickets - Suporte TI

Este é um projeto de sistema de tickets desenvolvido para a gestão de solicitações de suporte em um ambiente corporativo. Ele permite que os usuários enviem tickets com informações detalhadas sobre seus problemas técnicos e que o time de suporte TI possa visualizar e gerenciar essas solicitações.

## Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.
- **Flask**: Framework web utilizado para criar as rotas e a API do backend.
- **SQLAlchemy**: ORM utilizado para a interação com o banco de dados.
- **PostgreSQL**: Banco de dados utilizado no projeto.
- **Streamlit**: Biblioteca utilizada para criar o frontend interativo.
- **Flask-Login**: Extensão para gerenciar autenticação de usuários.
- **Flask-Migrate**: Extensão para lidar com migrações de banco de dados usando Alembic.
- **WTForms**: Biblioteca usada para criação de formulários com validação no backend.

## Funcionalidades

- Envio de tickets de suporte por usuários.
- Login e autenticação de usuários.
- Listagem e visualização de tickets para administradores.
- Geração de relatórios de tickets com filtros personalizados.
- Sistema de notificações via e-mail para o status dos tickets.

## Como Rodar o Projeto

1. Clone o repositório:

   ```bash
   git clone https://github.com/LeonardoRFragoso/TicketsTI-Flask
   cd TicketsTI-Flask
   ```

2. Crie um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate   # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure suas variáveis de ambiente no arquivo `.env`:

   ```
   SECRET_KEY=sua_chave_secreta
   DATABASE_URL=postgresql://usuario:senha@localhost:5432/seubanco
   ```

5. Realize as migrações para configurar o banco de dados:

   ```bash
   flask db upgrade
   ```

6. Rode a aplicação:

   ```bash
   python manage.py
   ```

7. Acesse o sistema no navegador:

   ```
   http://localhost:8005
   ```

## Repositório no GitHub

Você pode acessar o código-fonte completo no GitHub através do link: [Sistema de Tickets - Suporte TI](https://github.com/LeonardoRFragoso/TicketsTI-Flask).