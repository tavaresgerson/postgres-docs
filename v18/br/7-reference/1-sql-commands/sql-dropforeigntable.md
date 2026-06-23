## DROP FOREIGN TABLE

DROP FOREIGN TABLE — remova uma tabela estrangeira

## Sinopse

```
DROP FOREIGN TABLE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

## Descrição

`DROP FOREIGN TABLE` remove uma tabela estrangeira. Apenas o proprietário de uma tabela estrangeira pode removê-la.

## Parâmetros

`IF EXISTS`: Não exija erro se a tabela estrangeira não existir. Um aviso é emitido neste caso.

*`name`*: O nome (opcionalmente qualificado por esquema) da tabela estrangeira a ser excluída.

`CASCADE`: Descarte automaticamente os objetos que dependem da tabela estrangeira (como vistas), e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15](ddl-depend.md)).

`RESTRICT`: Rejeitar a eliminação da tabela estrangeira se quaisquer objetos dependerem dela. Este é o padrão.

## Exemplos

Para destruir duas tabelas estrangeiras, `films` e `distributors`:

```
DROP FOREIGN TABLE films, distributors;
```

## Compatibilidade

Este comando está de acordo com a ISO/IEC 9075-9 (SQL/MED), exceto pelo fato de que o padrão só permite que uma tabela estrangeira seja excluída por comando, e, à parte a opção `IF EXISTS`, que é uma extensão do PostgreSQL.

## Veja também

[ALTERAR TABELA EXTERNA](sql-alterforeigntable.md "ALTER FOREIGN TABLE"), [CADASTRAR TABELA EXTERNA](sql-createforeigntable.md "CREATE FOREIGN TABLE")