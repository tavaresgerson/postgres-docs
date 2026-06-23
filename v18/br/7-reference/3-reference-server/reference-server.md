# Aplicações do servidor PostgreSQL

---

Esta parte contém informações de referência para aplicações de servidor PostgreSQL e utilitários de suporte. Esses comandos só podem ser executados de forma útil no host onde o servidor de banco de dados reside. Outros programas de utilitário estão listados em [Aplicações de cliente PostgreSQL](reference-client.md).

**Índice**

* [initdb](app-initdb.md) — criar um novo clúster de banco de dados PostgreSQL
* [pg_archivecleanup](pgarchivecleanup.md) — limpar arquivos de arquivo WAL de PostgreSQL
* [pg_checksums](app-pgchecksums.md) — habilitar, desabilitar ou verificar verificações de dados em um clúster de banco de dados PostgreSQL
* [pg_controldata](app-pgcontroldata.md) — exibir informações de controle de um clúster de banco de dados PostgreSQL
* [pg_createsubscriber](app-pgcreatesubscriber.md) — converter uma replica física em uma nova replica lógica
* [pg_ctl](app-pg-ctl.md) — inicializar, iniciar, parar ou controlar um servidor PostgreSQL
* [pg_resetwal](app-pgresetwal.md) — redefinir o log de antecipação e outras informações de controle de um clúster de banco de dados PostgreSQL
* [pg_rewind](app-pgrewind.md) — sincronizar um diretório de dados PostgreSQL com outro diretório de dados que foi criado a partir dele
* [pg_test_fsync](pgtestfsync.md) — determinar o `wal_sync_method` mais rápido para PostgreSQL
* [pg_test_timing](pgtesttiming.md) — medir o tempo de sobrecarga
* [pg_upgrade](pgupgrade.md) — atualizar uma instância do servidor PostgreSQL
* [pg_waldump](pgwaldump.md) — exibir uma representação legível para humanos do log de antecipação de um clúster de banco de dados PostgreSQL
* [pg_walsummary](app-pgwalsummary.md) — imprimir o conteúdo dos arquivos de resumo WAL
* [postgres](app-postgres.md) — servidor de banco de dados PostgreSQL