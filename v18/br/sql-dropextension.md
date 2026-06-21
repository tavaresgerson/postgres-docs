## DROP EXTENSION

DROP EXTENSION — remover uma extensão

## Sinopse

```
DROP EXTENSION [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

## Descrição

`DROP EXTENSION` remove extensões do banco de dados. A eliminação de uma extensão faz com que seus objetos membros e outras rotinas explicitamente dependentes (consulte a ação [[ALTER ROUTINE]] (sql-alterroutine.md "ALTER ROUTINE"), `DEPENDS ON EXTENSION extension_name`), também sejam eliminados.

Você deve possuir a extensão para usar `DROP EXTENSION`.

## Parâmetros

`IF EXISTS`: Não exija erro se a extensão não existir. Um aviso é emitido neste caso.

*`name`*: O nome de uma extensão instalada.

`CASCADE`: Descarte automaticamente os objetos que dependem da extensão e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15](ddl-depend.md)).

`RESTRICT`: Esta opção impede que as extensões especificadas sejam descartadas se outros objetos, além dessas extensões, seus membros e suas rotinas explicitamente dependentes, dependam delas. Esta é a opção padrão.

## Exemplos

Para remover a extensão `hstore` do banco de dados atual:

```
DROP EXTENSION hstore;
```

Este comando falhará se qualquer um dos objetos do `hstore` estiver em uso no banco de dados, por exemplo, se houver quaisquer tabelas com colunas do tipo `hstore`. Adicione a opção `CASCADE` para remover forçadamente esses objetos dependentes também.

## Compatibilidade

`DROP EXTENSION` é uma extensão do PostgreSQL.

## Veja também

[CREATE EXTENSION](sql-createextension.md "CREATE EXTENSION"), [ALTER EXTENSION](sql-alterextension.md "ALTER EXTENSION")