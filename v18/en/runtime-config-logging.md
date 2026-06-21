## 19.8. Error Reporting and Logging [#](#RUNTIME-CONFIG-LOGGING)

* [19.8.1. Where to Log](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-WHERE)
* [19.8.2. When to Log](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-WHEN)
* [19.8.3. What to Log](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-WHAT)
* [19.8.4. Using CSV-Format Log Output](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-CSVLOG)
* [19.8.5. Using JSON-Format Log Output](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-JSONLOG)
* [19.8.6. Process Title](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-PROC-TITLE)

### 19.8.1. Where to Log [#](#RUNTIME-CONFIG-LOGGING-WHERE)

`log_destination` (`string`) [#](#GUC-LOG-DESTINATION): PostgreSQL supports several methods for logging server messages, including stderr, csvlog, jsonlog, and syslog. On Windows, eventlog is also supported. Set this parameter to a list of desired log destinations separated by commas. The default is to log to stderr only. This parameter can only be set in the `postgresql.conf` file or on the server command line.

If csvlog is included in `log_destination`, log entries are output in “comma-separated value” (CSV) format, which is convenient for loading logs into programs. See [Section 19.8.4](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-CSVLOG "19.8.4. Using CSV-Format Log Output") for details. [logging_collector](runtime-config-logging.md#GUC-LOGGING-COLLECTOR) must be enabled to generate CSV-format log output.

If jsonlog is included in `log_destination`, log entries are output in JSON format, which is convenient for loading logs into programs. See [Section 19.8.5](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-JSONLOG "19.8.5. Using JSON-Format Log Output") for details. [logging_collector](runtime-config-logging.md#GUC-LOGGING-COLLECTOR) must be enabled to generate JSON-format log output.

When either stderr, csvlog or jsonlog are included, the file `current_logfiles` is created to record the location of the log file(s) currently in use by the logging collector and the associated logging destination. This provides a convenient way to find the logs currently in use by the instance. Here is an example of this file's content:

``` stderr log/postgresql.log csvlog log/postgresql.csv jsonlog log/postgresql.json
    ```

    `current_logfiles` is recreated when a new log file is created as an effect of rotation, and when `log_destination` is reloaded. It is removed when none of stderr, csvlog or jsonlog are included in `log_destination`, and when the logging collector is disabled.

    ### Note

    On most Unix systems, you will need to alter the configuration of your system's syslog daemon in order to make use of the syslog option for `log_destination`. PostgreSQL can log to syslog facilities `LOCAL0` through `LOCAL7` (see [syslog_facility](runtime-config-logging.md#GUC-SYSLOG-FACILITY)), but the default syslog configuration on most platforms will discard all such messages. You will need to add something like:

    ```
    local0.*    /var/log/postgresql
    ```

    to the syslog daemon's configuration file to make it work.

    On Windows, when you use the `eventlog` option for `log_destination`, you should register an event source and its library with the operating system so that the Windows Event Viewer can display event log messages cleanly. See [Section 18.12](event-log-registration.md "18.12. Registering Event Log on Windows") for details.

`logging_collector` (`boolean`) [#](#GUC-LOGGING-COLLECTOR): This parameter enables the *logging collector*, which is a background process that captures log messages sent to stderr and redirects them into log files. This approach is often more useful than logging to syslog, since some types of messages might not appear in syslog output. (One common example is dynamic-linker failure messages; another is error messages produced by scripts such as `archive_command`.) This parameter can only be set at server start.

### Note

It is possible to log to stderr without using the logging collector; the log messages will just go to wherever the server's stderr is directed. However, that method is only suitable for low log volumes, since it provides no convenient way to rotate log files. Also, on some platforms not using the logging collector can result in lost or garbled log output, because multiple processes writing concurrently to the same log file can overwrite each other's output.

### Note

The logging collector is designed to never lose messages. This means that in case of extremely high load, server processes could be blocked while trying to send additional log messages when the collector has fallen behind. In contrast, syslog prefers to drop messages if it cannot write them, which means it may fail to log some messages in such cases but it will not block the rest of the system.

`log_directory` (`string`) [#](#GUC-LOG-DIRECTORY): When `logging_collector` is enabled, this parameter determines the directory in which log files will be created. It can be specified as an absolute path, or relative to the cluster data directory. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is `log`.

`log_filename` (`string`) [#](#GUC-LOG-FILENAME): When `logging_collector` is enabled, this parameter sets the file names of the created log files. The value is treated as a `strftime` pattern, so `%`-escapes can be used to specify time-varying file names. (Note that if there are any time-zone-dependent `%`-escapes, the computation is done in the zone specified by [log_timezone](runtime-config-logging.md#GUC-LOG-TIMEZONE).) The supported `%`-escapes are similar to those listed in the Open Group's [strftime](https://pubs.opengroup.org/onlinepubs/009695399/functions/strftime.html) specification. Note that the system's `strftime` is not used directly, so platform-specific (nonstandard) extensions do not work. The default is `postgresql-%Y-%m-%d_%H%M%S.log`.

If you specify a file name without escapes, you should plan to use a log rotation utility to avoid eventually filling the entire disk. In releases prior to 8.4, if no `%` escapes were present, PostgreSQL would append the epoch of the new log file's creation time, but this is no longer the case.

If CSV-format output is enabled in `log_destination`, `.csv` will be appended to the timestamped log file name to create the file name for CSV-format output. (If `log_filename` ends in `.log`, the suffix is replaced instead.)

If JSON-format output is enabled in `log_destination`, `.json` will be appended to the timestamped log file name to create the file name for JSON-format output. (If `log_filename` ends in `.log`, the suffix is replaced instead.)

This parameter can only be set in the `postgresql.conf` file or on the server command line.

`log_file_mode` (`integer`) [#](#GUC-LOG-FILE-MODE): On Unix systems this parameter sets the permissions for log files when `logging_collector` is enabled. (On Microsoft Windows this parameter is ignored.) The parameter value is expected to be a numeric mode specified in the format accepted by the `chmod` and `umask` system calls. (To use the customary octal format the number must start with a `0` (zero).)

The default permissions are `0600`, meaning only the server owner can read or write the log files. The other commonly useful setting is `0640`, allowing members of the owner's group to read the files. Note however that to make use of such a setting, you'll need to alter [log_directory](runtime-config-logging.md#GUC-LOG-DIRECTORY) to store the files somewhere outside the cluster data directory. In any case, it's unwise to make the log files world-readable, since they might contain sensitive data.

This parameter can only be set in the `postgresql.conf` file or on the server command line.

`log_rotation_age` (`integer`) [#](#GUC-LOG-ROTATION-AGE): When `logging_collector` is enabled, this parameter determines the maximum amount of time to use an individual log file, after which a new log file will be created. If this value is specified without units, it is taken as minutes. The default is 24 hours. Set to zero to disable time-based creation of new log files. This parameter can only be set in the `postgresql.conf` file or on the server command line.

`log_rotation_size` (`integer`) [#](#GUC-LOG-ROTATION-SIZE): When `logging_collector` is enabled, this parameter determines the maximum size of an individual log file. After this amount of data has been emitted into a log file, a new log file will be created. If this value is specified without units, it is taken as kilobytes. The default is 10 megabytes. Set to zero to disable size-based creation of new log files. This parameter can only be set in the `postgresql.conf` file or on the server command line.

`log_truncate_on_rotation` (`boolean`) [#](#GUC-LOG-TRUNCATE-ON-ROTATION): When `logging_collector` is enabled, this parameter will cause PostgreSQL to truncate (overwrite), rather than append to, any existing log file of the same name. However, truncation will occur only when a new file is being opened due to time-based rotation, not during server startup or size-based rotation. When off, pre-existing files will be appended to in all cases. For example, using this setting in combination with a `log_filename` like `postgresql-%H.log` would result in generating twenty-four hourly log files and then cyclically overwriting them. This parameter can only be set in the `postgresql.conf` file or on the server command line.

Example: To keep 7 days of logs, one log file per day named `server_log.Mon`, `server_log.Tue`, etc., and automatically overwrite last week's log with this week's log, set `log_filename` to `server_log.%a`, `log_truncate_on_rotation` to `on`, and `log_rotation_age` to `1440`.

Example: To keep 24 hours of logs, one log file per hour, but also rotate sooner if the log file size exceeds 1GB, set `log_filename` to `server_log.%H%M`, `log_truncate_on_rotation` to `on`, `log_rotation_age` to `60`, and `log_rotation_size` to `1000000`. Including `%M` in `log_filename` allows any size-driven rotations that might occur to select a file name different from the hour's initial file name.

`syslog_facility` (`enum`) [#](#GUC-SYSLOG-FACILITY): When logging to syslog is enabled, this parameter determines the syslog “facility” to be used. You can choose from `LOCAL0`, `LOCAL1`, `LOCAL2`, `LOCAL3`, `LOCAL4`, `LOCAL5`, `LOCAL6`, `LOCAL7`; the default is `LOCAL0`. See also the documentation of your system's syslog daemon. This parameter can only be set in the `postgresql.conf` file or on the server command line.

`syslog_ident` (`string`) [#](#GUC-SYSLOG-IDENT): When logging to syslog is enabled, this parameter determines the program name used to identify PostgreSQL messages in syslog logs. The default is `postgres`. This parameter can only be set in the `postgresql.conf` file or on the server command line.

`syslog_sequence_numbers` (`boolean`) [#](#GUC-SYSLOG-SEQUENCE-NUMBERS): When logging to syslog and this is on (the default), then each message will be prefixed by an increasing sequence number (such as `[2]`). This circumvents the “--- last message repeated N times ---” suppression that many syslog implementations perform by default. In more modern syslog implementations, repeated message suppression can be configured (for example, `$RepeatedMsgReduction` in rsyslog), so this might not be necessary. Also, you could turn this off if you actually want to suppress repeated messages.

This parameter can only be set in the `postgresql.conf` file or on the server command line.

`syslog_split_messages` (`boolean`) [#](#GUC-SYSLOG-SPLIT-MESSAGES): When logging to syslog is enabled, this parameter determines how messages are delivered to syslog. When on (the default), messages are split by lines, and long lines are split so that they will fit into 1024 bytes, which is a typical size limit for traditional syslog implementations. When off, PostgreSQL server log messages are delivered to the syslog service as is, and it is up to the syslog service to cope with the potentially bulky messages.

If syslog is ultimately logging to a text file, then the effect will be the same either way, and it is best to leave the setting on, since most syslog implementations either cannot handle large messages or would need to be specially configured to handle them. But if syslog is ultimately writing into some other medium, it might be necessary or more useful to keep messages logically together.

This parameter can only be set in the `postgresql.conf` file or on the server command line.

`event_source` (`string`) [#](#GUC-EVENT-SOURCE): When logging to event log is enabled, this parameter determines the program name used to identify PostgreSQL messages in the log. The default is `PostgreSQL`. This parameter can only be set at server start.

### 19.8.2. When to Log [#](#RUNTIME-CONFIG-LOGGING-WHEN)

`log_min_messages` (`enum`) [#](#GUC-LOG-MIN-MESSAGES): Controls which [message levels](runtime-config-logging.md#RUNTIME-CONFIG-SEVERITY-LEVELS "Table 19.2. Message Severity Levels") are written to the server log. Valid values are `DEBUG5`, `DEBUG4`, `DEBUG3`, `DEBUG2`, `DEBUG1`, `INFO`, `NOTICE`, `WARNING`, `ERROR`, `LOG`, `FATAL`, and `PANIC`. Each level includes all the levels that follow it. The later the level, the fewer messages are sent to the log. The default is `WARNING`. Note that `LOG` has a different rank here than in [client_min_messages](runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES). Only superusers and users with the appropriate `SET` privilege can change this setting.

`log_min_error_statement` (`enum`) [#](#GUC-LOG-MIN-ERROR-STATEMENT): Controls which SQL statements that cause an error condition are recorded in the server log. The current SQL statement is included in the log entry for any message of the specified [severity](runtime-config-logging.md#RUNTIME-CONFIG-SEVERITY-LEVELS "Table 19.2. Message Severity Levels") or higher. Valid values are `DEBUG5`, `DEBUG4`, `DEBUG3`, `DEBUG2`, `DEBUG1`, `INFO`, `NOTICE`, `WARNING`, `ERROR`, `LOG`, `FATAL`, and `PANIC`. The default is `ERROR`, which means statements causing errors, log messages, fatal errors, or panics will be logged. To effectively turn off logging of failing statements, set this parameter to `PANIC`. Only superusers and users with the appropriate `SET` privilege can change this setting.

`log_min_duration_statement` (`integer`) [#](#GUC-LOG-MIN-DURATION-STATEMENT): Causes the duration of each completed statement to be logged if the statement ran for at least the specified amount of time. For example, if you set it to `250ms` then all SQL statements that run 250ms or longer will be logged. Enabling this parameter can be helpful in tracking down unoptimized queries in your applications. If this value is specified without units, it is taken as milliseconds. Setting this to zero prints all statement durations. `-1` (the default) disables logging statement durations. Only superusers and users with the appropriate `SET` privilege can change this setting.

This overrides [log_min_duration_sample](runtime-config-logging.md#GUC-LOG-MIN-DURATION-SAMPLE), meaning that queries with duration exceeding this setting are not subject to sampling and are always logged.

For clients using extended query protocol, durations of the Parse, Bind, and Execute steps are logged independently.

### Note

When using this option together with [log_statement](runtime-config-logging.md#GUC-LOG-STATEMENT), the text of statements that are logged because of `log_statement` will not be repeated in the duration log message. If you are not using syslog, it is recommended that you log the PID or session ID using [log_line_prefix](runtime-config-logging.md#GUC-LOG-LINE-PREFIX) so that you can link the statement message to the later duration message using the process ID or session ID.

`log_min_duration_sample` (`integer`) [#](#GUC-LOG-MIN-DURATION-SAMPLE): Allows sampling the duration of completed statements that ran for at least the specified amount of time. This produces the same kind of log entries as [log_min_duration_statement](runtime-config-logging.md#GUC-LOG-MIN-DURATION-STATEMENT), but only for a subset of the executed statements, with sample rate controlled by [log_statement_sample_rate](runtime-config-logging.md#GUC-LOG-STATEMENT-SAMPLE-RATE). For example, if you set it to `100ms` then all SQL statements that run 100ms or longer will be considered for sampling. Enabling this parameter can be helpful when the traffic is too high to log all queries. If this value is specified without units, it is taken as milliseconds. Setting this to zero samples all statement durations. `-1` (the default) disables sampling statement durations. Only superusers and users with the appropriate `SET` privilege can change this setting.

This setting has lower priority than `log_min_duration_statement`, meaning that statements with durations exceeding `log_min_duration_statement` are not subject to sampling and are always logged.

Other notes for `log_min_duration_statement` apply also to this setting.

`log_statement_sample_rate` (`floating point`) [#](#GUC-LOG-STATEMENT-SAMPLE-RATE): Determines the fraction of statements with duration exceeding [log_min_duration_sample](runtime-config-logging.md#GUC-LOG-MIN-DURATION-SAMPLE) that will be logged. Sampling is stochastic, for example `0.5` means there is statistically one chance in two that any given statement will be logged. The default is `1.0`, meaning to log all sampled statements. Setting this to zero disables sampled statement-duration logging, the same as setting `log_min_duration_sample` to `-1`. Only superusers and users with the appropriate `SET` privilege can change this setting.

`log_transaction_sample_rate` (`floating point`) [#](#GUC-LOG-TRANSACTION-SAMPLE-RATE): Sets the fraction of transactions whose statements are all logged, in addition to statements logged for other reasons. It applies to each new transaction regardless of its statements' durations. Sampling is stochastic, for example `0.1` means there is statistically one chance in ten that any given transaction will be logged. `log_transaction_sample_rate` can be helpful to construct a sample of transactions. The default is `0`, meaning not to log statements from any additional transactions. Setting this to `1` logs all statements of all transactions. Only superusers and users with the appropriate `SET` privilege can change this setting.

### Note

Like all statement-logging options, this option can add significant overhead.

`log_startup_progress_interval` (`integer`) [#](#GUC-LOG-STARTUP-PROGRESS-INTERVAL): Sets the amount of time after which the startup process will log a message about a long-running operation that is still in progress, as well as the interval between further progress messages for that operation. The default is 10 seconds. A setting of `0` disables the feature. If this value is specified without units, it is taken as milliseconds. This setting is applied separately to each operation. This parameter can only be set in the `postgresql.conf` file or on the server command line.

For example, if syncing the data directory takes 25 seconds and thereafter resetting unlogged relations takes 8 seconds, and if this setting has the default value of 10 seconds, then a messages will be logged for syncing the data directory after it has been in progress for 10 seconds and again after it has been in progress for 20 seconds, but nothing will be logged for resetting unlogged relations.

[Table 19.2](runtime-config-logging.md#RUNTIME-CONFIG-SEVERITY-LEVELS "Table 19.2. Message Severity Levels") explains the message severity levels used by PostgreSQL. If logging output is sent to syslog or Windows' eventlog, the severity levels are translated as shown in the table.

**Table 19.2. Message Severity Levels**



<table border="1" class="table" summary="Message Severity Levels">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
  <col class="col4"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Severity
   </th>
   <th>
    Usage
   </th>
   <th>
    <span class="systemitem">
     syslog
    </span>
   </th>
   <th>
    <span class="systemitem">
     eventlog
    </span>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     DEBUG1 .. DEBUG5
    </code>
   </td>
   <td>
    Provides successively-more-detailed information for use by
         developers.
   </td>
   <td>
    <code class="literal">
     DEBUG
    </code>
   </td>
   <td>
    <code class="literal">
     INFORMATION
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     INFO
    </code>
   </td>
   <td>
    Provides information implicitly requested by the user, e.g., output from
    <code class="command">
     VACUUM VERBOSE
    </code>
    .
   </td>
   <td>
    <code class="literal">
     INFO
    </code>
   </td>
   <td>
    <code class="literal">
     INFORMATION
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     NOTICE
    </code>
   </td>
   <td>
    Provides information that might be helpful to users, e.g., notice of truncation of long identifiers.
   </td>
   <td>
    <code class="literal">
     NOTICE
    </code>
   </td>
   <td>
    <code class="literal">
     INFORMATION
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     WARNING
    </code>
   </td>
   <td>
    Provides warnings of likely problems, e.g.,
    <code class="command">
     COMMIT
    </code>
    outside a transaction block.
   </td>
   <td>
    <code class="literal">
     NOTICE
    </code>
   </td>
   <td>
    <code class="literal">
     WARNING
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ERROR
    </code>
   </td>
   <td>
    Reports an error that caused the current command to abort.
   </td>
   <td>
    <code class="literal">
     WARNING
    </code>
   </td>
   <td>
    <code class="literal">
     ERROR
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LOG
    </code>
   </td>
   <td>
    Reports information of interest to administrators, e.g., checkpoint activity.
   </td>
   <td>
    <code class="literal">
     INFO
    </code>
   </td>
   <td>
    <code class="literal">
     INFORMATION
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     FATAL
    </code>
   </td>
   <td>
    Reports an error that caused the current session to abort.
   </td>
   <td>
    <code class="literal">
     ERR
    </code>
   </td>
   <td>
    <code class="literal">
     ERROR
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     PANIC
    </code>
   </td>
   <td>
    Reports an error that caused all database sessions to abort.
   </td>
   <td>
    <code class="literal">
     CRIT
    </code>
   </td>
   <td>
    <code class="literal">
     ERROR
    </code>
   </td>
  </tr>
 </tbody>
</table>




### 19.8.3. What to Log [#](#RUNTIME-CONFIG-LOGGING-WHAT)

### Note

What you choose to log can have security implications; see [Section 24.3](logfile-maintenance.md "24.3. Log File Maintenance").

`application_name` (`string`) [#](#GUC-APPLICATION-NAME): The `application_name` can be any string of less than `NAMEDATALEN` characters (64 characters in a standard build). It is typically set by an application upon connection to the server. The name will be displayed in the `pg_stat_activity` view and included in CSV log entries. It can also be included in regular log entries via the [log_line_prefix](runtime-config-logging.md#GUC-LOG-LINE-PREFIX) parameter. Only printable ASCII characters may be used in the `application_name` value. Other characters are replaced with [C-style hexadecimal escapes](sql-syntax-lexical.md#SQL-SYNTAX-STRINGS-ESCAPE "4.1.2.2. String Constants with C-Style Escapes").

`debug_print_parse` (`boolean`) `debug_print_rewritten` (`boolean`) `debug_print_plan` (`boolean`) [#](#GUC-DEBUG-PRINT-PARSE): These parameters enable various debugging output to be emitted. When set, they print the resulting parse tree, the query rewriter output, or the execution plan for each executed query. These messages are emitted at `LOG` message level, so by default they will appear in the server log but will not be sent to the client. You can change that by adjusting [client_min_messages](runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES) and/or [log_min_messages](runtime-config-logging.md#GUC-LOG-MIN-MESSAGES). These parameters are off by default.

`debug_pretty_print` (`boolean`) [#](#GUC-DEBUG-PRETTY-PRINT): When set, `debug_pretty_print` indents the messages produced by `debug_print_parse`, `debug_print_rewritten`, or `debug_print_plan`. This results in more readable but much longer output than the “compact” format used when it is off. It is on by default.

`log_autovacuum_min_duration` (`integer`) [#](#GUC-LOG-AUTOVACUUM-MIN-DURATION): Causes each action executed by autovacuum to be logged if it ran for at least the specified amount of time. Setting this to zero logs all autovacuum actions. `-1` disables logging autovacuum actions. If this value is specified without units, it is taken as milliseconds. For example, if you set this to `250ms` then all automatic vacuums and analyzes that run 250ms or longer will be logged. In addition, when this parameter is set to any value other than `-1`, a message will be logged if an autovacuum action is skipped due to a conflicting lock or a concurrently dropped relation. The default is `10min`. Enabling this parameter can be helpful in tracking autovacuum activity. This parameter can only be set in the `postgresql.conf` file or on the server command line; but the setting can be overridden for individual tables by changing table storage parameters.

`log_checkpoints` (`boolean`) [#](#GUC-LOG-CHECKPOINTS): Causes checkpoints and restartpoints to be logged in the server log. Some statistics are included in the log messages, including the number of buffers written and the time spent writing them. This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is on.

`log_connections` (`string`) [#](#GUC-LOG-CONNECTIONS): Causes aspects of each connection to the server to be logged. The default is the empty string, `''`, which disables all connection logging. The following options may be specified alone or in a comma-separated list:

**Table 19.3. Log Connection Options**

    

<table border="1" class="table" summary="Log Connection Options">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Name
   </th>
   <th>
    Description
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     receipt
    </code>
   </td>
   <td>
    Logs receipt of a connection.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     authentication
    </code>
   </td>
   <td>
    Logs the original identity used by an authentication method to identify a user. In most cases, the identity string matches the
    <span class="productname">
     PostgreSQL
    </span>
    username, but some third-party authentication methods may alter the original user identifier before the server stores it. Failed authentication is always logged regardless of the value of this setting.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     authorization
    </code>
   </td>
   <td>
    Logs successful completion of authorization. At this point the connection has been established but the backend is not yet fully set up. The log message includes the authorized username as well as the database name and application name, if applicable.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     setup_durations
    </code>
   </td>
   <td>
    Logs the time spent establishing the connection and setting up the backend until the connection is ready to execute its first query. The log message includes three durations:  the total setup duration (starting from the postmaster accepting the incoming connection and ending when the connection is ready for query), the time it took to fork the new backend, and the time it took to authenticate the user.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     all
    </code>
   </td>
   <td>
    A convenience alias equivalent to specifying all options. If
    <code class="literal">
     all
    </code>
    is specified in a list of other
            options, all connection aspects will be logged.
   </td>
  </tr>
 </tbody>
</table>




      

    Disconnection logging is separately controlled by [log_disconnections](runtime-config-logging.md#GUC-LOG-DISCONNECTIONS).

    For the purposes of backwards compatibility, `on`, `off`, `true`, `false`, `yes`, `no`, `1`, and `0` are still supported. The positive values are equivalent to specifying the `receipt`, `authentication`, and `authorization` options.

    Only superusers and users with the appropriate `SET` privilege can change this parameter at session start, and it cannot be changed at all within a session.

    ### Note

    Some client programs, like psql, attempt to connect twice while determining if a password is required, so duplicate “connection received” messages do not necessarily indicate a problem.

`log_disconnections` (`boolean`) [#](#GUC-LOG-DISCONNECTIONS): Causes session terminations to be logged. The log output provides information similar to `log_connections`, plus the duration of the session. Only superusers and users with the appropriate `SET` privilege can change this parameter at session start, and it cannot be changed at all within a session. The default is `off`.

`log_duration` (`boolean`) [#](#GUC-LOG-DURATION): Causes the duration of every completed statement to be logged. The default is `off`. Only superusers and users with the appropriate `SET` privilege can change this setting.

For clients using extended query protocol, durations of the Parse, Bind, and Execute steps are logged independently.

### Note

The difference between enabling `log_duration` and setting [log_min_duration_statement](runtime-config-logging.md#GUC-LOG-MIN-DURATION-STATEMENT) to zero is that exceeding `log_min_duration_statement` forces the text of the query to be logged, but this option doesn't. Thus, if `log_duration` is `on` and `log_min_duration_statement` has a positive value, all durations are logged but the query text is included only for statements exceeding the threshold. This behavior can be useful for gathering statistics in high-load installations.

`log_error_verbosity` (`enum`) [#](#GUC-LOG-ERROR-VERBOSITY): Controls the amount of detail written in the server log for each message that is logged. Valid values are `TERSE`, `DEFAULT`, and `VERBOSE`, each adding more fields to displayed messages. `TERSE` excludes the logging of `DETAIL`, `HINT`, `QUERY`, and `CONTEXT` error information. `VERBOSE` output includes the `SQLSTATE` error code (see also [Appendix A](errcodes-appendix.md "Appendix A. PostgreSQL Error Codes")) and the source code file name, function name, and line number that generated the error. Only superusers and users with the appropriate `SET` privilege can change this setting.

`log_hostname` (`boolean`) [#](#GUC-LOG-HOSTNAME): By default, connection log messages only show the IP address of the connecting host. Turning this parameter on causes logging of the host name as well. Note that depending on your host name resolution setup this might impose a non-negligible performance penalty. This parameter can only be set in the `postgresql.conf` file or on the server command line.

`log_line_prefix` (`string`) [#](#GUC-LOG-LINE-PREFIX): This is a `printf`-style string that is output at the beginning of each log line. `%` characters begin “escape sequences” that are replaced with status information as outlined below. Unrecognized escapes are ignored. Other characters are copied straight to the log line. Some escapes are only recognized by session processes, and will be treated as empty by background processes such as the main server process. Status information may be aligned either left or right by specifying a numeric literal after the % and before the option. A negative value will cause the status information to be padded on the right with spaces to give it a minimum width, whereas a positive value will pad on the left. Padding can be useful to aid human readability in log files.

This parameter can only be set in the `postgresql.conf` file or on the server command line. The default is `'%m [%p] '` which logs a time stamp and the process ID.

    

<table border="1" class="informaltable">
 <colgroup>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Escape
   </th>
   <th>
    Effect
   </th>
   <th>
    Session only
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     %a
    </code>
   </td>
   <td>
    Application name
   </td>
   <td>
    yes
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %u
    </code>
   </td>
   <td>
    User name
   </td>
   <td>
    yes
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %d
    </code>
   </td>
   <td>
    Database name
   </td>
   <td>
    yes
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %r
    </code>
   </td>
   <td>
    Remote host name or IP address, and remote port
   </td>
   <td>
    yes
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %h
    </code>
   </td>
   <td>
    Remote host name or IP address
   </td>
   <td>
    yes
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %L
    </code>
   </td>
   <td>
    Local address (the IP address on the server that the
             client connected to)
   </td>
   <td>
    yes
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %b
    </code>
   </td>
   <td>
    Backend type
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %p
    </code>
   </td>
   <td>
    Process ID
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %P
    </code>
   </td>
   <td>
    Process ID of the parallel group leader, if this process is a parallel query worker
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %t
    </code>
   </td>
   <td>
    Time stamp without milliseconds
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %m
    </code>
   </td>
   <td>
    Time stamp with milliseconds
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %n
    </code>
   </td>
   <td>
    Time stamp with milliseconds (as a Unix epoch)
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %i
    </code>
   </td>
   <td>
    Command tag: type of session's current command
   </td>
   <td>
    yes
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %e
    </code>
   </td>
   <td>
    SQLSTATE error code
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %c
    </code>
   </td>
   <td>
    Session ID: see below
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %l
    </code>
   </td>
   <td>
    Number of the log line for each session or process, starting at 1
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %s
    </code>
   </td>
   <td>
    Process start time stamp
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %v
    </code>
   </td>
   <td>
    Virtual transaction ID (procNumber/localXID);  see
    <a class="xref" href="transaction-id.md" title="67.1. Transactions and Identifiers">
     Section 67.1
    </a>
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %x
    </code>
   </td>
   <td>
    Transaction ID (0 if none is assigned);  see
    <a class="xref" href="transaction-id.md" title="67.1. Transactions and Identifiers">
     Section 67.1
    </a>
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %q
    </code>
   </td>
   <td>
    Produces no output, but tells non-session
             processes to stop at this point in the string; ignored by session processes
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %Q
    </code>
   </td>
   <td>
    Query identifier of the current query.  Query identifiers are not computed by default, so this field will be zero unless
    <a class="xref" href="runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID">
     compute_query_id
    </a>
    parameter is enabled or a third-party module that computes query identifiers is configured.
   </td>
   <td>
    yes
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     %%
    </code>
   </td>
   <td>
    Literal
    <code class="literal">
     %
    </code>
   </td>
   <td>
    no
   </td>
  </tr>
 </tbody>
</table>




    The backend type corresponds to the column `backend_type` in the view [`pg_stat_activity`](monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW "27.2.3. pg_stat_activity"), but additional types can appear in the log that don't show in that view.

    The `%c` escape prints a quasi-unique session identifier, consisting of two 4-byte hexadecimal numbers (without leading zeros) separated by a dot. The numbers are the process start time and the process ID, so `%c` can also be used as a space saving way of printing those items. For example, to generate the session identifier from `pg_stat_activity`, use this query:

    ```
    SELECT to_hex(trunc(EXTRACT(EPOCH FROM backend_start))::integer) || '.' || to_hex(pid) FROM pg_stat_activity;
    ```

    ### Tip

    If you set a nonempty value for `log_line_prefix`, you should usually make its last character be a space, to provide visual separation from the rest of the log line. A punctuation character can be used too.

    ### Tip

    Syslog produces its own time stamp and process ID information, so you probably do not want to include those escapes if you are logging to syslog.

    ### Tip

    The `%q` escape is useful when including information that is only available in session (backend) context like user or database name. For example:

    ```
    log_line_prefix = '%m [%p] %q%u@%d/%a '
    ```

    ### Note

    The `%Q` escape always reports a zero identifier for lines output by [log_statement](runtime-config-logging.md#GUC-LOG-STATEMENT) because `log_statement` generates output before an identifier can be calculated, including invalid statements for which an identifier cannot be calculated.

`log_lock_waits` (`boolean`) [#](#GUC-LOG-LOCK-WAITS): Controls whether a log message is produced when a session waits longer than [deadlock_timeout](runtime-config-locks.md#GUC-DEADLOCK-TIMEOUT) to acquire a lock. This is useful in determining if lock waits are causing poor performance. The default is `off`. Only superusers and users with the appropriate `SET` privilege can change this setting.

`log_lock_failures` (`boolean`) [#](#GUC-LOG-LOCK-FAILURES): Controls whether a detailed log message is produced when a lock acquisition fails. This is useful for analyzing the causes of lock failures. Currently, only lock failures due to `SELECT NOWAIT` is supported. The default is `off`. Only superusers and users with the appropriate `SET` privilege can change this setting.

`log_recovery_conflict_waits` (`boolean`) [#](#GUC-LOG-RECOVERY-CONFLICT-WAITS): Controls whether a log message is produced when the startup process waits longer than `deadlock_timeout` for recovery conflicts. This is useful in determining if recovery conflicts prevent the recovery from applying WAL.

The default is `off`. This parameter can only be set in the `postgresql.conf` file or on the server command line.

`log_parameter_max_length` (`integer`) [#](#GUC-LOG-PARAMETER-MAX-LENGTH): If greater than zero, each bind parameter value logged with a non-error statement-logging message is trimmed to this many bytes. Zero disables logging of bind parameters for non-error statement logs. `-1` (the default) allows bind parameters to be logged in full. If this value is specified without units, it is taken as bytes. Only superusers and users with the appropriate `SET` privilege can change this setting.

This setting only affects log messages printed as a result of [log_statement](runtime-config-logging.md#GUC-LOG-STATEMENT), [log_duration](runtime-config-logging.md#GUC-LOG-DURATION), and related settings. Non-zero values of this setting add some overhead, particularly if parameters are sent in binary form, since then conversion to text is required.

`log_parameter_max_length_on_error` (`integer`) [#](#GUC-LOG-PARAMETER-MAX-LENGTH-ON-ERROR): If greater than zero, each bind parameter value reported in error messages is trimmed to this many bytes. Zero (the default) disables including bind parameters in error messages. `-1` allows bind parameters to be printed in full. If this value is specified without units, it is taken as bytes.

Non-zero values of this setting add overhead, as PostgreSQL will need to store textual representations of parameter values in memory at the start of each statement, whether or not an error eventually occurs. The overhead is greater when bind parameters are sent in binary form than when they are sent as text, since the former case requires data conversion while the latter only requires copying the string.

`log_statement` (`enum`) [#](#GUC-LOG-STATEMENT): Controls which SQL statements are logged. Valid values are `none` (off), `ddl`, `mod`, and `all` (all statements). `ddl` logs all data definition statements, such as `CREATE`, `ALTER`, and `DROP` statements. `mod` logs all `ddl` statements, plus data-modifying statements such as `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`, and `COPY FROM`. `PREPARE`, `EXECUTE`, and `EXPLAIN ANALYZE` statements are also logged if their contained command is of an appropriate type. For clients using extended query protocol, logging occurs when an Execute message is received, and values of the Bind parameters are included (with any embedded single-quote marks doubled).

The default is `none`. Only superusers and users with the appropriate `SET` privilege can change this setting.

### Note

Statements that contain simple syntax errors are not logged even by the `log_statement` = `all` setting, because the log message is emitted only after basic parsing has been done to determine the statement type. In the case of extended query protocol, this setting likewise does not log statements that fail before the Execute phase (i.e., during parse analysis or planning). Set `log_min_error_statement` to `ERROR` (or lower) to log such statements.

Logged statements might reveal sensitive data and even contain plaintext passwords.

`log_replication_commands` (`boolean`) [#](#GUC-LOG-REPLICATION-COMMANDS): Causes each replication command and `walsender` process's replication slot acquisition/release to be logged in the server log. See [Section 54.4](protocol-replication.md "54.4. Streaming Replication Protocol") for more information about replication command. The default value is `off`. Only superusers and users with the appropriate `SET` privilege can change this setting.

`log_temp_files` (`integer`) [#](#GUC-LOG-TEMP-FILES): Controls logging of temporary file names and sizes. Temporary files can be created for sorts, hashes, and temporary query results. If enabled by this setting, a log entry is emitted for each temporary file, with the file size specified in bytes, when it is deleted. A value of zero logs all temporary file information, while positive values log only files whose size is greater than or equal to the specified amount of data. If this value is specified without units, it is taken as kilobytes. The default setting is -1, which disables such logging. Only superusers and users with the appropriate `SET` privilege can change this setting.

`log_timezone` (`string`) [#](#GUC-LOG-TIMEZONE): Sets the time zone used for timestamps written in the server log. Unlike [TimeZone](runtime-config-client.md#GUC-TIMEZONE), this value is cluster-wide, so that all sessions will report timestamps consistently. The built-in default is `GMT`, but that is typically overridden in `postgresql.conf`; initdb will install a setting there corresponding to its system environment. See [Section 8.5.3](datatype-datetime.md#DATATYPE-TIMEZONES "8.5.3. Time Zones") for more information. This parameter can only be set in the `postgresql.conf` file or on the server command line.

### 19.8.4. Using CSV-Format Log Output [#](#RUNTIME-CONFIG-LOGGING-CSVLOG)

Including `csvlog` in the `log_destination` list provides a convenient way to import log files into a database table. This option emits log lines in comma-separated-values (CSV) format, with these columns: time stamp with milliseconds, user name, database name, process ID, client host:port number, session ID, per-session line number, command tag, session start time, virtual transaction ID, regular transaction ID, error severity, SQLSTATE code, error message, error message detail, hint, internal query that led to the error (if any), character count of the error position therein, error context, user query that led to the error (if any and enabled by `log_min_error_statement`), character count of the error position therein, location of the error in the PostgreSQL source code (if `log_error_verbosity` is set to `verbose`), application name, backend type, process ID of parallel group leader, and query id. Here is a sample table definition for storing CSV-format log output:

```
CREATE TABLE postgres_log ( log_time timestamp(3) with time zone, user_name text, database_name text, process_id integer, connection_from text, session_id text, session_line_num bigint, command_tag text, session_start_time timestamp with time zone, virtual_transaction_id text, transaction_id bigint, error_severity text, sql_state_code text, message text, detail text, hint text, internal_query text, internal_query_pos integer, context text, query text, query_pos integer, location text, application_name text, backend_type text, leader_pid integer, query_id bigint, PRIMARY KEY (session_id, session_line_num) );
```

To import a log file into this table, use the `COPY FROM` command:

```
COPY postgres_log FROM '/full/path/to/logfile.csv' WITH csv;
```

It is also possible to access the file as a foreign table, using the supplied [file_fdw](file-fdw.md "F.15. file_fdw — access data files in the server's file system") module.

There are a few things you need to do to simplify importing CSV log files:

1. Set `log_filename` and `log_rotation_age` to provide a consistent, predictable naming scheme for your log files. This lets you predict what the file name will be and know when an individual log file is complete and therefore ready to be imported.
2. Set `log_rotation_size` to 0 to disable size-based log rotation, as it makes the log file name difficult to predict.
3. Set `log_truncate_on_rotation` to `on` so that old log data isn't mixed with the new in the same file.
4. The table definition above includes a primary key specification. This is useful to protect against accidentally importing the same information twice. The `COPY` command commits all of the data it imports at one time, so any error will cause the entire import to fail. If you import a partial log file and later import the file again when it is complete, the primary key violation will cause the import to fail. Wait until the log is complete and closed before importing. This procedure will also protect against accidentally importing a partial line that hasn't been completely written, which would also cause `COPY` to fail.

### 19.8.5. Using JSON-Format Log Output [#](#RUNTIME-CONFIG-LOGGING-JSONLOG)

Including `jsonlog` in the `log_destination` list provides a convenient way to import log files into many different programs. This option emits log lines in JSON format.

String fields with null values are excluded from output. Additional fields may be added in the future. User applications that process `jsonlog` output should ignore unknown fields.

Each log line is serialized as a JSON object with the set of keys and their associated values shown in [Table 19.4](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-JSONLOG-KEYS-VALUES "Table 19.4. Keys and Values of JSON Log Entries").

**Table 19.4. Keys and Values of JSON Log Entries**



<table border="1" class="table" summary="Keys and Values of JSON Log Entries">
 <colgroup>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Key name
   </th>
   <th>
    Type
   </th>
   <th>
    Description
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     timestamp
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Time stamp with milliseconds
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     user
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    User name
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     dbname
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Database name
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     pid
    </code>
   </td>
   <td>
    number
   </td>
   <td>
    Process ID
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     remote_host
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Client host
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     remote_port
    </code>
   </td>
   <td>
    number
   </td>
   <td>
    Client port
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     session_id
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Session ID
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     line_num
    </code>
   </td>
   <td>
    number
   </td>
   <td>
    Per-session line number
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ps
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Current ps display
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     session_start
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Session start time
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     vxid
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Virtual transaction ID
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     txid
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Regular transaction ID
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     error_severity
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Error severity
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     state_code
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    SQLSTATE code
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     message
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Error message
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     detail
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Error message detail
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     hint
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Error message hint
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     internal_query
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Internal query that led to the error
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     internal_position
    </code>
   </td>
   <td>
    number
   </td>
   <td>
    Cursor index into internal query
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     context
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Error context
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     statement
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Client-supplied query string
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     cursor_position
    </code>
   </td>
   <td>
    number
   </td>
   <td>
    Cursor index into query string
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     func_name
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Error location function name
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     file_name
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    File name of error location
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     file_line_num
    </code>
   </td>
   <td>
    number
   </td>
   <td>
    File line number of the error location
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     application_name
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Client application name
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     backend_type
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Type of backend
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     leader_pid
    </code>
   </td>
   <td>
    number
   </td>
   <td>
    Process ID of leader for active parallel workers
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     query_id
    </code>
   </td>
   <td>
    number
   </td>
   <td>
    Query ID
   </td>
  </tr>
 </tbody>
</table>




### 19.8.6. Process Title [#](#RUNTIME-CONFIG-LOGGING-PROC-TITLE)

These settings control how process titles of server processes are modified. Process titles are typically viewed using programs like ps or, on Windows, Process Explorer. See [Section 27.1](monitoring-ps.md "27.1. Standard Unix Tools") for details.

`cluster_name` (`string`) [#](#GUC-CLUSTER-NAME): Sets a name that identifies this database cluster (instance) for various purposes. The cluster name appears in the process title for all server processes in this cluster. Moreover, it is the default application name for a standby connection (see [synchronous_standby_names](runtime-config-replication.md#GUC-SYNCHRONOUS-STANDBY-NAMES)).

The name can be any string of less than `NAMEDATALEN` characters (64 characters in a standard build). Only printable ASCII characters may be used in the `cluster_name` value. Other characters are replaced with [C-style hexadecimal escapes](sql-syntax-lexical.md#SQL-SYNTAX-STRINGS-ESCAPE "4.1.2.2. String Constants with C-Style Escapes"). No name is shown if this parameter is set to the empty string `''` (which is the default). This parameter can only be set at server start.

`update_process_title` (`boolean`) [#](#GUC-UPDATE-PROCESS-TITLE): Enables updating of the process title every time a new SQL command is received by the server. This setting defaults to `on` on most platforms, but it defaults to `off` on Windows due to that platform's larger overhead for updating the process title. Only superusers and users with the appropriate `SET` privilege can change this setting.
