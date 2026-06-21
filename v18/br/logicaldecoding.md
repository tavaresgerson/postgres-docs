## Capítulo 47. Decodificação Lógica

**Índice**

* [47.1. Exemplos de Decodificação Lógica][(logicaldecoding-example.md)
* [47.2. Conceitos de Decodificação Lógica][(logicaldecoding-explanation.md)

+ [47.2.1. Decodificação Lógica][(logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-LOG-DEC)]
+ [47.2.2. Fendas de Replicação][(logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS)]
+ [47.2.3. Sincronização da Fenda de Replicação][(logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION)]
+ [47.2.4. Plugins de Saída][(logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-OUTPUT-PLUGINS)]
+ [47.2.5. Instantâneos Exportados][(logicaldecoding-explanation.md#LOGICALDECODING-EXPLANATION-EXPORTED-SNAPSHOTS)]

* [47.3. Protocolo de Replicação de Streaming](logicaldecoding-walsender.md)
* [47.4. Interface de Decodificação Lógica SQL](logicaldecoding-sql.md)
* [47.5. Catálogos do Sistema Relacionados à Decodificação Lógica](logicaldecoding-catalogs.md)
* [47.6. Plugins de Saída de Decodificação Lógica](logicaldecoding-output-plugin.md)

+ [47.6.1. Função de Inicialização][(logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-INIT)]
+ [47.6.2. Capacidades][(logicaldecoding-output-plugin.md#LOGICALDECODING-CAPABILITIES)]
+ [47.6.3. Modos de Saída][(logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-MODE)]
+ [47.6.4. Chamadas de Retorno de Plugin de Saída][(logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-PLUGIN-CALLBACKS)]
+ [47.6.5. Funções para Produzir Saída][(logicaldecoding-output-plugin.md#LOGICALDECODING-OUTPUT-PLUGIN-OUTPUT)]

* [47.7. Escritores de Saída de Decodificação Lógica](logicaldecoding-writer.md)
* [47.8. Suporte a Replicação Síncrona para Decodificação Lógica](logicaldecoding-synchronous.md)

+ [47.8.1. Visão geral](logicaldecoding-synchronous.md#LOGICALDECODING-SYNCHRONOUS-OVERVIEW)
+ [47.8.2. Observações](logicaldecoding-synchronous.md#LOGICALDECODING-SYNCHRONOUS-CAVEATS)

* [47.9. Streaming de Grandes Transações para Decodificação Lógica](logicaldecoding-streaming.md)
* [47.10. Suporte a Compromisso de Duas Fases para Decodificação Lógica](logicaldecoding-two-phase-commits.md)

O PostgreSQL fornece infraestrutura para transmitir as modificações realizadas via SQL para consumidores externos. Essa funcionalidade pode ser usada para uma variedade de propósitos, incluindo soluções de replicação e auditoria.

As alterações são enviadas em fluxos identificados por intervalos de replicação lógica.

O formato no qual essas alterações são transmitidas é determinado pelo plugin de saída utilizado. Um exemplo de plugin é fornecido na distribuição do PostgreSQL. Plugins adicionais podem ser escritos para ampliar a escolha dos formatos disponíveis sem modificar qualquer código central. Cada plugin de saída tem acesso a cada nova linha individual produzida por `INSERT` e à nova versão da linha criada por `UPDATE`. A disponibilidade das versões antigas das linhas para `UPDATE` e `DELETE` depende da identidade da replica configurada (consulte [`REPLICA IDENTITY`](sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY)).

As alterações podem ser consumidas utilizando o protocolo de replicação em streaming (consulte [Seção 54.4] [(protocol-replication.md "54.4. Streaming Replication Protocol")] e [Seção 47.3] [(logicaldecoding-walsender.md "47.3. Streaming Replication Protocol Interface")]) ou chamando funções via SQL (consulte [Seção 47.4] [(logicaldecoding-sql.md "47.4. Logical Decoding SQL Interface")]). Também é possível escrever métodos adicionais para consumir a saída de um slot de replicação sem modificar o código principal (consulte [Seção 47.7] [(logicaldecoding-writer.md "47.7. Logical Decoding Output Writers")]).