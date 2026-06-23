## dblink_is_busy

dblink_is_busy — verifica se a conexão está ocupada com uma consulta assíncrona

## Sinopse

```
dblink_is_busy(text connname) returns int
```

## Descrição

`dblink_is_busy` testa se uma consulta assíncrona está em andamento.

## Argumentos

*`connname`*: Nome da conexão a ser verificada.

## Valor de retorno

Retorna 1 se a conexão estiver ocupada, 0 se não estiver. Se essa função retornar 0, é garantido que `dblink_get_result` não bloqueará.

## Exemplos

```
SELECT dblink_is_busy('dtest1');
```
