## 18.9. Conexões TCP/IP seguras com SSL [#](#SSL-TCP)

* [18.9.1. Configuração Básica](ssl-tcp.md#SSL-SETUP)
* [18.9.2. Configuração do OpenSSL](ssl-tcp.md#SSL-OPENSSL-CONFIG)
* [18.9.3. Uso de Certificados de Cliente](ssl-tcp.md#SSL-CLIENT-CERTIFICATES)
* [18.9.4. Uso do Arquivo do Servidor SSL](ssl-tcp.md#SSL-SERVER-FILES)
* [18.9.5. Criação de Certificados](ssl-tcp.md#SSL-CERTIFICATE-CREATION)

O PostgreSQL tem suporte nativo para usar conexões SSL para criptografar comunicações cliente/servidor para maior segurança. Isso exige que o OpenSSL esteja instalado nos sistemas cliente e servidor e que o suporte no PostgreSQL seja habilitado na hora da construção (consulte [Capítulo 17][(installation.md "Chapter 17. Installation from Source Code")]).

Os termos SSL e TLS são frequentemente usados de forma intercambiável para significar uma conexão criptografada segura usando um protocolo TLS. Os protocolos SSL são os precursores dos protocolos TLS, e o termo SSL ainda é usado para conexões criptografadas, mesmo que os protocolos SSL não sejam mais suportados. SSL é usado de forma intercambiável com TLS no PostgreSQL.

### 18.9.1. Configuração básica [#](#SSL-SETUP)

Com o suporte SSL compilado, o servidor PostgreSQL pode ser iniciado com suporte para conexões criptografadas usando protocolos TLS habilitados, definindo o parâmetro [ssl](runtime-config-connection.md#GUC-SSL) para `on` em `postgresql.conf`. O servidor ouvirá conexões normais e SSL na mesma porta TCP, e negociará com qualquer cliente que se conecte sobre o uso do SSL. Por padrão, isso é uma opção do cliente; veja [Seção 20.1](auth-pg-hba-conf.md "20.1. The pg_hba.conf File") sobre como configurar o servidor para exigir o uso do SSL para algumas ou todas as conexões.

Para começar no modo SSL, os arquivos que contêm o certificado do servidor e a chave privada devem existir. Por padrão, espera-se que esses arquivos sejam nomeados `server.crt` e `server.key`, respectivamente, no diretório de dados do servidor, mas outros nomes e locais podem ser especificados usando os parâmetros de configuração [ssl_cert_file](runtime-config-connection.md#GUC-SSL-CERT-FILE) e [ssl_key_file](runtime-config-connection.md#GUC-SSL-KEY-FILE).

Nos sistemas Unix, as permissões de `server.key` devem impedir qualquer acesso ao mundo ou ao grupo; realize isso pelo comando `chmod 0600 server.key`. Alternativamente, o arquivo pode ser de propriedade do root e ter acesso de leitura do grupo (ou seja, as permissões de `0640`). Esse esquema é destinado a instalações onde os arquivos de certificado e chave são gerenciados pelo sistema operacional. O usuário sob o qual o servidor PostgreSQL é executado deve, então, ser feito membro do grupo que tem acesso a esses arquivos de certificado e chave.

Se o diretório de dados permitir acesso de leitura em grupo, os arquivos de certificado podem precisar estar localizados fora do diretório de dados, a fim de atender aos requisitos de segurança descritos acima. Geralmente, o acesso em grupo é habilitado para permitir que um usuário não privilegiado faça backup do banco de dados, e, nesse caso, o software de backup não será capaz de ler os arquivos de certificado e provavelmente apresentará erro.

Se a chave privada estiver protegida com uma frase de senha, o servidor solicitará a senha e não iniciará até que ela seja inserida. O uso de uma frase de senha por padrão desativa a capacidade de alterar a configuração SSL do servidor sem um reinício do servidor, mas veja [ssl_passphrase_command_supports_reload][(runtime-config-connection.md#GUC-SSL-PASSPHRASE-COMMAND-SUPPORTS-RELOAD)]. Além disso, as chaves privadas protegidas por senha não podem ser usadas em absoluto no Windows.

O primeiro certificado no `server.crt` deve ser o certificado do servidor, pois ele deve corresponder à chave privada do servidor. Os certificados das autoridades de certificados intermediárias também podem ser anexados ao arquivo. Ao fazer isso, evita-se a necessidade de armazenar certificados intermediários nos clientes, assumindo que os certificados raiz e intermediários foram criados com extensões `v3_ca`. (Isso define a restrição básica do certificado no `CA` para `true`.) Isso permite uma expiração mais fácil dos certificados intermediários.

Não é necessário adicionar o certificado raiz ao `server.crt`. Em vez disso, os clientes devem ter o certificado raiz da cadeia de certificados do servidor.

### 18.9.2. Configuração OpenSSL [#](#SSL-OPENSSL-CONFIG)

O PostgreSQL lê o arquivo de configuração do OpenSSL de nível de sistema. Por padrão, este arquivo é denominado `openssl.cnf` e está localizado no diretório informado por `openssl version -d`. Este padrão pode ser ignorado definindo a variável de ambiente `OPENSSL_CONF` com o nome do arquivo de configuração desejado.

O OpenSSL suporta uma ampla gama de cifra e algoritmos de autenticação, de força variável. Embora uma lista de cifras possa ser especificada no arquivo de configuração do OpenSSL, você pode especificar cifras especificamente para uso pelo servidor de banco de dados, modificando [ssl_ciphers][(runtime-config-connection.md#GUC-SSL-CIPHERS)] em `postgresql.conf`.

### Nota

É possível ter autenticação sem sobrecarga de criptografia usando os cifradores `NULL-SHA` ou `NULL-MD5`. No entanto, um homem no meio pode ler e passar comunicações entre cliente e servidor. Além disso, a sobrecarga de criptografia é mínima em comparação com a sobrecarga da autenticação. Por essas razões, os cifradores NULL não são recomendados.

### 18.9.3. Uso de Certificados do Cliente [#](#SSL-CLIENT-CERTIFICATES)

Para exigir que o cliente forneça um certificado confiável, coloque certificados das autoridades de certificação de raiz (CA) nas quais você confia em um arquivo no diretório de dados, defina o parâmetro [ssl_ca_file][(runtime-config-connection.md#GUC-SSL-CA-FILE)] em `postgresql.conf` para o novo nome do arquivo e adicione a opção de autenticação `clientcert=verify-ca` ou `clientcert=verify-full` à(s) linha(s) apropriada(s) de `hostssl` em `pg_hba.conf`. Um certificado será então solicitado ao cliente durante o início da conexão SSL. (Consulte [Seção 32.19][(libpq-ssl.md "32.19. SSL Support")] para uma descrição de como configurar certificados no cliente.)

Para uma entrada `hostssl` com `clientcert=verify-ca`, o servidor verificará se o certificado do cliente foi assinado por uma das autoridades de certificado confiáveis. Se `clientcert=verify-full` for especificado, o servidor não apenas verificará a cadeia de certificados, mas também verificará se o nome de usuário ou sua correspondência corresponde ao `cn` (Nome Comum) do certificado fornecido. Note que a validação da cadeia de certificados é sempre assegurada quando o método de autenticação `cert` é usado (ver [Seção 20.12] (auth-cert.md "20.12. Certificate Authentication")).

Certificados intermediários que se alinham até certificados raiz existentes também podem aparecer no arquivo [ssl_ca_file][(runtime-config-connection.md#GUC-SSL-CA-FILE)] se você deseja evitar armazená-los nos clientes (assumindo que os certificados raiz e intermediários foram criados com extensões `v3_ca`). As entradas da Lista de Revogação de Certificados (CRL) também são verificadas se o parâmetro [ssl_crl_file][(runtime-config-connection.md#GUC-SSL-CRL-FILE)] ou [ssl_crl_dir][(runtime-config-connection.md#GUC-SSL-CRL-DIR)] estiver definido.

A opção de autenticação `clientcert` está disponível para todos os métodos de autenticação, mas apenas nas linhas `pg_hba.conf` especificadas como `hostssl`. Quando `clientcert` não é especificado, o servidor verifica o certificado do cliente contra seu arquivo CA apenas se um certificado do cliente for apresentado e a CA estiver configurada.

Existem duas abordagens para impor que os usuários forneçam um certificado durante o login.

A primeira abordagem utiliza o método de autenticação `cert` para entradas `hostssl` em `pg_hba.conf`, de modo que o próprio certificado é usado para autenticação, além de fornecer segurança na conexão ssl. Consulte [Seção 20.12][(auth-cert.md "20.12. Certificate Authentication")] para detalhes. (Não é necessário especificar explicitamente quaisquer opções `clientcert` ao usar o método de autenticação `cert`. Neste caso, o `cn` (Nome Comum) fornecido no certificado é verificado contra o nome do usuário ou um mapeamento aplicável.

A segunda abordagem combina qualquer método de autenticação para as entradas do `hostssl` com a verificação de certificados do cliente, definindo a opção de autenticação do `clientcert` para `verify-ca` ou `verify-full`. A primeira opção apenas garante que o certificado é válido, enquanto a segunda também garante que o `cn` (Nome Comum) no certificado corresponda ao nome do usuário ou a um mapeamento aplicável.

### 18.9.4. Uso do arquivo do servidor SSL [#](#SSL-SERVER-FILES)

[Tabela 18.2][(ssl-tcp.md#SSL-FILE-USAGE "Table 18.2. SSL Server File Usage")] resume os arquivos que são relevantes para a configuração SSL no servidor. (Os nomes de arquivo mostrados são nomes padrão. Os nomes configurados localmente podem ser diferentes.)

**Tabela 18.2. Uso do arquivo do servidor SSL**



<table border="1" class="table" summary="SSL Server File Usage">
<colgroup>
<col/>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>
    File
   </th>
<th>Conteúdo</th>
<th>Efeito</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<a class="xref" href="runtime-config-connection.md#GUC-SSL-CERT-FILE">
     ssl_cert_file
    </a>
    (
    <code class="filename">
     $PGDATA/server.crt
    </code>
    )
   </td>
<td>certificado do servidor</td>
<td>enviado ao cliente para indicar a identidade do servidor</td>
</tr>
<tr>
<td>
<a class="xref" href="runtime-config-connection.md#GUC-SSL-KEY-FILE">
     ssl_key_file
    </a>
    (
    <code class="filename">
     $PGDATA/server.key
    </code>
    )
   </td>
<td>chave privada do servidor</td>
<td>prova que o certificado do servidor foi enviado pelo proprietário; não indica</td>
</tr>
<tr>
<td>
<a class="xref" href="runtime-config-connection.md#GUC-SSL-CA-FILE">
     ssl_ca_file
    </a>
</td>
<td>autoridades de certificação confiáveis</td>
<td>verifica que o certificado do cliente foi assinado por uma autoridade de certificação confiável</td>
</tr>
<tr>
<td>
<a class="xref" href="runtime-config-connection.md#GUC-SSL-CRL-FILE">
     ssl_crl_file
    </a>
</td>
<td>certificados revogados por autoridades de certificação</td>
<td>o certificado do cliente não deve estar nesta lista</td>
</tr>
</tbody>
</table>




  

O servidor lê esses arquivos no início do servidor e sempre que a configuração do servidor é recarregada. Em sistemas Windows, eles também são lidos novamente sempre que um novo processo de backend é gerado para uma nova conexão do cliente.

Se um erro nesses arquivos for detectado no início do servidor, o servidor se negará a iniciar. Mas se um erro for detectado durante uma recarga da configuração, os arquivos são ignorados e a configuração SSL antiga continua sendo usada. Em sistemas Windows, se um erro nesses arquivos for detectado no início do backend, esse backend não conseguirá estabelecer uma conexão SSL. Em todos esses casos, a condição do erro é relatada no log do servidor.

### 18.9.5. Criar Certificados [#](#SSL-CERTIFICATE-CREATION)

Para criar um certificado autoassinado simples para o servidor, válido por 365 dias, use o seguinte comando do OpenSSL, substituindo *`dbhost.yourdomain.com`* pelo nome de host do servidor:

```
openssl req -new -x509 -days 365 -nodes -text -out server.crt \
  -keyout server.key -subj "/CN=dbhost.yourdomain.com"
```

Então faça:

```
chmod og-rwx server.key
```

porque o servidor rejeitará o arquivo se suas permissões forem mais liberais do que isso. Para mais detalhes sobre como criar sua chave privada e certificado do servidor, consulte a documentação do OpenSSL.

Embora um certificado autoassinado possa ser usado para testes, um certificado assinado por uma autoridade de certificação (CA) (geralmente uma CA raiz para toda a empresa) deve ser usado em produção.

Para criar um certificado de servidor cuja identidade possa ser validada pelos clientes, primeiro crie um pedido de assinatura de certificado (CSR) e um arquivo de chave pública/privada:

```
openssl req -new -nodes -text -out root.csr \
  -keyout root.key -subj "/CN=root.yourdomain.com"
chmod og-rwx root.key
```

Em seguida, assine o pedido com a chave para criar uma autoridade de certificação raiz (usando o local padrão do arquivo de configuração do OpenSSL no Linux):

```
openssl x509 -req -in root.csr -text -days 3650 \
  -extfile /etc/ssl/openssl.cnf -extensions v3_ca \
  -signkey root.key -out root.crt
```

Por fim, crie um certificado do servidor assinado pela nova autoridade de certificação raiz:

```
openssl req -new -nodes -text -out server.csr \
  -keyout server.key -subj "/CN=dbhost.yourdomain.com"
chmod og-rwx server.key

openssl x509 -req -in server.csr -text -days 365 \
  -CA root.crt -CAkey root.key -CAcreateserial \
  -out server.crt
```

`server.crt` e `server.key` devem ser armazenados no servidor, e `root.crt` deve ser armazenado no cliente, para que o cliente possa verificar se o certificado de folha do servidor foi assinado pelo seu certificado raiz de confiança. `root.key` deve ser armazenado offline para uso na criação de certificados futuros.

É também possível criar uma cadeia de confiança que inclua certificados intermediários:

```
# root
openssl req -new -nodes -text -out root.csr \
  -keyout root.key -subj "/CN=root.yourdomain.com"
chmod og-rwx root.key
openssl x509 -req -in root.csr -text -days 3650 \
  -extfile /etc/ssl/openssl.cnf -extensions v3_ca \
  -signkey root.key -out root.crt

# intermediate
openssl req -new -nodes -text -out intermediate.csr \
  -keyout intermediate.key -subj "/CN=intermediate.yourdomain.com"
chmod og-rwx intermediate.key
openssl x509 -req -in intermediate.csr -text -days 1825 \
  -extfile /etc/ssl/openssl.cnf -extensions v3_ca \
  -CA root.crt -CAkey root.key -CAcreateserial \
  -out intermediate.crt

# leaf
openssl req -new -nodes -text -out server.csr \
  -keyout server.key -subj "/CN=dbhost.yourdomain.com"
chmod og-rwx server.key
openssl x509 -req -in server.csr -text -days 365 \
  -CA intermediate.crt -CAkey intermediate.key -CAcreateserial \
  -out server.crt
```

`server.crt` e `intermediate.crt` devem ser concatenados em um pacote de arquivos de certificado e armazenados no servidor. `server.key` também deve ser armazenado no servidor. `root.crt` deve ser armazenado no cliente para que o cliente possa verificar que o certificado de folha do servidor foi assinado por uma cadeia de certificados ligados ao seu certificado raiz de confiança. `root.key` e `intermediate.key` devem ser armazenados offline para uso na criação de certificados futuros.