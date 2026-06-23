## DEALLOCATE DESCRIPTOR

DEALLOCATE DESCRIPTOR — desalojar uma área de descritor SQL

## Sinopse

```
DEALLOCATE DESCRIPTOR name
```

## Descrição

`DEALLOCATE DESCRIPTOR` desaloja uma área de descritor SQL nomeada.

## Parâmetros

*`name`* [#](#ECPG-SQL-DEALLOCATE-DESCRIPTOR-NAME): O nome do descritor que será desalocado. É sensível a maiúsculas e minúsculas. Isso pode ser um identificador SQL ou uma variável de host.

## Exemplos

```
EXEC SQL DEALLOCATE DESCRIPTOR mydesc;
```

## Compatibilidade

`DEALLOCATE DESCRIPTOR` é especificado no padrão SQL.

## Veja também

(ecpg-sql-allocate-descriptor.md "ALLOCATE DESCRIPTOR"), (ecpg-sql-get-descriptor.md "GET DESCRIPTOR"), (ecpg-sql-set-descriptor.md "SET DESCRIPTOR")