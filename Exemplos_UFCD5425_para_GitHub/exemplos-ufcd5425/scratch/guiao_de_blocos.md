# Guião de blocos — ListaDeTarefas

Este guião descreve, passo a passo, como construir o programa
"ListaDeTarefas" no editor do Scratch, bloco a bloco. Pode ser usado
de duas formas: para confirmar visualmente a estrutura do ficheiro
`ListaDeTarefas.sb3` já fornecido, ou como exercício — pedir aos
alunos que o reconstruam eles próprios, categoria por categoria.

## Parte 1 — Preparar as variáveis e a lista

Antes de colocar blocos no palco de programação, é preciso criar três
variáveis e uma lista (categoria **Variáveis**, botão "Criar uma
variável" / "Criar uma lista"):

| Nome       | Tipo     | Valor inicial |
|------------|----------|----------------|
| `escolha`  | variável | (vazio)        |
| `continuar`| variável | `1`             |
| `i`        | variável | `1`             |
| `Tarefas`  | lista     | (vazia)         |

## Parte 2 — O início do programa

1. Categoria **Eventos** → arrastar o bloco **quando a bandeira verde
   for clicada** para o palco de programação. Este é o bloco que
   inicia o programa sempre que se clica no ícone verde da bandeira,
   por cima do palco.
2. Categoria **Variáveis** → encaixar por baixo o bloco **apagar tudo
   de [Tarefas]**. Garante que o programa começa sempre com a lista
   vazia, mesmo que já tenha sido usado antes.
3. Categoria **Variáveis** → encaixar **definir [continuar] para
   (1)**. A variável `continuar` funciona como um "interruptor": o
   programa mantém-se em funcionamento enquanto ela valer `1`, e para
   quando passar a `0`.

## Parte 3 — O ciclo principal (o menu)

4. Categoria **Controlo** → encaixar o bloco **repetir até < >**.
   Dentro do espaço da condição (o hexágono), vamos colocar:
   - Categoria **Operadores** → o bloco **( ) = ( )**;
   - No lado esquerdo, arrastar a variável **continuar** (categoria
     Variáveis);
   - No lado direito, escrever o número `0`.

   Ou seja: o ciclo repete-se **até** `continuar = 0` — por outras
   palavras, continua enquanto `continuar` for `1`.

Dentro deste "repetir até" (na abertura em forma de "C"), vamos
encaixar, por esta ordem, os blocos das partes seguintes.

### 3.1 — Perguntar o que fazer

5. Categoria **Sensores** → **perguntar [O que quer fazer? Escreva:
   adicionar, listar, remover ou sair] e esperar**.
6. Categoria **Variáveis** → **definir [escolha] para ( )**, e dentro
   do espaço, categoria **Sensores** → o bloco reporter **resposta**
   (a bolinha oval que guarda o que a pessoa escreveu).

### 3.2 — Ramo "adicionar"

7. Categoria **Controlo** → **se < > então**. Na condição: bloco
   **( ) = ( )** (Operadores) com a variável **escolha** à esquerda e
   o texto `adicionar` à direita.
8. Dentro do "se": **perguntar [Qual é a tarefa?] e esperar**
   (Sensores).
9. A seguir: **acrescentar ( ) a [Tarefas]** (Variáveis), com o
   reporter **resposta** (Sensores) dentro do espaço do item.
10. A seguir: **dizer [Tarefa adicionada!] durante (1) segundos**
    (Aparência).

### 3.3 — Ramo "listar"

11. Outro bloco **se < > então**, com a condição **escolha = listar**.
12. Dentro: **definir [i] para (1)** (Variáveis) — `i` vai servir para
    percorrer a lista posição a posição, do 1 até ao fim.
13. A seguir, outro **repetir até < >**, com a condição
    **(i) > (comprimento de [Tarefas])** — os blocos "comprimento de"
    e o operador "maior que" ficam ambos na categoria
    Operadores/Variáveis.
14. Dentro deste ciclo interno:
    - **dizer ( ) durante (1) segundos** (Aparência), onde o texto é
      construído juntando três partes com dois blocos **juntar ( )
      ( )** (Operadores) encaixados um dentro do outro: primeiro
      **juntar (i) (". " + item)**, e dentro desse, **juntar (". ")
      (item (i) de [Tarefas])**. Na prática: "1. Comprar pão",
      "2. Estudar matemática", etc.
    - **mudar [i] por (1)** (Variáveis), para avançar para a posição
      seguinte.
15. Depois do ciclo (ainda dentro do "se listar", mas fora do "repetir
    até"): outro **se < > então** com a condição **comprimento de
    [Tarefas] = 0**, e dentro, **dizer [Ainda não há tarefas.] durante
    (1) segundos** — para o caso de a lista estar vazia.

### 3.4 — Ramo "remover"

16. Outro **se < > então**, condição **escolha = remover**.
17. Dentro: **perguntar [Qual o número da tarefa a remover?] e
    esperar** (Sensores).
18. A seguir: **apagar ( ) de [Tarefas]** (Variáveis), com o reporter
    **resposta** dentro do espaço do número.
19. A seguir: **dizer [Tarefa removida!] durante (1) segundos**.

### 3.5 — Ramo "sair"

20. Último **se < > então** do menu, condição **escolha = sair**.
21. Dentro: **definir [continuar] para (0)** — é este bloco que faz o
    "repetir até" principal parar na próxima verificação.
22. A seguir: **dizer [Até à próxima!] durante (1) segundos**.

## Parte 4 — Conferir a montagem

No final, dentro do grande "repetir até" do menu principal devem
estar, em sequência: o par pergunta+guardar escolha, seguido pelos
**quatro blocos "se"** (adicionar, listar, remover, sair), um a
seguir ao outro — nunca um dentro do outro, já que cada um trata uma
opção diferente e independente das outras.

## Sugestão de exploração com os alunos

Depois de montado, desafie os alunos a:

- Adicionar uma quinta opção ao menu, por exemplo **"editar"**, que
  pergunte o número da tarefa e o novo texto, e substitua o conteúdo
  dessa posição na lista (bloco **substituir item ( ) de [Tarefas]
  por ( )**);
- Fazer o ator "dizer" uma mensagem diferente se a pessoa escrever uma
  palavra que o programa não reconheça;
- Comparar esta solução com a versão em HTML/JavaScript
  (ContactosFácil, no Anexo A): os mesmos conceitos — guardar dados
  numa lista, perguntar, decidir, repetir — aparecem nas duas
  linguagens, apenas com uma sintaxe diferente.
