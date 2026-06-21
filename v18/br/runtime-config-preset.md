## 19.15. Opções Predefinidas [#](#RUNTIME-CONFIG-PRESET)

Os seguintes "parâmetros" são apenas de leitura. Como tal, foram excluídos do arquivo de amostra `postgresql.conf`. Essas opções relatam vários aspectos do comportamento do PostgreSQL que podem ser de interesse para certas aplicações, particularmente interfaces administrativas. A maioria deles é determinada quando o PostgreSQL é compilado ou quando é instalado.

`block_size` (`integer`) [#](#GUC-BLOCK-SIZE): Representa o tamanho de um bloco de disco. É determinado pelo valor de `BLCKSZ` ao construir o servidor. O valor padrão é de 8192 bytes. O significado de algumas variáveis de configuração (como [shared_buffers](runtime-config-resource.md#GUC-SHARED-BUFFERS)) é influenciado por `block_size`. Consulte [Seção 19.4](runtime-config-resource.md "19.4. Resource Consumption") para obter informações.

`data_checksums` (`boolean`) [#](#GUC-DATA-CHECKSUMS): Representa se os checksums de dados estão habilitados para este clúster. Consulte [`-k`](app-initdb.md#APP-INITDB-DATA-CHECKSUMS) para mais informações.

`data_directory_mode` (`integer`) [#](#GUC-DATA-DIRECTORY-MODE): Nos sistemas Unix, este parâmetro reporta as permissões que o diretório de dados (definido por [data_directory](runtime-config-file-locations.md#GUC-DATA-DIRECTORY)) tinha no início do servidor. (Nos sistemas Microsoft Windows, este parâmetro sempre exibirá `0700`.) Consulte a opção `-g` de initdb `-g`(app-initdb.md#APP-INITDB-ALLOW-GROUP-ACCESS) para obter mais informações.

`debug_assertions` (`boolean`) [#](#GUC-DEBUG-ASSERTIONS): Relata se o PostgreSQL foi construído com as asserções habilitadas. Esse é o caso se a macro `USE_ASSERT_CHECKING` for definida quando o PostgreSQL é construído (realizada, por exemplo, pela opção `configure` `--enable-cassert`). Por padrão, o PostgreSQL é construído sem asserções.

`huge_pages_status` (`enum`) [#](#GUC-HUGE-PAGES-STATUS): Representa o estado de páginas enormes na instância atual: `on`, `off`, ou `unknown` (se exibida com `postgres -C`). Este parâmetro é útil para determinar se a alocação de páginas enormes foi bem-sucedida sob `huge_pages=try`. Consulte [huge_pages](runtime-config-resource.md#GUC-HUGE-PAGES) para mais informações.

`integer_datetimes` (`boolean`) [#](#GUC-INTEGER-DATETIMES): Indica se o PostgreSQL foi construído com suporte para datas e horários de inteiros de 64 bits. A partir do PostgreSQL 10, isso é sempre `on`.

`in_hot_standby` (`boolean`) [#](#GUC-IN-HOT-STANDBY): Relata se o servidor está atualmente no modo standby quente. Quando isso é `on`, todas as transações são forçadas a serem somente de leitura. Dentro de uma sessão, isso só pode ser alterado se o servidor for promovido como primário. Consulte [Seção 26.4](hot-standby.md "26.4. Hot Standby") para mais informações.

`max_function_args` (`integer`) [#](#GUC-MAX-FUNCTION-ARGS): Representa o número máximo de argumentos de função. É determinado pelo valor de `FUNC_MAX_ARGS` ao construir o servidor. O valor padrão é 100 argumentos.

`max_identifier_length` (`integer`) [#](#GUC-MAX-IDENTIFIER-LENGTH): Representa o comprimento máximo do identificador. É determinado como um menos do que o valor de `NAMEDATALEN` ao construir o servidor. O valor padrão de `NAMEDATALEN` é 64; portanto, o `max_identifier_length` padrão é de 63 bytes, o que pode ser menos de 63 caracteres quando se usa codificações multibyte.

`max_index_keys` (`integer`) [#](#GUC-MAX-INDEX-KEYS): Representa o número máximo de chaves de índice. É determinado pelo valor de `INDEX_MAX_KEYS` ao construir o servidor. O valor padrão é de 32 chaves.

`num_os_semaphores` (`integer`) [#](#GUC-NUM-OS-SEMAPHORES): Representa o número de semaforos necessários para o servidor com base no número configurado de conexões permitidas ([max_connections](runtime-config-connection.md#GUC-MAX-CONNECTIONS)), processos de trabalho de autovacuum permitidos ([autovacuum_max_workers](runtime-config-vacuum.md#GUC-AUTOVACUUM-MAX-WORKERS)), processos de emissor de WAL permitidos ([max_wal_senders](runtime-config-replication.md#GUC-MAX-WAL-SENDERS)), processos de fundo permitidos ([max_worker_processes](runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES)), etc.

`segment_size` (`integer`) [#](#GUC-SEGMENT-SIZE): Representa o número de blocos (páginas) que podem ser armazenados dentro de um segmento de arquivo. É determinado pelo valor de `RELSEG_SIZE` ao construir o servidor. O tamanho máximo de um arquivo de segmento em bytes é igual a `segment_size` multiplicado por `block_size`; por padrão, isso é 1 GB.

`server_encoding` (`string`) [#](#GUC-SERVER-ENCODING): Representa o codificação do banco de dados (conjunto de caracteres). É determinado quando o banco de dados é criado. Normalmente, os clientes precisam apenas se preocupar com o valor de [client_encoding](runtime-config-client.md#GUC-CLIENT-ENCODING).

`server_version` (`string`) [#](#GUC-SERVER-VERSION): Representa o número da versão do servidor. É determinado pelo valor de `PG_VERSION` ao construir o servidor.

`server_version_num` (`integer`) [#](#GUC-SERVER-VERSION-NUM): Representa o número de versão do servidor como um número inteiro. É determinado pelo valor de `PG_VERSION_NUM` ao construir o servidor.

`shared_memory_size` (`integer`) [#](#GUC-SHARED-MEMORY-SIZE): Representa o tamanho da área principal de memória compartilhada, arredondado para o megabyte mais próximo.

`shared_memory_size_in_huge_pages` (`integer`) [#](#GUC-SHARED-MEMORY-SIZE-IN-HUGE-PAGES): Representa o número de páginas enormes que são necessárias para a área principal de memória compartilhada, com base no tamanho especificado de página enorme (runtime-config-resource.md#GUC-HUGE-PAGE-SIZE). Se as páginas enormes não forem suportadas, isso será `-1`.

Este ajuste é suportado apenas no Linux. Ele é sempre definido como `-1` em outras plataformas. Para mais detalhes sobre o uso de páginas enormes no Linux, consulte [Seção 18.4.5][(kernel-resources.md#LINUX-HUGE-PAGES "18.4.5. Linux Huge Pages")].

`ssl_library` (`string`) [#](#GUC-SSL-LIBRARY): Representa o nome da biblioteca SSL com a qual este servidor PostgreSQL foi construído (mesmo que o SSL não esteja configurado ou em uso neste momento), por exemplo, `OpenSSL`, ou uma string vazia se nenhuma.

`wal_block_size` (`integer`) [#](#GUC-WAL-BLOCK-SIZE): Representa o tamanho de um bloco de disco WAL. É determinado pelo valor de `XLOG_BLCKSZ` ao construir o servidor. O valor padrão é de 8192 bytes.

`wal_segment_size` (`integer`) [#](#GUC-WAL-SEGMENT-SIZE): Representa o tamanho dos segmentos de log de pré-escrita. O valor padrão é de 16 MB. Consulte [Seção 28.5](wal-configuration.md "28.5. WAL Configuration") para obter mais informações.