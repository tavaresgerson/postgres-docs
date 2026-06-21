## DROP AGGREGATE

DROP AGGREGATE — remova uma função agregada

## Sinopse

```
DROP AGGREGATE [ IF EXISTS ] name ( aggregate_signature ) [, ...] [ CASCADE | RESTRICT ]

where aggregate_signature is:

* |
[ argmode ] [ argname ] argtype [ , ... ] |
[ [ argmode ] [ argname ] argtype [ , ... ] ] ORDER BY [ argmode ] [ argname ] argtype [ , ... ]
```

## Descrição

`DROP AGGREGATE` remove uma função agregada existente. Para executar este comando, o usuário atual deve ser o proprietário da função agregada.

## Parâmetros

`IF EXISTS`: Não exija erro se o agregado não existir. Neste caso, é emitido um aviso.

*`name`*: O nome (opcionalmente qualificado por esquema) de uma função agregada existente.

*`argmode`*: O modo de um argumento: `IN` ou `VARIADIC`. Se omitido, o padrão é `IN`.

*`argname`*: O nome de um argumento. Note que `DROP AGGREGATE` não presta atenção na verdade aos nomes dos argumentos, uma vez que apenas os tipos de dados dos argumentos são necessários para determinar a identidade da função agregada.

*`argtype`*: Um tipo de dados de entrada sobre o qual a função agregada opera. Para referenciar uma função agregada de argumento zero, escreva `*` no lugar da lista de especificações de argumento. Para referenciar uma função agregada de conjunto ordenado, escreva `ORDER BY` entre as especificações de argumento direto e agregada.

`CASCADE`: Descarte automaticamente os objetos que dependem da função agregada (como as visualizações que a utilizam), e, por sua vez, todos os objetos que dependem desses objetos (consulte a [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Não se recusar a descartar a função agregada se houver objetos que dependem dela. Esse é o padrão.

## Notas

As sintaxes alternativas para referência de agregados de conjuntos ordenados são descritas em [ALTER AGGREGATE](sql-alteraggregate.md "ALTER AGGREGATE").

## Exemplos

Para remover a função agregada `myavg` para o tipo `integer`:

```
DROP AGGREGATE myavg(integer);
```

Para remover a função agregada de conjunto hipotético `myrank`, que recebe uma lista arbitrária de colunas de ordenação e uma lista correspondente de argumentos diretos:

```
DROP AGGREGATE myrank(VARIADIC "any" ORDER BY VARIADIC "any");
```

Para remover várias funções agregadas em um comando:

```
DROP AGGREGATE myavg(integer), myavg(bigint);
```

## Compatibilidade

Não há nenhuma declaração `DROP AGGREGATE` no padrão SQL.

## Veja também

[ALTERA AGREGADO](sql-alteraggregate.md "ALTER AGGREGATE"), [CREE AGREGADO](sql-createaggregate.md "CREATE AGGREGATE")