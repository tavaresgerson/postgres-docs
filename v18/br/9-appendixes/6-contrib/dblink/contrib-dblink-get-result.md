## dblink_get_result

dblink_get_result — obtém um resultado de consulta assíncrona

## Sinopse

```
dblink_get_result(text connname [, bool fail_on_error]) returns setof record
```

## Descrição

`dblink_get_result` coleta os resultados de uma consulta assíncrona enviada anteriormente com `dblink_send_query`. Se a consulta ainda não estiver concluída, `dblink_get_result` aguardará até que ela esteja.

## Argumentos

*`connname`*: Nome da conexão a ser utilizada.

*`fail_on_error`*: Se verdadeiro (o padrão quando omitido), um erro lançado no lado remoto da conexão causa um erro também a ser lançado localmente. Se falso, o erro remoto é relatado localmente como um NOTÍCIE, e a função retorna nenhuma linha.

## Valor de retorno

Para uma consulta assíncrona (ou seja, uma declaração SQL que retorna linhas), a função retorna a(s) linha(s) produzida(s) pela consulta. Para usar essa função, você precisará especificar o conjunto esperado de colunas, como discutido anteriormente para `dblink`.

Para um comando assíncrono (ou seja, uma instrução SQL que não retorna linhas), a função retorna uma única linha com uma única coluna de texto que contém a string de status do comando. Ainda é necessário especificar que o resultado terá uma única coluna de texto na cláusula `FROM` que faz a chamada.

## Notas

Essa função *deve* ser chamada se `dblink_send_query` retornou 1. Deve ser chamada uma vez para cada consulta enviada e uma vez adicionalmente para obter um resultado de conjunto vazio, antes que a conexão possa ser usada novamente.

Ao usar `dblink_send_query` e `dblink_get_result`, o dblink obtém o resultado completo da consulta remota antes de retornar qualquer parte dele para o processador de consulta local. Se a consulta retornar um grande número de linhas, isso pode resultar em inchaço de memória transitório na sessão local. Pode ser melhor abrir tal consulta como um cursor com `dblink_open` e, em seguida, obter um número gerenciável de linhas de cada vez. Alternativamente, use o simples `dblink()`, que evita o inchaço de memória ao enviar grandes conjuntos de resultados para o disco.

## Exemplos

```
contrib_regression=# SELECT dblink_connect('dtest1', 'dbname=contrib_regression');
 dblink_connect
----------------
 OK
(1 row)

contrib_regression=# SELECT * FROM
contrib_regression-# dblink_send_query('dtest1', 'select * from foo where f1 < 3') AS t1;
 t1
----
  1
(1 row)

contrib_regression=# SELECT * FROM dblink_get_result('dtest1') AS t1(f1 int, f2 text, f3 text[]);
 f1 | f2 |     f3
----+----+------------
  0 | a  | {a0,b0,c0}
  1 | b  | {a1,b1,c1}
  2 | c  | {a2,b2,c2}
(3 rows)

contrib_regression=# SELECT * FROM dblink_get_result('dtest1') AS t1(f1 int, f2 text, f3 text[]);
 f1 | f2 | f3
----+----+----
(0 rows)

contrib_regression=# SELECT * FROM
contrib_regression-# dblink_send_query('dtest1', 'select * from foo where f1 < 3; select * from foo where f1 > 6') AS t1;
 t1
----
  1
(1 row)

contrib_regression=# SELECT * FROM dblink_get_result('dtest1') AS t1(f1 int, f2 text, f3 text[]);
 f1 | f2 |     f3
----+----+------------
  0 | a  | {a0,b0,c0}
  1 | b  | {a1,b1,c1}
  2 | c  | {a2,b2,c2}
(3 rows)

contrib_regression=# SELECT * FROM dblink_get_result('dtest1') AS t1(f1 int, f2 text, f3 text[]);
 f1 | f2 |      f3
----+----+---------------
  7 | h  | {a7,b7,c7}
  8 | i  | {a8,b8,c8}
  9 | j  | {a9,b9,c9}
 10 | k  | {a10,b10,c10}
(4 rows)

contrib_regression=# SELECT * FROM dblink_get_result('dtest1') AS t1(f1 int, f2 text, f3 text[]);
 f1 | f2 | f3
----+----+----
(0 rows)
```
