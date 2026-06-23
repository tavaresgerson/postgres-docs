## DISCONNECT

DISCONNECT — encerrar uma conexão de banco de dados

## Sinopse

```
DISCONNECT connection_name
DISCONNECT [ CURRENT ]
DISCONNECT ALL
```

## Descrição

`DISCONNECT` fecha uma conexão (ou todas as conexões) ao banco de dados.

## Parâmetros

*`connection_name`* [#](#ECPG-SQL-DISCONNECT-CONNECTION-NAME): Um nome de conexão de banco de dados estabelecido pelo comando `CONNECT`.

`CURRENT` [#](#ECPG-SQL-DISCONNECT-CURRENT): Feche a conexão “corrente”, que é a conexão mais recentemente aberta ou a conexão definida pelo comando `SET CONNECTION`. Isso também é o padrão se nenhum argumento for dado ao comando `DISCONNECT`.

`ALL` [#](#ECPG-SQL-DISCONNECT-ALL): Feche todas as conexões abertas.

## Exemplos

```
int
main(void)
{
    EXEC SQL CONNECT TO testdb AS con1 USER testuser;
    EXEC SQL CONNECT TO testdb AS con2 USER testuser;
    EXEC SQL CONNECT TO testdb AS con3 USER testuser;

    EXEC SQL DISCONNECT CURRENT;  /* close con3          */
    EXEC SQL DISCONNECT ALL;      /* close con2 and con1 */

    return 0;
}
```

## Compatibilidade

`DISCONNECT` é especificado no padrão SQL.

## Veja também

[CONECTAR](ecpg-sql-connect.md "CONNECT"), [ESTABELECER CONEXÃO](ecpg-sql-set-connection.md "SET CONNECTION")