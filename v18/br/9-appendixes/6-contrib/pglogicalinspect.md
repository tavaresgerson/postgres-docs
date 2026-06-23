## F.28. pg_logicalinspect — inspeção de componentes de decodificação lógica [#](#PGLOGICALINSPECT)

* [F.28.1. Funções](pglogicalinspect.md#PGLOGICALINSPECT-FUNCS)
* [F.28.2. Autor](pglogicalinspect.md#PGLOGICALINSPECT-AUTHOR)

O módulo `pg_logicalinspect` fornece funções SQL que permitem inspecionar o conteúdo de componentes de decodificação lógica. Permite a inspeção de instantâneos lógicos serializados de um clúster de banco de dados PostgreSQL em execução, o que é útil para fins de depuração ou educacionais.

Por padrão, o uso dessas funções é restrito a superusuários e membros do papel `pg_read_server_files`. O acesso pode ser concedido por superusuários a outros usuários que utilizam `GRANT`.

### F.28.1. Funções [#](#PGLOGICALINSPECT-FUNCS)

`pg_get_logical_snapshot_meta(filename text) returns record` [#](#PGLOGICALINSPECT-FUNCS-PG-GET-LOGICAL-SNAPSHOT-META): Obtém metadados lógicos de instantâneo sobre um arquivo de instantâneo que está localizado no diretório `pg_logical/snapshots` do servidor. O argumento *`filename`* representa o nome do arquivo de instantâneo. Por exemplo:

```
postgres=# SELECT * FROM pg_ls_logicalsnapdir(); -[ RECORD 1 ]+----------------------- name         | 0-40796E18.snap size         | 152 modification | 2024-08-14 16:36:32+00

postgres=# SELECT * FROM pg_get_logical_snapshot_meta('0-40796E18.snap'); -[ RECORD 1 ]-------- magic    | 1369563137 checksum | 1028045905 version  | 6

postgres=# SELECT ss.name, meta.* FROM pg_ls_logicalsnapdir() AS ss, pg_get_logical_snapshot_meta(ss.name) AS meta; -[ RECORD 1 ]------------- name     | 0-40796E18.snap magic    | 1369563137 checksum | 1028045905 version  | 6
```

Se *`filename`* não corresponder a um arquivo de instantâneo, a função gera um erro.

`pg_get_logical_snapshot_info(filename text) returns record` [#](#PGLOGICALINSPECT-FUNCS-PG-GET-LOGICAL-SNAPSHOT-INFO): Obtém informações lógicas de instantâneo sobre um arquivo de instantâneo que está localizado no diretório `pg_logical/snapshots` do servidor. O argumento *`filename`* representa o nome do arquivo de instantâneo. Por exemplo:

```
postgres=# SELECT * FROM pg_ls_logicalsnapdir(); -[ RECORD 1 ]+----------------------- name         | 0-40796E18.snap size         | 152 modification | 2024-08-14 16:36:32+00

postgres=# SELECT * FROM pg_get_logical_snapshot_info('0-40796E18.snap'); -[ RECORD 1 ]------------+----------- state                    | consistent xmin                     | 751 xmax                     | 751 start_decoding_at        | 0/40796AF8 two_phase_at             | 0/40796AF8 initial_xmin_horizon     | 0 building_full_snapshot   | f in_slot_creation         | f last_serialized_snapshot | 0/0 next_phase_at            | 0 committed_count          | 0 committed_xip            | catchange_count          | 2 catchange_xip            | {751,752}

postgres=# SELECT ss.name, info.* FROM pg_ls_logicalsnapdir() AS ss, pg_get_logical_snapshot_info(ss.name) AS info; -[ RECORD 1 ]------------+---------------- name                     | 0-40796E18.snap state                    | consistent xmin                     | 751 xmax                     | 751 start_decoding_at        | 0/40796AF8 two_phase_at             | 0/40796AF8 initial_xmin_horizon     | 0 building_full_snapshot   | f in_slot_creation         | f last_serialized_snapshot | 0/0 next_phase_at            | 0 committed_count          | 0 committed_xip            | catchange_count          | 2 catchange_xip            | {751,752}
```

Se *`filename`* não corresponder a um arquivo de instantâneo, a função gera um erro.

### F.28.2. Autor [#](#PGLOGICALINSPECT-AUTHOR)

Bertrand Drouvot `<bertranddrouvot.pg@gmail.com>`