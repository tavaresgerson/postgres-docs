## F.42. sslinfo — obter informações SSL do cliente [#](#SSLINFO)

* [F.42.1. Funções Fornecidas](sslinfo.md#SSLINFO-FUNCTIONS)
* [F.42.2. Autor](sslinfo.md#SSLINFO-AUTHOR)

O módulo `sslinfo` fornece informações sobre o certificado SSL que o cliente atual forneceu ao se conectar ao PostgreSQL. O módulo é inútil (a maioria das funções retornará NULL) se a conexão atual não usar SSL.

Algumas das informações disponíveis através deste módulo também podem ser obtidas usando a visão do sistema embutido [[`pg_stat_ssl`][(monitoring-stats.md#MONITORING-PG-STAT-SSL-VIEW "27.2.10. pg_stat_ssl")]].

Essa extensão não será construída de forma alguma, a menos que a instalação tenha sido configurada com `--with-ssl=openssl`.

### F.42.1. Funções Fornecidas [#](#SSLINFO-FUNCTIONS)

`ssl_is_used() returns boolean`: Retorna verdadeiro se a conexão atual com o servidor usa SSL e falso caso contrário.

`ssl_version() returns text`: Retorna o nome do protocolo utilizado para a conexão SSL (por exemplo, TLSv1.0, TLSv1.1, TLSv1.2 ou TLSv1.3).

`ssl_cipher() returns text`: Retorna o nome do cifrador utilizado para a conexão SSL (por exemplo, DHE-RSA-AES256-SHA).

`ssl_client_cert_present() returns boolean`: Retorna verdadeiro se o cliente atual apresentou um certificado de cliente SSL válido ao servidor, e falso caso contrário. (O servidor pode ou não estar configurado para exigir um certificado de cliente.)

`ssl_client_serial() returns numeric`: Retorna o número de série do certificado atual do cliente. A combinação do número de série do certificado e do emissor do certificado é garantida para identificar de forma única um certificado (mas não seu proprietário — o proprietário deve alterar regularmente suas chaves e obter novos certificados do emissor).

Então, se você gerencia sua própria CA e permite que apenas certificados dessa CA sejam aceitos pelo servidor, o número de série é o meio mais confiável (embora não muito memorável) para identificar um usuário.

`ssl_client_dn() returns text`: Retorna o sujeito completo do certificado do cliente atual, convertendo dados de caracteres no codificação do banco de dados atual. Assume-se que, se você usar caracteres não ASCII nos nomes do certificado, seu banco de dados também é capaz de representar esses caracteres. Se o seu banco de dados usa o codificação SQL_ASCII, caracteres não ASCII no nome serão representados como sequências UTF-8.

O resultado parece ser `/CN=Somebody /C=Some country/O=Some organization`.

`ssl_issuer_dn() returns text`: Retorna o nome completo do emissor do certificado do cliente atual, convertendo dados de caracteres no codificação do banco de dados atual. As conversões de codificação são tratadas da mesma forma que para `ssl_client_dn`.

A combinação do valor de retorno dessa função com o número de série do certificado identifica de forma única o certificado.

Essa função é realmente útil apenas se você tiver mais de um certificado de CA confiável no arquivo de autoridade de certificado do seu servidor, ou se essa CA tenha emitido alguns certificados de autoridade de certificado intermediária.

`ssl_client_dn_field(fieldname text) returns text`: Esta função retorna o valor do campo especificado no sujeito do certificado, ou NULL se o campo não estiver presente. Os nomes dos campos são constantes de string que são convertidas em identificadores de objeto ASN1 usando o banco de dados de objetos OpenSSL. Os seguintes valores são aceitáveis:

``` commonName (alias CN) surname (alias SN) name givenName (alias GN) countryName (alias C) localityName (alias L) stateOrProvinceName (alias ST) organizationName (alias O) organizationalUnitName (alias OU) title description initials postalCode streetAddress generationQualifier description dnQualifier x500UniqueIdentifier pseudonym role emailAddress
    ```

Todos esses campos são opcionais, exceto `commonName`. Depende inteiramente da política da sua CA qual deles será incluído e qual não será. O significado desses campos, no entanto, é estritamente definido pelas normas X.500 e X.509, então você não pode simplesmente atribuir um significado arbitrário a eles.

`ssl_issuer_field(fieldname text) returns text`: Igual a `ssl_client_dn_field`, mas para o emissor do certificado e não para o sujeito do certificado.

`ssl_extension_info() returns setof record`: Forneça informações sobre as extensões do certificado do cliente: nome da extensão, valor da extensão e se é uma extensão crítica.

### F.42.2. Autor [#](#SSLINFO-AUTHOR)

Victor Wagner `<vitus@cryptocom.ru>`, Cryptocom LTD

Dmitry Voronin `<carriingfate92@yandex.ru>`

E-mail do grupo de desenvolvimento do Cryptocom OpenSSL: `<openssl@cryptocom.ru>`