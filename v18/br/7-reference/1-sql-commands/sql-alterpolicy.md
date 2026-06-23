## ALTERAR POLÍTICA

ALTERAR POLÍTICA — alterar a definição de uma política de segurança de nível de linha

## Sinopse

```
ALTER POLICY name ON table_name RENAME TO new_name

ALTER POLICY name ON table_name
    [ TO { role_name | PUBLIC | CURRENT_ROLE | CURRENT_USER | SESSION_USER } [, ...] ]
    [ USING ( using_expression ) ]
    [ WITH CHECK ( check_expression ) ]
```

## Descrição

`ALTER POLICY` altera a definição de uma política de segurança de nível de linha existente. Observe que `ALTER POLICY` permite apenas o conjunto de papéis aos quais a política se aplica e as expressões `USING` e `WITH CHECK` podem ser modificadas. Para alterar outras propriedades de uma política, como o comando ao qual ela se aplica ou se é permissiva ou restritiva, a política deve ser descartada e recriada.

Para usar `ALTER POLICY`, você deve possuir a tabela à qual a política se aplica.

Na segunda forma do `ALTER POLICY`, a lista de papéis, *`using_expression`* e *`check_expression`* são substituídos de forma independente, se especificados. Quando uma dessas cláusulas é omitida, a parte correspondente da política permanece inalterada.

## Parâmetros

*`name`*: O nome de uma política existente para alterar.

*`table_name`*: O nome (opcionalmente qualificado por esquema) da tabela na qual a política está.

*`new_name`*: O novo nome da política.

*`role_name`*: O(s) papel(es) ao qual a política se aplica. Múltiplos papéis podem ser especificados de uma só vez. Para aplicar a política a todos os papéis, use `PUBLIC`.

*`using_expression`*: A expressão `USING` para a política. Consulte [CREATE POLICY](sql-createpolicy.md "CREATE POLICY") para obter detalhes.

*`check_expression`*: A expressão `WITH CHECK` para a política. Consulte [CREATE POLICY](sql-createpolicy.md "CREATE POLICY") para detalhes.

## Compatibilidade

`ALTER POLICY` é uma extensão do PostgreSQL.

## Veja também

[Crie a política](sql-createpolicy.md "CREATE POLICY"), [Remeta a política](sql-droppolicy.md "DROP POLICY")