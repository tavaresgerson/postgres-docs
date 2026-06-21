## DROP FUNCTION

DROP FUNCTION — remover uma função

## Sinopse

```
DROP FUNCTION [ IF EXISTS ] name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] [, ...]
    [ CASCADE | RESTRICT ]
```

## Descrição

`DROP FUNCTION` remove a definição de uma função existente. Para executar este comando, o usuário deve ser o proprietário da função. Os tipos de argumentos para a função devem ser especificados, pois várias funções diferentes podem existir com o mesmo nome e listas de argumentos diferentes.

## Parâmetros

`IF EXISTS`: Não exija erro se a função não existir. Neste caso, é emitido um aviso.

*`name`*: O nome (opcionalmente qualificado por esquema) de uma função existente. Se não for especificada uma lista de argumentos, o nome deve ser único em seu esquema.

*`argmode`*: O modo de um argumento: `IN`, `OUT`, `INOUT` ou `VARIADIC`. Se omitido, o padrão é `IN`. Note que `DROP FUNCTION` não presta atenção na verdade em argumentos `OUT`, uma vez que apenas os argumentos de entrada são necessários para determinar a identidade da função. Portanto, é suficiente listar os argumentos `IN`, `INOUT` e `VARIADIC`.

*`argname`*: O nome de um argumento. Observe que `DROP FUNCTION` não presta atenção na verdade aos nomes dos argumentos, uma vez que apenas os tipos de dados dos argumentos são necessários para determinar a identidade da função.

*`argtype`*: O(s) tipo(s) de dados dos argumentos da função (opcionalmente qualificados por esquema), se houver.

`CASCADE`: Descarte automaticamente os objetos que dependem da função (como operadores ou gatilhos), e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Rejeitar a eliminação da função se houver objetos que dependem dela. Esse é o padrão.

## Exemplos

Este comando remove a função raiz quadrada:

```
DROP FUNCTION sqrt(integer);
```

Deixe várias funções em um comando:

```
DROP FUNCTION sqrt(integer), sqrt(bigint);
```

Se o nome da função for único em seu esquema, ele pode ser referido sem uma lista de argumentos:

```
DROP FUNCTION update_employee_salaries;
```

Observe que isso é diferente de

```
DROP FUNCTION update_employee_salaries();
```

que se refere a uma função com zero argumentos, enquanto a primeira variante pode se referir a uma função com qualquer número de argumentos, incluindo zero, desde que o nome seja único.

## Compatibilidade

Este comando está de acordo com o padrão SQL, com essas extensões do PostgreSQL:

* O padrão permite que apenas uma função seja descartada por comando. * A opção `IF EXISTS` * A capacidade de especificar modos e nomes de argumentos

## Veja também

[Crie função](sql-createfunction.md "CREATE FUNCTION"), [Altere função](sql-alterfunction.md "ALTER FUNCTION"), [Exclua procedimento](sql-dropprocedure.md "DROP PROCEDURE"), [Exclua rotina](sql-droproutine.md "DROP ROUTINE")