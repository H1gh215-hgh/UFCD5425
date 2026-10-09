/*
 * tarefa.c — AgendaC
 * Implementação das operações sobre a lista de tarefas.
 */

#include <stdio.h>
#include <string.h>
#include "tarefa.h"

void tarefas_inicializar(ListaTarefas *lt) {
    lt->total = 0;
    lt->proximo_id = 1;
}

int tarefas_adicionar(ListaTarefas *lt, const char *titulo, Prioridade prioridade) {
    if (lt->total >= MAX_TAREFAS) {
        return -1;
    }

    Tarefa *t = &lt->itens[lt->total];
    t->id = lt->proximo_id;
    strncpy(t->titulo, titulo, TAM_TITULO - 1);
    t->titulo[TAM_TITULO - 1] = '\0';
    t->prioridade = prioridade;
    t->concluida = 0;
    t->ativo = 1;

    lt->total++;
    lt->proximo_id++;
    return t->id;
}

static Tarefa *obter_por_id(ListaTarefas *lt, int id) {
    for (int i = 0; i < lt->total; i++) {
        if (lt->itens[i].ativo && lt->itens[i].id == id) {
            return &lt->itens[i];
        }
    }
    return NULL;
}

int tarefas_alternar_concluida(ListaTarefas *lt, int id) {
    Tarefa *t = obter_por_id(lt, id);
    if (t == NULL) {
        return 0;
    }
    t->concluida = !t->concluida;
    return 1;
}

int tarefas_eliminar(ListaTarefas *lt, int id) {
    Tarefa *t = obter_por_id(lt, id);
    if (t == NULL) {
        return 0;
    }
    t->ativo = 0;
    return 1;
}

const char *tarefas_nome_prioridade(Prioridade p) {
    switch (p) {
        case PRIORIDADE_BAIXA: return "Baixa";
        case PRIORIDADE_MEDIA: return "Média";
        case PRIORIDADE_ALTA:  return "Alta";
        default:                return "?";
    }
}

void tarefas_listar(const ListaTarefas *lt) {
    int encontrados = 0;

    printf("\n%-4s %-40s %-8s %-10s\n", "ID", "Título", "Prior.", "Estado");
    printf("--------------------------------------------------------------\n");

    /* Mostramos primeiro as tarefas de prioridade mais alta. Como a
     * lista nunca é muito grande num projeto deste tipo, um algoritmo
     * simples (percorrer todas as prioridades, da mais alta para a
     * mais baixa) é suficiente e fácil de entender. */
    for (int nivel = PRIORIDADE_ALTA; nivel >= PRIORIDADE_BAIXA; nivel--) {
        for (int i = 0; i < lt->total; i++) {
            const Tarefa *t = &lt->itens[i];
            if (t->ativo && (int)t->prioridade == nivel) {
                printf("%-4d %-40s %-8s %-10s\n",
                       t->id, t->titulo,
                       tarefas_nome_prioridade(t->prioridade),
                       t->concluida ? "Concluída" : "Pendente");
                encontrados++;
            }
        }
    }

    if (encontrados == 0) {
        printf("(ainda não há nenhuma tarefa guardada)\n");
    }
}

int tarefas_contar_pendentes(const ListaTarefas *lt) {
    int total = 0;
    for (int i = 0; i < lt->total; i++) {
        if (lt->itens[i].ativo && !lt->itens[i].concluida) {
            total++;
        }
    }
    return total;
}
