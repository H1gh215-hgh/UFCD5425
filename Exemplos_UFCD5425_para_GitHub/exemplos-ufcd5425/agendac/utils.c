/*
 * utils.c — AgendaC
 * Implementação das funções auxiliares declaradas em utils.h.
 */

#include <stdio.h>
#include <string.h>
#include "utils.h"

void ler_linha(char *destino, int tamanho) {
    if (fgets(destino, tamanho, stdin) != NULL) {
        /* fgets() guarda a mudança de linha ('\n') dentro da string.
         * Procuramo-la e substituímo-la por '\0' para a eliminar. */
        size_t comprimento = strlen(destino);
        if (comprimento > 0 && destino[comprimento - 1] == '\n') {
            destino[comprimento - 1] = '\0';
        }
    } else {
        destino[0] = '\0';
    }
}

int ler_inteiro(const char *mensagem, int minimo, int maximo) {
    char linha[32];
    int valor;
    int valido;

    do {
        printf("%s", mensagem);
        ler_linha(linha, sizeof(linha));

        /* sscanf devolve o número de valores lidos com sucesso.
         * Se não conseguir converter "linha" para um inteiro, devolve 0. */
        valido = (sscanf(linha, "%d", &valor) == 1);

        if (!valido) {
            printf("  -> Valor inválido. Escreva apenas um número.\n");
        } else if (valor < minimo || valor > maximo) {
            printf("  -> O número deve estar entre %d e %d.\n", minimo, maximo);
            valido = 0;
        }
    } while (!valido);

    return valor;
}

void pausar(const char *mensagem) {
    printf("%s", mensagem);
    char linha[8];
    ler_linha(linha, sizeof(linha));
}

void limpar_ecra(void) {
    printf("\n\n");
}
