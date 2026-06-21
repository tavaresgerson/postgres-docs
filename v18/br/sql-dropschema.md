## DROP SCHEMA

DROP SCHEMA — remova um esquema

## Sinopse

```
DROP SCHEMA [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

## Descrição

`DROP SCHEMA` remove esquemas do banco de dados.

Um esquema só pode ser descartado pelo seu proprietário ou por um superusuário. Observe que o proprietário pode descartar o esquema (e, portanto, todos os objetos contidos) mesmo que não possua alguns dos objetos dentro do esquema.

## Parâmetros

`IF EXISTS`: Não exija erro se o esquema não existir. Um aviso é emitido neste caso.

*`name`*: O nome de um esquema.

`CASCADE`: Descarte automaticamente os objetos (tabelas, funções, etc.) que estão contidos no esquema e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15](ddl-depend.md)).

`RESTRICT`: Rejeitar a eliminação do esquema se ele contiver quaisquer objetos. Esse é o padrão.

## Notas

Usar a opção `CASCADE` pode fazer com que o comando remova objetos em outros esquemas além do(s) nomeado(s).

## Exemplos

Para remover o esquema `mystuff` do banco de dados, juntamente com tudo o que ele contém:

```
DROP SCHEMA mystuff CASCADE;
```

## Compatibilidade

`DROP SCHEMA` está totalmente conforme com o padrão SQL, exceto pelo fato de que o padrão só permite que um esquema seja excluído por comando, e, à parte a opção `IF EXISTS`, que é uma extensão do PostgreSQL.

## Veja também

[ALTERAR SCHEMA](sql-alterschema.md "ALTER SCHEMA"), [Cria SCHEMA](sql-createschema.md "CREATE SCHEMA")