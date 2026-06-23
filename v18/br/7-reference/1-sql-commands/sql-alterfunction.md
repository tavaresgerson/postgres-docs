## ALTER FUNCTION

ALTER FUNCTION — alterar a definição de uma função

## Sinopse

```
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    action [ ... ] [ RESTRICT ]
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    RENAME TO new_name
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    SET SCHEMA new_schema
ALTER FUNCTION name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    [ NO ] DEPENDS ON EXTENSION extension_name

where action is one of:

    CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT
    IMMUTABLE | STABLE | VOLATILE
    [ NOT ] LEAKPROOF
    [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER
    PARALLEL { UNSAFE | RESTRICTED | SAFE }
    COST execution_cost
    ROWS result_rows
    SUPPORT support_function
    SET configuration_parameter { TO | = } { value | DEFAULT }
    SET configuration_parameter FROM CURRENT
    RESET configuration_parameter
    RESET ALL
```

## Descrição

`ALTER FUNCTION` altera a definição de uma função.

Você deve possuir a função para usar `ALTER FUNCTION`. Para alterar o esquema de uma função, você também deve ter privilégio `CREATE` no novo esquema. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário, e esse papel deve ter privilégio `CREATE` no esquema da função. (Essas restrições garantem que alterar o proprietário não faz nada que você não pudesse fazer ao descartar e recriar a função. No entanto, um superusuário pode alterar a propriedade de qualquer função de qualquer maneira.)

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de uma função existente. Se não for especificada uma lista de argumentos, o nome deve ser único em seu esquema.

*`argmode`*: O modo de um argumento: `IN`, `OUT`, `INOUT` ou `VARIADIC`. Se omitido, o padrão é `IN`. Note que `ALTER FUNCTION` não presta atenção na verdade em argumentos `OUT`, uma vez que apenas os argumentos de entrada são necessários para determinar a identidade da função. Portanto, é suficiente listar os argumentos `IN`, `INOUT` e `VARIADIC`.

*`argname`*: O nome de um argumento. Observe que `ALTER FUNCTION` não presta atenção na verdade aos nomes dos argumentos, uma vez que apenas os tipos de dados dos argumentos são necessários para determinar a identidade da função.

*`argtype`*: O(s) tipo(s) de dados dos argumentos da função (opcionalmente qualificados por esquema), se houver.

*`new_name`*: O novo nome da função.

*`new_owner`*: O novo proprietário da função. Observe que, se a função estiver marcada como `SECURITY DEFINER`, ela será executada posteriormente pelo novo proprietário.

*`new_schema`*: O novo esquema para a função.

`DEPENDS ON EXTENSION extension_name` `NO DEPENDS ON EXTENSION extension_name`: Este formulário marca a função como dependente da extensão, ou não mais dependente dessa extensão se `NO` for especificado. Uma função que é marcada como dependente de uma extensão é descartada quando a extensão é descartada, mesmo que `CASCADE` não seja especificado. Uma função pode depender de múltiplas extensões e será descartada quando qualquer uma dessas extensões for descartada.

`CALLED ON NULL INPUT` `RETURNS NULL ON NULL INPUT` `STRICT`: `CALLED ON NULL INPUT` altera a função para que ela seja invocada quando alguns ou todos os seus argumentos são nulos. `RETURNS NULL ON NULL INPUT` ou `STRICT` altera a função para que ela não seja invocada se qualquer um de seus argumentos for nulo; em vez disso, um resultado nulo é assumido automaticamente. Consulte [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION") para obter mais informações.

`IMMUTABLE` `STABLE` `VOLATILE`: Altere a volatilidade da função para o ajuste especificado. Consulte [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION") para obter detalhes.

`[ EXTERNAL ] SECURITY INVOKER` `[ EXTERNAL ] SECURITY DEFINER`: Altere se a função é um definidor de segurança ou não. A palavra-chave `EXTERNAL` é ignorada para conformidade com SQL. Consulte [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION") para obter mais informações sobre essa capacidade.

`PARALLEL`: Altere se a função é considerada segura para paralelismo. Consulte [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION") para obter detalhes.

`LEAKPROOF`: Altere se a função é considerada estanque ou não. Consulte [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION") para obter mais informações sobre essa capacidade.

`COST` *`execution_cost`*: Altere o custo estimado de execução da função. Consulte [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION") para obter mais informações.

`ROWS` *`result_rows`*: Altere o número estimado de linhas devolvidas por uma função que retorna um conjunto. Consulte [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION") para obter mais informações.

`SUPPORT` *`support_function`*: Defina ou altere a função de suporte do planejador a ser usada para esta função. Consulte [Seção 36.11](xfunc-optimization.md) para obter detalhes. Você deve ser um superusuário para usar esta opção.

Essa opção não pode ser usada para remover a função de suporte completamente, pois ela deve nomear uma nova função de suporte. Use `CREATE OR REPLACE FUNCTION` se você precisar fazer isso.

*`configuration_parameter`* *`value`*: Adicione ou altere a atribuição a ser feita a um parâmetro de configuração quando a função é chamada. Se *`value`* for `DEFAULT` ou, de forma equivalente, `RESET` for usado, o ajuste local da função é removido, de modo que a função execute com o valor presente em seu ambiente. Use `RESET ALL` para limpar todos os ajustes locais da função. `SET FROM CURRENT` salva o valor do parâmetro que é atual quando `ALTER FUNCTION` é executado como o valor a ser aplicado quando a função é inserida.

Veja [SET](sql-set.md "SET") e [Capítulo 19](runtime-config.md "Chapter 19. Server Configuration") para mais informações sobre os nomes e valores permitidos dos parâmetros.

`RESTRICT`: Ignorado para conformidade com o padrão SQL.

## Exemplos

Para renomear a função `sqrt` para o tipo `integer` para `square_root`:

```
ALTER FUNCTION sqrt(integer) RENAME TO square_root;
```

Para alterar o proprietário da função `sqrt` para o tipo `integer` para `joe`:

```
ALTER FUNCTION sqrt(integer) OWNER TO joe;
```

Para alterar o esquema da função `sqrt` para o tipo `integer` para `maths`:

```
ALTER FUNCTION sqrt(integer) SET SCHEMA maths;
```

Para marcar a função `sqrt` para o tipo `integer` como dependente da extensão `mathlib`:

```
ALTER FUNCTION sqrt(integer) DEPENDS ON EXTENSION mathlib;
```

Para ajustar o caminho de busca que é definido automaticamente para uma função:

```
ALTER FUNCTION check_password(text) SET search_path = admin, pg_temp;
```

Para desativar a configuração automática de `search_path` para uma função:

```
ALTER FUNCTION check_password(text) RESET search_path;
```

A função agora será executada com o caminho de busca usado pelo seu chamador.

## Compatibilidade

Essa declaração é parcialmente compatível com a declaração `ALTER FUNCTION` no padrão SQL. O padrão permite que mais propriedades de uma função sejam modificadas, mas não fornece a capacidade de renomear uma função, tornar uma função um definidor de segurança, anexar valores de parâmetros de configuração a uma função ou alterar o proprietário, o esquema ou a volatilidade de uma função. O padrão também exige a palavra-chave `RESTRICT`, que é opcional no PostgreSQL.

## Veja também

[Crie função](sql-createfunction.md "CREATE FUNCTION"), [Exclua função](sql-dropfunction.md "DROP FUNCTION"), [Altere procedimento](sql-alterprocedure.md "ALTER PROCEDURE"), [Altere rotina](sql-alterroutine.md "ALTER ROUTINE")