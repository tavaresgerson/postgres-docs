## ATTRIBUTE DESCRIÇÃO

ALLOCATE DESCRIPTOR — alocar uma área de descritor SQL

## Sinopse

```
ALLOCATE DESCRIPTOR name
```

## Descrição

`ALLOCATE DESCRIPTOR` aloca uma nova área de descritor SQL com nome, que pode ser usada para trocar dados entre o servidor PostgreSQL e o programa hospedeiro.

As áreas de descriptografia devem ser liberadas após o uso usando o comando `DEALLOCATE DESCRIPTOR`.

## Parâmetros

*`name`* [#](#ECPG-SQL-ALLOCATE-DESCRIPTOR-NAME): Um nome de descritor SQL, sensível a maiúsculas e minúsculas. Pode ser um identificador SQL ou uma variável de host.

## Exemplos

```
EXEC SQL ALLOCATE DESCRIPTOR mydesc;
```

## Compatibilidade

`ALLOCATE DESCRIPTOR` é especificado no padrão SQL.

## Veja também

[DESALLOCITAR DESCRIADOR](ecpg-sql-deallocate-descriptor.md "DEALLOCATE DESCRIPTOR"), [OBTER DESCRIADOR](ecpg-sql-get-descriptor.md "GET DESCRIPTOR"), [DEFINIR DESCRIADOR](ecpg-sql-set-descriptor.md "SET DESCRIPTOR")