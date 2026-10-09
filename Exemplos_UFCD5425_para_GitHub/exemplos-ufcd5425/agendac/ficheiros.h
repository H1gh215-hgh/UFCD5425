/*
 * ficheiros.h — AgendaC
 *
 * Operações de gravação e leitura dos dados em disco, para que a
 * informação não se perca quando o programa termina.
 *
 * Nota pedagógica: usamos ficheiros BINÁRIOS (fwrite/fread), que
 * copiam a memória da estrutura diretamente para o ficheiro, byte a
 * byte. É a forma mais simples de guardar structs em C, mas tem uma
 * limitação importante que vale a pena discutir na aula: um ficheiro
 * binário só é garantido que se volta a ler corretamente no mesmo
 * tipo de computador/compilador que o criou. Para dados que precisem
 * de ser lidos por outros programas ou noutras máquinas, o mais
 * indicado seria um formato de texto (por exemplo CSV), à custa de
 * mais código.
 */

#ifndef FICHEIROS_H
#define FICHEIROS_H

#include "contacto.h"
#include "tarefa.h"

#define FICHEIRO_CONTACTOS "dados/contactos.dat"
#define FICHEIRO_TAREFAS "dados/tarefas.dat"

/* Grava toda a lista de contactos no ficheiro FICHEIRO_CONTACTOS.
 * Devolve 1 se a gravação foi bem sucedida, ou 0 em caso de erro
 * (por exemplo, se a pasta "dados" não existir). */
int ficheiros_guardar_contactos(const ListaContactos *lc);

/* Lê a lista de contactos do ficheiro FICHEIRO_CONTACTOS para "lc".
 * Se o ficheiro ainda não existir (primeira utilização do programa),
 * "lc" é apenas inicializado vazio e a função devolve 0, sem ser
 * considerado um erro grave. */
int ficheiros_carregar_contactos(ListaContactos *lc);

/* Equivalentes para a lista de tarefas. */
int ficheiros_guardar_tarefas(const ListaTarefas *lt);
int ficheiros_carregar_tarefas(ListaTarefas *lt);

#endif /* FICHEIROS_H */
