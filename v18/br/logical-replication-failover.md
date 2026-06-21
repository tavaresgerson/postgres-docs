## 29.3. Falha de failover de replicação lógica [#](#LOGICAL-REPLICATION-FAILOVER)

Para permitir que os nós dos assinantes continuem replicando dados do nó do editor, mesmo quando o nó do editor falhar, deve haver um estado de espera físico correspondente ao nó do editor. As faixas lógicas no servidor primário que correspondem às assinaturas podem ser sincronizadas com o servidor de espera especificando `failover = true` ao criar as assinaturas. Consulte [Seção 47.2.3][(logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION "47.2.3. Replication Slot Synchronization")] para obter detalhes. A ativação do parâmetro [[`failover`][(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER)]] garante uma transição sem problemas dessas assinaturas após a promoção do estado de espera. Eles podem continuar a se inscrever em publicações no novo servidor primário.

Como a lógica de sincronização de slots é copiada de forma assíncrona, é necessário confirmar que os slots de replicação foram sincronizados com o servidor de espera antes de ocorrer a falha. Para garantir um sucesso na falha, o servidor de espera deve estar à frente do assinante. Isso pode ser alcançado configurando `synchronized_standby_slots` (runtime-config-replication.md#GUC-SYNCHRONIZED-STANDBY-SLOTS).

Para confirmar que o servidor de espera está de fato pronto para falha de um assinante específico, siga estes passos para verificar que todos os slots de replicação lógica exigidos por esse assinante foram sincronizados com o servidor de espera:

1. No nó do assinante, use a seguinte consulta SQL para identificar quais slots de replicação devem ser sincronizados com o standby que planejamos promover. Essa consulta retornará os slots de replicação relevantes associados às assinaturas habilitadas para falha.

2. No nó do assinante, use a seguinte consulta SQL para identificar quais slots de sincronização de tabela devem ser sincronizados com o standby que planejamos promover. Essa consulta deve ser executada em cada banco de dados que inclui a(s) assinatura(ões) habilitada(s) para falha. Note que o slot de sincronização de tabela deve ser sincronizado com o servidor de standby apenas se a cópia da tabela estiver concluída (Consulte [Seção 52.55][(catalog-pg-subscription-rel.md "52.55. pg_subscription_rel")]). Não precisamos garantir que os slots de sincronização de tabela sejam sincronizados em outros cenários, pois eles serão eliminados ou recriados no novo servidor primário nesses casos.

3. Verifique se os slots de replicação lógica identificados acima existem no servidor de espera e estão prontos para falha.

   ```
   /* standby # */ SELECT slot_name, (synced AND NOT temporary AND invalidation_reason IS NULL) AS failover_ready
                  FROM pg_replication_slots
                  WHERE slot_name IN
                      ('sub1','sub2','sub3', 'pg_16394_sync_16385_7394666715149055164');
     slot_name                                 | failover_ready
   --------------------------------------------+----------------
     sub1                                      | t
     sub2                                      | t
     sub3                                      | t
     pg_16394_sync_16385_7394666715149055164   | t
   (4 rows)
   ```

Se todos os slots estiverem presentes no servidor de espera e o resultado (`failover_ready`) da consulta SQL acima for verdadeiro, as assinaturas existentes podem continuar a se inscrever em publicações no novo servidor primário.

Os dois primeiros passos do procedimento acima são destinados a um assinante do PostgreSQL. Recomenda-se executar esses passos em cada nó do assinante, que será atendido pelo standby designado após o failover, para obter a lista completa de faixas de replicação. Essa lista pode então ser verificada no Passo 3 para garantir a prontidão para o failover. Os assinantes que não são PostgreSQL, por outro lado, podem usar seus próprios métodos para identificar as faixas de replicação usadas por suas respectivas assinaturas.

Em alguns casos, como durante uma falha planejada, é necessário confirmar que todos os assinantes, sejam eles PostgreSQL ou não, poderão continuar a replicação após a falha para um servidor de espera específico. Nesses casos, use a seguinte consulta SQL, em vez de realizar os dois primeiros passos acima, para identificar quais slots de replicação no primário precisam ser sincronizados com o de espera que está destinado à promoção. Esta consulta retorna os slots de replicação relevantes associados a todas as assinaturas habilitadas para falha.

```
/* primary # */ SELECT array_agg(quote_literal(r.slot_name)) AS slots
               FROM pg_replication_slots r
               WHERE r.failover AND NOT r.temporary;
 slots
-------
 {'sub1','sub2','sub3', 'pg_16394_sync_16385_7394666715149055164'}
(1 row)
```
