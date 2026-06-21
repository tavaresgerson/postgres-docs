## Capítulo 13. Controle de Concorrência

**Índice**

* [13.1. Introdução](mvcc-intro.md)
* [13.2. Isolamento de Transação](transaction-iso.md)

+ [13.2.1. Nível de Isolamento de Leitura Comprometido](transaction-iso.md#XACT-READ-COMMITTED)
+ [13.2.2. Nível de Leitura Repetível](transaction-iso.md#XACT-REPEATABLE-READ)
+ [13.2.3. Nível de Isolamento Serializável](transaction-iso.md#XACT-SERIALIZABLE)

* [13.3. Fechamento explícito](explicit-locking.md)

+ [13.3.1. Lâminas de bloqueio de nível de tabela](explicit-locking.md#LOCKING-TABLES)
+ [13.3.2. Lâminas de bloqueio de nível de linha](explicit-locking.md#LOCKING-ROWS)
+ [13.3.3. Lâminas de bloqueio de nível de página](explicit-locking.md#LOCKING-PAGES)
+ [13.3.4. Deadlocks](explicit-locking.md#LOCKING-DEADLOCKS)
+ [13.3.5. Lâminas de aconselhamento](explicit-locking.md#ADVISORY-LOCKS)

* [13.4. Verificação de Consistência de Dados no Nível da Aplicação](applevel-consistency.md)

+ [13.4.1. Exigir consistência com transações serializáveis][(applevel-consistency.md#SERIALIZABLE-CONSISTENCY)]
+ [13.4.2. Exigir consistência com bloqueios explícitos][(applevel-consistency.md#NON-SERIALIZABLE-CONSISTENCY)]

* [13.5. Tratamento de falha de serialização](mvcc-serialization-failure-handling.md)
* [13.6. Observações](mvcc-caveats.md)
* [13.7. Acionamento e índices](locking-indexes.md)

Este capítulo descreve o comportamento do sistema de banco de dados PostgreSQL quando duas ou mais sessões tentam acessar os mesmos dados ao mesmo tempo. Os objetivos nessa situação são permitir o acesso eficiente para todas as sessões, mantendo a integridade dos dados rigorosa. Todo desenvolvedor de aplicativos de banco de dados deve estar familiarizado com os tópicos abordados neste capítulo.