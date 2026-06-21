## Crie a tabela como

CREATE TABLE AS — defina uma nova tabela a partir dos resultados de uma consulta

## Sinopse

```
CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name
    [ (column_name [, ...] ) ]
    [ USING method ]
    [ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
    [ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
    [ TABLESPACE tablespace_name ]
    AS query
    [ WITH [ NO ] DATA ]
```

## Descrição

`CREATE TABLE AS` cria uma tabela e a preenche com dados calculados por um comando `SELECT`. As colunas da tabela têm os nomes e os tipos de dados associados às colunas de saída do `SELECT` (exceto que você pode substituir os nomes das colunas fornecendo uma lista explícita de novos nomes de colunas).

`CREATE TABLE AS` tem alguma semelhança com a criação de uma visão, mas é realmente bem diferente: ela cria uma nova tabela e avalia a consulta apenas uma vez para preencher a nova tabela inicialmente. A nova tabela não acompanhará as alterações subsequentes nas tabelas de origem da consulta. Em contraste, uma visão reavalia sua declaração `SELECT` sempre que é consultada.

`CREATE TABLE AS` exige privilégio `CREATE` no esquema usado para a tabela.

## Parâmetros

`GLOBAL` ou `LOCAL`: Ignorado para compatibilidade. O uso dessas palavras-chave é desaconselhado; consulte [CREATE TABLE](sql-createtable.md "CREATE TABLE") para detalhes.

`TEMPORARY` ou `TEMP`: Se especificado, a tabela é criada como uma tabela temporária. Consulte [CREATE TABLE](sql-createtable.md "CREATE TABLE") para obter detalhes.

`UNLOGGED`: Se especificado, a tabela é criada como uma tabela não registrada. Consulte [CREATE TABLE](sql-createtable.md "CREATE TABLE") para obter detalhes.

`IF NOT EXISTS`: Não lance um erro se uma relação com o mesmo nome já existir; simplesmente emita um aviso e deixe a tabela sem modificações.

*`table_name`*: O nome (opcionalmente qualificado por esquema) da tabela a ser criada.

*`column_name`*: O nome de uma coluna na nova tabela. Se os nomes das colunas não forem fornecidos, eles serão retirados dos nomes de colunas de saída da consulta.

`USING method`: Esta cláusula opcional especifica o método de acesso à tabela a ser utilizado para armazenar o conteúdo da nova tabela; o método deve ser um método de acesso do tipo `TABLE`. Consulte [Capítulo 62](tableam.md "Chapter 62. Table Access Method Interface Definition") para obter mais informações. Se esta opção não for especificada, o método de acesso à tabela padrão será escolhido para a nova tabela. Consulte [default_table_access_method](runtime-config-client.md#GUC-DEFAULT-TABLE-ACCESS-METHOD) para obter mais informações.

`WITH ( storage_parameter [= value] [, ... ] )`: Esta cláusula especifica parâmetros de armazenamento opcionais para a nova tabela; consulte [Parâmetros de armazenamento](sql-createtable.md#SQL-CREATETABLE-STORAGE-PARAMETERS "Storage Parameters") na documentação do [CREATE TABLE](sql-createtable.md "CREATE TABLE") para mais informações. Para compatibilidade reversa, a cláusula `WITH` para uma tabela também pode incluir `OIDS=FALSE` para especificar que as linhas da nova tabela não devem conter OIDs (identificadores de objeto), `OIDS=TRUE` não é mais suportado.

`WITHOUT OIDS`: Esta é uma sintaxe compatível com versões anteriores para declarar uma tabela `WITHOUT OIDS`, a criação de uma tabela `WITH OIDS` não é mais suportada.

`ON COMMIT`: O comportamento das tabelas temporárias no final de um bloco de transação pode ser controlado usando `ON COMMIT`. As três opções são:

`PRESERVE ROWS` :   Não são tomadas ações especiais nas extremidades das transações. Esse é o comportamento padrão.

`DELETE ROWS` :   Todas as linhas da tabela temporária serão excluídas no final de cada bloco de transação. Essencialmente, um `TRUNCATE` automático é realizado em cada commit.

`DROP` : A tabela temporária será descartada no final do bloco atual de transação.

`TABLESPACE tablespace_name`: O *`tablespace_name` é o nome do tablespace no qual a nova tabela deve ser criada. Se não for especificado, [default_tablespace](runtime-config-client.md#GUC-DEFAULT-TABLESPACE) é consultado, ou [temp_tablespaces](runtime-config-client.md#GUC-TEMP-TABLESPACES) se a tabela for temporária.

*`query`*: Um comando [`SELECT`(sql-select.md "SELECT"), [`TABLE`(sql-select.md#SQL-TABLE "TABLE Command"), ou [`VALUES`(sql-values.md "VALUES")]] ou um comando [`EXECUTE`(sql-execute.md "EXECUTE")]] que executa uma consulta preparada [`SELECT`, [`TABLE`, ou [`VALUES`]].

`WITH [ NO ] DATA`: Esta cláusula especifica se os dados produzidos pela consulta devem ser copiados para a nova tabela ou não. Se não, apenas a estrutura da tabela é copiada. O padrão é copiar os dados.

## Notas

Este comando é funcionalmente semelhante ao [SELECT INTO](sql-selectinto.md "SELECT INTO"), mas é preferido, pois é menos provável que seja confundido com outros usos da sintaxe `SELECT INTO`. Além disso, `CREATE TABLE AS` oferece um conjunto superconjunto das funcionalidades oferecidas por `SELECT INTO`.

## Exemplos

Crie uma nova tabela `films_recent` composta apenas por entradas recentes da tabela `films`:

```
CREATE TABLE films_recent AS
  SELECT * FROM films WHERE date_prod >= '2002-01-01';
```

Para copiar uma tabela completamente, a forma abreviada usando o comando `TABLE` também pode ser usada:

```
CREATE TABLE films2 AS
  TABLE films;
```

Crie uma nova tabela temporária `films_recent`, composta apenas por entradas recentes da tabela `films`, usando uma declaração preparada. A nova tabela será descartada no commit:

```
PREPARE recentfilms(date) AS
  SELECT * FROM films WHERE date_prod > $1;
CREATE TEMP TABLE films_recent ON COMMIT DROP AS
  EXECUTE recentfilms('2002-01-01');
```

## Compatibilidade

`CREATE TABLE AS` está em conformidade com o padrão SQL. As seguintes são extensões não padronizadas:

* O padrão exige parênteses ao redor da cláusula da subconsulta; no PostgreSQL, esses parênteses são opcionais.
* No padrão, a cláusula `WITH [ NO ] DATA` é exigida; no PostgreSQL, ela é opcional.
* O PostgreSQL trata as tabelas temporárias de uma maneira bastante diferente do padrão; veja [CREATE TABLE][(sql-createtable.md "CREATE TABLE")] para detalhes.
* A cláusula `WITH` é uma extensão do PostgreSQL; os parâmetros de armazenamento não estão no padrão.
* O conceito de tablespaces do PostgreSQL não faz parte do padrão. Portanto, a cláusula `TABLESPACE` é uma extensão.

## Veja também

[Crie uma visualização materializada](sql-creatematerializedview.md "CREATE MATERIALIZED VIEW"), [Crie uma tabela](sql-createtable.md "CREATE TABLE"), [Execute](sql-execute.md "EXECUTE"), [Selecione](sql-select.md "SELECT"), [Selecione em](sql-selectinto.md "SELECT INTO"), [Valores](sql-values.md "VALUES")