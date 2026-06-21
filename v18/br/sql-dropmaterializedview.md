## DROP MATERIALIZED VIEW

DROP MATERIALIZED VIEW — remova uma visão materializada

## Sinopse

```
DROP MATERIALIZED VIEW [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

## Descrição

`DROP MATERIALIZED VIEW` elimina uma visão materializada existente. Para executar este comando, você deve ser o proprietário da visão materializada.

## Parâmetros

`IF EXISTS`: Não exija erro se a visão materializada não existir. Um aviso é emitido neste caso.

*`name`*: O nome (opcionalmente qualificado por esquema) da visão materializada a ser removida.

`CASCADE`: Descarte automaticamente os objetos que dependem da visão materializada (como outras visões materializadas ou visões regulares), e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15](ddl-depend.md)).

`RESTRICT`: Rejeitar a eliminação da visão materializada se houver algum objeto dependente dela. Esse é o padrão.

## Exemplos

Este comando removerá a visão materializada chamada `order_summary`:

```
DROP MATERIALIZED VIEW order_summary;
```

## Compatibilidade

`DROP MATERIALIZED VIEW` é uma extensão do PostgreSQL.

## Veja também

[Crie uma visualização materializada](sql-creatematerializedview.md "CREATE MATERIALIZED VIEW"), [Alterar visualização materializada](sql-altermaterializedview.md "ALTER MATERIALIZED VIEW"), [Atualizar visualização materializada](sql-refreshmaterializedview.md "REFRESH MATERIALIZED VIEW")