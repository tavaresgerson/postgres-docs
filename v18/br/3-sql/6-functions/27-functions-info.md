### 9.27. Funções e Operadores de Informação do Sistema [#](#FUNCTIONS-INFO)

* [9.27.1. Funções de Informações de Sessão](functions-info.md#FUNCTIONS-INFO-SESSION)
* [9.27.2. Funções de Consultas de Privilegios de Acesso](functions-info.md#FUNCTIONS-INFO-ACCESS)
* [9.27.3. Funções de Consultas de Visibilidade do Esquema](functions-info.md#FUNCTIONS-INFO-SCHEMA)
* [9.27.4. Funções de Informações do Catálogo do Sistema](functions-info.md#FUNCTIONS-INFO-CATALOG)
* [9.27.5. Funções de Informações e Endereçamento de Objetos](functions-info.md#FUNCTIONS-INFO-OBJECT)
* [9.27.6. Funções de Informações de Comentários](functions-info.md#FUNCTIONS-INFO-COMMENT)
* [9.27.7. Funções de Verificação da Validade dos Dados](functions-info.md#FUNCTIONS-INFO-VALIDITY)
* [9.27.8. Funções de ID de Transação e Informações de Escaneamento](functions-info.md#FUNCTIONS-INFO-SNAPSHOT)
* [9.27.9. Funções de Informações de Transação Comprovada](functions-info.md#FUNCTIONS-INFO-COMMIT-TIMESTAMP)
* [9.27.10. Funções de Dados de Controle](functions-info.md#FUNCTIONS-INFO-CONTROLDATA)
* [9.27.11. Funções de Informações de Versão](functions-info.md#FUNCTIONS-INFO-VERSION)
* [9.27.12. Funções de Informações de Resumo do WAL](functions-info.md#FUNCTIONS-INFO-WAL-SUMMARY)

As funções descritas nesta seção são usadas para obter várias informações sobre uma instalação do PostgreSQL.

#### 9.27.1. Funções de Informações de Sessão [#](#FUNCTIONS-INFO-SESSION)

[Tabela 9.71](functions-info.md#FUNCTIONS-INFO-SESSION-TABLE) mostra várias funções que extraem informações de sessão e sistema.

Além das funções listadas nesta seção, há várias funções relacionadas ao sistema de estatísticas que também fornecem informações sobre o sistema. Consulte [Seção 27.2.26](monitoring-stats.md#MONITORING-STATS-FUNCTIONS) para obter mais informações.

**Tabela 9.71. Funções de Informações de Sessão**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      current_catalog
     </code>
     →
     <code>
      name
     </code>
    </p>
    <p class="func_signature">
     <code>
      current_database
     </code>
     () →
     <code>
      name
     </code>
    </p>
    <p>
     Returns the name of the current database.  (Databases are called
     <span class="quote">
      “
      <span class="quote">
       catalogs
      </span>
      ”
     </span>
     in the SQL standard, so
     <code>
      current_catalog
     </code>
     is the standard's spelling.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      current_query
     </code>
     () →
     <code>
      text
     </code>
    </p>
    <p>
     Returns the text of the currently executing query, as submitted by the client (which might contain more than one statement).
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      current_role
     </code>
     →
     <code>
      name
     </code>
    </p>
    <p>
     This is equivalent to
     <code>
      current_user
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      current_schema
     </code>
     →
     <code>
      name
     </code>
    </p>
    <p class="func_signature">
     <code>
      current_schema
     </code>
     () →
     <code>
      name
     </code>
    </p>
    <p>
     Returns the name of the schema that is first in the search path (or a null value if the search path is empty).  This is the schema that will be used for any tables or other named objects that are created without specifying a target schema.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      current_schemas
     </code>
     (
     <em class="parameter">
      <code>
       include_implicit
      </code>
     </em>
     <code>
      boolean
     </code>
     ) →
     <code>
      name[]
     </code>
    </p>
    <p>
     Returns an array of the names of all schemas presently in the effective search path, in their priority order.  (Items in the current
     <a class="xref" href="runtime-config-client.md#GUC-SEARCH-PATH">
      search_path
     </a>
     setting that do not correspond to existing, searchable schemas are omitted.)  If the Boolean argument is
     <code>
      true
     </code>
     , then implicitly-searched system schemas such as
     <code>
      pg_catalog
     </code>
     are included in the result.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      current_user
     </code>
     →
     <code>
      name
     </code>
    </p>
    <p>
     Returns the user name of the current execution context.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      inet_client_addr
     </code>
     () →
     <code>
      inet
     </code>
    </p>
    <p>
     Returns the IP address of the current client, or
     <code>
      NULL
     </code>
     if the current connection is via a Unix-domain socket.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      inet_client_port
     </code>
     () →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns the IP port number of the current client, or
     <code>
      NULL
     </code>
     if the current connection is via a Unix-domain socket.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      inet_server_addr
     </code>
     () →
     <code>
      inet
     </code>
    </p>
    <p>
     Returns the IP address on which the server accepted the current connection, or
     <code>
      NULL
     </code>
     if the current connection is via a Unix-domain socket.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      inet_server_port
     </code>
     () →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns the IP port number on which the server accepted the current connection, or
     <code>
      NULL
     </code>
     if the current connection is via a Unix-domain socket.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_backend_pid
     </code>
     () →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns the process ID of the server process attached to the current session.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_blocking_pids
     </code>
     (
     <code>
      integer
     </code>
     ) →
     <code>
      integer[]
     </code>
    </p>
    <p>
     Returns an array of the process ID(s) of the sessions that are blocking the server process with the specified process ID from acquiring a lock, or an empty array if there is no such server process or it is not blocked.
    </p>
    <p>
     One server process blocks another if it either holds a lock that conflicts with the blocked process's lock request (hard block), or is waiting for a lock that would conflict with the blocked process's lock request and is ahead of it in the wait queue (soft block).  When using parallel queries the result always lists client-visible process IDs (that is,
     <code>
      pg_backend_pid
     </code>
     results) even if the actual lock is held or awaited by a child worker process.  As a result of that, there may be duplicated PIDs in the result.  Also note that when a prepared transaction holds a conflicting lock, it will be represented by a zero process ID.
    </p>
    <p>
     Frequent calls to this function could have some impact on database performance, because it needs exclusive access to the lock manager's shared state for a short time.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_conf_load_time
     </code>
     () →
     <code>
      timestamp with time zone
     </code>
    </p>
    <p>
     Returns the time when the server configuration files were last loaded. If the current session was alive at the time, this will be the time when the session itself re-read the configuration files (so the reading will vary a little in different sessions).  Otherwise it is the time when the postmaster process re-read the configuration files.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_current_logfile
     </code>
     ( [
     <span class="optional">
      <code>
       text
      </code>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Returns the path name of the log file currently in use by the logging collector.  The path includes the
     <a class="xref" href="runtime-config-logging.md#GUC-LOG-DIRECTORY">
      log_directory
     </a>
     directory and the individual log file name.  The result is
     <code>
      NULL
     </code>
     if the logging collector is disabled. When multiple log files exist, each in a different format,
     <code>
      pg_current_logfile
     </code>
     without an argument returns the path of the file having the first format found in the ordered list:
     <code>
      stderr
     </code>
     ,
     <code>
      csvlog
     </code>
     ,
     <code>
      jsonlog
     </code>
     .
     <code>
      NULL
     </code>
     is returned if no log file has any of these formats. To request information about a specific log file format, supply either
     <code>
      csvlog
     </code>
     ,
     <code>
      jsonlog
     </code>
     or
     <code>
      stderr
     </code>
     as the value of the optional parameter. The result is
     <code>
      NULL
     </code>
     if the log format requested is not configured in
     <a class="xref" href="runtime-config-logging.md#GUC-LOG-DESTINATION">
      log_destination
     </a>
     . The result reflects the contents of the
     <code>
      current_logfiles
     </code>
     file.
    </p>
    <p>
     This function is restricted to superusers and roles with privileges of the
     <code>
      pg_monitor
     </code>
     role by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_loaded_modules
     </code>
     () →
     <code>
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       module_name
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       version
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       file_name
      </code>
     </em>
     <code>
      text
     </code>
     )
    </p>
    <p>
     Returns a list of the loadable modules that are loaded into the current server session.  The
     <em class="parameter">
      <code>
       module_name
      </code>
     </em>
     and
     <em class="parameter">
      <code>
       version
      </code>
     </em>
     fields are NULL unless the module author supplied values for them using the
     <code>
      PG_MODULE_MAGIC_EXT
     </code>
     macro. The
     <em class="parameter">
      <code>
       file_name
      </code>
     </em>
     field gives the file name of the module (shared library).
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_my_temp_schema
     </code>
     () →
     <code>
      oid
     </code>
    </p>
    <p>
     Returns the OID of the current session's temporary schema, or zero if it has none (because it has not created any temporary tables).
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_is_other_temp_schema
     </code>
     (
     <code>
      oid
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Returns true if the given OID is the OID of another session's temporary schema.  (This can be useful, for example, to exclude other sessions' temporary tables from a catalog display.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_jit_available
     </code>
     () →
     <code>
      boolean
     </code>
    </p>
    <p>
     Returns true if a
     <acronym class="acronym">
      JIT
     </acronym>
     compiler extension is available (see
     <a class="xref" href="jit.md" title="Chapter 30. Just-in-Time Compilation (JIT)">
      Chapter 30
     </a>
     ) and the
     <a class="xref" href="runtime-config-query.md#GUC-JIT">
      jit
     </a>
     configuration parameter is set to
     <code>
      on
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_numa_available
     </code>
     () →
     <code>
      boolean
     </code>
    </p>
    <p>
     Returns true if the server has been compiled with
     <acronym class="acronym">
      NUMA
     </acronym>
     support.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_listening_channels
     </code>
     () →
     <code>
      setof text
     </code>
    </p>
    <p>
     Returns the set of names of asynchronous notification channels that the current session is listening to.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_notification_queue_usage
     </code>
     () →
     <code>
      double precision
     </code>
    </p>
    <p>
     Returns the fraction (0–1) of the asynchronous notification queue's maximum size that is currently occupied by notifications that are waiting to be processed. See
     <a class="xref" href="sql-listen.md" title="LISTEN">
      <span class="refentrytitle">
       LISTEN
      </span>
     </a>
     and
     <a class="xref" href="sql-notify.md" title="NOTIFY">
      <span class="refentrytitle">
       NOTIFY
      </span>
     </a>
     for more information.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_postmaster_start_time
     </code>
     () →
     <code>
      timestamp with time zone
     </code>
    </p>
    <p>
     Returns the time when the server started.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_safe_snapshot_blocking_pids
     </code>
     (
     <code>
      integer
     </code>
     ) →
     <code>
      integer[]
     </code>
    </p>
    <p>
     Returns an array of the process ID(s) of the sessions that are blocking the server process with the specified process ID from acquiring a safe snapshot, or an empty array if there is no such server process or it is not blocked.
    </p>
    <p>
     A session running a
     <code>
      SERIALIZABLE
     </code>
     transaction blocks a
     <code>
      SERIALIZABLE READ ONLY DEFERRABLE
     </code>
     transaction from acquiring a snapshot until the latter determines that it is safe to avoid taking any predicate locks.  See
     <a class="xref" href="transaction-iso.md#XACT-SERIALIZABLE" title="13.2.3. Serializable Isolation Level">
      Section 13.2.3
     </a>
     for more information about serializable and deferrable transactions.
    </p>
    <p>
     Frequent calls to this function could have some impact on database performance, because it needs access to the predicate lock manager's shared state for a short time.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_trigger_depth
     </code>
     () →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns the current nesting level of
     <span class="productname">
      PostgreSQL
     </span>
     triggers (0 if not called, directly or indirectly, from inside a trigger).
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      session_user
     </code>
     →
     <code>
      name
     </code>
    </p>
    <p>
     Returns the session user's name.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      system_user
     </code>
     →
     <code>
      text
     </code>
    </p>
    <p>
     Returns the authentication method and the identity (if any) that the user presented during the authentication cycle before they were assigned a database role. It is represented as
     <code>
      auth_method:identity
     </code>
     or
     <code>
      NULL
     </code>
     if the user has not been authenticated (for example if
     <a class="link" href="auth-trust.md" title="20.4. Trust Authentication">
      Trust authentication
     </a>
     has been used).
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      user
     </code>
     →
     <code>
      name
     </code>
    </p>
    <p>
     This is equivalent to
     <code>
      current_user
     </code>
     .
    </p>
   </td>
  </tr>
 </tbody>
</table>

Nota

`current_catalog`, `current_role`, `current_schema`, `current_user`, `session_user` e `user` têm um status sintático especial no SQL: eles devem ser chamados sem parênteses finais. No PostgreSQL, os parênteses podem ser usados opcionalmente com `current_schema`, mas não com os outros.

O `session_user` é normalmente o usuário que iniciou a conexão atual com o banco de dados; mas os superusuários podem alterar essa configuração com [SET SESSION AUTHORIZATION](sql-set-session-authorization.md "SET SESSION AUTHORIZATION"). O `current_user` é o identificador do usuário que é aplicável para verificação de permissão. Normalmente, é igual ao usuário da sessão, mas pode ser alterado com [SET ROLE](sql-set-role.md "SET ROLE"). Também muda durante a execução de funções com o atributo `SECURITY DEFINER`. Na linguagem Unix, o usuário da sessão é o “usuário real” e o usuário atual é o “usuário efetivo”. `current_role` e `user` são sinônimos para `current_user`. (O padrão SQL faz uma distinção entre `current_role` e `current_user`, mas o PostgreSQL não, uma vez que unifica usuários e papéis em um único tipo de entidade.)

#### 9.27.2. Funções de Consulta de Privilegios de Acesso [#](#FUNCTIONS-INFO-ACCESS)

[Tabela 9.72](functions-info.md#FUNCTIONS-INFO-ACCESS-TABLE) lista funções que permitem consultar os privilégios de acesso a objetos de forma programática. (Veja [Seção 5.8](ddl-priv.md) para mais informações sobre privilégios.) Nessas funções, o usuário cujos privilégios estão sendo verificados pode ser especificado pelo nome ou pelo OID (`pg_authid`.`oid`), ou se o nome for fornecido como `public`, então os privilégios do pseudorole PUBLIC são verificados. Além disso, o argumento *`user`* pode ser omitido completamente, no caso, o `current_user` é assumido. O objeto que está sendo verificado pode ser especificado pelo nome ou pelo OID, também. Ao especificar pelo nome, um nome de esquema pode ser incluído, se relevante. O privilégio de acesso de interesse é especificado por uma string de texto, que deve avaliar para uma das palavras-chave de privilégio apropriadas para o tipo do objeto (e.g., `SELECT`). Opcionalmente, `WITH GRANT OPTION` pode ser adicionado a um tipo de privilégio para testar se o privilégio é mantido com opção de concessão. Além disso, vários tipos de privilégios podem ser listados separados por vírgulas, no caso, o resultado será verdadeiro se qualquer um dos privilégios listados for mantido. (O caso da string de privilégio não é significativo, e espaço em branco extra é permitido entre, mas não dentro dos nomes de privilégio.) Alguns exemplos:

```sql
SELECT has_table_privilege('myschema.mytable', 'select');
SELECT has_table_privilege('joe', 'mytable', 'INSERT, SELECT WITH GRANT OPTION');
```

**Tabela 9.72. Funções de consulta de privilégios de acesso**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      has_any_column_privilege
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        user
       </code>
      </em>
      <code>
       name
      </code>
      or
      <code>
       oid
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       table
      </code>
     </em>
     <code>
      text
     </code>
     or
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       privilege
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Does user have privilege for any column of table? This succeeds either if the privilege is held for the whole table, or if there is a column-level grant of the privilege for at least one column. Allowable privilege types are
     <code>
      SELECT
     </code>
     ,
     <code>
      INSERT
     </code>
     ,
     <code>
      UPDATE
     </code>
     , and
     <code>
      REFERENCES
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      has_column_privilege
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        user
       </code>
      </em>
      <code>
       name
      </code>
      or
      <code>
       oid
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       table
      </code>
     </em>
     <code>
      text
     </code>
     or
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       column
      </code>
     </em>
     <code>
      text
     </code>
     or
     <code>
      smallint
     </code>
     ,
     <em class="parameter">
      <code>
       privilege
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Does user have privilege for the specified table column? This succeeds either if the privilege is held for the whole table, or if there is a column-level grant of the privilege for the column. The column can be specified by name or by attribute number (
     <code>
      pg_attribute
     </code>
     .
     <code>
      attnum
     </code>
     ). Allowable privilege types are
     <code>
      SELECT
     </code>
     ,
     <code>
      INSERT
     </code>
     ,
     <code>
      UPDATE
     </code>
     , and
     <code>
      REFERENCES
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      has_database_privilege
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        user
       </code>
      </em>
      <code>
       name
      </code>
      or
      <code>
       oid
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       database
      </code>
     </em>
     <code>
      text
     </code>
     or
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       privilege
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Does user have privilege for database? Allowable privilege types are
     <code>
      CREATE
     </code>
     ,
     <code>
      CONNECT
     </code>
     ,
     <code>
      TEMPORARY
     </code>
     , and
     <code>
      TEMP
     </code>
     (which is equivalent to
     <code>
      TEMPORARY
     </code>
     ).
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      has_foreign_data_wrapper_privilege
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        user
       </code>
      </em>
      <code>
       name
      </code>
      or
      <code>
       oid
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       fdw
      </code>
     </em>
     <code>
      text
     </code>
     or
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       privilege
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Does user have privilege for foreign-data wrapper? The only allowable privilege type is
     <code>
      USAGE
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      has_function_privilege
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        user
       </code>
      </em>
      <code>
       name
      </code>
      or
      <code>
       oid
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       function
      </code>
     </em>
     <code>
      text
     </code>
     or
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       privilege
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Does user have privilege for function? The only allowable privilege type is
     <code>
      EXECUTE
     </code>
     .
    </p>
    <p>
     When specifying a function by name rather than by OID, the allowed input is the same as for the
     <code>
      regprocedure
     </code>
     data type (see
     <a class="xref" href="datatype-oid.md" title="8.19. Object Identifier Types">
      Section 8.19
     </a>
     ). An example is:
    </p>
    <pre class="programlisting">
SELECT has_function_privilege('joeuser', 'myfunc(int, text)', 'execute');
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      has_language_privilege
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        user
       </code>
      </em>
      <code>
       name
      </code>
      or
      <code>
       oid
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       language
      </code>
     </em>
     <code>
      text
     </code>
     or
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       privilege
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Does user have privilege for language? The only allowable privilege type is
     <code>
      USAGE
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      has_largeobject_privilege
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        user
       </code>
      </em>
      <code>
       name
      </code>
      or
      <code>
       oid
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       largeobject
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       privilege
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Does user have privilege for large object? Allowable privilege types are
     <code>
      SELECT
     </code>
     and
     <code>
      UPDATE
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      has_parameter_privilege
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        user
       </code>
      </em>
      <code>
       name
      </code>
      or
      <code>
       oid
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       parameter
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       privilege
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Does user have privilege for configuration parameter? The parameter name is case-insensitive. Allowable privilege types are
     <code>
      SET
     </code>
     and
     <code>
      ALTER SYSTEM
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      has_schema_privilege
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        user
       </code>
      </em>
      <code>
       name
      </code>
      or
      <code>
       oid
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       schema
      </code>
     </em>
     <code>
      text
     </code>
     or
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       privilege
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Does user have privilege for schema? Allowable privilege types are
     <code>
      CREATE
     </code>
     and
     <code>
      USAGE
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      has_sequence_privilege
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        user
       </code>
      </em>
      <code>
       name
      </code>
      or
      <code>
       oid
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       sequence
      </code>
     </em>
     <code>
      text
     </code>
     or
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       privilege
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Does user have privilege for sequence? Allowable privilege types are
     <code>
      USAGE
     </code>
     ,
     <code>
      SELECT
     </code>
     , and
     <code>
      UPDATE
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      has_server_privilege
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        user
       </code>
      </em>
      <code>
       name
      </code>
      or
      <code>
       oid
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       server
      </code>
     </em>
     <code>
      text
     </code>
     or
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       privilege
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Does user have privilege for foreign server? The only allowable privilege type is
     <code>
      USAGE
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      has_table_privilege
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        user
       </code>
      </em>
      <code>
       name
      </code>
      or
      <code>
       oid
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       table
      </code>
     </em>
     <code>
      text
     </code>
     or
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       privilege
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Does user have privilege for table? Allowable privilege types are
     <code>
      SELECT
     </code>
     ,
     <code>
      INSERT
     </code>
     ,
     <code>
      UPDATE
     </code>
     ,
     <code>
      DELETE
     </code>
     ,
     <code>
      TRUNCATE
     </code>
     ,
     <code>
      REFERENCES
     </code>
     ,
     <code>
      TRIGGER
     </code>
     , and
     <code>
      MAINTAIN
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      has_tablespace_privilege
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        user
       </code>
      </em>
      <code>
       name
      </code>
      or
      <code>
       oid
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       tablespace
      </code>
     </em>
     <code>
      text
     </code>
     or
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       privilege
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Does user have privilege for tablespace? The only allowable privilege type is
     <code>
      CREATE
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      has_type_privilege
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        user
       </code>
      </em>
      <code>
       name
      </code>
      or
      <code>
       oid
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       type
      </code>
     </em>
     <code>
      text
     </code>
     or
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       privilege
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Does user have privilege for data type? The only allowable privilege type is
     <code>
      USAGE
     </code>
     . When specifying a type by name rather than by OID, the allowed input is the same as for the
     <code>
      regtype
     </code>
     data type (see
     <a class="xref" href="datatype-oid.md" title="8.19. Object Identifier Types">
      Section 8.19
     </a>
     ).
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_has_role
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        user
       </code>
      </em>
      <code>
       name
      </code>
      or
      <code>
       oid
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       role
      </code>
     </em>
     <code>
      text
     </code>
     or
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       privilege
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Does user have privilege for role? Allowable privilege types are
     <code>
      MEMBER
     </code>
     ,
     <code>
      USAGE
     </code>
     , and
     <code>
      SET
     </code>
     .
     <code>
      MEMBER
     </code>
     denotes direct or indirect membership in the role without regard to what specific privileges may be conferred.
     <code>
      USAGE
     </code>
     denotes whether the privileges of the role are immediately available without doing
     <code>
      SET ROLE
     </code>
     , while
     <code>
      SET
     </code>
     denotes whether it is possible to change to the role using the
     <code>
      SET ROLE
     </code>
     command.
     <code>
      WITH ADMIN OPTION
     </code>
     or
     <code>
      WITH GRANT OPTION
     </code>
     can be added to any of these privilege types to test whether the
     <code>
      ADMIN
     </code>
     privilege is held (all six spellings test the same thing). This function does not allow the special case of setting
     <em class="parameter">
      <code>
       user
      </code>
     </em>
     to
     <code>
      public
     </code>
     , because the PUBLIC pseudo-role can never be a member of real roles.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      row_security_active
     </code>
     (
     <em class="parameter">
      <code>
       table
      </code>
     </em>
     <code>
      text
     </code>
     or
     <code>
      oid
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Is row-level security active for the specified table in the context of the current user and current environment?
    </p>
   </td>
  </tr>
 </tbody>
</table>

[Tabela 9.73](functions-info.md#FUNCTIONS-ACLITEM-OP-TABLE) mostra os operadores disponíveis para o tipo `aclitem`, que é a representação de catálogo de privilégios de acesso. Consulte [Seção 5.8](ddl-priv.md) para obter informações sobre como ler os valores de privilégios de acesso.

**Tabela 9.73. Operadores `aclitem`

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Operator
    </p>
    <p>
     Description
    </p>
    <p>
     Example(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      aclitem
     </code>
     <code>
      =
     </code>
     <code>
      aclitem
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     Are
     <code>
      aclitem
     </code>
     s equal?  (Notice that type
     <code>
      aclitem
     </code>
     lacks the usual set of comparison operators; it has only equality.  In turn,
     <code>
      aclitem
     </code>
     arrays can only be compared for equality.)
    </p>
    <p>
     <code>
      'calvin=r*w/hobbes'::aclitem = 'calvin=r*w*/hobbes'::aclitem
     </code>
     →
     <code>
      f
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      aclitem[]
     </code>
     <code>
      @&gt;
     </code>
     <code>
      aclitem
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     Does array contain the specified privileges?  (This is true if there is an array entry that matches the
     <code>
      aclitem
     </code>
     's grantee and grantor, and has at least the specified set of privileges.)
    </p>
    <p>
     <code>
      '{calvin=r*w/hobbes,hobbes=r*w*/postgres}'::aclitem[] @&gt; 'calvin=r*/hobbes'::aclitem
     </code>
     →
     <code>
      t
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      aclitem[]
     </code>
     <code>
      ~
     </code>
     <code>
      aclitem
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     This is a deprecated alias for
     <code>
      @&gt;
     </code>
     .
    </p>
    <p>
     <code>
      '{calvin=r*w/hobbes,hobbes=r*w*/postgres}'::aclitem[] ~ 'calvin=r*/hobbes'::aclitem
     </code>
     →
     <code>
      t
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>

[Tabela 9.74](functions-info.md#FUNCTIONS-ACLITEM-FN-TABLE) mostra algumas funções adicionais para gerenciar o tipo `aclitem`.

**Tabela 9.74. Funções `aclitem`**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função
    </p>
    <p>
     Descrição
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      acldefault
     </code>
     (
     <em class="parameter">
      <code>
       type
      </code>
     </em>
     <code>
      "char"
     </code>
     ,
     <em class="parameter">
      <code>
       ownerId
      </code>
     </em>
     <code>
      oid
     </code>
     )
     <code>
      aclitem[]
     </code>
    </p>
    <p>
     constrói
     <code>
      aclitem
     </code>
     um array que contém os privilégios de acesso padrão para um objeto do tipo
     <em class="parameter">
      <code>
       type
      </code>
     </em>
     pertencente ao papel com OID
     <em class="parameter">
      <code>
       ownerId
      </code>
     </em>
     . Isso representa os privilégios de acesso que serão assumidos quando um objeto é acessado.
     <acronym class="acronym">
      ACL
     </acronym>
     a entrada é nula. (Os privilégios de acesso padrão são descritos em
     <a class="xref" href="ddl-priv.md" title="5.8. Privileges">
      Seção 5.8
     </a>
     .) O
     <em class="parameter">
      <code>
       type
      </code>
     </em>
     o parâmetro deve ser um dos valores 'c' para
     <code>
      COLUMN
     </code>
     , 'r' para
     <code>
      TABLE
     </code>
     e objetos semelhantes a mesas, 's' para
     <code>
      SEQUENCE
     </code>
     , 'd' para
     <code>
      DATABASE
     </code>
     , 'f' para
     <code>
      FUNCTION
     </code>
     ou
     <code>
      PROCEDURE
     </code>
     , 'l' para
     <code>
      LANGUAGE
     </code>
     , 'L' para
     <code>
      LARGE OBJECT
     </code>
     , 'n' para
     <code>
      SCHEMA
     </code>
     , 'p' para
     <code>
      PARAMETER
     </code>
     , 't' para
     <code>
      TABLESPACE
     </code>
     , 'F' para
     <code>
      FOREIGN DATA WRAPPER
     </code>
     , 'S' para
     <code>
      FOREIGN SERVER
     </code>
     , ou 'T' para
     <code>
      TYPE
     </code>
     ou
     <code>
      DOMAIN
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      aclexplode
     </code>
     (
     <code>
      aclitem[]
     </code>
     )
     <code>
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       grantor
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       grantee
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       privilege_type
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       is_grantable
      </code>
     </em>
     <code>
      boolean
     </code>
     )
    </p>
    <p>
     Retorna o
     <code>
      aclitem
     </code>
     um array como um conjunto de linhas. Se o destinatário for o pseudorole PUBLIC, ele é representado por zero no
     <em class="parameter">
      <code>
       grantee
      </code>
     </em>
     coluna. Cada privilégio concedido é representado como
     <code>
      SELECT
     </code>
     ,
     <code>
      INSERT
     </code>
     , etc. (ver
     <a class="xref" href="ddl-priv.md#PRIVILEGE-ABBREVS-TABLE" title="Table 5.1. ACL Privilege Abbreviations">
      Tabela 5.1
     </a>
     (para uma lista completa). Observe que cada privilégio é exibido como uma linha separada, portanto, apenas uma palavra-chave aparece na tabela.
     <em class="parameter">
      <code>
       privilege_type
      </code>
     </em>
     column.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      makeaclitem
     </code>
     (
     <em class="parameter">
      <code>
       grantee
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       grantor
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       privileges
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       is_grantable
      </code>
     </em>
     <code>
      boolean
     </code>
     )
     <code>
      aclitem
     </code>
    </p>
    <p>
     constrói
     <code>
      aclitem
     </code>
     com as propriedades dadas.
     <em class="parameter">
      <code>
       privileges
      </code>
     </em>
     é uma lista separada por vírgula de nomes de privilégios, como
     <code>
      SELECT
     </code>
     ,
     <code>
      INSERT
     </code>
     , etc., todas as quais estão definidas no resultado. (O caso da string de privilégio não é significativo, e espaços em branco extras são permitidos entre, mas não dentro, dos nomes de privilégio.)
    </p>
   </td>
  </tr>
 </tbody>
</table>

#### 9.27.3. Funções de consulta de visibilidade do esquema [#](#FUNCTIONS-INFO-SCHEMA)

[Tabela 9.75](functions-info.md#FUNCTIONS-INFO-SCHEMA-TABLE) mostra funções que determinam se um determinado objeto é *visível* no caminho de busca do esquema atual. Por exemplo, uma tabela é considerada visível se seu esquema contendo estiver no caminho de busca e nenhuma tabela com o mesmo nome aparecer anteriormente no caminho de busca. Isso é equivalente à afirmação de que a tabela pode ser referenciada pelo nome sem qualificação explícita do esquema. Assim, para listar os nomes de todas as tabelas visíveis:

```sql
SELECT relname FROM pg_class WHERE pg_table_is_visible(oid);
```

Para funções e operadores, um objeto no caminho de busca é dito ser visível se não houver um objeto com o mesmo nome e o mesmo tipo de dados de argumento anteriormente no caminho. Para as classes e famílias de operadores, tanto o nome quanto o método de acesso ao índice associado são considerados.

**Tabela 9.75. Funções de consulta de visibilidade de esquema**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_collation_is_visible
     </code>
     (
     <em class="parameter">
      <code>
       collation
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Is collation visible in search path?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_conversion_is_visible
     </code>
     (
     <em class="parameter">
      <code>
       conversion
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Is conversion visible in search path?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_function_is_visible
     </code>
     (
     <em class="parameter">
      <code>
       function
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Is function visible in search path? (This also works for procedures and aggregates.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_opclass_is_visible
     </code>
     (
     <em class="parameter">
      <code>
       opclass
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Is operator class visible in search path?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_operator_is_visible
     </code>
     (
     <em class="parameter">
      <code>
       operator
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Is operator visible in search path?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_opfamily_is_visible
     </code>
     (
     <em class="parameter">
      <code>
       opclass
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Is operator family visible in search path?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_statistics_obj_is_visible
     </code>
     (
     <em class="parameter">
      <code>
       stat
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Is statistics object visible in search path?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_table_is_visible
     </code>
     (
     <em class="parameter">
      <code>
       table
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Is table visible in search path? (This works for all types of relations, including views, materialized views, indexes, sequences and foreign tables.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_ts_config_is_visible
     </code>
     (
     <em class="parameter">
      <code>
       config
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Is text search configuration visible in search path?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_ts_dict_is_visible
     </code>
     (
     <em class="parameter">
      <code>
       dict
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Is text search dictionary visible in search path?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_ts_parser_is_visible
     </code>
     (
     <em class="parameter">
      <code>
       parser
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Is text search parser visible in search path?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_ts_template_is_visible
     </code>
     (
     <em class="parameter">
      <code>
       template
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Is text search template visible in search path?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_type_is_visible
     </code>
     (
     <em class="parameter">
      <code>
       type
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Is type (or domain) visible in search path?
    </p>
   </td>
  </tr>
 </tbody>
</table>

Todas essas funções exigem OIDs de objeto para identificar o objeto a ser verificado. Se você deseja testar um objeto pelo nome, é conveniente usar os tipos de alias de OID, como `regclass`, `regtype`, `regprocedure`, `regoperator`, `regconfig` ou `regdictionary`, por exemplo:

```sql
SELECT pg_type_is_visible('myschema.widget'::regtype);
```

Observe que não faria muito sentido testar um nome de tipo não qualificado por esquema dessa maneira — se o nome pode ser reconhecido, ele deve ser visível.

#### 9.27.4. Funções de informações do catálogo do sistema [#](#FUNCTIONS-INFO-CATALOG)

[Tabela 9.76](functions-info.md#FUNCTIONS-INFO-CATALOG-TABLE) lista funções que extraem informações dos catálogos do sistema.

**Tabela 9.76. Funções de Informações do Catálogo do Sistema**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry" id="FORMAT-TYPE">
    <p class="func_signature">
     <code>
      format_type
     </code>
     (
     <em class="parameter">
      <code>
       type
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       typemod
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Returns the SQL name for a data type that is identified by its type OID and possibly a type modifier.  Pass NULL for the type modifier if no specific modifier is known.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_basetype
     </code>
     (
     <code>
      regtype
     </code>
     ) →
     <code>
      regtype
     </code>
    </p>
    <p>
     Returns the OID of the base type of a domain identified by its type OID.  If the argument is the OID of a non-domain type, returns the argument as-is.  Returns NULL if the argument is not a valid type OID.  If there's a chain of domain dependencies, it will recurse until finding the base type.
    </p>
    <p>
     Assuming
     <code>
      CREATE DOMAIN mytext AS text
     </code>
     :
    </p>
    <p>
     <code>
      pg_basetype('mytext'::regtype)
     </code>
     →
     <code>
      text
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-CHAR-TO-ENCODING">
    <p class="func_signature">
     <code>
      pg_char_to_encoding
     </code>
     (
     <em class="parameter">
      <code>
       encoding
      </code>
     </em>
     <code>
      name
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Converts the supplied encoding name into an integer representing the internal identifier used in some system catalog tables. Returns
     <code>
      -1
     </code>
     if an unknown encoding name is provided.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-ENCODING-TO-CHAR">
    <p class="func_signature">
     <code>
      pg_encoding_to_char
     </code>
     (
     <em class="parameter">
      <code>
       encoding
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      name
     </code>
    </p>
    <p>
     Converts the integer used as the internal identifier of an encoding in some system catalog tables into a human-readable string. Returns an empty string if an invalid encoding number is provided.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_catalog_foreign_keys
     </code>
     () →
     <code>
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       fktable
      </code>
     </em>
     <code>
      regclass
     </code>
     ,
     <em class="parameter">
      <code>
       fkcols
      </code>
     </em>
     <code>
      text[]
     </code>
     ,
     <em class="parameter">
      <code>
       pktable
      </code>
     </em>
     <code>
      regclass
     </code>
     ,
     <em class="parameter">
      <code>
       pkcols
      </code>
     </em>
     <code>
      text[]
     </code>
     ,
     <em class="parameter">
      <code>
       is_array
      </code>
     </em>
     <code>
      boolean
     </code>
     ,
     <em class="parameter">
      <code>
       is_opt
      </code>
     </em>
     <code>
      boolean
     </code>
     )
    </p>
    <p>
     Returns a set of records describing the foreign key relationships that exist within the
     <span class="productname">
      PostgreSQL
     </span>
     system catalogs. The
     <em class="parameter">
      <code>
       fktable
      </code>
     </em>
     column contains the name of the referencing catalog, and the
     <em class="parameter">
      <code>
       fkcols
      </code>
     </em>
     column contains the name(s) of the referencing column(s).  Similarly, the
     <em class="parameter">
      <code>
       pktable
      </code>
     </em>
     column contains the name of the referenced catalog, and the
     <em class="parameter">
      <code>
       pkcols
      </code>
     </em>
     column contains the name(s) of the referenced column(s). If
     <em class="parameter">
      <code>
       is_array
      </code>
     </em>
     is true, the last referencing column is an array, each of whose elements should match some entry in the referenced catalog. If
     <em class="parameter">
      <code>
       is_opt
      </code>
     </em>
     is true, the referencing column(s) are allowed to contain zeroes instead of a valid reference.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_constraintdef
     </code>
     (
     <em class="parameter">
      <code>
       constraint
      </code>
     </em>
     <code>
      oid
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        pretty
       </code>
      </em>
      <code>
       boolean
      </code>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Reconstructs the creating command for a constraint. (This is a decompiled reconstruction, not the original text of the command.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_expr
     </code>
     (
     <em class="parameter">
      <code>
       expr
      </code>
     </em>
     <code>
      pg_node_tree
     </code>
     ,
     <em class="parameter">
      <code>
       relation
      </code>
     </em>
     <code>
      oid
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        pretty
       </code>
      </em>
      <code>
       boolean
      </code>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Decompiles the internal form of an expression stored in the system catalogs, such as the default value for a column.  If the expression might contain Vars, specify the OID of the relation they refer to as the second parameter; if no Vars are expected, passing zero is sufficient.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_functiondef
     </code>
     (
     <em class="parameter">
      <code>
       func
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Reconstructs the creating command for a function or procedure. (This is a decompiled reconstruction, not the original text of the command.) The result is a complete
     <code>
      CREATE OR REPLACE FUNCTION
     </code>
     or
     <code>
      CREATE OR REPLACE PROCEDURE
     </code>
     statement.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_function_arguments
     </code>
     (
     <em class="parameter">
      <code>
       func
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Reconstructs the argument list of a function or procedure, in the form it would need to appear in within
     <code>
      CREATE FUNCTION
     </code>
     (including default values).
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_function_identity_arguments
     </code>
     (
     <em class="parameter">
      <code>
       func
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Reconstructs the argument list necessary to identify a function or procedure, in the form it would need to appear in within commands such as
     <code>
      ALTER FUNCTION
     </code>
     .  This form omits default values.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_function_result
     </code>
     (
     <em class="parameter">
      <code>
       func
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Reconstructs the
     <code>
      RETURNS
     </code>
     clause of a function, in the form it would need to appear in within
     <code>
      CREATE FUNCTION
     </code>
     .  Returns
     <code>
      NULL
     </code>
     for a procedure.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_indexdef
     </code>
     (
     <em class="parameter">
      <code>
       index
      </code>
     </em>
     <code>
      oid
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        column
       </code>
      </em>
      <code>
       integer
      </code>
      ,
      <em class="parameter">
       <code>
        pretty
       </code>
      </em>
      <code>
       boolean
      </code>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Reconstructs the creating command for an index. (This is a decompiled reconstruction, not the original text of the command.)  If
     <em class="parameter">
      <code>
       column
      </code>
     </em>
     is supplied and is not zero, only the definition of that column is reconstructed.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_keywords
     </code>
     () →
     <code>
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       word
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       catcode
      </code>
     </em>
     <code>
      "char"
     </code>
     ,
     <em class="parameter">
      <code>
       barelabel
      </code>
     </em>
     <code>
      boolean
     </code>
     ,
     <em class="parameter">
      <code>
       catdesc
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       baredesc
      </code>
     </em>
     <code>
      text
     </code>
     )
    </p>
    <p>
     Returns a set of records describing the SQL keywords recognized by the server.  The
     <em class="parameter">
      <code>
       word
      </code>
     </em>
     column contains the keyword.  The
     <em class="parameter">
      <code>
       catcode
      </code>
     </em>
     column contains a category code:
     <code>
      U
     </code>
     for an unreserved keyword,
     <code>
      C
     </code>
     for a keyword that can be a column name,
     <code>
      T
     </code>
     for a keyword that can be a type or function name, or
     <code>
      R
     </code>
     for a fully reserved keyword. The
     <em class="parameter">
      <code>
       barelabel
      </code>
     </em>
     column contains
     <code>
      true
     </code>
     if the keyword can be used as a
     <span class="quote">
      “
      <span class="quote">
       bare
      </span>
      ”
     </span>
     column label in
     <code>
      SELECT
     </code>
     lists, or
     <code>
      false
     </code>
     if it can only be used after
     <code>
      AS
     </code>
     . The
     <em class="parameter">
      <code>
       catdesc
      </code>
     </em>
     column contains a possibly-localized string describing the keyword's category. The
     <em class="parameter">
      <code>
       baredesc
      </code>
     </em>
     column contains a possibly-localized string describing the keyword's column label status.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_partition_constraintdef
     </code>
     (
     <em class="parameter">
      <code>
       table
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Reconstructs the definition of a partition constraint. (This is a decompiled reconstruction, not the original text of the command.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_partkeydef
     </code>
     (
     <em class="parameter">
      <code>
       table
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Reconstructs the definition of a partitioned table's partition key, in the form it would have in the
     <code>
      PARTITION BY
     </code>
     clause of
     <code>
      CREATE TABLE
     </code>
     . (This is a decompiled reconstruction, not the original text of the command.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_ruledef
     </code>
     (
     <em class="parameter">
      <code>
       rule
      </code>
     </em>
     <code>
      oid
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        pretty
       </code>
      </em>
      <code>
       boolean
      </code>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Reconstructs the creating command for a rule. (This is a decompiled reconstruction, not the original text of the command.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_serial_sequence
     </code>
     (
     <em class="parameter">
      <code>
       table
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       column
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Returns the name of the sequence associated with a column, or NULL if no sequence is associated with the column. If the column is an identity column, the associated sequence is the sequence internally created for that column. For columns created using one of the serial types (
     <code>
      serial
     </code>
     ,
     <code>
      smallserial
     </code>
     ,
     <code>
      bigserial
     </code>
     ), it is the sequence created for that serial column definition. In the latter case, the association can be modified or removed with
     <code>
      ALTER SEQUENCE OWNED BY
     </code>
     . (This function probably should have been called
     <code>
      pg_get_owned_sequence
     </code>
     ; its current name reflects the fact that it has historically been used with serial-type columns.)  The first parameter is a table name with optional schema, and the second parameter is a column name.  Because the first parameter potentially contains both schema and table names, it is parsed per usual SQL rules, meaning it is lower-cased by default. The second parameter, being just a column name, is treated literally and so has its case preserved.  The result is suitably formatted for passing to the sequence functions (see
     <a class="xref" href="functions-sequence.md" title="9.17. Sequence Manipulation Functions">
      Section 9.17
     </a>
     ).
    </p>
    <p>
     A typical use is in reading the current value of the sequence for an identity or serial column, for example:
    </p>
    <pre class="programlisting">
SELECT currval(pg_get_serial_sequence('sometable', 'id'));
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_statisticsobjdef
     </code>
     (
     <em class="parameter">
      <code>
       statobj
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Reconstructs the creating command for an extended statistics object. (This is a decompiled reconstruction, not the original text of the command.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_triggerdef
     </code>
     (
     <em class="parameter">
      <code>
       trigger
      </code>
     </em>
     <code>
      oid
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        pretty
       </code>
      </em>
      <code>
       boolean
      </code>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Reconstructs the creating command for a trigger. (This is a decompiled reconstruction, not the original text of the command.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_userbyid
     </code>
     (
     <em class="parameter">
      <code>
       role
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      name
     </code>
    </p>
    <p>
     Returns a role's name given its OID.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_viewdef
     </code>
     (
     <em class="parameter">
      <code>
       view
      </code>
     </em>
     <code>
      oid
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        pretty
       </code>
      </em>
      <code>
       boolean
      </code>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Reconstructs the underlying
     <code>
      SELECT
     </code>
     command for a view or materialized view.  (This is a decompiled reconstruction, not the original text of the command.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_viewdef
     </code>
     (
     <em class="parameter">
      <code>
       view
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       wrap_column
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Reconstructs the underlying
     <code>
      SELECT
     </code>
     command for a view or materialized view.  (This is a decompiled reconstruction, not the original text of the command.)  In this form of the function, pretty-printing is always enabled, and long lines are wrapped to try to keep them shorter than the specified number of columns.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_viewdef
     </code>
     (
     <em class="parameter">
      <code>
       view
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        pretty
       </code>
      </em>
      <code>
       boolean
      </code>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Reconstructs the underlying
     <code>
      SELECT
     </code>
     command for a view or materialized view, working from a textual name for the view rather than its OID.  (This is deprecated; use the OID variant instead.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_index_column_has_property
     </code>
     (
     <em class="parameter">
      <code>
       index
      </code>
     </em>
     <code>
      regclass
     </code>
     ,
     <em class="parameter">
      <code>
       column
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       property
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Tests whether an index column has the named property. Common index column properties are listed in
     <a class="xref" href="functions-info.md#FUNCTIONS-INFO-INDEX-COLUMN-PROPS" title="Table 9.77. Index Column Properties">
      Table 9.77
     </a>
     .</p>

        (Note that extension access methods can define additional property names for their indexes.)
     <code>
      NULL
     </code>
     is returned if the property name is not known or does not apply to the particular object, or if the OID or column number does not identify a valid object.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_index_has_property
     </code>
     (
     <em class="parameter">
      <code>
       index
      </code>
     </em>
     <code>
      regclass
     </code>
     ,
     <em class="parameter">
      <code>
       property
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Tests whether an index has the named property. Common index properties are listed in
     <a class="xref" href="functions-info.md#FUNCTIONS-INFO-INDEX-PROPS" title="Table 9.78. Index Properties">
      Table 9.78
     </a>
     .

        (Note that extension access methods can define additional property names for their indexes.)
     <code>
      NULL
     </code>
     is returned if the property name is not known or does not apply to the particular object, or if the OID does not identify a valid object.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_indexam_has_property
     </code>
     (
     <em class="parameter">
      <code>
       am
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       property
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Tests whether an index access method has the named property. Access method properties are listed in
     <a class="xref" href="functions-info.md#FUNCTIONS-INFO-INDEXAM-PROPS" title="Table 9.79. Index Access Method Properties">
      Table 9.79
     </a>
     .
     <code>
      NULL
     </code>
     is returned if the property name is not known or does not apply to the particular object, or if the OID does not identify a valid object.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_options_to_table
     </code>
     (
     <em class="parameter">
      <code>
       options_array
      </code>
     </em>
     <code>
      text[]
     </code>
     ) →
     <code>
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       option_name
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       option_value
      </code>
     </em>
     <code>
      text
     </code>
     )
    </p>
    <p>
     Returns the set of storage options represented by a value from
     <code>
      pg_class
     </code>
     .
     <code>
      reloptions
     </code>
     or
     <code>
      pg_attribute
     </code>
     .
     <code>
      attoptions
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_settings_get_flags
     </code>
     (
     <em class="parameter">
      <code>
       guc
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      text[]
     </code>
    </p>
    <p>
     Returns an array of the flags associated with the given GUC, or
     <code>
      NULL
     </code>
     if it does not exist. The result is an empty array if the GUC exists but there are no flags to show. Only the most useful flags listed in
     <a class="xref" href="functions-info.md#FUNCTIONS-PG-SETTINGS-FLAGS" title="Table 9.80. GUC Flags">
      Table 9.80
     </a>
     are exposed.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_tablespace_databases
     </code>
     (
     <em class="parameter">
      <code>
       tablespace
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      setof oid
     </code>
    </p>
    <p>
     Returns the set of OIDs of databases that have objects stored in the specified tablespace.  If this function returns any rows, the tablespace is not empty and cannot be dropped.  To identify the specific objects populating the tablespace, you will need to connect to the database(s) identified by
     <code>
      pg_tablespace_databases
     </code>
     and query their
     <code>
      pg_class
     </code>
     catalogs.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_tablespace_location
     </code>
     (
     <em class="parameter">
      <code>
       tablespace
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Returns the file system path that this tablespace is located in.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_typeof
     </code>
     (
     <code>
      "any"
     </code>
     ) →
     <code>
      regtype
     </code>
    </p>
    <p>
     Returns the OID of the data type of the value that is passed to it. This can be helpful for troubleshooting or dynamically constructing SQL queries.  The function is declared as returning
     <code>
      regtype
     </code>
     , which is an OID alias type (see
     <a class="xref" href="datatype-oid.md" title="8.19. Object Identifier Types">
      Section 8.19
     </a>
     ); this means that it is the same as an OID for comparison purposes but displays as a type name.
    </p>
    <p>
     <code>
      pg_typeof(33)
     </code>
     →
     <code>
      integer
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      COLLATION FOR
     </code>
     (
     <code>
      "any"
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Returns the name of the collation of the value that is passed to it. The value is quoted and schema-qualified if necessary.  If no collation was derived for the argument expression, then
     <code>
      NULL
     </code>
     is returned.  If the argument is not of a collatable data type, then an error is raised.
    </p>
    <p>
     <code>
      collation for ('foo'::text)
     </code>
     →
     <code>
      "default"
     </code>
    </p>
    <p>
     <code>
      collation for ('foo' COLLATE "de_DE")
     </code>
     →
     <code>
      "de_DE"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      to_regclass
     </code>
     (
     <code>
      text
     </code>
     ) →
     <code>
      regclass
     </code>
    </p>
    <p>
     Translates a textual relation name to its OID.  A similar result is obtained by casting the string to type
     <code>
      regclass
     </code>
     (see
     <a class="xref" href="datatype-oid.md" title="8.19. Object Identifier Types">
      Section 8.19
     </a>
     ); however, this function will return
     <code>
      NULL
     </code>
     rather than throwing an error if the name is not found.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      to_regcollation
     </code>
     (
     <code>
      text
     </code>
     ) →
     <code>
      regcollation
     </code>
    </p>
    <p>
     Translates a textual collation name to its OID.  A similar result is obtained by casting the string to type
     <code>
      regcollation
     </code>
     (see
     <a class="xref" href="datatype-oid.md" title="8.19. Object Identifier Types">
      Section 8.19
     </a>
     ); however, this function will return
     <code>
      NULL
     </code>
     rather than throwing an error if the name is not found.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      to_regnamespace
     </code>
     (
     <code>
      text
     </code>
     ) →
     <code>
      regnamespace
     </code>
    </p>
    <p>
     Translates a textual schema name to its OID.  A similar result is obtained by casting the string to type
     <code>
      regnamespace
     </code>
     (see
     <a class="xref" href="datatype-oid.md" title="8.19. Object Identifier Types">
      Section 8.19
     </a>
     ); however, this function will return
     <code>
      NULL
     </code>
     rather than throwing an error if the name is not found.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      to_regoper
     </code>
     (
     <code>
      text
     </code>
     ) →
     <code>
      regoper
     </code>
    </p>
    <p>
     Translates a textual operator name to its OID.  A similar result is obtained by casting the string to type
     <code>
      regoper
     </code>
     (see
     <a class="xref" href="datatype-oid.md" title="8.19. Object Identifier Types">
      Section 8.19
     </a>
     ); however, this function will return
     <code>
      NULL
     </code>
     rather than throwing an error if the name is not found or is ambiguous.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      to_regoperator
     </code>
     (
     <code>
      text
     </code>
     ) →
     <code>
      regoperator
     </code>
    </p>
    <p>
     Translates a textual operator name (with parameter types) to its OID.  A similar result is obtained by casting the string to type
     <code>
      regoperator
     </code>
     (see
     <a class="xref" href="datatype-oid.md" title="8.19. Object Identifier Types">
      Section 8.19
     </a>
     ); however, this function will return
     <code>
      NULL
     </code>
     rather than throwing an error if the name is not found.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      to_regproc
     </code>
     (
     <code>
      text
     </code>
     ) →
     <code>
      regproc
     </code>
    </p>
    <p>
     Translates a textual function or procedure name to its OID.  A similar result is obtained by casting the string to type
     <code>
      regproc
     </code>
     (see
     <a class="xref" href="datatype-oid.md" title="8.19. Object Identifier Types">
      Section 8.19
     </a>
     ); however, this function will return
     <code>
      NULL
     </code>
     rather than throwing an error if the name is not found or is ambiguous.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      to_regprocedure
     </code>
     (
     <code>
      text
     </code>
     ) →
     <code>
      regprocedure
     </code>
    </p>
    <p>
     Translates a textual function or procedure name (with argument types) to its OID.  A similar result is obtained by casting the string to type
     <code>
      regprocedure
     </code>
     (see
     <a class="xref" href="datatype-oid.md" title="8.19. Object Identifier Types">
      Section 8.19
     </a>
     ); however, this function will return
     <code>
      NULL
     </code>
     rather than throwing an error if the name is not found.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      to_regrole
     </code>
     (
     <code>
      text
     </code>
     ) →
     <code>
      regrole
     </code>
    </p>
    <p>
     Translates a textual role name to its OID.  A similar result is obtained by casting the string to type
     <code>
      regrole
     </code>
     (see
     <a class="xref" href="datatype-oid.md" title="8.19. Object Identifier Types">
      Section 8.19
     </a>
     ); however, this function will return
     <code>
      NULL
     </code>
     rather than throwing an error if the name is not found.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="TO-REGTYPE">
    <p class="func_signature">
     <code>
      to_regtype
     </code>
     (
     <code>
      text
     </code>
     ) →
     <code>
      regtype
     </code>
    </p>
    <p>
     Parses a string of text, extracts a potential type name from it, and translates that name into a type OID.  A syntax error in the string will result in an error; but if the string is a syntactically valid type name that happens not to be found in the catalogs, the result is
     <code>
      NULL
     </code>
     .  A similar result is obtained by casting the string to type
     <code>
      regtype
     </code>
     (see
     <a class="xref" href="datatype-oid.md" title="8.19. Object Identifier Types">
      Section 8.19
     </a>
     ), except that that will throw error for name not found.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      to_regtypemod
     </code>
     (
     <code>
      text
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Parses a string of text, extracts a potential type name from it, and translates its type modifier, if any.  A syntax error in the string will result in an error; but if the string is a syntactically valid type name that happens not to be found in the catalogs, the result is
     <code>
      NULL
     </code>
     .  The result is
     <code>
      -1
     </code>
     if no type modifier is present.
    </p>
    <p>
     <code>
      to_regtypemod
     </code>
     can be combined with
     <a class="xref" href="functions-info.md#TO-REGTYPE">
      to_regtype
     </a>
     to produce appropriate inputs for
     <a class="xref" href="functions-info.md#FORMAT-TYPE">
      format_type
     </a>
     , allowing a string representing a type name to be canonicalized.
    </p>
    <p>
     <code>
      format_type(to_regtype('varchar(32)'), to_regtypemod('varchar(32)'))
     </code>
     →
     <code>
      character varying(32)
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>










A maioria das funções que reconstruem (decompilam) objetos de banco de dados tem uma bandeira opcional *`pretty`*, que, se `true` causar o resultado a ser “impresso de forma bonita”. A impressão bonita suprime as chaves e parênteses desnecessários e adiciona espaços em branco para legibilidade. O formato impresso de forma bonita é mais legível, mas o formato padrão é mais provável que seja interpretado da mesma maneira por versões futuras do PostgreSQL; portanto, evite usar saída impressa de forma bonita para fins de dump. Passar `false` para o parâmetro *`pretty`* produz o mesmo resultado que omitir o parâmetro.

**Tabela 9.77. Propriedades da coluna de índice**



<table>
 <thead>
  <tr>
   <th>
    Name
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     asc
    </code>
   </td>
   <td>
    A coluna é ordenada em ordem crescente em uma varredura para frente?
   </td>
  </tr>
  <tr>
   <td>
    <code>
     desc
    </code>
   </td>
   <td>
    A coluna é ordenada em ordem decrescente em uma varredura para frente?
   </td>
  </tr>
  <tr>
   <td>
    <code>
     nulls_first
    </code>
   </td>
   <td>
    A coluna ordena com os nulos primeiro em uma varredura direta?
   </td>
  </tr>
  <tr>
   <td>
    <code>
     nulls_last
    </code>
   </td>
   <td>
    A coluna é ordenada com nulos por último em uma varredura para frente?
   </td>
  </tr>
  <tr>
   <td>
    <code>
     orderable
    </code>
   </td>
   <td>
    A coluna possui algum tipo de ordem de classificação definida?
   </td>
  </tr>
  <tr>
   <td>
    <code>
     distance_orderable
    </code>
   </td>
   <td>
    Pode a coluna ser percorrida em ordem por
    <span class="quote">
     “
     <span class="quote">
      distância
     </span>
     ”
    </span>
    operador, por exemplo
    <code>
     ORDER BY col &lt;-&gt; constant
    </code>
    ?
   </td>
  </tr>
  <tr>
   <td>
    <code>
     returnable
    </code>
   </td>
   <td>
    O valor da coluna pode ser retornado por uma varredura apenas por índice?
   </td>
  </tr>
  <tr>
   <td>
    <code>
     search_array
    </code>
   </td>
   <td>
    A coluna suporta nativamente
    <code>
     col = ANY(array)
    </code>
    pesquisas?
   </td>
  </tr>
  <tr>
   <td>
    <code>
     search_nulls
    </code>
   </td>
   <td>
    A coluna suporta
    <code>
     IS NULL
    </code>
    e
    <code>
     IS NOT NULL
    </code>
    pesquisas?
   </td>
  </tr>
 </tbody>
</table>

**Tabela 9.78. Propriedades do índice**

<table>
 <thead>
  <tr>
   <th>
    Name
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     clusterable
    </code>
   </td>
   <td>
    Pode o índice ser utilizado em um
    <code>
     CLUSTER
    </code>
    qual o comando?
   </td>
  </tr>
  <tr>
   <td>
    <code>
     index_scan
    </code>
   </td>
   <td>
    O índice suporta varreduras simples (sem bitmap)?
   </td>
  </tr>
  <tr>
   <td>
    <code>
     bitmap_scan
    </code>
   </td>
   <td>
    O índice suporta varreduras de bitmap?
   </td>
  </tr>
  <tr>
   <td>
    <code>
     backward_scan
    </code>
   </td>
   <td>
    É possível alterar a direção do exame durante o exame (para
    <code>
     FETCH BACKWARD
    </code>
    sobre um cursor sem necessidade de materialização)?
   </td>
  </tr>
 </tbody>
</table>

**Tabela 9.79. Propriedades do Método de Acesso ao Índice**

<table>
 <thead>
  <tr>
   <th>
    Name
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     can_order
    </code>
   </td>
   <td>
    O método de acesso suporta
    <code>
     ASC
    </code>
    ,
    <code>
     DESC
    </code>
    e palavras-chave relacionadas em
    <code>
     CREATE INDEX
    </code>
    ?
   </td>
  </tr>
  <tr>
   <td>
    <code>
     can_unique
    </code>
   </td>
   <td>
    O método de acesso suporta índices únicos?
   </td>
  </tr>
  <tr>
   <td>
    <code>
     can_multi_col
    </code>
   </td>
   <td>
    O método de acesso suporta índices com múltiplas colunas?
   </td>
  </tr>
  <tr>
   <td>
    <code>
     can_exclude
    </code>
   </td>
   <td>
    O método de acesso suporta restrições de exclusão?
   </td>
  </tr>
  <tr>
   <td>
    <code>
     can_include
    </code>
   </td>
   <td>
    O método de acesso suporta o
    <code>
     INCLUDE
    </code>
    cláusula de
    <code>
     CREATE INDEX
    </code>
    ?
   </td>
  </tr>
 </tbody>
</table>

**Tabela 9.80. Fлагаres do GUC**

<table>
 <thead>
  <tr>
   <th>
    Flag
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     EXPLAIN
    </code>
   </td>
   <td>
    Os parâmetros com essa bandeira estão incluídos em
    <code>
     EXPLAIN (SETTINGS)
    </code>
    commands.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     NO_SHOW_ALL
    </code>
   </td>
   <td>
    Os parâmetros com essa bandeira são excluídos
    <code>
     SHOW ALL
    </code>
    commands.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     NO_RESET
    </code>
   </td>
   <td>
    Os parâmetros com esta bandeira não são suportados
    <code>
     RESET
    </code>
    commands.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     NO_RESET_ALL
    </code>
   </td>
   <td>
    Os parâmetros com essa bandeira são excluídos
    <code>
     RESET ALL
    </code>
    commands.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     NOT_IN_SAMPLE
    </code>
   </td>
   <td>
    Os parâmetros com essa bandeira não são incluídos
    <code>
     postgresql.conf
    </code>
    padrão.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     RUNTIME_COMPUTED
    </code>
   </td>
   <td>
    Os parâmetros com essa bandeira são calculados dinamicamente.
   </td>
  </tr>
 </tbody>
</table>

#### 9.27.5. Informações sobre o objeto e funções de endereçamento [#](#FUNCTIONS-INFO-OBJECT)

[Tabela 9.81](functions-info.md#FUNCTIONS-INFO-OBJECT-TABLE) lista funções relacionadas à identificação e endereçamento de objetos de banco de dados.

**Tabela 9.81. Informações e funções de endereçamento de objetos**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_acl
     </code>
     (
     <em class="parameter">
      <code>
       classid
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       objid
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       objsubid
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      aclitem[]
     </code>
    </p>
    <p>
     Returns the
     <acronym class="acronym">
      ACL
     </acronym>
     for a database object, specified by catalog OID, object OID and sub-object ID. This function returns
     <code>
      NULL
     </code>
     values for undefined objects.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_describe_object
     </code>
     (
     <em class="parameter">
      <code>
       classid
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       objid
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       objsubid
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Returns a textual description of a database object identified by catalog OID, object OID, and sub-object ID (such as a column number within a table; the sub-object ID is zero when referring to a whole object).  This description is intended to be human-readable, and might be translated, depending on server configuration.  This is especially useful to determine the identity of an object referenced in the
     <code>
      pg_depend
     </code>
     catalog. This function returns
     <code>
      NULL
     </code>
     values for undefined objects.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_identify_object
     </code>
     (
     <em class="parameter">
      <code>
       classid
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       objid
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       objsubid
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      record
     </code>
     (
     <em class="parameter">
      <code>
       type
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       schema
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       name
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       identity
      </code>
     </em>
     <code>
      text
     </code>
     )
    </p>
    <p>
     Returns a row containing enough information to uniquely identify the database object specified by catalog OID, object OID and sub-object ID. This information is intended to be machine-readable, and is never translated.
     <em class="parameter">
      <code>
       type
      </code>
     </em>
     identifies the type of database object;
     <em class="parameter">
      <code>
       schema
      </code>
     </em>
     is the schema name that the object belongs in, or
     <code>
      NULL
     </code>
     for object types that do not belong to schemas;
     <em class="parameter">
      <code>
       name
      </code>
     </em>
     is the name of the object, quoted if necessary, if the name (along with schema name, if pertinent) is sufficient to uniquely identify the object, otherwise
     <code>
      NULL
     </code>
     ;
     <em class="parameter">
      <code>
       identity
      </code>
     </em>
     is the complete object identity, with the precise format depending on object type, and each name within the format being schema-qualified and quoted as necessary. Undefined objects are identified with
     <code>
      NULL
     </code>
     values.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_identify_object_as_address
     </code>
     (
     <em class="parameter">
      <code>
       classid
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       objid
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       objsubid
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      record
     </code>
     (
     <em class="parameter">
      <code>
       type
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       object_names
      </code>
     </em>
     <code>
      text[]
     </code>
     ,
     <em class="parameter">
      <code>
       object_args
      </code>
     </em>
     <code>
      text[]
     </code>
     )
    </p>
    <p>
     Returns a row containing enough information to uniquely identify the database object specified by catalog OID, object OID and sub-object ID. The returned information is independent of the current server, that is, it could be used to identify an identically named object in another server.
     <em class="parameter">
      <code>
       type
      </code>
     </em>
     identifies the type of database object;
     <em class="parameter">
      <code>
       object_names
      </code>
     </em>
     and
     <em class="parameter">
      <code>
       object_args
      </code>
     </em>
     are text arrays that together form a reference to the object. These three values can be passed to
     <code>
      pg_get_object_address
     </code>
     to obtain the internal address of the object.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_object_address
     </code>
     (
     <em class="parameter">
      <code>
       type
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       object_names
      </code>
     </em>
     <code>
      text[]
     </code>
     ,
     <em class="parameter">
      <code>
       object_args
      </code>
     </em>
     <code>
      text[]
     </code>
     ) →
     <code>
      record
     </code>
     (
     <em class="parameter">
      <code>
       classid
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       objid
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       objsubid
      </code>
     </em>
     <code>
      integer
     </code>
     )
    </p>
    <p>
     Returns a row containing enough information to uniquely identify the database object specified by a type code and object name and argument arrays. The returned values are the ones that would be used in system catalogs such as
     <code>
      pg_depend
     </code>
     ; they can be passed to other system functions such as
     <code>
      pg_describe_object
     </code>
     or
     <code>
      pg_identify_object
     </code>
     .
     <em class="parameter">
      <code>
       classid
      </code>
     </em>
     is the OID of the system catalog containing the object;
     <em class="parameter">
      <code>
       objid
      </code>
     </em>
     is the OID of the object itself, and
     <em class="parameter">
      <code>
       objsubid
      </code>
     </em>
     is the sub-object ID, or zero if none. This function is the inverse of
     <code>
      pg_identify_object_as_address
     </code>
     . Undefined objects are identified with
     <code>
      NULL
     </code>
     values.
    </p>
   </td>
  </tr>
 </tbody>
</table>

`pg_get_acl` é útil para recuperar e inspecionar os privilégios associados a objetos de banco de dados sem olhar para catálogos específicos. Por exemplo, para recuperar todos os privilégios concedidos em objetos no banco de dados atual:

```sql
postgres=# SELECT
    (pg_identify_object(s.classid,s.objid,s.objsubid)).*,
    pg_catalog.pg_get_acl(s.classid,s.objid,s.objsubid) AS acl
FROM pg_catalog.pg_shdepend AS s
JOIN pg_catalog.pg_database AS d
    ON d.datname = current_database() AND
       d.oid = s.dbid
JOIN pg_catalog.pg_authid AS a
    ON a.oid = s.refobjid AND
       s.refclassid = 'pg_authid'::regclass
WHERE s.deptype = 'a';
-[ RECORD 1 ]-----------------------------------------
type     | table
schema   | public
name     | testtab
identity | public.testtab
acl      | {postgres=arwdDxtm/postgres,foo=r/postgres}
```

#### 9.27.6. Comentários sobre as funções de informação [#](#FUNCTIONS-INFO-COMMENT)

As funções mostradas na [Tabela 9.82](functions-info.md#FUNCTIONS-INFO-COMMENT-TABLE) extraem comentários que foram armazenados anteriormente com o comando [COMMENT](sql-comment.md). Um valor nulo é retornado se nenhum comentário puder ser encontrado para os parâmetros especificados.

**Tabela 9.82. Funções de Comentário**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      col_description
     </code>
     (
     <em class="parameter">
      <code>
       table
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       column
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Returns the comment for a table column, which is specified by the OID of its table and its column number. (
     <code>
      obj_description
     </code>
     cannot be used for table columns, since columns do not have OIDs of their own.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      obj_description
     </code>
     (
     <em class="parameter">
      <code>
       object
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       catalog
      </code>
     </em>
     <code>
      name
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Returns the comment for a database object specified by its OID and the name of the containing system catalog.  For example,
     <code>
      obj_description(123456, 'pg_class')
     </code>
     would retrieve the comment for the table with OID 123456.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      obj_description
     </code>
     (
     <em class="parameter">
      <code>
       object
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Returns the comment for a database object specified by its OID alone. This is
     <span class="emphasis">
      <em>
       deprecated
      </em>
     </span>
     since there is no guarantee that OIDs are unique across different system catalogs; therefore, the wrong comment might be returned.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      shobj_description
     </code>
     (
     <em class="parameter">
      <code>
       object
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       catalog
      </code>
     </em>
     <code>
      name
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Returns the comment for a shared database object specified by its OID and the name of the containing system catalog.  This is just like
     <code>
      obj_description
     </code>
     except that it is used for retrieving comments on shared objects (that is, databases, roles, and tablespaces).  Some system catalogs are global to all databases within each cluster, and the descriptions for objects in them are stored globally as well.
    </p>
   </td>
  </tr>
 </tbody>
</table>

#### 9.27.7. Funções de verificação da validade dos dados [#](#FUNCTIONS-INFO-VALIDITY)

As funções apresentadas na [Tabela 9.83](functions-info.md#FUNCTIONS-INFO-VALIDITY-TABLE) podem ser úteis para verificar a validade dos dados de entrada propostos.

**Tabela 9.83. Funções de verificação de validade de dados**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função
    </p>
    <p>
     Descrição
    </p>
    <p>
     Exemplo(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_input_is_valid
     </code>
     (
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       type
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Teste se o dado
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     é uma entrada válida para o tipo de dados especificado, retornando true ou false.
    </p>
    <p>
     Essa função só funcionará conforme o desejado se a função de entrada do tipo de dados tiver sido atualizada para relatar entrada inválida como
     <span class="quote">
      “
      <span class="quote">
       suave
      </span>
      ”
     </span>
     Caso contrário, a entrada inválida abortará a transação, assim como se a string tivesse sido convertida diretamente para o tipo.
    </p>
    <p>
     <code>
      pg_input_is_valid('42', 'integer')
     </code>
     →
     <code>
      t
     </code>
    </p>
    <p>
     <code>
      pg_input_is_valid('42000000000', 'integer')
     </code>
     →
     <code>
      f
     </code>
    </p>
    <p>
     <code>
      pg_input_is_valid('1234.567', 'numeric(7,4)')
     </code>
     →
     <code>
      f
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_input_error_info
     </code>
     (
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       type
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      record
     </code>
     (
     <em class="parameter">
      <code>
       message
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       detail
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       hint
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       sql_error_code
      </code>
     </em>
     <code>
      text
     </code>
     )
    </p>
    <p>
     Teste se o dado
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     é uma entrada válida para o tipo de dados especificado; se não for, retorne os detalhes do erro que teria sido lançado. Se a entrada for válida, os resultados são NULL. As entradas são as mesmas que para
     <code>
      pg_input_is_valid
     </code>
     .
    </p>
    <p>
     Essa função só funcionará conforme o desejado se a função de entrada do tipo de dados tiver sido atualizada para relatar entrada inválida como
     <span class="quote">
      “
      <span class="quote">
       suave
      </span>
      ”
     </span>
     Caso contrário, a entrada inválida abortará a transação, assim como se a string tivesse sido convertida diretamente para o tipo.
    </p>
    <p>
     <code>
      SELECT * FROM pg_input_error_info('42000000000', 'integer')
     </code>
     →
     <code>
     </code>
    </p>
    <pre class="programlisting">
                       message                        | detail | hint | sql_error_code ------------------------------------------------------+--------+------+---------------- value "42000000000" is out of range for type integer |        |      | 22003
</pre>
    <p>
    </p>
   </td>
  </tr>
 </tbody>
</table>

#### 9.27.8. Funções de ID de Transação e Informações de Escaneamento [#](#FUNCTIONS-INFO-SNAPSHOT)

As funções apresentadas na [Tabela 9.84](functions-info.md#FUNCTIONS-PG-SNAPSHOT) fornecem informações sobre transações do servidor em um formato exportable. O uso principal dessas funções é determinar quais transações foram realizadas entre dois instantâneos.

**Tabela 9.84. Funções de ID de Transação e Informações de Instantâneo**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      age
     </code>
     (
     <code>
      xid
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns the number of transactions between the supplied transaction id and the current transaction counter.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      mxid_age
     </code>
     (
     <code>
      xid
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns the number of multixacts IDs between the supplied multixact ID and the current multixacts counter.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_current_xact_id
     </code>
     () →
     <code>
      xid8
     </code>
    </p>
    <p>
     Returns the current transaction's ID.  It will assign a new one if the current transaction does not have one already (because it has not performed any database updates);  see
     <a class="xref" href="transaction-id.md" title="67.1. Transactions and Identifiers">
      Section 67.1
     </a>
     for details.  If executed in a subtransaction, this will return the top-level transaction ID; see
     <a class="xref" href="subxacts.md" title="67.3. Subtransactions">
      Section 67.3
     </a>
     for details.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_current_xact_id_if_assigned
     </code>
     () →
     <code>
      xid8
     </code>
    </p>
    <p>
     Returns the current transaction's ID, or
     <code>
      NULL
     </code>
     if no ID is assigned yet.  (It's best to use this variant if the transaction might otherwise be read-only, to avoid unnecessary consumption of an XID.) If executed in a subtransaction, this will return the top-level transaction ID.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_xact_status
     </code>
     (
     <code>
      xid8
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Reports the commit status of a recent transaction. The result is one of
     <code>
      in progress
     </code>
     ,
     <code>
      committed
     </code>
     , or
     <code>
      aborted
     </code>
     , provided that the transaction is recent enough that the system retains the commit status of that transaction. If it is old enough that no references to the transaction survive in the system and the commit status information has been discarded, the result is
     <code>
      NULL
     </code>
     . Applications might use this function, for example, to determine whether their transaction committed or aborted after the application and database server become disconnected while a
     <code>
      COMMIT
     </code>
     is in progress. Note that prepared transactions are reported as
     <code>
      in progress
     </code>
     ; applications must check
     <a class="link" href="view-pg-prepared-xacts.md" title="53.17. pg_prepared_xacts">
      <code>
       pg_prepared_xacts
      </code>
     </a>
     if they need to determine whether a transaction ID belongs to a prepared transaction.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_current_snapshot
     </code>
     () →
     <code>
      pg_snapshot
     </code>
    </p>
    <p>
     Returns a current
     <em class="firstterm">
      snapshot
     </em>
     , a data structure showing which transaction IDs are now in-progress. Only top-level transaction IDs are included in the snapshot; subtransaction IDs are not shown;  see
     <a class="xref" href="subxacts.md" title="67.3. Subtransactions">
      Section 67.3
     </a>
     for details.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_snapshot_xip
     </code>
     (
     <code>
      pg_snapshot
     </code>
     ) →
     <code>
      setof xid8
     </code>
    </p>
    <p>
     Returns the set of in-progress transaction IDs contained in a snapshot.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_snapshot_xmax
     </code>
     (
     <code>
      pg_snapshot
     </code>
     ) →
     <code>
      xid8
     </code>
    </p>
    <p>
     Returns the
     <code>
      xmax
     </code>
     of a snapshot.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_snapshot_xmin
     </code>
     (
     <code>
      pg_snapshot
     </code>
     ) →
     <code>
      xid8
     </code>
    </p>
    <p>
     Returns the
     <code>
      xmin
     </code>
     of a snapshot.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_visible_in_snapshot
     </code>
     (
     <code>
      xid8
     </code>
     ,
     <code>
      pg_snapshot
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Is the given transaction ID
     <em class="firstterm">
      visible
     </em>
     according to this snapshot (that is, was it completed before the snapshot was taken)?  Note that this function will not give the correct answer for a subtransaction ID (subxid);  see
     <a class="xref" href="subxacts.md" title="67.3. Subtransactions">
      Section 67.3
     </a>
     for details.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_multixact_members
     </code>
     (
     <em class="parameter">
      <code>
       multixid
      </code>
     </em>
     <code>
      xid
     </code>
     ) →
     <code>
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       xid
      </code>
     </em>
     <code>
      xid
     </code>
     ,
     <em class="parameter">
      <code>
       mode
      </code>
     </em>
     <code>
      text
     </code>
     )
    </p>
    <p>
     Returns the transaction ID and lock mode for each member of the specified multixact ID.  The lock modes
     <code>
      forupd
     </code>
     ,
     <code>
      fornokeyupd
     </code>
     ,
     <code>
      sh
     </code>
     , and
     <code>
      keysh
     </code>
     correspond to the row-level locks
     <code>
      FOR UPDATE
     </code>
     ,
     <code>
      FOR NO KEY UPDATE
     </code>
     ,
     <code>
      FOR SHARE
     </code>
     , and
     <code>
      FOR KEY SHARE
     </code>
     , respectively, as described in
     <a class="xref" href="explicit-locking.md#LOCKING-ROWS" title="13.3.2. Row-Level Locks">
      Section 13.3.2
     </a>
     .  Two additional modes are specific to multixacts:
     <code>
      nokeyupd
     </code>
     , used by updates that do not modify key columns, and
     <code>
      upd
     </code>
     , used by updates or deletes that modify key columns.
    </p>
   </td>
  </tr>
 </tbody>
</table>

O tipo de ID de transação interna `xid` é de 32 bits e volta ao início a cada 4 bilhões de transações. No entanto, as funções mostradas na [Tabela 9.84](functions-info.md#FUNCTIONS-PG-SNAPSHOT "Table 9.84. Transaction ID and Snapshot Information Functions"), exceto `age`, `mxid_age` e `pg_get_multixact_members`, utilizam um tipo de 64 bits `xid8` que não volta ao início durante a vida de uma instalação e pode ser convertido para `xid` por colagem, se necessário; consulte [Seção 67.1](transaction-id.md "67.1. Transactions and Identifiers") para detalhes. O tipo de dados `pg_snapshot` armazena informações sobre a visibilidade do ID de transação em um momento específico. Seus componentes são descritos na [Tabela 9.85](functions-info.md#FUNCTIONS-PG-SNAPSHOT-PARTS "Table 9.85. Snapshot Components"). A representação textual de `pg_snapshot` é `xmin:xmax:xip_list`. Por exemplo, `10:20:10,14,15` significa `xmin=10, xmax=20, xip_list=10, 14, 15`.

**Tabela 9.85. Componentes do Instantâneo**

<table>
 <thead>
  <tr>
   <th>
    Name
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     xmin
    </code>
   </td>
   <td>
    ID de transação mais baixo que ainda estava ativo. Todos os IDs de transação menores que
    <code>
     xmin
    </code>
    ou são comprometidos e visíveis, ou são recuados e mortos.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     xmax
    </code>
   </td>
   <td>
    Um acima do ID da transação mais alta concluída. Todos os IDs de transação maiores ou iguais a
    <code>
     xmax
    </code>
    não haviam sido concluídos até o momento do instantâneo, e, portanto, são invisíveis.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     xip_list
    </code>
   </td>
   <td>
    Transações em andamento no momento do instantâneo. Um ID de transação que é
    <code>
     xmin &lt;=
     <em class="replaceable">
      <code>
       X
      </code>
     </em>
     &lt; xmax
    </code>
    e que não estava nessa lista quando o instantâneo foi feito, e, portanto, é visível ou morta de acordo com seu status de compromisso. Esta lista não inclui os IDs de transação das subtransações (subxids).
   </td>
  </tr>
 </tbody>
</table>

Nas versões do PostgreSQL anteriores à 13, não havia o tipo `xid8`. Portanto, foram fornecidas variantes dessas funções que utilizavam `bigint` para representar um XID de 64 bits, com um tipo de dados de instantâneo correspondentemente distinto `txid_snapshot`. Essas funções mais antigas têm `txid` em seus nomes. Elas ainda são suportadas para compatibilidade reversa, mas podem ser removidas em uma versão futura. Veja [Tabela 9.86](functions-info.md#FUNCTIONS-TXID-SNAPSHOT).

**Tabela 9.86. Funções de ID de Transação e Informações de Escaneamento Desatualizadas**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      txid_current
     </code>
     () →
     <code>
      bigint
     </code>
    </p>
    <p>
     See
     <code>
      pg_current_xact_id()
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      txid_current_if_assigned
     </code>
     () →
     <code>
      bigint
     </code>
    </p>
    <p>
     See
     <code>
      pg_current_xact_id_if_assigned()
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      txid_current_snapshot
     </code>
     () →
     <code>
      txid_snapshot
     </code>
    </p>
    <p>
     See
     <code>
      pg_current_snapshot()
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      txid_snapshot_xip
     </code>
     (
     <code>
      txid_snapshot
     </code>
     ) →
     <code>
      setof bigint
     </code>
    </p>
    <p>
     See
     <code>
      pg_snapshot_xip()
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      txid_snapshot_xmax
     </code>
     (
     <code>
      txid_snapshot
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     See
     <code>
      pg_snapshot_xmax()
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      txid_snapshot_xmin
     </code>
     (
     <code>
      txid_snapshot
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     See
     <code>
      pg_snapshot_xmin()
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      txid_visible_in_snapshot
     </code>
     (
     <code>
      bigint
     </code>
     ,
     <code>
      txid_snapshot
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     See
     <code>
      pg_visible_in_snapshot()
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      txid_status
     </code>
     (
     <code>
      bigint
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     See
     <code>
      pg_xact_status()
     </code>
     .
    </p>
   </td>
  </tr>
 </tbody>
</table>

#### 9.27.9. Funções de Informações de Transações Comprometidas [#](#FUNCTIONS-INFO-COMMIT-TIMESTAMP)

As funções mostradas na [Tabela 9.87](functions-info.md#FUNCTIONS-COMMIT-TIMESTAMP) fornecem informações sobre quando as transações passadas foram realizadas. Elas fornecem dados úteis apenas quando a opção de configuração [track_commit_timestamp](runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP) é habilitada, e apenas para transações que foram realizadas após sua habilitação. As informações do timestamp de compromisso são removidas rotineiramente durante o vácuo.

**Tabela 9.87. Funções de Informações de Transação Comprometida**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_xact_commit_timestamp
     </code>
     (
     <code>
      xid
     </code>
     ) →
     <code>
      timestamp with time zone
     </code>
    </p>
    <p>
     Returns the commit timestamp of a transaction.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_xact_commit_timestamp_origin
     </code>
     (
     <code>
      xid
     </code>
     ) →
     <code>
      record
     </code>
     (
     <em class="parameter">
      <code>
       timestamp
      </code>
     </em>
     <code>
      timestamp with time zone
     </code>
     ,
     <em class="parameter">
      <code>
       roident
      </code>
     </em>
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Returns the commit timestamp and replication origin of a transaction.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_last_committed_xact
     </code>
     () →
     <code>
      record
     </code>
     (
     <em class="parameter">
      <code>
       xid
      </code>
     </em>
     <code>
      xid
     </code>
     ,
     <em class="parameter">
      <code>
       timestamp
      </code>
     </em>
     <code>
      timestamp with time zone
     </code>
     ,
     <em class="parameter">
      <code>
       roident
      </code>
     </em>
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Returns the transaction ID, commit timestamp and replication origin of the latest committed transaction.
    </p>
   </td>
  </tr>
 </tbody>
</table>

#### 9.27.10. Funções de Controle de Dados [#](#FUNCTIONS-INFO-CONTROLDATA)

As funções mostradas na [Tabela 9.88](functions-info.md#FUNCTIONS-CONTROLDATA) imprimem informações inicializadas durante `initdb`, como a versão do catálogo. Elas também mostram informações sobre o registro prévio de escrita e o processamento de pontos de verificação. Essas informações são válidas para todo o clúster, e não são específicas para nenhum banco de dados. Essas funções fornecem a maioria das mesmas informações, provenientes da mesma fonte, que o aplicativo [pg_controldata](app-pgcontroldata.md).

**Tabela 9.88. Funções de dados de controle**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_control_checkpoint
     </code>
     () →
     <code>
      record
     </code>
    </p>
    <p>
     Returns information about current checkpoint state, as shown in
     <a class="xref" href="functions-info.md#FUNCTIONS-PG-CONTROL-CHECKPOINT" title="Table 9.89. pg_control_checkpoint Output Columns">
      Table 9.89
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_control_system
     </code>
     () →
     <code>
      record
     </code>
    </p>
    <p>
     Returns information about current control file state, as shown in
     <a class="xref" href="functions-info.md#FUNCTIONS-PG-CONTROL-SYSTEM" title="Table 9.90. pg_control_system Output Columns">
      Table 9.90
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_control_init
     </code>
     () →
     <code>
      record
     </code>
    </p>
    <p>
     Returns information about cluster initialization state, as shown in
     <a class="xref" href="functions-info.md#FUNCTIONS-PG-CONTROL-INIT" title="Table 9.91. pg_control_init Output Columns">
      Table 9.91
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_control_recovery
     </code>
     () →
     <code>
      record
     </code>
    </p>
    <p>
     Returns information about recovery state, as shown in
     <a class="xref" href="functions-info.md#FUNCTIONS-PG-CONTROL-RECOVERY" title="Table 9.92. pg_control_recovery Output Columns">
      Table 9.92
     </a>
     .
    </p>
   </td>
  </tr>
 </tbody>
</table>

**Tabela 9.89. Colunas de saída `pg_control_checkpoint`**

<table>
 <thead>
  <tr>
   <th>
    Column Name
   </th>
   <th>
    Data Type
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     checkpoint_lsn
    </code>
   </td>
   <td>
    <code>
     pg_lsn
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     redo_lsn
    </code>
   </td>
   <td>
    <code>
     pg_lsn
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     redo_wal_file
    </code>
   </td>
   <td>
    <code>
     text
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     timeline_id
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     prev_timeline_id
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     full_page_writes
    </code>
   </td>
   <td>
    <code>
     boolean
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     next_xid
    </code>
   </td>
   <td>
    <code>
     text
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     next_oid
    </code>
   </td>
   <td>
    <code>
     oid
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     next_multixact_id
    </code>
   </td>
   <td>
    <code>
     xid
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     next_multi_offset
    </code>
   </td>
   <td>
    <code>
     xid
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     oldest_xid
    </code>
   </td>
   <td>
    <code>
     xid
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     oldest_xid_dbid
    </code>
   </td>
   <td>
    <code>
     oid
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     oldest_active_xid
    </code>
   </td>
   <td>
    <code>
     xid
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     oldest_multi_xid
    </code>
   </td>
   <td>
    <code>
     xid
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     oldest_multi_dbid
    </code>
   </td>
   <td>
    <code>
     oid
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     oldest_commit_ts_xid
    </code>
   </td>
   <td>
    <code>
     xid
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     newest_commit_ts_xid
    </code>
   </td>
   <td>
    <code>
     xid
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     checkpoint_time
    </code>
   </td>
   <td>
    <code>
     timestamp with time zone
    </code>
   </td>
  </tr>
 </tbody>
</table>

**Tabela 9.90. Colunas de Saída `pg_control_system`**

<table>
 <thead>
  <tr>
   <th>
    Column Name
   </th>
   <th>
    Data Type
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     pg_control_version
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     catalog_version_no
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     system_identifier
    </code>
   </td>
   <td>
    <code>
     bigint
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     pg_control_last_modified
    </code>
   </td>
   <td>
    <code>
     timestamp with time zone
    </code>
   </td>
  </tr>
 </tbody>
</table>

**Tabela 9.91. Colunas de Saída `pg_control_init`**

<table>
 <thead>
  <tr>
   <th>
    Column Name
   </th>
   <th>
    Data Type
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     max_data_alignment
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     database_block_size
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     blocks_per_segment
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     wal_block_size
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     bytes_per_wal_segment
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     max_identifier_length
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     max_index_columns
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     max_toast_chunk_size
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     large_object_chunk_size
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     float8_pass_by_value
    </code>
   </td>
   <td>
    <code>
     boolean
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     data_page_checksum_version
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     default_char_signedness
    </code>
   </td>
   <td>
    <code>
     boolean
    </code>
   </td>
  </tr>
 </tbody>
</table>

**Tabela 9.92. Colunas de Saída `pg_control_recovery`**

<table>
 <thead>
  <tr>
   <th>
    Column Name
   </th>
   <th>
    Data Type
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     min_recovery_end_lsn
    </code>
   </td>
   <td>
    <code>
     pg_lsn
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     min_recovery_end_timeline
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     backup_start_lsn
    </code>
   </td>
   <td>
    <code>
     pg_lsn
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     backup_end_lsn
    </code>
   </td>
   <td>
    <code>
     pg_lsn
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     end_of_backup_record_required
    </code>
   </td>
   <td>
    <code>
     boolean
    </code>
   </td>
  </tr>
 </tbody>
</table>

#### 9.27.11. Informações sobre a versão Funções [#](#FUNCTIONS-INFO-VERSION)

As funções mostradas na [Tabela 9.93](functions-info.md#FUNCTIONS-VERSION) imprimem informações da versão.

**Tabela 9.93. Informações sobre a versão das funções**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      version
     </code>
     () →
     <code>
      text
     </code>
    </p>
    <p>
     Returns a string describing the
     <span class="productname">
      PostgreSQL
     </span>
     server's version.  You can also get this information from
     <a class="xref" href="runtime-config-preset.md#GUC-SERVER-VERSION">
      server_version
     </a>
     , or for a machine-readable version use
     <a class="xref" href="runtime-config-preset.md#GUC-SERVER-VERSION-NUM">
      server_version_num
     </a>
     .  Software developers should use
     <code>
      server_version_num
     </code>
     (available since 8.2) or
     <a class="xref" href="libpq-status.md#LIBPQ-PQSERVERVERSION">
      <code>
       PQserverVersion
      </code>
     </a>
     instead of parsing the text version.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      unicode_version
     </code>
     () →
     <code>
      text
     </code>
    </p>
    <p>
     Returns a string representing the version of Unicode used by
     <span class="productname">
      PostgreSQL
     </span>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      icu_unicode_version
     </code>
     () →
     <code>
      text
     </code>
    </p>
    <p>
     Returns a string representing the version of Unicode used by ICU, if the server was built with ICU support; otherwise returns
     <code>
      NULL
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>

#### 9.27.12. Funções de Resumo de Informação WAL [#](#FUNCTIONS-INFO-WAL-SUMMARY)

As funções mostradas na [Tabela 9.94](functions-info.md#FUNCTIONS-WAL-SUMMARY) imprimem informações sobre o status da sumarização do WAL. Veja [summarize_wal](runtime-config-wal.md#GUC-SUMMARIZE-WAL).

**Tabela 9.94. Funções de informações de resumo do WAL**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_available_wal_summaries
     </code>
     () →
     <code>
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       tli
      </code>
     </em>
     <code>
      bigint
     </code>
     ,
     <em class="parameter">
      <code>
       start_lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ,
     <em class="parameter">
      <code>
       end_lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     )
    </p>
    <p>
     Returns information about the WAL summary files present in the data directory, under
     <code>
      pg_wal/summaries
     </code>
     . One row will be returned per WAL summary file. Each file summarizes WAL on the indicated TLI within the indicated LSN range. This function might be useful to determine whether enough WAL summaries are present on the server to take an incremental backup based on some prior backup whose start LSN is known.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_wal_summary_contents
     </code>
     (
     <em class="parameter">
      <code>
       tli
      </code>
     </em>
     <code>
      bigint
     </code>
     ,
     <em class="parameter">
      <code>
       start_lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ,
     <em class="parameter">
      <code>
       end_lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ) →
     <code>
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       relfilenode
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       reltablespace
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       reldatabase
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       relforknumber
      </code>
     </em>
     <code>
      smallint
     </code>
     ,
     <em class="parameter">
      <code>
       relblocknumber
      </code>
     </em>
     <code>
      bigint
     </code>
     ,
     <em class="parameter">
      <code>
       is_limit_block
      </code>
     </em>
     <code>
      boolean
     </code>
     )
    </p>
    <p>
     Returns one information about the contents of a single WAL summary file identified by TLI and starting and ending LSNs. Each row with
     <code>
      is_limit_block
     </code>
     false indicates that the block identified by the remaining output columns was modified by at least one WAL record within the range of records summarized by this file. Each row with
     <code>
      is_limit_block
     </code>
     true indicates either that (a) the relation fork was truncated to the length given by
     <code>
      relblocknumber
     </code>
     within the relevant range of WAL records or (b) that the relation fork was created or dropped within the relevant range of WAL records; in such cases,
     <code>
      relblocknumber
     </code>
     will be zero.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_wal_summarizer_state
     </code>
     () →
     <code>
      record
     </code>
     (
     <em class="parameter">
      <code>
       summarized_tli
      </code>
     </em>
     <code>
      bigint
     </code>
     ,
     <em class="parameter">
      <code>
       summarized_lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ,
     <em class="parameter">
      <code>
       pending_lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ,
     <em class="parameter">
      <code>
       summarizer_pid
      </code>
     </em>
     <code>
      int
     </code>
     )
    </p>
    <p>
     Returns information about the progress of the WAL summarizer. If the WAL summarizer has never run since the instance was started, then
     <code>
      summarized_tli
     </code>
     and
     <code>
      summarized_lsn
     </code>
     will be
     <code>
      0
     </code>
     and
     <code>
      0/0
     </code>
     respectively; otherwise, they will be the TLI and ending LSN of the last WAL summary file written to disk. If the WAL summarizer is currently running,
     <code>
      pending_lsn
     </code>
     will be the ending LSN of the last record that it has consumed, which must always be greater than or equal to
     <code>
      summarized_lsn
     </code>
     ; if the WAL summarizer is not running, it will be equal to
     <code>
      summarized_lsn
     </code>
     .
     <code>
      summarizer_pid
     </code>
     is the PID of the WAL summarizer process, if it is running, and otherwise NULL.
    </p>
    <p>
     As a special exception, the WAL summarizer will refuse to generate WAL summary files if run on WAL generated under
     <code>
      wal_level=minimal
     </code>
     , since such summaries would be unsafe to use as the basis for an incremental backup. In this case, the fields above will continue to advance as if summaries were being generated, but nothing will be written to disk. Once the summarizer reaches WAL generated while
     <code>
      wal_level
     </code>
     was set to
     <code>
      replica
     </code>
     or higher, it will resume writing summaries to disk.
    </p>
   </td>
  </tr>
 </tbody>
</table>
