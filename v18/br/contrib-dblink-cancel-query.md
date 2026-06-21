## dblink_cancel_query

dblink_cancel_query — cancela qualquer consulta ativa na conexão designada

## Sinopse

```
dblink_cancel_query(text connname) returns text
```

## Descrição

`dblink_cancel_query` tenta cancelar qualquer consulta em andamento na conexão nomeada. Note que isso não é certo de ser bem-sucedido (já que, por exemplo, a consulta remota pode já ter terminado). Um pedido de cancelamento simplesmente melhora as chances de a consulta falhar em breve. Você ainda deve completar o protocolo de consulta normal, por exemplo, chamando `dblink_get_result`.

## Argumentos

*`connname`*: Nome da conexão a ser utilizada.

## Valor de retorno

Retorna `OK` se o pedido de cancelamento tiver sido enviado, ou o texto de uma mensagem de erro em caso de falha.

## Exemplos

```
SELECT dblink_cancel_query('dtest1');
```
