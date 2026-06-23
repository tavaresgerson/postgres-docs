## 29.13. Atualize [#](#LOGICAL-REPLICATION-UPGRADE)

* [29.13.1. Prepare-se para atualizações do Publisher][(logical-replication-upgrade.md#PREPARE-PUBLISHER-UPGRADES)
* [29.13.2. Prepare-se para atualizações do assinante][(logical-replication-upgrade.md#PREPARE-SUBSCRIBER-UPGRADES)
* [29.13.3. Atualize os clusters de replicação lógica][(logical-replication-upgrade.md#UPGRADING-LOGICAL-REPLICATION-CLUSTERS)

A migração dos [*[clusters de replicação lógica](glossary.md#GLOSSARY-LOGICAL-REPLICATION-CLUSTER)*](glossário.md#GLÓSSICO-CLUSTERS-DE-REPLICAÇÃO-LÓGICA) é possível apenas quando todos os membros dos antigos clusters de replicação lógica são versões 17.0 ou posteriores.

### 29.13.1. Prepare-se para as atualizações do Publisher [#](#PREPARE-PUBLISHER-UPGRADES)

O pg_upgrade tenta migrar slots lógicos. Isso ajuda a evitar a necessidade de definir manualmente os mesmos slots lógicos no novo editor. A migração de slots lógicos só é suportada quando o antigo clúster é versão 17.0 ou posterior. Os slots lógicos em clústeres antes da versão 17.0 serão ignorados silenciosamente.

Antes de começar a atualizar o clúster do editor, certifique-se de que a assinatura esteja desativada temporariamente, executando `ALTER SUBSCRIPTION ... DISABLE` (sql-altersubscription.md "ALTER SUBSCRIPTION"). Reavalie a assinatura após a atualização.

Há alguns pré-requisitos para o pg_upgrade poder fazer a atualização dos slots lógicos. Se esses pré-requisitos não forem atendidos, um erro será relatado.

* O novo clúster deve ter `wal_level` como (runtime-config-wal.md#GUC-WAL-LEVEL).
* O novo clúster deve ter [`max_replication_slots`](runtime-config-replication.md#GUC-MAX-REPLICATION-SLOTS) configurado com um valor maior ou igual ao número de faixas presentes no clúster antigo.
* Os plugins de saída referenciados pelas faixas no clúster antigo devem ser instalados no diretório executável do PostgreSQL.
* O clúster antigo replicou todas as transações e mensagens de decodificação lógica para os assinantes.
* Todas as faixas no clúster antigo devem ser utilizáveis, ou seja, não devem haver faixas cujas [pg_replication_slots](view-pg-replication-slots.md "53.20. pg_replication_slots").`conflicting` não é `true`.
* O novo clúster não deve ter faixas lógicas permanentes, ou seja, não deve haver faixas onde [pg_replication_slots](view-pg-replication-slots.md "53.20. pg_replication_slots").`temporary` é `false`.

### 29.13.2. Prepare-se para as atualizações do assinante [#](#PREPARE-SUBSCRIBER-UPGRADES)

Configure as configurações do [assinante](logical-replication-config.md#LOGICAL-REPLICATION-CONFIG-SUBSCRIBER) no novo assinante. O pg_upgrade tenta migrar as dependências da assinatura, que incluem as informações da tabela da assinatura presentes no catálogo do sistema [pg_subscription_rel](catalog-pg-subscription-rel.md) e também a origem de replicação da assinatura. Isso permite a replicação lógica no novo assinante para continuar do ponto onde o antigo assinante estava. A migração das dependências da assinatura só é suportada quando o antigo clúster é versão 17.0 ou posterior. As dependências da assinatura em clústeres antes da versão 17.0 serão ignoradas silenciosamente.

Existem alguns pré-requisitos para o pg_upgrade poder atualizar as assinaturas. Se esses pré-requisitos não forem atendidos, um erro será relatado.

* Todas as tabelas de assinatura no antigo assinante devem estar no estado `i` (inicializado) ou `r` (pronto). Isso pode ser verificado verificando [pg_subscription_rel](catalog-pg-subscription-rel.md "52.55. pg_subscription_rel").`srsubstate`.
* A entrada de origem de replicação correspondente a cada uma das assinaturas deve existir no antigo clúster. Isso pode ser encontrado verificando as tabelas de sistema [pg_subscription](catalog-pg-subscription.md "52.54. pg_subscription") e [pg_replication_origin](catalog-pg-replication-origin.md "52.44. pg_replication_origin").
* O novo clúster deve ter [`max_active_replication_origins`](runtime-config-replication.md#GUC-MAX-ACTIVE-REPLICATION-ORIGINS) configurado para um valor maior ou igual ao número de assinaturas presentes no antigo clúster.

### 29.13.3. Atualização de clusters de replicação lógica [#](#UPGRADING-LOGICAL-REPLICATION-CLUSTERS)

Ao atualizar um assinante, as operações de escrita podem ser realizadas no editor. Essas alterações serão replicadas para o assinante assim que a atualização do assinante for concluída.

### Nota

As restrições de replicação lógica também se aplicam a atualizações de clúster de replicação lógica. Consulte [Seção 29.8](logical-replication-restrictions.md) para obter detalhes.

Os pré-requisitos da atualização do editor se aplicam também aos upgrades de clúster de replicação lógica. Consulte [Seção 29.13.1](logical-replication-upgrade.md#PREPARE-PUBLISHER-UPGRADES) para obter detalhes.

Os pré-requisitos da atualização do assinante também se aplicam às atualizações de clúster de replicação lógica. Consulte [Seção 29.13.2](logical-replication-upgrade.md#PREPARE-SUBSCRIBER-UPGRADES) para obter detalhes.

### Aviso

Para atualizar um clúster de replicação lógica, é necessário realizar várias etapas em vários nós. Como nem todas as operações são transacionais, recomenda-se que o usuário faça backups conforme descrito em [Seção 25.3.2](continuous-archiving.md#BACKUP-BASE-BACKUP).

Os passos para atualizar os seguintes clústeres de replicação lógica são detalhados abaixo:

* Siga os passos especificados em [Seção 29.13.3.1](logical-replication-upgrade.md#STEPS-TWO-NODE-LOGICAL-REPLICATION-CLUSTER) para atualizar um clúster de replicação lógica de dois nós.
* Siga os passos especificados em [Seção 29.13.3.2](logical-replication-upgrade.md#STEPS-CASCADED-LOGICAL-REPLICATION-CLUSTER) para atualizar um clúster de replicação lógica casca.
* Siga os passos especificados em [Seção 29.13.3.3](logical-replication-upgrade.md#STEPS-TWO-NODE-CIRCULAR-LOGICAL-REPLICATION-CLUSTER) para atualizar um clúster de replicação lógica circular de dois nós.

#### 29.13.3.1. Passos para Atualizar um Clúster de Replicação Lógica de Dois Nodos [#](#STEPS-TWO-NODE-LOGICAL-REPLICATION-CLUSTER)

Digamos que o editor esteja em `node1` e o assinante esteja em `node2`. O assinante `node2` tem uma assinatura `sub1_node1_node2` que está assinando as alterações de `node1`.

1. Desative todas as assinaturas em `node2` que estão assinando as alterações de `node1` usando [`ALTER SUBSCRIPTION ... DISABLE`](sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE), por exemplo:

2. Parar o servidor do editor em `node1`, por exemplo:

3. Inicie a instância do ``` pg_ctl -D /opt/PostgreSQL/data1 stop
```
usando a versão mais recente necessária.
4. Atualize o servidor do editor `data1_upgraded` para a versão mais recente necessária, por exemplo:

5. Inicie o servidor do editor atualizado em `node1`, por exemplo:

6. Parar o servidor de assinante em `node2`, por exemplo:

7. Inicie a instância ```
pg_ctl -D /opt/PostgreSQL/data2 stop
```
8. Atualize o servidor do assinante `data2_upgraded` para a versão nova necessária, por exemplo:

9. Inicie o servidor de assinante atualizado em `node2`, por exemplo:

10. Em ``` pg_ctl -D /opt/PostgreSQL/data2_upgraded start -l logfile
```
, crie quaisquer tabelas que foram criadas no servidor do editor atualizado `node1` entre [Passo 1](logical-replication-upgrade.md#TWO-NODE-CLUSTER-DISABLE-SUBSCRIPTIONS-NODE2 "Step 1") e agora, por exemplo:

11. Ative todas as assinaturas em ```
 /* node2 # */ CREATE TABLE distributors (did integer PRIMARY KEY, name varchar(40));
```

12. Atualize as publicações da assinatura do ``` /* node2 # */ ALTER SUBSCRIPTION sub1_node1_node2 ENABLE;
```
usando [`node2`](sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-REFRESH-PUBLICATION), por exemplo:

```
    /* node2 # */ ALTER SUBSCRIPTION sub1_node1_node2 REFRESH PUBLICATION;
```

### Nota

Nos passos descritos acima, o editor é atualizado primeiro, seguido pelo assinante. Alternativamente, o usuário pode usar passos semelhantes para atualizar o assinante primeiro, seguido pelo editor.

#### 29.13.3.2. Passos para Atualizar um Clúster de Replicação Lógica Cascadinho [#](#STEPS-CASCADED-LOGICAL-REPLICATION-CLUSTER)

Digamos que tenhamos uma configuração de replicação lógica em cascata `node1`->`node2`->`node3`. Aqui, `node2` está assinando as alterações de `node1` e `node3` está assinando as alterações de `node2`. O `node2` tem uma assinatura `sub1_node1_node2` que está assinando as alterações de `node1`. O `node3` tem uma assinatura `sub1_node2_node3` que está assinando as alterações de `node2`.

1. Desative todas as assinaturas em `node2` que estão assinando as alterações de `node1` usando [`ALTER SUBSCRIPTION ... DISABLE`](sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE), por exemplo:

2. Parar o servidor em `node1`, por exemplo:

3. Inicie a instância do ```
pg_ctl -D /opt/PostgreSQL/data1 stop
```
4. Atualize o servidor do `node1` para a versão mais recente necessária, por exemplo:

5. Inicie o servidor atualizado em `node1`, por exemplo:

6. Desative todas as assinaturas em ``` pg_ctl -D /opt/PostgreSQL/data1_upgraded start -l logfile
```
que estão assinando as alterações de [[PH_CBK_131]] usando [`ALTER SUBSCRIPTION ... DISABLE`](sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE), por exemplo:

7. Parar o servidor em `node2`, por exemplo:

8. Inicie a instância ```
pg_ctl -D /opt/PostgreSQL/data2 stop
```
9. Atualize o servidor do `node2` para a versão nova necessária, por exemplo:

10. Inicie o servidor atualizado em `node2`, por exemplo:

```
    pg_ctl -D /opt/PostgreSQL/data2_upgraded start -l logfile
```

12. Ative todas as assinaturas em ``` /* node2 # */ CREATE TABLE distributors (did integer PRIMARY KEY, name varchar(40));
```
que estão assinando as alterações de [[PH_CBK_18142]], usando [`ALTER SUBSCRIPTION ... ENABLE`](sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-ENABLE), por exemplo:

13. Atualize as publicações da assinatura do ```
/* node2 # */ ALTER SUBSCRIPTION sub1_node1_node2 ENABLE;
```

14. Parar o servidor em `node3`, por exemplo:

15. Inicie a instância do ``` pg_ctl -D /opt/PostgreSQL/data3 stop
```
usando a versão mais recente necessária.
16. Atualize o servidor do `node3` para a versão nova necessária, por exemplo:

17. Inicie o servidor atualizado em `node3`, por exemplo:

18. Em ```
pg_ctl -D /opt/PostgreSQL/data3_upgraded start -l logfile
```

19. Ative todas as assinaturas em ``` /* node3 # */ CREATE TABLE distributors (did integer PRIMARY KEY, name varchar(40));
```
que estão assinando as alterações de [[PH_CBK_156]] usando [`ALTER SUBSCRIPTION ... ENABLE`](sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-ENABLE), por exemplo:

20. Atualize as publicações da assinatura do ```
/* node3 # */ ALTER SUBSCRIPTION sub1_node2_node3 ENABLE;
```

```
/* node3 # */ ALTER SUBSCRIPTION sub1_node2_node3 REFRESH PUBLICATION;
```

#### 29.13.3.3. Passos para Atualizar um Clúster de Replicação Lógica Circular de Dois Nodos [#](#STEPS-TWO-NODE-CIRCULAR-LOGICAL-REPLICATION-CLUSTER)

Digamos que tenhamos uma configuração de replicação lógica circular `node1`->`node2` e `node2`->`node1`. Aqui, `node2` está assinando as alterações de `node1` e `node1` está assinando as alterações de `node2`. O `node1` tem uma assinatura `sub1_node2_node1` que está assinando as alterações de `node2`. O `node2` tem uma assinatura `sub1_node1_node2` que está assinando as alterações de `node1`.

1. Desative todas as assinaturas em `node2` que estão assinando as alterações de `node1` usando [`ALTER SUBSCRIPTION ... DISABLE`](sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE), por exemplo:

2. Parar o servidor em `node1`, por exemplo:

3. Inicie a instância de ``` pg_ctl -D /opt/PostgreSQL/data1 stop
```
usando a versão mais recente necessária.
4. Atualize o servidor do `node1` para a versão mais recente necessária, por exemplo:

5. Inicie o servidor atualizado em `node1`, por exemplo:

6. Ative todas as assinaturas em ```
pg_ctl -D /opt/PostgreSQL/data1_upgraded start -l logfile
```

```
   /* node2 # */ ALTER SUBSCRIPTION sub1_node1_node2 ENABLE;
```

8. Atualize as publicações da assinatura do ``` /* node1 # */ CREATE TABLE distributors (did integer PRIMARY KEY, name varchar(40));
```
para copiar os dados iniciais da tabela do `node2` usando [`ALTER SUBSCRIPTION ... REFRESH PUBLICATION`](sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-REFRESH-PUBLICATION), por exemplo:

9. Desative todas as assinaturas em ```
/* node1 # */ ALTER SUBSCRIPTION sub1_node2_node1 REFRESH PUBLICATION;
```

10. Parar o servidor em `node2`, por exemplo:

11. Inicie a instância do ``` pg_ctl -D /opt/PostgreSQL/data2 stop
```
usando a versão mais recente necessária.
12. Atualize o servidor do `node2` para a versão nova necessária, por exemplo:

13. Inicie o servidor atualizado em `node2`, por exemplo:

14. Ative todas as assinaturas em ```
pg_ctl -D /opt/PostgreSQL/data2_upgraded start -l logfile
```

15. Em ``` /* node1 # */ ALTER SUBSCRIPTION sub1_node2_node1 ENABLE;
```
, crie quaisquer tabelas que foram criadas no `node1` atualizado entre [Passo 9](logical-replication-upgrade.md#CIRCULAR-CLUSTER-DISABLE-SUB-NODE1 "Step 9") e agora, por exemplo:

16. Atualize as publicações da assinatura do ```
/* node2 # */ CREATE TABLE distributors (did integer PRIMARY KEY, name varchar(40));
```

```
/* node2 # */ ALTER SUBSCRIPTION sub1_node1_node2 REFRESH PUBLICATION;
```
