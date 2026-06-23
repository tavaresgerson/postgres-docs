## CONECTAR-SE

CONFIGURAR CONEXÃO — selecione uma conexão de banco de dados

## Sinopse

```
SET CONNECTION [ TO | = ] connection_name
```

## Descrição

`SET CONNECTION` define a conexão de banco de dados "corrente", que é a que todos os comandos usam, a menos que seja sobrescrita.

## Parâmetros

*`connection_name`* [#](#ECPG-SQL-SET-CONNECTION-CONNECTION-NAME): Um nome de conexão de banco de dados estabelecido pelo comando `CONNECT`.

`CURRENT` [#](#ECPG-SQL-SET-CONNECTION-CURRENT): Defina a conexão com a conexão atual (assim, nada acontece).

## Exemplos

```
EXEC SQL SET CONNECTION TO con2;
EXEC SQL SET CONNECTION = con1;
```

## Compatibilidade

`SET CONNECTION` é especificado no padrão SQL.

## Veja também

[CONECTAR](ecpg-sql-connect.md "CONNECT"), [DESCONECTAR](ecpg-sql-disconnect.md "DISCONNECT")