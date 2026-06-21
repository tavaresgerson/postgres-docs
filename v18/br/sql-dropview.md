## DROP VIEW

DROP VIEW — remover uma visão

## Sinopse

```
DROP VIEW [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

## Descrição

`DROP VIEW` elimina uma visão existente. Para executar este comando, você deve ser o proprietário da visão.

## Parâmetros

`IF EXISTS`: Não exija erro se a visualização não existir. Um aviso é emitido neste caso.

*`name`*: O nome (opcionalmente qualificado por esquema) da visualização a ser removida.

`CASCADE`: Descarte automaticamente os objetos que dependem da visualização (como outras visualizações), e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Rejeitar a eliminação da visão se algum objeto depender dela. Esse é o padrão.

## Exemplos

Este comando removerá a visualização chamada `kinds`:

```
DROP VIEW kinds;
```

## Compatibilidade

Este comando está de acordo com o padrão SQL, exceto pelo fato de que o padrão só permite que uma visão seja descartada por comando, e, além da opção `IF EXISTS`, que é uma extensão do PostgreSQL.

## Veja também

[ALTERAR VISTA](sql-alterview.md "ALTER VIEW"), [CADA VISTA](sql-createview.md "CREATE VIEW")