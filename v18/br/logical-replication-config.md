## 29.12. Configurações de configuração [#](#LOGICAL-REPLICATION-CONFIG)

* [29.12.1. Editores](logical-replication-config.md#LOGICAL-REPLICATION-CONFIG-PUBLISHER)
* [29.12.2. Assinantes](logical-replication-config.md#LOGICAL-REPLICATION-CONFIG-SUBSCRIBER)

A replicação lógica exige que várias opções de configuração sejam definidas. Essas opções são relevantes apenas em um dos lados da replicação.

### 29.12.1. Editores [#](#LOGICAL-REPLICATION-CONFIG-PUBLISHER)

`wal_level`](runtime-config-wal.md#GUC-WAL-LEVEL) deve ser definido como `logical`.

`max_replication_slots`](runtime-config-replication.md#GUC-MAX-REPLICATION-SLOTS) deve ser definido como no mínimo o número de assinaturas esperadas para se conectar, mais uma reserva para a sincronização da tabela.

Os slots de replicação lógica também são afetados por `idle_replication_slot_timeout`(runtime-config-replication.md#GUC-IDLE-REPLICATION-SLOT-TIMEOUT).

`max_wal_senders`](runtime-config-replication.md#GUC-MAX-WAL-SENDERS) deve ser definido como no mínimo o mesmo que `max_replication_slots`, mais o número de réplicas físicas que estão conectadas ao mesmo tempo.

A replicação lógica walsender também é afetada por `wal_sender_timeout` (runtime-config-replication.md#GUC-WAL-SENDER-TIMEOUT).

### 29.12.2. Subscritores [#](#LOGICAL-REPLICATION-CONFIG-SUBSCRIBER)

`max_active_replication_origins`](runtime-config-replication.md#GUC-MAX-ACTIVE-REPLICATION-ORIGINS) deve ser definido como pelo menos o número de assinaturas que serão adicionadas ao assinante, mais uma reserva para a sincronização da tabela.

`max_logical_replication_workers`](runtime-config-replication.md#GUC-MAX-LOGICAL-REPLICATION-WORKERS) deve ser definido como no mínimo o número de assinaturas (para o líder aplicar trabalhadores), mais uma reserva para os trabalhadores de sincronização de tabela e os trabalhadores de aplicação paralela.

`max_worker_processes` (runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES) pode precisar ser ajustado para acomodar trabalhadores de replicação, pelo menos (`max_logical_replication_workers` (runtime-config-replication.md#GUC-MAX-LOGICAL-REPLICATION-WORKERS)) + `1`. Observe que algumas extensões e consultas paralelas também pedem slots de trabalhadores de `max_worker_processes`.

`max_sync_workers_per_subscription`](runtime-config-replication.md#GUC-MAX-SYNC-WORKERS-PER-SUBSCRIPTION) controla a quantidade de paralelismo da cópia inicial de dados durante a inicialização da assinatura ou quando novas tabelas são adicionadas.

`max_parallel_apply_workers_per_subscription`](runtime-config-replication.md#GUC-MAX-PARALLEL-APPLY-WORKERS-PER-SUBSCRIPTION) controla a quantidade de paralelismo para o streaming de transações em andamento com o parâmetro de assinatura `streaming = parallel`.

Os trabalhadores de replicação lógica também são afetados por `wal_receiver_timeout`(runtime-config-replication.md#GUC-WAL-RECEIVER-TIMEOUT), [`wal_receiver_status_interval`](runtime-config-replication.md#GUC-WAL-RECEIVER-STATUS-INTERVAL) e [`wal_retrieve_retry_interval`(runtime-config-replication.md#GUC-WAL-RETRIEVE-RETRY-INTERVAL).