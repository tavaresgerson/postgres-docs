## Crie Usuário

Crie usuário — defina um novo papel de banco de dados

## Sinopse

```
CREATE USER name [ [ WITH ] option [ ... ] ]

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

`CREATE USER` é agora um alias para [`CREATE ROLE`](sql-createrole.md "CREATE ROLE"). A única diferença é que, quando o comando é escrito como `CREATE USER`, `LOGIN` é assumido por padrão, enquanto `NOLOGIN` é assumido quando o comando é escrito como `CREATE ROLE`.

## Compatibilidade

A declaração `CREATE USER` é uma extensão do PostgreSQL. O padrão SQL deixa a definição de usuários para a implementação.

## Veja também

[Crie um papel](sql-createrole.md "CREATE ROLE")