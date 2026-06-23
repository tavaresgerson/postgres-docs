## dblink_build_sql_insert

dblink_build_sql_insert — constrói uma declaração INSERT usando um par ordenado local, substituindo os valores do campo chave primária pelos valores alternativos fornecidos

## Sinopse

```
dblink_build_sql_insert(text relname,
                        int2vector primary_key_attnums,
                        integer num_primary_key_atts,
                        text[] src_pk_att_vals_array,
                        text[] tgt_pk_att_vals_array) returns text
```

## Descrição

`dblink_build_sql_insert` pode ser útil para fazer uma replicação seletiva de uma tabela local para um banco de dados remoto. Ele seleciona uma linha da tabela local com base na chave primária e, em seguida, constrói um comando SQL `INSERT` que duplicará essa linha, mas com os valores da chave primária substituídos pelos valores do último argumento. (Para fazer uma cópia exata da linha, basta especificar os mesmos valores para os dois últimos argumentos.)

## Argumentos

*`relname`*: Nome de uma relação local, por exemplo `foo` ou `myschema.mytab`. Inclua aspas duplas se o nome for composto por maiúsculas e minúsculas ou contiver caracteres especiais, por exemplo `"FooBar"`; sem aspas, a string será convertida para minúsculas.

*`primary_key_attnums`*: Números de atributos (de 1 em 1) dos campos da chave primária, por exemplo `1 2`.

*`num_primary_key_atts`*: Número de campos de chave primária.

*`src_pk_att_vals_array`*: Valores dos campos da chave primária a serem usados para procurar a tupla local. Cada campo é representado em forma de texto. Um erro é lançado se não houver uma linha local com esses valores da chave primária.

*`tgt_pk_att_vals_array`*: Valores dos campos da chave primária a serem colocados no comando resultante do `INSERT`. Cada campo é representado em forma de texto.

## Valor de retorno

Retorna a declaração SQL solicitada como texto.

## Notas

A partir do PostgreSQL 9.0, os números dos atributos em *`primary_key_attnums`* são interpretados como números de coluna lógicos, correspondendo à posição da coluna no `SELECT * FROM relname`. As versões anteriores interpretavam os números como posições físicas das colunas. Há uma diferença, se houver, se alguma ou algumas colunas à esquerda da coluna indicada foram excluídas durante a vida útil da tabela.

## Exemplos

```
SELECT dblink_build_sql_insert('foo', '1 2', 2, '{"1", "a"}', '{"1", "b''a"}');
             dblink_build_sql_insert
--------------------------------------------------
 INSERT INTO foo(f1,f2,f3) VALUES('1','b''a','1')
(1 row)
```
