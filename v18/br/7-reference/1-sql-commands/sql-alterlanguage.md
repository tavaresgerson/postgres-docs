## ALTERAR LINGUAGEM

ALTERAR LINGUAGEM — alterar a definição de uma linguagem procedural

## Sinopse

```
ALTER [ PROCEDURAL ] LANGUAGE name RENAME TO new_name
ALTER [ PROCEDURAL ] LANGUAGE name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
```

## Descrição

`ALTER LANGUAGE` altera a definição de uma linguagem procedural. A única funcionalidade é renomear a linguagem ou atribuir um novo proprietário. Você deve ser um superusuário ou proprietário da linguagem para usar `ALTER LANGUAGE`.

## Parâmetros

*`name`*: Nome de uma língua

*`new_name`*: O novo nome da língua

*`new_owner`*: O novo proprietário da língua

## Compatibilidade

Não há nenhuma declaração `ALTER LANGUAGE` no padrão SQL.

## Veja também

[Crie Linguagem](sql-createlanguage.md "CREATE LANGUAGE"), [Remova Linguagem](sql-droplanguage.md "DROP LANGUAGE")