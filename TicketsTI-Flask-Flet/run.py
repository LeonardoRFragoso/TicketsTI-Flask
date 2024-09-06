from app import create_app

# Cria a aplicação Flask com as configurações definidas
app = create_app()

if __name__ == "__main__":
    # Inicia o servidor Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
