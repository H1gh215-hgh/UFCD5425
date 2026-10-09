"""
run.py — ponto de entrada da aplicação TarefaFácil.

Para iniciar a aplicação em modo de desenvolvimento:

    python run.py

A aplicação fica disponível em http://127.0.0.1:5000
"""

from app import criar_app

app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
