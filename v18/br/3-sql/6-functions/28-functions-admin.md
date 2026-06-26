## 9.28. Funções de Administração do Sistema [#](#FUNCTIONS-ADMIN)

* [9.28.1. Funções de Configurações de Configuração](functions-admin.md#FUNCTIONS-ADMIN-SET)
* [9.28.2. Funções de Sinalização do Servidor](functions-admin.md#FUNCTIONS-ADMIN-SIGNAL)
* [9.28.3. Funções de Controle de Backup](functions-admin.md#FUNCTIONS-ADMIN-BACKUP)
* [9.28.4. Funções de Controle de Recuperação](functions-admin.md#FUNCTIONS-RECOVERY-CONTROL)
* [9.28.5. Funções de Sincronização de Instantâneo](functions-admin.md#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION)
* [9.28.6. Funções de Gerenciamento de Replicação](functions-admin.md#FUNCTIONS-REPLICATION)
* [9.28.7. Funções de Gerenciamento de Objeto de Banco de Dados](functions-admin.md#FUNCTIONS-ADMIN-DBOBJECT)
* [9.28.8. Funções de Manutenção de Índices](functions-admin.md#FUNCTIONS-ADMIN-INDEX)
* [9.28.9. Funções de Acesso Genérico a Arquivo](functions-admin.md#FUNCTIONS-ADMIN-GENFILE)
* [9.28.10. Funções de Fechamento Consultivo](functions-admin.md#FUNCTIONS-ADVISORY-LOCKS)

As funções descritas nesta seção são usadas para controlar e monitorar uma instalação do PostgreSQL.

### 9.28.1. Funções de Configurações de Configuração [#](#FUNCTIONS-ADMIN-SET)

[Tabela 9.95](functions-admin.md#FUNCTIONS-ADMIN-SET-TABLE) mostra as funções disponíveis para consultar e alterar parâmetros de configuração de tempo de execução.

**Tabela 9.95. Funções de Configurações de Configuração**



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
      current_setting
     </code>
     (
     <em class="parameter">
      <code>
       setting_name
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
        missing_ok
       </code>
      </em>
      <code>
       boolean
      </code>
     </span>
     ] )
     <code>
      text
     </code>
    </p>
    <p>
     Retorna o valor atual do ajuste
     <em class="parameter">
      <code>
       setting_name
      </code>
     </em>
     Se não houver essa configuração,
     <code>
      current_setting
     </code>
     lança um erro, a menos que
     <em class="parameter">
      <code>
       missing_ok
      </code>
     </em>
     é fornecida e é
     <code>
      true
     </code>
     (nesse caso, NULL é retornado). Esta função corresponde à
     <acronym class="acronym">
      SQL
     </acronym>
     comando
     <a class="xref" href="sql-show.md" title="SHOW">
      <span class="refentrytitle">
       MOSTRE
      </span>
     </a>
     .
    </p>
    <p>
     <code>
      current_setting('datestyle')
     </code>
     →
     <code>
      ISO, MDY
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      set_config
     </code>
     (
     <em class="parameter">
      <code>
       setting_name
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       new_value
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       is_local
      </code>
     </em>
     <code>
      boolean
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Define o parâmetro
     <em class="parameter">
      <code>
       setting_name
      </code>
     </em>
     para
     <em class="parameter">
      <code>
       new_value
      </code>
     </em>
     , e retorna esse valor. Se
     <em class="parameter">
      <code>
       is_local
      </code>
     </em>
     é
     <code>
      true
     </code>
     , o novo valor só será aplicado durante a transação atual. Se você deseja que o novo valor seja aplicado para o resto da sessão atual, use
     <code>
      false
     </code>
     em vez disso. Essa função corresponde ao comando SQL
     <a class="xref" href="sql-set.md" title="SET">
      <span class="refentrytitle">
       SET
      </span>
     </a>
     .
    </p>
    <p>
     <code>
      set_config
     </code>
     aceita o valor NULL para
     <em class="parameter">
      <code>
       new_value
      </code>
     </em>
     , mas como as configurações não podem ser nulos, é interpretado como um pedido para redefinir a configuração para seu valor padrão.
    </p>
    <p>
     <code>
      set_config('log_statement_stats', 'off', false)
     </code>
     →
     <code>
      off
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 9.28.2. Funções de Sinalização do Servidor [#](#FUNCTIONS-ADMIN-SIGNAL)

As funções exibidas na [Tabela 9.96](functions-admin.md#FUNCTIONS-ADMIN-SIGNAL-TABLE) enviam sinais de controle para outros processos do servidor. O uso dessas funções é restrito por padrão a superusuários, mas o acesso pode ser concedido a outros usuários usando `GRANT`, com exceções indicadas.

Cada uma dessas funções retorna `true` se o sinal for enviado com sucesso e `false` se o envio do sinal falhou.

**Tabela 9.96. Funções de sinalização do servidor**



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
      pg_cancel_backend
     </code>
     (
     <em class="parameter">
      <code>
       pid
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Cancels the current query of the session whose backend process has the specified process ID.  This is also allowed if the calling role is a member of the role whose backend is being canceled or the calling role has privileges of
     <code>
      pg_signal_backend
     </code>
     , however only superusers can cancel superuser backends. As an exception, roles with privileges of
     <code>
      pg_signal_autovacuum_worker
     </code>
     are permitted to cancel autovacuum worker processes, which are otherwise considered superuser backends.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_log_backend_memory_contexts
     </code>
     (
     <em class="parameter">
      <code>
       pid
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Requests to log the memory contexts of the backend with the specified process ID.  This function can send the request to backends and auxiliary processes except logger.  These memory contexts will be logged at
     <code>
      LOG
     </code>
     message level. They will appear in the server log based on the log configuration set (see
     <a class="xref" href="runtime-config-logging.md" title="19.8. Error Reporting and Logging">
      Section 19.8
     </a>
     for more information), but will not be sent to the client regardless of
     <a class="xref" href="runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES">
      client_min_messages
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_reload_conf
     </code>
     () →
     <code>
      boolean
     </code>
    </p>
    <p>
     Causes all processes of the
     <span class="productname">
      PostgreSQL
     </span>
     server to reload their configuration files.  (This is initiated by sending a
     <span class="systemitem">
      SIGHUP
     </span>
     signal to the postmaster process, which in turn sends
     <span class="systemitem">
      SIGHUP
     </span>
     to each of its children.) You can use the
     <a class="link" href="view-pg-file-settings.md" title="53.8. pg_file_settings">
      <code>
       pg_file_settings
      </code>
     </a>
     ,
     <a class="link" href="view-pg-hba-file-rules.md" title="53.10. pg_hba_file_rules">
      <code>
       pg_hba_file_rules
      </code>
     </a>
     and
     <a class="link" href="view-pg-ident-file-mappings.md" title="53.11. pg_ident_file_mappings">
      <code>
       pg_ident_file_mappings
      </code>
     </a>
     views to check the configuration files for possible errors, before reloading.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_rotate_logfile
     </code>
     () →
     <code>
      boolean
     </code>
    </p>
    <p>
     Signals the log-file manager to switch to a new output file immediately.  This works only when the built-in log collector is running, since otherwise there is no log-file manager subprocess.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_terminate_backend
     </code>
     (
     <em class="parameter">
      <code>
       pid
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       timeout
      </code>
     </em>
     <code>
      bigint
     </code>
     <code>
      DEFAULT
     </code>
     <code>
      0
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Terminates the session whose backend process has the specified process ID.  This is also allowed if the calling role is a member of the role whose backend is being terminated or the calling role has privileges of
     <code>
      pg_signal_backend
     </code>
     , however only superusers can terminate superuser backends. As an exception, roles with privileges of
     <code>
      pg_signal_autovacuum_worker
     </code>
     are permitted to terminate autovacuum worker processes, which are otherwise considered superuser backends.
    </p>
    <p>
     If
     <em class="parameter">
      <code>
       timeout
      </code>
     </em>
     is not specified or zero, this function returns
     <code>
      true
     </code>
     whether the process actually terminates or not, indicating only that the sending of the signal was successful.  If the
     <em class="parameter">
      <code>
       timeout
      </code>
     </em>
     is specified (in milliseconds) and greater than zero, the function waits until the process is actually terminated or until the given time has passed. If the process is terminated, the function returns
     <code>
      true
     </code>
     .  On timeout, a warning is emitted and
     <code>
      false
     </code>
     is returned.
    </p>
   </td>
  </tr>
 </tbody>
</table>










`pg_cancel_backend` e `pg_terminate_backend` enviam sinais (SIGINT ou SIGTERM, respectivamente) para os processos de nível de profundidade identificados pelo ID de processo. O ID de processo de um backend ativo pode ser encontrado na coluna `pid` da visualização `pg_stat_activity`, ou listando os processos `postgres` no servidor (usando o comando ps no Unix ou o Gerenciador de Tarefas no Windows). O papel de um backend ativo pode ser encontrado na coluna `usename` da visualização `pg_stat_activity`.

`pg_log_backend_memory_contexts` pode ser usado para registrar os contextos de memória de um processo de backend. Por exemplo:

```
postgres=# SELECT pg_log_backend_memory_contexts(pg_backend_pid());
 pg_log_backend_memory_contexts
--------------------------------
 t
(1 row)
```

Uma mensagem para cada contexto de memória será registrada. Por exemplo:

```
LOG:  logging memory contexts of PID 10377
STATEMENT:  SELECT pg_log_backend_memory_contexts(pg_backend_pid());
LOG:  level: 1; TopMemoryContext: 80800 total in 6 blocks; 14432 free (5 chunks); 66368 used
LOG:  level: 2; pgstat TabStatusArray lookup hash table: 8192 total in 1 blocks; 1408 free (0 chunks); 6784 used
LOG:  level: 2; TopTransactionContext: 8192 total in 1 blocks; 7720 free (1 chunks); 472 used
LOG:  level: 2; RowDescriptionContext: 8192 total in 1 blocks; 6880 free (0 chunks); 1312 used
LOG:  level: 2; MessageContext: 16384 total in 2 blocks; 5152 free (0 chunks); 11232 used
LOG:  level: 2; Operator class cache: 8192 total in 1 blocks; 512 free (0 chunks); 7680 used
LOG:  level: 2; smgr relation table: 16384 total in 2 blocks; 4544 free (3 chunks); 11840 used
LOG:  level: 2; TransactionAbortContext: 32768 total in 1 blocks; 32504 free (0 chunks); 264 used
...
LOG:  level: 2; ErrorContext: 8192 total in 1 blocks; 7928 free (3 chunks); 264 used
LOG:  Grand total: 1651920 bytes in 201 blocks; 622360 free (88 chunks); 1029560 used
```

Se houver mais de 100 contextos de criança sob o mesmo pai, os primeiros 100 contextos de criança são registrados, juntamente com um resumo dos contextos restantes. Observe que chamadas frequentes a essa função podem gerar um custo significativo, pois podem gerar um grande número de mensagens de registro.

### 9.28.3. Funções de controle de backup [#](#FUNCTIONS-ADMIN-BACKUP)

As funções apresentadas na [Tabela 9.97](functions-admin.md#FUNCTIONS-ADMIN-BACKUP-TABLE) auxiliam na realização de backups on-line. Essas funções não podem ser executadas durante a recuperação (exceto `pg_backup_start`, `pg_backup_stop` e `pg_wal_lsn_diff`).

Para obter detalhes sobre o uso adequado dessas funções, consulte [Seção 25.3](continuous-archiving.md)").

**Tabela 9.97. Funções de controle de backup**



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
      pg_create_restore_point
     </code>
     (
     <em class="parameter">
      <code>
       name
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     Creates a named marker record in the write-ahead log that can later be used as a recovery target, and returns the corresponding write-ahead log location.  The given name can then be used with
     <a class="xref" href="runtime-config-wal.md#GUC-RECOVERY-TARGET-NAME">
      recovery_target_name
     </a>
     to specify the point up to which recovery will proceed.  Avoid creating multiple restore points with the same name, since recovery will stop at the first one whose name matches the recovery target.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_current_wal_flush_lsn
     </code>
     () →
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     Returns the current write-ahead log flush location (see notes below).
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_current_wal_insert_lsn
     </code>
     () →
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     Returns the current write-ahead log insert location (see notes below).
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_current_wal_lsn
     </code>
     () →
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     Returns the current write-ahead log write location (see notes below).
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_backup_start
     </code>
     (
     <em class="parameter">
      <code>
       label
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
        fast
       </code>
      </em>
      <code>
       boolean
      </code>
     </span>
     ] ) →
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     Prepares the server to begin an on-line backup.  The only required parameter is an arbitrary user-defined label for the backup. (Typically this would be the name under which the backup dump file will be stored.) If the optional second parameter is given as
     <code>
      true
     </code>
     , it specifies executing
     <code>
      pg_backup_start
     </code>
     as quickly as possible.  This forces an immediate checkpoint which will cause a spike in I/O operations, slowing any concurrently executing queries.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_backup_stop
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        wait_for_archive
       </code>
      </em>
      <code>
       boolean
      </code>
     </span>
     ] ) →
     <code>
      record
     </code>
     (
     <em class="parameter">
      <code>
       lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ,
     <em class="parameter">
      <code>
       labelfile
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       spcmapfile
      </code>
     </em>
     <code>
      text
     </code>
     )
    </p>
    <p>
     Finishes performing an on-line backup.  The desired contents of the backup label file and the tablespace map file are returned as part of the result of the function and must be written to files in the backup area.  These files must not be written to the live data directory (doing so will cause PostgreSQL to fail to restart in the event of a crash).
    </p>
    <p>
     There is an optional parameter of type
     <code>
      boolean
     </code>
     . If false, the function will return immediately after the backup is completed, without waiting for WAL to be archived.  This behavior is only useful with backup software that independently monitors WAL archiving.  Otherwise, WAL required to make the backup consistent might be missing and make the backup useless.  By default or when this parameter is true,
     <code>
      pg_backup_stop
     </code>
     will wait for WAL to be archived when archiving is enabled.  (On a standby, this means that it will wait only when
     <code>
      archive_mode
     </code>
     =
     <code>
      always
     </code>
     .  If write activity on the primary is low, it may be useful to run
     <code>
      pg_switch_wal
     </code>
     on the primary in order to trigger an immediate segment switch.)
    </p>
    <p>
     When executed on a primary, this function also creates a backup history file in the write-ahead log archive area.  The history file includes the label given to
     <code>
      pg_backup_start
     </code>
     , the starting and ending write-ahead log locations for the backup, and the starting and ending times of the backup.  After recording the ending location, the current write-ahead log insertion point is automatically advanced to the next write-ahead log file, so that the ending write-ahead log file can be archived immediately to complete the backup.
    </p>
    <p>
     The result of the function is a single record. The
     <em class="parameter">
      <code>
       lsn
      </code>
     </em>
     column holds the backup's ending write-ahead log location (which again can be ignored).  The second column returns the contents of the backup label file, and the third column returns the contents of the tablespace map file.  These must be stored as part of the backup and are required as part of the restore process.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_switch_wal
     </code>
     () →
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     Forces the server to switch to a new write-ahead log file, which allows the current file to be archived (assuming you are using continuous archiving).  The result is the ending write-ahead log location plus 1 within the just-completed write-ahead log file.  If there has been no write-ahead log activity since the last write-ahead log switch,
     <code>
      pg_switch_wal
     </code>
     does nothing and returns the start location of the write-ahead log file currently in use.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_walfile_name
     </code>
     (
     <em class="parameter">
      <code>
       lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Converts a write-ahead log location to the name of the WAL file holding that location.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_walfile_name_offset
     </code>
     (
     <em class="parameter">
      <code>
       lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ) →
     <code>
      record
     </code>
     (
     <em class="parameter">
      <code>
       file_name
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       file_offset
      </code>
     </em>
     <code>
      integer
     </code>
     )
    </p>
    <p>
     Converts a write-ahead log location to a WAL file name and byte offset within that file.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_split_walfile_name
     </code>
     (
     <em class="parameter">
      <code>
       file_name
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
       segment_number
      </code>
     </em>
     <code>
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       timeline_id
      </code>
     </em>
     <code>
      bigint
     </code>
     )
    </p>
    <p>
     Extracts the sequence number and timeline ID from a WAL file name.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_wal_lsn_diff
     </code>
     (
     <em class="parameter">
      <code>
       lsn1
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ,
     <em class="parameter">
      <code>
       lsn2
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ) →
     <code>
      numeric
     </code>
    </p>
    <p>
     Calculates the difference in bytes (
     <em class="parameter">
      <code>
       lsn1
      </code>
     </em>
     -
     <em class="parameter">
      <code>
       lsn2
      </code>
     </em>
     ) between two write-ahead log locations.  This can be used with
     <code>
      pg_stat_replication
     </code>
     or some of the functions shown in
     <a class="xref" href="functions-admin.md#FUNCTIONS-ADMIN-BACKUP-TABLE" title="Table 9.97. Backup Control Functions">
      Table 9.97
     </a>
     to get the replication lag.
    </p>
   </td>
  </tr>
 </tbody>
</table>










`pg_current_wal_lsn` exibe a localização atual do log de pré-escrita no mesmo formato utilizado pelas funções acima. Da mesma forma, `pg_current_wal_insert_lsn` exibe a localização atual de inserção do log de pré-escrita e `pg_current_wal_flush_lsn` exibe a localização atual de esvaziamento do log de pré-escrita. A localização de inserção é o "lógico" final do log de pré-escrita em qualquer instante, enquanto a localização de escrita é o final do que foi efetivamente escrito dos buffers internos do servidor, e a localização de esvaziamento é a última localização conhecida que foi escrita em armazenamento durável. A localização de escrita é o final do que pode ser examinado de fora do servidor, e geralmente é o que você deseja se estiver interessado em arquivar arquivos de log de pré-escrita parcialmente completos. As localizações de inserção e esvaziamento são disponibilizadas principalmente para fins de depuração do servidor. Essas são todas operações somente de leitura e não requerem permissões de superusuário.

Você pode usar `pg_walfile_name_offset` para extrair o nome do arquivo de registro de pré-escrita correspondente e o deslocamento de byte de um valor `pg_lsn`. Por exemplo:

```
postgres=# SELECT * FROM pg_walfile_name_offset((pg_backup_stop()).lsn);
        file_name         | file_offset
--------------------------+-------------
 00000001000000000000000D |     4039624
(1 row)
```

Da mesma forma, `pg_walfile_name` extrai apenas o nome do arquivo de registro de pré-escrita.

`pg_split_walfile_name` é útil para calcular um LSN a partir de um deslocamento de arquivo e do nome do arquivo WAL, por exemplo:

```
postgres=# \set file_name '000000010000000100C000AB'
postgres=# \set offset 256
postgres=# SELECT '0/0'::pg_lsn + pd.segment_number * ps.setting::int + :offset AS lsn
  FROM pg_split_walfile_name(:'file_name') pd,
       pg_show_all_settings() ps
  WHERE ps.name = 'wal_segment_size';
      lsn
---------------
 C001/AB000100
(1 row)
```

### 9.28.4. Funções de Controle de Recuperação [#](#FUNCTIONS-RECOVERY-CONTROL)

As funções apresentadas na [Tabela 9.98](functions-admin.md#FUNCTIONS-RECOVERY-INFO-TABLE) fornecem informações sobre o estado atual de um servidor de espera. Essas funções podem ser executadas tanto durante a recuperação quanto no funcionamento normal.

**Tabela 9.98. Funções de Recuperação de Informações**



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
      pg_is_in_recovery
     </code>
     () →
     <code>
      boolean
     </code>
    </p>
    <p>
     Returns true if recovery is still in progress.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_last_wal_receive_lsn
     </code>
     () →
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     Returns the last write-ahead log location that has been received and synced to disk by streaming replication. While streaming replication is in progress this will increase monotonically. If recovery has completed then this will remain static at the location of the last WAL record received and synced to disk during recovery. If streaming replication is disabled, or if it has not yet started, the function returns
     <code>
      NULL
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_last_wal_replay_lsn
     </code>
     () →
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     Returns the last write-ahead log location that has been replayed during recovery.  If recovery is still in progress this will increase monotonically.  If recovery has completed then this will remain static at the location of the last WAL record applied during recovery. When the server has been started normally without recovery, the function returns
     <code>
      NULL
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_last_xact_replay_timestamp
     </code>
     () →
     <code>
      timestamp with time zone
     </code>
    </p>
    <p>
     Returns the time stamp of the last transaction replayed during recovery.  This is the time at which the commit or abort WAL record for that transaction was generated on the primary.  If no transactions have been replayed during recovery, the function returns
     <code>
      NULL
     </code>
     .  Otherwise, if recovery is still in progress this will increase monotonically.  If recovery has completed then this will remain static at the time of the last transaction applied during recovery.  When the server has been started normally without recovery, the function returns
     <code>
      NULL
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_wal_resource_managers
     </code>
     () →
     <code>
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       rm_id
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       rm_name
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       rm_builtin
      </code>
     </em>
     <code>
      boolean
     </code>
     )
    </p>
    <p>
     Returns the currently-loaded WAL resource managers in the system. The column
     <em class="parameter">
      <code>
       rm_builtin
      </code>
     </em>
     indicates whether it's a built-in resource manager, or a custom resource manager loaded by an extension.
    </p>
   </td>
  </tr>
 </tbody>
</table>










As funções mostradas na [Tabela 9.99](functions-admin.md#FUNCTIONS-RECOVERY-CONTROL-TABLE) controlam o progresso da recuperação. Essas funções podem ser executadas apenas durante a recuperação.

**Tabela 9.99. Funções de Controle de Recuperação**



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
      pg_is_wal_replay_paused
     </code>
     () →
     <code>
      boolean
     </code>
    </p>
    <p>
     Returns true if recovery pause is requested.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_get_wal_replay_pause_state
     </code>
     () →
     <code>
      text
     </code>
    </p>
    <p>
     Returns recovery pause state.  The return values are
     <code>
      not paused
     </code>
     if pause is not requested,
     <code>
      pause requested
     </code>
     if pause is requested but recovery is not yet paused, and
     <code>
      paused
     </code>
     if the recovery is actually paused.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_promote
     </code>
     (
     <em class="parameter">
      <code>
       wait
      </code>
     </em>
     <code>
      boolean
     </code>
     <code>
      DEFAULT
     </code>
     <code>
      true
     </code>
     ,
     <em class="parameter">
      <code>
       wait_seconds
      </code>
     </em>
     <code>
      integer
     </code>
     <code>
      DEFAULT
     </code>
     <code>
      60
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Promotes a standby server to primary status. With
     <em class="parameter">
      <code>
       wait
      </code>
     </em>
     set to
     <code>
      true
     </code>
     (the default), the function waits until promotion is completed or
     <em class="parameter">
      <code>
       wait_seconds
      </code>
     </em>
     seconds have passed, and returns
     <code>
      true
     </code>
     if promotion is successful and
     <code>
      false
     </code>
     otherwise. If
     <em class="parameter">
      <code>
       wait
      </code>
     </em>
     is set to
     <code>
      false
     </code>
     , the function returns
     <code>
      true
     </code>
     immediately after sending a
     <code>
      SIGUSR1
     </code>
     signal to the postmaster to trigger promotion.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_wal_replay_pause
     </code>
     () →
     <code>
      void
     </code>
    </p>
    <p>
     Request to pause recovery.  A request doesn't mean that recovery stops right away.  If you want a guarantee that recovery is actually paused, you need to check for the recovery pause state returned by
     <code>
      pg_get_wal_replay_pause_state()
     </code>
     .  Note that
     <code>
      pg_is_wal_replay_paused()
     </code>
     returns whether a request is made.  While recovery is paused, no further database changes are applied. If hot standby is active, all new queries will see the same consistent snapshot of the database, and no further query conflicts will be generated until recovery is resumed.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_wal_replay_resume
     </code>
     () →
     <code>
      void
     </code>
    </p>
    <p>
     Restarts recovery if it was paused.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
 </tbody>
</table>










`pg_wal_replay_pause` e `pg_wal_replay_resume` não podem ser executados enquanto uma promoção está em andamento. Se uma promoção for acionada enquanto a recuperação está em pausa, o estado de pausa termina e a promoção continua.

Se a replicação em streaming estiver desativada, o estado pausado pode continuar indefinidamente sem problemas. Se a replicação em streaming estiver em andamento, os registros WAL continuarão a ser recebidos, o que acabará por preencher o espaço em disco disponível, dependendo da duração da pausa, da taxa de geração de WAL e do espaço em disco disponível.

### 9.28.5. Funções de sincronização de instantâneo [#](#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION)

O PostgreSQL permite que as sessões do banco de dados sincronizem seus snapshots. Um *snapshot* determina quais dados são visíveis para a transação que está usando o snapshot. Snapshots sincronizados são necessários quando duas ou mais sessões precisam ver conteúdo idêntico no banco de dados. Se duas sessões começam suas transações independentemente, sempre há a possibilidade de que alguma terceira transação seja confirmada entre as execuções dos dois comandos `START TRANSACTION`, de modo que uma sessão veja os efeitos dessa transação e a outra

Para resolver esse problema, o PostgreSQL permite que uma transação *exporte* o instantâneo que está usando. Desde que a transação de exportação permaneça aberta, outras transações podem *importar* seu instantâneo, garantindo assim que elas vejam exatamente a mesma visão do banco de dados que a primeira transação vê. Mas observe que quaisquer alterações no banco de dados feitas por uma dessas transações permanecem invisíveis para as outras transações, como é comum em alterações feitas por transações não comprometidas. Portanto, as transações são sincronizadas em relação aos dados pré-existentes, mas atuam normalmente para as alterações que elas mesmas fazem.

Os instantâneos são exportados com a função `pg_export_snapshot`, mostrada na [Tabela 9.100](functions-admin.md#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION-TABLE "Table 9.100. Snapshot Synchronization Functions"), e importados com o comando [SET TRANSACTION](sql-set-transaction.md "SET TRANSACTION").

**Tabela 9.100. Funções de sincronização de instantâneo**



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
      pg_export_snapshot
     </code>
     ()
     <code>
      text
     </code>
    </p>
    <p>
     Salva o instantâneo atual da transação e retorna um
     <code>
      text
     </code>
     string que identifica o instantâneo. Essa string deve ser passada (fora do banco de dados) para clientes que desejam importar o instantâneo. O instantâneo está disponível para importação apenas até o final da transação que o exportou.
    </p>
    <p>
     Uma transação pode exportar mais de um instantâneo, se necessário. Observe que essa ação só é útil em
     <code>
      READ COMMITTED
     </code>
     transações, já que em
     <code>
      REPEATABLE READ
     </code>
     e níveis de isolamento mais altos, as transações utilizam o mesmo instantâneo ao longo de sua vida útil. Uma vez que uma transação tenha exportado quaisquer instantâneos, ela não pode ser preparada com
     <a class="xref" href="sql-prepare-transaction.md" title="PREPARE TRANSACTION">
      <span class="refentrytitle">
       PREPARE TRANSAÇÃO
      </span>
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_log_standby_snapshot
     </code>
     ()
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     Faça um instantâneo das transações em execução e escreva-o no WAL, sem precisar esperar pelo bgwriter ou checkpointer para registrar uma. Isso é útil para a decodificação lógica em standby, pois a criação de slot lógico precisa esperar até que tal registro seja reinterpretado no standby.
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 9.28.6. Funções de Gerenciamento de Replicação [#](#FUNCTIONS-REPLICATION)

As funções apresentadas na [Tabela 9.101](functions-admin.md#FUNCTIONS-REPLICATION-TABLE) são para controlar e interagir com recursos de replicação. Consulte [Seção 26.2.5](warm-standby.md#STREAMING-REPLICATION), [Seção 26.2.6](warm-standby.md#STREAMING-REPLICATION-SLOTS) e [Capítulo 48](replication-origins.md) para informações sobre os recursos subjacentes. O uso de funções para origem de replicação é permitido apenas pelo superusuário por padrão, mas pode ser permitido a outros usuários usando o comando `GRANT`. O uso de funções para faixas de replicação é restrito a superusuários e usuários com privilégio `REPLICATION`.

Muitas dessas funções têm comandos equivalentes no protocolo de replicação; veja [Seção 54.4](protocol-replication.md).

As funções descritas em [Seção 9.28.3](functions-admin.md#FUNCTIONS-ADMIN-BACKUP), [Seção 9.28.4](functions-admin.md#FUNCTIONS-RECOVERY-CONTROL) e [Seção 9.28.5](functions-admin.md#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION) também são relevantes para a replicação.

**Tabela 9.101. Funções de Gerenciamento de Replicação**



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
      pg_create_physical_replication_slot
     </code>
     (
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     <code>
      name
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        immediately_reserve
       </code>
      </em>
      <code>
       boolean
      </code>
      ,
      <em class="parameter">
       <code>
        temporary
       </code>
      </em>
      <code>
       boolean
      </code>
     </span>
     ] ) →
     <code>
      record
     </code>
     (
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     <code>
      name
     </code>
     ,
     <em class="parameter">
      <code>
       lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     )
    </p>
    <p>
     Creates a new physical replication slot named
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     . The optional second parameter, when
     <code>
      true
     </code>
     , specifies that the
     <acronym class="acronym">
      LSN
     </acronym>
     for this replication slot be reserved immediately; otherwise the
     <acronym class="acronym">
      LSN
     </acronym>
     is reserved on first connection from a streaming replication client. Streaming changes from a physical slot is only possible with the streaming-replication protocol — see
     <a class="xref" href="protocol-replication.md" title="54.4. Streaming Replication Protocol">
      Section 54.4
     </a>
     . The optional third parameter,
     <em class="parameter">
      <code>
       temporary
      </code>
     </em>
     , when set to true, specifies that the slot should not be permanently stored to disk and is only meant for use by the current session. Temporary slots are also released upon any error. This function corresponds to the replication protocol command
     <code>
      CREATE_REPLICATION_SLOT ... PHYSICAL
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_drop_replication_slot
     </code>
     (
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     <code>
      name
     </code>
     ) →
     <code>
      void
     </code>
    </p>
    <p>
     Drops the physical or logical replication slot named
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     . Same as replication protocol command
     <code>
      DROP_REPLICATION_SLOT
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-CREATE-LOGICAL-REPLICATION-SLOT">
    <p class="func_signature">
     <code>
      pg_create_logical_replication_slot
     </code>
     (
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     <code>
      name
     </code>
     ,
     <em class="parameter">
      <code>
       plugin
      </code>
     </em>
     <code>
      name
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        temporary
       </code>
      </em>
      <code>
       boolean
      </code>
      ,
      <em class="parameter">
       <code>
        twophase
       </code>
      </em>
      <code>
       boolean
      </code>
      ,
      <em class="parameter">
       <code>
        failover
       </code>
      </em>
      <code>
       boolean
      </code>
     </span>
     ] ) →
     <code>
      record
     </code>
     (
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     <code>
      name
     </code>
     ,
     <em class="parameter">
      <code>
       lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     )
    </p>
    <p>
     Creates a new logical (decoding) replication slot named
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     using the output plugin
     <em class="parameter">
      <code>
       plugin
      </code>
     </em>
     . The optional third parameter,
     <em class="parameter">
      <code>
       temporary
      </code>
     </em>
     , when set to true, specifies that the slot should not be permanently stored to disk and is only meant for use by the current session. Temporary slots are also released upon any error. The optional fourth parameter,
     <em class="parameter">
      <code>
       twophase
      </code>
     </em>
     , when set to true, specifies that the decoding of prepared transactions is enabled for this slot. The optional fifth parameter,
     <em class="parameter">
      <code>
       failover
      </code>
     </em>
     , when set to true, specifies that this slot is enabled to be synced to the standbys so that logical replication can be resumed after failover. A call to this function has the same effect as the replication protocol command
     <code>
      CREATE_REPLICATION_SLOT ... LOGICAL
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_copy_physical_replication_slot
     </code>
     (
     <em class="parameter">
      <code>
       src_slot_name
      </code>
     </em>
     <code>
      name
     </code>
     ,
     <em class="parameter">
      <code>
       dst_slot_name
      </code>
     </em>
     <code>
      name
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        temporary
       </code>
      </em>
      <code>
       boolean
      </code>
     </span>
     ] ) →
     <code>
      record
     </code>
     (
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     <code>
      name
     </code>
     ,
     <em class="parameter">
      <code>
       lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     )
    </p>
    <p>
     Copies an existing physical replication slot named
     <em class="parameter">
      <code>
       src_slot_name
      </code>
     </em>
     to a physical replication slot named
     <em class="parameter">
      <code>
       dst_slot_name
      </code>
     </em>
     . The copied physical slot starts to reserve WAL from the same
     <acronym class="acronym">
      LSN
     </acronym>
     as the source slot.
     <em class="parameter">
      <code>
       temporary
      </code>
     </em>
     is optional. If
     <em class="parameter">
      <code>
       temporary
      </code>
     </em>
     is omitted, the same value as the source slot is used. Copy of an invalidated slot is not allowed.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_copy_logical_replication_slot
     </code>
     (
     <em class="parameter">
      <code>
       src_slot_name
      </code>
     </em>
     <code>
      name
     </code>
     ,
     <em class="parameter">
      <code>
       dst_slot_name
      </code>
     </em>
     <code>
      name
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        temporary
       </code>
      </em>
      <code>
       boolean
      </code>
      [
      <span class="optional">
       ,
       <em class="parameter">
        <code>
         plugin
        </code>
       </em>
       <code>
        name
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code>
      record
     </code>
     (
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     <code>
      name
     </code>
     ,
     <em class="parameter">
      <code>
       lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     )
    </p>
    <p>
     Copies an existing logical replication slot named
     <em class="parameter">
      <code>
       src_slot_name
      </code>
     </em>
     to a logical replication slot named
     <em class="parameter">
      <code>
       dst_slot_name
      </code>
     </em>
     , optionally changing the output plugin and persistence.  The copied logical slot starts from the same
     <acronym class="acronym">
      LSN
     </acronym>
     as the source logical slot.  Both
     <em class="parameter">
      <code>
       temporary
      </code>
     </em>
     and
     <em class="parameter">
      <code>
       plugin
      </code>
     </em>
     are optional; if they are omitted, the values of the source slot are used. The
     <code>
      failover
     </code>
     option of the source logical slot is not copied and is set to
     <code>
      false
     </code>
     by default. This is to avoid the risk of being unable to continue logical replication after failover to standby where the slot is being synchronized. Copy of an invalidated slot is not allowed.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-LOGICAL-SLOT-GET-CHANGES">
    <p class="func_signature">
     <code>
      pg_logical_slot_get_changes
     </code>
     (
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     <code>
      name
     </code>
     ,
     <em class="parameter">
      <code>
       upto_lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ,
     <em class="parameter">
      <code>
       upto_nchanges
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <code>
      VARIADIC
     </code>
     <em class="parameter">
      <code>
       options
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
       lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ,
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
       data
      </code>
     </em>
     <code>
      text
     </code>
     )
    </p>
    <p>
     Returns changes in the slot
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     , starting from the point from which changes have been consumed last.  If
     <em class="parameter">
      <code>
       upto_lsn
      </code>
     </em>
     and
     <em class="parameter">
      <code>
       upto_nchanges
      </code>
     </em>
     are NULL, logical decoding will continue until end of WAL.  If
     <em class="parameter">
      <code>
       upto_lsn
      </code>
     </em>
     is non-NULL, decoding will include only those transactions which commit prior to the specified LSN.  If
     <em class="parameter">
      <code>
       upto_nchanges
      </code>
     </em>
     is non-NULL, decoding will stop when the number of rows produced by decoding exceeds the specified value.  Note, however, that the actual number of rows returned may be larger, since this limit is only checked after adding the rows produced when decoding each new transaction commit. If the specified slot is a logical failover slot then the function will not return until all physical slots specified in
     <a class="link" href="runtime-config-replication.md#GUC-SYNCHRONIZED-STANDBY-SLOTS">
      <code>
       synchronized_standby_slots
      </code>
     </a>
     have confirmed WAL receipt.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-LOGICAL-SLOT-PEEK-CHANGES">
    <p class="func_signature">
     <code>
      pg_logical_slot_peek_changes
     </code>
     (
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     <code>
      name
     </code>
     ,
     <em class="parameter">
      <code>
       upto_lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ,
     <em class="parameter">
      <code>
       upto_nchanges
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <code>
      VARIADIC
     </code>
     <em class="parameter">
      <code>
       options
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
       lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ,
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
       data
      </code>
     </em>
     <code>
      text
     </code>
     )
    </p>
    <p>
     Behaves just like the
     <code>
      pg_logical_slot_get_changes()
     </code>
     function, except that changes are not consumed; that is, they will be returned again on future calls.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-LOGICAL-SLOT-GET-BINARY-CHANGES">
    <p class="func_signature">
     <code>
      pg_logical_slot_get_binary_changes
     </code>
     (
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     <code>
      name
     </code>
     ,
     <em class="parameter">
      <code>
       upto_lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ,
     <em class="parameter">
      <code>
       upto_nchanges
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <code>
      VARIADIC
     </code>
     <em class="parameter">
      <code>
       options
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
       lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ,
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
       data
      </code>
     </em>
     <code>
      bytea
     </code>
     )
    </p>
    <p>
     Behaves just like the
     <code>
      pg_logical_slot_get_changes()
     </code>
     function, except that changes are returned as
     <code>
      bytea
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_logical_slot_peek_binary_changes
     </code>
     (
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     <code>
      name
     </code>
     ,
     <em class="parameter">
      <code>
       upto_lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ,
     <em class="parameter">
      <code>
       upto_nchanges
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <code>
      VARIADIC
     </code>
     <em class="parameter">
      <code>
       options
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
       lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ,
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
       data
      </code>
     </em>
     <code>
      bytea
     </code>
     )
    </p>
    <p>
     Behaves just like the
     <code>
      pg_logical_slot_peek_changes()
     </code>
     function, except that changes are returned as
     <code>
      bytea
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-REPLICATION-SLOT-ADVANCE">
    <p class="func_signature">
     <code>
      pg_replication_slot_advance
     </code>
     (
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     <code>
      name
     </code>
     ,
     <em class="parameter">
      <code>
       upto_lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ) →
     <code>
      record
     </code>
     (
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     <code>
      name
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
     Advances the current confirmed position of a replication slot named
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     . The slot will not be moved backwards, and it will not be moved beyond the current insert location. Returns the name of the slot and the actual position that it was advanced to. The updated slot position information is written out at the next checkpoint if any advancing is done. So in the event of a crash, the slot may return to an earlier position. If the specified slot is a logical failover slot then the function will not return until all physical slots specified in
     <a class="link" href="runtime-config-replication.md#GUC-SYNCHRONIZED-STANDBY-SLOTS">
      <code>
       synchronized_standby_slots
      </code>
     </a>
     have confirmed WAL receipt.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-REPLICATION-ORIGIN-CREATE">
    <p class="func_signature">
     <code>
      pg_replication_origin_create
     </code>
     (
     <em class="parameter">
      <code>
       node_name
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      oid
     </code>
    </p>
    <p>
     Creates a replication origin with the given external name, and returns the internal ID assigned to it. The name must be no longer than 512 bytes.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-REPLICATION-ORIGIN-DROP">
    <p class="func_signature">
     <code>
      pg_replication_origin_drop
     </code>
     (
     <em class="parameter">
      <code>
       node_name
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      void
     </code>
    </p>
    <p>
     Deletes a previously-created replication origin, including any associated replay progress.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_replication_origin_oid
     </code>
     (
     <em class="parameter">
      <code>
       node_name
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      oid
     </code>
    </p>
    <p>
     Looks up a replication origin by name and returns the internal ID. If no such replication origin is found,
     <code>
      NULL
     </code>
     is returned.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-REPLICATION-ORIGIN-SESSION-SETUP">
    <p class="func_signature">
     <code>
      pg_replication_origin_session_setup
     </code>
     (
     <em class="parameter">
      <code>
       node_name
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      void
     </code>
    </p>
    <p>
     Marks the current session as replaying from the given origin, allowing replay progress to be tracked. Can only be used if no origin is currently selected. Use
     <code>
      pg_replication_origin_session_reset
     </code>
     to undo.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_replication_origin_session_reset
     </code>
     () →
     <code>
      void
     </code>
    </p>
    <p>
     Cancels the effects of
     <code>
      pg_replication_origin_session_setup()
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_replication_origin_session_is_setup
     </code>
     () →
     <code>
      boolean
     </code>
    </p>
    <p>
     Returns true if a replication origin has been selected in the current session.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-REPLICATION-ORIGIN-SESSION-PROGRESS">
    <p class="func_signature">
     <code>
      pg_replication_origin_session_progress
     </code>
     (
     <em class="parameter">
      <code>
       flush
      </code>
     </em>
     <code>
      boolean
     </code>
     ) →
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     Returns the replay location for the replication origin selected in the current session. The parameter
     <em class="parameter">
      <code>
       flush
      </code>
     </em>
     determines whether the corresponding local transaction will be guaranteed to have been flushed to disk or not.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-REPLICATION-ORIGIN-XACT-SETUP">
    <p class="func_signature">
     <code>
      pg_replication_origin_xact_setup
     </code>
     (
     <em class="parameter">
      <code>
       origin_lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ,
     <em class="parameter">
      <code>
       origin_timestamp
      </code>
     </em>
     <code>
      timestamp with time zone
     </code>
     ) →
     <code>
      void
     </code>
    </p>
    <p>
     Marks the current transaction as replaying a transaction that has committed at the given
     <acronym class="acronym">
      LSN
     </acronym>
     and timestamp. Can only be called when a replication origin has been selected using
     <code>
      pg_replication_origin_session_setup
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-REPLICATION-ORIGIN-XACT-RESET">
    <p class="func_signature">
     <code>
      pg_replication_origin_xact_reset
     </code>
     () →
     <code>
      void
     </code>
    </p>
    <p>
     Cancels the effects of
     <code>
      pg_replication_origin_xact_setup()
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-REPLICATION-ORIGIN-ADVANCE">
    <p class="func_signature">
     <code>
      pg_replication_origin_advance
     </code>
     (
     <em class="parameter">
      <code>
       node_name
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       lsn
      </code>
     </em>
     <code>
      pg_lsn
     </code>
     ) →
     <code>
      void
     </code>
    </p>
    <p>
     Sets replication progress for the given node to the given location. This is primarily useful for setting up the initial location, or setting a new location after configuration changes and similar. Be aware that careless use of this function can lead to inconsistently replicated data.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-REPLICATION-ORIGIN-PROGRESS">
    <p class="func_signature">
     <code>
      pg_replication_origin_progress
     </code>
     (
     <em class="parameter">
      <code>
       node_name
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       flush
      </code>
     </em>
     <code>
      boolean
     </code>
     ) →
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     Returns the replay location for the given replication origin. The parameter
     <em class="parameter">
      <code>
       flush
      </code>
     </em>
     determines whether the corresponding local transaction will be guaranteed to have been flushed to disk or not.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-LOGICAL-EMIT-MESSAGE">
    <p class="func_signature">
     <code>
      pg_logical_emit_message
     </code>
     (
     <em class="parameter">
      <code>
       transactional
      </code>
     </em>
     <code>
      boolean
     </code>
     ,
     <em class="parameter">
      <code>
       prefix
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       content
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
        flush
       </code>
      </em>
      <code>
       boolean
      </code>
      <code>
       DEFAULT
      </code>
      <code>
       false
      </code>
     </span>
     ] ) →
     <code>
      pg_lsn
     </code>
    </p>
    <p class="func_signature">
     <code>
      pg_logical_emit_message
     </code>
     (
     <em class="parameter">
      <code>
       transactional
      </code>
     </em>
     <code>
      boolean
     </code>
     ,
     <em class="parameter">
      <code>
       prefix
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       content
      </code>
     </em>
     <code>
      bytea
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        flush
       </code>
      </em>
      <code>
       boolean
      </code>
      <code>
       DEFAULT
      </code>
      <code>
       false
      </code>
     </span>
     ] ) →
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     Emits a logical decoding message. This can be used to pass generic messages to logical decoding plugins through WAL. The
     <em class="parameter">
      <code>
       transactional
      </code>
     </em>
     parameter specifies if the message should be part of the current transaction, or if it should be written immediately and decoded as soon as the logical decoder reads the record. The
     <em class="parameter">
      <code>
       prefix
      </code>
     </em>
     parameter is a textual prefix that can be used by logical decoding plugins to easily recognize messages that are interesting for them. The
     <em class="parameter">
      <code>
       content
      </code>
     </em>
     parameter is the content of the message, given either in text or binary form. The
     <em class="parameter">
      <code>
       flush
      </code>
     </em>
     parameter (default set to
     <code>
      false
     </code>
     ) controls if the message is immediately flushed to WAL or not.
     <em class="parameter">
      <code>
       flush
      </code>
     </em>
     has no effect with
     <em class="parameter">
      <code>
       transactional
      </code>
     </em>
     , as the message's WAL record is flushed along with its transaction.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry" id="PG-SYNC-REPLICATION-SLOTS">
    <p class="func_signature">
     <code>
      pg_sync_replication_slots
     </code>
     () →
     <code>
      void
     </code>
    </p>
    <p>
     Synchronize the logical failover replication slots from the primary server to the standby server. This function can only be executed on the standby server. Temporary synced slots, if any, cannot be used for logical decoding and must be dropped after promotion. See
     <a class="xref" href="logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION" title="47.2.3. Replication Slot Synchronization">
      Section 47.2.3
     </a>
     for details. Note that this function is primarily intended for testing and debugging purposes and should be used with caution. Additionally, this function cannot be executed if
     <a class="link" href="runtime-config-replication.md#GUC-SYNC-REPLICATION-SLOTS">
      <code>
       sync_replication_slots
      </code>
     </a>
     is enabled and the slotsync worker is already running to perform the synchronization of slots.
    </p>
    <div class="caution">
     <h3 class="title">
      Caution
     </h3>
     <p>
      If, after executing the function,
      <a class="link" href="runtime-config-replication.md#GUC-HOT-STANDBY-FEEDBACK">
       <code>
        hot_standby_feedback
       </code>
      </a>
      is disabled on the standby or the physical slot configured in
      <a class="link" href="runtime-config-replication.md#GUC-PRIMARY-SLOT-NAME">
       <code>
        primary_slot_name
       </code>
      </a>
      is removed, then it is possible that the necessary rows of the synchronized slot will be removed by the VACUUM process on the primary server, resulting in the synchronized slot becoming invalidated.
     </p>
    </div>
   </td>
  </tr>
 </tbody>
</table>







### 9.28.7. Funções de Gerenciamento de Objetos de Banco de Dados [#](#FUNCTIONS-ADMIN-DBOBJECT)

As funções apresentadas na [Tabela 9.102](functions-admin.md#FUNCTIONS-ADMIN-DBSIZE) calculam o uso do espaço em disco dos objetos do banco de dados, ou auxiliam na apresentação ou compreensão dos resultados de uso. Os resultados `bigint` são medidos em bytes. Se um OID que não representa um objeto existente for passado para uma dessas funções, `NULL` é retornado.

**Tabela 9.102. Funções de tamanho de objeto de banco de dados**



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
      pg_column_size
     </code>
     (
     <code>
      "any"
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Shows the number of bytes used to store any individual data value.  If applied directly to a table column value, this reflects any compression that was done.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_column_compression
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
     Shows the compression algorithm that was used to compress an individual variable-length value. Returns
     <code>
      NULL
     </code>
     if the value is not compressed.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_column_toast_chunk_id
     </code>
     (
     <code>
      "any"
     </code>
     ) →
     <code>
      oid
     </code>
    </p>
    <p>
     Shows the
     <code>
      chunk_id
     </code>
     of an on-disk
     <acronym class="acronym">
      TOAST
     </acronym>
     ed value.  Returns
     <code>
      NULL
     </code>
     if the value is un-
     <acronym class="acronym">
      TOAST
     </acronym>
     ed or not on-disk.  See
     <a class="xref" href="storage-toast.md" title="66.2. TOAST">
      Section 66.2
     </a>
     for more information about
     <acronym class="acronym">
      TOAST
     </acronym>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_database_size
     </code>
     (
     <code>
      name
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p class="func_signature">
     <code>
      pg_database_size
     </code>
     (
     <code>
      oid
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     Computes the total disk space used by the database with the specified name or OID.  To use this function, you must have
     <code>
      CONNECT
     </code>
     privilege on the specified database (which is granted by default) or have privileges of the
     <code>
      pg_read_all_stats
     </code>
     role.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_indexes_size
     </code>
     (
     <code>
      regclass
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     Computes the total disk space used by indexes attached to the specified table.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_relation_size
     </code>
     (
     <em class="parameter">
      <code>
       relation
      </code>
     </em>
     <code>
      regclass
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        fork
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     Computes the disk space used by one
     <span class="quote">
      “
      <span class="quote">
       fork
      </span>
      ”
     </span>
     of the specified relation.  (Note that for most purposes it is more convenient to use the higher-level functions
     <code>
      pg_total_relation_size
     </code>
     or
     <code>
      pg_table_size
     </code>
     , which sum the sizes of all forks.)  With one argument, this returns the size of the main data fork of the relation.  The second argument can be provided to specify which fork to examine:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist compact" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        <code>
         main
        </code>
        returns the size of the main data fork of the relation.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code>
         fsm
        </code>
        returns the size of the Free Space Map (see
        <a class="xref" href="storage-fsm.md" title="66.3. Free Space Map">
         Section 66.3
        </a>
        ) associated with the relation.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code>
         vm
        </code>
        returns the size of the Visibility Map (see
        <a class="xref" href="storage-vm.md" title="66.4. Visibility Map">
         Section 66.4
        </a>
        ) associated with the relation.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code>
         init
        </code>
        returns the size of the initialization fork, if any, associated with the relation.
       </p>
      </li>
     </ul>
    </div>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_size_bytes
     </code>
     (
     <code>
      text
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     Converts a size in human-readable format (as returned by
     <code>
      pg_size_pretty
     </code>
     ) into bytes.  Valid units are
     <code>
      bytes
     </code>
     ,
     <code>
      B
     </code>
     ,
     <code>
      kB
     </code>
     ,
     <code>
      MB
     </code>
     ,
     <code>
      GB
     </code>
     ,
     <code>
      TB
     </code>
     , and
     <code>
      PB
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_size_pretty
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
    <p class="func_signature">
     <code>
      pg_size_pretty
     </code>
     (
     <code>
      numeric
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Converts a size in bytes into a more easily human-readable format with size units (bytes, kB, MB, GB, TB, or PB as appropriate).  Note that the units are powers of 2 rather than powers of 10, so 1kB is 1024 bytes, 1MB is 1024
     <sup>
      2
     </sup>
     = 1048576 bytes, and so on.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_table_size
     </code>
     (
     <code>
      regclass
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     Computes the disk space used by the specified table, excluding indexes (but including its TOAST table if any, free space map, and visibility map).
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_tablespace_size
     </code>
     (
     <code>
      name
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p class="func_signature">
     <code>
      pg_tablespace_size
     </code>
     (
     <code>
      oid
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     Computes the total disk space used in the tablespace with the specified name or OID. To use this function, you must have
     <code>
      CREATE
     </code>
     privilege on the specified tablespace or have privileges of the
     <code>
      pg_read_all_stats
     </code>
     role, unless it is the default tablespace for the current database.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_total_relation_size
     </code>
     (
     <code>
      regclass
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     Computes the total disk space used by the specified table, including all indexes and
     <acronym class="acronym">
      TOAST
     </acronym>
     data.  The result is equivalent to
     <code>
      pg_table_size
     </code>
     <code>
      +
     </code>
     <code>
      pg_indexes_size
     </code>
     .
    </p>
   </td>
  </tr>
 </tbody>
</table>










As funções acima que operam em tabelas ou índices aceitam um argumento `regclass`, que é simplesmente o OID da tabela ou índice no catálogo de sistema `pg_class`. No entanto, você não precisa procurar o OID manualmente, pois o conversor de entrada do tipo de dados `regclass` fará o trabalho por você. Veja [Seção 8.19](datatype-oid.md) para detalhes.

As funções apresentadas na [Tabela 9.103](functions-admin.md#FUNCTIONS-ADMIN-DBLOCATION) auxiliam na identificação dos arquivos específicos do disco associados aos objetos do banco de dados.

**Tabela 9.103. Funções de localização de objetos de banco de dados**



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
      pg_relation_filenode
     </code>
     (
     <em class="parameter">
      <code>
       relation
      </code>
     </em>
     <code>
      regclass
     </code>
     ) →
     <code>
      oid
     </code>
    </p>
    <p>
     Returns the
     <span class="quote">
      “
      <span class="quote">
       filenode
      </span>
      ”
     </span>
     number currently assigned to the specified relation.  The filenode is the base component of the file name(s) used for the relation (see
     <a class="xref" href="storage-file-layout.md" title="66.1. Database File Layout">
      Section 66.1
     </a>
     for more information). For most relations the result is the same as
     <code>
      pg_class
     </code>
     .
     <code>
      relfilenode
     </code>
     , but for certain system catalogs
     <code>
      relfilenode
     </code>
     is zero and this function must be used to get the correct value.  The function returns NULL if passed a relation that does not have storage, such as a view.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_relation_filepath
     </code>
     (
     <em class="parameter">
      <code>
       relation
      </code>
     </em>
     <code>
      regclass
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Returns the entire file path name (relative to the database cluster's data directory,
     <code>
      PGDATA
     </code>
     ) of the relation.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_filenode_relation
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
     ,
     <em class="parameter">
      <code>
       filenode
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      regclass
     </code>
    </p>
    <p>
     Returns a relation's OID given the tablespace OID and filenode it is stored under.  This is essentially the inverse mapping of
     <code>
      pg_relation_filepath
     </code>
     .  For a relation in the database's default tablespace, the tablespace can be specified as zero. Returns
     <code>
      NULL
     </code>
     if no relation in the current database is associated with the given values, or if dealing with a temporary relation.
    </p>
   </td>
  </tr>
 </tbody>
</table>










[Tabela 9.104](functions-admin.md#FUNCTIONS-ADMIN-COLLATION) lista as funções usadas para gerenciar colatões.

**Tabela 9.104. Funções de Gerenciamento de Colaboração**



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
      pg_collation_actual_version
     </code>
     (
     <code>
      oid
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Returns the actual version of the collation object as it is currently installed in the operating system.  If this is different from the value in
     <code>
      pg_collation
     </code>
     .
     <code>
      collversion
     </code>
     , then objects depending on the collation might need to be rebuilt.  See also
     <a class="xref" href="sql-altercollation.md" title="ALTER COLLATION">
      <span class="refentrytitle">
       ALTER COLLATION
      </span>
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_database_collation_actual_version
     </code>
     (
     <code>
      oid
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Returns the actual version of the database's collation as it is currently installed in the operating system.  If this is different from the value in
     <code>
      pg_database
     </code>
     .
     <code>
      datcollversion
     </code>
     , then objects depending on the collation might need to be rebuilt.  See also
     <a class="xref" href="sql-alterdatabase.md" title="ALTER DATABASE">
      <span class="refentrytitle">
       ALTER DATABASE
      </span>
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_import_system_collations
     </code>
     (
     <em class="parameter">
      <code>
       schema
      </code>
     </em>
     <code>
      regnamespace
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Adds collations to the system catalog
     <code>
      pg_collation
     </code>
     based on all the locales it finds in the operating system.  This is what
     <code>
      initdb
     </code>
     uses; see
     <a class="xref" href="collation.md#COLLATION-MANAGING" title="23.2.2. Managing Collations">
      Section 23.2.2
     </a>
     for more details.  If additional locales are installed into the operating system later on, this function can be run again to add collations for the new locales. Locales that match existing entries in
     <code>
      pg_collation
     </code>
     will be skipped.  (But collation objects based on locales that are no longer present in the operating system are not removed by this function.) The
     <em class="parameter">
      <code>
       schema
      </code>
     </em>
     parameter would typically be
     <code>
      pg_catalog
     </code>
     , but that is not a requirement; the collations could be installed into some other schema as well.  The function returns the number of new collation objects it created. Use of this function is restricted to superusers.
    </p>
   </td>
  </tr>
 </tbody>
</table>










[Tabela 9.105](functions-admin.md#FUNCTIONS-ADMIN-STATSMOD) lista funções usadas para manipular estatísticas. Essas funções não podem ser executadas durante a recuperação.

### Aviso

As alterações feitas por essas funções de manipulação de estatísticas provavelmente serão sobrescritas por [autovacuum](routine-vacuuming.md#AUTOVACUUM)(ou manual `VACUUM` ou `ANALYZE`) e devem ser consideradas temporárias.

**Tabela 9.105. Funções de manipulação de estatísticas de objetos de banco de dados**



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
      pg_restore_relation_stats
     </code>
     (
     <code>
      VARIADIC
     </code>
     <em class="parameter">
      <code>
       kwargs
      </code>
     </em>
     <code>
      "any"
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Updates table-level statistics.  Ordinarily, these statistics are collected automatically or updated as a part of
     <a class="xref" href="sql-vacuum.md" title="VACUUM">
      <span class="refentrytitle">
       VACUUM
      </span>
     </a>
     or
     <a class="xref" href="sql-analyze.md" title="ANALYZE">
      <span class="refentrytitle">
       ANALYZE
      </span>
     </a>
     , so it's not necessary to call this function.  However, it is useful after a restore to enable the optimizer to choose better plans if
     <code>
      ANALYZE
     </code>
     has not been run yet.
    </p>
    <p>
     The tracked statistics may change from version to version, so arguments are passed as pairs of
     <em class="replaceable">
      <code>
       argname
      </code>
     </em>
     and
     <em class="replaceable">
      <code>
       argvalue
      </code>
     </em>
     in the form:
    </p>
    <pre class="programlisting">
SELECT pg_restore_relation_stats( '<code>arg1name</code>', '<code>arg1value</code>'::<code>arg1type</code>, '<code>arg2name</code>', '<code>arg2value</code>'::<code>arg2type</code>, '<code>arg3name</code>', '<code>arg3value</code>'::<code>arg3type</code>);
</pre>
    <p>
    </p>
    <p>
     For example, to set the
     <code>
      relpages
     </code>
     and
     <code>
      reltuples
     </code>
     values for the table
     <code>
      mytable
     </code>
     :
    </p>
    <pre class="programlisting">
SELECT pg_restore_relation_stats( 'schemaname', 'myschema', 'relname',    'mytable', 'relpages',   173::integer, 'reltuples',  10000::real);
</pre>
    <p>
    </p>
    <p>
     The arguments
     <code>
      schemaname
     </code>
     and
     <code>
      relname
     </code>
     are required, and specify the table. Other arguments are the names and values of statistics corresponding to certain columns in
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code>
       pg_class
      </code>
     </a>
     . The currently-supported relation statistics are
     <code>
      relpages
     </code>
     with a value of type
     <code>
      integer
     </code>
     ,
     <code>
      reltuples
     </code>
     with a value of type
     <code>
      real
     </code>
     ,
     <code>
      relallvisible
     </code>
     with a value of type
     <code>
      integer
     </code>
     , and
     <code>
      relallfrozen
     </code>
     with a value of type
     <code>
      integer
     </code>
     .
    </p>
    <p>
     Additionally, this function accepts argument name
     <code>
      version
     </code>
     of type
     <code>
      integer
     </code>
     , which specifies the server version from which the statistics originated. This is anticipated to be helpful in porting statistics from older versions of
     <span class="productname">
      PostgreSQL
     </span>
     .
    </p>
    <p>
     Minor errors are reported as a
     <code>
      WARNING
     </code>
     and ignored, and remaining statistics will still be restored. If all specified statistics are successfully restored, returns
     <code>
      true
     </code>
     , otherwise
     <code>
      false
     </code>
     .
    </p>
    <p>
     The caller must have the
     <code>
      MAINTAIN
     </code>
     privilege on the table or be the owner of the database.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_clear_relation_stats
     </code>
     (
     <em class="parameter">
      <code>
       schemaname
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       relname
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      void
     </code>
    </p>
    <p>
     Clears table-level statistics for the given relation, as though the table was newly created.
    </p>
    <p>
     The caller must have the
     <code>
      MAINTAIN
     </code>
     privilege on the table or be the owner of the database.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_restore_attribute_stats
     </code>
     (
     <code>
      VARIADIC
     </code>
     <em class="parameter">
      <code>
       kwargs
      </code>
     </em>
     <code>
      "any"
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Creates or updates column-level statistics.  Ordinarily, these statistics are collected automatically or updated as a part of
     <a class="xref" href="sql-vacuum.md" title="VACUUM">
      <span class="refentrytitle">
       VACUUM
      </span>
     </a>
     or
     <a class="xref" href="sql-analyze.md" title="ANALYZE">
      <span class="refentrytitle">
       ANALYZE
      </span>
     </a>
     , so it's not necessary to call this function.  However, it is useful after a restore to enable the optimizer to choose better plans if
     <code>
      ANALYZE
     </code>
     has not been run yet.
    </p>
    <p>
     The tracked statistics may change from version to version, so arguments are passed as pairs of
     <em class="replaceable">
      <code>
       argname
      </code>
     </em>
     and
     <em class="replaceable">
      <code>
       argvalue
      </code>
     </em>
     in the form:
    </p>
    <pre class="programlisting">
SELECT pg_restore_attribute_stats( '<code>arg1name</code>', '<code>arg1value</code>'::<code>arg1type</code>, '<code>arg2name</code>', '<code>arg2value</code>'::<code>arg2type</code>, '<code>arg3name</code>', '<code>arg3value</code>'::<code>arg3type</code>);
</pre>
    <p>
    </p>
    <p>
     For example, to set the
     <code>
      avg_width
     </code>
     and
     <code>
      null_frac
     </code>
     values for the attribute
     <code>
      col1
     </code>
     of the table
     <code>
      mytable
     </code>
     :
    </p>
    <pre class="programlisting">
SELECT pg_restore_attribute_stats( 'schemaname', 'myschema', 'relname',    'mytable', 'attname',    'col1', 'inherited',  false, 'avg_width',  125::integer, 'null_frac',  0.5::real);
</pre>
    <p>
    </p>
    <p>
     The required arguments are
     <code>
      schemaname
     </code>
     and
     <code>
      relname
     </code>
     with a value of type
     <code>
      text
     </code>
     which specify the table; either
     <code>
      attname
     </code>
     with a value of type
     <code>
      text
     </code>
     or
     <code>
      attnum
     </code>
     with a value of type
     <code>
      smallint
     </code>
     , which specifies the column; and
     <code>
      inherited
     </code>
     , which specifies whether the statistics include values from child tables.  Other arguments are the names and values of statistics corresponding to columns in
     <a class="link" href="view-pg-stats.md" title="53.29. pg_stats">
      <code>
       pg_stats
      </code>
     </a>
     .
    </p>
    <p>
     Additionally, this function accepts argument name
     <code>
      version
     </code>
     of type
     <code>
      integer
     </code>
     , which specifies the server version from which the statistics originated. This is anticipated to be helpful in porting statistics from older versions of
     <span class="productname">
      PostgreSQL
     </span>
     .
    </p>
    <p>
     Minor errors are reported as a
     <code>
      WARNING
     </code>
     and ignored, and remaining statistics will still be restored. If all specified statistics are successfully restored, returns
     <code>
      true
     </code>
     , otherwise
     <code>
      false
     </code>
     .
    </p>
    <p>
     The caller must have the
     <code>
      MAINTAIN
     </code>
     privilege on the table or be the owner of the database.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_clear_attribute_stats
     </code>
     (
     <em class="parameter">
      <code>
       schemaname
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       relname
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       attname
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       inherited
      </code>
     </em>
     <code>
      boolean
     </code>
     ) →
     <code>
      void
     </code>
    </p>
    <p>
     Clears column-level statistics for the given relation and attribute, as though the table was newly created.
    </p>
    <p>
     The caller must have the
     <code>
      MAINTAIN
     </code>
     privilege on the table or be the owner of the database.
    </p>
   </td>
  </tr>
 </tbody>
</table>










[Tabela 9.106](functions-admin.md#FUNCTIONS-INFO-PARTITION) lista funções que fornecem informações sobre a estrutura de tabelas particionadas.

**Tabela 9.106. Funções de informações de particionamento**



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
      pg_partition_tree
     </code>
     (
     <code>
      regclass
     </code>
     ) →
     <code>
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       relid
      </code>
     </em>
     <code>
      regclass
     </code>
     ,
     <em class="parameter">
      <code>
       parentrelid
      </code>
     </em>
     <code>
      regclass
     </code>
     ,
     <em class="parameter">
      <code>
       isleaf
      </code>
     </em>
     <code>
      boolean
     </code>
     ,
     <em class="parameter">
      <code>
       level
      </code>
     </em>
     <code>
      integer
     </code>
     )
    </p>
    <p>
     Lists the tables or indexes in the partition tree of the given partitioned table or partitioned index, with one row for each partition.  Information provided includes the OID of the partition, the OID of its immediate parent, a boolean value telling if the partition is a leaf, and an integer telling its level in the hierarchy. The level value is 0 for the input table or index, 1 for its immediate child partitions, 2 for their partitions, and so on. Returns no rows if the relation does not exist or is not a partition or partitioned table.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_partition_ancestors
     </code>
     (
     <code>
      regclass
     </code>
     ) →
     <code>
      setof regclass
     </code>
    </p>
    <p>
     Lists the ancestor relations of the given partition, including the relation itself.  Returns no rows if the relation does not exist or is not a partition or partitioned table.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_partition_root
     </code>
     (
     <code>
      regclass
     </code>
     ) →
     <code>
      regclass
     </code>
    </p>
    <p>
     Returns the top-most parent of the partition tree to which the given relation belongs.  Returns
     <code>
      NULL
     </code>
     if the relation does not exist or is not a partition or partitioned table.
    </p>
   </td>
  </tr>
 </tbody>
</table>










Por exemplo, para verificar o tamanho total dos dados contidos em uma tabela particionada `measurement`, é possível usar a seguinte consulta:

```
SELECT pg_size_pretty(sum(pg_relation_size(relid))) AS total_size
  FROM pg_partition_tree('measurement');
```

### 9.28.8. Funções de manutenção de índice [#](#FUNCTIONS-ADMIN-INDEX)

[Tabela 9.107](functions-admin.md#FUNCTIONS-ADMIN-INDEX-TABLE) mostra as funções disponíveis para tarefas de manutenção de índices. (Observe que essas tarefas de manutenção são normalmente realizadas automaticamente pelo autovacuum; o uso dessas funções é necessário apenas em casos especiais.) Essas funções não podem ser executadas durante a recuperação. O uso dessas funções é restrito a superusuários e ao proprietário do índice dado.

**Tabela 9.107. Funções de manutenção de índice**



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
      brin_summarize_new_values
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
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Scans the specified BRIN index to find page ranges in the base table that are not currently summarized by the index; for any such range it creates a new summary index tuple by scanning those table pages. Returns the number of new page range summaries that were inserted into the index.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      brin_summarize_range
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
       blockNumber
      </code>
     </em>
     <code>
      bigint
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Summarizes the page range covering the given block, if not already summarized.  This is like
     <code>
      brin_summarize_new_values
     </code>
     except that it only processes the page range that covers the given table block number.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      brin_desummarize_range
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
       blockNumber
      </code>
     </em>
     <code>
      bigint
     </code>
     ) →
     <code>
      void
     </code>
    </p>
    <p>
     Removes the BRIN index tuple that summarizes the page range covering the given table block, if there is one.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      gin_clean_pending_list
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
     ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     Cleans up the
     <span class="quote">
      “
      <span class="quote">
       pending
      </span>
      ”
     </span>
     list of the specified GIN index by moving entries in it, in bulk, to the main GIN data structure. Returns the number of pages removed from the pending list. If the argument is a GIN index built with the
     <code>
      fastupdate
     </code>
     option disabled, no cleanup happens and the result is zero, because the index doesn't have a pending list. See
     <a class="xref" href="gin.md#GIN-FAST-UPDATE" title="65.4.4.1. GIN Fast Update Technique">
      Section 65.4.4.1
     </a>
     and
     <a class="xref" href="gin.md#GIN-TIPS" title="65.4.5. GIN Tips and Tricks">
      Section 65.4.5
     </a>
     for details about the pending list and
     <code>
      fastupdate
     </code>
     option.
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 9.28.9. Funções de acesso a arquivos genéricos [#](#FUNCTIONS-ADMIN-GENFILE)

As funções exibidas na [Tabela 9.108](functions-admin.md#FUNCTIONS-ADMIN-GENFILE-TABLE) fornecem acesso nativo a arquivos na máquina que hospeda o servidor. Apenas os arquivos dentro do diretório do clúster do banco de dados e do `log_directory` podem ser acessados, a menos que o usuário seja um superusuário ou tenha concedido o papel `pg_read_server_files`. Use um caminho relativo para arquivos no diretório do clúster e um caminho que corresponda ao ajuste de configuração `log_directory` para arquivos de log.

Observe que conceder aos usuários o privilégio EXECUTE em `pg_read_file()`, ou funções relacionadas, permite que eles leiam qualquer arquivo no servidor que o servidor de banco de dados possa ler; essas funções contornam todas as verificações de privilégio no banco de dados. Isso significa que, por exemplo, um usuário com esse acesso pode ler o conteúdo da tabela `pg_authid`, onde as informações de autenticação são armazenadas, bem como ler qualquer dado da tabela no banco de dados. Portanto, a concessão de acesso a essas funções deve ser cuidadosamente considerada.

Ao conceder privilégios nessas funções, observe que as entradas da tabela que mostram os parâmetros opcionais são implementadas principalmente como várias funções físicas com listas de parâmetros diferentes. O privilégio deve ser concedido separadamente em cada uma dessas funções, se ela deve ser usada. O comando `\df` do psql pode ser útil para verificar quais são as assinaturas reais das funções.

Algumas dessas funções aceitam um parâmetro opcional *`missing_ok`*, que especifica o comportamento quando o arquivo ou diretório não existir. Se `true`, a função retorna `NULL` ou um conjunto de resultados vazio, conforme apropriado. Se `false`, um erro é gerado. (Condições de falha que não são "arquivo não encontrado" são relatadas como erros em qualquer caso.) O padrão é `false`.

**Tabela 9.108. Funções genéricas de acesso a arquivos**



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
      pg_ls_dir
     </code>
     (
     <em class="parameter">
      <code>
       dirname
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
        missing_ok
       </code>
      </em>
      <code>
       boolean
      </code>
      ,
      <em class="parameter">
       <code>
        include_dot_dirs
       </code>
      </em>
      <code>
       boolean
      </code>
     </span>
     ] ) →
     <code>
      setof text
     </code>
    </p>
    <p>
     Returns the names of all files (and directories and other special files) in the specified directory. The
     <em class="parameter">
      <code>
       include_dot_dirs
      </code>
     </em>
     parameter indicates whether
     <span class="quote">
      “
      <span class="quote">
       .
      </span>
      ”
     </span>
     and
     <span class="quote">
      “
      <span class="quote">
       ..
      </span>
      ”
     </span>
     are to be included in the result set; the default is to exclude them.  Including them can be useful when
     <em class="parameter">
      <code>
       missing_ok
      </code>
     </em>
     is
     <code>
      true
     </code>
     , to distinguish an empty directory from a non-existent directory.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_ls_logdir
     </code>
     () →
     <code>
      setof record
     </code>
     (
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
       size
      </code>
     </em>
     <code>
      bigint
     </code>
     ,
     <em class="parameter">
      <code>
       modification
      </code>
     </em>
     <code>
      timestamp with time zone
     </code>
     )
    </p>
    <p>
     Returns the name, size, and last modification time (mtime) of each ordinary file in the server's log directory.  Filenames beginning with a dot, directories, and other special files are excluded.
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
      pg_ls_waldir
     </code>
     () →
     <code>
      setof record
     </code>
     (
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
       size
      </code>
     </em>
     <code>
      bigint
     </code>
     ,
     <em class="parameter">
      <code>
       modification
      </code>
     </em>
     <code>
      timestamp with time zone
     </code>
     )
    </p>
    <p>
     Returns the name, size, and last modification time (mtime) of each ordinary file in the server's write-ahead log (WAL) directory. Filenames beginning with a dot, directories, and other special files are excluded.
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
      pg_ls_logicalmapdir
     </code>
     () →
     <code>
      setof record
     </code>
     (
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
       size
      </code>
     </em>
     <code>
      bigint
     </code>
     ,
     <em class="parameter">
      <code>
       modification
      </code>
     </em>
     <code>
      timestamp with time zone
     </code>
     )
    </p>
    <p>
     Returns the name, size, and last modification time (mtime) of each ordinary file in the server's
     <code>
      pg_logical/mappings
     </code>
     directory. Filenames beginning with a dot, directories, and other special files are excluded.
    </p>
    <p>
     This function is restricted to superusers and members of the
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
      pg_ls_logicalsnapdir
     </code>
     () →
     <code>
      setof record
     </code>
     (
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
       size
      </code>
     </em>
     <code>
      bigint
     </code>
     ,
     <em class="parameter">
      <code>
       modification
      </code>
     </em>
     <code>
      timestamp with time zone
     </code>
     )
    </p>
    <p>
     Returns the name, size, and last modification time (mtime) of each ordinary file in the server's
     <code>
      pg_logical/snapshots
     </code>
     directory. Filenames beginning with a dot, directories, and other special files are excluded.
    </p>
    <p>
     This function is restricted to superusers and members of the
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
      pg_ls_replslotdir
     </code>
     (
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      setof record
     </code>
     (
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
       size
      </code>
     </em>
     <code>
      bigint
     </code>
     ,
     <em class="parameter">
      <code>
       modification
      </code>
     </em>
     <code>
      timestamp with time zone
     </code>
     )
    </p>
    <p>
     Returns the name, size, and last modification time (mtime) of each ordinary file in the server's
     <code>
      pg_replslot/slot_name
     </code>
     directory, where
     <em class="parameter">
      <code>
       slot_name
      </code>
     </em>
     is the name of the replication slot provided as input of the function. Filenames beginning with a dot, directories, and other special files are excluded.
    </p>
    <p>
     This function is restricted to superusers and members of the
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
      pg_ls_summariesdir
     </code>
     () →
     <code>
      setof record
     </code>
     (
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
       size
      </code>
     </em>
     <code>
      bigint
     </code>
     ,
     <em class="parameter">
      <code>
       modification
      </code>
     </em>
     <code>
      timestamp with time zone
     </code>
     )
    </p>
    <p>
     Returns the name, size, and last modification time (mtime) of each ordinary file in the server's WAL summaries directory (
     <code>
      pg_wal/summaries
     </code>
     ).  Filenames beginning with a dot, directories, and other special files are excluded.
    </p>
    <p>
     This function is restricted to superusers and members of the
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
      pg_ls_archive_statusdir
     </code>
     () →
     <code>
      setof record
     </code>
     (
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
       size
      </code>
     </em>
     <code>
      bigint
     </code>
     ,
     <em class="parameter">
      <code>
       modification
      </code>
     </em>
     <code>
      timestamp with time zone
     </code>
     )
    </p>
    <p>
     Returns the name, size, and last modification time (mtime) of each ordinary file in the server's WAL archive status directory (
     <code>
      pg_wal/archive_status
     </code>
     ).  Filenames beginning with a dot, directories, and other special files are excluded.
    </p>
    <p>
     This function is restricted to superusers and members of the
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
      pg_ls_tmpdir
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        tablespace
       </code>
      </em>
      <code>
       oid
      </code>
     </span>
     ] ) →
     <code>
      setof record
     </code>
     (
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
       size
      </code>
     </em>
     <code>
      bigint
     </code>
     ,
     <em class="parameter">
      <code>
       modification
      </code>
     </em>
     <code>
      timestamp with time zone
     </code>
     )
    </p>
    <p>
     Returns the name, size, and last modification time (mtime) of each ordinary file in the temporary file directory for the specified
     <em class="parameter">
      <code>
       tablespace
      </code>
     </em>
     . If
     <em class="parameter">
      <code>
       tablespace
      </code>
     </em>
     is not provided, the
     <code>
      pg_default
     </code>
     tablespace is examined.  Filenames beginning with a dot, directories, and other special files are excluded.
    </p>
    <p>
     This function is restricted to superusers and members of the
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
      pg_read_file
     </code>
     (
     <em class="parameter">
      <code>
       filename
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
        offset
       </code>
      </em>
      <code>
       bigint
      </code>
      ,
      <em class="parameter">
       <code>
        length
       </code>
      </em>
      <code>
       bigint
      </code>
     </span>
     ] [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        missing_ok
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
     Returns all or part of a text file, starting at the given byte
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     , returning at most
     <em class="parameter">
      <code>
       length
      </code>
     </em>
     bytes (less if the end of file is reached first).  If
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     is negative, it is relative to the end of the file.  If
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     and
     <em class="parameter">
      <code>
       length
      </code>
     </em>
     are omitted, the entire file is returned.  The bytes read from the file are interpreted as a string in the database's encoding; an error is thrown if they are not valid in that encoding.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_read_binary_file
     </code>
     (
     <em class="parameter">
      <code>
       filename
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
        offset
       </code>
      </em>
      <code>
       bigint
      </code>
      ,
      <em class="parameter">
       <code>
        length
       </code>
      </em>
      <code>
       bigint
      </code>
     </span>
     ] [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        missing_ok
       </code>
      </em>
      <code>
       boolean
      </code>
     </span>
     ] ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Returns all or part of a file.  This function is identical to
     <code>
      pg_read_file
     </code>
     except that it can read arbitrary binary data, returning the result as
     <code>
      bytea
     </code>
     not
     <code>
      text
     </code>
     ; accordingly, no encoding checks are performed.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
    <p>
     In combination with the
     <code>
      convert_from
     </code>
     function, this function can be used to read a text file in a specified encoding and convert to the database's encoding:
    </p>
    <pre class="programlisting">
SELECT convert_from(pg_read_binary_file('file_in_utf8.txt'), 'UTF8');
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_stat_file
     </code>
     (
     <em class="parameter">
      <code>
       filename
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
        missing_ok
       </code>
      </em>
      <code>
       boolean
      </code>
     </span>
     ] ) →
     <code>
      record
     </code>
     (
     <em class="parameter">
      <code>
       size
      </code>
     </em>
     <code>
      bigint
     </code>
     ,
     <em class="parameter">
      <code>
       access
      </code>
     </em>
     <code>
      timestamp with time zone
     </code>
     ,
     <em class="parameter">
      <code>
       modification
      </code>
     </em>
     <code>
      timestamp with time zone
     </code>
     ,
     <em class="parameter">
      <code>
       change
      </code>
     </em>
     <code>
      timestamp with time zone
     </code>
     ,
     <em class="parameter">
      <code>
       creation
      </code>
     </em>
     <code>
      timestamp with time zone
     </code>
     ,
     <em class="parameter">
      <code>
       isdir
      </code>
     </em>
     <code>
      boolean
     </code>
     )
    </p>
    <p>
     Returns a record containing the file's size, last access time stamp, last modification time stamp, last file status change time stamp (Unix platforms only), file creation time stamp (Windows only), and a flag indicating if it is a directory.
    </p>
    <p>
     This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
    </p>
   </td>
  </tr>
 </tbody>
</table>







### 9.28.10. Funções de bloqueio de aconselhamento [#](#FUNCTIONS-ADVISORY-LOCKS)

As funções apresentadas na [Tabela 9.109](functions-admin.md#FUNCTIONS-ADVISORY-LOCKS-TABLE) gerenciam bloqueios de aconselhamento. Para obter detalhes sobre o uso adequado dessas funções, consulte [Seção 13.3.5](explicit-locking.md#ADVISORY-LOCKS).

Todas essas funções são destinadas a ser usadas para bloquear recursos definidos pela aplicação, que podem ser identificados por um único valor de chave de 64 bits ou por dois valores de chave de 32 bits (note que esses dois espaços de chave não se sobrepõem). Se outra sessão já tiver um bloqueio conflitante no mesmo identificador de recurso, as funções aguardará até que o recurso se torne disponível, ou retornará um resultado `false`, conforme apropriado para a função. Os bloqueios podem ser compartilhados ou exclusivos: um bloqueio compartilhado não conflita com outros bloqueios compartilhados no mesmo recurso, apenas com bloqueios exclusivos. Os bloqueios podem ser tomados em nível de sessão (para que sejam mantidos até serem liberados ou até o término da sessão) ou em nível de transação (para que sejam mantidos até o término da transação atual; não há disposição para liberação manual). Vários pedidos de bloqueio em nível de sessão se acumulam, portanto, se o mesmo identificador de recurso for bloqueado três vezes, então devem haver três solicitações de desbloqueio para liberar o recurso antes do término da sessão.

**Tabela 9.109. Funções de bloqueio de consulta**



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
      pg_advisory_lock
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      bigint
     </code>
     ) →
     <code>
      void
     </code>
    </p>
    <p class="func_signature">
     <code>
      pg_advisory_lock
     </code>
     (
     <em class="parameter">
      <code>
       key1
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       key2
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      void
     </code>
    </p>
    <p>
     Obtains an exclusive session-level advisory lock, waiting if necessary.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_advisory_lock_shared
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      bigint
     </code>
     ) →
     <code>
      void
     </code>
    </p>
    <p class="func_signature">
     <code>
      pg_advisory_lock_shared
     </code>
     (
     <em class="parameter">
      <code>
       key1
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       key2
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      void
     </code>
    </p>
    <p>
     Obtains a shared session-level advisory lock, waiting if necessary.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_advisory_unlock
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      bigint
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p class="func_signature">
     <code>
      pg_advisory_unlock
     </code>
     (
     <em class="parameter">
      <code>
       key1
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       key2
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Releases a previously-acquired exclusive session-level advisory lock. Returns
     <code>
      true
     </code>
     if the lock is successfully released. If the lock was not held,
     <code>
      false
     </code>
     is returned, and in addition, an SQL warning will be reported by the server.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_advisory_unlock_all
     </code>
     () →
     <code>
      void
     </code>
    </p>
    <p>
     Releases all session-level advisory locks held by the current session. (This function is implicitly invoked at session end, even if the client disconnects ungracefully.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_advisory_unlock_shared
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      bigint
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p class="func_signature">
     <code>
      pg_advisory_unlock_shared
     </code>
     (
     <em class="parameter">
      <code>
       key1
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       key2
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Releases a previously-acquired shared session-level advisory lock. Returns
     <code>
      true
     </code>
     if the lock is successfully released. If the lock was not held,
     <code>
      false
     </code>
     is returned, and in addition, an SQL warning will be reported by the server.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_advisory_xact_lock
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      bigint
     </code>
     ) →
     <code>
      void
     </code>
    </p>
    <p class="func_signature">
     <code>
      pg_advisory_xact_lock
     </code>
     (
     <em class="parameter">
      <code>
       key1
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       key2
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      void
     </code>
    </p>
    <p>
     Obtains an exclusive transaction-level advisory lock, waiting if necessary.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_advisory_xact_lock_shared
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      bigint
     </code>
     ) →
     <code>
      void
     </code>
    </p>
    <p class="func_signature">
     <code>
      pg_advisory_xact_lock_shared
     </code>
     (
     <em class="parameter">
      <code>
       key1
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       key2
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      void
     </code>
    </p>
    <p>
     Obtains a shared transaction-level advisory lock, waiting if necessary.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_try_advisory_lock
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      bigint
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p class="func_signature">
     <code>
      pg_try_advisory_lock
     </code>
     (
     <em class="parameter">
      <code>
       key1
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       key2
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Obtains an exclusive session-level advisory lock if available. This will either obtain the lock immediately and return
     <code>
      true
     </code>
     , or return
     <code>
      false
     </code>
     without waiting if the lock cannot be acquired immediately.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_try_advisory_lock_shared
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      bigint
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p class="func_signature">
     <code>
      pg_try_advisory_lock_shared
     </code>
     (
     <em class="parameter">
      <code>
       key1
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       key2
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Obtains a shared session-level advisory lock if available. This will either obtain the lock immediately and return
     <code>
      true
     </code>
     , or return
     <code>
      false
     </code>
     without waiting if the lock cannot be acquired immediately.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_try_advisory_xact_lock
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      bigint
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p class="func_signature">
     <code>
      pg_try_advisory_xact_lock
     </code>
     (
     <em class="parameter">
      <code>
       key1
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       key2
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Obtains an exclusive transaction-level advisory lock if available. This will either obtain the lock immediately and return
     <code>
      true
     </code>
     , or return
     <code>
      false
     </code>
     without waiting if the lock cannot be acquired immediately.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_try_advisory_xact_lock_shared
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      bigint
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p class="func_signature">
     <code>
      pg_try_advisory_xact_lock_shared
     </code>
     (
     <em class="parameter">
      <code>
       key1
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       key2
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Obtains a shared transaction-level advisory lock if available. This will either obtain the lock immediately and return
     <code>
      true
     </code>
     , or return
     <code>
      false
     </code>
     without waiting if the lock cannot be acquired immediately.
    </p>
   </td>
  </tr>
 </tbody>
</table>





