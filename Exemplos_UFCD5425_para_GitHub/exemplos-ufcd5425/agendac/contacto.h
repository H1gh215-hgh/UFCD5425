/*
 * contacto.h — AgendaC
 *
 * Define a estrutura "Contacto" e todas as operações disponíveis sobre
 * a lista de contactos: inicializar, adicionar, editar, eliminar,
 * listar e procurar.
 *
 * Nota pedagógica: em C não existem listas que crescem automaticamente
 * como em Python ou JavaScript. Por isso usamos um array de tamanho
 * fixo (MAX_CONTACTOS) e guardamos também quantos contactos estão
 * realmente a ser usados (campo "total").
 */

#ifndef CONTACTO_H
#define CONTACTO_H

#define MAX_CONTACTOS 100
#define TAM_NOME 50
#define TAM_TELEFONE 20
#define TAM_EMAIL 60

typedef struct {
    int id;
    char nome[TAM_NOME];
    char telefone[TAM_TELEFONE];
    char email[TAM_EMAIL];
    int ativo;  /* 1 = contacto válido; 0 = eliminado (eliminação lógica) */
} Contacto;

typedef struct {
    Contacto itens[MAX_CONTACTOS];
    int total;        /* número de posições ocupadas no array (incluindo inativas) */
    int proximo_id;    /* próximo identificador a atribuir a um novo contacto */
} ListaContactos;

/* Prepara a lista para começar vazia. Deve ser chamada antes de
 * qualquer outra operação sobre "lc". */
void contactos_inicializar(ListaContactos *lc);

/* Adiciona um novo contacto com os dados indicados. Devolve o id
 * atribuído, ou -1 se a lista já estiver cheia. */
int contactos_adicionar(ListaContactos *lc, const char *nome,
                         const char *telefone, const char *email);

/* Atualiza os dados do contacto com o id indicado. Devolve 1 se o
 * contacto foi encontrado e atualizado, ou 0 caso contrário. */
int contactos_editar(ListaContactos *lc, int id, const char *nome,
                      const char *telefone, const char *email);

/* Marca o contacto com o id indicado como eliminado. Devolve 1 se
 * encontrado, ou 0 caso contrário. Os dados não são removidos do
 * array (seria mais complexo deslocar os elementos seguintes); são
 * apenas marcados como inativos e deixam de ser mostrados. */
int contactos_eliminar(ListaContactos *lc, int id);

/* Mostra no ecrã todos os contactos ativos, em formato de tabela
 * simples. Mostra uma mensagem própria se não houver nenhum. */
void contactos_listar(const ListaContactos *lc);

/* Mostra os contactos cujo nome contém o texto "termo" (sem distinguir
 * maiúsculas de minúsculas). Devolve o número de resultados encontrados. */
int contactos_procurar_por_nome(const ListaContactos *lc, const char *termo);

/* Devolve um apontador para o contacto com o id indicado, ou NULL se
 * não existir (ou estiver inativo). Permite tanto ler como alterar
 * esse contacto diretamente a partir do apontador devolvido. */
Contacto *contactos_obter_por_id(ListaContactos *lc, int id);

#endif /* CONTACTO_H */
