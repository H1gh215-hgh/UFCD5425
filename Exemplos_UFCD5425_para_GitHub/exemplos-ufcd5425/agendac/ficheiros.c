/*
 * ficheiros.c — AgendaC
 * Implementação da gravação/leitura em ficheiros binários.
 */

#include <stdio.h>
#include "ficheiros.h"

int ficheiros_guardar_contactos(const ListaContactos *lc) {
    FILE *f = fopen(FICHEIRO_CONTACTOS, "wb");
    if (f == NULL) {
        return 0;
    }

    /* Gravamos primeiro os dois números de controlo (total e
     * próximo_id) e depois o array de contactos. Ao gravar o array
     * completo (MAX_CONTACTOS elementos) simplificamos a leitura,
     * ao preço de o ficheiro ocupar sempre o mesmo tamanho, mesmo com
     * poucos contactos — uma troca razoável para um programa deste
     * nível. */
    fwrite(&lc->total, sizeof(int), 1, f);
    fwrite(&lc->proximo_id, sizeof(int), 1, f);
    fwrite(lc->itens, sizeof(Contacto), MAX_CONTACTOS, f);

    fclose(f);
    return 1;
}

int ficheiros_carregar_contactos(ListaContactos *lc) {
    contactos_inicializar(lc);

    FILE *f = fopen(FICHEIRO_CONTACTOS, "rb");
    if (f == NULL) {
        return 0;  /* ainda não existem dados gravados — não é um erro */
    }

    fread(&lc->total, sizeof(int), 1, f);
    fread(&lc->proximo_id, sizeof(int), 1, f);
    fread(lc->itens, sizeof(Contacto), MAX_CONTACTOS, f);

    fclose(f);
    return 1;
}

int ficheiros_guardar_tarefas(const ListaTarefas *lt) {
    FILE *f = fopen(FICHEIRO_TAREFAS, "wb");
    if (f == NULL) {
        return 0;
    }

    fwrite(&lt->total, sizeof(int), 1, f);
    fwrite(&lt->proximo_id, sizeof(int), 1, f);
    fwrite(lt->itens, sizeof(Tarefa), MAX_TAREFAS, f);

    fclose(f);
    return 1;
}

int ficheiros_carregar_tarefas(ListaTarefas *lt) {
    tarefas_inicializar(lt);

    FILE *f = fopen(FICHEIRO_TAREFAS, "rb");
    if (f == NULL) {
        return 0;
    }

    fread(&lt->total, sizeof(int), 1, f);
    fread(&lt->proximo_id, sizeof(int), 1, f);
    fread(lt->itens, sizeof(Tarefa), MAX_TAREFAS, f);

    fclose(f);
    return 1;
}
