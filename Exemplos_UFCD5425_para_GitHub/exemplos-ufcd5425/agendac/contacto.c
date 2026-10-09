/*
 * contacto.c — AgendaC
 * Implementação das operações sobre a lista de contactos.
 */

#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include "contacto.h"

/* strcasestr() não faz parte do C padrão (é uma extensão GNU, ausente
 * em vários compiladores, incluindo o MinGW no Windows). Para que este
 * programa compile em qualquer sistema, escrevemos a nossa própria
 * versão: procura "agulha" dentro de "palheiro", ignorando a diferença
 * entre maiúsculas e minúsculas. Devolve 1 se encontrar, 0 caso
 * contrário. */
static int contem_sem_distinguir_maiusculas(const char *palheiro, const char *agulha) {
    size_t tam_agulha = strlen(agulha);
    if (tam_agulha == 0) {
        return 1;
    }
    for (size_t i = 0; palheiro[i] != '\0'; i++) {
        size_t j = 0;
        while (j < tam_agulha &&
               palheiro[i + j] != '\0' &&
               tolower((unsigned char)palheiro[i + j]) == tolower((unsigned char)agulha[j])) {
            j++;
        }
        if (j == tam_agulha) {
            return 1;
        }
    }
    return 0;
}

void contactos_inicializar(ListaContactos *lc) {
    lc->total = 0;
    lc->proximo_id = 1;
}

int contactos_adicionar(ListaContactos *lc, const char *nome,
                         const char *telefone, const char *email) {
    if (lc->total >= MAX_CONTACTOS) {
        return -1;  /* lista cheia */
    }

    Contacto *c = &lc->itens[lc->total];
    c->id = lc->proximo_id;
    /* strncpy copia no máximo (tamanho - 1) caracteres e garante que
     * sobra sempre espaço para o '\0' final, escrito explicitamente
     * na linha seguinte — outra proteção comum contra buffer overflow. */
    strncpy(c->nome, nome, TAM_NOME - 1);
    c->nome[TAM_NOME - 1] = '\0';
    strncpy(c->telefone, telefone, TAM_TELEFONE - 1);
    c->telefone[TAM_TELEFONE - 1] = '\0';
    strncpy(c->email, email, TAM_EMAIL - 1);
    c->email[TAM_EMAIL - 1] = '\0';
    c->ativo = 1;

    lc->total++;
    lc->proximo_id++;
    return c->id;
}

Contacto *contactos_obter_por_id(ListaContactos *lc, int id) {
    for (int i = 0; i < lc->total; i++) {
        if (lc->itens[i].ativo && lc->itens[i].id == id) {
            return &lc->itens[i];
        }
    }
    return NULL;
}

int contactos_editar(ListaContactos *lc, int id, const char *nome,
                      const char *telefone, const char *email) {
    Contacto *c = contactos_obter_por_id(lc, id);
    if (c == NULL) {
        return 0;
    }
    strncpy(c->nome, nome, TAM_NOME - 1);
    c->nome[TAM_NOME - 1] = '\0';
    strncpy(c->telefone, telefone, TAM_TELEFONE - 1);
    c->telefone[TAM_TELEFONE - 1] = '\0';
    strncpy(c->email, email, TAM_EMAIL - 1);
    c->email[TAM_EMAIL - 1] = '\0';
    return 1;
}

int contactos_eliminar(ListaContactos *lc, int id) {
    Contacto *c = contactos_obter_por_id(lc, id);
    if (c == NULL) {
        return 0;
    }
    c->ativo = 0;
    return 1;
}

void contactos_listar(const ListaContactos *lc) {
    int encontrados = 0;

    printf("\n%-4s %-25s %-15s %-30s\n", "ID", "Nome", "Telefone", "Email");
    printf("--------------------------------------------------------------------\n");

    for (int i = 0; i < lc->total; i++) {
        const Contacto *c = &lc->itens[i];
        if (c->ativo) {
            printf("%-4d %-25s %-15s %-30s\n", c->id, c->nome, c->telefone, c->email);
            encontrados++;
        }
    }

    if (encontrados == 0) {
        printf("(ainda não há nenhum contacto guardado)\n");
    }
}

int contactos_procurar_por_nome(const ListaContactos *lc, const char *termo) {
    int encontrados = 0;

    printf("\nResultados para \"%s\":\n", termo);
    printf("%-4s %-25s %-15s %-30s\n", "ID", "Nome", "Telefone", "Email");
    printf("--------------------------------------------------------------------\n");

    for (int i = 0; i < lc->total; i++) {
        const Contacto *c = &lc->itens[i];
        if (c->ativo && contem_sem_distinguir_maiusculas(c->nome, termo)) {
            printf("%-4d %-25s %-15s %-30s\n", c->id, c->nome, c->telefone, c->email);
            encontrados++;
        }
    }

    if (encontrados == 0) {
        printf("(nenhum contacto corresponde à pesquisa)\n");
    }
    return encontrados;
}
