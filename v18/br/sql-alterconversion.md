## ALTERAR A CONVERSÃO

ALTERAR CONVERSÃO — alterar a definição de uma conversão

## Sinopse

```
ALTER CONVERSION name RENAME TO new_name
ALTER CONVERSION name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER CONVERSION name SET SCHEMA new_schema
```

## Descrição

`ALTER CONVERSION` altera a definição de uma conversão.

Você deve ser o proprietário da conversão para usar `ALTER CONVERSION`. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário, e esse papel deve ter `CREATE` privilégio no esquema da conversão. (Essas restrições garantem que alterar o proprietário não faz nada que você não poderia fazer ao descartar e recriar a conversão. No entanto, um superusuário pode alterar a propriedade de qualquer conversão de qualquer maneira.)

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de uma conversão existente.

*`new_name`*: O novo nome da conversão.

*`new_owner`*: O novo proprietário da conversão.

*`new_schema`*: O novo esquema para a conversão.

## Exemplos

Para renomear a conversão `iso_8859_1_to_utf8` para `latin1_to_unicode`:

```
ALTER CONVERSION iso_8859_1_to_utf8 RENAME TO latin1_to_unicode;
```

Para alterar o proprietário da conversão `iso_8859_1_to_utf8` para `joe`:

```
ALTER CONVERSION iso_8859_1_to_utf8 OWNER TO joe;
```

## Compatibilidade

Não há nenhuma declaração `ALTER CONVERSION` no padrão SQL.

## Veja também

[Crie conversão](sql-createconversion.md "CREATE CONVERSION"), [Retire conversão](sql-dropconversion.md "DROP CONVERSION")