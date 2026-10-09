/*
 * tarefa.h — AgendaC
 *
 * Define a estrutura "Tarefa" e as operações sobre a lista de tarefas.
 * Funciona de forma semelhante ao módulo "contacto", mas acrescenta
 * dois conceitos novos: um tipo enumerado (enum) para representar um
 * conjunto fixo de opções (a prioridade), e um indicador de estado
 * (concluída ou não).
 */

#ifndef TAREFA_H
#define TAREFA_H

#define MAX_TAREFAS 100
#define TAM_TITULO 80

/* Um "enum" dá nomes a um conjunto de valores inteiros, tornando o
 * código mais legível do que usar números "mágicos" como 1, 2 e 3
 * diretamente. */
typedef enum {
    PRIORIDADE_BAIXA = 1,
    PRIORIDADE_MEDIA = 2,
    PRIORIDADE_ALTA = 3
} Prioridade;

typedef struct {
    int id;
    char titulo[TAM_TITULO];
    Prioridade prioridade;
    int concluida;  /* 0 = pendente; 1 = concluída */
    int ativo;       /* 1 = tarefa válida; 0 = eliminada (eliminação lógica) */
} Tarefa;

typedef struct {
    Tarefa itens[MAX_TAREFAS];
    int total;
    int proximo_id;
} ListaTarefas;

void tarefas_inicializar(ListaTarefas *lt);

/* Adiciona uma nova tarefa pendente. Devolve o id atribuído, ou -1
 * se a lista estiver cheia. */
int tarefas_adicionar(ListaTarefas *lt, const char *titulo, Prioridade prioridade);

/* Alterna o estado da tarefa entre pendente e concluída. Devolve 1 se
 * a tarefa foi encontrada, ou 0 caso contrário. */
int tarefas_alternar_concluida(ListaTarefas *lt, int id);

/* Marca a tarefa como eliminada. Devolve 1 se encontrada, 0 caso
 * contrário. */
int tarefas_eliminar(ListaTarefas *lt, int id);

/* Mostra todas as tarefas ativas, ordenadas por prioridade (mais alta
 * primeiro) e indicando se já foram concluídas. */
void tarefas_listar(const ListaTarefas *lt);

/* Devolve o número de tarefas pendentes (ainda não concluídas). */
int tarefas_contar_pendentes(const ListaTarefas *lt);

/* Converte o valor da prioridade no texto correspondente ("Baixa",
 * "Média" ou "Alta"), para facilitar a exibição no ecrã. */
const char *tarefas_nome_prioridade(Prioridade p);

#endif /* TAREFA_H */
