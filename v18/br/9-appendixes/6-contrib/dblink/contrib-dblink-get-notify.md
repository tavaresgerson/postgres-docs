## dblink_get_notify

dblink_get_notify — recuperar notificações assíncronas em uma conexão

## Sinopse

```
dblink_get_notify() returns setof (notify_name text, be_pid int, extra text)
dblink_get_notify(text connname) returns setof (notify_name text, be_pid int, extra text)
```

## Descrição

`dblink_get_notify` recupera notificações na conexão sem nome, ou em uma conexão nomeada, se especificada. Para receber notificações via dblink, `LISTEN` deve ser emitido primeiro, usando `dblink_exec`. Para detalhes, consulte [LISTEN](sql-listen.md "LISTEN") e [NOTIFY](sql-notify.md "NOTIFY").

## Argumentos

*`connname`*: O nome de uma conexão nomeada para receber notificações.

## Valor de retorno

Retorna `setof (notify_name text, be_pid int, extra text)`, ou um conjunto vazio se nenhum.

## Exemplos

```
SELECT dblink_exec('LISTEN virtual');
 dblink_exec
-------------
 LISTEN
(1 row)

SELECT * FROM dblink_get_notify();
 notify_name | be_pid | extra
-------------+--------+-------
(0 rows)

NOTIFY virtual;
NOTIFY

SELECT * FROM dblink_get_notify();
 notify_name | be_pid | extra
-------------+--------+-------
 virtual     |   1229 |
(1 row)
```
