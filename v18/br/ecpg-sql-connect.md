## CONECTAR

CONECTAR — estabelecer uma conexão de banco de dados

## Sinopse

```
CONNECT TO connection_target [ AS connection_name ] [ USER connection_user ]
CONNECT TO DEFAULT
CONNECT connection_user
DATABASE connection_target
```

## Descrição

O comando `CONNECT` estabelece uma conexão entre o cliente e o servidor PostgreSQL.

## Parâmetros

*`connection_target`* [#](#ECPG-SQL-CONNECT-CONNECTION-TARGET): *`connection_target`* especifica o servidor alvo da conexão em uma das várias formas.

[ *`database_name`* ] [ `@`*`host`* ] [ `:`*`port`* ] [#](#ECPG-SQL-CONNECT-CONNECTION-TARGET-DATABASE-NAME) :   Conecte-se via TCP/IP

`unix:postgresql://`*`host`* [ `:`*`port`* ] `/` [ *`database_name`* ] [ `?`*`connection_option`* ] [#](#ECPG-SQL-CONNECT-CONNECTION-TARGET-UNIX-DOMAIN-SOCKETS) :   Conecte-se através de sockets de domínio Unix

`tcp:postgresql://`*`host`* [ `:`*`port`* ] `/` [ *`database_name`* ] [ `?`*`connection_option`* ] [#](#ECPG-SQL-CONNECT-CONNECTION-TARGET-TCP-IP) :   Conecte-se via TCP/IP

Constantes de cadeia de SQL [#](#ECPG-SQL-CONNECT-CONNECTION-TARGET-CONSTANT) :   contendo um valor em uma das formas acima

variável host [#](#ECPG-SQL-CONNECT-CONNECTION-TARGET-HOST-VARIABLE) :   variável host do tipo `char[]` ou `VARCHAR[]` contendo um valor em uma das formas acima

*`connection_name`* [#](#ECPG-SQL-CONNECT-CONNECTION-NAME): Um identificador opcional para a conexão, para que possa ser referido em outros comandos. Isso pode ser um identificador SQL ou uma variável de host.

*`connection_user`* [#](#ECPG-SQL-CONNECT-CONNECTION-USER): O nome do usuário para a conexão do banco de dados.

Este parâmetro também pode especificar o nome do usuário e a senha, usando um dos formulários `user_name/password`, `user_name IDENTIFIED BY password` ou `user_name USING password`.

O nome do usuário e a senha podem ser identificadores SQL, constantes de cadeia ou variáveis de host.

`DEFAULT` [#](#ECPG-SQL-CONNECT-DEFAULT): Use todos os parâmetros de conexão padrão, conforme definido pelo libpq.

## Exemplos

Aqui, há várias variantes para especificar os parâmetros de conexão:

```
EXEC SQL CONNECT TO "connectdb" AS main;
EXEC SQL CONNECT TO "connectdb" AS second;
EXEC SQL CONNECT TO "unix:postgresql://200.46.204.71/connectdb" AS main USER connectuser;
EXEC SQL CONNECT TO "unix:postgresql://localhost/connectdb" AS main USER connectuser;
EXEC SQL CONNECT TO 'connectdb' AS main;
EXEC SQL CONNECT TO 'unix:postgresql://localhost/connectdb' AS main USER :user;
EXEC SQL CONNECT TO :db AS :id;
EXEC SQL CONNECT TO :db USER connectuser USING :pw;
EXEC SQL CONNECT TO @localhost AS main USER connectdb;
EXEC SQL CONNECT TO REGRESSDB1 as main;
EXEC SQL CONNECT TO AS main USER connectdb;
EXEC SQL CONNECT TO connectdb AS :id;
EXEC SQL CONNECT TO connectdb AS main USER connectuser/connectdb;
EXEC SQL CONNECT TO connectdb AS main;
EXEC SQL CONNECT TO connectdb@localhost AS main;
EXEC SQL CONNECT TO tcp:postgresql://localhost/ USER connectdb;
EXEC SQL CONNECT TO tcp:postgresql://localhost/connectdb USER connectuser IDENTIFIED BY connectpw;
EXEC SQL CONNECT TO tcp:postgresql://localhost:20/connectdb USER connectuser IDENTIFIED BY connectpw;
EXEC SQL CONNECT TO unix:postgresql://localhost/ AS main USER connectdb;
EXEC SQL CONNECT TO unix:postgresql://localhost/connectdb AS main USER connectuser;
EXEC SQL CONNECT TO unix:postgresql://localhost/connectdb USER connectuser IDENTIFIED BY "connectpw";
EXEC SQL CONNECT TO unix:postgresql://localhost/connectdb USER connectuser USING "connectpw";
EXEC SQL CONNECT TO unix:postgresql://localhost/connectdb?connect_timeout=14 USER connectuser;
```

Aqui está um exemplo de programa que ilustra o uso de variáveis hostis para especificar parâmetros de conexão:

```
int
main(void)
{
EXEC SQL BEGIN DECLARE SECTION;
    char *dbname     = "testdb";    /* database name */
    char *user       = "testuser";  /* connection user name */
    char *connection = "tcp:postgresql://localhost:5432/testdb";
                                    /* connection string */
    char ver[256];                  /* buffer to store the version string */
EXEC SQL END DECLARE SECTION;

    ECPGdebug(1, stderr);

    EXEC SQL CONNECT TO :dbname USER :user;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL SELECT version() INTO :ver;
    EXEC SQL DISCONNECT;

    printf("version: %s\n", ver);

    EXEC SQL CONNECT TO :connection USER :user;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL SELECT version() INTO :ver;
    EXEC SQL DISCONNECT;

    printf("version: %s\n", ver);

    return 0;
}
```

## Compatibilidade

`CONNECT` é especificado no padrão SQL, mas o formato dos parâmetros de conexão é específico da implementação.

## Veja também

[DESCONECTAR](ecpg-sql-disconnect.md "DISCONNECT"), [ESTABELECER CONEXÃO](ecpg-sql-set-connection.md "SET CONNECTION")