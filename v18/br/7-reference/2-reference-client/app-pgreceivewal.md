## pg_receivewal

pg_receivewal — fluxo de registros de pré-escrita de dados de um servidor PostgreSQL

## Sinopse

`pg_receivewal` [*`option`*...]

## Descrição

O pg_receivewal é usado para transmitir o log de pré-escrita de um cluster PostgreSQL em execução. O log de pré-escrita é transmitido usando o protocolo de replicação de streaming e é escrito em um diretório local de arquivos. Esse diretório pode ser usado como local de arquivo para realizar uma restauração usando recuperação em ponto no tempo (consulte [Seção 25.3](continuous-archiving.md)).

pg_receivewal transmite o log de pré-escrita em tempo real à medida que é gerado no servidor e não espera que os segmentos sejam concluídos, como o [archive_command](runtime-config-wal.md#GUC-ARCHIVE-COMMAND) e o [archive_library](runtime-config-wal.md#GUC-ARCHIVE-LIBRARY) fazem. Por essa razão, não é necessário definir [archive_timeout](runtime-config-wal.md#GUC-ARCHIVE-TIMEOUT) ao usar pg_receivewal.

Ao contrário do receptor WAL de um servidor de espera PostgreSQL, o pg_receivewal, por padrão, esvazia os dados do WAL apenas quando um arquivo WAL é fechado. A opção `--synchronous` deve ser especificada para esvaziar os dados do WAL em tempo real. Como o pg_receivewal não aplica o WAL, você não deve permitir que ele se torne um standby síncrono quando [síncrono_commit](runtime-config-wal.md#GUC-SYNCHRONOUS-COMMIT) é igual a `remote_apply`. Se isso ocorrer, ele parecerá ser um standby que nunca se atualiza e causará bloqueio dos commits de transação. Para evitar isso, você deve configurar um valor apropriado para [síncrono_standby_names](runtime-config-replication.md#GUC-SYNCHRONOUS-STANDBY-NAMES), ou especificar `application_name` para o pg_receivewal que não corresponda a ele, ou alterar o valor de `synchronous_commit` para algo diferente de `remote_apply`.

O log de pré-escrita é transmitido através de uma conexão regular do PostgreSQL e utiliza o protocolo de replicação. A conexão deve ser feita com um usuário que tenha permissões `REPLICATION` (consulte [Seção 21.2](role-attributes.md)) ou um superusuário, e `pg_hba.conf` deve permitir a conexão de replicação. O servidor também deve ser configurado com [max_wal_senders](runtime-config-replication.md#GUC-MAX-WAL-SENDERS) definido o suficiente para deixar pelo menos uma sessão disponível para o fluxo.

O ponto de partida do streaming de log de escrita prévia é calculado quando o pg_receivewal começa:

1. Primeiro, faça uma varredura no diretório onde os arquivos de segmento WAL são escritos e encontre o arquivo de segmento mais recente concluído, usando como ponto de partida o início do próximo arquivo de segmento WAL.
2. Se um ponto de partida não puder ser calculado com o método anterior e se um intervalo de replicação for usado, um comando extra `READ_REPLICATION_SLOT` é emitido para recuperar o `restart_lsn` do intervalo para usar como ponto de partida. Esta opção só está disponível quando os logs de escrita antecipada são transmitidos a partir do PostgreSQL 15 e em versões posteriores.
3. Se um ponto de partida não puder ser calculado com o método anterior, o último local de esvaziamento do WAL é usado conforme relatado pelo servidor a partir de um comando `IDENTIFY_SYSTEM`.

Se a conexão for perdida ou se não puder ser estabelecida inicialmente, com um erro não fatal, o pg_receivewal tentará reconectar indefinidamente e restabelecer o streaming o mais rápido possível. Para evitar esse comportamento, use o parâmetro `-n`.

Na ausência de erros fatais, o pg_receivewal será executado até ser encerrado pelo sinal SIGINT (**Controle** + **C**) ou SIGTERM.

## Opções

`-D directory` `--directory=directory`: Diretório para escrever a saída.

Este parâmetro é necessário.

`-E lsn` `--endpos=lsn`: Parar automaticamente a replicação e sair com o status de saída normal 0 quando o recebimento atingir o LSN especificado.

Se houver um registro com LSN exatamente igual a *`lsn`*, o registro será processado.

`--if-not-exists`: Não erre quando o `--create-slot` é especificado e um slot com o nome especificado já existe.

`-n` `--no-loop`: Não faça um loop em erros de conexão. Em vez disso, saia imediatamente com um erro.

`--no-sync`: Esta opção faz com que `pg_receivewal` não force a eliminação dos dados do WAL para o disco. Isso é mais rápido, mas significa que um posterior falha do sistema operacional pode deixar os segmentos do WAL corrompidos. Geralmente, esta opção é útil para testes, mas não deve ser usada ao realizar arquivamento do WAL em uma implantação de produção.

Esta opção é incompatível com `--synchronous`.

`-s interval` `--status-interval=interval`: Especifica o número de segundos entre os pacotes de status enviados de volta ao servidor. Isso permite uma monitorização mais fácil do progresso a partir do servidor. Um valor de zero desativa as atualizações periódicas de status completamente, embora uma atualização ainda seja enviada quando solicitada pelo servidor, para evitar a desconexão por tempo excedido. O valor padrão é de 10 segundos.

`-S slotname` `--slot=slotname`: Requer que o pg_receivewal use um slot de replicação existente (consulte [Seção 26.2.6](warm-standby.md#STREAMING-REPLICATION-SLOTS)). Quando esta opção é usada, o pg_receivewal informará ao servidor uma posição de esvaziamento, indicando quando cada segmento foi sincronizado com o disco, para que o servidor possa remover esse segmento se não for necessário.

Quando o cliente de replicação do pg_receivewal é configurado no servidor como um standby síncrono, então o uso de um slot de replicação informará ao servidor a posição de esvaziamento, mas apenas quando um arquivo WAL é fechado. Portanto, essa configuração fará com que as transações no primário esperem por um longo tempo e, efetivamente, não funcionem de forma satisfatória. A opção `--synchronous` (veja abaixo) deve ser especificada adicionalmente para que isso funcione corretamente.

`--synchronous`: Limpe os dados WAL no disco imediatamente após recebê-los. Além disso, envie um pacote de status de volta ao servidor imediatamente após a limpeza, independentemente de `--status-interval`.

Essa opção deve ser especificada se o cliente de replicação do pg_receivewal estiver configurado no servidor como um standby síncrono, para garantir que o feedback oportuno seja enviado ao servidor.

`-v` `--verbose`: Habilita o modo verbose.

`-Z level` `-Z method[:detail]` `--compress=level` `--compress=method[:detail]`: Habilita a compressão de logs de pré-escrita.

O método de compressão pode ser definido como `gzip`, `lz4` (se o PostgreSQL foi compilado com `--with-lz4`) ou `none` para sem compressão. Uma string de detalhe de compressão pode ser especificada opcionalmente. Se a string de detalhe for um número inteiro, ela especifica o nível de compressão. Caso contrário, deve ser uma lista de itens separados por vírgula, cada um na forma *`keyword`* ou *`keyword=value`*. Atualmente, a única palavra-chave compatível é `level`.

Se nenhum nível de compressão for especificado, o nível de compressão padrão será usado. Se apenas um nível for especificado sem mencionar um algoritmo, a compressão `gzip` será usada se o nível for maior que 0, e não será usada compressão se o nível for 0.

O sufixo `.gz` será adicionado automaticamente a todos os nomes de arquivo ao usar `gzip`, e o sufixo `.lz4` é adicionado ao usar `lz4`.

As opções de linha de comando a seguir controlam os parâmetros de conexão do banco de dados.

`-d connstr`: Especifica os parâmetros usados para se conectar ao servidor, como uma [string de conexão](libpq-connect.md#LIBPQ-CONNSTRING); esses parâmetros substituirão quaisquer opções de linha de comando conflitantes.

Essa opção é chamada `--dbname` para manter a consistência com outras aplicações do cliente, mas, como o pg_receivewal não se conecta a nenhum banco de dados específico no clúster, qualquer nome de banco de dados incluído na string de conexão será ignorado pelo servidor. No entanto, um nome de banco de dados fornecido dessa maneira substitui o nome de banco de dados padrão (`replication`) para fins de busca da senha da conexão de replicação em `~/.pgpass`. Da mesma forma, o middleware ou proxies utilizados na conexão com o PostgreSQL podem utilizar o nome para fins como roteamento de conexão.

`-h host` `--host=host`: Especifica o nome do host da máquina na qual o servidor está sendo executado. Se o valor começar com uma barra, ele é usado como o diretório para o socket de domínio Unix. O padrão é tomado da variável de ambiente `PGHOST`, se definida, caso contrário, uma conexão de socket de domínio Unix é tentada.

`-p port` `--port=port`: Especifica a porta TCP ou a extensão de arquivo de soquete de domínio Unix local em que o servidor está ouvindo conexões. Tem como padrão a variável de ambiente `PGPORT`, se definida, ou um padrão incorporado.

`-U username` `--username=username`: Nome do usuário para se conectar como.

`-w` `--no-password`: Nunca emita um prompt de senha. Se o servidor exigir autenticação por senha e uma senha não estiver disponível por outros meios, como um arquivo `.pgpass`, a tentativa de conexão falhará. Esta opção pode ser útil em trabalhos em lote e scripts onde nenhum usuário está presente para inserir uma senha.

`-W` `--password`: Forçar o pg_receivewal a solicitar uma senha antes de se conectar a um banco de dados.

Essa opção nunca é essencial, pois o pg_receivewal solicitará automaticamente uma senha se o servidor exigir autenticação por senha. No entanto, o pg_receivewal desperdiçará uma tentativa de conexão descobrindo que o servidor deseja uma senha. Em alguns casos, vale a pena digitar `-W` para evitar a tentativa extra de conexão.

O pg_receivewal pode realizar uma das duas ações a seguir para controlar os slots de replicação física:

`--create-slot`: Crie um novo slot de replicação física com o nome especificado em `--slot`, e então saia.

`--drop-slot`: Descarte o slot de replicação com o nome especificado em `--slot`, e então saia.

Outras opções também estão disponíveis:

`-V` `--version`: Imprimir a versão do pg_receivewal e sair.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando pg_receivewal e sair.

## Status de saída

pg_receivewal sairá com status 0 quando encerrado pelo sinal SIGINT ou SIGTERM. (Essa é a maneira normal de encerrá-lo. Portanto, não é um erro.) Para erros fatais ou outros sinais, o status de saída será diferente de zero.

## Meio Ambiente

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, utiliza as variáveis de ambiente suportadas pelo libpq (consulte a [Seção 32.15](libpq-envars.md)).

A variável de ambiente `PG_COLOR` especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

## Notas

Ao usar pg_receivewal em vez de [archive_command](runtime-config-wal.md#GUC-ARCHIVE-COMMAND) ou [archive_library](runtime-config-wal.md#GUC-ARCHIVE-LIBRARY) como o principal método de backup do WAL, é altamente recomendável usar slots de replicação. Caso contrário, o servidor pode reciclar ou remover arquivos de log de antecipação antes de serem protegidos, porque não tem nenhuma informação, seja do [archive_command](runtime-config-wal.md#GUC-ARCHIVE-COMMAND) ou [archive_library](runtime-config-wal.md#GUC-ARCHIVE-LIBRARY) ou dos slots de replicação, sobre o quão longe o fluxo do WAL foi arquivado. No entanto, note que um slot de replicação ocupará o espaço em disco do servidor se o receptor não acompanhar a obtenção dos dados do WAL.

pg_receivewal preservará as permissões de grupo nos arquivos WAL recebidos se as permissões de grupo estiverem habilitadas no clúster de origem.

## Exemplos

Para transmitir o registro prévio de escrita do servidor em `mydbserver` e armazená-lo no diretório local `/usr/local/pgsql/archive`:

```
$ pg_receivewal -h mydbserver -D /usr/local/pgsql/archive
```

## Veja também

[pg_basebackup](app-pgbasebackup.md "pg_basebackup")
