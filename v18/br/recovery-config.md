## O.1. O arquivo `recovery.conf` foi incorporado ao `postgresql.conf` [#](#RECOVERY-CONFIG)

O PostgreSQL 11 e versões anteriores utilizavam um arquivo de configuração chamado `recovery.conf` para gerenciar réplicas e standby. O suporte a esse arquivo foi removido no PostgreSQL 12. Consulte as notas de lançamento do PostgreSQL 12 [(release-prior.md "E.6. Prior Releases") para obter detalhes sobre essa mudança.

Em PostgreSQL 12 e superior, [recuperação de arquivo, replicação em fluxo e PITR](continuous-archiving.md "25.3. Continuous Archiving and Point-in-Time Recovery (PITR) são configurados usando [parâmetros de configuração normal do servidor](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-STANDBY "19.6.3. Standby Servers"). Esses são definidos em `postgresql.conf` ou por meio de [ALTER SYSTEM](sql-altersystem.md "ALTER SYSTEM") como qualquer outro parâmetro.

O servidor não será iniciado se existir um `recovery.conf`.

PostgreSQL 15 e versões anteriores tinham uma configuração `promote_trigger_file`, ou `trigger_file` antes do 12. Use `pg_ctl promote` ou chame `pg_promote()` para promover um modo de espera em vez disso.

O ajuste `standby_mode` foi removido. Um arquivo `standby.signal` no diretório de dados é usado em vez disso. Veja [Operação do servidor em espera](warm-standby.md#STANDBY-SERVER-OPERATION "26.2.2. Standby Server Operation") para detalhes.