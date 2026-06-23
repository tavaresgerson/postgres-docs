## ALTER TABLESPACE

ALTER TABLESPACE — alterar a definição de um tablespace

## Sinopse

```
ALTER TABLESPACE name RENAME TO new_name
ALTER TABLESPACE name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER TABLESPACE name SET ( tablespace_option = value [, ... ] )
ALTER TABLESPACE name RESET ( tablespace_option [, ... ] )
```

## Descrição

`ALTER TABLESPACE` pode ser usado para alterar a definição de um tablespace.

Você deve possuir o tablespace para alterar a definição de um tablespace. Para alterar o proprietário, você também deve ser capaz de `SET ROLE` para o novo papel de proprietário. (Observe que os superusuários têm esses privilégios automaticamente.)

## Parâmetros

*`name`*: O nome de um espaço de tabela existente.

*`new_name`*: O novo nome do tablespace. O novo nome não pode começar com `pg_`, pois tais nomes são reservados para tablespaces de tabelas do sistema.

*`new_owner`*: O novo proprietário do espaço de tabelas.

*`tablespace_option`*: Um parâmetro de espaço de tabelas a ser definido ou redefinido. Atualmente, os únicos parâmetros disponíveis são `seq_page_cost`, `random_page_cost`, `effective_io_concurrency` e `maintenance_io_concurrency`. Definir esses valores para um espaço de tabelas específico substituirá a estimativa usual do planejador do custo de leitura de páginas de tabelas nesse espaço de tabelas, e quantas operações de E/S concorrentes são emitidas, conforme estabelecido pelos parâmetros de configuração do mesmo nome (consulte [seq_page_cost](runtime-config-query.md#GUC-SEQ-PAGE-COST), [random_page_cost](runtime-config-query.md#GUC-RANDOM-PAGE-COST), [effective_io_concurrency](runtime-config-resource.md#GUC-EFFECTIVE-IO-CONCURRENCY), [maintenance_io_concurrency](runtime-config-resource.md#GUC-MAINTENANCE-IO-CONCURRENCY)). Isso pode ser útil se um espaço de tabelas estiver localizado em um disco que é mais rápido ou mais lento que o restante do subsistema de E/S.

## Exemplos

Renomeie o tablespace `index_space` para `fast_raid`:

```
ALTER TABLESPACE index_space RENAME TO fast_raid;
```

Altere o proprietário do espaço de tabela `index_space`:

```
ALTER TABLESPACE index_space OWNER TO mary;
```

## Compatibilidade

Não há nenhuma declaração `ALTER TABLESPACE` no padrão SQL.

## Veja também

[CREATE TABLESPACE](sql-createtablespace.md "CREATE TABLESPACE"), [DROP TABLESPACE](sql-droptablespace.md "DROP TABLESPACE")