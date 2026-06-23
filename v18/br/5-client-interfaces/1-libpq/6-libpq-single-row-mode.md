## 32.6. Recuperação de resultados de consulta em fragmentos [#](#LIBPQ-SINGLE-ROW-MODE)

Normalmente, o libpq coleta todo o resultado de um comando SQL e o retorna ao aplicativo como um único `PGresult`. Isso pode não ser viável para comandos que retornam um grande número de linhas. Para esses casos, os aplicativos podem usar `PQsendQuery`(libpq-async.md#LIBPQ-PQSENDQUERY) e `PQgetResult`(libpq-async.md#LIBPQ-PQGETRESULT) no modo *de uma única linha* ou *em modo truncado*. Nesses modos, o(s) resultado(s) da linha(s) é(são) retornado(s) ao aplicativo conforme recebido(s) do servidor, uma de cada vez para o modo de uma única linha ou em grupos para o modo truncado.

Para entrar em um desses modos, ligue imediatamente para `PQsetSingleRowMode`(libpq-single-row-mode.md#LIBPQ-PQSETSINGLEROWMODE) ou `PQsetChunkedRowsMode`(libpq-single-row-mode.md#LIBPQ-PQSETCHUNKEDROWSMODE) após uma chamada bem-sucedida de `PQsendQuery`(libpq-async.md#LIBPQ-PQSENDQUERY) (ou uma função irmã). Essa seleção de modo é eficaz apenas para a consulta atualmente em execução. Em seguida, chame `PQgetResult`(libpq-async.md#LIBPQ-PQGETRESULT) repetidamente, até que ela retorne null, conforme documentado em [Seção 32.4](libpq-async.md "32.4. Asynchronous Command Processing"). Se a consulta retornar alguma linha, elas são devolvidas como um ou mais objetos `PGresult`, que parecem resultados normais de consulta, exceto pelo fato de terem o código de status `PGRES_SINGLE_TUPLE` para o modo de uma única linha ou `PGRES_TUPLES_CHUNK` para o modo truncado, em vez de `PGRES_TUPLES_OK`. Há exatamente uma linha de resultado em cada objeto `PGRES_SINGLE_TUPLE`, enquanto um objeto `PGRES_TUPLES_CHUNK` contém pelo menos uma linha, mas não mais do que o número especificado de linhas por bloco. Após a última linha, ou imediatamente se a consulta retornar zero linhas, um objeto de zero linha com status `PGRES_TUPLES_OK` é devolvido; este é o sinal de que mais linhas não chegarão. (Mas note que ainda é necessário continuar chamando [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT)] até que ela retorne null.) Todos esses objetos `PGresult` conterão os mesmos dados de descrição de linha (nomes de coluna, tipos, etc.) que um objeto `PGresult` comum para a consulta teria. Cada objeto deve ser liberado com [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) como de costume.

Ao usar o modo de pipeline, o modo de linha única ou em blocos precisa ser ativado para cada consulta no pipeline antes de recuperar os resultados para essa consulta com `PQgetResult`. Consulte a [Seção 32.5](libpq-pipeline-mode.md) para mais informações.

`PQsetSingleRowMode` [#](#LIBPQ-PQSETSINGLEROWMODE): Selecionar o modo de uma única linha para a consulta atualmente em execução.

```
int PQsetSingleRowMode(PGconn *conn);
```

Essa função só pode ser chamada imediatamente após `PQsendQuery` ou uma de suas funções irmãs, antes de qualquer outra operação na conexão, como `PQconsumeInput` ou `PQgetResult` ou (libpq-async.md#LIBPQ-PQGETRESULT). Se chamada no momento correto, a função ativa o modo de única linha para a consulta atual e retorna 1. Caso contrário, o modo permanece inalterado e a função retorna 0. Em qualquer caso, o modo retorna ao normal após a conclusão da consulta atual.

`PQsetChunkedRowsMode` [#](#LIBPQ-PQSETCHUNKEDROWSMODE): Selecionar o modo em blocos para a consulta atualmente em execução.

```
int PQsetChunkedRowsMode(PGconn *conn, int chunkSize);
```

Essa função é semelhante a `PQsetSingleRowMode`(libpq-single-row-mode.md#LIBPQ-PQSETSINGLEROWMODE), exceto que especifica a recuperação de até *`chunkSize`* linhas `PGresult`, não necessariamente apenas uma linha. Essa função só pode ser chamada imediatamente após `PQsendQuery`(libpq-async.md#LIBPQ-PQSENDQUERY) ou uma de suas funções irmãs, antes de qualquer outra operação na conexão, como `PQconsumeInput`(libpq-async.md#LIBPQ-PQCONSUMEINPUT) ou `PQgetResult`(libpq-async.md#LIBPQ-PQGETRESULT). Se chamada no momento correto, a função ativa o modo em blocos para a consulta atual e retorna 1. Caso contrário, o modo permanece inalterado e a função retorna 0. Em qualquer caso, o modo retorna ao normal após a conclusão da consulta atual.

### Atenção

Ao processar uma consulta, o servidor pode retornar algumas linhas e, em seguida, encontrar um erro, fazendo com que a consulta seja abortada. Normalmente, libpq descarta quaisquer dessas linhas e relata apenas o erro. Mas, no modo de linha única ou em partes, algumas linhas já podem ter sido devolvidas ao aplicativo. Assim, o aplicativo verá alguns objetos `PGRES_SINGLE_TUPLE` ou `PGRES_TUPLES_CHUNK` `PGresult` seguidos por um objeto `PGRES_FATAL_ERROR`. Para um comportamento transacional adequado, o aplicativo deve ser projetado para descartar ou desfazer o que foi feito com as linhas previamente processadas, se a consulta falhar.