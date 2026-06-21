## 47.3. Protocolo de Replicação de Streaming Interface [#](#LOGICALDECODING-WALSENDER)

Os comandos

* `CREATE_REPLICATION_SLOT slot_name LOGICAL output_plugin`
* `DROP_REPLICATION_SLOT slot_name` [ `WAIT` ]
* `START_REPLICATION SLOT slot_name LOGICAL ...`

são usados para criar, descartar e transmitir alterações de um intervalo de replicação, respectivamente. Esses comandos só estão disponíveis através de uma conexão de replicação; eles não podem ser usados via SQL. Consulte [Seção 54.4][(protocol-replication.md "54.4. Streaming Replication Protocol")] para obter detalhes sobre esses comandos.

O comando [pg_recvlogical](app-pgrecvlogical.md "pg_recvlogical") pode ser usado para controlar a decodificação lógica em uma conexão de replicação em fluxo. (Ele usa esses comandos internamente.)