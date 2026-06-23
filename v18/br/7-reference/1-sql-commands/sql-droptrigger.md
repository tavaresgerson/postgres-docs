## DROP TRIGGER

DROP TRIGGER — remover um gatilho

## Sinopse

```
DROP TRIGGER [ IF EXISTS ] name ON table_name [ CASCADE | RESTRICT ]
```

## Descrição

`DROP TRIGGER` remove uma definição de gatilho existente. Para executar este comando, o usuário atual deve ser o proprietário da tabela para a qual o gatilho é definido.

## Parâmetros

`IF EXISTS`: Não exija erro se o gatilho não existir. Um aviso é emitido neste caso.

*`name`*: O nome do gatilho a ser removido.

*`table_name`*: O nome (opcionalmente qualificado por esquema) da tabela para a qual o gatilho é definido.

`CASCADE`: Descarte automaticamente os objetos que dependem do gatilho e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15](ddl-depend.md)).

`RESTRICT`: Rejeitar a eliminação do gatilho se quaisquer objetos dependerem dele. Esse é o padrão.

## Exemplos

Destruir o gatilho `if_dist_exists` na mesa `films`:

```
DROP TRIGGER if_dist_exists ON films;
```

## Compatibilidade

A declaração `DROP TRIGGER` no PostgreSQL é incompatível com o padrão SQL. No padrão SQL, os nomes dos gatilhos não são locais às tabelas, então o comando é simplesmente `DROP TRIGGER name`.

## Veja também

[Crie TRIGGER](sql-createtrigger.md "CREATE TRIGGER")