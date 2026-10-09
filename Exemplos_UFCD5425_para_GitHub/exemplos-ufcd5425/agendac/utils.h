/*
 * utils.h — AgendaC
 *
 * Pequenas funções auxiliares de entrada de dados, usadas em todo o
 * programa para ler texto e números do teclado de forma segura.
 */

#ifndef UTILS_H
#define UTILS_H

/* Lê uma linha de texto do teclado para "destino", com no máximo
 * "tamanho" caracteres (incluindo o caracter final '\0'). Remove a
 * mudança de linha final, caso exista. Usar fgets() em vez de
 * scanf("%s") evita um dos erros mais comuns em C: ultrapassar o
 * limite de um array de caracteres (buffer overflow). */
void ler_linha(char *destino, int tamanho);

/* Pede repetidamente um número inteiro ao utilizador, mostrando
 * "mensagem", até receber um valor válido entre "minimo" e "maximo"
 * (inclusive). Nunca é possível "bloquear" o programa com uma
 * resposta inválida — a função só devolve quando o valor é correto. */
int ler_inteiro(const char *mensagem, int minimo, int maximo);

/* Mostra "mensagem" e espera que o utilizador pressione Enter.
 * Útil para pausar o ecrã antes de voltar a um menu. */
void pausar(const char *mensagem);

/* Limpa o ecrã do terminal (funciona em Linux/macOS; em Windows
 * mostra apenas várias linhas em branco, para manter o código
 * simples e portátil). */
void limpar_ecra(void);

#endif /* UTILS_H */
