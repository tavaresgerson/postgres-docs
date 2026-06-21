## Capítulo 29. Replicação Lógica

**Índice**

* [29.1. Publicação](logical-replication-publication.md)

+ [29.1.1. Identidade Replicável](logical-replication-publication.md#LOGICAL-REPLICATION-PUBLICATION-REPLICA-IDENTITY)

* [29.2. Assinatura](logical-replication-subscription.md)

+ [29.2.1. Gerenciamento de Fendas de Replicação](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-SLOT)
+ [29.2.2. Exemplos: Configuração de Replicação Lógica](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES)
+ [29.2.3. Exemplos: Criação de Fenda de Replicação Adiada](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT)

* [29.3. Falha de failover de replicação lógica](logical-replication-failover.md)
* [29.4. Filtros de linha](logical-replication-row-filter.md)

+ [29.4.1. Regras de filtro de linha](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-RULES)
+ [29.4.2. Restrições de expressão](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-RESTRICTIONS)
+ [29.4.3. Transformações de atualização](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-TRANSFORMATIONS)
+ [29.4.4. Tabelas particionadas](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-PARTITIONED-TABLE)
+ [29.4.5. Sincronização de dados inicial](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-INITIAL-DATA-SYNC)
+ [29.4.6. Combinando vários filtros de linha](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-COMBINING)
+ [29.4.7. Exemplos](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-EXAMPLES)

* [29.5. Listas de Colunas](logical-replication-col-lists.md)

+ [29.5.1. Exemplos](logical-replication-col-lists.md#LOGICAL-REPLICATION-COL-LIST-EXAMPLES)

* [29.6. Replicação de Coluna Gerada](logical-replication-gencols.md)
* [29.7. Conflitos](logical-replication-conflicts.md)
* [29.8. Restrições](logical-replication-restrictions.md)
* [29.9. Arquitetura](logical-replication-architecture.md)

+ [29.9.1. Instantâneo inicial](logical-replication-architecture.md#LOGICAL-REPLICATION-SNAPSHOT)

* [29.10. Monitoramento](logical-replication-monitoring.md)
* [29.11. Segurança](logical-replication-security.md)
* [29.12. Configurações de configuração](logical-replication-config.md)

+ [29.12.1. Editores](logical-replication-config.md#LOGICAL-REPLICATION-CONFIG-PUBLISHER)
+ [29.12.2. Assinantes](logical-replication-config.md#LOGICAL-REPLICATION-CONFIG-SUBSCRIBER)

* [29.13. Atualizar](logical-replication-upgrade.md)

+ [29.13.1. Prepare-se para atualizações do Publisher][(logical-replication-upgrade.md#PREPARE-PUBLISHER-UPGRADES)
+ [29.13.2. Prepare-se para atualizações do assinante][(logical-replication-upgrade.md#PREPARE-SUBSCRIBER-UPGRADES)
+ [29.13.3. Atualize os clusters de replicação lógica][(logical-replication-upgrade.md#UPGRADING-LOGICAL-REPLICATION-CLUSTERS)

* [29.14. Configuração Rápida](logical-replication-quick-setup.md)

A replicação lógica é um método de replicação de objetos de dados e suas alterações, com base em sua identidade de replicação (geralmente uma chave primária). Usamos o termo lógico em contraste com a replicação física, que utiliza endereços exatos de bloco e replicação de byte por byte. O PostgreSQL suporta ambos os mecanismos simultaneamente, veja [Capítulo 26](high-availability.md). A replicação lógica permite controle fino tanto sobre a replicação de dados quanto sobre a segurança.

A replicação lógica utiliza um modelo de *publicar* e *subscrição* com um ou mais *subscritores* que se submetem a uma ou mais *publicações* em um nó *editor*. Os assinantes obtêm dados das publicações às quais se submetem e, posteriormente, podem republicar os dados para permitir a replicação em cascata ou configurações mais complexas.

Quando a replicação lógica de uma tabela geralmente começa, o PostgreSQL tira um instantâneo dos dados da tabela no banco de dados do emissor e os copia para o assinante. Uma vez concluída, as alterações no emissor desde a cópia inicial são enviadas continuamente para o assinante. O assinante aplica os dados na mesma ordem que o emissor, para garantir a consistência transacional para publicações dentro de uma única assinatura. Esse método de replicação de dados é às vezes referido como replicação transacional.

Os casos típicos de uso para replicação lógica são:

* Enviar alterações incrementais em um único banco de dados ou um subconjunto de um banco de dados para os assinantes à medida que ocorrem.
* Executar gatilhos para alterações individuais à medida que chegam ao assinante.
* Consolidar vários bancos de dados em um único (por exemplo, para fins analíticos).
* Replicar entre diferentes versões principais do PostgreSQL.
* Replicar entre instâncias do PostgreSQL em diferentes plataformas (por exemplo, Linux para Windows).
* Dar acesso aos dados replicados a diferentes grupos de usuários.
* Compartilhar um subconjunto do banco de dados entre vários bancos de dados.

O banco de dados de assinantes se comporta da mesma maneira que qualquer outra instância do PostgreSQL e pode ser usado como um publicador para outros bancos de dados, definindo suas próprias publicações. Quando o assinante é tratado como de leitura somente por uma aplicação, não haverá conflitos de uma única assinatura. Por outro lado, se houver outras escritas feitas por uma aplicação ou por outros assinantes para o mesmo conjunto de tabelas, conflitos podem surgir.