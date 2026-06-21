## 54.9. Formatos de Mensagens de Replicação Lógica [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS)

Esta seção descreve o formato detalhado de cada mensagem de replicação lógica. Essas mensagens são devolvidas pela interface SQL do slot de replicação ou são enviadas por um walsender. No caso de um walsender, elas são encapsuladas dentro de mensagens de protocolo de replicação WAL, conforme descrito em [Seção 54.4][(protocol-replication.md "54.4. Streaming Replication Protocol")], e geralmente obedecem ao mesmo fluxo de mensagens da replicação física.

Comece [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-BEGIN): Byte1('B') :   Identifica a mensagem como uma mensagem de início.

Int64 (XLogRecPtr) :   O LSN final da transação.

Int64 (TimestampTz):   Data e hora do commit da transação. O valor é o número de microsegundos desde o período de PostgreSQL (2000-01-01).

Int32 (TransactionId):   Xid da transação.

Mensagem [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-MESSAGE): Byte1('M') :   Identifica a mensagem como uma mensagem de decodificação lógica.

Int32 (TransactionId): Xid da transação (apenas presente em transações transmitidas). Este campo está disponível desde a versão do protocolo 2.

Int8:   Flags; Ou 0 para nenhuma bandeira ou 1 se a mensagem de decodificação lógica for transacional.

Int64 (XLogRecPtr) :   O LSN (Local Storage Number) da mensagem de decodificação lógica.

String:   O prefixo da mensagem de decodificação lógica.

Int32:   Comprimento do conteúdo.

Byte*`n`* :   O conteúdo da mensagem de decodificação lógica.

Comitamento [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-COMMIT): Byte1('C') :   Identifica a mensagem como uma mensagem de commit.

Int8(0) :   Flags; atualmente não utilizado.

Int64 (XLogRecPtr) :   O LSN do commit.

Int64 (XLogRecPtr) :   O LSN final da transação.

Int64 (TimestampTz):   Data e hora do commit da transação. O valor é o número de microsegundos desde o período de PostgreSQL (2000-01-01).

Origem [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-ORIGIN): Byte1('O') :   Identifica a mensagem como uma mensagem de origem.

Int64 (XLogRecPtr) :   O LSN do compromisso no servidor de origem.

String:   Nome da origem.

Observe que pode haver várias mensagens de origem dentro de uma única transação.

Relação [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-RELATION): Byte1('R') :   Identifica a mensagem como uma mensagem de relação.

Int32 (TransactionId): Xid da transação (apenas presente em transações transmitidas). Este campo está disponível desde a versão do protocolo 2.

Int32 (Oid): OID da relação.

String:   Namespace (string vazia para `pg_catalog`).

String:   Nome da relação.

Int8:   Configuração de identidade replicada para a relação (mesma que `relreplident` em `pg_class`).

Int16: Número de colunas.

Em seguida, a seguinte parte de mensagem aparece para cada coluna incluída na publicação:

Int8:   Flags para a coluna. Atualmente, pode ser 0 (sem flags) ou 1, que marca a coluna como parte da chave.

String:   Nome da coluna.

Int32 (Oid): OID do tipo de dados da coluna.

Int32: Modificador de tipo da coluna (`atttypmod`).

Tipo [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-TYPE): Byte1('Y') :   Identifica a mensagem como uma mensagem de tipo.

Int32 (TransactionId): Xid da transação (apenas presente em transações transmitidas). Este campo está disponível desde a versão do protocolo 2.

Int32 (Oid): OID do tipo de dados.

String:   Namespace (string vazia para `pg_catalog`).

String: Nome do tipo de dados.

Inserir [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-INSERT): Byte1('I') :   Identifica a mensagem como uma mensagem de inserção.

Int32 (TransactionId): Xid da transação (apenas presente em transações transmitidas). Este campo está disponível desde a versão do protocolo 2.

Int32 (Oid): OID da relação correspondente ao ID na mensagem de relação.

Byte1('N') :   Identifica a seguinte mensagem TupleData como um novo tupla.

TupleData: Parte da mensagem TupleData que representa o conteúdo da nova tupla.

Atualizar [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-UPDATE): Byte1('U') :   Identifica a mensagem como uma mensagem de atualização.

Int32 (TransactionId): Xid da transação (apenas presente em transações transmitidas). Este campo está disponível desde a versão do protocolo 2.

Int32 (Oid): OID da relação correspondente ao ID na mensagem de relação.

Byte1('K') :   Identifica a seguinte submensagem TupleData como uma chave. Este campo é opcional e está presente apenas se a atualização alterou dados em qualquer uma das colunas que fazem parte do índice REPLICA IDENTITY.

Byte1('O') :   Identifica o submensageiro TupleData seguinte como um antigo tupla. Este campo é opcional e está presente apenas se a tabela na qual a atualização ocorreu tiver a REPLICA IDENTITY definida como FULL.

TupleData: Parte da mensagem TupleData que representa o conteúdo da antiga tupla ou chave primária. Presente apenas se a parte anterior 'O' ou 'K' estiver presente.

Byte1('N') :   Identifica a seguinte mensagem TupleData como um novo tupla.

TupleData: Parte da mensagem TupleData que representa o conteúdo de uma nova tupla.

A mensagem de atualização pode conter uma parte da mensagem 'K' ou uma parte da mensagem 'O' ou nenhuma delas, mas nunca ambas.

Exclua [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-DELETE): Byte1('D') :   Identifica a mensagem como uma mensagem de exclusão.

Int32 (TransactionId): Xid da transação (apenas presente em transações transmitidas). Este campo está disponível desde a versão do protocolo 2.

Int32 (Oid): OID da relação correspondente ao ID na mensagem de relação.

Byte1('K') :   Identifica o submensageiro TupleData seguinte como uma chave. Este campo está presente se a tabela na qual a exclusão ocorreu usa um índice como REPLICA IDENTITY.

Byte1('O') :   Identifica a seguinte mensagem TupleData como um antigo tuplo. Este campo está presente se a tabela na qual a exclusão ocorreu tiver a REPLICA IDENTITY definida como FULL.

TupleData: Parte da mensagem TupleData que representa o conteúdo do antigo tuplo ou chave primária, dependendo do campo anterior.

A mensagem de Excluir pode conter uma parte da mensagem 'K' ou uma parte da mensagem 'O', mas nunca ambas.

Retorne [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-TRUNCATE): Byte1('T') :   Identifica a mensagem como uma mensagem de truncar.

Int32 (TransactionId): Xid da transação (apenas presente em transações transmitidas). Este campo está disponível desde a versão do protocolo 2.

Int32: Número de relações

Int8:   Bits de opção para `TRUNCATE`: 1 para `CASCADE`, 2 para `RESTART IDENTITY`

Int32 (Oid): OID da relação correspondente ao ID na mensagem de relação. Este campo é repetido para cada relação.

As seguintes mensagens (Início do fluxo, Parar o fluxo, Compromisso do fluxo e Abrir o fluxo) estão disponíveis desde a versão do protocolo 2.

Stream Start [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-STREAM-START): Byte1('S') :   Identifica a mensagem como uma mensagem de início de fluxo.

Int32 (TransactionId):   Xid da transação.

Int8:   Um valor de 1 indica que este é o primeiro segmento de fluxo para este XID, 0 para qualquer outro segmento de fluxo.

Parar de transmitir [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-STREAM-STOP): Byte1('E') :   Identifica a mensagem como uma mensagem de parada de transmissão.

Stream Commit [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-STREAM-COMMIT): Byte1('c') :   Identifica a mensagem como uma mensagem de commit de fluxo.

Int32 (TransactionId):   Xid da transação.

Int8(0) :   Flags; atualmente não utilizado.

Int64 (XLogRecPtr) :   O LSN do commit.

Int64 (XLogRecPtr) :   O LSN final da transação.

Int64 (TimestampTz):   Data e hora do commit da transação. O valor é o número de microsegundos desde o período de PostgreSQL (2000-01-01).

Aborrecimento de fluxo [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-STREAM-ABORT): Byte1('A') :   Identifica a mensagem como um aborrecimento de fluxo.

Int32 (TransactionId):   Xid da transação.

Int32 (TransactionId):   Xid da subtransação (será o mesmo que o xid da transação para as transações de nível superior).

Int64 (XLogRecPtr) :   O LSN (Local Stream Number) da operação de aborrecimento, presente apenas quando o fluxo está configurado em paralelo. Este campo está disponível desde a versão 4 do protocolo.

Int64 (TimestampTz):   Aguarda o timestamp da transação, presente apenas quando o streaming está configurado em paralelo. O valor é em número de microsegundos desde a época do PostgreSQL (2000-01-01). Este campo está disponível desde a versão do protocolo 4.

As seguintes mensagens (Comece a preparar, Prepare, Comunique-se com o preparado, Revolva o preparado, Prepare) estão disponíveis desde a versão do protocolo 3.

Começar Preparar [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-BEGIN-PREPARE): Byte1('b') :   Identifica a mensagem como o início de uma mensagem de transação preparada.

Int64 (XLogRecPtr):   O LSN do prepare.

Int64 (XLogRecPtr) :   O LSN final da transação preparada.

Int64 (TimestampTz):   Prepare o timestamp da transação. O valor está em número de microsegundos desde o período do PostgreSQL (2000-01-01).

Int32 (TransactionId):   Xid da transação.

String: O GID definido pelo usuário da transação preparada.

Prepare [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-PREPARE): Byte1('P') :   Identifica a mensagem como uma mensagem de transação preparada.

Int8(0) :   Flags; atualmente não utilizado.

Int64 (XLogRecPtr):   O LSN do prepare.

Int64 (XLogRecPtr) :   O LSN final da transação preparada.

Int64 (TimestampTz):   Prepare o timestamp da transação. O valor está em número de microsegundos desde o período do PostgreSQL (2000-01-01).

Int32 (TransactionId):   Xid da transação.

String: O GID definido pelo usuário da transação preparada.

Comit Preparado [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-COMMIT-PREPARED): Byte1('K') :   Identifica a mensagem como o commit de uma mensagem de transação preparada.

Int8(0) :   Flags; atualmente não utilizado.

Int64 (XLogRecPtr) :   O LSN (Local Storage Number) do commit da transação preparada.

Int64 (XLogRecPtr) : O LSN final do commit da transação preparada.

Int64 (TimestampTz):   Data e hora do commit da transação. O valor é o número de microsegundos desde o período de PostgreSQL (2000-01-01).

Int32 (TransactionId):   Xid da transação.

String: O GID definido pelo usuário da transação preparada.

Recuo Preparado [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-ROLLBACK-PREPARED): Byte1('r') :   Identifica a mensagem como o recuo de uma mensagem de transação preparada.

Int8(0) :   Flags; atualmente não utilizado.

Int64 (XLogRecPtr) :   O LSN final da transação preparada.

Int64 (XLogRecPtr) : O LSN final do rollback da transação preparada.

Int64 (TimestampTz):   Prepare o timestamp da transação. O valor está em número de microsegundos desde o período do PostgreSQL (2000-01-01).

Int64 (TimestampTz):   Data de desvio da transação. O valor é em número de microsegundos desde a época do PostgreSQL (2000-01-01).

Int32 (TransactionId):   Xid da transação.

String: O GID definido pelo usuário da transação preparada.

Stream Prepare [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-STREAM-PREPARE): Byte1('p') :   Identifica a mensagem como uma mensagem de transação preparada em fluxo.

Int8(0) :   Flags; atualmente não utilizado.

Int64 (XLogRecPtr):   O LSN do prepare.

Int64 (XLogRecPtr) :   O LSN final da transação preparada.

Int64 (TimestampTz):   Prepare o timestamp da transação. O valor está em número de microsegundos desde o período do PostgreSQL (2000-01-01).

Int32 (TransactionId):   Xid da transação.

String: O GID definido pelo usuário da transação preparada.

As seguintes partes de mensagem são compartilhadas pelas mensagens acima.

TupleData [#](#PROTOCOL-LOGICALREP-MESSAGE-FORMATS-TUPLEDATA): Int16 :   Número de colunas.

Em seguida, uma das seguintes submensagens aparece para cada coluna publicada:

Byte1('n') :   Identifica os dados como valor NULL.

Ou

Byte1('u'):   Identifica o valor TOAST não alterado (o valor real não é enviado).

Ou

Byte1('t') : Identifica os dados como um valor formatado em texto.

Ou

Byte1('b') :   Identifica os dados como um valor formatado em binário.

Int32:   Comprimento do valor da coluna.

Byte*`n`* :   O valor da coluna, seja em formato binário ou em texto. (Conforme especificado no formato anterior byte). *`n`* é o comprimento acima.