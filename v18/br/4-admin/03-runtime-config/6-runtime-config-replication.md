## 19.6. Replicação [#](#RUNTIME-CONFIG-REPLICATION)

* [19.6.1. Servidores de envio](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-SENDER)
* [19.6.2. Servidor principal](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-PRIMARY)
* [19.6.3. Servidores de reserva](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-STANDBY)
* [19.6.4. Subscritores](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-SUBSCRIBER)

Esses ajustes controlam o comportamento do recurso de *replicação em streaming* integrado (consulte [Seção 26.2.5](warm-standby.md#STREAMING-REPLICATION)) e do recurso de *replicação lógica* integrado (consulte [Capítulo 29](logical-replication.md)).

Para a *replicação em fluxo*, os servidores serão servidores primários ou de reserva. Os primários podem enviar dados, enquanto os de reserva são sempre receptores de dados replicados. Quando a replicação em cascata (ver [Seção 26.2.7](warm-standby.md#CASCADING-REPLICATION)) é usada, os servidores de reserva também podem ser emissores, bem como receptores. Os parâmetros são principalmente para servidores de envio e de reserva, embora alguns parâmetros tenham significado apenas no servidor primário. As configurações podem variar sem problemas em todo o clúster se isso for necessário.

Para a *replicação lógica*, os *publicadores* (servidores que fazem `CREATE PUBLICATION`)(sql-createpublication.md "CREATE PUBLICATION") replicam dados para os *subscritores* (servidores que fazem `CREATE SUBSCRIPTION`)(sql-createsubscription.md "CREATE SUBSCRIPTION"). Os servidores também podem ser publicadores e assinantes ao mesmo tempo. Observe que as seções seguintes se referem aos publicadores como "emitentes". Para mais detalhes sobre as configurações de configuração de replicação lógica, consulte [Seção 29.12](logical-replication-config.md "29.12. Configuration Settings").

### 19.6.1. Servidores de envio [#](#RUNTIME-CONFIG-REPLICATION-SENDER)

Esses parâmetros podem ser configurados em qualquer servidor que deve enviar dados de replicação para um ou mais servidores de espera. O primário é sempre um servidor de envio, portanto, esses parâmetros devem ser sempre configurados no primário. O papel e o significado desses parâmetros não mudam após um servidor de espera se tornar o primário.

`max_wal_senders` (`integer`) [#](#GUC-MAX-WAL-SENDERS): Especifica o número máximo de conexões concorrentes dos servidores de reserva ou clientes de backup de streaming (ou seja, o número máximo de processos de emissor WAL que podem ser executados simultaneamente). O padrão é `10`. O valor `0` significa que a replicação está desativada. A desconexão abrupta de um cliente de streaming pode deixar um slot de conexão órfã até que um tempo de espera seja atingido, portanto, este parâmetro deve ser ajustado um pouco mais alto que o número máximo de clientes esperados, para que os clientes desconectados possam se reconectar imediatamente. Este parâmetro só pode ser ajustado no início do servidor. Além disso, `wal_level` deve ser ajustado para `replica` ou superior para permitir conexões dos servidores de reserva.

Ao executar um servidor de espera, você deve definir esse parâmetro no mesmo valor ou superior ao do servidor primário. Caso contrário, as consultas não serão permitidas no servidor de espera.

`max_replication_slots` (`integer`) [#](#GUC-MAX-REPLICATION-SLOTS): Especifica o número máximo de slots de replicação (ver [Seção 26.2.6] (warm-standby.md#STREAMING-REPLICATION-SLOTS "26.2.6. Replication Slots")) que o servidor pode suportar. O padrão é 10. Este parâmetro só pode ser definido no início do servidor. Definí-lo com um valor menor que o número de slots de replicação atualmente existentes impedirá o início do servidor. Além disso, `wal_level` deve ser definido como `replica` ou superior para permitir que os slots de replicação sejam usados.

`wal_keep_size` (`integer`) [#](#GUC-WAL-KEEP-SIZE): Especifica o tamanho mínimo dos arquivos WAL mantidos no diretório `pg_wal`, caso um servidor de espera precise obtê-los para replicação em streaming. Se um servidor de espera conectado ao servidor de envio ficar para trás em mais de `wal_keep_size` megabytes, o servidor de envio pode remover um segmento WAL ainda necessário pelo servidor de espera, nesse caso, a conexão de replicação será terminada. Conexões subsequentes também falharão como resultado. (No entanto, o servidor de espera pode se recuperar ao obter o segmento do arquivo, se o arquivamento WAL estiver em uso.)

Isso define apenas o tamanho mínimo dos segmentos retidos em `pg_wal`; o sistema pode precisar reter mais segmentos para arquivamento WAL ou para recuperação de um ponto de verificação. Se `wal_keep_size` for zero (o padrão), o sistema não mantém nenhum segmento extra para fins de standby, portanto, o número de segmentos antigos do WAL disponíveis para servidores de standby é uma função da localização do ponto de verificação anterior e do status do arquivamento WAL. Se este valor for especificado sem unidades, ele é considerado em megabytes. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`max_slot_wal_keep_size` (`integer`) [#](#GUC-MAX-SLOT-WAL-KEEP-SIZE): Especifique o tamanho máximo dos arquivos WAL que os slots de replicação podem reter no diretório `pg_wal` no momento do ponto de verificação. Se `max_slot_wal_keep_size` for -1 (o padrão), os slots de replicação podem reter uma quantidade ilimitada de arquivos WAL. Caso contrário, se o restart_lsn de um slot de replicação ficar atrás do LSN atual em mais de tamanho dado, o standby que está usando o slot pode não ser mais capaz de continuar a replicação devido à remoção dos arquivos WAL necessários. Você pode ver a disponibilidade de WAL dos slots de replicação em [pg_replication_slots](view-pg-replication-slots.md "53.20. pg_replication_slots"). Se este valor for especificado sem unidades, ele é considerado em megabytes. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`idle_replication_slot_timeout` (`integer`) [#](#GUC-IDLE-REPLICATION-SLOT-TIMEOUT): Invalida os slots de replicação que permaneceram inativos (não utilizados por uma conexão de replicação) por mais tempo do que este período. Se este valor for especificado sem unidades, ele é considerado em segundos. Um valor de zero (padrão) desativa o mecanismo de invalidação do tempo de espera em inatividade. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

A invalidação de slot devido ao tempo de espera em atividade ocorre durante o ponto de verificação. Como os pontos de verificação ocorrem em intervalos de `checkpoint_timeout`, pode haver um atraso entre o momento em que o `idle_replication_slot_timeout` foi excedido e quando a invalidação do slot é acionada no próximo ponto de verificação. Para evitar tais atrasos, os usuários podem forçar um ponto de verificação a invalidar prontamente os slots inativos. A duração da inatividade do slot é calculada usando o valor do slot [pg_replication_slots](view-pg-replication-slots.md "53.20. pg_replication_slots").`inactive_since`.

Observe que o mecanismo de invalidação do tempo de espera em branco não é aplicável para faixas que não reservam WAL ou para faixas no servidor de espera que estão sendo sincronizadas a partir do servidor primário (ou seja, faixas de espera que têm o valor [pg_replication_slots](view-pg-replication-slots.md "53.20. pg_replication_slots").`synced`). As faixas sincronizadas são sempre consideradas inativas porque elas não realizam decodificação lógica para produzir mudanças.

`wal_sender_timeout` (`integer`) [#](#GUC-WAL-SENDER-TIMEOUT): Interrompa as conexões de replicação que estão inativas por mais tempo do que esse período. Isso é útil para o servidor de envio detectar um acidente de espera ou interrupção de rede. Se esse valor for especificado sem unidades, ele é considerado em milissegundos. O valor padrão é de 60 segundos. Um valor de zero desativa o mecanismo de tempo limite.

Com um grupo distribuído em várias localidades geográficas, usar diferentes valores por localização traz mais flexibilidade na gestão do grupo. Um valor menor é útil para detecção mais rápida de falhas com um standby que tem uma conexão de rede de baixa latência, e um valor maior ajuda a julgar melhor a saúde de um standby se localizado em uma localização remota, com uma conexão de rede de alta latência.

`track_commit_timestamp` (`boolean`) [#](#GUC-TRACK-COMMIT-TIMESTAMP): Registre o tempo de compromisso das transações. Este parâmetro só pode ser definido no início do servidor. O valor padrão é `off`.

### 19.6.2. Servidor primário [#](#RUNTIME-CONFIG-REPLICATION-PRIMARY)

Esses parâmetros podem ser definidos no servidor principal que deve enviar dados de replicação para um ou mais servidores de espera. Observe que, além desses parâmetros, [wal_level](runtime-config-wal.md#GUC-WAL-LEVEL) deve ser definido apropriadamente no servidor principal, e opcionalmente, o arquivamento WAL também pode ser habilitado (consulte [Seção 19.5.3](runtime-config-wal.md#RUNTIME-CONFIG-WAL-ARCHIVING)). Os valores desses parâmetros nos servidores de espera são irrelevantes, embora você possa desejar defini-los lá, em preparação para a possibilidade de um servidor de espera se tornar o principal.

`synchronous_standby_names` (`string`) [#](#GUC-SYNCHRONOUS-STANDBY-NAMES): Especifica uma lista de servidores de espera que podem suportar *replicação síncrona*, conforme descrito em [Seção 26.2.8](warm-standby.md#SYNCHRONOUS-REPLICATION "26.2.8. Synchronous Replication"). Haverá um ou mais servidores síncronos ativos; as transações que aguardam confirmação serão permitidas a prosseguir após esses servidores de espera confirmarem a recepção de seus dados. Os servidores síncronos serão aqueles cujos nomes aparecem nesta lista e que estão atualmente conectados e transmitindo dados em tempo real (como mostrado por um estado de `streaming` na visão do [`pg_stat_replication`](monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-VIEW "27.2.4. pg_stat_replication")). Especificar mais de um servidor síncrono pode permitir uma disponibilidade muito alta e proteção contra perda de dados.

O nome de um servidor de espera para este propósito é o ajuste `application_name` do standby, conforme definido nas informações de conexão do standby. Em caso de standby de replicação física, este deve ser definido no ajuste `primary_conninfo`; o padrão é o ajuste de [cluster_name](runtime-config-logging.md#GUC-CLUSTER-NAME), se definido, caso contrário, `walreceiver`. Para replicação lógica, este pode ser definido nas informações de conexão da assinatura, e o padrão é o nome da assinatura. Para outros consumidores de fluxo de replicação, consulte a documentação deles.

Este parâmetro especifica uma lista de servidores de espera usando uma das seguintes sintaxes:

```
[FIRST] num_sync ( standby_name [, ...] ) ANY num_sync ( standby_name [, ...] ) standby_name [, ...]
```

onde *`num_sync`* é o número de standby síncronos para os quais as transações precisam esperar respostas, e *`standby_name`* é o nome de um servidor de standby. *`num_sync`* deve ser um valor inteiro maior que zero. `FIRST` e `ANY` especificam o método para escolher standby síncronos dos servidores listados.

A palavra-chave `FIRST`, juntamente com *`num_sync`*, especifica uma replicação síncrona baseada em prioridade e faz com que os compromissos de transação esperem até que seus registros WAL sejam replicados para os *`num_sync`* stand-by síncronos escolhidos com base em suas prioridades. Por exemplo, uma configuração de `FIRST 3 (s1, s2, s3, s4)` fará com que cada compromisso espere respostas de três stand-by de maior prioridade escolhidos dos servidores stand-by `s1`, `s2`, `s3` e `s4`. Os stand-by cujos nomes aparecem mais cedo na lista têm prioridade maior e serão considerados como síncronos. Outros servidores stand-by que aparecem mais tarde nesta lista representam potenciais stand-by síncronos. Se qualquer um dos stand-by síncronos atuais se desconectar por qualquer motivo, ele será imediatamente substituído pelo próximo stand-by de maior prioridade. A palavra-chave `FIRST` é opcional.

A palavra-chave `ANY`, juntamente com *`num_sync`*, especifica uma replicação síncrona baseada em quórum e faz com que os compromissos de transação esperem até que seus registros WAL sejam replicados para *pelo menos* *`num_sync`* standby listados. Por exemplo, uma configuração de `ANY 3 (s1, s2, s3, s4)` fará com que cada compromisso seja processado assim que pelo menos três standby de `s1`, `s2`, `s3` e `s4` respondam.

`FIRST` e `ANY` são sensíveis a maiúsculas e minúsculas. Se essas palavras-chave forem usadas como o nome de um servidor de espera, seu *`standby_name`* deve ser citado em duplicado.

A terceira sintaxe foi usada antes da versão 9.6 do PostgreSQL e ainda é suportada. É a mesma sintaxe da primeira, com `FIRST` e *`num_sync`* iguais a 1. Por exemplo, `FIRST 1 (s1, s2)` e `s1, s2` têm o mesmo significado: ou `s1` ou `s2` é escolhido como um standby síncrono.

A entrada especial `*` corresponde a qualquer nome de espera.

Não há mecanismo para impor a unicidade dos nomes de standby. Em caso de duplicatas, um dos standby correspondentes será considerado de maior prioridade, embora exatamente qual seja indeterminado.

Nota

Cada *`standby_name`* deve ter a forma de um identificador SQL válido, a menos que seja `*`. Você pode usar aspas duplas, se necessário. Mas observe que os *`standby_name`* são comparados aos nomes de aplicativos de espera de forma insensível ao caso, seja com aspas duplas ou

Se não forem especificados nomes de standby síncronos aqui, a replicação síncrona não será habilitada e os compromissos de transação não aguardarão a replicação. Esta é a configuração padrão. Mesmo quando a replicação síncrona é habilitada, as transações individuais podem ser configuradas para não aguardar a replicação, definindo o parâmetro [synchronous_commit](runtime-config-wal.md#GUC-SYNCHRONOUS-COMMIT) para `local` ou `off`.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`synchronized_standby_slots` (`string`) [#](#GUC-SYNCHRONIZED-STANDBY-SLOTS): Uma lista de nomes de slots de standby de replicação em streaming separados por vírgula que os processos de emissor lógico de WAL esperam. Os processos de emissor lógico de WAL enviarão as alterações decodificadas aos plugins apenas após os slots de replicação especificados confirmarem a recepção do WAL. Isso garante que os slots de falha de replicação lógica não consumam as alterações até que essas alterações sejam recebidas e esvaziadas para os stand-by físicos correspondentes. Se uma conexão de replicação lógica for destinada a mudar para um stand-by físico após a promoção do stand-by, o slot de replicação física para o stand-by deve ser listado aqui. Observe que a replicação lógica não prosseguirá se os slots especificados em `synchronized_standby_slots` não existirem ou forem invalidados. Além disso, as funções de gerenciamento de replicação [`pg_replication_slot_advance`](functions-admin.md#PG-REPLICATION-SLOT-ADVANCE), [`pg_logical_slot_get_changes`](functions-admin.md#PG-LOGICAL-SLOT-GET-CHANGES) e [`pg_logical_slot_peek_changes`](functions-admin.md#PG-LOGICAL-SLOT-PEEK-CHANGES), quando usadas com slots de falha lógica, bloquearão até que todos os slots físicos especificados em `synchronized_standby_slots` tenham confirmado a recepção do WAL.

Os standby correspondentes aos slots de replicação física em `synchronized_standby_slots` devem configurar `sync_replication_slots = true` para que possam receber mudanças de slot de falha lógica do primário.

### 19.6.3. Servidores em espera [#](#RUNTIME-CONFIG-REPLICATION-STANDBY)

Esses ajustes controlam o comportamento de um [servidor em espera](warm-standby.md#STANDBY-SERVER-OPERATION) que deve receber dados de replicação. Seus valores no servidor principal são irrelevantes.

`primary_conninfo` (`string`) [#](#GUC-PRIMARY-CONNINFO): Especifica uma cadeia de conexão a ser usada para que o servidor de espera se conecte a um servidor de envio. Essa cadeia de conexão está no formato descrito em [Seção 32.1.1] (libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings"). Se qualquer opção não for especificada nessa cadeia de conexão, então a variável de ambiente correspondente (ver [Seção 32.15] (libpq-envars.md "32.15. Environment Variables")) é verificada. Se a variável de ambiente não for definida, então os valores padrão são usados.

A cadeia de conexão deve especificar o nome (ou endereço) do servidor de envio, bem como o número de porta, se não for o mesmo que o padrão do servidor de reserva. Além disso, especifique um nome de usuário correspondente a um papel com privilégios adequados no servidor de envio (consulte [Seção 26.2.5.1](warm-standby.md#STREAMING-REPLICATION-AUTHENTICATION)). Também é necessário fornecer uma senha, se o remetente exigir autenticação por senha. Ela pode ser fornecida na cadeia de `primary_conninfo`, ou em um arquivo separado de `~/.pgpass` no servidor de reserva (use `replication` como o nome do banco de dados).

Para a sincronização de slots de replicação (consulte [Seção 47.2.3](logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION)), também é necessário especificar um `dbname` válido na string `primary_conninfo`. Isso será usado apenas para sincronização de slots. É ignorado para streaming.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. Se este parâmetro for alterado enquanto o processo de recepção WAL estiver em execução, esse processo é sinalizado para ser desligado e espera-se que seja reiniciado com a nova configuração (exceto se `primary_conninfo` for uma string vazia). Este ajuste não tem efeito se o servidor não estiver no modo standby.

`primary_slot_name` (`string`) [#](#GUC-PRIMARY-SLOT-NAME): Especifica opcionalmente um intervalo de replicação existente a ser utilizado ao se conectar ao servidor de envio por replicação em streaming para controlar a remoção de recursos no nó upstream (ver [Seção 26.2.6](warm-standby.md#STREAMING-REPLICATION-SLOTS)). Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. Se este parâmetro for alterado enquanto o processo do receptor WAL estiver em execução, esse processo é sinalizado para ser desligado e espera-se que seja reiniciado com a nova configuração. Este ajuste não tem efeito se `primary_conninfo` não for definido ou se o servidor não estiver no modo standby.

`hot_standby` (`boolean`) [#](#GUC-HOT-STANDBY): Especifica se é possível conectar e executar consultas durante a recuperação, conforme descrito em [Seção 26.4](hot-standby.md "26.4. Hot Standby"). O valor padrão é `on`. Este parâmetro só pode ser definido no início do servidor. Ele só tem efeito durante a recuperação de arquivo ou no modo standby.

`max_standby_archive_delay` (`integer`) [#](#GUC-MAX-STANDBY-ARCHIVE-DELAY): Quando o modo quente de espera estiver ativo, este parâmetro determina quanto tempo o servidor de espera deve esperar antes de cancelar as consultas de espera que estejam em conflito com as entradas WAL que estão prestes a ser aplicadas, conforme descrito em [Seção 26.4.2](hot-standby.md#HOT-STANDBY-CONFLICT "26.4.2. Handling Query Conflicts"). `max_standby_archive_delay` se aplica quando os dados do WAL estão sendo lidos do arquivo WAL (e, portanto, não são atualizados). Se este valor for especificado sem unidades, ele é considerado em milissegundos. O padrão é 30 segundos. Um valor de -1 permite que o modo quente de espera espere para sempre que as consultas em conflito sejam concluídas. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

Observe que `max_standby_archive_delay` não é o mesmo que o período máximo de tempo em que uma consulta pode ser executada antes de ser cancelada; ao contrário, é o período total máximo permitido para aplicar os dados de qualquer um dos segmentos do WAL. Assim, se uma consulta resultou em um atraso significativo anteriormente no segmento do WAL, consultas conflitantes subsequentes terão muito menos tempo de gravidade.

`max_standby_streaming_delay` (`integer`) [#](#GUC-MAX-STANDBY-STREAMING-DELAY): Quando o modo quente de espera estiver ativo, este parâmetro determina quanto tempo o servidor de espera deve esperar antes de cancelar consultas de espera que estejam em conflito com as entradas WAL que estão prestes a ser aplicadas, conforme descrito em [Seção 26.4.2](hot-standby.md#HOT-STANDBY-CONFLICT "26.4.2. Handling Query Conflicts"). `max_standby_streaming_delay` é aplicado quando os dados do WAL estão sendo recebidos via replicação em fluxo. Se este valor for especificado sem unidades, ele é considerado em milissegundos. O padrão é 30 segundos. Um valor de -1 permite que o standby espere para sempre que as consultas em conflito sejam concluídas. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

Observe que `max_standby_streaming_delay` não é o mesmo que o período máximo de tempo em que uma consulta pode ser executada antes de ser cancelada; ao contrário, é o período total máximo permitido para aplicar os dados do WAL uma vez que eles tenham sido recebidos do servidor principal. Assim, se uma consulta resultou em um atraso significativo, as consultas subsequentes conflitantes terão muito menos tempo de gravidade até que o servidor de espera consiga novamente.

`wal_receiver_create_temp_slot` (`boolean`) [#](#GUC-WAL-RECEIVER-CREATE-TEMP-SLOT): Especifica se o processo receptor WAL deve criar um slot de replicação temporário na instância remota quando não tiver sido configurada uma slot de replicação permanente para uso (usando [primary_slot_name](runtime-config-replication.md#GUC-PRIMARY-SLOT-NAME)). O padrão é desligado. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. Se este parâmetro for alterado enquanto o processo receptor WAL estiver em execução, esse processo é sinalizado para ser desligado e espera-se que seja reiniciado com o novo ajuste.

`wal_receiver_status_interval` (`integer`) [#](#GUC-WAL-RECEIVER-STATUS-INTERVAL): Especifica a frequência mínima para o processo de receptor WAL no modo standby enviar informações sobre o progresso da replicação para o principal ou o standby upstream, onde elas podem ser visualizadas usando a vista [`pg_stat_replication`](monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-VIEW "27.2.4. pg_stat_replication"). O standby informará a última localização do log de pré-escrita que ele escreveu, a última posição que ele esvaziou no disco e a última posição que ele aplicou. O valor desse parâmetro é o período máximo entre os relatórios. As atualizações são enviadas sempre que as posições de escrita ou esvaziamento mudam, ou tão frequentemente quanto especificado por esse parâmetro, se definido para um valor não nulo. Há casos adicionais em que as atualizações são enviadas ignorando esse parâmetro; por exemplo, quando o processamento do WAL existente é concluído ou quando `synchronous_commit` é definido para `remote_apply`. Assim, a posição de aplicação pode ficar ligeiramente atrasada em relação à posição real. Se esse valor for especificado sem unidades, ele é considerado em segundos. O valor padrão é de 10 segundos. Esse parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`hot_standby_feedback` (`boolean`) [#](#GUC-HOT-STANDBY-FEEDBACK): Especifica se um standby quente enviará ou não feedback ao standby primário ou upstream sobre as consultas atualmente em execução no standby. Este parâmetro pode ser usado para eliminar cancelamentos de consulta causados por registros de limpeza, mas pode causar bloat no banco de dados primário para algumas cargas de trabalho. As mensagens de feedback não serão enviadas com mais frequência do que uma vez por `wal_receiver_status_interval`. O valor padrão é `off`. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

Se a replicação em cascata estiver em uso, o feedback é passado para o lado de cima até que ele eventualmente atinja o primário. Os standbys não fazem outro uso do feedback que recebem, além de passar para o lado de cima.

Observe que, se o relógio em espera for movido para a frente ou para trás, a mensagem de feedback pode não ser enviada no intervalo necessário. Em casos extremos, isso pode levar a um risco prolongado de não remover linhas mortas no primário por períodos prolongados, pois o mecanismo de feedback é baseado em marcações de tempo.

`wal_receiver_timeout` (`integer`) [#](#GUC-WAL-RECEIVER-TIMEOUT): Interrompa as conexões de replicação que estão inativas por mais tempo do que esse período. Isso é útil para o servidor de espera receptor detectar um crash do nó primário ou uma interrupção de rede. Se esse valor for especificado sem unidades, ele é considerado em milissegundos. O valor padrão é de 60 segundos. Um valor de zero desativa o mecanismo de tempo limite. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`wal_retrieve_retry_interval` (`integer`) [#](#GUC-WAL-RETRIEVE-RETRY-INTERVAL): Especifica quanto tempo o servidor de espera deve esperar quando os dados do WAL não estão disponíveis em nenhuma fonte (replicação em fluxo, local `pg_wal` ou arquivo WAL) antes de tentar novamente recuperar os dados do WAL. Se este valor for especificado sem unidades, ele é considerado em milissegundos. O valor padrão é de 5 segundos. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

Este parâmetro é útil em configurações onde um nó em recuperação precisa controlar o tempo que espera para que novos dados WAL estejam disponíveis. Por exemplo, na recuperação de arquivo, é possível tornar a recuperação mais responsiva na detecção de um novo arquivo WAL, reduzindo o valor deste parâmetro. Em um sistema com baixa atividade WAL, aumentando-o reduz a quantidade de solicitações necessárias para acessar os arquivos WAL, algo útil, por exemplo, em ambientes em nuvem, onde o número de vezes que uma infraestrutura é acessada é levado em consideração.

Na replicação lógica, esse parâmetro também limita a frequência com que um trabalhador de aplicação de sincronização de replicação falhando ou um trabalhador de sincronização de tabela será respawnado.

`recovery_min_apply_delay` (`integer`) [#](#GUC-RECOVERY-MIN-APPLY-DELAY): Por padrão, um servidor de espera restaura os registros WAL do servidor de envio o mais rápido possível. Pode ser útil ter uma cópia com atraso do tempo, oferecendo oportunidades para corrigir erros de perda de dados. Este parâmetro permite que você ative a recuperação com um período de tempo especificado. Por exemplo, se você definir este parâmetro para `5min`, o servidor de espera repetirá cada compromisso de transação apenas quando o tempo do sistema no servidor de espera estiver, pelo menos, cinco minutos após o horário de compromisso relatado pelo primário. Se este valor for especificado sem unidades, ele é considerado em milissegundos. O padrão é zero, sem adiamento.

É possível que o atraso de replicação entre os servidores exceda o valor deste parâmetro, no qual caso, nenhum atraso é adicionado. Note que o atraso é calculado entre o selo de tempo WAL conforme escrito no primário e a hora atual no de reserva. Os atrasos na transferência devido ao atraso de rede ou configurações de replicação em cascata podem reduzir significativamente o tempo de espera real. Se os relógios do sistema nos primário e de reserva não estiverem sincronizados, isso pode levar à recuperação de registros mais cedo do que o esperado; mas isso não é um problema grave, porque as configurações úteis deste parâmetro são muito maiores do que os típicos desvios de tempo entre os servidores.

O atraso ocorre apenas nos registros WAL para os commits de transação. Outros registros são regravados o mais rapidamente possível, o que não é um problema, porque as regras de visibilidade MVCC garantem que seus efeitos não sejam visíveis até que o registro de commit correspondente seja aplicado.

O atraso ocorre quando o banco de dados em recuperação atinge um estado consistente, até que o standby seja promovido ou acionado. Após isso, o standby terminará a recuperação sem mais espera.

Os registros do WAL devem ser mantidos em standby até estarem prontos para serem aplicados. Portanto, atrasos mais longos resultarão em um maior acúmulo de arquivos do WAL, aumentando os requisitos de espaço em disco para o diretório `pg_wal` do standby.

Este parâmetro é destinado para uso em implantações de replicação em streaming; no entanto, se o parâmetro for especificado, ele será respeitado em todos os casos, exceto na recuperação em caso de falha. `hot_standby_feedback` será atrasado pelo uso deste recurso, o que pode levar ao aumento do tamanho do primário; use ambos juntos com cuidado.

### Aviso

A replicação síncrona é afetada por essa configuração quando `synchronous_commit` está definido como `remote_apply`; cada `COMMIT` precisará esperar para ser aplicado.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`sync_replication_slots` (`boolean`) [#](#GUC-SYNC-REPLICATION-SLOTS): Permite um standby físico para sincronizar slots de falha lógica do servidor primário, de modo que os assinantes lógicos possam retomar a replicação a partir do novo servidor primário após a falha.

Ele é desativado por padrão. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

### 19.6.4. Subscritores [#](#RUNTIME-CONFIG-REPLICATION-SUBSCRIBER)

Esses ajustes controlam o comportamento de um assinante de replicação lógica. Seus valores no publicador são irrelevantes. Consulte [Seção 29.12](logical-replication-config.md) para mais detalhes.

`max_active_replication_origins` (`integer`) [#](#GUC-MAX-ACTIVE-REPLICATION-ORIGINS): Especifica quantas origens de replicação (ver [Capítulo 48](replication-origins.md "Chapter 48. Replication Progress Tracking")) podem ser rastreadas simultaneamente, limitando efetivamente quantas assinaturas de replicação lógicas podem ser criadas no servidor. Definindo-o para um valor menor que o número atual de origens de replicação rastreadas (refletido em [pg_replication_origin_status](view-pg-replication-origin-status.md "53.19. pg_replication_origin_status")) impedirá que o servidor seja iniciado. Ele tem como padrão 10. Este parâmetro só pode ser definido no início do servidor. `max_active_replication_origins` deve ser definido como pelo menos o número de assinaturas que serão adicionadas ao assinante, mais algumas reservas para a sincronização de tabelas.

`max_logical_replication_workers` (`integer`) [#](#GUC-MAX-LOGICAL-REPLICATION-WORKERS): Especifica o número máximo de trabalhadores de replicação lógica. Isso inclui trabalhadores de aplicar líder, trabalhadores de aplicar em paralelo e trabalhadores de sincronização de tabela.

Os trabalhadores de replicação lógica são retirados do conjunto definido por `max_worker_processes`.

O valor padrão é 4. Este parâmetro só pode ser definido no início do servidor.

`max_sync_workers_per_subscription` (`integer`) [#](#GUC-MAX-SYNC-WORKERS-PER-SUBSCRIPTION): Número máximo de trabalhadores de sincronização por assinatura. Este parâmetro controla a quantidade de paralelismo da cópia inicial de dados durante a inicialização da assinatura ou quando novas tabelas são adicionadas.

Atualmente, pode haver apenas um trabalhador de sincronização por tabela.

Os trabalhadores de sincronização são retirados do conjunto definido por `max_logical_replication_workers`.

O valor padrão é 2. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`max_parallel_apply_workers_per_subscription` (`integer`) [#](#GUC-MAX-PARALLEL-APPLY-WORKERS-PER-SUBSCRIPTION): Número máximo de trabalhadores de aplicação paralelos por assinatura. Este parâmetro controla a quantidade de paralelismo para o streaming de transações em andamento com o parâmetro de assinatura `streaming = parallel`.

Os trabalhadores paralelos são retirados do conjunto definido por `max_logical_replication_workers`.

O valor padrão é 2. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.