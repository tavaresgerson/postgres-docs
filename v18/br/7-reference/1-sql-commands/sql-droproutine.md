## DROP ROUTINE

DROP ROUTINE — remover uma rotina

## Sinopse

```
DROP ROUTINE [ IF EXISTS ] name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] [, ...]
    [ CASCADE | RESTRICT ]
```

## Descrição

`DROP ROUTINE` remove a definição de uma ou mais rotinas existentes. O termo “rotina” inclui funções agregadas, funções normais e procedimentos. Consulte [DROP AGGREGATE](sql-dropaggregate.md "DROP AGGREGATE"), [DROP FUNCTION](sql-dropfunction.md "DROP FUNCTION") e [DROP PROCEDURE](sql-dropprocedure.md "DROP PROCEDURE") para a descrição dos parâmetros, mais exemplos e detalhes adicionais.

## Notas

As regras de consulta usadas pelo `DROP ROUTINE` são fundamentalmente as mesmas que as do `DROP PROCEDURE`; em particular, o `DROP ROUTINE` compartilha o comportamento desse comando de considerar uma lista de argumentos que não tem marcadores *`argmode`* como possivelmente usando a definição do padrão SQL de que os argumentos `OUT` são incluídos na lista. (O `DROP AGGREGATE` e o `DROP FUNCTION` não fazem isso.)

Em alguns casos em que o mesmo nome é compartilhado por rotinas de diferentes tipos, é possível que o `DROP ROUTINE` falhe com um erro de ambiguidade quando um comando mais específico (`DROP FUNCTION`, etc.) funcionaria. Especificar a lista do tipo de argumento com mais cuidado também resolverá tais problemas.

Essas regras de busca também são utilizadas por outros comandos que atuam em rotinas existentes, como `ALTER ROUTINE` e `COMMENT ON ROUTINE`.

## Exemplos

Para descartar a rotina `foo` para o tipo `integer`:

```
DROP ROUTINE foo(integer);
```

Este comando funcionará independentemente de `foo` ser um agregado, uma função ou um procedimento.

## Compatibilidade

Este comando está de acordo com o padrão SQL, com essas extensões do PostgreSQL:

* O padrão permite que apenas uma rotina seja descartada por comando.
* A opção `IF EXISTS` é uma extensão.
* A capacidade de especificar modos e nomes de argumentos é uma extensão, e as regras de busca diferem quando os modos são fornecidos.
* As funções agregadas definíveis pelo usuário são uma extensão.

## Veja também

[DROP AGGREGATE](sql-dropaggregate.md "DROP AGGREGATE"), [DROP FUNCTION](sql-dropfunction.md "DROP FUNCTION"), [DROP PROCEDURE](sql-dropprocedure.md "DROP PROCEDURE"), [ALTER ROUTINE](sql-alterroutine.md "ALTER ROUTINE")

Observe que não há comando `CREATE ROUTINE`.