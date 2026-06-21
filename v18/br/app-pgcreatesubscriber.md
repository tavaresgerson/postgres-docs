## pg_createsubscriber

pg_createsubscriber — converter uma replica física em uma nova replica lógica

## Sinopse

`pg_createsubscriber` [*`option`*...] { `-d` | `--database` }*`dbname`* { `-D` | `--pgdata` }*`datadir`* { `-P` | `--publisher-server` }*`connstr`*

## Descrição

pg_createsubscriber cria uma nova replica lógica a partir de um servidor de espera físico. Todas as tabelas no banco de dados especificado estão incluídas no [replicação lógica][(logical-replication.md "Chapter 29. Logical Replication")] configuração. Um par de objetos de publicação e subscrição são criados para cada banco de dados. Deve ser executado no servidor alvo.

Após uma execução bem-sucedida, o estado do servidor alvo é análogo a uma configuração de replicação lógica fresca. A principal diferença entre a configuração de replicação lógica e o pg_createsubscriber é a forma como a sincronização dos dados é feita. O pg_createsubscriber não copia os dados iniciais da tabela. Ele realiza apenas a fase de sincronização, que garante que cada tabela seja trazida a um estado sincronizado.

pg_createsubscriber é voltado para grandes sistemas de banco de dados, pois, na configuração de replicação lógica, a maior parte do tempo é gasto fazendo a cópia inicial dos dados. Além disso, um efeito colateral desse longo tempo gasto na sincronização dos dados geralmente é uma grande quantidade de alterações a serem aplicadas (que foram produzidas durante a cópia inicial dos dados), o que aumenta ainda mais o tempo em que a replica lógica estará disponível. Para bancos de dados menores, é recomendável configurar a replicação lógica com sincronização de dados inicial. Para detalhes, consulte a opção `CREATE SUBSCRIPTION` [`copy_data`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-COPY-DATA).

## Opções

pg_createsubscriber aceita os seguintes argumentos de linha de comando:

`-a` `--all`: Crie uma assinatura por banco de dados no servidor de destino. As exceções são bancos de dados de modelo e bancos de dados que não permitem conexões. Para descobrir a lista de todos os bancos de dados, conecte-se ao servidor de origem usando o nome do banco de dados especificado na cadeia de conexão `--publisher-server`, ou, se não for especificado, o banco de dados `postgres` será usado, ou se este não existir, será usado `template1`. Nomes automaticamente gerados para assinaturas, publicações e faixas de replicação são usados quando esta opção é especificada. Esta opção não pode ser usada juntamente com `--database`, `--publication`, `--replication-slot` ou `--subscription`.

`-d dbname` `--database=dbname`: O nome do banco de dados no qual deseja criar uma assinatura. Múltiplos bancos de dados podem ser selecionados escrevendo múltiplos interruptores `-d`. Esta opção não pode ser usada juntamente com `-a`. Se a opção `-d` não for fornecida, o nome do banco de dados será obtido a partir da opção `-P`. Se o nome do banco de dados não for especificado na opção `-d`, ou na opção `-P`, e a opção `-a` não for especificada, um erro será relatado.

`-D directory` `--pgdata=directory`: O diretório de destino que contém um diretório de cluster de uma replica física.

`-n` `--dry-run`: Faça tudo, exceto modificar o diretório de destino.

`-p port` `--subscriber-port=port`: O número de porta no qual o servidor alvo está ouvindo conexões. Por padrão, o servidor alvo é executado na porta 50432 para evitar conexões não intencionais do cliente.

`-P connstr` `--publisher-server=connstr`: A cadeia de conexão ao editor. Para detalhes, consulte [Seção 32.1.1](libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings").

`-s dir` `--socketdir=dir`: O diretório a ser usado para sockets do postmaster no servidor alvo. O padrão é o diretório atual.

`-t seconds` `--recovery-timeout=seconds`: O número máximo de segundos para esperar que a recuperação termine. Definir 0 desativa. O padrão é 0.

`-T` `--enable-two-phase`: Habilita o compromisso da assinatura. Quando várias bases de dados são especificadas, esta opção se aplica uniformemente a todas as assinaturas criadas nessas bases de dados. O padrão é `false`.

`-U username` `--subscriber-username=username`: O nome do usuário para se conectar no servidor alvo. O padrão é o nome do usuário do sistema operacional atual.

`-v` `--verbose`: Habilita o modo verbose. Isso fará com que o pg_createsubscriber exiba mensagens de progresso e informações detalhadas sobre cada etapa no erro padrão. Repetindo a opção, mensagens adicionais de nível de depuração aparecerão no erro padrão.

`--clean=objtype`: Remova todos os objetos do tipo especificado a partir dos bancos de dados especificados no servidor de destino.

* `publications`: As publicações do `FOR ALL TABLES` estabelecidas para este assinante são sempre descartadas; especificar este tipo de objeto faz com que todas as outras publicações replicadas do servidor de origem também sejam descartadas.

Os objetos selecionados para serem descartados são registrados individualmente, inclusive durante um `--dry-run`. Não há oportunidade de afetar ou parar o descarte dos objetos selecionados, então considere fazer um backup deles usando pg_dump.

`--config-file=filename`: Use o arquivo de configuração principal especificado para o diretório de dados de destino. O pg_createsubscriber usa internamente o comando pg_ctl para iniciar e parar o servidor de destino. Permite que você especifique o arquivo de configuração real `postgresql.conf` se ele estiver armazenado fora do diretório de dados.

`--publication=name`: O nome da publicação para configurar a replicação lógica. Múltiplos nomes de publicação podem ser especificados escrevendo múltiplos interruptores `--publication`. O número de nomes de publicação deve corresponder ao número de bancos de dados especificados, caso contrário, um erro é relatado. A ordem dos múltiplos interruptores de nome de publicação deve corresponder à ordem dos interruptores de banco de dados. Se esta opção não for especificada, um nome gerado é atribuído ao nome da publicação. Esta opção não pode ser usada juntamente com `--all`.

`--replication-slot=name`: O nome do slot de replicação para configurar a replicação lógica. Múltiplos slots de replicação podem ser especificados escrevendo múltiplos interruptores `--replication-slot`. O número de nomes de slots de replicação deve corresponder ao número de bancos de dados especificados, caso contrário, será relatado um erro. A ordem dos múltiplos interruptores de nome de slot de replicação deve corresponder à ordem dos interruptores de banco de dados. Se esta opção não for especificada, o nome da assinatura é atribuído ao nome do slot de replicação. Esta opção não pode ser usada juntamente com `--all`.

`--subscription=name`: O nome da assinatura para configurar a replicação lógica. Múltiplos nomes de assinatura podem ser especificados escrevendo múltiplos interruptores `--subscription`. O número de nomes de assinatura deve corresponder ao número de bancos de dados especificados, caso contrário, um erro é relatado. A ordem dos múltiplos interruptores de nome de assinatura deve corresponder à ordem dos interruptores de banco de dados. Se esta opção não for especificada, um nome gerado é atribuído ao nome da assinatura. Esta opção não pode ser usada juntamente com `--all`.

`-V` `--version`: Imprimir a versão do pg_createsubscriber e sair.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando pg_createsubscriber e sair.

## Notas

### Pré-requisitos

Existem alguns pré-requisitos para o pg_createsubscriber converter o servidor de destino em uma replica lógica. Se esses pré-requisitos não forem atendidos, um erro será relatado. Os servidores de origem e de destino devem ter a mesma versão principal do pg_createsubscriber. O diretório de dados de destino fornecido deve ter o mesmo identificador de sistema que o diretório de dados de origem. O usuário de banco de dados fornecido para o diretório de dados de destino deve ter privilégios para criar [assinaturas](sql-createsubscription.md "CREATE SUBSCRIPTION") e usar [[`pg_replication_origin_advance()`](functions-admin.md#PG-REPLICATION-ORIGIN-ADVANCE)].

O servidor-alvo deve ser usado como um standby físico. O servidor-alvo deve ter [max_active_replication_origins][(runtime-config-replication.md#GUC-MAX-ACTIVE-REPLICATION-ORIGINS)] e [max_logical_replication_workers][(runtime-config-replication.md#GUC-MAX-LOGICAL-REPLICATION-WORKERS)] configurados para um valor maior ou igual ao número de bancos de dados especificados. O servidor-alvo deve ter [max_worker_processes][(runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES)] configurado para um valor maior que o número de bancos de dados especificados. O servidor-alvo deve aceitar conexões locais. Se você planeja usar o switch `--enable-two-phase`, também precisará configurar o [max_prepared_transactions][(runtime-config-resource.md#GUC-MAX-PREPARED-TRANSACTIONS)] de forma apropriada.

O servidor de origem deve aceitar conexões do servidor de destino. O servidor de origem não deve estar em recuperação. O servidor de origem deve ter [wal_level][(runtime-config-wal.md#GUC-WAL-LEVEL)] como `logical`. O servidor de origem deve ter [max_replication_slots][(runtime-config-replication.md#GUC-MAX-REPLICATION-SLOTS)] configurado para um valor maior ou igual ao número de bancos de dados especificados mais os slots de replicação existentes. O servidor de origem deve ter [max_wal_senders][(runtime-config-replication.md#GUC-MAX-WAL-SENDERS)] configurado para um valor maior ou igual ao número de bancos de dados especificados e aos processos de emissor de WAL existentes.

### Avisos

Se o pg_createsubscriber falhar após o servidor alvo ter sido promovido, é provável que o diretório de dados não esteja em um estado que possa ser recuperado. Nesse caso, é recomendável criar um novo servidor de espera.

O pg_createsubscriber geralmente inicia o servidor-alvo com diferentes configurações de conexão durante a transformação. Portanto, as conexões ao servidor-alvo devem falhar.

Como os comandos DDL não são replicados pela replicação lógica, evite executar comandos DDL que alterem o esquema do banco de dados enquanto estiver executando o pg_createsubscriber. Se o servidor de destino já tiver sido convertido para replica lógica, os comandos DDL podem não ser replicados, o que pode causar um erro.

Se o pg_createsubscriber falhar durante o processamento, os objetos (publicações, faixas de replicação) criados no servidor de origem são removidos. A remoção pode falhar se o servidor de destino não conseguir se conectar ao servidor de origem. Nesse caso, uma mensagem de aviso informará os objetos restantes. Se o servidor de destino estiver em execução, ele será parado.

Se a replicação estiver usando [primary_slot_name][(runtime-config-replication.md#GUC-PRIMARY-SLOT-NAME)], ela será removida do servidor de origem após a configuração de replicação lógica.

Se o servidor alvo for uma replica síncrona, os commits de transação no primário podem esperar pela replicação enquanto o pg_createsubscriber está sendo executado.

A menos que o interruptor `--enable-two-phase` seja especificado, o pg_createsubscriber configura a replicação lógica com o commit de duas fases desativado. Isso significa que quaisquer transações preparadas serão replicadas no momento do `COMMIT PREPARED`, sem preparação antecipada. Uma vez que a configuração esteja completa, você pode descartar e recriar manualmente a(s) assinatura(ões) com a opção [`two_phase`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE)] habilitada.

O pg_createsubscriber altera o identificador do sistema usando o pg_resetwal. Isso evitaria situações em que o servidor alvo poderia usar arquivos WAL do servidor fonte. Se o servidor alvo tiver um standby, a replicação será interrompida e um novo standby deve ser criado.

Falhas de replicação podem ocorrer se os arquivos WAL necessários estiverem ausentes. Para evitar isso, o servidor de origem deve definir [max_slot_wal_keep_size][(runtime-config-replication.md#GUC-MAX-SLOT-WAL-KEEP-SIZE)] para `-1` para garantir que os arquivos WAL necessários não sejam removidos prematuramente.

### Como Funciona

A ideia básica é ter um ponto de início de replicação a partir do servidor de origem e configurar uma replicação lógica para começar a partir deste ponto:

1. Inicie o servidor-alvo com as opções de linha de comando especificadas. Se o servidor-alvo já estiver em execução, o pg_createsubscriber terminará com um erro.
2. Verifique se o servidor-alvo pode ser convertido. Há também algumas verificações no servidor-fonte. Se qualquer um dos pré-requisitos não for atendido, o pg_createsubscriber terminará com um erro.
3. Crie uma publicação e um slot de replicação para cada banco de dados especificado no servidor-fonte. Cada publicação é criada usando `FOR ALL TABLES`(sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-ALL-TABLES). Se a opção `--publication` não for especificada, a publicação tem o seguinte padrão de nome: “`pg_createsubscriber_%u_%x`” (parâmetro: banco de dados *`oid`*, aleatório *`int`*). Se a opção `--replication-slot` não for especificada, o slot de replicação tem o seguinte padrão de nome: “`pg_createsubscriber_%u_%x`” (parâmetros: banco de dados *`oid`*, aleatório *`int`*). Esses slots de replicação serão usados pelas assinaturas em uma etapa futura. O último slot de replicação LSN é usado como um ponto de parada no parâmetro [recovery_target_lsn](runtime-config-wal.md#GUC-RECOVERY-TARGET-LSN) e pelas assinaturas como um ponto de início de replicação. Isso garante que nenhuma transação será perdida.
4. Escreva os parâmetros de recuperação no diretório de dados do alvo e reinicie o servidor-alvo. Especifica um LSN ([recovery_target_lsn](runtime-config-wal.md#GUC-RECOVERY-TARGET-LSN)) da localização do log de antecipação até a qual a recuperação prosseguirá. Também especifica `promote` como a ação que o servidor deve tomar uma vez que o alvo de recuperação seja alcançado. Parâmetros de recuperação adicionais (runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY-TARGET "19.5.6. Recovery Target") são adicionados para evitar comportamento inesperado durante o processo de recuperação, como o fim da recuperação assim que um estado consistente é alcançado (o WAL deve ser aplicado até o ponto de início de replicação) e múltiplos alvos de recuperação que podem causar uma falha. Esta etapa termina uma vez que o servidor termina o modo standby e está aceitando transações de leitura e escrita. Se a opção `--recovery-timeout` for definida, o pg_createsubscriber terminará se a recuperação não terminar até o número especificado de segundos.
5. Crie uma assinatura para cada banco de dados especificado no servidor-alvo. Se a opção `--subscription` não for especificada, a assinatura tem o seguinte padrão de nome: “`pg_createsubscriber_%u_%x`” (parâmetros: banco de dados *`oid`*, aleatório *`int`*). Não copia dados existentes do servidor-fonte. Não cria um slot de replicação. Em vez disso, usa o slot de replicação que foi criado em uma etapa anterior. A assinatura é criada, mas ainda não é habilitada. O motivo é que o progresso da replicação deve ser definido para o ponto de início de replicação antes de iniciar a replicação.
6. Descarte as publicações no servidor-alvo que foram replicadas porque foram criadas antes da localização de início de replicação. Não tem uso no assinante.
7. Defina o progresso da replicação para o ponto de início de replicação para cada assinatura. Quando o servidor-alvo inicia o processo de recuperação, ele alcança o ponto de início de replicação. Esse é o LSN exato que será usado como uma localização de replicação inicial para cada assinatura. O nome da origem da replicação é obtido desde que a assinatura foi criada. O nome da origem da replicação e o ponto de início de replicação são usados em [`pg_replication_origin_advance()`](functions-admin.md#PG-REPLICATION-ORIGIN-ADVANCE) para configurar a localização de replicação inicial.
8. Habilite a assinatura para cada banco de dados especificado no servidor-alvo. A assinatura começa a aplicar transações a partir do ponto de início de replicação.
9. Se o servidor de standby estava usando [primary_slot_name](runtime-config-replication.md#GUC-PRIMARY-SLOT-NAME), não tem uso a partir de agora, então descarte-o.
10. Se o servidor de standby contém [failover replication slots](logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION "47.2.3. Replication Slot Synchronization"), eles não podem ser sincronizados mais, então descarte-os.
11. Atualize o identificador do sistema no servidor-alvo. O [pg_resetwal](app-pgresetwal.md "pg_resetwal") é executado para modificar o identificador do sistema. O servidor-alvo é parado como um requisito de `pg_resetwal`.

## Exemplos

Para criar uma replica lógica para os bancos de dados `hr` e `finance` a partir de uma replica física em `foo`:

```
$ pg_createsubscriber -D /usr/local/pgsql/data -P "host=foo" -d hr -d finance
```

## Veja também

[pg_basebackup](app-pgbasebackup.md "pg_basebackup")
