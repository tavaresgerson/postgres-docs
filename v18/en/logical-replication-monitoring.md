## 29.10. Monitoring [#](#LOGICAL-REPLICATION-MONITORING)

Because logical replication is based on a similar architecture as [physical streaming replication](warm-standby.md#STREAMING-REPLICATION "26.2.5. Streaming Replication"), the monitoring on a publication node is similar to monitoring of a physical replication primary (see [Section 26.2.5.2](warm-standby.md#STREAMING-REPLICATION-MONITORING "26.2.5.2. Monitoring")).

The monitoring information about subscription is visible in [`pg_stat_subscription`](monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION "27.2.8. pg_stat_subscription"). This view contains one row for every subscription worker. A subscription can have zero or more active subscription workers depending on its state.

Normally, there is a single apply process running for an enabled subscription. A disabled subscription or a crashed subscription will have zero rows in this view. If the initial data synchronization of any table is in progress, there will be additional workers for the tables being synchronized. Moreover, if the [`streaming`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-STREAMING) transaction is applied in parallel, there may be additional parallel apply workers.
