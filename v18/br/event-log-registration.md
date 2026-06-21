## 18.12. Registro do Registro de Eventos no Windows [#](#EVENT-LOG-REGISTRATION)

Para registrar uma biblioteca de registro de eventos do Windows com o sistema operacional, execute este comando:

```
regsvr32 pgsql_library_directory/pgevent.dll
```

Isso cria entradas de registro usadas pelo Assistente de eventos, sob a fonte de evento padrão denominada `PostgreSQL`.

Para especificar um nome de fonte de evento diferente (consulte [event_source][(runtime-config-logging.md#GUC-EVENT-SOURCE)]), use as opções `/n` e `/i`:

```
regsvr32 /n /i:event_source_name pgsql_library_directory/pgevent.dll
```

Para desinscrever a biblioteca do registro de eventos do sistema operacional, execute este comando:

```
regsvr32 /u [/i:event_source_name] pgsql_library_directory/pgevent.dll
```

### Nota

Para habilitar o registro de eventos no servidor de banco de dados, modifique [log_destination][(runtime-config-logging.md#GUC-LOG-DESTINATION)] para incluir `eventlog` em `postgresql.conf`.