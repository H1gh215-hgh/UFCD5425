# Makefile — AgendaC
#
# Automatiza a compilação do programa. Em vez de escrever o comando
# gcc completo todas as vezes, basta executar "make" nesta pasta.

CC = gcc
CFLAGS = -Wall -Wextra -std=c11
FONTES = main.c contacto.c tarefa.c ficheiros.c utils.c
EXECUTAVEL = agendac

$(EXECUTAVEL): $(FONTES) contacto.h tarefa.h ficheiros.h utils.h
	$(CC) $(CFLAGS) -o $(EXECUTAVEL) $(FONTES)

.PHONY: limpar executar
limpar:
	rm -f $(EXECUTAVEL) dados/*.dat

executar: $(EXECUTAVEL)
	./$(EXECUTAVEL)
