## dblink_get_connections

dblink_get_connections — retorna os nomes de todas as conexões abertas do dblink

## Sinopse

```
dblink_get_connections() returns text[]
```

## Descrição

`dblink_get_connections` retorna um array com os nomes de todas as conexões nomeadas abertas `dblink`.

## Valor de retorno

Retorna um array de texto com os nomes das conexões, ou NULL se nenhum.

## Exemplos

```
SELECT dblink_get_connections();
```
