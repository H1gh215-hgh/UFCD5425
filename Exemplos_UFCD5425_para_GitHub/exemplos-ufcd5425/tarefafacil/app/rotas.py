"""
rotas.py — TarefaFácil

Este ficheiro define todos os "endereços" (rotas) da aplicação: o que acontece
quando o utilizador visita cada página ou submete cada formulário.
"""

from datetime import date, datetime, timedelta
from functools import wraps

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app import modelos

rotas = Blueprint("rotas", __name__)


# ---------------------------------------------------------------------------
# Autenticação
# ---------------------------------------------------------------------------

def login_necessario(funcao):
    """Impede o acesso a uma página a quem não tiver sessão iniciada."""
    @wraps(funcao)
    def funcao_protegida(*args, **kwargs):
        if "id_utilizador" not in session:
            flash("Inicie sessão para continuar.", "erro")
            return redirect(url_for("rotas.login"))
        return funcao(*args, **kwargs)
    return funcao_protegida


@rotas.route("/")
def inicio():
    if "id_utilizador" in session:
        return redirect(url_for("rotas.tarefas"))
    return redirect(url_for("rotas.login"))


@rotas.route("/registo", methods=["GET", "POST"])
def registo():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not nome or not email or not password:
            flash("Preencha o nome, o email e a palavra-passe.", "erro")
            return render_template("registo.html")

        if len(password) < 4:
            flash("A palavra-passe deve ter pelo menos 4 caracteres.", "erro")
            return render_template("registo.html")

        if modelos.obter_utilizador_por_email(email):
            flash("Já existe uma conta com este email.", "erro")
            return render_template("registo.html")

        password_hash = generate_password_hash(password)
        id_utilizador = modelos.criar_utilizador(nome, email, password_hash)
        session["id_utilizador"] = id_utilizador
        session["nome_utilizador"] = nome
        flash("Conta criada com sucesso. Bem-vindo(a)!", "sucesso")
        return redirect(url_for("rotas.tarefas"))

    return render_template("registo.html")


@rotas.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        utilizador = modelos.obter_utilizador_por_email(email)
        if not utilizador or not check_password_hash(utilizador["password_hash"], password):
            flash("Email ou palavra-passe incorretos.", "erro")
            return render_template("login.html")

        session["id_utilizador"] = utilizador["id"]
        session["nome_utilizador"] = utilizador["nome"]
        return redirect(url_for("rotas.tarefas"))

    return render_template("login.html")


@rotas.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("rotas.login"))


# ---------------------------------------------------------------------------
# Tarefas
# ---------------------------------------------------------------------------

@rotas.route("/tarefas")
@login_necessario
def tarefas():
    lista_tarefas = modelos.obter_tarefas_por_utilizador(session["id_utilizador"])
    tarefas_com_estado = [
        {"tarefa": t, "atrasada": modelos.tarefa_esta_atrasada(t)} for t in lista_tarefas
    ]
    total = len(lista_tarefas)
    concluidas = len([t for t in lista_tarefas if t["estado"] == "concluída"])
    return render_template(
        "tarefas.html",
        tarefas_com_estado=tarefas_com_estado,
        total=total,
        concluidas=concluidas,
        hoje=date.today().isoformat(),
    )


@rotas.route("/tarefas", methods=["POST"])
@login_necessario
def criar_tarefa():
    titulo = request.form.get("titulo", "").strip()
    prazo = request.form.get("prazo", "").strip()

    if not titulo:
        flash("Escreva um título para a tarefa.", "erro")
        return redirect(url_for("rotas.tarefas"))

    modelos.criar_tarefa(titulo, prazo, session["id_utilizador"])
    flash("Tarefa adicionada.", "sucesso")
    return redirect(url_for("rotas.tarefas"))


@rotas.route("/tarefas/<int:id_tarefa>/editar", methods=["GET", "POST"])
@login_necessario
def editar_tarefa(id_tarefa):
    tarefa = modelos.obter_tarefa(id_tarefa, session["id_utilizador"])
    if not tarefa:
        flash("Tarefa não encontrada.", "erro")
        return redirect(url_for("rotas.tarefas"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        prazo = request.form.get("prazo", "").strip()
        if not titulo:
            flash("Escreva um título para a tarefa.", "erro")
            return render_template("editar_tarefa.html", tarefa=tarefa)

        modelos.editar_tarefa(id_tarefa, session["id_utilizador"], titulo, prazo)
        flash("Tarefa atualizada.", "sucesso")
        return redirect(url_for("rotas.tarefas"))

    return render_template("editar_tarefa.html", tarefa=tarefa)


@rotas.route("/tarefas/<int:id_tarefa>/concluir", methods=["POST"])
@login_necessario
def concluir_tarefa(id_tarefa):
    tarefa = modelos.obter_tarefa(id_tarefa, session["id_utilizador"])
    if not tarefa:
        flash("Tarefa não encontrada.", "erro")
    elif tarefa["estado"] == "concluída":
        modelos.reabrir_tarefa(id_tarefa, session["id_utilizador"])
    else:
        modelos.concluir_tarefa(id_tarefa, session["id_utilizador"])
    return redirect(url_for("rotas.tarefas"))


@rotas.route("/tarefas/<int:id_tarefa>/apagar", methods=["POST"])
@login_necessario
def apagar_tarefa(id_tarefa):
    modelos.apagar_tarefa(id_tarefa, session["id_utilizador"])
    flash("Tarefa eliminada.", "sucesso")
    return redirect(url_for("rotas.tarefas"))


# ---------------------------------------------------------------------------
# Eventos e calendário semanal
# ---------------------------------------------------------------------------

NOMES_DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]


@rotas.route("/calendario")
@login_necessario
def calendario():
    deslocamento = request.args.get("semana", default=0, type=int)
    hoje = date.today()
    inicio_semana_atual = hoje - timedelta(days=hoje.weekday())  # segunda-feira desta semana
    inicio_semana = inicio_semana_atual + timedelta(weeks=deslocamento)

    eventos = modelos.obter_eventos_da_semana(session["id_utilizador"], inicio_semana)

    dias = []
    for i in range(7):
        dia = inicio_semana + timedelta(days=i)
        eventos_do_dia = [e for e in eventos if e["data"] == dia.isoformat()]
        dias.append({
            "data": dia,
            "nome": NOMES_DIAS[i],
            "eventos": eventos_do_dia,
            "hoje": dia.isoformat() == hoje.isoformat(),
        })

    return render_template(
        "calendario.html",
        dias=dias,
        inicio_semana=inicio_semana,
        fim_semana=inicio_semana + timedelta(days=6),
        deslocamento=deslocamento,
    )


@rotas.route("/eventos", methods=["POST"])
@login_necessario
def criar_evento():
    titulo = request.form.get("titulo", "").strip()
    data_evento = request.form.get("data", "").strip()
    hora = request.form.get("hora", "").strip()
    deslocamento = request.form.get("semana", default=0, type=int)

    if not titulo or not data_evento:
        flash("Indique pelo menos o título e a data do evento.", "erro")
    else:
        modelos.criar_evento(titulo, data_evento, hora, session["id_utilizador"])
        flash("Evento adicionado.", "sucesso")

    return redirect(url_for("rotas.calendario", semana=deslocamento))


@rotas.route("/eventos/<int:id_evento>/apagar", methods=["POST"])
@login_necessario
def apagar_evento(id_evento):
    deslocamento = request.form.get("semana", default=0, type=int)
    modelos.apagar_evento(id_evento, session["id_utilizador"])
    flash("Evento eliminado.", "sucesso")
    return redirect(url_for("rotas.calendario", semana=deslocamento))
