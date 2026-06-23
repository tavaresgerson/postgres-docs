## 29.9. Arquitetura [#](#LOGICAL-REPLICATION-ARCHITECTURE)

* [29.9.1. Instantâneo inicial](logical-replication-architecture.md#LOGICAL-REPLICATION-SNAPSHOT)

A replicação lógica é construída com uma arquitetura semelhante à replicação de fluxo físico (consulte [Seção 26.2.5](warm-standby.md#STREAMING-REPLICATION)). É implementada pelos processos `walsender` e `apply`. O processo walsender inicia a decodificação lógica (descrita em [Capítulo 47](logicaldecoding.md)) do WAL e carrega o plugin padrão de saída de decodificação lógica (`pgoutput`). O plugin transforma as alterações lidas do WAL no protocolo de replicação lógica (consulte [Seção 54.5](protocol-logical-replication.md)) e filtra os dados de acordo com a especificação de publicação. Os dados são então transferidos continuamente usando o protocolo de replicação de fluxo para o trabalhador de aplicação, que mapeia os dados para tabelas locais e aplica as alterações individuais à medida que são recebidas, em ordem transacional correta.

O processo de aplicação no banco de dados do assinante sempre é executado com `session_replication_role` definido como (runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE) e `replica`. Isso significa que, por padrão, os gatilhos e regras não serão acionados em um assinante. Os usuários podem optar por habilitar gatilhos e regras em uma tabela usando o comando `ALTER TABLE` e as cláusulas `ENABLE TRIGGER` e `ENABLE RULE`.

O processo de replicação lógica atualmente só aciona gatilhos de linha, não gatilhos de declaração. A sincronização inicial da tabela, no entanto, é implementada como um comando `COPY` e, portanto, aciona gatilhos de linha e de declaração para `INSERT`.

### 29.9.1. Instantâneo inicial [#](#LOGICAL-REPLICATION-SNAPSHOT)

Os dados iniciais das tabelas já subscritas são capturados e copiados em instâncias paralelas de um tipo especial de processo de aplicação. Esses processos de sincronização de tabelas especiais são trabalhadores dedicados à sincronização de tabelas, gerados para cada tabela a ser sincronizada. Cada processo de sincronização de tabela criará seu próprio slot de replicação e copiará os dados existentes. Assim que a cópia for concluída, o conteúdo da tabela se tornará visível para outros backends. Uma vez que os dados existentes forem copiados, o trabalhador entrará no modo de sincronização, o que garante que a tabela seja trazida a um estado sincronizado com o processo de aplicação principal, ao transmitir quaisquer alterações que ocorreram durante a cópia dos dados iniciais usando replicação lógica padrão. Durante essa fase de sincronização, as alterações são aplicadas e comprometidas na mesma ordem em que ocorreram no publicador. Uma vez concluída a sincronização, o controle da replicação da tabela é devolvido ao processo de aplicação principal, onde a replicação continua normalmente.

Nota

O parâmetro da publicação `publish`(sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH) afeta apenas quais operações de DML serão replicadas. A sincronização inicial de dados não leva em conta este parâmetro ao copiar os dados da tabela existente.

Nota

Se um trabalhador de sincronização de tabela falhar durante a cópia, o trabalhador de aplicação detecta o erro e refaz o trabalhador de sincronização de tabela para continuar o processo de sincronização. Esse comportamento garante que os erros transitórios não interrompam permanentemente a configuração de replicação. Veja também `wal_retrieve_retry_interval`(runtime-config-replication.md#GUC-WAL-RETRIEVE-RETRY-INTERVAL).