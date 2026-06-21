# Parte VIII. Apêndices

**Índice**

* [A. Códigos de Erro do PostgreSQL](errcodes-appendix.md)
* [B. Suporte de Data/Hora](datetime-appendix.md)

+ [B.1. Interpretação de Entrada de Data/Hora](datetime-input-rules.md)
+ [B.2. Tratamento de Timestamps Inválidos ou Ambíguos](datetime-invalid-input.md)
+ [B.3. Palavras-chave de Data/Hora](datetime-keywords.md)
+ [B.4. Arquivos de Configuração de Data/Hora](datetime-config-files.md)
+ [B.5. Especificações de Fuso Horário POSIX](datetime-posix-timezone-specs.md)
+ [B.6. Histórico de Unidades](datetime-units-history.md)
+ [B.7. Datas Julianas](datetime-julian-dates.md)

* [C. Palavras-chave SQL](sql-keywords-appendix.md)
* [D. Conformidade SQL](features.md)

+ [D.1. Recursos suportados](features-sql-standard.md)
+ [D.2. Recursos não suportados](unsupported-features-sql-standard.md)
+ [D.3. Limites XML e conformidade com SQL/XML](xml-limits-conformance.md)

* [Notas de lançamento][(release.md)]

+ [E.1. Versão 18.4](release-18-4.md)
+ [E.2. Versão 18.3](release-18-3.md)
+ [E.3. Versão 18.2](release-18-2.md)
+ [E.4. Versão 18.1](release-18-1.md)
+ [E.5. Versão 18](release-18.md)
+ [E.6. Versões anteriores](release-prior.md)

* [F. Módulos e extensões adicionais fornecidos](contrib.md)

+ [F.1. amcheck — ferramentas para verificar a consistência de tabelas e índices](amcheck.md)
+ [F.2. auth_delay — pausar a autenticação em caso de falha](auth-delay.md)
+ [F.3. auto_explain — registrar os planos de execução de consultas lentas](auto-explain.md)
+ [F.4. basebackup_to_shell — exemplo de módulo "shell" pg_basebackup](basebackup-to-shell.md)
+ [F.5. basic_archive — exemplo de módulo de arquivo WAL](basic-archive.md)
+ [F.6. bloom — método de acesso a índices de filtro de bloom](bloom.md)
+ [F.7. btree_gin — classes de operadores GIN com comportamento de árvore B](btree-gin.md)
+ [F.8. btree_gist — classes de operadores GiST com comportamento de árvore B](btree-gist.md)
+ [F.9. citext — tipo de cadeia de caracteres sensível a maiúsculas e minúsculas](citext.md)
+ [F.10. cube — tipo de dados de cubo multidimensional](cube.md)
+ [F.11. dblink — conectar-se a outros bancos de dados PostgreSQL](dblink.md)
+ [F.12. dict_int — exemplo de dicionário de busca full-text para inteiros](dict-int.md)
+ [F.13. dict_xsyn — exemplo de dicionário de busca full-text de sinônimos](dict-xsyn.md)
+ [F.14. earthdistance — calcular distâncias em círculo máximo](earthdistance.md)
+ [F.15. file_fdw — acessar arquivos de dados no sistema de arquivos do servidor](file-fdw.md)
+ [F.16. fuzzystrmatch — determinar semelhanças e distância de cadeias de caracteres](fuzzystrmatch.md)
+ [F.17. hstore — datatype de chave/valor hstore](hstore.md)
+ [F.18. intagg — agregador e enumerador de inteiros](intagg.md)
+ [F.19. intarray — manipulação de arrays de inteiros](intarray.md)
+ [F.20. isn — tipos de dados para números padrão internacionais (ISBN, EAN, UPC, etc.)](isn.md)
+ [F.21. lo — gerenciamento de objetos grandes](lo.md)
+ [F.22. ltree — tipo de dados hierárquico semelhante a uma árvore](ltree.md)
+ [F.23. pageinspect — inspeção de nível baixo de páginas de banco de dados](pageinspect.md)
+ [F.24. passwordcheck — verificar a força da senha](passwordcheck.md)
+ [F.25. pg_buffercache — inspeção do estado da cache de buffer de PostgreSQL](pgbuffercache.md)
+ [F.26. pgcrypto — funções criptográficas](pgcrypto.md)
+ [F.27. pg_freespacemap — exame do mapa de espaço livre](pgfreespacemap.md)
+ [F.28. pg_logicalinspect — inspeção de componentes de decodificação lógica](pglogicalinspect.md)
+ [F.29. pg_overexplain — permitir que o EXPLAIN gere ainda mais detalhes](pgoverexplain.md)
+ [F.30. pg_prewarm — pré-carregar dados de relação em caches de buffer](pgprewarm.md)
+ [F.31. pgrowlocks — informações de bloqueio de linha de tabela e utilitários](pgrowlocks.md)
+ [F.32. pg_stat_statements — acompanhamento das estatísticas de planejamento e execução SQL](pgstatstatements.md)
+ [F.33. pgstattuple — obtenção de estatísticas de nível de tupla](pgstattuple.md)
+ [F.34. pg_surgery — cirurgia de baixo nível em dados de relação](pgsurgery.md)
+ [F.35. pg_trgm — suporte para similaridade de texto usando trigramamento](pgtrgm.md)
+ [F.36. pg_visibility — informações de mapa de visibilidade e utilitários](pgvisibility.md)
+ [F.37. pg_walinspect — inspeção de baixo nível de WAL](pgwalinspect.md)
+ [F.38. postgres_fdw — acesso a dados armazenados em servidores PostgreSQL externos](postgres-fdw.md)
+ [F.39. seg — um datatype para segmentos de linha ou intervalos de ponto flutuante](seg.md)
+ [F.40. sepgsql — módulo de SELinux, com controle de acesso obrigatório baseado em rótulos (MAC)](sepgsql.md)
+ [F.41. spi — recursos de interface de programação do servidor/exemplos](contrib-spi.md)
+ [F.42. sslinfo — obtenção de informações sobre SSL do cliente](sslinfo.md)
+ [F.43. tablefunc — funções que retornam tabelas (`crosstab` e outros)](tablefunc.md)
+ [F.44. tcn — uma função de gatilho para notificar os ouvintes sobre alterações no conteúdo da tabela](tcn.md)
+ [F.45. test_decoding — módulo de exemplo/teste baseado em SQL para decodificação lógica de WAL](test-decoding.md)
+ [F.46. tsm_system_rows — o método de amostragem `SYSTEM_ROWS` para `TABLESAMPLE`(tsm-system-rows.md)
+ [F.47. tsm_system_time — o método de amostragem `SYSTEM_TIME` para `TABLESAMPLE`(tsm-system-time.md)

* [Programas adicionais fornecidos][(contrib-prog.md)]

+ [G.1. Aplicações de Cliente](contrib-prog-client.md)
+ [G.2. Aplicações de Servidor](contrib-prog-server.md)

* [Projetos Externos](external-projects.md)

+ [H.1. Interfaces do Cliente](external-interfaces.md)
+ [H.2. Ferramentas de Administração](external-admin-tools.md)
+ [H.3. Linguagens Procedimentais](external-pl.md)
+ [H.4. Extensões](external-extensions.md)

* [Repositório de Código-fonte][(sourcerepo.md)]

+ [I.1. Obter a fonte via Git](git.md)

* [Documentação](docguide.md)

+ [J.1. DocBook][(docguide-docbook.md)]
+ [J.2. Conjuntos de Ferramentas][(docguide-toolsets.md)]
+ [J.3. Construção da Documentação com Make][(docguide-build.md)]
+ [J.4. Construção da Documentação com Meson][(docguide-build-meson.md)]
+ [J.5. Autoria da Documentação][(docguide-authoring.md)]
+ [J.6. Guia de Estilo][(docguide-style.md)]

* [K. Limites do PostgreSQL](limits.md)
* [L. Abreviações](acronyms.md)
* [M. Glossário](glossary.md)
* [N. Suporte a cores](color.md)

+ [N.1. Quando a cor é usada](color-when.md)
+ [N.2. Configurando as cores](color-which.md)

* [Recursos obsoletos ou renomeados][(appendix-obsolete.md)]

+ [O.1. O arquivo `recovery.conf` foi incorporado ao `postgresql.conf`](recovery-config.md)
+ [O.2. Os papéis padrão renomeados para papéis pré-definidos](default-roles.md)
+ [O.3. `pg_xlogdump` renomeado para `pg_waldump`](pgxlogdump.md)
+ [O.4. `pg_resetxlog` renomeado para `pg_resetwal`](app-pgresetxlog.md)
+ [O.5. `pg_receivexlog` renomeado para `pg_receivewal`](app-pgreceivexlog.md)