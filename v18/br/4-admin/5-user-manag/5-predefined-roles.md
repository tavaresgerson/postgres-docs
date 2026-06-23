## 21.5. Papéis pré-definidos [#](#PREDEFINED-ROLES)

O PostgreSQL oferece um conjunto de papéis predefinidos que fornecem acesso a certas capacidades e informações privilegiadas, comumente necessárias. Os administradores (incluindo papéis que possuem o privilégio `CREATEROLE`) podem `GRANT` esses papéis para usuários e/ou outros papéis em seu ambiente, fornecendo a esses usuários acesso às capacidades e informações especificadas. Por exemplo:

```
GRANT pg_signal_backend TO admin_user;
```

### Aviso

É preciso ter cuidado ao conceder esses papéis, garantindo que eles sejam usados apenas quando necessário e com o entendimento de que esses papéis conferem acesso a informações privilegiadas.

Os papéis predefinidos são descritos abaixo. Observe que as permissões específicas para cada um dos papéis podem mudar no futuro, à medida que funcionalidades adicionais são adicionadas. Os administradores devem monitorar as notas de lançamento para mudanças.

`pg_checkpoint` [#](#PREDEFINED-ROLE-PG-CHECKPOINT): `pg_checkpoint` permite a execução do comando [`CHECKPOINT`](sql-checkpoint.md)].

`pg_create_subscription` [#](#PREDEFINED-ROLE-PG-CREATE-SUBSCRIPTION): `pg_create_subscription` permite que os usuários com permissão `CREATE` no banco de dados emitam [`CREATE SUBSCRIPTION`](sql-createsubscription.md "CREATE SUBSCRIPTION").

`pg_database_owner` [#](#PREDEFINED-ROLE-PG-DATABASE-OWNER): `pg_database_owner` sempre tem exatamente um membro implícito: o proprietário atual do banco de dados. Não pode ser concedido a membros em qualquer papel, e nenhum papel pode ser concedido a membros em `pg_database_owner`. No entanto, como qualquer outro papel, ele pode possuir objetos e receber concessões de privilégios de acesso. Consequentemente, uma vez que `pg_database_owner` tenha direitos dentro de um banco de dados de modelo, cada proprietário de um banco de dados instanciado a partir desse modelo possuirá esses direitos. Inicialmente, esse papel possui o esquema `public`, então cada proprietário de um banco de dados instanciado a partir desse modelo governa o uso local desse esquema.

`pg_maintain` [#](#PREDEFINED-ROLE-PG-MAINTAIN): `pg_maintain` permite executar [`VACUUM`](sql-vacuum.md "VACUUM"), [`ANALYZE`](sql-analyze.md "ANALYZE"), [`CLUSTER`](sql-cluster.md "CLUSTER"), [`REFRESH MATERIALIZED VIEW`](sql-refreshmaterializedview.md "REFRESH MATERIALIZED VIEW"), [`REINDEX`](sql-reindex.md "REINDEX"), e [`LOCK TABLE`](sql-lock.md "LOCK") em todas as relações, como se tivesse direitos `MAINTAIN` sobre esses objetos.

`pg_monitor` `pg_read_all_settings` `pg_read_all_stats` `pg_stat_scan_tables` [#](#PREDEFINED-ROLE-PG-MONITOR): Esses papéis são destinados a permitir que os administradores configurem facilmente um papel para o monitoramento do servidor de banco de dados. Eles concedem um conjunto de privilégios comuns que permitem ao papel ler vários ajustes de configuração úteis, estatísticas e outras informações do sistema normalmente restritas a superusuários.

`pg_monitor` permite a leitura/execução de várias visualizações e funções de monitoramento. Este papel é membro de `pg_read_all_settings`, `pg_read_all_stats` e `pg_stat_scan_tables`.

`pg_read_all_settings` permite a leitura de todas as variáveis de configuração, mesmo aquelas que normalmente são visíveis apenas para superusuários.

`pg_read_all_stats` permite a leitura de todas as vistas pg_stat_* e o uso de várias extensões relacionadas a estatísticas, mesmo aquelas que normalmente são visíveis apenas para superusuários.

`pg_stat_scan_tables` permite a execução de funções de monitoramento que podem requerer `ACCESS SHARE` de bloqueio em tabelas, potencialmente por um longo período (por exemplo, `pgrowlocks(text)` na extensão [pgrowlocks](pgrowlocks.md "F.31. pgrowlocks — show a table's row locking information")).

`pg_read_all_data` `pg_write_all_data` [#](#PREDEFINED-ROLE-PG-READ-ALL-DATA): `pg_read_all_data` permite a leitura de todos os dados (tabelas, visualizações, sequências), como se tivesse direitos `SELECT` sobre esses objetos e direitos `USAGE` em todos os esquemas. Este papel não contorna as políticas de segurança em nível de linha (RLS). Se a RLS estiver sendo usada, um administrador pode querer definir `BYPASSRLS` em papéis a que este papel é concedido.

`pg_write_all_data` permite escrever todos os dados (tabelas, visualizações, sequências), como se tivesse os direitos de `INSERT`, `UPDATE` e `DELETE` sobre esses objetos e os direitos de `USAGE` em todos os esquemas. Este papel não contorna as políticas de segurança em nível de linha (RLS). Se a RLS estiver sendo usada, um administrador pode querer definir `BYPASSRLS` em papéis para os quais este papel é concedido.

`pg_read_server_files` `pg_write_server_files` `pg_execute_server_program` [#](#PREDEFINED-ROLE-PG-READ-SERVER-FILES): Esses papéis são destinados a permitir que os administradores tenham papéis confiáveis, mas não de superusuário, que possam acessar arquivos e executar programas no servidor de banco de dados como o usuário que o banco de dados executa. Eles ignoram todas as verificações de permissão de nível de banco de dados ao acessar arquivos diretamente e poderiam ser usados para obter acesso de nível de superusuário. Portanto, grande cuidado deve ser tomado ao conceder esses papéis aos usuários.

`pg_read_server_files` permite a leitura de arquivos de qualquer local que o banco de dados possa acessar no servidor usando `COPY` e outras funções de acesso a arquivos.

`pg_write_server_files` permite a escrita em arquivos em qualquer local que o banco de dados possa acessar no servidor usando `COPY` e outras funções de acesso a arquivos.

`pg_execute_server_program` permite executar programas no servidor de banco de dados como o usuário que o banco de dados executa usando `COPY` e outras funções que permitem executar um programa do lado do servidor.

`pg_signal_autovacuum_worker` [#](#PREDEFINED-ROLE-PG-SIGNAL-AUTOVACUUM-WORKER): `pg_signal_autovacuum_worker` permite que os trabalhadores do autovacuum cancele o vácuo da tabela atual ou termine sua sessão. Veja [Seção 9.28.2](functions-admin.md#FUNCTIONS-ADMIN-SIGNAL "9.28.2. Server Signaling Functions").

`pg_signal_backend` [#](#PREDEFINED-ROLE-PG-SIGNAL-BACKEND): `pg_signal_backend` permite sinalizar a outro backend para cancelar uma consulta ou encerrar sua sessão. Observe que este papel não permite sinalizar backends de propriedade de um superusuário. Veja [Seção 9.28.2](functions-admin.md#FUNCTIONS-ADMIN-SIGNAL "9.28.2. Server Signaling Functions").

`pg_use_reserved_connections` [#](#PREDEFINED-ROLE-PG-USE-RESERVED-CONNECTIONS): `pg_use_reserved_connections` permite o uso de faixas de conexão reservadas por meio de [reservadas_conexões](runtime-config-connection.md#GUC-RESERVED-CONNECTIONS).