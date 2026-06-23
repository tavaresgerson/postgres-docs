## 47.2. Conceitos de Decodificação Lógica [#](#LOGICALDECODING-EXPLANATION)

* [47.2.1. Decodificação Lógica][(logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-LOG-DEC)
* [47.2.2. Fendas de Replicação][(logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS)
* [47.2.3. Sincronização de Fenda de Replicação][(logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION)
* [47.2.4. Plugins de Saída][(logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-OUTPUT-PLUGINS)
* [47.2.5. Instantâneos Exportados][(logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-EXPORTED-SNAPSHOTS)

### 47.2.1. Decodificação lógica [#](#LOGICALDECODING-EXPLANATION-LOG-DEC)

A decodificação lógica é o processo de extrair todas as alterações persistentes nas tabelas de um banco de dados em um formato coerente e fácil de entender, que pode ser interpretado sem conhecimento detalhado do estado interno do banco de dados.

No PostgreSQL, a decodificação lógica é implementada decodificando o conteúdo do [registro de pré-aviso](wal.md), que descrevem as alterações em um nível de armazenamento, em uma forma específica para a aplicação, como um fluxo de tuplas ou declarações SQL.

### 47.2.2. Canais de replicação [#](#LOGICALDECODING-REPLICATION-SLOTS)

No contexto da replicação lógica, um slot representa um fluxo de alterações que podem ser reproduzidos para um cliente na ordem em que foram feitas no servidor de origem. Cada slot transmite uma sequência de alterações de um único banco de dados.

Nota

O PostgreSQL também possui slots de replicação em streaming (consulte a [Seção 26.2.5](warm-standby.md#STREAMING-REPLICATION)), mas eles são usados de maneira um pouco diferente lá.

Um slot de replicação tem um identificador que é único em todos os bancos de dados em um clúster PostgreSQL. Os slots persistem independentemente da conexão que os utiliza e são resistentes a falhas.

Um slot lógico emitirá cada alteração apenas uma vez no funcionamento normal. A posição atual de cada slot é persistida apenas no ponto de verificação, portanto, no caso de um crash, o slot pode retornar a um LSN anterior, o que fará com que as alterações recentes sejam enviadas novamente quando o servidor for reiniciado. Os clientes de decodificação lógica são responsáveis por evitar os efeitos negativos de lidar com a mesma mensagem mais de uma vez. Os clientes podem desejar registrar o último LSN que viram ao decodificar e ignorar qualquer dado repetido ou (ao usar o protocolo de replicação) solicitar que a decodificação comece a partir desse LSN, em vez de deixar o servidor determinar o ponto de início. O recurso de Rastreamento de Progresso da Replicação é projetado para esse propósito, consulte [origens de replicação](replication-origins.md).

Pode haver vários slots independentes para um único banco de dados. Cada slot tem seu próprio estado, permitindo que diferentes consumidores recebam alterações de diferentes pontos no fluxo de alterações do banco de dados. Para a maioria das aplicações, será necessário um slot separado para cada consumidor.

Um slot de replicação lógica não sabe nada sobre o estado do(s) receptor(es). É possível ter vários receptores diferentes usando o mesmo slot em diferentes momentos; eles apenas receberão as alterações que surgem a partir do momento em que o último receptor parou de consumi-las. Apenas um receptor pode consumir alterações de um slot em um determinado momento.

Um slot de replicação lógica também pode ser criado em um standby quente. Para evitar que o `VACUUM` remova as linhas necessárias dos catálogos do sistema, o `hot_standby_feedback` deve ser definido no standby. Apesar disso, se alguma linha necessária for removida, o slot fica inválido. É altamente recomendável usar um slot físico entre o principal e o standby. Caso contrário, o `hot_standby_feedback` funcionará, mas apenas enquanto a conexão estiver ativa (por exemplo, um reinício do nó a quebrará). Em seguida, o principal pode excluir as linhas do catálogo do sistema que possam ser necessárias pela decodificação lógica no standby (já que ele não sabe sobre o `catalog_xmin` no standby). Os slots lógicos existentes no standby também ficam inválidos se o `wal_level` no principal for reduzido para menos que `logical`. Isso é feito assim que o standby detecta tal mudança no fluxo WAL. Isso significa que, para walsenders que estão atrasados (se houver algum), alguns registros WAL até a mudança do parâmetro `wal_level` no principal não serão decodificados.

A criação de um slot lógico requer informações sobre todas as transações atualmente em execução. No primário, essas informações estão disponíveis diretamente, mas em standby, essas informações precisam ser obtidas do primário. Assim, a criação de um slot lógico pode precisar esperar que alguma atividade ocorra no primário. Se o primário estiver parado, a criação de um slot lógico em standby pode levar um tempo notável. Isso pode ser acelerado chamando a função `pg_log_standby_snapshot` no primário.

### Atenção

Os slots de replicação persistem mesmo em falhas e não sabem nada sobre o estado de seu(s) consumidor(es). Eles impedirão a remoção dos recursos necessários, mesmo quando não há conexão usando-os. Isso consome armazenamento porque nem o WAL necessário nem as linhas necessárias dos catálogos do sistema podem ser removidas pelo `VACUUM` enquanto ainda forem necessárias por um slot de replicação. Em casos extremos, isso pode fazer com que o banco de dados seja desligado para evitar o enrolamento de ID de transação (consulte [Seção 24.1.5](routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)). Portanto, se um slot não for mais necessário, ele deve ser descartado.

### 47.2.3. Sincronização do Slot de Replicação [#](#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION)

Os slots de replicação lógica no primário podem ser sincronizados com o standby quente usando o parâmetro `failover` da opção (functions-admin.md#PG-CREATE-LOGICAL-REPLICATION-SLOT), ou usando a opção [`failover`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER) do `CREATE SUBSCRIPTION` durante a criação do slot. Além disso, é necessário habilitar [`sync_replication_slots`](runtime-config-replication.md#GUC-SYNC-REPLICATION-SLOTS) no standby. Ao habilitar [`sync_replication_slots`](runtime-config-replication.md#GUC-SYNC-REPLICATION-SLOTS) no standby, os slots de falha podem ser sincronizados periodicamente no trabalhador slotsync. Para que a sincronização funcione, é obrigatório ter um slot de replicação física entre o primário e o standby (ou seja, [`primary_slot_name`](runtime-config-replication.md#GUC-PRIMARY-SLOT-NAME) deve ser configurado no standby), e [`hot_standby_feedback`](runtime-config-replication.md#GUC-HOT-STANDBY-FEEDBACK) deve ser habilitado no standby. Também é necessário especificar um `dbname` válido no [`primary_conninfo`](runtime-config-replication.md#GUC-PRIMARY-CONNINFO). É altamente recomendável que o referido slot de replicação física seja nomeado na lista [`synchronized_standby_slots`](runtime-config-replication.md#GUC-SYNCHRONIZED-STANDBY-SLOTS) no primário, para evitar que o assinante consuma as alterações mais rápido do que o standby quente. Mesmo quando corretamente configurado, espera-se alguma latência ao enviar alterações para assinantes lógicos devido à espera em slots nomeados em [`synchronized_standby_slots`](runtime-config-replication.md#GUC-SYNCHRONIZED-STANDBY-SLOTS). Quando o `synchronized_standby_slots` é utilizado, o servidor primário não será completamente desligado até que os correspondentes standby, associados aos slots de replicação física especificados em `synchronized_standby_slots`, tenham confirmado a recepção do WAL até a posição mais recente esvaziada no servidor primário.

Nota

Embora a habilitação de `sync_replication_slots` permita a sincronização periódica automática dos slots de falha, eles também podem ser sincronizados manualmente usando a função `pg_sync_replication_slots` no modo standby. No entanto, essa função é destinada principalmente a testes e depuração e deve ser usada com cautela. Ao contrário da sincronização automática, ela não inclui tentativas cíclicas, tornando-a mais propensa a falhas de sincronização, particularmente durante cenários de sincronização inicial, onde os arquivos WAL ou as linhas do catálogo necessários para o slot podem já ter sido removidos ou estão em risco de serem removidos no modo standby. Em contraste, a sincronização automática via `sync_replication_slots` fornece atualizações contínuas de slots, permitindo uma falha de falha sem problemas e suportando alta disponibilidade. Portanto, é o método recomendado para sincronizar slots.

Quando a sincronização de slots é configurada conforme recomendado e a sincronização inicial é realizada automaticamente ou manualmente via `pg_sync_replication_slots`, o standby pode persistir o slot sincronizado apenas se a seguinte condição for atendida: O slot de replicação lógica no primário deve reter WALs e linhas do catálogo do sistema que ainda estão disponíveis no standby. Isso garante a integridade dos dados e permite que a replicação lógica continue sem problemas após a promoção. Se as WALs ou linhas do catálogo necessárias já tiverem sido apagadas do standby, o slot não será persistido para evitar a perda de dados. Nesses casos, a seguinte mensagem de log pode aparecer:

```
LOG:  could not synchronize replication slot "failover_slot"
DETAIL:  Synchronization could lead to data loss, because the remote slot needs WAL at LSN 0/3003F28 and catalog xmin 754, but the standby has LSN 0/3003F28 and catalog xmin 756.
```

Se o slot de replicação lógica estiver sendo ativamente utilizado por um consumidor, não é necessário nenhuma intervenção manual; o slot avançará automaticamente e a sincronização será retomada no próximo ciclo. No entanto, se nenhum consumidor estiver configurado, é aconselhável avançar manualmente o slot no primário usando `pg_logical_slot_get_changes`(functions-admin.md#PG-LOGICAL-SLOT-GET-CHANGES) ou `pg_logical_slot_get_binary_changes`(functions-admin.md#PG-LOGICAL-SLOT-GET-BINARY-CHANGES), permitindo que a sincronização prossiga.

A capacidade de retomar a replicação lógica após o failover depende do valor de [pg_replication_slots](view-pg-replication-slots.md).`synced` para os slots sincronizados no standby no momento do failover. Apenas os slots persistentes que tenham atingido o estado sincronizado como verdadeiro no standby antes do failover podem ser usados para replicação lógica após o failover. Os slots sincronizados temporários não podem ser usados para decodificação lógica, portanto, a replicação lógica para esses slots não pode ser retomada. Por exemplo, se o slot sincronizado não puder se tornar persistente no standby devido a uma assinatura desativada, então a assinatura não pode ser retomada após o failover, mesmo quando é ativada.

Para retomar a replicação lógica após a falha do failover dos slots lógicos sincronizados, a 'conninfo' da assinatura deve ser alterada para apontar para o novo servidor primário. Isso é feito usando `ALTER SUBSCRIPTION ... CONNECTION`(sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-CONNECTION). Recomenda-se que as assinaturas sejam desativadas primeiro antes de promover o modo standby e sejam reativadas após a alteração da cadeia de conexão.

### Atenção

Há uma chance de que o antigo servidor primário volte a estar disponível durante a promoção e, se as assinaturas não forem desativadas, os assinantes lógicos podem continuar a receber dados do servidor primário antigo mesmo após a promoção, até que a cadeia de conexão seja alterada. Isso pode resultar em problemas de inconsistência de dados, impedindo que os assinantes lógicos possam continuar a replicação do novo servidor primário.

### 47.2.4. Plugins de saída [#](#LOGICALDECODING-EXPLANATION-OUTPUT-PLUGINS)

Os plugins de saída transformam os dados da representação interna do log de pré-escrita no formato que o consumidor de um slot de replicação deseja.

### 47.2.5. Snapshots exportados [#](#LOGICALDECODING-EXPLANATION-EXPORTED-SNAPSHOTS)

Quando um novo intervalo de replicação é criado usando a interface de replicação em streaming (consulte [CREATE_REPLICATION_SLOT](protocol-replication.md#PROTOCOL-REPLICATION-CREATE-REPLICATION-SLOT)), um instantâneo é exportado (consulte [Seção 9.28.5](functions-admin.md#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION "9.28.5. Snapshot Synchronization Functions")), que mostrará exatamente o estado do banco de dados, após o qual todas as alterações serão incluídas no fluxo de alterações. Isso pode ser usado para criar uma nova replica usando [`SET TRANSACTION SNAPSHOT`](sql-set-transaction.md "SET TRANSACTION") para ler o estado do banco de dados no momento em que o intervalo foi criado. Essa transação pode então ser usada para drenar o estado do banco de dados naquele momento, que posteriormente pode ser atualizado usando o conteúdo do intervalo sem perder nenhuma alteração.

Aplicações que não exigem exportação de instantâneo podem suprimi-la com a opção `SNAPSHOT 'nothing'`.