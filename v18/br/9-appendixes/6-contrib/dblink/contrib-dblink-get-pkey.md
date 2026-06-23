## dblink_get_pkey

dblink_get_pkey — retorna as posições e os nomes dos campos da chave primária de uma relação

## Sinopse

```
dblink_get_pkey(text relname) returns setof dblink_pkey_results
```

## Descrição

`dblink_get_pkey` fornece informações sobre a chave primária de uma relação no banco de dados local. Isso às vezes é útil na geração de consultas que serão enviadas para bancos de dados remotos.

## Argumentos

*`relname`*: Nome de uma relação local, por exemplo `foo` ou `myschema.mytab`. Inclua aspas duplas se o nome for composto por maiúsculas e minúsculas ou contiver caracteres especiais, por exemplo `"FooBar"`; sem aspas, a string será convertida para minúsculas.

## Valor de retorno

Retorna uma linha para cada campo da chave primária, ou nenhuma linha se a relação não tiver chave primária. O tipo de linha de resultado é definido como

```
CREATE TYPE dblink_pkey_results AS (position int, colname text);
```

A coluna `position` simplesmente vai de 1 até *`N`*; é o número do campo dentro da chave primária, não o número dentro das colunas da tabela.

## Exemplos

```
CREATE TABLE foobar (
    f1 int,
    f2 int,
    f3 int,
    PRIMARY KEY (f1, f2, f3)
);
CREATE TABLE

SELECT * FROM dblink_get_pkey('foobar');
 position | colname
----------+---------
        1 | f1
        2 | f2
        3 | f3
(3 rows)
```
