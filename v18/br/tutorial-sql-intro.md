## 2.1. Introdução [#](#TUTORIAL-SQL-INTRO)

Este capítulo fornece uma visão geral de como usar o SQL para realizar operações simples. Este tutorial destina-se apenas a fornecer uma introdução e não é de forma alguma um tutorial completo sobre SQL. Vários livros foram escritos sobre SQL, incluindo [[melt93]](biblio.md#MELT93 "Understanding the New SQL") e [[date97]](biblio.md#DATE97 "A Guide to the SQL Standard"). Você deve estar ciente de que algumas características da linguagem do PostgreSQL são extensões do padrão.

Nos exemplos que se seguem, assumimos que você criou um banco de dados chamado `mydb`, conforme descrito no capítulo anterior, e conseguiu iniciar o psql.

Exemplos neste manual também podem ser encontrados na distribuição de fonte do PostgreSQL no diretório `src/tutorial/`. (Distribuições binárias do PostgreSQL podem não fornecer esses arquivos. Para usar esses arquivos, primeiro mude para esse diretório e execute o comando make:

```
$ cd .../src/tutorial
$ make
```

Isso cria os scripts e compila os arquivos C que contêm funções e tipos definidos pelo usuário. Em seguida, para iniciar o tutorial, faça o seguinte:

```
$ psql -s mydb

...

mydb=> \i basics.sql
```

O comando `\i` lê comandos do arquivo especificado. A opção `psql` de `-s` coloca o modo de único passo, que pausa antes de enviar cada declaração ao servidor. Os comandos usados nesta seção estão no arquivo `basics.sql`.