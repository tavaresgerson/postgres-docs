## 54.5. Protocolo de Replicação de Streaming Lógico [#](#PROTOCOL-LOGICAL-REPLICATION)

* [54.5.1. Parâmetros de Replicação de Streaming Lógico](protocol-logical-replication.md#PROTOCOL-LOGICAL-REPLICATION-PARAMS)
* [54.5.2. Mensagens de Protocolo de Replicação Lógico](protocol-logical-replication.md#PROTOCOL-LOGICAL-MESSAGES)
* [54.5.3. Fluxo de Mensagens de Protocolo de Replicação Lógico](protocol-logical-replication.md#PROTOCOL-LOGICAL-MESSAGES-FLOW)

Esta seção descreve o protocolo de replicação lógica, que é o fluxo de mensagens iniciado pelo comando de replicação `START_REPLICATION` `SLOT` *`slot_name`* `LOGICAL` do `START_REPLICATION`.

O protocolo de replicação de fluxo lógico é baseado nos primitivos do protocolo de replicação de fluxo físico.

A decodificação lógica do PostgreSQL suporta plugins de saída. `pgoutput` é o padrão usado para a replicação lógica integrada.

### 54.5.1. Parâmetros de Replicação de Streaming Lógico [#](#PROTOCOL-LOGICAL-REPLICATION-PARAMS)

Usando o comando `START_REPLICATION`, `pgoutput` aceita as seguintes opções:

proto_version: Versão do protocolo. Atualmente, as versões `1`, `2`, `3` e `4` são suportadas. É necessária uma versão válida.

A versão `2` é compatível apenas com a versão do servidor 14 e superior, e permite o streaming de transações grandes em andamento.

A versão `3` é compatível apenas com a versão do servidor 15 e superior, e permite o streaming de commits de duas fases.

A versão `4` é compatível apenas com a versão do servidor 16 e superior, e permite que fluxos de transações grandes em andamento sejam aplicados em paralelo.

nomes_de_publicação: Lista de nomes de publicação separados por vírgula para os quais se deseja se inscrever (receber alterações). Os nomes individuais de publicação são tratados como nomes de objetos padrão e podem ser citados conforme necessário. Pelo menos um nome de publicação é necessário.

binário: opção booleana para usar o modo de transferência binária. O modo binário é mais rápido que o modo de texto, mas um pouco menos robusto.

mensagens: Opção booleana para habilitar o envio das mensagens escritas por `pg_logical_emit_message`.

streaming: Opção para habilitar o streaming de transações em andamento. Os valores válidos são `off` (o padrão), `on` e `parallel`. O ajuste `parallel` permite enviar informações extras com algumas mensagens para serem usadas para paralelização. É necessário o mínimo versão do protocolo 2 para ativá-lo `on`. É necessário o mínimo versão do protocolo 4 para o valor `parallel`.

two_phase: Opção booleana para habilitar transações de dois estágios. É necessário o mínimo da versão 3 do protocolo para ativá-la.

origem: Opção para enviar alterações por sua origem. Os valores possíveis são `none` para enviar apenas as alterações que não têm origem associada, ou `any` para enviar as alterações, independentemente de sua origem. Isso pode ser usado para evitar loops (replicação infinita dos mesmos dados) entre os nós de replicação.

### 54.5.2. Mensagens do Protocolo de Replicação Lógica [#](#PROTOCOL-LOGICAL-MESSAGES)

As mensagens de protocolo individuais são discutidas nas seções a seguir. As mensagens individuais são descritas em [Seção 54.9](protocol-logicalrep-message-formats.md).

Todas as mensagens de protocolo de nível superior começam com um byte de tipo de mensagem. Embora representado em código como um caractere, este é um byte assinado sem codificação associada.

Como o protocolo de replicação de streaming fornece um comprimento de mensagem, não há necessidade de mensagens de protocolo de nível superior incorporarem um comprimento em seu cabeçalho.

### 54.5.3. Fluxo de Mensagem do Protocolo de Replicação Lógica [#](#PROTOCOL-LOGICAL-MESSAGES-FLOW)

Com exceção do comando `START_REPLICATION` e das mensagens de progresso de reprodução, todas as informações fluem apenas do backend para o frontend.

O protocolo de replicação lógica envia transações individuais uma a uma. Isso significa que todas as mensagens entre um par de mensagens Begin e Commit pertencem à mesma transação. Da mesma forma, todas as mensagens entre um par de mensagens Begin Prepare e Prepare pertencem à mesma transação. Também envia mudanças de transações grandes em andamento entre um par de mensagens Stream Start e Stream Stop. A última corrente de uma tal transação contém uma mensagem Stream Commit ou Stream Abort.

Cada transação enviada contém zero ou mais mensagens DML (Inserir, Atualizar, Deletar). Em caso de configuração em cascata, também pode conter mensagens de origem. A mensagem de origem indica que a transação foi originada em um nó de replicação diferente. Como um nó de replicação no âmbito do protocolo de replicação lógica pode ser praticamente qualquer coisa, o único identificador é o nome da origem. É responsabilidade do downstream lidar com isso conforme necessário (se necessário). A mensagem de origem é sempre enviada antes de quaisquer mensagens DML na transação.

Cada mensagem DML contém um OID de relação, que identifica a relação do publicador que foi afetada. Antes da primeira mensagem DML para um OID de relação específico, uma mensagem de Relação será enviada, descrevendo o esquema dessa relação. Posteriormente, uma nova mensagem de Relação será enviada se a definição da relação tiver sido alterada desde que a última mensagem de Relação foi enviada para ela. (O protocolo assume que o cliente é capaz de lembrar esses metadados para tantas relações quanto necessário.)

Mensagens de relação identificam os tipos de coluna por seus OIDs. No caso de um tipo embutido, presume-se que o cliente possa consultar esse OID de tipo localmente, portanto, não são necessários dados adicionais. Para um OID de tipo não embutido, uma mensagem de Tipo será enviada antes da mensagem de Relação, para fornecer o nome do tipo associado a esse OID. Assim, um cliente que precisa identificar especificamente os tipos de colunas de relação deve armazenar o conteúdo das mensagens de Tipo e, primeiro, consultar esse cache para ver se o OID do tipo está definido lá. Se não, consulte o OID do tipo localmente.