## 27.4. Relatórios de progresso [#](#PROGRESS-REPORTING)

* [27.4.1. RELATÓRIO DE PROGRSS](progress-reporting.md#ANALYZE-PROGRESS-REPORTING)
* [27.4.2. RELATÓRIO DE CLUSTER](progress-reporting.md#CLUSTER-PROGRESS-REPORTING)
* [27.4.3. COPIAR RELATÓRIO DE PROGRSS](progress-reporting.md#COPY-PROGRESS-REPORTING)
* [27.4.4. CRIAR ÍNDICE DE RELATÓRIO DE PROGRSS](progress-reporting.md#CREATE-INDEX-PROGRESS-REPORTING)
* [27.4.5. VACUUM RELATÓRIO DE PROGRSS](progress-reporting.md#VACUUM-PROGRESS-REPORTING)
* [27.4.6. RELATÓRIO DE SUSTENTABILIDADE DE BASE](progress-reporting.md#BASEBACKUP-PROGRESS-REPORTING)

O PostgreSQL tem a capacidade de relatar o progresso de certos comandos durante a execução do comando. Atualmente, os únicos comandos que suportam o relatório de progresso são `ANALYZE`, `CLUSTER`, `CREATE INDEX`, `VACUUM`, `COPY` e [BASE_BACKUP](protocol-replication.md#PROTOCOL-REPLICATION-BASE-BACKUP) (ou seja, o comando de replicação que o [pg_basebackup](app-pgbasebackup.md "pg_basebackup") emite para fazer um backup de base). Isso pode ser expandido no futuro.

### 27.4.1. ANÁLISE DO RELATÓRIO DE PROGRSS [#](#ANALYZE-PROGRESS-REPORTING)

Sempre que o `ANALYZE` estiver em execução, a visualização `pg_stat_progress_analyze` conterá uma linha para cada backend que esteja atualmente executando esse comando. As tabelas abaixo descrevem as informações que serão relatadas e fornecem informações sobre como interpretá-las.

**Tabela 27.38. `pg_stat_progress_analyze` Visualização**



<table>
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
     <code>
      pid
     </code>
     <code>
      integer
     </code>
    </p>
    <p>
     ID de processo do backend.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      datid
     </code>
     <code>
      oid
     </code>
    </p>
    <p>
     OID do banco de dados ao qual este backend está conectado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      datname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome do banco de dados ao qual este backend está conectado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      relid
     </code>
     <code>
      oid
     </code>
    </p>
    <p>
     OID da tabela que está sendo analisada.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      phase
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Fase atual de processamento. Veja
     <a class="xref" href="progress-reporting.md#ANALYZE-PHASES" title="Table 27.39. ANALYZE Phases">
      Tabela 27.39
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      sample_blks_total
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número total de blocos de pilha que serão amostrados.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      sample_blks_scanned
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de blocos de pilha escaneados.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      ext_stats_total
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de estatísticas estendidas.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      ext_stats_computed
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de estatísticas estendidas calculadas. Esse contador avança apenas quando a fase é
     <code>
      computing extended statistics
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      child_tables_total
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de mesas infantis.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      child_tables_done
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de tabelas de crianças analisadas. Esse contador avança apenas quando a fase é
     <code>
      acquiring inherited sample rows
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      current_child_table_relid
     </code>
     <code>
      oid
     </code>
    </p>
    <p>
     OID da tabela de crianças que está sendo atualmente analisada. Esse campo é válido apenas quando a fase é
     <code>
      acquiring inherited sample rows
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      delay_time
     </code>
     <code>
      double precision
     </code>
    </p>
    <p>
     Tempo total gasto dormindo devido ao atraso baseado no custo (ver
     <a class="xref" href="runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST" title="19.10.2. Cost-based Vacuum Delay">
      Seção 19.10.2
     </a>
     ), em milissegundos
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-COST-DELAY-TIMING">
      track_cost_delay_timing
     </a>
     se estiver habilitado, caso contrário, zero).
    </p>
   </td>
  </tr>
 </tbody>
</table>










**Tabela 27.39. Fases de ANÁLISE**



<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Phase
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     initializing
    </code>
   </td>
   <td>
    O comando está se preparando para começar a varredura do heap. Essa fase deve ser muito breve.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     acquiring sample rows
    </code>
   </td>
   <td>
    O comando está atualmente analisando a tabela fornecida por
    <code>
     relid
    </code>
    para obter linhas de amostra.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     acquiring inherited sample rows
    </code>
   </td>
   <td>
    O comando está atualmente analisando tabelas de crianças para obter linhas de amostra. Colunas
    <code>
     child_tables_total
    </code>
    ,
    <code>
     child_tables_done
    </code>
    , e
    <code>
     current_child_table_relid
    </code>
    contenha as informações sobre o progresso nesta fase.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     computing statistics
    </code>
   </td>
   <td>
    O comando está calculando estatísticas das linhas da amostra obtidas durante a varredura da tabela.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     computing extended statistics
    </code>
   </td>
   <td>
    O comando está calculando estatísticas estendidas das linhas da amostra obtidas durante a varredura da tabela.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     finalizing analyze
    </code>
   </td>
   <td>
    O comando está sendo atualizado
    <code>
     pg_class
    </code>
    Quando esta fase for concluída,
    <code>
     ANALYZE
    </code>
    isso terminará.
   </td>
  </tr>
 </tbody>
</table>










Nota

Observe que, quando o `ANALYZE` é executado em uma tabela particionada sem a palavra-chave `ONLY`, todas as suas particionamentos também são analisados recursivamente. Nesse caso, o progresso do `ANALYZE` é relatado primeiro para a tabela principal, onde suas estatísticas de herança são coletadas, seguido por cada particionamento.

### 27.4.2. Relatório de progresso do CLUSTER [#](#CLUSTER-PROGRESS-REPORTING)

Sempre que o `CLUSTER` ou o `VACUUM FULL` estiver em execução, a visualização `pg_stat_progress_cluster` conterá uma linha para cada backend que esteja executando atualmente um dos comandos. As tabelas abaixo descrevem as informações que serão relatadas e fornecem informações sobre como interpretá-las.

**Tabela 27.40. `pg_stat_progress_cluster` Visualização**



<table>
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
     <code>
      pid
     </code>
     <code>
      integer
     </code>
    </p>
    <p>
     ID de processo do backend.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      datid
     </code>
     <code>
      oid
     </code>
    </p>
    <p>
     OID do banco de dados ao qual este backend está conectado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      datname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome do banco de dados ao qual este backend está conectado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      relid
     </code>
     <code>
      oid
     </code>
    </p>
    <p>
     OID da tabela que está sendo agrupada.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      command
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     O comando que está em execução. Ou
     <code>
      CLUSTER
     </code>
     ou
     <code>
      VACUUM FULL
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      phase
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Fase atual de processamento. Veja
     <a class="xref" href="progress-reporting.md#CLUSTER-PHASES" title="Table 27.41. CLUSTER and VACUUM FULL Phases">
      Tabela 27.41
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      cluster_index_relid
     </code>
     <code>
      oid
     </code>
    </p>
    <p>
     Se a tabela está sendo pesquisada usando um índice, este é o OID do índice que está sendo usado; caso contrário, é zero.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      heap_tuples_scanned
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de tuplas de pilha analisadas. Esse contador avança apenas quando a fase está
     <code>
      seq scanning heap
     </code>
     ,
     <code>
      index scanning heap
     </code>
     ou
     <code>
      writing new heap
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      heap_tuples_written
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de tuplas de pilha escritas. Esse contador avança apenas quando a fase está
     <code>
      seq scanning heap
     </code>
     ,
     <code>
      index scanning heap
     </code>
     ou
     <code>
      writing new heap
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      heap_blks_total
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número total de blocos de pilha na tabela. Esse número é relatado a partir do início
     <code>
      seq scanning heap
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      heap_blks_scanned
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de blocos de pilha examinados. Esse contador avança apenas quando a fase está
     <code>
      seq scanning heap
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      index_rebuild_count
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de índices reconstruídos. Esse contador só avança quando a fase está
     <code>
      rebuilding index
     </code>
     .
    </p>
   </td>
  </tr>
 </tbody>
</table>










**Tabela 27.41. Fases CLUSTER e VACUUM FULL**



<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Phase
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     initializing
    </code>
   </td>
   <td>
    O comando está se preparando para começar a varredura do heap. Essa fase deve ser muito breve.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     seq scanning heap
    </code>
   </td>
   <td>
    O comando está atualmente digitalizando a tabela usando uma varredura sequencial.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     index scanning heap
    </code>
   </td>
   <td>
    <code>
     CLUSTER
    </code>
    está atualmente a digitalizar a tabela usando uma varredura de índice.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     sorting tuples
    </code>
   </td>
   <td>
    <code>
     CLUSTER
    </code>
    está atualmente classificando tuplas.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     writing new heap
    </code>
   </td>
   <td>
    <code>
     CLUSTER
    </code>
    está escrevendo atualmente o novo heap.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     swapping relation files
    </code>
   </td>
   <td>
    O comando está atualmente trocando arquivos recém-construídos no lugar.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     rebuilding index
    </code>
   </td>
   <td>
    O comando está atualmente reconstruindo um índice.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     performing final cleanup
    </code>
   </td>
   <td>
    O comando está realizando a limpeza final. Quando esta fase for concluída,
    <code>
     CLUSTER
    </code>
    ou
    <code>
     VACUUM FULL
    </code>
    isso terminará.
   </td>
  </tr>
 </tbody>
</table>







### 27.4.3. Reportagem de progresso da cópia [#](#COPY-PROGRESS-REPORTING)

Sempre que o `COPY` estiver em execução, a visualização `pg_stat_progress_copy` conterá uma linha para cada backend que esteja atualmente executando um comando `COPY`. A tabela abaixo descreve as informações que serão relatadas e fornece informações sobre como interpretá-las.

**Tabela 27.42. `pg_stat_progress_copy` Visualização**



<table>
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
     <code>
      pid
     </code>
     <code>
      integer
     </code>
    </p>
    <p>
     ID de processo do backend.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      datid
     </code>
     <code>
      oid
     </code>
    </p>
    <p>
     OID do banco de dados ao qual este backend está conectado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      datname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome do banco de dados ao qual este backend está conectado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      relid
     </code>
     <code>
      oid
     </code>
    </p>
    <p>
     OID da tabela em que o
     <code>
      COPY
     </code>
     O comando é executado. Está definido para
     <code>
      0
     </code>
     se copiar de um
     <code>
      SELECT
     </code>
     query.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      command
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     O comando que está em execução:
     <code>
      COPY FROM
     </code>
     , ou
     <code>
      COPY TO
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      type
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     O tipo de E/S do qual os dados são lidos ou escritos:
     <code>
      FILE
     </code>
     ,
     <code>
      PROGRAM
     </code>
     ,
     <code>
      PIPE
     </code>
     (para
     <code>
      COPY FROM STDIN
     </code>
     e
     <code>
      COPY TO STDOUT
     </code>
     ), ou
     <code>
      CALLBACK
     </code>
     (usado, por exemplo, durante a sincronização inicial da tabela na replicação lógica).
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      bytes_processed
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de bytes já processados por
     <code>
      COPY
     </code>
     command.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      bytes_total
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Tamanho do arquivo fonte para
     <code>
      COPY FROM
     </code>
     comando em bytes. Ele está configurado para
     <code>
      0
     </code>
     se não estiver disponível.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tuples_processed
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de tuplas já processadas por
     <code>
      COPY
     </code>
     command.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tuples_excluded
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de tuplas que não foram processadas porque foram excluídas pelo
     <code>
      WHERE
     </code>
     cláusula do
     <code>
      COPY
     </code>
     command.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tuples_skipped
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de tuplas ignoradas porque contêm dados malformados. Esse contador avança apenas quando um valor diferente de
     <code>
      stop
     </code>
     é especificado para
     <code>
      ON_ERROR
     </code>
     option.
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.4.4. CRIAR RELATÓRIO DE PROGRESSO [#](#CREATE-INDEX-PROGRESS-REPORTING)

Sempre que o `CREATE INDEX` ou o `REINDEX` estiver em execução, a visualização `pg_stat_progress_create_index` conterá uma linha para cada backend que está atualmente criando índices. As tabelas abaixo descrevem as informações que serão relatadas e fornecem informações sobre como interpretá-las.

**Tabela 27.43. `pg_stat_progress_create_index` Visualização**



<table>
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
     <code>
      pid
     </code>
     <code>
      integer
     </code>
    </p>
    <p>
     ID do processo do backend que cria índices.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      datid
     </code>
     <code>
      oid
     </code>
    </p>
    <p>
     OID do banco de dados ao qual este backend está conectado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      datname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome do banco de dados ao qual este backend está conectado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      relid
     </code>
     <code>
      oid
     </code>
    </p>
    <p>
     OID da tabela na qual o índice está sendo criado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      index_relid
     </code>
     <code>
      oid
     </code>
    </p>
    <p>
     OID do índice que está sendo criado ou reindexado. Durante uma operação não concorrente
     <code>
      CREATE INDEX
     </code>
     , isso é 0.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      command
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Tipo de comando específico:
     <code>
      CREATE INDEX
     </code>
     ,
     <code>
      CREATE INDEX CONCURRENTLY
     </code>
     ,
     <code>
      REINDEX
     </code>
     , ou
     <code>
      REINDEX CONCURRENTLY
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      phase
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Fase atual de processamento da criação do índice. Veja
     <a class="xref" href="progress-reporting.md#CREATE-INDEX-PHASES" title="Table 27.44. CREATE INDEX Phases">
      Tabela 27.44
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      lockers_total
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número total de armários a aguardar, quando aplicável.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      lockers_done
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de armários já aguardados.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      current_locker_pid
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     ID do processo do armário que está sendo aguardado atualmente.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      blocks_total
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número total de blocos a serem processados na fase atual.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      blocks_done
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de blocos já processados na fase atual.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tuples_total
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número total de tuplas a serem processadas na fase atual.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tuples_done
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de tuplas já processadas na fase atual.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      partitions_total
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número total de partições nas quais o índice deve ser criado ou anexado, incluindo partições diretas e indiretas.
     <code>
      0
     </code>
     durante um
     <code>
      REINDEX
     </code>
     , ou quando o índice não está particionado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      partitions_done
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de partições nas quais o índice já foi criado ou anexado, incluindo partições diretas e indiretas.
     <code>
      0
     </code>
     durante um
     <code>
      REINDEX
     </code>
     , ou quando o índice não está particionado.
    </p>
   </td>
  </tr>
 </tbody>
</table>










**Tabela 27.44. CRIAR ÍNDICE Fases**



<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Fase
   </th>
   <th>
    Description
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     initializing
    </code>
   </td>
   <td>
    <code>
     CREATE INDEX
    </code>
    or
    <code>
     REINDEX
    </code>
    is preparing to create the index.  This phase is expected to be very brief.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     waiting for writers before build
    </code>
   </td>
   <td>
    <code>
     CREATE INDEX CONCURRENTLY
    </code>
    or
    <code>
     REINDEX CONCURRENTLY
    </code>
    is waiting for transactions with write locks that can potentially see the table to finish. This phase is skipped when not in concurrent mode. Columns
    <code>
     lockers_total
    </code>
    ,
    <code>
     lockers_done
    </code>
    and
    <code>
     current_locker_pid
    </code>
    contain the progress information for this phase.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     building index
    </code>
   </td>
   <td>
    The index is being built by the access method-specific code.  In this phase, access methods that support progress reporting fill in their own progress data, and the subphase is indicated in this column.  Typically,
    <code>
     blocks_total
    </code>
    and
    <code>
     blocks_done
    </code>
    will contain progress data, as well as potentially
    <code>
     tuples_total
    </code>
    and
    <code>
     tuples_done
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code>
     waiting for writers before validation
    </code>
   </td>
   <td>
    <code>
     CREATE INDEX CONCURRENTLY
    </code>
    or
    <code>
     REINDEX CONCURRENTLY
    </code>
    is waiting for transactions with write locks that can potentially write into the table to finish. This phase is skipped when not in concurrent mode. Columns
    <code>
     lockers_total
    </code>
    ,
    <code>
     lockers_done
    </code>
    and
    <code>
     current_locker_pid
    </code>
    contain the progress information for this phase.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     index validation: scanning index
    </code>
   </td>
   <td>
    <code>
     CREATE INDEX CONCURRENTLY
    </code>
    is scanning the index searching for tuples that need to be validated. This phase is skipped when not in concurrent mode. Columns
    <code>
     blocks_total
    </code>
    (set to the total size of the index) and
    <code>
     blocks_done
    </code>
    contain the progress information for this phase.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     index validation: sorting tuples
    </code>
   </td>
   <td>
    <code>
     CREATE INDEX CONCURRENTLY
    </code>
    is sorting the output of the index scanning phase.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     index validation: scanning table
    </code>
   </td>
   <td>
    <code>
     CREATE INDEX CONCURRENTLY
    </code>
    is scanning the table to validate the index tuples collected in the previous two phases. This phase is skipped when not in concurrent mode. Columns
    <code>
     blocks_total
    </code>
    (set to the total size of the table) and
    <code>
     blocks_done
    </code>
    contain the progress information for this phase.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     waiting for old snapshots
    </code>
   </td>
   <td>
    <code>
     CREATE INDEX CONCURRENTLY
    </code>
    or
    <code>
     REINDEX CONCURRENTLY
    </code>
    is waiting for transactions that can potentially see the table to release their snapshots.  This phase is skipped when not in concurrent mode. Columns
    <code>
     lockers_total
    </code>
    ,
    <code>
     lockers_done
    </code>
    and
    <code>
     current_locker_pid
    </code>
    contain the progress information for this phase.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     waiting for readers before marking dead
    </code>
   </td>
   <td>
    <code>
     REINDEX CONCURRENTLY
    </code>
    is waiting for transactions with read locks on the table to finish, before marking the old index dead. This phase is skipped when not in concurrent mode. Columns
    <code>
     lockers_total
    </code>
    ,
    <code>
     lockers_done
    </code>
    and
    <code>
     current_locker_pid
    </code>
    contain the progress information for this phase.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     waiting for readers before dropping
    </code>
   </td>
   <td>
    <code>
     REINDEX CONCURRENTLY
    </code>
    is waiting for transactions with read locks on the table to finish, before dropping the old index. This phase is skipped when not in concurrent mode. Columns
    <code>
     lockers_total
    </code>
    ,
    <code>
     lockers_done
    </code>
    and
    <code>
     current_locker_pid
    </code>
    contain the progress information for this phase.
   </td>
  </tr>
 </tbody>
</table>







### 27.4.5. Relatório de progresso do VACUUM [#](#VACUUM-PROGRESS-REPORTING)

Sempre que o `VACUUM` estiver em execução, a visualização `pg_stat_progress_vacuum` conterá uma linha para cada backend (incluindo processos de trabalhadores do autovacuum) que esteja atualmente realizando uma limpeza. As tabelas abaixo descrevem as informações que serão relatadas e fornecem informações sobre como interpretá-las. O progresso dos comandos do `VACUUM FULL` é relatado via `pg_stat_progress_cluster`, pois tanto o `VACUUM FULL` quanto o `CLUSTER` reescrevem a tabela, enquanto o `VACUUM` regular apenas a modifica no local. Veja [Seção 27.4.2](progress-reporting.md#CLUSTER-PROGRESS-REPORTING).

**Tabela 27.45. `pg_stat_progress_vacuum` Visualização**



<table>
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
     <code>
      pid
     </code>
     <code>
      integer
     </code>
    </p>
    <p>
     ID de processo do backend.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      datid
     </code>
     <code>
      oid
     </code>
    </p>
    <p>
     OID do banco de dados ao qual este backend está conectado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      datname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome do banco de dados ao qual este backend está conectado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      relid
     </code>
     <code>
      oid
     </code>
    </p>
    <p>
     OID da tabela que está sendo aspirada.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      phase
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Fase atual de processamento do vácuo. Veja
     <a class="xref" href="progress-reporting.md#VACUUM-PHASES" title="Table 27.46. VACUUM Phases">
      Tabela 27.46
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      heap_blks_total
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número total de blocos de pilha na tabela. Esse número é relatado a partir do início da varredura; blocos adicionados posteriormente não serão (e não precisam ser) visitados por este
     <code>
      VACUUM
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      heap_blks_scanned
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de blocos de pilha escaneados. Como o
     <a class="link" href="storage-vm.md" title="66.4. Visibility Map">
      mapa de visibilidade
     </a>
     é usado para otimizar as varreduras, alguns blocos serão ignorados sem inspeção; os blocos ignorados estão incluídos neste total, de modo que este número acabará se tornando igual a
     <code>
      heap_blks_total
     </code>
     quando o vácuo estiver completo. Esse contador só avança quando a fase estiver
     <code>
      scanning heap
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      heap_blks_vacuumed
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de blocos de pilha aspirados. A menos que a tabela não tenha índices, esse contador só avança quando a fase está
     <code>
      vacuuming heap
     </code>
     Os blocos que não contêm tuplas mortas são ignorados, portanto, o contador pode, às vezes, avançar em grandes incrementos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      index_vacuum_count
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de ciclos de vácuo de índice concluídos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      max_dead_tuple_bytes
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Quantidade de dados de tupla mortos que podemos armazenar antes de precisar realizar um ciclo de vácuo de índice, com base em
     <a class="xref" href="runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM">
      maintenance_work_mem
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      dead_tuple_bytes
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Quantidade de dados de tupla mortos coletados desde o último ciclo de vácuo do índice.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      num_dead_item_ids
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de identificadores de itens mortos coletados desde o último ciclo de vácuo do índice.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indexes_total
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número total de índices que serão aspirados ou limpos. Esse número é relatado no início do
     <code>
      vacuuming indexes
     </code>
     fase ou a
     <code>
      cleaning up indexes
     </code>
     phase.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indexes_processed
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de índices processados. Esse contador avança apenas quando a fase é
     <code>
      vacuuming indexes
     </code>
     ou
     <code>
      cleaning up indexes
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      delay_time
     </code>
     <code>
      double precision
     </code>
    </p>
    <p>
     Tempo total gasto dormindo devido ao atraso baseado no custo (ver
     <a class="xref" href="runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST" title="19.10.2. Cost-based Vacuum Delay">
      Seção 19.10.2
     </a>
     ), em milissegundos
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-COST-DELAY-TIMING">
      track_cost_delay_timing
     </a>
     se estiver habilitado, caso contrário, zero). Isso inclui o tempo que quaisquer trabalhadores paralelos associados dormiram. No entanto, os trabalhadores paralelos relatam seu tempo de sono não com mais frequência do que uma vez por segundo, portanto, o valor relatado pode ser ligeiramente desatualizado.
    </p>
   </td>
  </tr>
 </tbody>
</table>










**Tabela 27.46. Fases do VACUUM**



<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Phase
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     initializing
    </code>
   </td>
   <td>
    <code>
     VACUUM
    </code>
    está se preparando para começar a varredura do heap. Essa fase deve ser muito breve.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     scanning heap
    </code>
   </td>
   <td>
    <code>
     VACUUM
    </code>
    está atualmente a digitalizar o heap. Ela podará e defragmenta cada página, se necessário, e, possivelmente, realizará atividade de congelamento. A
    <code>
     heap_blks_scanned
    </code>
    A coluna pode ser usada para monitorar o progresso do exame.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     vacuuming indexes
    </code>
   </td>
   <td>
    <code>
     VACUUM
    </code>
    está atualmente limpando os índices. Se uma tabela tiver algum índice, isso ocorrerá pelo menos uma vez por limpeza, após o heap ter sido completamente escaneado. Pode ocorrer várias vezes por limpeza se
    <a class="xref" href="runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM">
     maintenance_work_mem
    </a>
    (ou, no caso do autovacuum,
    <a class="xref" href="runtime-config-resource.md#GUC-AUTOVACUUM-WORK-MEM">
     autovacuum_work_mem
    </a>
    se definido) é insuficiente para armazenar o número de tuplas mortas encontradas.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     vacuuming heap
    </code>
   </td>
   <td>
    <code>
     VACUUM
    </code>
    está atualmente aspirando a pilha. Aspirar a pilha é distinto de varrer a pilha, e ocorre após cada instância de aspiração de índices. Se
    <code>
     heap_blks_scanned
    </code>
    é menor que
    <code>
     heap_blks_total
    </code>
    , o sistema voltará a varrer a pilha após esta fase ser concluída; caso contrário, começará a limpar os índices após esta fase ser concluída.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     cleaning up indexes
    </code>
   </td>
   <td>
    <code>
     VACUUM
    </code>
    Atualmente, está limpando os índices. Isso ocorre após o heap ter sido completamente escaneado e toda a varredura dos índices e do heap ter sido concluída.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     truncating heap
    </code>
   </td>
   <td>
    <code>
     VACUUM
    </code>
    Atualmente, está truncando o heap para retornar páginas vazias no final da relação ao sistema operacional. Isso ocorre após a limpeza dos índices.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     performing final cleanup
    </code>
   </td>
   <td>
    <code>
     VACUUM
    </code>
    está realizando a limpeza final. Durante esta fase,
    <code>
     VACUUM
    </code>
    vaçará o mapa do espaço livre, atualizará as estatísticas
    <code>
     pg_class
    </code>
    , e informe as estatísticas ao sistema de estatísticas acumuladas. Quando essa fase for concluída,
    <code>
     VACUUM
    </code>
    isso terminará.
   </td>
  </tr>
 </tbody>
</table>







### 27.4.6. Relatório de progresso do backup da base [#](#BASEBACKUP-PROGRESS-REPORTING)

Sempre que um aplicativo como o pg_basebackup estiver fazendo um backup de base, a visão `pg_stat_progress_basebackup` conterá uma linha para cada processo emissor de WAL que esteja executando o comando de replicação `BASE_BACKUP` e streaming o backup. As tabelas abaixo descrevem as informações que serão relatadas e fornecem informações sobre como interpretá-las.

**Tabela 27.47. `pg_stat_progress_basebackup` Visualização**



<table>
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
     <code>
      pid
     </code>
     <code>
      integer
     </code>
    </p>
    <p>
     ID de processo de um processo de emissor WAL.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      phase
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Fase atual de processamento. Veja
     <a class="xref" href="progress-reporting.md#BASEBACKUP-PHASES" title="Table 27.48. Base Backup Phases">
      Tabela 27.48
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      backup_total
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Quantidade total de dados que serão transmitidos. Isso é estimado e relatado a partir do início
     <code>
      streaming database files
     </code>
     Observe que essa é apenas uma aproximação, pois o banco de dados pode mudar durante o processo.
     <code>
      streaming database files
     </code>
     A fase e o registro WAL podem ser incluídos no backup posteriormente. Este é sempre o mesmo valor que
     <code>
      backup_streamed
     </code>
     uma vez que o volume de dados transmitidos exceda o tamanho total estimado. Se a estimativa estiver desativada
     <span class="application">
      pg_basebackup
     </span>
     (i.e.,
     <code>
      --no-estimate-size
     </code>
     se especificado uma opção), isso é
     <code>
      NULL
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      backup_streamed
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Quantidade de dados transmitidos. Esse contador avança apenas quando a fase é
     <code>
      streaming database files
     </code>
     ou
     <code>
      transferring wal files
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tablespaces_total
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número total de espaços de tabela que serão transmitidos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tablespaces_streamed
     </code>
     <code>
      bigint
     </code>
    </p>
    <p>
     Número de espaços de tabela transmitidos. Esse contador avança apenas quando a fase é
     <code>
      streaming database files
     </code>
     .
    </p>
   </td>
  </tr>
 </tbody>
</table>










**Tabela 27.48. Fases de Backup Básico**



<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Fase
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     initializing
    </code>
   </td>
   <td>
    O processo de envio WAL está se preparando para iniciar o backup. Espera-se que essa fase seja muito breve.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     waiting for checkpoint to finish
    </code>
   </td>
   <td>
    O processo de envio WAL está atualmente em execução
    <code>
     pg_backup_start
    </code>
    para se preparar para fazer um backup básico e esperar que o ponto de verificação de início do backup seja concluído.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     estimating backup size
    </code>
   </td>
   <td>
    O processo de envio WAL está atualmente estimando o total de arquivos de banco de dados que serão transmitidos como um backup básico.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     streaming database files
    </code>
   </td>
   <td>
    O processo de envio WAL está atualmente transmitindo arquivos de banco de dados como backup básico.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     waiting for wal archiving to finish
    </code>
   </td>
   <td>
    O processo de envio WAL está atualmente em execução
    <code>
     pg_backup_stop
    </code>
    para finalizar o backup, e esperar que todos os arquivos WAL necessários para o backup de base sejam arquivados com sucesso. Se qualquer um dos
    <code>
     --wal-method=none
    </code>
    ou
    <code>
     --wal-method=stream
    </code>
    é especificado em
    <span class="application">
     pg_basebackup
    </span>
    O backup terminará quando esta fase for concluída.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     transferring wal files
    </code>
   </td>
   <td>
    O processo de emissor WAL está atualmente transferindo todos os registros WAL gerados durante o backup. Essa fase ocorre após
    <code>
     waiting for wal archiving to finish
    </code>
    fase se
    <code>
     --wal-method=fetch
    </code>
    é especificado em
    <span class="application">
     pg_basebackup
    </span>
    O backup terminará quando esta fase for concluída.
   </td>
  </tr>
 </tbody>
</table>





