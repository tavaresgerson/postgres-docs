## dblink_connect

dblink_connect — abre uma conexão persistente a um banco de dados remoto

## Sinopse

```
dblink_connect(text connstr) returns text
dblink_connect(text connname, text connstr) returns text
```

## Descrição

`dblink_connect()` estabelece uma conexão com um banco de dados PostgreSQL remoto. O servidor e o banco de dados a serem contatados são identificados por meio de uma string de conexão padrão libpq. Opcionalmente, um nome pode ser atribuído à conexão. Múltiplas conexões com nome podem ser abertas ao mesmo tempo, mas apenas uma conexão sem nome é permitida de cada vez. A conexão persistirá até ser fechada ou até que a sessão do banco de dados seja encerrada.

A cadeia de conexão também pode ser o nome de um servidor externo existente. Recomenda-se o uso do wrapper de dados externos `dblink_fdw` ao definir o servidor externo. Veja o exemplo abaixo, bem como [CREATE SERVER](sql-createserver.md "CREATE SERVER") e [CREATE USER MAPPING](sql-createusermapping.md "CREATE USER MAPPING").

## Argumentos

*`connname`*: O nome a ser usado para essa conexão; se omitido, uma conexão sem nome é aberta, substituindo qualquer conexão sem nome existente.

*`connstr`*: string de informações de conexão estilo libpq, por exemplo `hostaddr=127.0.0.1 port=5432 dbname=mydb user=postgres password=mypasswd options=-csearch_path=`. Para detalhes, consulte [Seção 32.1.1][(libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings")]. Alternativamente, o nome de um servidor externo.

## Valor de retorno

Retorna o status, que é sempre `OK` (já que qualquer erro faz com que a função lance um erro em vez de retornar).

## Notas

Se usuários não confiáveis tiverem acesso a um banco de dados que não adotou um padrão de uso de esquema seguro (ddl-schemas.md#DDL-SCHEMAS-PATTERNS "5.10.6. Usage Patterns"), comece cada sessão removendo esquemas que podem ser escritos publicamente de `search_path`. Por exemplo, pode-se adicionar `options=-csearch_path=` a *`connstr`*. Esta consideração não é específica de `dblink`; ela se aplica a todas as interfaces para executar comandos SQL arbitrários.

O wrapper de dados estrangeiros `dblink_fdw` tem uma opção booleana adicional `use_scram_passthrough` que controla se o `dblink` usará a autenticação de passagem SCRAM para se conectar ao banco de dados remoto. Com a autenticação de passagem SCRAM, o `dblink` usa segredos criptografados SCRAM em vez de senhas de usuário em texto plano para se conectar ao servidor remoto. Isso evita o armazenamento de senhas de usuário em texto plano nos catálogos do sistema PostgreSQL. Consulte a documentação da opção equivalente `use_scram_passthrough` do postgres_fdw para obter mais detalhes e restrições.

Apenas superusuários podem usar `dblink_connect` para criar conexões que não utilizem autenticação por senha, passagem SCRAM ou autenticação GSSAPI. Se os não superusuários precisam dessa capacidade, use `dblink_connect_u` em vez disso.

Não é prudente escolher nomes de conexão que contenham sinais iguais, pois isso expõe o risco de confusão com as strings de informações de conexão em outras funções do `dblink`.

## Exemplos

```
SELECT dblink_connect('dbname=postgres options=-csearch_path=');
 dblink_connect
----------------
 OK
(1 row)

SELECT dblink_connect('myconn', 'dbname=postgres options=-csearch_path=');
 dblink_connect
----------------
 OK
(1 row)

-- FOREIGN DATA WRAPPER functionality
-- Note: local connections that don't use SCRAM pass-through require password
--       authentication for this to work properly. Otherwise, you will receive
--       the following error from dblink_connect():
--       ERROR:  password is required
--       DETAIL:  Non-superuser cannot connect if the server does not request a password.
--       HINT:  Target server's authentication method must be changed.

CREATE SERVER fdtest FOREIGN DATA WRAPPER dblink_fdw OPTIONS (hostaddr '127.0.0.1', dbname 'contrib_regression');

CREATE USER regress_dblink_user WITH PASSWORD 'secret';
CREATE USER MAPPING FOR regress_dblink_user SERVER fdtest OPTIONS (user 'regress_dblink_user', password 'secret');
GRANT USAGE ON FOREIGN SERVER fdtest TO regress_dblink_user;
GRANT SELECT ON TABLE foo TO regress_dblink_user;

\set ORIGINAL_USER :USER
\c - regress_dblink_user
SELECT dblink_connect('myconn', 'fdtest');
 dblink_connect
----------------
 OK
(1 row)

SELECT * FROM dblink('myconn', 'SELECT * FROM foo') AS t(a int, b text, c text[]);
 a  | b |       c
----+---+---------------
  0 | a | {a0,b0,c0}
  1 | b | {a1,b1,c1}
  2 | c | {a2,b2,c2}
  3 | d | {a3,b3,c3}
  4 | e | {a4,b4,c4}
  5 | f | {a5,b5,c5}
  6 | g | {a6,b6,c6}
  7 | h | {a7,b7,c7}
  8 | i | {a8,b8,c8}
  9 | j | {a9,b9,c9}
 10 | k | {a10,b10,c10}
(11 rows)

\c - :ORIGINAL_USER
REVOKE USAGE ON FOREIGN SERVER fdtest FROM regress_dblink_user;
REVOKE SELECT ON TABLE foo FROM regress_dblink_user;
DROP USER MAPPING FOR regress_dblink_user SERVER fdtest;
DROP USER regress_dblink_user;
DROP SERVER fdtest;
```
