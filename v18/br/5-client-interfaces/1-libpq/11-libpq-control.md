## 32.11. Funções de Controle [#](#LIBPQ-CONTROL)

Essas funções controlam detalhes diversos do comportamento do libpq.

`PQclientEncoding` [#](#LIBPQ-PQCLIENTENCODING): Retorna o codificação do cliente.

```
int PQclientEncoding(const PGconn *conn);
```

Observe que ele retorna o ID de codificação, não uma string simbólica como `EUC_JP`. Se não for bem-sucedido, ele retorna -1. Para converter um ID de codificação em um nome de codificação, você pode usar:

```
char *pg_encoding_to_char(int encoding_id);
```

`PQsetClientEncoding` [#](#LIBPQ-PQSETCLIENTENCODING): Define o codificação do cliente.

```
int PQsetClientEncoding(PGconn *conn, const char *encoding);
```

*`conn`* é uma conexão com o servidor, e *`encoding`* é o codificação que você deseja utilizar. Se a função definir com sucesso a codificação, ela retorna 0, caso contrário, -1. O codificação atual para esta conexão pode ser determinado usando [[`PQclientEncoding`](libpq-control.md#LIBPQ-PQCLIENTENCODING)].

`PQsetErrorVerbosity` [#](#LIBPQ-PQSETERRORVERBOSITY): Determina a verbosidade das mensagens retornadas por [`PQerrorMessage`](libpq-status.md#LIBPQ-PQERRORMESSAGE) e [`PQresultErrorMessage`](libpq-exec.md#LIBPQ-PQRESULTERRORMESSAGE).

```
typedef enum { PQERRORS_TERSE, PQERRORS_DEFAULT, PQERRORS_VERBOSE, PQERRORS_SQLSTATE } PGVerbosity;

PGVerbosity PQsetErrorVerbosity(PGconn *conn, PGVerbosity verbosity);
```

`PQsetErrorVerbosity`](libpq-control.md#LIBPQ-PQSETERRORVERBOSITY) define o modo de verbosidade, retornando a configuração anterior da conexão. No modo *TERSE*, as mensagens devolvidas incluem severidade, texto primário e posição apenas; isso normalmente cabe em uma única linha. O modo *DEFAULT* produz mensagens que incluem o acima mencionado, além de qualquer campo de detalhe, dica ou contexto (estes podem ocupar várias linhas). O modo *VERBOSE* inclui todos os campos disponíveis. O modo *SQLSTATE* inclui apenas a gravidade do erro e o código de erro `SQLSTATE`, se houver um disponível (se não, a saída é como modo *TERSE*).

Altere a configuração de verbosidade não afeta as mensagens disponíveis de objetos já existentes `PGresult`, apenas os posteriormente criados.

(Mas veja `PQresultVerboseErrorMessage`(libpq-exec.md#LIBPQ-PQRESULTVERBOSEERRORMESSAGE) se você deseja imprimir um erro anterior com uma verbosidade diferente.)

`PQsetErrorContextVisibility` [#](#LIBPQ-PQSETERRORCONTEXTVISIBILITY): Determina o tratamento dos campos `CONTEXT` em mensagens retornadas por [`PQerrorMessage`](libpq-status.md#LIBPQ-PQERRORMESSAGE) e [`PQresultErrorMessage`](libpq-exec.md#LIBPQ-PQRESULTERRORMESSAGE).

```
typedef enum { PQSHOW_CONTEXT_NEVER, PQSHOW_CONTEXT_ERRORS, PQSHOW_CONTEXT_ALWAYS } PGContextVisibility;

PGContextVisibility PQsetErrorContextVisibility(PGconn *conn, PGContextVisibility show_context);
```

`PQsetErrorContextVisibility` define o modo de exibição do contexto, retornando a configuração anterior da conexão. Esse modo controla se o campo `CONTEXT` é incluído nas mensagens. O modo *NÃO* nunca inclui `CONTEXT`, enquanto *SEMPRE* o inclui sempre que estiver disponível. No modo *ERROS* (o padrão), os campos `CONTEXT` são incluídos apenas em mensagens de erro, não em avisos e alertas. (No entanto, se a configuração de verbosidade for *TERSE* ou *SQLSTATE*, os campos `CONTEXT` são omitidos, independentemente do modo de exibição do contexto.)

Altere este modo não afeta as mensagens disponíveis dos objetos já existentes de `PGresult`, apenas dos posteriormente criados. (Mas veja `PQresultVerboseErrorMessage`(libpq-exec.md#LIBPQ-PQRESULTVERBOSEERRORMESSAGE) se você deseja imprimir um erro anterior com um modo de exibição diferente.)

`PQtrace` [#](#LIBPQ-PQTRACE): Permite o rastreamento da comunicação cliente/servidor para um fluxo de arquivo de depuração.

```
void PQtrace(PGconn *conn, FILE *stream);
```

Cada linha consiste em: um marcador de tempo opcional, um indicador de direção (`F` para mensagens do cliente para o servidor ou `B` para mensagens do servidor para o cliente), comprimento da mensagem, tipo de mensagem e conteúdo da mensagem. Os campos de conteúdo não-mensagem (marcador de tempo, direção, comprimento e tipo de mensagem) são separados por uma tabulação. O conteúdo da mensagem é separado por um espaço. As strings de protocolo são encerradas em aspas duplas, enquanto as strings usadas como valores de dados são encerradas em aspas simples. Os caracteres não imprimíveis são impressos como escapamentos hexadecimais. Mais detalhes específicos sobre o tipo de mensagem podem ser encontrados em [Seção 54.7](protocol-message-formats.md).

### Nota

Em Windows, se a biblioteca libpq e um aplicativo forem compilados com diferentes flags, essa chamada de função irá falhar o aplicativo porque a representação interna dos ponteiros `FILE` é diferente. Especificamente, as flags multithread/single-threaded, release/debug e estática/dinâmica devem ser as mesmas para a biblioteca e todos os aplicativos que utilizam essa biblioteca.

`PQsetTraceFlags` [#](#LIBPQ-PQSETTRACEFLAGS): Controla o comportamento de rastreamento da comunicação cliente/servidor.

```
void PQsetTraceFlags(PGconn *conn, int flags);
```

`flags` contém bits de bandeira que descrevem o modo de operação do rastreamento. Se `flags` contém `PQTRACE_SUPPRESS_TIMESTAMPS`, então o timestamp não é incluído ao imprimir cada mensagem. Se `flags` contém `PQTRACE_REGRESS_MODE`, então alguns campos são ocultos ao imprimir cada mensagem, como OIDs de objeto, para tornar a saída mais conveniente para uso em frameworks de teste. Esta função deve ser chamada após chamar `PQtrace`.

`PQuntrace` [#](#LIBPQ-PQUNTRACE): Desabilita o rastreamento iniciado por [`PQtrace`](libpq-control.md#LIBPQ-PQTRACE).

```
void PQuntrace(PGconn *conn);
```
