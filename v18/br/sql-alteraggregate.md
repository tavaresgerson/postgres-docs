## ALTER AGGREGATE

ALTER AGGREGATE — alterar a definição de uma função agregada

## Sinopse

```
ALTER AGGREGATE name ( aggregate_signature ) RENAME TO new_name
ALTER AGGREGATE name ( aggregate_signature )
                OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER AGGREGATE name ( aggregate_signature ) SET SCHEMA new_schema

where aggregate_signature is:

* |
[ argmode ] [ argname ] argtype [ , ... ] |
[ [ argmode ] [ argname ] argtype [ , ... ] ] ORDER BY [ argmode ] [ argname ] argtype [ , ... ]
```

## Descrição

`ALTER AGGREGATE` altera a definição de uma função agregada.

Você deve possuir a função agregada para usar `ALTER AGGREGATE`. Para alterar o esquema de uma função agregada, você também deve ter privilégio `CREATE` no novo esquema. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário, e esse papel deve ter privilégio `CREATE` no esquema da função agregada. (Essas restrições garantem que alterar o proprietário não faz nada que você não pudesse fazer ao descartar e recriar a função agregada. No entanto, um superusuário pode alterar a propriedade de qualquer função agregada de qualquer maneira.)

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de uma função agregada existente.

*`argmode`*: O modo de um argumento: `IN` ou `VARIADIC`. Se omitido, o padrão é `IN`.

*`argname`*: O nome de um argumento. Observe que `ALTER AGGREGATE` não presta atenção na verdade aos nomes dos argumentos, uma vez que apenas os tipos de dados dos argumentos são necessários para determinar a identidade da função agregada.

*`argtype`*: Um tipo de dados de entrada sobre o qual a função agregada opera. Para referenciar uma função agregada de argumento zero, escreva `*` no lugar da lista de especificações de argumento. Para referenciar uma função agregada de conjunto ordenado, escreva `ORDER BY` entre as especificações de argumento direto e agregada.

*`new_name`*: O novo nome da função agregada.

*`new_owner`*: O novo proprietário da função agregada.

*`new_schema`*: O novo esquema para a função agregada.

## Notas

A sintaxe recomendada para referenciar um agregado de conjunto ordenado é escrever `ORDER BY` entre as especificações de argumentos diretos e agregados, no mesmo estilo que em `CREATE AGGREGATE`(sql-createaggregate.md "CREATE AGGREGATE"). No entanto, também funcionará omitir `ORDER BY` e simplesmente executar as especificações de argumentos diretos e agregados em uma única lista. Nesta forma abreviada, se `VARIADIC "any"` foi usado tanto nas listas de argumentos diretos quanto agregados, escreva `VARIADIC "any"` apenas uma vez.

## Exemplos

Para renomear a função agregada `myavg` para o tipo `integer` para `my_average`:

```
ALTER AGGREGATE myavg(integer) RENAME TO my_average;
```

Para alterar o proprietário da função agregada `myavg` para o tipo `integer` para `joe`:

```
ALTER AGGREGATE myavg(integer) OWNER TO joe;
```

Para mover o agregado de conjunto ordenado `mypercentile` com argumento direto do tipo `float8` e argumento agregado do tipo `integer` no esquema `myschema`:

```
ALTER AGGREGATE mypercentile(float8 ORDER BY integer) SET SCHEMA myschema;
```

Isso também funcionará:

```
ALTER AGGREGATE mypercentile(float8, integer) SET SCHEMA myschema;
```

## Compatibilidade

Não há nenhuma declaração `ALTER AGGREGATE` no padrão SQL.

## Veja também

[Crie AGGREGADO](sql-createaggregate.md "CREATE AGGREGATE"), [Remova AGGREGADO](sql-dropaggregate.md "DROP AGGREGATE")