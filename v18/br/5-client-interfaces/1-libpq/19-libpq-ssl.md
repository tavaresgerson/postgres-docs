## 32.19. Suporte SSL [#](#LIBPQ-SSL)

* [32.19.1. Verificação do Cliente dos Certificados do Servidor](libpq-ssl.md#LIBQ-SSL-CERTIFICATES)
* [32.19.2. Certificados do Cliente](libpq-ssl.md#LIBPQ-SSL-CLIENTCERT)
* [32.19.3. Proteção Fornecida em Diferentes Modos](libpq-ssl.md#LIBPQ-SSL-PROTECTION)
* [32.19.4. Uso do Arquivo de Cliente SSL](libpq-ssl.md#LIBPQ-SSL-FILEUSAGE)
* [32.19.5. Inicialização da Biblioteca SSL](libpq-ssl.md#LIBPQ-SSL-INITIALIZE)

O PostgreSQL tem suporte nativo para usar conexões SSL para criptografar comunicações cliente/servidor usando protocolos TLS para maior segurança. Consulte a [Seção 18.9] para obter detalhes sobre a funcionalidade SSL do lado do servidor.

O libpq lê o arquivo de configuração do OpenSSL de nível de sistema. Por padrão, esse arquivo é chamado `openssl.cnf` e está localizado no diretório informado pelo `openssl version -d`. Esse padrão pode ser ignorado definindo a variável de ambiente `OPENSSL_CONF` com o nome do arquivo de configuração desejado.

### 32.19.1. Verificação do cliente dos certificados do servidor [#](#LIBQ-SSL-CERTIFICATES)

Por padrão, o PostgreSQL não realizará nenhuma verificação do certificado do servidor. Isso significa que é possível falsificar a identidade do servidor (por exemplo, modificando um registro DNS ou assumindo o endereço IP do servidor) sem que o cliente saiba. Para evitar a falsificação, o cliente deve ser capaz de verificar a identidade do servidor por meio de uma cadeia de confiança. Uma cadeia de confiança é estabelecida colocando um certificado de autoridade de certificação (CA) raiz (autoassinado) em um computador e um certificado de folha *assinado* pelo certificado raiz em outro computador. Também é possível usar um certificado "intermediário" que é assinado pelo certificado raiz e assina certificados de folha.

Para permitir que o cliente verifique a identidade do servidor, coloque um certificado raiz no cliente e um certificado de folha assinado pelo certificado raiz no servidor. Para permitir que o servidor verifique a identidade do cliente, coloque um certificado raiz no servidor e um certificado de folha assinado pelo certificado raiz no cliente. Um ou mais certificados intermediários (geralmente armazenados com o certificado de folha) também podem ser usados para vincular o certificado de folha ao certificado raiz.

Uma vez que uma cadeia de confiança tenha sido estabelecida, há duas maneiras para o cliente validar o certificado de folha enviado pelo servidor. Se o parâmetro `sslmode` estiver definido como `verify-ca`, o libpq verificará se o servidor é confiável, verificando a cadeia de certificados até o certificado raiz armazenado no cliente. Se `sslmode` estiver definido como `verify-full`, o libpq *também* verificará se o nome do host do servidor corresponde ao nome armazenado no certificado do servidor. A conexão SSL falhará se o certificado do servidor não puder ser verificado. `verify-full` é recomendado na maioria dos ambientes sensíveis à segurança.

No modo `verify-full`, o nome do host é comparado com o(s) atributo(s) de Nome Alternativo do Certificado (SAN), ou com o atributo de Nome Comum se não houver nenhum SAN do tipo `dNSName`. Se o atributo de nome do certificado começar com um asterisco (`*`,), o asterisco será tratado como um caractere wildcard, que corresponderá a todos os caracteres *exceto* um ponto (`.`). Isso significa que o certificado não corresponderá a subdomínios. Se a conexão for feita usando um endereço IP em vez de um nome de host, o endereço IP será comparado (sem fazer qualquer pesquisa DNS) com SANs do tipo `iPAddress` ou `dNSName`. Se não houver nenhum SAN `iPAddress` e não houver nenhum SAN de correspondência `dNSName`, o endereço IP do host será comparado com o atributo de Nome Comum.

Nota

Para compatibilidade reversa com versões anteriores do PostgreSQL, o endereço IP do host é verificado de uma maneira diferente de [RFC 6125](https://datatracker.ietf.org/doc/html/rfc6125). O endereço IP do host é sempre verificado contra SANs `dNSName` e `iPAddress`, e pode ser verificado contra o atributo Common Name se não houver SANs relevantes.

Para permitir a verificação do certificado do servidor, um ou mais certificados raiz devem ser colocados no arquivo `~/.postgresql/root.crt` no diretório de usuário. (No Microsoft Windows, o arquivo é denominado `%APPDATA%\postgresql\root.crt`.) Certificados intermediários também devem ser adicionados ao arquivo se forem necessários para vincular a cadeia de certificados enviada pelo servidor aos certificados raiz armazenados no cliente.

As entradas da Lista de Revogação de Certificado (CRL) também são verificadas se o arquivo `~/.postgresql/root.crl` existir (`%APPDATA%\postgresql\root.crl` no Microsoft Windows).

A localização do arquivo de certificado raiz e do CRL pode ser alterada definindo os parâmetros de conexão `sslrootcert` e `sslcrl` ou as variáveis de ambiente `PGSSLROOTCERT` e `PGSSLCRL`. `sslcrldir` ou a variável de ambiente `PGSSLCRLDIR` também pode ser usada para especificar um diretório que contenha arquivos de CRL.

Nota

Para compatibilidade reversa com versões anteriores do PostgreSQL, se um arquivo de CA raiz existir, o comportamento do `sslmode=require` será o mesmo do `verify-ca`, o que significa que o certificado do servidor é validado contra a CA. Confiar nesse comportamento é desencorajado, e as aplicações que precisam de validação de certificado devem sempre usar `verify-ca` ou `verify-full`.

### 32.19.2. Certificados do cliente [#](#LIBPQ-SSL-CLIENTCERT)

Se o servidor tentar verificar a identidade do cliente, solicitando o certificado de folha do cliente, o libpq enviará os certificados armazenados no arquivo `~/.postgresql/postgresql.crt` no diretório doméstico do usuário. Os certificados devem estar em cadeia com o certificado raiz confiável pelo servidor. Também deve estar presente um arquivo de chave privada correspondente `~/.postgresql/postgresql.key`. Em sistemas Microsoft Windows, esses arquivos são nomeados `%APPDATA%\postgresql\postgresql.crt` e `%APPDATA%\postgresql\postgresql.key`. A localização dos arquivos de certificado e chave pode ser sobrescrita pelos parâmetros de conexão `sslcert` e `sslkey`, ou pelas variáveis de ambiente `PGSSLCERT` e `PGSSLKEY`.

Nos sistemas Unix, as permissões no arquivo da chave privada devem impedir qualquer acesso ao mundo ou ao grupo; para isso, use um comando como `chmod 0600 ~/.postgresql/postgresql.key`. Alternativamente, o arquivo pode ser de propriedade do root e ter acesso de leitura do grupo (ou seja, as permissões `0640`). Esse esquema é destinado a instalações onde os arquivos de certificado e chave são gerenciados pelo sistema operacional. O usuário do libpq deve, então, ser membro do grupo que tem acesso a esses arquivos de certificado e chave. (Em Microsoft Windows, não há verificação de permissões de arquivo, uma vez que o diretório `%APPDATA%\postgresql` é presumido seguro.)

O primeiro certificado em `postgresql.crt` deve ser o certificado do cliente, pois ele deve corresponder à chave privada do cliente. Os certificados “intermediários” podem ser anexados opcionalmente ao arquivo — isso evita a necessidade de armazenamento de certificados intermediários no servidor ([ssl_ca_file](runtime-config-connection.md#GUC-SSL-CA-FILE)).

O certificado e a chave podem estar no formato PEM ou ASN.1 DER.

A chave pode ser armazenada em texto claro ou criptografada com uma senha usando qualquer algoritmo suportado pelo OpenSSL, como AES-128. Se a chave for armazenada criptografada, a senha pode ser fornecida na opção de conexão [sslpassword](libpq-connect.md#LIBPQ-CONNECT-SSLPASSWORD). Se uma chave criptografada for fornecida e a opção `sslpassword` estiver ausente ou em branco, a senha será solicitada interativamente pelo OpenSSL com um prompt `Enter PEM pass phrase:` se um TTY estiver disponível. As aplicações podem sobrepor o prompt do certificado do cliente e o tratamento do parâmetro `sslpassword` fornecendo seu próprio callback de senha da chave; veja [`PQsetSSLKeyPassHook_OpenSSL`](libpq-connect.md#LIBPQ-PQSETSSLKEYPASSHOOK-OPENSSL).

Para obter instruções sobre como criar certificados, consulte [Seção 18.9.5](ssl-tcp.md#SSL-CERTIFICATE-CREATION).

### 32.19.3. Proteção fornecida em diferentes modos [#](#LIBPQ-SSL-PROTECTION)

Os diferentes valores para o parâmetro `sslmode` fornecem diferentes níveis de proteção. O SSL pode fornecer proteção contra três tipos de ataques:

Escutando: Se um terceiro puder examinar o tráfego de rede entre o cliente e o servidor, ele pode ler as informações de conexão (incluindo o nome de usuário e a senha) e os dados que são passados. O SSL usa criptografia para evitar isso.

Man-in-the-middle (MITM): Se um terceiro pode modificar os dados enquanto passa entre o cliente e o servidor, ele pode fingir ser o servidor e, portanto, ver e modificar dados *mesmo que estejam criptografados*. O terceiro pode, então, encaminhar as informações de conexão e os dados para o servidor original, tornando impossível detectar esse ataque. Vectores comuns para fazer isso incluem envenenamento de DNS e seqüestro de endereços, pelo qual o cliente é direcionado para um servidor diferente do pretendido. Existem também vários outros métodos de ataque que podem realizar isso. O SSL usa a verificação de certificados para prevenir isso, autentificando o servidor para o cliente.

Imitação: Se um terceiro pode fingir ser um cliente autorizado, ele pode simplesmente acessar dados que não deveria ter acesso. Normalmente, isso pode acontecer por meio de gerenciamento de senha inseguro. O SSL usa certificados de cliente para evitar isso, garantindo que apenas os detentores de certificados válidos possam acessar o servidor.

Para que uma conexão seja conhecida como SSL-segura, o uso do SSL deve ser configurado em *ambos o cliente e o servidor* antes de a conexão ser feita. Se for configurado apenas no servidor, o cliente pode acabar enviando informações sensíveis (por exemplo, senhas) antes de saber que o servidor requer alta segurança. No libpq, conexões seguras podem ser garantidas definindo o parâmetro `sslmode` para `verify-full` ou `verify-ca`, e fornecendo ao sistema um certificado raiz para verificação. Isso é análogo ao uso de um URL `https` para navegação na web criptografada.

Uma vez que o servidor tenha sido autenticado, o cliente pode passar dados sensíveis. Isso significa que, até esse ponto, o cliente não precisa saber se os certificados serão usados para autenticação, o que torna seguro especificar isso apenas na configuração do servidor.

Todas as opções de SSL apresentam custos na forma de criptografia e troca de chaves, portanto, há um compromisso que deve ser feito entre desempenho e segurança. [Tabela 32.1](libpq-ssl.md#LIBPQ-SSL-SSLMODE-STATEMENTS "Table 32.1. SSL Mode Descriptions") ilustra os riscos que os diferentes valores de `sslmode` protegem contra e o que eles dizem sobre segurança e custos.

**Tabela 32.1. Descrições do Modo SSL**



<table border="1" class="table" summary="SSL Mode Descriptions">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
  <col class="col4"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    <code class="literal">
     sslmode
    </code>
   </th>
   <th>
    Eavesdropping protection
   </th>
   <th>
    <acronym class="acronym">
     MITM
    </acronym>
    protection
   </th>
   <th>
    Declaração
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     disable
    </code>
   </td>
   <td>
    No
   </td>
   <td>
    No
   </td>
   <td>
    Não me importo com a segurança e não quero pagar as despesas com criptografia.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     allow
    </code>
   </td>
   <td>
    Maybe
   </td>
   <td>
    No
   </td>
   <td>
    Não me importo com a segurança, mas vou pagar o custo da criptografia se o servidor insistir nisso.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     prefer
    </code>
   </td>
   <td>
    Maybe
   </td>
   <td>
    No
   </td>
   <td>
    Não me importo com a criptografia, mas gostaria de pagar o custo da criptografia se o servidor a suportar.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     require
    </code>
   </td>
   <td>
    Yes
   </td>
   <td>
    No
   </td>
   <td>
    Eu quero que meus dados sejam criptografados e aceito o custo adicional. Confio que a rede se encarregará de garantir que eu sempre me conecte ao servidor que quero.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     verify-ca
    </code>
   </td>
   <td>
    Yes
   </td>
   <td>
    Depends on CA policy
   </td>
   <td>
    Eu quero meus dados criptografados e aceito o custo adicional. Quero ter certeza de que me conecto a um servidor em que confio.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     verify-full
    </code>
   </td>
   <td>
    Yes
   </td>
   <td>
    Yes
   </td>
   <td>
    Eu quero meus dados criptografados e aceito o custo adicional. Quero ter certeza de que me conecto a um servidor em que confio e que é o que especifico.
   </td>
  </tr>
 </tbody>
</table>










A diferença entre `verify-ca` e `verify-full` depende da política da CA raiz. Se uma CA pública for usada, `verify-ca` permite conexões a um servidor que *alguém mais* pode ter registrado com a CA. Neste caso, `verify-full` deve ser sempre usado. Se uma CA local for usada, ou até mesmo um certificado autoassinado, usar `verify-ca` muitas vezes oferece proteção suficiente.

O valor padrão para `sslmode` é `prefer`. Como mostrado na tabela, isso não faz sentido do ponto de vista de segurança, e promete apenas sobrecarga de desempenho se possível. É fornecido apenas como padrão para compatibilidade reversa e não é recomendado em implantações seguras.

### 32.19.4. Uso do arquivo de cliente SSL [#](#LIBPQ-SSL-FILEUSAGE)

[Tabela 32.2](libpq-ssl.md#LIBPQ-SSL-FILE-USAGE) resume os arquivos que são relevantes para a configuração SSL no cliente.

**Tabela 32.2. Uso do arquivo SSL Libpq/Client**



<table border="1" class="table" summary="Libpq/Client SSL File Usage">
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
   <th>
    Conteúdo
   </th>
   <th>
    Efeito
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="filename">
     ~/.postgresql/postgresql.crt
    </code>
   </td>
   <td>
    certificado do cliente
   </td>
   <td>
    enviado ao servidor
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     ~/.postgresql/postgresql.key
    </code>
   </td>
   <td>
    chave privada do cliente
   </td>
   <td>
    prova que o certificado do cliente foi enviado pelo proprietário; não indica que o proprietário do certificado é confiável
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     ~/.postgresql/root.crt
    </code>
   </td>
   <td>
    autoridades de certificação confiáveis
   </td>
   <td>
    verifica que o certificado do servidor é assinado por uma autoridade de certificação confiável
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     ~/.postgresql/root.crl
    </code>
   </td>
   <td>
    certificados revogados por autoridades de certificação
   </td>
   <td>
    o certificado do servidor não deve estar nesta lista
   </td>
  </tr>
 </tbody>
</table>







### 32.19.5. Inicialização da Biblioteca SSL [#](#LIBPQ-SSL-INITIALIZE)

Os aplicativos que precisam ser compatíveis com versões mais antigas do PostgreSQL, usando a versão OpenSSL 1.0.2 ou versões anteriores, precisam inicializar a biblioteca SSL antes de usá-la. Os aplicativos que inicializam as bibliotecas `libssl` e/ou `libcrypto` devem chamar `PQinitOpenSSL`(libpq-ssl.md#LIBPQ-PQINITOPENSSL) para informar ao libpq que as bibliotecas `libssl` e/ou `libcrypto` foram inicializadas pelo aplicativo, para que o libpq não inicialize essas bibliotecas também. No entanto, isso é desnecessário ao usar a versão OpenSSL 1.1.0 ou posterior, pois as inicializações duplicadas não são mais problemáticas.

Consulte a documentação da versão do PostgreSQL que você está utilizando para obter detalhes sobre seu uso.

`PQinitOpenSSL` [#](#LIBPQ-PQINITOPENSSL): Permite que os aplicativos selecionem quais bibliotecas de segurança devem ser inicializadas.

```
void PQinitOpenSSL(int do_ssl, int do_crypto);
```

Essa função é desatualizada e está presente apenas para compatibilidade reversa, ela não faz nada.

`PQinitSSL` [#](#LIBPQ-PQINITSSL): Permite que os aplicativos selecionem quais bibliotecas de segurança devem ser inicializadas.

```
void PQinitSSL(int do_ssl);
```

Essa função é equivalente a `PQinitOpenSSL(do_ssl, do_ssl)`. Essa função é descontinuada e apenas presente para compatibilidade reversa, ela não faz nada.

[`PQinitSSL`](libpq-ssl.md#LIBPQ-PQINITSSL) e [`PQinitOpenSSL`](libpq-ssl.md#LIBPQ-PQINITOPENSSL) são mantidos para compatibilidade reversa, mas não são mais necessários desde o PostgreSQL 18. [`PQinitSSL`](libpq-ssl.md#LIBPQ-PQINITSSL) está presente desde o PostgreSQL 8.0, enquanto [`PQinitOpenSSL`](libpq-ssl.md#LIBPQ-PQINITOPENSSL) foi adicionado no PostgreSQL 8.4, então [`PQinitSSL`](libpq-ssl.md#LIBPQ-PQINITSSL) pode ser preferível para aplicações que precisam trabalhar com versões mais antigas do libpq.