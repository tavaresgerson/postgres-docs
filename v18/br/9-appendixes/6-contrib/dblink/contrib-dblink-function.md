## dblink

dblink — executa uma consulta em um banco de dados remoto

## Sinopse

```
dblink(text connname, text sql [, bool fail_on_error]) returns setof record
dblink(text connstr, text sql [, bool fail_on_error]) returns setof record
dblink(text sql [, bool fail_on_error]) returns setof record
```

## Descrição

`dblink` executa uma consulta (geralmente uma `SELECT`, mas pode ser qualquer declaração SQL que retorne linhas) em um banco de dados remoto.

Quando são fornecidos dois argumentos `text`, o primeiro é procurado como o nome de uma conexão persistente; se encontrado, o comando é executado nessa conexão. Se não for encontrado, o primeiro argumento é tratado como uma string de informações de conexão, como no caso de `dblink_connect`, e a conexão indicada é feita apenas durante a duração deste comando.

## Argumentos

*`connname`*: Nome da conexão a ser usada; omita este parâmetro para usar a conexão sem nome.

*`connstr`*: Uma string de informações de conexão, conforme descrito anteriormente para `dblink_connect`.

*`sql`*: A consulta SQL que você deseja executar no banco de dados remoto, por exemplo `select * from foo`.

*`fail_on_error`*: Se verdadeiro (o padrão quando omitido), um erro lançado no lado remoto da conexão causa um erro também a ser lançado localmente. Se falso, o erro remoto é relatado localmente como um NOTÍCIE, e a função retorna nenhuma linha.

## Valor de retorno

A função retorna a(s) linha(s) produzida(s) pela consulta. Como `dblink` pode ser usado com qualquer consulta, é declarado para retornar `record`, em vez de especificar qualquer conjunto específico de colunas. Isso significa que você deve especificar o conjunto esperado de colunas na consulta que está fazendo a chamada — caso contrário, o PostgreSQL não saberia o que esperar. Aqui está um exemplo:

```
SELECT *
    FROM dblink('dbname=mydb options=-csearch_path=',
                'select proname, prosrc from pg_proc')
      AS t1(proname name, prosrc text)
    WHERE proname LIKE 'bytea%';
```

A parte “alias” da cláusula `FROM` deve especificar os nomes e tipos das colunas que a função retornará. (Especificar os nomes das colunas em uma alias é, na verdade, a sintaxe padrão do SQL, mas especificar os tipos das colunas é uma extensão do PostgreSQL.) Isso permite que o sistema entenda para o que a `*` deve expandir e para o que a `proname` na cláusula `WHERE` se refere, antes de tentar executar a função. No momento da execução, um erro será lançado se o resultado real da consulta do banco de dados remoto não tiver o mesmo número de colunas exibidas na cláusula `FROM`. Os nomes das colunas não precisam corresponder, no entanto, e a `dblink` não insiste em correspondências exatas de tipos. Ela terá sucesso desde que as strings de dados retornadas sejam entradas válidas para o tipo de coluna declarado na cláusula `FROM`.

## Notas

Uma maneira conveniente de usar `dblink` com consultas predeterminadas é criar uma visão. Isso permite que as informações sobre o tipo de coluna sejam ocultas na visão, em vez de precisar escrevê-las em cada consulta. Por exemplo,

```
CREATE VIEW myremote_pg_proc AS
  SELECT *
    FROM dblink('dbname=postgres options=-csearch_path=',
                'select proname, prosrc from pg_proc')
    AS t1(proname name, prosrc text);

SELECT * FROM myremote_pg_proc WHERE proname LIKE 'bytea%';
```

## Exemplos

```
SELECT * FROM dblink('dbname=postgres options=-csearch_path=',
                     'select proname, prosrc from pg_proc')
  AS t1(proname name, prosrc text) WHERE proname LIKE 'bytea%';
  proname   |   prosrc
------------+------------
 byteacat   | byteacat
 byteaeq    | byteaeq
 bytealt    | bytealt
 byteale    | byteale
 byteagt    | byteagt
 byteage    | byteage
 byteane    | byteane
 byteacmp   | byteacmp
 bytealike  | bytealike
 byteanlike | byteanlike
 byteain    | byteain
 byteaout   | byteaout
(12 rows)

SELECT dblink_connect('dbname=postgres options=-csearch_path=');
 dblink_connect
----------------
 OK
(1 row)

SELECT * FROM dblink('select proname, prosrc from pg_proc')
  AS t1(proname name, prosrc text) WHERE proname LIKE 'bytea%';
  proname   |   prosrc
------------+------------
 byteacat   | byteacat
 byteaeq    | byteaeq
 bytealt    | bytealt
 byteale    | byteale
 byteagt    | byteagt
 byteage    | byteage
 byteane    | byteane
 byteacmp   | byteacmp
 bytealike  | bytealike
 byteanlike | byteanlike
 byteain    | byteain
 byteaout   | byteaout
(12 rows)

SELECT dblink_connect('myconn', 'dbname=regression options=-csearch_path=');
 dblink_connect
----------------
 OK
(1 row)

SELECT * FROM dblink('myconn', 'select proname, prosrc from pg_proc')
  AS t1(proname name, prosrc text) WHERE proname LIKE 'bytea%';
  proname   |   prosrc
------------+------------
 bytearecv  | bytearecv
 byteasend  | byteasend
 byteale    | byteale
 byteagt    | byteagt
 byteage    | byteage
 byteane    | byteane
 byteacmp   | byteacmp
 bytealike  | bytealike
 byteanlike | byteanlike
 byteacat   | byteacat
 byteaeq    | byteaeq
 bytealt    | bytealt
 byteain    | byteain
 byteaout   | byteaout
(14 rows)
```
