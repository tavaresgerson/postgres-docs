## Capítulo 27. Monitoramento da atividade do banco de dados

**Índice**

* [27.1. Ferramentas Unix padrão](monitoring-ps.md)
* [27.2. O sistema de estatísticas cumulativas](monitoring-stats.md)

+ [27.2.1. Configuração de Coleta de Estatísticas](monitoring-stats.md#MONITORING-STATS-SETUP)
+ [27.2.2. Visualização de Estatísticas](monitoring-stats.md#MONITORING-STATS-VIEWS)
+ [27.2.3. `pg_stat_activity`](monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW)
+ [27.2.4. `pg_stat_replication`](monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-VIEW)
+ [27.2.5. `pg_stat_replication_slots`](monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-SLOTS-VIEW)
+ [27.2.6. `pg_stat_wal_receiver`](monitoring-stats.md#MONITORING-PG-STAT-WAL-RECEIVER-VIEW)
+ [27.2.7. `pg_stat_recovery_prefetch`](monitoring-stats.md#MONITORING-PG-STAT-RECOVERY-PREFETCH)
+ [27.2.8. `pg_stat_subscription`](monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION)
+ [27.2.9. `pg_stat_subscription_stats`](monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION-STATS)
+ [27.2.10. `pg_stat_ssl`](monitoring-stats.md#MONITORING-PG-STAT-SSL-VIEW)
+ [27.2.11. `pg_stat_gssapi`](monitoring-stats.md#MONITORING-PG-STAT-GSSAPI-VIEW)
+ [27.2.12. `pg_stat_archiver`](monitoring-stats.md#MONITORING-PG-STAT-ARCHIVER-VIEW)
+ [27.2.13. `pg_stat_io`](monitoring-stats.md#MONITORING-PG-STAT-IO-VIEW)
+ [27.2.14. `pg_stat_bgwriter`](monitoring-stats.md#MONITORING-PG-STAT-BGWRITER-VIEW)
+ [27.2.15. `pg_stat_checkpointer`](monitoring-stats.md#MONITORING-PG-STAT-CHECKPOINTER-VIEW)
+ [27.2.16. `pg_stat_wal`](monitoring-stats.md#MONITORING-PG-STAT-WAL-VIEW)
+ [27.2.17. `pg_stat_database`](monitoring-stats.md#MONITORING-PG-STAT-DATABASE-VIEW)
+ [27.2.18. `pg_stat_database_conflicts`](monitoring-stats.md#MONITORING-PG-STAT-DATABASE-CONFLICTS-VIEW)
+ [27.2.19. `pg_stat_all_tables`](monitoring-stats.md#MONITORING-PG-STAT-ALL-TABLES-VIEW)
+ [27.2.20. `pg_stat_all_indexes`](monitoring-stats.md#MONITORING-PG-STAT-ALL-INDEXES-VIEW)
+ [27.2.21. `pg_statio_all_tables`](monitoring-stats.md#MONITORING-PG-STATIO-ALL-TABLES-VIEW)
+ [27.2.22. `pg_statio_all_indexes`](monitoring-stats.md#MONITORING-PG-STATIO-ALL-INDEXES-VIEW)
+ [27.2.23. `pg_statio_all_sequences`](monitoring-stats.md#MONITORING-PG-STATIO-ALL-SEQUENCES-VIEW)
+ [27.2.24. `pg_stat_user_functions`](monitoring-stats.md#MONITORING-PG-STAT-USER-FUNCTIONS-VIEW)
+ [27.2.25. `pg_stat_slru`](monitoring-stats.md#MONITORING-PG-STAT-SLRU-VIEW)
+ [27.2.26. Funções Estatísticas](monitoring-stats.md#MONITORING-STATS-FUNCTIONS)

* [27.3. Visualização de bloqueios](monitoring-locks.md)
* [27.4. Relatórios de progresso](progress-reporting.md)

+ [27.4.1. RELATÓRIO DE PROGRSO](progress-reporting.md#ANALYZE-PROGRESS-REPORTING)
+ [27.4.2. RELATÓRIO DE CLUSTER](progress-reporting.md#CLUSTER-PROGRESS-REPORTING)
+ [27.4.3. COPIAR RELATÓRIO DE PROGRSO](progress-reporting.md#COPY-PROGRESS-REPORTING)
+ [27.4.4. CRIAR ÍNDICE DE RELATÓRIO DE PROGRSO](progress-reporting.md#CREATE-INDEX-PROGRESS-REPORTING)
+ [27.4.5. VACUUM RELATÓRIO DE PROGRSO](progress-reporting.md#VACUUM-PROGRESS-REPORTING)
+ [27.4.6. RELATÓRIO DE BACKUP DE BASE](progress-reporting.md#BASEBACKUP-PROGRESS-REPORTING)

* [27.5. Rastreamento Dinâmico](dynamic-trace.md)

+ [27.5.1. Compilando para Rastreamento Dinâmico][(dynamic-trace.md#COMPILING-FOR-TRACE)
+ [27.5.2. Sondas Integradas][(dynamic-trace.md#TRACE-POINTS)
+ [27.5.3. Usando Sondas][(dynamic-trace.md#USING-TRACE-POINTS)
+ [27.5.4. Definindo Novas Sondas][(dynamic-trace.md#DEFINING-TRACE-POINTS)

* [27.6. Monitoramento do uso do disco](diskusage.md)

+ [27.6.1. Determinação do uso do disco](diskusage.md#DISK-USAGE)
+ [27.6.2. Falha de esgotamento do disco](diskusage.md#DISK-FULL)

Um administrador de banco de dados frequentemente se pergunta: “O que o sistema está fazendo agora?” Este capítulo discute como descobrir isso.

Várias ferramentas estão disponíveis para monitorar a atividade do banco de dados e analisar o desempenho. A maior parte deste capítulo é dedicada à descrição do sistema de estatísticas cumulativas do PostgreSQL, mas não se deve negligenciar programas regulares de monitoramento Unix, como `ps`, `top`, `iostat` e `vmstat`. Além disso, uma vez que se tenha identificado uma consulta com desempenho inadequado, pode ser necessário realizar uma investigação adicional usando o comando `EXPLAIN` do PostgreSQL. [Seção 14.1](using-explain.md "14.1. Using EXPLAIN") discute `EXPLAIN` e outros métodos para entender o comportamento de uma consulta individual.