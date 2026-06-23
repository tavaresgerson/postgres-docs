## dblink_send_query

dblink_send_query — envia uma consulta assíncrona a um banco de dados remoto

## Sinopse

```
dblink_send_query(text connname, text sql) returns int
```

## Descrição

`dblink_send_query` envia uma consulta para ser executada de forma assíncrona, ou seja, sem esperar imediatamente pelo resultado. Não deve haver uma consulta assíncrona em andamento na conexão.

Após enviar com sucesso uma consulta assíncrona, o status de conclusão pode ser verificado com `dblink_is_busy`, e os resultados são coletados com `dblink_get_result`. Também é possível tentar cancelar uma consulta assíncrona ativa usando `dblink_cancel_query`.

## Argumentos

*`connname`*: Nome da conexão a ser utilizada.

*`sql`*: A declaração SQL que você deseja executar no banco de dados remoto, por exemplo `select * from pg_class`.

## Valor de retorno

Retorna 1 se a consulta foi enviada com sucesso, caso contrário, retorna 0.

## Exemplos

```
SELECT dblink_send_query('dtest1', 'SELECT * FROM foo WHERE f1 < 3');
```
