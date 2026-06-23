## 38.1. Visão geral do comportamento do gatilho de evento [#](#EVENT-TRIGGER-DEFINITION)

* [38.1.1. login](event-trigger-definition.md#EVENT-TRIGGER-LOGIN)
* [38.1.2. ddl_command_start](event-trigger-definition.md#EVENT-TRIGGER-DDL_COMMAND_START)
* [38.1.3. ddl_command_end](event-trigger-definition.md#EVENT-TRIGGER-DDL_COMMAND_END)
* [38.1.4. sql_drop](event-trigger-definition.md#EVENT-TRIGGER-SQL_DROP)
* [38.1.5. table_rewrite](event-trigger-definition.md#EVENT-TRIGGER-TABLE_REWRITE)
* [38.1.6. Triggers de Evento em Transações Abortadas](event-trigger-definition.md#EVENT-TRIGGER-ABORTED-TRANSACTIONS)
* [38.1.7. Criando Triggers de Evento](event-trigger-definition.md#EVENT-TRIGGER-CREATING)

Um gatilho de evento é acionado sempre que o evento com o qual está associado ocorre no banco de dados no qual é definido. Atualmente, os eventos suportados são `login`, `ddl_command_start`, `ddl_command_end`, `table_rewrite` e `sql_drop`. O suporte para eventos adicionais pode ser adicionado em versões futuras.

### 38.1.1. login [#](#EVENT-TRIGGER-LOGIN)

O evento `login` ocorre quando um usuário autenticado faz login no sistema. Qualquer erro em um procedimento de disparo para este evento pode impedir o login bem-sucedido no sistema. Tais erros podem ser contornados definindo [event_triggers](runtime-config-client.md#GUC-EVENT-TRIGGERS) para `false` em uma string de conexão ou arquivo de configuração. Alternativamente, você pode reiniciar o sistema no modo de usuário único (já que os gatilhos de eventos são desativados nesse modo). Consulte a página de referência [postgres](app-postgres.md) para obter detalhes sobre o uso do modo de usuário único. O evento `login` também será acionado em servidores de espera. Para evitar que os servidores se tornem inacessíveis, tais gatilhos devem evitar escrever qualquer coisa no banco de dados ao executar em um standby. Além disso, é recomendável evitar consultas de longa duração nos gatilhos de eventos `login`. Observe, por exemplo, que cancelar uma conexão no psql não cancelará o gatilho `login` em andamento.

Para um exemplo de como usar o gatilho de evento `login`, consulte [Seção 38.5](event-trigger-database-login-example.md).

### 38.1.2. ddl_command_start [#](#EVENT-TRIGGER-DDL_COMMAND_START)

O evento `ddl_command_start` ocorre logo antes da execução de um comando DDL. Os comandos DDL neste contexto são:

* `CREATE`
* `ALTER`
* `DROP`
* `COMMENT`
* `GRANT`
* `IMPORT FOREIGN SCHEMA`
* `REINDEX`
* `REFRESH MATERIALIZED VIEW`
* `REVOKE`
* `SECURITY LABEL`

`ddl_command_start` também ocorre logo antes da execução de um comando `SELECT INTO`, uma vez que isso é equivalente a `CREATE TABLE AS`.

Como exceção, este evento não ocorre para comandos DDL direcionados a objetos compartilhados:

* bancos de dados
* papéis (definições de papéis e associações de papéis)
* espaços de tabela
* privilégios de parâmetros
* `ALTER SYSTEM`

Esse evento também não ocorre para comandos que visam os próprios gatilhos de evento.

Não é verificado se o objeto afetado existe ou não antes de o gatilho do evento ser acionado.

### 38.1.3. ddl_command_end [#](#EVENT-TRIGGER-DDL_COMMAND_END)

O evento `ddl_command_end` ocorre logo após a execução do mesmo conjunto de comandos que o `ddl_command_start`. Para obter mais detalhes sobre as operações de DDL que ocorreram, use a função de retorno de conjunto `pg_event_trigger_ddl_commands()` do código de gatilho do evento `ddl_command_end` (consulte [Seção 9.30] (functions-event-triggers.md "9.30. Event Trigger Functions")). Observe que o gatilho é acionado após as ações terem sido realizadas (mas antes da transação ser confirmada), e, portanto, os catálogos do sistema podem ser lidos como já alterados.

### 38.1.4. sql_drop [#](#EVENT-TRIGGER-SQL_DROP)

O evento `sql_drop` ocorre logo antes do gatilho de evento `ddl_command_end` para qualquer operação que elimine objetos do banco de dados. Observe que, além dos comandos óbvios `DROP`, alguns comandos `ALTER` também podem desencadear um evento `sql_drop`.

Para listar os objetos que foram descartados, use a função de retorno de conjunto `pg_event_trigger_dropped_objects()` do código de gatilho de evento `sql_drop` (consulte [Seção 9.30](functions-event-triggers.md)). Observe que o gatilho é executado após os objetos terem sido excluídos dos catálogos do sistema, portanto, não é possível consultá-los mais.

### 38.1.5. tabela_rewrite [#](#EVENT-TRIGGER-TABLE_REWRITE)

O evento `table_rewrite` ocorre logo antes de uma tabela ser reescrita por algumas ações dos comandos `ALTER TABLE` e `ALTER TYPE`. Embora outras instruções de controle estejam disponíveis para reescrever uma tabela, como `CLUSTER` e `VACUUM`, o evento `table_rewrite` não é acionado por eles. Para encontrar o OID da tabela que foi reescrita, use a função `pg_event_trigger_table_rewrite_oid()`, para descobrir as razões da reescrita, use a função `pg_event_trigger_table_rewrite_reason()` (ver [Seção 9.30](functions-event-triggers.md)).

### 38.1.6. Gatilhos de evento em transações canceladas [#](#EVENT-TRIGGER-ABORTED-TRANSACTIONS)

Os gatilhos de evento (como outras funções) não podem ser executados em uma transação abortada. Assim, se um comando DDL falhar com um erro, quaisquer gatilhos `ddl_command_end` associados não serão executados. Por outro lado, se um gatilho `ddl_command_start` falhar com um erro, nenhum outro gatilho de evento será acionado e não haverá tentativa de executar o próprio comando. Da mesma forma, se um gatilho `ddl_command_end` falhar com um erro, os efeitos da declaração DDL serão revertidos, assim como aconteceria em qualquer outro caso em que a transação contida abortado.

### 38.1.7. Criar gatilhos de evento [#](#EVENT-TRIGGER-CREATING)

Os gatilhos de evento são criados usando o comando [CREATE EVENT TRIGGER](sql-createeventtrigger.md "CREATE EVENT TRIGGER"). Para criar um gatilho de evento, você deve primeiro criar uma função com o tipo de retorno especial `event_trigger`. Essa função não precisa (e não pode) retornar um valor; o tipo de retorno serve apenas como um sinal de que a função deve ser invocada como um gatilho de evento.

Se mais de um gatilho de evento for definido para um evento específico, eles serão acionados em ordem alfabética pelo nome do gatilho.

Uma definição de gatilho também pode especificar uma condição `WHEN` para que, por exemplo, um gatilho `ddl_command_start` possa ser disparado apenas para comandos específicos que o usuário deseja interceptar. Um uso comum desses gatilhos é restringir a gama de operações DDL que os usuários podem realizar.