# ListaDeTarefas (Scratch)

Pequeno programa em **Scratch 3.0** (programação em blocos) que
implementa uma lista de tarefas simples. Serve como exemplo de nível
inicial no âmbito da UFCD 5425 — Projeto de Tecnologias e Programação
de Sistemas de Informação, pensado para alunos que estão a dar os
primeiros passos na programação.

## Como abrir

O ficheiro `ListaDeTarefas.sb3` pode ser aberto:

- Online, em <https://scratch.mit.edu/create> (menu Ficheiro → Carregar
  do seu computador);
- Na aplicação Scratch Desktop (offline);
- Em <https://turbowarp.org>, uma versão compatível que corre
  diretamente no browser.

## O que o programa faz

Ao clicar na bandeira verde, o ator pergunta repetidamente o que o
utilizador quer fazer, e entende quatro palavras:

- **adicionar** — pergunta o nome da tarefa e acrescenta-a à lista;
- **listar** — mostra todas as tarefas guardadas, numeradas;
- **remover** — pergunta o número da tarefa e remove-a da lista;
- **sair** — termina o programa.

Todos os dados ficam guardados na lista "Tarefas", visível no palco
enquanto o programa corre.

## Conceitos de programação em blocos demonstrados

- Eventos (bloco "quando a bandeira verde for clicada");
- Variáveis (`escolha`, `continuar`, `i`);
- Uma lista (`Tarefas`) e as suas operações: acrescentar, remover,
  obter item pela posição, calcular o comprimento;
- Ciclos ("repetir até");
- Decisões ("se ... então"), incluindo várias decisões seguidas para
  tratar cada opção do menu;
- Interação com o utilizador ("perguntar ... e esperar");
- Texto: juntar (concatenar) palavras e números para formar uma frase.

Este programa foi pensado para ser o primeiro dos quatro exemplos do
Anexo A: antes de programar em HTML/JavaScript, Python ou C, os alunos
podem ver e alterar exatamente a mesma lógica (um menu que pergunta o
que fazer, e trata cada opção) em blocos visuais, sem se preocuparem
com erros de sintaxe.

## Ficheiro "guiao_de_blocos.md"

Este ficheiro descreve, passo a passo, como montar o programa bloco a
bloco no editor do Scratch — útil tanto para o professor confirmar
visualmente a estrutura do projeto, como para os alunos o
reconstruírem eles próprios como exercício.

## Nota técnica (geração do ficheiro)

O ficheiro `.sb3` foi gerado programaticamente a partir do script
`gerar_sb3.py` (incluído nesta pasta), que escreve diretamente a
estrutura interna que um projeto Scratch usa. Isto permite recriar ou
afinar o exemplo de forma controlada. O resultado foi validado de duas
formas:

1. Verificação estrutural de todas as referências entre blocos
   (nenhum bloco "aponta" para um id inexistente, cada variável e
   lista usada está declarada, etc.);
2. Execução real do projeto através do motor oficial do Scratch
   (`scratch-vm`, usado internamente pelo próprio Scratch), simulando
   uma sessão completa de utilização (adicionar duas tarefas, listar,
   remover uma, listar novamente, sair) e confirmando que todas as
   mensagens esperadas apareceram na ordem certa.
