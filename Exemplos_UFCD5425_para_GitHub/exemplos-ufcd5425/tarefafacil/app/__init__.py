"""
__init__.py — TarefaFácil

Cria e configura a aplicação Flask ("app factory"). Manter esta criação
separada num ficheiro próprio facilita depois escrever testes e organizar
o projeto à medida que cresce.
"""

import os

from flask import Flask


def criar_app():
    # As pastas "templates" e "static" ficam na raiz do projeto (não dentro de
    # "app/"), tal como descrito na estrutura de pastas do manual — por isso
    # indicamos aqui os caminhos explicitamente.
    raiz_projeto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app = Flask(
        __name__,
        template_folder=os.path.join(raiz_projeto, "templates"),
        static_folder=os.path.join(raiz_projeto, "static"),
    )

    # Em produção, esta chave deveria vir de uma variável de ambiente e nunca
    # ser escrita diretamente no código.
    app.config["SECRET_KEY"] = os.environ.get("TAREFAFACIL_SECRET_KEY", "chave-de-exemplo-para-a-ufcd-5425")

    from app import modelos
    modelos.inicializar_bd()

    from app.rotas import rotas
    app.register_blueprint(rotas)

    return app
