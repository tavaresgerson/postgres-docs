## F.11. dblink — conectar-se a outros bancos de dados PostgreSQL [#](#DBLINK)

* [dblink_connect](contrib-dblink-connect.md) — abre uma conexão persistente em um banco de dados remoto
* [dblink_connect_u](contrib-dblink-connect-u.md) — abre uma conexão persistente em um banco de dados remoto, de forma insegura
* [dblink_disconnect](contrib-dblink-disconnect.md) — fecha uma conexão persistente em um banco de dados remoto
* [dblink](contrib-dblink-function.md) — executa uma consulta em um banco de dados remoto
* [dblink_exec](contrib-dblink-exec.md) — executa um comando em um banco de dados remoto
* [dblink_open](contrib-dblink-open.md) — abre um cursor em um banco de dados remoto
* [dblink_fetch](contrib-dblink-fetch.md) — retorna linhas de um cursor aberto em um banco de dados remoto
* [dblink_close](contrib-dblink-close.md) — fecha um cursor em um banco de dados remoto
* [dblink_get_connections](contrib-dblink-get-connections.md) — retorna os nomes de todas as conexões de dblink abertas
* [dblink_error_message](contrib-dblink-error-message.md) — obtém a última mensagem de erro na conexão nomeada
* [dblink_send_query](contrib-dblink-send-query.md) — envia uma consulta assíncrona para um banco de dados remoto
* [dblink_is_busy](contrib-dblink-is-busy.md) — verifica se a conexão está ocupada com uma consulta assíncrona
* [dblink_get_notify](contrib-dblink-get-notify.md) — recupera notificações assíncronas em uma conexão
* [dblink_get_result](contrib-dblink-get-result.md) — obtém o resultado de uma consulta assíncrona
* [dblink_cancel_query](contrib-dblink-cancel-query.md) — cancela qualquer consulta ativa na conexão nomeada
* [dblink_get_pkey](contrib-dblink-get-pkey.md) — retorna as posições e os nomes dos campos da chave primária de uma relação
* [dblink_build_sql_insert](contrib-dblink-build-sql-insert.md) — constrói uma declaração INSERT usando uma tupla local, substituindo os valores do campo da chave primária pelos valores alternativos fornecidos
* [dblink_build_sql_delete](contrib-dblink-build-sql-delete.md) — constrói uma declaração DELETE usando os valores fornecidos para os campos da chave primária
* [dblink_build_sql_update](contrib-dblink-build-sql-update.md) — constrói uma declaração UPDATE usando uma tupla local, substituindo os valores do campo da chave primária pelos valores alternativos fornecidos

`dblink` é um módulo que suporta conexões a outros bancos de dados PostgreSQL dentro de uma sessão de banco de dados.

`dblink` pode relatar os seguintes eventos de espera sob o tipo de evento de espera `Extension`.

`DblinkConnect`: Aguardando a estabelecimento de uma conexão com um servidor remoto.

`DblinkGetConnect`: Esperando estabelecer uma conexão com um servidor remoto quando ele não foi encontrado na lista de conexões já abertas.

`DblinkGetResult`: Aguardando a recepção dos resultados de uma consulta de um servidor remoto.

Veja também [postgres_fdw][(postgres-fdw.md "F.38. postgres_fdw — access data stored in external PostgreSQL servers")], que oferece aproximadamente a mesma funcionalidade usando uma infraestrutura mais moderna e conforme com os padrões.