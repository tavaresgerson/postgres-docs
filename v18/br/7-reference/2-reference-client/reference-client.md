# Aplicações de cliente do PostgreSQL

---

Esta parte contém informações de referência para aplicações e utilitários do cliente PostgreSQL. Nem todos esses comandos são de utilidade geral; alguns podem exigir privilégios especiais. A característica comum desses aplicativos é que eles podem ser executados em qualquer host, independentemente de onde o servidor de banco de dados reside.

Quando especificados na linha de comando, os nomes de usuário e de banco de dados são preservados em maiúsculas — a presença de espaços ou caracteres especiais pode exigir citação. Os nomes de tabelas e outros identificadores não são preservados em maiúsculas, exceto onde documentado, e podem exigir citação.

**Índice**

* [clusterdb][(app-clusterdb.md) — agrupar um banco de dados PostgreSQL
* [createdb][(app-createdb.md) — criar um novo banco de dados PostgreSQL
* [createuser][(app-createuser.md) — definir uma nova conta de usuário PostgreSQL
* [dropdb][(app-dropdb.md) — remover um banco de dados PostgreSQL
* [dropuser][(app-dropuser.md) — remover uma conta de usuário PostgreSQL
* [ecpg][(app-ecpg.md) — pré-processador de SQL C embutido
* [pg_amcheck][(app-pgamcheck.md) — verificar a corrupção em um ou mais bancos de dados PostgreSQL
* [pg_basebackup][(app-pgbasebackup.md) — fazer um backup de base de um grupo de PostgreSQL
* [pgbench][(pgbench.md) — executar um teste de benchmark no PostgreSQL
* [pg_combinebackup][(app-pgcombinebackup.md) — reconstruir um backup completo a partir de um backup incremental e backups dependentes
* [pg_config][(app-pgconfig.md) — obter informações sobre a versão instalada do PostgreSQL
* [pg_dump][(app-pgdump.md) — exportar um banco de dados PostgreSQL como um script SQL ou para outros formatos
* [pg_dumpall][(app-pg-dumpall.md) — extrair um grupo de bancos de dados PostgreSQL em um arquivo de script
* [pg_isready][(app-pg-isready.md) — verificar o status de conexão de um servidor PostgreSQL
* [pg_receivewal][(app-pgreceivewal.md) — transmitir logs de antecipação de escrita de um servidor PostgreSQL
* [pg_recvlogical][(app-pgrecvlogical.md) — controlar fluxos de decodificação lógica do PostgreSQL
* [pg_restore][(app-pgrestore.md) — restaurar um banco de dados PostgreSQL a partir de um arquivo de arquivo criado por pg_dump
* [pg_verifybackup][(app-pgverifybackup.md) — verificar a integridade de um backup de base de um grupo de PostgreSQL
* [psql][(app-psql.md) — terminal interativo PostgreSQL
* [reindexdb][(app-reindexdb.md) — reindexar um banco de dados PostgreSQL
* [vacuumdb][(app-vacuumdb.md) — coletar lixo e analisar um banco de dados PostgreSQL