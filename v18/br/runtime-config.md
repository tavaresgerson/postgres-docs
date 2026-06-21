## Capítulo 19. Configuração do servidor

**Índice**

* [19.1. Configuração de Parâmetros](config-setting.md)

+ [19.1.1. Nomes e Valores dos Parâmetros](config-setting.md#CONFIG-SETTING-NAMES-VALUES)
+ [19.1.2. Interação do Parâmetro via Arquivo de Configuração](config-setting.md#CONFIG-SETTING-CONFIGURATION-FILE)
+ [19.1.3. Interação do Parâmetro via SQL](config-setting.md#CONFIG-SETTING-SQL)
+ [19.1.4. Interação do Parâmetro via Shell](config-setting.md#CONFIG-SETTING-SHELL)
+ [19.1.5. Gerenciamento do Conteúdo do Arquivo de Configuração](config-setting.md#CONFIG-INCLUDES)

* [19.2. Localização dos arquivos](runtime-config-file-locations.md)
* [19.3. Conexões e autenticação](runtime-config-connection.md)

+ [19.3.1. Configurações de Conexão](runtime-config-connection.md#RUNTIME-CONFIG-CONNECTION-SETTINGS)
+ [19.3.2. Configurações TCP](runtime-config-connection.md#RUNTIME-CONFIG-TCP-SETTINGS)
+ [19.3.3. Autenticação](runtime-config-connection.md#RUNTIME-CONFIG-CONNECTION-AUTHENTICATION)
+ [19.3.4. SSL](runtime-config-connection.md#RUNTIME-CONFIG-CONNECTION-SSL)

* [19.4. Consumo de recursos](runtime-config-resource.md)

+ [19.4.1. Memória](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-MEMORY)
+ [19.4.2. Disco](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-DISK)
+ [19.4.3. Uso de Recursos do Kernel](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-KERNEL)
+ [19.4.4. Escritor de Plano de Fundo](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-BACKGROUND-WRITER)
+ [19.4.5. E/S](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-IO)
+ [19.4.6. Processos de Trabalhador](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-WORKER-PROCESSES)

* [19.5. Registro de escrita antecipada](runtime-config-wal.md)

+ [19.5.1. Configurações](runtime-config-wal.md#RUNTIME-CONFIG-WAL-SETTINGS)
+ [19.5.2. Pontos de verificação](runtime-config-wal.md#RUNTIME-CONFIG-WAL-CHECKPOINTS)
+ [19.5.3. Arquivamento](runtime-config-wal.md#RUNTIME-CONFIG-WAL-ARCHIVING)
+ [19.5.4. Recuperação](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY)
+ [19.5.5. Recuperação de arquivo](runtime-config-wal.md#RUNTIME-CONFIG-WAL-ARCHIVE-RECOVERY)
+ [19.5.6. Alvo de recuperação](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY-TARGET)
+ [19.5.7. Resumo WAL](runtime-config-wal.md#RUNTIME-CONFIG-WAL-SUMMARIZATION)

* [19.6. Replicação](runtime-config-replication.md)

+ [19.6.1. Servidores de envio](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-SENDER)
+ [19.6.2. Servidor principal](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-PRIMARY)
+ [19.6.3. Servidores de reserva](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-STANDBY)
+ [19.6.4. Subscritores](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-SUBSCRIBER)

* [19.7. Planejamento de consulta](runtime-config-query.md)

+ [19.7.1. Configuração do Método de Planejamento](runtime-config-query.md#RUNTIME-CONFIG-QUERY-ENABLE)
+ [19.7.2. Constantes de Custo do Planejador](runtime-config-query.md#RUNTIME-CONFIG-QUERY-CONSTANTS)
+ [19.7.3. Otimizador de Consulta Genética](runtime-config-query.md#RUNTIME-CONFIG-QUERY-GEQO)
+ [19.7.4. Outras Opções do Planejador](runtime-config-query.md#RUNTIME-CONFIG-QUERY-OTHER)

* [19.8. Relatório de Erros e Registro][(runtime-config-logging.md)]

+ [19.8.1. Onde registrar](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-WHERE)
+ [19.8.2. Quando registrar](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-WHEN)
+ [19.8.3. O que registrar](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-WHAT)
+ [19.8.4. Usando saída de registro no formato CSV](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-CSVLOG)
+ [19.8.5. Usando saída de registro no formato JSON](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-JSONLOG)
+ [19.8.6. Título do processo](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-PROC-TITLE)

* [19.9. Estatísticas de execução](runtime-config-statistics.md)

+ [19.9.1. Estatísticas de consulta cumulativa e índice](runtime-config-statistics.md#RUNTIME-CONFIG-CUMULATIVE-STATISTICS)
+ [19.9.2. Monitoramento de estatísticas](runtime-config-statistics.md#RUNTIME-CONFIG-STATISTICS-MONITOR)

* [19.10. Aspiração](runtime-config-vacuum.md)

+ [19.10.1. Aspiração Automática](runtime-config-vacuum.md#RUNTIME-CONFIG-AUTOVACUUM)
+ [19.10.2. Atraso de Aspiração Baseado em Custo](runtime-config-vacuum.md#RUNTIME-CONFIG-RESOURCE-VACUUM-COST)
+ [19.10.3. Comportamento Padrão](runtime-config-vacuum.md#RUNTIME-CONFIG-VACUUM-DEFAULT)
+ [19.10.4. Congelamento](runtime-config-vacuum.md#RUNTIME-CONFIG-VACUUM-FREEZING)

* [19.11. Configurações padrão de conexão do cliente](runtime-config-client.md)

+ [19.11.1. Comportamento de declaração](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-STATEMENT)
+ [19.11.2. Local e formatação](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-FORMAT)
+ [19.11.3. Pré-carga de biblioteca compartilhada](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-PRELOAD)
+ [19.11.4. Outros padrões](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-OTHER)

* [19.12. Gerenciamento de bloqueio](runtime-config-locks.md)
* [19.13. Compatibilidade de versão e plataforma](runtime-config-compatible.md)

+ [19.13.1. Versões anteriores do PostgreSQL](runtime-config-compatible.md#RUNTIME-CONFIG-COMPATIBLE-VERSION)
+ [19.13.2. Compatibilidade da plataforma e do cliente](runtime-config-compatible.md#RUNTIME-CONFIG-COMPATIBLE-CLIENTS)

* [19.14. Gerenciamento de Erros](runtime-config-error-handling.md)
* [19.15. Opções Predefinidas](runtime-config-preset.md)
* [19.16. Opções Personalizadas](runtime-config-custom.md)
* [19.17. Opções para Desenvolvedores](runtime-config-developer.md)
* [19.18. Opções Breves](runtime-config-short.md)

Existem muitos parâmetros de configuração que afetam o comportamento do sistema de banco de dados. Na primeira seção deste capítulo, descrevemos como interagir com os parâmetros de configuração. As seções subsequentes discutem cada parâmetro em detalhe.