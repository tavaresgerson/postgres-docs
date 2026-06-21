# Parte III. Administração do servidor

Esta parte abrange tópicos que são de interesse para um administrador do PostgreSQL. Isso inclui instalação, configuração do servidor, gerenciamento de usuários e bancos de dados, e tarefas de manutenção. Qualquer pessoa que esteja executando o servidor PostgreSQL, mesmo para uso pessoal, mas especialmente em produção, deve estar familiarizada com esses tópicos.

A informação tenta ser apresentada na ordem em que um novo usuário deve lê-la. Os capítulos são autocontidos e podem ser lidos individualmente, conforme desejado. A informação é apresentada em forma narrativa em unidades temáticas. Os leitores que procuram uma descrição completa de um comando são incentivados a revisar o [Parte VI][(reference.md "Part VI. Reference")].

Os primeiros capítulos são escritos para que possam ser compreendidos sem conhecimento prévio, para que novos usuários que precisam configurar seu próprio servidor possam começar sua exploração. O restante desta parte trata de ajuste e gerenciamento; esse material assume que o leitor está familiarizado com o uso geral do sistema de banco de dados PostgreSQL. Os leitores são incentivados a revisar as partes [Parte I][(tutorial.md "Part I. Tutorial")] e [Parte II][(sql.md "Part II. The SQL Language")] para obter informações adicionais.

**Índice**

* [16. Instalação a partir de Binários](install-binaries.md)
* [17. Instalação a partir de Código-fonte](installation.md)

+ [17.1. Requisitos][(install-requirements.md)]
+ [17.2. Obter a Fonte][(install-getsource.md)]
+ [17.3. Construção e Instalação com Autoconf e Make][(install-make.md)]
+ [17.4. Construção e Instalação com Meson][(install-meson.md)]
+ [17.5. Configuração Pós-Instalação][(install-post.md)]
+ [17.6. Plataformas Suporteadas][(supported-platforms.md)]
+ [17.7. Notas Específicas da Plataforma][(installation-platform-notes.md)]

* [18. Configuração e Operação do Servidor](runtime.md)

+ [18.1. Conta de Usuário do PostgreSQL][(postgres-user.md)]
+ [18.2. Criando um Clúster de Banco de Dados][(creating-cluster.md)]
+ [18.3. Iniciando o Servidor de Banco de Dados][(server-start.md)]
+ [18.4. Gerenciando Recursos do Kernel][(kernel-resources.md)]
+ [18.5. Desligando o Servidor][(server-shutdown.md)]
+ [18.6. Atualizando um Clúster do PostgreSQL][(upgrading.md)]
+ [18.7. Prevenindo Spoofing do Servidor][(preventing-server-spoofing.md)]
+ [18.8. Opções de Criptografia][(encryption-options.md)]
+ [18.9. Conexões TCP/IP Seguras com SSL][(ssl-tcp.md)]
+ [18.10. Conexões TCP/IP Seguras com Criptografia GSSAPI][(gssapi-enc.md)]
+ [18.11. Conexões TCP/IP Seguras com Túneis SSH][(ssh-tunnels.md)]
+ [18.12. Registrando o Diário de Eventos no Windows][(event-log-registration.md)]

* [19. Configuração do servidor](runtime-config.md)

+ [19.1. Configuração de Parâmetros](config-setting.md)
+ [19.2. Localizações de Arquivos](runtime-config-file-locations.md)
+ [19.3. Conexões e Autenticação](runtime-config-connection.md)
+ [19.4. Consumo de Recursos](runtime-config-resource.md)
+ [19.5. Log de Escrita Antecipada](runtime-config-wal.md)
+ [19.6. Replicação](runtime-config-replication.md)
+ [19.7. Planejamento de Consulta](runtime-config-query.md)
+ [19.8. Relatório de Erros e Registro](runtime-config-logging.md)
+ [19.9. Estatísticas de Tempo Real](runtime-config-statistics.md)
+ [19.10. Vacúmen](runtime-config-vacuum.md)
+ [19.11. Padrões Padrão de Conexão do Cliente](runtime-config-client.md)
+ [19.12. Gerenciamento de Bloqueio](runtime-config-locks.md)
+ [19.13. Compatibilidade de Versão e Plataforma](runtime-config-compatible.md)
+ [19.14. Tratamento de Erros](runtime-config-error-handling.md)
+ [19.15. Opções Predefinidas](runtime-config-preset.md)
+ [19.16. Opções Personalizadas](runtime-config-custom.md)
+ [19.17. Opções para Desenvolvedores](runtime-config-developer.md)
+ [19.18. Opções Breves](runtime-config-short.md)

* [Autenticação do cliente][(client-authentication.md)]

+ [20.1. Arquivo `pg_hba.conf`](auth-pg-hba-conf.md)
+ [20.2. Mapas de Nome do Usuário](auth-username-maps.md)
+ [20.3. Métodos de Autenticação](auth-methods.md)
+ [20.4. Autenticação de Confiança](auth-trust.md)
+ [20.5. Autenticação por Senha](auth-password.md)
+ [20.6. Autenticação GSSAPI](gssapi-auth.md)
+ [20.7. Autenticação SSPI](sspi-auth.md)
+ [20.8. Autenticação Ident](auth-ident.md)
+ [20.9. Autenticação Peer](auth-peer.md)
+ [20.10. Autenticação LDAP](auth-ldap.md)
+ [20.11. Autenticação RADIUS](auth-radius.md)
+ [20.12. Autenticação por Certificado](auth-cert.md)
+ [20.13. Autenticação PAM](auth-pam.md)
+ [20.14. Autenticação BSD](auth-bsd.md)
+ [20.15. Autenticação/Autorização OAuth](auth-oauth.md)
+ [20.16. Problemas de Autenticação](client-authentication-problems.md)

* [21. Papéis de banco de dados](user-manag.md)

+ [21.1. Papéis de banco de dados](database-roles.md)
+ [21.2. Atributos de papel](role-attributes.md)
+ [21.3. Membros do papel](role-membership.md)
+ [21.4. Remoção de papéis](role-removal.md)
+ [21.5. Papéis predefinidos](predefined-roles.md)
+ [21.6. Segurança de função](perm-functions.md)

* [22. Gerenciamento de bancos de dados](managing-databases.md)

+ [22.1. Visão geral][(manage-ag-overview.md)]
+ [22.2. Criando um banco de dados][(manage-ag-createdb.md)]
+ [22.3. Bancos de dados de modelo][(manage-ag-templatedbs.md)]
+ [22.4. Configuração do banco de dados][(manage-ag-config.md)]
+ [22.5. Destruição de um banco de dados][(manage-ag-dropdb.md)]
+ [22.6. Espaços de tabelas][(manage-ag-tablespaces.md)]

* [23. Localização](charset.md)

+ [23.1. Suporte a localização](locale.md)
+ [23.2. Suporte de colagem](collation.md)
+ [23.3. Suporte a conjunto de caracteres](multibyte.md)

* [24. Tarefas de manutenção de banco de dados de rotina](maintenance.md)

+ [24.1. Aspiração de rotina](routine-vacuuming.md)
+ [24.2. Reindexação de rotina](routine-reindex.md)
+ [24.3. Manutenção de arquivo de registro](logfile-maintenance.md)

* [25. Backup e Restauração](backup.md)

+ [25.1. Dump de SQL](backup-dump.md)
+ [25.2. Backup em nível de sistema de arquivos](backup-file.md)
+ [25.3. Arquivamento contínuo e recuperação ponto em tempo (PITR)](continuous-archiving.md)

* Disponibilidade alta, balanceamento de carga e replicação (high-availability.md)

+ [26.1. Comparação de diferentes soluções][(different-replication-solutions.md)]
+ [26.2. Servidores de espera de envio de logs][(warm-standby.md)]
+ [26.3. Failover][(warm-standby-failover.md)]
+ [26.4. Standby quente][(hot-standby.md)]

* [27. Monitoramento da atividade do banco de dados](monitoring.md)

+ [27.1. Ferramentas Unix Padrão][(monitoring-ps.md)]
+ [27.2. O Sistema de Estatísticas Cumulativas][(monitoring-stats.md)]
+ [27.3. Visualização de Controles][(monitoring-locks.md)]
+ [27.4. Relatórios de Progresso][(progress-reporting.md)]
+ [27.5. Rastreamento Dinâmico][(dynamic-trace.md)]
+ [27.6. Monitoramento do Uso do Disco][(diskusage.md)]

* [28. Confiabilidade e o Log de Escrita Antecipada](wal.md)

+ [28.1. Confiabilidade][(wal-reliability.md)]
+ [28.2. Checagens de dados][(checksums.md)]
+ [28.3. Registro prévio de escrita (WAL)][(wal-intro.md)]
+ [28.4. Compromisso assíncrono][(wal-async-commit.md)]
+ [28.5. Configuração WAL][(wal-configuration.md)]
+ [28.6. Interiores do WAL][(wal-internals.md)]

* [29. Replicação lógica](logical-replication.md)

+ [29.1. Publicação][(logical-replication-publication.md)]
+ [29.2. Assinatura][(logical-replication-subscription.md)]
+ [29.3. Failover de replicação lógica][(logical-replication-failover.md)]
+ [29.4. Filtros de linha][(logical-replication-row-filter.md)]
+ [29.5. Listas de colunas][(logical-replication-col-lists.md)]
+ [29.6. Replicação de coluna gerada][(logical-replication-gencols.md)]
+ [29.7. Conflitos][(logical-replication-conflicts.md)]
+ [29.8. Restrições][(logical-replication-restrictions.md)]
+ [29.9. Arquitetura][(logical-replication-architecture.md)]
+ [29.10. Monitoramento][(logical-replication-monitoring.md)]
+ [29.11. Segurança][(logical-replication-security.md)]
+ [29.12. Configurações de configuração][(logical-replication-config.md)]
+ [29.13. Atualização][(logical-replication-upgrade.md)]
+ [29.14. Configuração rápida][(logical-replication-quick-setup.md)]

* Compilação Just-in-Time (JIT) [(jit.md)]

+ [30.1. O que é a compilação JIT?](jit-reason.md)
+ [30.2. Quando usar JIT?](jit-decision.md)
+ [30.3. Configuração](jit-configuration.md)
+ [30.4. Extensibilidade](jit-extensibility.md)

* [31. Testes de Regressão](regress.md)

+ [31.1. Realização dos testes][(regress-run.md)]
+ [31.2. Avaliação dos testes][(regress-evaluation.md)]
+ [31.3. Arquivos de comparação de variantes][(regress-variant.md)]
+ [31.4. Testes TAP][(regress-tap.md)]
+ [31.5. Exame da cobertura de testes][(regress-coverage.md)]