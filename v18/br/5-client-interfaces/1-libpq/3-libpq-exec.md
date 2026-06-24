## 32.3. Funções de Execução de Comando [#](#LIBPQ-EXEC)

* [32.3.1. Funções Principais](libpq-exec.md#LIBPQ-EXEC-MAIN)
* [32.3.2. Recuperação de Informações do Resultado da Consulta](libpq-exec.md#LIBPQ-EXEC-SELECT-INFO)
* [32.3.3. Recuperação de Outras Informações do Resultado](libpq-exec.md#LIBPQ-EXEC-NONSELECT)
* [32.3.4. Echappement de Strings para Inclusão em Comandos SQL](libpq-exec.md#LIBPQ-EXEC-ESCAPE-STRING)

Uma vez que uma conexão com um servidor de banco de dados tenha sido estabelecida com sucesso, as funções descritas aqui são usadas para realizar consultas e comandos SQL.

### 32.3.1. Funções Principais [#](#LIBPQ-EXEC-MAIN)

`PQexec` [#](#LIBPQ-PQEXEC): Envia um comando ao servidor e aguarda o resultado.

```
PGresult *PQexec(PGconn *conn, const char *command);
```

Retorna um ponteiro `PGresult` ou possivelmente um ponteiro nulo. Um ponteiro não nulo geralmente será retornado, exceto em condições de falta de memória ou erros graves, como a incapacidade de enviar o comando ao servidor. A função `PQresultStatus`(libpq-exec.md#LIBPQ-PQRESULTSTATUS) deve ser chamada para verificar o valor de retorno por quaisquer erros (incluindo o valor de um ponteiro nulo, no qual caso, ele retornará `PGRES_FATAL_ERROR`). Use `PQerrorMessage`(libpq-status.md#LIBPQ-PQERRORMESSAGE) para obter mais informações sobre tais erros.

A string de comando pode incluir vários comandos SQL (separados por pontos e vírgulas). Múltiplas consultas enviadas em uma única chamada `PQexec`(libpq-exec.md#LIBPQ-PQEXEC) são processadas em uma única transação, a menos que haja comandos explícitos `BEGIN`/`COMMIT` incluídos na string de consulta para dividi-la em várias transações. (Veja [Seção 54.2.2.1](protocol-flow.md#PROTOCOL-FLOW-MULTI-STATEMENT) para mais detalhes sobre como o servidor lida com strings de consulta múltipla.) No entanto, observe que a estrutura `PGresult` devolvida descreve apenas o resultado do último comando executado a partir da string. Se um dos comandos falhar, o processamento da string para com ele e a estrutura `PGresult` devolvida descreve a condição de erro.

`PQexecParams` [#](#LIBPQ-PQEXECPARAMS): Envia um comando ao servidor e aguarda o resultado, com a capacidade de passar parâmetros separadamente do texto do comando SQL.

```
PGresult *PQexecParams(PGconn *conn, const char *command, int nParams, const Oid *paramTypes, const char * const *paramValues, const int *paramLengths, const int *paramFormats, int resultFormat);
```

[`PQexecParams`](libpq-exec.md#LIBPQ-PQEXECPARAMS) é como [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC), mas oferece funcionalidades adicionais: os valores dos parâmetros podem ser especificados separadamente da string própria do comando e os resultados da consulta podem ser solicitados em formato de texto ou binário.

Os argumentos da função são:

*`conn`* :   O objeto de conexão para enviar o comando.

*`command`* :   A string de comando SQL a ser executada. Se forem utilizados parâmetros, eles são referenciados na string de comando como `$1`, `$2`, etc.

*`nParams`* :   O número de parâmetros fornecidos; é o comprimento dos arrays *`paramTypes[]`*, *`paramValues[]`*, *`paramLengths[]`*, e *`paramFormats[]`*. (Os ponteiros dos arrays podem ser `NULL` quando *`nParams`* é zero.)

*`paramTypes[]`*  Especifica, por OID, os tipos de dados a serem atribuídos aos símbolos dos parâmetros. Se *`paramTypes`* é `NULL`, ou qualquer elemento específico na matriz é zero, o servidor infere um tipo de dados para o símbolo do parâmetro da mesma maneira que faria para uma string literal não tipificada.

*`paramValues[]`* :   Especifica os valores reais dos parâmetros. Um ponteiro nulo neste array significa que o parâmetro correspondente é nulo; caso contrário, o ponteiro aponta para uma string de texto terminada por zero (para o formato de texto) ou dados binários no formato esperado pelo servidor (para o formato binário).

*`paramLengths[]`*  Especifica as longitudes de dados reais dos parâmetros de formato binário.  É ignorado para parâmetros nulos e parâmetros de formato de texto. O ponteiro do array pode ser nulo quando não há parâmetros binários.

*`paramFormats[]`*  Especifica se os parâmetros são de texto (coloque um zero na entrada do array para o parâmetro correspondente) ou binário (coloque um um na entrada do array para o parâmetro correspondente). Se o ponteiro do array for nulo, todos os parâmetros são presumidos serem strings de texto.

Os valores passados em formato binário exigem conhecimento da representação interna esperada pelo backend. Por exemplo, os inteiros devem ser passados na ordem de byte da rede. A passagem de valores de `numeric` exige conhecimento do formato de armazenamento do servidor, conforme implementado em `src/backend/utils/adt/numeric.c::numeric_send()` e `src/backend/utils/adt/numeric.c::numeric_recv()`.

*`resultFormat`* :   Especifique zero para obter resultados em formato de texto, ou um para obter resultados em formato binário. (Atualmente, não há disposição para obter colunas de resultados diferentes em diferentes formatos, embora isso seja possível no protocolo subjacente.)

A principal vantagem do `PQexecParams` sobre (libpq-exec.md#LIBPQ-PQEXECPARAMS) é que os valores dos parâmetros podem ser separados da string de comando, evitando assim a necessidade de citação e escapagem tediosas e propensas a erros.

Ao contrário de `PQexec`](libpq-exec.md#LIBPQ-PQEXEC), [`PQexecParams`](libpq-exec.md#LIBPQ-PQEXECPARAMS) permite no máximo um comando SQL na string dada. (Pode haver pontos e vírgulas nela, mas não mais de um comando não vazio.) Esta é uma limitação do protocolo subjacente, mas tem alguma utilidade como uma defesa extra contra ataques de injeção SQL.

DICA

Especificar tipos de parâmetros via OIDs é tedioso, especialmente se você prefere não vincular valores específicos de OID ao seu programa. No entanto, você pode evitar fazer isso mesmo nos casos em que o servidor por si só não pode determinar o tipo do parâmetro ou escolhe um tipo diferente do que você deseja. No texto do comando SQL, adicione uma cast explícita ao símbolo do parâmetro para mostrar qual tipo de dados você enviará. Por exemplo:

```
SELECT * FROM mytable WHERE x = $1::bigint;
```

Isso obriga o parâmetro `$1` a ser tratado como `bigint`, enquanto por padrão, ele seria atribuído o mesmo tipo que `x`. Forçar a decisão do tipo do parâmetro, dessa forma ou especificando um tipo de OID numérico, é fortemente recomendado ao enviar valores de parâmetro em formato binário, porque o formato binário tem menos redundância que o formato de texto e, portanto, há menos chance de que o servidor detecte um erro de incompatibilidade de tipo para você.

`PQprepare` [#](#LIBPQ-PQPREPARE) :   Envia uma solicitação para criar uma declaração preparada com os parâmetros fornecidos e aguarda a conclusão.

```
PGresult *PQprepare(PGconn *conn, const char *stmtName, const char *query, int nParams, const Oid *paramTypes);
```

`PQprepare` cria uma declaração preparada para execução posterior com (libpq-exec.md#LIBPQ-PQPREPARE). Esse recurso permite que comandos sejam executados repetidamente sem serem analisados e planejados a cada vez; consulte [PREPARAR](sql-prepare.md) para detalhes.

A função cria uma declaração preparada denominada *`stmtName`* a partir da string *`query`*, que deve conter um único comando SQL. *`stmtName`* pode ser `""` para criar uma declaração sem nome, no caso, qualquer declaração sem nome preexistente é automaticamente substituída; caso contrário, é um erro se o nome da declaração já estiver definido na sessão atual. Se forem usados quaisquer parâmetros, eles são referenciados na consulta como *`$1`, *`$2`, etc.* *`nParams`* é o número de parâmetros para os quais os tipos são pré-especificados na matriz *`paramTypes[]`*. (O ponteiro da matriz pode ser *`NULL`* quando *`nParams`* é zero.) *`paramTypes[]`* especifica, por OID, os tipos de dados a serem atribuídos aos símbolos do parâmetro. Se *`paramTypes`* é *`NULL`, ou qualquer elemento particular na matriz é zero, o servidor atribui um tipo de dados ao símbolo do parâmetro da mesma maneira que faria para uma string literal não tipificada. Além disso, a consulta pode usar símbolos de parâmetro com números superiores a *`nParams`*; os tipos de dados serão inferidos para esses símbolos também. (Consulte *[`PQdescribePrepared`](libpq-exec.md#LIBPQ-PQDESCRIBEPREPARED)* para um meio de descobrir quais tipos de dados foram inferidos.)

Assim como em `PQexec`](libpq-exec.md#LIBPQ-PQEXEC), o resultado é normalmente um objeto `PGresult` cujos conteúdos indicam o sucesso ou falha do lado do servidor. Um resultado nulo indica falta de memória ou incapacidade de enviar o comando. Use `PQerrorMessage`](libpq-status.md#LIBPQ-PQERRORMESSAGE) para obter mais informações sobre tais erros.

Declarações preparadas para uso com `PQexecPrepared`(libpq-exec.md#LIBPQ-PQEXECPREPARED) também podem ser criadas executando declarações SQL [PREPARE](sql-prepare.md "PREPARE").

`PQexecPrepared` [#](#LIBPQ-PQEXECPREPARED) :   Envia uma solicitação para executar uma declaração preparada com os parâmetros fornecidos e aguarda o resultado.

```
PGresult *PQexecPrepared(PGconn *conn, const char *stmtName, int nParams, const char * const *paramValues, const int *paramLengths, const int *paramFormats, int resultFormat);
```

`PQexecPrepared` é como (libpq-exec.md#LIBPQ-PQEXECPREPARED), mas o comando a ser executado é especificado ao nomear uma declaração previamente preparada, em vez de fornecer uma string de consulta. Este recurso permite que comandos que serão utilizados repetidamente sejam analisados e planejados apenas uma vez, em vez de cada vez que são executados. A declaração deve ter sido preparada previamente na sessão atual.

Os parâmetros são idênticos a `PQexecParams`(libpq-exec.md#LIBPQ-PQEXECPARAMS), exceto pelo fato de que o nome de uma declaração preparada é dado em vez de uma string de consulta, e o parâmetro *`paramTypes[]`* não está presente (não é necessário, uma vez que os tipos de parâmetros da declaração preparada foram determinados quando ela foi criada).

`PQdescribePrepared` [#](#LIBPQ-PQDESCRIBEPREPARED) :   Envia uma solicitação para obter informações sobre a declaração preparada especificada e aguarda a conclusão.

```
PGresult *PQdescribePrepared(PGconn *conn, const char *stmtName);
```

`PQdescribePrepared`](libpq-exec.md#LIBPQ-PQDESCRIBEPREPARED) permite que uma aplicação obtenha informações sobre uma declaração previamente preparada.

*`stmtName`* pode ser `""` ou `NULL` para referência à declaração não nomeada, caso contrário, deve ser o nome de uma declaração preparada existente. Em caso de sucesso, é retornado um `PGresult` com status `PGRES_COMMAND_OK`. As funções `PQnparams`(libpq-exec.md#LIBPQ-PQNPARAMS) e `PQparamtype`(libpq-exec.md#LIBPQ-PQPARAMTYPE) podem ser aplicadas a este `PGresult` para obter informações sobre os parâmetros da declaração preparada, e as funções `PQnfields`(libpq-exec.md#LIBPQ-PQNFIELDS), `PQfname`(libpq-exec.md#LIBPQ-PQFNAME), `PQftype`(libpq-exec.md#LIBPQ-PQFTYPE), etc. fornecem informações sobre as colunas de resultado (se houver) da declaração.

`PQdescribePortal` [#](#LIBPQ-PQDESCRIBEPORTAL) :   Envia uma solicitação para obter informações sobre o portal especificado e aguarda a conclusão.

```
PGresult *PQdescribePortal(PGconn *conn, const char *portalName);
```

`PQdescribePortal`](libpq-exec.md#LIBPQ-PQDESCRIBEPORTAL) permite que uma aplicação obtenha informações sobre um portal criado anteriormente. (O libpq não fornece acesso direto aos portais, mas você pode usar essa função para inspecionar as propriedades de um cursor criado com um comando SQL `DECLARE CURSOR`.

*`portalName`* pode ser `""` ou `NULL` para referência ao portal sem nome, caso contrário, deve ser o nome de um portal existente. Em caso de sucesso, é retornado um `PGresult` com o status `PGRES_COMMAND_OK`. As funções `PQnfields`(libpq-exec.md#LIBPQ-PQNFIELDS), `PQfname`(libpq-exec.md#LIBPQ-PQFNAME), `PQftype`(libpq-exec.md#LIBPQ-PQFTYPE), etc. podem ser aplicadas ao `PGresult` para obter informações sobre as colunas de resultado (se houver) do portal.

`PQclosePrepared` [#](#LIBPQ-PQCLOSEPREPARED) :   Envia uma solicitação para fechar a declaração preparada especificada e aguarda a conclusão.

```
PGresult *PQclosePrepared(PGconn *conn, const char *stmtName);
```

`PQclosePrepared` permite que uma aplicação feche uma declaração previamente preparada. Fechar uma declaração libera todos os recursos associados no servidor e permite que seu nome seja reutilizado.

*`stmtName`* pode ser `""` ou `NULL` para referenciar a declaração não nomeada. Não há problema se não existir uma declaração com esse nome, nesse caso, a operação é uma operação sem efeito. Se for bem-sucedida, um `PGresult` com status `PGRES_COMMAND_OK` é retornado.

`PQclosePortal` [#](#LIBPQ-PQCLOSEPORTAL) :   Envia uma solicitação para fechar o portal especificado e aguarda a conclusão.

```
PGresult *PQclosePortal(PGconn *conn, const char *portalName);
```

`PQclosePortal`](libpq-exec.md#LIBPQ-PQCLOSEPORTAL) permite que uma aplicação faça o fechamento de um portal criado anteriormente. Fechar um portal libera todos os recursos associados ao servidor e permite que seu nome seja reutilizado. (O libpq não fornece acesso direto aos portais, mas você pode usar essa função para fechar um cursor criado com um comando SQL `DECLARE CURSOR`.)

*`portalName`* pode ser `""` ou `NULL` para referenciar o portal sem nome. Não há problema se não existir nenhum portal com esse nome, nesse caso, a operação é uma operação sem efeito. Se for bem-sucedida, um `PGresult` com status `PGRES_COMMAND_OK` é retornado.

A estrutura `PGresult` encapsula o resultado retornado pelo servidor. Os programadores da aplicação libpq devem ter cuidado para manter a abstração `PGresult`. Use as funções de acesso abaixo para acessar o conteúdo do `PGresult`. Evite referenciar diretamente os campos da estrutura `PGresult`, pois eles estão sujeitos a mudanças no futuro.

`PQresultStatus` [#](#LIBPQ-PQRESULTSTATUS) :  Retorna o status do resultado do comando.

```
ExecStatusType PQresultStatus(const PGresult *res);
```

`PQresultStatus`](libpq-exec.md#LIBPQ-PQRESULTSTATUS) pode retornar um dos seguintes valores:

`PGRES_EMPTY_QUERY` [#](#LIBPQ-PGRES-EMPTY-QUERY) :   A string enviada ao servidor estava vazia.

`PGRES_COMMAND_OK` [#](#LIBPQ-PGRES-COMMAND-OK) :   Conclusão bem-sucedida de um comando que não retorna dados.

`PGRES_TUPLES_OK` [#](#LIBPQ-PGRES-TUPLES-OK) :   Conclusão bem-sucedida de um comando que retorna dados (como `SELECT` ou `SHOW`).

`PGRES_COPY_OUT` [#](#LIBPQ-PGRES-COPY-OUT) :   Transferência de dados de cópia (do servidor) iniciada.

`PGRES_COPY_IN` [#](#LIBPQ-PGRES-COPY-IN) :   A transferência de dados (para o servidor) iniciou.

`PGRES_BAD_RESPONSE` [#](#LIBPQ-PGRES-BAD-RESPONSE) :   A resposta do servidor não foi compreendida.

`PGRES_NONFATAL_ERROR` [#](#LIBPQ-PGRES-NONFATAL-ERROR) :   Houve um erro não fatal (um aviso ou alerta) ocorrido.

`PGRES_FATAL_ERROR` [#](#LIBPQ-PGRES-FATAL-ERROR) :   Houve um erro fatal.

`PGRES_COPY_BOTH` [#](#LIBPQ-PGRES-COPY-BOTH) :   Transferência de dados de entrada/saída (para e do servidor) iniciada. Esta função é atualmente usada apenas para replicação em streaming, portanto, este status não deve ocorrer em aplicações comuns.

`PGRES_SINGLE_TUPLE` [#](#LIBPQ-PGRES-SINGLE-TUPLE) :   O `PGresult` contém um único tupla de resultado do comando atual. Esse status ocorre apenas quando o modo de única linha foi selecionado para a consulta (veja [Seção 32.6](libpq-single-row-mode.md "32.6. Retrieving Query Results in Chunks")).

`PGRES_TUPLES_CHUNK` [#](#LIBPQ-PGRES-TUPLES-CHUNK) :   O `PGresult` contém vários tuplos de resultado do comando atual. Esse status ocorre apenas quando o modo em blocos foi selecionado para a consulta (veja [Seção 32.6](libpq-single-row-mode.md "32.6. Retrieving Query Results in Chunks")). O número de tuplos não excederá o limite passado para [`PQsetChunkedRowsMode`](libpq-single-row-mode.md#LIBPQ-PQSETCHUNKEDROWSMODE)].

`PGRES_PIPELINE_SYNC` [#](#LIBPQ-PGRES-PIPELINE-SYNC) :   O `PGresult` representa um ponto de sincronização no modo de canal, solicitado por `PQpipelineSync` ou `PQsendPipelineSync`, respectivamente. Este status ocorre apenas quando o modo de canal foi selecionado.

`PGRES_PIPELINE_ABORTED` [#](#LIBPQ-PGRES-PIPELINE-ABORTED) :   O `PGresult` representa um pipeline que recebeu um erro do servidor. `PQgetResult` deve ser chamado repetidamente, e cada vez que será retornado este código de status até o final do pipeline atual, momento em que será retornado `PGRES_PIPELINE_SYNC` e o processamento normal pode retomar.

Se o status do resultado for `PGRES_TUPLES_OK`, `PGRES_SINGLE_TUPLE`, ou `PGRES_TUPLES_CHUNK`, então as funções descritas abaixo podem ser usadas para recuperar as linhas retornadas pela consulta. Observe que um comando `SELECT` que, por acaso, retorne zero linhas ainda mostra `PGRES_TUPLES_OK`. `PGRES_COMMAND_OK` é para comandos que nunca podem retornar linhas (`INSERT` ou `UPDATE` sem uma cláusula `RETURNING`, etc.). Uma resposta de `PGRES_EMPTY_QUERY` pode indicar um bug no software do cliente.

Um resultado do status `PGRES_NONFATAL_ERROR` nunca será retornado diretamente pelo `PQexec`(libpq-exec.md#LIBPQ-PQEXEC) ou outras funções de execução de consulta; os resultados desse tipo são, em vez disso, passados para o processador de notificações (consulte [Seção 32.13](libpq-notice-processing.md)).

`PQresStatus` [#](#LIBPQ-PQRESSTATUS): Converte o tipo enumerado retornado por [`PQresultStatus`](libpq-exec.md#LIBPQ-PQRESULTSTATUS) em uma constante de string que descreve o código de status. O chamador não deve liberar o resultado.

```
char *PQresStatus(ExecStatusType status);
```

`PQresultErrorMessage` [#](#LIBPQ-PQRESULTERRORMESSAGE): Retorna a mensagem de erro associada ao comando, ou uma string vazia, se não houver erro.

```
char *PQresultErrorMessage(const PGresult *res);
```

Se houver um erro, a string devolvida incluirá uma nova linha final. O chamador não deve liberar o resultado diretamente. Ele será liberado quando o controle associado ao `PGresult` for passado para `PQclear`(libpq-exec.md#LIBPQ-PQCLEAR).

Imediatamente após uma chamada de `PQexec`(libpq-exec.md#LIBPQ-PQEXEC) ou [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT), [`PQerrorMessage`](libpq-status.md#LIBPQ-PQERRORMESSAGE) (na conexão) retornará a mesma string que [`PQresultErrorMessage`](libpq-exec.md#LIBPQ-PQRESULTERRORMESSAGE) (no resultado). No entanto, um `PGresult` retém sua mensagem de erro até ser destruído, enquanto a mensagem de erro da conexão mudará quando operações subsequentes forem realizadas. Use [`PQresultErrorMessage`](libpq-exec.md#LIBPQ-PQRESULTERRORMESSAGE) quando você deseja conhecer o status associado a um `PGresult` específico; use [`PQerrorMessage`](libpq-status.md#LIBPQ-PQERRORMESSAGE) quando você deseja conhecer o status da última operação na conexão.

`PQresultVerboseErrorMessage` [#](#LIBPQ-PQRESULTVERBOSEERRORMESSAGE): Retorna uma versão reformatada da mensagem de erro associada ao objeto `PGresult`.

```
char *PQresultVerboseErrorMessage(const PGresult *res, PGVerbosity verbosity, PGContextVisibility show_context);
```

Em algumas situações, um cliente pode desejar obter uma versão mais detalhada de um erro reportado anteriormente. [`PQresultVerboseErrorMessage`](libpq-exec.md#LIBPQ-PQRESULTVERBOSEERRORMESSAGE) aborda essa necessidade calculando a mensagem que teria sido produzida [`PQresultErrorMessage`](libpq-exec.md#LIBPQ-PQRESULTERRORMESSAGE) se as configurações de verbosidade especificadas tivessem sido efetivas para a conexão quando o `PGresult` foi gerado. Se `PGresult` não é um resultado de erro, "PGresult não é um resultado de erro" é relatado em vez disso. A string devolvida inclui uma nova linha final.

Ao contrário da maioria das outras funções para extrair dados da `PGresult`, o resultado desta função é uma string recém-alocada. O chamador deve liberá-la usando `PQfreemem()` quando a string não for mais necessária.

Um retorno NULL é possível se houver memória insuficiente.

`PQresultErrorField` [#](#LIBPQ-PQRESULTERRORFIELD): Retorna um campo individual de um relatório de erro.

```
char *PQresultErrorField(const PGresult *res, int fieldcode);
```

*`fieldcode`* é um identificador de campo de erro; veja os símbolos listados abaixo. `NULL` é retornado se o `PGresult` não for um resultado de erro ou aviso, ou não inclua o campo especificado. Os valores dos campos normalmente não incluirão uma nova linha final. O chamador não deve liberar o resultado diretamente. Ele será liberado quando o handle associado a `PGresult` for passado para `PQclear`(libpq-exec.md#LIBPQ-PQCLEAR).

Os seguintes códigos de campo estão disponíveis:

`PG_DIAG_SEVERITY` [#](#LIBPQ-PG-DIAG-SEVERITY) :   A gravidade; os conteúdos do campo são `ERROR`, `FATAL`, ou `PANIC` (em uma mensagem de erro), ou `WARNING`, `NOTICE`, `DEBUG`, `INFO`, ou `LOG` (em uma mensagem de aviso), ou uma tradução localizada de uma dessas. Sempre presente.

`PG_DIAG_SEVERITY_NONLOCALIZED` [#](#LIBPQ-PG-DIAG-SEVERITY-NONLOCALIZED) :   A gravidade; os conteúdos do campo são `ERROR`, `FATAL`, ou `PANIC` (em uma mensagem de erro), ou `WARNING`, `NOTICE`, `DEBUG`, `INFO`, ou `LOG` (em uma mensagem de aviso). . Isso é idêntico ao campo `PG_DIAG_SEVERITY`, exceto que os conteúdos nunca são localizados. Isso está presente apenas em relatórios gerados por versões do PostgreSQL 9.6 e posteriores.

`PG_DIAG_SQLSTATE` [#](#LIBPQ-PG-DIAG-SQLSTATE) :   O código SQLSTATE para o erro. O código SQLSTATE identifica o tipo de erro que ocorreu; ele pode ser usado por aplicativos de interface gráfica para realizar operações específicas (como tratamento de erros) em resposta a um erro específico do banco de dados. Para uma lista dos códigos SQLSTATE possíveis, consulte o [Apêndice A](errcodes-appendix.md "Appendix A. PostgreSQL Error Codes"). Este campo não é traduzível e está sempre presente.

`PG_DIAG_MESSAGE_PRIMARY` [#](#LIBPQ-PG-DIAG-MESSAGE-PRIMARY) :   A mensagem de erro primária legível pelo ser humano (tipicamente uma linha). Sempre presente.

`PG_DIAG_MESSAGE_DETAIL` [#](#LIBPQ-PG-DIAG-MESSAGE-DETAIL) :   Detalhe: uma mensagem de erro secundária opcional que traz mais detalhes sobre o problema. Pode ocupar várias linhas.

`PG_DIAG_MESSAGE_HINT` [#](#LIBPQ-PG-DIAG-MESSAGE-HINT) :  Sugestão opcional sobre o que fazer com o problema. Este é destinado a diferir do detalhe, pois oferece conselhos (potencialmente inadequados) em vez de fatos concretos. Pode ocupar várias linhas.

`PG_DIAG_STATEMENT_POSITION` [#](#LIBPQ-PG-DIAG-STATEMENT-POSITION) :   Uma string que contém um número decimal inteiro indicando a posição do cursor de erro como um índice na string original da declaração. O primeiro caractere tem índice 1, e as posições são medidas em caracteres, não em bytes.

`PG_DIAG_INTERNAL_POSITION` [#](#LIBPQ-PG-DIAG-INTERNAL-POSITION) :   Isso é definido da mesma forma que o campo `PG_DIAG_STATEMENT_POSITION`, mas é usado quando a posição do cursor se refere a um comando gerado internamente, em vez do que foi enviado pelo cliente. O campo `PG_DIAG_INTERNAL_QUERY` sempre aparecerá quando este campo aparecer.

`PG_DIAG_INTERNAL_QUERY` [#](#LIBPQ-PG-DIAG-INTERNAL-QUERY) :   O texto de um comando gerado internamente que falhou. Isso pode ser, por exemplo, uma consulta SQL emitida por uma função PL/pgSQL.

`PG_DIAG_CONTEXT` [#](#LIBPQ-PG-DIAG-CONTEXT) :   Uma indicação do contexto em que o erro ocorreu. Atualmente, isso inclui um histórico de pilha de chamadas de funções de linguagem procedural ativa e consultas geradas internamente. O rastreamento é uma entrada por linha, a mais recente em primeiro lugar.

`PG_DIAG_SCHEMA_NAME` [#](#LIBPQ-PG-DIAG-SCHEMA-NAME) :   Se o erro estiver associado a um objeto específico do banco de dados, o nome do esquema que contém esse objeto, se houver.

`PG_DIAG_TABLE_NAME` [#](#LIBPQ-PG-DIAG-TABLE-NAME) :   Se o erro estiver associado a uma tabela específica, o nome da tabela. (Consulte o campo nome do esquema para o nome do esquema da tabela.)

`PG_DIAG_COLUMN_NAME` [#](#LIBPQ-PG-DIAG-COLUMN-NAME) :   Se o erro estiver associado a uma coluna específica da tabela, o nome da coluna. (Consulte os campos de nome do esquema e da tabela para identificar a tabela.)

`PG_DIAG_DATATYPE_NAME` [#](#LIBPQ-PG-DIAG-DATATYPE-NAME) :   Se o erro estiver associado a um tipo de dado específico, o nome do tipo de dado. (Consulte o campo nome do esquema para o nome do esquema do tipo de dado.)

`PG_DIAG_CONSTRAINT_NAME` [#](#LIBPQ-PG-DIAG-CONSTRAINT-NAME) :   Se o erro estiver associado a uma restrição específica, o nome da restrição. Consulte os campos listados acima para a tabela ou domínio associado. (Para este propósito, os índices são tratados como restrições, mesmo que não tenham sido criados com sintaxe de restrição.)

`PG_DIAG_SOURCE_FILE` [#](#LIBPQ-PG-DIAG-SOURCE-FILE) :   O nome do arquivo da localização do código-fonte onde o erro foi relatado.

`PG_DIAG_SOURCE_LINE` [#](#LIBPQ-PG-DIAG-SOURCE-LINE) :   O número da linha da localização do código fonte onde o erro foi relatado.

`PG_DIAG_SOURCE_FUNCTION` [#](#LIBPQ-PG-DIAG-SOURCE-FUNCTION) :   O nome da função de código-fonte que reporta o erro.

Nota

Os campos para o nome do esquema, nome da tabela, nome da coluna, nome do tipo de dados e nome da restrição são fornecidos apenas para um número limitado de tipos de erro; veja [Apêndice A](errcodes-appendix.md). Não assuma que a presença de qualquer um desses campos garanta a presença de outro campo. As fontes de erro principais observam as inter-relações mencionadas acima, mas as funções definidas pelo usuário podem usar esses campos de outras maneiras. Da mesma forma, não assuma que esses campos denotem objetos contemporâneos no banco de dados atual.

O cliente é responsável por formatar as informações exibidas para atender às suas necessidades; em particular, deve quebrar linhas longas conforme necessário. Os caracteres de nova linha que aparecem nos campos de mensagem de erro devem ser tratados como quebra de parágrafo, e não como quebra de linha.

Os erros gerados internamente pelo libpq terão gravidade e mensagem principal, mas, normalmente, não terão outros campos.

Observe que os campos de erro estão disponíveis apenas nos objetos `PGresult`, não nos objetos `PGconn`; não há função `PQerrorField`.

`PQclear` [#](#LIBPQ-PQCLEAR): Libera o armazenamento associado a um `PGresult`. Todo resultado de comando deve ser liberado via [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) quando não for mais necessário.

```
void PQclear(PGresult *res);
```

Se o argumento for um ponteiro `NULL`, nenhuma operação é realizada.

Você pode manter um objeto `PGresult` por tanto tempo quanto precisar; ele não desaparece quando você emite um novo comando, nem mesmo se você fechar a conexão. Para se livrar dele, você deve chamar `PQclear`(libpq-exec.md#LIBPQ-PQCLEAR). Se você não fizer isso, isso resultará em vazamentos de memória em sua aplicação.

### 32.3.2. Recuperação de informações sobre o resultado da consulta [#](#LIBPQ-EXEC-SELECT-INFO)

Essas funções são usadas para extrair informações de um objeto `PGresult` que representa um resultado de consulta bem-sucedida (ou seja, aquele que tem status `PGRES_TUPLES_OK`, `PGRES_SINGLE_TUPLE` ou `PGRES_TUPLES_CHUNK`). Elas também podem ser usadas para extrair informações de uma operação de Descrição bem-sucedida: o resultado de uma Descrição tem todas as mesmas informações de coluna que a execução real da consulta forneceria, mas tem zero linhas. Para objetos com outros valores de status, essas funções agirão como se o resultado tivesse zero linhas e zero colunas.

`PQntuples` [#](#LIBPQ-PQNTUPLES): Retorna o número de linhas (tuplas) no resultado da consulta.

(Observe que os objetos `PGresult` são limitados a não mais do que `INT_MAX` linhas, portanto, um resultado `int` é suficiente.)

```
int PQntuples(const PGresult *res);
```

`PQnfields` [#](#LIBPQ-PQNFIELDS): Retorna o número de colunas (campos) em cada linha do resultado da consulta.

```
int PQnfields(const PGresult *res);
```

`PQfname` [#](#LIBPQ-PQFNAME): Retorna o nome da coluna associado ao número de coluna fornecido. Os números de coluna começam em 0. O chamador não deve liberar o resultado diretamente. Ele será liberado quando o controle associado `PGresult` for passado para [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR).

```
char *PQfname(const PGresult *res, int column_number);
```

`NULL` é retornado se o número da coluna estiver fora do intervalo.

`PQfnumber` [#](#LIBPQ-PQFNUMBER): Retorna o número da coluna associado ao nome da coluna fornecido.

```
int PQfnumber(const PGresult *res, const char *column_name);
```

-1 é retornado se o nome fornecido não corresponder a nenhuma coluna.

O nome dado é tratado como um identificador em um comando SQL, ou seja, é minúsculo, a menos que seja citado em duplicado. Por exemplo, o resultado de uma consulta gerado a partir do comando SQL:

```
SELECT 1 AS FOO, 2 AS "BAR";
```

nós teríamos os resultados:

```
PQfname(res, 0)              foo PQfname(res, 1)              BAR PQfnumber(res, "FOO")        0 PQfnumber(res, "foo")        0 PQfnumber(res, "BAR")        -1 PQfnumber(res, "\"BAR\"")    1
```

`PQftable` [#](#LIBPQ-PQFTABLE) :   Retorna o OID da tabela a partir da qual a coluna fornecida foi obtida. Os números de coluna começam em 0.

```
Oid PQftable(const PGresult *res, int column_number);
```

`InvalidOid` é retornado se o número da coluna estiver fora do intervalo, ou se a coluna especificada não for uma referência simples a uma coluna de tabela. Você pode consultar a tabela do sistema `pg_class` para determinar exatamente qual tabela está sendo referenciada.

O tipo `Oid` e a constante `InvalidOid` serão definidos quando você incluir o arquivo de cabeçalho libpq. Ambos serão algum tipo de inteiro.

`PQftablecol` [#](#LIBPQ-PQFTABLECOL): Retorna o número da coluna (dentro de sua tabela) da coluna que compõe a coluna do resultado da consulta especificada. Os números de colunas de resultado de consulta começam em 0, mas as colunas da tabela têm números não nulos.

```
int PQftablecol(const PGresult *res, int column_number);
```

Zero é retornado se o número da coluna estiver fora do intervalo, ou se a coluna especificada não for uma referência simples a uma coluna de tabela.

`PQfformat` [#](#LIBPQ-PQFFORMAT): Retorna o código de formato que indica o formato da coluna fornecida. Os números de coluna começam em 0.

```
int PQfformat(const PGresult *res, int column_number);
```

O código de formato zero indica representação de dados textuais, enquanto o código de formato um indica representação binária. (Outros códigos são reservados para definição futura.)

`PQftype` [#](#LIBPQ-PQFTYPE): Retorna o tipo de dados associado ao número da coluna fornecido. O número inteiro retornado é o número interno OID do tipo. Os números de coluna começam em 0.

```
Oid PQftype(const PGresult *res, int column_number);
```

Você pode consultar a tabela do sistema `pg_type` para obter os nomes e as propriedades dos vários tipos de dados. Os OIDs dos tipos de dados embutidos são definidos no arquivo `catalog/pg_type_d.h` no diretório `include` da instalação do PostgreSQL.

`PQfmod` [#](#LIBPQ-PQFMOD): Retorna o modificador de tipo da coluna associada ao número de coluna dado. Os números de coluna começam em 0.

```
int PQfmod(const PGresult *res, int column_number);
```

A interpretação dos valores dos modificadores é específica do tipo; eles geralmente indicam limites de precisão ou tamanho. O valor -1 é usado para indicar "nenhuma informação disponível". A maioria dos tipos de dados não usa modificadores, no caso, o valor é sempre -1.

`PQfsize` [#](#LIBPQ-PQFSIZE): Retorna o tamanho em bytes da coluna associada ao número de coluna dado. Os números de coluna começam em 0.

```
int PQfsize(const PGresult *res, int column_number);
```

`PQfsize`](libpq-exec.md#LIBPQ-PQFSIZE) retorna o espaço alocado para esta coluna em uma linha do banco de dados, ou seja, o tamanho da representação interna do servidor do tipo de dados. (Consequentemente, não é muito útil para os clientes.) Um valor negativo indica que o tipo de dados é de comprimento variável.

`PQbinaryTuples` [#](#LIBPQ-PQBINARYTUPLES): Retorna 1 se o `PGresult` contiver dados binários e 0 se contiver dados de texto.

```
int PQbinaryTuples(const PGresult *res);
```

Essa função é desaconselhada (exceto quando usada em conexão com `COPY`), porque é possível que um único `PGresult` contenha dados de texto em algumas colunas e dados binários em outras. `PQfformat` é preferido. `PQbinaryTuples` retorna 1 apenas se todas as colunas do resultado forem binárias (formato 1).

`PQgetvalue` [#](#LIBPQ-PQGETVALUE): Retorna um único valor de campo de uma `PGresult`. Os números de linha e coluna começam em 0. O chamador não deve liberar o resultado diretamente. Ele será liberado quando o controle associado ao `PGresult` for passado para [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR).

```
char *PQgetvalue(const PGresult *res, int row_number, int column_number);
```

Para dados em formato de texto, o valor retornado por `PQgetvalue`(libpq-exec.md#LIBPQ-PQGETVALUE) é uma representação de cadeia de caracteres terminada por nulo da representação do valor do campo. Para dados em formato binário, o valor está na representação binária determinada pelas funções `typsend` e `typreceive` do tipo de dados. (O valor é de fato seguido por um byte zero neste caso também, mas isso não é comum, uma vez que o valor provavelmente conterá nulos embutidos.)

Uma string vazia é devolvida se o valor do campo for nulo. Consulte `PQgetisnull` para distinguir valores nulos de valores de string vazia.

O ponteiro retornado por `PQgetvalue`(libpq-exec.md#LIBPQ-PQGETVALUE) aponta para armazenamento que faz parte da estrutura `PGresult`. Não se deve modificar os dados a que ele aponta, e é necessário copiar explicitamente os dados para outro armazenamento se eles devem ser usados após o período de vida útil da própria estrutura `PGresult`.

`PQgetisnull` [#](#LIBPQ-PQGETISNULL): Testa um campo em busca de um valor nulo. Os números de linha e coluna começam em 0.

```
int PQgetisnull(const PGresult *res, int row_number, int column_number);
```

Essa função retorna 1 se o campo for nulo e 0 se ele conter um valor não nulo. (Observe que `PQgetvalue`(libpq-exec.md#LIBPQ-PQGETVALUE) retornará uma string vazia, não um ponteiro nulo, para um campo nulo.)

`PQgetlength` [#](#LIBPQ-PQGETLENGTH): Retorna o comprimento real de um valor de campo em bytes. Os números de linha e coluna começam em 0.

```
int PQgetlength(const PGresult *res, int row_number, int column_number);
```

Este é o comprimento real do valor de dados específico, ou seja, o tamanho do objeto apontado por `PQgetvalue`(libpq-exec.md#LIBPQ-PQGETVALUE). Para o formato de dados de texto, este é o mesmo que `strlen()`. Para o formato binário, esta é informação essencial. Note que não se deve *não* confiar em [`PQfsize`](libpq-exec.md#LIBPQ-PQFSIZE) para obter o comprimento real dos dados.

`PQnparams` [#](#LIBPQ-PQNPARAMS): Retorna o número de parâmetros de uma declaração preparada.

```
int PQnparams(const PGresult *res);
```

Essa função só é útil ao inspecionar o resultado de `PQdescribePrepared`(libpq-exec.md#LIBPQ-PQDESCRIBEPREPARED). Para outros tipos de resultados, ela retornará zero.

`PQparamtype` [#](#LIBPQ-PQPARAMTYPE): Retorna o tipo de dados do parâmetro da declaração indicada. Os números dos parâmetros começam em 0.

```
Oid PQparamtype(const PGresult *res, int param_number);
```

Essa função só é útil ao inspecionar o resultado de `PQdescribePrepared`(libpq-exec.md#LIBPQ-PQDESCRIBEPREPARED). Para outros tipos de resultados, ela retornará zero.

`PQprint` [#](#LIBPQ-PQPRINT) :   Imprime todas as linhas e, opcionalmente, os nomes das colunas para a corrente de saída especificada.

```
void PQprint(FILE *fout,      /* output stream */ const PGresult *res, const PQprintOpt *po); typedef struct { pqbool  header;      /* print output field headings and row count */ pqbool  align;       /* fill align the fields */ pqbool  standard;    /* old brain dead format */ pqbool  html3;       /* output HTML tables */ pqbool  expanded;    /* expand tables */ pqbool  pager;       /* use pager for output if needed */ char    *fieldSep;   /* field separator */ char    *tableOpt;   /* attributes for HTML table element */ char    *caption;    /* HTML table caption */ char    **fieldName; /* null-terminated array of replacement field names */ } PQprintOpt;
```

Essa função era anteriormente usada pelo psql para imprimir os resultados das consultas, mas isso não é mais o caso. Note que ela assume que todos os dados estão em formato de texto.

### 32.3.3. Recuperação de outras informações sobre resultados [#](#LIBPQ-EXEC-NONSELECT)

Essas funções são usadas para extrair outras informações dos objetos `PGresult`.

`PQcmdStatus` [#](#LIBPQ-PQCMDSTATUS): Retorna a tag de status do comando a partir do comando SQL que gerou o `PGresult`.

```
char *PQcmdStatus(PGresult *res);
```

Geralmente, isso é apenas o nome do comando, mas pode incluir dados adicionais, como o número de linhas processadas. O chamador não deve liberar o resultado diretamente. Ele será liberado quando o controle associado ao `PGresult` for passado para `PQclear`(libpq-exec.md#LIBPQ-PQCLEAR).

`PQcmdTuples` [#](#LIBPQ-PQCMDTUPLES) :   Retorna o número de linhas afetadas pelo comando SQL.

```
char *PQcmdTuples(PGresult *res);
```

Essa função retorna uma string contendo o número de linhas afetadas pelo comando SQL que gerou o `PGresult`. Essa função só pode ser usada após a execução de um comando do tipo `SELECT`, `CREATE TABLE AS`, `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `MOVE`, `FETCH`, ou `COPY`. Ou de um `EXECUTE` de uma consulta preparada que contenha um comando do tipo `INSERT`, `UPDATE`, `DELETE`, ou `MERGE`. Se o comando que gerou o `PGresult` foi algo diferente, [`PQcmdTuples`](libpq-exec.md#LIBPQ-PQCMDTUPLES) retorna uma string vazia. O chamador não deve liberar o valor de retorno diretamente. Ele será liberado quando o handle associado ao `PGresult` for passado para [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR).

`PQoidValue` [#](#LIBPQ-PQOIDVALUE): Retorna o OID da linha inserida, se o comando SQL foi um `INSERT` que inseriu exatamente uma linha em uma tabela que possui OIDs, ou o `EXECUTE` de uma consulta preparada contendo uma declaração adequada `INSERT`. Caso contrário, esta função retorna `InvalidOid`. Esta função também retorna `InvalidOid` se a tabela afetada pela declaração `INSERT` não contiver OIDs.

```
Oid PQoidValue(const PGresult *res);
```

`PQoidStatus` [#](#LIBPQ-PQOIDSTATUS): Essa função é descontinuada em favor de [`PQoidValue`](libpq-exec.md#LIBPQ-PQOIDVALUE) e não é segura para uso em threads. Ela retorna uma string com o OID da linha inserida, enquanto [`PQoidValue`](libpq-exec.md#LIBPQ-PQOIDVALUE) retorna o valor do OID.

```
char *PQoidStatus(const PGresult *res);
```

### 32.3.4. Echappement de strings para inclusão em comandos SQL [#](#LIBPQ-EXEC-ESCAPE-STRING)

`PQescapeLiteral` [#](#LIBPQ-PQESCAPELITERAL): ``` char *PQescapeLiteral(PGconn *conn, const char *str, size_t length);
```

`PQescapeLiteral` (libpq-exec.md#LIBPQ-PQESCAPELITERAL) escapa uma string para uso dentro de um comando SQL. Isso é útil ao inserir valores de dados como constantes literais em comandos SQL. Certos caracteres (como aspas e barras invertidas) devem ser escamados para evitar que sejam interpretados especialmente pelo analisador SQL. `PQescapeLiteral` (libpq-exec.md#LIBPQ-PQESCAPELITERAL) realiza essa operação.

`PQescapeLiteral` retorna uma versão escapada do parâmetro *`str`* na memória alocada com `malloc()`. Essa memória deve ser liberada usando `PQfreemem()` quando o resultado não for mais necessário. Um byte nulo final não é necessário e não deve ser contado em *`length`*. (Se um byte nulo final for encontrado antes de os bytes *`length`* serem processados, [`PQescapeLiteral`](libpq-exec.md#LIBPQ-PQESCAPELITERAL) para o zero; o comportamento é, portanto, semelhante a `strncpy`.]) A string de retorno tem todos os caracteres especiais substituídos para que possam ser processados adequadamente pelo analisador de literal de string do PostgreSQL. Um byte nulo final também é adicionado. As aspas que devem envolver os literais de string do PostgreSQL são incluídas na string de resultado.

Em caso de erro, `PQescapeLiteral`(libpq-exec.md#LIBPQ-PQESCAPELITERAL) retorna `NULL` e uma mensagem adequada é armazenada no objeto *`conn`*.

DICA

É especialmente importante fazer a devida escapamento ao manipular strings que foram recebidas de uma fonte não confiável. Caso contrário, há um risco de segurança: você é vulnerável a ataques de "injeção SQL", nos quais comandos SQL indesejados são alimentados em seu banco de dados.

Observe que não é necessário nem correto realizar escapamento quando um valor de dados é passado como um parâmetro separado em `PQexecParams` (libpq-exec.md#LIBPQ-PQEXECPARAMS) ou em suas rotinas irmãs.

`PQescapeIdentifier` [#](#LIBPQ-PQESCAPEIDENTIFIER): ``` char *PQescapeIdentifier(PGconn *conn, const char *str, size_t length);
```

`PQescapeIdentifier` (libpq-exec.md#LIBPQ-PQESCAPEIDENTIFIER) escapa uma string para uso como um identificador SQL, como nome de tabela, coluna ou função. Isso é útil quando um identificador fornecido pelo usuário pode conter caracteres especiais que, de outra forma, não seriam interpretados como parte do identificador pelo analisador SQL, ou quando o identificador pode conter caracteres em maiúsculas cuja grafia deve ser preservada.

`PQescapeIdentifier` retém uma versão do parâmetro *`str`* escapado como um identificador SQL em memória alocada com `malloc()`. Essa memória deve ser liberada usando `PQfreemem()` quando o resultado não for mais necessário. Um byte final nulo não é necessário e não deve ser contado em *`length`*. (Se um byte nulo final for encontrado antes de os bytes *`length`* serem processados, [`PQescapeIdentifier`](libpq-exec.md#LIBPQ-PQESCAPEIDENTIFIER) para o zero; o comportamento é, portanto, semelhante a `strncpy`.). A string de retorno tem todos os caracteres especiais substituídos para que seja processada corretamente como um identificador SQL. Um byte nulo final também é adicionado. A string de retorno também será cercada por aspas duplas.

Em caso de erro, `PQescapeIdentifier`(libpq-exec.md#LIBPQ-PQESCAPEIDENTIFIER) retorna `NULL` e uma mensagem adequada é armazenada no objeto *`conn`*.

DICA

Assim como as cadeias de caracteres, para evitar ataques de injeção SQL, os identificadores SQL devem ser escamados quando recebidos de uma fonte não confiável.

`PQescapeStringConn` [#](#LIBPQ-PQESCAPESTRINGCONN): ``` size_t PQescapeStringConn(PGconn *conn, char *to, const char *from, size_t length, int *error);
```

[`PQescapeStringConn`](libpq-exec.md#LIBPQ-PQESCAPESTRINGCONN) escapa de caracteres de string, assim como [`PQescapeLiteral`](libpq-exec.md#LIBPQ-PQESCAPELITERAL). Ao contrário de [`PQescapeLiteral`](libpq-exec.md#LIBPQ-PQESCAPELITERAL), o chamador é responsável por fornecer um buffer de tamanho apropriado. Além disso, [`PQescapeStringConn`](libpq-exec.md#LIBPQ-PQESCAPESTRINGCONN) não gera as aspas simples que devem envolver as literais de string do PostgreSQL; elas devem ser fornecidas no comando SQL no qual o resultado é inserido. O parâmetro *`from`* aponta para o primeiro caractere da string que deve ser escamado, e o parâmetro *`length`* dá o número de bytes nesta string. Um byte final não é necessário e não deve ser contado em *`length`*. (Se um byte final for encontrado antes de os bytes *`length`* serem processados, [`PQescapeStringConn`](libpq-exec.md#LIBPQ-PQESCAPESTRINGCONN) para no zero; o comportamento é, portanto, semelhante a `strncpy`.)*`to`* deve apontar para um buffer que seja capaz de conter pelo menos um byte a mais do que o dobro do valor de *`length`*, caso contrário, o comportamento é indefinido. O comportamento também é indefinido se as strings *`to`* e *`from`* se sobrepuserem.

Se o parâmetro *`error`* não for `NULL`, então `*error` é definido como zero em caso de sucesso, não nulo em caso de erro. Atualmente, as únicas condições de erro possíveis envolvem codificação multibyte inválida na string de origem. A string de saída ainda é gerada em caso de erro, mas espera-se que o servidor a rejeite como malformada. Em caso de erro, uma mensagem adequada é armazenada no objeto *`conn`*, independentemente de *`error`* ser `NULL` ou

`PQescapeStringConn`](libpq-exec.md#LIBPQ-PQESCAPESTRINGCONN) retorna o número de bytes escritos em *`to`*, excluindo o byte zero final.

`PQescapeString` [#](#LIBPQ-PQESCAPESTRING): [`PQescapeString`](libpq-exec.md#LIBPQ-PQESCAPESTRING) é uma versão mais antiga, descontinuada, de [`PQescapeStringConn`](libpq-exec.md#LIBPQ-PQESCAPESTRINGCONN).

```
```

A única diferença de `PQescapeStringConn` é que (libpq-exec.md#LIBPQ-PQESCAPESTRINGCONN) não aceita os parâmetros `PQescapeString` ou *`error`*. Por isso, não pode ajustar seu comportamento de acordo com as propriedades da conexão (como codificação de caracteres) e, portanto, *pode gerar resultados errados*. Além disso, não tem como relatar condições de erro.

`PQescapeString`](libpq-exec.md#LIBPQ-PQESCAPESTRING) pode ser usado com segurança em programas de clientes que trabalham com apenas uma conexão PostgreSQL de cada vez (neste caso, ele pode descobrir o que precisa saber “nos bastidores”). Em outros contextos, é um perigo de segurança e deve ser evitado em favor de `PQescapeStringConn`](libpq-exec.md#LIBPQ-PQESCAPESTRINGCONN).

`PQescapeByteaConn` [#](#LIBPQ-PQESCAPEBYTEACONN): Escapes dados binários para uso dentro de um comando SQL com o tipo `bytea`. Assim como em [`PQescapeStringConn`](libpq-exec.md#LIBPQ-PQESCAPESTRINGCONN), isso é usado apenas ao inserir dados diretamente em uma string de comando SQL.

```
```

Certos valores de byte devem ser escapados quando utilizados como parte de um literal `bytea` em uma declaração SQL. (libpq-exec.md#LIBPQ-PQESCAPEBYTEACONN) escapa bytes usando codificação hexadecimal ou escapamento com barra invertida. Consulte [Seção 8.4](datatype-binary.md) para mais informações.

O parâmetro *`from`* aponta para o primeiro byte da string que deve ser escapado, e o
*`from_length`* parâmetro dá o número de bytes nesta string binária. (Um byte zero final não é necessário nem contado.) O parâmetro *`to_length`* aponta para uma variável que guardará o comprimento da string escapada resultante. Este comprimento da string resultante inclui o byte zero final do resultado.

`PQescapeByteaConn`(libpq-exec.md#LIBPQ-PQESCAPEBYTEACONN) retorna uma versão escapada da
*`from`* string binária do parâmetro na memória
alocada com `malloc()`. Essa memória deve ser liberada usando
`PQfreemem()` quando o resultado não for mais necessário. A
string de retorno tem todos os caracteres especiais substituídos para que possam
ser processados corretamente pelo parser de literal de string do PostgreSQL, e pela
função de entrada `bytea`. Um byte nulo final também é adicionado. As aspas que devem
circundar os literais de string de PostgreSQL não fazem parte da string de resultado.

Em caso de erro, um ponteiro nu é retornado e uma mensagem de erro adequada é armazenada no objeto *`conn`*. Atualmente, o único erro possível é a memória insuficiente para a string de resultado.

`PQescapeBytea` [#](#LIBPQ-PQESCAPEBYTEA) é uma versão mais antiga, descontinuada, de
[`PQescapeBytea`](libpq-exec.md#LIBPQ-PQESCAPEBYTEA).
`PQescapeByteaConn`[[]] é uma versão mais antiga, descontinuada, de
[(libpq-exec.md#LIBPQ-PQESCAPEBYTEACONN).

```
    unsigned char *PQescapeBytea(const unsigned char *from, size_t from_length, size_t *to_length);
```

A única diferença de `PQescapeByteaConn` é que
(libpq-exec.md#LIBPQ-PQESCAPEBYTEACONN) não aceita um parâmetro `PGconn`
`PQescapeBytea` não aceita um parâmetro (libpq-exec.md#LIBPQ-PQESCAPEBYTEA)
. Por isso, `PQescapeBytea` só pode ser usado com segurança em programas cliente que usam uma única conexão PostgreSQL de cada vez (neste caso, pode descobrir o que precisa saber "nos bastidores"). Pode *dar resultados errados* se usado em programas que usam múltiplas conexões de banco de dados (use `PQescapeByteaConn` em tais casos).

`PQunescapeBytea` [#](#LIBPQ-PQUNESCAPEBYTEA): Converte uma representação de string de dados binários em dados binários
— o inverso de [`PQescapeBytea`](libpq-exec.md#LIBPQ-PQESCAPEBYTEA)]. Isso é necessário ao recuperar dados `bytea` em formato de texto, mas não quando recuperá-los em formato binário.

```
    unsigned char *PQunescapeBytea(const unsigned char *from, size_t *to_length);
```

O parâmetro *`from`* aponta para uma string,
tal como pode ser retornada por [`PQgetvalue`](libpq-exec.md#LIBPQ-PQGETVALUE), quando aplicada
a uma coluna `bytea`. [`PQunescapeBytea`](libpq-exec.md#LIBPQ-PQUNESCAPEBYTEA)
converte essa representação de string em sua representação binária.
Ele retorna um ponteiro para um buffer alocado com
`malloc()`, ou `NULL` em caso de erro, e coloca o tamanho
do buffer em *`to_length`*. O resultado deve ser
libertado usando [`PQfreemem`](libpq-misc.md#LIBPQ-PQFREEMEM) quando não for mais necessário.

Essa conversão não é exatamente o inverso de
`PQescapeBytea`(libpq-exec.md#LIBPQ-PQESCAPEBYTEA), porque a string não é esperada
`PQgetvalue`(libpq-exec.md#LIBPQ-PQGETVALUE). Isso significa, em particular, que não há necessidade de considerar a citação de strings,
e, portanto, não há necessidade de um parâmetro `PGconn`.