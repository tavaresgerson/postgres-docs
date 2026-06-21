## REFRESH VIEW MATERIALIZADO

REFAZER VISÃO MATERIALIZADA — substituir o conteúdo de uma visão materializada

## Sinopse

```
REFRESH MATERIALIZED VIEW [ CONCURRENTLY ] name
    [ WITH [ NO ] DATA ]
```

## Descrição

`REFRESH MATERIALIZED VIEW` substitui completamente o conteúdo de uma visão materializada. Para executar este comando, você deve ter o privilégio `MAINTAIN` na visão materializada. O conteúdo antigo é descartado. Se `WITH DATA` for especificado (ou padrão), a consulta de suporte é executada para fornecer os novos dados, e a visão materializada é deixada em um estado de varredura. Se `WITH NO DATA` for especificado, não são gerados novos dados e a visão materializada é deixada em um estado não scanável.

`CONCURRENTLY` e `WITH NO DATA` não podem ser especificados juntos.

## Parâmetros

`CONCURRENTLY`: Atualize a visão materializada sem bloquear seleções concorrentes na visão materializada. Sem essa opção, uma atualização que afeta muitas linhas tende a usar menos recursos e completar mais rapidamente, mas pode bloquear outras conexões que estão tentando ler a visão materializada. Essa opção pode ser mais rápida em casos em que um pequeno número de linhas é afetado.

Esta opção só é permitida se houver pelo menos um índice `UNIQUE` na visão materializada que utilize apenas nomes de colunas e inclua todas as linhas; ou seja, não deve ser um índice de expressão ou incluir uma cláusula `WHERE`.

Essa opção só pode ser usada quando a visão materializada já está preenchida.

Mesmo com essa opção, apenas um `REFRESH` pode ser executado por vez contra qualquer visão materializada.

*`name`*: O nome (opcionalmente qualificado por esquema) da visão materializada a ser atualizada.

## Notas

Se houver uma cláusula `ORDER BY` na consulta que define a visão materializada, o conteúdo original da visão materializada será ordenado dessa maneira; mas a `REFRESH MATERIALIZED VIEW` não garante a preservação dessa ordem.

Enquanto o `REFRESH MATERIALIZED VIEW` está em execução, o [search_path](runtime-config-client.md#GUC-SEARCH-PATH) é temporariamente alterado para `pg_catalog, pg_temp`.

## Exemplos

Este comando substituirá o conteúdo da visão materializada chamada `order_summary` usando a consulta da definição da visão materializada, e a deixará em um estado de varredura:

```
REFRESH MATERIALIZED VIEW order_summary;
```

Este comando liberará o armazenamento associado à visão materializada `annual_statistics_basis` e a deixará em um estado não rastreável:

```
REFRESH MATERIALIZED VIEW annual_statistics_basis WITH NO DATA;
```

## Compatibilidade

`REFRESH MATERIALIZED VIEW` é uma extensão do PostgreSQL.

## Veja também

[Crie uma visualização materializada](sql-creatematerializedview.md "CREATE MATERIALIZED VIEW"), [Alterar visualização materializada](sql-altermaterializedview.md "ALTER MATERIALIZED VIEW"), [Remova visualização materializada](sql-dropmaterializedview.md "DROP MATERIALIZED VIEW")