## 32.13. Processamento de Notificações [#](#LIBPQ-NOTICE-PROCESSING)

Mensagens de aviso e de notificação geradas pelo servidor não são devolvidas pelas funções de execução de consulta, uma vez que elas não implicam falha na consulta. Em vez disso, elas são passadas para uma função de tratamento de notificação, e a execução continua normalmente após o manipulador retornar. A função padrão de tratamento de notificação imprime a mensagem em `stderr`, mas o aplicativo pode sobrepor esse comportamento fornecendo sua própria função de tratamento.

Por razões históricas, existem dois níveis de manipulação de notificações, chamados receptor de notificações e processador de notificações. O comportamento padrão é que o receptor de notificações formate a notificação e passe uma string para o processador de notificações para impressão. No entanto, uma aplicação que opta por fornecer seu próprio receptor de notificações geralmente ignora a camada de processador de notificações e realiza todo o trabalho no próprio receptor de notificações.

A função `PQsetNoticeReceiver` define ou examina o receptor de notificações atual para um objeto de conexão. Da mesma forma, `PQsetNoticeProcessor` define ou examina o processador de notificações atual.

```
typedef void (*PQnoticeReceiver) (void *arg, const PGresult *res);

PQnoticeReceiver
PQsetNoticeReceiver(PGconn *conn,
                    PQnoticeReceiver proc,
                    void *arg);

typedef void (*PQnoticeProcessor) (void *arg, const char *message);

PQnoticeProcessor
PQsetNoticeProcessor(PGconn *conn,
                     PQnoticeProcessor proc,
                     void *arg);
```

Cada uma dessas funções retorna o ponteiro anterior da função de receptor ou processador de notificações e define o novo valor. Se você fornecer um ponteiro de função nulo, nenhuma ação é realizada, mas o ponteiro atual é retornado.

Quando um aviso ou mensagem de alerta é recebido do servidor ou gerado internamente pela libpq, a função de recebimento de notificação é chamada. Ela recebe a mensagem na forma de um `PGRES_NONFATAL_ERROR` `PGresult`. (Isso permite que o receptor extraia campos individuais usando `PQresultErrorField`(libpq-exec.md#LIBPQ-PQRESULTERRORFIELD), ou obtenha uma mensagem preformatada completa usando `PQresultErrorMessage`(libpq-exec.md#LIBPQ-PQRESULTERRORMESSAGE) ou `PQresultVerboseErrorMessage`(libpq-exec.md#LIBPQ-PQRESULTVERBOSEERRORMESSAGE).). O mesmo ponteiro nulo passado para `PQsetNoticeReceiver` também é passado. (Esse ponteiro pode ser usado para acessar o estado específico da aplicação, se necessário.)

O receptor de notificação padrão simplesmente extrai a mensagem (usando `PQresultErrorMessage`(libpq-exec.md#LIBPQ-PQRESULTERRORMESSAGE)) e a passa para o processador de notificação.

O processador de notificação é responsável por lidar com uma notificação ou mensagem de alerta dada em formato de texto. Ele recebe o texto da mensagem (incluindo uma nova linha final), além de um ponteiro nulo que é o mesmo que é passado para `PQsetNoticeProcessor`. (Este ponteiro pode ser usado para acessar o estado específico da aplicação, se necessário.)

O processador de notificações padrão é simplesmente:

```
static void
defaultNoticeProcessor(void *arg, const char *message)
{
    fprintf(stderr, "%s", message);
}
```

Uma vez que você tenha configurado um receptor ou processador de notificações, você deve esperar que essa função possa ser chamada enquanto o objeto `PGconn` ou os objetos `PGresult` feitos a partir dele existirem. Na criação de um `PGresult`, os ponteiros atuais de manipulação de notificações do `PGconn` são copiados para o `PGresult`, para possível uso por funções como [`PQgetvalue`(libpq-exec.md#LIBPQ-PQGETVALUE)].