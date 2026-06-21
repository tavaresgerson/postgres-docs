## Crie um grupo

CREATE GROUP — definir um novo papel de banco de dados

## Sinopse

```
CREATE GROUP name [ [ WITH ] option [ ... ] ]

where option can be:

      SUPERUSER | NOSUPERUSER
    | CREATEDB | NOCREATEDB
    | CREATEROLE | NOCREATEROLE
    | INHERIT | NOINHERIT
    | LOGIN | NOLOGIN
    | REPLICATION | NOREPLICATION
    | BYPASSRLS | NOBYPASSRLS
    | CONNECTION LIMIT connlimit
    | [ ENCRYPTED ] PASSWORD 'password' | PASSWORD NULL
    | VALID UNTIL 'timestamp'
    | IN ROLE role_name [, ...]
    | IN GROUP role_name [, ...]
    | ROLE role_name [, ...]
    | ADMIN role_name [, ...]
    | USER role_name [, ...]
    | SYSID uid
```

## Descrição

`CREATE GROUP` é agora um alias para [CREATE ROLE](sql-createrole.md "CREATE ROLE").

## Compatibilidade

Não há nenhuma declaração `CREATE GROUP` no padrão SQL.

## Veja também

[Crie um papel](sql-createrole.md "CREATE ROLE")