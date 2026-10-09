# TarefaFácil

Aplicação web em **Python (Flask) + SQLite** para gerir tarefas e um
calendário semanal de eventos. Serve como exemplo de nível intermédio
no âmbito da UFCD 5425 — Projeto de Tecnologias e Programação de
Sistemas de Informação.

## Funcionalidades

- Registo e autenticação de utilizadores (palavra-passe encriptada).
- Criação, edição, conclusão e eliminação de tarefas.
- Deteção automática de tarefas atrasadas (prazo já passado e não
  concluídas).
- Calendário semanal com navegação entre semanas e criação/eliminação
  de eventos.
- Dados guardados numa base de dados SQLite local.

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requisitos.txt
python run.py
```

A aplicação fica disponível em `http://127.0.0.1:5000`.

## Estrutura do projeto

```
tarefafacil/
  app/
    __init__.py      # fábrica da aplicação (criar_app)
    modelos.py        # acesso à base de dados (SQLite)
    rotas.py           # rotas/endereços da aplicação
  templates/           # páginas HTML (Jinja2)
  static/
    css/estilo.css
    js/app.js
  bd/                   # onde é criada a base de dados (tarefafacil.db)
  run.py
  requisitos.txt
```

## Objetivo pedagógico

Este exemplo mostra uma aplicação com **várias entidades relacionadas**
(utilizadores, tarefas, eventos), autenticação, e persistência em
base de dados — um passo acima do exemplo ContactosFácil, preparando
os alunos para projetos finais mais completos.
