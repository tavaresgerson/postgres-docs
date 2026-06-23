## CRIAR VISÃO MATERIALIZADA

Crie uma visualização materializada — defina uma nova visualização materializada

## Sinopse

```
CREATE MATERIALIZED VIEW [ IF NOT EXISTS ] table_name
    [ (column_name [, ...] ) ]
    [ USING method ]
    [ WITH ( storage_parameter [= value] [, ... ] ) ]
    [ TABLESPACE tablespace_name ]
    AS query
    [ WITH [ NO ] DATA ]
```

## Descrição

`CREATE MATERIALIZED VIEW` define uma visão materializada de uma consulta. A consulta é executada e usada para preencher a visão no momento em que o comando é emitido (a menos que `WITH NO DATA` seja usado) e pode ser atualizada posteriormente usando `REFRESH MATERIALIZED VIEW`.

`CREATE MATERIALIZED VIEW` é semelhante a `CREATE TABLE AS`, exceto que ele também lembra a consulta usada para inicializar a visão, para que possa ser atualizada posteriormente, quando necessário. Uma visão materializada tem muitas das mesmas propriedades que uma tabela, mas não há suporte para visões materializadas temporárias.

O `CREATE MATERIALIZED VIEW` requer privilégio `CREATE` no esquema usado para a visão materializada.

## Parâmetros

`IF NOT EXISTS`: Não exija um erro se uma visão materializada com o mesmo nome já existir. Um aviso é emitido neste caso. Observe que não há garantia de que a visão materializada existente seja algo parecido com a que teria sido criada.

*`table_name`*: O nome (opcionalmente qualificado por esquema) da visão materializada a ser criada. O nome deve ser distinto do nome de qualquer outra relação (tabela, sequência, índice, visão, visão materializada ou tabela estrangeira) no mesmo esquema.

*`column_name`*: O nome de uma coluna na nova visão materializada. Se os nomes das colunas não forem fornecidos, eles serão retirados dos nomes de colunas de saída da consulta.

`USING method`: Esta cláusula opcional especifica o método de acesso à tabela a ser utilizado para armazenar o conteúdo da nova visão materializada; o método deve ser um método de acesso do tipo `TABLE`. Consulte [Capítulo 62](tableam.md "Chapter 62. Table Access Method Interface Definition") para obter mais informações. Se esta opção não for especificada, o método de acesso à tabela padrão é escolhido para a nova visão materializada. Consulte [default_table_access_method](runtime-config-client.md#GUC-DEFAULT-TABLE-ACCESS-METHOD) para obter mais informações.

`WITH ( storage_parameter [= value] [, ... ] )`: Esta cláusula especifica parâmetros de armazenamento opcionais para a nova visão materializada; consulte [Parâmetros de armazenamento](sql-createtable.md#SQL-CREATETABLE-STORAGE-PARAMETERS "Storage Parameters") na documentação do [CREATE TABLE](sql-createtable.md "CREATE TABLE") para mais informações. Todos os parâmetros suportados para `CREATE TABLE` também são suportados para `CREATE MATERIALIZED VIEW`. Consulte [CREATE TABLE](sql-createtable.md "CREATE TABLE") para mais informações.

`TABLESPACE tablespace_name`: O *`tablespace_name`* é o nome do tablespace no qual a nova visão materializada deve ser criada. Se não for especificado, [default_tablespace](runtime-config-client.md#GUC-DEFAULT-TABLESPACE) é consultado.

*`query`*: Um comando [`SELECT`](sql-select.md), [`TABLE`](sql-select.md#SQL-TABLE), ou [`VALUES`](sql-values.md)]. Esta consulta será executada dentro de uma operação com restrições de segurança; em particular, as chamadas a funções que criam tabelas temporárias falharão. Além disso, enquanto a consulta estiver sendo executada, o [search_path](runtime-config-client.md#GUC-SEARCH-PATH) será alterado temporariamente para `pg_catalog, pg_temp`.

`WITH [ NO ] DATA`: Esta cláusula especifica se a visão materializada deve ser preenchida no momento da criação. Se não for o caso, a visão materializada será marcada como não scanável e não poderá ser consultada até que `REFRESH MATERIALIZED VIEW` seja usado.

## Compatibilidade

`CREATE MATERIALIZED VIEW` é uma extensão do PostgreSQL.

## Veja também

[ALTERAR VISUALIZADOR MATERIALIZADO](sql-altermaterializedview.md "ALTER MATERIALIZED VIEW"), [CADASTRAR Tabela COMO](sql-createtableas.md "CREATE TABLE AS"), [CADASTRAR VISUALIZADOR](sql-createview.md "CREATE VIEW"), [CANCELAR VISUALIZADOR MATERIALIZADO](sql-dropmaterializedview.md "DROP MATERIALIZED VIEW"), [REFAZER VISUALIZADOR MATERIALIZADO](sql-refreshmaterializedview.md "REFRESH MATERIALIZED VIEW")