## dblink_open

dblink_open — abre um cursor em um banco de dados remoto

## Sinopse

```
dblink_open(text cursorname, text sql [, bool fail_on_error]) returns text
dblink_open(text connname, text cursorname, text sql [, bool fail_on_error]) returns text
```

## Descrição

`dblink_open()` abre um cursor em um banco de dados remoto. O cursor pode ser manipulado posteriormente com `dblink_fetch()` e `dblink_close()`.

## Argumentos

*`connname`*: Nome da conexão a ser usada; omita este parâmetro para usar a conexão sem nome.

*`cursorname`*: O nome a ser atribuído a este cursor.

*`sql`*: A declaração `SELECT` que você deseja executar no banco de dados remoto, por exemplo `select * from pg_class`.

*`fail_on_error`*: Se verdadeiro (o padrão quando omitido), um erro lançado no lado remoto da conexão causa um erro também a ser lançado localmente. Se falso, o erro remoto é relatado localmente como um NOTÍCIE, e o valor de retorno da função é definido como `ERROR`.

## Valor de retorno

Retorna o status, que pode ser `OK` ou `ERROR`.

## Notas

Como um cursor só pode persistir dentro de uma transação, `dblink_open` inicia um bloco de transação explícito (`BEGIN`) no lado remoto, se o lado remoto não estivesse já dentro de uma transação. Essa transação será fechada novamente quando o `dblink_close` correspondente for executado. Note que, se você usar `dblink_exec` para alterar dados entre `dblink_open` e `dblink_close`, e então ocorrer um erro ou você usar `dblink_disconnect` antes de `dblink_close`, sua alteração *será perdida* porque a transação será abortada.

## Exemplos

```
SELECT dblink_connect('dbname=postgres options=-csearch_path=');
 dblink_connect
----------------
 OK
(1 row)

SELECT dblink_open('foo', 'select proname, prosrc from pg_proc');
 dblink_open
-------------
 OK
(1 row)
```
