## 32.1. Funções de Controle de Conexão de Banco de Dados [#](#LIBPQ-CONNECT)

* [32.1.1. Conexões de conexão](libpq-connect.md#LIBPQ-CONNSTRING)
* [32.1.2. Palavras-chave de parâmetros](libpq-connect.md#LIBPQ-PARAMKEYWORDS)

As funções a seguir lidam com a conexão a um servidor de banco de dados PostgreSQL. Um programa de aplicação pode ter várias conexões de banco de dados abertas ao mesmo tempo. (Uma razão para fazer isso é acessar mais de um banco de dados.) Cada conexão é representada por um objeto `PGconn`, que é obtido a partir da função `PQconnectdb`(libpq-connect.md#LIBPQ-PQCONNECTDB), `PQconnectdbParams`(libpq-connect.md#LIBPQ-PQCONNECTDBPARAMS) ou `PQsetdbLogin`(libpq-connect.md#LIBPQ-PQSETDBLOGIN). Note que essas funções sempre retornarão um ponteiro de objeto não nulo, a menos que talvez haja pouco memória até mesmo para alocar o objeto [[`PGconn`]. A função `PQstatus`(libpq-status.md#LIBPQ-PQSTATUS) deve ser chamada para verificar o valor de retorno para uma conexão bem-sucedida antes de as consultas serem enviadas via o objeto de conexão.

### Aviso

Se usuários não confiáveis tiverem acesso a um banco de dados que não adotou um padrão de uso de esquema seguro (ddl-schemas.md#DDL-SCHEMAS-PATTERNS "5.10.6. Usage Patterns"), comece cada sessão removendo esquemas que podem ser escritos publicamente de `search_path`. Pode-se definir a palavra-chave do parâmetro `options` para o valor `-csearch_path=`. Alternativamente, pode-se emitir `PQexec(conn, "SELECT pg_catalog.set_config('search_path', '', false)")` após a conexão. Esta consideração não é específica do libpq; ela se aplica a todas as interfaces para executar comandos SQL arbitrários.

### Aviso

Em Unix, a divisão de um processo com conexões abertas do libpq pode levar a resultados imprevisíveis, pois o processo pai e o filho compartilham os mesmos sockets e recursos do sistema operacional. Por essa razão, esse uso não é recomendado, embora fazer um `exec` do processo filho para carregar um novo executável seja seguro.

`PQconnectdbParams` [#](#LIBPQ-PQCONNECTDBPARAMS): Faz uma nova conexão com o servidor de banco de dados.

```
PGconn *PQconnectdbParams(const char * const *keywords, const char * const *values, int expand_dbname);
```

Essa função abre uma nova conexão de banco de dados usando os parâmetros tomados de dois arrays terminados com `NULL`. O primeiro, `keywords`, é definido como um array de strings, cada uma sendo uma palavra-chave. O segundo, `values`, dá o valor para cada palavra-chave. Ao contrário de [`PQsetdbLogin`](libpq-connect.md#LIBPQ-PQSETDBLOGIN) abaixo, o conjunto de parâmetros pode ser estendido sem alterar a assinatura da função, portanto, o uso dessa função (ou seus análogos não bloqueados [`PQconnectStartParams`](libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS) e `PQconnectPoll`) é preferido para nova programação de aplicativos.

As palavras-chave de parâmetro atualmente reconhecidas estão listadas em [Seção 32.1.2](libpq-connect.md#LIBPQ-PARAMKEYWORDS).

Os arrays passados podem ser vazios para usar todos os parâmetros padrão, ou podem conter uma ou mais configurações de parâmetro. Eles devem ser correspondidos em comprimento. O processamento parará na primeira entrada `NULL` no array `keywords`. Além disso, se a entrada `values` associada a uma entrada `keywords` que não é `NULL` for `NULL` ou uma string vazia, essa entrada é ignorada e o processamento continua com o próximo par de entradas do array.

Quando `expand_dbname` não é nulo, o valor da primeira palavra-chave *`dbname`* é verificado para verificar se é uma *string de conexão*. Se for, ela é “expansão” em os parâmetros de conexão individuais extraídos da string. O valor é considerado uma string de conexão, em vez de apenas um nome de banco de dados, se contiver um sinal de igual (`=`) ou começar com um designator de esquema URI. (Mais detalhes sobre os formatos de strings de conexão aparecem em [Seção 32.1.1](libpq-connect.md#LIBPQ-CONNSTRING).). Apenas a primeira ocorrência de *`dbname`* é tratada dessa maneira; qualquer parâmetro subsequente *`dbname`* é processado como um nome de banco de dados simples.

Em geral, os arrays de parâmetros são processados de início a fim. Se qualquer palavra-chave for repetida, o último valor (isto é, que não seja `NULL` ou vazio) é usado. Esta regra se aplica, em particular, quando uma palavra-chave encontrada em uma string de conexão entra em conflito com uma que aparece no array `keywords`. Assim, o programador pode determinar se as entradas do array podem substituir ou ser substituídas por valores tomados de uma string de conexão. As entradas do array que aparecem antes de uma entrada expandida *`dbname`* podem ser substituídas por campos da string de conexão, e, por sua vez, esses campos são substituídos por entradas do array que aparecem após *`dbname`* (mas, novamente, apenas se essas entradas fornecem valores não vazios).

Após processar todas as entradas da matriz e quaisquer strings de conexão expandidas, quaisquer parâmetros de conexão que permaneçam não definidos são preenchidos com valores padrão. Se a variável de ambiente correspondente a um parâmetro não definido (ver [Seção 32.15] (libpq-envars.md "32.15. Environment Variables")) for definida, seu valor é usado. Se a variável de ambiente não for definida, então o valor padrão interno do parâmetro é usado.

`PQconnectdb` [#](#LIBPQ-PQCONNECTDB): Faz uma nova conexão com o servidor de banco de dados.

```
PGconn *PQconnectdb(const char *conninfo);
```

Essa função abre uma nova conexão de banco de dados usando os parâmetros tomados da string `conninfo`.

A string passada pode ser vazia para usar todos os parâmetros padrão, ou pode conter uma ou mais configurações de parâmetro separadas por espaço em branco, ou pode conter um URI. Consulte [Seção 32.1.1](libpq-connect.md#LIBPQ-CONNSTRING) para obter detalhes.

`PQsetdbLogin` [#](#LIBPQ-PQSETDBLOGIN) : Faz uma nova conexão com o servidor de banco de dados.

```
PGconn *PQsetdbLogin(const char *pghost, const char *pgport, const char *pgoptions, const char *pgtty, const char *dbName, const char *login, const char *pwd);
```

Este é o antecessor de `PQconnectdb` (libpq-connect.md#LIBPQ-PQCONNECTDB) com um conjunto fixo de parâmetros. Tem a mesma funcionalidade, exceto que os parâmetros ausentes sempre terão valores padrão. Escreva `NULL` ou uma string vazia para qualquer um dos parâmetros fixos que devem ser definidos como padrão.

Se o *`dbName`* contiver um sinal `=` ou tiver um prefixo de URI de conexão válido, ele é considerado uma string *`conninfo`* exatamente da mesma maneira que se tivesse sido passado para [`PQconnectdb`](libpq-connect.md#LIBPQ-PQCONNECTDB), e os parâmetros restantes são então aplicados conforme especificado para [`PQconnectdbParams`](libpq-connect.md#LIBPQ-PQCONNECTDBPARAMS).

`pgtty` não é mais utilizado e qualquer valor passado será ignorado.

`PQsetdb` [#](#LIBPQ-PQSETDB): Faz uma nova conexão com o servidor de banco de dados.

```
PGconn *PQsetdb(char *pghost, char *pgport, char *pgoptions, char *pgtty, char *dbName);
```

Este é um macro que chama `PQsetdbLogin` com ponteiros nulos para os parâmetros *`login`* e *`pwd`*. É fornecido para compatibilidade reversa com programas muito antigos.

`PQconnectStartParams` `PQconnectStart` `PQconnectPoll` [#](#LIBPQ-PQCONNECTSTARTPARAMS): Faça uma conexão ao servidor de banco de dados de forma não bloqueante.

```
PGconn *PQconnectStartParams(const char * const *keywords, const char * const *values, int expand_dbname);

PGconn *PQconnectStart(const char *conninfo);

PostgresPollingStatusType PQconnectPoll(PGconn *conn);
```

Essas três funções são usadas para abrir uma conexão com um servidor de banco de dados, de modo que o fio de execução da sua aplicação não fique bloqueado em I/O remoto enquanto isso. O ponto dessa abordagem é que as espera para o I/O ser completado pode ocorrer no loop principal da aplicação, em vez de dentro de `PQconnectdbParams`(libpq-connect.md#LIBPQ-PQCONNECTDBPARAMS) ou `PQconnectdb`(libpq-connect.md#LIBPQ-PQCONNECTDB), e assim a aplicação pode gerenciar essa operação em paralelo com outras atividades.

Com `PQconnectStartParams`, a conexão com o banco de dados é feita usando os parâmetros tomados dos arrays (libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS) e `values`, e controlada por `expand_dbname`, como descrito acima para `PQconnectdbParams`(libpq-connect.md#LIBPQ-PQCONNECTDBPARAMS).

Com `PQconnectStart`, a conexão com o banco de dados é feita usando os parâmetros tomados da string `conninfo` como descrito acima para `PQconnectdb`(libpq-connect.md#LIBPQ-PQCONNECTDB).

Nenhuma das `PQconnectStartParams` (libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS) ou `PQconnectStart` será bloqueada, desde que sejam atendidas algumas restrições:

* O parâmetro `hostaddr` deve ser usado adequadamente para evitar que consultas DNS sejam feitas. Consulte a documentação deste parâmetro em [Seção 32.1.2](libpq-connect.md#LIBPQ-PARAMKEYWORDS) para obter detalhes.
* Se você chamar `PQtrace`[(libpq-control.md#LIBPQ-PQTRACE)], certifique-se de que o objeto de fluxo no qual você está rastreando não bloqueie.
* Você deve garantir que o socket esteja no estado apropriado antes de chamar `PQconnectPoll`, conforme descrito abaixo.

Para iniciar uma solicitação de conexão não bloqueante, chame `PQconnectStart` ou `PQconnectStartParams`(libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS). Se o resultado for nulo, então a libpq não conseguiu alocar uma nova estrutura `PGconn`. Caso contrário, um ponteiro `PGconn` válido é retornado (embora ainda não representando uma conexão válida com o banco de dados). Em seguida, chame `PQstatus(conn)`. Se o resultado for `CONNECTION_BAD`, a tentativa de conexão já falhou, tipicamente devido a parâmetros de conexão inválidos.

Se `PQconnectStart` ou `PQconnectStartParams`(libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS) tiver sucesso, a próxima etapa é fazer uma consulta à libpq para que ela possa prosseguir com a sequência de conexão. Use `PQsocket(conn)` para obter o descritor do socket que suporta a conexão com o banco de dados. (Cuidado: não se pode assumir que o socket permaneça o mesmo em todas as chamadas de `PQconnectPoll`.) Assim, faça o seguinte: Se `PQconnectPoll(conn)` retornar `PGRES_POLLING_READING`, espere até que o socket esteja pronto para leitura (como indicado por `select()`, `poll()` ou uma função semelhante do sistema). Note que `PQsocketPoll` pode ajudar a reduzir a padronização ao abstrair a configuração de `select(2)` ou `poll(2)`, se estiver disponível no seu sistema. Em seguida, chame `PQconnectPoll(conn)` novamente. Por outro lado, se `PQconnectPoll(conn)` retornar `PGRES_POLLING_WRITING`, espere até que o socket esteja pronto para escrita, então chame `PQconnectPoll(conn)` novamente. Na primeira iteração, ou seja, se ainda não tiver chamado `PQconnectPoll`, se comporte como se `PGRES_POLLING_WRITING` tivesse retornado. Continue esse loop até que `PQconnectPoll(conn)` retorne `PGRES_POLLING_FAILED`, indicando que o procedimento de conexão falhou, ou `PGRES_POLLING_OK`, indicando que a conexão foi feita com sucesso.

Em qualquer momento durante a conexão, o status da conexão pode ser verificado chamando `PQstatus`(libpq-status.md#LIBPQ-PQSTATUS). Se essa chamada retornar `CONNECTION_BAD`, então o procedimento de conexão falhou; se a chamada retornar `CONNECTION_OK`, então a conexão está pronta. Ambos esses estados são igualmente detectáveis pelo valor de retorno de `PQconnectPoll`, descrito acima. Outros estados também podem ocorrer (e apenas durante) um procedimento de conexão assíncrono. Esses indicam o estágio atual do procedimento de conexão e podem ser úteis para fornecer feedback ao usuário, por exemplo. Esses status são:

`CONNECTION_STARTED` [#](#LIBPQ-CONNECTION-STARTED) :   Esperando que a conexão seja feita.

`CONNECTION_MADE` [#](#LIBPQ-CONNECTION-MADE) :   Conexão OK; aguardando para enviar.

`CONNECTION_AWAITING_RESPONSE` [#](#LIBPQ-CONNECTION-AWAITING-RESPONSE) :   Esperando uma resposta do servidor.

`CONNECTION_AUTH_OK` [#](#LIBPQ-CONNECTION-AUTH-OK) :   Recebeu autenticação; aguardando o término do início do backend.

`CONNECTION_SSL_STARTUP` [#](#LIBPQ-CONNECTION-SSL-STARTUP) :   Negociar criptografia SSL.

`CONNECTION_GSS_STARTUP` [#](#LIBPQ-CONNECTION-GSS-STARTUP) :   Negociação da criptografia GSS.

`CONNECTION_CHECK_WRITABLE` [#](#LIBPQ-CONNECTION-CHECK-WRITABLE) :   Verificando se a conexão é capaz de lidar com transações de escrita.

`CONNECTION_CHECK_STANDBY` [#](#LIBPQ-CONNECTION-CHECK-STANDBY) :   Verificando se a conexão está em um servidor em modo de espera.

`CONNECTION_CONSUME` [#](#LIBPQ-CONNECTION-CONSUME) :   Consumir quaisquer mensagens de resposta restantes na conexão.

Observe que, embora essas constantes permaneçam (para manter a compatibilidade), uma aplicação nunca deve depender dessas ocorrer em uma ordem específica, ou de forma alguma, ou de que o status esteja sempre em um desses valores documentados. Uma aplicação pode fazer algo assim:

```
switch(PQstatus(conn)) { case CONNECTION_STARTED: feedback = "Connecting..."; break;

        case CONNECTION_MADE: feedback = "Connected to server..."; break; . . . default: feedback = "Connecting..."; }
```

O parâmetro de conexão `connect_timeout` é ignorado quando se usa `PQconnectPoll`; é responsabilidade da aplicação decidir se há um período excessivo de tempo. Caso contrário, `PQconnectStart` seguido por um loop `PQconnectPoll` é equivalente a `PQconnectdb`(libpq-connect.md#LIBPQ-PQCONNECTDB).

Observe que, quando `PQconnectStart` ou `PQconnectStartParams`(libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS) retorna um ponteiro não nulo, você deve chamar `PQfinish`(libpq-connect.md#LIBPQ-PQFINISH) quando você estiver terminado com ele, a fim de descartar a estrutura e quaisquer blocos de memória associados. Isso deve ser feito mesmo que a tentativa de conexão falhe ou seja abandonada.

`PQsocketPoll` [#](#LIBPQ-PQSOCKETPOLL): Pergunte o descritor de soquete subjacente de uma conexão recuperado com [`PQsocket`](libpq-status.md#LIBPQ-PQSOCKET). O uso principal desta função é iterar pela sequência de conexão descrita na documentação de [`PQconnectStartParams`](libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS).

```
typedef int64_t pg_usec_time_t;

int PQsocketPoll(int sock, int forRead, int forWrite, pg_usec_time_t end_time);
```

Essa função realiza a verificação de um descritor de arquivo, opcionalmente com um timeout. Se *`forRead`* for diferente de zero, a função terminará quando o socket estiver pronto para leitura. Se *`forWrite`* for diferente de zero, a função terminará quando o socket estiver pronto para escrita.

O tempo de espera é especificado por *`end_time`, que* é o tempo para parar de esperar expresso como um número de microsegundos desde a época Unix (ou seja, `time_t` vezes 1 milhão). O tempo de espera é infinito se *`end_time`* *`-1`*. O tempo de espera é imediato (sem bloqueio) se *`end_time`* é *`0` (ou de fato, qualquer tempo antes de agora). Os valores de tempo de espera podem ser calculados convenientemente adicionando o número desejado de microsegundos ao resultado de [`PQgetCurrentTimeUSec`](libpq-misc.md#LIBPQ-PQGETCURRENTTIMEUSEC)]. Note que as chamadas de sistema subjacentes podem ter menos precisão do que um microsegundo, de modo que o atraso real pode ser impreciso.

A função retorna um valor maior que `0` se a condição especificada for atendida, `0` se ocorreu um tempo de espera, ou `-1` se ocorreu um erro. O erro pode ser recuperado verificando o valor de `errno(3)`. No caso em que tanto *`forRead`* quanto *`forWrite`* são zero, a função retorna imediatamente uma indicação de tempo de espera.

`PQsocketPoll` é implementado usando ou `poll(2)` ou `select(2)`, dependendo da plataforma. Consulte `POLLIN` e `POLLOUT` de `poll(2)`, ou *`readfds`* e *`writefds`* de `select(2)`, para mais informações.

`PQconndefaults` [#](#LIBPQ-PQCONNDEFAULTS) : Retorna as opções de conexão padrão.

```
PQconninfoOption *PQconndefaults(void);

typedef struct { char   *keyword;   /* The keyword of the option */ char   *envvar;    /* Fallback environment variable name */ char   *compiled;  /* Fallback compiled in default value */ char   *val;       /* Option's current value, or NULL */ char   *label;     /* Label for field in connect dialog */ char   *dispchar;  /* Indicates how to display this field in a connect dialog. Values are: ""        Display entered value as is "*"       Password field - hide value "D"       Debug option - don't show by default */ int     dispsize;  /* Field size in characters for dialog */ } PQconninfoOption;
```

Retorna um array de opções de conexão. Isso pode ser usado para determinar todas as opções possíveis de `PQconnectdb` e seus valores padrão atuais. O valor de retorno aponta para um array de estruturas de `PQconninfoOption`, que termina com uma entrada que tem um ponteiro `keyword` nulo. O ponteiro nulo é retornado se a memória não puder ser alocada. Note que os valores padrão atuais (campos `val`) dependerão de variáveis de ambiente e outros contextos. Um arquivo de serviço ausente ou inválido será ignorado silenciosamente. Os chamados devem tratar os dados das opções de conexão como somente leitura.

Após processar o array de opções, libere-o passando-o para [`PQconninfoFree`](libpq-misc.md#LIBPQ-PQCONNINFOFREE). Se isso não for feito, uma pequena quantidade de memória é vazada a cada chamada para [`PQconndefaults`](libpq-connect.md#LIBPQ-PQCONNDEFAULTS).

`PQconninfo` [#](#LIBPQ-PQCONNINFO) :   Retorna as opções de conexão usadas por uma conexão ao vivo.

```
PQconninfoOption *PQconninfo(PGconn *conn);
```

Retorna um array de opções de conexão. Isso pode ser usado para determinar todas as opções possíveis de `PQconnectdb`(libpq-connect.md#LIBPQ-PQCONNECTDB) e os valores que foram usados para se conectar ao servidor. O valor de retorno aponta para um array de estruturas de `PQconninfoOption`, que termina com uma entrada que tem um ponteiro `keyword` nulo. Todas as notas acima para `PQconndefaults`(libpq-connect.md#LIBPQ-PQCONNDEFAULTS) também se aplicam ao resultado de `PQconninfo`(libpq-connect.md#LIBPQ-PQCONNINFO).

`PQconninfoParse` [#](#LIBPQ-PQCONNINFOPARSE): Retorna as opções de conexão analisadas a partir da string de conexão fornecida.

```
PQconninfoOption *PQconninfoParse(const char *conninfo, char **errmsg);
```

Analisa uma cadeia de conexão e retorna as opções resultantes como um array; ou retorna `NULL` se houver um problema com a cadeia de conexão. Esta função pode ser usada para extrair as opções `PQconnectdb`(libpq-connect.md#LIBPQ-PQCONNECTDB) na cadeia de conexão fornecida. O valor de retorno aponta para um array de estruturas `PQconninfoOption`, que termina com uma entrada com um ponteiro `keyword` nulo.

Todas as opções legais estarão presentes na matriz de resultados, mas o `PQconninfoOption` para qualquer opção que não esteja presente na string de conexão terá `val` definido como `NULL`; os valores padrão não são inseridos.

Se `errmsg` não for `NULL`, então `*errmsg` é definido como `NULL` em caso de sucesso, caso contrário, para uma string de erro `malloc` com explicação do problema. (Também é possível que `*errmsg` seja definido como `NULL` e a função retorne `NULL`; isso indica uma condição de falta de memória.)

Após processar a matriz de opções, libere-a passando-a para `PQconninfoFree`](libpq-misc.md#LIBPQ-PQCONNINFOFREE). Se isso não for feito, alguma memória é vazada a cada chamada para `PQconninfoParse`](libpq-connect.md#LIBPQ-PQCONNINFOPARSE). Por outro lado, se ocorrer um erro e `errmsg` não for `NULL`, certifique-se de liberar a string de erro usando `PQfreemem`](libpq-misc.md#LIBPQ-PQFREEMEM).

`PQfinish` [#](#LIBPQ-PQFINISH): Fecha a conexão com o servidor. Também libera a memória usada pelo objeto `PGconn`.

```
void PQfinish(PGconn *conn);
```

Observe que, mesmo que a tentativa de conexão com o servidor falhe (como indicado por `PQstatus`][(libpq-status.md#LIBPQ-PQSTATUS)), o aplicativo deve chamar `PQfinish`][(libpq-connect.md#LIBPQ-PQFINISH) para liberar a memória usada pelo objeto `PGconn`. O ponteiro `PGconn` não deve ser usado novamente após `PQfinish`][(libpq-connect.md#LIBPQ-PQFINISH) ter sido chamado.

`PQreset` [#](#LIBPQ-PQRESET) : Redefine o canal de comunicação com o servidor.

```
void PQreset(PGconn *conn);
```

Essa função fechará a conexão com o servidor e tentará estabelecer uma nova conexão, usando todos os mesmos parâmetros utilizados anteriormente. Isso pode ser útil para recuperação de erros, caso uma conexão funcional seja perdida.

`PQresetStart` `PQresetPoll` [#](#LIBPQ-PQRESETSTART): Reinicie o canal de comunicação com o servidor, de forma não bloqueante.

```
int PQresetStart(PGconn *conn);

PostgresPollingStatusType PQresetPoll(PGconn *conn);
```

Essas funções fecharão a conexão com o servidor e tentarão estabelecer uma nova conexão, usando todos os mesmos parâmetros utilizados anteriormente. Isso pode ser útil para recuperação de erros se uma conexão funcional for perdida. Elas diferem de `PQreset`(libpq-connect.md#LIBPQ-PQRESET) (acima) na medida em que atuam de forma não bloqueante. Essas funções sofrem das mesmas restrições que `PQconnectStartParams`(libpq-connect.md#LIBPQ-PQCONNECTSTARTPARAMS), `PQconnectStart` e `PQconnectPoll`.

Para iniciar um restabelecimento de conexão, ligue para `PQresetStart`(libpq-connect.md#LIBPQ-PQRESETSTART). Se ele retornar 0, o restabelecimento falhou. Se ele retornar 1, faça uma pesquisa do restabelecimento usando `PQresetPoll` exatamente da mesma maneira que você criaria a conexão usando `PQconnectPoll`.

`PQpingParams` [#](#LIBPQ-PQPINGPARAMS) relata o status do servidor. Aceita parâmetros de conexão idênticos aos da `PQpingParams`(libpq-connect.md#LIBPQ-PQPINGPARAMS), descritos acima. Não é necessário fornecer valores corretos para nome de usuário, senha ou nome do banco de dados para obter o status do servidor; no entanto, se valores incorretos forem fornecidos, o servidor registrará uma tentativa de conexão falhada.

```
PGPing PQpingParams(const char * const *keywords, const char * const *values, int expand_dbname);
```

A função retorna um dos seguintes valores:

`PQPING_OK` [#](#LIBPQ-PQPINGPARAMS-PQPING_OK) :   O servidor está em execução e parece estar aceitando conexões.

`PQPING_REJECT` [#](#LIBPQ-PQPINGPARAMS-PQPING_REJECT) :   O servidor está em execução, mas em um estado que não permite conexões (recuperação de inicialização, desligamento ou falha).

`PQPING_NO_RESPONSE` [#](#LIBPQ-PQPINGPARAMS-PQPING_NO_RESPONSE) :   O servidor não pôde ser contatado. Isso pode indicar que o servidor não está em execução, ou que há algo errado com os parâmetros de conexão fornecidos (por exemplo, número de porta incorreto), ou que há um problema de conectividade de rede (por exemplo, um firewall bloqueando a solicitação de conexão).

`PQPING_NO_ATTEMPT` [#](#LIBPQ-PQPINGPARAMS-PQPING_NO_ATTEMPT) :   Não foi feita nenhuma tentativa de contato com o servidor, porque os parâmetros fornecidos eram obviamente incorretos ou havia algum problema do lado do cliente (por exemplo, falta de memória).

`PQping` [#](#LIBPQ-PQPING) informa o status do servidor. Aceita parâmetros de conexão idênticos aos da `PQconnectdb` (libpq-connect.md#LIBPQ-PQCONNECTDB), descritos acima. Não é necessário fornecer valores corretos para nome de usuário, senha ou nome do banco de dados para obter o status do servidor; no entanto, se valores incorretos forem fornecidos, o servidor registrará uma tentativa de conexão falhada.

```
PGPing PQping(const char *conninfo);
```

Os valores de retorno são os mesmos que para `PQpingParams`(libpq-connect.md#LIBPQ-PQPINGPARAMS).

`PQsetSSLKeyPassHook_OpenSSL` [#](#LIBPQ-PQSETSSLKEYPASSHOOK-OPENSSL): `PQsetSSLKeyPassHook_OpenSSL` permite que uma aplicação substitua a manipulação [de arquivos de chave de certificado de cliente criptografado](libpq-ssl.md#LIBPQ-SSL-CLIENTCERT "32.19.2. Certificados de cliente") do [libpq](libpq-ssl.md) usando [sslpassword](libpq-connect.md#LIBPQ-CONNECT-SSLPASSWORD) ou solicitação interativa.

```
void PQsetSSLKeyPassHook_OpenSSL(PQsslKeyPassHook_OpenSSL_type hook);
```

O aplicativo passa um ponteiro para uma função de chamada com a assinatura:

```
int callback_fn(char *buf, int size, PGconn *conn);
```

que libpq chamará em seguida *em vez* do seu manipulador padrão `PQdefaultSSLKeyPassHook_OpenSSL` O callback deve determinar a senha para a chave e copiá-la para `buf`* de tamanho *`size`*. A string em *`buf`* deve ser terminada com um null. O callback deve retornar o comprimento da senha armazenada em *`buf`* excluindo o null terminator. Em caso de falha, o callback deve definir `buf[0] = '\0'` e retornar 0. Veja `PQdefaultSSLKeyPassHook_OpenSSL` no código-fonte do libpq para um exemplo.

Se o usuário especificar uma localização de chave explícita, seu caminho será em `conn->sslkey` quando o callback for invocado. Este será vazio se o caminho padrão da chave estiver sendo usado. Para chaves que são especificadores de motor, cabe às implementações do motor se elas usam o callback de senha OpenSSL ou definem seu próprio tratamento.

O aplicativo pode optar por delegar casos não tratados para o `PQdefaultSSLKeyPassHook_OpenSSL`, ou chamá-lo primeiro e tentar outra coisa se ele retornar 0, ou substituí-lo completamente.

O callback *não deve* escapar do controle normal de fluxo, com exceções, `longjmp(...)`, etc. Ele deve retornar normalmente.

`PQgetSSLKeyPassHook_OpenSSL` [#](#LIBPQ-PQGETSSLKEYPASSHOOK-OPENSSL) :   `PQgetSSLKeyPassHook_OpenSSL` retorna a senha atual do gancho da chave de certificado do cliente, ou `NULL` se nenhuma tiver sido definida.

```
PQsslKeyPassHook_OpenSSL_type PQgetSSLKeyPassHook_OpenSSL(void);
```

### 32.1.1. Chaves de conexão [#](#LIBPQ-CONNSTRING)

Várias funções do libpq analisam uma string especificada pelo usuário para obter parâmetros de conexão. Existem dois formatos aceitos para essas strings: strings de palavras-chave/valores simples e URIs. Os URIs geralmente seguem [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986), exceto que as strings de conexão multi-host são permitidas conforme descrito abaixo.

#### 32.1.1.1. Conexões de palavras-chave/valores [#](#LIBPQ-CONNSTRING-KEYWORD-VALUE)

No formato palavra-chave/valor, cada configuração do parâmetro está na forma *`keyword`* `=` *`value`*, com espaço(s) entre as configurações. Espaços ao redor do sinal de igual de uma configuração são opcional. Para escrever um valor vazio ou um valor contendo espaços, envolva-o com aspas simples, por exemplo `keyword = 'a value'`. As aspas simples e barras invertidas dentro de um valor devem ser escapadas com uma barra invertida, ou seja, `\'` e `\\`.

Exemplo:

```
host=localhost port=5432 dbname=mydb connect_timeout=10
```

As palavras-chave de parâmetro reconhecidas estão listadas em [Seção 32.1.2](libpq-connect.md#LIBPQ-PARAMKEYWORDS).

#### 32.1.1.2. URIs de conexão [#](#LIBPQ-CONNSTRING-URIS)

A forma geral para uma URI de conexão é:

```
postgresql://[userspec@][hostspec][/dbname][?paramspec]

where userspec is:

user[:password]

and hostspec is:

[host][:port][,...]

and paramspec is:

name=value[&...]
```

O designador do esquema URI pode ser `postgresql://` ou `postgres://`. Cada uma das partes restantes do URI é opcional. Os seguintes exemplos ilustram a sintaxe válida do URI:

```
postgresql:// postgresql://localhost postgresql://localhost:5433 postgresql://localhost/mydb postgresql://user@localhost postgresql://user:secret@localhost postgresql://other@localhost/otherdb?connect_timeout=10&application_name=myapp postgresql://host1:123,host2:456/somedb?target_session_attrs=any&application_name=myapp
```

Os valores que normalmente aparecem na parte hierárquica do URI podem ser fornecidos como parâmetros nomeados como alternativa. Por exemplo:

```
postgresql:///mydb?host=localhost&port=5433
```

Todos os parâmetros nominais devem corresponder às palavras-chave listadas em [Seção 32.1.2] (libpq-connect.md#LIBPQ-PARAMKEYWORDS "32.1.2. Parameter Key Words"), exceto que, para compatibilidade com URIs de conexão JDBC, as instâncias de `ssl=true` são traduzidas em `sslmode=require`.

O URI de conexão precisa ser codificado com [percent-encoding](https://datatracker.ietf.org/doc/html/rfc3986#section-2.1) se ele incluir símbolos com significado especial em qualquer uma de suas partes. Aqui está um exemplo onde o sinal de igual (`=`) é substituído por `%3D` e o caractere de espaço com `%20`:

```
postgresql://user@localhost:5433/mydb?options=-c%20synchronous_commit%3Doff
```

A parte de host pode ser um nome de host ou um endereço IP. Para especificar um endereço IPv6, coloque-o entre colchetes:

```
postgresql://[2001:db8::1234]/database
```

A parte do host é interpretada conforme descrito para o parâmetro [host](libpq-connect.md#LIBPQ-CONNECT-HOST). Em particular, uma conexão de socket de domínio Unix é escolhida se a parte do host estiver vazia ou parecer um nome de caminho absoluto, caso contrário, uma conexão TCP/IP é iniciada. Note, no entanto, que o barra é um caractere reservado na parte hierárquica do URI. Portanto, para especificar um diretório de socket de domínio Unix não padrão, ou omita a parte do host do URI e especifique o host como um parâmetro nomeado, ou percent-encode o caminho na parte do host do URI:

```
postgresql:///dbname?host=/var/lib/postgresql postgresql://%2Fvar%2Flib%2Fpostgresql/dbname
```

É possível especificar vários componentes de host, cada um com um componente de porta opcional, em um único URI. Um URI do tipo `postgresql://host1:port1,host2:port2,host3:port3/` é equivalente a uma cadeia de conexão do tipo `host=host1,host2,host3 port=port1,port2,port3`. Como descrito mais adiante, cada host será tentado em ordem até que uma conexão seja estabelecida com sucesso.

#### 32.1.1.3. Especificação de múltiplos hosts [#](#LIBPQ-MULTIPLE-HOSTS)

É possível especificar vários hosts para se conectar, de modo que eles sejam provados na ordem dada. No formato Palavra-chave/Valor, as opções `host`, `hostaddr` e `port` aceitam listas de valores separadas por vírgula. O mesmo número de elementos deve ser dado em cada opção que é especificada, como, por exemplo, o primeiro `hostaddr` corresponde ao primeiro nome de host, o segundo `hostaddr` corresponde ao segundo nome de host, e assim por diante. Como exceção, se apenas uma `port` for especificada, ela se aplica a todos os hosts.

No formato URI de conexão, você pode listar vários pares `host:port` separados por vírgulas no componente `host` do URI.

Em qualquer formato, um único nome de host pode traduzir-se em múltiplos endereços de rede. Um exemplo comum disso é um host que tem tanto uma endereço IPv4 quanto um IPv6.

Quando vários hosts são especificados, ou quando um único nome de host é traduzido em vários endereços, todos os hosts e endereços serão testados em ordem, até que um deles tenha sucesso. Se nenhum dos hosts puder ser alcançado, a conexão falha. Se uma conexão for estabelecida com sucesso, mas a autenticação falha, os hosts restantes na lista não são testados.

Se um arquivo de senha for usado, você pode ter diferentes senhas para diferentes hosts. Todas as outras opções de conexão são as mesmas para cada host na lista; não é possível, por exemplo, especificar diferentes nomes de usuário para diferentes hosts.

### 32.1.2. Palavras-chave de parâmetros [#](#LIBPQ-PARAMKEYWORDS)

As palavras-chave de parâmetro atualmente reconhecidas são:

`host` [#](#LIBPQ-CONNECT-HOST): Nome do host para se conectar. Se o nome do host parecer um nome de caminho absoluto, especifica comunicação de domínio Unix em vez de comunicação TCP/IP; o valor é o nome do diretório em que o arquivo do socket é armazenado. (Em Unix, um nome de caminho absoluto começa com uma barra. Em Windows, caminhos que começam com letras de unidade também são reconhecidos.) Se o nome do host começar com `@`, ele é considerado um socket de domínio Unix no espaço abstrato (atualmente suportado em Linux e Windows). O comportamento padrão quando `host` não é especificado ou está vazio é conectar-se a um socket de domínio Unix em  `/tmp` (ou qualquer diretório de socket especificado quando o PostgreSQL foi construído). Em Windows,  o padrão é conectar-se a `localhost`.

Uma lista de nomes de host separados por vírgula também é aceita, nesse caso, cada nome de host na lista é testado em ordem; um item vazio na lista seleciona o comportamento padrão conforme explicado acima. Consulte [Seção 32.1.1.3](libpq-connect.md#LIBPQ-MULTIPLE-HOSTS) para detalhes.

`hostaddr` [#](#LIBPQ-CONNECT-HOSTADDR): Endereço IP numérico do host a ser conectado. Isso deve estar no formato padrão de endereço IPv4, por exemplo, `172.28.40.9`. Se sua máquina suporta IPv6, você também pode usar esses endereços. A comunicação TCP/IP é sempre usada quando uma string não vazia é especificada para este parâmetro. Se este parâmetro não for especificado, o valor de `host` será procurado para encontrar o endereço IP correspondente — ou, se `host` especificar um endereço IP, esse valor será usado diretamente.

Usar `hostaddr` permite que o aplicativo evite uma pesquisa de nome de host, o que pode ser importante em aplicativos com restrições de tempo. No entanto, um nome de host é necessário para os métodos de autenticação GSSAPI ou SSPI, bem como para a verificação de certificado SSL `verify-full`. As seguintes regras são usadas:

* Se `host` for especificado sem `hostaddr`, ocorre uma busca de nome de host.

(Ao usar `PQconnectPoll`, a busca ocorre quando `PQconnectPoll` considera pela primeira vez esse nome de host, e pode fazer com que `PQconnectPoll` bloqueie por um período significativo de tempo.)
* Se `hostaddr` for especificado sem `host`, o valor para `hostaddr` fornece o endereço da rede do servidor. A tentativa de conexão falhará se o método de autenticação exigir um nome de host.
* Se ambos `host` e `hostaddr` forem especificados, o valor para `hostaddr` fornece o endereço da rede do servidor. O valor para `host` é ignorado, a menos que o método de autenticação o exija, no qual caso será usado como nome de host.

Observe que a autenticação provavelmente falhará se `host` não for o nome do servidor no endereço de rede `hostaddr`. Além disso, quando tanto `host` quanto `hostaddr` são especificados, `host` é usado para identificar a conexão em um arquivo de senha (consulte [Seção 32.16](libpq-pgpass.md)).

Uma lista de valores `hostaddr` separados por vírgula também é aceita, nesse caso, cada host na lista é testado em ordem. Um item vazio na lista faz com que o nome do host correspondente seja usado, ou o nome padrão do host se este também estiver vazio. Consulte [Seção 32.1.1.3](libpq-connect.md#LIBPQ-MULTIPLE-HOSTS) para detalhes.

Sem nome de host ou endereço de host, o libpq se conectará usando um socket de domínio Unix local; ou, no Windows, tentará se conectar ao `localhost`.

`port` [#](#LIBPQ-CONNECT-PORT) :   Número de porta para se conectar no host do servidor, ou nome de arquivo de soquete. Extensão de nome de domínio de Unix. Se vários hosts foram fornecidos nos parâmetros `host` ou `hostaddr`, este parâmetro pode especificar uma lista de portas separadas por vírgula com o mesmo comprimento da lista de hosts, ou pode especificar um único número de porta a ser usado para todos os hosts. Uma string vazia ou um item vazio em uma lista separada por vírgula, especifica o número de porta padrão estabelecido quando o PostgreSQL foi construído.

`dbname` [#](#LIBPQ-CONNECT-DBNAME): O nome do banco de dados. Por padrão, é o mesmo que o nome do usuário. Em certos contextos, o valor é verificado para formatos extensos; consulte [Seção 32.1.1](libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings") para mais detalhes sobre esses.

`user` [#](#LIBPQ-CONNECT-USER): Nome do usuário do PostgreSQL para se conectar como. Por padrão, deve ser o mesmo nome do sistema operacional do usuário que está executando o aplicativo.

`password` [#](#LIBPQ-CONNECT-PASSWORD): Senha a ser usada se o servidor exigir autenticação por senha.

`passfile` [#](#LIBPQ-CONNECT-PASSFILE): Especifica o nome do arquivo usado para armazenar senhas (consulte [Seção 32.16](libpq-pgpass.md "32.16. The Password File")). Por padrão, é `~/.pgpass`, ou `%APPDATA%\postgresql\pgpass.conf` no Microsoft Windows.

(Não é relatado nenhum erro se esse arquivo não existir.)

`require_auth` [#](#LIBPQ-CONNECT-REQUIRE-AUTH): Especifica o método de autenticação que o cliente exige do servidor. Se o servidor não usar o método exigido para autenticar o cliente, ou se o aperto de mão de autenticação não for totalmente completado pelo servidor, a conexão falhará. Uma lista de métodos separados por vírgula também pode ser fornecida, dos quais o servidor deve usar exatamente um para que a conexão seja bem-sucedida. Por padrão, qualquer método de autenticação é aceito, e o servidor é livre para ignorar a autenticação completamente.

Os métodos podem ser negados com a adição de um prefixo `!`, caso em que o servidor *não* deve tentar o método listado; qualquer outro método é aceito, e o servidor é livre para não autenticar o cliente. Se uma lista separada por vírgula for fornecida, o servidor pode não tentar *qualquer* dos métodos negados listados. Formas negadas e não negadas não podem ser combinadas no mesmo ambiente.

Como um caso especial final, o método `none` exige que o servidor não use um desafio de autenticação. (Também pode ser negado, para exigir alguma forma de autenticação.)

Os seguintes métodos podem ser especificados:

`password`: O servidor deve solicitar autenticação de senha em texto plano.

`md5`: O servidor deve solicitar autenticação com senha criptografada MD5.

### Aviso

O suporte para senhas criptografadas com MD5 é desatualizado e será removido em uma versão futura do PostgreSQL. Consulte [Seção 20.5](auth-password.md) para obter detalhes sobre a migração para outro tipo de senha.

`gss`: O servidor deve solicitar um aperto de mão Kerberos via GSSAPI ou estabelecer um canal criptografado GSS (consulte também [gssencmode](libpq-connect.md#LIBPQ-CONNECT-GSSENCMODE)).

`sspi` :   O servidor deve solicitar autenticação SSPI do Windows.

`scram-sha-256` :   O servidor deve completar com sucesso uma troca de autenticação SCRAM-SHA-256 com o cliente.

`oauth`: O servidor deve solicitar um token de portador OAuth do cliente.

`none` :   O servidor não deve solicitar ao cliente uma troca de autenticação. (Isso não proíbe a autenticação com certificado do cliente via TLS, nem a autenticação GSS via seu transporte criptografado.)

`channel_binding` [#](#LIBPQ-CONNECT-CHANNEL-BINDING): Esta opção controla o uso do cliente em relação à vinculação de canal. Uma configuração de `require` significa que a conexão deve utilizar vinculação de canal, `prefer` significa que o cliente escolherá a vinculação de canal se estiver disponível, e `disable` previne o uso de vinculação de canal. O padrão é `prefer` se o PostgreSQL for compilado com suporte SSL; caso contrário, o padrão é `disable`.

A vinculação de canal é um método para o servidor se autenticar ao cliente. É suportada apenas em conexões SSL com servidores PostgreSQL 11 ou posteriores, usando o método de autenticação `SCRAM`.

`connect_timeout` [#](#LIBPQ-CONNECT-CONNECT-TIMEOUT): Tempo máximo para aguardar durante a conexão, em segundos (escreva como um número inteiro decimal, ex., `10`). Zero, negativo ou não especificado significa aguardar indefinidamente. Este tempo limite aplica-se separadamente a cada nome de host ou endereço IP. Por exemplo, se você especificar dois hosts e `connect_timeout` for 5, cada host expirará o tempo se nenhuma conexão for feita dentro de 5 segundos, então o tempo total gasto esperando uma conexão pode ser até 10 segundos.

`client_encoding` [#](#LIBPQ-CONNECT-CLIENT-ENCODING): Este define o parâmetro de configuração `client_encoding` para esta conexão. Além dos valores aceitos pela opção do servidor correspondente, você pode usar `auto` para determinar o código de codificação correto a partir do local atual no cliente (`LC_CTYPE` variável de ambiente em sistemas Unix).

`options` [#](#LIBPQ-CONNECT-OPTIONS): Especifica as opções de linha de comando a serem enviadas ao servidor na inicialização da conexão. Por exemplo, definir isso para `-c geqo=off` ou `--geqo=off` define o valor da sessão do parâmetro `geqo` para `off`. Espaços dentro desta string são considerados para separar argumentos de linha de comando, a menos que sejam escapados com uma barra invertida (`\`); escreva `\\` para representar uma barra invertida literal. Para uma discussão detalhada das opções disponíveis, consulte [Capítulo 19](runtime-config.md "Chapter 19. Server Configuration").

`application_name` [#](#LIBPQ-CONNECT-APPLICATION-NAME): Especifica um valor para o parâmetro de configuração [application_name](runtime-config-logging.md#GUC-APPLICATION-NAME).

`fallback_application_name` [#](#LIBPQ-CONNECT-FALLBACK-APPLICATION-NAME): Especifica um valor de fallback para o parâmetro de configuração [application_name](runtime-config-logging.md#GUC-APPLICATION-NAME). Este valor será usado se nenhum valor tiver sido dado para `application_name` por meio de um parâmetro de conexão ou a variável de ambiente `PGAPPNAME`. Especificar um nome de fallback é útil em programas de utilidade genéricos que desejam definir um nome de aplicativo padrão, mas permitem que ele seja sobreescrito pelo usuário.

`keepalives` [#](#LIBPQ-KEEPALIVES): Controla se os keepalives TCP do lado do cliente são usados. O valor padrão é 1, o que significa que está ativado, mas você pode alterar para 0, o que significa desativado, se não quiser manter os keepalives. Este parâmetro é ignorado para conexões feitas por meio de um socket de domínio Unix.

`keepalives_idle` [#](#LIBPQ-KEEPALIVES-IDLE): Controla o número de segundos de inatividade após o qual o TCP deve enviar uma mensagem de manutenção ao servidor. Um valor de zero usa o padrão do sistema. Este parâmetro é ignorado para conexões feitas por meio de um socket de domínio Unix, ou se as manutenções forem desativadas. É suportado apenas em sistemas onde `TCP_KEEPIDLE` ou uma opção de socket equivalente está disponível, e em Windows; em outros sistemas, não tem efeito.

`keepalives_interval` [#](#LIBPQ-KEEPALIVES-INTERVAL): Controla o número de segundos após o qual uma mensagem de manutenção TCP que não é reconhecida pelo servidor deve ser retransmitida. Um valor de zero usa o padrão do sistema. Este parâmetro é ignorado para conexões feitas por meio de um socket de domínio Unix, ou se as manutenções forem desativadas. É suportado apenas em sistemas onde `TCP_KEEPINTVL` ou uma opção de socket equivalente está disponível, e em Windows; em outros sistemas, não tem efeito.

`keepalives_count` [#](#LIBPQ-KEEPALIVES-COUNT): Controla o número de keepalives TCP que podem ser perdidos antes que a conexão do cliente com o servidor seja considerada morta. Um valor de zero usa o padrão do sistema. Este parâmetro é ignorado para conexões feitas via socket de domínio Unix, ou se os keepalives forem desativados. É suportado apenas em sistemas onde `TCP_KEEPCNT` ou uma opção de socket equivalente está disponível; em outros sistemas, não tem efeito.

`tcp_user_timeout` [#](#LIBPQ-TCP-USER-TIMEOUT): Controla o número de milissegundos que os dados transmitidos podem permanecer não confirmados antes de uma conexão ser fechada à força. Um valor de zero usa o padrão do sistema. Este parâmetro é ignorado para conexões feitas por meio de um socket de domínio Unix. Ele só é suportado em sistemas onde `TCP_USER_TIMEOUT` está disponível; em outros sistemas, ele não tem efeito.

`replication` [#](#LIBPQ-CONNECT-REPLICATION): Esta opção determina se a conexão deve usar o protocolo de replicação em vez do protocolo normal. É o que as conexões de replicação do PostgreSQL, bem como ferramentas como o pg_basebackup, usam internamente, mas também pode ser usado por aplicativos de terceiros. Para uma descrição do protocolo de replicação, consulte [Seção 54.4](protocol-replication.md "54.4. Streaming Replication Protocol").

Os seguintes valores, que são sensíveis a maiúsculas e minúsculas, são suportados:

`true`, `on`, `yes`, `1` :   A conexão entra no modo de replicação física.

`database`: A conexão entra no modo de replicação lógica, conectando-se ao banco de dados especificado no parâmetro `dbname`.

`false`, `off`, `no`, `0` :   A conexão é uma conexão padrão, que é o comportamento padrão.

No modo de replicação física ou lógica, apenas o protocolo de consulta simples pode ser usado.

`gssencmode` [#](#LIBPQ-CONNECT-GSSENCMODE): Esta opção determina se uma conexão segura GSS TCP/IP será negociada com o servidor ou com qual prioridade. Existem três modos:

`disable`: tenha apenas uma tentativa de conexão não criptografada com GSSAPI

`prefer` (padrão) :   se houver credenciais GSSAPI presentes (ou seja, em um cache de credenciais), primeiro tente uma conexão criptografada GSSAPI; se isso falhar ou não houver credenciais, tente uma conexão não criptografada GSSAPI. Isso é o padrão quando o PostgreSQL foi compilado com suporte GSSAPI.

Apenas tente uma conexão criptografada com GSSAPI

`gssencmode` é ignorado para comunicação por soquete de domínio Unix. Se o PostgreSQL for compilado sem suporte ao GSSAPI, o uso da opção `require` causará um erro, enquanto `prefer` será aceito, mas a libpq não tentará, na verdade, uma conexão criptografada com GSSAPI.

`sslmode` [#](#LIBPQ-CONNECT-SSLMODE): Esta opção determina se uma conexão segura SSL TCP/IP será negociada com o servidor ou com qual prioridade. Existem seis modos:

`disable`: apenas tente uma conexão não SSL

`allow` :   primeiro, tente uma conexão sem SSL; se isso falhar, tente uma conexão SSL

`prefer` (padrão) :   primeiro, tente uma conexão SSL; se isso falhar, tente uma conexão sem SSL

`require`   :   tenha apenas uma conexão SSL. Se um arquivo de CA raiz estiver presente, verifique o certificado da mesma maneira que se `verify-ca` foi especificado

`verify-ca`: tenha apenas uma conexão SSL e verifique se o certificado do servidor é emitido por uma autoridade de certificação confiável (CA)

`verify-full`: apenas tente uma conexão SSL, verifique se o certificado do servidor é emitido por uma CA de confiança e se o nome de host do servidor solicitado corresponde ao do certificado

Veja [Seção 32.19](libpq-ssl.md) para uma descrição detalhada de como essas opções funcionam.

`sslmode` é ignorado para comunicação por soquete de domínio Unix. Se o PostgreSQL for compilado sem suporte SSL, o uso das opções `require`, `verify-ca` ou `verify-full` causará um erro, enquanto as opções `allow` e `prefer` serão aceitas, mas a libpq não tentará, na verdade, uma conexão SSL.

Observe que, se a criptografia GSSAPI for possível, essa será usada em preferência à criptografia SSL, independentemente do valor de `sslmode`. Para forçar o uso da criptografia SSL em um ambiente que tenha infraestrutura GSSAPI funcionante (como um servidor Kerberos), também defina `gssencmode` para `disable`.

`requiressl` [#](#LIBPQ-CONNECT-REQUIRESSL): Esta opção é descontinuada em favor do ajuste `sslmode`.

Se definido como 1, uma conexão SSL com o servidor é necessária (isso é equivalente a `sslmode` `require`). O libpq então se recusará a se conectar se o servidor não aceitar uma conexão SSL. Se definido como 0 (padrão), o libpq negociará o tipo de conexão com o servidor (equivalente a `sslmode` `prefer`). Esta opção só está disponível se o PostgreSQL for compilado com suporte SSL.

`sslnegotiation` [#](#LIBPQ-CONNECT-SSLNEGOTIATION): Esta opção controla como a criptografia SSL é negociada com o servidor, se o SSL é usado. No modo padrão `postgres`, o cliente primeiro pergunta ao servidor se o SSL é suportado. No modo `direct`, o cliente inicia a mão de aperto SSL padrão diretamente após estabelecer a conexão TCP/IP. A negociação do protocolo PostgreSQL tradicional é a mais flexível com diferentes configurações do servidor. Se o servidor é conhecido por suportar conexões SSL diretas, então esta última requer uma viagem de ida e volta reduzindo a latência da conexão e também permite o uso de ferramentas de rede SSL agnósticas ao protocolo. A opção SSL direta foi introduzida na versão 17 do PostgreSQL.

`postgres` :   realizar a negociação do protocolo PostgreSQL. Isso é o padrão se a opção não for fornecida.

`direct`   :   começar a troca SSL diretamente após estabelecer a conexão TCP/IP. Isso só é permitido com `sslmode=require` ou superior, porque as configurações mais fracas podem levar a uma autenticação em texto plano não intencional quando o servidor não suporta a troca SSL direta.

`sslcompression` [#](#LIBPQ-CONNECT-SSLCOMPRESSION): Se definido como 1, os dados enviados em conexões SSL serão comprimidos. Se definido como 0, a compressão será desativada. O padrão é 0. Este parâmetro é ignorado se uma conexão sem SSL for feita.

A compressão SSL é considerada insegura atualmente e seu uso não é mais recomendado. OpenSSL 1.1.0 desativou a compressão por padrão, e muitas distribuições de sistemas operacionais também a desativaram em versões anteriores, portanto, definir este parâmetro para on não terá nenhum efeito se o servidor não aceitar compressão. PostgreSQL 14 desativou a compressão completamente no backend.

Se a segurança não for uma preocupação primária, a compressão pode melhorar o desempenho se a rede for o gargalo. Desativar a compressão pode melhorar o tempo de resposta e o desempenho se o desempenho da CPU for o fator limitante.

`sslcert` [#](#LIBPQ-CONNECT-SSLCERT): Este parâmetro especifica o nome do arquivo do certificado SSL do cliente, substituindo o padrão `~/.postgresql/postgresql.crt`. Este parâmetro é ignorado se uma conexão SSL não for feita.

`sslkey` [#](#LIBPQ-CONNECT-SSLKEY): Este parâmetro especifica o local para a chave secreta usada para o certificado do cliente. Ele pode especificar um nome de arquivo que será usado em vez do padrão `~/.postgresql/postgresql.key`, ou pode especificar uma chave obtida de um "motor" externo (os motores são módulos carregáveis OpenSSL). Uma especificação de motor externo deve consistir em um nome de motor separado por colon e um identificador de chave específico do motor. Este parâmetro é ignorado se uma conexão SSL não for feita.

`sslkeylogfile` [#](#LIBPQ-CONNECT-SSLKEYLOGFILE): Este parâmetro especifica o local onde a libpq registrará as chaves usadas neste contexto SSL. Isso é útil para depuração das interações do protocolo PostgreSQL ou conexões de cliente usando ferramentas de inspeção de rede como o Wireshark. Este parâmetro é ignorado se uma conexão SSL não for feita, ou se o LibreSSL for usado (o LibreSSL não suporta registro de chaves). As chaves são registradas usando o formato NSS.

### Aviso

O registro de teclas expõe informações potencialmente sensíveis no arquivo keylog. Arquivos keylog devem ser tratados com o mesmo cuidado que os arquivos [sslkey](libpq-connect.md#LIBPQ-CONNECT-SSLKEY) .

`sslpassword` [#](#LIBPQ-CONNECT-SSLPASSWORD): Este parâmetro especifica a senha para a chave secreta especificada em `sslkey`, permitindo que as chaves privadas de certificado do cliente sejam armazenadas em forma encriptada no disco, mesmo quando a entrada de frase de interação não é prática.

Especificar este parâmetro com qualquer valor não vazio suprime o prompt `Enter PEM pass phrase:` que o OpenSSL emitirá por padrão quando uma chave de certificado cliente criptografada for fornecida ao libpq.

Se a chave não estiver criptografada, este parâmetro é ignorado. O parâmetro não tem efeito sobre as chaves especificadas pelos motores OpenSSL, a menos que o motor use o mecanismo de chamada de senha OpenSSL para solicitações.

Não há uma variável de ambiente equivalente a esta opção, e não há facilidade para consultá-la em `.pgpass`. Pode ser usada em uma definição de conexão de arquivo de serviço. Os usuários com usos mais sofisticados devem considerar o uso de motores e ferramentas OpenSSL, como PKCS#11 ou dispositivos de criptografia USB.

`sslcertmode` [#](#LIBPQ-CONNECT-SSLCERTMODE): Esta opção determina se um certificado do cliente pode ser enviado ao servidor e se o servidor é obrigado a solicitar um. Existem três modos:

`disable` :   Um certificado do cliente nunca é enviado, mesmo que esteja disponível (local padrão ou fornecido via [sslcert](libpq-connect.md#LIBPQ-CONNECT-SSLCERT)).

`allow` (padrão): Um certificado pode ser enviado, se o servidor solicitar um e o cliente tiver um para enviar.

`require` :   O servidor *deve* solicitar um certificado. A conexão falhará se o cliente não enviar um certificado e o servidor autenticar o cliente de qualquer forma.

Nota

`sslcertmode=require` não adiciona nenhuma segurança adicional, uma vez que não há garantia de que o servidor esteja validando o certificado corretamente; os servidores PostgreSQL geralmente solicitam certificados TLS dos clientes, independentemente de eles os validar ou não. A opção pode ser útil ao solucionar problemas em configurações TLS mais complicadas.

`sslrootcert` [#](#LIBPQ-CONNECT-SSLROOTCERT): Este parâmetro especifica o nome de um arquivo que contém o(s) certificado(s) da autoridade de certificação SSL. Se o arquivo existir, o certificado do servidor será verificado para ser assinado por uma dessas autoridades. O padrão é `~/.postgresql/root.crt`.

O valor especial `system` pode ser especificado em vez disso, nesse caso, as raízes de CA confiáveis da implementação SSL serão carregadas. As localizações exatas desses certificados raiz diferem de acordo com a implementação SSL e a plataforma. Para o OpenSSL, em particular, as localizações podem ser modificadas ainda mais pelas variáveis de ambiente `SSL_CERT_DIR` e `SSL_CERT_FILE`.

Nota

Ao usar `sslrootcert=system`, o padrão `sslmode` é alterado para `verify-full`, e qualquer configuração mais fraca resultará em um erro. Na maioria dos casos, é trivial para qualquer pessoa obter um certificado confiável pelo sistema para um nome de domínio que controla, tornando `verify-ca` e todos os modos mais fracos inúteis.

O valor mágico `system` terá precedência sobre um arquivo de certificado local com o mesmo nome. Se, por algum motivo, você se encontrar nessa situação, use um caminho alternativo como `sslrootcert=./system` em vez disso.

`sslcrl` [#](#LIBPQ-CONNECT-SSLCRL): Este parâmetro especifica o nome do arquivo do certificado de revogação do servidor SSL (CRL). Os certificados listados neste arquivo, se existir, serão rejeitados ao tentar autenticar o certificado do servidor. Se não for definido nem o [sslcrl](libpq-connect.md#LIBPQ-CONNECT-SSLCRL) nem [sslcrldir](libpq-connect.md#LIBPQ-CONNECT-SSLCRLDIR), este ajuste é considerado `~/.postgresql/root.crl`.

`sslcrldir` [#](#LIBPQ-CONNECT-SSLCRLDIR): Este parâmetro especifica o nome do diretório do certificado de servidor SSL de lista de revalidação (CRL). Os certificados listados nos arquivos neste diretório, se existir, serão rejeitados ao tentar autenticar o certificado do servidor.

O diretório precisa ser preparado com o comando OpenSSL `openssl rehash` ou `c_rehash`. Consulte a documentação para obter detalhes.

Ambos os `sslcrl` e `sslcrldir` podem ser especificados juntos.

`sslsni` [#](#LIBPQ-CONNECT-SSLSNI): Se definido como 1 (padrão), o libpq define a extensão TLS “Indicação de Nome do Servidor” (SNI) em conexões habilitadas SSL. Ao definir este parâmetro para 0, isso é desativado.

A Indicação do Nome do Servidor pode ser usada por proxies que reconhecem SSL para encaminhar conexões sem precisar descriptografar o fluxo SSL. (Observe que, a menos que o proxy esteja ciente do aperto de mão do protocolo PostgreSQL, isso exigiria definir `sslnegotiation` para `direct`.). No entanto, o SNI faz com que o nome do host de destino apareça em texto claro no tráfego de rede, então pode ser indesejável em alguns casos.

`requirepeer` [#](#LIBPQ-CONNECT-REQUIREPEER): Este parâmetro especifica o nome do usuário do sistema operacional do servidor, por exemplo `requirepeer=postgres`. Quando se faz uma conexão de soquete de domínio Unix, se este parâmetro estiver definido, o cliente verifica no início da conexão se o processo do servidor está em execução sob o nome de usuário especificado; se não estiver, a conexão é interrompida com um erro. Este parâmetro pode ser usado para fornecer autenticação do servidor semelhante àquela disponível com certificados SSL em conexões TCP/IP.

(Observe que se o soquete de domínio Unix estiver em `/tmp` ou em outro local publicamente legível, qualquer usuário pode iniciar um servidor que esteja ouvindo lá. Use este parâmetro para garantir que você esteja conectado a um servidor executado por um usuário de confiança.) Esta opção só é suportada em plataformas para as quais o método de autenticação `peer` é implementado; veja [Seção 20.9](auth-peer.md "20.9. Peer Authentication").

`ssl_min_protocol_version` [#](#LIBPQ-CONNECT-SSL-MIN-PROTOCOL-VERSION): Este parâmetro especifica a versão mínima do protocolo SSL/TLS para permitir a conexão. Os valores válidos são `TLSv1`, `TLSv1.1`, `TLSv1.2` e `TLSv1.3`. Os protocolos suportados dependem da versão do OpenSSL utilizada, as versões mais antigas não suportam as versões de protocolo mais modernas. Se não especificado, o padrão é `TLSv1.2`, que satisfaz as melhores práticas da indústria conforme esta redação.

`ssl_max_protocol_version` [#](#LIBPQ-CONNECT-SSL-MAX-PROTOCOL-VERSION): Este parâmetro especifica a versão máxima do protocolo SSL/TLS a ser permitida para a conexão. Os valores válidos são `TLSv1`, `TLSv1.1`, `TLSv1.2` e `TLSv1.3`. Os protocolos suportados dependem da versão do OpenSSL utilizada, as versões mais antigas não suportam as versões de protocolo mais modernas. Se não definido, este parâmetro é ignorado e a conexão utilizará o limite máximo definido pelo backend, se definido. Definir a versão do protocolo máxima é principalmente útil para testes ou se algum componente tiver problemas para trabalhar com um protocolo mais novo.

`min_protocol_version` [#](#LIBPQ-CONNECT-MIN-PROTOCOL-VERSION): Especifica a versão mínima do protocolo para permitir a conexão. O padrão é permitir qualquer versão do protocolo PostgreSQL suportada pelo libpq, que atualmente significa `3.0`. Se o servidor não suportar pelo menos essa versão do protocolo, a conexão será fechada.

Os valores atuais suportados são `3.0`, `3.2`, e `latest`. O valor `latest` é equivalente à versão mais recente do protocolo suportada pela versão do libpq que está sendo usada, que atualmente é `3.2`.

`max_protocol_version` [#](#LIBPQ-CONNECT-MAX-PROTOCOL-VERSION): Especifica a versão do protocolo a ser solicitada ao servidor. O padrão é usar a versão `3.0` do protocolo PostgreSQL, a menos que a string de conexão especifique uma característica que dependa de uma versão de protocolo mais alta, no qual caso, a versão mais recente suportada pelo libpq é usada. Se o servidor não suportar a versão do protocolo solicitada pelo cliente, a conexão é automaticamente desvalorizada para uma versão menor de protocolo menor que o servidor suporta. Após a tentativa de conexão ter sido concluída, você pode usar [`PQfullProtocolVersion`](libpq-status.md#LIBPQ-PQFULLPROTOCOLVERSION) para descobrir qual versão exata do protocolo foi negociada.

Os valores atuais suportados são `3.0`, `3.2`, e `latest`. O valor `latest` é equivalente à versão mais recente do protocolo suportada pela versão do libpq que está sendo usada, que atualmente é `3.2`.

`krbsrvname` [#](#LIBPQ-CONNECT-KRBSRVNAME): Nome do serviço Kerberos a ser usado na autenticação com GSSAPI. Este nome deve corresponder ao nome do serviço especificado na configuração do servidor para que a autenticação Kerberos seja bem-sucedida. (Veja também [Seção 20.6](gssapi-auth.md "20.6. GSSAPI Authentication")). O valor padrão é normalmente `postgres`, mas isso pode ser alterado ao construir o PostgreSQL via a opção `--with-krb-srvnam` do configure. Na maioria dos ambientes, este parâmetro nunca precisa ser alterado. Algumas implementações do Kerberos podem exigir um nome de serviço diferente, como o Microsoft Active Directory, que requer o nome do serviço a ser em maiúsculas (`POSTGRES`).

`gsslib` [#](#LIBPQ-CONNECT-GSSLIB): Biblioteca GSS para uso de autenticação GSSAPI. Atualmente, isso é ignorado, exceto em compilações do Windows que incluem suporte tanto para GSSAPI quanto para SSPI. Nesse caso, defina isso para `gssapi` para fazer com que o libpq use a biblioteca GSSAPI para autenticação em vez do SSPI padrão.

`gssdelegation` [#](#LIBPQ-CONNECT-GSSDELEGATION): Forwarde (delegue) as credenciais do GSS para o servidor. O padrão é `0` que significa que as credenciais não serão encaminhadas para o servidor. Defina isso para `1` para ter credenciais encaminhadas quando possível.

`scram_client_key` [#](#LIBPQ-CONNECT-SCRAM-CLIENT-KEY): A chave do cliente SCRAM codificada em base64. Esta pode ser usada por wrappers de dados estrangeiros ou middleware semelhante para habilitar a autenticação SCRAM pass-through. Veja [Seção F.38.1.10](postgres-fdw.md#POSTGRES-FDW-OPTIONS-CONNECTION-MANAGEMENT "F.38.1.10. Connection Management Options") para uma implementação desse tipo. Não é destinado a ser especificada diretamente por usuários ou aplicativos de cliente.

`scram_server_key` [#](#LIBPQ-CONNECT-SCRAM-SERVER-KEY): A chave do servidor SCRAM codificada em base64. Esta pode ser usada por wrappers de dados estrangeiros ou middleware semelhante para habilitar a autenticação SCRAM pass-through. Veja [Seção F.38.1.10](postgres-fdw.md#POSTGRES-FDW-OPTIONS-CONNECTION-MANAGEMENT "F.38.1.10. Connection Management Options") para uma implementação desse tipo. Não é destinado a ser especificado diretamente por usuários ou aplicativos de cliente.

`service` [#](#LIBPQ-CONNECT-SERVICE): Nome do serviço a ser usado para parâmetros adicionais. Especifica um nome de serviço em `pg_service.conf` que contém parâmetros de conexão adicionais. Isso permite que as aplicações especifiquem apenas um nome de serviço, de modo que os parâmetros de conexão possam ser mantidos centralmente. Veja [Seção 32.17](libpq-pgservice.md "32.17. The Connection Service File").

`target_session_attrs` [#](#LIBPQ-CONNECT-TARGET-SESSION-ATTRS): Esta opção determina se a sessão deve ter certas propriedades para ser aceitável. É tipicamente usada em combinação com vários nomes de host para selecionar a primeira alternativa aceitável entre vários hosts. Existem seis modos:

`any` (padrão): qualquer conexão bem-sucedida é aceitável

`read-write` :   a sessão deve aceitar transações de leitura e escrita por padrão (ou seja, o servidor não deve estar no modo de espera quente e o parâmetro `default_transaction_read_only` deve ser `off`)

`read-only`: A sessão não deve aceitar transações de leitura e escrita por padrão (o converse)

`primary` O servidor não deve estar no modo de standby quente

`standby`  : o servidor deve estar no modo de standby quente

`prefer-standby` :   primeiro, tente encontrar um servidor de espera, mas se nenhum dos hosts listados for um servidor de espera, tente novamente no modo `any`

`load_balance_hosts` [#](#LIBPQ-CONNECT-LOAD-BALANCE-HOSTS): Controla a ordem em que o cliente tenta se conectar aos hosts e endereços disponíveis. Uma vez que a tentativa de conexão seja bem-sucedida, nenhum outro host ou endereço será tentado. Este parâmetro é tipicamente usado em combinação com múltiplos nomes de host ou um registro DNS que retorne múltiplos IPs. Este parâmetro pode ser usado em combinação com [target_session_attrs](libpq-connect.md#LIBPQ-CONNECT-TARGET-SESSION-ATTRS) para, por exemplo, equilibrar a carga apenas em servidores de espera. Uma vez que a conexão seja bem-sucedida, as consultas subsequentes sobre a conexão retornada serão enviadas todas para o mesmo servidor. Atualmente, existem dois modos:

`disable` (padrão) :   Não é realizada a balança de carga entre os hosts. Os hosts são testados na ordem em que são fornecidos e os endereços são testados na ordem em que são recebidos do DNS ou de um arquivo de hosts.

`random` :   Os anfitriões e endereços são testados em ordem aleatória. Este valor é principalmente útil ao abrir várias conexões ao mesmo tempo, possivelmente a partir de diferentes máquinas. Dessa forma, as conexões podem ser balanceadas em múltiplos servidores PostgreSQL.

Embora o balanceamento aleatório de carga, devido à sua natureza aleatória, quase nunca resulte em uma distribuição completamente uniforme, ele se aproxima estatisticamente bastante. Um aspecto importante aqui é que este algoritmo utiliza dois níveis de escolhas aleatórias: primeiro, os hosts serão resolvidos em ordem aleatória. Em seguida, em segundo lugar, antes de resolver o próximo host, todas as endereços resolvidos para o host atual serão experimentados em ordem aleatória. Esse comportamento pode distorcer a quantidade de conexões que cada nó recebe em certos casos, por exemplo, quando alguns hosts resolvem mais endereços do que outros. Mas tal distorção também pode ser usada propositalmente, por exemplo, para aumentar o número de conexões que um servidor maior recebe, fornecendo seu nome de domínio várias vezes na string de host.

Ao usar esse valor, é recomendável configurar também um valor razoável para [connect_timeout](libpq-connect.md#LIBPQ-CONNECT-CONNECT-TIMEOUT). Porque, se um dos nós que são usados para balanceamento de carga não estiver respondendo, um novo nó será tentado.

`oauth_issuer` [#](#LIBPQ-CONNECT-OAUTH-ISSUER): O URL HTTPS de um emissor de confiança para entrar em contato se o servidor solicitar um token OAuth para a conexão. Este parâmetro é necessário para todas as conexões OAuth; ele deve corresponder exatamente ao ajuste `issuer` definido em [a configuração HBA do servidor](auth-oauth.md "20.15. OAuth Authorization/Authentication").

Como parte da troca de boas-vindas de autenticação padrão, o libpq solicitará ao servidor um *documento de descoberta*: uma URL que forneça um conjunto de parâmetros de configuração OAuth. O servidor deve fornecer uma URL que seja diretamente construída a partir dos componentes do `oauth_issuer`, e esse valor deve corresponder exatamente ao identificador do emissor que é declarado no próprio documento de descoberta, ou a conexão falhará. Isso é necessário para evitar uma classe de ataques de [[mix-up attacks]] (ataques de confusão) em clientes OAuth.

Você também pode explicitamente definir `oauth_issuer` para o URI `/.well-known/` usado para descoberta OAuth. Neste caso, se o servidor solicitar um URL diferente, a conexão falhará, mas um [fluxo OAuth personalizado](libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-HOOKS) pode ser capaz de acelerar o aperto padrão usando tokens previamente armazenados. (Neste caso, é recomendado que (libpq-connect.md#LIBPQ-CONNECT-OAUTH-SCOPE) seja definido também, uma vez que o cliente não terá a chance de pedir ao servidor um conjunto de escopo correto, e os escopos padrão para um token podem não ser suficientes para se conectar.) A libpq atualmente suporta os seguintes pontos finais bem conhecidos:

* `/.well-known/openid-configuration`
* `/.well-known/oauth-authorization-server`

### Aviso

Os emissor são altamente privilegiados durante o aperto de mão da conexão OAuth. Como regra geral, se você não confiar no operador de um URL para lidar com o acesso aos seus servidores, ou para se identificar diretamente como você, esse URL não deve ser confiável como um `oauth_issuer`.

`oauth_client_id` [#](#LIBPQ-CONNECT-OAUTH-CLIENT-ID): Um identificador de cliente OAuth 2.0, conforme emitido pelo servidor de autorização. Se o servidor PostgreSQL [solicitar um token OAuth](auth-oauth.md "20.15. OAuth Authorization/Authentication") para a conexão (e se não estiver instalado um [gancho OAuth personalizado](libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-HOOKS "32.20.1. Ganchos de Authdata"), para fornecer um), então este parâmetro deve ser definido; caso contrário, a conexão falhará.

`oauth_client_secret` [#](#LIBPQ-CONNECT-OAUTH-CLIENT-SECRET): A senha do cliente, se houver, a ser usada ao entrar em contato com o servidor de autorização OAuth. Se esse parâmetro é necessário ou não é determinado pelo provedor OAuth; clientes "públicos" geralmente não usam um segredo, enquanto os clientes "confidenciais" geralmente o fazem.

`oauth_scope` [#](#LIBPQ-CONNECT-OAUTH-SCOPE): O escopo da solicitação de acesso enviada ao servidor de autorização, especificado como uma lista (possivelmente vazia) de identificadores de escopo OAuth separados por espaço. Este parâmetro é opcional e destinado para uso avançado.

Normalmente, o cliente obterá as configurações apropriadas de escopo do servidor PostgreSQL. Se este parâmetro for usado, a lista de escopo solicitada pelo servidor será ignorada. Isso pode impedir que um servidor menos confiável solicite escopos de acesso inadequados do usuário final. No entanto, se a configuração de escopo do cliente não contiver os escopos necessários do servidor, o servidor provavelmente rejeitará o token emitido e a conexão falhará.

O significado de uma lista de escopo vazia depende do provedor. Um servidor de autorização OAuth pode optar por emitir um token com " escopo padrão ", o que aconteça, ou pode rejeitar o pedido de token completamente.