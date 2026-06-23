## 47.9. Streaming de Grandes Transações para Decodificação Lógica [#](#LOGICALDECODING-STREAMING)

Os callbacks dos plugins de saída básicos (por exemplo, `begin_cb`, `change_cb`, `commit_cb` e `message_cb`) são invocados apenas quando a transação é realmente confirmada. As alterações ainda são decodificadas do log de transação, mas são apenas passadas para o plugin de saída no momento do commit (e descartadas se a transação abortar).

Isso significa que, embora a decodificação aconteça de forma incremental e possa se espalhar para o disco para manter o uso de memória sob controle, todas as alterações decodificadas precisam ser transmitidas quando a transação finalmente é confirmada (ou, mais precisamente, quando o commit é decodificado do log de transação). Dependendo do tamanho da transação e da largura de banda da rede, o tempo de transferência pode aumentar significativamente o atraso de aplicação.

Para reduzir o atraso de aplicação causado por transações grandes, um plugin de saída pode fornecer um callback adicional para suportar o streaming incremental de transações em andamento. Existem vários callbacks de streaming necessários (`stream_start_cb`, `stream_stop_cb`, `stream_abort_cb`, `stream_commit_cb` e `stream_change_cb`) e dois callbacks opcionais (`stream_message_cb` e `stream_truncate_cb`). Além disso, se o streaming de comandos de duas fases deve ser suportado, então callbacks adicionais devem ser fornecidos. (Veja [Seção 47.10] para detalhes).

Ao transmitir uma transação em andamento, as alterações (e as mensagens) são transmitidas em blocos demarcados pelos callbacks `stream_start_cb` e `stream_stop_cb`. Uma vez que todas as alterações decodificadas são transmitidas, a transação pode ser comprometida usando o callback `stream_commit_cb` (ou possivelmente interrompida usando o callback `stream_abort_cb`). Se os compromissos de duas fases forem suportados, a transação pode ser preparada usando o callback `stream_prepare_cb`, `COMMIT PREPARED` usando o callback `commit_prepared_cb` ou interrompida usando o callback `rollback_prepared_cb`.

Uma sequência de chamada de retorno de streaming para uma transação pode parecer assim:

```
stream_start_cb(...);   <-- start of first block of changes
  stream_change_cb(...);
  stream_change_cb(...);
  stream_message_cb(...);
  stream_change_cb(...);
  ...
  stream_change_cb(...);
stream_stop_cb(...);    <-- end of first block of changes

stream_start_cb(...);   <-- start of second block of changes
  stream_change_cb(...);
  stream_change_cb(...);
  stream_change_cb(...);
  ...
  stream_message_cb(...);
  stream_change_cb(...);
stream_stop_cb(...);    <-- end of second block of changes


[a. when using normal commit]
stream_commit_cb(...);    <-- commit of the streamed transaction

[b. when using two-phase commit]
stream_prepare_cb(...);   <-- prepare the streamed transaction
commit_prepared_cb(...);  <-- commit of the prepared transaction
```

A sequência real das chamadas de callback pode, é claro, ser mais complicada. Pode haver blocos para várias transações transmitidas, algumas das transações podem ser interrompidas, etc.

Semelhante ao comportamento de spill para disco, o streaming é acionado quando a quantidade total de alterações decodificadas do WAL (para todas as transações em andamento) excede o limite definido pelo ajuste `logical_decoding_work_mem`. Nesse ponto, a transação de maior nível superior (medida pelo volume de memória atualmente usada para alterações decodificadas) é selecionada e transmitida. No entanto, em alguns casos, ainda temos que spill para disco, mesmo que o streaming esteja habilitado, porque excedemos o limite de memória, mas ainda não decodificamos o conjunto completo, por exemplo, decodificamos apenas o insert da tabela de toast, mas não o insert da tabela principal.

Mesmo ao fazer transações grandes em streaming, as alterações ainda são aplicadas na ordem de commit, preservando as mesmas garantias que o modo sem streaming.