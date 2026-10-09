#!/usr/bin/env python3
"""
gerar_sb3.py — gera o ficheiro "ListaDeTarefas.sb3" (Scratch 3) usado
como exemplo de nível inicial (programação em blocos) na UFCD 5425.

Em vez de desenhar os blocos à mão no editor do Scratch e exportar o
ficheiro, este script gera diretamente o "project.json" que um
ficheiro .sb3 contém (um .sb3 é, no fundo, um ficheiro .zip com esse
JSON e os ficheiros das imagens/sons usados). Isto permite reconstruir
o exemplo de forma reprodutível e documentada.

O programa gerado pode ser aberto normalmente no editor do Scratch
(https://scratch.mit.edu ou a aplicação offline) ou no TurboWarp
(https://turbowarp.org), e os blocos podem ser inspecionados e
editados como qualquer outro projeto Scratch.
"""

import hashlib
import json
import zipfile
from pathlib import Path

PASTA = Path(__file__).parent
SAIDA = PASTA / "ListaDeTarefas.sb3"


# ---------------------------------------------------------------------------
# Construtor de blocos — pequenas funções auxiliares que montam a
# estrutura JSON exigida pelo formato .sb3, para não a escrever à mão
# repetidamente (e arriscar erros de cópia).
# ---------------------------------------------------------------------------

class Construtor:
    def __init__(self):
        self.blocos = {}
        self._contador = 0

    def _novo_id(self, prefixo):
        self._contador += 1
        return f"{prefixo}{self._contador}"

    def bloco(self, opcode, inputs=None, fields=None, top_level=False, x=0, y=0, prefixo="b"):
        id_ = self._novo_id(prefixo)
        self.blocos[id_] = {
            "opcode": opcode,
            "next": None,
            "parent": None,
            "inputs": inputs or {},
            "fields": fields or {},
            "shadow": False,
            "topLevel": top_level,
        }
        if top_level:
            self.blocos[id_]["x"] = x
            self.blocos[id_]["y"] = y
        return id_

    def ligar_pilha(self, ids, pai_id):
        """Liga uma lista de ids de blocos em sequência (cada um é o
        "next" do anterior) e define o "parent" de cada um — o
        primeiro aponta para "pai_id" (o bloco ou script que os
        contém), os seguintes apontam para o bloco anterior na
        pilha."""
        ids = [i for i in ids if i is not None]
        if not ids:
            return None
        for posicao, id_ in enumerate(ids):
            self.blocos[id_]["parent"] = pai_id if posicao == 0 else ids[posicao - 1]
            self.blocos[id_]["next"] = ids[posicao + 1] if posicao + 1 < len(ids) else None
        return ids[0]


# Tipos de "shadow" usados dentro dos arrays de input, conforme o
# formato .sb3 (ver documentação do Scratch File Format):
#   4 = número, 10 = texto, 12 = variável, 13 = lista
def valor_texto(texto):
    return [1, [10, str(texto)]]


def valor_numero(numero):
    return [1, [4, str(numero)]]


def valor_bloco(id_bloco):
    """Uma entrada cujo valor vem de outro bloco (um "reporter",
    como uma operação ou uma pergunta)."""
    return [2, id_bloco]


def valor_variavel(nome, id_var):
    """Uma entrada cujo valor é diretamente uma variável — o Scratch
    representa isto sem criar um bloco "data_variable" próprio,
    usando antes este formato abreviado."""
    return [3, [12, nome, id_var], [10, ""]]


def campo(nome, id_):
    return [nome, id_]


def gerar_projeto():
    c = Construtor()

    # -----------------------------------------------------------------
    # Variáveis e lista usadas no projeto (identificadores + nomes)
    # -----------------------------------------------------------------
    VAR_ESCOLHA = "var_escolha"
    VAR_CONTINUAR = "var_continuar"
    VAR_I = "var_i"
    LISTA_TAREFAS = "lista_tarefas"

    variaveis = {
        VAR_ESCOLHA: ["escolha", ""],
        VAR_CONTINUAR: ["continuar", 1],
        VAR_I: ["i", 1],
    }
    listas = {
        LISTA_TAREFAS: ["Tarefas", []],
    }

    # -----------------------------------------------------------------
    # Bloco "quando a bandeira verde for clicada" (início do programa)
    # -----------------------------------------------------------------
    id_bandeira = c.bloco("event_whenflagclicked", top_level=True, x=50, y=50)

    id_apagar_tudo = c.bloco(
        "data_deletealloflist",
        fields={"LIST": campo("Tarefas", LISTA_TAREFAS)},
    )

    id_iniciar_continuar = c.bloco(
        "data_setvariableto",
        fields={"VARIABLE": campo("continuar", VAR_CONTINUAR)},
        inputs={"VALUE": valor_numero(1)},
    )

    # -----------------------------------------------------------------
    # Corpo do "repetir até continuar = 0" — o menu principal
    # -----------------------------------------------------------------

    # condição: continuar = 0
    id_cond_zero = c.bloco("operator_equals")
    c.blocos[id_cond_zero]["inputs"] = {
        "OPERAND1": valor_variavel("continuar", VAR_CONTINUAR),
        "OPERAND2": valor_numero(0),
    }

    # pergunta principal
    id_perguntar_menu = c.bloco(
        "sensing_askandwait",
        inputs={
            "QUESTION": valor_texto(
                "O que quer fazer? Escreva: adicionar, listar, remover ou sair"
            )
        },
    )
    id_guardar_escolha = c.bloco(
        "data_setvariableto",
        fields={"VARIABLE": campo("escolha", VAR_ESCOLHA)},
        inputs={"VALUE": valor_bloco(c.bloco("sensing_answer"))},
    )

    # --- ramo "adicionar" ---
    id_cond_adicionar = c.bloco("operator_equals")
    c.blocos[id_cond_adicionar]["inputs"] = {
        "OPERAND1": valor_variavel("escolha", VAR_ESCOLHA),
        "OPERAND2": valor_texto("adicionar"),
    }
    id_perguntar_tarefa = c.bloco(
        "sensing_askandwait",
        inputs={"QUESTION": valor_texto("Qual é a tarefa?")},
    )
    id_adicionar_lista = c.bloco(
        "data_addtolist",
        fields={"LIST": campo("Tarefas", LISTA_TAREFAS)},
        inputs={"ITEM": valor_bloco(c.bloco("sensing_answer"))},
    )
    id_dizer_adicionada = c.bloco(
        "looks_sayforsecs",
        inputs={"MESSAGE": valor_texto("Tarefa adicionada!"), "SECS": valor_numero(1)},
    )
    id_primeiro_adicionar = c.ligar_pilha(
        [id_perguntar_tarefa, id_adicionar_lista, id_dizer_adicionada], None
    )
    id_if_adicionar = c.bloco(
        "control_if",
        inputs={
            "CONDITION": valor_bloco(id_cond_adicionar),
            "SUBSTACK": valor_bloco(id_primeiro_adicionar),
        },
    )
    c.blocos[id_primeiro_adicionar]["parent"] = id_if_adicionar

    # --- ramo "listar" ---
    id_cond_listar = c.bloco("operator_equals")
    c.blocos[id_cond_listar]["inputs"] = {
        "OPERAND1": valor_variavel("escolha", VAR_ESCOLHA),
        "OPERAND2": valor_texto("listar"),
    }

    id_definir_i = c.bloco(
        "data_setvariableto",
        fields={"VARIABLE": campo("i", VAR_I)},
        inputs={"VALUE": valor_numero(1)},
    )

    # condição do ciclo interno: i > comprimento da lista
    id_comprimento_lista = c.bloco(
        "data_lengthoflist", fields={"LIST": campo("Tarefas", LISTA_TAREFAS)}
    )
    id_cond_fim_lista = c.bloco("operator_gt")
    c.blocos[id_cond_fim_lista]["inputs"] = {
        "OPERAND1": valor_variavel("i", VAR_I),
        "OPERAND2": valor_bloco(id_comprimento_lista),
    }

    # corpo do ciclo: diz "i. tarefa" e incrementa i
    id_item_lista = c.bloco(
        "data_itemoflist",
        fields={"LIST": campo("Tarefas", LISTA_TAREFAS)},
        inputs={"INDEX": valor_variavel("i", VAR_I)},
    )
    id_juntar_texto = c.bloco("operator_join")
    id_juntar_ponto = c.bloco("operator_join")
    c.blocos[id_juntar_ponto]["inputs"] = {
        "STRING1": valor_texto(". "),
        "STRING2": valor_bloco(id_item_lista),
    }
    c.blocos[id_juntar_texto]["inputs"] = {
        "STRING1": valor_variavel("i", VAR_I),
        "STRING2": valor_bloco(id_juntar_ponto),
    }
    id_dizer_item = c.bloco(
        "looks_sayforsecs",
        inputs={"MESSAGE": valor_bloco(id_juntar_texto), "SECS": valor_numero(1)},
    )
    id_incrementar_i = c.bloco(
        "data_changevariableby",
        fields={"VARIABLE": campo("i", VAR_I)},
        inputs={"VALUE": valor_numero(1)},
    )
    id_primeiro_corpo_ciclo = c.ligar_pilha([id_dizer_item, id_incrementar_i], None)

    id_repetir_listagem = c.bloco(
        "control_repeat_until",
        inputs={
            "CONDITION": valor_bloco(id_cond_fim_lista),
            "SUBSTACK": valor_bloco(id_primeiro_corpo_ciclo),
        },
    )
    c.blocos[id_primeiro_corpo_ciclo]["parent"] = id_repetir_listagem

    # mensagem quando a lista está vazia
    id_cond_lista_vazia = c.bloco("operator_equals")
    c.blocos[id_cond_lista_vazia]["inputs"] = {
        "OPERAND1": valor_bloco(
            c.bloco("data_lengthoflist", fields={"LIST": campo("Tarefas", LISTA_TAREFAS)})
        ),
        "OPERAND2": valor_numero(0),
    }
    id_dizer_vazia = c.bloco(
        "looks_sayforsecs",
        inputs={"MESSAGE": valor_texto("Ainda não há tarefas."), "SECS": valor_numero(1)},
    )
    id_if_vazia = c.bloco(
        "control_if",
        inputs={"CONDITION": valor_bloco(id_cond_lista_vazia), "SUBSTACK": valor_bloco(id_dizer_vazia)},
    )
    c.blocos[id_dizer_vazia]["parent"] = id_if_vazia

    id_primeiro_listar = c.ligar_pilha(
        [id_definir_i, id_repetir_listagem, id_if_vazia], None
    )
    id_if_listar = c.bloco(
        "control_if",
        inputs={"CONDITION": valor_bloco(id_cond_listar), "SUBSTACK": valor_bloco(id_primeiro_listar)},
    )
    c.blocos[id_primeiro_listar]["parent"] = id_if_listar

    # --- ramo "remover" ---
    id_cond_remover = c.bloco("operator_equals")
    c.blocos[id_cond_remover]["inputs"] = {
        "OPERAND1": valor_variavel("escolha", VAR_ESCOLHA),
        "OPERAND2": valor_texto("remover"),
    }
    id_perguntar_numero = c.bloco(
        "sensing_askandwait",
        inputs={"QUESTION": valor_texto("Qual o número da tarefa a remover?")},
    )
    id_remover_item = c.bloco(
        "data_deleteoflist",
        fields={"LIST": campo("Tarefas", LISTA_TAREFAS)},
        inputs={"INDEX": valor_bloco(c.bloco("sensing_answer"))},
    )
    id_dizer_removida = c.bloco(
        "looks_sayforsecs",
        inputs={"MESSAGE": valor_texto("Tarefa removida!"), "SECS": valor_numero(1)},
    )
    id_primeiro_remover = c.ligar_pilha(
        [id_perguntar_numero, id_remover_item, id_dizer_removida], None
    )
    id_if_remover = c.bloco(
        "control_if",
        inputs={"CONDITION": valor_bloco(id_cond_remover), "SUBSTACK": valor_bloco(id_primeiro_remover)},
    )
    c.blocos[id_primeiro_remover]["parent"] = id_if_remover

    # --- ramo "sair" ---
    id_cond_sair = c.bloco("operator_equals")
    c.blocos[id_cond_sair]["inputs"] = {
        "OPERAND1": valor_variavel("escolha", VAR_ESCOLHA),
        "OPERAND2": valor_texto("sair"),
    }
    id_definir_continuar_zero = c.bloco(
        "data_setvariableto",
        fields={"VARIABLE": campo("continuar", VAR_CONTINUAR)},
        inputs={"VALUE": valor_numero(0)},
    )
    id_dizer_adeus = c.bloco(
        "looks_sayforsecs",
        inputs={"MESSAGE": valor_texto("Até à próxima!"), "SECS": valor_numero(1)},
    )
    id_primeiro_sair = c.ligar_pilha([id_definir_continuar_zero, id_dizer_adeus], None)
    id_if_sair = c.bloco(
        "control_if",
        inputs={"CONDITION": valor_bloco(id_cond_sair), "SUBSTACK": valor_bloco(id_primeiro_sair)},
    )
    c.blocos[id_primeiro_sair]["parent"] = id_if_sair

    # -----------------------------------------------------------------
    # Monta o corpo do repetir-até principal: pergunta + guardar
    # escolha + os quatro "se"
    # -----------------------------------------------------------------
    id_primeiro_menu = c.ligar_pilha(
        [
            id_perguntar_menu,
            id_guardar_escolha,
            id_if_adicionar,
            id_if_listar,
            id_if_remover,
            id_if_sair,
        ],
        None,
    )

    id_repetir_principal = c.bloco(
        "control_repeat_until",
        inputs={"CONDITION": valor_bloco(id_cond_zero), "SUBSTACK": valor_bloco(id_primeiro_menu)},
    )
    c.blocos[id_primeiro_menu]["parent"] = id_repetir_principal

    # -----------------------------------------------------------------
    # Liga o script completo ao bloco do "quando a bandeira verde for
    # clicada"
    # -----------------------------------------------------------------
    c.ligar_pilha([id_bandeira, id_apagar_tudo, id_iniciar_continuar, id_repetir_principal], None)

    return c.blocos, variaveis, listas


# ---------------------------------------------------------------------------
# Imagens (costumes) minímas em SVG — um fundo de palco em branco e um
# "gato" simplificado para o ator. O Scratch exige que todos os alvos
# (palco e atores) tenham pelo menos uma imagem.
# ---------------------------------------------------------------------------

SVG_PALCO = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360">'
    '<rect width="480" height="360" fill="#ffffff"/></svg>'
)

SVG_ATOR = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" '
    'viewBox="0 0 60 60">'
    '<circle cx="30" cy="30" r="26" fill="#f2a65a" stroke="#0f2c3f" stroke-width="3"/>'
    '<text x="30" y="38" font-size="24" text-anchor="middle" '
    'font-family="sans-serif">📋</text>'
    "</svg>"
)


def asset_svg(conteudo_svg, nome):
    dados = conteudo_svg.encode("utf-8")
    md5 = hashlib.md5(dados).hexdigest()
    nome_ficheiro = f"{md5}.svg"
    costume = {
        "assetId": md5,
        "name": nome,
        "md5ext": nome_ficheiro,
        "dataFormat": "svg",
        "rotationCenterX": 30,
        "rotationCenterY": 30,
    }
    return costume, nome_ficheiro, dados


def main():
    blocos, variaveis, listas = gerar_projeto()

    custom_palco, ficheiro_palco, dados_palco = asset_svg(SVG_PALCO, "palco1")
    custom_ator, ficheiro_ator, dados_ator = asset_svg(SVG_ATOR, "ator1")

    alvo_palco = {
        "isStage": True,
        "name": "Stage",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": {},
        "comments": {},
        "currentCostume": 0,
        "costumes": [custom_palco],
        "sounds": [],
        "volume": 100,
        "layerOrder": 0,
        "tempo": 60,
        "videoTransparency": 50,
        "videoState": "on",
        "textToSpeechLanguage": None,
    }

    alvo_ator = {
        "isStage": False,
        "name": "Assistente",
        "variables": variaveis,
        "lists": listas,
        "broadcasts": {},
        "blocks": blocos,
        "comments": {},
        "currentCostume": 0,
        "costumes": [custom_ator],
        "sounds": [],
        "volume": 100,
        "layerOrder": 1,
        "visible": True,
        "x": 0,
        "y": 0,
        "size": 100,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around",
    }

    projeto = {
        "targets": [alvo_palco, alvo_ator],
        "monitors": [],
        "extensions": [],
        "meta": {
            "semver": "3.0.0",
            "vm": "5.0.300",
            "agent": "",
        },
    }

    with zipfile.ZipFile(SAIDA, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("project.json", json.dumps(projeto, ensure_ascii=False))
        zf.writestr(ficheiro_palco, dados_palco)
        zf.writestr(ficheiro_ator, dados_ator)

    print(f"Gerado: {SAIDA} ({SAIDA.stat().st_size} bytes)")
    print(f"Total de blocos no ator: {len(blocos)}")


if __name__ == "__main__":
    main()
