## F.32. pg_stat_statements — acompanhe estatísticas de planejamento e execução de SQL [#](#PGSTATSTATEMENTS)

* [F.32.1. A Visão do `pg_stat_statements`](pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS)
* [F.32.2. A Visão do `pg_stat_statements_info`](pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS-INFO)
* [F.32.3. Funções](pgstatstatements.md#PGSTATSTATEMENTS-FUNCS)
* [F.32.4. Parâmetros de Configuração](pgstatstatements.md#PGSTATSTATEMENTS-CONFIG-PARAMS)
* [F.32.5. Saída de Amostra](pgstatstatements.md#PGSTATSTATEMENTS-SAMPLE-OUTPUT)
* [F.32.6. Autores](pgstatstatements.md#PGSTATSTATEMENTS-AUTHORS)

O módulo `pg_stat_statements` fornece uma maneira de acompanhar as estatísticas de planejamento e execução de todas as declarações SQL executadas por um servidor.

O módulo deve ser carregado adicionando `pg_stat_statements` a [shared_preload_libraries](runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) em `postgresql.conf`, porque ele requer memória compartilhada adicional. Isso significa que é necessário reiniciar o servidor para adicionar ou remover o módulo. Além disso, o cálculo do identificador da consulta deve ser habilitado para que o módulo seja ativo, o que é feito automaticamente se [compute_query_id](runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID) estiver definido como `auto` ou `on`, ou qualquer módulo de terceiros que calcule identificadores de consulta seja carregado.

Quando o `pg_stat_statements` está ativo, ele rastreia estatísticas em todos os bancos de dados do servidor. Para acessar e manipular essas estatísticas, o módulo fornece as visualizações `pg_stat_statements` e `pg_stat_statements_info`, e as funções utilitárias `pg_stat_statements_reset` e `pg_stat_statements`. Essas não estão disponíveis globalmente, mas podem ser habilitadas para um banco de dados específico com `CREATE EXTENSION pg_stat_statements`.

### F.32.1. A `pg_stat_statements` [#](#PGSTATSTATEMENTS-PG-STAT-STATEMENTS)

As estatísticas coletadas pelo módulo são disponibilizadas por meio de uma visualização denominada `pg_stat_statements`. Essa visualização contém uma linha para cada combinação distinta de ID do banco de dados, ID do usuário, ID da consulta e se é uma declaração de nível superior ou não (até o número máximo de declarações distintas que o módulo pode rastrear). As colunas da visualização são mostradas em [Tabela F.22](pgstatstatements.md#PGSTATSTATEMENTS-COLUMNS).

**Tabela F.22. Colunas `pg_stat_statements`**



<table border="1" class="table" summary="pg_stat_statements Columns">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="catalog_table_entry">
    <p class="column_definition">
     Column Type
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      userid
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code class="structname">
       pg_authid
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     OID of user who executed the statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      dbid
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-database.md" title="52.15. pg_database">
      <code class="structname">
       pg_database
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     OID of database in which the statement was executed
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      toplevel
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     True if the query was executed as a top-level statement (always true if
     <code class="varname">
      pg_stat_statements.track
     </code>
     is set to
     <code class="literal">
      top
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      queryid
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Hash code to identify identical normalized queries.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      query
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Text of a representative statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      plans
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times the statement was planned (if
     <code class="varname">
      pg_stat_statements.track_planning
     </code>
     is enabled, otherwise zero)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      total_plan_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total time spent planning the statement, in milliseconds (if
     <code class="varname">
      pg_stat_statements.track_planning
     </code>
     is enabled, otherwise zero)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      min_plan_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Minimum time spent planning the statement, in milliseconds. This field will be zero if
     <code class="varname">
      pg_stat_statements.track_planning
     </code>
     is disabled, or if the counter has been reset using the
     <code class="function">
      pg_stat_statements_reset
     </code>
     function with the
     <code class="structfield">
      minmax_only
     </code>
     parameter set to
     <code class="literal">
      true
     </code>
     and never been planned since.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      max_plan_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Maximum time spent planning the statement, in milliseconds. This field will be zero if
     <code class="varname">
      pg_stat_statements.track_planning
     </code>
     is disabled, or if the counter has been reset using the
     <code class="function">
      pg_stat_statements_reset
     </code>
     function with the
     <code class="structfield">
      minmax_only
     </code>
     parameter set to
     <code class="literal">
      true
     </code>
     and never been planned since.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      mean_plan_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Mean time spent planning the statement, in milliseconds (if
     <code class="varname">
      pg_stat_statements.track_planning
     </code>
     is enabled, otherwise zero)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      stddev_plan_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Population standard deviation of time spent planning the statement, in milliseconds (if
     <code class="varname">
      pg_stat_statements.track_planning
     </code>
     is enabled, otherwise zero)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      calls
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times the statement was executed
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      total_exec_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total time spent executing the statement, in milliseconds
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      min_exec_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Minimum time spent executing the statement, in milliseconds, this field will be zero until this statement is executed first time after reset performed by the
     <code class="function">
      pg_stat_statements_reset
     </code>
     function with the
     <code class="structfield">
      minmax_only
     </code>
     parameter set to
     <code class="literal">
      true
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      max_exec_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Maximum time spent executing the statement, in milliseconds, this field will be zero until this statement is executed first time after reset performed by the
     <code class="function">
      pg_stat_statements_reset
     </code>
     function with the
     <code class="structfield">
      minmax_only
     </code>
     parameter set to
     <code class="literal">
      true
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      mean_exec_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Mean time spent executing the statement, in milliseconds
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      stddev_exec_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Population standard deviation of time spent executing the statement, in milliseconds
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rows
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of rows retrieved or affected by the statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      shared_blks_hit
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of shared block cache hits by the statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      shared_blks_read
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of shared blocks read by the statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      shared_blks_dirtied
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of shared blocks dirtied by the statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      shared_blks_written
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of shared blocks written by the statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      local_blks_hit
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of local block cache hits by the statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      local_blks_read
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of local blocks read by the statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      local_blks_dirtied
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of local blocks dirtied by the statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      local_blks_written
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of local blocks written by the statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      temp_blks_read
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of temp blocks read by the statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      temp_blks_written
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of temp blocks written by the statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      shared_blk_read_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total time the statement spent reading shared blocks, in milliseconds (if
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-IO-TIMING">
      track_io_timing
     </a>
     is enabled, otherwise zero)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      shared_blk_write_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total time the statement spent writing shared blocks, in milliseconds (if
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-IO-TIMING">
      track_io_timing
     </a>
     is enabled, otherwise zero)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      local_blk_read_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total time the statement spent reading local blocks, in milliseconds (if
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-IO-TIMING">
      track_io_timing
     </a>
     is enabled, otherwise zero)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      local_blk_write_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total time the statement spent writing local blocks, in milliseconds (if
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-IO-TIMING">
      track_io_timing
     </a>
     is enabled, otherwise zero)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      temp_blk_read_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total time the statement spent reading temporary file blocks, in milliseconds (if
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-IO-TIMING">
      track_io_timing
     </a>
     is enabled, otherwise zero)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      temp_blk_write_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total time the statement spent writing temporary file blocks, in milliseconds (if
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-IO-TIMING">
      track_io_timing
     </a>
     is enabled, otherwise zero)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      wal_records
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of WAL records generated by the statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      wal_fpi
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of WAL full page images generated by the statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      wal_bytes
     </code>
     <code class="type">
      numeric
     </code>
    </p>
    <p>
     Total amount of WAL generated by the statement in bytes
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      wal_buffers_full
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times the WAL buffers became full
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      jit_functions
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of functions JIT-compiled by the statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      jit_generation_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total time spent by the statement on generating JIT code, in milliseconds
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      jit_inlining_count
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times functions have been inlined
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      jit_inlining_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total time spent by the statement on inlining functions, in milliseconds
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      jit_optimization_count
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times the statement has been optimized
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      jit_optimization_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total time spent by the statement on optimizing, in milliseconds
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      jit_emission_count
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times code has been emitted
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      jit_emission_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total time spent by the statement on emitting code, in milliseconds
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      jit_deform_count
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of tuple deform functions JIT-compiled by the statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      jit_deform_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total time spent by the statement on JIT-compiling tuple deform functions, in milliseconds
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      parallel_workers_to_launch
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of parallel workers planned to be launched
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      parallel_workers_launched
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of parallel workers actually launched
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      stats_since
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Time at which statistics gathering started for this statement
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      minmax_stats_since
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Time at which min/max statistics gathering started for this statement (fields
     <code class="structfield">
      min_plan_time
     </code>
     ,
     <code class="structfield">
      max_plan_time
     </code>
     ,
     <code class="structfield">
      min_exec_time
     </code>
     and
     <code class="structfield">
      max_exec_time
     </code>
     )
    </p>
   </td>
  </tr>
 </tbody>
</table>










Por razões de segurança, apenas superusuários e papéis com privilégios da função `pg_read_all_stats` têm permissão para ver o texto SQL e as consultas `queryid` executadas por outros usuários. Outros usuários, no entanto, podem ver as estatísticas, desde que a visualização tenha sido instalada em seu banco de dados.

As consultas planejáveis (ou seja, `SELECT`, `INSERT`, `UPDATE`, `DELETE` e `MERGE`) e os comandos de utilidade são combinados em uma única entrada `pg_stat_statements` sempre que tiverem estruturas de consulta idênticas de acordo com um cálculo de hash interno. Tipicamente, duas consultas serão consideradas iguais para este propósito se forem semanticamente equivalentes, exceto pelos valores das constantes literais que aparecem na consulta.

Nota

Os seguintes detalhes sobre substituição constante e `queryid` só se aplicam quando [compute_query_id](runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID) está habilitado. Se você usar um módulo externo em vez disso para calcular `queryid`, você deve consultar a documentação dele para obter detalhes.

Quando o valor de uma constante foi ignorado para fins de correspondência com outras consultas, a constante é substituída por um símbolo de parâmetro, como `$1`, no display `pg_stat_statements`. O restante do texto da consulta é o da primeira consulta que tinha o valor de hash `queryid` específico associado à entrada `pg_stat_statements`.

As consultas nas quais a normalização pode ser aplicada podem ser observadas com valores constantes em `pg_stat_statements`, especialmente quando há uma alta taxa de realocação de entradas. Para reduzir a probabilidade de isso acontecer, considere aumentar `pg_stat_statements.max`. A visualização `pg_stat_statements_info`, discutida abaixo em [Seção F.32.2](pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS-INFO "F.32.2. The pg_stat_statements_info View"), fornece estatísticas sobre a alocação de entradas.

Em alguns casos, consultas com textos visivelmente diferentes podem ser unidas em uma única entrada `pg_stat_statements`; como explicado acima, isso é esperado para consultas semanticamente equivalentes. Além disso, se a única diferença entre as consultas é o número de elementos em uma lista de constantes, a lista será reduzida a um único elemento, mas exibida com um indicador de lista comentado:

```
=# SELECT pg_stat_statements_reset();
=# SELECT * FROM test WHERE a IN (1, 2, 3, 4, 5, 6, 7);
=# SELECT * FROM test WHERE a IN (1, 2, 3, 4, 5, 6, 7, 8);
=# SELECT query, calls FROM pg_stat_statements
   WHERE query LIKE 'SELECT%';
-[ RECORD 1 ]------------------------------
query | SELECT * FROM test WHERE a IN ($1 /*, ... */)
calls | 2
```

Além desses casos, há uma pequena chance de colisões de hash causar a fusão de consultas não relacionadas em uma única entrada. (Isso, no entanto, não pode acontecer para consultas pertencentes a diferentes usuários ou bancos de dados.)

Como o valor de hash `queryid` é calculado na representação de análise pós-parsa das consultas, o oposto também é possível: consultas com textos idênticos podem aparecer como entradas separadas, se tiverem significados diferentes como resultado de fatores, como diferentes configurações de `search_path`.

Os consumidores de `pg_stat_statements` podem desejar usar `queryid` (provavelmente em combinação com `dbid` e `userid`) como um identificador mais estável e confiável para cada entrada do que seu texto de consulta. No entanto, é importante entender que há apenas garantias limitadas em torno da estabilidade do valor do hash `queryid`. Como o identificador é derivado da árvore de análise pós-processamento, seu valor é uma função, entre outras coisas, dos identificadores de objeto interno que aparecem nesta representação. Isso tem algumas implicações contraintuitivas. Por exemplo, `pg_stat_statements` considerará duas consultas aparentemente idênticas como distintas, se elas referenciarem, por exemplo, uma função que foi descartada e recriada entre as execuções das duas consultas. Por outro lado, se uma tabela for descartada e recriada entre as execuções das consultas, duas consultas aparentemente idênticas podem ser consideradas iguais. No entanto, se o alias de uma tabela for diferente para consultas de outra forma semelhantes, essas consultas serão consideradas distintas. O processo de hashing também é sensível a diferenças na arquitetura da máquina e outros aspectos da plataforma. Além disso, não é seguro assumir que `queryid` será estável em versões principais do PostgreSQL.

Pode-se esperar que dois servidores que participam da replicação com base em replay físico de WAL tenham valores idênticos de `queryid` para a mesma consulta. No entanto, os esquemas de replicação lógica não prometem manter as réplicas idênticas em todos os detalhes relevantes, portanto, `queryid` não será um identificador útil para acumular custos em um conjunto de réplicas lógicas. Se houver dúvidas, é recomendado realizar testes diretos.

Geralmente, pode-se assumir que os valores de `queryid` são estáveis entre as versões menores do PostgreSQL, desde que as instâncias estejam executando na mesma arquitetura da máquina e os detalhes do metadados do catálogo correspondam. A compatibilidade só será quebrada entre versões menores como último recurso.

Os símbolos de parâmetros usados para substituir constantes em textos de consulta representativos começam a partir do próximo número após o parâmetro `$`*`n`* no texto de consulta original, ou `$1` se não houvesse nenhum. Vale ressaltar que, em alguns casos, podem haver símbolos de parâmetros ocultos que afetam essa numeração. Por exemplo, o PL/pgSQL usa símbolos de parâmetros ocultos para inserir valores de variáveis locais de função em consultas, de modo que uma declaração PL/pgSQL como `SELECT i + 1 INTO j` teria texto representativo como `SELECT i + $2`.

Os textos de consulta representativos são mantidos em um arquivo em disco externo e não consomem memória compartilhada. Portanto, mesmo textos de consulta muito extensos podem ser armazenados com sucesso. No entanto, se muitos textos de consulta longos forem acumulados, o arquivo externo pode crescer de forma incontrolável. Como método de recuperação, se isso acontecer, `pg_stat_statements` pode optar por descartar os textos de consulta, após o que todas as entradas existentes na visão `pg_stat_statements` mostrarão campos `query` nulos, embora as estatísticas associadas a cada `queryid` sejam preservadas. Se isso acontecer, considere reduzir `pg_stat_statements.max` para evitar recorrências.

`plans` e `calls` nem sempre são esperados para corresponder, porque as estatísticas de planejamento e execução são atualizadas em sua respectiva fase final e apenas para operações bem-sucedidas. Por exemplo, se uma declaração é planejada com sucesso, mas falha durante a fase de execução, apenas suas estatísticas de planejamento serão atualizadas. Se o planejamento é ignorado porque um plano armazenado é usado, apenas suas estatísticas de execução serão atualizadas.

### F.32.2. A `pg_stat_statements_info` [#](#PGSTATSTATEMENTS-PG-STAT-STATEMENTS-INFO)

As estatísticas do próprio módulo `pg_stat_statements` são acompanhadas e disponibilizadas por meio de uma visualização denominada `pg_stat_statements_info`. Essa visualização contém apenas uma única linha. As colunas da visualização são mostradas na [Tabela F.23](pgstatstatements.md#PGSTATSTATEMENTSINFO-COLUMNS "Table F.23. pg_stat_statements_info Columns").

**Tabela F.23. `pg_stat_statements_info` Colunas**



<table border="1" class="table" summary="pg_stat_statements_info Columns">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="catalog_table_entry">
    <p class="column_definition">
     Tipo de coluna
    </p>
    <p>
     Descrição
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      dealloc
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número total de vezes
     <code class="structname">
      pg_stat_statements
     </code>
     as entradas sobre as declarações menos executadas foram realocadas porque havia mais declarações distintas do que
     <code class="varname">
      pg_stat_statements.max
     </code>
     foram observados
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      stats_reset
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Tempo em que todas as estatísticas estão
     <code class="structname">
      pg_stat_statements
     </code>
     a vista foi a última a ser redefinida.
    </p>
   </td>
  </tr>
 </tbody>
</table>







### F.32.3. Funções [#](#PGSTATSTATEMENTS-FUNCS)

`pg_stat_statements_reset(userid Oid, dbid Oid, queryid bigint, minmax_only boolean) returns timestamp with time zone`: `pg_stat_statements_reset` descarta as estatísticas coletadas até o momento por `pg_stat_statements` correspondentes ao `userid`, `dbid` e `queryid` especificados. Se algum dos parâmetros não for especificado, o valor padrão `0`(inválido) é usado para cada um deles e as estatísticas que correspondem a outros parâmetros serão redefinidas. Se nenhum parâmetro for especificado ou todos os parâmetros especificados forem `0`(inválidos), ele descartará todas as estatísticas. Se todas as estatísticas na visão `pg_stat_statements` forem descartadas, também redefinirá as estatísticas na visão `pg_stat_statements_info`. Quando `minmax_only` é `true` apenas os valores do tempo mínimo e máximo de planejamento e execução serão redefinidos (ou seja, os campos `min_plan_time`, `max_plan_time`, `min_exec_time` e `max_exec_time`). O valor padrão para o parâmetro `minmax_only` é `false`. O tempo da última redefinição de min/max é mostrado no campo `minmax_stats_since` da visão `pg_stat_statements`. Esta função retorna o tempo de uma redefinição. Este tempo é salvo no campo `stats_reset` da visão `pg_stat_statements_info` ou no campo `minmax_stats_since` da visão `pg_stat_statements` se a redefinição correspondente foi realmente realizada. Por padrão, esta função só pode ser executada por superusuários. O acesso pode ser concedido a outros usuários usando `GRANT`.

`pg_stat_statements(showtext boolean) returns setof record`: A vista `pg_stat_statements` é definida em termos de uma função também denominada `pg_stat_statements`. É possível que os clientes chamem diretamente a função `pg_stat_statements`, e, ao especificar `showtext := false`, que o texto da consulta seja omitido (ou seja, o argumento `OUT` que corresponde à coluna `query` da vista retornará nulos). Esta funcionalidade é destinada a suportar ferramentas externas que possam desejar evitar o esforço de recuperação repetida de textos de consulta de comprimento indeterminado. Tais ferramentas podem, em vez disso, armazenar o primeiro texto de consulta observado para cada entrada por si mesmas, uma vez que é tudo o que a própria `pg_stat_statements` faz, e, em seguida, recuperar textos de consulta apenas conforme necessário. Como o servidor armazena textos de consulta em um arquivo, essa abordagem pode reduzir o I/O físico para exame repetido dos dados `pg_stat_statements`.

### F.32.4. Parâmetros de configuração [#](#PGSTATSTATEMENTS-CONFIG-PARAMS)

`pg_stat_statements.max` (`integer`): `pg_stat_statements.max` é o número máximo de declarações rastreadas pelo módulo (ou seja, o número máximo de linhas na visão `pg_stat_statements`). Se forem observadas mais declarações distintas do que esse número, as informações sobre as declarações menos executadas são descartadas. O número de vezes que essas informações foram descartadas pode ser visto na visão `pg_stat_statements_info`. O valor padrão é 5000. Este parâmetro só pode ser definido no início do servidor.

`pg_stat_statements.track` (`enum`): `pg_stat_statements.track` controla quais declarações são contadas pelo módulo. Especifique `top` para rastrear declarações de nível superior (as emitidas diretamente pelos clientes), `all` para também rastrear declarações aninhadas (como declarações invocadas dentro de funções), ou `none` para desativar a coleta de estatísticas de declarações. O valor padrão é `top`. Somente superusuários podem alterar essa configuração.

`pg_stat_statements.track_utility` (`boolean`): `pg_stat_statements.track_utility` controla se os comandos de utilidade são rastreados pelo módulo. Os comandos de utilidade são todos aqueles que não são `SELECT`, `INSERT`, `UPDATE`, `DELETE` e `MERGE`. O valor padrão é `on`. Somente os superusuários podem alterar essa configuração.

`pg_stat_statements.track_planning` (`boolean`): `pg_stat_statements.track_planning` controla se as operações de planejamento e duração são rastreadas pelo módulo. Habilitar este parâmetro pode resultar em uma penalidade de desempenho perceptível, especialmente quando declarações com estrutura de consulta idêntica são executadas por muitas conexões concorrentes que competem para atualizar um pequeno número de `pg_stat_statements` entradas. O valor padrão é `off`. Somente superusuários podem alterar este ajuste.

`pg_stat_statements.save` (`boolean`): `pg_stat_statements.save` especifica se as estatísticas das declarações devem ser salvas durante as interrupções do servidor. Se for `off`, as estatísticas não são salvas durante a interrupção nem recarregadas no início do servidor. O valor padrão é `on`. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

O módulo requer memória compartilhada adicional proporcional a `pg_stat_statements.max`. Observe que essa memória é consumida sempre que o módulo é carregado, mesmo se `pg_stat_statements.track` estiver definido como `none`.

Esses parâmetros devem ser definidos em `postgresql.conf`. O uso típico pode ser:

```
# postgresql.conf
shared_preload_libraries = 'pg_stat_statements'

compute_query_id = on
pg_stat_statements.max = 10000
pg_stat_statements.track = all
```

### F.32.5. Saída de amostra [#](#PGSTATSTATEMENTS-SAMPLE-OUTPUT)

```
bench=# SELECT pg_stat_statements_reset();

$ pgbench -i bench
$ pgbench -c10 -t300 bench

bench=# \x
bench=# SELECT query, calls, total_exec_time, rows, 100.0 * shared_blks_hit /
               nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
          FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 5;
-[ RECORD 1 ]---+--------------------------------------------------​------------------
query           | UPDATE pgbench_branches SET bbalance = bbalance + $1 WHERE bid = $2
calls           | 3000
total_exec_time | 25565.855387
rows            | 3000
hit_percent     | 100.0000000000000000
-[ RECORD 2 ]---+--------------------------------------------------​------------------
query           | UPDATE pgbench_tellers SET tbalance = tbalance + $1 WHERE tid = $2
calls           | 3000
total_exec_time | 20756.669379
rows            | 3000
hit_percent     | 100.0000000000000000
-[ RECORD 3 ]---+--------------------------------------------------​------------------
query           | copy pgbench_accounts from stdin
calls           | 1
total_exec_time | 291.865911
rows            | 100000
hit_percent     | 100.0000000000000000
-[ RECORD 4 ]---+--------------------------------------------------​------------------
query           | UPDATE pgbench_accounts SET abalance = abalance + $1 WHERE aid = $2
calls           | 3000
total_exec_time | 271.232977
rows            | 3000
hit_percent     | 98.8454011741682975
-[ RECORD 5 ]---+--------------------------------------------------​------------------
query           | alter table pgbench_accounts add primary key (aid)
calls           | 1
total_exec_time | 160.588563
rows            | 0
hit_percent     | 100.0000000000000000


bench=# SELECT pg_stat_statements_reset(0,0,s.queryid) FROM pg_stat_statements AS s
            WHERE s.query = 'UPDATE pgbench_branches SET bbalance = bbalance + $1 WHERE bid = $2';

bench=# SELECT query, calls, total_exec_time, rows, 100.0 * shared_blks_hit /
               nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
          FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 5;
-[ RECORD 1 ]---+--------------------------------------------------​------------------
query           | UPDATE pgbench_tellers SET tbalance = tbalance + $1 WHERE tid = $2
calls           | 3000
total_exec_time | 20756.669379
rows            | 3000
hit_percent     | 100.0000000000000000
-[ RECORD 2 ]---+--------------------------------------------------​------------------
query           | copy pgbench_accounts from stdin
calls           | 1
total_exec_time | 291.865911
rows            | 100000
hit_percent     | 100.0000000000000000
-[ RECORD 3 ]---+--------------------------------------------------​------------------
query           | UPDATE pgbench_accounts SET abalance = abalance + $1 WHERE aid = $2
calls           | 3000
total_exec_time | 271.232977
rows            | 3000
hit_percent     | 98.8454011741682975
-[ RECORD 4 ]---+--------------------------------------------------​------------------
query           | alter table pgbench_accounts add primary key (aid)
calls           | 1
total_exec_time | 160.588563
rows            | 0
hit_percent     | 100.0000000000000000
-[ RECORD 5 ]---+--------------------------------------------------​------------------
query           | vacuum analyze pgbench_accounts
calls           | 1
total_exec_time | 136.448116
rows            | 0
hit_percent     | 99.9201915403032721

bench=# SELECT pg_stat_statements_reset(0,0,0);

bench=# SELECT query, calls, total_exec_time, rows, 100.0 * shared_blks_hit /
               nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
          FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 5;
-[ RECORD 1 ]---+--------------------------------------------------​---------------------------
query           | SELECT pg_stat_statements_reset(0,0,0)
calls           | 1
total_exec_time | 0.189497
rows            | 1
hit_percent     |
-[ RECORD 2 ]---+--------------------------------------------------​---------------------------
query           | SELECT query, calls, total_exec_time, rows, $1 * shared_blks_hit /          +
                |                nullif(shared_blks_hit + shared_blks_read, $2) AS hit_percent+
                |           FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT $3
calls           | 0
total_exec_time | 0
rows            | 0
hit_percent     |
```

### F.32.6. Autores [#](#PGSTATSTATEMENTS-AUTHORS)

Takahiro Itagaki `<itagaki.takahiro@oss.ntt.co.jp>`. Normalização de consulta adicionada por Peter Geoghegan `<peter@2ndquadrant.com>`.