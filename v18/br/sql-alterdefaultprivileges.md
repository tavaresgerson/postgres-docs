ALTERAR PRIVILEGIOS PREDEFINIDOS

ALTERAR PRIVILEGIOS PREDEFINIDOS — definir privilégios de acesso predefinidos

## Sinopse

```
ALTER DEFAULT PRIVILEGES
    [ FOR { ROLE | USER } target_role [, ...] ]
    [ IN SCHEMA schema_name [, ...] ]
    abbreviated_grant_or_revoke

where abbreviated_grant_or_revoke is one of:

GRANT { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER | MAINTAIN }
    [, ...] | ALL [ PRIVILEGES ] }
    ON TABLES
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]

GRANT { { USAGE | SELECT | UPDATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON SEQUENCES
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]

GRANT { EXECUTE | ALL [ PRIVILEGES ] }
    ON { FUNCTIONS | ROUTINES }
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON TYPES
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]

GRANT { { USAGE | CREATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON SCHEMAS
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]

GRANT { { SELECT | UPDATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON LARGE OBJECTS
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]

REVOKE [ GRANT OPTION FOR ]
    { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER | MAINTAIN }
    [, ...] | ALL [ PRIVILEGES ] }
    ON TABLES
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { USAGE | SELECT | UPDATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON SEQUENCES
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { EXECUTE | ALL [ PRIVILEGES ] }
    ON { FUNCTIONS | ROUTINES }
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON TYPES
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { USAGE | CREATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON SCHEMAS
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { SELECT | UPDATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON LARGE OBJECTS
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]
```

## Descrição

`ALTER DEFAULT PRIVILEGES` permite definir os privilégios que serão aplicados a objetos criados no futuro. (Não afeta os privilégios atribuídos a objetos já existentes.) Os privilégios podem ser definidos globalmente (ou seja, para todos os objetos criados no banco de dados atual), ou apenas para objetos criados em esquemas especificados.

Embora você possa alterar seus próprios privilégios padrão e os padrões dos papéis dos quais é membro, no momento da criação do objeto, as novas permissões do objeto são afetadas apenas pelos privilégios padrão do papel atual e não são herdadas de quaisquer papéis nos quais o papel atual é membro.

Como explicado na [Seção 5.8][(ddl-priv.md "5.8. Privileges")], os privilégios padrão para qualquer tipo de objeto normalmente concedem todos os permissões concedíveis ao proprietário do objeto e podem conceder alguns privilégios ao `PUBLIC` também. No entanto, esse comportamento pode ser alterado alterando os privilégios padrão globais com `ALTER DEFAULT PRIVILEGES`.

Atualmente, apenas os privilégios para esquemas, tabelas (incluindo vistas e tabelas externas), sequências, funções, tipos (incluindo domínios) e grandes objetos podem ser alterados. Para este comando, as funções incluem agregados e procedimentos. As palavras `FUNCTIONS` e `ROUTINES` são equivalentes neste comando. (`ROUTINES` é preferido a partir de agora como o termo padrão para funções e procedimentos tomados juntos. Em versões anteriores do PostgreSQL, apenas a palavra `FUNCTIONS` era permitida. Não é possível definir privilégios padrão para funções e procedimentos separadamente.)

Os privilégios padrão especificados por esquema são adicionados a qualquer privilégio padrão global que o tipo de objeto específico tenha. Isso significa que você não pode revogar privilégios por esquema se eles forem concedidos globalmente (de forma padrão ou de acordo com um comando anterior `ALTER DEFAULT PRIVILEGES` que não especificou um esquema). O `REVOKE` por esquema é útil apenas para reverter os efeitos de um `GRANT` anterior por esquema.

### Parâmetros

*`target_role`*: Altere os privilégios padrão para objetos criados pelo *`target_role`*, ou o papel atual, se não especificado.

*`schema_name`*: O nome de um esquema existente. Se especificado, os privilégios padrão são alterados para objetos posteriormente criados nesse esquema. Se `IN SCHEMA` for omitido, os privilégios padrão globais são alterados. `IN SCHEMA` não é permitido ao definir privilégios para esquemas e grandes objetos, uma vez que os esquemas não podem ser aninhados e os grandes objetos não pertencem a um esquema.

*`role_name`*: O nome de um papel existente para conceder ou revogar privilégios. Este parâmetro, e todos os outros parâmetros em *`abbreviated_grant_or_revoke`*, atuam conforme descrito em [GRANT](sql-grant.md "GRANT") ou [REVOKE](sql-revoke.md "REVOKE"), exceto que um está definindo permissões para uma classe inteira de objetos em vez de objetos específicos com nomes específicos.

## Notas

Utilize o comando (app-psql.md "psql") de [psql][(app-psql.md "psql")] para obter informações sobre as atribuições de privilégios padrão existentes. O significado da exibição de privilégios é o mesmo explicado para `\dp` em [Seção 5.8][(ddl-priv.md "5.8. Privileges")].

Se você deseja excluir um papel para o qual os privilégios padrão foram alterados, é necessário reverter as alterações nos seus privilégios padrão ou usar `DROP OWNED BY` para se livrar da entrada de privilégios padrão para o papel.

## Exemplos

Concede privilégio SELECT a todos para todas as tabelas (e visualizações) que você criar posteriormente no esquema `myschema`, e permita que o papel `webuser` também faça INSERT nelas:

```
ALTER DEFAULT PRIVILEGES IN SCHEMA myschema GRANT SELECT ON TABLES TO PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA myschema GRANT INSERT ON TABLES TO webuser;
```

Desfaça o que foi feito acima, para que as tabelas criadas posteriormente não tenham mais permissões do que o normal:

```
ALTER DEFAULT PRIVILEGES IN SCHEMA myschema REVOKE SELECT ON TABLES FROM PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA myschema REVOKE INSERT ON TABLES FROM webuser;
```

Remova a permissão EXECUTE pública que é normalmente concedida em funções, para todas as funções posteriormente criadas pelo papel `admin`:

```
ALTER DEFAULT PRIVILEGES FOR ROLE admin REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
```

Observe, no entanto, que você *não* pode alcançar esse efeito com um comando limitado a um único esquema. Esse comando não tem efeito, a menos que esteja desfazendo uma correspondência com `GRANT`:

```
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
```

Isso ocorre porque os privilégios padrão por esquema só podem adicionar privilégios ao ajuste global, não remover privilégios concedidos por ele.

## Compatibilidade

Não há nenhuma declaração `ALTER DEFAULT PRIVILEGES` no padrão SQL.

## Veja também

[PRESTAÇÃO][(sql-grant.md "GRANT"), [REVOGA][(sql-revoke.md "REVOKE")