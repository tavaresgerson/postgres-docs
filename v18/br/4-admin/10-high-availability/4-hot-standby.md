## 26.4. Standby quente [#](#HOT-STANDBY)

* [26.4.1. Visão Geral do Usuário](hot-standby.md#HOT-STANDBY-USERS)
* [26.4.2. Tratamento de Conflitos de Consulta](hot-standby.md#HOT-STANDBY-CONFLICT)
* [26.4.3. Visão Geral do Administrador](hot-standby.md#HOT-STANDBY-ADMIN)
* [26.4.4. Referência do Parâmetro de Standby Quente](hot-standby.md#HOT-STANDBY-PARAMETERS)
* [26.4.5. Observações](hot-standby.md#HOT-STANDBY-CAVEATS)

O modo standby quente é o termo usado para descrever a capacidade de se conectar ao servidor e executar consultas somente de leitura enquanto o servidor estiver em modo de recuperação de arquivo ou modo standby. Isso é útil tanto para fins de replicação quanto para restaurar um backup a um estado desejado com grande precisão. O termo modo standby quente também se refere à capacidade do servidor de passar da recuperação para o funcionamento normal, enquanto os usuários continuam executando consultas e/ou mantendo suas conexões abertas.

Executar consultas no modo de espera quente é semelhante à operação normal de consulta, embora haja várias diferenças de uso e administrativas explicadas abaixo.

### 26.4.1. Visão geral do usuário [#](#HOT-STANDBY-USERS)

Quando o parâmetro [hot_standby](runtime-config-replication.md#GUC-HOT-STANDBY) é definido como verdadeiro em um servidor em espera, ele começará a aceitar conexões assim que a recuperação tiver levado o sistema a um estado consistente e estiver pronto para o modo de espera quente. Todas essas conexões são estritamente apenas de leitura; nem sequer tabelas temporárias podem ser escritas.

Os dados no modo standby demoram algum tempo para chegar do servidor principal, portanto, haverá um atraso mensurável entre o principal e o standby. Portanto, executar a mesma consulta quase simultaneamente no principal e no standby pode retornar resultados diferentes. Dizemos que os dados no modo standby são *eventualmente consistentes* com o principal. Uma vez que o registro de compromisso de uma transação seja reinterpretado no standby, as alterações feitas por essa transação serão visíveis em quaisquer novos instantâneos tomados no standby. Instantâneos podem ser tomados no início de cada consulta ou no início de cada transação, dependendo do nível atual de isolamento de transação. Para mais detalhes, consulte [Seção 13.2](transaction-iso.md).

As transações iniciadas durante o modo standby quente podem emitir os seguintes comandos:

* Acesso a consulta: `SELECT`, `COPY TO`
* Comandos de cursor: `DECLARE`, `FETCH`, `CLOSE`
* Configurações: `SHOW`, `SET`, `RESET`
* Comandos de gerenciamento de transações:

+ `BEGIN`, `END`, `ABORT`, `START TRANSACTION`
  + `SAVEPOINT`, `RELEASE`, `ROLLBACK TO SAVEPOINT`
  + `EXCEPTION` blocos e outras subtransações internas
* `LOCK TABLE`, embora apenas quando explicitamente em um desses modos: `ACCESS SHARE`, `ROW SHARE` ou `ROW EXCLUSIVE`.
* Planos e recursos: `PREPARE`, `EXECUTE`, `DEALLOCATE`, `DISCARD`
* Plugins e extensões: `LOAD`
* `UNLISTEN`

As transações iniciadas durante o modo standby quente nunca receberão um ID de transação e não poderão gravar no log de pré-escrita do sistema. Portanto, as seguintes ações produzirão mensagens de erro:

* Linguagem de Manipulação de Dados (DML): `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `COPY FROM`, `TRUNCATE`. Observe que não há ações permitidas que resultem na execução de um gatilho durante a recuperação. Esta restrição se aplica mesmo a tabelas temporárias, porque as linhas de tabela não podem ser lidas ou escritas sem atribuir um ID de transação, o que atualmente não é possível em um ambiente de standby quente.
* Linguagem de Definição de Dados (DDL): `CREATE`, `DROP`, `ALTER`, `COMMENT`. Esta restrição se aplica mesmo a tabelas temporárias, porque realizar essas operações exigiria a atualização das tabelas de catálogo do sistema.
* `SELECT ... FOR SHARE | UPDATE`, porque os bloqueios de linha não podem ser tomados sem atualizar os arquivos de dados subjacentes.
* Regras sobre as declarações `SELECT` que geram comandos DML.
* `LOCK` que explicitamente solicita um modo superior a `ROW EXCLUSIVE MODE`.
* `LOCK` na forma padrão curta, uma vez que solicita `ACCESS EXCLUSIVE MODE`.
* Comandos de gerenciamento de transação que explicitamente definem estado não somente leitura:

+ `BEGIN READ WRITE`, `START TRANSACTION READ WRITE`
  + `SET TRANSACTION READ WRITE`, `SET SESSION CHARACTERISTICS AS TRANSACTION READ WRITE`
  + `SET transaction_read_only = off`
* Comandos de commit de duas fases: `PREPARE TRANSACTION`, `COMMIT PREPARED`, `ROLLBACK PREPARED` porque até mesmo transações apenas de leitura precisam escrever WAL na fase de preparação (a primeira fase do commit de duas fases).
* Atualizações sequenciais: `nextval()`, `setval()`
* `LISTEN`, `NOTIFY`

Em operação normal, as transações de leitura somente são permitidas para usar `LISTEN` e `NOTIFY`, portanto, as sessões de standby quente operam sob restrições ligeiramente mais rígidas do que as sessões de leitura somente comuns. É possível que algumas dessas restrições possam ser relaxadas em uma versão futura.

Durante o modo de espera quente, o parâmetro `transaction_read_only` é sempre verdadeiro e não pode ser alterado. Mas, desde que não haja tentativa de modificar o banco de dados, as conexões durante o modo de espera quente funcionarão de maneira muito semelhante a qualquer outra conexão de banco de dados. Se ocorrer falha de passagem ou mudança de modo, o banco de dados passará para o modo de processamento normal. As sessões permanecerão conectadas enquanto o servidor muda de modo. Após o término do modo de espera quente, será possível iniciar transações de leitura e escrita (mesmo a partir de uma sessão iniciada durante o modo de espera quente).

Os usuários podem determinar se o standby quente está atualmente ativo para sua sessão emitindo `SHOW in_hot_standby`. (Em versões do servidor antes da 14, o parâmetro `in_hot_standby` não existia; um método substituto funcional para servidores mais antigos é `SHOW transaction_read_only`. Além disso, um conjunto de funções ([Tabela 9.98](functions-admin.md#FUNCTIONS-RECOVERY-INFO-TABLE)) permite que os usuários acessem informações sobre o servidor de standby. Essas permitem que você escreva programas que estejam cientes do estado atual do banco de dados. Essas podem ser usadas para monitorar o progresso da recuperação ou para permitir que você escreva programas complexos que restauram o banco de dados a estados específicos.

### 26.4.2. Gerenciamento de conflitos de consulta [#](#HOT-STANDBY-CONFLICT)

Os servidores primário e de reserva estão, de muitas maneiras, de forma solta conectados. As ações no servidor primário terão um efeito no servidor de reserva. Como resultado, há potencial para interações ou conflitos negativos entre eles. O conflito mais fácil de entender é o desempenho: se uma grande carga de dados estiver ocorrendo no servidor primário, isso gerará um fluxo semelhante de registros WAL no servidor de reserva, então as consultas do standby podem competir por recursos do sistema, como I/O.

Existem também tipos adicionais de conflitos que podem ocorrer com o standby quente. Esses conflitos são *conflitos difíceis* no sentido de que as consultas podem precisar ser canceladas e, em alguns casos, as sessões desconectadas para resolvê-los. O usuário é fornecido com várias maneiras de lidar com esses conflitos. Os casos de conflito incluem:

* Acesso a bloqueios exclusivos obtidos no servidor principal, incluindo tanto comandos explícitos do `LOCK` quanto várias ações DDL, conflitam com acessos a tabelas em consultas de espera.
* A eliminação de um espaço de tabela no principal conflitam com consultas de espera que utilizam esse espaço de tabela para arquivos de trabalho temporários.
* A eliminação de um banco de dados no principal conflitam com sessões conectadas a esse banco de dados na espera.
* A aplicação de um registro de limpeza de vácuo do WAL conflitam com transações de espera cujos instantâneos ainda podem "ver" qualquer uma das linhas a serem removidas.
* A aplicação de um registro de limpeza de vácuo do WAL conflitam com consultas que acessam a página de destino no standby, independentemente de os dados a serem removidos serem visíveis ou

No servidor primário, esses casos resultam simplesmente em espera; e o usuário pode optar por cancelar qualquer uma das ações conflitantes. No entanto, no modo standby, não há escolha: a ação registrada no WAL já ocorreu no primário, então o standby não deve falhar em aplicá-la. Além disso, permitir que o aplicativo WAL espere indefinidamente pode ser muito indesejável, porque o estado do standby ficará cada vez mais atrasado em relação ao do primário. Portanto, é fornecido um mecanismo para cancelar forçosamente as consultas do standby que estejam em conflito com os registros WAL que devem ser aplicados.

Um exemplo da situação problemática é um administrador no servidor primário executando `DROP TABLE` em uma tabela que está atualmente sendo consultada no servidor de espera. Claramente, a consulta de espera não pode continuar se o `DROP TABLE` for aplicado na espera. Se essa situação ocorrer no primário, o `DROP TABLE` aguardará até que a outra consulta tenha terminado. Mas quando o `DROP TABLE` é executado no primário, o primário não tem informações sobre quais consultas estão sendo executadas na espera, então ele não aguardará por quaisquer consultas de espera desse tipo. Os registros de alteração do WAL chegam ao servidor de espera enquanto a consulta de espera ainda está em execução, causando um conflito. O servidor de espera deve adiar a aplicação dos registros do WAL (e também de tudo o que vem depois) ou, caso contrário, cancelar a consulta conflitante para que o `DROP TABLE` possa ser aplicado.

Quando uma consulta conflitante é curta, é geralmente desejável permitir que ela seja concluída, adiando a aplicação do WAL por um pouco de tempo; mas um longo atraso na aplicação do WAL geralmente não é desejável. Portanto, o mecanismo de cancelamento tem parâmetros, [max_standby_archive_delay](runtime-config-replication.md#GUC-MAX-STANDBY-ARCHIVE-DELAY) e [max_standby_streaming_delay](runtime-config-replication.md#GUC-MAX-STANDBY-STREAMING-DELAY), que definem o atraso máximo permitido na aplicação do WAL. As consultas conflitantes serão canceladas assim que tiverem levado mais tempo do que o ajuste relevante para aplicar qualquer dados WAL recém-recebidos. Existem dois parâmetros para que diferentes valores de atraso possam ser especificados para o caso de leitura de dados WAL de um arquivo (ou seja, recuperação inicial a partir de um backup de base ou “acabar com” um servidor de standby que ficou muito para trás) em comparação com a leitura de dados WAL via replicação em streaming.

Em um servidor de espera que existe principalmente para alta disponibilidade, é melhor definir os parâmetros de atraso relativamente curtos, para que o servidor não possa ficar muito atrás do principal devido a atrasos causados por consultas de espera. No entanto, se o servidor de espera for destinado a executar consultas de longa duração, então um valor de atraso alto ou até infinito pode ser preferível. Tenha em mente, no entanto, que uma consulta de longa duração pode fazer com que outras sessões no servidor de espera não vejam mudanças recentes no principal, se atrasar a aplicação dos registros WAL.

Uma vez que o atraso especificado por `max_standby_archive_delay` ou `max_standby_streaming_delay` tenha sido excedido, as consultas conflitantes serão canceladas. Isso geralmente resulta apenas em um erro de cancelamento, embora, no caso de repetir um `DROP DATABASE`, a sessão conflitante inteira seja encerrada. Além disso, se o conflito for sobre um bloqueio mantido por uma transação inativa, a sessão conflitante é encerrada (este comportamento pode mudar no futuro).

As consultas canceladas podem ser repetidas imediatamente (claro, após iniciar uma nova transação). Como o cancelamento de consulta depende da natureza dos registros WAL que estão sendo reinterpretados, uma consulta que foi cancelada pode bem ter sucesso se for executada novamente.

Tenha em mente que os parâmetros de atraso são comparados ao tempo decorrido desde que os dados WAL foram recebidos pelo servidor de espera. Assim, o período de indulgência permitido a qualquer consulta na espera nunca é maior que o parâmetro de atraso, e pode ser consideravelmente menor se a espera já estiver atrasada como resultado da espera por consultas anteriores serem concluídas, ou como resultado de não conseguir acompanhar uma carga de atualização pesada.

A razão mais comum para o conflito entre consultas de espera e o replay do WAL é a "limpeza precoce". Normalmente, o PostgreSQL permite a limpeza de versões antigas de linhas quando não há transações que precisem vê-las para garantir a visibilidade correta dos dados de acordo com as regras MVCC. No entanto, essa regra só pode ser aplicada para transações que executam no primário. Portanto, é possível que a limpeza no primário remova versões de linha que ainda são visíveis para uma transação na espera.

A limpeza da versão de linha não é a única causa potencial de conflitos com consultas de espera. Todos os varreduras apenas de índice (incluindo aquelas que são executadas em standby) devem usar um instantâneo MVCC que “agrede” com o mapa de visibilidade. Portanto, conflitos são necessários sempre que `VACUUM` [define uma página como totalmente visível no mapa de visibilidade](routine-vacuuming.md#VACUUM-FOR-VISIBILITY-MAP "24.1.4. Updating the Visibility Map") que contenha uma ou mais linhas *não* visíveis para todas as consultas de espera. Portanto, mesmo executando `VACUUM` contra uma tabela sem linhas atualizadas ou excluídas que exijam limpeza pode levar a conflitos.

Os usuários devem estar cientes de que tabelas que são regularmente e fortemente atualizadas no servidor principal rapidamente causarão a cancelamento de consultas de longa duração no standby. Nesses casos, a definição de um valor finito para `max_standby_archive_delay` ou `max_standby_streaming_delay` pode ser considerada semelhante à definição de `statement_timeout`.

Existem possibilidades de correção se o número de cancelamentos de consultas de espera for considerado inaceitável. A primeira opção é definir o parâmetro `hot_standby_feedback`, que impede que `VACUUM` remova linhas recentemente mortas, e assim os conflitos de limpeza não ocorram. Se você fizer isso, deve notar que isso atrasará a limpeza das linhas mortas no primário, o que pode resultar em um bloat indesejável da tabela. No entanto, a situação de limpeza não será pior do que se as consultas de espera estivessem executando diretamente no servidor primário, e você ainda estará obtendo o benefício de transferir a execução para o standby. Se os servidores de standby se conectarem e desconectarem frequentemente, você pode querer fazer ajustes para lidar com o período em que o feedback `hot_standby_feedback` não está sendo fornecido. Por exemplo, considere aumentar `max_standby_archive_delay` para que as consultas não sejam rapidamente canceladas por conflitos em arquivos de arquivo WAL durante períodos desconectados. Você também deve considerar aumentar `max_standby_streaming_delay` para evitar cancelamentos rápidos por entradas de WAL de streaming recém-chegadas após a reconexão.

O número de cancelamentos de consultas e o motivo deles podem ser visualizados usando a visualização do sistema `pg_stat_database_conflicts` no servidor de espera. A visualização do sistema `pg_stat_database` também contém informações resumidas.

Os usuários podem controlar se uma mensagem de registro é produzida quando o WAL espera mais do que `deadlock_timeout` por conflitos. Isso é controlado pelo parâmetro [log_recovery_conflict_waits](runtime-config-logging.md#GUC-LOG-RECOVERY-CONFLICT-WAITS).

### 26.4.3. Visão Geral do Administrador [#](#HOT-STANDBY-ADMIN)

Se `hot_standby` for `on` em `postgresql.conf` (o valor padrão) e houver um arquivo [`standby.signal`](warm-standby.md#FILE-STANDBY-SIGNAL) presente, o servidor funcionará no modo standby quente. No entanto, pode levar algum tempo para as conexões de standby quente serem permitidas, porque o servidor não aceitará conexões até que tenha completado uma recuperação suficiente para fornecer um estado consistente contra o qual as consultas possam ser executadas. Durante esse período, os clientes que tentam se conectar serão recusados com uma mensagem de erro. Para confirmar que o servidor foi ativado, tente conectar-se ao aplicativo ou procure essas mensagens nos logs do servidor:

```
LOG:  entering standby mode

... then some time later ...

LOG:  consistent recovery state reached
LOG:  database system is ready to accept read-only connections
```

As informações de consistência são registradas uma vez por ponto de verificação no primário. Não é possível habilitar o modo standby quente ao ler o WAL escrito durante um período em que `wal_level` não estava definido como `replica` ou `logical` no primário. Mesmo após alcançar um estado consistente, o instantâneo de recuperação pode não estar pronto para o modo standby quente se ambas as seguintes condições forem atendidas, atrasando a aceitação de conexões somente de leitura. Para habilitar o modo standby quente, transações de escrita de longa duração com mais de 64 subtransações precisam ser fechadas no primário.

* Uma transação de escrita tem mais de 64 subtransações
* Transações de escrita muito de longa duração

Se você estiver executando o envio de logs baseado em arquivos (modo "standby quente"), talvez precise esperar até que o próximo arquivo WAL chegue, o que pode demorar tanto quanto o ajuste `archive_timeout` no primário.

Os parâmetros de configuração determinam o tamanho da memória compartilhada para o rastreamento de IDs de transação, bloqueios e transações preparadas. Essas estruturas de memória compartilhada não devem ser menores no modo standby do que no modo primário, a fim de garantir que o modo standby não se esgote de memória compartilhada durante a recuperação. Por exemplo, se o primário tivesse usado uma transação preparada, mas o modo standby não tivesse alocado nenhuma memória compartilhada para o rastreamento de transações preparadas, então a recuperação não poderia continuar até que a configuração do modo standby fosse alterada. Os parâmetros afetados são:

* `max_connections`
* `max_prepared_transactions`
* `max_locks_per_transaction`
* `max_wal_senders`
* `max_worker_processes`

A maneira mais fácil de garantir que isso não se torne um problema é ter esses parâmetros definidos nos servidores de reserva com valores iguais ou maiores que os do servidor primário. Portanto, se você deseja aumentar esses valores, deve fazê-lo primeiro em todos os servidores de reserva, antes de aplicar as alterações no servidor primário. Por outro lado, se você deseja diminuir esses valores, deve fazê-lo primeiro no servidor primário, antes de aplicar as alterações em todos os servidores de reserva. Tenha em mente que, quando um servidor de reserva é promovido, ele se torna a nova referência para as configurações dos parâmetros necessários para os servidores de reserva que o seguem. Portanto, para evitar que isso se torne um problema durante uma transição ou falha, é recomendável manter esses ajustes iguais em todos os servidores de reserva.

O WAL acompanha as alterações nesses parâmetros no primário. Se um standby quente processar o WAL e indicar que o valor atual no primário é maior que o seu próprio valor, ele registrará um aviso e pausar a recuperação, por exemplo:

```
WARNING:  hot standby is not possible because of insufficient parameter settings
DETAIL:  max_connections = 80 is a lower setting than on the primary server, where its value was 100.
LOG:  recovery has paused
DETAIL:  If recovery is unpaused, the server will shut down.
HINT:  You can then restart the server after making the necessary configuration changes.
```

Nesse ponto, os parâmetros do modo standby precisam ser atualizados e a instância precisa ser reiniciada antes que a recuperação possa continuar. Se o modo standby não for um modo standby quente, ele será desligado imediatamente, sem pausar, pois não há valor em mantê-lo ativo.

É importante que o administrador selecione configurações apropriadas para [max_standby_archive_delay](runtime-config-replication.md#GUC-MAX-STANDBY-ARCHIVE-DELAY) e [max_standby_streaming_delay](runtime-config-replication.md#GUC-MAX-STANDBY-STREAMING-DELAY). As melhores escolhas variam dependendo das prioridades do negócio. Por exemplo, se o servidor estiver principalmente encarregado como um servidor de Alta Disponibilidade, então você deseja configurações de baixa demora, talvez até zero, embora isso seja um ajuste muito agressivo. Se o servidor de espera estiver encarregado como um servidor adicional para consultas de suporte de decisão, então pode ser aceitável definir os valores de atraso máximo em muitas horas, ou até -1, o que significa esperar para sempre que as consultas sejam concluídas.

Os "bits de indicação" do status da transação escritos no primário não são registrados no WAL, portanto, os dados no standby provavelmente reescreverão os indicativos novamente no standby. Assim, o servidor de standby ainda realizará gravações em disco, mesmo que todos os usuários sejam apenas de leitura; não ocorrerão alterações nos próprios valores dos dados. Os usuários ainda escreverão grandes arquivos temporários de classificação e recriarão os arquivos de informações relcache, portanto, nenhuma parte do banco de dados será verdadeiramente apenas de leitura durante o modo de standby quente. Note também que as gravações em bancos de dados remotos usando o módulo dblink e outras operações fora do banco de dados usando funções PL ainda serão possíveis, mesmo que a transação seja apenas de leitura localmente.

Os seguintes tipos de comandos de administração não são aceitos durante o modo de recuperação:

* Linguagem de Definição de Dados (DDL): ex., `CREATE INDEX`
* Privilegios e Propriedade: `GRANT`, `REVOKE`, `REASSIGN`
* Comandos de manutenção: `ANALYZE`, `VACUUM`, `CLUSTER`, `REINDEX`

Mais uma vez, observe que alguns desses comandos são, na verdade, permitidos durante transações em modo "somente leitura" no primário.

Como resultado, você não pode criar índices adicionais que existam apenas no standby, nem estatísticas que existam apenas no standby. Se esses comandos de administração forem necessários, eles devem ser executados no primário, e essas alterações se propagarão ao standby.

`pg_cancel_backend()` e `pg_terminate_backend()` funcionarão nos backends do usuário, mas não no processo de inicialização, que realiza a recuperação. `pg_stat_activity` não exibe transações recuperadas como ativas. Como resultado, `pg_prepared_xacts` está sempre vazio durante a recuperação. Se você deseja resolver transações preparadas em dúvida, consulte `pg_prepared_xacts` no primário e emita comandos para resolver as transações ou resolvê-las após o término da recuperação.

`pg_locks` mostrará bloqueios mantidos pelos backends, como de costume. `pg_locks` também mostra uma transação virtual gerenciada pelo processo de inicialização que possui todos os `AccessExclusiveLocks` mantidos por transações que estão sendo reinterpretadas pela recuperação. Observe que o processo de inicialização não adquire bloqueios para fazer alterações no banco de dados, e, portanto, os bloqueios que não são `AccessExclusiveLocks` não aparecem em `pg_locks` para o processo de inicialização; eles são apenas presumidos existir.

O plugin Nagios check_pgsql funcionará, porque as informações simples que ele verifica existem. O script de monitoramento check_postgres também funcionará, embora alguns valores relatados possam dar resultados diferentes ou confusos. Por exemplo, o último horário de vácuo não será mantido, uma vez que não há vácuo no modo standby. Os vácuos que funcionam no primário ainda enviam suas alterações para o standby.

Os comandos de controle de arquivo WAL não funcionarão durante a recuperação, por exemplo, `pg_backup_start`, `pg_switch_wal`, etc.

Os módulos dinamicamente carregáveis funcionam, incluindo `pg_stat_statements`.

As bloqueadoras de aconselhamento funcionam normalmente na recuperação, incluindo a detecção de deadlocks. Observe que as bloqueadoras de aconselhamento nunca são registradas no WAL, portanto, é impossível que uma bloqueadora de aconselhamento no primário ou no secundário entre em conflito com a reprodução do WAL. Além disso, não é possível adquirir uma bloqueadora de aconselhamento no primário e, em seguida, iniciá-la para que inicie uma bloqueadora de aconselhamento semelhante no secundário. As bloqueadoras de aconselhamento se relacionam apenas com o servidor no qual elas são adquiridas.

Sistemas de replicação baseados em gatilho, como Slony, Londiste e Bucardo, não funcionarão no modo standby, embora funcionem felizmente no servidor primário, desde que as alterações não sejam enviadas para os servidores de standby para serem aplicadas. O replay WAL não é baseado em gatilho, portanto, você não pode repassar do modo standby para qualquer sistema que exija escritas adicionais no banco de dados ou que dependa do uso de gatilhos.

Não é possível atribuir novos OIDs, embora alguns geradores de UUID ainda possam funcionar, desde que não dependam da escrita de um novo status no banco de dados.

Atualmente, a criação de tabelas temporárias não é permitida durante transações de leitura somente, portanto, em alguns casos, os scripts existentes não serão executados corretamente. Essa restrição pode ser relaxada em uma versão posterior. Esse é um problema de conformidade com o padrão SQL e um problema técnico.

`DROP TABLESPACE` só pode ser bem-sucedido se o tablespace estiver vazio. Alguns usuários de espera podem estar usando ativamente o tablespace através de seu parâmetro `temp_tablespaces`. Se houver arquivos temporários no tablespace, todas as consultas ativas serão canceladas para garantir que os arquivos temporários sejam removidos, de modo que o tablespace possa ser removido e o replay do WAL possa continuar.

Executar `DROP DATABASE` ou `ALTER DATABASE ... SET TABLESPACE` no primário gerará uma entrada no WAL que fará com que todos os usuários conectados a esse banco de dados no standby sejam desconectados à força. Essa ação ocorre imediatamente, independentemente da configuração de `max_standby_streaming_delay`. Note que `ALTER DATABASE ... RENAME` não desconecta os usuários, o que, na maioria dos casos, passará despercebido, embora, em alguns casos, possa causar confusão em um programa se depender de alguma forma do nome do banco de dados.

No modo normal (não de recuperação), se você emitir `DROP USER` ou `DROP ROLE` para um papel com capacidade de login enquanto o usuário ainda estiver conectado, nada acontece com o usuário conectado — ele permanece conectado. O usuário, no entanto, não pode se reconectar. Esse comportamento também se aplica na recuperação, portanto, um `DROP USER` no primário não desconecta o usuário em standby.

O sistema de estatísticas cumulativas está ativo durante a recuperação. Todos os varreduras, leituras, blocos, uso do índice, etc., serão registrados normalmente no modo standby. No entanto, o replay WAL não incrementará os contadores específicos da relação e do banco de dados. Ou seja, o replay não incrementará as colunas `pg_stat_all_tables` (como `n_tup_ins`), nem as leituras ou escritas realizadas pelo processo de inicialização serão rastreadas nas visualizações `pg_statio_`, nem as colunas `pg_stat_database` associadas serão incrementadas.

O Autovacuum não está ativo durante a recuperação. Ele começará normalmente no final da recuperação.

O processo de verificador de ponto de verificação e o processo de escritor de segundo plano estão ativos durante a recuperação. O processo de verificador de ponto de verificação realizará pontos de reinício (semelhantes aos pontos de verificação no servidor primário) e o processo de escritor de segundo plano realizará atividades normais de limpeza de blocos. Isso pode incluir atualizações das informações do bit de indicação armazenadas no servidor de espera. O comando `CHECKPOINT` é aceito durante a recuperação, embora ele realize um ponto de reinício em vez de um novo ponto de verificação.

### 26.4.4. Referência do parâmetro de standby quente [#](#HOT-STANDBY-PARAMETERS)

Vários parâmetros foram mencionados acima em [Seção 26.4.2](hot-standby.md#HOT-STANDBY-CONFLICT) e [Seção 26.4.3](hot-standby.md#HOT-STANDBY-ADMIN).

No primário, o parâmetro [wal_level](runtime-config-wal.md#GUC-WAL-LEVEL) pode ser usado. [max_standby_archive_delay](runtime-config-replication.md#GUC-MAX-STANDBY-ARCHIVE-DELAY) e [max_standby_streaming_delay](runtime-config-replication.md#GUC-MAX-STANDBY-STREAMING-DELAY) não têm efeito se configurados no primário.

Em espera, os parâmetros [hot_standby](runtime-config-replication.md#GUC-HOT-STANDBY), [max_standby_archive_delay](runtime-config-replication.md#GUC-MAX-STANDBY-ARCHIVE-DELAY) e [max_standby_streaming_delay](runtime-config-replication.md#GUC-MAX-STANDBY-STREAMING-DELAY) podem ser utilizados.

### 26.4.5. **Aviso [#](#HOT-STANDBY-CAVEATS)

Há várias limitações do modo standby quente. Essas podem e provavelmente serão corrigidas em versões futuras:

* É necessário ter conhecimento completo sobre as transações em execução antes que instantâneos possam ser tomados. Transações que utilizam um grande número de subtransações (atualmente maior que 64) atrasarão o início das conexões somente de leitura até o término da transação de escrita em execução mais longa. Se essa situação ocorrer, mensagens explicativas serão enviadas ao log do servidor.
* Pontos de partida válidos para consultas de standby são gerados em cada ponto de verificação no principal. Se o standby for desligado enquanto o principal estiver em estado de desligamento, pode não ser possível reingressar no modo standby quente até que o principal seja iniciado, de modo que ele gere mais pontos de partida nos logs WAL. Essa situação não é um problema nas situações mais comuns em que isso pode acontecer. Geralmente, se o principal for desligado e não estiver mais disponível, isso provavelmente é devido a uma falha grave que exige que o standby seja convertido para operar como o novo principal de qualquer maneira. E em situações em que o principal está sendo intencionalmente desligado, coordenar para garantir que o standby se torne o novo principal de forma suave também é um procedimento padrão.
* No final da recuperação, as transações `AccessExclusiveLocks` mantidas por transações preparadas exigirão o dobro do número normal de entradas na tabela de bloqueio. Se você planeja executar um grande número de transações preparadas concorrentes que normalmente levam `AccessExclusiveLocks`, ou planeja ter uma grande transação que leva muitos `AccessExclusiveLocks`, é aconselhável selecionar um valor maior de `max_locks_per_transaction`, talvez tanto quanto o dobro do valor do parâmetro no servidor principal. Você não precisa considerar isso de forma alguma se sua configuração de `max_prepared_transactions` for 0.
* O nível de isolamento de transação serializável ainda não está disponível no standby quente. (Consulte [Seção 13.2.3](transaction-iso.md#XACT-SERIALIZABLE) e [Seção 13.4.1](applevel-consistency.md#SERIALIZABLE-CONSISTENCY) para detalhes.) Uma tentativa de definir uma transação para o nível de isolamento serializável no modo de standby quente gerará um erro.