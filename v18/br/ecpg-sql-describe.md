## DESCRIÇÃO

DESCRIBE — obter informações sobre um conjunto de declaração ou resultado preparado

## Sinopse

```
DESCRIBE [ OUTPUT ] prepared_name USING [ SQL ] DESCRIPTOR descriptor_name
DESCRIBE [ OUTPUT ] prepared_name INTO [ SQL ] DESCRIPTOR descriptor_name
DESCRIBE [ OUTPUT ] prepared_name INTO sqlda_name
```

## Descrição

`DESCRIBE` recupera informações de metadados sobre as colunas de resultado contidas em uma declaração preparada, sem, na verdade, obter uma linha.

## Parâmetros

*`prepared_name`* [#](#ECPG-SQL-DESCRIBE-PREPARED-NAME): O nome de uma declaração preparada. Isso pode ser um identificador SQL ou uma variável de host.

*`descriptor_name`* [#](#ECPG-SQL-DESCRIBE-DESCRIPTOR-NAME): Um nome de descritor. É sensível a maiúsculas e minúsculas. Pode ser um identificador SQL ou uma variável de host.

*`sqlda_name`* [#](#ECPG-SQL-DESCRIBE-SQLDA-NAME): O nome de uma variável SQLDA.

## Exemplos

```
EXEC SQL ALLOCATE DESCRIPTOR mydesc;
EXEC SQL PREPARE stmt1 FROM :sql_stmt;
EXEC SQL DESCRIBE stmt1 INTO SQL DESCRIPTOR mydesc;
EXEC SQL GET DESCRIPTOR mydesc VALUE 1 :charvar = NAME;
EXEC SQL DEALLOCATE DESCRIPTOR mydesc;
```

## Compatibilidade

`DESCRIBE` é especificado no padrão SQL.

## Veja também

[ATTRIBUAR DESCRIÇÃO][(ecpg-sql-allocate-descriptor.md "ALLOCATE DESCRIPTOR"), [OBTER DESCRIÇÃO][(ecpg-sql-get-descriptor.md "GET DESCRIPTOR")