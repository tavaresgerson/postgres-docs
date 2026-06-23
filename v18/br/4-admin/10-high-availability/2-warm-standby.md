## 26.2. Servidores de standby em espera para log-shipping [#](#WARM-STANDBY)

* [26.2.1. Planejamento](warm-standby.md#STANDBY-PLANNING)
* [26.2.2. Operação de servidor em espera](warm-standby.md#STANDBY-SERVER-OPERATION)
* [26.2.3. Preparação do primário para servidores em espera](warm-standby.md#PREPARING-PRIMARY-FOR-STANDBY)
* [26.2.4. Configuração de um servidor em espera](warm-standby.md#STANDBY-SERVER-SETUP)
* [26.2.5. Replicação em fluxo](warm-standby.md#STREAMING-REPLICATION)
* [26.2.6. Fissuras de replicação](warm-standby.md#STREAMING-REPLICATION-SLOTS)
* [26.2.7. Replicação em cascata](warm-standby.md#CASCADING-REPLICATION)
* [26.2.8. Replicação síncrona](warm-standby.md#SYNCHRONOUS-REPLICATION)
* [26.2.9. Arquivamento contínuo em espera](warm-standby.md#CONTINUOUS-ARCHIVING-IN-STANDBY)

O arquivamento contínuo pode ser usado para criar uma configuração de clúster de *alta disponibilidade* (HA) com um ou mais *servidores de espera* prontos para assumir as operações se o servidor primário falhar. Essa capacidade é amplamente referida como *standby quente* ou *log shipping*.

O servidor primário e o servidor de reserva trabalham juntos para fornecer essa capacidade, embora os servidores estejam apenas mal acoplados. O servidor primário opera em modo de arquivamento contínuo, enquanto cada servidor de reserva opera em modo de recuperação contínua, lendo os arquivos WAL do primário. Não são necessárias alterações nas tabelas do banco de dados para habilitar essa capacidade, portanto, oferece baixo custo de administração em comparação com algumas outras soluções de replicação. Essa configuração também tem um impacto de desempenho relativamente baixo no servidor primário.

Mover diretamente os registros WAL de um servidor de banco de dados para outro é tipicamente descrito como log shipping. O PostgreSQL implementa o log shipping baseado em arquivos, transferindo registros WAL um arquivo (semente WAL) de cada vez. Arquivos WAL (16 MB) podem ser enviados facilmente e de forma barata por qualquer distância, seja para um sistema adjacente, outro sistema no mesmo local ou outro sistema no lado mais distante do globo. A largura de banda necessária para essa técnica varia de acordo com a taxa de transação do servidor primário. O log shipping baseado em registros é mais granular e transmite as alterações WAL de forma incremental por meio de uma conexão de rede (consulte [Seção 26.2.5](warm-standby.md#STREAMING-REPLICATION)).

Deve-se notar que o envio de logs é assíncrono, ou seja, os registros do WAL são enviados após o compromisso da transação. Como resultado, há uma janela para perda de dados caso o servidor primário sofra uma falha catastrófica; as transações ainda não enviadas serão perdidas. O tamanho da janela de perda de dados no envio de logs baseado em arquivos pode ser limitado pelo uso do parâmetro `archive_timeout`, que pode ser definido como baixo, no mínimo, alguns segundos. No entanto, uma configuração tão baixa aumentará substancialmente a largura de banda necessária para o envio de arquivos. A replicação em fluxo (ver [Seção 26.2.5](warm-standby.md#STREAMING-REPLICATION)) permite uma janela de perda de dados muito menor.

O desempenho de recuperação é suficientemente bom para que o modo de espera geralmente esteja apenas a alguns momentos de disponibilidade total, uma vez que tenha sido ativado. Como resultado, isso é chamado de configuração de espera quente, que oferece alta disponibilidade. Restaurar um servidor a partir de um backup arquivado e o rollforward levará muito mais tempo, portanto, essa técnica oferece apenas uma solução para a recuperação de desastres, não alta disponibilidade. Um servidor de espera também pode ser usado para consultas de leitura, nesse caso, é chamado de servidor de *espera quente*. Consulte [Seção 26.4] para obter mais informações. [(hot-standby.md "26.4. Hot Standby")]

### 26.2.1. Planejamento [#](#STANDBY-PLANNING)

É geralmente sábio criar os servidores primário e de espera de forma que sejam o mais semelhantes possível, pelo menos na perspectiva do servidor de banco de dados. Em particular, os nomes de caminho associados aos espaços de tabela serão passados sem modificação, então tanto os servidores primário quanto os de espera devem ter os mesmos caminhos de montagem para espaços de tabela, se essa característica for usada. Tenha em mente que, se [CREATE TABLESPACE](sql-createtablespace.md) for executado no primário, qualquer novo ponto de montagem necessário para ele deve ser criado no primário e em todos os servidores de espera antes de o comando ser executado. O hardware não precisa ser exatamente o mesmo, mas a experiência mostra que manter dois sistemas idênticos é mais fácil do que manter dois sistemas diferentes ao longo da vida do aplicativo e do sistema. Em qualquer caso, a arquitetura do hardware deve ser a mesma — mudar de, por exemplo, um sistema de 32 bits para um de 64 bits não funcionará.

De forma geral, o envio de logs entre servidores que executam diferentes níveis de versão principal do PostgreSQL não é possível. É a política do PostgreSQL Global Development Group não fazer alterações nos formatos de disco durante atualizações de versões menores, portanto, é provável que executar diferentes níveis de versão menor em servidores primários e de reserva funcione com sucesso. No entanto, não é oferecido suporte formal para isso e é aconselhável manter os servidores primários e de reserva no mesmo nível de versão o máximo possível. Ao atualizar para uma nova versão menor, a política mais segura é atualizar os servidores de reserva primeiro — uma nova versão menor é mais provável de ser capaz de ler arquivos WAL de uma versão menor anterior do que vice-versa.

### 26.2.2. Operação do servidor em espera [#](#STANDBY-SERVER-OPERATION)

Um servidor entra no modo de espera se um arquivo `standby.signal` existir no diretório de dados quando o servidor é iniciado.

No modo standby, o servidor aplica continuamente o WAL recebido do servidor principal. O servidor de standby pode ler o WAL de um arquivo WAL (consulte [restore_command](runtime-config-wal.md#GUC-RESTORE-COMMAND)) ou diretamente do principal através de uma conexão TCP (replicação em fluxo). O servidor de standby também tentará restaurar qualquer WAL encontrado no diretório `pg_wal` do cluster de standby. Isso geralmente acontece após o reinício do servidor, quando o standby retransmite novamente o WAL que foi transmitido do principal antes do reinício, mas você também pode copiar manualmente os arquivos para `pg_wal` a qualquer momento para que eles sejam retransmitidos.

Ao inicializar, o standby começa restaurando todos os WAL disponíveis na localização do arquivo, chamando `restore_command`. Uma vez que atinge o fim dos WAL disponíveis lá e `restore_command` falha, ele tenta restaurar qualquer WAL disponível no diretório `pg_wal`. Se isso falhar e a replicação em streaming tiver sido configurada, o standby tenta se conectar ao servidor primário e iniciar a transmissão de WAL a partir do último registro válido encontrado no arquivo ou `pg_wal`. Se isso falhar ou a replicação em streaming não for configurada, ou se a conexão for desconectada posteriormente, o standby volta ao passo 1 e tenta restaurar o arquivo do arquivo novamente. Esse ciclo de tentativas a partir do arquivo, `pg_wal`, e via replicação em streaming continua até que o servidor seja parado ou promovido.

O modo standby é encerrado e o servidor passa para o funcionamento normal quando o `pg_ctl promote` é executado ou o `pg_promote()` é chamado. Antes do failover, qualquer WAL imediatamente disponível no arquivo ou no `pg_wal` será restaurado, mas não há tentativa de se conectar ao primário.

### 26.2.3. Preparando o Primário para Servidores de Standby [#](#PREPARING-PRIMARY-FOR-STANDBY)

Configure a arquivamento contínuo no diretório primário para um diretório de arquivamento acessível a partir do standby, conforme descrito em [Seção 25.3](continuous-archiving.md)). O local de arquivamento deve ser acessível a partir do standby mesmo quando o primário estiver fora de operação, ou seja, deve residir no próprio servidor de standby ou em outro servidor confiável, e não no servidor primário.

Se você deseja usar a replicação de streaming, configure a autenticação no servidor primário para permitir conexões de replicação do(s) servidor(es) de espera; ou seja, crie um papel e forneça uma entrada ou entradas adequadas em `pg_hba.conf` com o campo de banco de dados definido como `replication`. Além disso, garanta que `max_wal_senders` esteja definido com um valor suficientemente grande no arquivo de configuração do servidor primário. Se slots de replicação serão usados, garanta que `max_replication_slots` esteja definido suficientemente alto também.

Faça um backup de base conforme descrito em [Seção 25.3.2](continuous-archiving.md#BACKUP-BASE-BACKUP) para inicializar o servidor de espera.

### 26.2.4. Configuração de um servidor de espera [#](#STANDBY-SERVER-SETUP)

Para configurar o servidor de espera, restaure o backup de base retirado do servidor primário (consulte [Seção 25.3.5](continuous-archiving.md#BACKUP-PITR-RECOVERY)). Crie um arquivo [[`standby.signal`](warm-standby.md#FILE-STANDBY-SIGNAL)] no diretório de dados do clúster do servidor de espera. Defina [restore_command](runtime-config-wal.md#GUC-RESTORE-COMMAND) com um comando simples para copiar arquivos do arquivo WAL. Se você planeja ter vários servidores de espera para fins de alta disponibilidade, certifique-se de que [[`recovery_target_timeline`][`latest`]] (o padrão) esteja definido, para que o servidor de espera siga a alteração do cronograma que ocorre durante a falha para outro servidor de espera.

### Nota

[comando de restauração](runtime-config-wal.md#GUC-RESTORE-COMMAND) deve retornar imediatamente se o arquivo não existir; o servidor tentará o comando novamente, se necessário.

Se você deseja usar a replicação de streaming, preencha [primary_conninfo](runtime-config-replication.md#GUC-PRIMARY-CONNINFO) com uma string de conexão libpq, incluindo o nome do host (ou endereço IP) e quaisquer detalhes adicionais necessários para se conectar ao servidor primário. Se o primário precisar de uma senha para autenticação, a senha também precisa ser especificada em [primary_conninfo](runtime-config-replication.md#GUC-PRIMARY-CONNINFO).

Se você está configurando o servidor de espera para fins de alta disponibilidade, configure a arquivamento WAL, conexões e autenticação como o servidor principal, porque o servidor de espera funcionará como um servidor principal após o failover.

Se você estiver usando um arquivo WAL, seu tamanho pode ser minimizado usando o parâmetro [archive_cleanup_command](runtime-config-wal.md#GUC-ARCHIVE-CLEANUP-COMMAND) para remover arquivos que não são mais necessários pelo servidor de espera. O utilitário pg_archivecleanup é projetado especificamente para ser usado com `archive_cleanup_command` em configurações típicas de um único servidor de espera, veja [pg_archivecleanup](pgarchivecleanup.md). No entanto, note que, se você estiver usando o arquivo para fins de backup, você precisa reter arquivos necessários para recuperar pelo menos o último backup de base, mesmo que eles não sejam mais necessários pelo standby.

Um exemplo simples de configuração é:

```
primary_conninfo = 'host=192.168.1.50 port=5432 user=foo password=foopass options=''-c wal_sender_timeout=5000'''
restore_command = 'cp /path/to/archive/%f %p'
archive_cleanup_command = 'pg_archivecleanup /path/to/archive %r'
```

Você pode ter qualquer número de servidores de espera, mas se você usar a replicação de streaming, certifique-se de que você configure `max_wal_senders` suficientemente alto no primário para permitir que eles sejam conectados simultaneamente.

### 26.2.5. Replicação de streaming [#](#STREAMING-REPLICATION)

A replicação em streaming permite que um servidor de espera permaneça mais atualizado do que é possível com o envio de registros de arquivo. O de espera se conecta ao primário, que transmite os registros WAL para o de espera à medida que são gerados, sem esperar que o arquivo WAL seja preenchido.

A replicação em fluxo é assíncrona por padrão (consulte [Seção 26.2.8](warm-standby.md#SYNCHRONOUS-REPLICATION)), nesse caso, há um pequeno atraso entre o commit de uma transação no primário e as mudanças se tornando visíveis no standby. Esse atraso, no entanto, é muito menor do que com o envio de logs baseado em arquivos, tipicamente inferior a um segundo, assumindo que o standby é poderoso o suficiente para acompanhar a carga. Com a replicação em fluxo, `archive_timeout` não é necessário para reduzir a janela de perda de dados.

Se você usar a replicação por streaming sem arquivamento contínuo baseado em arquivos, o servidor pode reciclar segmentos antigos do WAL antes que o standby os receba. Se isso ocorrer, o standby precisará ser reiniciado a partir de um novo backup de base. Você pode evitar isso configurando `wal_keep_size` para um valor grande o suficiente para garantir que os segmentos do WAL não sejam reciclados muito cedo, ou configurando um intervalo de replicação para o standby. Se você configurar um arquivo WAL acessível pelo standby, essas soluções não são necessárias, uma vez que o standby sempre pode usar o arquivo para recuperar o atraso, desde que retenha segmentos suficientes.

Para usar a replicação por streaming, configure um servidor de espera de envio de log baseado em arquivos conforme descrito em [Seção 26.2](warm-standby.md). O passo que transforma um servidor de espera de envio de log baseado em arquivos em um servidor de espera de replicação por streaming é definir a configuração `primary_conninfo` para apontar para o servidor primário. Defina [endereços de escuta](runtime-config-connection.md#GUC-LISTEN-ADDRESSES) e as opções de autenticação (consulte `pg_hba.conf`) no servidor primário para que o servidor de espera possa se conectar ao pseudo-banco de dados `replication` no servidor primário (consulte [Seção 26.2.5.1](warm-standby.md#STREAMING-REPLICATION-AUTHENTICATION)).

Em sistemas que suportam a opção de socket keepalive, definir [tcp_keepalives_idle](runtime-config-connection.md#GUC-TCP-KEEPALIVES-IDLE), [tcp_keepalives_interval](runtime-config-connection.md#GUC-TCP-KEEPALIVES-INTERVAL) e [tcp_keepalives_count](runtime-config-connection.md#GUC-TCP-KEEPALIVES-COUNT) ajuda o principal a notar prontamente uma conexão quebrada.

Defina o número máximo de conexões concorrentes dos servidores de espera (consulte [max_wal_senders](runtime-config-replication.md#GUC-MAX-WAL-SENDERS) para obter detalhes).

Quando o modo standby é iniciado e o `primary_conninfo` é configurado corretamente, o modo standby se conectará ao primário após refazer todos os arquivos WAL disponíveis no arquivo. Se a conexão for estabelecida com sucesso, você verá um `walreceiver` no modo standby e um processo correspondente `walsender` no primário.

#### 26.2.5.1. Autenticação [#](#STREAMING-REPLICATION-AUTHENTICATION)

É muito importante configurar os privilégios de acesso para replicação para que apenas usuários confiáveis possam ler o fluxo WAL, pois é fácil extrair informações privilegiadas dele. Os servidores de espera devem autenticar-se no primário como uma conta que tenha o privilégio `REPLICATION` ou um superusuário. Recomenda-se criar uma conta de usuário dedicada com os privilégios `REPLICATION` e `LOGIN` para replicação. Embora o privilégio `REPLICATION` ofereça permissões muito elevadas, ele não permite que o usuário modifique quaisquer dados no sistema primário, o que o privilégio `SUPERUSER` permite.

A autenticação do cliente para replicação é controlada por um registro `pg_hba.conf` que especifica `replication` no campo *`database`*. Por exemplo, se o standby estiver executando no IP do host `192.168.1.100` e o nome da conta para replicação é `foo`, o administrador pode adicionar a seguinte linha ao arquivo `pg_hba.conf` no primário:

```
# Allow the user "foo" from host 192.168.1.100 to connect to the primary
# as a replication standby if the user's password is correctly supplied.
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    replication     foo             192.168.1.100/32        scram-sha-256
```

O nome do host e o número do porto do nome do usuário de conexão primário e a senha são especificados no [primary_conninfo](runtime-config-replication.md#GUC-PRIMARY-CONNINFO). A senha também pode ser definida no arquivo `~/.pgpass` no modo standby (especifique `replication` no campo *`database`). Por exemplo, se o primário estiver executando no IP do host `192.168.1.50`, porta `5432`, o nome da conta para replicação é `foo`, e a senha é `foopass`, o administrador pode adicionar a seguinte linha no arquivo `postgresql.conf` no modo standby:

```
# The standby connects to the primary that is running on host 192.168.1.50
# and port 5432 as the user "foo" whose password is "foopass".
primary_conninfo = 'host=192.168.1.50 port=5432 user=foo password=foopass'
```

#### 26.2.5.2. Monitoramento [#](#STREAMING-REPLICATION-MONITORING)

Um importante indicador de saúde da replicação em streaming é a quantidade de registros WAL gerados no primário, mas ainda não aplicados no standby. Você pode calcular esse atraso comparando a localização atual de escrita do WAL no primário com a última localização do WAL recebida pelo standby. Esses locais podem ser recuperados usando `pg_current_wal_lsn` no primário e `pg_last_wal_receive_lsn` no standby, respectivamente (consulte [Tabela 9.97](functions-admin.md#FUNCTIONS-ADMIN-BACKUP-TABLE) e [Tabela 9.98](functions-admin.md#FUNCTIONS-RECOVERY-INFO-TABLE) para detalhes). A última localização de recebimento do WAL no standby também é exibida no status do processo do receptor do WAL, exibido usando o comando `ps` (consulte [Seção 27.1](monitoring-ps.md) para detalhes).

Você pode recuperar uma lista de processos de emissor WAL através da visualização `pg_stat_replication`(monitoring-stats.md#MONITORING-PG-STAT-REPLICATION-VIEW "27.2.4. pg_stat_replication"). Grandes diferenças entre `pg_current_wal_lsn` e o campo `sent_lsn` da visualização podem indicar que o servidor primário está com carga pesada, enquanto diferenças entre `sent_lsn` e `pg_last_wal_receive_lsn` no modo de espera podem indicar um atraso na rede, ou que o modo de espera está com carga pesada.

Em modo de espera quente, o status do processo de recepção do WAL pode ser recuperado através da visualização `pg_stat_wal_receiver` (monitoring-stats.md#MONITORING-PG-STAT-WAL-RECEIVER-VIEW "27.2.6. pg_stat_wal_receiver"). Uma grande diferença entre `pg_last_wal_replay_lsn` e o `flushed_lsn` da visualização indica que o WAL está sendo recebido mais rápido do que pode ser reinterpretado.

### 26.2.6. Fendas de replicação [#](#STREAMING-REPLICATION-SLOTS)

Os slots de replicação fornecem uma maneira automatizada de garantir que o servidor principal não remova segmentos WAL até que eles tenham sido recebidos por todos os backups, e que o principal não remova linhas que possam causar um [conflitos de recuperação](hot-standby.md#HOT-STANDBY-CONFLICT) mesmo quando o backup é desconectado.

Em vez de usar slots de replicação, é possível impedir a remoção de segmentos WAL antigos usando [wal_keep_size](runtime-config-replication.md#GUC-WAL-KEEP-SIZE), ou armazenando os segmentos em um arquivo usando [archive_command](runtime-config-wal.md#GUC-ARCHIVE-COMMAND) ou [archive_library](runtime-config-wal.md#GUC-ARCHIVE-LIBRARY). Uma desvantagem desses métodos é que eles geralmente resultam na retenção de mais segmentos WAL do que o necessário, enquanto os slots de replicação retêm apenas o número de segmentos que se sabe serem necessários.

Da mesma forma, [hot_standby_feedback](runtime-config-replication.md#GUC-HOT-STANDBY-FEEDBACK) por si só, sem também utilizar um slot de replicação, oferece proteção contra a remoção de linhas relevantes por vácuo, mas não oferece proteção durante qualquer período de tempo em que o standby não esteja conectado.

### Atenção

Cuidado: as faixas de replicação podem fazer com que o servidor retenha tantos segmentos WAL que eles preencham o espaço alocado para `pg_wal`. [max_slot_wal_keep_size](runtime-config-replication.md#GUC-MAX-SLOT-WAL-KEEP-SIZE) pode ser usado para limitar o tamanho dos arquivos WAL retidos pelas faixas de replicação.

#### 26.2.6.1. Consultar e manipular slots de replicação [#](#STREAMING-REPLICATION-SLOTS-MANIPULATION)

Cada slot de replicação tem um nome, que pode conter letras minúsculas, números e o caractere sublinhado.

Os slots de replicação existentes e seu estado podem ser vistos na visualização `pg_replication_slots`(view-pg-replication-slots.md "53.20. pg_replication_slots").

Os slots podem ser criados e removidos por meio do protocolo de replicação em streaming (consulte [Seção 54.4](protocol-replication.md)) ou por meio de funções SQL (consulte [Seção 9.28.6](functions-admin.md#FUNCTIONS-REPLICATION)).

#### 26.2.6.2. Exemplo de configuração [#](#STREAMING-REPLICATION-SLOTS-CONFIG)

Você pode criar um slot de replicação assim:

```
postgres=# SELECT * FROM pg_create_physical_replication_slot('node_a_slot');
  slot_name  | lsn
-------------+-----
 node_a_slot |

postgres=# SELECT slot_name, slot_type, active FROM pg_replication_slots;
  slot_name  | slot_type | active
-------------+-----------+--------
 node_a_slot | physical  | f
(1 row)
```

Para configurar o standby para usar este slot, o `primary_slot_name` deve ser configurado no standby. Aqui está um exemplo simples:

```
primary_conninfo = 'host=192.168.1.50 port=5432 user=foo password=foopass'
primary_slot_name = 'node_a_slot'
```

### 26.2.7. Replicação em cascata [#](#CASCADING-REPLICATION)

O recurso de replicação em cascata permite que um servidor de espera aceite conexões de replicação e transmita registros WAL para outros servidores de espera, atuando como um retransmissor. Isso pode ser usado para reduzir o número de conexões diretas ao primário e também para minimizar os custos de largura de banda entre sites.

Um standby que atua tanto como receptor quanto como emissor é conhecido como standby em cascata. Os standby que estão mais diretamente conectados ao primário são conhecidos como servidores upstream, enquanto os servidores standby mais distantes são servidores downstream. A replicação em cascata não coloca limites sobre o número ou disposição dos servidores downstream, embora cada standby se conecte apenas a um servidor upstream que, por sua vez, se conecta a um único servidor primário.

Um standby em cascata envia não apenas os registros WAL recebidos do primário, mas também aqueles restaurados do arquivo. Portanto, mesmo que a conexão de replicação em alguma conexão upstream seja encerrada, a replicação em fluxo continua no sentido descendente, desde que novos registros WAL estejam disponíveis.

A replicação em cascata atualmente é assíncrona. As configurações de replicação síncrona (consulte [Seção 26.2.8](warm-standby.md#SYNCHRONOUS-REPLICATION)) não têm efeito na replicação em cascata no momento.

O feedback de standby quente se propaga em direção ao upstream, independentemente da disposição em cascata.

Se um servidor de espera upstream for promovido para se tornar o novo primário, os servidores downstream continuarão a transmitir dados do novo primário se `recovery_target_timeline` estiver definido como `'latest'` (o padrão).

Para usar a replicação em cascata, configure o standby em cascata de modo que ele possa aceitar conexões de replicação (ou seja, defina [max_wal_senders](runtime-config-replication.md#GUC-MAX-WAL-SENDERS) e [hot_standby](runtime-config-replication.md#GUC-HOT-STANDBY), e configure [autenticação baseada em host](auth-pg-hba-conf.md)). Você também precisará definir [[`primary_conninfo`] no standby downstream para apontar para o standby em cascata.

### 26.2.8. Replicação Síncrona [#](#SYNCHRONOUS-REPLICATION)

A replicação em streaming do PostgreSQL é assíncrona por padrão. Se o servidor primário falhar, algumas transações que foram comprometidas podem não ter sido replicadas para o servidor de espera, causando perda de dados. A quantidade de perda de dados é proporcional ao atraso de replicação no momento do failover.

A replicação síncrona oferece a capacidade de confirmar que todas as alterações feitas por uma transação foram transferidas para um ou mais servidores de espera síncronos. Isso estende o nível padrão de durabilidade oferecido por um compromisso de transação. Esse nível de proteção é referido como replicação 2-segura na teoria da informática, e grupo-1-segura (grupo-segura e 1-segura) quando `synchronous_commit` está definido como `remote_write`.

Ao solicitar replicação síncrona, cada commit de uma transação de escrita irá esperar até receber a confirmação de que o commit foi escrito no log de antecipação no disco de ambos os servidores primário e de reserva. A única possibilidade de perda de dados é se ambos, o primário e o de reserva, sofrerem falhas ao mesmo tempo. Isso pode proporcionar um nível muito maior de durabilidade, embora apenas se o sysadmin for cauteloso quanto à colocação e gestão dos dois servidores. A espera pela confirmação aumenta a confiança do usuário de que as alterações não serão perdidas em caso de falhas dos servidores, mas também aumenta necessariamente o tempo de resposta para a transação solicitante. O tempo mínimo de espera é o tempo de ida e volta entre o primário e o de reserva.

As transações somente de leitura e os recuos de transações não precisam esperar respostas dos servidores de espera. Os compromissos de subtransação não esperam respostas dos servidores de espera, apenas os compromissos de nível superior. Ações de longa duração, como o carregamento de dados ou a construção de índices, não esperam até a mensagem de commit final. Todas as ações de compromisso de duas fases exigem espera de commit, incluindo tanto o preparo quanto o commit.

Um standby síncrono pode ser um standby de replicação física ou um assinante de replicação lógica. Também pode ser qualquer outro consumidor de fluxo de replicação WAL físico ou lógico, que saiba enviar as mensagens de feedback apropriadas. Além dos sistemas de replicação física e lógica integrados, isso inclui programas especiais como `pg_receivewal` e `pg_recvlogical`, bem como alguns sistemas de replicação de terceiros e programas personalizados. Verifique a documentação respectiva para obter detalhes sobre o suporte à replicação síncrona.

#### 26.2.8.1. Configuração Básica [#](#SYNCHRONOUS-REPLICATION-CONFIG)

Uma vez que a replicação em streaming tenha sido configurada, a configuração da replicação síncrona requer apenas um passo adicional de configuração: o [synchronous_standby_names](runtime-config-replication.md#GUC-SYNCHRONOUS-STANDBY-NAMES) deve ser definido com um valor não vazio. O `synchronous_commit` também deve ser definido como `on`, mas, como este é o valor padrão, normalmente não é necessário fazer nenhuma alteração. (Consulte [Seção 19.5.1](runtime-config-wal.md#RUNTIME-CONFIG-WAL-SETTINGS) e [Seção 19.6.2](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-PRIMARY).). Esta configuração fará com que cada commit espere a confirmação de que o standby escreveu o registro do commit no armazenamento durável. O `synchronous_commit` pode ser definido por usuários individuais, portanto, pode ser configurado no arquivo de configuração, para usuários ou bancos de dados específicos, ou dinamicamente por aplicativos, a fim de controlar a garantia de durabilidade em uma base por transação.

Após um registro de commit ter sido escrito em disco no primário, o registro WAL é então enviado para o standby. O standby envia mensagens de resposta toda vez que um novo lote de dados WAL é escrito em disco, a menos que `wal_receiver_status_interval` seja definido como zero no standby. No caso em que `synchronous_commit` é definido como `remote_apply`, o standby envia mensagens de resposta quando o registro de commit é reinterpretado, tornando a transação visível. Se o standby for escolhido como um standby síncrono, de acordo com a configuração de `synchronous_standby_names` no primário, as mensagens de resposta desse standby serão consideradas juntamente com as de outros standbys síncronos para decidir quando liberar as transações que aguardam confirmação de que o registro de commit foi recebido. Esses parâmetros permitem que o administrador especifique quais servidores de standby devem ser standbys síncronos. Note que a configuração da replicação síncrona é principalmente no primário. Os standbys nomeados devem estar diretamente conectados ao primário; o primário não sabe nada sobre os servidores de standby de baixo nível que usam replicação em cascata.

Definir `synchronous_commit` para `remote_write` fará com que cada commit espere a confirmação de que o standby recebeu o registro do commit e o escreveu em seu próprio sistema operacional, mas não para que os dados sejam descarregados no disco do standby. Esta definição oferece uma garantia de durabilidade mais fraca do que a `on`: o standby pode perder os dados no caso de um crash do sistema operacional, embora não de um crash do PostgreSQL. No entanto, é um ajuste útil na prática, pois pode diminuir o tempo de resposta da transação. A perda de dados só pode ocorrer se o primário e o standby falharem e o banco de dados do primário também se corromperem ao mesmo tempo.

Definir `synchronous_commit` para `remote_apply` fará com que cada commit espere até que os backups síncronos atuais relatem que eles replicaram a transação, tornando-a visível para consultas do usuário. Em casos simples, isso permite o balanceamento de carga com consistência causal.

Os usuários deixarão de esperar se uma parada rápida for solicitada. No entanto, como no caso da replicação assíncrona, o servidor não será totalmente desligado até que todos os registros WAL pendentes sejam transferidos para os servidores de espera atualmente conectados.

#### 26.2.8.2. Múltiplos standby síncronos [#](#SYNCHRONOUS-REPLICATION-MULTIPLE-STANDBYS)

A replicação síncrona suporta um ou mais servidores de espera síncronos; as transações aguardam até que todos os servidores de espera que são considerados síncronos confirmem a recepção dos seus dados. O número de standby síncronos para os quais as transações devem aguardar respostas é especificado em `synchronous_standby_names`. Este parâmetro também especifica uma lista de nomes de standby e o método (`FIRST` e `ANY`) para escolher standby síncronos dentre os listados.

O método `FIRST` especifica uma replicação síncrona baseada em prioridade e faz com que os compromissos de transação esperem até que seus registros WAL sejam replicados para o número solicitado de standby síncronos escolhidos com base em suas prioridades. Os standby cujo nome aparece mais cedo na lista têm prioridade mais alta e serão considerados síncronos. Outros servidores standby que aparecem mais tarde nesta lista representam standby síncronos potenciais. Se qualquer um dos standby síncronos atuais se desconectar por qualquer motivo, ele será imediatamente substituído pelo próximo standby de maior prioridade.

Um exemplo de `synchronous_standby_names` para múltiplos standby síncronos com base em prioridade é:

```
synchronous_standby_names = 'FIRST 2 (s1, s2, s3)'
```

Neste exemplo, se quatro servidores de espera `s1`, `s2`, `s3` e `s4` estiverem em execução, os dois servidores de espera `s1` e `s2` serão escolhidos como servidores síncronos porque seus nomes aparecem no início da lista de nomes de espera. `s3` é um servidor potencial síncrono e assumirá o papel de servidor síncrono quando qualquer um dos servidores `s1` ou `s2` falhar. `s4` é um servidor assíncrono, pois seu nome não está na lista.

O método `ANY` especifica uma replicação sincronizada baseada em quórum e faz com que os compromissos de transação esperem até que seus registros WAL sejam replicados para *pelo menos* o número solicitado de backups síncronos na lista.

Um exemplo de `synchronous_standby_names` para múltiplos standby síncronos baseados em quórum é:

```
synchronous_standby_names = 'ANY 2 (s1, s2, s3)'
```

Neste exemplo, se quatro servidores de espera `s1`, `s2`, `s3` e `s4` estiverem em execução, os compromissos de transação aguardam respostas de pelo menos dois servidores de espera de `s1`, `s2` e `s3`. `s4` é um standby assíncrono, uma vez que seu nome não está na lista.

Os estados síncronos dos servidores em espera podem ser visualizados usando a visualização `pg_stat_replication`.

#### 26.2.8.3. Planejamento para Desempenho [#](#SYNCHRONOUS-REPLICATION-PERFORMANCE)

A replicação síncrona geralmente exige servidores de espera cuidadosamente planejados e colocados para garantir que os aplicativos sejam executados de forma aceitável. A espera não utiliza recursos do sistema, mas as bloqueadoras de transação continuam sendo mantidas até que a transferência seja confirmada. Como resultado, o uso imprudente da replicação síncrona reduzirá o desempenho dos aplicativos de banco de dados devido ao aumento dos tempos de resposta e à maior concorrência.

O PostgreSQL permite que o desenvolvedor da aplicação especifique o nível de durabilidade necessário por meio da replicação. Isso pode ser especificado para o sistema como um todo, embora também possa ser especificado para usuários ou conexões específicas, ou até mesmo para transações individuais.

Por exemplo, uma carga de trabalho de aplicativos pode consistir em: 10% das alterações são detalhes importantes do cliente, enquanto 90% das alterações são dados menos importantes que a empresa pode mais facilmente sobreviver se forem perdidos, como mensagens de bate-papo entre usuários.

Com opções de replicação síncrona especificadas no nível do aplicativo (no primário), podemos oferecer replicação síncrona para as mudanças mais importantes, sem desacelerar a maior parte da carga de trabalho total. As opções no nível do aplicativo são uma ferramenta importante e prática para permitir os benefícios da replicação síncrona para aplicativos de alto desempenho.

Você deve considerar que a largura de banda da rede deve ser maior que a taxa de geração de dados WAL.

#### 26.2.8.4. Planejamento para alta disponibilidade [#](#SYNCHRONOUS-REPLICATION-HA)

`synchronous_standby_names` especifica o número e os nomes dos standby síncronos que os compromissos de transação feitos quando `synchronous_commit` está definido para `on`, `remote_apply` ou `remote_write` aguardará respostas de. Esses compromissos de transação podem nunca ser concluídos se qualquer um dos standby síncronos falhar.

A melhor solução para alta disponibilidade é garantir que você mantenha o maior número possível de standby síncronos conforme solicitado. Isso pode ser alcançado ao nomear vários standby síncronos potenciais usando `synchronous_standby_names`.

Em uma replicação síncrona baseada em prioridade, os standbys cujos nomes aparecem mais cedo na lista serão usados como standbys síncronos. Os standbys listados após esses serão responsáveis pelo papel de stand-by síncrono se um dos atuais falhar.

Em uma replicação síncrona baseada em quórum, todos os standbys que aparecem na lista serão usados como candidatos para standbys síncronos. Mesmo que um deles falhe, os outros standbys continuarão desempenhando o papel de candidatos de standby síncrono.

Quando um standby se conecta pela primeira vez ao primário, ele ainda não estará corretamente sincronizado. Isso é descrito como o modo `catchup`. Uma vez que o atraso entre o standby e o primário atinja zero pela primeira vez, passamos para o estado de tempo real [[`streaming`]. A duração do término pode ser longa imediatamente após o standby ter sido criado. Se o standby for desligado, o período de término aumentará de acordo com o tempo que o standby esteve fora de operação. O standby só poderá se tornar um standby sincronizado quando atingir o estado [[`streaming`]. Esse estado pode ser visualizado usando a vista [[`pg_stat_replication`].

Se o primário reiniciar enquanto as transações estão aguardando confirmação, essas transações em espera serão marcadas como totalmente confirmadas assim que o banco de dados primário se recuperar. Não há como ter certeza de que todas as standby receberam todos os dados WAL no momento do crash do primário. Algumas transações podem não ser mostradas como confirmadas na standby, embora sejam confirmadas no primário. A garantia que oferecemos é que o aplicativo não receberá confirmação explícita do sucesso do commit de uma transação até que os dados WAL sejam conhecidos como sendo recebidos com segurança por todas as standby síncronas.

Se você realmente não pode manter tantos standby síncronos conforme solicitado, deve diminuir o número de standby síncronos para os quais as transações devem esperar respostas em `synchronous_standby_names` (ou desativá-lo) e recarregar o arquivo de configuração no servidor primário.

Se o primário for isolado dos servidores de espera restantes, você deve realizar uma transição para o melhor candidato desses outros servidores de espera restantes.

Se você precisar recriar um servidor de espera enquanto as transações estão aguardando, certifique-se de que as funções `pg_backup_start()` e `pg_backup_stop()` sejam executadas em uma sessão com `synchronous_commit` = `off`, caso contrário, esses pedidos aguardam para sempre a aparição do standby.

### 26.2.9. Arquivamento contínuo em standby [#](#CONTINUOUS-ARCHIVING-IN-STANDBY)

Quando o arquivamento WAL contínuo é usado em um estado de espera, existem dois cenários diferentes: o arquivo WAL pode ser compartilhado entre o principal e o de espera, ou o de espera pode ter seu próprio arquivo WAL. Quando o de espera tem seu próprio arquivo WAL, defina `archive_mode` para `always`, e o de espera chamará o comando de arquivo para cada segmento WAL que receber, seja restaurando do arquivo ou por streaming de replicação. O arquivo compartilhado pode ser tratado de maneira semelhante, mas o `archive_command` ou `archive_library` deve testar se o arquivo que está sendo arquivado já existe e se o arquivo existente tem conteúdos idênticos. Isso requer mais cuidado no `archive_command` ou `archive_library`, pois deve ser cuidadoso para não sobrescrever um arquivo existente com conteúdos diferentes, mas retornar sucesso se o arquivo exatamente igual for arquivado duas vezes. E tudo isso deve ser feito sem condições de corrida, se dois servidores tentarem arquivar o mesmo arquivo ao mesmo tempo.

Se `archive_mode` estiver definido como `on`, o arquivador não será ativado durante o modo de recuperação ou standby. Se o servidor de standby for promovido, ele começará a arquivar após a promoção, mas não arquivará quaisquer arquivos de histórico WAL ou cronograma que ele não tenha gerado ele mesmo. Para obter uma série completa de arquivos WAL no arquivo, você deve garantir que todo o WAL seja arquivado, antes de ele atingir o standby. Isso é inerentemente verdadeiro com o envio de logs baseado em arquivos, pois o standby só pode restaurar arquivos que são encontrados no arquivo, mas não se a replicação por streaming estiver habilitada. Quando um servidor não está no modo de recuperação, não há diferença entre os modos `on` e `always`.