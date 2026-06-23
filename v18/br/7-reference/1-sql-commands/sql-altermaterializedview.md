## ALTERAR VISUAL MATERIALIZADO

ALTERAR VISTO MATERIALIZADO — alterar a definição de um visto materializado

## Sinopse

```
ALTER MATERIALIZED VIEW [ IF EXISTS ] name
    action [, ... ]
ALTER MATERIALIZED VIEW name
    [ NO ] DEPENDS ON EXTENSION extension_name
ALTER MATERIALIZED VIEW [ IF EXISTS ] name
    RENAME [ COLUMN ] column_name TO new_column_name
ALTER MATERIALIZED VIEW [ IF EXISTS ] name
    RENAME TO new_name
ALTER MATERIALIZED VIEW [ IF EXISTS ] name
    SET SCHEMA new_schema
ALTER MATERIALIZED VIEW ALL IN TABLESPACE name [ OWNED BY role_name [, ... ] ]
    SET TABLESPACE new_tablespace [ NOWAIT ]

where action is one of:

    ALTER [ COLUMN ] column_name SET STATISTICS integer
    ALTER [ COLUMN ] column_name SET ( attribute_option = value [, ... ] )
    ALTER [ COLUMN ] column_name RESET ( attribute_option [, ... ] )
    ALTER [ COLUMN ] column_name SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT }
    ALTER [ COLUMN ] column_name SET COMPRESSION compression_method
    CLUSTER ON index_name
    SET WITHOUT CLUSTER
    SET ACCESS METHOD new_access_method
    SET TABLESPACE new_tablespace
    SET ( storage_parameter [= value] [, ... ] )
    RESET ( storage_parameter [, ... ] )
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
```

## Descrição

`ALTER MATERIALIZED VIEW` altera várias propriedades auxiliares de uma visão materializada existente.

Você deve possuir a visão materializada para usar `ALTER MATERIALIZED VIEW`. Para alterar o esquema de uma visão materializada, você também deve ter o privilégio `CREATE` no novo esquema. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel proprietário, e esse papel deve ter o privilégio `CREATE` no esquema da visão materializada. (Essas restrições garantem que alterar o proprietário não faz nada que você não poderia fazer ao descartar e recriar a visão materializada. No entanto, um superusuário pode alterar a propriedade de qualquer visão de qualquer maneira.)

Os subformularios e ações disponíveis para `ALTER MATERIALIZED VIEW` são um subconjunto dos disponíveis para `ALTER TABLE`, e têm o mesmo significado quando utilizados para visualizações materializadas. Consulte as descrições para [`ALTER TABLE`](sql-altertable.md "ALTER TABLE") para obter detalhes.

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de uma visão materializada existente.

*`column_name`*: Nome de uma coluna existente.

*`extension_name`*: O nome da extensão da qual a visão materializada deve depender (ou que não deve mais depender, se `NO` for especificado). Uma visão materializada marcada como dependente de uma extensão é automaticamente descartada quando a extensão é descartada.

*`new_column_name`*: Novo nome para uma coluna existente.

*`new_owner`*: O nome do usuário do novo proprietário da visão materializada.

*`new_name`*: O novo nome para a visão materializada.

*`new_schema`*: O novo esquema para a visão materializada.

## Exemplos

Para renomear a visualização materializada `foo` para `bar`:

```
ALTER MATERIALIZED VIEW foo RENAME TO bar;
```

## Compatibilidade

`ALTER MATERIALIZED VIEW` é uma extensão do PostgreSQL.

## Veja também

[Crie uma visualização materializada](sql-creatematerializedview.md "CREATE MATERIALIZED VIEW"), [Remova uma visualização materializada](sql-dropmaterializedview.md "DROP MATERIALIZED VIEW"), [Atualize uma visualização materializada](sql-refreshmaterializedview.md "REFRESH MATERIALIZED VIEW")