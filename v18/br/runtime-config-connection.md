## 19.3. Conexões e Autenticação [#](#RUNTIME-CONFIG-CONNECTION)

* [19.3.1. Configurações de Conexão](runtime-config-connection.md#RUNTIME-CONFIG-CONNECTION-SETTINGS)
* [19.3.2. Configurações TCP](runtime-config-connection.md#RUNTIME-CONFIG-TCP-SETTINGS)
* [19.3.3. Autenticação](runtime-config-connection.md#RUNTIME-CONFIG-CONNECTION-AUTHENTICATION)
* [19.3.4. SSL](runtime-config-connection.md#RUNTIME-CONFIG-CONNECTION-SSL)

### 19.3.1. Configurações de conexão [#](#RUNTIME-CONFIG-CONNECTION-SETTINGS)

`listen_addresses` (`string`) [#](#GUC-LISTEN-ADDRESSES): Especifica o(s) endereço(s) TCP/IP no qual o servidor deve ouvir conexões de aplicações de cliente. O valor assume a forma de uma lista de nomes de host e/ou endereços IP numéricos separados por vírgula. A entrada especial `*` corresponde a todas as interfaces IP disponíveis. A entrada `0.0.0.0` permite ouvir todos os endereços IPv4 e `::` permite ouvir todos os endereços IPv6. Se a lista estiver vazia, o servidor não ouvirá nenhuma interface IP, no caso em que apenas conexões de Unix-domain podem ser usadas para conectá-lo. Se a lista não estiver vazia, o servidor começará se puder ouvir pelo menos um endereço TCP/IP. Um aviso será emitido para qualquer endereço TCP/IP que não possa ser aberto. O valor padrão é localhost, que permite que apenas conexões locais de "loopback" TCP/IP sejam feitas.

Enquanto a autenticação do cliente ([Capítulo 20][(client-authentication.md "Chapter 20. Client Authentication")]) permite um controle detalhado sobre quem pode acessar o servidor, o `listen_addresses` controla quais interfaces aceitam tentativas de conexão, o que pode ajudar a prevenir solicitações de conexão maliciosas repetidas em interfaces de rede inseguras. Este parâmetro só pode ser definido no início do servidor.

`port` (`integer`) [#](#GUC-PORT): A porta TCP que o servidor escuta; 5432 por padrão. Observe que o mesmo número de porta é usado para todos os endereços IP que o servidor escuta. Este parâmetro só pode ser definido no início do servidor.

`max_connections` (`integer`) [#](#GUC-MAX-CONNECTIONS): Determina o número máximo de conexões concorrentes ao servidor de banco de dados. O padrão é normalmente 100 conexões, mas pode ser menor se as configurações do kernel não o suportarão (determinado durante o initdb). Este parâmetro só pode ser definido no início do servidor.

O PostgreSQL dimensiona certos recursos diretamente com base no valor de `max_connections`. Aumentar seu valor leva a uma alocação mais alta desses recursos, incluindo memória compartilhada.

Ao executar um servidor de espera, você deve definir esse parâmetro no mesmo valor ou superior ao do servidor primário. Caso contrário, as consultas não serão permitidas no servidor de espera.

`reserved_connections` (`integer`) [#](#GUC-RESERVED-CONNECTIONS): Determina o número de "faixas" de conexão que são reservadas para conexões por papéis com privilégios do papel [[pg_use_reserved_connections]] (predefined-roles.md#PREDEFINED-ROLE-PG-USE-RESERVED-CONNECTIONS). Sempre que o número de faixas de conexão livres for maior que [[superuser_reserved_connections]] (runtime-config-connection.md#GUC-SUPERUSER-RESERVED-CONNECTIONS), mas menor ou igual à soma de `superuser_reserved_connections` e `reserved_connections`, novas conexões serão aceitas apenas para superusuários e papéis com privilégios de `pg_use_reserved_connections`. Se `superuser_reserved_connections` ou menos faixas de conexão estiverem disponíveis, novas conexões serão aceitas apenas para superusuários.

O valor padrão é zero conexões. O valor deve ser menor que `max_connections` menos `superuser_reserved_connections`. Este parâmetro só pode ser definido no início do servidor.

`superuser_reserved_connections` (`integer`) [#](#GUC-SUPERUSER-RESERVED-CONNECTIONS): Determina o número de "faixas" de conexão que são reservadas para conexões por superusuários do PostgreSQL. No máximo, [max_connections](runtime-config-connection.md#GUC-MAX-CONNECTIONS) conexões podem estar ativas simultaneamente. Sempre que o número de conexões ativas concorrentes estiver, pelo menos, em `max_connections` menos `superuser_reserved_connections`, novas conexões serão aceitas apenas para superusuários. As faixas de conexão reservadas por este parâmetro são destinadas como reserva final para uso de emergência após os slots reservados por [reserved_connections](runtime-config-connection.md#GUC-RESERVED-CONNECTIONS) terem sido esgotados.

O valor padrão é de três conexões. O valor deve ser menor que `max_connections` menos `reserved_connections`. Este parâmetro só pode ser definido no início do servidor.

`unix_socket_directories` (`string`) [#](#GUC-UNIX-SOCKET-DIRECTORIES): Especifica o diretório do(s) socket(s) de domínio Unix em que o servidor deve ouvir conexões de aplicativos de cliente. Múltiplos sockets podem ser criados listando múltiplos diretórios separados por vírgulas. Espaços em branco entre entradas são ignorados; envolva o nome do diretório com aspas duplas se precisar incluir espaços em branco ou vírgulas no nome. Um valor vazio especifica não ouvir em nenhum socket de domínio Unix, nesse caso, apenas sockets TCP/IP podem ser usados para se conectar ao servidor.

Um valor que começa com `@` especifica que um socket de domínio Unix no espaço abstrato deve ser criado (atualmente suportado apenas no Linux). Nesse caso, esse valor não especifica um "diretório", mas um prefixo a partir do qual o nome do socket real é calculado da mesma maneira que para o espaço de nomes do sistema de arquivos. Embora o prefixo do nome do socket abstrato possa ser escolhido livremente, uma vez que não é uma localização de sistema de arquivos, a convenção é, no entanto, usar valores semelhantes ao do sistema de arquivos, como `@/tmp`.

O valor padrão é normalmente `/tmp`, mas isso pode ser alterado na hora da construção. No Windows, o padrão é vazio, o que significa que não é criado um soquete de domínio Unix por padrão. Este parâmetro só pode ser definido no início do servidor.

Além do próprio arquivo de soquete, que é denominado `.s.PGSQL.nnnn`, onde *`nnnn`* é o número da porta do servidor, um arquivo comum denominado `.s.PGSQL.nnnn.lock` será criado em cada um dos diretórios `unix_socket_directories`. Nenhum desses arquivos deve ser removido manualmente. Para soquetes no namespace abstrato, nenhum arquivo de bloqueio é criado.

`unix_socket_group` (`string`) [#](#GUC-UNIX-SOCKET-GROUP): Define o grupo proprietário do(s) socket(s) de domínio Unix. (O usuário proprietário dos sockets é sempre o usuário que inicia o servidor.) Em combinação com o parâmetro `unix_socket_permissions`, este pode ser usado como um mecanismo adicional de controle de acesso para conexões de domínio Unix. Por padrão, esta é uma string vazia, que usa o grupo padrão do usuário do servidor. Este parâmetro só pode ser definido no início do servidor.

Este parâmetro não é suportado no Windows. Qualquer configuração será ignorada. Além disso, os sockets no namespace abstrato não têm proprietário de arquivo, portanto, essa configuração também é ignorada nesse caso.

`unix_socket_permissions` (`integer`) [#](#GUC-UNIX-SOCKET-PERMISSIONS): Define as permissões de acesso do(s) socket(s) de domínio Unix. Os sockets de domínio Unix utilizam o conjunto de permissões usual do sistema de arquivos Unix. O valor do parâmetro deve ser um modo numérico especificado no formato aceito pelas chamadas de sistema `chmod` e `umask`. (Para usar o formato octal comum, o número deve começar com um `0` (zero).)

Os permissões padrão são `0777`, o que significa que qualquer pessoa pode se conectar. Alternativas razoáveis são `0770` (apenas usuário e grupo, veja também `unix_socket_group`) e `0700` (apenas usuário). (Observe que, para uma conexão de domínio Unix, apenas a permissão de escrita importa, portanto, não há sentido em definir ou revogar permissões de leitura ou execução.)

Esse mecanismo de controle de acesso é independente do descrito em [Capítulo 20] [(client-authentication.md "Chapter 20. Client Authentication")].

Este parâmetro só pode ser definido no início do servidor.

Este parâmetro é irrelevante em sistemas, especialmente o Solaris a partir do Solaris 10, que ignora as permissões de soquete por completo. Lá, é possível obter um efeito semelhante, apontando `unix_socket_directories` para um diretório com permissão de busca limitada ao público desejado.

Os sockets na abstração do namespace não têm permissões de arquivo, portanto, essa configuração também é ignorada nesse caso.

`bonjour` (`boolean`) [#](#GUC-BONJOUR): Habilita a divulgação da existência do servidor via Bonjour. O padrão é desativado. Este parâmetro só pode ser definido na inicialização do servidor.

`bonjour_name` (`string`) [#](#GUC-BONJOUR-NAME): Especifica o nome do serviço Bonjour. O nome do computador é usado se este parâmetro for definido como a string vazia `''` (que é a opção padrão). Este parâmetro é ignorado se o servidor não foi compilado com suporte Bonjour. Este parâmetro só pode ser definido no início do servidor.

### 19.3.2. Configurações TCP [#](#RUNTIME-CONFIG-TCP-SETTINGS)

`tcp_keepalives_idle` (`integer`) [#](#GUC-TCP-KEEPALIVES-IDLE): Especifica o tempo sem atividade na rede após o qual o sistema operacional deve enviar uma mensagem de manutenção TCP ao cliente. Se esse valor for especificado sem unidades, ele é considerado em segundos. Um valor de 0 (padrão) seleciona o valor padrão do sistema operacional. Em Windows, definir um valor de 0 configurará este parâmetro para 2 horas, uma vez que o Windows não fornece uma maneira de ler o valor padrão do sistema. Este parâmetro é suportado apenas em sistemas que suportam `TCP_KEEPIDLE` ou uma opção de soquete equivalente, e em Windows; em outros sistemas, ele deve ser zero. Em sessões conectadas via um soquete de domínio Unix, este parâmetro é ignorado e sempre é lido como zero.

`tcp_keepalives_interval` (`integer`) [#](#GUC-TCP-KEEPALIVES-INTERVAL): Especifica o período de tempo após o qual uma mensagem de manutenção TCP que não foi reconhecida pelo cliente deve ser retransmitida. Se este valor for especificado sem unidades, ele é considerado em segundos. Um valor de 0 (padrão) seleciona o valor padrão do sistema operacional. Em Windows, definir um valor de 0 configurará este parâmetro para 1 segundo, uma vez que o Windows não fornece uma maneira de ler o valor padrão do sistema. Este parâmetro é suportado apenas em sistemas que suportam `TCP_KEEPINTVL` ou uma opção de soquete equivalente, e em Windows; em outros sistemas, ele deve ser zero. Em sessões conectadas via um soquete de domínio Unix, este parâmetro é ignorado e sempre é lido como zero.

`tcp_keepalives_count` (`integer`) [#](#GUC-TCP-KEEPALIVES-COUNT): Especifica o número de mensagens de manutenção TCP que podem ser perdidas antes que a conexão do servidor com o cliente seja considerada morta. Um valor de 0 (padrão) seleciona o padrão do sistema operacional. Este parâmetro é suportado apenas em sistemas que suportam `TCP_KEEPCNT` ou uma opção de soquete equivalente (que não inclui o Windows); em outros sistemas, ele deve ser zero. Em sessões conectadas via um soquete de domínio Unix, este parâmetro é ignorado e sempre é lido como zero.

`tcp_user_timeout` (`integer`) [#](#GUC-TCP-USER-TIMEOUT): Especifica o tempo que os dados transmitidos podem permanecer não confirmados antes que a conexão TCP seja encerrada à força. Se este valor for especificado sem unidades, ele é considerado em milissegundos. Um valor de 0 (padrão) seleciona o padrão do sistema operacional. Este parâmetro é suportado apenas em sistemas que suportam `TCP_USER_TIMEOUT` (que não inclui o Windows); em outros sistemas, ele deve ser zero. Em sessões conectadas por meio de um socket de domínio Unix, este parâmetro é ignorado e sempre é lido como zero.

`client_connection_check_interval` (`integer`) [#](#GUC-CLIENT-CONNECTION-CHECK-INTERVAL): Define o intervalo de tempo entre as verificações opcionais de que o cliente ainda está conectado, enquanto executa consultas. A verificação é realizada através de uma pesquisa no socket e permite que consultas de longa duração sejam interrompidas mais cedo se o kernel relatar que a conexão foi fechada.

Essa opção depende de eventos do kernel expostos pelo Linux, macOS, illumos e a família de sistemas operacionais BSD, e atualmente não está disponível em outros sistemas.

Se o valor for especificado sem unidades, ele será considerado em milissegundos. O valor padrão é `0`, que desativa as verificações de conexão. Sem verificações de conexão, o servidor detectará a perda da conexão apenas na próxima interação com o soquete, quando ele espera, recebe ou envia dados.

Para que o próprio kernel detecte conexões TCP perdidas de forma confiável e dentro de um período conhecido em todos os cenários, incluindo falha na rede, também pode ser necessário ajustar as configurações de manutenção TCP do sistema operacional, ou as configurações [tcp_keepalives_idle][(runtime-config-connection.md#GUC-TCP-KEEPALIVES-IDLE)], [tcp_keepalives_interval][(runtime-config-connection.md#GUC-TCP-KEEPALIVES-INTERVAL)] e [tcp_keepalives_count][(runtime-config-connection.md#GUC-TCP-KEEPALIVES-COUNT)] do PostgreSQL.

### 19.3.3. Autenticação [#](#RUNTIME-CONFIG-CONNECTION-AUTHENTICATION)

`authentication_timeout` (`integer`) [#](#GUC-AUTHENTICATION-TIMEOUT): Quantidade máxima de tempo permitida para completar a autenticação do cliente. Se um cliente em potencial não tiver completado o protocolo de autenticação em esse período de tempo, o servidor fecha a conexão. Isso previne que clientes bloqueados ocupem uma conexão indefinidamente. Se esse valor for especificado sem unidades, ele é considerado em segundos. O padrão é um minuto (`1m`). Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`password_encryption` (`enum`) [#](#GUC-PASSWORD-ENCRYPTION): Quando uma senha é especificada em [CREATE ROLE](sql-createrole.md "CREATE ROLE") ou [ALTER ROLE](sql-alterrole.md "ALTER ROLE"), este parâmetro determina o algoritmo a ser usado para criptografar a senha. Os valores possíveis são `scram-sha-256`, que criptografará a senha com SCRAM-SHA-256, e `md5`, que armazenará a senha como um hash MD5. O padrão é `scram-sha-256`.

Observe que os clientes mais antigos podem não ter suporte para o mecanismo de autenticação SCRAM, e, portanto, não funcionar com senhas criptografadas com SCRAM-SHA-256. Consulte [Seção 20.5] para obter mais detalhes.

### Aviso

O suporte para senhas criptografadas com MD5 é desatualizado e será removido em uma versão futura do PostgreSQL. Consulte [Seção 20.5][(auth-password.md "20.5. Password Authentication")] para obter detalhes sobre a migração para outro tipo de senha.

`scram_iterations` (`integer`) [#](#GUC-SCRAM-ITERATIONS): O número de iterações computacionais a serem realizadas ao criptografar uma senha usando SCRAM-SHA-256. O padrão é `4096`. Um número maior de iterações oferece proteção adicional contra ataques brutais em senhas armazenadas, mas torna a autenticação mais lenta. Alterar o valor não tem efeito em senhas existentes criptografadas com SCRAM-SHA-256, pois o número de iterações é fixo no momento da criptografia. Para utilizar um valor alterado, uma nova senha deve ser definida.

`md5_password_warnings` (`boolean`) [#](#GUC-MD5-PASSWORD-WARNINGS): Controla se um `WARNING` sobre a depreciação da senha MD5 é gerado quando uma declaração `CREATE ROLE` ou `ALTER ROLE` define uma senha criptografada MD5. O valor padrão é `on`.

`krb_server_keyfile` (`string`) [#](#GUC-KRB-SERVER-KEYFILE): Define a localização do arquivo de chave Kerberos do servidor. O padrão é `FILE:/usr/local/pgsql/etc/krb5.keytab` (onde a parte do diretório é o que foi especificado como `sysconfdir` na hora da construção; use `pg_config --sysconfdir` para determinar isso). Se este parâmetro for definido como uma string vazia, ele é ignorado e um padrão dependente do sistema é usado. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. Consulte [Seção 20.6](gssapi-auth.md "20.6. GSSAPI Authentication") para obter mais informações.

`krb_caseins_users` (`boolean`) [#](#GUC-KRB-CASEINS-USERS): Define se os nomes dos usuários do GSSAPI devem ser tratados de forma case-insensitive. O padrão é `off` (case sensitive). Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`gss_accept_delegation` (`boolean`) [#](#GUC-GSS-ACCEPT-DELEGATION): Define se a delegação GSSAPI deve ser aceita do cliente. O padrão é `off`, o que significa que as credenciais do cliente *não* serão aceitas. Alterar para `on` fará com que o servidor aceite as credenciais delegadas a ele pelo cliente. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`oauth_validator_libraries` (`string`) [#](#GUC-OAUTH-VALIDATOR-LIBRARIES): A biblioteca/bibliotecas a serem utilizadas para validar tokens de conexão OAuth. Se apenas uma biblioteca de validação for fornecida, ela será usada por padrão para quaisquer conexões OAuth; caso contrário, todas as entradas [`oauth` HBA](auth-oauth.md "20.15. OAuth Authorization/Authentication") devem definir explicitamente um `validator` escolhido desta lista. Se definida como uma string vazia (o padrão), as conexões OAuth serão recusadas. Este parâmetro só pode ser definido no arquivo `postgresql.conf`.

Os módulos de validação devem ser implementados/obtidos separadamente; o PostgreSQL não vem com nenhuma implementação padrão. Para mais informações sobre a implementação de validadores OAuth, consulte o [Capítulo 50][(oauth-validators.md "Chapter 50. OAuth Validator Modules")].

### 19.3.4. SSL [#](#RUNTIME-CONFIG-CONNECTION-SSL)

Consulte a [Seção 18.9][(ssl-tcp.md "18.9. Secure TCP/IP Connections with SSL")] para obter mais informações sobre a configuração do SSL. Os parâmetros de configuração para controlar a criptografia de transferência usando protocolos TLS são denominados `ssl` por razões históricas, embora o suporte ao protocolo SSL tenha sido descontinuado. O SSL é usado nesse contexto de forma intercambiável com TLS.

`ssl` (`boolean`) [#](#GUC-SSL): Habilita conexões SSL. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. O padrão é `off`.

`ssl_ca_file` (`string`) [#](#GUC-SSL-CA-FILE): Especifica o nome do arquivo que contém a autoridade de certificação do servidor SSL (CA). As referências relativas são relativas ao diretório de dados. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. O padrão é vazio, o que significa que nenhum arquivo CA é carregado e a verificação de certificado do cliente não é realizada.

`ssl_cert_file` (`string`) [#](#GUC-SSL-CERT-FILE): Especifica o nome do arquivo que contém o certificado do servidor SSL. As referências relativas são relativas ao diretório de dados. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. O padrão é `server.crt`.

`ssl_crl_file` (`string`) [#](#GUC-SSL-CRL-FILE): Especifica o nome do arquivo que contém a lista de revogação de certificados de cliente SSL (CRL). As passagens relativas são relativas ao diretório de dados. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. O padrão é vazio, o que significa que nenhum arquivo CRL é carregado (a menos que [ssl_crl_dir][(runtime-config-connection.md#GUC-SSL-CRL-DIR)] seja definido).

`ssl_crl_dir` (`string`) [#](#GUC-SSL-CRL-DIR): Especifica o nome do diretório que contém a lista de revogação de certificados de cliente SSL (CRL). As passagens relativas são relativas ao diretório de dados. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. O padrão é vazio, o que significa que não são usadas CRLs (a menos que [ssl_crl_file][(runtime-config-connection.md#GUC-SSL-CRL-FILE)] esteja definido).

O diretório precisa ser preparado com o comando OpenSSL `openssl rehash` ou `c_rehash`. Consulte a documentação para obter detalhes.

Ao usar essa configuração, as CRLs no diretório especificado são carregadas sob demanda no momento da conexão. Novos CRLs podem ser adicionados ao diretório e serão usados imediatamente. Isso é diferente de [ssl_crl_file][(runtime-config-connection.md#GUC-SSL-CRL-FILE)], que faz com que a CRL no arquivo seja carregada no momento do início do servidor ou quando a configuração é recarregada. Ambos os ajustes podem ser usados juntos.

`ssl_key_file` (`string`) [#](#GUC-SSL-KEY-FILE): Especifica o nome do arquivo que contém a chave privada do servidor SSL. As referências relativas são relativas ao diretório de dados. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. O padrão é `server.key`.

`ssl_tls13_ciphers` (`string`) [#](#GUC-SSL-TLS13-CIPHERS): Especifica uma lista de suítes de cifra permitidas por conexões que utilizam a versão 1.3 do TLS. Múltiplas suítes de cifra podem ser especificadas usando uma lista separada por vírgula. Se deixada em branco, o conjunto padrão de suítes de cifra no OpenSSL será utilizado.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`ssl_ciphers` (`string`) [#](#GUC-SSL-CIPHERS): Especifica uma lista de cifras SSL permitidas por conexões que utilizam a versão 1.2 do TLS e versões inferiores, consulte [ssl_tls13_ciphers](runtime-config-connection.md#GUC-SSL-TLS13-CIPHERS) para conexões com a versão 1.3 do TLS. Consulte a página do manual de cifras no pacote OpenSSL para a sintaxe deste ajuste e uma lista de valores suportados. O valor padrão é `HIGH:MEDIUM:+3DES:!aNULL`. O padrão é geralmente uma escolha razoável, a menos que você tenha requisitos de segurança específicos.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

Explicação do valor padrão:

`HIGH` [#](#GUC-SSL-CIPHERS-HIGH) : Suítes de cifra que utilizam cifras do grupo `HIGH` (por exemplo, AES, Camellia, 3DES)

`MEDIUM` [#](#GUC-SSL-CIPHERS-MEDIUM) :   Suítes de cifra que utilizam cifras do grupo `MEDIUM` (por exemplo, RC4, SEED)

`+3DES` [#](#GUC-SSL-CIPHERS-PLUS-3DES) :   A ordem padrão do OpenSSL para `HIGH` é problemática porque ordena o 3DES acima do AES128. Isso está errado porque o 3DES oferece menos segurança do que o AES128, e também é muito mais lento. `+3DES` reordena tudo após todos os outros cifradores `HIGH` e `MEDIUM`.

`!aNULL` [#](#GUC-SSL-CIPHERS-NOT-ANULL) :   Desabilita suítes de cifra anônima que não oferecem autenticação. Tais suítes de cifra são vulneráveis a ataques MITM e, portanto, não devem ser usadas.

Os detalhes disponíveis sobre a suíte de cifra variam entre as versões do OpenSSL. Use o comando `openssl ciphers -v 'HIGH:MEDIUM:+3DES:!aNULL'` para ver os detalhes reais da versão do OpenSSL instalada atualmente. Observe que essa lista é filtrada no momento da execução com base no tipo de chave do servidor.

`ssl_prefer_server_ciphers` (`boolean`) [#](#GUC-SSL-PREFER-SERVER-CIPHERS): Especifica se deve usar as preferências de cifra SSL do servidor, em vez das do cliente. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. O padrão é `on`.

As versões do PostgreSQL anteriores a 9.4 não possuem essa configuração e sempre usam as preferências do cliente. Essa configuração é principalmente para compatibilidade reversa com essas versões. Usar as preferências do servidor é geralmente melhor, pois é mais provável que o servidor esteja configurado adequadamente.

`ssl_groups` (`string`) [#](#GUC-SSL-GROUPS): Especifica o nome da curva a ser usada na troca de chave ECDH. Ela precisa ser suportada por todos os clientes que se conectam. Múltiplas curvas podem ser especificadas usando uma lista separada por vírgula. Não precisa ser a mesma curva usada pela chave de curva elíptica do servidor. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. O padrão é `X25519:prime256v1`.

Os nomes de curvas mais comuns do OpenSSL são: `prime256v1` (NIST P-256), `secp384r1` (NIST P-384), `secp521r1` (NIST P-521). Uma lista incompleta dos grupos disponíveis pode ser exibida com o comando `openssl ecparam -list_curves`. No entanto, nem todos eles são utilizáveis com TLS, e muitos dos nomes e aliases de grupos suportados são omitidos.

Nas versões do PostgreSQL anteriores à 18.0, essa configuração era denominada `ssl_ecdh_curve` e aceitava apenas um valor.

`ssl_min_protocol_version` (`enum`) [#](#GUC-SSL-MIN-PROTOCOL-VERSION): Define a versão mínima do protocolo SSL/TLS a ser utilizada. Os valores válidos atualmente são: `TLSv1`, `TLSv1.1`, `TLSv1.2`, `TLSv1.3`. Versões mais antigas da biblioteca OpenSSL não suportam todos os valores; um erro será exibido se uma configuração não suportada for escolhida. As versões de protocolo antes do TLS 1.0, nomeadamente as versões SSL 2 e 3, são sempre desativadas.

O padrão é `TLSv1.2`, que atende às melhores práticas da indústria conforme esta escrita.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`ssl_max_protocol_version` (`enum`) [#](#GUC-SSL-MAX-PROTOCOL-VERSION): Define a versão máxima do protocolo SSL/TLS a ser usada. Os valores válidos são os mesmos que para [ssl_min_protocol_version](runtime-config-connection.md#GUC-SSL-MIN-PROTOCOL-VERSION), com adição de uma string vazia, que permite qualquer versão do protocolo. O padrão é permitir qualquer versão. Definir a versão máxima do protocolo é principalmente útil para testes ou se algum componente tiver problemas para trabalhar com um protocolo mais recente.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`ssl_dh_params_file` (`string`) [#](#GUC-SSL-DH-PARAMS-FILE): Especifica o nome do arquivo que contém os parâmetros Diffie-Hellman usados para a chamada família efêmera de cifras SSL. O padrão é vazio, no qual caso os parâmetros DH padrão compilados são usados. Usar parâmetros DH personalizados reduz a exposição se um atacante conseguir quebrar os parâmetros DH compilados bem conhecidos. Você pode criar seu próprio arquivo de parâmetros DH com o comando `openssl dhparam -out dhparams.pem 2048`.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`ssl_passphrase_command` (`string`) [#](#GUC-SSL-PASSPHRASE-COMMAND): Define um comando externo que será invocado quando uma senha para descriptografar um arquivo SSL, como uma chave privada, precisar ser obtida. Por padrão, este parâmetro está vazio, o que significa que o mecanismo de solicitação integrado é usado.

O comando deve imprimir a senha padrão na saída padrão e sair com código 0. No valor do parâmetro, `%p` é substituído por uma string de prompt. (Escreva `%%` para um literal `%`.). Observe que a string de prompt provavelmente conterá espaços em branco, então certifique-se de cobri-los adequadamente. Uma única nova linha é removida do final da saída, se presente.

O comando não precisa, na verdade, solicitar uma senha ao usuário. Ele pode lê-la a partir de um arquivo, obtê-la de uma instalação de chaveiro ou algo semelhante. Cabe ao usuário garantir que o mecanismo escolhido seja adequadamente seguro.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`ssl_passphrase_command_supports_reload` (`boolean`) [#](#GUC-SSL-PASSPHRASE-COMMAND-SUPPORTS-RELOAD): Este parâmetro determina se o comando de senha definido por `ssl_passphrase_command` também será chamado durante uma recarga da configuração se um arquivo de chave precisar de uma senha. Se este parâmetro for `off` (o padrão), então `ssl_passphrase_command` será ignorado durante uma recarga e a configuração SSL não será recarregada se uma senha for necessária. Esse ajuste é apropriado para um comando que requer um TTY para solicitação, que pode não estar disponível quando o servidor estiver em execução. Definir este parâmetro para on pode ser apropriado se a senha for obtida de um arquivo, por exemplo.

Este parâmetro deve ser definido como `on` quando executado no Windows, pois todas as conexões realizarão uma recarga de configuração devido ao modelo de processo diferente dessa plataforma.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.