"""
modelos.py — TarefaFácil

Este ficheiro trata de tudo o que envolve a base de dados: criar as tabelas,
e guardar/consultar/atualizar/apagar utilizadores, tarefas e eventos.

Usa-se sqlite3 (já incluído no Python) em vez de um sistema mais complexo,
porque para um projeto de 45 horas é mais do que suficiente e ajuda a perceber
exatamente o que está a acontecer a cada pedido feito à base de dados.
"""

import os
import sqlite3
from datetime import date, timedelta

CAMINHO_BD = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bd", "tarefafacil.db"
)


def obter_ligacao():
    """Abre uma ligação à base de dados, devolvendo linhas como dicionários."""
    ligacao = sqlite3.connect(CAMINHO_BD)
    ligacao.row_factory = sqlite3.Row
    ligacao.execute("PRAGMA foreign_keys = ON")
    return ligacao


def inicializar_bd():
    """Cria as tabelas da aplicação, caso ainda não existam."""
    ligacao = obter_ligacao()
    ligacao.executescript(
        """
        CREATE TABLE IF NOT EXISTS utilizadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'pendente',
            prazo TEXT,
            id_utilizador INTEGER NOT NULL,
            FOREIGN KEY (id_utilizador) REFERENCES utilizadores (id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            data TEXT NOT NULL,
            hora TEXT,
            id_utilizador INTEGER NOT NULL,
            FOREIGN KEY (id_utilizador) REFERENCES utilizadores (id) ON DELETE CASCADE
        );
        """
    )
    ligacao.commit()
    ligacao.close()


# ---------------------------------------------------------------------------
# Utilizadores
# ---------------------------------------------------------------------------

def criar_utilizador(nome, email, password_hash):
    ligacao = obter_ligacao()
    ligacao.execute(
        "INSERT INTO utilizadores (nome, email, password_hash) VALUES (?, ?, ?)",
        (nome, email, password_hash),
    )
    ligacao.commit()
    novo_id = ligacao.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
    ligacao.close()
    return novo_id


def obter_utilizador_por_email(email):
    ligacao = obter_ligacao()
    utilizador = ligacao.execute(
        "SELECT * FROM utilizadores WHERE email = ?", (email,)
    ).fetchone()
    ligacao.close()
    return utilizador


def obter_utilizador_por_id(id_utilizador):
    ligacao = obter_ligacao()
    utilizador = ligacao.execute(
        "SELECT * FROM utilizadores WHERE id = ?", (id_utilizador,)
    ).fetchone()
    ligacao.close()
    return utilizador


# ---------------------------------------------------------------------------
# Tarefas
# ---------------------------------------------------------------------------

def criar_tarefa(titulo, prazo, id_utilizador):
    ligacao = obter_ligacao()
    ligacao.execute(
        "INSERT INTO tarefas (titulo, estado, prazo, id_utilizador) VALUES (?, 'pendente', ?, ?)",
        (titulo, prazo or None, id_utilizador),
    )
    ligacao.commit()
    ligacao.close()


def obter_tarefas_por_utilizador(id_utilizador):
    ligacao = obter_ligacao()
    tarefas = ligacao.execute(
        """
        SELECT * FROM tarefas
        WHERE id_utilizador = ?
        ORDER BY
            CASE WHEN estado = 'concluída' THEN 1 ELSE 0 END,
            CASE WHEN prazo IS NULL OR prazo = '' THEN 1 ELSE 0 END,
            prazo ASC
        """,
        (id_utilizador,),
    ).fetchall()
    ligacao.close()
    return tarefas


def obter_tarefa(id_tarefa, id_utilizador):
    ligacao = obter_ligacao()
    tarefa = ligacao.execute(
        "SELECT * FROM tarefas WHERE id = ? AND id_utilizador = ?",
        (id_tarefa, id_utilizador),
    ).fetchone()
    ligacao.close()
    return tarefa


def editar_tarefa(id_tarefa, id_utilizador, titulo, prazo):
    ligacao = obter_ligacao()
    ligacao.execute(
        "UPDATE tarefas SET titulo = ?, prazo = ? WHERE id = ? AND id_utilizador = ?",
        (titulo, prazo or None, id_tarefa, id_utilizador),
    )
    ligacao.commit()
    ligacao.close()


def concluir_tarefa(id_tarefa, id_utilizador):
    ligacao = obter_ligacao()
    ligacao.execute(
        "UPDATE tarefas SET estado = 'concluída' WHERE id = ? AND id_utilizador = ?",
        (id_tarefa, id_utilizador),
    )
    ligacao.commit()
    ligacao.close()


def reabrir_tarefa(id_tarefa, id_utilizador):
    ligacao = obter_ligacao()
    ligacao.execute(
        "UPDATE tarefas SET estado = 'pendente' WHERE id = ? AND id_utilizador = ?",
        (id_tarefa, id_utilizador),
    )
    ligacao.commit()
    ligacao.close()


def apagar_tarefa(id_tarefa, id_utilizador):
    ligacao = obter_ligacao()
    ligacao.execute(
        "DELETE FROM tarefas WHERE id = ? AND id_utilizador = ?",
        (id_tarefa, id_utilizador),
    )
    ligacao.commit()
    ligacao.close()


def tarefa_esta_atrasada(tarefa):
    """
    Uma tarefa está atrasada se tiver um prazo definido, esse prazo já tiver
    passado, e a tarefa ainda não estiver concluída.
    """
    if not tarefa["prazo"]:
        return False
    if tarefa["estado"] == "concluída":
        return False
    return tarefa["prazo"] < date.today().isoformat()


# ---------------------------------------------------------------------------
# Eventos
# ---------------------------------------------------------------------------

def criar_evento(titulo, data_evento, hora, id_utilizador):
    ligacao = obter_ligacao()
    ligacao.execute(
        "INSERT INTO eventos (titulo, data, hora, id_utilizador) VALUES (?, ?, ?, ?)",
        (titulo, data_evento, hora or None, id_utilizador),
    )
    ligacao.commit()
    ligacao.close()


def apagar_evento(id_evento, id_utilizador):
    ligacao = obter_ligacao()
    ligacao.execute(
        "DELETE FROM eventos WHERE id = ? AND id_utilizador = ?",
        (id_evento, id_utilizador),
    )
    ligacao.commit()
    ligacao.close()


def obter_eventos_da_semana(id_utilizador, inicio_semana):
    """
    Devolve os eventos do utilizador entre inicio_semana e os 6 dias seguintes
    (uma semana completa, de segunda a domingo), ordenados por data e hora.
    """
    fim_semana = inicio_semana + timedelta(days=6)
    ligacao = obter_ligacao()
    eventos = ligacao.execute(
        """
        SELECT * FROM eventos
        WHERE id_utilizador = ? AND data BETWEEN ? AND ?
        ORDER BY data ASC, hora ASC
        """,
        (id_utilizador, inicio_semana.isoformat(), fim_semana.isoformat()),
    ).fetchall()
    ligacao.close()
    return eventos
