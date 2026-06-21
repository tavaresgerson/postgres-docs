## dblink_exec

dblink_exec — executa um comando em um banco de dados remoto

## Sinopse

```
dblink_exec(text connname, text sql [, bool fail_on_error]) returns text
dblink_exec(text connstr, text sql [, bool fail_on_error]) returns text
dblink_exec(text sql [, bool fail_on_error]) returns text
```

## Descrição

`dblink_exec` executa um comando (ou seja, qualquer declaração SQL que não retorne linhas) em um banco de dados remoto.

Quando são fornecidos dois argumentos `text`, o primeiro é procurado como o nome de uma conexão persistente; se encontrado, o comando é executado nessa conexão. Se não for encontrado, o primeiro argumento é tratado como uma string de informações de conexão, como no caso de `dblink_connect`, e a conexão indicada é feita apenas durante a duração deste comando.

## Argumentos

*`connname`*: Nome da conexão a ser usada; omita este parâmetro para usar a conexão sem nome.

*`connstr`*: Uma string de informações de conexão, conforme descrito anteriormente para `dblink_connect`.

*`sql`*: O comando SQL que você deseja executar no banco de dados remoto, por exemplo `insert into foo values(0, 'a', '{"a0","b0","c0"}')`.

*`fail_on_error`*: Se verdadeiro (o padrão quando omitido), um erro lançado no lado remoto da conexão causa um erro também a ser lançado localmente. Se falso, o erro remoto é relatado localmente como um NOTÍCIE, e o valor de retorno da função é definido como `ERROR`.

## Valor de retorno

Retorna o status, seja a string de status do comando ou `ERROR`.

## Exemplos

```
SELECT dblink_connect('dbname=dblink_test_standby');
 dblink_connect
----------------
 OK
(1 row)

SELECT dblink_exec('insert into foo values(21, ''z'', ''{"a0","b0","c0"}'');');
   dblink_exec
-----------------
 INSERT 943366 1
(1 row)

SELECT dblink_connect('myconn', 'dbname=regression');
 dblink_connect
----------------
 OK
(1 row)

SELECT dblink_exec('myconn', 'insert into foo values(21, ''z'', ''{"a0","b0","c0"}'');');
   dblink_exec
------------------
 INSERT 6432584 1
(1 row)

SELECT dblink_exec('myconn', 'insert into pg_class values (''foo'')',false);
NOTICE:  sql error
DETAIL:  ERROR:  null value in column "relnamespace" violates not-null constraint

 dblink_exec
-------------
 ERROR
(1 row)
```
