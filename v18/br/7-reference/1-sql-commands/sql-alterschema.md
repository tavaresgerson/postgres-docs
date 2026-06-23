## ALTER SCHEMA

ALTERAR ESCHEMA — alterar a definição de um esquema

## Sinopse

```
ALTER SCHEMA name RENAME TO new_name
ALTER SCHEMA name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
```

## Descrição

`ALTER SCHEMA` altera a definição de um esquema.

Você deve possuir o esquema para usar `ALTER SCHEMA`. Para renomear um esquema, você também deve ter o privilégio `CREATE` para o banco de dados. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário, e esse papel deve ter o privilégio `CREATE` para o banco de dados. (Observe que os superusuários têm todos esses privilégios automaticamente.)

## Parâmetros

*`name`*: O nome de um esquema existente.

*`new_name`*: O novo nome do esquema. O novo nome não pode começar com `pg_`, pois tais nomes são reservados para esquemas de sistema.

*`new_owner`*: O novo proprietário do esquema.

## Compatibilidade

Não há nenhuma declaração `ALTER SCHEMA` no padrão SQL.

## Veja também

[Crie o esquema](sql-createschema.md "CREATE SCHEMA"), [Exclua o esquema](sql-dropschema.md "DROP SCHEMA")