## 54.4. Protocolo de Replicação de Streaming [#](#PROTOCOL-REPLICATION)

Para iniciar a replicação de streaming, o frontend envia o parâmetro `replication` na mensagem de inicialização. Um valor booleano de `true` (ou `on`, `yes`, `1`) informa ao backend para entrar no modo de replicação física walsender, no qual um pequeno conjunto de comandos de replicação, mostrados abaixo, pode ser emitido em vez de declarações SQL.

Passar `database` como o valor para o parâmetro `replication` instrui o backend a entrar no modo de replicação lógica walsender, conectando-se ao banco de dados especificado no parâmetro `dbname`. No modo de replicação lógica walsender, os comandos de replicação mostrados abaixo, bem como comandos SQL normais, podem ser emitidos.

Em modo de replicação física ou lógica walsender, apenas o protocolo de consulta simples pode ser usado.

Para testar comandos de replicação, você pode estabelecer uma conexão de replicação via psql ou qualquer outra ferramenta que utilize a libpq, com uma string de conexão que inclua a opção `replication`, por exemplo:

```
psql "dbname=postgres replication=database" -c "IDENTIFY_SYSTEM;"
```

No entanto, é frequentemente mais útil usar [pg_receivewal][(app-pgreceivewal.md "pg_receivewal")] (para replicação física) ou [pg_recvlogical][(app-pgrecvlogical.md "pg_recvlogical")] (para replicação lógica).

Os comandos de replicação são registrados no log do servidor quando [log_replication_commands][(runtime-config-logging.md#GUC-LOG-REPLICATION-COMMANDS) está habilitado.

Os comandos aceitos no modo de replicação são:

`IDENTIFY_SYSTEM` [#](#PROTOCOL-REPLICATION-IDENTIFY-SYSTEM): Solicita que o servidor se identifique. O servidor responde com um conjunto de resultados de uma única linha, contendo quatro campos:

`systemid` (`text`) :   O identificador único do sistema que identifica o grupo. Isso pode ser usado para verificar se o backup de base utilizado para inicializar o standby veio do mesmo grupo.

`timeline` (`int8`) : ID do cronograma atual. Também útil para verificar se o modo standby está consistente com o principal.

`xlogpos` (`text`) :   Local atual do esvaziamento do WAL. Útil para obter um local conhecido no log de pré-escrita onde o fluxo pode começar.

`dbname` (`text`) :   Banco de dados conectado ou nulo.

`SHOW` *`name`* [#](#PROTOCOL-REPLICATION-SHOW): Pede ao servidor que envie a configuração atual de um parâmetro de tempo de execução. Isso é semelhante ao comando SQL [SHOW](sql-show.md "SHOW").

*`name`* :   O nome de um parâmetro de tempo de execução. Os parâmetros disponíveis estão documentados em [Capítulo 19][(runtime-config.md "Chapter 19. Server Configuration")].

`TIMELINE_HISTORY` *`tli`* [#](#PROTOCOL-REPLICATION-TIMELINE-HISTORY): Pede ao servidor que envie o arquivo de histórico da linha do tempo para a linha do tempo *`tli`*. O servidor responde com um conjunto de resultados de uma única linha, contendo dois campos. Embora os campos estejam rotulados como `text`, eles efetivamente retornam bytes brutos, sem conversão de codificação:

`filename` (`text`) :   Nome do arquivo do histórico do cronograma, por exemplo, `00000002.history`.

`content` (`text`) :   Conteúdo do arquivo de histórico de linha de tempo.

`CREATE_REPLICATION_SLOT` *`slot_name`* [ `TEMPORARY` ] { `PHYSICAL` | `LOGICAL` *`output_plugin`* } [ ( *`option`* [, ...] ) ] [#](#PROTOCOL-REPLICATION-CREATE-REPLICATION-SLOT): Crie um slot de replicação físico ou lógico. Consulte [Seção 26.2.6](warm-standby.md#STREAMING-REPLICATION-SLOTS "26.2.6. Replication Slots") para mais informações sobre slots de replicação.

*`slot_name`* :   O nome do slot a ser criado. Deve ser um nome válido de slot de replicação (consulte [Seção 26.2.6.1][(warm-standby.md#STREAMING-REPLICATION-SLOTS-MANIPULATION "26.2.6.1. Querying and Manipulating Replication Slots")]).

*`output_plugin`* :   O nome do plugin de saída utilizado para decodificação lógica (ver [Seção 47.6][(logicaldecoding-output-plugin.md "47.6. Logical Decoding Output Plugins")]).

`TEMPORARY` : Especifique que este slot de replicação é temporário. Os slots temporários não são salvos no disco e são automaticamente descartados em caso de erro ou quando a sessão termina.

As seguintes opções são suportadas:

`TWO_PHASE [ boolean ]` :   Se verdadeiro, este slot de replicação lógica suporta a decodificação do compromisso de duas fases. Com esta opção, os comandos relacionados ao compromisso de duas fases, como `PREPARE TRANSACTION`, `COMMIT PREPARED` e `ROLLBACK PREPARED`, são decodificados e transmitidos. A transação será decodificada e transmitida no momento de `PREPARE TRANSACTION`. O padrão é falso.

`RESERVE_WAL [ boolean ]` :   Se verdadeiro, este slot de replicação física reserva o WAL imediatamente. Caso contrário, o WAL é reservado apenas após a conexão de um cliente de replicação em streaming. O padrão é falso.

`SNAPSHOT { 'export' | 'use' | 'nothing' }` : Decide o que fazer com o instantâneo criado durante a inicialização do slot lógico. `'export'`, que é o padrão, exportará o instantâneo para uso em outras sessões. Esta opção não pode ser usada dentro de uma transação. `'use'` usará o instantâneo para a transação atual que está executando o comando. Esta opção deve ser usada em uma transação, e `CREATE_REPLICATION_SLOT` deve ser o primeiro comando executado nessa transação. Finalmente, `'nothing'` usará apenas o instantâneo para decodificação lógica como de costume, mas não fará nada além disso.

`FAILOVER [ boolean ]` :   Se verdadeiro, a posição é habilitada para ser sincronizada com os standbys, de modo que a replicação lógica possa ser retomada após o failover. O padrão é falso.

Em resposta a este comando, o servidor enviará um conjunto de resultados de uma única linha contendo os seguintes campos:

`slot_name` (`text`) :   O nome do slot de replicação recém-criado.

`consistent_point` (`text`) :   A localização do WAL na qual a posição se tornou consistente. Esta é a localização mais antiga a partir da qual o streaming pode começar nesta posição de replicação.

`snapshot_name` (`text`) :   O identificador do instantâneo exportado pelo comando. O instantâneo é válido até que um novo comando seja executado nesta conexão ou a conexão de replicação seja fechada. Nulo se o slot criado for físico.

`output_plugin` (`text`) :   O nome do plugin de saída utilizado pelo slot de replicação recém-criado. Nulo se o slot criado for físico.

`CREATE_REPLICATION_SLOT` *`slot_name`* [ `TEMPORARY` ] { `PHYSICAL` [ `RESERVE_WAL` ] | `LOGICAL` *`output_plugin`* [ `EXPORT_SNAPSHOT` | `NOEXPORT_SNAPSHOT` | `USE_SNAPSHOT` | `TWO_PHASE` ] } [#](#PROTOCOL-REPLICATION-CREATE-REPLICATION-SLOT-LEGACY): Para compatibilidade com versões anteriores, essa sintaxe alternativa para o comando `CREATE_REPLICATION_SLOT` ainda é suportada.

`ALTER_REPLICATION_SLOT` *`slot_name`* ( *`option`* [, ...] ) [#](#PROTOCOL-REPLICATION-ALTER-REPLICATION-SLOT): Altere a definição de um slot de replicação. Consulte [Seção 26.2.6](warm-standby.md#STREAMING-REPLICATION-SLOTS "26.2.6. Replication Slots") para mais informações sobre slots de replicação. Este comando é atualmente suportado apenas para slots de replicação lógicos.

*`slot_name`* :   O nome do slot a ser alterado. Deve ser um nome válido de slot de replicação (consulte [Seção 26.2.6.1][(warm-standby.md#STREAMING-REPLICATION-SLOTS-MANIPULATION "26.2.6.1. Querying and Manipulating Replication Slots")]).

As seguintes opções são suportadas:

`TWO_PHASE [ boolean ]` :   Se verdadeiro, este slot de replicação lógica suporta a decodificação do compromisso de duas fases. Com esta opção, os comandos relacionados ao compromisso de duas fases, como `PREPARE TRANSACTION`, `COMMIT PREPARED` e `ROLLBACK PREPARED`, são decodificados e transmitidos. A transação será decodificada e transmitida no momento `PREPARE TRANSACTION`.

`FAILOVER [ boolean ]` :   Se verdadeiro, a posição é habilitada para ser sincronizada com os standbys, de modo que a replicação lógica possa ser retomada após o failover.

`READ_REPLICATION_SLOT` *`slot_name`* [#](#PROTOCOL-REPLICATION-READ-REPLICATION-SLOT): Leia algumas informações associadas a um slot de replicação. Retorna um tuple com os valores de `NULL` se o slot de replicação não existir. Este comando é atualmente suportado apenas para slots de replicação física.

Em resposta a este comando, o servidor retornará um conjunto de resultados de uma única linha, contendo os seguintes campos:

`slot_type` (`text`) :   O tipo de slot de replicação, `physical` ou `NULL`.

`restart_lsn` (`text`) : A fenda de replicação `restart_lsn`.

`restart_tli` (`int8`) :   O ID de linha de tempo associado a `restart_lsn`, de acordo com o histórico atual da linha de tempo.

`START_REPLICATION` [ `SLOT` *`slot_name`* ] [ `PHYSICAL` ] *`XXX/XXX`* [ `TIMELINE` *`tli`* ] [#](#PROTOCOL-REPLICATION-START-REPLICATION): Instrui o servidor a começar a transmitir o WAL, começando na localização do WAL *`XXX/XXX`*. Se a opção `TIMELINE` for especificada, a transmissão começa no cronograma *`tli`*; caso contrário, o cronograma atual do servidor é selecionado. O servidor pode responder com um erro, por exemplo, se a seção solicitada do WAL já tiver sido reciclada. Se for bem-sucedido, o servidor responde com uma mensagem CopyBothResponse, e então começa a transmitir o WAL para o frontend.

Se o nome de um slot for fornecido via *`slot_name`*, ele será atualizado à medida que a replicação avança, para que o servidor saiba quais segmentos do WAL e, se `hot_standby_feedback` está em quais transações, ainda são necessários pelo standby.

Se o cliente solicitar uma linha do tempo que não é a mais recente, mas faz parte do histórico do servidor, o servidor transmitirá todo o WAL nessa linha do tempo, começando pelo ponto de início solicitado até o ponto em que o servidor mudou para outra linha do tempo. Se o cliente solicitar a transmissão exatamente no final de uma linha do tempo antiga, o servidor pulará o modo COPIAR por completo.

Após transmitir todos os WAL em uma linha de tempo que não é a mais recente, o servidor terminará a transmissão saindo do modo COPY. Quando o cliente confirma isso, também saindo do modo COPY, o servidor envia um conjunto de resultados com uma linha e duas colunas, indicando a próxima linha de tempo na história desse servidor. A primeira coluna é o ID da próxima linha de tempo (tipo `int8`), e a segunda coluna é a localização do WAL onde ocorreu a mudança (tipo `text`). Normalmente, a posição da mudança é o final do WAL que foi transmitido, mas há casos especiais em que o servidor pode enviar alguns WAL da linha de tempo antiga que ele não replicou antes de promover. Finalmente, o servidor envia duas mensagens CommandComplete (uma que termina o CopyData e a outra termina o próprio `START_REPLICATION`), e está pronto para aceitar um novo comando.

Os dados do WAL são enviados como uma série de mensagens CopyData; consulte [Seção 54.6][(protocol-message-types.md "54.6. Message Data Types")] e [Seção 54.7][(protocol-message-formats.md "54.7. Message Formats")] para detalhes. (Isso permite que outras informações sejam misturadas; em particular, o servidor pode enviar uma mensagem ErrorResponse se encontrar uma falha após começar a transmitir.) O payload de cada mensagem CopyData do servidor para o cliente contém uma mensagem de um dos seguintes formatos:

XLogData (B) [#](#PROTOCOL-REPLICATION-XLOGDATA) :   Byte1('w') :   Identifica a mensagem como dados WAL.

Int64:   O ponto de partida dos dados WAL nesta mensagem.

Int64:   O fim atual do WAL no servidor.

Int64:   O relógio do sistema do servidor no momento da transmissão, em microsegundos desde a meia-noite de 2000-01-01.

Byte*`n`* :   Uma seção do fluxo de dados WAL.

Um único registro WAL nunca é dividido em duas mensagens XLogData. Quando um registro WAL cruza uma borda de página WAL e, portanto, já está dividido usando registros de continuidade, ele pode ser dividido na borda da página. Em outras palavras, o primeiro registro principal WAL e seus registros de continuidade podem ser enviados em diferentes mensagens XLogData.

Mensagem de keepalive primária (B) [#](#PROTOCOL-REPLICATION-PRIMARY-KEEPALIVE-MESSAGE) :   Byte1('k') :   Identifica a mensagem como uma keepalive do remetente.

Int64:   O fim atual do WAL no servidor.

Int64:   O relógio do sistema do servidor no momento da transmissão, em microsegundos desde a meia-noite de 2000-01-01.

Byte1:   1 significa que o cliente deve responder a esta mensagem o mais rápido possível, para evitar uma desconexão por tempo excedido. 0 caso contrário.

O processo de recebimento pode enviar respostas de volta ao remetente a qualquer momento, usando um dos seguintes formatos de mensagem (também no payload de uma mensagem CopyData):

Atualização do estado de espera (F) [#](#PROTOCOL-REPLICATION-STANDBY-STATUS-UPDATE) :   Byte1('r') :   Identifica a mensagem como uma atualização do status de receptor.

Int64:   A localização do último byte WAL recebido e escrito no disco no modo standby.

Int64:   A localização do último byte WAL  + 1 que foi descarregado no disco no modo standby.

Int64:   A localização do último byte WAL + 1 aplicado no standby.

Int64:   O relógio do sistema do cliente no momento da transmissão, em microsegundos desde a meia-noite de 2000-01-01.

Byte1:   Se 1, o cliente solicita que o servidor responda a esta mensagem imediatamente. Isso pode ser usado para pingar o servidor, para testar se a conexão ainda está saudável.

Mensagem de feedback em modo standby quente (F) [#](#PROTOCOL-REPLICATION-HOT-STANDBY-FEEDBACK-MESSAGE) :   Byte1('h') :   Identifica a mensagem como uma mensagem de feedback em modo standby quente.

Int64:   O relógio do sistema do cliente no momento da transmissão, em microsegundos desde a meia-noite de 2000-01-01.

Int32: O atual `xmin` do standby, excluindo o `catalog_xmin` de quaisquer slots de replicação. Se tanto este valor quanto o seguinte `catalog_xmin` forem 0, isso é tratado como uma notificação de que o feedback do standby quente não será enviado mais nesta conexão. Mensagens posteriores que não sejam zero podem reiniciar o mecanismo de feedback.

Int32:   A época do xid global `xmin` em standby.

Int32:   O menor `catalog_xmin` de qualquer slot de replicação no modo standby. Definido como 0 se não existir nenhum `catalog_xmin` no modo standby ou se o feedback de standby quente estiver sendo desativado.

Int32:   A época do xid `catalog_xmin` em standby.

`START_REPLICATION` `SLOT` *`slot_name`* `LOGICAL` *`XXX/XXX`* [ ( *`option_name`* [ *`option_value`* ] [, ...] ) ] [#](#PROTOCOL-REPLICATION-START-REPLICATION-SLOT-LOGICAL): Instrui o servidor a começar a transmitir o WAL para a replicação lógica, começando em qualquer localização do WAL *`XXX/XXX`* ou no slot `confirmed_flush_lsn` (ver [Seção 53.20](view-pg-replication-slots.md "53.20. pg_replication_slots")), o que for maior. Esse comportamento facilita para os clientes evitar a atualização do status local do LSN quando não há dados a serem processados. No entanto, começar em um LSN diferente do solicitado pode não detectar certos tipos de erros do cliente; portanto, o cliente pode desejar verificar se `confirmed_flush_lsn` corresponde às suas expectativas antes de emitir `START_REPLICATION`.

O servidor pode responder com um erro, por exemplo, se a posição não existir. Se for bem-sucedido, o servidor responde com uma mensagem CopyBothResponse e, em seguida, começa a transmitir o WAL para o frontend.

As mensagens dentro das mensagens CopyBothResponse têm o mesmo formato documentado para `START_REPLICATION ... PHYSICAL`, incluindo duas mensagens CommandComplete.

O plugin de saída associado ao slot selecionado é usado para processar a saída para transmissão em streaming.

`SLOT` *`slot_name`* :   O nome do slot para transmissão de alterações. Este parâmetro é obrigatório e deve corresponder a um slot de replicação lógica existente criado com `CREATE_REPLICATION_SLOT` no modo `LOGICAL`.

*`XXX/XXX`* :   O local do WAL para começar a transmitir.

*`option_name`* :   O nome de uma opção passada para a saída de decodificação lógica do slot. Consulte a [Seção 54.5][(protocol-logical-replication.md "54.5. Logical Streaming Replication Protocol") para opções que são aceitas pelo plugin padrão (`pgoutput`).

*`option_value`* :   Valor opcional, na forma de uma constante de string, associado à opção especificada.

`DROP_REPLICATION_SLOT` *`slot_name`* [ `WAIT` ] [#](#PROTOCOL-REPLICATION-DROP-REPLICATION-SLOT): Descarta um slot de replicação, liberando quaisquer recursos reservados no lado do servidor.

*`slot_name`* :   O nome do slot a ser descartado.

`WAIT` :   Essa opção faz com que o comando espere até que o slot se torne inativo, em vez do comportamento padrão de gerar um erro.

`UPLOAD_MANIFEST` [#](#PROTOCOL-REPLICATION-UPLOAD-MANIFEST): Carrega um manifesto de backup em preparação para a realização de um backup incremental.

`BASE_BACKUP` [ ( *`option`* [, ...] ) ] [#](#PROTOCOL-REPLICATION-BASE-BACKUP): Instrui o servidor a iniciar o streaming de um backup de base. O sistema será automaticamente colocado no modo de backup antes do início do backup e retirado dele quando o backup estiver completo. As seguintes opções são aceitas:

`LABEL` *`'label'`* :   Define o rótulo do backup. Se não for especificado, será usado um rótulo de backup de `base backup`. As regras de citação para o rótulo são as mesmas de uma string SQL padrão com [standard_conforming_strings](runtime-config-compatible.md#GUC-STANDARD-CONFORMING-STRINGS) ativado.

`TARGET` *`'target'`* : Diz ao servidor para onde enviar o backup. Se o alvo for `client`, que é o padrão, os dados do backup são enviados ao cliente. Se for `server`, os dados do backup são escritos no servidor no caminho especificado pela opção `TARGET_DETAIL`. Se for `blackhole`, os dados do backup não são enviados para nenhum lugar; eles são simplesmente descartados.

O alvo `server` exige privilégio de superusuário ou concessão do papel `pg_write_server_files`.

`TARGET_DETAIL` *`'detail'`* :   Fornece informações adicionais sobre o alvo de backup.

Atualmente, essa opção só pode ser usada quando o alvo de backup é `server`. Especifica o diretório do servidor para o qual o backup deve ser escrito.

`PROGRESS [ boolean ]` :   Se definido como verdadeiro, solicita informações necessárias para gerar um relatório de progresso. Isso enviará um tamanho aproximado no cabeçalho de cada espaço de tabela, que pode ser usado para calcular até que ponto o fluxo está concluído. Isso é calculado enumerando todos os tamanhos de arquivo uma vez antes de a transferência ser iniciada, e, como tal, pode ter um impacto negativo no desempenho. Em particular, pode levar mais tempo até que os primeiros dados sejam transmitidos. Como os arquivos do banco de dados podem mudar durante o backup, o tamanho é apenas aproximado e pode crescer e diminuir entre o momento da aproximação e o envio dos arquivos reais. O padrão é falso.

`CHECKPOINT { 'fast' | 'spread' }` :   Define o tipo de verificação a ser realizada no início do backup da base. O padrão é `spread`.

`WAL [ boolean ]` : Se definido como verdadeiro, inclua os segmentos WAL necessários no backup. Isso incluirá todos os arquivos entre o início e o fim do backup no diretório `pg_wal` do arquivo de diretório base. O padrão é falso.

`WAIT [ boolean ]` : Se definido como verdadeiro, o backup aguardará até que o último segmento WAL necessário tenha sido arquivado, ou emitirá um aviso se o arquivamento do WAL não estiver habilitado. Se falso, o backup não aguardará nem emitirá um aviso, deixando o cliente responsável por garantir que o log necessário esteja disponível. O padrão é verdadeiro.

`COMPRESSION` *`'method'`* : Instrui o servidor a comprimir o backup usando o método especificado. Atualmente, os métodos suportados são `gzip`, `lz4` e `zstd`.

`COMPRESSION_DETAIL` *`detail`* : Especifica os detalhes do método de compressão escolhido. Isso deve ser usado apenas em conjunto com a opção `COMPRESSION`. Se o valor for um número inteiro, ele especifica o nível de compressão. Caso contrário, deve ser uma lista de itens separados por vírgula, cada um na forma de *`keyword`* ou *`keyword=value`*. Atualmente, as palavras-chave suportadas são `level`, `long` e `workers`.

A palavra-chave `level` define o nível de compressão. Para `gzip`, o nível de compressão deve ser um número inteiro entre `1` e `9` (padrão `Z_DEFAULT_COMPRESSION` ou `-1`), para `lz4`, um número inteiro entre 1 e 12 (padrão `0` para o modo de compressão rápida), e para `zstd`, um número inteiro entre `ZSTD_minCLevel()` (geralmente `-131072`) e `ZSTD_maxCLevel()` (geralmente `22`), (padrão `ZSTD_CLEVEL_DEFAULT` ou `3`).

A palavra-chave `long` habilita o modo de correspondência de longa distância, para uma melhor taxa de compressão, às custas do uso de memória maior. O modo de longa distância é suportado apenas para `zstd`.

A palavra-chave `workers` define o número de threads que devem ser usadas para compressão paralela. A compressão paralela é suportada apenas para `zstd`.

`MAX_RATE` *`rate`* :   Limite (regulador) a quantidade máxima de dados transferidos do servidor para o cliente por unidade de tempo. A unidade esperada é kilobytes por segundo. Se esta opção for especificada, o valor deve ser igual a zero ou deve estar dentro da faixa de 32 kB até 1 GB (inclusive). Se zero for passado ou a opção não for especificada, nenhuma restrição é imposta à transferência.

`TABLESPACE_MAP [ boolean ]` :   Se verdadeiro, inclua informações sobre os links simbólicos presentes no diretório `pg_tblspc` em um arquivo denominado `tablespace_map`. O arquivo de mapa do tablespace inclui cada nome do link simbólico conforme ele existe no diretório `pg_tblspc/` e o caminho completo desse link simbólico. O padrão é falso.

`VERIFY_CHECKSUMS [ boolean ]` :   Se verdadeiro, os checksums são verificados durante um backup básico se estiverem habilitados. Se falso, isso é ignorado. O padrão é verdadeiro.

`MANIFEST` *`manifest_option`* :   Quando esta opção é especificada com um valor de `yes` ou `force-encode`, um manifesto de backup é criado e enviado juntamente com o backup. O manifesto é uma lista de todos os arquivos presentes no backup, com exceção de quaisquer arquivos WAL que possam ser incluídos. Ele também armazena o tamanho, o horário de última modificação e, opcionalmente, um checksum para cada arquivo. Um valor de `force-encode` força que todos os nomes de arquivos sejam codificados em hexadecimal; caso contrário, este tipo de codificação é realizado apenas para arquivos cujos nomes são sequências de octal não UTF8. `force-encode` é destinado principalmente para fins de teste, para garantir que os clientes que leem o manifesto de backup possam lidar com este caso. Para compatibilidade com versões anteriores, o padrão é `MANIFEST 'no'`.

`MANIFEST_CHECKSUMS` *`checksum_algorithm`* : Especifica o algoritmo de verificação de checksum que deve ser aplicado a cada arquivo incluído no manifesto de backup. Atualmente, os algoritmos disponíveis são `NONE`, `CRC32C`, `SHA224`, `SHA256`, `SHA384` e `SHA512`. O padrão é `CRC32C`.

`INCREMENTAL` : Solicita um backup incremental. O comando `UPLOAD_MANIFEST` deve ser executado antes de executar um backup de base com esta opção.

Quando o backup for iniciado, o servidor enviará primeiro dois conjuntos de resultados comuns, seguidos por um ou mais resultados CopyOutResponse.

O primeiro conjunto de resultados ordinário contém a posição inicial do backup, em uma única linha com duas colunas. A primeira coluna contém a posição inicial dada no formato XLogRecPtr, e a segunda coluna contém o ID correspondente da linha de tempo.

O segundo conjunto de resultados ordinário tem uma linha para cada tablespace. Os campos nesta linha são:

`spcoid` (`oid`) :   O OID do tablespace, ou nulo se for o diretório base.

`spclocation` (`text`) :   O caminho completo do diretório do tablespace, ou nulo se for o diretório base.

`size` (`int8`) :   O tamanho aproximado do espaço de tabelas, em kilobytes (1024 bytes), se o relatório de progresso tiver sido solicitado; caso contrário, é nulo.

Após o segundo conjunto de resultados regulares, uma resposta de cópia será enviada. O payload de cada mensagem de CopyData conterá uma mensagem em um dos seguintes formatos:

novo arquivo (B) :   Byte1('n') :   Identifica a mensagem como indicando o início de um novo arquivo. Haverá um arquivo para o diretório de dados principal e um para cada espaço de tabela adicional; cada um usará o formato tar (seguindo o "formato de intercâmbio ustar" especificado no padrão POSIX 1003.1-2008).

String:   O nome do arquivo para este arquivo.

String:   Para o diretório de dados principal, uma string vazia. Para outros espaços de tabela, o caminho completo para o diretório a partir do qual este arquivo foi criado.

manifesto (B) : Byte1('m') : Identifica a mensagem que indica o início do manifesto de backup.

arquivo ou manifesto de dados (B) : Byte1('d') : Identifica a mensagem como contendo dados de arquivo ou manifesto.

Byte*`n`* : Bytes de dados.

Relatório de progresso (B) : Byte1('p') : Identifica a mensagem como um relatório de progresso.

Int64:   O número de bytes da área de tabelas atual para a qual o processamento foi concluído.

Após a resposta de cópia ter sido enviada, ou todas as respostas, um conjunto final de resultados ordinários será enviado, contendo a posição final do WAL do backup, no mesmo formato da posição inicial.

O arquivo tar do diretório de dados e de cada espaço de tabela conterá todos os arquivos dos diretórios, independentemente de serem arquivos do PostgreSQL ou outros arquivos adicionados ao mesmo diretório. Os únicos arquivos excluídos são:

* `postmaster.pid` * `postmaster.opts` * `pg_internal.init` (encontrado em vários diretórios) * Vários arquivos e diretórios temporários criados durante o funcionamento do servidor PostgreSQL, como qualquer arquivo ou diretório que comece com `pgsql_tmp` e relações temporárias. * Relações não registradas, exceto o fork init, que é necessário para recriar a relação (vazia) não registrada na recuperação. * `pg_wal`, incluindo subdiretórios. Se o backup for executado com arquivos WAL incluídos, uma versão sintetizada de `pg_wal` será incluída, mas ela conterá apenas os arquivos necessários para o backup funcionar, não o resto do conteúdo. * `pg_dynshmem`, `pg_notify`, `pg_replslot`, `pg_serial`, `pg_snapshots`, `pg_stat_tmp` e `pg_subtrans` são copiados como diretórios vazios (mesmo que sejam links simbólicos). * Arquivos que não são arquivos regulares e diretórios, como links simbólicos (exceto para os diretórios listados acima) e arquivos especiais de dispositivos e sistemas operacionais, são ignorados. (Links simbólicos em `pg_tblspc` são mantidos.)

O modo de proprietário, grupo e arquivo é definido se o sistema de arquivos subjacente no servidor o suportar.

Em todos os comandos acima, ao especificar um parâmetro do tipo `boolean`, a parte *`value`* pode ser omitida, o que é equivalente a especificar `TRUE`.