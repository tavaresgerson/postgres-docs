## Apêndice F. Módulos e extensões adicionais fornecidos

**Índice**

* [F.1. amcheck — ferramentas para verificar a consistência de tabelas e índices](amcheck.md)

+ [F.1.1. Funções](amcheck.md#AMCHECK-FUNCTIONS)
+ [F.1.2. Verificação opcional *`heapallindexed`*](amcheck.md#AMCHECK-OPTIONAL-HEAPALLINDEXED-VERIFICATION)
+ [F.1.3. Uso eficaz de `amcheck`](amcheck.md#AMCHECK-USING-AMCHECK-EFFECTIVELY)
+ [F.1.4. Reparo de corrupção](amcheck.md#AMCHECK-REPAIRING-CORRUPTION)

* [F.2. auth_delay — pausar após falha na autenticação](auth-delay.md)

+ [F.2.1. Parâmetros de Configuração](auth-delay.md#AUTH-DELAY-CONFIGURATION-PARAMETERS)
+ [F.2.2. Autor](auth-delay.md#AUTH-DELAY-AUTHOR)

* [F.3. auto_explain — registro dos planos de execução de consultas lentas](auto-explain.md)

+ [F.3.1. Parâmetros de Configuração](auto-explain.md#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS)
+ [F.3.2. Exemplo](auto-explain.md#AUTO-EXPLAIN-EXAMPLE)
+ [F.3.3. Autor](auto-explain.md#AUTO-EXPLAIN-AUTHOR)

* [F.4. basebackup_to_shell — exemplo "shell" módulo pg_basebackup](basebackup-to-shell.md)

+ [F.4.1. Parâmetros de Configuração](basebackup-to-shell.md#BASEBACKUP-TO-SHELL-CONFIGURATION-PARAMETERS)
+ [F.4.2. Autor](basebackup-to-shell.md#BASEBACKUP-TO-SHELL-AUTHOR)

* [F.5. archive_basic — um exemplo de módulo de arquivo WAL](basic-archive.md)

+ [F.5.1. Parâmetros de Configuração](basic-archive.md#BASIC-ARCHIVE-CONFIGURATION-PARAMETERS)
+ [F.5.2. Notas](basic-archive.md#BASIC-ARCHIVE-NOTES)
+ [F.5.3. Autor](basic-archive.md#BASIC-ARCHIVE-AUTHOR)

* [F.6. bloom — método de acesso ao índice do filtro bloom](bloom.md)

+ [F.6.1. Parâmetros](bloom.md#BLOOM-PARAMETERS)
+ [F.6.2. Exemplos](bloom.md#BLOOM-EXAMPLES)
+ [F.6.3. Interface da Classe Operadora](bloom.md#BLOOM-OPERATOR-CLASS-INTERFACE)
+ [F.6.4. Limitações](bloom.md#BLOOM-LIMITATIONS)
+ [F.6.5. Autores](bloom.md#BLOOM-AUTHORS)

* [F.7. btree_gin — Classes de operadores GIN com comportamento de B-tree](btree-gin.md)

+ [F.7.1. Exemplo de uso](btree-gin.md#BTREE-GIN-EXAMPLE-USAGE)
+ [F.7.2. Autores](btree-gin.md#BTREE-GIN-AUTHORS)

* [F.8. btree_gist — Classes de operadores GiST com comportamento de B-tree](btree-gist.md)

+ [F.8.1. Exemplo de uso](btree-gist.md#BTREE-GIST-EXAMPLE-USAGE)
+ [F.8.2. Autores](btree-gist.md#BTREE-GIST-AUTHORS)

* [F.9. citext — um tipo de cadeia de caracteres insensível a maiúsculas e minúsculas](citext.md)

+ [F.9.1. Razão](citext.md#CITEXT-RATIONALE)
+ [F.9.2. Como usá-lo](citext.md#CITEXT-HOW-TO-USE-IT)
+ [F.9.3. Comportamento de comparação de strings](citext.md#CITEXT-STRING-COMPARISON-BEHAVIOR)
+ [F.9.4. Limitações](citext.md#CITEXT-LIMITATIONS)
+ [F.9.5. Autor](citext.md#CITEXT-AUTHOR)

* [F.10. cubo — um tipo de dados cubo multidimensional](cube.md)

+ [F.10.1. Sintaxe](cube.md#CUBE-SYNTAX)
+ [F.10.2. Precisão](cube.md#CUBE-PRECISION)
+ [F.10.3. Uso](cube.md#CUBE-USAGE)
+ [F.10.4. Definições Padrão](cube.md#CUBE-DEFAULTS)
+ [F.10.5. Notas](cube.md#CUBE-NOTES)
+ [F.10.6. Créditos](cube.md#CUBE-CREDITS)

* [F.11. dblink — conectar-se a outros bancos de dados PostgreSQL](dblink.md)

+ [dblink_connect](contrib-dblink-connect.md) — abre uma conexão persistente a um banco de dados remoto
+ [dblink_connect_u](contrib-dblink-connect-u.md) — abre uma conexão persistente a um banco de dados remoto, de forma insegura
+ [dblink_disconnect](contrib-dblink-disconnect.md) — fecha uma conexão persistente a um banco de dados remoto
+ [dblink](contrib-dblink-function.md) — executa uma consulta em um banco de dados remoto
+ [dblink_exec](contrib-dblink-exec.md) — executa um comando em um banco de dados remoto
+ [dblink_open](contrib-dblink-open.md) — abre um cursor em um banco de dados remoto
+ [dblink_fetch](contrib-dblink-fetch.md) — retorna linhas de um cursor aberto em um banco de dados remoto
+ [dblink_close](contrib-dblink-close.md) — fecha um cursor em um banco de dados remoto
+ [dblink_get_connections](contrib-dblink-get-connections.md) — retorna os nomes de todas as conexões de dblink nomeadas abertas
+ [dblink_error_message](contrib-dblink-error-message.md) — obtém o último erro da conexão nomeada
+ [dblink_send_query](contrib-dblink-send-query.md) — envia uma consulta assíncrona a um banco de dados remoto
+ [dblink_is_busy](contrib-dblink-is-busy.md) — verifica se a conexão está ocupada com uma consulta assíncrona
+ [dblink_get_notify](contrib-dblink-get-notify.md) — recupera notificações assíncronas em uma conexão
+ [dblink_get_result](contrib-dblink-get-result.md) — obtém o resultado de uma consulta assíncrona
+ [dblink_cancel_query](contrib-dblink-cancel-query.md) — cancela qualquer consulta ativa na conexão nomeada
+ [dblink_get_pkey](contrib-dblink-get-pkey.md) — retorna as posições e os nomes dos campos da chave primária de uma relação
+ [dblink_build_sql_insert](contrib-dblink-build-sql-insert.md) — constrói uma declaração de INSERT usando uma tupla local, substituindo os valores do campo da chave primária pelos valores alternativos fornecidos
+ [dblink_build_sql_delete](contrib-dblink-build-sql-delete.md) — constrói uma declaração de DELETE usando os valores fornecidos para os campos da chave primária
+ [dblink_build_sql_update](contrib-dblink-build-sql-update.md) — constrói uma declaração de UPDATE usando uma tupla local, substituindo os valores do campo da chave primária pelos valores alternativos fornecidos

* [F.12. dict_int — dicionário de busca de texto completo para inteiros](dict-int.md)

+ [F.12.1. Configuração](dict-int.md#DICT-INT-CONFIG)
+ [F.12.2. Uso](dict-int.md#DICT-INT-USAGE)

* [F.13. dict_xsyn — dicionário de busca de sinônimos de texto completo](dict-xsyn.md)

+ [F.13.1. Configuração](dict-xsyn.md#DICT-XSYN-CONFIG)
+ [F.13.2. Uso](dict-xsyn.md#DICT-XSYN-USAGE)

* [F.14. earthdistance — calcular distâncias em círculo máximo](earthdistance.md)

+ [F.14.1. Distâncias à Terra baseadas em cubos](earthdistance.md#EARTHDISTANCE-CUBE-BASED)
+ [F.14.2. Distâncias à Terra baseadas em pontos](earthdistance.md#EARTHDISTANCE-POINT-BASED)

* [F.15. file_fdw — acesso a arquivos de dados no sistema de arquivos do servidor](file-fdw.md)
* [F.16. fuzzystrmatch — determinar semelhanças e distância de strings](fuzzystrmatch.md)

+ [F.16.1. Soundex](fuzzystrmatch.md#FUZZYSTRMATCH-SOUNDEX)
+ [F.16.2. Daitch-Mokotoff Soundex](fuzzystrmatch.md#FUZZYSTRMATCH-DAITCH-MOKOTOFF)
+ [F.16.3. Levenshtein](fuzzystrmatch.md#FUZZYSTRMATCH-LEVENSHTEIN)
+ [F.16.4. Metaphone](fuzzystrmatch.md#FUZZYSTRMATCH-METAPHONE)
+ [F.16.5. Double Metaphone](fuzzystrmatch.md#FUZZYSTRMATCH-DOUBLE-METAPHONE)

* [F.17. hstore — hstore chave/tipo de dado valor](hstore.md)

+ [F.17.1. `hstore` Representação Externa](hstore.md#HSTORE-EXTERNAL-REP)
+ [F.17.2. `hstore` Operadores e Funções](hstore.md#HSTORE-OPS-FUNCS)
+ [F.17.3. Índices](hstore.md#HSTORE-INDEXES)
+ [F.17.4. Exemplos](hstore.md#HSTORE-EXAMPLES)
+ [F.17.5. Estatísticas](hstore.md#HSTORE-STATISTICS)
+ [F.17.6. Compatibilidade](hstore.md#HSTORE-COMPATIBILITY)
+ [F.17.7. Transformações](hstore.md#HSTORE-TRANSFORMS)
+ [F.17.8. Autores](hstore.md#HSTORE-AUTHORS)

* [F.18. intagg — agregador e enumerador de inteiros](intagg.md)

+ [F.18.1. Funções](intagg.md#INTAGG-FUNCTIONS)
+ [F.18.2. Exemplos de uso](intagg.md#INTAGG-SAMPLES)

* [F.19. intarray — manipular arrays de inteiros](intarray.md)

+ [F.19.1. `intarray` Funções e Operadores](intarray.md#INTARRAY-FUNCS-OPS)
+ [F.19.2. Suporte de Índice](intarray.md#INTARRAY-INDEX)
+ [F.19.3. Exemplo](intarray.md#INTARRAY-EXAMPLE)
+ [F.19.4. Benchmark](intarray.md#INTARRAY-BENCHMARK)
+ [F.19.5. Autores](intarray.md#INTARRAY-AUTHORS)

* [F.20. isn — tipos de dados para números padrão internacional (ISBN, EAN, UPC, etc.)](isn.md)

+ [F.20.1. Tipos de Dados](isn.md#ISN-DATA-TYPES)
+ [F.20.2. Casts](isn.md#ISN-CASTS)
+ [F.20.3. Funções e Operadores](isn.md#ISN-FUNCS-OPS)
+ [F.20.4. Parâmetros de Configuração](isn.md#ISN-CONFIGURATION-PARAMETERS)
+ [F.20.5. Exemplos](isn.md#ISN-EXAMPLES)
+ [F.20.6. Bibliografia](isn.md#ISN-BIBLIOGRAPHY)
+ [F.20.7. Autor](isn.md#ISN-AUTHOR)

* [F.21. lo — gerenciar objetos grandes](lo.md)

+ [F.21.1. Razão][(lo.md#LO-RATIONALE)
+ [F.21.2. Como usá-lo][(lo.md#LO-HOW-TO-USE)
+ [F.21.3. Limitações][(lo.md#LO-LIMITATIONS)
+ [F.21.4. Autor][(lo.md#LO-AUTHOR)

* [F.22. ltree — tipo de dados hierárquico semelhante a uma árvore](ltree.md)

+ [F.22.1. Definições](ltree.md#LTREE-DEFINITIONS)
+ [F.22.2. Operadores e Funções](ltree.md#LTREE-OPS-FUNCS)
+ [F.22.3. Índices](ltree.md#LTREE-INDEXES)
+ [F.22.4. Exemplo](ltree.md#LTREE-EXAMPLE)
+ [F.22.5. Transformações](ltree.md#LTREE-TRANSFORMS)
+ [F.22.6. Autores](ltree.md#LTREE-AUTHORS)

* [F.23. pageinspect — inspeção de nível baixo de páginas de banco de dados](pageinspect.md)

+ [F.23.1. Funções Gerais](pageinspect.md#PAGEINSPECT-GENERAL-FUNCS)
+ [F.23.2. Funções de Pilha](pageinspect.md#PAGEINSPECT-HEAP-FUNCS)
+ [F.23.3. Funções de B-Tree](pageinspect.md#PAGEINSPECT-B-TREE-FUNCS)
+ [F.23.4. Funções BRIN](pageinspect.md#PAGEINSPECT-BRIN-FUNCS)
+ [F.23.5. Funções GIN](pageinspect.md#PAGEINSPECT-GIN-FUNCS)
+ [F.23.6. Funções GiST](pageinspect.md#PAGEINSPECT-GIST-FUNCS)
+ [F.23.7. Funções Hash](pageinspect.md#PAGEINSPECT-HASH-FUNCS)

* [F.24. passwordcheck — verificar a força da senha](passwordcheck.md)

+ [F.24.1. Parâmetros de Configuração](passwordcheck.md#PASSWORDCHECK-CONFIGURATION-PARAMETERS)

* [F.25. pg_buffercache — inspecionar o estado do cache de buffer do PostgreSQL](pgbuffercache.md)

+ [F.25.1. A Visão `pg_buffercache`](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE)
+ [F.25.2. A Visão `pg_buffercache_numa`](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-NUMA)
+ [F.25.3. A Função `pg_buffercache_summary()`](pgbuffercache.md#PGBUFFERCACHE-SUMMARY)
+ [F.25.4. A Função `pg_buffercache_usage_counts()`](pgbuffercache.md#PGBUFFERCACHE-USAGE-COUNTS)
+ [F.25.5. A Função `pg_buffercache_evict()`](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT)
+ [F.25.6. A Função `pg_buffercache_evict_relation()`](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-RELATION)
+ [F.25.7. A Função `pg_buffercache_evict_all()`](pgbuffercache.md#PGBUFFERCACHE-PG-BUFFERCACHE-EVICT-ALL)
+ [F.25.8. Saída de Amostra](pgbuffercache.md#PGBUFFERCACHE-SAMPLE-OUTPUT)
+ [F.25.9. Autores](pgbuffercache.md#PGBUFFERCACHE-AUTHORS)

* [F.26. pgcrypto — funções criptográficas](pgcrypto.md)

+ [F.26.1. Funções de Hashamento Geral](pgcrypto.md#PGCRYPTO-GENERAL-HASHING-FUNCS)
+ [F.26.2. Funções de Hash de Senhas](pgcrypto.md#PGCRYPTO-PASSWORD-HASHING-FUNCS)
+ [F.26.3. Funções de Criptografia PGP](pgcrypto.md#PGCRYPTO-PGP-ENC-FUNCS)
+ [F.26.4. Funções de Criptografia Raw](pgcrypto.md#PGCRYPTO-RAW-ENC-FUNCS)
+ [F.26.5. Funções de Dados Aleatórios](pgcrypto.md#PGCRYPTO-RANDOM-DATA-FUNCS)
+ [F.26.6. Funções de Suporte OpenSSL](pgcrypto.md#PGCRYPTO-OPENSSL-SUPPORT-FUNCS)
+ [F.26.7. Parâmetros de Configuração](pgcrypto.md#PGCRYPTO-CONFIGURATION-PARAMETERS)
+ [F.26.8. Notas](pgcrypto.md#PGCRYPTO-NOTES)
+ [F.26.9. Autor](pgcrypto.md#PGCRYPTO-AUTHOR)

* [F.27. pg_freespacemap — examinar o mapa de espaço livre](pgfreespacemap.md)

+ [F.27.1. Funções](pgfreespacemap.md#PGFREESPACEMAP-FUNCS)
+ [F.27.2. Saída de amostra](pgfreespacemap.md#PGFREESPACEMAP-SAMPLE-OUTPUT)
+ [F.27.3. Autor](pgfreespacemap.md#PGFREESPACEMAP-AUTHOR)

* [F.28. pg_logicalinspect — inspeção de componentes de decodificação lógica](pglogicalinspect.md)

+ [F.28.1. Funções](pglogicalinspect.md#PGLOGICALINSPECT-FUNCS)
+ [F.28.2. Autor](pglogicalinspect.md#PGLOGICALINSPECT-AUTHOR)

* [F.29. pg_overexplain — permitir que o EXPLAIN descarregue ainda mais detalhes](pgoverexplain.md)

+ [F.29.1. EXPLICAR (DEBUSTO)](pgoverexplain.md#PGOVEREXPLAIN-DEBUG)
+ [F.29.2. EXPLICAR (TABELA DE CAMADAS DE LIGAÇÃO)](pgoverexplain.md#PGOVEREXPLAIN-RANGE-TABLE)
+ [F.29.3. Autor](pgoverexplain.md#PGOVEREXPLAIN-AUTHOR)

* [F.30. pg_prewarm — pré-carregar dados de relação em caches de buffer](pgprewarm.md)

+ [F.30.1. Funções](pgprewarm.md#PGPREWARM-FUNCS)
+ [F.30.2. Parâmetros de Configuração](pgprewarm.md#PGPREWARM-CONFIG-PARAMS)
+ [F.30.3. Autor](pgprewarm.md#PGPREWARM-AUTHOR)

* [F.31. pgrowlocks — mostrar informações de bloqueio de linha de uma tabela](pgrowlocks.md)

+ [F.31.1. Visão geral](pgrowlocks.md#PGROWLOCKS-OVERVIEW)
+ [F.31.2. Saída de amostra](pgrowlocks.md#PGROWLOCKS-SAMPLE-OUTPUT)
+ [F.31.3. Autor](pgrowlocks.md#PGROWLOCKS-AUTHOR)

* [F.32. pg_stat_statements — acompanhar estatísticas de planejamento e execução de SQL](pgstatstatements.md)

+ [F.32.1. A Visão do `pg_stat_statements`](pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS)
+ [F.32.2. A Visão do `pg_stat_statements_info`](pgstatstatements.md#PGSTATSTATEMENTS-PG-STAT-STATEMENTS-INFO)
+ [F.32.3. Funções](pgstatstatements.md#PGSTATSTATEMENTS-FUNCS)
+ [F.32.4. Parâmetros de Configuração](pgstatstatements.md#PGSTATSTATEMENTS-CONFIG-PARAMS)
+ [F.32.5. Saída de Amostra](pgstatstatements.md#PGSTATSTATEMENTS-SAMPLE-OUTPUT)
+ [F.32.6. Autores](pgstatstatements.md#PGSTATSTATEMENTS-AUTHORS)

* [F.33. pgstattuple — obter estatísticas em nível de tupla](pgstattuple.md)

+ [F.33.1. Funções](pgstattuple.md#PGSTATTUPLE-FUNCS)
+ [F.33.2. Autores](pgstattuple.md#PGSTATTUPLE-AUTHORS)

* [F.34. pg_surgery — realizar cirurgia de baixo nível em dados de relação](pgsurgery.md)

+ [F.34.1. Funções](pgsurgery.md#PGSURGERY-FUNCS)
+ [F.34.2. Autores](pgsurgery.md#PGSURGERY-AUTHORS)

* [F.35. pg_trgm — suporte para similaridade de texto usando correspondência de trigramas](pgtrgm.md)

+ [F.35.1. Conceitos de Trigrama (ou Trigráfico)](pgtrgm.md#PGTRGM-CONCEPTS)
+ [F.35.2. Funções e Operadores](pgtrgm.md#PGTRGM-FUNCS-OPS)
+ [F.35.3. Parâmetros do GUC](pgtrgm.md#PGTRGM-GUC)
+ [F.35.4. Suporte a Índice](pgtrgm.md#PGTRGM-INDEX)
+ [F.35.5. Integração de Pesquisa de Texto](pgtrgm.md#PGTRGM-TEXT-SEARCH)
+ [F.35.6. Referências](pgtrgm.md#PGTRGM-REFERENCES)
+ [F.35.7. Autores](pgtrgm.md#PGTRGM-AUTHORS)

* [F.36. pg_visibility — informações e utilitários do mapa de visibilidade](pgvisibility.md)

+ [F.36.1. Funções](pgvisibility.md#PGVISIBILITY-FUNCS)
+ [F.36.2. Autor](pgvisibility.md#PGVISIBILITY-AUTHOR)

* [F.37. pg_walinspect — inspeção de WAL de nível baixo](pgwalinspect.md)

+ [F.37.1. Funções Gerais](pgwalinspect.md#PGWALINSPECT-FUNCS)
+ [F.37.2. Autor](pgwalinspect.md#PGWALINSPECT-AUTHOR)

* [F.38. postgres_fdw — acesso a dados armazenados em servidores PostgreSQL externos](postgres-fdw.md)

+ [F.38.1. Opções de FDW de postgres_fdw](postgres-fdw.md#POSTGRES-FDW-OPTIONS)
+ [F.38.2. Funções](postgres-fdw.md#POSTGRES-FDW-FUNCTIONS)
+ [F.38.3. Gerenciamento de Conexão](postgres-fdw.md#POSTGRES-FDW-CONNECTION-MANAGEMENT)
+ [F.38.4. Gerenciamento de Transação](postgres-fdw.md#POSTGRES-FDW-TRANSACTION-MANAGEMENT)
+ [F.38.5. Otimização de Consulta Remota](postgres-fdw.md#POSTGRES-FDW-REMOTE-QUERY-OPTIMIZATION)
+ [F.38.6. Ambiente de Execução de Consulta Remota](postgres-fdw.md#POSTGRES-FDW-REMOTE-QUERY-EXECUTION-ENVIRONMENT)
+ [F.38.7. Compatibilidade entre Versões Cruzadas](postgres-fdw.md#POSTGRES-FDW-CROSS-VERSION-COMPATIBILITY)
+ [F.38.8. Eventos de Aguardar](postgres-fdw.md#POSTGRES-FDW-WAIT-EVENTS)
+ [F.38.9. Parâmetros de Configuração](postgres-fdw.md#POSTGRES-FDW-CONFIGURATION-PARAMETERS)
+ [F.38.10. Exemplos](postgres-fdw.md#POSTGRES-FDW-EXAMPLES)
+ [F.38.11. Autor](postgres-fdw.md#POSTGRES-FDW-AUTHOR)

* [F.39. seg — um tipo de dado para segmentos de linha ou intervalos de ponto flutuante](seg.md)

+ [F.39.1. Raciocínio](seg.md#SEG-RATIONALE)
+ [F.39.2. Sintaxe](seg.md#SEG-SYNTAX)
+ [F.39.3. Precisão](seg.md#SEG-PRECISION)
+ [F.39.4. Uso](seg.md#SEG-USAGE)
+ [F.39.5. Notas](seg.md#SEG-NOTES)
+ [F.39.6. Créditos](seg.md#SEG-CREDITS)

* [F.40. sepgsql — Módulo de segurança de controle de acesso obrigatório (MAC) baseado em SELinux e rótulo](sepgsql.md)

+ [F.40.1. Visão geral](sepgsql.md#SEPGSQL-OVERVIEW)
+ [F.40.2. Instalação](sepgsql.md#SEPGSQL-INSTALLATION)
+ [F.40.3. Testes de regressão](sepgsql.md#SEPGSQL-REGRESSION)
+ [F.40.4. Parâmetros do GUC](sepgsql.md#SEPGSQL-PARAMETERS)
+ [F.40.5. Recursos](sepgsql.md#SEPGSQL-FEATURES)
+ [F.40.6. Funções Sepgsql](sepgsql.md#SEPGSQL-FUNCTIONS)
+ [F.40.7. Limitações](sepgsql.md#SEPGSQL-LIMITATIONS)
+ [F.40.8. Recursos externos](sepgsql.md#SEPGSQL-RESOURCES)
+ [F.40.9. Autor](sepgsql.md#SEPGSQL-AUTHOR)

* [F.41. spi — Recursos/exemplos de interface de programação do servidor](contrib-spi.md)

+ [F.41.1. refint — Funções para implementar integridade referencial](contrib-spi.md#CONTRIB-SPI-REFINT)
+ [F.41.2. autoinc — Funções para autoincremento de campos](contrib-spi.md#CONTRIB-SPI-AUTOINC)
+ [F.41.3. insert_username — Funções para rastrear quem modificou uma tabela](contrib-spi.md#CONTRIB-SPI-INSERT-USERNAME)
+ [F.41.4. moddatetime — Funções para rastrear a última hora de modificação](contrib-spi.md#CONTRIB-SPI-MODDATETIME)

* [F.42. sslinfo — obter informações SSL do cliente](sslinfo.md)

+ [F.42.1. Funções Fornecidas](sslinfo.md#SSLINFO-FUNCTIONS)
+ [F.42.2. Autor](sslinfo.md#SSLINFO-AUTHOR)

* [F.43. tablefunc — funções que retornam tabelas (`crosstab` e outras)](tablefunc.md)

+ [F.43.1. Funções Fornecidas](tablefunc.md#TABLEFUNC-FUNCTIONS-SECT)
+ [F.43.2. Autor](tablefunc.md#TABLEFUNC-AUTHOR)

* [F.44. tcn — uma função de disparo para notificar os ouvintes sobre alterações no conteúdo da tabela](tcn.md)
* [F.45. test_decoding — módulo de teste/exemplo baseado em SQL para decodificação lógica do WAL](test-decoding.md)
* [F.46. tsm_system_rows — o método de amostragem `SYSTEM_ROWS` para `TABLESAMPLE`](tsm-system-rows.md)

+ [F.46.1. Exemplos](tsm-system-rows.md#TSM-SYSTEM-ROWS-EXAMPLES)

* [F.47. tsm_system_time — o método de amostragem `SYSTEM_TIME` para `TABLESAMPLE`](tsm-system-time.md)

+ [F.47.1. Exemplos](tsm-system-time.md#TSM-SYSTEM-TIME-EXAMPLES)

* [F.48. unaccent — um dicionário de busca de texto que remove diacríticos](unaccent.md)

+ [F.48.1. Configuração](unaccent.md#UNACCENT-CONFIGURATION)
+ [F.48.2. Uso](unaccent.md#UNACCENT-USAGE)
+ [F.48.3. Funções](unaccent.md#UNACCENT-FUNCTIONS)

* [F.49. uuid-ossp — um gerador de UUID](uuid-ossp.md)

+ [F.49.1. `uuid-ossp` Funções](uuid-ossp.md#UUID-OSSP-FUNCTIONS-SECT)
+ [F.49.2. Edifício `uuid-ossp`](uuid-ossp.md#UUID-OSSP-BUILDING)
+ [F.49.3. Autor](uuid-ossp.md#UUID-OSSP-AUTHOR)

* [F.50. xml2 — Consulta XPath e funcionalidades XSLT](xml2.md)

+ [F.50.1. Aviso de Depreciação](xml2.md#XML2-DEPRECATION)
+ [F.50.2. Descrição das Funções](xml2.md#XML2-FUNCTIONS)
+ [F.50.3. `xpath_table`](xml2.md#XML2-XPATH-TABLE)
+ [F.50.4. Funções XSLT](xml2.md#XML2-XSLT)
+ [F.50.5. Autor](xml2.md#XML2-AUTHOR)

Este apêndice e o próximo contêm informações sobre os componentes opcionais encontrados no diretório `contrib` da distribuição PostgreSQL. Esses incluem ferramentas de porting, utilitários de análise e recursos de plug-in que não fazem parte do sistema PostgreSQL básico. Eles são separados principalmente porque atendem a um público limitado ou são muito experimentais para fazer parte da árvore de fonte principal. Isso não exclui sua utilidade.

Este apêndice abrange extensões e outras bibliotecas de módulos de plug-in do servidor encontradas em `contrib`. [Apêndice G](contrib-prog.md "Appendix G. Additional Supplied Programs") abrange programas utilitários.

Ao construir a partir da distribuição de origem, esses componentes opcionais não são construídos automaticamente, a menos que você construa o alvo "mundo" (consulte [Passo 2](install-make.md#BUILD)). Você pode construir e instalar todos eles executando:

```
make
make install
```

no diretório `contrib` de uma árvore de origem configurada; ou para construir e instalar apenas um módulo selecionado, faça o mesmo no subdiretório do módulo. Muitos dos módulos têm testes de regressão, que podem ser executados executando:

```
make check
```

antes da instalação ou

```
make installcheck
```

uma vez que você tenha um servidor PostgreSQL em execução.

Se você estiver usando uma versão pré-embalada do PostgreSQL, esses componentes são normalmente disponibilizados como um subpacote separado, como `postgresql-contrib`.

Muitos componentes fornecem novas funções definidas pelo usuário, operadores ou tipos, embalados como *extensões*. Para usar uma dessas extensões, após instalar o código necessário, você deve registrar os novos objetos SQL no sistema de banco de dados. Isso é feito executando um comando [CREATE EXTENSION](sql-createextension.md). Em um banco de dados novo, você pode simplesmente fazer

```
CREATE EXTENSION extension_name;
```

Este comando registra os novos objetos SQL apenas no banco de dados atual, portanto, você precisa executá-lo em todos os bancos nos quais você deseja que as facilidades da extensão estejam disponíveis. Alternativamente, execute-o no banco de dados `template1` para que a extensão seja copiada por padrão em bancos criados posteriormente.

Para todas as extensões, o comando `CREATE EXTENSION` deve ser executado por um superusuário do banco de dados, a menos que a extensão seja considerada “confiável”. Extensões confiáveis podem ser executadas por qualquer usuário que tenha privilégio `CREATE` no banco de dados atual. As extensões confiáveis são identificadas como tais nas seções que se seguem. Geralmente, as extensões confiáveis são aquelas que não podem fornecer acesso a funcionalidades externas ao banco de dados.

As seguintes extensões são confiáveis em uma instalação padrão:



<table border="0" class="simplelist" summary="Simple list">
 <tr>
  <td>
   <a class="xref" href="btree-gin.md" title="F.7. btree_gin — GIN operator classes with B-tree behavior">
    btree_gin
   </a>
  </td>
  <td>
   <a class="xref" href="fuzzystrmatch.md" title="F.16. fuzzystrmatch — determine string similarities and distance">
    fuzzystrmatch
   </a>
  </td>
  <td>
   <a class="xref" href="ltree.md" title="F.22. ltree — hierarchical tree-like data type">
    ltree
   </a>
  </td>
  <td>
   <a class="xref" href="tcn.md" title="F.44. tcn — a trigger function to notify listeners of changes to table content">
    tcn
   </a>
  </td>
 </tr>
 <tr>
  <td>
   <a class="xref" href="btree-gist.md" title="F.8. btree_gist — GiST operator classes with B-tree behavior">
    btree_gist
   </a>
  </td>
  <td>
   <a class="xref" href="hstore.md" title="F.17. hstore — hstore key/value datatype">
    hstore
   </a>
  </td>
  <td>
   <a class="xref" href="pgcrypto.md" title="F.26. pgcrypto — cryptographic functions">
    pgcrypto
   </a>
  </td>
  <td>
   <a class="xref" href="tsm-system-rows.md" title="F.46. tsm_system_rows — the SYSTEM_ROWS sampling method for TABLESAMPLE">
    tsm_system_rows
   </a>
  </td>
 </tr>
 <tr>
  <td>
   <a class="xref" href="citext.md" title="F.9. citext — a case-insensitive character string type">
    citext
   </a>
  </td>
  <td>
   <a class="xref" href="intarray.md" title="F.19. intarray — manipulate arrays of integers">
    intarray
   </a>
  </td>
  <td>
   <a class="xref" href="pgtrgm.md" title="F.35. pg_trgm — support for similarity of text using trigram matching">
    pg_trgm
   </a>
  </td>
  <td>
   <a class="xref" href="tsm-system-time.md" title="F.47. tsm_system_time — the SYSTEM_TIME sampling method for TABLESAMPLE">
    tsm_system_time
   </a>
  </td>
 </tr>
 <tr>
  <td>
   <a class="xref" href="cube.md" title="F.10. cube — a multi-dimensional cube data type">
    cube
   </a>
  </td>
  <td>
   <a class="xref" href="isn.md" title="F.20. isn — data types for international standard numbers (ISBN, EAN, UPC, etc.)">
    isn
   </a>
  </td>
  <td>
   <a class="xref" href="seg.md" title="F.39. seg — a datatype for line segments or floating point intervals">
    seg
   </a>
  </td>
  <td>
   <a class="xref" href="unaccent.md" title="F.48. unaccent — a text search dictionary which removes diacritics">
    unaccent
   </a>
  </td>
 </tr>
 <tr>
  <td>
   <a class="xref" href="dict-int.md" title="F.12. dict_int — example full-text search dictionary for integers">
    dict_int
   </a>
  </td>
  <td>
   <a class="xref" href="lo.md" title="F.21. lo — manage large objects">
    lo
   </a>
  </td>
  <td>
   <a class="xref" href="tablefunc.md" title="F.43. tablefunc — functions that return tables (crosstab and others)">
    tablefunc
   </a>
  </td>
  <td>
   <a class="xref" href="uuid-ossp.md" title="F.49. uuid-ossp — a UUID generator">
    uuid-ossp
   </a>
  </td>
 </tr>
</table>







Muitas extensões permitem que você instale seus objetos em um esquema de sua escolha. Para fazer isso, adicione `SCHEMA schema_name` ao comando `CREATE EXTENSION`. Por padrão, os objetos serão colocados no seu esquema atual de destino de criação, que, por sua vez, é padrão para `public`.

Observe, no entanto, que alguns desses componentes não são “extensões” nesse sentido, mas são carregados no servidor de alguma outra forma, por exemplo, por meio de [shared_preload_libraries](runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES). Consulte a documentação de cada componente para obter detalhes.