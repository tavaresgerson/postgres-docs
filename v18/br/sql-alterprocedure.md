## ALTER PROCEDURE

ALTER PROCEDURE — alterar a definição de um procedimento

## Sinopse

```
ALTER PROCEDURE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    action [ ... ] [ RESTRICT ]
ALTER PROCEDURE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    RENAME TO new_name
ALTER PROCEDURE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER PROCEDURE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    SET SCHEMA new_schema
ALTER PROCEDURE name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ]
    [ NO ] DEPENDS ON EXTENSION extension_name

where action is one of:

    [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER
    SET configuration_parameter { TO | = } { value | DEFAULT }
    SET configuration_parameter FROM CURRENT
    RESET configuration_parameter
    RESET ALL
```

## Descrição

`ALTER PROCEDURE` altera a definição de um procedimento.

Você deve possuir o procedimento para usar `ALTER PROCEDURE`. Para alterar o esquema de um procedimento, você também deve ter privilégio `CREATE` no novo esquema. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário, e esse papel deve ter privilégio `CREATE` no esquema do procedimento. (Essas restrições garantem que alterar o proprietário não faz nada que você não poderia fazer ao descartar e recriar o procedimento. No entanto, um superusuário pode alterar a propriedade de qualquer procedimento de qualquer maneira.)

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de um procedimento existente. Se não for especificada uma lista de argumentos, o nome deve ser único em seu esquema.

*`argmode`*: O modo de um argumento: `IN`, `OUT`, `INOUT` ou `VARIADIC`. Se omitido, o padrão é `IN`.

*`argname`*: O nome de um argumento. Observe que `ALTER PROCEDURE` não presta atenção na verdade aos nomes dos argumentos, uma vez que apenas os tipos de dados dos argumentos são usados para determinar a identidade do procedimento.

*`argtype`*: O(s) tipo(s) de dados dos argumentos do procedimento (opcionalmente qualificados por esquema), se houver. Consulte [DROP PROCEDURE](sql-dropprocedure.md "DROP PROCEDURE") para obter detalhes sobre como o procedimento é pesquisado usando o(s) tipo(s) de dados dos argumentos.

*`new_name`*: O novo nome do procedimento.

*`new_owner`*: O novo proprietário do procedimento. Observe que, se o procedimento estiver marcado `SECURITY DEFINER`, ele será executado posteriormente como o novo proprietário.

*`new_schema`*: O novo esquema para o procedimento.

*`extension_name`*: Este formulário marca o procedimento como dependente da extensão, ou não mais dependente da extensão se `NO` for especificado. Um procedimento marcado como dependente de uma extensão é descartado quando a extensão é descartada, mesmo que a cascata não seja especificada. Um procedimento pode depender de múltiplas extensões e será descartado quando qualquer uma dessas extensões for descartada.

`[ EXTERNAL ] SECURITY INVOKER` `[ EXTERNAL ] SECURITY DEFINER`: Altere se o procedimento é um definidor de segurança ou não. A palavra-chave `EXTERNAL` é ignorada para conformidade com SQL. Consulte [CREATE PROCEDURE](sql-createprocedure.md "CREATE PROCEDURE") para obter mais informações sobre essa capacidade.

*`configuration_parameter`* *`value`*: Adicione ou altere a atribuição a ser feita a um parâmetro de configuração quando o procedimento é chamado. Se *`value`* for `DEFAULT` ou, de forma equivalente, `RESET` for usado, a configuração local do procedimento é removida, de modo que o procedimento execute com o valor presente em seu ambiente. Use `RESET ALL` para limpar todas as configurações locais do procedimento. `SET FROM CURRENT` salva o valor do parâmetro que é atual quando `ALTER PROCEDURE` é executado como o valor a ser aplicado quando o procedimento é iniciado.

Consulte [SET](sql-set.md "SET") e [Capítulo 19](runtime-config.md "Chapter 19. Server Configuration") para obter mais informações sobre os nomes e valores permitidos dos parâmetros.

`RESTRICT`: Ignorado para conformidade com o padrão SQL.

## Exemplos

Para renomear o procedimento `insert_data` com dois argumentos do tipo `integer` para `insert_record`:

```
ALTER PROCEDURE insert_data(integer, integer) RENAME TO insert_record;
```

Para alterar o proprietário do procedimento `insert_data` com dois argumentos do tipo `integer` para `joe`:

```
ALTER PROCEDURE insert_data(integer, integer) OWNER TO joe;
```

Para alterar o esquema do procedimento `insert_data` com dois argumentos do tipo `integer` para `accounting`:

```
ALTER PROCEDURE insert_data(integer, integer) SET SCHEMA accounting;
```

Para marcar o procedimento `insert_data(integer, integer)` como dependente da extensão `myext`:

```
ALTER PROCEDURE insert_data(integer, integer) DEPENDS ON EXTENSION myext;
```

Para ajustar o caminho de busca que é definido automaticamente para um procedimento:

```
ALTER PROCEDURE check_password(text) SET search_path = admin, pg_temp;
```

Para desativar a configuração automática de `search_path` para um procedimento:

```
ALTER PROCEDURE check_password(text) RESET search_path;
```

O procedimento agora será executado com o caminho de busca usado pelo seu chamador.

## Compatibilidade

Essa declaração é parcialmente compatível com a declaração `ALTER PROCEDURE` no padrão SQL. O padrão permite que mais propriedades de um procedimento sejam modificadas, mas não fornece a capacidade de renomear um procedimento, tornar um procedimento um definidor de segurança, anexar valores de parâmetros de configuração a um procedimento ou alterar o proprietário, o esquema ou a volatilidade de um procedimento. O padrão também exige a palavra-chave `RESTRICT`, que é opcional no PostgreSQL.

## Veja também

[Crie procedimento](sql-createprocedure.md "CREATE PROCEDURE"), [Retire procedimento](sql-dropprocedure.md "DROP PROCEDURE"), [Altere função](sql-alterfunction.md "ALTER FUNCTION"), [Altere rotina](sql-alterroutine.md "ALTER ROUTINE")