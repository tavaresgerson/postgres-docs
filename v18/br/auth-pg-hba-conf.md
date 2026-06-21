## 20.1. O arquivo `pg_hba.conf` [#](#AUTH-PG-HBA-CONF)

A autenticação do cliente é controlada por um arquivo de configuração, que tradicionalmente é chamado de `pg_hba.conf` e é armazenado no diretório de dados do clúster de banco de dados. (HBA significa autenticação baseada em host.) Um arquivo padrão `pg_hba.conf` é instalado quando o diretório de dados é inicializado por [initdb](app-initdb.md "initdb"). É possível colocar o arquivo de configuração de autenticação em outro lugar, no entanto; veja o parâmetro de configuração [hba_file](runtime-config-file-locations.md#GUC-HBA-FILE).

O arquivo `pg_hba.conf` é lido ao iniciar o sistema e quando o processo do servidor principal recebe um sinal SIGHUP. Se você editar o arquivo em um sistema ativo, você precisará sinalizar o postmaster (usando `pg_ctl reload`, chamando a função SQL `pg_reload_conf()`, ou usando `kill -HUP`) para fazer com que ele leia o arquivo novamente.

### Nota

A afirmação anterior não é verdadeira no Microsoft Windows: lá, quaisquer alterações no arquivo `pg_hba.conf` são aplicadas imediatamente pelas novas conexões subsequentes.

A visualização do sistema `pg_hba_file_rules`(view-pg-hba-file-rules.md "53.10. pg_hba_file_rules") pode ser útil para testar prévia as alterações no arquivo `pg_hba.conf`, ou para diagnosticar problemas se o carregamento do arquivo não tiver tido os efeitos desejados. As linhas da visualização com campos `error` não nulos indicam problemas nas linhas correspondentes do arquivo.

O formato geral do arquivo `pg_hba.conf` é um conjunto de registros, um por linha. Linhas em branco são ignoradas, assim como qualquer texto após o caractere de comentário `#`. Um registro pode ser continuado na linha seguinte terminando a linha com uma barra invertida. (Barras invertidas não são especiais, exceto no final de uma linha.) Um registro é composto por vários campos que são separados por espaços e/ou tabs. Os campos podem conter espaço em branco se o valor do campo for citado duplamente. Citar um dos termos-chave em um campo de banco de dados, usuário ou endereço (por exemplo, `all` ou `replication`) faz com que a palavra perca seu significado especial e apenas corresponda a um banco de dados, usuário ou host com esse nome. A continuação de linha com barra invertida se aplica mesmo dentro do texto citado ou comentários.

Cada registro de autenticação especifica um tipo de conexão, uma faixa de endereço IP do cliente (se relevante para o tipo de conexão), um nome de banco de dados, um nome de usuário e o método de autenticação a ser usado para conexões que correspondem a esses parâmetros. O primeiro registro com um tipo de conexão correspondente, endereço IP do cliente, banco de dados solicitado e nome de usuário é usado para realizar a autenticação. Não há "transbordamento" ou "backup": se um registro é escolhido e a autenticação falha, os registros subsequentes não são considerados. Se nenhum registro corresponder, o acesso é negado.

Cada registro pode ser uma directiva de inclusão ou um registro de autenticação. As diretivas de inclusão especificam os arquivos que podem ser incluídos, que contêm registros adicionais. Os registros serão inseridos no lugar das diretivas de inclusão. As diretivas de inclusão contêm apenas dois campos: `include`, `include_if_exists` ou `include_dir` e o arquivo ou diretório a ser incluído. O arquivo ou diretório pode ser um caminho relativo ou absoluto e pode ser citado duplamente. Para o formulário `include_dir`, todos os arquivos que não começam com um `.` e terminam com `.conf` serão incluídos. Múltiplos arquivos dentro de um diretório de inclusão são processados em ordem de nome de arquivo (de acordo com as regras do C locale, ou seja, números antes de letras e letras maiúsculas antes de minúsculas).

Um registro pode ter vários formatos:

```
local               database  user  auth-method [auth-options]
host                database  user  address     auth-method  [auth-options]
hostssl             database  user  address     auth-method  [auth-options]
hostnossl           database  user  address     auth-method  [auth-options]
hostgssenc          database  user  address     auth-method  [auth-options]
hostnogssenc        database  user  address     auth-method  [auth-options]
host                database  user  IP-address  IP-mask      auth-method  [auth-options]
hostssl             database  user  IP-address  IP-mask      auth-method  [auth-options]
hostnossl           database  user  IP-address  IP-mask      auth-method  [auth-options]
hostgssenc          database  user  IP-address  IP-mask      auth-method  [auth-options]
hostnogssenc        database  user  IP-address  IP-mask      auth-method  [auth-options]
include             file
include_if_exists   file
include_dir         directory
```

O significado dos campos é o seguinte:

`local`: Este registro corresponde a tentativas de conexão usando sockets de domínio Unix. Sem um registro desse tipo, as conexões de socket de domínio Unix são desaconselhadas.

`host`: Este registro corresponde às tentativas de conexão feitas usando TCP/IP. Os registros `host` correspondem a tentativas de conexão SSL ou não SSL, bem como tentativas de conexão criptografadas GSSAPI ou não criptografadas GSSAPI.

### Nota

As conexões remotas TCP/IP não serão possíveis, a menos que o servidor seja iniciado com um valor apropriado para o parâmetro de configuração [listen_addresses][(runtime-config-connection.md#GUC-LISTEN-ADDRESSES)], uma vez que o comportamento padrão é ouvir conexões TCP/IP apenas no endereço local de bucle `localhost`.

`hostssl`: Este registro corresponde a tentativas de conexão feitas usando TCP/IP, mas apenas quando a conexão é feita com criptografia SSL.

Para utilizar essa opção, o servidor deve ser construído com suporte SSL. Além disso, o SSL deve ser habilitado definindo o parâmetro de configuração [ssl][(runtime-config-connection.md#GUC-SSL)] (consulte [Seção 18.9][(ssl-tcp.md "18.9. Secure TCP/IP Connections with SSL")] para obter mais informações). Caso contrário, o registro `hostssl` é ignorado, exceto para registrar um aviso de que ele não pode corresponder a nenhuma conexão.

`hostnossl`: Este tipo de registro tem comportamento oposto ao de `hostssl`; ele só corresponde a tentativas de conexão feitas por meio de TCP/IP que não utilizam SSL.

`hostgssenc`: Este registro corresponde a tentativas de conexão feitas usando TCP/IP, mas apenas quando a conexão é feita com criptografia GSSAPI.

Para utilizar essa opção, o servidor deve ser construído com suporte ao GSSAPI. Caso contrário, o registro `hostgssenc` é ignorado, exceto para registrar um aviso de que ele não pode corresponder a nenhuma conexão.

`hostnogssenc`: Este tipo de registro tem comportamento oposto ao de `hostgssenc`; ele só corresponde a tentativas de conexão feitas por meio de TCP/IP que não utilizam criptografia GSSAPI.

*`database`*: Especifica qual(is) nome(s) do banco de dados este registro corresponde. O valor `all` especifica que corresponde a todos os bancos de dados. O valor `sameuser` especifica que o registro corresponde se o banco de dados solicitado tiver o mesmo nome que o usuário solicitado. O valor `samerole` especifica que o usuário solicitado deve ser membro do papel com o mesmo nome que o banco de dados solicitado. (`samegroup` é uma ortografia obsoleta, mas ainda aceita, de `samerole`.) Superusuários não são considerados membros de um papel para os propósitos de `samerole`, a menos que sejam membros explícitos do papel, diretamente ou indiretamente, e não apenas em virtude de serem superusuários. O valor `replication` especifica que o registro corresponde se uma conexão de replicação física for solicitada, no entanto, não corresponde com conexões de replicação lógica. Note que as conexões de replicação física não especificam nenhum banco de dados particular, enquanto as conexões de replicação lógica especificam. Caso contrário, este é o nome de um banco de dados PostgreSQL específico ou uma expressão regular. Múltiplos nomes de banco de dados e/ou expressões regulares podem ser fornecidos, separando-os com vírgulas.

Se o nome do banco de dados começar com um traço (`/`), o restante do nome é tratado como uma expressão regular. (Consulte a [Seção 9.7.3.1][(functions-matching.md#POSIX-SYNTAX-DETAILS "9.7.3.1. Regular Expression Details")] para obter detalhes sobre a sintaxe de expressão regular do PostgreSQL.)

Um arquivo separado contendo nomes de bancos de dados e/ou expressões regulares pode ser especificado precedendo o nome do arquivo com `@`.

*`user`*: Especifica qual(is) nome(s) de usuário(s) do banco de dados este registro corresponde. O valor `all` especifica que corresponde a todos os usuários. Caso contrário, este é o nome de um usuário específico do banco de dados, uma expressão regular (quando começa com uma barra (`/`, ou o nome de um grupo precedido por `+`. (Lembre-se de que não há uma verdadeira distinção entre usuários e grupos no PostgreSQL; uma marca `+` realmente significa “corresponder a qualquer um dos papéis que são membros diretamente ou indiretamente deste papel”, enquanto um nome sem uma marca `+` corresponde apenas a esse papel específico.) Para este propósito, um superusuário é considerado membro de um papel apenas se for explicitamente um membro do papel, diretamente ou indiretamente, e não apenas em virtude de ser um superusuário. Múltiplos nomes de usuário e/ou expressões regulares podem ser fornecidos separando-os com vírgulas.

Se o nome do usuário começar com uma barra (`/`), o restante do nome é tratado como uma expressão regular. (Consulte [Seção 9.7.3.1][(functions-matching.md#POSIX-SYNTAX-DETAILS "9.7.3.1. Regular Expression Details")] para obter detalhes sobre a sintaxe de expressão regular do PostgreSQL.)

Um arquivo separado contendo nomes de usuários e/ou expressões regulares pode ser especificado ao antecipar o nome do arquivo com `@`.

*`address`*: Especifica o(s) endereço(s) da máquina cliente que este registro corresponde. Este campo pode conter um nome de host, uma faixa de endereços IP ou uma das palavras-chave especiais mencionadas abaixo.

Uma faixa de endereços IP é especificada usando notação numérica padrão para o endereço inicial da faixa, então um traço (`/`) e um comprimento da máscara CIDR. O comprimento da máscara indica o número de bits de alta ordem do endereço IP do cliente que devem corresponder. Os bits à direita deste devem ser zero no endereço IP fornecido. Não deve haver espaço em branco entre o endereço IP, o `/` e o comprimento da máscara CIDR.

Exemplos típicos de uma faixa de endereço IPv4 especificada dessa maneira são `172.20.143.89/32` para um único host, ou `172.20.143.0/24` para uma pequena rede, ou `10.6.0.0/16` para uma rede maior. Uma faixa de endereço IPv6 pode parecer `::1/128` para um único host (neste caso, o endereço de loopback IPv6) ou `fe80::7a31:c1ff:0000:0000/96` para uma pequena rede. `0.0.0.0/0` representa todos os endereços IPv4, e `::0/0` representa todos os endereços IPv6. Para especificar um único host, use um comprimento de máscara de 32 para IPv4 ou 128 para IPv6. Em um endereço de rede, não omita zeros finais.

Uma entrada fornecida em formato IPv4 corresponderá apenas a conexões IPv4, e uma entrada fornecida em formato IPv6 corresponderá apenas a conexões IPv6, mesmo que o endereço representado esteja na faixa IPv4-in-IPv6.

Você também pode escrever `all` para corresponder a qualquer endereço IP, `samehost` para corresponder a qualquer endereço IP do próprio servidor, ou `samenet` para corresponder a qualquer endereço em qualquer sub-rede para a qual o servidor está diretamente conectado.

Se um nome de host for especificado (qualquer coisa que não seja um intervalo de endereço IP ou uma palavra-chave especial é tratada como um nome de host), esse nome é comparado com o resultado de uma resolução reversa do nome do endereço IP do cliente (por exemplo, pesquisa reversa DNS, se o DNS for usado). As comparações de nomes de host são sensíveis ao caso. Se houver uma correspondência, então uma resolução de nome para frente (por exemplo, pesquisa DNS para frente) é realizada no nome de host para verificar se algum dos endereços que ele resolve são iguais ao endereço IP do cliente. Se ambas as direções corresponderem, então a entrada é considerada correspondente. (O nome de host que é usado em `pg_hba.conf` deve ser o que a resolução de endereço-para-nome do endereço IP do cliente retorna, caso contrário, a linha não será correspondida. Algumas bases de dados de nomes de host permitem associar um endereço IP com múltiplos nomes de host, mas o sistema operacional apenas retornará um nome de host quando solicitado a resolver um endereço IP.)

Uma especificação de nome de host que começa com um ponto (`.`) corresponde a um sufixo do nome de host real. Portanto, `.example.com` corresponderia a `foo.example.com` (mas não apenas a `example.com`).

Quando os nomes de host são especificados em `pg_hba.conf`, você deve garantir que a resolução de nomes seja razoavelmente rápida. Pode ser vantajoso configurar um cache de resolução de nomes local, como `nscd`. Além disso, você pode querer habilitar o parâmetro de configuração `log_hostname` para ver o nome do host do cliente em vez do endereço IP no log.

Esses campos não se aplicam aos registros de `local`.

### Nota

Os usuários às vezes se perguntam por que os nomes de host são tratados dessa maneira aparentemente complicada, com duas resoluções de nome, incluindo uma pesquisa reversa do endereço IP do cliente. Isso complica o uso do recurso no caso de a entrada de DNS reversa do cliente não estar configurada ou gerar algum nome de host indesejado. Isso é feito principalmente por eficiência: dessa forma, uma tentativa de conexão requer, no máximo, duas pesquisas de resolver, uma reversa e uma para frente. Se houver um problema de resolver com algum endereço, torna-se apenas o problema do cliente. Uma implementação alternativa hipotética que realizasse apenas pesquisas para frente teria que resolver cada nome de host mencionado em `pg_hba.conf` durante cada tentativa de conexão. Isso poderia ser bastante lento se muitos nomes estiverem listados. E se houver um problema de resolver com um dos nomes de host, torna-se o problema de todos.

Além disso, uma pesquisa reversa é necessária para implementar a funcionalidade de correspondência de sufixo, porque o nome real do host do cliente precisa ser conhecido para que ele possa ser correspondido ao padrão.

Observe que esse comportamento é consistente com outras implementações populares de controle de acesso baseado em nome de host, como o Apache HTTP Server e os TCP Wrappers.

*`IP-address`* *`IP-mask`*: Esses dois campos podem ser usados como alternativa à notação *`IP-address`*`/`*`mask-length`*. Em vez de especificar o comprimento da máscara, a máscara real é especificada em uma coluna separada. Por exemplo, `255.0.0.0` representa um comprimento de máscara CIDR IPv4 de 8, e `255.255.255.255` representa um comprimento de máscara CIDR de 32.

Esses campos não se aplicam aos registros `local`.

*`auth-method`*: Especifica o método de autenticação a ser utilizado quando uma conexão corresponder a este registro. As opções possíveis são resumidas aqui; os detalhes estão em [Seção 20.3](auth-methods.md "20.3. Authentication Methods"). Todas as opções são minúsculas e tratadas sensatamente, portanto, até mesmo siglas como `ldap` devem ser especificadas em minúsculas.

`trust` :   Permitir a conexão incondicionalmente. Esse método permite que qualquer pessoa que possa se conectar ao servidor de banco de dados PostgreSQL faça login como qualquer usuário do PostgreSQL que desejar, sem a necessidade de uma senha ou qualquer outra autenticação. Consulte [Seção 20.4][(auth-trust.md "20.4. Trust Authentication")] para obter detalhes.

`reject` :   Recusar a conexão incondicionalmente. Isso é útil para "filtrar" certos hosts de um grupo, por exemplo, uma linha `reject` pode bloquear um host específico de se conectar, enquanto uma linha posterior permite que os hosts restantes em uma rede específica se conectem.

`scram-sha-256` : Realize a autenticação SCRAM-SHA-256 para verificar a senha do usuário. Consulte a [Seção 20.5][(auth-password.md "20.5. Password Authentication")] para obter detalhes.

`md5` : Realize autenticação SCRAM-SHA-256 ou MD5 para verificar a senha do usuário. Consulte a [Seção 20.5][(auth-password.md "20.5. Password Authentication")] para obter detalhes.

### Aviso

O suporte para senhas criptografadas com MD5 é desatualizado e será removido em uma versão futura do PostgreSQL. Consulte [Seção 20.5][(auth-password.md "20.5. Password Authentication")] para obter detalhes sobre a migração para outro tipo de senha.

`password` :   Exija que o cliente forneça uma senha não criptografada para autenticação. Como a senha é enviada em texto claro pela rede, isso não deve ser usado em redes não confiáveis. Consulte [Seção 20.5][(auth-password.md "20.5. Password Authentication")] para obter detalhes.

`gss` :   Use o GSSAPI para autenticar o usuário. Isso está disponível apenas para conexões TCP/IP. Consulte a [Seção 20.6][(gssapi-auth.md "20.6. GSSAPI Authentication")] para obter detalhes. Pode ser usado em conjunto com criptografia GSSAPI.

`sspi` :   Utilize SSPI para autenticar o usuário. Isso está disponível apenas no Windows. Consulte a [Seção 20.7][(sspi-auth.md "20.7. SSPI Authentication")] para obter detalhes.

`ident` :   Obtenha o nome do usuário do sistema operacional do cliente, entrando em contato com o servidor ident no cliente e verificando se ele corresponde ao nome de usuário do banco de dados solicitado. A autenticação Ident só pode ser usada em conexões TCP/IP. Quando especificada para conexões locais, a autenticação de pares será usada em vez disso. Veja [Seção 20.8][(auth-ident.md "20.8. Ident Authentication")] para detalhes.

`peer` :   Obtenha o nome do usuário do sistema operacional do cliente a partir do sistema operacional e verifique se ele corresponde ao nome do usuário do banco de dados solicitado. Isso está disponível apenas para conexões locais. Consulte [Seção 20.9][(auth-peer.md "20.9. Peer Authentication")] para obter detalhes.

`ldap` :   Autentique usando um servidor LDAP. Consulte a [Seção 20.10][(auth-ldap.md "20.10. LDAP Authentication")] para obter detalhes.

`radius` :   Autentique usando um servidor RADIUS. Consulte a [Seção 20.11][(auth-radius.md "20.11. RADIUS Authentication")] para obter detalhes.

`cert` :   Autentique usando certificados de cliente SSL. Consulte [Seção 20.12][(auth-cert.md "20.12. Certificate Authentication")] para detalhes.

`pam` :   Autentique usando o serviço de Módulos de Autenticação Conectam-se (PAM) fornecido pelo sistema operacional. Consulte a [Seção 20.13][(auth-pam.md "20.13. PAM Authentication")] para obter detalhes.

`bsd` :   Autentique usando o serviço de autenticação BSD fornecido pelo sistema operacional. Consulte [Seção 20.14][(auth-bsd.md "20.14. BSD Authentication")] para obter detalhes.

`oauth` :   Autorizar e, opcionalmente, autenticar usando um provedor de identidade OAuth 2.0 de terceiros. Consulte a [Seção 20.15][(auth-oauth.md "20.15. OAuth Authorization/Authentication")] para obter detalhes.

*`auth-options`*: Após o campo *`auth-method`*, pode haver(em) campo(s) na forma *`name`*`=`*`value`* que especificam opções para o método de autenticação. Os detalhes sobre quais opções estão disponíveis para quais métodos de autenticação aparecem abaixo.

Além das opções específicas do método listadas abaixo, há uma opção de autenticação independente do método `clientcert`, que pode ser especificada em qualquer registro `hostssl`. Esta opção pode ser definida para `verify-ca` ou `verify-full`. Ambas as opções exigem que o cliente apresente um certificado SSL válido (confiável), enquanto `verify-full` reforça adicionalmente que o `cn` (Nome Comum) no certificado corresponda ao nome de usuário ou a um mapeamento aplicável. Esse comportamento é semelhante ao método de autenticação `cert` (ver [Seção 20.12][(auth-cert.md "20.12. Certificate Authentication")]) mas permite a combinação da verificação de certificados do cliente com qualquer método de autenticação que suporte entradas `hostssl`.

Em qualquer registro que utilize autenticação com certificado do cliente (ou seja, um que utilize o método de autenticação `cert` ou um que utilize a opção `clientcert`, você pode especificar qual parte das credenciais do certificado do cliente deve ser correspondida usando a opção `clientname`. Esta opção pode ter um dos dois valores. Se você especificar `clientname=CN`, que é o padrão, o nome de usuário é correspondido ao `Common Name (CN)` do certificado. Se, em vez disso, você especificar `clientname=DN`, o nome de usuário é correspondido ao `Distinguished Name (DN)` inteiro do certificado. Esta opção é provavelmente a melhor usada em conjunto com um mapa de nome de usuário. A comparação é feita com o `DN` no formato [RFC 2253](https://datatracker.ietf.org/doc/html/rfc2253). Para ver o `DN` de um certificado do cliente neste formato, faça

``` openssl x509 -in myclient.crt -noout -subject -nameopt RFC2253 | sed "s/^subject=//"
    ```

É preciso ter cuidado ao usar essa opção, especialmente ao usar correspondência com expressão regular contra o `DN`.

`include`: Esta linha será substituída pelo conteúdo do arquivo fornecido.

`include_if_exists`: Esta linha será substituída pelo conteúdo do arquivo fornecido, se o arquivo existir. Caso contrário, uma mensagem será registrada para indicar que o arquivo foi ignorado.

`include_dir`: Esta linha será substituída pelo conteúdo de todos os arquivos encontrados no diretório, se eles não começarem com `.` e não terminarem com `.conf`, processados em ordem de nome de arquivo (de acordo com as regras do C locale, ou seja, números antes de letras e letras maiúsculas antes de minúsculas).

Os arquivos incluídos pelos construtos `@` são lidos como listas de nomes, que podem ser separados por espaços em branco ou vírgulas. Comentários são introduzidos por `#`, assim como em `pg_hba.conf`, e construtos aninhados `@` são permitidos. A menos que o nome do arquivo após `@` seja um caminho absoluto, ele é considerado relativo ao diretório que contém o arquivo de referência.

Como os registros do `pg_hba.conf` são examinados sequencialmente para cada tentativa de conexão, a ordem dos registros é significativa. Tipicamente, os registros anteriores terão parâmetros de correspondência de conexão mais apertados e métodos de autenticação mais fracos, enquanto os registros posteriores terão parâmetros de correspondência mais laços e métodos de autenticação mais fortes. Por exemplo, pode-se desejar usar a autenticação do `trust` para conexões locais TCP/IP, mas exigir uma senha para conexões remotas TCP/IP. Neste caso, um registro que especifique a autenticação do `trust` para conexões a partir de 127.0.0.1 apareceria antes de um registro que especifique a autenticação por senha para uma gama mais ampla de endereços IP de clientes permitidos.

### DICA

Para se conectar a um banco de dados específico, o usuário não deve apenas passar pelos `pg_hba.conf` de verificação, mas deve ter o `CONNECT` privilégio para o banco de dados. Se você deseja restringir quais usuários podem se conectar a quais bancos de dados, geralmente é mais fácil controlar isso concedendo/revocando o `CONNECT` privilégio do que colocar as regras nas entradas do `pg_hba.conf`.

Alguns exemplos de entradas do `pg_hba.conf` são mostrados em [Exemplo 20.1][(auth-pg-hba-conf.md#EXAMPLE-PG-HBA.CONF "Example 20.1. Example pg_hba.conf Entries")]. Veja a próxima seção para obter detalhes sobre os diferentes métodos de autenticação.

**Exemplo 20.1. Exemplos de entradas `pg_hba.conf`**

```
# Allow any user on the local system to connect to any database with
# any database user name using Unix-domain sockets (the default for local
# connections).
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     trust

# The same using local loopback TCP/IP connections.
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             127.0.0.1/32            trust

# The same as the previous line, but using a separate netmask column
#
# TYPE  DATABASE        USER            IP-ADDRESS      IP-MASK             METHOD
host    all             all             127.0.0.1       255.255.255.255     trust

# The same over IPv6.
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             ::1/128                 trust

# The same using a host name (would typically cover both IPv4 and IPv6).
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             localhost               trust

# The same using a regular expression for DATABASE, that allows connection
# to any databases with a name beginning with "db" and finishing with a
# number using two to four digits (like "db1234" or "db12").
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    "/^db\d{2,4}$"  all             localhost               trust

# Allow any user from any host with IP address 192.168.93.x to connect
# to database "postgres" as the same user name that ident reports for
# the connection (typically the operating system user name).
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    postgres        all             192.168.93.0/24         ident

# Allow any user from host 192.168.12.10 to connect to database
# "postgres" if the user's password is correctly supplied.
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    postgres        all             192.168.12.10/32        scram-sha-256

# Allow any user from hosts in the example.com domain to connect to
# any database if the user's password is correctly supplied.
#
# Require SCRAM authentication for most users, but make an exception
# for user 'mike', who uses an older client that doesn't support SCRAM
# authentication.
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             mike            .example.com            md5 host    all             all             .example.com            scram-sha-256

# In the absence of preceding "host" lines, these three lines will
# reject all connections from 192.168.54.1 (since that entry will be
# matched first), but allow GSSAPI-encrypted connections from anywhere else
# on the Internet.  The zero mask causes no bits of the host IP address to
# be considered, so it matches any host.  Unencrypted GSSAPI connections
# (which "fall through" to the third line since "hostgssenc" only matches
# encrypted GSSAPI connections) are allowed, but only from 192.168.12.10.
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             192.168.54.1/32         reject hostgssenc all          all             0.0.0.0/0               gss host    all             all             192.168.12.10/32        gss

# Allow users from 192.168.x.x hosts to connect to any database, if
# they pass the ident check.  If, for example, ident says the user is
# "bryanh" and he requests to connect as PostgreSQL user "guest1", the
# connection is allowed if there is an entry in pg_ident.conf for map
# "omicron" that says "bryanh" is allowed to connect as "guest1".
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             192.168.0.0/16          ident map=omicron

# If these are the only four lines for local connections, they will
# allow local users to connect only to their own databases (databases
# with the same name as their database user name) except for users whose
# name end with "helpdesk", administrators and members of role "support",
# who can connect to all databases.  The file $PGDATA/admins contains a
# list of names of administrators.  Passwords are required in all cases.
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   sameuser        all                                     scram-sha-256 local   all             /^.*helpdesk$                           scram-sha-256 local   all             @admins                                 scram-sha-256 local   all             +support                                scram-sha-256

# The last two lines above can be combined into a single line:
local   all             @admins,+support                        scram-sha-256

# The database column can also use lists and file names:
local   db1,db2,@demodbs  all                                   scram-sha-256
```
