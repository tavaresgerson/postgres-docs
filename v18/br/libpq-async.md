## 32.4. Processamento de comandos assíncrono [#](#LIBPQ-ASYNC)

A função `PQexec`(libpq-exec.md#LIBPQ-PQEXEC) é adequada para enviar comandos em aplicações normais e síncronas. No entanto, ela possui algumas deficiências que podem ser importantes para alguns usuários:

* `PQexec` espera que o comando seja concluído. O aplicativo pode ter outras tarefas a serem realizadas (como manter uma interface de usuário), e, nesse caso, não desejará bloquear a espera pela resposta.
* Como a execução do aplicativo cliente é suspensa enquanto ele espera pelo resultado, é difícil para o aplicativo decidir que gostaria de tentar cancelar o comando em andamento. (Isso pode ser feito a partir de um manipulador de sinal, mas não de outra forma.)
* `PQexec` pode retornar apenas uma estrutura `PGresult`. Se a string de comando enviada contiver vários comandos SQL, todos, exceto o último `PGresult`, são descartados por `PQexec`](libpq-exec.md#LIBPQ-PQEXEC).
* `PQexec` sempre coleta o resultado completo do comando, armazenando-o em um único `PGresult`. Embora isso simplifique a lógica de tratamento de erros para o aplicativo, pode ser impraticável para resultados que contêm muitas linhas.

As aplicações que não gostam dessas limitações podem, em vez disso, usar as funções subjacentes de que o `PQexec` é construído: (libpq-exec.md#LIBPQ-PQEXEC) e `PQsendQuery` e (libpq-async.md#LIBPQ-PQSENDQUERY) e `PQgetResult` e (libpq-async.md#LIBPQ-PQGETRESULT). Também existem `PQsendQueryParams` e (libpq-async.md#LIBPQ-PQSENDQUERYPARAMS), `PQsendPrepare` e (libpq-async.md#LIBPQ-PQSENDPREPARE), `PQsendQueryPrepared` e (libpq-async.md#LIBPQ-PQSENDQUERYPREPARED), `PQsendDescribePrepared` e (libpq-async.md#LIBPQ-PQSENDDESCRIBEPREPARED), `PQsendDescribePortal` e (libpq-async.md#LIBPQ-PQSENDDESCRIBEPORTAL), `PQsendClosePrepared` e (libpq-async.md#LIBPQ-PQSENDCLOSEPREPARED), e `PQsendClosePortal` e (libpq-async.md#LIBPQ-PQSENDCLOSEPORTAL), que podem ser usadas com `PQgetResult` e (libpq-async.md#LIBPQ-PQGETRESULT) para duplicar a funcionalidade de `PQexecParams` e (libpq-exec.md#LIBPQ-PQEXECPARAMS), `PQprepare` e (libpq-exec.md#LIBPQ-PQPREPARE), `PQexecPrepared` e (libpq-exec.md#LIBPQ-PQEXECPREPARED), `PQdescribePrepared` e (libpq-exec.md#LIBPQ-PQDESCRIBEPREPARED), `PQdescribePortal` e (libpq-exec.md#LIBPQ-PQDESCRIBEPORTAL), `PQclosePrepared` e (libpq-exec.md#LIBPQ-PQCLOSEPREPARED), e `PQclosePortal` e (libpq-exec.md#LIBPQ-PQCLOSEPORTAL), respectivamente.

`PQsendQuery` [#](#LIBPQ-PQSENDQUERY): Envia um comando ao servidor sem esperar pelo(s) resultado(s). O valor 1 é retornado se o comando foi enviado com sucesso e 0 se não for (neste caso, use `PQerrorMessage`(libpq-status.md#LIBPQ-PQERRORMESSAGE) para obter mais informações sobre a falha).

``` int PQsendQuery(PGconn *conn, const char *command);
    ```

Após chamar com sucesso `PQsendQuery`](libpq-async.md#LIBPQ-PQSENDQUERY), chame `PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT) uma ou mais vezes para obter os resultados. `PQsendQuery`](libpq-async.md#LIBPQ-PQSENDQUERY) não pode ser chamado novamente (na mesma conexão) até que `PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT) retorne um ponteiro nulo, indicando que o comando foi concluído.

No modo de canal, essa função não é permitida.

`PQsendQueryParams` [#](#LIBPQ-PQSENDQUERYPARAMS): Envia um comando e parâmetros separados para o servidor sem esperar pelo(s) resultado(s).

``` int PQsendQueryParams(PGconn *conn, const char *command, int nParams, const Oid *paramTypes, const char * const *paramValues, const int *paramLengths, const int *paramFormats, int resultFormat);
    ```

Isso é equivalente a `PQsendQuery`(libpq-async.md#LIBPQ-PQSENDQUERY), exceto que os parâmetros da consulta podem ser especificados separadamente da cadeia de consulta. Os parâmetros da função são tratados de forma idêntica a `PQexecParams`(libpq-exec.md#LIBPQ-PQEXECPARAMS). Assim como `PQexecParams`(libpq-exec.md#LIBPQ-PQEXECPARAMS), permite apenas um comando na cadeia de consulta.

`PQsendPrepare` [#](#LIBPQ-PQSENDPREPARE)
:   Envia um pedido para criar uma declaração preparada com os parâmetros fornecidos, sem esperar pela conclusão.

    ```
    int PQsendPrepare(PGconn *conn, const char *stmtName, const char *query, int nParams, const Oid *paramTypes);
    ```

Esta é uma versão assíncrona de `PQprepare`(libpq-exec.md#LIBPQ-PQPREPARE): ela
retorna 1 se conseguiu enviar a solicitação, e 0 se não conseguiu.
Após uma chamada bem-sucedida, chame `PQgetResult`(libpq-async.md#LIBPQ-PQGETRESULT) para
determinar se o servidor criou com sucesso a declaração preparada. Os parâmetros da
função são tratados de forma idêntica a `PQprepare`(libpq-exec.md#LIBPQ-PQPREPARE).

`PQsendQueryPrepared` [#](#LIBPQ-PQSENDQUERYPREPARED)
:   Envia um pedido para executar uma declaração preparada com os parâmetros fornecidos, sem esperar pelo(s) resultado(s).

    ```
    int PQsendQueryPrepared(PGconn *conn, const char *stmtName, int nParams, const char * const *paramValues, const int *paramLengths, const int *paramFormats, int resultFormat);
    ```

Isso é semelhante a `PQsendQueryParams`(libpq-async.md#LIBPQ-PQSENDQUERYPARAMS), mas o comando a ser executado é especificado ao nomear uma declaração previamente preparada, em vez de fornecer uma string de consulta. Os parâmetros da função são tratados de forma idêntica a `PQexecPrepared`(libpq-exec.md#LIBPQ-PQEXECPREPARED).

`PQsendDescribePrepared` [#](#LIBPQ-PQSENDDESCRIBEPREPARED) :   Envia uma solicitação para obter informações sobre a declaração preparada especificada, sem esperar a conclusão.

    ```
    int PQsendDescribePrepared(PGconn *conn, const char *stmtName);
    ```

Esta é uma versão assíncrona de `PQdescribePrepared`(libpq-exec.md#LIBPQ-PQDESCRIBEPREPARED):
retorna 1 se conseguiu enviar a solicitação, e 0 se não conseguiu.
Após uma chamada bem-sucedida, chame `PQgetResult`(libpq-async.md#LIBPQ-PQGETRESULT) para
obter os resultados. Os parâmetros da função são tratados
identicamente a `PQdescribePrepared`(libpq-exec.md#LIBPQ-PQDESCRIBEPREPARED).

`PQsendDescribePortal` [#](#LIBPQ-PQSENDDESCRIBEPORTAL) :   Envia uma solicitação para obter informações sobre o portal especificado, sem esperar a conclusão.

    ```
    int PQsendDescribePortal(PGconn *conn, const char *portalName);
    ```

Esta é uma versão assíncrona de `PQdescribePortal`(libpq-exec.md#LIBPQ-PQDESCRIBEPORTAL):
retorna 1 se conseguiu enviar a solicitação, e 0 se não conseguiu.
Após uma chamada bem-sucedida, chame `PQgetResult`(libpq-async.md#LIBPQ-PQGETRESULT) para
obter os resultados. Os parâmetros da função são tratados
identicamente a `PQdescribePortal`(libpq-exec.md#LIBPQ-PQDESCRIBEPORTAL).

`PQsendClosePrepared` [#](#LIBPQ-PQSENDCLOSEPREPARED) : Envia uma solicitação para fechar a declaração preparada especificada, sem esperar a conclusão.

    ```
    int PQsendClosePrepared(PGconn *conn, const char *stmtName);
    ```

Esta é uma versão assíncrona de `PQclosePrepared`(libpq-exec.md#LIBPQ-PQCLOSEPREPARED):
retorna 1 se conseguiu enviar a solicitação, e 0 se não conseguiu.
Após uma chamada bem-sucedida, chame `PQgetResult`(libpq-async.md#LIBPQ-PQGETRESULT) para
obter os resultados. Os parâmetros da função são tratados
identicamente a `PQclosePrepared`(libpq-exec.md#LIBPQ-PQCLOSEPREPARED).

`PQsendClosePortal` [#](#LIBPQ-PQSENDCLOSEPORTAL) :   Envia uma solicitação para fechar o portal especificado, sem esperar a conclusão.

    ```
    int PQsendClosePortal(PGconn *conn, const char *portalName);
    ```

Esta é uma versão assíncrona de `PQclosePortal`(libpq-exec.md#LIBPQ-PQCLOSEPORTAL):
retorna 1 se conseguiu enviar a solicitação, e 0 se não conseguiu.
Após uma chamada bem-sucedida, chame `PQgetResult`(libpq-async.md#LIBPQ-PQGETRESULT) para
obter os resultados. Os parâmetros da função são tratados
identicamente a `PQclosePortal`(libpq-exec.md#LIBPQ-PQCLOSEPORTAL).

Espera pelo próximo resultado de um pedido anterior
    [`PQsendQuery`](libpq-async.md#LIBPQ-PQSENDQUERY),
    [`PQsendQueryParams`](libpq-async.md#LIBPQ-PQSENDQUERYPARAMS),
    [`PQsendPrepare`](libpq-async.md#LIBPQ-PQSENDPREPARE),
    [`PQsendQueryPrepared`](libpq-async.md#LIBPQ-PQSENDQUERYPREPARED),
    [`PQsendDescribePrepared`](libpq-async.md#LIBPQ-PQSENDDESCRIBEPREPARED),
    [`PQsendDescribePortal`](libpq-async.md#LIBPQ-PQSENDDESCRIBEPORTAL),
    [`PQsendClosePrepared`](libpq-async.md#LIBPQ-PQSENDCLOSEPREPARED),
    [`PQsendClosePortal`](libpq-async.md#LIBPQ-PQSENDCLOSEPORTAL),
    [`PQsendPipelineSync`](libpq-pipeline-mode.md#LIBPQ-PQSENDPIPELINESYNC), ou
    [`PQpipelineSync`](libpq-pipeline-mode.md#LIBPQ-PQPIPELINESYNC)
    e retorna-o.
Um ponteiro nulo é retornado quando o comando está completo e não haverá mais resultados.

    ```
    PGresult *PQgetResult(PGconn *conn);
    ```

`PQgetResult` deve ser chamado repetidamente até que retorne um ponteiro nulo, indicando que o comando está concluído. (Se chamado quando não há comando ativo, `PQgetResult` apenas retornará um ponteiro nulo de uma vez.) Cada resultado não nulo de `PQgetResult` deve ser processado usando as mesmas funções de acesso `PGresult` descritas anteriormente. Não se esqueça de liberar cada objeto de resultado com `PQclear` quando estiver pronto para descartá-lo. Note que `PQgetResult` bloqueará apenas se um comando estiver ativo e os dados de resposta necessários ainda não tenham sido lidos por `PQconsumeInput` (libpq-async.md#LIBPQ-PQCONSUMEINPUT).

No modo de pipeline, `PQgetResult` retornará normalmente, a menos que ocorra um erro; para qualquer consulta subsequente enviada após aquela que causou o erro até (e excluindo) o próximo ponto de sincronização, um resultado especial do tipo `PGRES_PIPELINE_ABORTED` será retornado, e um ponteiro nulo será retornado após ele. Quando o ponto de sincronização do pipeline for alcançado, um resultado do tipo `PGRES_PIPELINE_SYNC` será retornado. O resultado da próxima consulta após o ponto de sincronização segue imediatamente (ou seja, não é retornado um ponteiro nulo após o ponto de sincronização).

### Nota

Mesmo quando `PQresultStatus` indica um erro fatal, (libpq-exec.md#LIBPQ-PQRESULTSTATUS) deve ser chamado até que ele retorne um ponteiro nulo, para permitir que o libpq processe completamente as informações do erro.

Usando `PQsendQuery` e (libpq-async.md#LIBPQ-PQSENDQUERY), e
[`PQgetResult` e (libpq-async.md#LIBPQ-PQGETRESULT) resolve um dos problemas do
[`PQexec` e (libpq-exec.md#LIBPQ-PQEXEC): Se uma string de comando contém
múltiplos comandos SQL, os resultados desses comandos
podem ser obtidos individualmente. (Isso permite uma forma simples de processamento
sobreposto, aliás: o cliente pode estar lidando com os resultados de um
comando enquanto o servidor ainda está trabalhando em consultas posteriores na
mesma string de comando.)

Outra característica frequentemente desejada que pode ser obtida com `PQsendQuery` e (libpq-async.md#LIBPQ-PQSENDQUERY) é a recuperação de resultados de consulta grandes, um número limitado de linhas de cada vez.
Isso é discutido em [Seção 32.6](libpq-single-row-mode.md "32.6. Retrieving Query Results in Chunks").

Por si só, chamar `PQgetResult`(libpq-async.md#LIBPQ-PQGETRESULT) ainda fará com que o cliente bloqueie até que o servidor complete o próximo comando SQL. Isso pode ser evitado pelo uso adequado de mais duas funções:

`PQconsumeInput` [#](#LIBPQ-PQCONSUMEINPUT)
:   Se o input estiver disponível no servidor, consuma-o.

    ```
    int PQconsumeInput(PGconn *conn);
    ```

`PQconsumeInput` normalmente retorna 1, indicando "sem erro", mas retorna 0 se houver algum tipo de problema (neste caso, `PQerrorMessage` pode ser consultado). Note que o resultado não diz se algum dado de entrada foi realmente coletado. Após chamar `PQconsumeInput`, o aplicativo pode verificar `PQisBusy` e/ou `PQnotifies` para ver se seu estado mudou.

`PQconsumeInput` pode ser chamado mesmo se o aplicativo não está preparado para lidar com um resultado ou notificação ainda. A função irá ler os dados disponíveis e salvá-los em um buffer, causando assim a indicação de `select()` pronta para leitura a desaparecer. O aplicativo pode, assim, usar `PQconsumeInput` para limpar a condição `select()` imediatamente e, em seguida, examinar os resultados com calma.

`PQisBusy` [#](#LIBPQ-PQISBUSY) Retorna 1 se um comando estiver ocupado, ou seja, `PQgetResult`(libpq-async.md#LIBPQ-PQGETRESULT) bloquearia a espera por entrada. Um retorno de 0 indica que `PQgetResult`(libpq-async.md#LIBPQ-PQGETRESULT) pode ser chamado com a garantia de não bloquear.

    ```
    int PQisBusy(PGconn *conn);
    ```

`PQisBusy` não tentará ler dados do servidor; portanto, `PQconsumeInput` deve ser invocado primeiro, ou o estado ocupado nunca terminará.

Uma aplicação típica que utiliza essas funções terá um loop principal que
usa `select()` ou `poll()` para esperar
todas as condições para as quais ele deve responder. Uma das condições
será a entrada disponível do servidor, o que, em termos de
`select()`, significa dados legíveis no descritor de arquivo
identificado por (libpq-status.md#LIBPQ-PQSOCKET). Quando o loop principal detecta que a entrada está pronta, ele deve chamar
`PQconsumeInput`(libpq-async.md#LIBPQ-PQCONSUMEINPUT) para ler a entrada. Em seguida, ele pode
chamar `PQisBusy`(libpq-async.md#LIBPQ-PQISBUSY), seguido por
`PQgetResult`[[(libpq-async.md#LIBPQ-PQGETRESULT)] se `PQisBusy`(libpq-async.md#LIBPQ-PQISBUSY) retorna falso (0). Ele também pode chamar `PQnotifies`
para detectar mensagens de `NOTIFY` (ver [Seção 32.9][(libpq-notify.md "32.9. Asynchronous Notification")]).

Um cliente que usa
[`PQsendQuery`](libpq-async.md#LIBPQ-PQSENDQUERY)/[`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT)
também pode tentar cancelar um comando que ainda está sendo processado
pelo servidor; veja [Seção 32.7](libpq-cancel.md "32.7. Canceling Queries in Progress"). Mas, independentemente
do valor de retorno de [`PQcancelBlocking`](libpq-cancel.md#LIBPQ-PQCANCELBLOCKING), o aplicativo
deve continuar com a sequência normal de leitura de resultados usando
[`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT). Um cancelamento bem-sucedido simplesmente fará com que o comando termine mais cedo do que teria
de outra forma.

Ao usar as funções descritas acima, é possível evitar o bloqueio enquanto espera a entrada do servidor de banco de dados. No entanto, ainda é possível que o aplicativo bloqueie enquanto espera para enviar saída para o servidor. Isso é relativamente incomum, mas pode acontecer se comandos SQL muito longos ou valores de dados forem enviados. (É muito mais provável se o aplicativo enviar dados via `COPY IN`, no entanto.) Para evitar essa possibilidade e obter uma operação de banco de dados completamente não bloqueável, as seguintes funções adicionais podem ser usadas.

`PQsetnonblocking` [#](#LIBPQ-PQSETNONBLOCKING) :   Define o estado não bloqueável da conexão.

    ```
    int PQsetnonblocking(PGconn *conn, int arg);
    ```

Define o estado da conexão como não bloqueante se
*`arg`* for 1, ou bloqueante se
*`arg`* for 0. Retorna 0 se OK, -1 se houver erro.

No estado não bloqueável, as chamadas bem-sucedidas em
[`PQsendQuery`](libpq-async.md#LIBPQ-PQSENDQUERY), [`PQputline`](libpq-copy.md#LIBPQ-PQPUTLINE),
[`PQputnbytes`](libpq-copy.md#LIBPQ-PQPUTNBYTES), [`PQputCopyData`](libpq-copy.md#LIBPQ-PQPUTCOPYDATA),
e [`PQendcopy`](libpq-copy.md#LIBPQ-PQENDCOPY) não bloquearão; suas alterações
são armazenadas no buffer de saída local até serem descarregadas.
Chamadas não bem-sucedidas retornarão um erro e devem ser repetidas.

Observe que `PQexec`(libpq-exec.md#LIBPQ-PQEXEC) não respeita o modo não bloqueável; se for chamado, ele atuará de qualquer forma em modo bloqueável.

`PQisnonblocking` [#](#LIBPQ-PQISNONBLOCKING)
:   Retorna o estado de bloqueio da conexão do banco de dados.

    ```
    int PQisnonblocking(const PGconn *conn);
    ```

Retorna 1 se a conexão estiver configurada no modo não bloqueante e 0 se estiver no modo bloqueante.

`PQflush` [#](#LIBPQ-PQFLUSH) :   Tenta limpar qualquer dados de saída em fila no servidor. Retorna 0 se o processo for bem-sucedido (ou se a fila de envio estiver vazia), -1 se falhou por algum motivo, ou 1 se não conseguiu enviar todos os dados na fila de envio ainda (este caso só pode ocorrer se a conexão não for bloqueada).

    ```
    int PQflush(PGconn *conn);
    ```

Após enviar qualquer comando ou dados em uma conexão não bloqueável, chame
`PQflush`(libpq-async.md#LIBPQ-PQFLUSH). Se ele retornar 1, espere até que o socket
se torne pronto para leitura ou escrita. Se ele se tornar pronto para escrita, chame
`PQflush`(libpq-async.md#LIBPQ-PQFLUSH) novamente. Se ele se tornar pronto para leitura, chame
`PQconsumeInput`(libpq-async.md#LIBPQ-PQCONSUMEINPUT), então chame
`PQflush`(libpq-async.md#LIBPQ-PQFLUSH) novamente. Repita até que
`PQflush`(libpq-async.md#LIBPQ-PQFLUSH) retorne 0. (É necessário verificar se está pronto para leitura e drenar a entrada com `PQconsumeInput`(libpq-async.md#LIBPQ-PQCONSUMEINPUT), porque o servidor pode bloquear ao tentar nos enviar dados, por exemplo, mensagens de NOTÍCIA, e não lerá nossos dados até que os lemos.) Uma vez
`PQflush`(libpq-async.md#LIBPQ-PQFLUSH) retorne 0, espere até que o socket esteja pronto para leitura e então leia a resposta conforme descrito acima.