/*
 * main.c — AgendaC
 *
 * Programa principal: gestor de contactos e tarefas em linha de
 * comandos, escrito em C. Serve como exemplo de nível avançado no
 * âmbito da UFCD 5425 — Projeto de Tecnologias e Programação de
 * Sistemas de Informação.
 *
 * Conceitos de C demonstrados neste exemplo:
 *   - organização do código em vários ficheiros .c/.h (módulos);
 *   - estruturas (struct) para agrupar dados relacionados;
 *   - arrays de tamanho fixo e gestão manual do seu preenchimento;
 *   - apontadores (ponteiros) para aceder e alterar dados sem os copiar;
 *   - enumerados (enum) para representar opções fixas;
 *   - leitura e escrita em ficheiros binários, para guardar dados
 *     entre execuções do programa.
 *
 * Para compilar (a partir desta pasta):
 *     gcc -Wall -Wextra -std=c11 -o agendac main.c contacto.c tarefa.c ficheiros.c utils.c
 *
 * Para executar:
 *     ./agendac
 */

#include <stdio.h>
#include "contacto.h"
#include "tarefa.h"
#include "ficheiros.h"
#include "utils.h"

/* Declarações das funções que implementam cada menu. Mantê-las
 * "estáticas" (static) significa que só são visíveis dentro deste
 * ficheiro — não há necessidade de as expor a outros módulos. */
static void menu_contactos(ListaContactos *lc);
static void menu_tarefas(ListaTarefas *lt);
static void guardar_tudo(const ListaContactos *lc, const ListaTarefas *lt);

int main(void) {
    ListaContactos contactos;
    ListaTarefas tarefas;
    int opcao;

    /* Ao iniciar, tentamos carregar dados gravados numa execução
     * anterior. Se não existirem (primeira utilização), as listas
     * ficam simplesmente vazias. */
    ficheiros_carregar_contactos(&contactos);
    ficheiros_carregar_tarefas(&tarefas);

    printf("=======================================\n");
    printf("   AgendaC - Gestor de Contactos e Tarefas\n");
    printf("=======================================\n");
    printf("(%d contacto(s) e %d tarefa(s) carregados)\n",
           contactos.total, tarefas.total);

    do {
        printf("\n----------- MENU PRINCIPAL -----------\n");
        printf("1. Gerir contactos\n");
        printf("2. Gerir tarefas\n");
        printf("3. Guardar dados agora\n");
        printf("0. Guardar e sair\n");
        opcao = ler_inteiro("Escolha uma opção: ", 0, 3);

        switch (opcao) {
            case 1:
                menu_contactos(&contactos);
                break;
            case 2:
                menu_tarefas(&tarefas);
                break;
            case 3:
                guardar_tudo(&contactos, &tarefas);
                pausar("Dados guardados. Pressione Enter para continuar...");
                break;
            case 0:
                guardar_tudo(&contactos, &tarefas);
                printf("Dados guardados. Até à próxima!\n");
                break;
        }
    } while (opcao != 0);

    return 0;
}

static void guardar_tudo(const ListaContactos *lc, const ListaTarefas *lt) {
    ficheiros_guardar_contactos(lc);
    ficheiros_guardar_tarefas(lt);
}

static void menu_contactos(ListaContactos *lc) {
    int opcao;
    char nome[TAM_NOME];
    char telefone[TAM_TELEFONE];
    char email[TAM_EMAIL];
    char termo[TAM_NOME];
    int id;

    do {
        printf("\n------- GESTÃO DE CONTACTOS -------\n");
        printf("1. Listar contactos\n");
        printf("2. Adicionar contacto\n");
        printf("3. Editar contacto\n");
        printf("4. Eliminar contacto\n");
        printf("5. Procurar contacto por nome\n");
        printf("0. Voltar ao menu principal\n");
        opcao = ler_inteiro("Escolha uma opção: ", 0, 5);

        switch (opcao) {
            case 1:
                contactos_listar(lc);
                break;

            case 2:
                printf("Nome: ");
                ler_linha(nome, sizeof(nome));
                printf("Telefone: ");
                ler_linha(telefone, sizeof(telefone));
                printf("Email: ");
                ler_linha(email, sizeof(email));

                int novo_id = contactos_adicionar(lc, nome, telefone, email);
                if (novo_id == -1) {
                    printf("Não foi possível adicionar: a agenda está cheia.\n");
                } else {
                    printf("Contacto adicionado com o número %d.\n", novo_id);
                }
                break;

            case 3:
                contactos_listar(lc);
                id = ler_inteiro("Número do contacto a editar (0 para cancelar): ", 0, 999999);
                if (id == 0) break;
                if (contactos_obter_por_id(lc, id) == NULL) {
                    printf("Não existe nenhum contacto com esse número.\n");
                    break;
                }
                printf("Novo nome: ");
                ler_linha(nome, sizeof(nome));
                printf("Novo telefone: ");
                ler_linha(telefone, sizeof(telefone));
                printf("Novo email: ");
                ler_linha(email, sizeof(email));
                contactos_editar(lc, id, nome, telefone, email);
                printf("Contacto atualizado.\n");
                break;

            case 4:
                contactos_listar(lc);
                id = ler_inteiro("Número do contacto a eliminar (0 para cancelar): ", 0, 999999);
                if (id == 0) break;
                if (contactos_eliminar(lc, id)) {
                    printf("Contacto eliminado.\n");
                } else {
                    printf("Não existe nenhum contacto com esse número.\n");
                }
                break;

            case 5:
                printf("Texto a procurar: ");
                ler_linha(termo, sizeof(termo));
                contactos_procurar_por_nome(lc, termo);
                break;
        }
    } while (opcao != 0);
}

static void menu_tarefas(ListaTarefas *lt) {
    int opcao;
    char titulo[TAM_TITULO];
    int id;

    do {
        printf("\n------- GESTÃO DE TAREFAS -------\n");
        printf("1. Listar tarefas (%d pendente(s))\n", tarefas_contar_pendentes(lt));
        printf("2. Adicionar tarefa\n");
        printf("3. Marcar/desmarcar como concluída\n");
        printf("4. Eliminar tarefa\n");
        printf("0. Voltar ao menu principal\n");
        opcao = ler_inteiro("Escolha uma opção: ", 0, 4);

        switch (opcao) {
            case 1:
                tarefas_listar(lt);
                break;

            case 2:
                printf("Título da tarefa: ");
                ler_linha(titulo, sizeof(titulo));
                int prioridade_num = ler_inteiro(
                    "Prioridade (1=Baixa, 2=Média, 3=Alta): ", 1, 3);

                int novo_id = tarefas_adicionar(lt, titulo, (Prioridade)prioridade_num);
                if (novo_id == -1) {
                    printf("Não foi possível adicionar: a lista está cheia.\n");
                } else {
                    printf("Tarefa adicionada com o número %d.\n", novo_id);
                }
                break;

            case 3:
                tarefas_listar(lt);
                id = ler_inteiro("Número da tarefa (0 para cancelar): ", 0, 999999);
                if (id == 0) break;
                if (tarefas_alternar_concluida(lt, id)) {
                    printf("Estado da tarefa atualizado.\n");
                } else {
                    printf("Não existe nenhuma tarefa com esse número.\n");
                }
                break;

            case 4:
                tarefas_listar(lt);
                id = ler_inteiro("Número da tarefa a eliminar (0 para cancelar): ", 0, 999999);
                if (id == 0) break;
                if (tarefas_eliminar(lt, id)) {
                    printf("Tarefa eliminada.\n");
                } else {
                    printf("Não existe nenhuma tarefa com esse número.\n");
                }
                break;
        }
    } while (opcao != 0);
}
