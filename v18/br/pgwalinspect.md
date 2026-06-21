## F.37. pg_walinspect — inspeção de WAL de nível baixo [#](#PGWALINSPECT)

* [F.37.1. Funções Gerais](pgwalinspect.md#PGWALINSPECT-FUNCS)
* [F.37.2. Autor](pgwalinspect.md#PGWALINSPECT-AUTHOR)

O módulo `pg_walinspect` fornece funções SQL que permitem inspecionar o conteúdo do log de pré-escrita de um clúster de banco de dados PostgreSQL em funcionamento, em um nível baixo, o que é útil para fins de depuração, analítica, relatórios ou educacionais. É semelhante ao [pg_waldump](pgwaldump.md), mas acessível por meio de SQL em vez de uma ferramenta separada.

Todas as funções deste módulo fornecerão as informações do WAL usando o ID atual da linha de tempo do servidor.

### Nota

As funções `pg_walinspect` são frequentemente chamadas usando um argumento LSN que especifica a localização em que um registro WAL conhecido de interesse *começa*. No entanto, algumas funções, como `pg_logical_emit_message`, retornam o LSN *após* o registro que foi inserido.

### DICA

Todas as funções do `pg_walinspect` que mostram informações sobre registros que estão dentro de um determinado intervalo de LSN são permissivas em relação ao recebimento de argumentos *`end_lsn`* que estão após o LSN atual do servidor. Usar um *`end_lsn`* “do futuro” não causará um erro.

Pode ser conveniente fornecer o valor `FFFFFFFF/FFFFFFFF` (o valor máximo válido `pg_lsn`) como um argumento *`end_lsn`*. Isso é equivalente a fornecer um argumento *`end_lsn`* que corresponda ao LSN atual do servidor.

Por padrão, o uso dessas funções é restrito a superusuários e membros do papel `pg_read_server_files`. O acesso pode ser concedido por superusuários a outros usuários usando `GRANT`.

### F.37.1. Funções Gerais [#](#PGWALINSPECT-FUNCS)

`pg_get_wal_record_info(in_lsn pg_lsn) returns record` [#](#PGWALINSPECT-FUNCS-PG-GET-WAL-RECORD-INFO): Obtém informações de registro WAL sobre um registro que está localizado em ou após o argumento *`in_lsn`*. Por exemplo:

```
postgres=# SELECT * FROM pg_get_wal_record_info('0/E419E28'); -[ RECORD 1 ]----+------------------------------------------------- start_lsn        | 0/E419E28 end_lsn          | 0/E419E68 prev_lsn         | 0/E419D78 xid              | 0 resource_manager | Heap2 record_type      | VACUUM record_length    | 58 main_data_length | 2 fpi_length       | 0 description      | nunused: 5, unused: [1, 2, 3, 4, 5] block_ref        | blkref #0: rel 1663/16385/1249 fork main blk 364
```

Se *`in_lsn`* não estiver no início de um registro WAL, as informações sobre o próximo registro WAL válido são mostradas em vez disso. Se não houver próximo registro WAL válido, a função gera um erro.

`pg_get_wal_records_info(start_lsn pg_lsn, end_lsn pg_lsn) returns setof record` [#](#PGWALINSPECT-FUNCS-PG-GET-WAL-RECORDS-INFO): Obtém informações de todos os registros WAL válidos entre *`start_lsn`* e *`end_lsn`*. Retorna uma linha por registro WAL. Por exemplo:

```
postgres=# SELECT * FROM pg_get_wal_records_info('0/1E913618', '0/1E913740') LIMIT 1; -[ RECORD 1 ]----+-------------------------------------------------------------- start_lsn        | 0/1E913618 end_lsn          | 0/1E913650 prev_lsn         | 0/1E9135A0 xid              | 0 resource_manager | Standby record_type      | RUNNING_XACTS record_length    | 50 main_data_length | 24 fpi_length       | 0 description      | nextXid 33775 latestCompletedXid 33774 oldestRunningXid 33775 block_ref        |
```

A função gera um erro se *`start_lsn`* não estiver disponível.

`pg_get_wal_block_info(start_lsn pg_lsn, end_lsn pg_lsn, show_data boolean DEFAULT true) returns setof record` [#](#PGWALINSPECT-FUNCS-PG-GET-WAL-BLOCK-INFO): Obtém informações sobre cada referência de bloco de todos os registros válidos WAL entre *`start_lsn`* e *`end_lsn`* com uma ou mais referências de bloco. Retorna uma linha por referência de bloco por registro WAL. Por exemplo:

```
postgres=# SELECT * FROM pg_get_wal_block_info('0/1230278', '0/12302B8'); -[ RECORD 1 ]-----+----------------------------------- start_lsn         | 0/1230278 end_lsn           | 0/12302B8 prev_lsn          | 0/122FD40 block_id          | 0 reltablespace     | 1663 reldatabase       | 1 relfilenode       | 2658 relforknumber     | 0 relblocknumber    | 11 xid               | 341 resource_manager  | Btree record_type       | INSERT_LEAF record_length     | 64 main_data_length  | 2 block_data_length | 16 block_fpi_length  | 0 block_fpi_info    | description       | off: 46 block_data        | \x00002a00070010402630000070696400 block_fpi_data    |
```

Este exemplo envolve um registro WAL que contém apenas uma referência a um bloco, mas muitos registros WAL contêm várias referências a blocos. As linhas geradas por `pg_get_wal_block_info` são garantidas a ter uma combinação única de *`start_lsn`* e *`block_id`*.

Muita das informações exibidas aqui correspondem à saída que `pg_get_wal_records_info` mostraria, dado os mesmos argumentos. No entanto, `pg_get_wal_block_info` transforma as informações de cada registro WAL em uma forma expandida, exibindo uma linha por referência de bloco, de modo que certos detalhes sejam rastreados no nível da referência de bloco, e não no nível do registro inteiro. Essa estrutura é útil em consultas que rastreiam como os blocos individuais mudaram ao longo do tempo. Observe que os registros sem referências de bloco (por exemplo, `COMMIT` registros WAL) não terão linhas retornadas, de modo que `pg_get_wal_block_info` pode realmente retornar *menos* linhas do que `pg_get_wal_records_info`.

Os parâmetros `reltablespace`, `reldatabase` e `relfilenode` referem-se a [`pg_tablespace`](catalog-pg-tablespace.md "52.56. pg_tablespace").`oid`, [`pg_database`](catalog-pg-database.md "52.15. pg_database").`oid` e [`pg_class`](catalog-pg-class.md "52.11. pg_class").`relfilenode`, respectivamente. O campo `relforknumber` é o número de bifurcação dentro da relação para a referência do bloco; consulte `common/relpath.h` para detalhes.

### DICA

A função `pg_filenode_relation` (consulte a [Tabela 9.103](functions-admin.md#FUNCTIONS-ADMIN-DBLOCATION)) pode ajudá-lo a determinar qual relação foi modificada durante a execução original.

É possível que os clientes evitem a sobrecarga de materialização de dados de bloco. Isso pode tornar a execução da função significativamente mais rápida. Quando *`show_data`* é definido como `false`, os valores de `block_data` e `block_fpi_data` são omitidos (ou seja, os argumentos `block_data` e `block_fpi_data` `OUT` são `NULL` para todas as linhas retornadas). Obviamente, essa otimização é apenas viável em consultas onde os dados de bloco não são realmente necessários.

A função gera um erro se *`start_lsn`* não estiver disponível.

`pg_get_wal_stats(start_lsn pg_lsn, end_lsn pg_lsn, per_record boolean DEFAULT false) returns setof record` [#](#PGWALINSPECT-FUNCS-PG-GET-WAL-STATS): Obtém estatísticas de todos os registros válidos do WAL entre *`start_lsn`* e *`end_lsn`*. Por padrão, ele retorna uma linha por *`resource_manager`*. Quando *`per_record`* é definido como `true`, ele retorna uma linha por *`record_type`*. Por exemplo:

```
postgres=# SELECT * FROM pg_get_wal_stats('0/1E847D00', '0/1E84F500') WHERE count > 0 AND "resource_manager/record_type" = 'Transaction' LIMIT 1; -[ RECORD 1 ]----------------+------------------- resource_manager/record_type | Transaction count                        | 2 count_percentage             | 8 record_size                  | 875 record_size_percentage       | 41.23468426013195 fpi_size                     | 0 fpi_size_percentage          | 0 combined_size                | 875 combined_size_percentage     | 2.8634072910530795
```

A função gera um erro se *`start_lsn`* não estiver disponível.

### F.37.2. Autor [#](#PGWALINSPECT-AUTHOR)

Bharath Rupireddy `<bharath.rupireddyforpostgres@gmail.com>`