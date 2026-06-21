## dblink_disconnect

dblink_disconnect — fecha uma conexão persistente a um banco de dados remoto

## Sinopse

```
dblink_disconnect() returns text
dblink_disconnect(text connname) returns text
```

## Descrição

`dblink_disconnect()` fecha uma conexão que foi aberta anteriormente por `dblink_connect()`. O formulário sem argumentos fecha uma conexão sem nome.

## Argumentos

*`connname`*: O nome de uma conexão nomeada a ser fechada.

## Valor de retorno

Retorna o status, que é sempre `OK` (já que qualquer erro faz com que a função lance um erro em vez de retornar).

## Exemplos

```
SELECT dblink_disconnect();
 dblink_disconnect
-------------------
 OK
(1 row)

SELECT dblink_disconnect('myconn');
 dblink_disconnect
-------------------
 OK
(1 row)
```
