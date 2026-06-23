## 47.6. Plugins de decodificação lógica [#](#LOGICALDECODING-OUTPUT-PLUGIN)

* [47.6.1. Função de Inicialização](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-INIT)
* [47.6.2. Capacidades](logicaldecoding-output-plugin.md#LOGICALDECODING-CAPABILITIES)
* [47.6.3. Modos de Saída](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-MODE)
* [47.6.4. Chamadas de Retorno de Plugin de Saída](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-PLUGIN-CALLBACKS)
* [47.6.5. Funções para Produzir Saída](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-PLUGIN-OUTPUT)

Um exemplo de plugin de saída pode ser encontrado no subdiretório `contrib/test_decoding` (test-decoding.md "F.45. test_decoding — SQL-based test/example module for WAL logical decoding") da árvore de origem do PostgreSQL.

### 47.6.1. Função de Inicialização [#](#LOGICALDECODING-OUTPUT-INIT)

Um plugin de saída é carregado ao carregar dinamicamente uma biblioteca compartilhada com o nome do plugin de saída como o nome da base da biblioteca. O caminho normal de busca da biblioteca é usado para localizar a biblioteca. Para fornecer os callbacks necessários do plugin de saída e indicar que a biblioteca é realmente um plugin de saída, ela precisa fornecer uma função chamada `_PG_output_plugin_init`. Esta função é passada uma estrutura que precisa ser preenchida com os ponteiros da função de callback para ações individuais.

```
typedef struct OutputPluginCallbacks
{
    LogicalDecodeStartupCB startup_cb;
    LogicalDecodeBeginCB begin_cb;
    LogicalDecodeChangeCB change_cb;
    LogicalDecodeTruncateCB truncate_cb;
    LogicalDecodeCommitCB commit_cb;
    LogicalDecodeMessageCB message_cb;
    LogicalDecodeFilterByOriginCB filter_by_origin_cb;
    LogicalDecodeShutdownCB shutdown_cb;
    LogicalDecodeFilterPrepareCB filter_prepare_cb;
    LogicalDecodeBeginPrepareCB begin_prepare_cb;
    LogicalDecodePrepareCB prepare_cb;
    LogicalDecodeCommitPreparedCB commit_prepared_cb;
    LogicalDecodeRollbackPreparedCB rollback_prepared_cb;
    LogicalDecodeStreamStartCB stream_start_cb;
    LogicalDecodeStreamStopCB stream_stop_cb;
    LogicalDecodeStreamAbortCB stream_abort_cb;
    LogicalDecodeStreamPrepareCB stream_prepare_cb;
    LogicalDecodeStreamCommitCB stream_commit_cb;
    LogicalDecodeStreamChangeCB stream_change_cb;
    LogicalDecodeStreamMessageCB stream_message_cb;
    LogicalDecodeStreamTruncateCB stream_truncate_cb;
} OutputPluginCallbacks;

typedef void (*LogicalOutputPluginInit) (struct OutputPluginCallbacks *cb);
```

Os callbacks `begin_cb`, `change_cb` e `commit_cb` são necessários, enquanto `startup_cb`, `truncate_cb`, `message_cb`, `filter_by_origin_cb` e `shutdown_cb` são opcionais. Se `truncate_cb` não for definido, mas um `TRUNCATE` deve ser decodificado, a ação será ignorada.

Um plugin de saída também pode definir funções para suportar o streaming de transações grandes e em andamento. Os `stream_start_cb`, `stream_stop_cb`, `stream_abort_cb`, `stream_commit_cb` e `stream_change_cb` são necessários, enquanto `stream_message_cb` e `stream_truncate_cb` são opcionais. O `stream_prepare_cb` também é necessário se o plugin de saída também suportar commits de duas fases.

Um plugin de saída também pode definir funções para suportar commits em duas fases, o que permite que ações sejam decodificadas no `PREPARE TRANSACTION`. Os callbacks `begin_prepare_cb`, `prepare_cb`, `commit_prepared_cb` e `rollback_prepared_cb` são necessários, enquanto o `filter_prepare_cb` é opcional. O `stream_prepare_cb` também é necessário se o plugin de saída também suportar o streaming de grandes transações em andamento.

### 47.6.2. Capacidades [#](#LOGICALDECODING-CAPABILITIES)

Para decodificar, formatar e emitir alterações, os plugins de saída podem utilizar a maior parte da infraestrutura normal do backend, incluindo a chamada de funções de saída. O acesso apenas de leitura às relações é permitido, desde que apenas as relações sejam acessadas que tenham sido criadas por `initdb` no esquema `pg_catalog`, ou tenham sido marcadas como tabelas de catálogo fornecidas pelo usuário usando

```
ALTER TABLE user_catalog_table SET (user_catalog_table = true);
CREATE TABLE another_catalog_table(data text) WITH (user_catalog_table = true);
```

Observe que o acesso às tabelas do catálogo de usuários ou às tabelas regulares do catálogo do sistema nos plugins de saída deve ser feito apenas via APIs de varredura `systable_*`. O acesso via APIs de varredura `heap_*` gerará um erro. Além disso, quaisquer ações que levem à atribuição de ID de transação são proibidas. Isso, entre outros, inclui escrever em tabelas, realizar alterações DDL e chamar `pg_current_xact_id()`.

### 47.6.3. Modos de saída [#](#LOGICALDECODING-OUTPUT-MODE)

Os callbacks dos plugins de saída podem passar dados para o consumidor em formatos quase arbitrários. Para alguns casos de uso, como visualizar as alterações via SQL, retornar dados em um tipo de dado que pode conter dados arbitrários (por exemplo, `bytea`) é trabalhoso. Se o plugin de saída só exibe dados textuais no codificação do servidor, pode declarar isso definindo `OutputPluginOptions.output_type` como `OUTPUT_PLUGIN_TEXTUAL_OUTPUT` em vez de `OUTPUT_PLUGIN_BINARY_OUTPUT` no [callback de inicialização](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-PLUGIN-STARTUP "47.6.4.1. Startup Callback"). Nesse caso, todos os dados devem estar no codificação do servidor para que um `text` possa contê-los. Isso é verificado em compilações com ativação de asserções.

### 47.6.4. Chamadas de retorno de plugins de saída [#](#LOGICALDECODING-OUTPUT-PLUGIN-CALLBACKS)

Um plugin de saída é notificado sobre as mudanças que estão ocorrendo por meio de vários callbacks que ele precisa fornecer.

As transações concorrentes são decodificadas na ordem do commit, e apenas as alterações pertencentes a uma transação específica são decodificadas entre os callbacks `begin` e `commit`. As transações que foram revertidas explicitamente ou implicitamente nunca são decodificadas. Os pontos de salvamento bem-sucedidos são incorporados à transação que os contém na ordem em que foram executados dentro dessa transação. Uma transação que é preparada para um compromisso de duas fases usando `PREPARE TRANSACTION` também será decodificada se os callbacks dos plugins de saída necessários para a decodificação forem fornecidos. É possível que a transação atualmente preparada que está sendo decodificada seja abortada concorrentemente via um comando `ROLLBACK PREPARED`. Nesse caso, a decodificação lógica dessa transação também será abortada. Todas as alterações dessa transação são ignoradas uma vez que o aborto é detectado e o callback `prepare_cb` é invocado. Assim, mesmo em caso de aborto concorrente, há informações suficientes fornecidas ao plugin de saída para que ele lidere adequadamente com `ROLLBACK PREPARED` uma vez que essa transação seja decodificada.

Nota

Apenas as transações que já foram descarregadas com segurança no disco serão decodificadas. Isso pode levar a um `COMMIT` que não seja decodificado imediatamente em um `pg_logical_slot_get_changes()` diretamente subsequente quando o `synchronous_commit` está configurado como `off`.

#### 47.6.4.1. Chamada inicial de retorno [#](#LOGICALDECODING-OUTPUT-PLUGIN-STARTUP)

O callback opcional `startup_cb` é chamado sempre que um slot de replicação é criado ou solicitado para transmitir alterações, independentemente do número de alterações prontas para serem publicadas.

```
typedef void (*LogicalDecodeStartupCB) (struct LogicalDecodingContext *ctx,
                                        OutputPluginOptions *options,
                                        bool is_init);
```

O parâmetro `is_init` será verdadeiro quando a lacuna de replicação estiver sendo criada e falso de outra forma. *`options`* aponta para uma estrutura de opções que os plugins de saída podem definir:

```
typedef struct OutputPluginOptions
{
    OutputPluginOutputType output_type;
    bool        receive_rewrites;
} OutputPluginOptions;
```

`output_type` tem que ser definido como `OUTPUT_PLUGIN_TEXTUAL_OUTPUT` ou `OUTPUT_PLUGIN_BINARY_OUTPUT`. Veja também [Seção 47.6.3](logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-MODE). Se `receive_rewrites` for verdadeiro, o plugin de saída também será chamado para alterações feitas por reescritas de pilha durante certas operações de DDL. Essas são de interesse para plugins que lidam com replicação de DDL, mas elas requerem tratamento especial.

O callback da inicialização deve validar as opções presentes em `ctx->output_plugin_options`. Se o plugin de saída precisar ter um estado, ele pode usar `ctx->output_plugin_private` para armazená-lo.

#### 47.6.4.2. Chamada de retorno de desligamento [#](#LOGICALDECODING-OUTPUT-PLUGIN-SHUTDOWN)

O callback opcional `shutdown_cb` é chamado sempre que um slot de replicação anteriormente ativo não é mais usado e pode ser usado para realocar recursos privados ao plugin de saída. O slot não está necessariamente sendo descartado, apenas o streaming está sendo interrompido.

```
typedef void (*LogicalDecodeShutdownCB) (struct LogicalDecodingContext *ctx);
```

#### 47.6.4.3. Chamada de Retorno de Início de Transação [#](#LOGICALDECODING-OUTPUT-PLUGIN-BEGIN)

O callback `begin_cb` necessário é chamado sempre que um início de uma transação comprometida foi decodificado. Transações aborrecidas e seus conteúdos nunca são decodificados.

```
typedef void (*LogicalDecodeBeginCB) (struct LogicalDecodingContext *ctx,
                                      ReorderBufferTXN *txn);
```

O parâmetro *`txn`* contém informações meta sobre a transação, como o rótulo de tempo em que foi comprometida e seu XID.

#### 47.6.4.4. Chamada de retorno de término de transação [#](#LOGICALDECODING-OUTPUT-PLUGIN-COMMIT)

O callback `commit_cb` necessário é chamado sempre que um commit de transação foi decodificado. Os callbacks `change_cb` para todas as linhas modificadas terão sido chamados antes disso, se houver alguma linha modificada.

```
typedef void (*LogicalDecodeCommitCB) (struct LogicalDecodingContext *ctx,
                                       ReorderBufferTXN *txn,
                                       XLogRecPtr commit_lsn);
```

#### 47.6.4.5. Retorno de chamada de alteração [#](#LOGICALDECODING-OUTPUT-PLUGIN-CHANGE)

O callback `change_cb` requerido é chamado para cada modificação de linha individual dentro de uma transação, seja ela um `INSERT`, `UPDATE` ou `DELETE`. Mesmo que o comando original tenha modificado várias linhas de uma vez, o callback será chamado individualmente para cada linha. O callback `change_cb` pode acessar tabelas de catálogo do sistema ou do usuário para auxiliar no processo de saída dos detalhes da modificação da linha. No caso de decodificar uma transação preparada (mas ainda não comprometida) ou decodificar uma transação não comprometida, esse callback de mudança também pode falhar devido ao rollback simultâneo dessa mesma transação. Nesse caso, a decodificação lógica dessa transação abortada é interrompida de forma graciosa.

```
typedef void (*LogicalDecodeChangeCB) (struct LogicalDecodingContext *ctx,
                                       ReorderBufferTXN *txn,
                                       Relation relation,
                                       ReorderBufferChange *change);
```

Os parâmetros *`ctx`* e *`txn` têm o mesmo conteúdo que os dos callbacks `begin_cb` e `commit_cb`, mas, adicionalmente, o descritor de relação *`relation`* aponta para a relação a que a linha pertence e uma estrutura *`change`* que descreve a modificação da linha são passados.

Nota

Apenas as alterações em tabelas definidas pelo usuário que não estejam não registradas (consulte `UNLOGGED` (sql-createtable.md#SQL-CREATETABLE-UNLOGGED)) e não temporárias (consulte `TEMPORARY` ou `TEMP` (sql-createtable.md#SQL-CREATETABLE-TEMPORARY)) podem ser extraídas usando decodificação lógica.

#### 47.6.4.6. Retornar chamada truncada [#](#LOGICALDECODING-OUTPUT-PLUGIN-TRUNCATE)

O callback opcional `truncate_cb` é chamado para um comando `TRUNCATE`.

```
typedef void (*LogicalDecodeTruncateCB) (struct LogicalDecodingContext *ctx,
                                         ReorderBufferTXN *txn,
                                         int nrelations,
                                         Relation relations[],
                                         ReorderBufferChange *change);
```

Os parâmetros são análogos ao callback `change_cb`. No entanto, como as ações `TRUNCATE` em tabelas conectadas por chaves estrangeiras precisam ser executadas juntas, este callback recebe um array de relações em vez de apenas uma única. Veja a descrição da declaração [TRUNCATE](sql-truncate.md) para detalhes.

#### 47.6.4.7. Chamada de retorno do filtro de origem [#](#LOGICALDECODING-OUTPUT-PLUGIN-FILTER-ORIGIN)

O callback opcional `filter_by_origin_cb` é chamado para determinar se os dados que foram retransmitidos a partir de *`origin_id`* são de interesse para o plugin de saída.

```
typedef bool (*LogicalDecodeFilterByOriginCB) (struct LogicalDecodingContext *ctx,
                                               RepOriginId origin_id);
```

O parâmetro *`ctx` tem os mesmos conteúdos que para os outros callbacks. Não há informações, exceto a origem, disponíveis. Para sinalizar que as alterações que têm origem no nó passado são irrelevantes, retorne verdadeiro, fazendo com que elas sejam filtradas; falso, caso contrário. Os outros callbacks não serão chamados para transações e alterações que tenham sido filtradas.

Isso é útil ao implementar soluções de replicação em cascata ou multidirecional. Filtrar por origem permite evitar a replicação das mesmas alterações para frente e para trás nessas configurações. Embora as transações e as alterações também carreguem informações sobre a origem, filtrar por meio desse callback é notavelmente mais eficiente.

#### 47.6.4.8. Retorno de Mensagem Genérico [#](#LOGICALDECODING-OUTPUT-PLUGIN-MESSAGE)

O callback opcional `message_cb` é chamado sempre que uma mensagem de decodificação lógica foi decodificada.

```
typedef void (*LogicalDecodeMessageCB) (struct LogicalDecodingContext *ctx,
                                        ReorderBufferTXN *txn,
                                        XLogRecPtr message_lsn,
                                        bool transactional,
                                        const char *prefix,
                                        Size message_size,
                                        const char *message);
```

O parâmetro *`txn`* contém informações meta sobre a transação, como o rótulo de tempo em que foi comprometida e seu XID. No entanto, ele pode ser NULL quando a mensagem não é transacional e o XID não foi atribuído ainda na transação que registrou a mensagem. O *`lsn`* tem a localização WAL da mensagem. O *`transactional`* diz se a mensagem foi enviada como transacional ou não. Semelhante ao callback de alteração, no caso de decodificar uma transação preparada (mas ainda não comprometida) ou decodificar uma transação não comprometida, este callback de mensagem também pode falhar devido ao rollback simultâneo desta mesma transação. Nesse caso, a decodificação lógica desta transação abortada é interrompida de forma graciosa. O *`prefix`* é um prefixo arbitrário terminado em nulo que pode ser usado para identificar mensagens interessantes para o plugin atual. E, finalmente, o parâmetro *`message`* contém a mensagem real do tamanho de *`message_size`*.

É necessário tomar cuidados extras para garantir que o prefixo que o plugin de saída considera interessante seja único. Usar o nome da extensão ou do próprio plugin de saída é, muitas vezes, uma boa escolha.

#### 47.6.4.9. Preparar o callback do filtro [#](#LOGICALDECODING-OUTPUT-PLUGIN-FILTER-PREPARE)

O callback opcional `filter_prepare_cb` é chamado para determinar se os dados que fazem parte da transação atual de dois estágios devem ser considerados para decodificação nesta etapa de preparação ou posteriormente como uma transação regular de um estágio, no momento `COMMIT PREPARED`. Para sinalizar que a decodificação deve ser ignorada, retorne `true`; `false` caso contrário. Quando o callback não é definido, `false` é assumido (ou seja, sem filtragem, todas as transações que usam dois estágios de compromisso são decodificadas em dois estágios também).

```
typedef bool (*LogicalDecodeFilterPrepareCB) (struct LogicalDecodingContext *ctx,
                                              TransactionId xid,
                                              const char *gid);
```

O parâmetro *`ctx`* tem os mesmos conteúdos que os outros callbacks. Os parâmetros *`xid`* e *`gid`* fornecem duas maneiras diferentes de identificar a transação. O último `COMMIT PREPARED` ou `ROLLBACK PREPARED` carrega ambos os identificadores, fornecendo a um plugin de saída a escolha do que usar.

O callback pode ser invocado várias vezes por transação para decodificar e deve fornecer a mesma resposta estática para um par dado de *`xid`* e *`gid`* toda vez que é chamado.

#### 47.6.4.10. Preparar o início da transação para o callback [#](#LOGICALDECODING-OUTPUT-PLUGIN-BEGIN-PREPARE)

O callback `begin_prepare_cb` necessário é chamado sempre que o início de uma transação preparada foi decodificado. O campo *`gid`*, que faz parte do parâmetro *`txn`*, pode ser usado neste callback para verificar se o plugin já recebeu este `PREPARE`, caso em que ele pode errar ou ignorar as mudanças restantes da transação.

```
typedef void (*LogicalDecodeBeginPrepareCB) (struct LogicalDecodingContext *ctx,
                                             ReorderBufferTXN *txn);
```

#### 47.6.4.11. Preparar o callback da transação [#](#LOGICALDECODING-OUTPUT-PLUGIN-PREPARE)

O callback `prepare_cb` necessário é chamado sempre que uma transação que está preparada para o commit de duas fases foi decodificada. O callback `change_cb` para todas as linhas modificadas será chamado antes disso, se houver alguma linha modificada. O campo *`gid`*, que faz parte do parâmetro *`txn`*, pode ser usado neste callback.

```
typedef void (*LogicalDecodePrepareCB) (struct LogicalDecodingContext *ctx,
                                        ReorderBufferTXN *txn,
                                        XLogRecPtr prepare_lsn);
```

#### 47.6.4.12. Chamada de Retorno Preparada para Compromisso de Transação [#](#LOGICALDECODING-OUTPUT-PLUGIN-COMMIT-PREPARED)

O callback `commit_prepared_cb` necessário é chamado sempre que uma transação `COMMIT PREPARED` foi decodificada. O campo *`gid`*, que faz parte do parâmetro *`txn`*, pode ser usado neste callback.

```
typedef void (*LogicalDecodeCommitPreparedCB) (struct LogicalDecodingContext *ctx,
                                               ReorderBufferTXN *txn,
                                               XLogRecPtr commit_lsn);
```

#### 47.6.4.13. Retorno de transação preparado para callback [#](#LOGICALDECODING-OUTPUT-PLUGIN-ROLLBACK-PREPARED)

O callback `rollback_prepared_cb` requerido é chamado sempre que uma transação `ROLLBACK PREPARED` foi decodificada. O campo *`gid`*, que faz parte do parâmetro *`txn`*, pode ser usado neste callback. Os parâmetros *`prepare_end_lsn`* e *`prepare_time`* podem ser usados para verificar se o plugin recebeu este `PREPARE TRANSACTION`, caso positivo, podendo aplicar o rollback; caso contrário, pode ignorar a operação de rollback. O *`gid`* sozinho não é suficiente, pois o nó subsequente pode ter uma transação preparada com o mesmo identificador.

```
typedef void (*LogicalDecodeRollbackPreparedCB) (struct LogicalDecodingContext *ctx,
                                                 ReorderBufferTXN *txn,
                                                 XLogRecPtr prepare_end_lsn,
                                                 TimestampTz prepare_time);
```

#### 47.6.4.14. Retorno de chamada para início do fluxo [#](#LOGICALDECODING-OUTPUT-PLUGIN-STREAM-START)

O callback `stream_start_cb` necessário é chamado ao abrir um bloco de mudanças em fluxo a partir de uma transação em andamento.

```
typedef void (*LogicalDecodeStreamStartCB) (struct LogicalDecodingContext *ctx,
                                            ReorderBufferTXN *txn);
```

#### 47.6.4.15. Retorno de chamada para parada de fluxo [#](#LOGICALDECODING-OUTPUT-PLUGIN-STREAM-STOP)

O callback `stream_stop_cb` necessário é chamado ao fechar um bloco de mudanças transmitidas de uma transação em andamento.

```
typedef void (*LogicalDecodeStreamStopCB) (struct LogicalDecodingContext *ctx,
                                           ReorderBufferTXN *txn);
```

#### 47.6.4.16. Abrir o Chamado de Retorno de Fluxo [#](#LOGICALDECODING-OUTPUT-PLUGIN-STREAM-ABORT)

O callback `stream_abort_cb` necessário é chamado para abortar uma transação previamente transmitida.

```
typedef void (*LogicalDecodeStreamAbortCB) (struct LogicalDecodingContext *ctx,
                                            ReorderBufferTXN *txn,
                                            XLogRecPtr abort_lsn);
```

#### 47.6.4.17. Preparar fluxo de chamada de retorno [#](#LOGICALDECODING-OUTPUT-PLUGIN-STREAM-PREPARE)

O callback `stream_prepare_cb` é chamado para preparar uma transação previamente transmitida como parte de um compromisso de duas fases. Este callback é necessário quando o plugin de saída suporta tanto a transmissão de grandes transações em andamento quanto compromissos de duas fases.

```
typedef void (*LogicalDecodeStreamPrepareCB) (struct LogicalDecodingContext *ctx,
                                              ReorderBufferTXN *txn,
                                              XLogRecPtr prepare_lsn);
```

#### 47.6.4.18. Retorno de compromisso de fluxo [#](#LOGICALDECODING-OUTPUT-PLUGIN-STREAM-COMMIT)

O callback `stream_commit_cb` necessário é chamado para confirmar uma transação previamente transmitida.

```
typedef void (*LogicalDecodeStreamCommitCB) (struct LogicalDecodingContext *ctx,
                                             ReorderBufferTXN *txn,
                                             XLogRecPtr commit_lsn);
```

#### 47.6.4.19. Retorno de chamada de alteração de fluxo [#](#LOGICALDECODING-OUTPUT-PLUGIN-STREAM-CHANGE)

O callback `stream_change_cb` necessário é chamado ao enviar uma mudança em um bloco de mudanças transmitidas (demarcadas por chamadas `stream_start_cb` e `stream_stop_cb`). As mudanças reais não são exibidas, pois a transação pode ser interrompida em um momento posterior e não decodificamos as mudanças para transações abortadas.

```
typedef void (*LogicalDecodeStreamChangeCB) (struct LogicalDecodingContext *ctx,
                                             ReorderBufferTXN *txn,
                                             Relation relation,
                                             ReorderBufferChange *change);
```

#### 47.6.4.20. Retorno de chamada de mensagem em fluxo [#](#LOGICALDECODING-OUTPUT-PLUGIN-STREAM-MESSAGE)

O callback opcional `stream_message_cb` é chamado ao enviar uma mensagem genérica em um bloco de mudanças transmitidas (demarcadas por chamadas de `stream_start_cb` e `stream_stop_cb`). O conteúdo da mensagem para mensagens transacionais não é exibido, pois a transação pode ser interrompida em um momento posterior e não decodificamos as mudanças para transações abortadas.

```
typedef void (*LogicalDecodeStreamMessageCB) (struct LogicalDecodingContext *ctx,
                                              ReorderBufferTXN *txn,
                                              XLogRecPtr message_lsn,
                                              bool transactional,
                                              const char *prefix,
                                              Size message_size,
                                              const char *message);
```

#### 47.6.4.21. Retorno de chamada de truncar fluxo [#](#LOGICALDECODING-OUTPUT-PLUGIN-STREAM-TRUNCATE)

O callback opcional `stream_truncate_cb` é chamado para um comando `TRUNCATE` em um bloco de mudanças transmitidas (demarcado por chamadas `stream_start_cb` e `stream_stop_cb`).

```
typedef void (*LogicalDecodeStreamTruncateCB) (struct LogicalDecodingContext *ctx,
                                               ReorderBufferTXN *txn,
                                               int nrelations,
                                               Relation relations[],
                                               ReorderBufferChange *change);
```

Os parâmetros são análogos ao callback `stream_change_cb`. No entanto, como as ações `TRUNCATE` em tabelas conectadas por chaves estrangeiras precisam ser executadas juntas, este callback recebe um array de relações em vez de apenas uma única. Veja a descrição da declaração [TRUNCATE](sql-truncate.md) para detalhes.

### 47.6.5. Funções para Produzir Saída [#](#LOGICALDECODING-OUTPUT-PLUGIN-OUTPUT)

Para produzir efetivamente a saída, os plugins de saída podem escrever dados no buffer de saída `StringInfo` em `ctx->out` quando estão dentro dos callbacks de `begin_cb`, `commit_cb` ou `change_cb`. Antes de escrever no buffer de saída, o *`OutputPluginPrepareWrite(ctx, last_write)`* deve ser chamado, e após terminar de escrever no buffer, o *`OutputPluginWrite(ctx, last_write)`* deve ser chamado para realizar a escrita. O *`last_write`* indica se uma escrita específica foi a última escrita do callback.

O exemplo a seguir mostra como enviar dados para o consumidor de um plugin de saída:

```
OutputPluginPrepareWrite(ctx, true);
appendStringInfo(ctx->out, "BEGIN %u", txn->xid);
OutputPluginWrite(ctx, true);
```
