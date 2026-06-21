## pg_basebackup

pg_basebackup — fazer um backup de base de um clúster PostgreSQL

## Sinopse

`pg_basebackup` [*`option`*...]

## Descrição

O pg_basebackup é usado para fazer um backup básico de um clúster de banco de dados PostgreSQL em execução. O backup é feito sem afetar outros clientes do banco de dados e pode ser usado tanto para recuperação em um ponto no tempo (consulte [Seção 25.3][(continuous-archiving.md "25.3. Continuous Archiving and Point-in-Time Recovery (PITR)]) quanto como ponto de partida para um servidor de envio de log ou de replicação em streaming (consulte [Seção 26.2][(warm-standby.md "26.2. Log-Shipping Standby Servers")]).

O pg_basebackup pode realizar um backup de base completo ou incremental do banco de dados. Quando usado para realizar um backup completo, ele faz uma cópia exata dos arquivos do clúster do banco de dados. Quando usado para realizar um backup incremental, alguns arquivos que seriam parte de um backup completo podem ser substituídos por versões incrementais dos mesmos arquivos, contendo apenas os blocos que foram modificados desde o backup de referência. Um backup incremental não pode ser usado diretamente; em vez disso, [pg_combinebackup][(app-pgcombinebackup.md "pg_combinebackup")] deve ser usado primeiro para combiná-lo com os backups anteriores dos quais depende. Consulte [Seção 25.3.3][(continuous-archiving.md#BACKUP-INCREMENTAL-BACKUP "25.3.3. Making an Incremental Backup")] para mais informações sobre backups incrementais e [Seção 25.3.5][(continuous-archiving.md#BACKUP-PITR-RECOVERY "25.3.5. Recovering Using a Continuous Archive Backup")] para etapas de recuperação a partir de um backup.

Em qualquer modo, o pg_basebackup garante que o servidor seja colocado no modo de backup e retirado dele automaticamente. Os backups são sempre feitos do conjunto de bancos de dados inteiros; não é possível fazer backups de bancos de dados ou objetos de banco de dados individuais. Para backups seletivos, outra ferramenta, como [pg_dump][(app-pgdump.md "pg_dump")], deve ser usada.

O backup é feito através de uma conexão regular com PostgreSQL que utiliza o protocolo de replicação. A conexão deve ser feita com um ID de usuário que tenha permissões `REPLICATION` (consulte [Seção 21.2][(role-attributes.md "21.2. Role Attributes")]) ou seja um superusuário, e [[`pg_hba.conf`][(auth-pg-hba-conf.md "20.1. The pg_hba.conf File")]] deve permitir a conexão de replicação. O servidor também deve ser configurado com [max_wal_senders][(runtime-config-replication.md#GUC-MAX-WAL-SENDERS)] definido o suficiente para fornecer pelo menos um walsender para o backup, além de um para o streaming WAL (se usado).

Pode haver vários `pg_basebackup`s em execução ao mesmo tempo, mas geralmente é melhor, do ponto de vista de desempenho, fazer apenas um backup e copiar o resultado.

O pg_basebackup pode fazer um backup de base não apenas de um servidor primário, mas também de um de reserva. Para fazer um backup de um de reserva, configure o de reserva para que ele possa aceitar conexões de replicação (ou seja, defina `max_wal_senders` e [hot_standby][(runtime-config-replication.md#GUC-HOT-STANDBY)] e configure seu `pg_hba.conf` adequadamente). Você também precisará habilitar [full_page_writes][(runtime-config-wal.md#GUC-FULL-PAGE-WRITES)] no primário.

Observe que há algumas limitações ao fazer um backup de um estado de espera:

* O arquivo de histórico de backup não é criado no clúster de banco de dados que está sendo protegido.
* O pg_basebackup não pode forçar o standby a mudar para um novo arquivo WAL no final do backup. Quando você está usando `-X none`, se a atividade de escrita no primário for baixa, o pg_basebackup pode precisar esperar um longo tempo para que o último arquivo WAL necessário para o backup seja trocado e arquivado. Neste caso, pode ser útil executar `pg_switch_wal` no primário para desencadear um imediato troco de arquivo WAL.
* Se o standby for promovido a ser primário durante o backup, o backup falha.
* Todos os registros WAL necessários para o backup devem conter escritas suficientes de página completa, o que exige que você habilite `full_page_writes` no primário.

Sempre que o pg_basebackup estiver fazendo um backup de base, a vista `pg_stat_progress_basebackup` do servidor informará o progresso do backup. Consulte [Seção 27.4.6][(progress-reporting.md#BASEBACKUP-PROGRESS-REPORTING "27.4.6. Base Backup Progress Reporting")] para obter detalhes.

## Opções

As opções de linha de comando a seguir controlam a localização e o formato do resultado:

`-D directory` `--pgdata=directory`: Define o diretório-alvo para onde o resultado será escrito. O pg_basebackup criará esse diretório (e quaisquer diretórios parentais ausentes) se ele não existir. Se ele já existir, ele deve estar vazio.

Quando o backup estiver no formato tar, o diretório de destino pode ser especificado como `-` (ponto e vírgula), fazendo com que o arquivo tar seja escrito em `stdout`.

Esta opção é necessária.

`-F format` `--format=format`: Seleciona o formato para a saída. *`format`* pode ser um dos seguintes:

`p` `plain` :   Escreva a saída como arquivos simples, com o mesmo layout do diretório de dados do servidor de origem e espaços de tabela. Quando o clúster não tiver espaços de tabela adicionais, o banco de dados inteiro será colocado no diretório de destino. Se o clúster contiver espaços de tabela adicionais, o diretório principal de dados será colocado no diretório de destino, mas todos os outros espaços de tabela serão colocados no mesmo caminho absoluto que têm no servidor de origem. (Consulte `--tablespace-mapping` para alterar isso.)

Este é o formato padrão.

`t` `tar` :   Escreva a saída como arquivos tar no diretório de destino. O conteúdo do diretório de dados principal será escrito em um arquivo denominado `base.tar`, e cada outro espaço de tabela será escrito em um arquivo tar separado, denominado conforme o OID do espaço de tabela.

Se o diretório de destino for especificado como `-` (ponto e vírgula), o conteúdo do tar será escrito na saída padrão, adequado para ser redirecionado para (por exemplo) gzip. Isso só é permitido se o clúster não tiver tabelas adicionais e o streaming WAL não for usado.

`-i old_manifest_file` `--incremental=old_manifest_file`: Realiza um [backup incremental](continuous-archiving.md#BACKUP-INCREMENTAL-BACKUP "25.3.3. Making an Incremental Backup"). O manifesto de backup para o backup de referência deve ser fornecido e será carregado no servidor, que responderá enviando o backup incremental solicitado.

`-R` `--write-recovery-conf`: Cria um arquivo [`standby.signal`](warm-standby.md#FILE-STANDBY-SIGNAL) e anexa as configurações de conexão ao arquivo `postgresql.auto.conf` no diretório de destino (ou dentro do arquivo de arquivo de base quando usando o formato tar). Isso facilita a configuração de um servidor de espera usando os resultados do backup.

O arquivo `postgresql.auto.conf` registrará as configurações de conexão e, se especificado, o slot de replicação que o pg_basebackup está usando, para que a replicação em fluxo e a [sincronização do slot de replicação lógica](logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION "47.2.3. Replication Slot Synchronization") usem as mesmas configurações mais tarde. O nome do banco de dados será registrado apenas se o nome do banco de dados foi especificado explicitamente na string de conexão ou na [variável de ambiente](libpq-envars.md "32.15. Environment Variables").

`-t target` `--target=target`: Instrua o servidor sobre o local onde deve ser colocado o backup básico. O alvo padrão é `client`, que especifica que o backup deve ser enviado para a máquina onde o pg_basebackup está sendo executado. Se o alvo for definido como `server:/some/path`, o backup será armazenado na máquina onde o servidor está sendo executado no diretório `/some/path`. Armazenar um backup no servidor requer privilégios de superusuário ou ter privilégios da função `pg_write_server_files`. Se o alvo for definido como `blackhole`, o conteúdo será descartado e não será armazenado em nenhum lugar. Isso deve ser usado apenas para fins de teste, pois você não terá um backup real.

Como o streaming WAL é implementado pelo pg_basebackup e não pelo servidor, essa opção não pode ser usada juntamente com `-Xstream`. Como esse é o padrão, quando essa opção é especificada, você também deve especificar `-Xfetch` ou `-Xnone`.

`-T olddir=newdir`: Recoloca o tablespace no diretório *`olddir`* para *`newdir`* durante o backup. Para ser eficaz, *`olddir`* deve corresponder exatamente à especificação do caminho do tablespace conforme definido no servidor de origem. (Mas não é um erro se não houver tablespace em *`olddir`* no servidor de origem.) Enquanto isso, *`newdir`* é um diretório no sistema de arquivos do host receptor. Assim como o diretório principal de destino, *`newdir`* não precisa existir já, mas se existir, deve estar vazio. Tanto *`olddir`* quanto *`newdir`* devem ser caminhos absolutos. Se qualquer um dos caminhos precisar conter um sinal de igual (`=`), preceda-o com uma barra invertida. Esta opção pode ser especificada várias vezes para vários tablespaces.

Se um espaço de tabela for realocado dessa maneira, os links simbólicos dentro do diretório de dados principal são atualizados para apontar para o novo local. Assim, o novo diretório de dados está pronto para ser usado para uma nova instância do servidor com todos os espaços de tabela nos locais atualizados.

Atualmente, essa opção só funciona com o formato de saída simples; ela é ignorada se o formato tar for selecionado.

`--waldir=waldir`: Define o diretório onde os arquivos WAL (log de antecipação de escrita) serão escritos. Por padrão, os arquivos WAL serão colocados no subdiretório `pg_wal` do diretório de destino, mas essa opção pode ser usada para colocá-los em outro lugar. *`waldir`* deve ser um caminho absoluto. Assim como o diretório principal de destino, *`waldir`* não precisa existir já, mas se existir, ele deve estar vazio. Esta opção só pode ser especificada quando o backup estiver no formato simples.

`-X method` `--wal-method=method`: Inclui os arquivos WAL (log de pré-escrita) necessários no backup. Isso incluirá todos os logs de pré-escrita gerados durante o backup. A menos que o método `none` seja especificado, é possível iniciar um postmaster no diretório de destino sem a necessidade de consultar o arquivo WAL, tornando assim a saída um backup completamente autônomo.

Os seguintes *`method`* para coletar logs de pré-escrita são suportados:

`n` `none` :   Não inclua logs de pré-escrita no backup.

`f` `fetch` :   Os arquivos de registro de pré-escrita são coletados no final do backup. Portanto, é necessário que o parâmetro [wal_keep_size](runtime-config-replication.md#GUC-WAL-KEEP-SIZE) do servidor de origem seja configurado com tamanho suficientemente alto para que os dados de registro necessários não sejam removidos antes do final do backup. Se os dados de registro necessários tiverem sido reciclados antes do momento de transferência, o backup falhará e será inutilizável.

Quando o formato tar é usado, os arquivos de registro de pré-escrita serão incluídos no arquivo `base.tar`.

`s` `stream` :   Escreva dados de log de pré-escrita enquanto o backup está sendo realizado. Esse método abrirá uma segunda conexão com o servidor e começará a transmitir o log de pré-escrita em paralelo enquanto o backup é executado. Portanto, isso exigirá duas conexões de replicação, não apenas uma. Desde que o cliente possa acompanhar os dados do log de pré-escrita, usando esse método não é necessário salvar logs de pré-escrita adicionais no servidor de origem.

Quando o formato tar é usado, os arquivos de registro de pré-escrita serão escritos em um arquivo separado denominado `pg_wal.tar` (se o servidor for uma versão anterior a 10, o arquivo será denominado `pg_xlog.tar`).

Esse valor é o padrão.

`-z` `--gzip`: Habilita a compressão gzip do arquivo tar, com o nível de compressão padrão. A compressão está disponível apenas quando se usa o formato tar, e o sufixo `.gz` será adicionado automaticamente a todos os nomes de arquivo tar.

`-Z level` `-Z [{client|server}-]method[:detail]` `--compress=level` `--compress=[{client|server}-]method[:detail]`: Solicita compressão do backup. Se `client` ou `server` for incluído, especifica onde a compressão deve ser realizada. A compressão no servidor reduzirá a largura de banda de transferência, mas aumentará o consumo de CPU do servidor. O padrão é `client`, exceto quando `--target` é usado. Nesse caso, o backup não está sendo enviado ao cliente, então apenas a compressão do servidor é sensível. Quando `-Xstream`, que é o padrão, é usado, a compressão do lado do servidor não será aplicada ao WAL. Para comprimir o WAL, use compressão do lado do cliente, ou especifique `-Xfetch`.

O método de compressão pode ser definido como `gzip`, `lz4`, `zstd`, `none` para sem compressão ou um número inteiro (sem compressão se for 0, `gzip` se for maior que 0). Uma string de detalhes de compressão pode ser especificada opcionalmente. Se a string de detalhes for um número inteiro, ela especifica o nível de compressão. Caso contrário, deve ser uma lista de itens separados por vírgula, cada um na forma *`keyword`* ou *`keyword=value`*. Atualmente, as palavras-chave suportadas são `level`, `long` e `workers`. A string de detalhes não pode ser usada quando o método de compressão é especificado como um número inteiro simples.

Se nenhum nível de compressão for especificado, o nível de compressão padrão será usado. Se apenas um nível for especificado sem mencionar um algoritmo, a compressão `gzip` será usada se o nível for maior que 0, e não será usada compressão se o nível for 0.

Quando o formato tar é usado com `gzip`, `lz4` ou `zstd`, o sufixo `.gz`, `.lz4` ou `.zst`, respectivamente, será adicionado automaticamente a todos os nomes de arquivo tar. Quando o formato simples é usado, a compressão do lado do cliente pode não ser especificada, mas ainda é possível solicitar compressão do lado do servidor. Se isso for feito, o servidor comprimirá o backup para transmissão, e o cliente o descomprimirá e extrairá.

Quando esta opção é usada em combinação com `-Xstream`, `pg_wal.tar` será comprimido usando `gzip` se a compressão gzip do lado do cliente for selecionada, mas não será comprimido se qualquer outro algoritmo de compressão for selecionado, ou se a compressão do lado do servidor for selecionada.

As opções de linha de comando a seguir controlam a geração do backup e a invocação do programa:

`-c {fast|spread}` `--checkpoint={fast|spread}`: Define o modo de verificação como rápido (imediato) ou espalhado (padrão) (consulte [Seção 25.3.4][(continuous-archiving.md#BACKUP-LOWLEVEL-BASE-BACKUP "25.3.4. Making a Base Backup Using the Low Level API")]).

`-C` `--create-slot`: Especifica que o slot de replicação nomeado pela opção `--slot` deve ser criado antes de iniciar o backup. Um erro é exibido se o slot já existir.

`-l label` `--label=label`: Define o rótulo para o backup. Se não for especificado, será usado um valor padrão de “[[`pg_basebackup base backup`]”.

`-n` `--no-clean`: Por padrão, quando o `pg_basebackup` é interrompido com um erro, ele remove quaisquer diretórios que ele possa ter criado antes de descobrir que não pode completar o trabalho (por exemplo, o diretório de destino e o diretório de log de pré-escrita). Esta opção inibe a limpeza e, portanto, é útil para depuração.

Observe que os diretórios dos tablespace também não são limpos.

`-N` `--no-sync`: Por padrão, `pg_basebackup` aguardará que todos os arquivos sejam escritos com segurança no disco. Esta opção faz com que `pg_basebackup` retorne sem aguardar, o que é mais rápido, mas significa que um posterior falha do sistema operacional pode deixar o backup de base corrompido. Geralmente, esta opção é útil para testes, mas não deve ser usada ao criar uma instalação de produção.

`-P` `--progress`: Habilita o relatório de progresso. Ao ativar essa opção, será entregue um relatório aproximado de progresso durante o backup. Como o banco de dados pode mudar durante o backup, isso é apenas uma aproximação e pode não terminar exatamente em `100%`. Em particular, quando o log WAL é incluído no backup, o volume total de dados não pode ser estimado antecipadamente, e, nesse caso, o tamanho alvo estimado aumentará uma vez que passe a estimativa total sem WAL.

`-r rate` `--max-rate=rate`: Define a taxa de transferência máxima na qual os dados são coletados do servidor fonte. Isso pode ser útil para limitar o impacto do pg_basebackup no servidor. Os valores são em kilobytes por segundo. Use um sufixo de `M` para indicar megabytes por segundo. Um sufixo de `k` também é aceito e não tem efeito. Os valores válidos estão entre 32 kilobytes por segundo e 1024 megabytes por segundo.

Essa opção sempre afeta a transferência do diretório de dados. A transferência dos arquivos WAL só é afetada se o método de coleta for `fetch`.

`-S slotname` `--slot=slotname`: Esta opção só pode ser usada em conjunto com `-X stream`. Ela faz com que o streaming WAL use o intervalo de replicação especificado. Se o backup de base for destinado a ser usado como um standby de replicação de streaming usando um intervalo de replicação, o standby deve, em seguida, usar o mesmo nome do intervalo de replicação que [primary_slot_name](runtime-config-replication.md#GUC-PRIMARY-SLOT-NAME). Isso garante que o servidor primário não remova nenhum dado WAL necessário no tempo entre o fim do backup de base e o início da replicação de streaming no novo standby.

O intervalo de replicação especificado deve existir, a menos que a opção `-C` também seja usada.

Se esta opção não for especificada e o servidor suportar slots de replicação temporários (versão 10 e posterior), então um slot de replicação temporário será usado automaticamente para o streaming WAL.

`--sync-method=method`: Quando configurado para `fsync`, que é o padrão, `pg_basebackup` abrirá e sincronizará recursivamente todos os arquivos no diretório de backup. Quando o formato simples é usado, a busca por arquivos seguirá links simbólicos para o diretório WAL e cada espaço de tabela configurado.

Em Linux, `syncfs` pode ser usado para pedir ao sistema operacional que sincronize todo o sistema de arquivos que contém o diretório de backup. Quando o formato simples é usado, `pg_basebackup` também sincronizará os sistemas de arquivos que contêm os arquivos WAL e cada espaço de tabela. Consulte [recovery_init_sync_method][(runtime-config-error-handling.md#GUC-RECOVERY-INIT-SYNC-METHOD)] para obter informações sobre as advertências a serem consideradas ao usar `syncfs`.

Esta opção não tem efeito quando o `--no-sync` é usado.

`-v` `--verbose`: Habilita o modo verbose. Exibirá alguns passos extras durante o início e o término, além de mostrar o nome exato do arquivo que está sendo processado, se o relatório de progresso também estiver habilitado.

`--manifest-checksums=algorithm`: Especifica o algoritmo de verificação de checksum que deve ser aplicado a cada arquivo incluído no manifesto de backup. Atualmente, os algoritmos disponíveis são `NONE`, `CRC32C`, `SHA224`, `SHA256`, `SHA384` e `SHA512`. O padrão é `CRC32C`.

Se `NONE` for selecionado, o manifesto de backup não conterá nenhum checksum. Caso contrário, ele conterá um checksum de cada arquivo no backup usando o algoritmo especificado. Além disso, o manifesto sempre conterá um checksum `SHA256` dos próprios conteúdos. Os algoritmos `SHA` são significativamente mais intensivos em CPU do que `CRC32C`, portanto, selecionar um deles pode aumentar o tempo necessário para completar o backup.

Usar uma função de hash SHA fornece um resumo criptográficamente seguro de cada arquivo para os usuários que desejam verificar se o backup não foi manipulado, enquanto o algoritmo CRC-32C fornece um checksum que é muito mais rápido de calcular; é bom para detectar erros devido a mudanças acidentais, mas não é resistente a modificações maliciosas. Note que, para ser útil contra um adversário que tem acesso ao backup, o manifesto do backup precisaria ser armazenado de forma segura em outro lugar ou, de outra forma, verificado para não ter sido modificado desde que o backup foi feito.

[pg_verifybackup](app-pgverifybackup.md "pg_verifybackup") pode ser usado para verificar a integridade de um backup em relação ao manifesto do backup.

`--manifest-force-encode`: Força todos os nomes de arquivo no manifesto de backup a serem codificados em hexadecimal. Se esta opção não for especificada, apenas os nomes de arquivo que não são UTF8 serão codificados em hexadecimal. Esta opção é principalmente destinada a testar que as ferramentas que leem corretamente um arquivo de manifesto de backup lidam com este caso.

`--no-estimate-size`: Previne o servidor de estimar a quantidade total de dados de backup que serão transmitidos, resultando na coluna `backup_total` na visualização `pg_stat_progress_basebackup` sempre sendo `NULL`.

Sem essa opção, o backup começará enumerando o tamanho de todo o banco de dados e, em seguida, voltará e enviará os conteúdos reais. Isso pode fazer com que o backup demore um pouco mais, e, em particular, levará mais tempo até que os primeiros dados sejam enviados. Essa opção é útil para evitar esse tempo de estimativa se for muito longo.

Esta opção não é permitida ao usar `--progress`.

`--no-manifest`: Desabilita a geração de um manifesto de backup. Se esta opção não for especificada, o servidor gerará e enviará um manifesto de backup que pode ser verificado usando [pg_verifybackup][(app-pgverifybackup.md "pg_verifybackup")]. O manifesto é uma lista de todos os arquivos presentes no backup, com exceção de quaisquer arquivos WAL que possam ser incluídos. Ele também armazena o tamanho, o horário de última modificação e um checksum opcional para cada arquivo.

`--no-slot`: Previne a criação de um slot de replicação temporário para o backup.

Por padrão, se a opção de streaming de logs for selecionada, mas não houver nome de slot fornecido com a opção `-S`, então um slot de replicação temporário será criado (se suportado pelo servidor de origem).

O principal objetivo desta opção é permitir a realização de um backup de base quando o servidor não tiver slots de replicação livres. Usar um slot de replicação é quase sempre a preferência, pois evita que o WAL necessário seja removido pelo servidor durante o backup.

`--no-verify-checksums`: Desabilita a verificação de checksums, se eles estiverem habilitados no servidor a partir do qual a cópia de segurança básica é feita.

Por padrão, os checksums são verificados e falhas no checksum resultarão em um status de saída não nulo. No entanto, o backup de base não será removido nesse caso, pois se a opção `--no-clean` tivesse sido usada. Falhas na verificação do checksum também serão relatadas na visão `pg_stat_database`(monitoring-stats.md#MONITORING-PG-STAT-DATABASE-VIEW "27.2.17. pg_stat_database").

As opções de linha de comando a seguir controlam a conexão com o servidor de origem:

`-d connstr` `--dbname=connstr`: Especifica os parâmetros usados para se conectar ao servidor, como uma [string de conexão](libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings"); esses parâmetros substituirão quaisquer opções de linha de comando conflitantes.

Essa opção é chamada `--dbname` para garantir a consistência com outras aplicações do cliente, mas, como o pg_basebackup não se conecta a nenhum banco de dados específico no clúster, qualquer nome de banco de dados incluído na string de conexão será ignorado pelo servidor. No entanto, um nome de banco de dados fornecido dessa maneira substitui o nome de banco de dados padrão (`replication`) para fins de busca da senha da conexão de replicação em `~/.pgpass`. Da mesma forma, o middleware ou proxies utilizados na conexão com o PostgreSQL podem utilizar o nome para fins como roteamento de conexão. O nome do banco de dados também pode ser utilizado pelo [sincronização de slot de replicação lógica][(logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION "47.2.3. Replication Slot Synchronization")].

`-h host`: Especifica o nome do host da máquina na qual o servidor está sendo executado. Se o valor começar com uma barra, ele é usado como o diretório para uma conexão de soquete de domínio Unix. O padrão é tomado da variável de ambiente `PGHOST`, se definida, caso contrário, uma conexão de soquete de domínio Unix é tentada.

`-p port` `--port=port`: Especifica a porta TCP ou a extensão de arquivo de soquete de domínio Unix local em que o servidor está ouvindo conexões. Tem como padrão a variável de ambiente `PGPORT`, se definida, ou um padrão incorporado.

`-s interval` `--status-interval=interval`: Especifica o número de segundos entre pacotes de status enviados de volta ao servidor de origem. Valores menores permitem um monitoramento mais preciso do progresso do backup a partir do servidor. Um valor de zero desativa as atualizações periódicas de status completamente, embora uma atualização ainda seja enviada quando solicitada pelo servidor, para evitar desconexões baseadas em tempo de espera. O valor padrão é de 10 segundos.

`-U username` `--username=username`: Especifica o nome do usuário para se conectar.

`-w` `--no-password`: Evita a emissão de um prompt de senha. Se o servidor exigir autenticação por senha e uma senha não estiver disponível por outros meios, como um arquivo `.pgpass`, a tentativa de conexão falhará. Esta opção pode ser útil em trabalhos em lote e scripts onde não há usuário presente para inserir uma senha.

`-W` `--password`: Força o pg_basebackup a solicitar uma senha antes de se conectar ao servidor de origem.

Essa opção nunca é essencial, pois o pg_basebackup solicitará automaticamente uma senha se o servidor exigir autenticação por senha. No entanto, o pg_basebackup desperdiçará uma tentativa de conexão descobrindo que o servidor deseja uma senha. Em alguns casos, vale a pena digitar `-W` para evitar a tentativa extra de conexão.

Outras opções também estão disponíveis:

`-V` `--version`: Imprime a versão do pg_basebackup e encerra.

`-?` `--help`: Mostra ajuda sobre os argumentos da linha de comando do comando pg_basebackup e sai.

## Meio Ambiente

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, utiliza as variáveis de ambiente suportadas pelo libpq (consulte a Seção 32.15 [(libpq-envars.md "32.15. Environment Variables")]).

A variável de ambiente `PG_COLOR` especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

## Notas

No início do backup, é necessário realizar um ponto de verificação no servidor de origem. Isso pode levar algum tempo (especialmente se a opção `--checkpoint=fast` não for usada), durante o qual o pg_basebackup parecerá estar parado.

O backup incluirá todos os arquivos no diretório de dados e nos espaços de tabela, incluindo os arquivos de configuração e quaisquer arquivos adicionais colocados no diretório por terceiros, exceto certos arquivos temporários gerenciados pelo PostgreSQL e arquivos do sistema operacional. Mas apenas arquivos e diretórios regulares são copiados, exceto que os links simbólicos usados para espaços de tabela são preservados. Os links simbólicos que apontam para determinados diretórios conhecidos pelo PostgreSQL são copiados como diretórios vazios. Outros links simbólicos e arquivos de dispositivo especiais são ignorados. Consulte [Seção 54.4] para obter os detalhes precisos.

Em formato simples, os espaços de tabela serão protegidos para o mesmo caminho que eles têm no servidor de origem, a menos que a opção `--tablespace-mapping` seja usada. Sem essa opção, executar um backup em formato simples na mesma máquina do servidor não funcionará se os espaços de tabela estiverem em uso, porque o backup teria que ser escrito nas mesmas localizações de diretório que os espaços de tabela originais.

Quando o formato tar é usado, é responsabilidade do usuário descompactar cada arquivo tar antes de iniciar um servidor PostgreSQL que utilize os dados. Se houver espaços de tabela adicionais, os arquivos tar para eles precisam ser descompactos nos locais corretos. Neste caso, os links simbólicos para esses espaços de tabela serão criados pelo servidor de acordo com o conteúdo do arquivo `tablespace_map` que está incluído no arquivo `base.tar`.

O pg_basebackup funciona com servidores da mesma versão principal ou versões anteriores, até a 9.1. No entanto, o modo de streaming WAL (`-X stream`) só funciona com a versão do servidor 9.3 e posterior, o formato tar (`--format=tar`) só funciona com a versão do servidor 9.5 e posterior, e o backup incremental (`--incremental`) só funciona com a versão do servidor 17 e posterior.

O pg_basebackup preservará as permissões de grupo dos arquivos de dados se as permissões de grupo estiverem habilitadas no clúster de origem.

## Exemplos

Para criar um backup básico do servidor em `mydbserver` e armazená-lo no diretório local `/usr/local/pgsql/data`:

```
$ pg_basebackup -h mydbserver -D /usr/local/pgsql/data
```

Para criar um backup do servidor local com um arquivo tar compactado para cada espaço de tabela, e armazená-lo no diretório `backup`, mostrando um relatório de progresso durante a execução:

```
$ pg_basebackup -D backup -Ft -z -P
```

Para criar um backup de um banco de dados local de espaço único e comp comprimí-lo com bzip2:

```
$ pg_basebackup -D - -Ft -X fetch | bzip2 > backup.tar.bz2
```

(Esse comando falhará se houver vários tablespaces no banco de dados.)

Para criar uma cópia de segurança de um banco de dados local onde o espaço de tabelas em `/opt/ts` é realocado em `./backup/ts`:

```
$ pg_basebackup -D backup/data -T /opt/ts=$(pwd)/backup/ts
```

Para criar um backup do servidor local com um arquivo tar para cada espaço de tabela comprimido com gzip no nível 9, armazenado no diretório `backup`:

```
$ pg_basebackup -D backup -Ft --compress=gzip:9
```

## Veja também

[pg_dump](app-pgdump.md "pg_dump"), [Seção 27.4.6](progress-reporting.md#BASEBACKUP-PROGRESS-REPORTING "27.4.6. Base Backup Progress Reporting")