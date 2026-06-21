## 32.18. Pesquisa LDAP de Parâmetros de Conexão [#](#LIBPQ-LDAP)

Se o libpq foi compilado com suporte LDAP (opção `--with-ldap` para `configure`) é possível recuperar opções de conexão como `host` ou `dbname` via LDAP de um servidor central. A vantagem é que, se os parâmetros de conexão de um banco de dados forem alterados, as informações de conexão não precisam ser atualizadas em todas as máquinas cliente.

A busca de parâmetros de conexão LDAP utiliza o arquivo de serviço de conexão `pg_service.conf` (consulte [Seção 32.17][(libpq-pgservice.md "32.17. The Connection Service File")]). Uma linha em uma estrofe de `pg_service.conf` que começa com `ldap://` será reconhecida como um URL LDAP e uma consulta LDAP será realizada. O resultado deve ser uma lista de pares de `keyword = value` que serão usados para definir as opções de conexão. O URL deve conformar-se com [RFC 1959][(https://datatracker.ietf.org/doc/html/rfc1959)] e ter a forma

```
ldap://[hostname[:port]]/search_base?attribute?search_scope?filter
```

onde *`hostname`* é padrão para `localhost` e *`port`* é padrão para 389.

O processamento do `pg_service.conf` é finalizado após uma busca bem-sucedida no LDAP, mas é continuado se o servidor LDAP não puder ser contatado. Isso é para fornecer uma opção de fallback com mais linhas de URL LDAP que apontam para diferentes servidores LDAP, pares clássicos do `keyword = value` ou opções de conexão padrão. Se você prefere receber uma mensagem de erro neste caso, adicione uma linha sintaticamente incorreta após a URL do LDAP.

Uma entrada LDAP de amostra que foi criada com o arquivo LDIF

```
version:1
dn:cn=mydatabase,dc=mycompany,dc=com
changetype:add
objectclass:top
objectclass:device
cn:mydatabase
description:host=dbserver.mycompany.com
description:port=5439
description:dbname=mydb
description:user=mydb_user
description:sslmode=require
```

pode ser consultada com o seguinte URL LDAP:

```
ldap://ldap.mycompany.com/dc=mycompany,dc=com?description?one?(cn=mydatabase)
```

Você também pode misturar entradas de arquivo de serviço regulares com consultas LDAP. Um exemplo completo para uma estrofe em `pg_service.conf` seria:

```
# only host and port are stored in LDAP, specify dbname and user explicitly
[customerdb]
dbname=customer
user=appuser
ldap://ldap.acme.com/cn=dbserver,cn=hosts?pgconnectinfo?base?(objectclass=*)
```
