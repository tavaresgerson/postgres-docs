## 29.7. Conflitos [#](#LOGICAL-REPLICATION-CONFLICTS)]

A replicação lógica se comporta de forma semelhante às operações normais de DML, no sentido de que os dados serão atualizados mesmo se forem alterados localmente no nó do assinante. Se os dados recebidos violarem quaisquer restrições, a replicação será interrompida. Isso é referido como um *conflito*. Ao replicar operações `UPDATE` ou `DELETE`, os dados ausentes também são considerados como um *conflito*, mas isso não resulta em um erro e tais operações serão simplesmente ignoradas.

O registro adicional é acionado e as estatísticas de conflito são coletadas (mostradas na visualização `pg_stat_subscription_stats` (monitoring-stats.md#MONITORING-PG-STAT-SUBSCRIPTION-STATS "27.2.9. pg_stat_subscription_stats")) nos seguintes casos de *conflitos*:

`insert_exists` [#](#CONFLICT-INSERT-EXISTS): Inserindo uma linha que viola uma restrição única de `NOT DEFERRABLE`. Observe que, para registrar o tempo de origem e os detalhes do timestamp do chave em conflito, [`track_commit_timestamp`](runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP) deve ser habilitado no assinante. Neste caso, um erro será exibido até que o conflito seja resolvido manualmente.

`update_origin_differs` [#](#CONFLICT-UPDATE-ORIGIN-DIFFERS): Atualizando uma linha que foi modificada anteriormente por outra origem. Note que esse conflito só pode ser detectado quando [[`track_commit_timestamp`](runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP)]] está habilitado no assinante. Atualmente, a atualização é sempre aplicada, independentemente da origem da linha local.

`update_exists` [#](#CONFLICT-UPDATE-EXISTS): O valor atualizado de uma linha viola uma `NOT DEFERRABLE` restrição única. Observe que, para registrar o detalhe do timestamp de origem e do compromisso da chave em conflito, [`track_commit_timestamp`](runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP) deve ser habilitado no assinante. Neste caso, um erro será exibido até que o conflito seja resolvido manualmente. Observe que, ao atualizar uma tabela particionada, se o valor da linha atualizado satisfazer outra restrição de partição, resultando na inserção da linha em uma nova partição, o conflito `insert_exists` pode surgir se a nova linha violar uma `NOT DEFERRABLE` restrição única.

`update_missing` [#](#CONFLICT-UPDATE-MISSING): A linha a ser atualizada não foi encontrada. A atualização será simplesmente ignorada neste cenário.

`delete_origin_differs` [#](#CONFLICT-DELETE-ORIGIN-DIFFERS): Excluindo uma linha que foi modificada anteriormente por outra origem. Observe que esse conflito só pode ser detectado quando [`track_commit_timestamp`](runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP) está habilitado no assinante. Atualmente, a exclusão é sempre aplicada, independentemente da origem da linha local.

`delete_missing` [#](#CONFLICT-DELETE-MISSING): A linha a ser excluída não foi encontrada. O delete será simplesmente ignorado neste cenário.

`multiple_unique_conflicts` [#](#CONFLICT-MULTIPLE-UNIQUE-CONFLICTS): Inserir ou atualizar uma linha viola múltiplas restrições únicas `NOT DEFERRABLE`. Observe que, para registrar o tempo de origem e os detalhes do timestamp de conflito das chaves conflitantes, certifique-se de que [`track_commit_timestamp`](runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP) está habilitado no assinante. Neste caso, um erro será exibido até que o conflito seja resolvido manualmente.

Observe que existem outros cenários de conflito, como violações de restrições de exclusão. Atualmente, não fornecemos detalhes adicionais para eles no log.

O formato de registro para conflitos de replicação lógica é o seguinte:

```
LOG:  conflict detected on relation "schemaname.tablename": conflict=conflict_type
DETAIL:  detailed_explanation.
{detail_values [; ... ]}.

where detail_values is one of:

    Key (column_name [, ...])=(column_value [, ...])
    existing local row [(column_name [, ...])=](column_value [, ...])
    remote row [(column_name [, ...])=](column_value [, ...])
    replica identity {(column_name [, ...])=(column_value [, ...]) | full [(column_name [, ...])=](column_value [, ...])}
```

O log fornece as seguintes informações:

`LOG`: * *`schemaname`*.*`tablename`* identifica a relação local envolvida no conflito. * *`conflict_type`* é o tipo de conflito que ocorreu (por exemplo, `insert_exists`, `update_exists`).

`DETAIL`: * *`detailed_explanation`* inclui a origem, o ID de transação e o timestamp de commit da transação que modificou a linha local existente, se disponível. * A seção `Key` inclui os valores chave da linha local que violaram uma restrição única para conflitos de `insert_exists`, `update_exists` ou `multiple_unique_conflicts`. * A seção `existing local row` inclui a linha local se sua origem difere da linha remota para conflitos de `update_origin_differs` ou `delete_origin_differs`, ou se o valor chave conflitar com a linha remota para conflitos de `insert_exists`, `update_exists` ou `multiple_unique_conflicts`. * A seção `remote row` inclui a nova linha da operação de inserção ou atualização remota que causou o conflito. Note que, para uma operação de atualização, o valor da coluna da nova linha será nulo se o valor não for alterado e torrado. * A seção `replica identity` inclui os valores de chave de identidade da replica que foram usados para pesquisar a linha local existente a ser atualizada ou excluída. Isso pode incluir o valor da linha completa se a relação local for marcada com [`REPLICA IDENTITY FULL`](sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY-FULL). * *`column_name`* é o nome da coluna. Para os casos de `existing local row`, `remote row` e `replica identity full`, os nomes das colunas são registrados apenas se o usuário não possui o privilégio de acessar todas as colunas da tabela. Se os nomes das colunas estiverem presentes, eles aparecem na mesma ordem que os valores correspondentes das colunas. * *`column_value`* é o valor da coluna. Os grandes valores das colunas são truncados para 64 bytes. * Note que, no caso de conflito de `multiple_unique_conflicts`, várias linhas de *`detailed_explanation`* e *`detail_values`* serão geradas, cada uma detalhando as informações de conflito associadas a restrições únicas distintas.

As operações de replicação lógica são realizadas com os privilégios do papel que possui a assinatura. Falhas de permissões em tabelas de destino causarão conflitos de replicação, assim como a segurança habilitada em nível de linha de dados em tabelas de destino sobre as quais o proprietário da assinatura está sujeito, independentemente de qualquer política rejeitar normalmente o (ddl-rowsecurity.md "5.9. Row Security Policies") (ddl-rowsecurity.md "5.9. Row Security Policies"), [[PH_LNK_67]] [[PH_LNK_67]], [[PH_LNK_68]] ou [[PH_LNK_69]] que está sendo replicado. Essa restrição em segurança em nível de linha de dados pode ser levantada em uma versão futura do PostgreSQL.

Um conflito que produza um erro interrompe a replicação; ele deve ser resolvido manualmente pelo usuário. Detalhes sobre o conflito podem ser encontrados no log do servidor do assinante.

A resolução pode ser feita alterando os dados ou permissões do assinante, de modo que não haja conflito com a mudança recebida, ou ignorando a transação que entra em conflito com os dados existentes. Quando um conflito produz um erro, a replicação não prosseguirá, e o trabalhador de replicação lógica emitirá o seguinte tipo de mensagem no log do servidor do assinante:

```
ERROR:  conflict detected on relation "public.test": conflict=insert_exists
DETAIL:  Key already exists in unique index "t_pkey", which was modified locally in transaction 740 at 2024-06-26 10:47:04.727375+08.
Key (c)=(1); existing local row (1, 'local'); remote row (1, 'remote').
CONTEXT:  processing remote data for replication origin "pg_16395" during "INSERT" for replication target relation "public.test" in transaction 725 finished at 0/14C0378
```

O LSN (Local Sequence Number) da transação que contém a alteração que viola a restrição e o nome da origem de replicação podem ser encontrados no log do servidor (LSN 0/14C0378 e origem de replicação `pg_16395` no caso acima). A transação que produziu o conflito pode ser ignorada usando [[`ALTER SUBSCRIPTION ... SKIP`](sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-SKIP)]] com o LSN de término (ou seja, LSN 0/14C0378). O LSN de término pode ser um LSN em que a transação é comprometida ou preparada no editor. Alternativamente, a transação também pode ser ignorada chamando a função [[`pg_replication_origin_advance()`](functions-admin.md#PG-REPLICATION-ORIGIN-ADVANCE)]. Antes de usar essa função, a assinatura precisa ser desativada temporariamente, seja usando [[`ALTER SUBSCRIPTION ... DISABLE`](sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE)]] ou, a assinatura pode ser usada com a opção [[`disable_on_error`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-DISABLE-ON-ERROR)]. Em seguida, você pode usar a função `pg_replication_origin_advance()` com o *`node_name`* (ou seja, `pg_16395`) e o próximo LSN do LSN de término (ou seja, 0/14C0379). A posição atual das origens pode ser vista na visualização do sistema [[`pg_replication_origin_status`](view-pg-replication-origin-status.md "53.19. pg_replication_origin_status")]. Por favor, note que ignorar toda a transação inclui ignorar alterações que podem não violar nenhuma restrição. Isso pode facilmente tornar o assinante inconsistente. Os detalhes adicionais sobre as linhas conflitantes, como sua origem e o timestamp de comprometimento, podem ser vistos na linha `DETAIL` do log. Mas note que essa informação está disponível apenas quando [[`track_commit_timestamp`](runtime-config-replication.md#GUC-TRACK-COMMIT-TIMESTAMP)]] está habilitada no assinante. Os usuários podem usar essa informação para decidir se devem reter a alteração local ou adotar a alteração remota. Por exemplo, a linha `DETAIL` no log acima indica que a linha existente foi modificada localmente. Os usuários podem realizar manualmente uma alteração remota-win.

Quando o modo `streaming`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-STREAMING) estiver configurado como `parallel`, o LSN de término de transações falhas pode não ser registrado. Nesse caso, pode ser necessário alterar o modo de transmissão para `on` ou `off` e causar os mesmos conflitos novamente, para que o LSN de término da transação falha seja escrito no log do servidor. Para o uso do LSN de término, consulte `ALTER SUBSCRIPTION ... SKIP`(sql-altersubscription.md "ALTER SUBSCRIPTION").