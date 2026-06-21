## 32.15. Variáveis de ambiente [#](#LIBPQ-ENVARS)

As seguintes variáveis de ambiente podem ser usadas para selecionar valores padrão de parâmetros de conexão, que serão usados por `PQconnectdb` (libpq-connect.md#LIBPQ-PQCONNECTDB), `PQsetdbLogin` (libpq-connect.md#LIBPQ-PQSETDBLOGIN) e `PQsetdb` (libpq-connect.md#LIBPQ-PQSETDB) se nenhum valor for especificado diretamente pelo código de chamada. Essas são úteis para evitar a codificação rígida da informação de conexão do banco de dados em aplicativos de cliente simples, por exemplo.

* `PGHOST` se comporta da mesma forma que o parâmetro de conexão [host](libpq-connect.md#LIBPQ-CONNECT-HOST)
* `PGSSLNEGOTIATION` se comporta da mesma forma que o parâmetro de conexão [sslnegotiation](libpq-connect.md#LIBPQ-CONNECT-SSLNEGOTIATION)
* `PGHOSTADDR` se comporta da mesma forma que o parâmetro de conexão [hostaddr](libpq-connect.md#LIBPQ-CONNECT-HOSTADDR) Este pode ser definido em vez de ou adicionalmente a `PGHOST` para evitar o overhead da pesquisa DNS.
* `PGPORT` se comporta da mesma forma que o parâmetro de conexão [port](libpq-connect.md#LIBPQ-CONNECT-PORT)
* `PGDATABASE` se comporta da mesma forma que o parâmetro de conexão [dbname](libpq-connect.md#LIBPQ-CONNECT-DBNAME)
* `PGUSER` se comporta da mesma forma que o parâmetro de conexão [user](libpq-connect.md#LIBPQ-CONNECT-USER)
* `PGPASSWORD` se comporta da mesma forma que o parâmetro de conexão [password](libpq-connect.md#LIBPQ-CONNECT-PASSWORD) O uso desta variável de ambiente não é recomendado por razões de segurança, pois alguns sistemas operacionais permitem que usuários não root vejam variáveis de ambiente de processo via ps; em vez disso, considere usar um arquivo de senha (consulte [Seção 32.16](libpq-pgpass.md "32.16. The Password File"))
* `PGPASSFILE` se comporta da mesma forma que o parâmetro de conexão [passfile](libpq-connect.md#LIBPQ-CONNECT-PASSFILE)
* `PGREQUIREAUTH` se comporta da mesma forma que o parâmetro de conexão [require_auth](libpq-connect.md#LIBPQ-CONNECT-REQUIRE-AUTH)
* `PGCHANNELBINDING` se comporta da mesma forma que o parâmetro de conexão [channel_binding](libpq-connect.md#LIBPQ-CONNECT-CHANNEL-BINDING)
* `PGSERVICE` se comporta da mesma forma que o parâmetro de conexão [service](libpq-connect.md#LIBPQ-CONNECT-SERVICE)
* `PGSERVICEFILE` especifica o nome do arquivo de serviço de conexão por usuário (consulte [Seção 32.17](libpq-pgservice.md "32.17. The Connection Service File"))
* `PGOPTIONS` se comporta da mesma forma que o parâmetro de conexão [options](libpq-connect.md#LIBPQ-CONNECT-OPTIONS)
* `PGAPPNAME` se comporta da mesma forma que o parâmetro de conexão [application_name](libpq-connect.md#LIBPQ-CONNECT-APPLICATION-NAME)
* `PGSSLMODE` se comporta da mesma forma que o parâmetro de conexão [sslmode](libpq-connect.md#LIBPQ-CONNECT-SSLMODE)
* `PGREQUIRESSL` se comporta da mesma forma que o parâmetro de conexão [requiressl](libpq-connect.md#LIBPQ-CONNECT-REQUIRESSL) Esta variável de ambiente é desatualizada em favor da variável `PGSSLMODE`; definir ambas as variáveis suprime o efeito desta.
* `PGSSLCOMPRESSION` se comporta da mesma forma que o parâmetro de conexão [sslcompression](libpq-connect.md#LIBPQ-CONNECT-SSLCOMPRESSION)
* `PGSSLCERT` se comporta da mesma forma que o parâmetro de conexão [sslcert](libpq-connect.md#LIBPQ-CONNECT-SSLCERT)
* `PGSSLKEY` se comporta da mesma forma que o parâmetro de conexão [sslkey](libpq-connect.md#LIBPQ-CONNECT-SSLKEY)
* `PGSSLCERTMODE` se comporta da mesma forma que o parâmetro de conexão [sslcertmode](libpq-connect.md#LIBPQ-CONNECT-SSLCERTMODE)
* `PGSSLROOTCERT` se comporta da mesma forma que o parâmetro de conexão [sslrootcert](libpq-connect.md#LIBPQ-CONNECT-SSLROOTCERT)
* `PGSSLCRL` se comporta da mesma forma que o parâmetro de conexão [sslcrl](libpq-connect.md#LIBPQ-CONNECT-SSLCRL)
* `PGSSLCRLDIR` se comporta da mesma forma que o parâmetro de conexão [sslcrldir](libpq-connect.md#LIBPQ-CONNECT-SSLCRLDIR)
* `PGSSLSNI` se comporta da mesma forma que o parâmetro de conexão [sslsni](libpq-connect.md#LIBPQ-CONNECT-SSLSNI)
* `PGREQUIREPEER` se comporta da mesma forma que o parâmetro de conexão [requirepeer](libpq-connect.md#LIBPQ-CONNECT-REQUIREPEER)
* `PGSSLMINPROTOCOLVERSION` se comporta da mesma forma que o parâmetro de conexão [ssl_min_protocol_version](libpq-connect.md#LIBPQ-CONNECT-SSL-MIN-PROTOCOL-VERSION)
* `PGSSLMAXPROTOCOLVERSION` se comporta da mesma forma que o parâmetro de conexão [ssl_max_protocol_version](libpq-connect.md#LIBPQ-CONNECT-SSL-MAX-PROTOCOL-VERSION)
* `PGGSSENCMODE` se comporta da mesma forma que o parâmetro de conexão [gssencmode](libpq-connect.md#LIBPQ-CONNECT-GSSENCMODE)
* `PGKRBSRVNAME` se comporta da mesma forma que o parâmetro de conexão [krbsrvname](libpq-connect.md#LIBPQ-CONNECT-KRBSRVNAME)
* `PGGSSLIB` se comporta da mesma forma que o parâmetro de conexão [gsslib](libpq-connect.md#LIBPQ-CONNECT-GSSLIB)
* `PGGSSDELEGATION` se comporta da mesma forma que o parâmetro de conexão [gssdelegation](libpq-connect.md#LIBPQ-CONNECT-GSSDELEGATION)
* `PGCONNECT_TIMEOUT` se comporta da mesma forma que o parâmetro de conexão [connect_timeout](libpq-connect.md#LIBPQ-CONNECT-CONNECT-TIMEOUT)
* `PGCLIENTENCODING` se comporta da mesma forma que o parâmetro de conexão [client_encoding](libpq-connect.md#LIBPQ-CONNECT-CLIENT-ENCODING)
* `PGTARGETSESSIONATTRS` se comporta da mesma forma que o parâmetro de conexão [target_session_attrs](libpq-connect.md#LIBPQ-CONNECT-TARGET-SESSION-ATTRS)
* `PGLOADBALANCEHOSTS` se comporta da mesma forma que o parâmetro de conexão [load_balance_hosts](libpq-connect.md#LIBPQ-CONNECT-LOAD-BALANCE-HOSTS)
* `PGMINPROTOCOLVERSION` se comporta da mesma forma que o parâmetro de conexão [min_protocol_version](libpq-connect.md#LIBPQ-CONNECT-MIN-PROTOCOL-VERSION)
* `PGMAXPROTOCOLVERSION` se comporta da mesma forma que o parâmetro de conexão [max_protocol_version](libpq-connect.md#LIBPQ-CONNECT-MAX-PROTOCOL-VERSION)

As seguintes variáveis de ambiente podem ser usadas para especificar o comportamento padrão para cada sessão do PostgreSQL. (Veja também os comandos [ALTER ROLE](sql-alterrole.md "ALTER ROLE") e [ALTER DATABASE](sql-alterdatabase.md "ALTER DATABASE") para formas de definir o comportamento padrão em uma base por usuário ou por banco de dados.)

* `PGDATESTYLE` define o estilo padrão de representação de data/hora. (Equivalente a `SET datestyle TO ...`.)
* `PGTZ` define o fuso horário padrão. (Equivalente a `SET timezone TO ...`.)
* `PGGEQO` define o modo padrão para o otimizador de consulta genética. (Equivalente a `SET geqo TO ...`.)

Consulte o comando SQL [SET](sql-set.md "SET") para obter informações sobre os valores corretos dessas variáveis de ambiente.

As seguintes variáveis de ambiente determinam o comportamento interno do libpq; elas substituem os valores padrão compilados.

* `PGSYSCONFDIR` define o diretório que contém o arquivo `pg_service.conf` e, em uma versão futura, possivelmente outros arquivos de configuração para todo o sistema.
* `PGLOCALEDIR` define o diretório que contém os arquivos `locale` para a localização de mensagens.