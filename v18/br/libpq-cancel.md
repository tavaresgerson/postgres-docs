## 32.7. Cancelamento de consultas em andamento [#](#LIBPQ-CANCEL)

* [32.7.1. Funções para Enviar Solicitações de Cancelamento](libpq-cancel.md#LIBPQ-CANCEL-FUNCTIONS)
* [32.7.2. Funções Obsoletas para Enviar Solicitações de Cancelamento](libpq-cancel.md#LIBPQ-CANCEL-DEPRECATED)

### 32.7.1. Funções para Enviar Solicitações de Cancelamento [#](#LIBPQ-CANCEL-FUNCTIONS)

`PQcancelCreate` [#](#LIBPQ-PQCANCELCREATE): Prepara uma conexão sobre a qual uma solicitação de cancelamento pode ser enviada.

``` PGcancelConn *PQcancelCreate(PGconn *conn);
    ```

`PQcancelCreate` cria um objeto (libpq-cancel.md#LIBPQ-PQCANCELCREATE) `PGcancelConn`, mas ele não começará a enviar uma solicitação de cancelamento imediatamente por essa conexão. Uma solicitação de cancelamento pode ser enviada por essa conexão de maneira bloqueante usando `PQcancelBlocking` (libpq-cancel.md#LIBPQ-PQCANCELBLOCKING) e de maneira não bloqueante usando `PQcancelStart` (libpq-cancel.md#LIBPQ-PQCANCELSTART). O valor de retorno pode ser passado para `PQcancelStatus` (libpq-cancel.md#LIBPQ-PQCANCELSTATUS) para verificar se o objeto `PGcancelConn` foi criado com sucesso. O objeto `PGcancelConn` é uma estrutura opaca que não deve ser acessada diretamente pela aplicação. Este objeto `PGcancelConn` pode ser usado para cancelar a consulta que está em execução na conexão original de maneira segura em relação aos threads.

Muitos dos parâmetros de conexão do cliente original serão reutilizados ao configurar a conexão para o pedido de cancelamento. É importante ressaltar que, se a conexão original exigir criptografia da conexão e/ou verificação do host-alvo (usando `sslmode` ou `gssencmode`), a conexão para o pedido de cancelamento será feita com esses mesmos requisitos. No entanto, quaisquer opções de conexão que sejam usadas apenas durante a autenticação ou após a autenticação do cliente serão ignoradas, pois os pedidos de cancelamento não exigem autenticação e a conexão é fechada logo após o pedido de cancelamento ser enviado.

Observe que, quando `PQcancelCreate` retorna um ponteiro não nulo, você deve chamar `PQcancelFinish` quando estiver terminado com ele, a fim de descartar a estrutura e quaisquer blocos de memória associados. Isso deve ser feito mesmo que a solicitação de cancelamento tenha falhado ou sido abandonada.

`PQcancelBlocking` [#](#LIBPQ-PQCANCELBLOCKING): Solicita que o servidor abandone o processamento do comando atual de forma bloqueante.

``` int PQcancelBlocking(PGcancelConn *cancelConn);
    ```

O pedido é feito através do dado `PGcancelConn`,
que precisa ser criado com (libpq-cancel.md#LIBPQ-PQCANCELCREATE).
O valor de retorno de `PQcancelBlocking`(libpq-cancel.md#LIBPQ-PQCANCELBLOCKING)
é 1 se o pedido de cancelamento foi enviado com sucesso
e 0 se não for. Se não tiver sido bem-sucedido, a mensagem de erro pode ser
recuperada usando `PQcancelErrorMessage`(libpq-cancel.md#LIBPQ-PQCANCELERRORMESSAGE).

O envio bem-sucedido da anulação não é garantia de que o pedido terá algum efeito, no entanto. Se a anulação for eficaz, o comando que está sendo cancelado terminará precocemente e retornará um resultado de erro. Se a anulação falhar (digamos, porque o servidor já havia processado o comando), então não haverá nenhum resultado visível.

`PQcancelStart` `PQcancelPoll` [#](#LIBPQ-PQCANCELSTART) :   Solicita que o servidor abandone o processamento do comando atual de forma não bloqueante.

    ```
    int PQcancelStart(PGcancelConn *cancelConn);

    PostgresPollingStatusType PQcancelPoll(PGcancelConn *cancelConn);
    ```

O pedido é feito sobre o dado `PGcancelConn`,
que precisa ser criado com (libpq-cancel.md#LIBPQ-PQCANCELCREATE).
O valor de retorno de `PQcancelStart`(libpq-cancel.md#LIBPQ-PQCANCELSTART)
é 1 se o pedido de cancelamento puder ser iniciado e 0 se não puder.
Se não tiver sido bem-sucedido, a mensagem de erro pode ser
recuperada usando `PQcancelErrorMessage`(libpq-cancel.md#LIBPQ-PQCANCELERRORMESSAGE).

Se `PQcancelStart` tiver sucesso, a próxima etapa é fazer uma consulta à libpq para que ela possa prosseguir com a sequência de cancelamento da conexão.
Use (libpq-cancel.md#LIBPQ-PQCANCELSOCKET) para obter o descritor do socket que suporta a conexão com o banco de dados.
(Cuidado: não se pode assumir que o socket permaneça o mesmo em todas as chamadas de `PQcancelPoll`.)
O ciclo é o seguinte: Se `PQcancelPoll(cancelConn)` retornou `PGRES_POLLING_READING` na última vez, espere até que o socket esteja pronto para leitura (conforme indicado por `select()`, `poll()` ou uma função semelhante do sistema).
Em seguida, chame `PQcancelPoll(cancelConn)` novamente.
Por outro lado, se `PQcancelPoll(cancelConn)` retornou `PGRES_POLLING_WRITING` na última vez, espere até que o socket esteja pronto para escrita, em seguida, chame `PQcancelPoll(cancelConn)` novamente.
Na primeira iteração, ou seja, se ainda não chamou `PQcancelPoll(cancelConn)`, se comporte como se tivesse retornado `PGRES_POLLING_WRITING`. Continue este ciclo até que `PQcancelPoll(cancelConn)` retorne
`PGRES_POLLING_FAILED`, indicando que o procedimento de conexão falhou, ou `PGRES_POLLING_OK`, indicando que a solicitação de cancelamento foi enviada com sucesso.

O envio bem-sucedido da anulação não é garantia de que o pedido terá algum efeito, no entanto. Se a anulação for eficaz, o comando que está sendo cancelado terminará precocemente e retornará um resultado de erro. Se a anulação falhar (digamos, porque o servidor já havia processado o comando), então não haverá nenhum resultado visível.

Em qualquer momento durante a conexão, o status da conexão pode ser verificado chamando `PQcancelStatus`(libpq-cancel.md#LIBPQ-PQCANCELSTATUS).
Se essa chamada retornar `CONNECTION_BAD`, então o procedimento de cancelamento falhou; se a chamada retornar `CONNECTION_OK`, então a solicitação de cancelamento foi enviada com sucesso.
Ambos esses estados são igualmente detectáveis pelo valor de retorno de `PQcancelPoll`, descrito acima.
Outros estados também podem ocorrer durante (e apenas durante) um procedimento de conexão assíncrona.
Esses indicam o estágio atual do procedimento de conexão e podem ser úteis para fornecer feedback ao usuário, por exemplo.
Esses status são:

`CONNECTION_ALLOCATED` [#](#LIBPQ-CANCEL-CONNECTION-ALLOCATED)
    :   Esperando uma chamada para [`PQcancelStart`](libpq-cancel.md#LIBPQ-PQCANCELSTART) ou
        [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING), para realmente abrir o
        socket. Este é o estado de conexão logo após
        chamar [`PQcancelCreate`](libpq-cancel.md#LIBPQ-PQCANCELCREATE)
        ou [`PQcancelReset`](libpq-cancel.md#LIBPQ-PQCANCELRESET). Ainda não foi iniciada nenhuma conexão com o
        servidor neste ponto. Para realmente começar a enviar a solicitação de cancelamento, use [`PQcancelStart`](libpq-cancel.md#LIBPQ-PQCANCELSTART) ou
        [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING).

`CONNECTION_STARTED` [#](#LIBPQ-CANCEL-CONNECTION-STARTED)
    :   Esperando que a conexão seja feita.

`CONNECTION_MADE` [#](#LIBPQ-CANCEL-CONNECTION-MADE)
    :   Conexão OK; aguardando para enviar.

`CONNECTION_AWAITING_RESPONSE` [#](#LIBPQ-CANCEL-CONNECTION-AWAITING-RESPONSE)
    :  Esperando uma resposta do servidor.

`CONNECTION_SSL_STARTUP` [#](#LIBPQ-CANCEL-CONNECTION-SSL-STARTUP)
    :   Negociar criptografia SSL.

`CONNECTION_GSS_STARTUP` [#](#LIBPQ-CANCEL-CONNECTION-GSS-STARTUP)
    :   Negociar criptografia GSS.

Observe que, embora essas constantes permaneçam (para manter a compatibilidade), uma aplicação nunca deve depender dessas ocorrer em uma ordem específica, ou de forma alguma, ou de que o status esteja sempre em um desses valores documentados. Uma aplicação pode fazer algo assim:

    ```
    switch(PQcancelStatus(conn)) { case CONNECTION_STARTED: feedback = "Connecting..."; break;

            case CONNECTION_MADE: feedback = "Connected to server..."; break; . . . default: feedback = "Connecting..."; }
    ```

O parâmetro de conexão `connect_timeout` é ignorado quando se usa `PQcancelPoll`; é responsabilidade da aplicação decidir se há um período excessivo de tempo. Caso contrário, `PQcancelStart` seguido por um loop `PQcancelPoll` é equivalente a `PQcancelBlocking`(libpq-cancel.md#LIBPQ-PQCANCELBLOCKING).

`PQcancelStatus` [#](#LIBPQ-PQCANCELSTATUS) :  Retorna o status da conexão cancelada.

    ```
    ConnStatusType PQcancelStatus(const PGcancelConn *cancelConn);
    ```

O status pode ser um dos vários valores. No entanto, apenas três desses são vistos fora de um procedimento de cancelamento assíncrono:
`CONNECTION_ALLOCATED`,
`CONNECTION_OK` e
`CONNECTION_BAD`. O estado inicial de um
`PGcancelConn` que foi criado com sucesso usando
[`PQcancelCreate`(libpq-cancel.md#LIBPQ-PQCANCELCREATE) é `CONNECTION_ALLOCATED`. Uma solicitação de cancelamento que foi enviada com sucesso tem o status
`CONNECTION_OK`. Uma tentativa de cancelamento falhada é sinalizada pelo status
`CONNECTION_BAD`. Um status OK permanecerá assim até que [`PQcancelFinish`(libpq-cancel.md#LIBPQ-PQCANCELFINISH) ou
[`PQcancelReset`(libpq-cancel.md#LIBPQ-PQCANCELRESET) seja chamado.

Veja a entrada para `PQcancelStart`(libpq-cancel.md#LIBPQ-PQCANCELSTART) em relação a outros códigos de status que podem ser retornados.

O envio bem-sucedido da anulação não é garantia de que o pedido terá algum efeito, no entanto. Se a anulação for eficaz, o comando que está sendo cancelado terminará precocemente e retornará um resultado de erro. Se a anulação falhar (digamos, porque o servidor já havia processado o comando), então não haverá nenhum resultado visível.

`PQcancelSocket` [#](#LIBPQ-PQCANCELSOCKET) : Obtém o número de descritor de arquivo do socket de conexão cancelada ao servidor.

    ```
    int PQcancelSocket(const PGcancelConn *cancelConn);
    ```

Um descritor válido será maior ou igual a 0;
um resultado de -1 indica que nenhuma conexão com o servidor está aberta atualmente.
Isso pode mudar como resultado da chamada de qualquer uma das funções
nesta seção no `PGcancelConn`
(exceto para [`PQcancelErrorMessage`](libpq-cancel.md#LIBPQ-PQCANCELERRORMESSAGE) e
`PQcancelSocket` em si).

`PQcancelErrorMessage` [#](#LIBPQ-PQCANCELERRORMESSAGE)
:   Retorna a mensagem de erro gerada mais recentemente por uma operação na conexão de cancelamento.

    ```
    char *PQcancelErrorMessage(const PGcancelConn *cancelconn);
    ```

Quase todas as funções libpq que aceitam um
`PGcancelConn` definirão uma mensagem para
(libpq-cancel.md#LIBPQ-PQCANCELERRORMESSAGE) se falharem.
Observe que, de acordo com a convenção da libpq,
um resultado não vazio
`PQcancelErrorMessage` pode consistir em várias linhas e incluirá uma nova linha final.
O chamador não deve liberar o resultado diretamente.
Ele será liberado quando o controle associado
`PGcancelConn` for passado para
`PQcancelFinish` e
(libpq-cancel.md#LIBPQ-PQCANCELFINISH). A string de resultado não deve ser
esperada para permanecer a mesma em operações na
`PGcancelConn` estrutura.

`PQcancelFinish` [#](#LIBPQ-PQCANCELFINISH)
:   Fecha a conexão cancelada (se ainda não tiver terminado de enviar a solicitação de cancelamento). Também libera a memória usada pelo objeto `PGcancelConn`.

    ```
    void PQcancelFinish(PGcancelConn *cancelConn);
    ```

Observe que, mesmo que a tentativa de cancelamento falhe (conforme indicado por `PQcancelStatus`][(libpq-cancel.md#LIBPQ-PQCANCELSTATUS)), o aplicativo deve chamar `PQcancelFinish`][(libpq-cancel.md#LIBPQ-PQCANCELFINISH) para liberar a memória usada pelo objeto `PGcancelConn`. O ponteiro `PGcancelConn` não deve ser usado novamente após [`PQcancelFinish`][(libpq-cancel.md#LIBPQ-PQCANCELFINISH) ter sido chamado.

`PQcancelReset` [#](#LIBPQ-PQCANCELRESET)
:   Redefine o `PGcancelConn` para que possa ser reutilizado para uma nova
    cancelar a conexão.

    ```
    void PQcancelReset(PGcancelConn *cancelConn);
    ```

Se o `PGcancelConn` estiver sendo usado para enviar uma solicitação de cancelamento, então essa conexão será fechada. Em seguida, o objeto `PGcancelConn` será preparado para que possa ser usado para enviar uma nova solicitação de cancelamento.

Isso pode ser usado para criar um `PGcancelConn` para um `PGconn` e reutilizá-lo várias vezes ao longo da vida útil do `PGconn` original.

### 32.7.2. Funções obsoletas para envio de solicitações de cancelamento [#](#LIBPQ-CANCEL-DEPRECATED)

Essas funções representam métodos mais antigos de envio de solicitações de cancelamento. Embora ainda funcionem, elas são desaconselhadas devido ao fato de não enviar as solicitações de cancelamento de forma encriptada, mesmo quando a conexão original especificou `sslmode` ou `gssencmode` para exigir encriptação. Assim, esses métodos mais antigos são fortemente desencorajados a serem usados em código novo, e é recomendado alterar o código existente para usar as novas funções em vez disso.

`PQgetCancel` [#](#LIBPQ-PQGETCANCEL)
:   Cria uma estrutura de dados contendo as informações necessárias para cancelar um comando usando [`PQcancel`](libpq-cancel.md#LIBPQ-PQCANCEL).

    ```
    PGcancel *PQgetCancel(PGconn *conn);
    ```

`PQgetCancel` cria um objeto (libpq-cancel.md#LIBPQ-PQGETCANCEL) dado um objeto de conexão `PGconn`.
Ele retornará `NULL` se o *`conn`* dado for `NULL` ou uma conexão inválida.
O objeto `PGcancel` é uma estrutura opaca que não deve ser acessada diretamente pelo aplicativo; ele só pode ser passado para [`PQcancel`(libpq-cancel.md#LIBPQ-PQCANCEL)]] ou [`PQfreeCancel`(libpq-cancel.md#LIBPQ-PQFREECANCEL)].

`PQfreeCancel` [#](#LIBPQ-PQFREECANCEL)
:   Libera uma estrutura de dados criada por [`PQgetCancel`](libpq-cancel.md#LIBPQ-PQGETCANCEL).

    ```
    void PQfreeCancel(PGcancel *cancel);
    ```

`PQfreeCancel` libera um objeto de dados previamente criado por `PQgetCancel`(libpq-cancel.md#LIBPQ-PQGETCANCEL).

`PQcancel` [#](#LIBPQ-PQCANCEL) é uma variante desatualizada e insegura
    de [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING), mas uma que pode ser
    utilizada com segurança dentro de um manipulador de sinal.

    ```
    int PQcancel(PGcancel *cancel, char *errbuf, int errbufsize);
    ```

`PQcancel` só existe por razões de compatibilidade reversa. (libpq-cancel.md#LIBPQ-PQCANCEL) deve ser usado em vez disso. O único benefício que `PQcancel` tem é que ele pode ser invocado com segurança a partir de um manipulador de sinal, se o *`errbuf`* é uma variável local no manipulador de sinal. No entanto, isso geralmente não é considerado um benefício grande o suficiente para valer as questões de segurança que essa função tem.

O objeto `PGcancel` é somente de leitura quanto ao que diz respeito a
`PQcancel`(libpq-cancel.md#LIBPQ-PQCANCEL), portanto, ele também pode ser invocado
de uma thread que é separada daquela que manipula o objeto
`PGconn`.

O valor de retorno de `PQcancel`(libpq-cancel.md#LIBPQ-PQCANCEL) é 1 se o pedido de cancelamento foi enviado com sucesso e 0 se não for.
Se não for, *`errbuf`* é preenchido com uma mensagem de erro explicativa.
*`errbuf`* deve ser um array de caracteres do tamanho de
*`errbufsize`* (o tamanho recomendado é de 256 bytes).

`PQrequestCancel` [#](#LIBPQ-PQREQUESTCANCEL) é uma variante desatualizada e insegura de [`PQrequestCancel`](libpq-cancel.md#LIBPQ-PQREQUESTCANCEL).

    ```
    int PQrequestCancel(PGconn *conn);
    ```

`PQrequestCancel` só existe por razões de compatibilidade reversa. (libpq-cancel.md#LIBPQ-PQREQUESTCANCEL) deve ser usado em vez disso. Não há benefício em usar `PQrequestCancel` sobre (libpq-cancel.md#LIBPQ-PQREQUESTCANCEL).

Solicita que o servidor abandone o processamento da ordem atual. Opera diretamente no objeto `PGconn` e, em caso de falha, armazena a mensagem de erro no objeto `PGconn` (onde pode ser recuperada por `PQerrorMessage`(libpq-status.md#LIBPQ-PQERRORMESSAGE)). Embora a funcionalidade seja a mesma, essa abordagem não é segura em programas com múltiplos threads ou manipuladores de sinal, pois é possível que a sobrescrita da mensagem de erro do `PGconn` atrapalhe a operação atualmente em andamento na conexão.