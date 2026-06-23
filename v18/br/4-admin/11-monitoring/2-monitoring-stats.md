## 27.2. Sistema de Estatísticas Cumulativas [#](#MONITORING-STATS)

* [Configuração de Coleta de Estatísticas](monitoring-stats.md#MONITORING-STATS-SETUP)
* [Visualização de Estatísticas](monitoring-stats.md#MONITORING-STATS-VIEWS)
* [`pg_stat_activity`](monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW)
* [`pg_stat_replication`](monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-VIEW)
* [`pg_stat_replication_slots`](monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-SLOTS-VIEW)
* [`pg_stat_wal_receiver`](monitoring-stats.md#MONITORING-PG-STAT-WAL-RECEIVER-VIEW)
* [`pg_stat_recovery_prefetch`](monitoring-stats.md#MONITORING-PG-STAT-RECOVERY-PREFETCH)
* [`pg_stat_subscription`](monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION)
* [`pg_stat_subscription_stats`](monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION-STATS)
* [`pg_stat_ssl`](monitoring-stats.md#MONITORING-PG-STAT-SSL-VIEW)
* [`pg_stat_gssapi`](monitoring-stats.md#MONITORING-PG-STAT-GSSAPI-VIEW)
* [`pg_stat_archiver`](monitoring-stats.md#MONITORING-PG-STAT-ARCHIVER-VIEW)
* [`pg_stat_io`](monitoring-stats.md#MONITORING-PG-STAT-IO-VIEW)
* [`pg_stat_bgwriter`](monitoring-stats.md#MONITORING-PG-STAT-BGWRITER-VIEW)
* [`pg_stat_checkpointer`](monitoring-stats.md#MONITORING-PG-STAT-CHECKPOINTER-VIEW)
* [`pg_stat_wal`](monitoring-stats.md#MONITORING-PG-STAT-WAL-VIEW)
* [`pg_stat_database`](monitoring-stats.md#MONITORING-PG-STAT-DATABASE-VIEW)
* [`pg_stat_database_conflicts`](monitoring-stats.md#MONITORING-PG-STAT-DATABASE-CONFLICTS-VIEW)
* [`pg_stat_all_tables`](monitoring-stats.md#MONITORING-PG-STAT-ALL-TABLES-VIEW)
* [`pg_stat_all_indexes`](monitoring-stats.md#MONITORING-PG-STAT-ALL-INDEXES-VIEW)
* [`pg_statio_all_tables`](monitoring-stats.md#MONITORING-PG-STATIO-ALL-TABLES-VIEW)
* [`pg_statio_all_indexes`](monitoring-stats.md#MONITORING-PG-STATIO-ALL-INDEXES-VIEW)
* [`pg_statio_all_sequences`](monitoring-stats.md#MONITORING-PG-STATIO-ALL-SEQUENCES-VIEW)
* [`pg_stat_user_functions`](monitoring-stats.md#MONITORING-PG-STAT-USER-FUNCTIONS-VIEW)
* [`pg_stat_slru`](monitoring-stats.md#MONITORING-PG-STAT-SLRU-VIEW)
* [Funções de Estatísticas](monitoring-stats.md#MONITORING-STATS-FUNCTIONS)

O sistema de *estatísticas cumulativas* do PostgreSQL suporta a coleta e o relatório de informações sobre a atividade do servidor. Atualmente, os acessos a tabelas e índices, tanto em termos de blocos de disco quanto de linhas individuais, são contados. O número total de linhas em cada tabela e informações sobre ações de vácuo e análise para cada tabela também são contados. Se habilitado, as chamadas a funções definidas pelo usuário e o tempo total gasto em cada uma também são contadas.

O PostgreSQL também suporta relatórios de informações dinâmicas sobre exatamente o que está acontecendo no sistema agora, como o comando exato que está sendo executado atualmente por outros processos do servidor e quais outras conexões existem no sistema. Essa facilidade é independente do sistema de estatísticas acumuladas.

### 27.2.1. Configuração de Coleta de Estatísticas [#](#MONITORING-STATS-SETUP)

Como a coleta de estatísticas adiciona algum overhead à execução da consulta, o sistema pode ser configurado para coletar ou não coletar informações. Isso é controlado por parâmetros de configuração que normalmente são definidos em `postgresql.conf`. (Consulte [Capítulo 19](runtime-config.md) para obter detalhes sobre a configuração dos parâmetros de configuração.)

O parâmetro [track_activities](runtime-config-statistics.md#GUC-TRACK-ACTIVITIES) permite o monitoramento do comando atual executado por qualquer processo do servidor.

O parâmetro [track_cost_delay_timing](runtime-config-statistics.md#GUC-TRACK-COST-DELAY-TIMING) permite o monitoramento do atraso de vácuo baseado em custo.

O parâmetro [track_counts](runtime-config-statistics.md#GUC-TRACK-COUNTS) controla se as estatísticas acumuladas são coletadas sobre acessos a tabelas e índices.

O parâmetro [track_functions](runtime-config-statistics.md#GUC-TRACK-FUNCTIONS) permite o rastreamento do uso de funções definidas pelo usuário.

O parâmetro [track_io_timing](runtime-config-statistics.md#GUC-TRACK-IO-TIMING) permite o monitoramento dos tempos de leitura, escrita, extensão e fsync de blocos.

O parâmetro [track_wal_io_timing](runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING) permite o monitoramento dos tempos de leitura, escrita e fsync do WAL.

Normalmente, esses parâmetros são definidos em `postgresql.conf` para que se apliquem a todos os processos do servidor, mas é possível ativá-los ou desativá-los em sessões individuais usando o comando [SET](sql-set.md "SET"). (Para evitar que usuários comuns ocultem sua atividade do administrador, apenas superusuários têm permissão para alterar esses parâmetros com `SET`.)

Estatísticas acumuladas são coletadas na memória compartilhada. Cada processo do PostgreSQL coleta estatísticas localmente, e depois atualiza os dados compartilhados em intervalos apropriados. Quando um servidor, incluindo uma replica física, é desligado de forma limpa, uma cópia permanente dos dados das estatísticas é armazenada no subdiretório `pg_stat`, para que as estatísticas possam ser mantidas após a reinicialização do servidor. Em contraste, quando é iniciado a partir de uma desligamento não limpo (por exemplo, após um desligamento imediato, um crash do servidor, a partir de um backup de base e recuperação em um ponto no tempo), todos os contadores de estatísticas são redefinidos.

### 27.2.2. Visualização de estatísticas [#](#MONITORING-STATS-VIEWS)

Vários pontos de vista predefinidos, listados em [Tabela 27.1](monitoring-stats.md#MONITORING-STATS-DYNAMIC-VIEWS-TABLE), estão disponíveis para mostrar o estado atual do sistema. Há também vários outros pontos de vista, listados em [Tabela 27.2](monitoring-stats.md#MONITORING-STATS-VIEWS-TABLE), disponíveis para mostrar as estatísticas acumuladas. Alternativamente, é possível criar pontos de vista personalizados usando as funções estatísticas cumulativas subjacentes, conforme discutido em [Seção 27.2.26](monitoring-stats.md#MONITORING-STATS-FUNCTIONS).

Ao usar as visualizações e funções de estatísticas cumulativas para monitorar os dados coletados, é importante perceber que as informações não são atualizadas instantaneamente. Cada processo de servidor individual elimina as estatísticas acumuladas da memória compartilhada pouco antes de ficar inativo, mas não com mais frequência do que uma vez a cada `PGSTAT_MIN_INTERVAL` milissegundos (1 segundo, a menos que seja alterado durante a construção do servidor); portanto, uma consulta ou transação em andamento não afeta os totais exibidos e as informações exibidas ficam atrasadas em relação à atividade real. No entanto, as informações da consulta atual coletadas por `track_activities` estão sempre atualizadas.

Outro ponto importante é que, quando um processo de servidor é solicitado a exibir qualquer uma das estatísticas acumuladas, os valores acessados são armazenados em cache até o final de sua transação atual na configuração padrão. Assim, as estatísticas mostrarão informações estáticas enquanto você continuar a transação atual. Da mesma forma, as informações sobre as consultas atuais de todas as sessões são coletadas quando qualquer informação desse tipo é solicitada pela primeira vez dentro de uma transação, e as mesmas informações serão exibidas ao longo da transação. Essa é uma característica, não um erro, porque permite que você realize várias consultas nas estatísticas e correle ao resultados sem se preocupar que os números estão mudando sob você. Ao analisar estatísticas interativamente, ou com consultas caras, o delta de tempo entre os acessos a estatísticas individuais pode levar a uma distorção significativa nas estatísticas armazenadas em cache. Para minimizar a distorção, `stats_fetch_consistency` pode ser configurado para `snapshot`, ao preço do aumento do uso de memória para armazenar dados de estatísticas não necessários. Por outro lado, se é sabido que as estatísticas são acessadas apenas uma vez, o armazenamento de estatísticas acessadas é desnecessário e pode ser evitado configurando `stats_fetch_consistency` para `none`. Você pode invocar `pg_stat_clear_snapshot()` para descartar o snapshot de estatísticas da transação atual ou os valores armazenados em cache (se houver). A próxima utilização das informações estatísticas (quando no modo snapshot) causará a construção de um novo snapshot ou (quando no modo cache) os dados de estatísticas armazenados em cache serão acessados.

Uma transação também pode ver suas próprias estatísticas (ainda não descarregadas para as estatísticas de memória compartilhada) nas visualizações `pg_stat_xact_all_tables`, `pg_stat_xact_sys_tables`, `pg_stat_xact_user_tables` e `pg_stat_xact_user_functions`. Esses números não atuam como afirmado acima; em vez disso, eles são atualizados continuamente ao longo da transação.

Algumas das informações nas visualizações de estatísticas dinâmicas mostradas na [Tabela 27.1] ((monitoring-stats.md#MONITORING-STATS-DYNAMIC-VIEWS-TABLE "Table 27.1. Dynamic Statistics Views")) são restritas em termos de segurança. Os usuários comuns podem apenas ver todas as informações sobre suas próprias sessões (sessões que pertencem a um papel do qual são membros). Nas linhas sobre outras sessões, muitas colunas serão nulos. No entanto, observe que a existência de uma sessão e suas propriedades gerais, como o usuário da sessão e o banco de dados, são visíveis para todos os usuários. Superusuários e papéis com privilégios de papel embutido [[`pg_read_all_stats`] ((predefined-roles.md#PREDEFINED-ROLE-PG-MONITOR))] podem ver todas as informações sobre todas as sessões.

**Tabela 27.1. Visualizações de estatísticas dinâmicas**



<table border="1" class="table" summary="Dynamic Statistics Views">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    View Name
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="structname">
     pg_stat_activity
    </code>
   </td>
   <td>
    Uma linha por processo do servidor, mostrando informações relacionadas à atividade atual desse processo, como estado e consulta atual. Veja
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW" title="27.2.3. pg_stat_activity">
     <code class="structname">
      pg_stat_activity
     </code>
    </a>
    para obter mais informações.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_replication
    </code>
   </td>
   <td>
    Uma linha por processo de emissor WAL, mostrando estatísticas sobre a replicação para o servidor de standby conectado a esse emissor. Veja
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-VIEW" title="27.2.4. pg_stat_replication">
     <code class="structname">
      pg_stat_replication
     </code>
    </a>
    para obter mais informações.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_wal_receiver
    </code>
   </td>
   <td>
    Apenas uma linha, mostrando estatísticas sobre o receptor WAL do servidor conectado desse receptor. Veja
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-WAL-RECEIVER-VIEW" title="27.2.6. pg_stat_wal_receiver">
     <code class="structname">
      pg_stat_wal_receiver
     </code>
    </a>
    para obter mais informações.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_recovery_prefetch
    </code>
   </td>
   <td>
    Apenas uma linha, mostrando estatísticas sobre os blocos pré-carregados durante a recuperação.
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-RECOVERY-PREFETCH" title="27.2.7. pg_stat_recovery_prefetch">
     <code class="structname">
      pg_stat_recovery_prefetch
     </code>
    </a>
    para obter mais informações.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_subscription
    </code>
   </td>
   <td>
    Pelo menos uma linha por assinatura, mostrando informações sobre os trabalhadores da assinatura. Veja
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION" title="27.2.8. pg_stat_subscription">
     <code class="structname">
      pg_stat_subscription
     </code>
    </a>
    para obter mais informações.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_ssl
    </code>
   </td>
   <td>
    Uma linha por conexão (regular e de replicação), mostrando informações sobre SSL usado nesta conexão. Veja
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-SSL-VIEW" title="27.2.10. pg_stat_ssl">
     <code class="structname">
      pg_stat_ssl
     </code>
    </a>
    para obter mais informações.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_gssapi
    </code>
   </td>
   <td>
    Uma linha por conexão (regular e de replicação), mostrando informações sobre a autenticação e criptografia GSSAPI usadas nesta conexão. Veja
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-GSSAPI-VIEW" title="27.2.11. pg_stat_gssapi">
     <code class="structname">
      pg_stat_gssapi
     </code>
    </a>
    para obter mais informações.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_progress_analyze
    </code>
   </td>
   <td>
    Uma linha para cada backend (incluindo processos de trabalho do autovacuum) em execução
    <code class="command">
     ANALYZE
    </code>
    , mostrando o progresso atual.
    <a class="xref" href="progress-reporting.md#ANALYZE-PROGRESS-REPORTING" title="27.4.1. ANALYZE Progress Reporting">
     Seção 27.4.1
    </a>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_progress_create_index
    </code>
   </td>
   <td>
    Uma linha para cada backend em execução
    <code class="command">
     CREATE INDEX
    </code>
    ou
    <code class="command">
     REINDEX
    </code>
    , mostrando o progresso atual. Veja
    <a class="xref" href="progress-reporting.md#CREATE-INDEX-PROGRESS-REPORTING" title="27.4.4. CREATE INDEX Progress Reporting">
     Seção 27.4.4
    </a>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_progress_vacuum
    </code>
   </td>
   <td>
    Uma linha para cada backend (incluindo processos de trabalho do autovacuum) em execução
    <code class="command">
     VACUUM
    </code>
    , mostrando o progresso atual.
    <a class="xref" href="progress-reporting.md#VACUUM-PROGRESS-REPORTING" title="27.4.5. VACUUM Progress Reporting">
     Seção 27.4.5
    </a>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_progress_cluster
    </code>
   </td>
   <td>
    Uma linha para cada backend em execução
    <code class="command">
     CLUSTER
    </code>
    ou
    <code class="command">
     VACUUM FULL
    </code>
    , mostrando o progresso atual.
    <a class="xref" href="progress-reporting.md#CLUSTER-PROGRESS-REPORTING" title="27.4.2. CLUSTER Progress Reporting">
     Seção 27.4.2
    </a>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_progress_basebackup
    </code>
   </td>
   <td>
    Uma linha para cada processo de emissor WAL que está fazendo streaming de um backup de base, mostrando o progresso atual. Veja
    <a class="xref" href="progress-reporting.md#BASEBACKUP-PROGRESS-REPORTING" title="27.4.6. Base Backup Progress Reporting">
     Seção 27.4.6
    </a>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_progress_copy
    </code>
   </td>
   <td>
    Uma linha para cada backend em execução
    <code class="command">
     COPY
    </code>
    , mostrando o progresso atual.
    <a class="xref" href="progress-reporting.md#COPY-PROGRESS-REPORTING" title="27.4.3. COPY Progress Reporting">
     Seção 27.4.3
    </a>
    .
   </td>
  </tr>
 </tbody>
</table>










**Tabela 27.2. Visualizações de estatísticas coletadas**



<table border="1" class="table" summary="Collected Statistics Views">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    View Name
   </th>
   <th>
    Description
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="structname">
     pg_stat_archiver
    </code>
   </td>
   <td>
    One row only, showing statistics about the WAL archiver process's activity. See
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-ARCHIVER-VIEW" title="27.2.12. pg_stat_archiver">
     <code class="structname">
      pg_stat_archiver
     </code>
    </a>
    for details.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_bgwriter
    </code>
   </td>
   <td>
    One row only, showing statistics about the background writer process's activity. See
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-BGWRITER-VIEW" title="27.2.14. pg_stat_bgwriter">
     <code class="structname">
      pg_stat_bgwriter
     </code>
    </a>
    for details.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_checkpointer
    </code>
   </td>
   <td>
    One row only, showing statistics about the checkpointer process's activity. See
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-CHECKPOINTER-VIEW" title="27.2.15. pg_stat_checkpointer">
     <code class="structname">
      pg_stat_checkpointer
     </code>
    </a>
    for details.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_database
    </code>
   </td>
   <td>
    One row per database, showing database-wide statistics. See
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-DATABASE-VIEW" title="27.2.17. pg_stat_database">
     <code class="structname">
      pg_stat_database
     </code>
    </a>
    for details.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_database_conflicts
    </code>
   </td>
   <td>
    One row per database, showing database-wide statistics about query cancels due to conflict with recovery on standby servers. See
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-DATABASE-CONFLICTS-VIEW" title="27.2.18. pg_stat_database_conflicts">
     <code class="structname">
      pg_stat_database_conflicts
     </code>
    </a>
    for details.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_io
    </code>
   </td>
   <td>
    One row for each combination of backend type, context, and target object containing cluster-wide I/O statistics. See
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-IO-VIEW" title="27.2.13. pg_stat_io">
     <code class="structname">
      pg_stat_io
     </code>
    </a>
    for details.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_replication_slots
    </code>
   </td>
   <td>
    One row per replication slot, showing statistics about the replication slot's usage. See
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-SLOTS-VIEW" title="27.2.5. pg_stat_replication_slots">
     <code class="structname">
      pg_stat_replication_slots
     </code>
    </a>
    for details.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_slru
    </code>
   </td>
   <td>
    One row per SLRU, showing statistics of operations. See
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-SLRU-VIEW" title="27.2.25. pg_stat_slru">
     <code class="structname">
      pg_stat_slru
     </code>
    </a>
    for details.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_subscription_stats
    </code>
   </td>
   <td>
    One row per subscription, showing statistics about errors and conflicts. See
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION-STATS" title="27.2.9. pg_stat_subscription_stats">
     <code class="structname">
      pg_stat_subscription_stats
     </code>
    </a>
    for details.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_wal
    </code>
   </td>
   <td>
    One row only, showing statistics about WAL activity. See
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-WAL-VIEW" title="27.2.16. pg_stat_wal">
     <code class="structname">
      pg_stat_wal
     </code>
    </a>
    for details.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_all_tables
    </code>
   </td>
   <td>
    One row for each table in the current database, showing statistics about accesses to that specific table. See
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-ALL-TABLES-VIEW" title="27.2.19. pg_stat_all_tables">
     <code class="structname">
      pg_stat_all_tables
     </code>
    </a>
    for details.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_sys_tables
    </code>
   </td>
   <td>
    Same as
    <code class="structname">
     pg_stat_all_tables
    </code>
    , except that only system tables are shown.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_user_tables
    </code>
   </td>
   <td>
    Same as
    <code class="structname">
     pg_stat_all_tables
    </code>
    , except that only user tables are shown.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_xact_all_tables
    </code>
   </td>
   <td>
    Similar to
    <code class="structname">
     pg_stat_all_tables
    </code>
    , but counts actions taken so far within the current transaction (which are
    <span class="emphasis">
     <em>
      not
     </em>
    </span>
    yet included in
    <code class="structname">
     pg_stat_all_tables
    </code>
    and related views). The columns for numbers of live and dead rows and vacuum and analyze actions are not present in this view.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_xact_sys_tables
    </code>
   </td>
   <td>
    Same as
    <code class="structname">
     pg_stat_xact_all_tables
    </code>
    , except that only system tables are shown.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_xact_user_tables
    </code>
   </td>
   <td>
    Same as
    <code class="structname">
     pg_stat_xact_all_tables
    </code>
    , except that only user tables are shown.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_all_indexes
    </code>
   </td>
   <td>
    One row for each index in the current database, showing statistics about accesses to that specific index. See
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-ALL-INDEXES-VIEW" title="27.2.20. pg_stat_all_indexes">
     <code class="structname">
      pg_stat_all_indexes
     </code>
    </a>
    for details.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_sys_indexes
    </code>
   </td>
   <td>
    Same as
    <code class="structname">
     pg_stat_all_indexes
    </code>
    , except that only indexes on system tables are shown.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_user_indexes
    </code>
   </td>
   <td>
    Same as
    <code class="structname">
     pg_stat_all_indexes
    </code>
    , except that only indexes on user tables are shown.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_user_functions
    </code>
   </td>
   <td>
    One row for each tracked function, showing statistics about executions of that function. See
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-USER-FUNCTIONS-VIEW" title="27.2.24. pg_stat_user_functions">
     <code class="structname">
      pg_stat_user_functions
     </code>
    </a>
    for details.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_stat_xact_user_functions
    </code>
   </td>
   <td>
    Similar to
    <code class="structname">
     pg_stat_user_functions
    </code>
    , but counts only calls during the current transaction (which are
    <span class="emphasis">
     <em>
      not
     </em>
    </span>
    yet included in
    <code class="structname">
     pg_stat_user_functions
    </code>
    ).
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_statio_all_tables
    </code>
   </td>
   <td>
    One row for each table in the current database, showing statistics about I/O on that specific table. See
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STATIO-ALL-TABLES-VIEW" title="27.2.21. pg_statio_all_tables">
     <code class="structname">
      pg_statio_all_tables
     </code>
    </a>
    for details.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_statio_sys_tables
    </code>
   </td>
   <td>
    Same as
    <code class="structname">
     pg_statio_all_tables
    </code>
    , except that only system tables are shown.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_statio_user_tables
    </code>
   </td>
   <td>
    Same as
    <code class="structname">
     pg_statio_all_tables
    </code>
    , except that only user tables are shown.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_statio_all_indexes
    </code>
   </td>
   <td>
    One row for each index in the current database, showing statistics about I/O on that specific index. See
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STATIO-ALL-INDEXES-VIEW" title="27.2.22. pg_statio_all_indexes">
     <code class="structname">
      pg_statio_all_indexes
     </code>
    </a>
    for details.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_statio_sys_indexes
    </code>
   </td>
   <td>
    Same as
    <code class="structname">
     pg_statio_all_indexes
    </code>
    , except that only indexes on system tables are shown.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_statio_user_indexes
    </code>
   </td>
   <td>
    Same as
    <code class="structname">
     pg_statio_all_indexes
    </code>
    , except that only indexes on user tables are shown.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_statio_all_sequences
    </code>
   </td>
   <td>
    One row for each sequence in the current database, showing statistics about I/O on that specific sequence. See
    <a class="link" href="monitoring-stats.md#MONITORING-PG-STATIO-ALL-SEQUENCES-VIEW" title="27.2.23. pg_statio_all_sequences">
     <code class="structname">
      pg_statio_all_sequences
     </code>
    </a>
    for details.
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_statio_sys_sequences
    </code>
   </td>
   <td>
    Same as
    <code class="structname">
     pg_statio_all_sequences
    </code>
    , except that only system sequences are shown.  (Presently, no system sequences are defined, so this view is always empty.)
   </td>
  </tr>
  <tr>
   <td>
    <code class="structname">
     pg_statio_user_sequences
    </code>
   </td>
   <td>
    Same as
    <code class="structname">
     pg_statio_all_sequences
    </code>
    , except that only user sequences are shown.
   </td>
  </tr>
 </tbody>
</table>










As estatísticas por índice são particularmente úteis para determinar quais índices estão sendo utilizados e quão eficazes eles são.

Os conjuntos de vistas `pg_stat_io` e `pg_statio_` são úteis para determinar a eficácia do cache de buffer. Eles podem ser usados para calcular um índice de acerto de cache. Note que, embora as estatísticas de I/O do PostgreSQL capturem a maioria das instâncias em que o kernel foi invocado para realizar I/O, elas não diferenciam entre os dados que tiveram que ser obtidos do disco e aqueles que já residiam no cache de páginas do kernel. Os usuários são aconselhados a usar as vistas de estatísticas do PostgreSQL em combinação com utilitários do sistema operacional para obter uma imagem mais completa do desempenho de I/O de seu banco de dados.

### 27.2.3. `pg_stat_activity` [#](#MONITORING-PG-STAT-ACTIVITY-VIEW)

A visualização `pg_stat_activity` terá uma linha por processo do servidor, exibindo informações relacionadas à atividade atual desse processo.

**Tabela 27.3. `pg_stat_activity` Visualização**



<table border="1" class="table" summary="pg_stat_activity View">
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
      datid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     OID of the database this backend is connected to
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      datname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Name of the database this backend is connected to
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      pid
     </code>
     <code class="type">
      integer
     </code>
    </p>
    <p>
     Process ID of this backend
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      leader_pid
     </code>
     <code class="type">
      integer
     </code>
    </p>
    <p>
     Process ID of the parallel group leader if this process is a parallel query worker, or process ID of the leader apply worker if this process is a parallel apply worker.
     <code class="literal">
      NULL
     </code>
     indicates that this process is a parallel group leader or leader apply worker, or does not participate in any parallel operation.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      usesysid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     OID of the user logged into this backend
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      usename
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Name of the user logged into this backend
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      application_name
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Name of the application that is connected to this backend
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      client_addr
     </code>
     <code class="type">
      inet
     </code>
    </p>
    <p>
     IP address of the client connected to this backend. If this field is null, it indicates either that the client is connected via a Unix socket on the server machine or that this is an internal process such as autovacuum.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      client_hostname
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Host name of the connected client, as reported by a reverse DNS lookup of
     <code class="structfield">
      client_addr
     </code>
     . This field will only be non-null for IP connections, and only when
     <a class="xref" href="runtime-config-logging.md#GUC-LOG-HOSTNAME">
      log_hostname
     </a>
     is enabled.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      client_port
     </code>
     <code class="type">
      integer
     </code>
    </p>
    <p>
     TCP port number that the client is using for communication with this backend, or
     <code class="literal">
      -1
     </code>
     if a Unix socket is used. If this field is null, it indicates that this is an internal server process.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      backend_start
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Time when this process was started.  For client backends, this is the time the client connected to the server.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      xact_start
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Time when this process' current transaction was started, or null if no transaction is active. If the current query is the first of its transaction, this column is equal to the
     <code class="structfield">
      query_start
     </code>
     column.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      query_start
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Time when the currently active query was started, or if
     <code class="structfield">
      state
     </code>
     is not
     <code class="literal">
      active
     </code>
     , when the last query was started
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      state_change
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Time when the
     <code class="structfield">
      state
     </code>
     was last changed
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      wait_event_type
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     The type of event for which the backend is waiting, if any; otherwise NULL.  See
     <a class="xref" href="monitoring-stats.md#WAIT-EVENT-TABLE" title="Table 27.4. Wait Event Types">
      Table 27.4
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      wait_event
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Wait event name if backend is currently waiting, otherwise NULL. See
     <a class="xref" href="monitoring-stats.md#WAIT-EVENT-ACTIVITY-TABLE" title="Table 27.5. Wait Events of Type Activity">
      Table 27.5
     </a>
     through
     <a class="xref" href="monitoring-stats.md#WAIT-EVENT-TIMEOUT-TABLE" title="Table 27.13. Wait Events of Type Timeout">
      Table 27.13
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      state
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Current overall state of this backend. Possible values are:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        <code class="literal">
         starting
        </code>
        : The backend is in initial startup. Client authentication is performed during this phase.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         active
        </code>
        : The backend is executing a query.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         idle
        </code>
        : The backend is waiting for a new client command.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         idle in transaction
        </code>
        : The backend is in a transaction, but is not currently executing a query.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         idle in transaction (aborted)
        </code>
        : This state is similar to
        <code class="literal">
         idle in transaction
        </code>
        , except one of the statements in the transaction caused an error.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         fastpath function call
        </code>
        : The backend is executing a fast-path function.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         disabled
        </code>
        : This state is reported if
        <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-ACTIVITIES">
         track_activities
        </a>
        is disabled in this backend.
       </p>
      </li>
     </ul>
    </div>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      backend_xid
     </code>
     <code class="type">
      xid
     </code>
    </p>
    <p>
     Top-level transaction identifier of this backend, if any;  see
     <a class="xref" href="transaction-id.md" title="67.1. Transactions and Identifiers">
      Section 67.1
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      backend_xmin
     </code>
     <code class="type">
      xid
     </code>
    </p>
    <p>
     The current backend's
     <code class="literal">
      xmin
     </code>
     horizon.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      query_id
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Identifier of this backend's most recent query. If
     <code class="structfield">
      state
     </code>
     is
     <code class="literal">
      active
     </code>
     this field shows the identifier of the currently executing query. In all other states, it shows the identifier of last query that was executed.  Query identifiers are not computed by default so this field will be null unless
     <a class="xref" href="runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID">
      compute_query_id
     </a>
     parameter is enabled or a third-party module that computes query identifiers is configured.
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
     Text of this backend's most recent query. If
     <code class="structfield">
      state
     </code>
     is
     <code class="literal">
      active
     </code>
     this field shows the currently executing query. In all other states, it shows the last query that was executed. By default the query text is truncated at 1024 bytes; this value can be changed via the parameter
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-ACTIVITY-QUERY-SIZE">
      track_activity_query_size
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      backend_type
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Type of current backend. Possible types are
     <code class="literal">
      autovacuum launcher
     </code>
     ,
     <code class="literal">
      autovacuum worker
     </code>
     ,
     <code class="literal">
      logical replication launcher
     </code>
     ,
     <code class="literal">
      logical replication worker
     </code>
     ,
     <code class="literal">
      parallel worker
     </code>
     ,
     <code class="literal">
      background writer
     </code>
     ,
     <code class="literal">
      client backend
     </code>
     ,
     <code class="literal">
      checkpointer
     </code>
     ,
     <code class="literal">
      archiver
     </code>
     ,
     <code class="literal">
      standalone backend
     </code>
     ,
     <code class="literal">
      startup
     </code>
     ,
     <code class="literal">
      walreceiver
     </code>
     ,
     <code class="literal">
      walsender
     </code>
     ,
     <code class="literal">
      walwriter
     </code>
     and
     <code class="literal">
      walsummarizer
     </code>
     . In addition, background workers registered by extensions may have additional types.
    </p>
   </td>
  </tr>
 </tbody>
</table>










Nota

As colunas `wait_event` e `state` são independentes. Se um backend estiver no estado `active`, ele pode ou não ser `waiting` em algum evento. Se o estado for `active` e `wait_event` não for nulo, isso significa que uma consulta está sendo executada, mas está sendo bloqueada em algum lugar do sistema. Para manter o overhead de relatórios baixo, o sistema não tenta sincronizar diferentes aspectos dos dados de atividade para um backend. Como resultado, podem existir discrepâncias efêmeras entre as colunas da visão.

**Tabela 27.4. Tipos de evento de espera**



<table border="1" class="table" summary="Wait Event Types">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Wait Event Type
   </th>
   <th>
    Description
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     Activity
    </code>
   </td>
   <td>
    The server process is idle.  This event type indicates a process waiting for activity in its main processing loop.
    <code class="literal">
     wait_event
    </code>
    will identify the specific wait point; see
    <a class="xref" href="monitoring-stats.md#WAIT-EVENT-ACTIVITY-TABLE" title="Table 27.5. Wait Events of Type Activity">
     Table 27.5
    </a>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BufferPin
    </code>
   </td>
   <td>
    The server process is waiting for exclusive access to a data buffer.  Buffer pin waits can be protracted if another process holds an open cursor that last read data from the buffer in question. See
    <a class="xref" href="monitoring-stats.md#WAIT-EVENT-BUFFERPIN-TABLE" title="Table 27.6. Wait Events of Type Bufferpin">
     Table 27.6
    </a>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     Client
    </code>
   </td>
   <td>
    The server process is waiting for activity on a socket connected to a user application.  Thus, the server expects something to happen that is independent of its internal processes.
    <code class="literal">
     wait_event
    </code>
    will identify the specific wait point; see
    <a class="xref" href="monitoring-stats.md#WAIT-EVENT-CLIENT-TABLE" title="Table 27.7. Wait Events of Type Client">
     Table 27.7
    </a>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     Extension
    </code>
   </td>
   <td>
    The server process is waiting for some condition defined by an extension module. See
    <a class="xref" href="monitoring-stats.md#WAIT-EVENT-EXTENSION-TABLE" title="Table 27.8. Wait Events of Type Extension">
     Table 27.8
    </a>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     InjectionPoint
    </code>
   </td>
   <td>
    The server process is waiting for an injection point to reach an outcome defined in a test.  See
    <a class="xref" href="xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS" title="36.10.14. Injection Points">
     Section 36.10.14
    </a>
    for more details.  This type has no predefined wait points.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     IO
    </code>
   </td>
   <td>
    The server process is waiting for an I/O operation to complete.
    <code class="literal">
     wait_event
    </code>
    will identify the specific wait point; see
    <a class="xref" href="monitoring-stats.md#WAIT-EVENT-IO-TABLE" title="Table 27.9. Wait Events of Type Io">
     Table 27.9
    </a>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     IPC
    </code>
   </td>
   <td>
    The server process is waiting for some interaction with another server process.
    <code class="literal">
     wait_event
    </code>
    will identify the specific wait point; see
    <a class="xref" href="monitoring-stats.md#WAIT-EVENT-IPC-TABLE" title="Table 27.10. Wait Events of Type Ipc">
     Table 27.10
    </a>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     Lock
    </code>
   </td>
   <td>
    The server process is waiting for a heavyweight lock. Heavyweight locks, also known as lock manager locks or simply locks, primarily protect SQL-visible objects such as tables.  However, they are also used to ensure mutual exclusion for certain internal operations such as relation extension.
    <code class="literal">
     wait_event
    </code>
    will identify the type of lock awaited; see
    <a class="xref" href="monitoring-stats.md#WAIT-EVENT-LOCK-TABLE" title="Table 27.11. Wait Events of Type Lock">
     Table 27.11
    </a>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LWLock
    </code>
   </td>
   <td>
    The server process is waiting for a lightweight lock. Most such locks protect a particular data structure in shared memory.
    <code class="literal">
     wait_event
    </code>
    will contain a name identifying the purpose of the lightweight lock.  (Some locks have specific names; others are part of a group of locks each with a similar purpose.) See
    <a class="xref" href="monitoring-stats.md#WAIT-EVENT-LWLOCK-TABLE" title="Table 27.12. Wait Events of Type Lwlock">
     Table 27.12
    </a>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     Timeout
    </code>
   </td>
   <td>
    The server process is waiting for a timeout to expire.
    <code class="literal">
     wait_event
    </code>
    will identify the specific wait point; see
    <a class="xref" href="monitoring-stats.md#WAIT-EVENT-TIMEOUT-TABLE" title="Table 27.13. Wait Events of Type Timeout">
     Table 27.13
    </a>
    .
   </td>
  </tr>
 </tbody>
</table>










**Tabela 27.5. Eventos de espera do tipo `Activity`**



<table border="1" class="table" summary="Wait Events of Type Activity">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    <code class="literal">
     Activity
    </code>
    Wait Event
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     ArchiverMain
    </code>
   </td>
   <td>
    Esperando no loop principal do processo do arqiver.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     AutovacuumMain
    </code>
   </td>
   <td>
    Esperando no loop principal do processo de inicializador de autovacuum.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BgwriterHibernate
    </code>
   </td>
   <td>
    Esperando no processo de escritor de fundo, hibernando.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BgwriterMain
    </code>
   </td>
   <td>
    Esperando no loop principal do processo de escritor de fundo.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     CheckpointerMain
    </code>
   </td>
   <td>
    Esperando no loop principal do processo de checkpointer.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     CheckpointerShutdown
    </code>
   </td>
   <td>
    Esperando que o processo de verificação seja concluído.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     IoWorkerMain
    </code>
   </td>
   <td>
    Esperando no loop principal do processo do trabalhador de E/S.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LogicalApplyMain
    </code>
   </td>
   <td>
    Aguardar no loop principal do processo de replicação lógica.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LogicalLauncherMain
    </code>
   </td>
   <td>
    Esperando no loop principal do processo de inicializador de replicação lógica.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LogicalParallelApplyMain
    </code>
   </td>
   <td>
    Esperando no loop principal do processo de aplicação paralela de replicação lógica.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     RecoveryWalStream
    </code>
   </td>
   <td>
    Esperando no loop principal do processo de inicialização para o WAL chegar, durante a recuperação de streaming.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ReplicationSlotsyncMain
    </code>
   </td>
   <td>
    Esperando no loop principal do trabalhador de sincronização de slot.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ReplicationSlotsyncShutdown
    </code>
   </td>
   <td>
    Esperando que o trabalhador de sincronização de intervalo seja desligado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SysloggerMain
    </code>
   </td>
   <td>
    Esperando no loop principal do processo syslogger.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalReceiverMain
    </code>
   </td>
   <td>
    Esperando no loop principal do processo do receptor WAL.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalSenderMain
    </code>
   </td>
   <td>
    Esperando no loop principal do processo de emissor WAL.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalSummarizerWal
    </code>
   </td>
   <td>
    Esperando no sumidor WAL para mais WAL serem gerados.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalWriterMain
    </code>
   </td>
   <td>
    Esperando no loop principal do processo de escritor WAL.
   </td>
  </tr>
 </tbody>
</table>










**Tabela 27.6. Eventos de espera do tipo `Bufferpin`**



<table border="1" class="table" summary="Wait Events of Type Bufferpin">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    <code class="literal">
     BufferPin
    </code>
    Wait Event
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     BufferPin
    </code>
   </td>
   <td>
    Esperando adquirir um pino exclusivo em um buffer.
   </td>
  </tr>
 </tbody>
</table>










**Tabela 27.7. Eventos de espera do tipo `Client`**



<table border="1" class="table" summary="Wait Events of Type Client">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    <code class="literal">
     Client
    </code>
    Wait Event
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     ClientRead
    </code>
   </td>
   <td>
    Esperando ler dados do cliente.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ClientWrite
    </code>
   </td>
   <td>
    Esperando para escrever dados para o cliente.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     GssOpenServer
    </code>
   </td>
   <td>
    Esperando ler dados do cliente enquanto estabelece uma sessão GSSAPI.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LibpqwalreceiverConnect
    </code>
   </td>
   <td>
    Esperando no receptor WAL para estabelecer conexão com o servidor remoto.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LibpqwalreceiverReceive
    </code>
   </td>
   <td>
    Esperando no receptor WAL para receber dados do servidor remoto.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SslOpenServer
    </code>
   </td>
   <td>
    Esperando SSL enquanto tenta conexão.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WaitForStandbyConfirmation
    </code>
   </td>
   <td>
    Esperando que o WAL seja recebido e descartado pelo standby físico.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalSenderWaitForWal
    </code>
   </td>
   <td>
    Esperando que o WAL seja descartado no processo de emissor de WAL.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalSenderWriteData
    </code>
   </td>
   <td>
    Esperar por qualquer atividade ao processar respostas do receptor WAL no processo de emissor WAL.
   </td>
  </tr>
 </tbody>
</table>










**Tabela 27.8. Eventos de espera do tipo `Extension`**



<table border="1" class="table" summary="Wait Events of Type Extension">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    <code class="literal">
     Extension
    </code>
    Wait Event
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     Extension
    </code>
   </td>
   <td>
    Esperando em uma extensão.
   </td>
  </tr>
 </tbody>
</table>










**Tabela 27.9. Eventos de espera do tipo `Io`**



<table border="1" class="table" summary="Wait Events of Type Io">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    <code class="literal">
     IO
    </code>
    Wait Event
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     AioIoCompletion
    </code>
   </td>
   <td>
    Esperando que outro processo complete a IO.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     AioIoUringExecution
    </code>
   </td>
   <td>
    Esperando a execução de IO via io_uring.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     AioIoUringSubmit
    </code>
   </td>
   <td>
    Esperando a submissão de IO via io_uring.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BasebackupRead
    </code>
   </td>
   <td>
    Esperando que o backup de base leia de um arquivo.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BasebackupSync
    </code>
   </td>
   <td>
    Esperando que os dados escritos por um backup de base atinjam armazenamento durável.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BasebackupWrite
    </code>
   </td>
   <td>
    Esperando que o backup de base escreva em um arquivo.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BuffileRead
    </code>
   </td>
   <td>
    Esperando uma leitura de um arquivo armazenado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BuffileTruncate
    </code>
   </td>
   <td>
    Esperando que um arquivo armazenado seja truncado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BuffileWrite
    </code>
   </td>
   <td>
    Esperando uma escrita em um arquivo armazenado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ControlFileRead
    </code>
   </td>
   <td>
    Esperando uma leitura do
    <code class="filename">
     pg_control
    </code>
    file.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ControlFileSync
    </code>
   </td>
   <td>
    Esperando pelo
    <code class="filename">
     pg_control
    </code>
    arquivo para alcançar armazenamento durável.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ControlFileSyncUpdate
    </code>
   </td>
   <td>
    Esperando por uma atualização para o
    <code class="filename">
     pg_control
    </code>
    arquivo para alcançar armazenamento durável.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ControlFileWrite
    </code>
   </td>
   <td>
    Esperando uma escrita para o
    <code class="filename">
     pg_control
    </code>
    file.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ControlFileWriteUpdate
    </code>
   </td>
   <td>
    Esperando por uma atualização para atualizar
    <code class="filename">
     pg_control
    </code>
    file.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     CopyFileCopy
    </code>
   </td>
   <td>
    Esperando por uma operação de cópia de arquivo.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     CopyFileRead
    </code>
   </td>
   <td>
    Esperando por uma leitura durante uma operação de cópia de arquivo.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     CopyFileWrite
    </code>
   </td>
   <td>
    Esperando por uma escrita durante uma operação de cópia de arquivo.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     DataFileExtend
    </code>
   </td>
   <td>
    Esperando que o arquivo de dados de relacionamento seja estendido.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     DataFileFlush
    </code>
   </td>
   <td>
    Esperando que um arquivo de dados de relacionamento atinja armazenamento durável.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     DataFileImmediateSync
    </code>
   </td>
   <td>
    Esperando uma sincronização imediata de um arquivo de dados de relação para armazenamento durável.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     DataFilePrefetch
    </code>
   </td>
   <td>
    Esperando por um pré-pré-visualização assíncrona de um arquivo de dados de relação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     DataFileRead
    </code>
   </td>
   <td>
    Esperando uma leitura de um arquivo de dados de relação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     DataFileSync
    </code>
   </td>
   <td>
    Esperando que os dados de uma relação atinjam o armazenamento permanente.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     DataFileTruncate
    </code>
   </td>
   <td>
    Esperando que um arquivo de dados de relação seja truncado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     DataFileWrite
    </code>
   </td>
   <td>
    Esperando uma escrita em um arquivo de dados de relacionamento.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     DsmAllocate
    </code>
   </td>
   <td>
    Esperando que um segmento de memória compartilhada dinâmica seja alocado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     DsmFillZeroWrite
    </code>
   </td>
   <td>
    Esperando preencher um arquivo de suporte de memória compartilhada dinâmica com zeros.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LockFileAddtodatadirRead
    </code>
   </td>
   <td>
    Esperando por uma leitura enquanto adiciona uma linha ao arquivo de bloqueio do diretório de dados.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LockFileAddtodatadirSync
    </code>
   </td>
   <td>
    Esperando que os dados atinjam o armazenamento permanente enquanto adiciona uma linha ao arquivo de bloqueio do diretório de dados.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LockFileAddtodatadirWrite
    </code>
   </td>
   <td>
    Esperando por uma escrita enquanto adiciona uma linha ao arquivo de bloqueio do diretório de dados.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LockFileCreateRead
    </code>
   </td>
   <td>
    Esperando para ler enquanto cria o arquivo de bloqueio do diretório de dados.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LockFileCreateSync
    </code>
   </td>
   <td>
    Esperando que os dados atinjam o armazenamento permanente enquanto cria o arquivo de bloqueio do diretório de dados.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LockFileCreateWrite
    </code>
   </td>
   <td>
    Esperando por uma escrita enquanto cria o arquivo de bloqueio do diretório de dados.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LockFileRecheckdatadirRead
    </code>
   </td>
   <td>
    Esperando por uma leitura durante a revalidação do arquivo de bloqueio do diretório de dados.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LogicalRewriteCheckpointSync
    </code>
   </td>
   <td>
    Esperando que as correspondências de reescrita lógica atinjam o armazenamento durável durante um ponto de verificação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LogicalRewriteMappingSync
    </code>
   </td>
   <td>
    Esperando que os dados de mapeamento atinjam armazenamento durável durante uma reescrita lógica.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LogicalRewriteMappingWrite
    </code>
   </td>
   <td>
    Esperando por uma gravação de dados de mapeamento durante uma reescrita lógica.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LogicalRewriteSync
    </code>
   </td>
   <td>
    Esperando que as mapearizações de reescrita lógica alcancem armazenamento durável.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LogicalRewriteTruncate
    </code>
   </td>
   <td>
    Esperando por o mapeamento de dados ser truncado durante uma reescrita lógica.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LogicalRewriteWrite
    </code>
   </td>
   <td>
    Esperando por uma descrição de mapeamentos de reescrita lógica.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     RelationMapRead
    </code>
   </td>
   <td>
    Esperando uma leitura do arquivo de mapa de relações.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     RelationMapReplace
    </code>
   </td>
   <td>
    Esperando substituição durável de um arquivo de mapa de relação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     RelationMapWrite
    </code>
   </td>
   <td>
    Esperando uma escrita no arquivo do mapa de relações.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ReorderBufferRead
    </code>
   </td>
   <td>
    Esperando uma leitura durante a gestão do buffer de reordenação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ReorderBufferWrite
    </code>
   </td>
   <td>
    Esperando por uma escrita durante a gestão do buffer de reordenação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ReorderLogicalMappingRead
    </code>
   </td>
   <td>
    Esperando por uma leitura de mapeamento lógico durante a gestão do buffer de reordenação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ReplicationSlotRead
    </code>
   </td>
   <td>
    Esperando por uma leitura de um arquivo de controle de slot de replicação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ReplicationSlotRestoreSync
    </code>
   </td>
   <td>
    Esperando que o arquivo de controle de slot de replicação atinja o armazenamento durável enquanto o restaura à memória.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ReplicationSlotSync
    </code>
   </td>
   <td>
    Esperando que o arquivo de controle de slot de replicação atinja o armazenamento durável.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ReplicationSlotWrite
    </code>
   </td>
   <td>
    Esperando por uma escrita em um arquivo de controle de slot de replicação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SlruFlushSync
    </code>
   </td>
   <td>
    Esperando que os dados do SLRU atinjam armazenamento durável durante um ponto de verificação ou desligamento do banco de dados.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SlruRead
    </code>
   </td>
   <td>
    Esperando uma leitura de uma página do SLRU.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SlruSync
    </code>
   </td>
   <td>
    Esperando que os dados do SLRU atinjam armazenamento durável após a escrita de uma página.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SlruWrite
    </code>
   </td>
   <td>
    Esperando por uma escrita de uma página SLRU.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SnapbuildRead
    </code>
   </td>
   <td>
    Esperando por uma leitura de um instantâneo de catálogo histórico serializado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SnapbuildSync
    </code>
   </td>
   <td>
    Esperando que um instantâneo serializado do catálogo histórico atinja o armazenamento durável.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SnapbuildWrite
    </code>
   </td>
   <td>
    Esperando por uma descrição de um instantâneo de catálogo histórico serializado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     TimelineHistoryFileSync
    </code>
   </td>
   <td>
    Esperando que um arquivo de histórico de cronologia recebido por replicação em streaming atinja armazenamento durável.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     TimelineHistoryFileWrite
    </code>
   </td>
   <td>
    Esperando por uma gravação de um arquivo de histórico de cronologia recebida por replicação em streaming.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     TimelineHistoryRead
    </code>
   </td>
   <td>
    Esperando uma leitura de um arquivo de histórico de linha do tempo.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     TimelineHistorySync
    </code>
   </td>
   <td>
    Esperando que o arquivo de histórico de linha do tempo recém-criado atinja o armazenamento durável.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     TimelineHistoryWrite
    </code>
   </td>
   <td>
    Esperando por uma gravação de um arquivo de histórico de linha do tempo recém-criado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     TwophaseFileRead
    </code>
   </td>
   <td>
    Esperando uma leitura de um arquivo de estado de duas fases.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     TwophaseFileSync
    </code>
   </td>
   <td>
    Esperando que um arquivo de estado de duas fases atinja armazenamento durável.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     TwophaseFileWrite
    </code>
   </td>
   <td>
    Esperando por uma escrita de um arquivo de estado de duas fases.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     VersionFileSync
    </code>
   </td>
   <td>
    Esperando que o arquivo de versão atinja o armazenamento durável enquanto cria um banco de dados.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     VersionFileWrite
    </code>
   </td>
   <td>
    Esperando que o arquivo de versão seja escrito durante a criação de um banco de dados.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalsenderTimelineHistoryRead
    </code>
   </td>
   <td>
    Esperando por uma leitura de um arquivo de histórico de linha de tempo durante um comando de linha de tempo walsender.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalBootstrapSync
    </code>
   </td>
   <td>
    Esperando que o WAL atinja armazenamento durável durante o bootstrapping.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalBootstrapWrite
    </code>
   </td>
   <td>
    Esperando por uma escrita de uma página WAL durante o arranque.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalCopyRead
    </code>
   </td>
   <td>
    Esperando por uma leitura ao criar um novo segmento WAL ao copiar um existente.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalCopySync
    </code>
   </td>
   <td>
    Esperando por um novo segmento WAL criado copiando um segmento existente para alcançar armazenamento durável.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalCopyWrite
    </code>
   </td>
   <td>
    Esperar por uma escrita ao criar um novo segmento WAL ao copiar um existente.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalInitSync
    </code>
   </td>
   <td>
    Esperando que o arquivo WAL recém-inicializado atinja o armazenamento durável.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalInitWrite
    </code>
   </td>
   <td>
    Esperando por uma escrita enquanto inicializa um novo arquivo WAL.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalRead
    </code>
   </td>
   <td>
    Esperando uma leitura de um arquivo WAL.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalSummaryRead
    </code>
   </td>
   <td>
    Esperando uma leitura de um arquivo de resumo WAL.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalSummaryWrite
    </code>
   </td>
   <td>
    Esperando uma escrita em um arquivo de resumo WAL.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalSync
    </code>
   </td>
   <td>
    Esperando que o arquivo WAL atinja o armazenamento durável.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalSyncMethodAssign
    </code>
   </td>
   <td>
    Esperando que os dados atinjam o armazenamento permanente enquanto se atribui um novo método de sincronização WAL.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalWrite
    </code>
   </td>
   <td>
    Esperando uma escrita em um arquivo WAL.
   </td>
  </tr>
 </tbody>
</table>










**Tabela 27.10. Eventos de espera do tipo `Ipc`**



<table border="1" class="table" summary="Wait Events of Type Ipc">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    <code class="literal">
     IPC
    </code>
    Wait Event
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     AppendReady
    </code>
   </td>
   <td>
    Esperando por nós de subplano de um
    <code class="literal">
     Append
    </code>
    O nó do plano estará pronto.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ArchiveCleanupCommand
    </code>
   </td>
   <td>
    Esperando por
    <a class="xref" href="runtime-config-wal.md#GUC-ARCHIVE-CLEANUP-COMMAND">
     archive_cleanup_command
    </a>
    para completar.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ArchiveCommand
    </code>
   </td>
   <td>
    Esperando por
    <a class="xref" href="runtime-config-wal.md#GUC-ARCHIVE-COMMAND">
     archive_command
    </a>
    para completar.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BackendTermination
    </code>
   </td>
   <td>
    Esperando pelo término de outro backend.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BackupWaitWalArchive
    </code>
   </td>
   <td>
    Esperando por arquivos WAL necessários para que o backup seja arquivado com sucesso.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BgworkerShutdown
    </code>
   </td>
   <td>
    Esperando que o trabalhador de fundo seja desligado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BgworkerStartup
    </code>
   </td>
   <td>
    Esperando que o trabalhador de fundo comece.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BtreePage
    </code>
   </td>
   <td>
    Esperando que o número da página necessário para continuar um varredura em árvore B paralela esteja disponível.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BufferIo
    </code>
   </td>
   <td>
    Esperando que o I/O de buffer seja concluído.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     CheckpointDelayComplete
    </code>
   </td>
   <td>
    Esperando por um backend que bloqueie a conclusão de um ponto de verificação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     CheckpointDelayStart
    </code>
   </td>
   <td>
    Esperando por um backend que bloqueie o início de um ponto de verificação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     CheckpointDone
    </code>
   </td>
   <td>
    Esperando que um ponto de controle seja concluído.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     CheckpointStart
    </code>
   </td>
   <td>
    Esperando que o posto de controle comece.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ExecuteGather
    </code>
   </td>
   <td>
    Esperando por atividade de um processo de criança enquanto executa um
    <code class="literal">
     Gather
    </code>
    nó do plano.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     HashBatchAllocate
    </code>
   </td>
   <td>
    Esperando que um participante Paralelo Hash eleito aloje uma tabela de hash.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     HashBatchElect
    </code>
   </td>
   <td>
    Esperando eleger um participante do Hash Paralelo para alocar uma tabela de hash.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     HashBatchLoad
    </code>
   </td>
   <td>
    Esperando que outros participantes do Hash Paralelo terminem de carregar uma tabela de hash.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     HashBuildAllocate
    </code>
   </td>
   <td>
    Esperando que um participante Paralelo Hash eleito aloje a tabela de hash inicial.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     HashBuildElect
    </code>
   </td>
   <td>
    Esperando eleger um participante do Hash Paralelo para alocar a tabela de hash inicial.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     HashBuildHashInner
    </code>
   </td>
   <td>
    Esperando que outros participantes do Hash Paralelo terminem de hashar a relação interna.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     HashBuildHashOuter
    </code>
   </td>
   <td>
    Esperando que outros participantes do Hash Paralelo terminem a partição da relação externa.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     HashGrowBatchesDecide
    </code>
   </td>
   <td>
    Esperando eleger um participante do Hash Paralelo para decidir sobre o crescimento do próximo lote.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     HashGrowBatchesElect
    </code>
   </td>
   <td>
    Esperando eleger um participante do Hash Paralelo para alocar mais lotes.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     HashGrowBatchesFinish
    </code>
   </td>
   <td>
    Esperando que um participante do Hash Paralelo eleito decida sobre o crescimento do próximo lote.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     HashGrowBatchesReallocate
    </code>
   </td>
   <td>
    Esperando que um participante do Hash Paralelo eleito aloje mais lotes.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     HashGrowBatchesRepartition
    </code>
   </td>
   <td>
    Esperando que outros participantes do Hash Paralelo terminem a redistribuição.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     HashGrowBucketsElect
    </code>
   </td>
   <td>
    Esperando eleger um participante do Hash Paralelo para alocar mais buckets.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     HashGrowBucketsReallocate
    </code>
   </td>
   <td>
    Esperando que um participante do Hash Paralelo eleito termine a alocação de mais buckets.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     HashGrowBucketsReinsert
    </code>
   </td>
   <td>
    Esperando que outros participantes do Hash Paralelo terminem de inserir tuplas em novos buckets.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LogicalApplySendData
    </code>
   </td>
   <td>
    Esperar que um líder de replicação lógica aplique o processo para enviar dados para um processo de aplicação paralela.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LogicalParallelApplyStateChange
    </code>
   </td>
   <td>
    Esperando por um processo de aplicação paralela de replicação lógica para alterar o estado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LogicalSyncData
    </code>
   </td>
   <td>
    Esperando por um servidor remoto de replicação lógica para enviar dados para a sincronização inicial da tabela.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LogicalSyncStateChange
    </code>
   </td>
   <td>
    Esperando por um servidor remoto de replicação lógica para mudar de estado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     MessageQueueInternal
    </code>
   </td>
   <td>
    Esperando que outro processo seja anexado a uma fila de mensagens compartilhada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     MessageQueuePutMessage
    </code>
   </td>
   <td>
    Esperando para escrever uma mensagem de protocolo em uma fila de mensagens compartilhada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     MessageQueueReceive
    </code>
   </td>
   <td>
    Esperando receber bytes de uma fila de mensagens compartilhada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     MessageQueueSend
    </code>
   </td>
   <td>
    Esperando enviar bytes para uma fila de mensagens compartilhada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     MultixactCreation
    </code>
   </td>
   <td>
    Esperando por uma criação multixact para ser concluída.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ParallelBitmapScan
    </code>
   </td>
   <td>
    Esperando que a varredura de bitmap paralela seja inicializada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ParallelCreateIndexScan
    </code>
   </td>
   <td>
    Esperando em paralelo
    <code class="command">
     CREATE INDEX
    </code>
    trabalhadores para finalizar a varredura do monte.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ParallelFinish
    </code>
   </td>
   <td>
    Esperando que os trabalhadores paralelos terminem de calcular.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ProcarrayGroupUpdate
    </code>
   </td>
   <td>
    Esperando que o líder do grupo confirme o ID da transação no final da transação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ProcSignalBarrier
    </code>
   </td>
   <td>
    Esperando que um evento de barreira seja processado por todos os backends.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     Promote
    </code>
   </td>
   <td>
    Esperando promoção de standby.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     RecoveryConflictSnapshot
    </code>
   </td>
   <td>
    Esperando pela resolução do conflito de recuperação para uma limpeza a vácuo.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     RecoveryConflictTablespace
    </code>
   </td>
   <td>
    Esperando pela resolução de conflitos de recuperação para a eliminação de um tablespace.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     RecoveryEndCommand
    </code>
   </td>
   <td>
    Esperando por
    <a class="xref" href="runtime-config-wal.md#GUC-RECOVERY-END-COMMAND">
     recovery_end_command
    </a>
    para completar.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     RecoveryPause
    </code>
   </td>
   <td>
    Esperando que a recuperação seja retomada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ReplicationOriginDrop
    </code>
   </td>
   <td>
    Esperando que a origem de replicação se torne inativa para que possa ser descartada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ReplicationSlotDrop
    </code>
   </td>
   <td>
    Esperando que um slot de replicação se torne inativo para que possa ser descartado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     RestoreCommand
    </code>
   </td>
   <td>
    Esperando por
    <a class="xref" href="runtime-config-wal.md#GUC-RESTORE-COMMAND">
     restore_command
    </a>
    para completar.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SafeSnapshot
    </code>
   </td>
   <td>
    Esperando obter um instantâneo válido para um
    <code class="literal">
     READ ONLY DEFERRABLE
    </code>
    transaction.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SyncRep
    </code>
   </td>
   <td>
    Esperando confirmação de um servidor remoto durante a replicação sincronizada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalReceiverExit
    </code>
   </td>
   <td>
    Esperando que o receptor WAL saia.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalReceiverWaitStart
    </code>
   </td>
   <td>
    Esperando pelo processo de inicialização para enviar dados iniciais para replicação em streaming.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalSummaryReady
    </code>
   </td>
   <td>
    Esperando que um novo resumo do WAL seja gerado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     XactGroupUpdate
    </code>
   </td>
   <td>
    Esperando que o líder do grupo atualize o status da transação no final da transação.
   </td>
  </tr>
 </tbody>
</table>










**Tabela 27.11. Eventos de espera do tipo `Lock`**



<table border="1" class="table" summary="Wait Events of Type Lock">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    <code class="literal">
     Lock
    </code>
    Wait Event
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     advisory
    </code>
   </td>
   <td>
    Esperando adquirir um bloqueio de usuário consultor.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     applytransaction
    </code>
   </td>
   <td>
    Esperando adquirir um bloqueio em uma transação remota que está sendo aplicada por um assinante de replicação lógica.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     extend
    </code>
   </td>
   <td>
    Esperando estender uma relação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     frozenid
    </code>
   </td>
   <td>
    Esperando atualizar
    <code class="structname">
     pg_database
    </code>
    .
    <code class="structfield">
     datfrozenxid
    </code>
    e
    <code class="structname">
     pg_database
    </code>
    .
    <code class="structfield">
     datminmxid
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     object
    </code>
   </td>
   <td>
    Esperando adquirir um bloqueio em um objeto de banco de dados não relacionado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     page
    </code>
   </td>
   <td>
    Esperando adquirir um bloqueio em uma página de uma relação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     relation
    </code>
   </td>
   <td>
    Esperando adquirir um elo em uma relação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     spectoken
    </code>
   </td>
   <td>
    Esperando adquirir um bloqueio de inserção especulativa.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     transactionid
    </code>
   </td>
   <td>
    Esperando que a transação termine.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     tuple
    </code>
   </td>
   <td>
    Esperando adquirir um bloqueio em uma tupla.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     userlock
    </code>
   </td>
   <td>
    Esperando adquirir um bloqueio de usuário.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     virtualxid
    </code>
   </td>
   <td>
    Esperando adquirir um bloqueio de ID de transação virtual; veja
    <a class="xref" href="transaction-id.md" title="67.1. Transactions and Identifiers">
     Seção 67.1
    </a>
    .
   </td>
  </tr>
 </tbody>
</table>










**Tabela 27.12. Eventos de espera do tipo `Lwlock`**



<table border="1" class="table" summary="Wait Events of Type Lwlock">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    <code class="literal">
     LWLock
    </code>
    Wait Event
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     AddinShmemInit
    </code>
   </td>
   <td>
    Esperando gerenciar a alocação de espaço de uma extensão na memória compartilhada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     AioUringCompletion
    </code>
   </td>
   <td>
    Esperando que outro processo complete a IO via io_uring.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     AioWorkerSubmissionQueue
    </code>
   </td>
   <td>
    Esperando acessar a fila de submissão de trabalhadores AIO.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     AutoFile
    </code>
   </td>
   <td>
    Esperando atualizar o
    <code class="filename">
     postgresql.auto.conf
    </code>
    file.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     Autovacuum
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar o estado atual dos trabalhadores do autovacuum.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     AutovacuumSchedule
    </code>
   </td>
   <td>
    Esperando para garantir que uma tabela selecionada para autovacuum ainda precise ser vacumada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BackgroundWorker
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar o estado do trabalhador de fundo.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BtreeVacuum
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar informações relacionadas ao vácuo para um índice de árvore B.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BufferContent
    </code>
   </td>
   <td>
    Esperando acessar uma página de dados na memória.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     BufferMapping
    </code>
   </td>
   <td>
    Esperando associar um bloco de dados a um buffer no pool de buffers.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     CheckpointerComm
    </code>
   </td>
   <td>
    Esperando para gerenciar solicitações fsync.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     CommitTs
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar o último valor definido para um timestamp de comprovação de transação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     CommitTsBuffer
    </code>
   </td>
   <td>
    Esperando por I/O em um buffer de marcação de tempo SLRU.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     CommitTsSLRU
    </code>
   </td>
   <td>
    Esperando acessar o cache de marcação de tempo SLRU.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ControlFile
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar o
    <code class="filename">
     pg_control
    </code>
    arquivo ou crie um novo arquivo WAL.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     DSMRegistry
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar o registro de memória compartilhada dinâmica.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     DSMRegistryDSA
    </code>
   </td>
   <td>
    Esperando acessar o alocador de memória compartilhada dinâmica do registro de memória compartilhada dinâmica.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     DSMRegistryHash
    </code>
   </td>
   <td>
    Esperando acessar a tabela hash compartilhada do registro de memória compartilhada dinâmica.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     DynamicSharedMemoryControl
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar informações de alocação dinâmica de memória compartilhada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     InjectionPoint
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar informações relacionadas aos pontos de injeção.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LockFastPath
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar as informações de bloqueio de caminho rápido de um processo.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LockManager
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar informações sobre
    <span class="quote">
     “
     <span class="quote">
      pesado
     </span>
     ”
    </span>
    locks.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LogicalRepLauncherDSA
    </code>
   </td>
   <td>
    Esperando acessar o alocador de memória compartilhada dinâmica do lançador de replicação lógica.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LogicalRepLauncherHash
    </code>
   </td>
   <td>
    Esperando acessar a tabela de hash compartilhada do lançador de replicação lógica.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LogicalRepWorker
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar o estado dos trabalhadores de replicação lógica.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     MultiXactGen
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar o estado multixact compartilhado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     MultiXactMemberBuffer
    </code>
   </td>
   <td>
    Esperando por I/O em um buffer SLRU de membro multixact.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     MultiXactMemberSLRU
    </code>
   </td>
   <td>
    Esperando acessar o cache multixact do membro SLRU.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     MultiXactOffsetBuffer
    </code>
   </td>
   <td>
    Esperando por I/O em um buffer SLRU de múltiplos acasos.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     MultiXactOffsetSLRU
    </code>
   </td>
   <td>
    Esperando acessar o cache SLRU de multixact offset.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     MultiXactTruncation
    </code>
   </td>
   <td>
    Esperando para ler ou truncar informações multixact.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     NotifyBuffer
    </code>
   </td>
   <td>
    Esperando por I/O em um
    <code class="command">
     NOTIFY
    </code>
    mensagem SLRU buffer.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     NotifyQueue
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar
    <code class="command">
     NOTIFY
    </code>
    messages.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     NotifyQueueTail
    </code>
   </td>
   <td>
    Esperando para atualizar o limite
    <code class="command">
     NOTIFY
    </code>
    armazenamento de mensagens.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     NotifySLRU
    </code>
   </td>
   <td>
    Esperando acessar o
    <code class="command">
     NOTIFY
    </code>
    mensagem SLRU cache.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     OidGen
    </code>
   </td>
   <td>
    Esperando alocar um novo OID.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ParallelAppend
    </code>
   </td>
   <td>
    Esperando escolher o próximo subplano durante a execução do plano de Append paralelo.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ParallelBtreeScan
    </code>
   </td>
   <td>
    Esperando sincronizar os trabalhadores durante a execução do plano de varredura em árvore paralela.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ParallelHashJoin
    </code>
   </td>
   <td>
    Esperando sincronizar os trabalhadores durante a execução do plano de junção hash paralela.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ParallelQueryDSA
    </code>
   </td>
   <td>
    Esperando por alocação dinâmica de memória compartilhada de consulta paralela.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ParallelVacuumDSA
    </code>
   </td>
   <td>
    Esperando por alocação dinâmica de memória compartilhada de vácuo paralela.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     PerSessionDSA
    </code>
   </td>
   <td>
    Esperando por alocação dinâmica de memória compartilhada de consulta paralela.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     PerSessionRecordType
    </code>
   </td>
   <td>
    Esperando acessar as informações de uma consulta paralela sobre tipos compostos.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     PerSessionRecordTypmod
    </code>
   </td>
   <td>
    Esperando acessar as informações de uma consulta paralela sobre modificadores de tipo que identificam tipos de registro anônimos.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     PerXactPredicateList
    </code>
   </td>
   <td>
    Esperando acessar a lista de bloqueios preditivos mantidos pela transação serializável atual durante uma consulta paralela.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     PgStatsData
    </code>
   </td>
   <td>
    Esperando acesso aos dados de estatísticas de memória compartilhada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     PgStatsDSA
    </code>
   </td>
   <td>
    Esperando pelo acesso do alocador de memória compartilhada dinâmica de estatísticas.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     PgStatsHash
    </code>
   </td>
   <td>
    Esperando por estatísticas de acesso à tabela de hash de memória compartilhada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     PredicateLockManager
    </code>
   </td>
   <td>
    Esperando acessar as informações de bloqueio de predicado usadas por transações serializáveis.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ProcArray
    </code>
   </td>
   <td>
    Esperando acessar as estruturas de dados compartilhadas por processo (tipicamente, para obter um instantâneo ou relatar o ID de transação de uma sessão).
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     RelationMapping
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar um
    <code class="filename">
     pg_filenode.map
    </code>
    arquivo (usado para rastrear as atribuições do filenode de certos catálogos do sistema).
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     RelCacheInit
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar um
    <code class="filename">
     pg_internal.init
    </code>
    arquivo de inicialização do cache de relação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ReplicationOrigin
    </code>
   </td>
   <td>
    Aguardar para criar, descartar ou usar uma origem de replicação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ReplicationOriginState
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar o progresso de uma origem de replicação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ReplicationSlotAllocation
    </code>
   </td>
   <td>
    Esperando alocar ou liberar um slot de replicação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ReplicationSlotControl
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar o estado do slot de replicação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ReplicationSlotIO
    </code>
   </td>
   <td>
    Esperando por I/O em um slot de replicação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SerialBuffer
    </code>
   </td>
   <td>
    Esperando por I/O em um buffer SLRU de conflito de transação serializável.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SerialControl
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar compartilhado
    <code class="filename">
     pg_serial
    </code>
    state.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SerializableFinishedList
    </code>
   </td>
   <td>
    Esperando acessar a lista de transações serializáveis concluídas.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SerializablePredicateList
    </code>
   </td>
   <td>
    Esperando acessar a lista de bloqueios preditivos mantidos por transações serializáveis.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SerializableXactHash
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar informações sobre transações serializáveis.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SerialSLRU
    </code>
   </td>
   <td>
    Esperando acessar o cache SLRU de conflitos de transação serializável.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SharedTidBitmap
    </code>
   </td>
   <td>
    Esperando acessar um bitmap compartilhado TID durante uma varredura paralela de índice de bitmap.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SharedTupleStore
    </code>
   </td>
   <td>
    Esperando acessar um banco de tuplas compartilhado durante uma consulta paralela.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ShmemIndex
    </code>
   </td>
   <td>
    Esperando encontrar ou alocar espaço na memória compartilhada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SInvalRead
    </code>
   </td>
   <td>
    Esperando recuperar mensagens da fila de invalidação do catálogo compartilhado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SInvalWrite
    </code>
   </td>
   <td>
    Esperando adicionar uma mensagem à fila de invalidação do catálogo compartilhado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SubtransBuffer
    </code>
   </td>
   <td>
    Esperando por I/O em um buffer SLRU de subtransação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SubtransSLRU
    </code>
   </td>
   <td>
    Esperando acessar o cache de subtransação SLRU.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SyncRep
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar informações sobre o estado da replicação sincronizada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SyncScan
    </code>
   </td>
   <td>
    Esperando para selecionar a localização inicial de um varredura de tabela sincronizada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     TablespaceCreate
    </code>
   </td>
   <td>
    Esperando criar ou descartar um espaço de tabela.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     TwoPhaseState
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar o estado das transações preparadas.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WaitEventCustom
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar informações de eventos de espera personalizados.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WALBufMapping
    </code>
   </td>
   <td>
    Esperando substituir uma página nos buffers do WAL.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WALInsert
    </code>
   </td>
   <td>
    Esperando inserir dados WAL em um buffer de memória.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WALSummarizer
    </code>
   </td>
   <td>
    Esperando para ler ou atualizar o estado de resumo do WAL.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WALWrite
    </code>
   </td>
   <td>
    Esperando que os buffers de WAL sejam escritos no disco.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WrapLimitsVacuum
    </code>
   </td>
   <td>
    Esperando atualizar os limites de identificação de transações e consumo multixact.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     XactBuffer
    </code>
   </td>
   <td>
    Esperando por I/O em um buffer de status de transação SLRU.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     XactSLRU
    </code>
   </td>
   <td>
    Esperando acessar o cache de status de transação SLRU.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     XactTruncation
    </code>
   </td>
   <td>
    Esperando executar
    <code class="function">
     pg_xact_status
    </code>
    ou atualize o ID de transação mais antigo disponível.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     XidGen
    </code>
   </td>
   <td>
    Esperando alocar um novo ID de transação.
   </td>
  </tr>
 </tbody>
</table>










**Tabela 27.13. Eventos de espera do tipo `Timeout`**



<table border="1" class="table" summary="Wait Events of Type Timeout">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    <code class="literal">
     Timeout
    </code>
    Wait Event
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     BaseBackupThrottle
    </code>
   </td>
   <td>
    Esperar durante o backup de base quando a atividade é controlada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     CheckpointWriteDelay
    </code>
   </td>
   <td>
    Esperando entre os registros enquanto realiza um ponto de verificação.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     PgSleep
    </code>
   </td>
   <td>
    Esperando devido a uma chamada
    <code class="function">
     pg_sleep
    </code>
    ou uma função de irmão.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     RecoveryApplyDelay
    </code>
   </td>
   <td>
    Esperando aplicar o WAL durante a recuperação devido a um atraso de configuração.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     RecoveryRetrieveRetryInterval
    </code>
   </td>
   <td>
    Esperar durante a recuperação quando os dados do WAL não estão disponíveis em nenhuma fonte (
    <code class="filename">
     pg_wal
    </code>
    , arquivar ou transmitir).
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     RegisterSyncRequest
    </code>
   </td>
   <td>
    Esperando enquanto envia solicitações de sincronização para o checkpointer, porque a fila de solicitações está cheia.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SpinDelay
    </code>
   </td>
   <td>
    Esperar enquanto adquire um spinlock confiante.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     VacuumDelay
    </code>
   </td>
   <td>
    Esperando em um ponto de atraso em vácuo baseado em custo.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     VacuumTruncate
    </code>
   </td>
   <td>
    Esperando adquirir um bloqueio exclusivo para truncar quaisquer páginas vazias no final de uma tabela varrida.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WalSummarizerError
    </code>
   </td>
   <td>
    Esperando após um erro do resumidor WAL.
   </td>
  </tr>
 </tbody>
</table>










Aqui estão exemplos de como os eventos de espera podem ser visualizados:

```
SELECT pid, wait_event_type, wait_event FROM pg_stat_activity WHERE wait_event is NOT NULL;
 pid  | wait_event_type | wait_event
------+-----------------+------------
 2540 | Lock            | relation
 6644 | LWLock          | ProcArray
(2 rows)
```

```
SELECT a.pid, a.wait_event, w.description
  FROM pg_stat_activity a JOIN
       pg_wait_events w ON (a.wait_event_type = w.type AND
                            a.wait_event = w.name)
  WHERE a.wait_event is NOT NULL and a.state = 'active';
-[ RECORD 1 ]------------------------------------------------------​------------
pid         | 686674
wait_event  | WALInitSync
description | Waiting for a newly initialized WAL file to reach durable storage
```

Nota

As extensões podem adicionar os eventos `Extension`, `InjectionPoint` e `LWLock` às listas exibidas em [Tabela 27.8](monitoring-stats.md#WAIT-EVENT-EXTENSION-TABLE "Table 27.8. Wait Events of Type Extension") e [Tabela 27.12](monitoring-stats.md#WAIT-EVENT-LWLOCK-TABLE "Table 27.12. Wait Events of Type Lwlock"). Em alguns casos, o nome de um `LWLock` atribuído por uma extensão não estará disponível em todos os processos do servidor. Pode ser relatado apenas como “`extension`” em vez do nome atribuído pela extensão.

### 27.2.4. `pg_stat_replication` [#](#MONITORING-PG-STAT-REPLICATION-VIEW)

A visão `pg_stat_replication` conterá uma linha por processo de emissor WAL, mostrando estatísticas sobre a replicação para o servidor de standby conectado a esse emissor. Apenas os standby diretamente conectados estão listados; não há informações disponíveis sobre servidores de standby em cascata.

**Tabela 27.14. `pg_stat_replication` Visualização**



<table border="1" class="table" summary="pg_stat_replication View">
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
      pid
     </code>
     <code class="type">
      integer
     </code>
    </p>
    <p>
     Process ID of a WAL sender process
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      usesysid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     OID of the user logged into this WAL sender process
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      usename
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Name of the user logged into this WAL sender process
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      application_name
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Name of the application that is connected to this WAL sender
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      client_addr
     </code>
     <code class="type">
      inet
     </code>
    </p>
    <p>
     IP address of the client connected to this WAL sender. If this field is null, it indicates that the client is connected via a Unix socket on the server machine.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      client_hostname
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Host name of the connected client, as reported by a reverse DNS lookup of
     <code class="structfield">
      client_addr
     </code>
     . This field will only be non-null for IP connections, and only when
     <a class="xref" href="runtime-config-logging.md#GUC-LOG-HOSTNAME">
      log_hostname
     </a>
     is enabled.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      client_port
     </code>
     <code class="type">
      integer
     </code>
    </p>
    <p>
     TCP port number that the client is using for communication with this WAL sender, or
     <code class="literal">
      -1
     </code>
     if a Unix socket is used
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      backend_start
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Time when this process was started, i.e., when the client connected to this WAL sender
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      backend_xmin
     </code>
     <code class="type">
      xid
     </code>
    </p>
    <p>
     This standby's
     <code class="literal">
      xmin
     </code>
     horizon reported by
     <a class="xref" href="runtime-config-replication.md#GUC-HOT-STANDBY-FEEDBACK">
      hot_standby_feedback
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      state
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Current WAL sender state. Possible values are:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        <code class="literal">
         startup
        </code>
        : This WAL sender is starting up.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         catchup
        </code>
        : This WAL sender's connected standby is catching up with the primary.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         streaming
        </code>
        : This WAL sender is streaming changes after its connected standby server has caught up with the primary.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         backup
        </code>
        : This WAL sender is sending a backup.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         stopping
        </code>
        : This WAL sender is stopping.
       </p>
      </li>
     </ul>
    </div>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      sent_lsn
     </code>
     <code class="type">
      pg_lsn
     </code>
    </p>
    <p>
     Last write-ahead log location sent on this connection
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      write_lsn
     </code>
     <code class="type">
      pg_lsn
     </code>
    </p>
    <p>
     Last write-ahead log location written to disk by this standby server
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      flush_lsn
     </code>
     <code class="type">
      pg_lsn
     </code>
    </p>
    <p>
     Last write-ahead log location flushed to disk by this standby server
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      replay_lsn
     </code>
     <code class="type">
      pg_lsn
     </code>
    </p>
    <p>
     Last write-ahead log location replayed into the database on this standby server
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      write_lag
     </code>
     <code class="type">
      interval
     </code>
    </p>
    <p>
     Time elapsed between flushing recent WAL locally and receiving notification that this standby server has written it (but not yet flushed it or applied it).  This can be used to gauge the delay that
     <code class="literal">
      synchronous_commit
     </code>
     level
     <code class="literal">
      remote_write
     </code>
     incurred while committing if this server was configured as a synchronous standby.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      flush_lag
     </code>
     <code class="type">
      interval
     </code>
    </p>
    <p>
     Time elapsed between flushing recent WAL locally and receiving notification that this standby server has written and flushed it (but not yet applied it).  This can be used to gauge the delay that
     <code class="literal">
      synchronous_commit
     </code>
     level
     <code class="literal">
      on
     </code>
     incurred while committing if this server was configured as a synchronous standby.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      replay_lag
     </code>
     <code class="type">
      interval
     </code>
    </p>
    <p>
     Time elapsed between flushing recent WAL locally and receiving notification that this standby server has written, flushed and applied it.  This can be used to gauge the delay that
     <code class="literal">
      synchronous_commit
     </code>
     level
     <code class="literal">
      remote_apply
     </code>
     incurred while committing if this server was configured as a synchronous standby.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      sync_priority
     </code>
     <code class="type">
      integer
     </code>
    </p>
    <p>
     Priority of this standby server for being chosen as the synchronous standby in a priority-based synchronous replication. This has no effect in a quorum-based synchronous replication.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      sync_state
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Synchronous state of this standby server. Possible values are:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        <code class="literal">
         async
        </code>
        : This standby server is asynchronous.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         potential
        </code>
        : This standby server is now asynchronous, but can potentially become synchronous if one of current synchronous ones fails.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         sync
        </code>
        : This standby server is synchronous.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         quorum
        </code>
        : This standby server is considered as a candidate for quorum standbys.
       </p>
      </li>
     </ul>
    </div>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      reply_time
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Send time of last reply message received from standby server
    </p>
   </td>
  </tr>
 </tbody>
</table>










Os tempos de atraso relatados na visualização `pg_stat_replication` são medições do tempo necessário para que as WAL recentes sejam escritas, esvaziadas e reinterpretadas e para que o remetente saiba disso. Esses tempos representam o atraso de commit que foi (ou teria sido) introduzido por cada nível de commit sincronizado, se o servidor remoto fosse configurado como um standby sincronizado. Para um standby assíncrono, a coluna `replay_lag` aproxima o atraso antes das transações recentes se tornarem visíveis para consultas. Se o servidor de standby tiver completado totalmente o servidor de envio e não houver mais atividade de WAL, os tempos de atraso mais recentemente medidos continuarão a ser exibidos por um curto período e, em seguida, mostrarão NULL.

Os tempos de atraso funcionam automaticamente para a replicação física. Os plugins de decodificação lógica podem emitir mensagens de rastreamento opcionalmente; se não o fizerem, o mecanismo de rastreamento simplesmente exibirá NULL lag.

Nota

Os tempos de atraso relatados não são previsões de quanto tempo levará para o standby alcançar o servidor de envio, assumindo a taxa atual de replay. Um sistema desse tipo mostraria tempos semelhantes enquanto o novo WAL é gerado, mas diferiria quando o remetente fica inativo. Em particular, quando o standby alcança completamente o que foi relatado, `pg_stat_replication` mostra o tempo gasto para escrever, esvaziar e replayar a localização mais recente do WAL relatada, em vez de zero, como alguns usuários podem esperar. Isso é consistente com o objetivo de medir os atrasos de visibilidade de commit e transação síncrona para transações de escrita recentes. Para reduzir a confusão dos usuários que esperam um modelo diferente de atraso, as colunas de atraso retornam a NULL após um curto período em um sistema totalmente replayado e inativo. Os sistemas de monitoramento devem escolher se representar isso como dados ausentes, zero ou continuar a exibir o último valor conhecido.

### 27.2.5. `pg_stat_replication_slots` [#](#MONITORING-PG-STAT-REPLICATION-SLOTS-VIEW)

A visualização `pg_stat_replication_slots` conterá uma linha por slot de replicação lógica, exibindo estatísticas sobre seu uso.

**Tabela 27.15. `pg_stat_replication_slots` Visualização**



<table border="1" class="table" summary="pg_stat_replication_slots View">
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
      slot_name
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     A unique, cluster-wide identifier for the replication slot
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      spill_txns
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of transactions spilled to disk once the memory used by logical decoding to decode changes from WAL has exceeded
     <code class="literal">
      logical_decoding_work_mem
     </code>
     . The counter gets incremented for both top-level transactions and subtransactions.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      spill_count
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times transactions were spilled to disk while decoding changes from WAL for this slot. This counter is incremented each time a transaction is spilled, and the same transaction may be spilled multiple times.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      spill_bytes
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Amount of decoded transaction data spilled to disk while performing decoding of changes from WAL for this slot. This and other spill counters can be used to gauge the I/O which occurred during logical decoding and allow tuning
     <code class="literal">
      logical_decoding_work_mem
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      stream_txns
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of in-progress transactions streamed to the decoding output plugin after the memory used by logical decoding to decode changes from WAL for this slot has exceeded
     <code class="literal">
      logical_decoding_work_mem
     </code>
     . Streaming only works with top-level transactions (subtransactions can't be streamed independently), so the counter is not incremented for subtransactions.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      stream_count
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times in-progress transactions were streamed to the decoding output plugin while decoding changes from WAL for this slot. This counter is incremented each time a transaction is streamed, and the same transaction may be streamed multiple times.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      stream_bytes
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Amount of transaction data decoded for streaming in-progress transactions to the decoding output plugin while decoding changes from WAL for this slot. This and other streaming counters for this slot can be used to tune
     <code class="literal">
      logical_decoding_work_mem
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      total_txns
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of decoded transactions sent to the decoding output plugin for this slot. This counts top-level transactions only, and is not incremented for subtransactions. Note that this includes the transactions that are streamed and/or spilled.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      total_bytes
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Amount of transaction data decoded for sending transactions to the decoding output plugin while decoding changes from WAL for this slot. Note that this includes data that is streamed and/or spilled.
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
     Time at which these statistics were last reset
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.2.6. `pg_stat_wal_receiver` [#](#MONITORING-PG-STAT-WAL-RECEIVER-VIEW)

A vista `pg_stat_wal_receiver` conterá apenas uma linha, mostrando estatísticas sobre o receptor WAL do servidor conectado desse receptor.

**Tabela 27.16. `pg_stat_wal_receiver` Visualização**



<table border="1" class="table" summary="pg_stat_wal_receiver View">
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
      pid
     </code>
     <code class="type">
      integer
     </code>
    </p>
    <p>
     Process ID of the WAL receiver process
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      status
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Activity status of the WAL receiver process
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      receive_start_lsn
     </code>
     <code class="type">
      pg_lsn
     </code>
    </p>
    <p>
     First write-ahead log location used when WAL receiver is started
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      receive_start_tli
     </code>
     <code class="type">
      integer
     </code>
    </p>
    <p>
     First timeline number used when WAL receiver is started
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      written_lsn
     </code>
     <code class="type">
      pg_lsn
     </code>
    </p>
    <p>
     Last write-ahead log location already received and written to disk, but not flushed. This should not be used for data integrity checks.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      flushed_lsn
     </code>
     <code class="type">
      pg_lsn
     </code>
    </p>
    <p>
     Last write-ahead log location already received and flushed to disk, the initial value of this field being the first log location used when WAL receiver is started
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      received_tli
     </code>
     <code class="type">
      integer
     </code>
    </p>
    <p>
     Timeline number of last write-ahead log location received and flushed to disk, the initial value of this field being the timeline number of the first log location used when WAL receiver is started
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      last_msg_send_time
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Send time of last message received from origin WAL sender
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      last_msg_receipt_time
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Receipt time of last message received from origin WAL sender
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      latest_end_lsn
     </code>
     <code class="type">
      pg_lsn
     </code>
    </p>
    <p>
     Last write-ahead log location reported to origin WAL sender
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      latest_end_time
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Time of last write-ahead log location reported to origin WAL sender
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      slot_name
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Replication slot name used by this WAL receiver
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      sender_host
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Host of the
     <span class="productname">
      PostgreSQL
     </span>
     instance this WAL receiver is connected to. This can be a host name, an IP address, or a directory path if the connection is via Unix socket.  (The path case can be distinguished because it will always be an absolute path, beginning with
     <code class="literal">
      /
     </code>
     .)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      sender_port
     </code>
     <code class="type">
      integer
     </code>
    </p>
    <p>
     Port number of the
     <span class="productname">
      PostgreSQL
     </span>
     instance this WAL receiver is connected to.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      conninfo
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Connection string used by this WAL receiver, with security-sensitive fields obfuscated.
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.2.7. `pg_stat_recovery_prefetch` [#](#MONITORING-PG-STAT-RECOVERY-PREFETCH)

A visualização `pg_stat_recovery_prefetch` conterá apenas uma linha. As colunas `wal_distance`, `block_distance` e `io_depth` mostram os valores atuais, e as outras colunas mostram contadores acumulados que podem ser redefinidos com a função `pg_stat_reset_shared`.

**Tabela 27.17. `pg_stat_recovery_prefetch` Visualização**



<table border="1" class="table" summary="pg_stat_recovery_prefetch View">
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
      stats_reset
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Time at which these statistics were last reset
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      prefetch
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of blocks prefetched because they were not in the buffer pool
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      hit
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of blocks not prefetched because they were already in the buffer pool
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      skip_init
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of blocks not prefetched because they would be zero-initialized
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      skip_new
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of blocks not prefetched because they didn't exist yet
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      skip_fpw
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of blocks not prefetched because a full page image was included in the WAL
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      skip_rep
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of blocks not prefetched because they were already recently prefetched
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      wal_distance
     </code>
     <code class="type">
      int
     </code>
    </p>
    <p>
     How many bytes ahead the prefetcher is looking
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      block_distance
     </code>
     <code class="type">
      int
     </code>
    </p>
    <p>
     How many blocks ahead the prefetcher is looking
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      io_depth
     </code>
     <code class="type">
      int
     </code>
    </p>
    <p>
     How many prefetches have been initiated but are not yet known to have completed
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.2.8. `pg_stat_subscription` [#](#MONITORING-PG-STAT-SUBSCRIPTION)

**Tabela 27.18. `pg_stat_subscription` Visualização**



<table border="1" class="table" summary="pg_stat_subscription View">
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
      subid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     OID da assinatura
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      subname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome da assinatura
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      worker_type
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Tipo do processo de trabalho da assinatura. Os tipos possíveis são
     <code class="literal">
      apply
     </code>
     ,
     <code class="literal">
      parallel apply
     </code>
     , e
     <code class="literal">
      table synchronization
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      pid
     </code>
     <code class="type">
      integer
     </code>
    </p>
    <p>
     ID de processo da subscrição do processo do trabalhador
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      leader_pid
     </code>
     <code class="type">
      integer
     </code>
    </p>
    <p>
     ID de processo do líder aplique ao trabalhador se este processo for um trabalhador de aplicação em paralelo; NULL se este processo for um trabalhador de aplicação em líder ou um trabalhador de sincronização de tabela
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     OID da relação que o trabalhador está sincronizando; NULL para o líder aplique trabalhador e aplique paralelamente os trabalhadores
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      received_lsn
     </code>
     <code class="type">
      pg_lsn
     </code>
    </p>
    <p>
     Última localização do log de pré-escrita recebida, sendo o valor inicial deste campo 0; NULL para trabalhadores de aplicação paralela
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      last_msg_send_time
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Tempo da última mensagem recebida da origem do remetente WAL; NULL para aplicar trabalhadores em paralelo
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      last_msg_receipt_time
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Tempo de recebimento da última mensagem recebida do remetente de origem WAL; NULL para trabalhadores de aplicação paralela
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      latest_end_lsn
     </code>
     <code class="type">
      pg_lsn
     </code>
    </p>
    <p>
     Última localização do log de pré-escrita relatada ao remetente WAL de origem; NULL para trabalhadores de aplicação paralela
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      latest_end_time
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Tempo da última localização do log de pré-escrita relatada ao remetente WAL de origem; NULL para trabalhadores de aplicação paralela
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.2.9. `pg_stat_subscription_stats` [#](#MONITORING-PG-STAT-SUBSCRIPTION-STATS)

A visualização `pg_stat_subscription_stats` conterá uma linha por assinatura.

**Tabela 27.19. `pg_stat_subscription_stats` Visualização**



<table border="1" class="table" summary="pg_stat_subscription_stats View">
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
      subid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     OID of the subscription
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      subname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Name of the subscription
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      apply_error_count
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times an error occurred while applying changes. Note that any conflict resulting in an apply error will be counted in both
     <code class="literal">
      apply_error_count
     </code>
     and the corresponding conflict count (e.g.,
     <code class="literal">
      confl_*
     </code>
     ).
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      sync_error_count
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times an error occurred during the initial table synchronization
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confl_insert_exists
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times a row insertion violated a
     <code class="literal">
      NOT DEFERRABLE
     </code>
     unique constraint during the application of changes. See
     <a class="xref" href="logical-replication-conflicts.md#CONFLICT-INSERT-EXISTS">
      insert_exists
     </a>
     for details about this conflict.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confl_update_origin_differs
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times an update was applied to a row that had been previously modified by another source during the application of changes. See
     <a class="xref" href="logical-replication-conflicts.md#CONFLICT-UPDATE-ORIGIN-DIFFERS">
      update_origin_differs
     </a>
     for details about this conflict.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confl_update_exists
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times that an updated row value violated a
     <code class="literal">
      NOT DEFERRABLE
     </code>
     unique constraint during the application of changes. See
     <a class="xref" href="logical-replication-conflicts.md#CONFLICT-UPDATE-EXISTS">
      update_exists
     </a>
     for details about this conflict.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confl_update_missing
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times the tuple to be updated was not found during the application of changes. See
     <a class="xref" href="logical-replication-conflicts.md#CONFLICT-UPDATE-MISSING">
      update_missing
     </a>
     for details about this conflict.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confl_delete_origin_differs
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times a delete operation was applied to row that had been previously modified by another source during the application of changes. See
     <a class="xref" href="logical-replication-conflicts.md#CONFLICT-DELETE-ORIGIN-DIFFERS">
      delete_origin_differs
     </a>
     for details about this conflict.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confl_delete_missing
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times the tuple to be deleted was not found during the application of changes. See
     <a class="xref" href="logical-replication-conflicts.md#CONFLICT-DELETE-MISSING">
      delete_missing
     </a>
     for details about this conflict.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confl_multiple_unique_conflicts
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times a row insertion or an updated row values violated multiple
     <code class="literal">
      NOT DEFERRABLE
     </code>
     unique constraints during the application of changes. See
     <a class="xref" href="logical-replication-conflicts.md#CONFLICT-MULTIPLE-UNIQUE-CONFLICTS">
      multiple_unique_conflicts
     </a>
     for details about this conflict.
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
     Time at which these statistics were last reset
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.2.10. `pg_stat_ssl` [#](#MONITORING-PG-STAT-SSL-VIEW)

A visão `pg_stat_ssl` conterá uma linha por processo de emissor de backend ou WAL, mostrando estatísticas sobre o uso do SSL nesta conexão. Ela pode ser associada a `pg_stat_activity` ou `pg_stat_replication` na coluna `pid` para obter mais detalhes sobre a conexão.

**Tabela 27.20. `pg_stat_ssl` Visualização**



<table border="1" class="table" summary="pg_stat_ssl View">
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
      pid
     </code>
     <code class="type">
      integer
     </code>
    </p>
    <p>
     ID de processo de um servidor de banco de dados ou processo de emissor WAL
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      ssl
     </code>
     <code class="type">
      boolean
     </code>
    </p>
    <p>
     Verdadeiro se SSL é usado nesta conexão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      version
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Versão do SSL em uso, ou NULL se o SSL não estiver em uso nesta conexão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      cipher
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Nome do cifrador SSL em uso, ou NULL se o SSL não estiver em uso nesta conexão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      bits
     </code>
     <code class="type">
      integer
     </code>
    </p>
    <p>
     Número de bits no algoritmo de criptografia utilizado, ou NULL se SSL não for utilizado nesta conexão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      client_dn
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Campo Nome Distinguido (DN) do certificado do cliente utilizado, ou NULL se nenhum certificado do cliente foi fornecido ou se o SSL não está em uso nesta conexão. Este campo é truncado se o campo DN for mais longo que
     <code class="symbol">
      NAMEDATALEN
     </code>
     (64 caracteres em uma versão padrão).
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      client_serial
     </code>
     <code class="type">
      numeric
     </code>
    </p>
    <p>
     Número serial do certificado do cliente, ou NULL se nenhum certificado do cliente foi fornecido ou se o SSL não está em uso nesta conexão. A combinação do número serial do certificado e do emissor do certificado identifica de forma única um certificado (a menos que o emissor reutilize erroneamente os números serial).
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      issuer_dn
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     DN do emissor do certificado do cliente, ou NULL se não foi fornecido nenhum certificado do cliente ou se o SSL não está em uso nesta conexão. Este campo é truncado como
     <code class="structfield">
      client_dn
     </code>
     .
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.2.11. `pg_stat_gssapi` [#](#MONITORING-PG-STAT-GSSAPI-VIEW)

A visão `pg_stat_gssapi` conterá uma linha por backend, mostrando informações sobre o uso do GSSAPI nesta conexão. Ela pode ser associada a `pg_stat_activity` ou `pg_stat_replication` na coluna `pid` para obter mais detalhes sobre a conexão.

**Tabela 27.21. `pg_stat_gssapi` Visualização**



<table border="1" class="table" summary="pg_stat_gssapi View">
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
      pid
     </code>
     <code class="type">
      integer
     </code>
    </p>
    <p>
     ID de processo de um backend
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      gss_authenticated
     </code>
     <code class="type">
      boolean
     </code>
    </p>
    <p>
     Verdadeiro se a autenticação GSSAPI foi usada para esta conexão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      principal
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     O principal costuma autenticar essa conexão, ou NULL se o GSSAPI não foi usado para autenticar essa conexão. Esse campo é truncado se o principal for mais longo que
     <code class="symbol">
      NAMEDATALEN
     </code>
     (64 caracteres em uma versão padrão).
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      encrypted
     </code>
     <code class="type">
      boolean
     </code>
    </p>
    <p>
     Verdadeiro se a criptografia GSSAPI está em uso nesta conexão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      credentials_delegated
     </code>
     <code class="type">
      boolean
     </code>
    </p>
    <p>
     Verdadeiro se as credenciais do GSSAPI foram delegadas nesta conexão.
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.2.12. `pg_stat_archiver` [#](#MONITORING-PG-STAT-ARCHIVER-VIEW)

A visão `pg_stat_archiver` sempre terá uma única linha, contendo dados sobre o processo de arquivamento do clúster.

**Tabela 27.22. `pg_stat_archiver` Visualização**



<table border="1" class="table" summary="pg_stat_archiver View">
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
      archived_count
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of WAL files that have been successfully archived
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      last_archived_wal
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Name of the WAL file most recently successfully archived
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      last_archived_time
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Time of the most recent successful archive operation
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      failed_count
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of failed attempts for archiving WAL files
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      last_failed_wal
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Name of the WAL file of the most recent failed archival operation
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      last_failed_time
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Time of the most recent failed archival operation
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
     Time at which these statistics were last reset
    </p>
   </td>
  </tr>
 </tbody>
</table>










Normalmente, os arquivos WAL são arquivados em ordem, do mais antigo ao mais recente, mas isso não é garantido e não se aplica em circunstâncias especiais, como quando se está promovendo um estado de espera ou após a recuperação após falha. Portanto, não é seguro assumir que todos os arquivos mais antigos do que `last_archived_wal` também tenham sido arquivados com sucesso.

### 27.2.13. `pg_stat_io` [#](#MONITORING-PG-STAT-IO-VIEW)

A visualização `pg_stat_io` conterá uma linha para cada combinação de tipo de backend, objeto de E/S alvo e contexto de E/S, mostrando estatísticas de E/S em todo o clúster. As combinações que não fazem sentido são omitidas.

Atualmente, o I/O em relação a relações (por exemplo, tabelas, índices) e a atividade do WAL são monitorados. No entanto, o I/O de relação que contorna buffers compartilhados (por exemplo, ao mover uma tabela de um espaço de tabelas para outro) atualmente não é rastreado.

**Tabela 27.23. `pg_stat_io` Visualização**



<table border="1" class="table" summary="pg_stat_io View">
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
      backend_type
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Tipo de backend (por exemplo, trabalhador de fundo, trabalhador de autovacuum). Veja
     <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW" title="27.2.3. pg_stat_activity">
      <code class="structname">
       pg_stat_activity
      </code>
     </a>
     para mais informações sobre
     <code class="varname">
      backend_type
     </code>
     algumas s.
     <code class="varname">
      backend_type
     </code>
     Eles não acumulam estatísticas de operação de E/S e não serão incluídos na visualização.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      object
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Objeto alvo de uma operação de E/S. Os valores possíveis são:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        <code class="literal">
         relation
        </code>
        Relações permanentes.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         temp relation
        </code>
        Relações temporárias.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         wal
        </code>
        : Registros de escrita antecipada.
       </p>
      </li>
     </ul>
    </div>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      context
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     O contexto de uma operação de E/S. Os valores possíveis são:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        <code class="literal">
         normal
        </code>
        : O padrão ou padrão
        <code class="varname">
         context
        </code>
        para um tipo de operação de E/S. Por exemplo, por padrão, os dados da relação são lidos e escritos em buffers compartilhados. Assim, as leituras e escritas de dados da relação em e a partir de buffers compartilhados são rastreadas em
        <code class="varname">
         context
        </code>
        <code class="literal">
         normal
        </code>
        .
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         init
        </code>
        : As operações de E/S realizadas durante a criação dos segmentos WAL são rastreadas em
        <code class="varname">
         context
        </code>
        <code class="literal">
         init
        </code>
        .
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         vacuum
        </code>
        : Operações de E/S realizadas fora dos buffers compartilhados durante a limpeza e análise de relações permanentes. Os vazamentos temporários de tabela utilizam o mesmo conjunto de buffers locais que outras operações de E/S de tabela temporária e são rastreados em
        <code class="varname">
         context
        </code>
        <code class="literal">
         normal
        </code>
        .
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         bulkread
        </code>
        : Algumas operações de leitura de grande porte realizadas fora dos buffers compartilhados, por exemplo, uma varredura sequencial de uma grande tabela.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         bulkwrite
        </code>
        : Algumas operações de escrita de grande porte realizadas fora dos buffers compartilhados, como
        <code class="command">
         COPY
        </code>
        .
       </p>
      </li>
     </ul>
    </div>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      reads
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de operações de leitura.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      read_bytes
     </code>
     <code class="type">
      numeric
     </code>
    </p>
    <p>
     O tamanho total das operações de leitura em bytes.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      read_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Tempo gasto esperando operações de leitura em milissegundos (se
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-IO-TIMING">
      track_io_timing
     </a>
     está habilitado e
     <code class="varname">
      object
     </code>
     não é
     <code class="literal">
      wal
     </code>
     , ou se
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING">
      track_wal_io_timing
     </a>
     está habilitado e
     <code class="varname">
      object
     </code>
     é
     <code class="literal">
      wal
     </code>
     , caso contrário, zero)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      writes
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de operações de escrita.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      write_bytes
     </code>
     <code class="type">
      numeric
     </code>
    </p>
    <p>
     O tamanho total das operações de escrita em bytes.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      write_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Tempo gasto esperando operações de escrita em milissegundos (se
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-IO-TIMING">
      track_io_timing
     </a>
     está habilitado e
     <code class="varname">
      object
     </code>
     não é
     <code class="literal">
      wal
     </code>
     , ou se
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING">
      track_wal_io_timing
     </a>
     está habilitado e
     <code class="varname">
      object
     </code>
     é
     <code class="literal">
      wal
     </code>
     , caso contrário, zero)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      writebacks
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de unidades do tamanho
     <code class="symbol">
      BLCKSZ
     </code>
     (geralmente 8 kB) que o processo solicitou que o kernel escrevesse para armazenamento permanente.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      writeback_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Tempo gasto esperando operações de writeback em milissegundos (se
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-IO-TIMING">
      track_io_timing
     </a>
     se habilitada, caso contrário, zero). Isso inclui o tempo gasto em filas de solicitações de saída e, potencialmente, o tempo gasto para escrever os dados sujos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      extends
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de operações de extensão de relação.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      extend_bytes
     </code>
     <code class="type">
      numeric
     </code>
    </p>
    <p>
     O tamanho total das operações de extensão de relação em bytes.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      extend_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Tempo gasto esperando operações de extensão em milissegundos. (se
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-IO-TIMING">
      track_io_timing
     </a>
     está habilitado e
     <code class="varname">
      object
     </code>
     não é
     <code class="literal">
      wal
     </code>
     , ou se
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING">
      track_wal_io_timing
     </a>
     está habilitado e
     <code class="varname">
      object
     </code>
     é
     <code class="literal">
      wal
     </code>
     , caso contrário, zero)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      hits
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     O número de vezes em que um bloco desejado foi encontrado em um buffer compartilhado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      evictions
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de vezes que um bloco foi escrito de um buffer compartilhado ou local para torná-lo disponível para outro uso.
    </p>
    <p>
     Em
     <code class="varname">
      context
     </code>
     <code class="literal">
      normal
     </code>
     , isso conta o número de vezes que um bloco foi ejetado de um buffer e substituído por outro bloco. Em
     <code class="varname">
      context
     </code>
     s
     <code class="literal">
      bulkwrite
     </code>
     ,
     <code class="literal">
      bulkread
     </code>
     , e
     <code class="literal">
      vacuum
     </code>
     , isso conta o número de vezes que um bloco foi excluído dos buffers compartilhados, a fim de adicionar o buffer compartilhado a um buffer de anel separado, com tamanho limitado, para uso em uma operação de E/S em massa.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      reuses
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     O número de vezes que um buffer existente em um buffer de anel limitado por tamanho, fora dos buffers compartilhados, foi reutilizado como parte de uma operação de E/S no
     <code class="literal">
      bulkread
     </code>
     ,
     <code class="literal">
      bulkwrite
     </code>
     , ou
     <code class="literal">
      vacuum
     </code>
     <code class="varname">
      context
     </code>
     s.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      fsyncs
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de
     <code class="literal">
      fsync
     </code>
     chamadas. Essas são apenas rastreadas em
     <code class="varname">
      context
     </code>
     <code class="literal">
      normal
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      fsync_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Tempo gasto esperando operações de fsync em milissegundos (se
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-IO-TIMING">
      track_io_timing
     </a>
     está habilitado e
     <code class="varname">
      object
     </code>
     não é
     <code class="literal">
      wal
     </code>
     , ou se
     <a class="xref" href="runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING">
      track_wal_io_timing
     </a>
     está habilitado e
     <code class="varname">
      object
     </code>
     é
     <code class="literal">
      wal
     </code>
     , caso contrário, zero)
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
     O horário em que essas estatísticas foram redefinidas pela última vez.
    </p>
   </td>
  </tr>
 </tbody>
</table>










Alguns tipos de backend nunca realizam operações de E/S em alguns objetos de E/S e/ou em alguns contextos de E/S. Essas linhas são omitidas da visualização. Por exemplo, o checkpointer não faz o checkpoint de tabelas temporárias, portanto, não haverá linhas para `backend_type` `checkpointer` e `object` `temp relation`.

Além disso, algumas operações de E/S nunca serão realizadas por certos tipos de backend ou em certos objetos de E/S e/ou em certos contextos de E/S. Essas células serão NULL. Por exemplo, as tabelas temporárias não são `fsync`adas, então `fsyncs` será NULL para `object` `temp relation`. Além disso, o escritor de segundo plano não realiza leituras, então `reads` será NULL em linhas para `backend_type` `background writer`.

Para os rastreadores `object`, `wal`, `fsyncs` e `fsync_time`, o fsync da atividade dos arquivos WAL é rastreado em `issue_xlog_fsync`. Os rastreadores `writes` e `write_time` rastreiam a atividade de escrita dos arquivos WAL realizados em `XLogWrite`. Consulte [Seção 28.5](wal-configuration.md "28.5. WAL Configuration") para mais informações.

`pg_stat_io` pode ser usado para informar o ajuste do banco de dados. Por exemplo:

* Um alto `evictions` pode indicar que os buffers compartilhados devem ser aumentados.
* Os backends de clientes dependem do checkpointer para garantir que os dados sejam persistentes no armazenamento permanente. Grandes números de `fsyncs` por `client backend`s poderiam indicar uma configuração incorreta dos buffers compartilhados ou do checkpointer. Mais informações sobre a configuração do checkpointer podem ser encontradas em [Seção 28.5](wal-configuration.md).
* Normalmente, os backends de clientes devem ser capazes de confiar em processos auxiliares como o checkpointer e o escritor de segundo plano para escrever dados sujos o máximo possível. Grandes números de escritas por backends de clientes poderiam indicar uma configuração incorreta dos buffers compartilhados ou do checkpointer. Mais informações sobre a configuração do checkpointer podem ser encontradas em [Seção 28.5](wal-configuration.md).

Nota

As colunas que rastreiam o tempo de espera de I/O só serão não nulos quando [track_io_timing](runtime-config-statistics.md#GUC-TRACK-IO-TIMING) está habilitado. O usuário deve ter cuidado ao fazer referência a essas colunas em combinação com suas operações de I/O correspondentes, caso `track_io_timing` não tenha sido habilitado durante todo o tempo desde o último reajuste de estatísticas.

### 27.2.14. `pg_stat_bgwriter` [#](#MONITORING-PG-STAT-BGWRITER-VIEW)

A vista `pg_stat_bgwriter` sempre terá uma única linha, contendo dados sobre o escritor de plano de fundo do clúster.

**Tabela 27.24. `pg_stat_bgwriter` Visualização**



<table border="1" class="table" summary="pg_stat_bgwriter View">
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
      buffers_clean
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of buffers written by the background writer
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      maxwritten_clean
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times the background writer stopped a cleaning scan because it had written too many buffers
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      buffers_alloc
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of buffers allocated
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
     Time at which these statistics were last reset
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.2.15.  `pg_stat_checkpointer` [#](#MONITORING-PG-STAT-CHECKPOINTER-VIEW)

A visão `pg_stat_checkpointer` sempre terá uma única linha, contendo dados sobre o processo de verificação do cluster.

**Tabela 27.25. `pg_stat_checkpointer` Visualização**



<table border="1" class="table" summary="pg_stat_checkpointer View">
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
      num_timed
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of scheduled checkpoints due to timeout
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      num_requested
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of requested checkpoints
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      num_done
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of checkpoints that have been performed
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      restartpoints_timed
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of scheduled restartpoints due to timeout or after a failed attempt to perform it
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      restartpoints_req
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of requested restartpoints
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      restartpoints_done
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of restartpoints that have been performed
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      write_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total amount of time that has been spent in the portion of processing checkpoints and restartpoints where files are written to disk, in milliseconds
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      sync_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total amount of time that has been spent in the portion of processing checkpoints and restartpoints where files are synchronized to disk, in milliseconds
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      buffers_written
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of shared buffers written during checkpoints and restartpoints
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      slru_written
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of SLRU buffers written during checkpoints and restartpoints
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
     Time at which these statistics were last reset
    </p>
   </td>
  </tr>
 </tbody>
</table>










Os pontos de verificação podem ser ignorados se o servidor não estiver ativo desde o último. `num_timed` e `num_requested` contam tanto os pontos de verificação completos quanto os ignorados, enquanto `num_done` registra apenas os completos. Da mesma forma, os pontos de reinício podem ser ignorados se o último registro de ponto de verificação reinterpretado já for o último ponto de reinício. `restartpoints_timed` e `restartpoints_req` contam tanto os pontos de verificação completos quanto os ignorados, enquanto `restartpoints_done` registra apenas os completos.

### 27.2.16.  `pg_stat_wal` [#](#MONITORING-PG-STAT-WAL-VIEW)

A vista `pg_stat_wal` sempre terá uma única linha, contendo dados sobre a atividade do WAL do clúster.

**Tabela 27.26. `pg_stat_wal` Visualização**



<table border="1" class="table" summary="pg_stat_wal View">
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
      wal_records
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of WAL records generated
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
     Total number of WAL full page images generated
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
     Total amount of WAL generated in bytes
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
     Number of times WAL data was written to disk because WAL buffers became full
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
     Time at which these statistics were last reset
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.2.17.  `pg_stat_database` [#](#MONITORING-PG-STAT-DATABASE-VIEW)

A visualização `pg_stat_database` conterá uma linha para cada banco de dados no clúster, além de uma linha para objetos compartilhados, mostrando estatísticas em nível de banco de dados.

**Tabela 27.27. `pg_stat_database` Visualização**



<table border="1" class="table" summary="pg_stat_database View">
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
      datid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     OID of this database, or 0 for objects belonging to a shared relation
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      datname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Name of this database, or
     <code class="literal">
      NULL
     </code>
     for shared objects.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      numbackends
     </code>
     <code class="type">
      integer
     </code>
    </p>
    <p>
     Number of backends currently connected to this database, or
     <code class="literal">
      NULL
     </code>
     for shared objects.  This is the only column in this view that returns a value reflecting current state; all other columns return the accumulated values since the last reset.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      xact_commit
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of transactions in this database that have been committed
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      xact_rollback
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of transactions in this database that have been rolled back
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      blks_read
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of disk blocks read in this database
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      blks_hit
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times disk blocks were found already in the buffer cache, so that a read was not necessary (this only includes hits in the PostgreSQL buffer cache, not the operating system's file system cache)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      tup_returned
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of live rows fetched by sequential scans and index entries returned by index scans in this database
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      tup_fetched
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of live rows fetched by index scans in this database
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      tup_inserted
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of rows inserted by queries in this database
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      tup_updated
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of rows updated by queries in this database
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      tup_deleted
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of rows deleted by queries in this database
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      conflicts
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of queries canceled due to conflicts with recovery in this database. (Conflicts occur only on standby servers; see
     <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-DATABASE-CONFLICTS-VIEW" title="27.2.18. pg_stat_database_conflicts">
      <code class="structname">
       pg_stat_database_conflicts
      </code>
     </a>
     for details.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      temp_files
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of temporary files created by queries in this database. All temporary files are counted, regardless of why the temporary file was created (e.g., sorting or hashing), and regardless of the
     <a class="xref" href="runtime-config-logging.md#GUC-LOG-TEMP-FILES">
      log_temp_files
     </a>
     setting.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      temp_bytes
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total amount of data written to temporary files by queries in this database. All temporary files are counted, regardless of why the temporary file was created, and regardless of the
     <a class="xref" href="runtime-config-logging.md#GUC-LOG-TEMP-FILES">
      log_temp_files
     </a>
     setting.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      deadlocks
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of deadlocks detected in this database
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      checksum_failures
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of data page checksum failures detected in this database (or on a shared object), or NULL if data checksums are disabled.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      checksum_last_failure
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Time at which the last data page checksum failure was detected in this database (or on a shared object), or NULL if data checksums are disabled.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      blk_read_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Time spent reading data file blocks by backends in this database, in milliseconds (if
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
      blk_write_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Time spent writing data file blocks by backends in this database, in milliseconds (if
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
      session_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Time spent by database sessions in this database, in milliseconds (note that statistics are only updated when the state of a session changes, so if sessions have been idle for a long time, this idle time won't be included)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      active_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Time spent executing SQL statements in this database, in milliseconds (this corresponds to the states
     <code class="literal">
      active
     </code>
     and
     <code class="literal">
      fastpath function call
     </code>
     in
     <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW" title="27.2.3. pg_stat_activity">
      <code class="structname">
       pg_stat_activity
      </code>
     </a>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      idle_in_transaction_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Time spent idling while in a transaction in this database, in milliseconds (this corresponds to the states
     <code class="literal">
      idle in transaction
     </code>
     and
     <code class="literal">
      idle in transaction (aborted)
     </code>
     in
     <a class="link" href="monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW" title="27.2.3. pg_stat_activity">
      <code class="structname">
       pg_stat_activity
      </code>
     </a>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      sessions
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of sessions established to this database
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      sessions_abandoned
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of database sessions to this database that were terminated because connection to the client was lost
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      sessions_fatal
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of database sessions to this database that were terminated by fatal errors
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      sessions_killed
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of database sessions to this database that were terminated by operator intervention
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
     Number of parallel workers planned to be launched by queries on this database
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
     Number of parallel workers launched by queries on this database
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
     Time at which these statistics were last reset
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.2.18.  `pg_stat_database_conflicts` [#](#MONITORING-PG-STAT-DATABASE-CONFLICTS-VIEW)

A visão `pg_stat_database_conflicts` conterá uma linha por banco de dados, mostrando estatísticas de nível de banco de dados sobre cancelamentos de consulta que ocorrem devido a conflitos com recuperação em servidores de espera. Esta visão conterá apenas informações sobre servidores de espera, uma vez que os conflitos não ocorrem em servidores primários.

**Tabela 27.28. `pg_stat_database_conflicts` Visualização**



<table border="1" class="table" summary="pg_stat_database_conflicts View">
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
      datid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     OID de um banco de dados
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      datname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome deste banco de dados
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confl_tablespace
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de consultas neste banco de dados que foram canceladas devido ao espaço de tabela descartado
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confl_lock
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de consultas nesse banco de dados que foram canceladas devido a tempos de bloqueio
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confl_snapshot
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de consultas neste banco de dados que foram canceladas devido a instantâneos antigos
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confl_bufferpin
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de consultas neste banco de dados que foram canceladas devido a buffers fixados
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confl_deadlock
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de consultas nesse banco de dados que foram canceladas devido a deadlocks
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confl_active_logicalslot
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de usos de slots lógicos neste banco de dados que foram cancelados devido a instantâneos antigos ou a um número muito baixo de
     <a class="xref" href="runtime-config-wal.md#GUC-WAL-LEVEL">
      wal_level
     </a>
     sobre o primário
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.2.19. `pg_stat_all_tables` [#](#MONITORING-PG-STAT-ALL-TABLES-VIEW)

A visualização `pg_stat_all_tables` conterá uma linha para cada tabela no banco de dados atual (incluindo tabelas TOAST), mostrando estatísticas sobre os acessos a essa tabela específica. As visualizações `pg_stat_user_tables` e `pg_stat_sys_tables` contêm as mesmas informações, mas filtradas para mostrar apenas as tabelas de usuário e sistema, respectivamente.

**Tabela 27.29. `pg_stat_all_tables` Visualização**



<table border="1" class="table" summary="pg_stat_all_tables View">
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
      relid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     OID of a table
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      schemaname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Name of the schema that this table is in
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Name of this table
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      seq_scan
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of sequential scans initiated on this table
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      last_seq_scan
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     The time of the last sequential scan on this table, based on the most recent transaction stop time
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      seq_tup_read
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of live rows fetched by sequential scans
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      idx_scan
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of index scans initiated on this table
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      last_idx_scan
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     The time of the last index scan on this table, based on the most recent transaction stop time
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      idx_tup_fetch
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of live rows fetched by index scans
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      n_tup_ins
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of rows inserted
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      n_tup_upd
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of rows updated.  (This includes row updates counted in
     <code class="structfield">
      n_tup_hot_upd
     </code>
     and
     <code class="structfield">
      n_tup_newpage_upd
     </code>
     , and remaining non-
     <acronym class="acronym">
      HOT
     </acronym>
     updates.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      n_tup_del
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Total number of rows deleted
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      n_tup_hot_upd
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of rows
     <a class="link" href="storage-hot.md" title="66.7. Heap-Only Tuples (HOT)">
      HOT updated
     </a>
     . These are updates where no successor versions are required in indexes.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      n_tup_newpage_upd
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of rows updated where the successor version goes onto a
     <span class="emphasis">
      <em>
       new
      </em>
     </span>
     heap page, leaving behind an original version with a
     <a class="link" href="storage-page-layout.md#STORAGE-TUPLE-LAYOUT" title="66.6.1. Table Row Layout">
      <code class="structfield">
       t_ctid
      </code>
      field
     </a>
     that points to a different heap page.  These are always non-
     <acronym class="acronym">
      HOT
     </acronym>
     updates.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      n_live_tup
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Estimated number of live rows
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      n_dead_tup
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Estimated number of dead rows
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      n_mod_since_analyze
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Estimated number of rows modified since this table was last analyzed
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      n_ins_since_vacuum
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Estimated number of rows inserted since this table was last vacuumed (not counting
     <code class="command">
      VACUUM FULL
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      last_vacuum
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Last time at which this table was manually vacuumed (not counting
     <code class="command">
      VACUUM FULL
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      last_autovacuum
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Last time at which this table was vacuumed by the autovacuum daemon
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      last_analyze
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Last time at which this table was manually analyzed
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      last_autoanalyze
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     Last time at which this table was analyzed by the autovacuum daemon
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      vacuum_count
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times this table has been manually vacuumed (not counting
     <code class="command">
      VACUUM FULL
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      autovacuum_count
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times this table has been vacuumed by the autovacuum daemon
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      analyze_count
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times this table has been manually analyzed
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      autoanalyze_count
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Number of times this table has been analyzed by the autovacuum daemon
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      total_vacuum_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total time this table has been manually vacuumed, in milliseconds (not counting
     <code class="command">
      VACUUM FULL
     </code>
     ). (This includes the time spent sleeping due to cost-based delays.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      total_autovacuum_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total time this table has been vacuumed by the autovacuum daemon, in milliseconds. (This includes the time spent sleeping due to cost-based delays.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      total_analyze_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total time this table has been manually analyzed, in milliseconds. (This includes the time spent sleeping due to cost-based delays.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      total_autoanalyze_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Total time this table has been analyzed by the autovacuum daemon, in milliseconds. (This includes the time spent sleeping due to cost-based delays.)
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.2.20. `pg_stat_all_indexes` [#](#MONITORING-PG-STAT-ALL-INDEXES-VIEW)

A visualização `pg_stat_all_indexes` conterá uma linha para cada índice no banco de dados atual, mostrando estatísticas sobre os acessos a esse índice específico. As visualizações `pg_stat_user_indexes` e `pg_stat_sys_indexes` contêm as mesmas informações, mas filtradas para mostrar apenas índices de usuário e sistema, respectivamente.

**Tabela 27.30. `pg_stat_all_indexes` Visualização**



<table border="1" class="table" summary="pg_stat_all_indexes View">
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
      relid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     OID da tabela para este índice
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      indexrelid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     OID deste índice
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      schemaname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome do esquema no qual este índice está
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome da tabela para este índice
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      indexrelname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome deste índice
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      idx_scan
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de varreduras de índice iniciadas neste índice
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      last_idx_scan
     </code>
     <code class="type">
      timestamp with time zone
     </code>
    </p>
    <p>
     O horário da última varredura deste índice, com base no horário mais recente de parada da transação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      idx_tup_read
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de entradas de índice retornadas por varreduras neste índice
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      idx_tup_fetch
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de linhas de tabela em execução obtido por varreduras de índice simples usando este índice
    </p>
   </td>
  </tr>
 </tbody>
</table>










Os índices podem ser usados por meio de varreduras simples de índice, varreduras de índice "bitmap" e pelo otimizador. Em uma varredura bitmap, a saída de vários índices pode ser combinada por meio de regras AND ou OR, portanto, é difícil associar buscas individuais de linha de pilha com índices específicos quando uma varredura bitmap é usada. Portanto, uma varredura bitmap incrementa o `pg_stat_all_indexes`.`idx_tup_read` (contas) dos índices que ela usa, e incrementa a `pg_stat_all_tables`.`idx_tup_fetch` (contas) da tabela, mas não afeta `pg_stat_all_indexes`.`idx_tup_fetch`. O otimizador também acessa índices para verificar constantes fornecidas cujos valores estão fora do intervalo registrado das estatísticas do otimizador, porque as estatísticas do otimizador podem estar desatualizadas.

Nota

As contagens de `idx_tup_read` e `idx_tup_fetch` podem ser diferentes mesmo sem qualquer uso de varreduras de mapa de bits, porque as entradas de índice de contagens `idx_tup_read` são recuperadas do índice, enquanto as contagens `idx_tup_fetch` contam linhas vivas obtidas da tabela. Este último será menor se quaisquer linhas mortas ou ainda não comprometidas forem obtidas usando o índice, ou se quaisquer consultas de heap forem evitadas por meio de uma varredura apenas de índice.

Nota

As varreduras de índice podem, às vezes, realizar múltiplas pesquisas de índice por execução. Cada pesquisa de índice incrementa `pg_stat_all_indexes`.`idx_scan`, portanto, é possível que o número de varreduras de índice exceda significativamente o número total de execuções de nós executor de varredura de índice.

Isso pode acontecer com consultas que utilizam certas construções SQL para procurar linhas que correspondem a qualquer valor de uma lista ou matriz de múltiplos valores escalares (consulte [Seção 9.25](functions-comparisons.md)). Também pode acontecer com consultas que possuem uma construção `column_name = value1 OR column_name = value2 ...`, embora apenas quando o otimizador transforme a construção em uma representação equivalente de matriz de múltiplos valores. Da mesma forma, quando as varreduras de índice B-tree utilizam a otimização de varredura de salto, uma pesquisa de índice é realizada cada vez que a varredura é reposicionada para a próxima página da folha de índice que pode ter tuplas correspondentes (consulte [Seção 11.3](indexes-multicolumn.md)).

### DICA

`EXPLAIN ANALYZE` exibe o número total de pesquisas de índice realizadas por cada nó de varredura de índice. Consulte [Seção 14.1.2](using-explain.md#USING-EXPLAIN-ANALYZE) para um exemplo que demonstra como isso funciona.

### 27.2.21. `pg_statio_all_tables` [#](#MONITORING-PG-STATIO-ALL-TABLES-VIEW)

A visualização `pg_statio_all_tables` conterá uma linha para cada tabela no banco de dados atual (incluindo as tabelas TOAST), mostrando estatísticas sobre o I/O nessa tabela específica. As visualizações `pg_statio_user_tables` e `pg_statio_sys_tables` contêm as mesmas informações, mas filtradas para mostrar apenas as tabelas de usuário e sistema, respectivamente.

**Tabela 27.31. `pg_statio_all_tables` Visualização**



<table border="1" class="table" summary="pg_statio_all_tables View">
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
      relid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     OID de uma tabela
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      schemaname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome do esquema em que a tabela está
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome desta tabela
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      heap_blks_read
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de blocos de disco lidos a partir desta tabela
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      heap_blks_hit
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de acertos de buffer nesta tabela
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      idx_blks_read
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de blocos de disco lidos de todos os índices nesta tabela
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      idx_blks_hit
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de acertos de buffer em todos os índices nesta tabela
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      toast_blks_read
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de blocos de disco lidos da tabela TOAST desta tabela (se houver)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      toast_blks_hit
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de acertos de buffer na tabela TOAST desta tabela (se houver)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      tidx_blks_read
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de blocos de disco lidos dos índices da tabela TOAST da tabela (se houver)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      tidx_blks_hit
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de acertos de buffer nos índices de tabela TOAST desta tabela (se houver)
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.2.22. `pg_statio_all_indexes` [#](#MONITORING-PG-STATIO-ALL-INDEXES-VIEW)

A visualização `pg_statio_all_indexes` conterá uma linha para cada índice no banco de dados atual, mostrando estatísticas sobre o I/O nesse índice específico. As visualizações `pg_statio_user_indexes` e `pg_statio_sys_indexes` contêm as mesmas informações, mas filtradas para mostrar apenas índices de usuário e sistema, respectivamente.

**Tabela 27.32. `pg_statio_all_indexes` Visualização**



<table border="1" class="table" summary="pg_statio_all_indexes View">
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
      relid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     OID da tabela para este índice
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      indexrelid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     OID deste índice
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      schemaname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome do esquema no qual este índice está
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome da tabela para este índice
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      indexrelname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome deste índice
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      idx_blks_read
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de blocos de disco lidos a partir deste índice
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      idx_blks_hit
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de acertos de buffer neste índice
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.2.23. `pg_statio_all_sequences` [#](#MONITORING-PG-STATIO-ALL-SEQUENCES-VIEW)

A visualização `pg_statio_all_sequences` conterá uma linha para cada sequência no banco de dados atual, mostrando estatísticas sobre o I/O nessa sequência específica.

**Tabela 27.33. `pg_statio_all_sequences` Visualização**



<table border="1" class="table" summary="pg_statio_all_sequences View">
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
      relid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     OID de uma sequência
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      schemaname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome do esquema no qual essa sequência está
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome dessa sequência
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      blks_read
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de blocos de disco lidos a partir dessa sequência
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      blks_hit
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de acertos de buffer nesta sequência
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.2.24. `pg_stat_user_functions` [#](#MONITORING-PG-STAT-USER-FUNCTIONS-VIEW)

A visualização `pg_stat_user_functions` conterá uma linha para cada função rastreada, mostrando estatísticas sobre as execuções dessa função. O parâmetro [track_functions](runtime-config-statistics.md#GUC-TRACK-FUNCTIONS) controla exatamente quais funções são rastreadas.

**Tabela 27.34. `pg_stat_user_functions` Visualização**



<table border="1" class="table" summary="pg_stat_user_functions View">
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
      funcid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     OID de uma função
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      schemaname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome do esquema no qual essa função está
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      funcname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome desta função
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
     Número de vezes que essa função foi chamada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      total_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Tempo total gasto nesta função e em todas as outras funções chamadas por ela, em milissegundos
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      self_time
     </code>
     <code class="type">
      double precision
     </code>
    </p>
    <p>
     Tempo total gasto nesta função, sem incluir outras funções chamadas por ela, em milissegundos
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.2.25. `pg_stat_slru` [#](#MONITORING-PG-STAT-SLRU-VIEW)

O PostgreSQL acessa certas informações em disco através dos `SLRU` (*simples menos recentemente usado*) caches. A vista `pg_stat_slru` conterá uma linha para cada cache SLRU rastreado, mostrando estatísticas sobre o acesso às páginas em cache.

Para cada cache `SLRU` que faz parte do servidor principal, há um parâmetro de configuração que controla seu tamanho, com o sufixo `_buffers` anexado.

**Tabela 27.35. `pg_stat_slru` Visualização**



<table border="1" class="table" summary="pg_stat_slru View">
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
      name
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Nome do SLRU
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      blks_zeroed
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de blocos zerados durante as inicializações
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      blks_hit
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de vezes em que blocos de disco foram encontrados já no SLRU, de modo que uma leitura não fosse necessária (isto inclui apenas acertos no SLRU, não o cache do sistema de arquivos do sistema operacional)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      blks_read
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de blocos de disco lidos para este SLRU
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      blks_written
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de blocos de disco escritos para este SLRU
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      blks_exists
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de blocos verificados quanto à existência para este SLRU
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      flushes
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de lavagens de dados sujos para este SLRU
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      truncates
     </code>
     <code class="type">
      bigint
     </code>
    </p>
    <p>
     Número de truncos para este SLRU
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
     Tempo em que essas estatísticas foram redefinidas pela última vez
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 27.2.26. Funções estatísticas [#](#MONITORING-STATS-FUNCTIONS)

Outras formas de analisar as estatísticas podem ser configuradas escrevendo consultas que utilizam as mesmas funções de acesso às estatísticas subjacentes utilizadas pelos pontos de vista padrão mostrados acima. Para obter detalhes, como os nomes das funções, consulte as definições dos pontos de vista padrão. (Por exemplo, no psql, você pode emitir `\d+ pg_stat_activity`. As funções de acesso às estatísticas por banco de dados aceitam um OID de banco de dados como argumento para identificar em qual banco de dados reportar. As funções por tabela e por índice aceitam um OID de tabela ou índice. As funções de estatísticas por função aceitam um OID de função. Note que apenas as tabelas, índices e funções no banco de dados atual podem ser visualizadas com essas funções.

Funções adicionais relacionadas ao sistema de estatísticas acumuladas estão listadas em [Tabela 27.36](monitoring-stats.md#MONITORING-STATS-FUNCS-TABLE).

**Tabela 27.36. Funções adicionais de estatísticas**



<table border="1" class="table" summary="Additional Statistics Functions">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_backend_pid
     </code>
     () →
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Returns the process ID of the server process attached to the current session.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-STAT-GET-BACKEND-IO">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_backend_io
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      setof record
     </code>
    </p>
    <p>
     Returns I/O statistics about the backend with the specified process ID. The output fields are exactly the same as the ones in the
     <code class="structname">
      pg_stat_io
     </code>
     view.
    </p>
    <p>
     The function does not return I/O statistics for the checkpointer, the background writer, the startup process and the autovacuum launcher as they are already visible in the
     <code class="structname">
      pg_stat_io
     </code>
     view and there is only one of each.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_activity
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      setof record
     </code>
    </p>
    <p>
     Returns a record of information about the backend with the specified process ID, or one record for each active backend in the system if
     <code class="literal">
      NULL
     </code>
     is specified.  The fields returned are a subset of those in the
     <code class="structname">
      pg_stat_activity
     </code>
     view.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-STAT-GET-BACKEND-WAL">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_backend_wal
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      record
     </code>
    </p>
    <p>
     Returns WAL statistics about the backend with the specified process ID. The output fields are exactly the same as the ones in the
     <code class="structname">
      pg_stat_wal
     </code>
     view.
    </p>
    <p>
     The function does not return WAL statistics for the checkpointer, the background writer, the startup process and the autovacuum launcher.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_snapshot_timestamp
     </code>
     () →
     <code class="returnvalue">
      timestamp with time zone
     </code>
    </p>
    <p>
     Returns the timestamp of the current statistics snapshot, or NULL if no statistics snapshot has been taken. A snapshot is taken the first time cumulative statistics are accessed in a transaction if
     <code class="varname">
      stats_fetch_consistency
     </code>
     is set to
     <code class="literal">
      snapshot
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_xact_blocks_fetched
     </code>
     (
     <code class="type">
      oid
     </code>
     ) →
     <code class="returnvalue">
      bigint
     </code>
    </p>
    <p>
     Returns the number of block read requests for table or index, in the current transaction. This number minus
     <code class="function">
      pg_stat_get_xact_blocks_hit
     </code>
     gives the number of kernel
     <code class="function">
      read()
     </code>
     calls; the number of actual physical reads is usually lower due to kernel-level buffering.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_xact_blocks_hit
     </code>
     (
     <code class="type">
      oid
     </code>
     ) →
     <code class="returnvalue">
      bigint
     </code>
    </p>
    <p>
     Returns the number of block read requests for table or index, in the current transaction, found in cache (not triggering kernel
     <code class="function">
      read()
     </code>
     calls).
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_clear_snapshot
     </code>
     () →
     <code class="returnvalue">
      void
     </code>
    </p>
    <p>
     Discards the current statistics snapshot or cached information.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_reset
     </code>
     () →
     <code class="returnvalue">
      void
     </code>
    </p>
    <p>
     Resets all statistics counters for the current database to zero.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_reset_shared
     </code>
     ( [
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code class="type">
      text
     </code>
     <code class="literal">
      DEFAULT
     </code>
     <code class="literal">
      NULL
     </code>
     ] ) →
     <code class="returnvalue">
      void
     </code>
    </p>
    <p>
     Resets some cluster-wide statistics counters to zero, depending on the argument.
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     can be:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        <code class="literal">
         archiver
        </code>
        : Reset all the counters shown in the
        <code class="structname">
         pg_stat_archiver
        </code>
        view.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         bgwriter
        </code>
        : Reset all the counters shown in the
        <code class="structname">
         pg_stat_bgwriter
        </code>
        view.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         checkpointer
        </code>
        : Reset all the counters shown in the
        <code class="structname">
         pg_stat_checkpointer
        </code>
        view.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         io
        </code>
        : Reset all the counters shown in the
        <code class="structname">
         pg_stat_io
        </code>
        view.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         recovery_prefetch
        </code>
        : Reset all the counters shown in the
        <code class="structname">
         pg_stat_recovery_prefetch
        </code>
        view.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         slru
        </code>
        : Reset all the counters shown in the
        <code class="structname">
         pg_stat_slru
        </code>
        view.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         wal
        </code>
        : Reset all the counters shown in the
        <code class="structname">
         pg_stat_wal
        </code>
        view.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         NULL
        </code>
        or not specified: All the counters from the views listed above are reset.
       </p>
      </li>
     </ul>
    </div>
    <p>
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_reset_single_table_counters
     </code>
     (
     <code class="type">
      oid
     </code>
     ) →
     <code class="returnvalue">
      void
     </code>
    </p>
    <p>
     Resets statistics for a single table or index in the current database or shared across all databases in the cluster to zero.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_reset_backend_stats
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      void
     </code>
    </p>
    <p>
     Resets statistics for a single backend with the specified process ID to zero.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_reset_single_function_counters
     </code>
     (
     <code class="type">
      oid
     </code>
     ) →
     <code class="returnvalue">
      void
     </code>
    </p>
    <p>
     Resets statistics for a single function in the current database to zero.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_reset_slru
     </code>
     ( [
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code class="type">
      text
     </code>
     <code class="literal">
      DEFAULT
     </code>
     <code class="literal">
      NULL
     </code>
     ] ) →
     <code class="returnvalue">
      void
     </code>
    </p>
    <p>
     Resets statistics to zero for a single SLRU cache, or for all SLRUs in the cluster. If
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     is
     <code class="literal">
      NULL
     </code>
     or is not specified, all the counters shown in the
     <code class="structname">
      pg_stat_slru
     </code>
     view for all SLRU caches are reset. The argument can be one of
     <code class="literal">
      commit_timestamp
     </code>
     ,
     <code class="literal">
      multixact_member
     </code>
     ,
     <code class="literal">
      multixact_offset
     </code>
     ,
     <code class="literal">
      notify
     </code>
     ,
     <code class="literal">
      serializable
     </code>
     ,
     <code class="literal">
      subtransaction
     </code>
     , or
     <code class="literal">
      transaction
     </code>
     to reset the counters for only that entry. If the argument is
     <code class="literal">
      other
     </code>
     (or indeed, any unrecognized name), then the counters for all other SLRU caches, such as extension-defined caches, are reset.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_reset_replication_slot
     </code>
     (
     <code class="type">
      text
     </code>
     ) →
     <code class="returnvalue">
      void
     </code>
    </p>
    <p>
     Resets statistics of the replication slot defined by the argument. If the argument is
     <code class="literal">
      NULL
     </code>
     , resets statistics for all the replication slots.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_reset_subscription_stats
     </code>
     (
     <code class="type">
      oid
     </code>
     ) →
     <code class="returnvalue">
      void
     </code>
    </p>
    <p>
     Resets statistics for a single subscription shown in the
     <code class="structname">
      pg_stat_subscription_stats
     </code>
     view to zero. If the argument is
     <code class="literal">
      NULL
     </code>
     , reset statistics for all subscriptions.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
 </tbody>
</table>










### Aviso

Usar `pg_stat_reset()` também redefere os contadores que o autovacuum usa para determinar quando deve ser executado um vácuo ou um análise. Redefinir esses contadores pode fazer com que o autovacuum não realize o trabalho necessário, o que pode causar problemas como o engasgo da tabela ou estatísticas de tabela desatualizadas. Um `ANALYZE` para todo o banco de dados é recomendado após a redefinição das estatísticas.

`pg_stat_get_activity`, a função subjacente da visão `pg_stat_activity`, retorna um conjunto de registros contendo todas as informações disponíveis sobre cada processo de backend. Às vezes, pode ser mais conveniente obter apenas um subconjunto dessas informações. Nesses casos, pode-se usar outro conjunto de funções de acesso a estatísticas por backend; essas são mostradas em [Tabela 27.37](monitoring-stats.md#MONITORING-STATS-BACKEND-FUNCS-TABLE). Essas funções de acesso usam o número de ID de backend da sessão, que é um pequeno inteiro (>= 0) que é distinto do ID de backend de qualquer sessão concorrente, embora o ID de uma sessão possa ser reciclado assim que ela sai. O ID de backend é usado, entre outras coisas, para identificar o esquema temporário da sessão, se tiver um. A função `pg_stat_get_backend_idset` fornece uma maneira conveniente de listar todos os números de ID dos backends ativos para invocar essas funções. Por exemplo, para mostrar os PIDs e consultas atuais de todos os backends:

```
SELECT pg_stat_get_backend_pid(backendid) AS pid,
       pg_stat_get_backend_activity(backendid) AS query
FROM pg_stat_get_backend_idset() AS backendid;
```

**Tabela 27.37. Funções de estatísticas por backend**



<table border="1" class="table" summary="Per-Backend Statistics Functions">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_backend_activity
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      text
     </code>
    </p>
    <p>
     Returns the text of this backend's most recent query.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_backend_activity_start
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      timestamp with time zone
     </code>
    </p>
    <p>
     Returns the time when the backend's most recent query was started.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_backend_client_addr
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      inet
     </code>
    </p>
    <p>
     Returns the IP address of the client connected to this backend.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_backend_client_port
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Returns the TCP port number that the client is using for communication.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_backend_dbid
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      oid
     </code>
    </p>
    <p>
     Returns the OID of the database this backend is connected to.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_backend_idset
     </code>
     () →
     <code class="returnvalue">
      setof integer
     </code>
    </p>
    <p>
     Returns the set of currently active backend ID numbers.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_backend_pid
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Returns the process ID of this backend.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_backend_start
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      timestamp with time zone
     </code>
    </p>
    <p>
     Returns the time when this process was started.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_backend_subxact
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      record
     </code>
    </p>
    <p>
     Returns a record of information about the subtransactions of the backend with the specified ID. The fields returned are
     <em class="parameter">
      <code>
       subxact_count
      </code>
     </em>
     , which is the number of subtransactions in the backend's subtransaction cache, and
     <em class="parameter">
      <code>
       subxact_overflow
      </code>
     </em>
     , which indicates whether the backend's subtransaction cache is overflowed or not.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_backend_userid
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      oid
     </code>
    </p>
    <p>
     Returns the OID of the user logged into this backend.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_backend_wait_event
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      text
     </code>
    </p>
    <p>
     Returns the wait event name if this backend is currently waiting, otherwise NULL. See
     <a class="xref" href="monitoring-stats.md#WAIT-EVENT-ACTIVITY-TABLE" title="Table 27.5. Wait Events of Type Activity">
      Table 27.5
     </a>
     through
     <a class="xref" href="monitoring-stats.md#WAIT-EVENT-TIMEOUT-TABLE" title="Table 27.13. Wait Events of Type Timeout">
      Table 27.13
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_backend_wait_event_type
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      text
     </code>
    </p>
    <p>
     Returns the wait event type name if this backend is currently waiting, otherwise NULL.  See
     <a class="xref" href="monitoring-stats.md#WAIT-EVENT-TABLE" title="Table 27.4. Wait Event Types">
      Table 27.4
     </a>
     for details.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_stat_get_backend_xact_start
     </code>
     (
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      timestamp with time zone
     </code>
    </p>
    <p>
     Returns the time when the backend's current transaction was started.
    </p>
   </td>
  </tr>
 </tbody>
</table>





