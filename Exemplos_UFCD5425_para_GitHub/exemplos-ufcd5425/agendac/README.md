# AgendaC

Gestor de contactos e tarefas em linha de comandos, escrito em **C
puro (padrão C11)**, sem bibliotecas externas. Serve como exemplo de
nível avançado no âmbito da UFCD 5425 — Projeto de Tecnologias e
Programação de Sistemas de Informação.

## Porque é o exemplo mais avançado dos quatro

Em comparação com o ContactosFácil (HTML/JS) e o TarefaFácil
(Python/Flask), este exemplo exige que o programador faça manualmente
tarefas que, nas outras linguagens, são feitas automaticamente:

- gerir a memória e o tamanho das listas (arrays de tamanho fixo, em
  vez de listas que crescem sozinhas);
- controlar com cuidado o tamanho de cada texto copiado para uma
  variável, para não escrever para fora dos limites de um array
  (*buffer overflow*);
- ler e escrever diretamente bytes num ficheiro, em vez de usar uma
  base de dados já pronta.

Por isso, este programa é o que exige mais atenção aos detalhes — e o
mais indicado para alunos que já têm alguma confiança com os
conceitos básicos de programação.

## Como compilar e executar

Com o `make` instalado:

```bash
make
./agendac
```

Sem `make`, diretamente com o `gcc`:

```bash
gcc -Wall -Wextra -std=c11 -o agendac main.c contacto.c tarefa.c ficheiros.c utils.c
./agendac
```

## Estrutura do projeto

```
agendac/
  main.c          # programa principal e menus
  contacto.h/.c    # estrutura Contacto e as suas operações
  tarefa.h/.c      # estrutura Tarefa e as suas operações
  ficheiros.h/.c   # gravação/leitura em ficheiros binários
  utils.h/.c       # leitura seguro de texto e números do teclado
  dados/            # onde são guardados contactos.dat e tarefas.dat
  Makefile
```

## Funcionalidades

- Contactos: adicionar, listar, editar, eliminar e procurar por nome.
- Tarefas: adicionar (com prioridade baixa/média/alta), listar
  (ordenadas por prioridade), marcar/desmarcar como concluída, e
  eliminar.
- Os dados ficam gravados em `dados/contactos.dat` e
  `dados/tarefas.dat` e são lidos automaticamente da próxima vez que
  o programa é executado.

## Limitações conhecidas (propositadamente simples)

- O número máximo de contactos e de tarefas é fixo (100 de cada),
  definido no topo de `contacto.h` e `tarefa.h`.
- Os ficheiros `.dat` são binários: guardam a memória das estruturas
  diretamente, o que é simples de programar mas significa que só são
  garantidamente lidos corretamente no mesmo tipo de computador e
  compilador que os criou. Para um projeto final mais robusto, uma
  alternativa a explorar seria gravar os dados em formato de texto
  (por exemplo CSV).
