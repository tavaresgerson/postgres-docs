## 32.2. Funções de Status de Conexão [#](#LIBPQ-STATUS)

Essas funções podem ser usadas para interrogar o status de um objeto de conexão de banco de dados existente.

### DICA

Os programadores de aplicativos libpq devem ter cuidado para manter a abstração `PGconn`. Use as funções de acesso descritas abaixo para acessar o conteúdo de `PGconn`. Não é recomendado fazer referência a campos internos de `PGconn` usando `libpq-int.h`, pois eles estão sujeitos a mudanças no futuro.

As seguintes funções retornam valores de parâmetro estabelecidos na conexão. Esses valores são fixos durante a vida útil da conexão. Se uma cadeia de conexão multi-host for usada, os valores de `PQhost`(libpq-status.md#LIBPQ-PQHOST), [`PQport`](libpq-status.md#LIBPQ-PQPORT) e [`PQpass`](libpq-status.md#LIBPQ-PQPASS) podem mudar se uma nova conexão for estabelecida usando o mesmo objeto `PGconn`. Outros valores são fixos para a vida útil do objeto `PGconn`.

`PQdb` [#](#LIBPQ-PQDB): Retorna o nome do banco de dados da conexão.

```
char *PQdb(const PGconn *conn);
```

`PQuser` [#](#LIBPQ-PQUSER): Retorna o nome do usuário da conexão.

```
char *PQuser(const PGconn *conn);
```

`PQpass` [#](#LIBPQ-PQPASS): Retorna a senha da conexão.

```
char *PQpass(const PGconn *conn);
```

`PQpass`](libpq-status.md#LIBPQ-PQPASS) retornará a senha especificada nos parâmetros de conexão, ou, se não houver nenhuma senha e a senha foi obtida do arquivo de senha [Senha](libpq-pgpass.md "32.16. O arquivo de senha"), ele retornará essa senha. No último caso, se vários hosts foram especificados nos parâmetros de conexão, não é possível confiar no resultado de `PQpass`(libpq-status.md#LIBPQ-PQPASS) até que a conexão seja estabelecida. O status da conexão pode ser verificado usando a função `PQstatus`(libpq-status.md#LIBPQ-PQSTATUS).

`PQhost` [#](#LIBPQ-PQHOST): Retorna o nome do host do servidor da conexão ativa. Isso pode ser um nome de host, um endereço IP ou um caminho de diretório se a conexão for via Unix socket. (O caminho pode ser distinguido porque sempre será um caminho absoluto, começando com `/`.)

```
char *PQhost(const PGconn *conn);
```

Se os parâmetros de conexão especificados tanto para `host` quanto para `hostaddr`, então [[`PQhost`](libpq-status.md#LIBPQ-PQHOST)]] retornará as informações do `host`. Se apenas `hostaddr` foi especificado, então isso será retornado. Se vários hosts foram especificados nos parâmetros de conexão, [[`PQhost`](libpq-status.md#LIBPQ-PQHOST)]] retorna o host que está realmente conectado.

`PQhost` retorna (libpq-status.md#LIBPQ-PQHOST) se o argumento `NULL` for. Caso contrário, se houver um erro na produção das informações do host (talvez se a conexão não tiver sido totalmente estabelecida ou houver ocorrido um erro), ele retorna uma string vazia.

Se vários hosts foram especificados nos parâmetros de conexão, não é possível confiar no resultado de `PQhost`(libpq-status.md#LIBPQ-PQHOST) até que a conexão seja estabelecida. O status da conexão pode ser verificado usando a função `PQstatus`(libpq-status.md#LIBPQ-PQSTATUS).

`PQhostaddr` [#](#LIBPQ-PQHOSTADDR): Retorna o endereço IP do servidor da conexão ativa. Isso pode ser o endereço para o qual um nome de host foi resolvido, ou um endereço IP fornecido através do parâmetro `hostaddr` .

```
char *PQhostaddr(const PGconn *conn);
```

`PQhostaddr`](libpq-status.md#LIBPQ-PQHOSTADDR) retorna `NULL` se o argumento *`conn`* for `NULL`. Caso contrário, se houver um erro na produção das informações do host (talvez se a conexão não tiver sido totalmente estabelecida ou houve um erro), ele retorna uma string vazia.

`PQport` [#](#LIBPQ-PQPORT) :  Retorna a porta da conexão ativa.

```
char *PQport(const PGconn *conn);
```

Se vários ports foram especificados nos parâmetros de conexão, `PQport` retorna o port que está realmente conectado.

`PQport` (libpq-status.md#LIBPQ-PQPORT) retorna `NULL` se o argumento *`conn`* for `NULL`. Caso contrário, se houver um erro na produção das informações da porta (talvez se a conexão não tiver sido totalmente estabelecida ou houver ocorrido um erro), ele retorna uma string vazia.

Se vários ports forem especificados nos parâmetros de conexão, não é possível confiar no resultado de `PQport`(libpq-status.md#LIBPQ-PQPORT) até que a conexão seja estabelecida. O status da conexão pode ser verificado usando a função `PQstatus`(libpq-status.md#LIBPQ-PQSTATUS).

`PQtty` [#](#LIBPQ-PQTTY): Essa função não faz mais nada, mas permanece para compatibilidade através. A função sempre retorna uma string vazia, ou `NULL` se o argumento *`conn`* for `NULL`.

```
char *PQtty(const PGconn *conn);
```

`PQoptions` [#](#LIBPQ-PQOPTIONS): Retorna as opções de linha de comando passadas na solicitação de conexão.

```
char *PQoptions(const PGconn *conn);
```

As funções a seguir retornam dados de status que podem mudar conforme as operações são executadas no objeto `PGconn`.

`PQstatus` [#](#LIBPQ-PQSTATUS) :  Retorna o status da conexão.

```
ConnStatusType PQstatus(const PGconn *conn);
```

O status pode ser um dos vários valores. No entanto, apenas dois desses são vistos fora de um procedimento de conexão assíncrona: `CONNECTION_OK` e `CONNECTION_BAD`. Uma boa conexão com o banco de dados tem o status `CONNECTION_OK`. Uma tentativa de conexão fracassada é sinalizada pelo status `CONNECTION_BAD`. Normalmente, um status OK permanecerá assim até `PQfinish`(libpq-connect.md#LIBPQ-PQFINISH), mas uma falha de comunicação pode resultar no status mudar para `CONNECTION_BAD` prematuramente. Nesse caso, o aplicativo pode tentar recuperar chamando `PQreset`(libpq-connect.md#LIBPQ-PQRESET).

Veja a entrada para `PQconnectStartParams`(libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS), `PQconnectStart` e `PQconnectPoll` em relação a outros códigos de status que podem ser retornados.

`PQtransactionStatus` [#](#LIBPQ-PQTRANSACTIONSTATUS) :  Retorna o status atual da transação do servidor.

```
PGTransactionStatusType PQtransactionStatus(const PGconn *conn);
```

O status pode ser `PQTRANS_IDLE` (atualmente inativo), `PQTRANS_ACTIVE` (um comando está em andamento), `PQTRANS_INTRANS` (ativo, em um bloco de transação válido), ou `PQTRANS_INERROR` (ativo, em um bloco de transação falha). `PQTRANS_UNKNOWN` é relatado se a conexão estiver ruim. `PQTRANS_ACTIVE` é relatado apenas quando uma consulta foi enviada ao servidor e ainda não foi concluída.

`PQparameterStatus` [#](#LIBPQ-PQPARAMETERSTATUS) :   Busca um parâmetro atual do servidor.

```
const char *PQparameterStatus(const PGconn *conn, const char *paramName);
```

Certos valores de parâmetros são reportados pelo servidor automaticamente na inicialização da conexão ou sempre que seus valores mudam. `PQparameterStatus`(libpq-status.md#LIBPQ-PQPARAMETERSTATUS) pode ser usado para interrogar essas configurações. Retorna o valor atual de um parâmetro se conhecido, ou `NULL` se o parâmetro não é conhecido.

Os parâmetros relatados a partir da versão atual incluem:



<table border="0" class="simplelist" summary="Simple list">
 <tr>
  <td>
   <code class="varname">
    application_name
   </code>
  </td>
  <td>
   <code class="varname">
    scram_iterations
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="varname">
    client_encoding
   </code>
  </td>
  <td>
   <code class="varname">
    search_path
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="varname">
    DateStyle
   </code>
  </td>
  <td>
   <code class="varname">
    server_encoding
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="varname">
    default_transaction_read_only
   </code>
  </td>
  <td>
   <code class="varname">
    server_version
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="varname">
    in_hot_standby
   </code>
  </td>
  <td>
   <code class="varname">
    session_authorization
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="varname">
    integer_datetimes
   </code>
  </td>
  <td>
   <code class="varname">
    standard_conforming_strings
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="varname">
    IntervalStyle
   </code>
  </td>
  <td>
   <code class="varname">
    TimeZone
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="varname">
    is_superuser
   </code>
  </td>
  <td>
  </td>
 </tr>
</table>






(`default_transaction_read_only` e `in_hot_standby` não foram relatados em lançamentos antes de 14; `scram_iterations` não foi relatado em lançamentos antes de 16; `search_path` não foi relatado em lançamentos antes de 18.) Observe que `server_version`, `server_encoding` e `integer_datetimes` não podem ser alterados após a inicialização.

Se não for informado nenhum valor para `standard_conforming_strings`, as aplicações podem assumir que é `off`, ou seja, barras invertidas são tratadas como escapamentos em literais de string. Além disso, a presença deste parâmetro pode ser considerada como uma indicação de que a sintaxe de string de escapamento (`E'...'`) é aceita.

Embora o ponteiro retornado seja declarado `const`, ele, na verdade, aponta para armazenamento mutável associado à estrutura `PGconn`. Não é prudente assumir que o ponteiro permanecerá válido em todas as consultas.

`PQfullProtocolVersion` [#](#LIBPQ-PQFULLPROTOCOLVERSION) :   Interroga o protocolo de frontend/backend que está sendo usado.

```
int PQfullProtocolVersion(const PGconn *conn);
```

As aplicações podem querer usar essa função para determinar se certas funcionalidades são suportadas. O resultado é formado multiplicando o número da versão principal do servidor por 10000 e adicionando o número da versão menor. Por exemplo, a versão 3.2 seria devolvida como 30002, e a versão 4.0 seria devolvida como 40000. Zero é devolvido se a conexão estiver ruim. O protocolo 3.0 é suportado pelas versões do servidor PostgreSQL 7.4 e superiores.

A versão do protocolo não mudará após a inicialização da conexão estar completa, mas teoricamente poderia mudar durante um reajuste da conexão.

`PQprotocolVersion` [#](#LIBPQ-PQPROTOCOLVERSION) :   Interroga a versão principal do protocolo frontend/backend.

```
int PQprotocolVersion(const PGconn *conn);
```

Ao contrário de `PQfullProtocolVersion`(libpq-status.md#LIBPQ-PQFULLPROTOCOLVERSION), este retorna apenas a versão do protocolo principal em uso, mas é suportada por uma gama mais ampla de versões do libpq, desde a versão 7.4. Atualmente, os valores possíveis são 3 (protocolo 3.0) ou zero (conexão ruim). Antes da versão 14.0, o libpq também podia retornar 2 (protocolo 2.0).

`PQserverVersion` [#](#LIBPQ-PQSERVERVERSION): Retorna um número inteiro que representa a versão do servidor.

```
int PQserverVersion(const PGconn *conn);
```

As aplicações podem usar essa função para determinar a versão do servidor de banco de dados a que estão conectadas. O resultado é formado multiplicando o número da versão principal do servidor por 10000 e adicionando o número da versão menor. Por exemplo, a versão 10.1 será retornada como 100001, e a versão 11.0 será retornada como 110000. Zero será retornado se a conexão estiver ruim.

Antes da versão principal 10, o PostgreSQL usava números de versão de três partes, nas quais as duas primeiras partes juntas representavam a versão principal. Para essas versões, `PQserverVersion`[(libpq-status.md#LIBPQ-PQSERVERVERSION)] usa dois dígitos para cada parte; por exemplo, a versão 9.1.5 será retornada como 90105, e a versão 9.2.0 será retornada como 90200.

Portanto, para fins de determinação da compatibilidade de recursos, as aplicações devem dividir o resultado de `PQserverVersion`(libpq-status.md#LIBPQ-PQSERVERVERSION) por 100 e não por 10000 para determinar um número lógico de versão principal. Em todas as séries de lançamento, apenas os dois últimos dígitos diferem entre as versões menores (releases de correção de bugs).

`PQerrorMessage` [#](#LIBPQ-PQERRORMESSAGE): Retorna a mensagem de erro gerada mais recentemente por uma operação na conexão.

```
char *PQerrorMessage(const PGconn *conn);
```

Quase todas as funções do libpq definirão uma mensagem se falharem. Observe que, de acordo com a convenção do libpq, um resultado não vazio `PQerrorMessage` pode consistir em várias linhas e incluirá uma nova linha final. O chamador não deve liberar o resultado diretamente. Ele será liberado quando o handle associado `PGconn` for passado para `PQfinish`. A string de resultado não deve ser esperada para permanecer a mesma em operações na estrutura `PGconn`.

`PQsocket` [#](#LIBPQ-PQSOCKET) Obtém o número de descritor de arquivo do socket de conexão com o servidor. Um descritor válido será maior ou igual a 0; um resultado de -1 indica que nenhuma conexão com o servidor está aberta atualmente. (Isso não mudará durante o funcionamento normal, mas pode mudar durante a configuração ou reinicialização da conexão.)

```
int PQsocket(const PGconn *conn);
```

`PQbackendPID` [#](#LIBPQ-PQBACKENDPID): Retorna o ID do processo (PID) do processo de backend que está lidando com essa conexão.

```
int PQbackendPID(const PGconn *conn);
```

O PID do backend é útil para fins de depuração e para comparação com as mensagens `NOTIFY` (que incluem o PID do processo de backend notificador). Observe que o PID pertence a um processo que está sendo executado no host do servidor de banco de dados, e não no host local!

`PQconnectionNeedsPassword` [#](#LIBPQ-PQCONNECTIONNEEDSPASSWORD): Retorna verdadeiro (1) se o método de autenticação de conexão exigiu uma senha, mas nenhuma estava disponível. Retorna falso (0) se não for o caso.

```
int PQconnectionNeedsPassword(const PGconn *conn);
```

Essa função pode ser aplicada após uma tentativa de conexão falhada para decidir se deve solicitar uma senha ao usuário.

`PQconnectionUsedPassword` [#](#LIBPQ-PQCONNECTIONUSEDPASSWORD): Retorna verdadeiro (1) se o método de autenticação de conexão usou uma senha. Retorna falso (0) se

```
int PQconnectionUsedPassword(const PGconn *conn);
```

Essa função pode ser aplicada após uma tentativa de conexão bem-sucedida ou não, para detectar se o servidor exigiu uma senha.

`PQconnectionUsedGSSAPI` [#](#LIBPQ-PQCONNECTIONUSEDGSSAPI): Retorna verdadeiro (1) se o método de autenticação de conexão utilizado for GSSAPI. Retorna falso (0) se não for.

```
int PQconnectionUsedGSSAPI(const PGconn *conn);
```

Essa função pode ser aplicada para detectar se a conexão foi autenticada com GSSAPI.

As funções a seguir retornam informações relacionadas ao SSL. Essas informações geralmente não mudam após a conexão ser estabelecida.

`PQsslInUse` [#](#LIBPQ-PQSSLINUSE) :   Retorna verdadeiro (1) se a conexão usa SSL, falso (0) se

```
int PQsslInUse(const PGconn *conn);
```

`PQsslAttribute` [#](#LIBPQ-PQSSLATTRIBUTE): Retorna informações relacionadas ao SSL sobre a conexão.

```
const char *PQsslAttribute(const PGconn *conn, const char *attribute_name);
```

A lista de atributos disponíveis varia conforme a biblioteca SSL que está sendo utilizada e o tipo de conexão. Retorna NULL se a conexão não utilizar SSL ou se o nome do atributo especificado não estiver definido para a biblioteca em uso.

Os seguintes atributos são comumente disponíveis:

`library`: Nome da implementação SSL em uso. (Atualmente, apenas o `"OpenSSL"` é implementado)

`protocol`: Versão do SSL/TLS em uso. Os valores comuns são `"TLSv1"`, `"TLSv1.1"` e `"TLSv1.2"`, mas uma implementação pode retornar outras strings se algum outro protocolo for usado.

`key_bits`: Número de bits chave utilizados pelo algoritmo de criptografia.

`cipher` :   Um nome curto do conjunto de cifra utilizado, por exemplo, `"DHE-RSA-DES-CBC3-SHA"`. Os nomes são específicos para cada implementação SSL.

`compression` : Retorna "on" se a compressão SSL estiver em uso, caso contrário, retorna "off".

`alpn`: Protocolo de aplicação selecionado pela extensão de Negociação de Protocolo de Camada de Aplicação (ALPN) TLS. O único protocolo suportado pelo libpq é `postgresql`, portanto, isso é principalmente útil para verificar se o servidor suportou ALPN ou não. String vazia se ALPN não foi usado.

Como um caso especial, o atributo `library` pode ser requerido sem uma conexão, passando NULL como o argumento `conn`. O resultado será o nome padrão da biblioteca SSL, ou NULL se a libpq foi compilada sem qualquer suporte SSL. (Antes da versão 15 do PostgreSQL, passar NULL como o argumento `conn` sempre resultou em NULL. Os programas do cliente que precisam diferenciar entre as implementações mais novas e mais antigas deste caso podem verificar a macro de recurso `LIBPQ_HAS_SSL_LIBRARY_DETECTION`.

`PQsslAttributeNames` [#](#LIBPQ-PQSSLATTRIBUTENAMES): Retorna um array de nomes de atributos SSL que podem ser usados em `PQsslAttribute()`. O array é terminado por um ponteiro nulo.

```
const char * const * PQsslAttributeNames(const PGconn *conn);
```

Se `conn` for NULL, os atributos disponíveis para a biblioteca SSL padrão são retornados, ou uma lista vazia se a libpq foi compilada sem qualquer suporte SSL. Se `conn` não for NULL, os atributos disponíveis para a biblioteca SSL em uso para a conexão são retornados, ou uma lista vazia se a conexão não estiver criptografada.

`PQsslStruct` [#](#LIBPQ-PQSSLSTRUCT): Retorna um ponteiro para um objeto específico da implementação SSL que descreve a conexão. Retorna NULL se a conexão não estiver criptografada ou se o tipo de objeto solicitado não estiver disponível na implementação SSL da conexão.

```
void *PQsslStruct(const PGconn *conn, const char *struct_name);
```

As estruturas disponíveis dependem da implementação SSL utilizada. Para o OpenSSL, há uma estrutura disponível sob o nome `OpenSSL`, e ela retorna um ponteiro para a estrutura `SSL` do OpenSSL. Para usar essa função, o código a seguir pode ser usado:

```
#include <libpq-fe.h>
#include <openssl/ssl.h>

...

    SSL *ssl;

    dbconn = PQconnectdb(...); ...

    ssl = PQsslStruct(dbconn, "OpenSSL"); if (ssl) { /* use OpenSSL functions to access ssl */ }
```

Essa estrutura pode ser usada para verificar os níveis de criptografia, verificar certificados de servidor e muito mais. Consulte a documentação do OpenSSL para obter informações sobre essa estrutura.

`PQgetssl` [#](#LIBPQ-PQGETSSL): Retorna a estrutura SSL usada na conexão, ou NULL se SSL não estiver em uso.

```
void *PQgetssl(const PGconn *conn);
```

Essa função é equivalente a `PQsslStruct(conn, "OpenSSL")`. Não deve ser usada em novas aplicações, porque a estrutura retornada é específica para o OpenSSL e não estará disponível se outra implementação SSL for usada. Para verificar se uma conexão usa SSL, chame `PQsslInUse` em vez disso, e, para mais detalhes sobre a conexão, use `PQsslAttribute` em vez disso.