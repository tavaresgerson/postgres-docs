## ALTERAR ROTINA

ALTERAR ROTINA — alterar a definição de uma rotina

## Sinopse

```
ALTER ROUTINE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    action [ ... ] [ RESTRICT ]
ALTER ROUTINE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    RENAME TO new_name
ALTER ROUTINE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER ROUTINE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    SET SCHEMA new_schema
ALTER ROUTINE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    [ NO ] DEPENDS ON EXTENSION extension_name

where action is one of:

    IMMUTABLE | STABLE | VOLATILE
    [ NOT ] LEAKPROOF
    [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER
    PARALLEL { UNSAFE | RESTRICTED | SAFE }
    COST execution_cost
    ROWS result_rows
    SET configuration_parameter { TO | = } { value | DEFAULT }
    SET configuration_parameter FROM CURRENT
    RESET configuration_parameter
    RESET ALL
```

## Descrição

`ALTER ROUTINE` altera a definição de uma rotina, que pode ser uma função agregada, uma função normal ou um procedimento. Consulte [ALTER AGGREGATE](sql-alteraggregate.md "ALTER AGGREGATE"), [ALTER FUNCTION](sql-alterfunction.md "ALTER FUNCTION") e [ALTER PROCEDURE](sql-alterprocedure.md "ALTER PROCEDURE") para a descrição dos parâmetros, mais exemplos e detalhes adicionais.

## Exemplos

Para renomear a rotina `foo` para o tipo `integer` para `foobar`:

```
ALTER ROUTINE foo(integer) RENAME TO foobar;
```

Este comando funcionará independentemente de `foo` ser um agregado, uma função ou um procedimento.

## Compatibilidade

Essa declaração é parcialmente compatível com a declaração `ALTER ROUTINE` no padrão SQL. Consulte [ALTER FUNCTION](sql-alterfunction.md "ALTER FUNCTION") e [ALTER PROCEDURE](sql-alterprocedure.md "ALTER PROCEDURE") para obter mais detalhes. Permitir que os nomes de rotina se refiram a funções agregadas é uma extensão do PostgreSQL.

## Veja também

[ALTER AGGREGATE](sql-alteraggregate.md "ALTER AGGREGATE"), [ALTER FUNCTION](sql-alterfunction.md "ALTER FUNCTION"), [ALTER PROCEDURE](sql-alterprocedure.md "ALTER PROCEDURE"), [DROP ROUTINE](sql-droproutine.md "DROP ROUTINE")

Observe que não há comando `CREATE ROUTINE`.