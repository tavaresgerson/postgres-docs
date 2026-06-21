## 47.8. Suporte à Replicação Síncrona para Decodificação Lógica [#](#LOGICALDECODING-SYNCHRONOUS)

* [47.8.1. Visão geral](logicaldecoding-synchronous.md#LOGICALDECODING-SYNCHRONOUS-OVERVIEW)
* [47.8.2. Observações](logicaldecoding-synchronous.md#LOGICALDECODING-SYNCHRONOUS-CAVEATS)

### 47.8.1. Visão geral [#](#LOGICALDECODING-SYNCHRONOUS-OVERVIEW)

A decodificação lógica pode ser usada para construir soluções de [[replicação síncrona]] com a mesma interface de usuário da replicação síncrona para [[replicação em fluxo]] (warm-standby.md#SYNCHRONOUS-REPLICATION "26.2.8. Synchronous Replication"). Para isso, a interface de replicação em fluxo (consulte [Seção 47.3] (logicaldecoding-walsender.md "47.3. Streaming Replication Protocol Interface")) deve ser usada para transmitir dados. Os clientes devem enviar mensagens `Standby status update (F)` (consulte [Seção 54.4] (protocol-replication.md "54.4. Streaming Replication Protocol")) assim como os clientes de replicação em fluxo.

### Nota

Uma replica síncrona que recebe alterações por meio de decodificação lógica funcionará no escopo de um único banco de dados. Como, em contraste, *`synchronous_standby_names`* atualmente é utilizado em todo o servidor, isso significa que essa técnica não funcionará corretamente se mais de um banco de dados estiver sendo utilizado ativamente.

### 47.8.2. Avisos [#](#LOGICALDECODING-SYNCHRONOUS-CAVEATS)

Em uma configuração de replicação síncrona, um bloqueio pode ocorrer se a transação tiver bloqueado as tabelas do catálogo do [usuário] exclusivamente. Consulte [Seção 47.6.2][(logicaldecoding-output-plugin.md#LOGICALDECODING-CAPABILITIES "47.6.2. Capabilities")] para obter informações sobre as tabelas do catálogo do usuário. Isso ocorre porque a decodificação lógica das transações pode bloquear as tabelas do catálogo para acessá-las. Para evitar isso, os usuários devem abster-se de tomar um bloqueio exclusivo nas tabelas do catálogo do [usuário]. Isso pode ocorrer das seguintes maneiras:

* Emitir um `LOCK` explícito sobre `pg_class` em uma transação.
* Realizar `CLUSTER` sobre `pg_class` em uma transação.
* `PREPARE TRANSACTION` após o comando `LOCK` em `pg_class` e permitir a decodificação lógica de transações de dois estágios.
* `PREPARE TRANSACTION` após o comando `CLUSTER` em `pg_trigger` e permitir a decodificação lógica de transações de dois estágios. Isso levará a um impasse apenas quando a tabela publicada tiver um gatilho.
* Executar `TRUNCATE` na tabela de catálogo [user] em uma transação.

Observe que esses comandos podem causar deadlocks não apenas para as tabelas do catálogo listadas acima, mas também para outras tabelas de catálogo.