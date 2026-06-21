## Capítulo 25. Backup e Restauração

**Índice**

* [25.1. Dump de SQL](backup-dump.md)

+ [25.1.1. Restauração do Dump](backup-dump.md#BACKUP-DUMP-RESTORE)
+ [25.1.2. Uso de pg_dumpall](backup-dump.md#BACKUP-DUMP-ALL)
+ [25.1.3. Tratamento de bancos de dados grandes](backup-dump.md#BACKUP-DUMP-LARGE)

* [25.2. Backup em nível de sistema de arquivos](backup-file.md)
* [25.3. Arquivamento contínuo e recuperação em ponto no tempo (PITR)](continuous-archiving.md)

+ [25.3.1. Configuração do arquivamento WAL](continuous-archiving.md#BACKUP-ARCHIVING-WAL)
+ [25.3.2. Fazer um backup de base](continuous-archiving.md#BACKUP-BASE-BACKUP)
+ [25.3.3. Fazer um backup incremental](continuous-archiving.md#BACKUP-INCREMENTAL-BACKUP)
+ [25.3.4. Fazer um backup de base usando a API de baixo nível](continuous-archiving.md#BACKUP-LOWLEVEL-BASE-BACKUP)
+ [25.3.5. Recuperação usando um backup de arquivo contínuo](continuous-archiving.md#BACKUP-PITR-RECOVERY)
+ [25.3.6. Linhas do tempo](continuous-archiving.md#BACKUP-TIMELINES)
+ [25.3.7. Dicas e exemplos](continuous-archiving.md#BACKUP-TIPS)
+ [25.3.8. Considerações](continuous-archiving.md#CONTINUOUS-ARCHIVING-CAVEATS)

Assim como qualquer coisa que contenha dados valiosos, os bancos de dados PostgreSQL devem ser feitos backups regularmente. Embora o procedimento seja essencialmente simples, é importante ter um entendimento claro das técnicas e suposições subjacentes.

Existem três abordagens fundamentalmente diferentes para fazer backup dos dados do PostgreSQL:

* Dump SQL
* Backup em nível de sistema de arquivos
* Arquivamento contínuo

Cada um tem suas próprias forças e fraquezas; cada um é discutido em ordem nas seções a seguir.