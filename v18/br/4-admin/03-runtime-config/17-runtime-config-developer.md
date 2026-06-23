## 19.17. Opções do Desenvolvedor [#](#RUNTIME-CONFIG-DEVELOPER)

Os seguintes parâmetros são destinados para testes de desenvolvedores e nunca devem ser usados em um banco de dados de produção. No entanto, alguns deles podem ser usados para auxiliar na recuperação de bancos de dados gravemente danificados. Como tal, eles foram excluídos do arquivo de amostra `postgresql.conf`. Note que muitos desses parâmetros requerem flags especiais de compilação de fonte para funcionar em tudo.

`allow_in_place_tablespaces` (`boolean`) [#](#GUC-ALLOW-IN-PLACE-TABLESPACES): Permite que espaços de tabela sejam criados como diretórios dentro de `pg_tblspc`, quando uma string de localização vazia é fornecida ao comando `CREATE TABLESPACE`. Isso visa permitir a realização de cenários de replicação de teste onde servidores primário e de espera estão em execução na mesma máquina. Esses diretórios provavelmente vão confundir as ferramentas de backup que esperam encontrar apenas links simbólicos naquela localização. Somente superusuários e usuários com o privilégio apropriado `SET` podem alterar essa configuração.

`allow_system_table_mods` (`boolean`) [#](#GUC-ALLOW-SYSTEM-TABLE-MODS): Permite a modificação da estrutura das tabelas do sistema, bem como certas outras ações arriscadas nas tabelas do sistema. Isso não é permitido, de outra forma, mesmo para superusuários. O uso inadequado deste ajuste pode causar perda de dados irrecuperável ou corromper seriamente o sistema do banco de dados. Somente superusuários e usuários com o privilégio apropriado `SET` podem alterar este ajuste.

`backtrace_functions` (`string`) [#](#GUC-BACKTRACE-FUNCTIONS): Este parâmetro contém uma lista de nomes de funções C separados por vírgula. Se um erro for gerado e o nome da função C interna onde o erro ocorre corresponder a um valor na lista, então um backtrace é escrito no log do servidor juntamente com a mensagem de erro. Isso pode ser usado para depurar áreas específicas do código-fonte.

O suporte de backtrace não está disponível em todas as plataformas, e a qualidade dos backtraces depende das opções de compilação.

Somente superusuários e usuários com o privilégio apropriado `SET` podem alterar essa configuração.

`debug_copy_parse_plan_trees` (`boolean`) [#](#GUC-DEBUG-COPY-PARSE-PLAN-TREES): Ativação dessa opção obriga que todas as árvores de análise e planejamento sejam passadas por `copyObject()`, para facilitar a detecção de erros e omissões em `copyObject()`. O padrão é desativado.

Este parâmetro só está disponível quando `DEBUG_NODE_TESTS_ENABLED` foi definido na hora da compilação (o que acontece automaticamente ao usar a opção de configuração `--enable-cassert`).

`debug_discard_caches` (`integer`) [#](#GUC-DEBUG-DISCARD-CACHES): Quando definido como `1`, cada entrada do cache do catálogo do sistema é invalida na primeira oportunidade possível, independentemente de algo que a tornaria inválida realmente ocorrer. O cache de catálogos de sistema é efetivamente desativado como resultado, então o servidor será executado extremamente lentamente. Valores mais altos executam a invalidação do cache recursivamente, o que é ainda mais lento e útil apenas para testar a lógica de cache em si. O valor padrão de `0` seleciona o comportamento normal de cache do catálogo.

Este parâmetro pode ser muito útil ao tentar desencadear bugs difíceis de reproduzir que envolvem mudanças de catálogo concorrentes, mas, de outra forma, raramente é necessário. Consulte os arquivos de código-fonte `inval.c` e `pg_config_manual.h` para obter detalhes.

Este parâmetro é suportado quando `DISCARD_CACHES_ENABLED` foi definido na hora da compilação (o que acontece automaticamente ao usar a opção de configuração `--enable-cassert`). Em builds de produção, seu valor será sempre `0` e tentativas de configurá-lo para outro valor gerará um erro.

`debug_io_direct` (`string`) [#](#GUC-DEBUG-IO-DIRECT): Peça ao kernel para minimizar os efeitos de cache para dados de relação e arquivos WAL usando `O_DIRECT` (a maioria dos sistemas semelhantes ao Unix), `F_NOCACHE` (macOS) ou `FILE_FLAG_NO_BUFFERING` (Windows).

Pode ser definido como uma string vazia (o padrão) para desabilitar o uso de I/O direto, ou uma lista de operações separadas por vírgula que devem usar I/O direto. As opções válidas são `data` para arquivos de dados principais, `wal` para arquivos WAL e `wal_init` para arquivos WAL quando inicialmente alocados. Este parâmetro só pode ser definido no início do servidor.

Alguns sistemas operacionais e sistemas de arquivos não suportam I/O direto, portanto, as configurações não padrão podem ser rejeitadas na inicialização ou causar erros.

Atualmente, essa funcionalidade reduz o desempenho e é destinada apenas para testes de desenvolvedores.

`debug_parallel_query` (`enum`) [#](#GUC-DEBUG-PARALLEL-QUERY): Permite o uso de consultas paralelas para fins de teste, mesmo em casos em que não se espera um benefício de desempenho. Os valores permitidos de `debug_parallel_query` são `off` (use o modo paralelo apenas quando se espera que melhore o desempenho), `on` (forçar consulta paralela para todas as consultas para as quais se acredita que seja seguro) e `regress` (como `on`, mas com mudanças de comportamento adicionais conforme explicado abaixo).

Mais especificamente, definir esse valor para `on` adicionará um nó `Gather` ao topo de qualquer plano de consulta para o qual isso parece ser seguro, para que a consulta seja executada dentro de um trabalhador paralelo. Mesmo quando um trabalhador paralelo não estiver disponível ou não puder ser usado, operações como o início de uma subtransação que seriam proibidas em um contexto de consulta paralela serão proibidas, a menos que o planejador acredite que isso causará o fracasso da consulta. Se falhas ou resultados inesperados ocorrerem quando essa opção é definida, algumas funções usadas pela consulta podem precisar ser marcadas `PARALLEL UNSAFE` (ou, possivelmente, `PARALLEL RESTRICTED`).

Definir esse valor para `regress` tem todos os mesmos efeitos que definir para `on`, além de alguns efeitos adicionais que visam facilitar o teste de regressão automatizado. Normalmente, as mensagens de um trabalhador paralelo incluem uma linha de contexto indicando isso, mas uma definição de `regress` suprime essa linha, de modo que a saída seja a mesma que na execução não paralela. Além disso, os nós `Gather` adicionados aos planos por essa definição são ocultados na saída de `EXPLAIN`, de modo que a saída corresponda ao que seria obtido se essa definição fosse `off`.

`debug_raw_expression_coverage_test` (`boolean`) [#](#GUC-DEBUG-RAW-EXPRESSION-COVERAGE-TEST): Ativação desta opção obriga que todas as árvores de análise bruta para declarações DML sejam analisadas por `raw_expression_tree_walker()`, para facilitar a detecção de erros e omissões nessa função. O padrão é desativado.

Este parâmetro só está disponível quando `DEBUG_NODE_TESTS_ENABLED` foi definido na hora da compilação (o que acontece automaticamente ao usar a opção de configuração `--enable-cassert`).

`debug_write_read_parse_plan_trees` (`boolean`) [#](#GUC-DEBUG-WRITE-READ-PARSE-PLAN-TREES): Ativação dessa opção obriga que todos os parse e planos sejam passados pelo `outfuncs.c`/`readfuncs.c`, para facilitar a detecção de erros e omissões nesses módulos. O padrão é desativado.

Este parâmetro só está disponível quando `DEBUG_NODE_TESTS_ENABLED` foi definido na hora da compilação (o que acontece automaticamente ao usar a opção de configuração `--enable-cassert`).

`ignore_system_indexes` (`boolean`) [#](#GUC-IGNORE-SYSTEM-INDEXES): Ignore índices do sistema ao ler tabelas do sistema (mas ainda atualize os índices ao modificar as tabelas). Isso é útil ao recuperar de índices do sistema danificados. Este parâmetro não pode ser alterado após o início da sessão.

`post_auth_delay` (`integer`) [#](#GUC-POST-AUTH-DELAY): O tempo de atraso quando um novo processo do servidor é iniciado, após ele realizar o procedimento de autenticação. Isso visa dar aos desenvolvedores a oportunidade de se conectar ao processo do servidor com um depurador. Se esse valor for especificado sem unidades, ele é considerado em segundos. Um valor de zero (padrão) desativa o atraso. Este parâmetro não pode ser alterado após o início da sessão.

`pre_auth_delay` (`integer`) [#](#GUC-PRE-AUTH-DELAY): O tempo de atraso imediatamente após um novo processo do servidor ser criado, antes de realizar o procedimento de autenticação. Isso visa dar aos desenvolvedores a oportunidade de se conectar ao processo do servidor com um depurador para identificar comportamentos incorretos na autenticação. Se esse valor for especificado sem unidades, ele é considerado em segundos. Um valor de zero (padrão) desativa o atraso. Esse parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`trace_notify` (`boolean`) [#](#GUC-TRACE-NOTIFY): Gera uma grande quantidade de saída de depuração para os comandos `LISTEN` e `NOTIFY`. [client_min_messages](runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES) ou [log_min_messages](runtime-config-logging.md#GUC-LOG-MIN-MESSAGES) deve ser `DEBUG1` ou inferior para enviar essa saída para os logs do cliente ou do servidor, respectivamente.

`trace_sort` (`boolean`) [#](#GUC-TRACE-SORT): Se ativado, emita informações sobre o uso de recursos durante operações de classificação.

`trace_locks` (`boolean`) [#](#GUC-TRACE-LOCKS): Se ativado, emita informações sobre o uso da trava. As informações descarregadas incluem o tipo de operação de trava, o tipo de trava e o identificador único do objeto que está sendo travado ou desbloqueado. Também estão incluídas máscaras de bits para os tipos de trava já concedidos neste objeto, bem como para os tipos de trava esperados neste objeto. Para cada tipo de trava, uma contagem do número de trava concedida e trava em espera também é descarregada, bem como os totais. Um exemplo da saída do arquivo de registro é mostrado aqui:

```
LOG:  LockAcquire: new: lock(0xb7acd844) id(24688,24696,0,0,0,1) grantMask(0) req(0,0,0,0,0,0,0)=0 grant(0,0,0,0,0,0,0)=0 wait(0) type(AccessShareLock) LOG:  GrantLock: lock(0xb7acd844) id(24688,24696,0,0,0,1) grantMask(2) req(1,0,0,0,0,0,0)=1 grant(1,0,0,0,0,0,0)=1 wait(0) type(AccessShareLock) LOG:  UnGrantLock: updated: lock(0xb7acd844) id(24688,24696,0,0,0,1) grantMask(0) req(0,0,0,0,0,0,0)=0 grant(0,0,0,0,0,0,0)=0 wait(0) type(AccessShareLock) LOG:  CleanUpLock: deleting: lock(0xb7acd844) id(24688,24696,0,0,0,1) grantMask(0) req(0,0,0,0,0,0,0)=0 grant(0,0,0,0,0,0,0)=0 wait(0) type(INVALID)
```

Detalhes da estrutura que está sendo descartada podem ser encontrados em `src/include/storage/lock.h`.

Este parâmetro só está disponível se a macro `LOCK_DEBUG` foi definida quando o PostgreSQL foi compilado.

`trace_lwlocks` (`boolean`) [#](#GUC-TRACE-LWLOCKS): Se ativado, emita informações sobre o uso de bloqueio leve. Os bloqueios leves são destinados principalmente a fornecer exclusão mútua do acesso a estruturas de dados de memória compartilhada.

Este parâmetro só está disponível se a macro `LOCK_DEBUG` foi definida quando o PostgreSQL foi compilado.

`trace_userlocks` (`boolean`) [#](#GUC-TRACE-USERLOCKS): Se ativado, emita informações sobre o uso de bloqueio do usuário. A saída é a mesma que para `trace_locks`, apenas para bloqueios de aconselhamento.

Este parâmetro só está disponível se a macro `LOCK_DEBUG` foi definida quando o PostgreSQL foi compilado.

`trace_lock_oidmin` (`integer`) [#](#GUC-TRACE-LOCK-OIDMIN): Se definido, não rastreie bloqueios para tabelas abaixo deste OID (usado para evitar saída em tabelas do sistema).

Este parâmetro só está disponível se a macro `LOCK_DEBUG` foi definida quando o PostgreSQL foi compilado.

`trace_lock_table` (`integer`) [#](#GUC-TRACE-LOCK-TABLE): Rastrear incondicionalmente bloqueios nesta tabela (OID).

Este parâmetro só está disponível se a macro `LOCK_DEBUG` foi definida quando o PostgreSQL foi compilado.

`debug_deadlocks` (`boolean`) [#](#GUC-DEBUG-DEADLOCKS): Se configurado, exibe informações sobre todos os bloqueios atuais quando ocorre o tempo limite de deadlock.

Este parâmetro só está disponível se a macro `LOCK_DEBUG` foi definida quando o PostgreSQL foi compilado.

`log_btree_build_stats` (`boolean`) [#](#GUC-LOG-BTREE-BUILD-STATS): Se configurado, registra estatísticas de uso de recursos do sistema (memória e CPU) em várias operações de árvore B.

Este parâmetro só está disponível se a macro `BTREE_BUILD_STATS` foi definida quando o PostgreSQL foi compilado.

`wal_consistency_checking` (`string`) [#](#GUC-WAL-CONSISTENCY-CHECKING): Este parâmetro é destinado a ser usado para verificar bugs nas rotinas de refazer WAL. Quando ativado, imagens de página inteira de quaisquer buffers modificados em conjunto com o registro WAL são adicionadas ao registro. Se o registro for posteriormente reinterpretado, o sistema aplicará primeiro cada registro e, em seguida, testará se os buffers modificados pelo registro correspondem às imagens armazenadas. Em certos casos (como bits de dica), variações menores são aceitáveis e serão ignoradas. Quaisquer diferenças inesperadas resultarão em um erro fatal, terminando a recuperação.

O valor padrão deste ajuste é a string vazia, que desativa o recurso. Pode ser definido como `all` para verificar todos os registros, ou como uma lista de geradores de recursos separados por vírgula para verificar apenas registros originados desses geradores de recursos. Atualmente, os geradores de recursos suportados são `heap`, `heap2`, `btree`, `hash`, `gin`, `gist`, `sequence`, `spgist`, `brin` e `generic`. As extensões podem definir geradores de recursos adicionais. Somente os superusuários e os usuários com o privilégio apropriado `SET` podem alterar este ajuste.

`wal_debug` (`boolean`) [#](#GUC-WAL-DEBUG): Se ativado, emita saída de depuração relacionada ao WAL. Este parâmetro só está disponível se a macro `WAL_DEBUG` foi definida quando o PostgreSQL foi compilado.

`ignore_checksum_failure` (`boolean`) [#](#GUC-IGNORE-CHECKSUM-FAILURE): Tem efeito apenas se os [`-k`](app-initdb.md#APP-INITDB-DATA-CHECKSUMS) estiverem habilitados.

A detecção de uma falha no checksum durante uma leitura normalmente faz com que o PostgreSQL informe um erro, abortando a transação atual. Definir `ignore_checksum_failure` para on faz com que o sistema ignore a falha (mas ainda informe um aviso) e continue processando. Esse comportamento pode *causar falhas, propagar ou esconder corrupção, ou outros problemas graves*. No entanto, pode permitir que você ignore o erro e recupere tuplas não danificadas que ainda podem estar presentes na tabela, se o cabeçalho do bloco ainda estiver sadio. Se o cabeçalho estiver corrompido, um erro será informado mesmo que essa opção esteja habilitada. O ajuste padrão é `off`. Apenas superusuários e usuários com o privilégio apropriado `SET` podem alterar essa configuração.

`zero_damaged_pages` (`boolean`) [#](#GUC-ZERO-DAMAGED-PAGES): A detecção de um cabeçalho de página danificado normalmente faz com que o PostgreSQL informe um erro, abortando a transação atual. Definir `zero_damaged_pages` para on faz com que o sistema, em vez disso, informe um aviso, apague a página danificada na memória e continue o processamento. Esse comportamento *destruirá os dados*, ou seja, todas as linhas na página danificada. No entanto, permite que você ignore o erro e recupere linhas de quaisquer páginas não danificadas que possam estar presentes na tabela. É útil para recuperar dados se a corrupção ocorrer devido a um erro de hardware ou software. Geralmente, você não deve definir isso até ter desistido da esperança de recuperar dados das páginas danificadas de uma tabela. As páginas apagadas não são forçadas ao disco, portanto, é recomendável recriar a tabela ou o índice antes de desligar novamente esse parâmetro. O ajuste padrão é `off`. Somente usuários superusuários e usuários com o privilégio apropriado `SET` podem alterar esse ajuste.

`ignore_invalid_pages` (`boolean`) [#](#GUC-IGNORE-INVALID-PAGES): Se configurado para `off` (o padrão), a detecção de registros WAL com referências a páginas inválidas durante a recuperação faz com que o PostgreSQL gere um erro de nível PANIC, abortando a recuperação. Configurar `ignore_invalid_pages` para `on` faz com que o sistema ignore as referências de página inválidas nos registros WAL (mas ainda informe um aviso) e continue a recuperação. Esse comportamento pode causar *quebras, perda de dados, propagação ou ocultação de corrupção, ou outros problemas graves*. No entanto, pode permitir que você ultrapasse o erro de nível PANIC, termine a recuperação e faça o servidor iniciar. O parâmetro só pode ser configurado na inicialização do servidor. Ele só tem efeito durante a recuperação ou no modo standby.

`jit_debugging_support` (`boolean`) [#](#GUC-JIT-DEBUGGING-SUPPORT): Se o LLVM tiver a funcionalidade necessária, registre as funções geradas com o GDB. Isso facilita a depuração. A configuração padrão é `off`. Somente usuários superusuários e usuários com o privilégio apropriado `SET` podem alterar este parâmetro no início da sessão, e não pode ser alterado em nenhuma sessão.

`jit_dump_bitcode` (`boolean`) [#](#GUC-JIT-DUMP-BITCODE): Escreve o IR gerado do LLVM para o sistema de arquivos, dentro de [data_directory](runtime-config-file-locations.md#GUC-DATA-DIRECTORY). Isso é útil apenas para trabalhar com os recursos internos da implementação JIT. A configuração padrão é `off`. Somente usuários superusuários e usuários com o privilégio apropriado `SET` podem alterar essa configuração.

`jit_expressions` (`boolean`) [#](#GUC-JIT-EXPRESSIONS): Determina se as expressões são compiladas JIT, quando a compilação JIT é ativada (ver [Seção 30.2] (jit-decision.md "30.2. When to JIT?")). O padrão é `on`.

`jit_profiling_support` (`boolean`) [#](#GUC-JIT-PROFILING-SUPPORT): Se o LLVM tiver a funcionalidade necessária, emita os dados necessários para permitir que o perf profile funções geradas pelo JIT. Isso escreve arquivos para `~/.debug/jit/`; o usuário é responsável por realizar a limpeza quando desejado. A configuração padrão é `off`. Somente superusuários e usuários com o privilégio apropriado `SET` podem alterar este parâmetro no início da sessão, e não pode ser alterado em nenhuma parte da sessão.

`jit_tuple_deforming` (`boolean`) [#](#GUC-JIT-TUPLE-DEFORMING): Determina se a compilação de tuple deforming é JIT compilada, quando a compilação JIT é ativada (ver [Seção 30.2](jit-decision.md "30.2. When to JIT?")). O padrão é `on`.

`remove_temp_files_after_crash` (`boolean`) [#](#GUC-REMOVE-TEMP-FILES-AFTER-CRASH): Quando definido como `on`, que é o padrão, o PostgreSQL removerá automaticamente os arquivos temporários após um travamento do backend. Se desativado, os arquivos serão retidos e podem ser usados, por exemplo, para depuração. No entanto, travamentos repetidos podem resultar na acumulação de arquivos inúteis. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`send_abort_for_crash` (`boolean`) [#](#GUC-SEND-ABORT-FOR-CRASH): Por padrão, após um travamento do backend, o postmaster parará os processos filhos restantes enviando-lhes sinais SIGQUIT, o que lhes permite sair de forma mais ou menos graciosa. Quando esta opção é definida como `on`, SIGABRT é enviado em vez disso. Isso normalmente resulta na produção de um arquivo de depuração de núcleo para cada processo filho. Isso pode ser útil para investigar os estados de outros processos após um travamento. Também pode consumir um monte de espaço em disco no caso de travamentos repetidos, então não ative esta opção em sistemas que você não está monitorando cuidadosamente. Esteja ciente de que não existe suporte para limpar o(s) arquivo(s) de núcleo automaticamente. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`send_abort_for_kill` (`boolean`) [#](#GUC-SEND-ABORT-FOR-KILL): Por padrão, após tentar parar um processo de filho com SIGQUIT, o postmaster aguardará cinco segundos e, em seguida, enviará SIGKILL para forçar a terminação imediata. Quando esta opção é definida como `on`, SIGABRT é enviado em vez de SIGKILL. Isso normalmente resulta na produção de um arquivo de depuração de núcleo para cada processo filho desse tipo. Isso pode ser útil para investigar os estados dos processos filho "traficados". Também pode consumir um monte de espaço em disco no caso de quedas repetidas, então não habilite esta opção em sistemas que não está monitorando com cuidado. Esteja ciente de que não existe suporte para limpar o(s) arquivo(s) de núcleo automaticamente. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`debug_logical_replication_streaming` (`enum`) [#](#GUC-DEBUG-LOGICAL-REPLICATION-STREAMING): Os valores permitidos são `buffered` e `immediate`. O padrão é `buffered`. Este parâmetro é destinado a ser usado para testar a decodificação e replicação lógica de transações grandes. O efeito de `debug_logical_replication_streaming` é diferente para o editor e o assinante:

Do lado do editor, `debug_logical_replication_streaming` permite que as mudanças sejam transmitidas ou serializadas imediatamente na decodificação lógica. Quando definido como `immediate`, transmita cada mudança se a opção [`streaming`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-STREAMING) do [`CREATE SUBSCRIPTION`](sql-createsubscription.md)]] estiver habilitada, caso contrário, serialize cada mudança. Quando definido como `buffered`, a decodificação transmitirá ou serializará as mudanças quando `logical_decoding_work_mem` for alcançado.

Do lado do assinante, se a opção `streaming` estiver definida como `parallel`, o `debug_logical_replication_streaming` pode ser usado para direcionar o líder a aplicar o trabalhador para enviar alterações à fila de memória compartilhada ou para serializar todas as alterações no arquivo. Quando definido como `buffered`, o líder envia alterações para trabalhadores de aplicação paralela via uma fila de memória compartilhada. Quando definido como `immediate`, o líder serializa todas as alterações nos arquivos e notifica os trabalhadores de aplicação paralela a ler e aplicá-las no final da transação.