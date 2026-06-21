## MOSTRA

SHOW — mostre o valor de um parâmetro de tempo de execução

## Sinopse

```
SHOW name
SHOW ALL
```

## Descrição

`SHOW` exibirá a configuração atual dos parâmetros de execução. Essas variáveis podem ser definidas usando a declaração `SET`, editando o arquivo de configuração `postgresql.conf`, através da variável ambiental `PGOPTIONS` (quando se usa o libpq ou uma aplicação baseada no libpq), ou através de flags de linha de comando ao iniciar o servidor `postgres`. Veja [Capítulo 19](runtime-config.md "Chapter 19. Server Configuration") para detalhes.

## Parâmetros

*`name`*: O nome de um parâmetro de tempo de execução. Os parâmetros disponíveis estão documentados no [Capítulo 19](runtime-config.md "Chapter 19. Server Configuration") e na página de referência [SET](sql-set.md "SET"). Além disso, há alguns parâmetros que podem ser exibidos, mas não definidos:

`SERVER_VERSION` : Mostra o número de versão do servidor.

`SERVER_ENCODING` :   Mostra o codificação de caracteres do lado do servidor. Atualmente, este parâmetro pode ser mostrado, mas não definido, porque a codificação é determinada no momento da criação do banco de dados.

`IS_SUPERUSER` :   Verdadeiro se o papel atual tiver privilégios de superusuário.

`ALL`: Mostre os valores de todos os parâmetros de configuração, com descrições.

## Notas

A função `current_setting` produz uma saída equivalente; veja [Seção 9.28.1](functions-admin.md#FUNCTIONS-ADMIN-SET "9.28.1. Configuration Settings Functions"). Além disso, a visão do sistema `pg_settings`(view-pg-settings.md "53.25. pg_settings") também produz as mesmas informações.

## Exemplos

Mostre a configuração atual do parâmetro `DateStyle`:

```
SHOW DateStyle;
 DateStyle
-----------
 ISO, MDY
(1 row)
```

Mostre a configuração atual do parâmetro `geqo`:

```
SHOW geqo;
 geqo
------
 on
(1 row)
```

Mostrar todas as configurações:

```
SHOW ALL;
            name         | setting |                description
-------------------------+---------+-------------------------------------------------
 allow_system_table_mods | off     | Allows modifications of the structure of ...
    .
    .
    .
 xmloption               | content | Sets whether XML data in implicit parsing ...
 zero_damaged_pages      | off     | Continues processing past damaged page headers.
(196 rows)
```

## Compatibilidade

O comando `SHOW` é uma extensão do PostgreSQL.

## Veja também

[SET](sql-set.md "SET"), [RESET](sql-reset.md "RESET")