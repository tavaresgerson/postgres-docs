## E.5. Versão 18 [#](#RELEASE-18)

* [E.5.1. Visão geral](release-18.md#RELEASE-18-HIGHLIGHTS)
* [E.5.2. Migração para a versão 18](release-18.md#RELEASE-18-MIGRATION)
* [E.5.3. Alterações](release-18.md#RELEASE-18-CHANGES)
* [E.5.4. Agradecimentos](release-18.md#RELEASE-18-ACKNOWLEDGEMENTS)

**Data de lançamento:** 25/09/2025

### E.5.1. Visão geral [#](#RELEASE-18-HIGHLIGHTS)

O PostgreSQL 18 contém muitas novas funcionalidades e aprimoramentos, incluindo:

* Um subsistema de E/S assíncrono (AIO) que pode melhorar o desempenho de varreduras sequenciais, varreduras de heap de bitmap, varreduras de vazamento e outras operações.
* [pg_upgrade](pgupgrade.md) agora retém estatísticas do otimizador.
* Suporte para buscas de "varredura ignorada" que permitem o uso de índices de árvore mista B-tree [(indexes-multicolumn.md "11.3. Multicolumn Indexes")] em mais casos.
* A função [[`uuidv7()`](functions-uuid.md#FUNC_UUID_GEN_TABLE)] para gerar UUIDs ordenados por timestamp.
* [colunas geradas](sql-createtable.md#SQL-CREATETABLE-PARMS-GENERATED-STORED) virtuais que calculam seus valores durante operações de leitura. Isso é agora o padrão para colunas geradas.
* Suporte para [autenticação OAuth](auth-oauth.md).
* Suporte para `OLD` e `NEW` para cláusulas [[`RETURNING`](dml-returning.md)] em comandos [INSERT](sql-insert.md), [UPDATE](sql-update.md), [DELETE](sql-delete.md) e [MERGE](sql-merge.md).
* Restrições temporais, ou restrições sobre intervalos, para restrições de [PRIMARY KEY](sql-createtable.md#SQL-CREATETABLE-PARMS-PRIMARY-KEY), [UNIQUE](sql-createtable.md#SQL-CREATETABLE-PARMS-UNIQUE) e [FOREIGN KEY](sql-createtable.md#SQL-CREATETABLE-PARMS-REFERENCES).

Os itens acima e outras novas funcionalidades do PostgreSQL 18 são explicados em detalhes nas seções abaixo.

### E.5.2. Migração para a Versão 18 [#](#RELEASE-18-MIGRATION)

Um descarte/restauração usando [pg_dumpall](app-pg-dumpall.md "pg_dumpall") ou o uso de [pg_upgrade](pgupgrade.md "pg_upgrade") ou replicação lógica é necessário para aqueles que desejam migrar dados de qualquer versão anterior. Consulte [Seção 18.6](upgrading.md "18.6. Upgrading a PostgreSQL Cluster") para informações gerais sobre migração para novas versões principais.

A versão 18 contém várias alterações que podem afetar a compatibilidade com versões anteriores. Observe as seguintes incompatibilidades:

* Altere [initdb](app-initdb.md) para habilitar verificações de checksum de dados (Greg Sabino Mullane) [§](https://postgr.es/c/04bec894a04)

Os checksums podem ser desativados com a nova opção `--no-data-checksums` de initdb. O [[pg_upgrade]][(pgupgrade.md "pg_upgrade") ] exige configurações de checksums de cluster correspondentes, portanto, essa nova opção pode ser útil para atualizar clusters antigos sem checksum. * Mudança no tratamento da abreviação do fuso horário (Tom Lane) [§](https://postgr.es/c/d7674c9fa)

O sistema agora favorecerá as abreviações do fuso horário da sessão atual antes de verificar a variável do servidor [timezone_abbreviations](runtime-config-client.md#GUC-TIMEZONE-ABBREVIATIONS). Anteriormente, a autenticação `timezone_abbreviations` era verificada primeiro. * Desaconselhe a autenticação com senha [MD5](auth-password.md "20.5. Password Authentication") (Nathan Bossart) [§](https://postgr.es/c/db6a4a985)

O suporte para senhas MD5 será removido em uma versão major futura. [CREATE ROLE](sql-createrole.md "CREATE ROLE") e [ALTER ROLE](sql-alterrole.md "ALTER ROLE") agora emitem avisos de depreciação ao definir senhas MD5. Esses avisos podem ser desativados definindo o parâmetro [md5_password_warnings](runtime-config-connection.md#GUC-MD5-PASSWORD-WARNINGS) para `off`. * Altere [VACUUM](sql-vacuum.md "VACUUM") e [ANALYZE](sql-analyze.md "ANALYZE") para processar as crianças de herança de um pai (Michael Harris) [§](https://postgr.es/c/62ddf7ee9)

O comportamento anterior pode ser realizado usando a nova opção `ONLY`.
* Impedir que `COPY FROM` trate (sql-copy.md "COPY") como um marcador de fim de arquivo ao ler arquivos CSV (Daniel Vérité, Tom Lane) [§](https://postgr.es/c/770233748) [§](https://postgr.es/c/da8a4c166)

[psql](app-psql.md) ainda tratará `\.` como um marcador de fim de arquivo ao ler arquivos CSV a partir de `STDIN`. Clientes mais antigos do psql que se conectam a servidores PostgreSQL 18 podem experimentar problemas com `\copy`(app-psql.md#APP-PSQL-META-COMMANDS-COPY). Esta versão também exige que `\.` apareça sozinho em uma linha. * Não permita tabelas particionadas não registradas (Michael Paquier) [§](https://postgr.es/c/e2bab2d79)

Anteriormente, `ALTER TABLE SET [UN]LOGGED` não fazia nada, e a criação de uma tabela particionada não registrada não fez com que seus filhos não fossem registrados.
* Execute `AFTER` [triggers](triggers.md "Chapter 37. Triggers") como o papel que estava ativo quando os eventos do gatilho estavam em fila (Laurenz Albe) [§](https://postgr.es/c/01463e1cc)

Anteriormente, esses gatilhos eram executados com o papel ativo no momento da execução do gatilho (por exemplo, em [COMMIT](sql-commit.md). Isso é significativo para casos em que o papel é alterado entre o tempo da fila e o compromisso da transação.
* Remova o suporte não funcional para privilégios de regra em [GRANT](sql-grant.md)/[REVOKE](sql-revoke.md) (Fujii Masao) [§](https://postgr.es/c/fefa76f70)

Esses campos não funcionam desde o PostgreSQL 8.2. * Remova a coluna `pg_backend_memory_contexts`(view-pg-backend-memory-contexts.md "53.5. pg_backend_memory_contexts").`parent` (Melih Mutlu) [§](https://postgr.es/c/f0d112759)

Isso não é mais necessário, uma vez que `pg_backend_memory_contexts`.`path` foi adicionado.
* Altere `pg_backend_memory_contexts`.`level` e [`pg_log_backend_memory_contexts()`](functions-admin.md#FUNCTIONS-ADMIN-SIGNAL-TABLE "Table 9.96. Server Signaling Functions") para ser baseado em um (Melih Mutlu, Atsushi Torikoshi, David Rowley, Fujii Masao) [§](https://postgr.es/c/32d3ed816) [§](https://postgr.es/c/d9e03864b) [§](https://postgr.es/c/706cbed35)

Esses eram anteriormente baseados em zero.
* Altere [pesquisa de texto completo](textsearch.md) para usar o provedor de collation padrão do clúster para ler arquivos de configuração e dicionários, em vez de sempre usar libc (Peter Eisentraut) [§](https://postgr.es/c/fb1a18810f0)

Os clusters que dependem de provedores de ordenação que não são do libc (por exemplo, ICU, embutido) que se comportam de maneira diferente da libc para caracteres processados pelo LC_CTYPE podem observar mudanças no comportamento de algumas funções de busca de texto completo, bem como da extensão [pg_trgm](pgtrgm.md "F.35. pg_trgm — support for similarity of text using trigram matching"). Ao atualizar esses clusters usando [pg_upgrade](pgupgrade.md "pg_upgrade"), é recomendável reindexar todos os índices relacionados à busca de texto completo e ao pg_trgm após a atualização.

### E.5.3. Alterações [#](#RELEASE-18-CHANGES)

Abaixo, você encontrará um relato detalhado das mudanças entre o PostgreSQL 18 e a versão anterior principal.

#### E.5.3.1. Servidor [#](#RELEASE-18-SERVER)

##### E.5.3.1.1. O otimizador [#](#RELEASE-18-OPTIMIZER)

* Remova automaticamente algumas autojoinhas de tabela desnecessárias (Andrey Lepikhov, Alexander Kuzmenkov, Alexander Korotkov, Alena Rybakina) [§](https://postgr.es/c/fc069a3a6)

Essa otimização pode ser desativada usando a variável do servidor [enable_self_join_elimination](runtime-config-query.md#GUC-ENABLE-SELF-JOIN-ELIMINATION).
* Converta alguns [`IN (VALUES ...)`](functions-comparisons.md#FUNCTIONS-COMPARISONS-IN-SCALAR) em `x = ANY ...` para estatísticas de otimizador melhores (Alena Rybakina, Andrei Lepikhov) [§](https://postgr.es/c/c0962a113)
* Permita a transformação de [`OR`](functions-logical.md) em matrizes para processamento de índice mais rápido (Alexander Korotkov, Andrey Lepikhov) [§](https://postgr.es/c/ae4569161)
* Acelere o processamento de [`INTERSECT`](sql-select.md#SQL-INTERSECT)], [`EXCEPT`](sql-select.md#SQL-EXCEPT)], agregados de janela][(tutorial-window.md "3.5. Window Functions")] e aliases de coluna de vista][(sql-createview.md "CREATE VIEW")] (Tom Lane, David Rowley) [§](https://postgr.es/c/52c707483) [§](https://postgr.es/c/276279295) [§](https://postgr.es/c/8d96f57d5) [§](https://postgr.es/c/908a96861)
* Permita que as chaves de [`SELECT DISTINCT`](sql-select.md#SQL-DISTINCT) sejam reordenadas internamente para evitar ordenação (Richard Guo) [§](https://postgr.es/c/a8ccf4e93)

Essa otimização pode ser desativada usando [enable_distinct_reordering](runtime-config-query.md#GUC-ENABLE-DISTINCT-REORDERING).
* Ignore as colunas [`GROUP BY`](sql-select.md#SQL-GROUPBY) que são funcionalmente dependentes de outras colunas (Zhang Mingli, Jian He, David Rowley) [§](https://postgr.es/c/bd10ec529)

Se uma cláusula `GROUP BY` incluir todas as colunas de um índice único, bem como outras colunas da mesma tabela, essas outras colunas são redundantes e podem ser excluídas do agrupamento. Isso já era verdadeiro para chaves primárias não diferidas.
* Permita que algumas cláusulas `HAVING`(sql-select.md#SQL-HAVING "HAVING Clause") em `GROUPING SETS`(queries-table-expressions.md#QUERIES-GROUPING-SETS "7.2.4. GROUPING SETS, CUBE, and ROLLUP") sejam empurradas para cláusulas `WHERE`(sql-select.md#SQL-WHERE "WHERE Clause") (Richard Guo) [§](https://postgr.es/c/67a54b9e8) [§](https://postgr.es/c/247dea89f) [§](https://postgr.es/c/f5050f795) [§](https://postgr.es/c/cc5d98525)

Isso permite o filtragem de linhas mais cedo. Esse lançamento também corrige algumas consultas `GROUPING SETS` que costumavam retornar resultados incorretos.
* Melhore as estimativas de linha para `generate_series()`(functions-srf.md#FUNCTIONS-SRF-SERIES "Table 9.69. Series Generating Functions") usando os valores de `numeric`(datatype-numeric.md "8.1. Numeric Types") e `timestamp`(datatype-datetime.md "8.5. Date/Time Types") (David Rowley, Song Jinzhou) [§](https://postgr.es/c/036bdcec9) [§](https://postgr.es/c/97173536e)
* Permita que o otimizador use os planos de `Right Semi Join` (Richard Guo) [§](https://postgr.es/c/aa86129e1)

As junções semi-conjuntas são usadas quando é necessário verificar se há pelo menos uma correspondência.
* Permita que as junções de fusão usem [ordens incrementais](runtime-config-query.md#GUC-ENABLE-INCREMENTAL-SORT) (Richard Guo) [§](https://postgr.es/c/828e94c9d)
* Melhore a eficiência do planejamento de consultas que acessam muitas partições (Ashutosh Bapat, Yuya Watari, David Rowley) [§](https://postgr.es/c/88f55bc97) [§](https://postgr.es/c/d69d45a5a)
* Permita [junções partições por partição](runtime-config-query.md#GUC-ENABLE-PARTITIONWISE-JOIN) em mais casos e reduza seu uso de memória (Richard Guo, Tom Lane, Ashutosh Bapat) [§](https://postgr.es/c/9b282a935) [§](https://postgr.es/c/513f4472a)
* Melhore as estimativas de custo de consultas de partições (Nikita Malakhov, Andrei Lepikhov) [§](https://postgr.es/c/fae535da0)
* Melhore o gerenciamento de recursos de otimizadores desativados (Robert Haas) [§](https://postgr.es/c/e22253467)

##### E.5.3.1.2. Índices [#](#RELEASE-18-INDEXES)

* Permita a omissão de varreduras de índices de funções de [btree](xfunc-sql.md)(Peter Geoghegan) [§](https://postgr.es/c/92fe23d93)[(https://postgr.es/c/8a510275d)

Isso permite que índices btree de várias colunas sejam usados em mais casos, como quando não há restrições nas primeiras ou primeiras colunas indexadas (ou há colunas que não são iguais), e há restrições úteis em colunas indexadas posteriormente.
* Permita que índices não únicos btree sejam usados como chaves de partição e em visualizações materializadas (Mark Dilger) [§](https://postgr.es/c/f278e1fe3) [§](https://postgr.es/c/9d6db8bec)

O tipo de índice ainda deve suportar a igualdade.
* Permitir que índices `GIN`(gin.md "65.4. GIN Indexes") sejam criados em paralelo (Tomas Vondra, Matthias van de Meent) [§](https://postgr.es/c/8492feb98)
* Permitir que os valores sejam ordenados para acelerar a construção de índices de tipo de faixa [GiST](gist.md "65.2. GiST Indexes") e [btree](btree.md "65.1. B-Tree Indexes") (Bernd Helmle) [§](https://postgr.es/c/e9e7b6604)

##### E.5.3.1.3. Desempenho Geral [#](#RELEASE-18-PERFORMANCE)

* Adicione um subsistema de E/S assíncrono (Andres Freund, Thomas Munro, Nazir Bilal Yavuz, Melanie Plageman) [§](https://postgr.es/c/02844012b) [§](https://postgr.es/c/da7226993) [§](https://postgr.es/c/55b454d0e) [§](https://postgr.es/c/247ce06b8) [§](https://postgr.es/c/10f664684) [§](https://postgr.es/c/06fb5612c) [§](https://postgr.es/c/c325a7633) [§](https://postgr.es/c/50cb7505b) [§](https://postgr.es/c/047cba7fa) [§](https://postgr.es/c/12ce89fd0) [§](https://postgr.es/c/2a5e709e7)

Essa funcionalidade permite que os backends ajustem várias solicitações de leitura, o que permite análises sequenciais mais eficientes, análises de heap de bitmap, varreduras de vazão, etc. Isso é ativado pela variável do servidor [io_method](runtime-config-resource.md#GUC-IO-METHOD), com as variáveis do servidor [io_combine_limit](runtime-config-resource.md#GUC-IO-COMBINE-LIMIT) e [io_max_combine_limit](runtime-config-resource.md#GUC-IO-MAX-COMBINE-LIMIT) adicionadas para controlá-la. Isso também permite valores de [effective_io_concurrency](runtime-config-resource.md#GUC-EFFECTIVE-IO-CONCURRENCY) e [maintenance_io_concurrency](runtime-config-resource.md#GUC-MAINTENANCE-IO-CONCURRENCY) maiores que zero para sistemas sem suporte ao `fadvise()`. A nova visão do sistema [`pg_aios`](view-pg-aios.md) mostra os identificadores de arquivo sendo usados para I/O assíncrono.
* Melhore o desempenho de bloqueio de consultas que acessam muitas relações (Tomas Vondra) [§](https://postgr.es/c/c4d5cb71d)
* Melhore o desempenho e reduza o uso de memória de junções de hash e [`GROUP BY`](sql-select.md#SQL-GROUPBY) (David Rowley, Jeff Davis) [§](https://postgr.es/c/adf97c156) [§](https://postgr.es/c/0f5738202) [§](https://postgr.es/c/4d143509c) [§](https://postgr.es/c/a0942f441) [§](https://postgr.es/c/626df47ad)

Isso também melhora as operações de conjuntos de hash usadas por `EXCEPT`(sql-select.md#SQL-EXCEPT "EXCEPT Clause"), e as pesquisas de hash de valores de subplano.
* Permita que os vazamentos normais fiquem congelados em algumas páginas, mesmo que sejam visíveis (Melanie Plageman) [§](https://postgr.es/c/052026c9b) [§](https://postgr.es/c/06eae9e62)

Isso reduz o overhead da posterior congelação de relação completa. A agressividade disso pode ser controlada pela variável do servidor e pelo ajuste por tabela [vacuum_max_eager_freeze_failure_rate](runtime-config-vacuum.md#GUC-VACUUM-MAX-EAGER-FREEZE-FAILURE-RATE). Anteriormente, o vacuum nunca processava todas as páginas visíveis até que a congelação fosse necessária.
* Adicione a variável do servidor [vacuum_truncate](runtime-config-vacuum.md#GUC-VACUUM-TRUNCATE) para controlar a truncagem de arquivo durante o [VACUUM](sql-vacuum.md "VACUUM") (Nathan Bossart, Gurjeet Singh) [§](https://postgr.es/c/0164a0f9e)

Um parâmetro de nível de armazenamento com o mesmo nome e comportamento já existia.
* Aumente os valores padrão das variáveis de servidor [effective_io_concurrency](runtime-config-resource.md#GUC-EFFECTIVE-IO-CONCURRENCY) e [maintenance_io_concurrency](runtime-config-resource.md#GUC-MAINTENANCE-IO-CONCURRENCY) para 16 (Melanie Plageman) [§](https://postgr.es/c/ff79b5b2a) [§](https://postgr.es/c/cc6be07eb)

Isso reflete mais precisamente o hardware moderno.

##### E.5.3.1.4. Monitoramento [#](#RELEASE-18-MONITORING)

* Aumente a granularidade de registro da variável do servidor [log_connections](runtime-config-logging.md#GUC-LOG-CONNECTIONS) (Melanie Plageman) [§](https://postgr.es/c/9219093ca)

Essa variável do servidor era anteriormente apenas booleana, que ainda é suportada.
* Adicione a opção `log_connections` para relatar a duração das etapas de conexão (Melanie Plageman) [§](https://postgr.es/c/18cd15e70)
* Adicione [log_line_prefix](runtime-config-logging.md#GUC-LOG-LINE-PREFIX) escape `%L` para exibir o endereço IP do cliente (Greg Sabino Mullane) [§](https://postgr.es/c/3516ea768)
* Adicione a variável do servidor [log_lock_failures](runtime-config-logging.md#GUC-LOG-LOCK-FAILURES) para registrar falhas na aquisição de bloqueio (Yuki Seino, Fujii Masao) [§](https://postgr.es/c/6d376c3b0) [§](https://postgr.es/c/73bdcfab3)

Especificamente, relata falhas de bloqueio `SELECT ... NOWAIT` (sql-select.md#SQL-FOR-UPDATE-SHARE "The Locking Clause").
* Modifique `pg_stat_all_tables` (monitoring-stats.md#MONITORING-PG-STAT-ALL-TABLES-VIEW "27.2.19. pg_stat_all_tables") e suas variantes para relatar o tempo gasto em [VACUUM](sql-vacuum.md "VACUUM"), [ANALYZE](sql-analyze.md "ANALYZE") e suas variantes [automáticas](routine-vacuuming.md#AUTOVACUUM "24.1.6. The Autovacuum Daemon") (Sami Imseih) [§](https://postgr.es/c/30a6ed0ce)

As novas colunas são `total_vacuum_time`, `total_autovacuum_time`, `total_analyze_time` e `total_autoanalyze_time`.
* Adicione o relatório de tempo de atraso em [VACUUM](sql-vacuum.md "VACUUM") e [ANALYZE](sql-analyze.md "ANALYZE") (Bertrand Drouvot, Nathan Bossart) [§](https://postgr.es/c/bb8dff999) [§](https://postgr.es/c/7720082ae)

Essa informação aparece no log do servidor, nas visualizações `pg_stat_progress_vacuum`(progress-reporting.md#VACUUM-PROGRESS-REPORTING "27.4.5. VACUUM Progress Reporting") e [`pg_stat_progress_analyze`](progress-reporting.md#PG-STAT-PROGRESS-ANALYZE-VIEW) e a saída de [VACUUM](sql-vacuum.md "VACUUM") e [ANALYZE](sql-analyze.md "ANALYZE") quando no modo `VERBOSE`; o rastreamento deve ser habilitado com a variável do servidor [track_cost_delay_timing](runtime-config-statistics.md#GUC-TRACK-COST-DELAY-TIMING).
* Adicione a contagem completa do buffer WAL, CPU e estatísticas de leitura média ao `ANALYZE VERBOSE` (Anthonin Bonnefoy) [§](https://postgr.es/c/4c1b4cdb8) [§](https://postgr.es/c/bb7775234)
* Adicione o registro completo do log do autovacuum (Bertrand Drouvot) ao `VACUUM`/`ANALYZE (VERBOSE)` e [§](https://postgr.es/c/6a8a7ce47)
* Adicione relatórios de estatísticas de I/O por banco de dados (Bertrand Drouvot) [§](https://postgr.es/c/9aea73fc6) [§](https://postgr.es/c/3f1db99bf)

As estatísticas são acessadas através de `pg_stat_get_backend_io()`(monitoring-stats.md#PG-STAT-GET-BACKEND-IO). As estatísticas de I/O por backend podem ser limpas através de `pg_stat_reset_backend_stats()`(monitoring-stats.md#MONITORING-STATS-FUNCS-TABLE "Table 27.36. Additional Statistics Functions").
* Adicione as colunas `pg_stat_io`(monitoring-stats.md#MONITORING-PG-STAT-IO-VIEW "27.2.13. pg_stat_io") ao relatório de atividade de I/O em bytes (Nazir Bilal Yavuz) [§](https://postgr.es/c/f92c854cf)

As novas colunas são `read_bytes`, `write_bytes` e `extend_bytes`. A coluna `op_bytes`, que sempre correspondia a [`BLCKSZ`](runtime-config-preset.md#GUC-BLOCK-SIZE), foi removida.
* Adicione linhas de atividade de I/O de WAL ao `pg_stat_io` (Nazir Bilal Yavuz, Bertrand Drouvot, Michael Paquier) [§](https://postgr.es/c/a051e71e2) [§](https://postgr.es/c/4538bd3f1) [§](https://postgr.es/c/7f7f324eb)

Isso inclui a atividade do receptor WAL e um evento de espera para tais escritas.
* Altere a variável do servidor [track_wal_io_timing](runtime-config-statistics.md#GUC-TRACK-WAL-IO-TIMING) para controlar o rastreamento do tempo do WAL em `pg_stat_io` em vez de [`pg_stat_wal`[(monitoring-stats.md#PG-STAT-WAL-VIEW "Table 27.26. pg_stat_wal View")]] (Bertrand Drouvot) [§](https://postgr.es/c/6c349d83b)
* Remova as colunas de leitura/sincronização de `pg_stat_wal` (Bertrand Drouvot) [§](https://postgr.es/c/2421e9a51)(https://postgr.es/c/6c349d83b)

Isso remove as colunas `wal_write`, `wal_sync`, `wal_write_time` e `wal_sync_time`.
* Adicione a função `pg_stat_get_backend_wal()`(monitoring-stats.md#PG-STAT-GET-BACKEND-WAL) para retornar estatísticas de WAL por backend (Bertrand Drouvot) [§](https://postgr.es/c/76def4cdd)

As estatísticas de WAL por backend podem ser limpas através de `pg_stat_reset_backend_stats()`(monitoring-stats.md#MONITORING-STATS-FUNCS-TABLE "Table 27.36. Additional Statistics Functions").
* Adicione a função `pg_ls_summariesdir()`(functions-admin.md#FUNCTIONS-ADMIN-GENFILE-TABLE "Table 9.108. Generic File Access Functions") para listar especificamente o conteúdo de `PGDATA`(storage-file-layout.md "66.1. Database File Layout")/`pg_wal/summaries`(runtime-config-wal.md#GUC-WAL-SUMMARY-KEEP-TIME) (Yushi Ogiwara) [§](https://postgr.es/c/4e1fad378)
* Adicione a coluna `pg_stat_checkpointer`(monitoring-stats.md#MONITORING-PG-STAT-CHECKPOINTER-VIEW "27.2.15. pg_stat_checkpointer").`num_done` para relatar o número de pontos de verificação concluídos (Anton A. Melnikov) [§](https://postgr.es/c/559efce1d)

As colunas `num_timed` e `num_requested` contam os pontos de verificação completos e os pontos de verificação ignorados.
* Adicione a coluna `pg_stat_checkpointer`.`slru_written` para relatar os buffers SLRU escritos (Nitin Jadhav) [§](https://postgr.es/c/17cc5f666)

Além disso, modifique a mensagem do log do servidor de ponto de verificação para relatar valores separados para o buffer compartilhado e o buffer SLRU.
* Adicione colunas ao `pg_stat_database` para relatar atividade de trabalhador paralelo (Benoit Lobréau) [§](https://postgr.es/c/e7a9496de)

As novas colunas são `parallel_workers_to_launch` e `parallel_workers_launched`.
* A computação de listas de constantes [query id](runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID) considera apenas as primeiras e últimas constantes (Dmitry Dolgov, Sami Imseih) [§](https://postgr.es/c/62d712ecf) [§](https://postgr.es/c/9fbd53dea) [§](https://postgr.es/c/c2da1a5d6)

O mesclagem é usado por [pg_stat_statements](pgstatstatements.md).
* Ajuste os cálculos de IDs de consulta para agrupar consultas que utilizam o mesmo nome de relação (Michael Paquier, Sami Imseih) [§](https://postgr.es/c/787514b30)

Isso é verdade mesmo que as tabelas em diferentes esquemas tenham nomes de colunas diferentes.
* Adicione a coluna `pg_backend_memory_contexts`(view-pg-backend-memory-contexts.md "53.5. pg_backend_memory_contexts").`type` ao relatório do tipo de contexto de memória (David Rowley) [§](https://postgr.es/c/12227a1d5)
* Adicione a coluna `pg_backend_memory_contexts`.`path` para mostrar os pais do contexto de memória (Melih Mutlu) [§](https://postgr.es/c/32d3ed816)

##### E.5.3.1.5. Privilegios [#](#RELEASE-18-PRIVILEGES)

* Adicione a função `pg_get_acl()`][(functions-info.md#FUNCTIONS-INFO-OBJECT-TABLE "Table 9.81. Object Information and Addressing Functions") para recuperar detalhes de controle de acesso ao banco de dados (Joel Jacobson) [§](https://postgr.es/c/4564f1ceb)[§][(https://postgr.es/c/d898665bf)
* Adicione a função [`has_largeobject_privilege()`][(functions-info.md#FUNCTIONS-INFO-ACCESS-TABLE "Table 9.72. Access Privilege Inquiry Functions") para verificar privilégios de objetos grandes (Yugo Nagata) [§][(https://postgr.es/c/4eada203a)
* Permita [ALTER PRIVILEGES DEFAULT][(sql-alterdefaultprivileges.md "ALTER DEFAULT PRIVILEGES") para definir privilégios padrão de objetos grandes (Takatsuka Haruka, Yugo Nagata, Laurenz Albe) [§][(https://postgr.es/c/0d6c47766)
* Adicione o papel predefinido [`pg_signal_autovacuum_worker`][(predefined-roles.md "21.5. Predefined Roles") (Kirill Reshke) [§][(https://postgr.es/c/ccd38024b)

Isso permite enviar sinais para os trabalhadores do autovacuum.

##### E.5.3.1.6. Configuração do servidor [#](#RELEASE-18-SERVER-CONFIG)

* Adicione suporte para o método de autenticação [OAuth](auth-oauth.md) (Jacob Champion, Daniel Gustafsson, Thomas Munro) [§](https://postgr.es/c/b3f0be788)

Isso adiciona um método de autenticação `oauth` a `pg_hba.conf` (auth-pg-hba-conf.md "20.1. The pg_hba.conf File"), opções de OAuth do libpq, uma variável do servidor [oauth_validator_libraries](runtime-config-connection.md#GUC-OAUTH-VALIDATOR-LIBRARIES) para carregar bibliotecas de validação de tokens e uma bandeira de configuração `--with-libcurl`[(install-make.md#CONFIGURE-OPTION-WITH-LIBCURL)] para adicionar as bibliotecas necessárias para o tempo de compilação.
* Adicione a variável do servidor [ssl_tls13_ciphers](runtime-config-connection.md#GUC-SSL-TLS13-CIPHERS) para permitir a especificação de múltiplas suítes de cifra TLSv1.3 separadas por colon (Erica Zhang, Daniel Gustafsson) [§](https://postgr.es/c/45188c2ea)
* Altere a variável do servidor [ssl_groups](runtime-config-connection.md#GUC-SSL-GROUPS) para incluir a curva elíptica X25519 (Daniel Gustafsson, Jacob Champion) [§](https://postgr.es/c/daa02c6bd)
* Renomeie a variável do servidor [[`ssl_ecdh_curve`] para [ssl_groups](runtime-config-connection.md#GUC-SSL-GROUPS) e permita que múltiplas curvas ECDH separadas por colon sejam especificadas (Erica Zhang, Daniel Gustafsson) [§](https://postgr.es/c/3d1ef3a15)

O nome anterior ainda funciona. * Faça [cancelar solicitação de chaves](functions-admin.md#FUNCTIONS-ADMIN-SIGNAL-TABLE "Table 9.96. Server Signaling Functions") 256 bits (Heikki Linnakangas, Jelte Fennema-Nio) [§](https://postgr.es/c/a460251f0) [§](https://postgr.es/c/9d9b9d46f)

Isso só é possível quando o servidor e o cliente suportam o protocolo de fio versão 3.2, introduzido nesta versão.
* Adicione a variável do servidor [autovacuum_worker_slots](runtime-config-vacuum.md#GUC-AUTOVACUUM-WORKER-SLOTS) para especificar o número máximo de trabalhadores de segundo plano (Nathan Bossart) [§](https://postgr.es/c/c758119e5)

Com essa variável definida, [autovacuum_max_workers](runtime-config-vacuum.md#GUC-AUTOVACUUM-MAX-WORKERS) pode ser ajustado em tempo real até esse máximo sem necessidade de reiniciar o servidor.
* Permitir a especificação do número fixo de tuplas mortas que acionará um [autovacuum](routine-vacuuming.md#AUTOVACUUM) (Nathan Bossart, Frédéric Yhuel) [§](https://postgr.es/c/306dc520b)

A variável do servidor é [autovacuum_vacuum_max_threshold](runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-MAX-THRESHOLD). Porcentagens ainda são usadas para o disparo. * Altere a variável do servidor [max_files_per_process](runtime-config-resource.md#GUC-MAX-FILES-PER-PROCESS) para limitar apenas arquivos abertos por um backend (Andres Freund) [§](https://postgr.es/c/adb5f85fa)

Anteriormente, os arquivos abertos pelo postmaster também eram contados para esse limite.
* Adicione a variável do servidor [num_os_semaphores](runtime-config-preset.md#GUC-NUM-OS-SEMAPHORES) para relatar o número necessário de semaforos (Nathan Bossart) [§](https://postgr.es/c/0dcaea569)

Isso é útil para a configuração do sistema operacional.
* Adicione a variável do servidor [extension_control_path](runtime-config-client.md#GUC-EXTENSION-CONTROL-PATH) para especificar a localização dos arquivos de controle de extensão (Peter Eisentraut, Matheus Alcantara) [§](https://postgr.es/c/4f7f7b037) [§](https://postgr.es/c/81eaaa2c4)

##### E.5.3.1.7. Replicação e recuperação por streaming [#](#RELEASE-18-REPLICATION)

* Permitir que os slots de replicação inativos sejam automaticamente invalidados usando a variável do servidor [idle_replication_slot_timeout](runtime-config-replication.md#GUC-IDLE-REPLICATION-SLOT-TIMEOUT) (Nisha Moond, Bharath Rupireddy) [§](https://postgr.es/c/ac0e33136)
* Adicionar a variável do servidor [max_active_replication_origins](runtime-config-replication.md#GUC-MAX-ACTIVE-REPLICATION-ORIGINS) para controlar as origens de replicação ativas máximas (Euler Taveira) [§](https://postgr.es/c/04ff636cb)

Isso era anteriormente controlado por [max_replication_slots](runtime-config-replication.md#GUC-MAX-REPLICATION-SLOTS), mas essa nova configuração permite um maior número de origens nos casos em que são necessárias menos faixas.

##### E.5.3.1.8. [[Replicação lógica]] (logical-replication.md "Chapter 29. Logical Replication") [#](#RELEASE-18-LOGICAL)

* Permita que os valores das colunas geradas (sql-createtable.md#SQL-CREATETABLE-PARMS-GENERATED-STORED) sejam replicados logicamente (Shubham Khanna, Vignesh C, Zhijie Hou, Shlok Kyal, Peter Smith) [§](https://postgr.es/c/745217a05)[(https://postgr.es/c/7054186c4)](https://postgr.es/c/87ce27de6)[(https://postgr.es/c/6252b1eaf)

Se a publicação especificar uma lista de colunas, todas as colunas especificadas, geradas e não geradas, são publicadas. Sem uma lista de colunas especificada, a opção de publicação `publish_generated_columns` controla se as colunas geradas são publicadas. As colunas previamente geradas não foram replicadas e o assinante teve que calcular os valores, se possível; isso é particularmente útil para assinantes que não são do PostgreSQL, que não possuem essa capacidade.
* Altere a opção padrão [CREATE SUBSCRIPTION](sql-createsubscription.md "CREATE SUBSCRIPTION") de streaming de `off` para `parallel` (Vignesh C) [§](https://postgr.es/c/1bf1140be)
* Permita que [ALTER SUBSCRIPTION](sql-altersubscription.md "ALTER SUBSCRIPTION") mude o comportamento do compromisso de duas fases do slot de replicação (Hayato Kuroda, Ajin Cherian, Amit Kapila, Zhijie Hou) [§](https://postgr.es/c/1462aad2e) [§](https://postgr.es/c/4868c96bc)
* Registre [conflitos](hot-standby.md#HOT-STANDBY-CONFLICT "26.4.2. Handling Query Conflicts") ao aplicar mudanças de replicação lógica (Zhijie Hou, Nisha Moond) [§](https://postgr.es/c/9758174e2) [§](https://postgr.es/c/edcb71258) [§](https://postgr.es/c/640178c92) [§](https://postgr.es/c/6c2b5edec) [§](https://postgr.es/c/73eba5004)

Relate também em novas colunas de `pg_stat_subscription_stats`(monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION-STATS "27.2.9. pg_stat_subscription_stats").

#### E.5.3.2. Comandos de Utilidade [#](#RELEASE-18-UTILITY)

* Permita que as colunas [geradas](sql-createtable.md#SQL-CREATETABLE-PARMS-GENERATED-STORED) sejam virtuais e faça delas a padrão (Peter Eisentraut, Jian He, Richard Guo, Dean Rasheed) [§](https://postgr.es/c/83ea6c540) [§](https://postgr.es/c/cdc168ad4) [§](https://postgr.es/c/1e4351af3)

As colunas geradas virtualmente geram seus valores quando as colunas são lidas, não escritas. O comportamento de escrita ainda pode ser especificado via a opção `STORED`. * Adicione suporte a [`OLD`]/[`NEW` para [(dml-returning.md "6.4. Returning Data from Modified Rows")](https://postgr.es/c/80feb727c) em consultas DML (Dean Rasheed) [§](https://postgr.es/c/80feb727c)

Anteriormente, `RETURNING` só retornava novos valores para [INSERT](sql-insert.md "INSERT") e [UPDATE](sql-update.md "UPDATE"), e valores antigos para [DELETE](sql-delete.md "DELETE"); [MERGE](sql-merge.md "MERGE") retornaria o valor apropriado para a consulta interna executada. Esta nova sintaxe permite que a lista `RETURNING` de `INSERT`/`UPDATE`/`DELETE`/`MERGE` retorne explicitamente valores antigos e novos usando os aliases especiais `old` e `new`. Esses aliases podem ser renomeados para evitar conflitos de identificadores.
* Permita que tabelas externas sejam criadas como tabelas locais existentes (Zhang Mingli) [§](https://postgr.es/c/302cf1575)

A sintaxe é `CREATE FOREIGN TABLE ... LIKE`](sql-createforeigntable.md "CREATE FOREIGN TABLE"). * Permita `LIKE`](functions-matching.md#FUNCTIONS-LIKE "9.7.1. LIKE") com [colunações não determinísticas](collation.md#COLLATION-NONDETERMINISTIC "23.2.2.4. Nondeterministic Collations") (Peter Eisentraut) [§](https://postgr.es/c/85b7efa1c) * Permita funções de busca de posição de texto com colunas não determinísticas (Peter Eisentraut) [§](https://postgr.es/c/329304c90)

Esses costumavam gerar um erro.
* Adicione o provedor de collation embutido `PG_UNICODE_FAST`(locale.md#LOCALE-PROVIDERS "23.1.4. Locale Providers") (Jeff Davis) [§](https://postgr.es/c/d3d098316)

Este local suporta mapeamento de casos, mas ordena em ordem de código de ponto, não em ordem de linguagem natural.
* Permita que [VACUUM](sql-vacuum.md) e [ANALYZE](sql-analyze.md) processem tabelas particionadas sem processar seus filhos (Michael Harris) [§](https://postgr.es/c/62ddf7ee9)

Isso é ativado com a nova opção `ONLY`. Isso é útil, pois o autovacuum não processa tabelas particionadas, apenas suas crianças.
* Adicione funções para modificar estatísticas de otimizador por relação e por coluna (Corey Huinker) [§](https://postgr.es/c/e839c8ecc) [§](https://postgr.es/c/d32d14639) [§](https://postgr.es/c/650ab8aaf)

As funções são `pg_restore_relation_stats()`, (functions-admin.md#FUNCTIONS-ADMIN-STATSMOD "Table 9.105. Database Object Statistics Manipulation Functions"), `pg_restore_attribute_stats()`, `pg_clear_relation_stats()` e `pg_clear_attribute_stats()`.
* Adicione a variável do servidor [file_copy_method](runtime-config-resource.md#GUC-FILE-COPY-METHOD) para controlar o método de cópia de arquivos (Nazir Bilal Yavuz) [§](https://postgr.es/c/f78ca6f3e)

Isso controla se o `CREATE DATABASE ... STRATEGY=FILE_COPY`(sql-createdatabase.md "CREATE DATABASE") e `ALTER DATABASE ... SET TABLESPACE`(sql-alterdatabase.md "ALTER DATABASE") usa cópia de arquivo ou clone.

##### E.5.3.2.1. [Restrições] (ddl-constraints.md "5.5. Constraints") [#](#RELEASE-18-CONSTRAINTS)

* Permita a especificação de restrições não sobrepostas `PRIMARY KEY`(sql-createtable.md#SQL-CREATETABLE-PARMS-PRIMARY-KEY), `UNIQUE`(sql-createtable.md#SQL-CREATETABLE-PARMS-UNIQUE) e [chave estrangeira](sql-createtable.md#SQL-CREATETABLE-PARMS-REFERENCES) (Paul A. Jungwirth) [§](https://postgr.es/c/fc0438b4e) [§](https://postgr.es/c/89f908a6d)

Isso é especificado para `WITHOUT OVERLAPS` para `PRIMARY KEY` e `UNIQUE`, e para `PERIOD` para chaves estrangeiras, todos aplicados à última coluna especificada.
* Permita que as restrições [`CHECK`](sql-createtable.md#SQL-CREATETABLE-PARMS-CHECK) e [chave estrangeira](sql-createtable.md#SQL-CREATETABLE-PARMS-REFERENCES) sejam especificadas como `NOT ENFORCED` (Amul Sul) [§](https://postgr.es/c/ca87c415e)(https://postgr.es/c/eec0040c4)

Isso também adiciona a coluna `pg_constraint`.(catalog-pg-constraint.md "52.13. pg_constraint").`conenforced`. * Requer relações de chave primária/estrangeira (sql-createtable.md#SQL-CREATETABLE-PARMS-REFERENCES) que utilizem colunas determinísticas ou as mesmas colunas não determinísticas (Peter Eisentraut) [§](https://postgr.es/c/9321d2fdf)

O restabelecimento de um [pg_dump](app-pgdump.md), também utilizado por [pg_upgrade](pgupgrade.md), falhará se essas exigências não forem atendidas; mudanças de esquema devem ser feitas para que esses métodos de atualização tenham sucesso.
* Especifique as especificações da coluna `NOT NULL`[(sql-createtable.md#SQL-CREATETABLE-PARMS-NOT-NULL)] em `pg_constraint`[(catalog-pg-constraint.md "52.13. pg_constraint")] (Álvaro Herrera, Bernd Helmle) [§](https://postgr.es/c/14e87ffa5)[(https://postgr.es/c/81ce602d4)]

Isso permite que nomes sejam especificados para a restrição `NOT NULL`. Isso também adiciona restrições `NOT NULL` a tabelas externas e controle de herança `NOT NULL` a tabelas locais.
* Permita que [ALTER TABLE](sql-altertable.md "ALTER TABLE") defina o atributo `NOT VALID` das restrições `NOT NULL` (Rushabh Lathia, Jian He) [§](https://postgr.es/c/a379061a2)
* Permita a modificação da hereditariedade das restrições `NOT NULL` (Suraj Kharage, Álvaro Herrera) [§](https://postgr.es/c/f4e53e10b) [§](https://postgr.es/c/4a02af8b1)

A sintaxe é `ALTER TABLE ... ALTER CONSTRAINT ... [NO] INHERIT`](sql-altertable.md "ALTER TABLE"). * Permita restrições de chave estrangeira `NOT VALID` em tabelas particionadas (Amul Sul) [§](https://postgr.es/c/b663b9436) * Permita a remoção de restrições (sql-altertable.md#SQL-ALTERTABLE-DESC-DROP-CONSTRAINT) de `ONLY` em tabelas particionadas (Álvaro Herrera) [§](https://postgr.es/c/4dea33ce7)

Isso era anteriormente erroneamente proibido.

##### E.5.3.2.2. [COPIAR](sql-copy.md)[[#](#RELEASE-18-COPY)

* Adicione `REJECT_LIMIT` para controlar o número de linhas inválidas que `COPY FROM` pode ignorar (Atsushi Torikoshi) [§](https://postgr.es/c/4ac2a9bec)

Isso está disponível quando `ON_ERROR = 'ignore'`.
* Permita que `COPY TO` copie linhas de visualizações materializadas preenchidas (Jian He) [§](https://postgr.es/c/534874fac)
* Adicione `COPY` `LOG_VERBOSITY` nível `silent` para suprimir a saída de log de linhas ignoradas (Atsushi Torikoshi) [§](https://postgr.es/c/e7834a1a2)

Este novo nível suprime a saída para linhas de entrada descartadas quando `on_error = 'ignore'`. * Desative `COPY FREEZE` em tabelas estrangeiras (Nathan Bossart) [§](https://postgr.es/c/401a6956f)

Anteriormente, o `COPY` funcionava, mas o `FREEZE` era ignorado, então não permita este comando.

##### E.5.3.2.3. [EXPLICAR](sql-explain.md) [#](#RELEASE-18-EXPLAIN)

* Inclua automaticamente a saída `BUFFERS` na saída `EXPLAIN ANALYZE` (Guillaume Lelarge, David Rowley) [§](https://postgr.es/c/c2a4078eb)
* Adicione o número total de contagem de buffer WAL à saída `EXPLAIN (WAL)` (Bertrand Drouvot) [§](https://postgr.es/c/320545bfc)
* Em `EXPLAIN ANALYZE`, informe o número de consultas de índice usadas por nó de varredura de índice (Peter Geoghegan) [§](https://postgr.es/c/0fbceae84)
* Modifique `EXPLAIN` para saída de contagem de linhas fracionárias (Ibrar Ahmed, Ilia Evdokimov, Robert Haas) [§](https://postgr.es/c/ddb17e387) [§](https://postgr.es/c/95dbd827f)
* Adicione detalhes sobre o uso de memória e disco aos nós de saída `Material`, `Window Aggregate` e nós de expressão de tabela comum para `EXPLAIN` (David Rowley, Tatsuo Ishii) [§](https://postgr.es/c/1eff8279d) [§](https://postgr.es/c/53abb1e0e) [§](https://postgr.es/c/95d6e9af0) [§](https://postgr.es/c/40708acd6)
* Adicione detalhes sobre os argumentos da função de janela à saída `EXPLAIN` (Tom Lane) [§](https://postgr.es/c/8b1b34254)
* Adicione as estatísticas de cache do trabalhador `Parallel Bitmap Heap Scan` à saída `EXPLAIN ANALYZE` (David Geier, Heikki Linnakangas, Donghang Lin, Alena Rybakina, David Rowley) [§](https://postgr.es/c/5a1e6df3b)
* Indique os nós desativados na saída `EXPLAIN ANALYZE` (Robert Haas, David Rowley, Laurenz Albe) [§](https://postgr.es/c/c01743aa4) [§](https://postgr.es/c/161320b4b) [§](https://postgr.es/c/84b8fccbe)

#### E.5.3.3. Tipos de dados [#](#RELEASE-18-DATATYPES)

* Melhorar o mapeamento e a conversão de mapeamento de maiúsculas completas [Unicode](collation.md#COLLATION-MANAGING-STANDARD) (Jeff Davis) [§](https://postgr.es/c/4e7f62bc3)[§](https://postgr.es/c/286a365b9)

Isso adiciona a capacidade de realizar mapeamento condicional e maiúsculas e minúsculas, e mapear caracteres únicos em caracteres múltiplos.
* Permita que os valores `jsonb`(datatype-json.md "8.14. JSON Types") `null` sejam convertidos em tipos escalares como `NULL` (Tom Lane) [§](https://postgr.es/c/a5579a90a)

Anteriormente, tais casts geravam um erro.
* Adicione o parâmetro opcional a `json{b}_strip_nulls` para permitir a remoção de elementos de matriz nulos (Florents Tselai) [§](https://postgr.es/c/4603903d2)
* Adicione a função `array_sort()` que ordena a primeira dimensão de uma matriz (Junwang Zhao, Jian He) [§](https://postgr.es/c/6c12ae09f)
* Adicione a função `array_reverse()` que inverte a primeira dimensão de uma matriz (Aleksander Alekseev) [§](https://postgr.es/c/49d6c7d8d)
* Adicione a função `reverse()` para reverter bytes de bytea (Aleksander Alekseev) [§](https://postgr.es/c/0697b2390)
* Permita a conversão entre tipos de inteiro e `bytea` (Aleksander Alekseev) [§](https://postgr.es/c/6da469bad)

Os valores inteiros são armazenados como valores de complemento de dois `bytea`.
* Atualize os dados Unicode para [Unicode](collation.md#COLLATION-MANAGING-STANDARD "23.2.2.1. Standard Collations") 16.0.0 (Peter Eisentraut) [§](https://postgr.es/c/82a46cca9)
* Adicione a pesquisa de texto completo [stemming](textsearch-dictionaries.md#TEXTSEARCH-SNOWBALL-DICTIONARY "12.6.6. Snowball Dictionary") para o estoniano (Tom Lane) [§](https://postgr.es/c/b464e51ab)
* Melhore os códigos de erro [`XML`](datatype-xml.md) para se alinhar mais de perto ao padrão SQL (Tom Lane) [§](https://postgr.es/c/cd838e200)

Esses erros são relatados em `SQLSTATE`(errcodes-appendix.md "Appendix A. PostgreSQL Error Codes").

#### E.5.3.4. Funções [#](#RELEASE-18-FUNCTIONS)

* Adicione a função `casefold()`(functions-string.md#FUNCTIONS-STRING-OTHER "Table 9.10. Other String Functions and Operators") para permitir uma correspondência mais sofisticada, não sensível a maiúsculas e minúsculas (Jeff Davis) [§](https://postgr.es/c/bfc599206)

Isso permite comparações mais precisas, ou seja, um caractere pode ter múltiplos equivalentes em maiúsculas ou minúsculas, ou a conversão de maiúsculas e minúsculas altera o número de caracteres.
* Permitir agregados `MIN()`(functions-aggregate.md#FUNCTIONS-AGGREGATE-TABLE "Table 9.62. General-Purpose Aggregate Functions")/[`MAX()`(functions-aggregate.md#FUNCTIONS-AGGREGATE-TABLE "Table 9.62. General-Purpose Aggregate Functions") em matrizes e tipos compostos (Aleksander Alekseev, Marat Buharov) [§](https://postgr.es/c/a0f1fce80) [§](https://postgr.es/c/2d24fd942)
* Adicionar uma opção `WEEK` para [`EXTRACT()`(functions-datetime.md#FUNCTIONS-DATETIME-EXTRACT "9.9.1. EXTRACT, date_part") (Tom Lane) [§](https://postgr.es/c/6be39d77a)
* Melhorar a saída `EXTRACT(QUARTER ...)` para valores negativos (Tom Lane) [§](https://postgr.es/c/6be39d77a)
* Adicionar suporte a numerais romanos para [`to_number()`(functions-formatting.md#FUNCTIONS-FORMATTING-TABLE "Table 9.26. Formatting Functions") (Hunaid Sohail) [§](https://postgr.es/c/172e6b3ad)

Isso é acessado através do padrão `RN`.
* Adicione a função de geração da versão 7 `UUID`(datatype-uuid.md "8.12. UUID Type") `uuidv7()`(functions-uuid.md#FUNC_UUID_GEN_TABLE "Table 9.45. UUID Generation Functions") (Andrey Borodin) [§](https://postgr.es/c/78c5e141e)

Este valor `UUID` é temporariamente ordenável. A função alias (functions-uuid.md#FUNC_UUID_GEN_TABLE "Table 9.45. UUID Generation Functions") foi adicionada para gerar explicitamente UUIDs da versão 4. * Adicione as funções `crc32()` e (functions-binarystring.md#FUNCTIONS-BINARYSTRING-OTHER "Table 9.12. Other Binary String Functions") e `crc32c()` e (functions-binarystring.md#FUNCTIONS-BINARYSTRING-OTHER "Table 9.12. Other Binary String Functions") para calcular os valores do CRC (Aleksander Alekseev) [§](https://postgr.es/c/760162fed) * Adicione as funções matemáticas `gamma()` e `lgamma()` (Dean Rasheed) [§](https://postgr.es/c/a3b6dfd41) * Permita a sintaxe `=>` para argumentos de cursor nomeados em [PL/pgSQL](plpgsql.md "Chapter 41. PL/pgSQL — SQL Procedural Language") (Pavel Stehule) [§](https://postgr.es/c/246dedc5d)

Anteriormente, só aceitávamos `:=`.
* Permita que `regexp_match[es][[PH_LNK_605]]`/`regexp_like()`/[[`regexp_replace()`]/`regexp_count()`/[[`regexp_instr()`]/`regexp_substr()`/`regexp_split_to_table()`/`regexp_split_to_array()` use argumentos nomeados (Jian He) [§](https://postgr.es/c/580f8727c)

#### E.5.3.5. [Libpq](libpq.md) [#](#RELEASE-18-LIBPQ)

* Adicione a função `PQfullProtocolVersion()` (libpq-status.md#LIBPQ-PQFULLPROTOCOLVERSION) para relatar o número completo do protocolo, incluindo o menor, da versão (Jacob Champion, Jelte Fennema-Nio) [§](https://postgr.es/c/cdb6b0fdb)
* Adicione o parâmetro de conexão libpq [parâmetros](libpq-connect.md#LIBPQ-CONNECT-SSL-MAX-PROTOCOL-VERSION) e [variáveis de ambiente](libpq-envars.md) para especificar a versão mínima e máxima aceitável do protocolo para conexões (Jelte Fennema-Nio) [§](https://postgr.es/c/285613c60) [§](https://postgr.es/c/507034910)
* Relate as mudanças no [caminho de pesquisa](runtime-config-client.md#GUC-SEARCH-PATH) ao cliente (Alexander Kukushkin, Jelte Fennema-Nio, Tomas Vondra) [§](https://postgr.es/c/28a1121fd) [§](https://postgr.es/c/0d06a7eac)
* Adicione a saída [`PQtrace()` (libpq-control.md#LIBPQ-PQTRACE) para todos os tipos de mensagem, incluindo autenticação (Jelte Fennema-Nio) [§](https://postgr.es/c/ea92f3a0a) [§](https://postgr.es/c/a5c6b8f22) [§](https://postgr.es/c/b8b3f861f) [§](https://postgr.es/c/e87c14b19) [§](https://postgr.es/c/7adec2d5f)
* Adicione o parâmetro de conexão libpq [`sslkeylogfile` ](libpq-connect.md#LIBPQ-CONNECT-SSLKEYLOGFILE) que exibe o material da chave SSL (Abhishek Chanda, Daniel Gustafsson) [§](https://postgr.es/c/2da74d8d6)

Isso é útil para depuração.
* Modifique algumas assinaturas de funções do libpq para usar `int64_t` (Thomas Munro) [§](https://postgr.es/c/3c86223c9)

Esses anteriormente utilizados `pg_int64`, que agora estão desatualizados.

#### E.5.3.6. [psql](app-psql.md "psql") [#](#RELEASE-18-PSQL)

* Permita que o psql parse, vincule e feche instruções preparadas nomeadas (Anthonin Bonnefoy, Michael Paquier) [§](https://postgr.es/c/d55322b0d) [§](https://postgr.es/c/fc39b286a)

Isso é feito com novos comandos `\parse` (app-psql.md#APP-PSQL-META-COMMAND-PARSE), `\bind_named` (app-psql.md#APP-PSQL-META-COMMAND-BIND-NAMED) e `\close_prepared` (app-psql.md#APP-PSQL-META-COMMAND-CLOSE-PREPARED).
* Adicione comandos de psql com barra invertida para permitir a emissão de consultas de pipeline (Anthonin Bonnefoy) [§](https://postgr.es/c/41625ab8e) [§](https://postgr.es/c/17caf6644) [§](https://postgr.es/c/2cce0fe44)

Os novos comandos são `\startpipeline`, (app-psql.md#APP-PSQL-META-COMMAND-PIPELINE), `\syncpipeline`, `\sendpipeline`, `\endpipeline`, `\flushrequest`, `\flush` e `\getresults`.
* Permita adicionar o status do pipeline ao prompt do psql e adicione variáveis de estado relacionadas (Anthonin Bonnefoy) [§](https://postgr.es/c/3ce357584)

O novo caractere de prompt é `%P` e as novas variáveis do psql são (app-psql.md#APP-PSQL-VARIABLES-PIPELINE-SYNC-COUNT), `PIPELINE_COMMAND_COUNT` e (app-psql.md#APP-PSQL-VARIABLES-PIPELINE-RESULT-COUNT).
* Permita adicionar o nome do serviço de conexão ao prompt do psql ou acedê-lo através da variável do psql (Michael Banck) [§](https://postgr.es/c/477728b5d)
* Adicione a opção do psql para usar o modo expandido em todos os comandos da lista (Dean Rasheed) [§](https://postgr.es/c/00f4c2959)

Adicionar o sufixo barra invertida `x` permite isso.
* Alterar [`\conninfo`](app-psql.md#APP-PSQL-META-COMMAND-CONNINFO) de psql para usar o formato tabular e incluir mais informações (Álvaro Herrera, Maiquel Grassi, Hunaid Sohail) [§](https://postgr.es/c/bba2fbc62)
* Adicionar o indicador de vazamento da função ao [`\df+`](app-psql.md#APP-PSQL-META-COMMAND-DF-LC), `\do+`, `\dAo+` e `\dC+` de psql (Yugo Nagata) [§](https://postgr.es/c/2355e5111)
* Adicionar detalhes do método de acesso para relações particionadas em [`\dP+`](app-psql.md#APP-PSQL-META-COMMAND-DP-UC) (Justin Pryzby) [§](https://postgr.es/c/978f38c77)
* Adicionar `default_version` à saída da extensão psql [`\dx`](app-psql.md#APP-PSQL-META-COMMAND-DX-LC) (Magnus Hagander) [§](https://postgr.es/c/d696406a9)
* Adicionar a variável psql [`WATCH_INTERVAL`](app-psql.md#APP-PSQL-VARIABLES-WATCH-INTERVAL) para definir o tempo de espera padrão [`\watch`](app-psql.md#APP-PSQL-META-COMMAND-WATCH) (Daniel Gustafsson) [§](https://postgr.es/c/1a759c832)

#### E.5.3.7. Aplicações de servidor [#](#RELEASE-18-SERVER-APPS)

* Altere [initdb](app-initdb.md) para permitir o cálculo de verificações (Greg Sabino Mullane) [§](https://postgr.es/c/983a588e0) [§](https://postgr.es/c/04bec894a)

A nova opção de initdb `--no-data-checksums` desativa os checksums.
* Adicione a opção de initdb `--no-sync-data-files` para evitar a sincronização dos arquivos de heap/index (Nathan Bossart) [§](https://postgr.es/c/cf131fa94)

A opção `--no-sync` de initdb ainda está disponível para evitar a sincronização de quaisquer arquivos. Adicione a opção (app-vacuumdb.md "vacuumdb") [`--missing-stats-only`] para calcular apenas as estatísticas do otimizador ausentes (Corey Huinker, Nathan Bossart) [§](https://postgr.es/c/edba754f0) [§](https://postgr.es/c/987910502)

Essa opção só pode ser executada por superusuários e só pode ser usada com as opções `--analyze-only` e `--analyze-in-stages`.
* Adicione a opção [pg_combinebackup](app-pgcombinebackup.md "pg_combinebackup") `-k`/`--link` para habilitar o linkeamento rígido (Israel Barth Rubio, Robert Haas) [§](https://postgr.es/c/99aeb8470)

Apenas alguns arquivos podem ser vinculados diretamente. Isso não deve ser usado se os backups forem utilizados de forma independente.
* Permita que [pg_verifybackup](app-pgverifybackup.md) verifique backups no formato tar (Amul Sul) [§](https://postgr.es/c/8dfd31290)
* Se o `--source-server` do [pg_rewind](app-pgrewind.md) especificar um nome de banco de dados, use-o na saída do `--write-recovery-conf` (Masahiko Sawada) [§](https://postgr.es/c/4ecdd4110)
* Adicione a opção [pg_resetwal](app-pgresetwal.md) ao `--char-signedness` para alterar a assinatura padrão do `char` (Masahiko Sawada) [§](https://postgr.es/c/30666d185)

##### E.5.3.7.1. [[pg_dump]] (app-pgdump.md "pg_dump")/[pg_dumpall] (app-pg-dumpall.md "pg_dumpall")/[pg_restore] (app-pgrestore.md "pg_restore") [#][(#RELEASE-18-PGDUMP)

* Adicione a opção [pg_dump](app-pgdump.md "pg_dump") `--statistics` (Jeff Davis) [§](https://postgr.es/c/bde2fb797) [§](https://postgr.es/c/a3e8dc143)
* Adicione as opções pg_dump e [pg_dumpall](app-pg-dumpall.md "pg_dumpall") para drenar dados de sequência que normalmente seriam excluídos (Nathan Bossart) [§](https://postgr.es/c/9c49f0e8c) [§](https://postgr.es/c/acea3fc49)
* Adicione as opções [pg_dump](app-pgdump.md "pg_dump"), [pg_dumpall](app-pg-dumpall.md "pg_dumpall"), e [pg_restore](app-pgrestore.md "pg_restore") `--statistics-only`, `--no-statistics`, `--no-data`, e `--no-schema` (Corey Huinker, Jeff Davis) [§](https://postgr.es/c/1fd1bd871)
* Adicione a opção `--no-policies` para desativar o processamento da política de segurança de nível de linha em [pg_dump](app-pgdump.md "pg_dump"), [pg_dumpall](app-pg-dumpall.md "pg_dumpall"), [pg_restore](app-pgrestore.md "pg_restore") (Nikolay Samokhvalov) [§](https://postgr.es/c/cd3c45125)

Isso é útil para migrar para sistemas com políticas diferentes.

##### E.5.3.7.2.  [pg_upgrade](pgupgrade.md) [#](#RELEASE-18-PGUPGRADE)

* Permita que o pg_upgrade preserve as estatísticas do otimizador (Corey Huinker, Jeff Davis, Nathan Bossart) [§](https://postgr.es/c/1fd1bd871) [§](https://postgr.es/c/c9d502eb6) [§](https://postgr.es/c/d5f1b6a75) [§](https://postgr.es/c/1fd1bd871)

As estatísticas estendidas não são preservadas. Adicione também a opção `--no-statistics` do pg_upgrade para desativar a preservação das estatísticas.
* Permita que o pg_upgrade processe os verificações do banco de dados em paralelo (Nathan Bossart) [§](https://postgr.es/c/40e2e5e92)[§](https://postgr.es/c/6d3d2e8e5)[§](https://postgr.es/c/7baa36de5)[§](https://postgr.es/c/46cad8b31)[§](https://postgr.es/c/6ab8f27bc)[§](https://postgr.es/c/bbf83cab9)[§](https://postgr.es/c/9db3018cf)[§](https://postgr.es/c/c34eabfbb)[§](https://postgr.es/c/cf2f82a37)[§][(https://postgr.es/c/f93f5f7b9)[§][(https://postgr.es/c/c880cf258)

Isso é controlado pela opção existente `--jobs`.
* Adicione a opção pg_upgrade `--swap` para trocar diretórios em vez de copiar, clonar ou vincular arquivos (Nathan Bossart) [§](https://postgr.es/c/626d7236b)

Esse modo é potencialmente o mais rápido.
* Adicione a opção pg_upgrade `--set-char-signedness` para definir a assinatura `char` padrão do novo clúster (Masahiko Sawada) [§](https://postgr.es/c/a8238f87f) [§](https://postgr.es/c/1aab68059)

Isto é para lidar com casos em que a assinatura de CPU padrão de um cluster pré-PostgreSQL 18 não corresponde ao novo cluster.

##### E.5.3.7.3. Aplicações de Replicação Lógica [#](#RELEASE-18-LOGICALREP-APP)

* Adicione a opção [pg_createsubscriber](app-pgcreatesubscriber.md) `--all` para criar réplicas lógicas para todos os bancos de dados (Shubham Khanna) [§](https://postgr.es/c/fb2ea12f4)
* Adicione a opção pg_createsubscriber `--clean` para remover publicações (Shubham Khanna) [§](https://postgr.es/c/e5aeed4b8) [§](https://postgr.es/c/60dda7bbc)
* Adicione a opção pg_createsubscriber `--enable-two-phase` para habilitar transações preparadas (Shubham Khanna) [§](https://postgr.es/c/e117cfb2f)
* Adicione a opção [pg_recvlogical](app-pgrecvlogical.md) `--enable-failover` para especificar slots de falha (Hayato Kuroda) [§](https://postgr.es/c/cf2655a90)

Adicione também a opção `--enable-two-phase` como sinônimo de `--two-phase`, e desconsidere esta última.
* Permita que o pg_recvlogical `--drop-slot` funcione sem `--dbname` (Hayato Kuroda) [§](https://postgr.es/c/c68100aa4)

#### E.5.3.8. Código-fonte [#](#RELEASE-18-SOURCE-CODE)

* Separe a carga e a execução dos pontos de [injeção](xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS) (Michael Paquier, Heikki Linnakangas) [§](https://postgr.es/c/4b211003e) [§](https://postgr.es/c/a0a5869a8)

Os pontos de injeção podem agora ser criados, mas não executados, via `INJECTION_POINT_LOAD()`(xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS "36.10.14. Injection Points"), e tais pontos de injeção podem ser executados via `INJECTION_POINT_CACHED()`(xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS "36.10.14. Injection Points").
* Suporte a argumentos de execução em pontos de injeção (Michael Paquier) [§](https://postgr.es/c/371f2db8b)
* Permitir código de teste de ponto de injeção inline com `IS_INJECTION_POINT_ATTACHED()`(xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS "36.10.14. Injection Points") (Heikki Linnakangas) [§](https://postgr.es/c/20e0e7da9)
* Melhorar o desempenho do processamento de strings longas `JSON`(datatype-json.md "8.14. JSON Types") usando SIMD (Single Instruction Multiple Data) (David Rowley) [§](https://postgr.es/c/ca6fde922)
* Acelerar os cálculos de CRC32C usando instruções x86 AVX-512 (Raghuveer Devulapalli, Paul Amonson) [§](https://postgr.es/c/3c6e8c123)
* Adicionar intrínsecos para CPU ARM Neon e SVE para popcount (contagem de bits inteiros) (Chiranmoy Bhattacharya, Devanga Susmitha, Rama Malladi) [§](https://postgr.es/c/6be53c276) [§](https://postgr.es/c/519338ace)
* Melhorar a velocidade da multiplicação e divisão numérica (Joel Jacobson, Dean Rasheed) [§](https://postgr.es/c/ca481d3c9) [§](https://postgr.es/c/c4e44224c) [§](https://postgr.es/c/8dc28d7eb) [§](https://postgr.es/c/9428c001f)
* Adicionar opção de configuração `--with-libnuma`(install-make.md#CONFIGURE-OPTION-WITH-LIBNUMA) para habilitar a consciência NUMA (Jakub Wartak, Bertrand Drouvot) [§](https://postgr.es/c/65c298f61) [§](https://postgr.es/c/8cc139bec) [§](https://postgr.es/c/ba2a3c230)

A função `pg_numa_available()`(functions-info.md#FUNCTIONS-INFO-SESSION-TABLE "Table 9.71. Session Information Functions") relata a consciência NUMA, e as visões do sistema `pg_shmem_allocations_numa`(view-pg-shmem-allocations-numa.md "53.28. pg_shmem_allocations_numa") e [`pg_buffercache_numa`](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-NUMA) que relatam a distribuição da memória compartilhada em nós NUMA.
* Adicione a tabela [TOAST](storage-toast.md "66.2. TOAST") ao [`pg_index`](catalog-pg-index.md) para permitir índices de expressão muito grandes (Nathan Bossart) [§](https://postgr.es/c/b52c4fc3c)
* Remova a coluna [`pg_attribute`](catalog-pg-attribute.md).`attcacheoff` (David Rowley) [§](https://postgr.es/c/02a8d0c45)
* Adicione a coluna [`pg_class`](catalog-pg-class.md).`relallfrozen` (Melanie Plageman) [§](https://postgr.es/c/99f8f3fbb)
* Adicione [`amgettreeheight`](indexam.md), `amconsistentequality`, e `amconsistentordering` ao método de acesso ao índice API (Mark Dilger) [§](https://postgr.es/c/56fead44d) [§](https://postgr.es/c/af4002b38)
* Adicione a função de suporte GiST [`stratnum()`(gist.md#GIST-EXTENSIBILITY "65.2.3. Extensibility") (Paul A. Jungwirth) [§](https://postgr.es/c/7406ab623)
* Registre a assinatura de CPU padrão de `char` em [pg_controldata](app-pgcontroldata.md "pg_controldata") (Masahiko Sawada) [§](https://postgr.es/c/44fe30fda)
* Adicione suporte para a API "Limpida" do Python em [PL/Python](plpython.md "Chapter 44. PL/Python — Python Procedural Language") (Peter Eisentraut) [§](https://postgr.es/c/72a3d0462) [§](https://postgr.es/c/0793ab810)

Isso ajuda a prevenir problemas causados por desalinhamentos entre as versões do Python 3.x.
* Altere a versão mínima de Python suportada para 3.6.8 (Jacob Champion) [§](https://postgr.es/c/45363fca6)
* Remova o suporte para versões do OpenSSL mais antigas do que 1.1.1 (Daniel Gustafsson) [§](https://postgr.es/c/a70e01d43) [§](https://postgr.es/c/6c66b7443)
* Se o LLVM estiver habilitado, exija versão 14 ou posterior (Thomas Munro) [§](https://postgr.es/c/972c2cd28)
* Adicione a macro [`PG_MODULE_MAGIC_EXT`](functions-info.md "9.27. System Information Functions and Operators") para permitir que as extensões relatem seu nome e versão (Andrei Lepikhov) [§](https://postgr.es/c/9324c8c58)

Essa informação pode ser acessada através da nova função `pg_get_loaded_modules()`(functions-info.md#FUNCTIONS-INFO-SESSION-TABLE "Table 9.71. Session Information Functions").
* O documento que [`SPI_connect()`(spi-spi-connect.md "SPI_connect")/[`SPI_connect_ext()`(spi-spi-connect.md "SPI_connect")]] sempre retorna sucesso (`SPI_OK_CONNECT`) (Stepan Neretin) [§](https://postgr.es/c/218527d01)

Os erros são sempre relatados via `ereport()`.
* Adicione [seção de documentação](xfunc-c.md#XFUNC-API-ABI-STABILITY-GUIDANCE "36.10.6. Server API and ABI Stability Guidance") sobre compatibilidade da API e ABI (David Wheeler, Peter Eisentraut) [§](https://postgr.es/c/e54a42ac9)
* Remova a designação experimental dos builds do Meson no Windows (Aleksander Alekseev) [§](https://postgr.es/c/5afaba629)
* Remova as opções de configuração `--disable-spinlocks` e `--disable-atomics` (Thomas Munro) [§](https://postgr.es/c/e25626677) [§](https://postgr.es/c/813852613)

Agora são necessárias operações atômicas de 32 bits.
* Remova o suporte para a arquitetura HPPA/PA-RISC (Tom Lane) [§](https://postgr.es/c/edadeb071)

#### E.5.3.9. Módulos adicionais [#](#RELEASE-18-MODULES)

* Adicione a extensão [pg_logicalinspect](pglogicalinspect.md) para inspecionar instantâneos lógicos (Bertrand Drouvot) [§](https://postgr.es/c/7cdfeee32)
* Adicione a extensão [pg_overexplain](pgoverexplain.md) que adiciona detalhes de depuração ao [`EXPLAIN`](sql-explain.md) de saída (Robert Haas) [§](https://postgr.es/c/8d5ceb113)
* Adicione colunas de saída ao [`postgres_fdw_get_connections()`](postgres-fdw.md#POSTGRES-FDW-FUNCTIONS) (Hayato Kuroda, Sagar Dilip Shedge) [§](https://postgr.es/c/c297a47c5) [§](https://postgr.es/c/857df3cef) [§](https://postgr.es/c/4f08ab554) [§](https://postgr.es/c/fe186bda7)

A nova coluna de saída `used_in_xact` indica se o revestimento de dados estrangeiro está sendo usado por uma transação atual, `closed` indica se ele está fechado, `user_name` indica o nome do usuário e `remote_backend_pid` indica o identificador do processo de backend remoto.
* Permita que a autenticação [SCRAM](auth-password.md "20.5. Password Authentication") do cliente seja passada para os servidores [postgres_fdw](postgres-fdw.md "F.38. postgres_fdw — access data stored in external PostgreSQL servers") (Matheus Alcantara, Peter Eisentraut) [§](https://postgr.es/c/761c79508)

Isso evita armazenar as informações de autenticação postgres_fdw no banco de dados e é habilitado com a opção de conexão postgres_fdw `use_scram_passthrough`(postgres-fdw.md#POSTGRES-FDW-OPTION-USE-SCRAM-PASSTHROUGH). O libpq usa novos parâmetros de conexão [scram_client_key](libpq-connect.md#LIBPQ-CONNECT-SCRAM-CLIENT-KEY) e [scram_server_key](libpq-connect.md#LIBPQ-CONNECT-SCRAM-SERVER-KEY).
* Permita que a autenticação SCRAM do cliente seja passada para os servidores [dblink](dblink.md "F.11. dblink — connect to other PostgreSQL databases") (Matheus Alcantara) [§](https://postgr.es/c/3642df265)
* Adicione as opções `on_error` e `log_verbosity` ao [file_fdw](file-fdw.md "F.15. file_fdw — access data files in the server's file system") (Atsushi Torikoshi) [§](https://postgr.es/c/a1c4c8a9e)

Esses controles determinam como o file_fdw lida e reporta linhas de arquivo inválidas.
* Adicione `reject_limit` para controlar o número de linhas de arquivo inválidas que o file_fdw pode ignorar (Atsushi Torikoshi) [§](https://postgr.es/c/6c8f67032)

Isso é ativo quando `ON_ERROR = 'ignore'`.
* Adicione a variável configurável `min_password_length` ao [passwordcheck](passwordcheck.md "F.24. passwordcheck — verify password strength") (Emanuele Musella, Maurizio Boriani) [§](https://postgr.es/c/f7e1b3828)

Isso controla o comprimento mínimo da senha.
* Faça com que [pgbench](pgbench.md) informe o número de transações que falharam, foram repetidas ou ignoradas em relatórios por script (Yugo Nagata) [§](https://postgr.es/c/cae0f3c40)
* Adicione a variável de servidor [isn](isn.md)] `weak` para controlar a aceitação de dígito de verificação inválido (Viktor Holmberg) [§](https://postgr.es/c/448904423)

Isso era anteriormente controlado apenas pela função `isn_weak()`.
* Permita que os valores sejam ordenados para acelerar a construção do índice de [btree_gist](btree-gist.md) (Bernd Helmle, Andrey Borodin) [§](https://postgr.es/c/e4309f73f)
* Adicione a função de verificação [amcheck](amcheck.md) `gin_index_check()` (amcheck.md#AMCHECK-FUNCTIONS "F.1.1. Functions") para verificar os índices `GIN` (Grigory Kryachko, Heikki Linnakangas, Andrey Borodin) [§](https://postgr.es/c/14ffaece0)
* Adicione as funções `pg_buffercache_evict_relation()` e `pg_buffercache_evict_all()` Function") para expulsar buffers compartilhados não marcados (Nazir Bilal Yavuz) [§](https://postgr.es/c/dcf7e1697)

A função existente `pg_buffercache_evict()` Function]") agora retorna o status de esvaziamento do buffer. * Permita que extensões instalem opções personalizadas de [EXPLAIN](sql-explain.md) (Robert Haas, Sami Imseih) [§](https://postgr.es/c/c65bc2e1d) [§](https://postgr.es/c/4fd02bf7c) [§](https://postgr.es/c/50ba65e73) * Permita que extensões usem a API de estatísticas acumuladas do servidor (Michael Paquier) [§](https://postgr.es/c/7949d9594) [§](https://postgr.es/c/2eff9e678)

##### E.5.3.9.1. [[pg_stat_statements]] (pgstatstatements.md "F.32. pg_stat_statements — track statistics of SQL planning and execution") [#](#RELEASE-18-PGSTATSTATEMENTS)

* Permita que as consultas de [CREATE TABLE AS](sql-createtableas.md "CREATE TABLE AS") e [DECLARE](sql-declare.md "DECLARE") sejam rastreadas pelo pg_stat_statements (Anthonin Bonnefoy) [§](https://postgr.es/c/6b652e6ce)

Eles também agora recebem IDs de consulta.
* Permita a parametrização dos valores de [SET](sql-set.md "SET") em pg_stat_statements (Greg Sabino Mullane, Michael Paquier) [§](https://postgr.es/c/dc6851596)

Isso reduz o inchaço causado por declarações `SET` com constantes diferentes.
* Adicione as colunas `pg_stat_statements`(pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS "F.32.1. The pg_stat_statements View") para relatar atividade paralela (Guillaume Lelarge) [§](https://postgr.es/c/cf54a2c00)

As novas colunas são `parallel_workers_to_launch` e `parallel_workers_launched`.
* Adicione `pg_stat_statements`.`wal_buffers_full` para relatar buffers completos do WAL (Bertrand Drouvot) [§](https://postgr.es/c/ce5bcc4a9)

##### E.5.3.9.2. [[pgcrypto]] (pgcrypto.md "F.26. pgcrypto — cryptographic functions") [#](#RELEASE-18-PGCRYPTO)

* Adicione os algoritmos de criptografia pgcrypto `sha256crypt`](pgcrypto.md#PGCRYPTO-CRYPT-ALGORITHMS "Table F.18. Supported Algorithms for crypt()") e [`sha512crypt`](pgcrypto.md#PGCRYPTO-CRYPT-ALGORITHMS "Table F.18. Supported Algorithms for crypt()") (Bernd Helmle) [§](https://postgr.es/c/749a9e20c)
* Adicione o modo [CFB](pgcrypto.md#PGCRYPTO-RAW-ENC-FUNCS "F.26.4. Raw Encryption Functions") à criptografia e descriptografia de pgcrypto (Umar Hayat) [§](https://postgr.es/c/9ad1b3d01)
* Adicione a função [`fips_mode()`](pgcrypto.md#PGCRYPTO-OPENSSL-SUPPORT-FUNCS "F.26.6. OpenSSL Support Functions") para relatar o modo FIPS do servidor (Daniel Gustafsson) [§](https://postgr.es/c/924d89a35)
* Adicione a variável de servidor pgcrypto [`builtin_crypto_enabled`](pgcrypto.md#PGCRYPTO-CONFIGURATION-PARAMETERS-BUILTIN_CRYPTO_ENABLED) para permitir a desativação de funções criptográficas não FIPS embutidas (Daniel Gustafsson, Joe Conway) [§](https://postgr.es/c/035f99cbe)

Isso é útil para garantir o comportamento do modo FIPS.

### E.5.4. Reconhecimento [#](#RELEASE-18-ACKNOWLEDGEMENTS)

As seguintes pessoas (em ordem alfabética) contribuíram para esta versão como autores de patches, committers, revisores, testadores ou relatores de problemas.



<table>
 <tr>
  <td>
   Abhishek Chanda
  </td>
 </tr>
 <tr>
  <td>
   Adam Guo
  </td>
 </tr>
 <tr>
  <td>
   Adam Rauch
  </td>
 </tr>
 <tr>
  <td>
   Aidar Imamov
  </td>
 </tr>
 <tr>
  <td>
   Ajin Cherian
  </td>
 </tr>
 <tr>
  <td>
   Alastair Turner
  </td>
 </tr>
 <tr>
  <td>
   Alec Cozens
  </td>
 </tr>
 <tr>
  <td>
   Aleksander Alekseev
  </td>
 </tr>
 <tr>
  <td>
   Alena Rybakina
  </td>
 </tr>
 <tr>
  <td>
   Alex Friedman
  </td>
 </tr>
 <tr>
  <td>
   Alex Richman
  </td>
 </tr>
 <tr>
  <td>
   Alexander Alehin
  </td>
 </tr>
 <tr>
  <td>
   Alexander Borisov
  </td>
 </tr>
 <tr>
  <td>
   Alexander Korotkov
  </td>
 </tr>
 <tr>
  <td>
   Alexander Kozhemyakin
  </td>
 </tr>
 <tr>
  <td>
   Alexander Kukushkin
  </td>
 </tr>
 <tr>
  <td>
   Alexander Kuzmenkov
  </td>
 </tr>
 <tr>
  <td>
   Alexander Kuznetsov
  </td>
 </tr>
 <tr>
  <td>
   Alexander Lakhin
  </td>
 </tr>
 <tr>
  <td>
   Alexander Pyhalov
  </td>
 </tr>
 <tr>
  <td>
   Alexandra Wang
  </td>
 </tr>
 <tr>
  <td>
   Alexey Dvoichenkov
  </td>
 </tr>
 <tr>
  <td>
   Alexey Makhmutov
  </td>
 </tr>
 <tr>
  <td>
   Alexey Shishkin
  </td>
 </tr>
 <tr>
  <td>
   Ali Akbar
  </td>
 </tr>
 <tr>
  <td>
   Álvaro Herrera
  </td>
 </tr>
 <tr>
  <td>
   Álvaro Mongil
  </td>
 </tr>
 <tr>
  <td>
   Amit Kapila
  </td>
 </tr>
 <tr>
  <td>
   Amit Langote
  </td>
 </tr>
 <tr>
  <td>
   Amul Sul
  </td>
 </tr>
 <tr>
  <td>
   Andreas Karlsson
  </td>
 </tr>
 <tr>
  <td>
   Andreas Scherbaum
  </td>
 </tr>
 <tr>
  <td>
   Andreas Ulbrich
  </td>
 </tr>
 <tr>
  <td>
   Andrei Lepikhov
  </td>
 </tr>
 <tr>
  <td>
   Andres Freund
  </td>
 </tr>
 <tr>
  <td>
   Andrew
  </td>
 </tr>
 <tr>
  <td>
   Andrew Bille
  </td>
 </tr>
 <tr>
  <td>
   Andrew Dunstan
  </td>
 </tr>
 <tr>
  <td>
   Andrew Jackson
  </td>
 </tr>
 <tr>
  <td>
   Andrew Kane
  </td>
 </tr>
 <tr>
  <td>
   Andrew Watkins
  </td>
 </tr>
 <tr>
  <td>
   Andrey Borodin
  </td>
 </tr>
 <tr>
  <td>
   Andrey Chudnovsky
  </td>
 </tr>
 <tr>
  <td>
   Andrey Rachitskiy
  </td>
 </tr>
 <tr>
  <td>
   Andrey Rudometov
  </td>
 </tr>
 <tr>
  <td>
   Andy Alsup
  </td>
 </tr>
 <tr>
  <td>
   Andy Fan
  </td>
 </tr>
 <tr>
  <td>
   Anthonin Bonnefoy
  </td>
 </tr>
 <tr>
  <td>
   Anthony Hsu
  </td>
 </tr>
 <tr>
  <td>
   Anthony Leung
  </td>
 </tr>
 <tr>
  <td>
   Anton Melnikov
  </td>
 </tr>
 <tr>
  <td>
   Anton Voloshin
  </td>
 </tr>
 <tr>
  <td>
   Antonin Houska
  </td>
 </tr>
 <tr>
  <td>
   Antti Lampinen
  </td>
 </tr>
 <tr>
  <td>
   Arseniy Mukhin
  </td>
 </tr>
 <tr>
  <td>
   Artur Zakirov
  </td>
 </tr>
 <tr>
  <td>
   Arun Thirupathi
  </td>
 </tr>
 <tr>
  <td>
   Ashutosh Bapat
  </td>
 </tr>
 <tr>
  <td>
   Asphator
  </td>
 </tr>
 <tr>
  <td>
   Atsushi Torikoshi
  </td>
 </tr>
 <tr>
  <td>
   Avi Weinberg
  </td>
 </tr>
 <tr>
  <td>
   Aya Iwata
  </td>
 </tr>
 <tr>
  <td>
   Ayush Tiwari
  </td>
 </tr>
 <tr>
  <td>
   Ayush Vatsa
  </td>
 </tr>
 <tr>
  <td>
   Bastien Roucariès
  </td>
 </tr>
 <tr>
  <td>
   Ben Peachey Higdon
  </td>
 </tr>
 <tr>
  <td>
   Benoit Lobréau
  </td>
 </tr>
 <tr>
  <td>
   Bernd Helmle
  </td>
 </tr>
 <tr>
  <td>
   Bernd Reiß
  </td>
 </tr>
 <tr>
  <td>
   Bernhard Wiedemann
  </td>
 </tr>
 <tr>
  <td>
   Bertrand Drouvot
  </td>
 </tr>
 <tr>
  <td>
   Bertrand Mamasam
  </td>
 </tr>
 <tr>
  <td>
   Bharath Rupireddy
  </td>
 </tr>
 <tr>
  <td>
   Bogdan Grigorenko
  </td>
 </tr>
 <tr>
  <td>
   Boyu Yang
  </td>
 </tr>
 <tr>
  <td>
   Braulio Fdo Gonzalez
  </td>
 </tr>
 <tr>
  <td>
   Bruce Momjian
  </td>
 </tr>
 <tr>
  <td>
   Bykov Ivan
  </td>
 </tr>
 <tr>
  <td>
   Cameron Vogt
  </td>
 </tr>
 <tr>
  <td>
   Cary Huang
  </td>
 </tr>
 <tr>
  <td>
   Cédric Villemain
  </td>
 </tr>
 <tr>
  <td>
   Cees van Zeeland
  </td>
 </tr>
 <tr>
  <td>
   ChangAo Chen
  </td>
 </tr>
 <tr>
  <td>
   Chao Li
  </td>
 </tr>
 <tr>
  <td>
   Chapman Flack
  </td>
 </tr>
 <tr>
  <td>
   Charles Samborski
  </td>
 </tr>
 <tr>
  <td>
   Chengwen Wu
  </td>
 </tr>
 <tr>
  <td>
   Chengxi Sun
  </td>
 </tr>
 <tr>
  <td>
   Chiranmoy Bhattacharya
  </td>
 </tr>
 <tr>
  <td>
   Chris Gooch
  </td>
 </tr>
 <tr>
  <td>
   Christian Charukiewicz
  </td>
 </tr>
 <tr>
  <td>
   Christoph Berg
  </td>
 </tr>
 <tr>
  <td>
   Christophe Courtois
  </td>
 </tr>
 <tr>
  <td>
   Christopher Inokuchi
  </td>
 </tr>
 <tr>
  <td>
   Clemens Ruck
  </td>
 </tr>
 <tr>
  <td>
   Corey Huinker
  </td>
 </tr>
 <tr>
  <td>
   Craig Milhiser
  </td>
 </tr>
 <tr>
  <td>
   Crisp Lee
  </td>
 </tr>
 <tr>
  <td>
   Dagfinn Ilmari Mannsåker
  </td>
 </tr>
 <tr>
  <td>
   Daniel Elishakov
  </td>
 </tr>
 <tr>
  <td>
   Daniel Gustafsson
  </td>
 </tr>
 <tr>
  <td>
   Daniel Vérité
  </td>
 </tr>
 <tr>
  <td>
   Daniel Westermann
  </td>
 </tr>
 <tr>
  <td>
   Daniele Varrazzo
  </td>
 </tr>
 <tr>
  <td>
   Daniil Davydov
  </td>
 </tr>
 <tr>
  <td>
   Daria Shanina
  </td>
 </tr>
 <tr>
  <td>
   Dave Cramer
  </td>
 </tr>
 <tr>
  <td>
   Dave Page
  </td>
 </tr>
 <tr>
  <td>
   David Benjamin
  </td>
 </tr>
 <tr>
  <td>
   David Christensen
  </td>
 </tr>
 <tr>
  <td>
   David Fiedler
  </td>
 </tr>
 <tr>
  <td>
   David G. Johnston
  </td>
 </tr>
 <tr>
  <td>
   David Geier
  </td>
 </tr>
 <tr>
  <td>
   David Rowley
  </td>
 </tr>
 <tr>
  <td>
   David Steele
  </td>
 </tr>
 <tr>
  <td>
   David Wheeler
  </td>
 </tr>
 <tr>
  <td>
   David Zhang
  </td>
 </tr>
 <tr>
  <td>
   Davinder Singh
  </td>
 </tr>
 <tr>
  <td>
   Dean Rasheed
  </td>
 </tr>
 <tr>
  <td>
   Devanga Susmitha
  </td>
 </tr>
 <tr>
  <td>
   Devrim Gündüz
  </td>
 </tr>
 <tr>
  <td>
   Dian Fay
  </td>
 </tr>
 <tr>
  <td>
   Dilip Kumar
  </td>
 </tr>
 <tr>
  <td>
   Dimitrios Apostolou
  </td>
 </tr>
 <tr>
  <td>
   Dipesh Dhameliya
  </td>
 </tr>
 <tr>
  <td>
   Dmitrii Bondar
  </td>
 </tr>
 <tr>
  <td>
   Dmitry Dolgov
  </td>
 </tr>
 <tr>
  <td>
   Dmitry Koval
  </td>
 </tr>
 <tr>
  <td>
   Dmitry Kovalenko
  </td>
 </tr>
 <tr>
  <td>
   Dmitry Yurichev
  </td>
 </tr>
 <tr>
  <td>
   Dominique Devienne
  </td>
 </tr>
 <tr>
  <td>
   Donghang Lin
  </td>
 </tr>
 <tr>
  <td>
   Dorjpalam Batbaatar
  </td>
 </tr>
 <tr>
  <td>
   Drew Callahan
  </td>
 </tr>
 <tr>
  <td>
   Duncan Sands
  </td>
 </tr>
 <tr>
  <td>
   Dwayne Towell
  </td>
 </tr>
 <tr>
  <td>
   Dzmitry Jachnik
  </td>
 </tr>
 <tr>
  <td>
   Egor Chindyaskin
  </td>
 </tr>
 <tr>
  <td>
   Egor Rogov
  </td>
 </tr>
 <tr>
  <td>
   Emanuel Ionescu
  </td>
 </tr>
 <tr>
  <td>
   Emanuele Musella
  </td>
 </tr>
 <tr>
  <td>
   Emre Hasegeli
  </td>
 </tr>
 <tr>
  <td>
   Eric Cyr
  </td>
 </tr>
 <tr>
  <td>
   Erica Zhang
  </td>
 </tr>
 <tr>
  <td>
   Erik Nordström
  </td>
 </tr>
 <tr>
  <td>
   Erik Rijkers
  </td>
 </tr>
 <tr>
  <td>
   Erik Wienhold
  </td>
 </tr>
 <tr>
  <td>
   Erki Eessaar
  </td>
 </tr>
 <tr>
  <td>
   Ethan Mertz
  </td>
 </tr>
 <tr>
  <td>
   Etienne LAFARGE
  </td>
 </tr>
 <tr>
  <td>
   Etsuro Fujita
  </td>
 </tr>
 <tr>
  <td>
   Euler Taveira
  </td>
 </tr>
 <tr>
  <td>
   Evan Si
  </td>
 </tr>
 <tr>
  <td>
   Evgeniy Gorbanev
  </td>
 </tr>
 <tr>
  <td>
   Fabio R. Sluzala
  </td>
 </tr>
 <tr>
  <td>
   Fabrízio de Royes Mello
  </td>
 </tr>
 <tr>
  <td>
   Feike Steenbergen
  </td>
 </tr>
 <tr>
  <td>
   Feliphe Pozzer
  </td>
 </tr>
 <tr>
  <td>
   Felix
  </td>
 </tr>
 <tr>
  <td>
   Fire Emerald
  </td>
 </tr>
 <tr>
  <td>
   Florents Tselai
  </td>
 </tr>
 <tr>
  <td>
   Francesco Degrassi
  </td>
 </tr>
 <tr>
  <td>
   Frank Streitzig
  </td>
 </tr>
 <tr>
  <td>
   Frédéric Yhuel
  </td>
 </tr>
 <tr>
  <td>
   Fredrik Widlert
  </td>
 </tr>
 <tr>
  <td>
   Gabriele Bartolini
  </td>
 </tr>
 <tr>
  <td>
   Gavin Panella
  </td>
 </tr>
 <tr>
  <td>
   Geoff Winkless
  </td>
 </tr>
 <tr>
  <td>
   George MacKerron
  </td>
 </tr>
 <tr>
  <td>
   Gilles Darold
  </td>
 </tr>
 <tr>
  <td>
   Grant Gryczan
  </td>
 </tr>
 <tr>
  <td>
   Greg Burd
  </td>
 </tr>
 <tr>
  <td>
   Greg Sabino Mullane
  </td>
 </tr>
 <tr>
  <td>
   Greg Stark
  </td>
 </tr>
 <tr>
  <td>
   Grigory Kryachko
  </td>
 </tr>
 <tr>
  <td>
   Guillaume Lelarge
  </td>
 </tr>
 <tr>
  <td>
   Gunnar Morling
  </td>
 </tr>
 <tr>
  <td>
   Gunnar Wagner
  </td>
 </tr>
 <tr>
  <td>
   Gurjeet Singh
  </td>
 </tr>
 <tr>
  <td>
   Haifang Wang
  </td>
 </tr>
 <tr>
  <td>
   Hajime Matsunaga
  </td>
 </tr>
 <tr>
  <td>
   Hamid Akhtar
  </td>
 </tr>
 <tr>
  <td>
   Hannu Krosing
  </td>
 </tr>
 <tr>
  <td>
   Hari Krishna Sunder
  </td>
 </tr>
 <tr>
  <td>
   Haruka Takatsuka
  </td>
 </tr>
 <tr>
  <td>
   Hayato Kuroda
  </td>
 </tr>
 <tr>
  <td>
   Heikki Linnakangas
  </td>
 </tr>
 <tr>
  <td>
   Hironobu Suzuki
  </td>
 </tr>
 <tr>
  <td>
   Holger Jakobs
  </td>
 </tr>
 <tr>
  <td>
   Hubert Lubaczewski
  </td>
 </tr>
 <tr>
  <td>
   Hugo Dubois
  </td>
 </tr>
 <tr>
  <td>
   Hugo Zhang
  </td>
 </tr>
 <tr>
  <td>
   Hunaid Sohail
  </td>
 </tr>
 <tr>
  <td>
   Hywel Carver
  </td>
 </tr>
 <tr>
  <td>
   Ian Barwick
  </td>
 </tr>
 <tr>
  <td>
   Ibrar Ahmed
  </td>
 </tr>
 <tr>
  <td>
   Igor Gnatyuk
  </td>
 </tr>
 <tr>
  <td>
   Igor Korot
  </td>
 </tr>
 <tr>
  <td>
   Ilia Evdokimov
  </td>
 </tr>
 <tr>
  <td>
   Ilya Gladyshev
  </td>
 </tr>
 <tr>
  <td>
   Ilyasov Ian
  </td>
 </tr>
 <tr>
  <td>
   Imran Zaheer
  </td>
 </tr>
 <tr>
  <td>
   Isaac Morland
  </td>
 </tr>
 <tr>
  <td>
   Israel Barth Rubio
  </td>
 </tr>
 <tr>
  <td>
   Ivan Kush
  </td>
 </tr>
 <tr>
  <td>
   Jacob Brazeal
  </td>
 </tr>
 <tr>
  <td>
   Jacob Champion
  </td>
 </tr>
 <tr>
  <td>
   Jaime Casanova
  </td>
 </tr>
 <tr>
  <td>
   Jakob Egger
  </td>
 </tr>
 <tr>
  <td>
   Jakub Wartak
  </td>
 </tr>
 <tr>
  <td>
   James Coleman
  </td>
 </tr>
 <tr>
  <td>
   James Hunter
  </td>
 </tr>
 <tr>
  <td>
   Jan Behrens
  </td>
 </tr>
 <tr>
  <td>
   Japin Li
  </td>
 </tr>
 <tr>
  <td>
   Jason Smith
  </td>
 </tr>
 <tr>
  <td>
   Jayesh Dehankar
  </td>
 </tr>
 <tr>
  <td>
   Jeevan Chalke
  </td>
 </tr>
 <tr>
  <td>
   Jeff Davis
  </td>
 </tr>
 <tr>
  <td>
   Jehan-Guillaume de Rorthais
  </td>
 </tr>
 <tr>
  <td>
   Jelte Fennema-Nio
  </td>
 </tr>
 <tr>
  <td>
   Jian He
  </td>
 </tr>
 <tr>
  <td>
   Jianghua Yang
  </td>
 </tr>
 <tr>
  <td>
   Jiao Shuntian
  </td>
 </tr>
 <tr>
  <td>
   Jim Jones
  </td>
 </tr>
 <tr>
  <td>
   Jim Nasby
  </td>
 </tr>
 <tr>
  <td>
   Jingtang Zhang
  </td>
 </tr>
 <tr>
  <td>
   Jingzhou Fu
  </td>
 </tr>
 <tr>
  <td>
   Joe Conway
  </td>
 </tr>
 <tr>
  <td>
   Joel Jacobson
  </td>
 </tr>
 <tr>
  <td>
   John Hutchins
  </td>
 </tr>
 <tr>
  <td>
   John Naylor
  </td>
 </tr>
 <tr>
  <td>
   Jonathan Katz
  </td>
 </tr>
 <tr>
  <td>
   Jorge Solórzano
  </td>
 </tr>
 <tr>
  <td>
   José Villanova
  </td>
 </tr>
 <tr>
  <td>
   Josef Šimánek
  </td>
 </tr>
 <tr>
  <td>
   Joseph Koshakow
  </td>
 </tr>
 <tr>
  <td>
   Julien Rouhaud
  </td>
 </tr>
 <tr>
  <td>
   Junwang Zhao
  </td>
 </tr>
 <tr>
  <td>
   Justin Pryzby
  </td>
 </tr>
 <tr>
  <td>
   Kaido Vaikla
  </td>
 </tr>
 <tr>
  <td>
   Kaimeh
  </td>
 </tr>
 <tr>
  <td>
   Karina Litskevich
  </td>
 </tr>
 <tr>
  <td>
   Karthik S
  </td>
 </tr>
 <tr>
  <td>
   Kartyshov Ivan
  </td>
 </tr>
 <tr>
  <td>
   Kashif Zeeshan
  </td>
 </tr>
 <tr>
  <td>
   Keisuke Kuroda
  </td>
 </tr>
 <tr>
  <td>
   Kevin Hale Boyes
  </td>
 </tr>
 <tr>
  <td>
   Kevin K Biju
  </td>
 </tr>
 <tr>
  <td>
   Kirill Reshke
  </td>
 </tr>
 <tr>
  <td>
   Kirill Zdornyy
  </td>
 </tr>
 <tr>
  <td>
   Koen De Groote
  </td>
 </tr>
 <tr>
  <td>
   Koichi Suzuki
  </td>
 </tr>
 <tr>
  <td>
   Koki Nakamura
  </td>
 </tr>
 <tr>
  <td>
   Konstantin Knizhnik
  </td>
 </tr>
 <tr>
  <td>
   Kouhei Sutou
  </td>
 </tr>
 <tr>
  <td>
   Kuntal Ghosh
  </td>
 </tr>
 <tr>
  <td>
   Kyotaro Horiguchi
  </td>
 </tr>
 <tr>
  <td>
   Lakshmi Narayana Velayudam
  </td>
 </tr>
 <tr>
  <td>
   Lars Kanis
  </td>
 </tr>
 <tr>
  <td>
   Laurence Parry
  </td>
 </tr>
 <tr>
  <td>
   Laurenz Albe
  </td>
 </tr>
 <tr>
  <td>
   Lele Gaifax
  </td>
 </tr>
 <tr>
  <td>
   Li Yong
  </td>
 </tr>
 <tr>
  <td>
   Lilian Ontowhee
  </td>
 </tr>
 <tr>
  <td>
   Lingbin Meng
  </td>
 </tr>
 <tr>
  <td>
   Luboslav Špilák
  </td>
 </tr>
 <tr>
  <td>
   Luca Vallisa
  </td>
 </tr>
 <tr>
  <td>
   Lukas Fittl
  </td>
 </tr>
 <tr>
  <td>
   Maciek Sakrejda
  </td>
 </tr>
 <tr>
  <td>
   Magnus Hagander
  </td>
 </tr>
 <tr>
  <td>
   Mahendra Singh Thalor
  </td>
 </tr>
 <tr>
  <td>
   Mahendrakar Srinivasarao
  </td>
 </tr>
 <tr>
  <td>
   Maiquel Grassi
  </td>
 </tr>
 <tr>
  <td>
   Maksim Korotkov
  </td>
 </tr>
 <tr>
  <td>
   Maksim Melnikov
  </td>
 </tr>
 <tr>
  <td>
   Man Zeng
  </td>
 </tr>
 <tr>
  <td>
   Marat Buharov
  </td>
 </tr>
 <tr>
  <td>
   Marc Balmer
  </td>
 </tr>
 <tr>
  <td>
   Marco Nenciarini
  </td>
 </tr>
 <tr>
  <td>
   Marcos Pegoraro
  </td>
 </tr>
 <tr>
  <td>
   Marina Polyakova
  </td>
 </tr>
 <tr>
  <td>
   Mark Callaghan
  </td>
 </tr>
 <tr>
  <td>
   Mark Dilger
  </td>
 </tr>
 <tr>
  <td>
   Marlene Brandstaetter
  </td>
 </tr>
 <tr>
  <td>
   Marlene Reiterer
  </td>
 </tr>
 <tr>
  <td>
   Martin Rakhmanov
  </td>
 </tr>
 <tr>
  <td>
   Masahiko Sawada
  </td>
 </tr>
 <tr>
  <td>
   Masahiro Ikeda
  </td>
 </tr>
 <tr>
  <td>
   Masao Fujii
  </td>
 </tr>
 <tr>
  <td>
   Mason Mackaman
  </td>
 </tr>
 <tr>
  <td>
   Mat Arye
  </td>
 </tr>
 <tr>
  <td>
   Matheus Alcantara
  </td>
 </tr>
 <tr>
  <td>
   Mats Kindahl
  </td>
 </tr>
 <tr>
  <td>
   Matthew Gabeler-Lee
  </td>
 </tr>
 <tr>
  <td>
   Matthew Kim
  </td>
 </tr>
 <tr>
  <td>
   Matthew Sterrett
  </td>
 </tr>
 <tr>
  <td>
   Matthew Woodcraft
  </td>
 </tr>
 <tr>
  <td>
   Matthias van de Meent
  </td>
 </tr>
 <tr>
  <td>
   Matthieu Denais
  </td>
 </tr>
 <tr>
  <td>
   Maurizio Boriani
  </td>
 </tr>
 <tr>
  <td>
   Max Johnson
  </td>
 </tr>
 <tr>
  <td>
   Max Madden
  </td>
 </tr>
 <tr>
  <td>
   Maxim Boguk
  </td>
 </tr>
 <tr>
  <td>
   Maxim Orlov
  </td>
 </tr>
 <tr>
  <td>
   Maximilian Chrzan
  </td>
 </tr>
 <tr>
  <td>
   Melanie Plageman
  </td>
 </tr>
 <tr>
  <td>
   Melih Mutlu
  </td>
 </tr>
 <tr>
  <td>
   Mert Alev
  </td>
 </tr>
 <tr>
  <td>
   Michael Banck
  </td>
 </tr>
 <tr>
  <td>
   Michael Bondarenko
  </td>
 </tr>
 <tr>
  <td>
   Michael Christofides
  </td>
 </tr>
 <tr>
  <td>
   Michael Guissine
  </td>
 </tr>
 <tr>
  <td>
   Michael Harris
  </td>
 </tr>
 <tr>
  <td>
   Michaël Paquier
  </td>
 </tr>
 <tr>
  <td>
   Michail Nikolaev
  </td>
 </tr>
 <tr>
  <td>
   Michal Kleczek
  </td>
 </tr>
 <tr>
  <td>
   Michel Pelletier
  </td>
 </tr>
 <tr>
  <td>
   Mikaël Gourlaouen
  </td>
 </tr>
 <tr>
  <td>
   Mikhail Gribkov
  </td>
 </tr>
 <tr>
  <td>
   Mikhail Kot
  </td>
 </tr>
 <tr>
  <td>
   Milosz Chmura
  </td>
 </tr>
 <tr>
  <td>
   Muralikrishna Bandaru
  </td>
 </tr>
 <tr>
  <td>
   Murat Efendioglu
  </td>
 </tr>
 <tr>
  <td>
   Mutaamba Maasha
  </td>
 </tr>
 <tr>
  <td>
   Naeem Akhter
  </td>
 </tr>
 <tr>
  <td>
   Nat Makarevitch
  </td>
 </tr>
 <tr>
  <td>
   Nathan Bossart
  </td>
 </tr>
 <tr>
  <td>
   Navneet Kumar
  </td>
 </tr>
 <tr>
  <td>
   Nazir Bilal Yavuz
  </td>
 </tr>
 <tr>
  <td>
   Neil Conway
  </td>
 </tr>
 <tr>
  <td>
   Niccolò Fei
  </td>
 </tr>
 <tr>
  <td>
   Nick Davies
  </td>
 </tr>
 <tr>
  <td>
   Nicolas Maus
  </td>
 </tr>
 <tr>
  <td>
   Niek Brasa
  </td>
 </tr>
 <tr>
  <td>
   Nikhil Raj
  </td>
 </tr>
 <tr>
  <td>
   Nikita
  </td>
 </tr>
 <tr>
  <td>
   Nikita Kalinin
  </td>
 </tr>
 <tr>
  <td>
   Nikita Malakhov
  </td>
 </tr>
 <tr>
  <td>
   Nikolay Samokhvalov
  </td>
 </tr>
 <tr>
  <td>
   Nikolay Shaplov
  </td>
 </tr>
 <tr>
  <td>
   Nisha Moond
  </td>
 </tr>
 <tr>
  <td>
   Nitin Jadhav
  </td>
 </tr>
 <tr>
  <td>
   Nitin Motiani
  </td>
 </tr>
 <tr>
  <td>
   Noah Misch
  </td>
 </tr>
 <tr>
  <td>
   Noboru Saito
  </td>
 </tr>
 <tr>
  <td>
   Noriyoshi Shinoda
  </td>
 </tr>
 <tr>
  <td>
   Ole Peder Brandtzæg
  </td>
 </tr>
 <tr>
  <td>
   Oleg Sibiryakov
  </td>
 </tr>
 <tr>
  <td>
   Oleg Tselebrovskiy
  </td>
 </tr>
 <tr>
  <td>
   Olleg Samoylov
  </td>
 </tr>
 <tr>
  <td>
   Onder Kalaci
  </td>
 </tr>
 <tr>
  <td>
   Ondrej Navratil
  </td>
 </tr>
 <tr>
  <td>
   Patrick Stählin
  </td>
 </tr>
 <tr>
  <td>
   Paul Amonson
  </td>
 </tr>
 <tr>
  <td>
   Paul Jungwirth
  </td>
 </tr>
 <tr>
  <td>
   Paul Ramsey
  </td>
 </tr>
 <tr>
  <td>
   Pavel Borisov
  </td>
 </tr>
 <tr>
  <td>
   Pavel Luzanov
  </td>
 </tr>
 <tr>
  <td>
   Pavel Nekrasov
  </td>
 </tr>
 <tr>
  <td>
   Pavel Stehule
  </td>
 </tr>
 <tr>
  <td>
   Peter Eisentraut
  </td>
 </tr>
 <tr>
  <td>
   Peter Geoghegan
  </td>
 </tr>
 <tr>
  <td>
   Peter Mittere
  </td>
 </tr>
 <tr>
  <td>
   Peter Smith
  </td>
 </tr>
 <tr>
  <td>
   Phil Eaton
  </td>
 </tr>
 <tr>
  <td>
   Philipp Salvisberg
  </td>
 </tr>
 <tr>
  <td>
   Philippe Beaudoin
  </td>
 </tr>
 <tr>
  <td>
   Pierre Giraud
  </td>
 </tr>
 <tr>
  <td>
   Pixian Shi
  </td>
 </tr>
 <tr>
  <td>
   Polina Bungina
  </td>
 </tr>
 <tr>
  <td>
   Przemyslaw Sztoch
  </td>
 </tr>
 <tr>
  <td>
   Quynh Tran
  </td>
 </tr>
 <tr>
  <td>
   Rafia Sabih
  </td>
 </tr>
 <tr>
  <td>
   Raghuveer Devulapalli
  </td>
 </tr>
 <tr>
  <td>
   Rahila Syed
  </td>
 </tr>
 <tr>
  <td>
   Rama Malladi
  </td>
 </tr>
 <tr>
  <td>
   Ran Benita
  </td>
 </tr>
 <tr>
  <td>
   Ranier Vilela
  </td>
 </tr>
 <tr>
  <td>
   Renan Alves Fonseca
  </td>
 </tr>
 <tr>
  <td>
   Richard Guo
  </td>
 </tr>
 <tr>
  <td>
   Richard Neill
  </td>
 </tr>
 <tr>
  <td>
   Rintaro Ikeda
  </td>
 </tr>
 <tr>
  <td>
   Robert Haas
  </td>
 </tr>
 <tr>
  <td>
   Robert Treat
  </td>
 </tr>
 <tr>
  <td>
   Robins Tharakan
  </td>
 </tr>
 <tr>
  <td>
   Roman Zharkov
  </td>
 </tr>
 <tr>
  <td>
   Ronald Cruz
  </td>
 </tr>
 <tr>
  <td>
   Ronan Dunklau
  </td>
 </tr>
 <tr>
  <td>
   Rui Zhao
  </td>
 </tr>
 <tr>
  <td>
   Rushabh Lathia
  </td>
 </tr>
 <tr>
  <td>
   Rustam Allakov
  </td>
 </tr>
 <tr>
  <td>
   Ryo Kanbayashi
  </td>
 </tr>
 <tr>
  <td>
   Ryohei Takahashi
  </td>
 </tr>
 <tr>
  <td>
   RyotaK
  </td>
 </tr>
 <tr>
  <td>
   Sagar Dilip Shedge
  </td>
 </tr>
 <tr>
  <td>
   Salvatore Dipietro
  </td>
 </tr>
 <tr>
  <td>
   Sam Gabrielsson
  </td>
 </tr>
 <tr>
  <td>
   Sam James
  </td>
 </tr>
 <tr>
  <td>
   Sameer Kumar
  </td>
 </tr>
 <tr>
  <td>
   Sami Imseih
  </td>
 </tr>
 <tr>
  <td>
   Samuel Thibault
  </td>
 </tr>
 <tr>
  <td>
   Satyanarayana Narlapuram
  </td>
 </tr>
 <tr>
  <td>
   Sebastian Skalacki
  </td>
 </tr>
 <tr>
  <td>
   Senglee Choi
  </td>
 </tr>
 <tr>
  <td>
   Sergei Kornilov
  </td>
 </tr>
 <tr>
  <td>
   Sergey Belyashov
  </td>
 </tr>
 <tr>
  <td>
   Sergey Dudoladov
  </td>
 </tr>
 <tr>
  <td>
   Sergey Prokhorenko
  </td>
 </tr>
 <tr>
  <td>
   Sergey Sargsyan
  </td>
 </tr>
 <tr>
  <td>
   Sergey Soloviev
  </td>
 </tr>
 <tr>
  <td>
   Sergey Tatarintsev
  </td>
 </tr>
 <tr>
  <td>
   Shaik Mohammad Mujeeb
  </td>
 </tr>
 <tr>
  <td>
   Shawn McCoy
  </td>
 </tr>
 <tr>
  <td>
   Shenhao Wang
  </td>
 </tr>
 <tr>
  <td>
   Shihao Zhong
  </td>
 </tr>
 <tr>
  <td>
   Shinya Kato
  </td>
 </tr>
 <tr>
  <td>
   Shlok Kyal
  </td>
 </tr>
 <tr>
  <td>
   Shubham Khanna
  </td>
 </tr>
 <tr>
  <td>
   Shveta Malik
  </td>
 </tr>
 <tr>
  <td>
   Simon Riggs
  </td>
 </tr>
 <tr>
  <td>
   Smolkin Grigory
  </td>
 </tr>
 <tr>
  <td>
   Sofia Kopikova
  </td>
 </tr>
 <tr>
  <td>
   Song Hongyu
  </td>
 </tr>
 <tr>
  <td>
   Song Jinzhou
  </td>
 </tr>
 <tr>
  <td>
   Soumyadeep Chakraborty
  </td>
 </tr>
 <tr>
  <td>
   Sravan Kumar
  </td>
 </tr>
 <tr>
  <td>
   Srinath Reddy
  </td>
 </tr>
 <tr>
  <td>
   Stan Hu
  </td>
 </tr>
 <tr>
  <td>
   Stepan Neretin
  </td>
 </tr>
 <tr>
  <td>
   Stephen Fewer
  </td>
 </tr>
 <tr>
  <td>
   Stephen Frost
  </td>
 </tr>
 <tr>
  <td>
   Steve Chavez
  </td>
 </tr>
 <tr>
  <td>
   Steven Niu
  </td>
 </tr>
 <tr>
  <td>
   Suraj Kharage
  </td>
 </tr>
 <tr>
  <td>
   Sven Klemm
  </td>
 </tr>
 <tr>
  <td>
   Takamichi Osumi
  </td>
 </tr>
 <tr>
  <td>
   Takeshi Ideriha
  </td>
 </tr>
 <tr>
  <td>
   Tatsuo Ishii
  </td>
 </tr>
 <tr>
  <td>
   Ted Yu
  </td>
 </tr>
 <tr>
  <td>
   Tels
  </td>
 </tr>
 <tr>
  <td>
   Tender Wang
  </td>
 </tr>
 <tr>
  <td>
   Teodor Sigaev
  </td>
 </tr>
 <tr>
  <td>
   Thom Brown
  </td>
 </tr>
 <tr>
  <td>
   Thomas Baehler
  </td>
 </tr>
 <tr>
  <td>
   Thomas Krennwallner
  </td>
 </tr>
 <tr>
  <td>
   Thomas Munro
  </td>
 </tr>
 <tr>
  <td>
   Tim Wood
  </td>
 </tr>
 <tr>
  <td>
   Timur Magomedov
  </td>
 </tr>
 <tr>
  <td>
   Tobias Wendorff
  </td>
 </tr>
 <tr>
  <td>
   Todd Cook
  </td>
 </tr>
 <tr>
  <td>
   Tofig Aliev
  </td>
 </tr>
 <tr>
  <td>
   Tom Lane
  </td>
 </tr>
 <tr>
  <td>
   Tomas Vondra
  </td>
 </tr>
 <tr>
  <td>
   Tomasz Rybak
  </td>
 </tr>
 <tr>
  <td>
   Tomasz Szypowski
  </td>
 </tr>
 <tr>
  <td>
   Torsten Foertsch
  </td>
 </tr>
 <tr>
  <td>
   Toshi Harada
  </td>
 </tr>
 <tr>
  <td>
   Tristan Partin
  </td>
 </tr>
 <tr>
  <td>
   Triveni N
  </td>
 </tr>
 <tr>
  <td>
   Umar Hayat
  </td>
 </tr>
 <tr>
  <td>
   Vallimaharajan G
  </td>
 </tr>
 <tr>
  <td>
   Vasya Boytsov
  </td>
 </tr>
 <tr>
  <td>
   Victor Yegorov
  </td>
 </tr>
 <tr>
  <td>
   Vignesh C
  </td>
 </tr>
 <tr>
  <td>
   Viktor Holmberg
  </td>
 </tr>
 <tr>
  <td>
   Vinícius Abrahão
  </td>
 </tr>
 <tr>
  <td>
   Vinod Sridharan
  </td>
 </tr>
 <tr>
  <td>
   Virender Singla
  </td>
 </tr>
 <tr>
  <td>
   Vitaly Davydov
  </td>
 </tr>
 <tr>
  <td>
   Vladlen Popolitov
  </td>
 </tr>
 <tr>
  <td>
   Vladyslav Nebozhyn
  </td>
 </tr>
 <tr>
  <td>
   Walid Ibrahim
  </td>
 </tr>
 <tr>
  <td>
   Webbo Han
  </td>
 </tr>
 <tr>
  <td>
   Wenhui Qiu
  </td>
 </tr>
 <tr>
  <td>
   Will Mortensen
  </td>
 </tr>
 <tr>
  <td>
   Will Storey
  </td>
 </tr>
 <tr>
  <td>
   Wolfgang Walther
  </td>
 </tr>
 <tr>
  <td>
   Xin Zhang
  </td>
 </tr>
 <tr>
  <td>
   Xing Guo
  </td>
 </tr>
 <tr>
  <td>
   Xuneng Zhou
  </td>
 </tr>
 <tr>
  <td>
   Yan Chengpen
  </td>
 </tr>
 <tr>
  <td>
   Yang Lei
  </td>
 </tr>
 <tr>
  <td>
   Yaroslav Saburov
  </td>
 </tr>
 <tr>
  <td>
   Yaroslav Syrytsia
  </td>
 </tr>
 <tr>
  <td>
   Yasir Hussain
  </td>
 </tr>
 <tr>
  <td>
   Yasuo Honda
  </td>
 </tr>
 <tr>
  <td>
   Yogesh Sharma
  </td>
 </tr>
 <tr>
  <td>
   Yonghao Lee
  </td>
 </tr>
 <tr>
  <td>
   Yoran Heling
  </td>
 </tr>
 <tr>
  <td>
   Yu Liang
  </td>
 </tr>
 <tr>
  <td>
   Yugo Nagata
  </td>
 </tr>
 <tr>
  <td>
   Yuhang Qiu
  </td>
 </tr>
 <tr>
  <td>
   Yuki Seino
  </td>
 </tr>
 <tr>
  <td>
   Yura Sokolov
  </td>
 </tr>
 <tr>
  <td>
   Yurii Rashkovskii
  </td>
 </tr>
 <tr>
  <td>
   Yushi Ogiwara
  </td>
 </tr>
 <tr>
  <td>
   Yusuke Sugie
  </td>
 </tr>
 <tr>
  <td>
   Yuta Katsuragi
  </td>
 </tr>
 <tr>
  <td>
   Yuto Sasaki
  </td>
 </tr>
 <tr>
  <td>
   Yuuki Fujii
  </td>
 </tr>
 <tr>
  <td>
   Yuya Watari
  </td>
 </tr>
 <tr>
  <td>
   Zane Duffield
  </td>
 </tr>
 <tr>
  <td>
   Zeyuan Hu
  </td>
 </tr>
 <tr>
  <td>
   Zhang Mingli
  </td>
 </tr>
 <tr>
  <td>
   Zhihong Yu
  </td>
 </tr>
 <tr>
  <td>
   Zhijie Hou
  </td>
 </tr>
 <tr>
  <td>
   Zsolt Parragi
  </td>
 </tr>
</table>





