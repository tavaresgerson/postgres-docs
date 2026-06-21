## dblink_close

dblink_close — fecha um cursor em um banco de dados remoto

## Sinopse

```
dblink_close(text cursorname [, bool fail_on_error]) returns text
dblink_close(text connname, text cursorname [, bool fail_on_error]) returns text
```

## Descrição

`dblink_close` fecha um cursor que foi aberto anteriormente com `dblink_open`.

## Argumentos

*`connname`*: Nome da conexão a ser usada; omita este parâmetro para usar a conexão sem nome.

*`cursorname`*: O nome do cursor a ser fechado.

*`fail_on_error`*: Se verdadeiro (o padrão quando omitido), então um erro lançado no lado remoto da conexão causa um erro também a ser lançado localmente. Se falso, o erro remoto é relatado localmente como um NOTÍCIE, e o valor de retorno da função é definido como `ERROR`.

## Valor de retorno

Retorna o status, seja `OK` ou `ERROR`.

## Notas

Se o `dblink_open` iniciou um bloco de transação explícito, e este é o último cursor aberto restante nesta conexão, o `dblink_close` emitirá o correspondente `COMMIT`.

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

SELECT dblink_close('foo');
 dblink_close
--------------
 OK
(1 row)
```
