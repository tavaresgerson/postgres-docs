## dblink_fetch

dblink_fetch — retorna linhas de um cursor aberto em um banco de dados remoto

## Sinopse

```
dblink_fetch(text cursorname, int howmany [, bool fail_on_error]) returns setof record
dblink_fetch(text connname, text cursorname, int howmany [, bool fail_on_error]) returns setof record
```

## Descrição

`dblink_fetch` recupera linhas de um cursor previamente estabelecido por `dblink_open`.

## Argumentos

*`connname`*: Nome da conexão a ser usada; omita este parâmetro para usar a conexão sem nome.

*`cursorname`*: O nome do cursor a ser recuperado.

*`howmany`*: O número máximo de linhas a serem recuperadas. As próximas *`howmany`* linhas são obtidas, partindo da posição atual do cursor, avançando. Uma vez que o cursor tenha alcançado seu fim, mais nenhuma linha é produzida.

*`fail_on_error`*: Se verdadeiro (o padrão quando omitido), um erro lançado no lado remoto da conexão causa um erro também a ser lançado localmente. Se falso, o erro remoto é relatado localmente como um NOTÍCIE, e a função retorna nenhuma linha.

## Valor de retorno

A função retorna a(s) linha(s) obtida(s) do cursor. Para usar essa função, você precisará especificar o conjunto esperado de colunas, como discutido anteriormente para `dblink`.

## Notas

Se houver uma incompatibilidade entre o número de colunas de retorno especificadas na cláusula `FROM`, e o número real de colunas retornadas pelo cursor remoto, um erro será lançado. Nesse caso, o cursor remoto ainda avança tantas linhas quanto teria sido se o erro não tivesse ocorrido. O mesmo vale para qualquer outro erro que ocorra na consulta local após o `FETCH` remoto ter sido feito.

## Exemplos

```
SELECT dblink_connect('dbname=postgres options=-csearch_path=');
 dblink_connect
----------------
 OK
(1 row)

SELECT dblink_open('foo', 'select proname, prosrc from pg_proc where proname like ''bytea%''');
 dblink_open
-------------
 OK
(1 row)

SELECT * FROM dblink_fetch('foo', 5) AS (funcname name, source text);
 funcname |  source
----------+----------
 byteacat | byteacat
 byteacmp | byteacmp
 byteaeq  | byteaeq
 byteage  | byteage
 byteagt  | byteagt
(5 rows)

SELECT * FROM dblink_fetch('foo', 5) AS (funcname name, source text);
 funcname  |  source
-----------+-----------
 byteain   | byteain
 byteale   | byteale
 bytealike | bytealike
 bytealt   | bytealt
 byteane   | byteane
(5 rows)

SELECT * FROM dblink_fetch('foo', 5) AS (funcname name, source text);
  funcname  |   source
------------+------------
 byteanlike | byteanlike
 byteaout   | byteaout
(2 rows)

SELECT * FROM dblink_fetch('foo', 5) AS (funcname name, source text);
 funcname | source
----------+--------
(0 rows)
```
