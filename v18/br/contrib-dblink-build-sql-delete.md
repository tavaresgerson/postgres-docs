## dblink_build_sql_delete

dblink_build_sql_delete — constrói uma declaração DELETE usando os valores fornecidos para os campos da chave primária

## Sinopse

```
dblink_build_sql_delete(text relname,
                        int2vector primary_key_attnums,
                        integer num_primary_key_atts,
                        text[] tgt_pk_att_vals_array) returns text
```

## Descrição

`dblink_build_sql_delete` pode ser útil para fazer uma replicação seletiva de uma tabela local para um banco de dados remoto. Ele constrói um comando SQL `DELETE` que excluirá a linha com os valores da chave primária fornecidos.

## Argumentos

*`relname`*: Nome de uma relação local, por exemplo `foo` ou `myschema.mytab`. Inclua aspas duplas se o nome for composto por maiúsculas e minúsculas ou contiver caracteres especiais, por exemplo `"FooBar"`; sem aspas, a string será convertida para minúsculas.

*`primary_key_attnums`*: Números de atributos (de 1 em 1) dos campos da chave primária, por exemplo `1 2`.

*`num_primary_key_atts`*: Número de campos de chave primária.

*`tgt_pk_att_vals_array`*: Valores dos campos da chave primária a serem utilizados no comando resultante do `DELETE`. Cada campo é representado em forma de texto.

## Valor de retorno

Retorna a declaração SQL solicitada como texto.

## Notas

A partir do PostgreSQL 9.0, os números dos atributos em *`primary_key_attnums`* são interpretados como números de coluna lógicos, correspondendo à posição da coluna em `SELECT * FROM relname`. As versões anteriores interpretavam os números como posições físicas das colunas. Há uma diferença, se houver, se alguma ou algumas colunas à esquerda da coluna indicada foram excluídas durante a vida útil da tabela.

## Exemplos

```
SELECT dblink_build_sql_delete('"MyFoo"', '1 2', 2, '{"1", "b"}');
           dblink_build_sql_delete
---------------------------------------------
 DELETE FROM "MyFoo" WHERE f1='1' AND f2='b'
(1 row)
```
