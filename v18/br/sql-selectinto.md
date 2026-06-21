## SELECT INTO

SELECT INTO — definir uma nova tabela a partir dos resultados de uma consulta

## Sinopse

```
[ WITH [ RECURSIVE ] with_query [, ...] ]
SELECT [ ALL | DISTINCT [ ON ( expression [, ...] ) ] ]
    [ { * | expression [ [ AS ] output_name ] } [, ...] ]
    INTO [ TEMPORARY | TEMP | UNLOGGED ] [ TABLE ] new_table
    [ FROM from_item [, ...] ]
    [ WHERE condition ]
    [ GROUP BY expression [, ...] ]
    [ HAVING condition ]
    [ WINDOW window_name AS ( window_definition ) [, ...] ]
    [ { UNION | INTERSECT | EXCEPT } [ ALL | DISTINCT ] select ]
    [ ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS { FIRST | LAST } ] [, ...] ]
    [ LIMIT { count | ALL } ]
    [ OFFSET start [ ROW | ROWS ] ]
    [ FETCH { FIRST | NEXT } [ count ] { ROW | ROWS } ONLY ]
    [ FOR { UPDATE | SHARE } [ OF table_name [, ...] ] [ NOWAIT ] [...] ]
```

## Descrição

`SELECT INTO` cria uma nova tabela e a preenche com dados calculados por uma consulta. Os dados não são retornados ao cliente, como é o caso de um `SELECT` normal. As colunas da nova tabela têm os nomes e os tipos de dados associados às colunas de saída do `SELECT`.

## Parâmetros

`TEMPORARY` ou `TEMP`: Se especificado, a tabela é criada como uma tabela temporária. Consulte [CREATE TABLE](sql-createtable.md "CREATE TABLE") para obter detalhes.

`UNLOGGED`: Se especificado, a tabela é criada como uma tabela não registrada. Consulte [CREATE TABLE](sql-createtable.md "CREATE TABLE") para obter detalhes.

*`new_table`*: O nome (opcionalmente qualificado por esquema) da tabela a ser criada.

Todos os outros parâmetros são descritos em detalhes em [SELECT](sql-select.md "SELECT").

## Notas

`CREATE TABLE AS` é funcionalmente semelhante a (sql-createtableas.md "CREATE TABLE AS"). `CREATE TABLE AS` é a sintaxe recomendada, pois essa forma de `SELECT INTO` não está disponível no ECPG ou no PL/pgSQL, porque eles interpretam a cláusula `INTO` de maneira diferente. Além disso, `CREATE TABLE AS` oferece um conjunto superconjunto das funcionalidades fornecidas por `SELECT INTO`.

Em contraste com `CREATE TABLE AS`, `SELECT INTO` não permite especificar propriedades como o método de acesso de uma tabela com [(sql-createtable.md#SQL-CREATETABLE-METHOD)]`USING method` ou o espaço de tabela da tabela com [`TABLESPACE tablespace_name`](sql-createtable.md#SQL-CREATETABLE-TABLESPACE). Use `CREATE TABLE AS` se necessário. Portanto, o método de acesso padrão de tabela é escolhido para a nova tabela. Consulte [default_table_access_method](runtime-config-client.md#GUC-DEFAULT-TABLE-ACCESS-METHOD) para mais informações.

## Exemplos

Crie uma nova tabela `films_recent` composta apenas por entradas recentes da tabela `films`:

```
SELECT * INTO films_recent FROM films WHERE date_prod >= '2002-01-01';
```

## Compatibilidade

O padrão SQL utiliza `SELECT INTO` para representar a seleção de valores em variáveis escalares de um programa hospedeiro, em vez de criar uma nova tabela. De fato, esse é o uso encontrado no ECPG (ver [Capítulo 34][(ecpg.md "Chapter 34. ECPG — Embedded SQL in C")]) e no PL/pgSQL (ver [Capítulo 41][(plpgsql.md "Chapter 41. PL/pgSQL — SQL Procedural Language")]). O uso do PostgreSQL de `SELECT INTO` para representar a criação de tabelas é histórico. Algumas outras implementações do SQL também usam `SELECT INTO` dessa maneira (mas a maioria das implementações do SQL suporta `CREATE TABLE AS` em vez disso). Além dessas considerações de compatibilidade, é melhor usar `CREATE TABLE AS` para esse propósito em código novo.

## Veja também

[Crie uma tabela como](sql-createtableas.md "CREATE TABLE AS")