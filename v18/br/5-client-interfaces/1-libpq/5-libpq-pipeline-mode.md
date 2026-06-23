## 32.5. Modo de Pipeline [#](#LIBPQ-PIPELINE-MODE)

* [32.5.1. Uso do Modo Pipeline](libpq-pipeline-mode.md#LIBPQ-PIPELINE-USING)
* [32.5.2. Funções Associadas ao Modo Pipeline](libpq-pipeline-mode.md#LIBPQ-PIPELINE-FUNCTIONS)
* [32.5.3. Quando Usar o Modo Pipeline](libpq-pipeline-mode.md#LIBPQ-PIPELINE-TIPS)

O modo pipeline do libpq permite que as aplicações enviem uma consulta sem precisar ler o resultado da consulta enviada anteriormente. Aproveitando o modo pipeline, um cliente esperará menos pelo servidor, uma vez que várias consultas/resultados podem ser enviados/recebidos em uma única transação de rede.

Embora o modo de pipeline ofereça um aumento significativo de desempenho, escrever clientes usando o modo de pipeline é mais complexo, pois envolve a gestão de uma fila de consultas pendentes e a identificação de qual resultado corresponde a qual consulta na fila.

O modo de pipeline também consome, em geral, mais memória tanto no cliente quanto no servidor, embora uma gestão cuidadosa e agressiva da fila de envio/recebimento possa mitigar isso. Isso se aplica independentemente de a conexão estar em modo de bloqueio ou

Embora a API de pipeline do libpq tenha sido introduzida no PostgreSQL 14, é uma característica do lado do cliente que não requer suporte especial do servidor e funciona em qualquer servidor que suporte o protocolo de consulta estendida v3. Para mais informações, consulte [Seção 54.2.4](protocol-flow.md#PROTOCOL-FLOW-PIPELINING).

### 32.5.1. Uso do Modo Pipeline [#](#LIBPQ-PIPELINE-USING)

Para emitir pipelines, o aplicativo deve alternar a conexão para o modo pipeline, o que é feito com `PQenterPipelineMode`(libpq-pipeline-mode.md#LIBPQ-PQENTERPIPELINEMODE). `PQpipelineStatus`(libpq-pipeline-mode.md#LIBPQ-PQPIPELINESTATUS) pode ser usado para testar se o modo pipeline está ativo. No modo pipeline, apenas operações assíncronas (libpq-async.md "32.4. Asynchronous Command Processing") que utilizam o protocolo de consulta estendida são permitidas, as cadeias de comando que contêm múltiplos comandos SQL são desaconselhadas, e o mesmo vale para `COPY`. Usar funções de execução de comandos síncronas, como `PQfn`, `PQexec`, `PQexecParams`, `PQprepare`, `PQexecPrepared`, `PQdescribePrepared`, `PQdescribePortal`, `PQclosePrepared`, `PQclosePortal`, é uma condição de erro. `PQsendQuery` também é desaconselhado, porque utiliza o protocolo de consulta simples. Uma vez que todos os comandos emitidos tenham tido seus resultados processados e o resultado final do pipeline tenha sido consumido, o aplicativo pode retornar ao modo não pipeline com [`PQexitPipelineMode`](libpq-pipeline-mode.md#LIBPQ-PQEXITPIPELINEMODE).

Nota

É melhor usar o modo de canal com o libpq em modo não bloqueante (libpq-async.md#LIBPQ-PQSETNONBLOCKING). Se usado em modo bloqueante, é possível ocorrer um bloqueio entre cliente e servidor. [[15]](#ftn.id-1.7.3.12.9.3.1.3)

#### 32.5.1.1. Emitir consultas [#](#LIBPQ-PIPELINE-SENDING)

Após entrar no modo de pipeline, o aplicativo envia solicitações usando `PQsendQueryParams`(libpq-async.md#LIBPQ-PQSENDQUERYPARAMS) ou seu irmão de consulta preparada `PQsendQueryPrepared`(libpq-async.md#LIBPQ-PQSENDQUERYPREPARED). Essas solicitações são colocadas em fila no lado do cliente até serem descarregadas no servidor; isso ocorre quando `PQpipelineSync`(libpq-pipeline-mode.md#LIBPQ-PQPIPELINESYNC) é usado para estabelecer um ponto de sincronização no pipeline, ou quando `PQflush`(libpq-async.md#LIBPQ-PQFLUSH) é chamado. As funções `PQsendPrepare`(libpq-async.md#LIBPQ-PQSENDPREPARE), `PQsendDescribePrepared`(libpq-async.md#LIBPQ-PQSENDDESCRIBEPREPARED), `PQsendDescribePortal`(libpq-async.md#LIBPQ-PQSENDDESCRIBEPORTAL), `PQsendClosePrepared`(libpq-async.md#LIBPQ-PQSENDCLOSEPREPARED) e `PQsendClosePortal`(libpq-async.md#LIBPQ-PQSENDCLOSEPORTAL) também funcionam no modo de pipeline. O processamento dos resultados é descrito abaixo.

O servidor executa instruções e retorna resultados na ordem em que o cliente as envia. O servidor começará a executar os comandos no pipeline imediatamente, sem esperar o fim do pipeline. Observe que os resultados são armazenados em buffer no lado do servidor; o servidor descarta esse buffer quando um ponto de sincronização é estabelecido com `PQpipelineSync` ou `PQsendPipelineSync`, ou quando `PQsendFlushRequest` é chamado. Se qualquer instrução encontrar um erro, o servidor interrompe a transação atual e não executa nenhum comando subsequente na fila até o próximo ponto de sincronização; um resultado de `PGRES_PIPELINE_ABORTED` é produzido para cada comando desse tipo. (Isso permanece verdadeiro mesmo se os comandos no pipeline desfazerem a transação.) O processamento da consulta é retomado após o ponto de sincronização.

É perfeitamente aceitável que uma operação dependa dos resultados de uma operação anterior; por exemplo, uma consulta pode definir uma tabela que a próxima consulta no mesmo pipeline utiliza. Da mesma forma, uma aplicação pode criar uma declaração preparada com nome e executá-la com declarações posteriores no mesmo pipeline.

#### 32.5.1.2. Processamento de Resultados [#](#LIBPQ-PIPELINE-RESULTS)

Para processar o resultado de uma consulta em um pipeline, o aplicativo chama `PQgetResult` repetidamente e processa cada resultado até que `PQgetResult` retorne nulo. O resultado da próxima consulta no pipeline pode então ser recuperado novamente usando `PQgetResult` e o ciclo pode ser repetido. O aplicativo processa os resultados individuais das declarações normalmente. Quando os resultados de todas as consultas no pipeline tiverem sido retornados, `PQgetResult` retorna um resultado contendo o valor de status `PGRES_PIPELINE_SYNC`.

O cliente pode optar por adiar o processamento dos resultados até que o pipeline completo tenha sido enviado, ou intercalá-lo com o envio de outras consultas no pipeline; veja [Seção 32.5.1.4](libpq-pipeline-mode.md#LIBPQ-PIPELINE-INTERLEAVE).

`PQgetResult` se comporta da mesma forma que para o processamento asíncrono normal, exceto que ele pode conter os novos tipos `PGresult` e `PGRES_PIPELINE_SYNC`. `PGRES_PIPELINE_SYNC` é relatado exatamente uma vez para cada `PQpipelineSync` ou `PQsendPipelineSync` no ponto correspondente na linha de produção. `PGRES_PIPELINE_ABORTED` é emitido em substituição a um resultado normal de consulta para o primeiro erro e todos os resultados subsequentes até o próximo `PGRES_PIPELINE_SYNC`; veja [Seção 32.5.1.3](libpq-pipeline-mode.md#LIBPQ-PIPELINE-ERRORS "32.5.1.3. Error Handling").

`PQisBusy`, `PQconsumeInput`, etc. funcionam normalmente ao processar os resultados do pipeline. Em particular, uma chamada para `PQisBusy` no meio de um pipeline retorna 0 se os resultados de todas as consultas emitidas até então tiverem sido consumidos.

O libpq não fornece nenhuma informação para o aplicativo sobre a consulta atualmente sendo processada (exceto que `PQgetResult` retorna nulo para indicar que começamos a retornar os resultados da próxima consulta). O aplicativo deve acompanhar a ordem em que enviou as consultas, para associá-las aos seus resultados correspondentes. Normalmente, os aplicativos usam uma máquina de estado ou uma fila FIFO para isso.

#### 32.5.1.3. Gerenciamento de Erros [#](#LIBPQ-PIPELINE-ERRORS)

Do ponto de vista do cliente, após o `PQresultStatus` retornar o `PGRES_FATAL_ERROR`, o pipeline é marcado como abortado. O `PQresultStatus` reportará um resultado `PGRES_PIPELINE_ABORTED` para cada operação restante em pipeline abortado. O resultado para o `PQpipelineSync` ou `PQsendPipelineSync` é reportado como `PGRES_PIPELINE_SYNC` para sinalizar o fim do pipeline abortado e a retomada do processamento normal dos resultados.

O cliente *deve* processar resultados com `PQgetResult` durante a recuperação de erros.

Se o pipeline tiver utilizado uma transação implícita, as operações que já foram executadas serão revertidas e as operações que estavam em fila para seguir a operação falha serão ignoradas completamente. O mesmo comportamento ocorre se o pipeline iniciar e confirmar uma única transação explícita (ou seja, a primeira declaração é `BEGIN` e a última é `COMMIT`) exceto que a sessão permaneça em um estado de transação abortado no final do pipeline. Se um pipeline contiver *múltiplas transações explícitas*, todas as transações que foram confirmadas antes do erro permanecem confirmadas, a transação atualmente em andamento é abortada e todas as operações subsequentes são ignoradas completamente, incluindo as transações subsequentes. Se um ponto de sincronização de pipeline ocorrer com um bloco de transação explícita em estado abortado, o próximo pipeline se tornará abortado imediatamente, a menos que o próximo comando coloque a transação no modo normal com `ROLLBACK`.

Nota

O cliente não deve assumir que o trabalho está comprometido quando *envia* um `COMMIT` — apenas quando o resultado correspondente é recebido para confirmar que o compromisso está completo. Como os erros chegam de forma assíncrona, o aplicativo precisa ser capaz de reiniciar a partir da última mudança *recebida* e reenviar o trabalho feito após esse ponto, se algo der errado.

#### 32.5.1.4. Processamento de resultados de intercalamento e despacho de consultas [#](#LIBPQ-PIPELINE-INTERLEAVE)

Para evitar travamentos em grandes oleodutos, o cliente deve ser estruturado em torno de um loop de eventos não bloqueável, utilizando facilidades do sistema operacional, como `select`, `poll`, `WaitForMultipleObjectEx`, etc.

O aplicativo cliente deve, em geral, manter uma fila de trabalhos pendentes a serem enviados e uma fila de trabalhos que foram enviados, mas ainda não tiveram seus resultados processados. Quando a soquete é legível, ela deve enviar mais trabalhos. Quando a soquete é legível, ela deve ler os resultados e processá-los, correspondendo-os à próxima entrada em sua fila de resultados correspondente. Com base na memória disponível, os resultados da soquete devem ser lidos frequentemente: não é necessário esperar até o final do pipeline para ler os resultados. As pipelinhas devem ser definidas em unidades lógicas de trabalho, geralmente (mas não necessariamente) uma transação por pipeline. Não é necessário sair do modo de pipeline e reentrá-lo entre as pipelinhas, ou esperar que uma pipeline termine antes de enviar a próxima.

Um exemplo que utiliza `select()` e uma máquina simples de estado para rastrear trabalhos enviados e recebidos está em `src/test/modules/libpq_pipeline/libpq_pipeline.c` na distribuição de código-fonte do PostgreSQL.

### 32.5.2. Funções associadas ao modo de tubulação [#](#LIBPQ-PIPELINE-FUNCTIONS)

`PQpipelineStatus` [#](#LIBPQ-PQPIPELINESTATUS): Retorna o estado atual do modo de pipeline da conexão libpq.

```
PGpipelineStatus PQpipelineStatus(const PGconn *conn);
```

`PQpipelineStatus` pode retornar um dos seguintes valores:

`PQ_PIPELINE_ON` :   A conexão libpq está no modo de pipeline.

`PQ_PIPELINE_OFF` :   A conexão libpq *não* está no modo de pipeline.

`PQ_PIPELINE_ABORTED` :   A conexão libpq está no modo de pipeline e ocorreu um erro ao processar o pipeline atual. A bandeira abortada é limpa quando `PQgetResult` retorna um resultado do tipo `PGRES_PIPELINE_SYNC`.

`PQenterPipelineMode` [#](#LIBPQ-PQENTERPIPELINEMODE): Faz com que a conexão entre no modo de pipeline se ela estiver atualmente parada ou já no modo de pipeline.

```
int PQenterPipelineMode(PGconn *conn);
```

Retorna 1 para sucesso. Retorna 0 e não tem efeito se a conexão não estiver atualmente inativa, ou seja, tem um resultado pronto, ou está esperando mais entrada do servidor, etc. Esta função não envia nada para o servidor, apenas muda o estado da conexão libpq.

`PQexitPipelineMode` [#](#LIBPQ-PQEXITPIPELINEMODE): Faz com que a conexão saia do modo de pipeline se estiver atualmente no modo de pipeline com uma fila vazia e sem resultados pendentes.

```
int PQexitPipelineMode(PGconn *conn);
```

Retorna 1 para sucesso. Retorna 1 e não realiza nenhuma ação se não estiver no modo pipeline. Se a declaração atual não tiver sido finalizada o processamento, ou `PQgetResult` não tiver sido chamado para coletar resultados de todas as consultas enviadas anteriormente, retorna 0 (neste caso, use [[`PQerrorMessage`](libpq-status.md#LIBPQ-PQERRORMESSAGE) para obter mais informações sobre a falha).

`PQpipelineSync` [#](#LIBPQ-PQPIPELINESYNC): Marca um ponto de sincronização em uma linha de produção enviando uma [mensagem de sincronização](protocol-flow.md#PROTOCOL-FLOW-EXT-QUERY "54.2.3. Extended Query") e esvaziando o buffer de envio. Isso serve como o delimitador de uma transação implícita e um ponto de recuperação de erro; veja [Seção 32.5.1.3](libpq-pipeline-mode.md#LIBPQ-PIPELINE-ERRORS "32.5.1.3. Error Handling").

```
int PQpipelineSync(PGconn *conn);
```

Retorna 1 para sucesso. Retorna 0 se a conexão não estiver no modo de pipeline ou se a mensagem de [sincronização](protocol-flow.md#PROTOCOL-FLOW-EXT-QUERY) falhou.

`PQsendPipelineSync` [#](#LIBPQ-PQSENDPIPELINESYNC): Marca um ponto de sincronização em um pipeline enviando uma [mensagem de sincronização](protocol-flow.md#PROTOCOL-FLOW-EXT-QUERY "54.2.3. Extended Query") sem esvaziar o buffer de envio. Isso serve como o delimitador de uma transação implícita e um ponto de recuperação de erro; veja [Seção 32.5.1.3](libpq-pipeline-mode.md#LIBPQ-PIPELINE-ERRORS "32.5.1.3. Error Handling").

```
int PQsendPipelineSync(PGconn *conn);
```

Retorna 1 para sucesso. Retorna 0 se a conexão não estiver no modo de pipeline ou se a mensagem de [sincronização](protocol-flow.md#PROTOCOL-FLOW-EXT-QUERY) falhou. Observe que a mensagem não é automaticamente enviada ao servidor; use `PQflush` se necessário.

`PQsendFlushRequest` [#](#LIBPQ-PQSENDFLUSHREQUEST) : Envia uma solicitação para que o servidor limpe seu buffer de saída.

```
int PQsendFlushRequest(PGconn *conn);
```

Retorna 1 para sucesso. Retorna 0 em caso de falha.

O servidor esvazia seu buffer de saída automaticamente como resultado de `PQpipelineSync` ser chamado, ou em qualquer solicitação quando não estiver no modo de pipeline; essa função é útil para fazer com que o servidor esvazie seu buffer de saída no modo de pipeline sem estabelecer um ponto de sincronização. Observe que a solicitação não é esvaziada automaticamente para o servidor; use `PQflush` se necessário.

### 32.5.3. Quando usar o modo Pipeline [#](#LIBPQ-PIPELINE-TIPS)

Assim como o modo de consulta assíncrona, não há sobrecarga significativa de desempenho ao usar o modo de pipeline. Ele aumenta a complexidade da aplicação do cliente, e é necessária cautela extra para evitar deadlocks cliente/servidor, mas o modo de pipeline pode oferecer melhorias consideráveis de desempenho, em troca do uso de memória aumentado ao deixar o estado por mais tempo.

O modo pipeline é mais útil quando o servidor está distante, ou seja, quando a latência da rede (tempo de ping) é alta, e também quando muitas operações pequenas estão sendo realizadas em rápida sucessão. Geralmente, há menos benefício em usar comandos em pipeline quando cada consulta leva muitos múltiplos do tempo de ida e volta do cliente/servidor para ser executada. Uma operação de 100 declarações executada em um servidor com uma latência de ida e volta de 300 ms levaria 30 segundos apenas na latência da rede; com o pipeline, pode gastar tão pouco quanto 0,3 s esperando os resultados do servidor.

Utilize comandos em pipeline quando sua aplicação realiza muitas operações pequenas `INSERT`, `UPDATE` e `DELETE` que não podem ser facilmente transformadas em operações em conjuntos, ou em uma operação `COPY`.

O modo pipeline não é útil quando as informações de uma operação são necessárias pelo cliente para produzir a próxima operação. Nesses casos, o cliente teria que introduzir um ponto de sincronização e esperar por um percurso completo cliente/servidor para obter os resultados necessários. No entanto, muitas vezes é possível ajustar o projeto do cliente para trocar as informações necessárias pelo lado do servidor. Os ciclos de leitura-modificação-escrita são candidatos especialmente bons; por exemplo:

```
BEGIN; SELECT x FROM mytable WHERE id = 42 FOR UPDATE; -- result: x=2 -- client adds 1 to x: UPDATE mytable SET x = 3 WHERE id = 42; COMMIT;
```

poderia ser feito de forma muito mais eficiente com:

```
UPDATE mytable SET x = x + 1 WHERE id = 42;
```

O pipelining é menos útil e mais complexo quando um único pipeline contém múltiplas transações (consulte [Seção 32.5.1.3](libpq-pipeline-mode.md#LIBPQ-PIPELINE-ERRORS)).

---

O cliente bloqueará a tentativa de enviar consultas ao servidor, mas o servidor bloqueará a tentativa de enviar resultados ao cliente a partir de consultas que já processou. Isso ocorre apenas quando o cliente envia consultas suficientes para encher tanto seu buffer de saída quanto o buffer de recepção do servidor antes de mudar para processar entrada do servidor, mas é difícil prever exatamente quando isso ocorrerá.