## Capítulo 51. Visão geral dos recursos internos do PostgreSQL

**Índice**

* [51.1. O Caminho de uma Consulta](query-path.md)
* [51.2. Como as Conexões São Estabelecidas](connect-estab.md)
* [51.3. A Fase do Parser](parser-stage.md)

+ [51.3.1. Parser](parser-stage.md#PARSER-STAGE-PARSER)
+ [51.3.2. Processo de Transformação](parser-stage.md#PARSER-STAGE-TRANSFORMATION-PROCESS)

* [51.4. Sistema de Regras do PostgreSQL](rule-system.md)
* [51.5. Planejador/Otimizador](planner-optimizer.md)

+ [51.5.1. Gerando Planos Possíveis](planner-optimizer.md#PLANNER-OPTIMIZER-GENERATING-POSSIBLE-PLANS)

* [51.6. Executor](executor.md)

### Autor

Este capítulo teve origem como parte da dissertação de mestrado de Stefan Simkovics, preparada na Universidade de Tecnologia de Viena sob a direção do O.Univ.Prof.Dr. Georg Gottlob e Univ.Ass. Mag. Katrin Seyr.

Este capítulo fornece uma visão geral da estrutura interna do backend do PostgreSQL. Após ler as seções a seguir, você deve ter uma ideia de como uma consulta é processada. Este capítulo visa ajudar o leitor a entender a sequência geral das operações que ocorrem dentro do backend, desde o ponto em que uma consulta é recebida até o ponto em que os resultados são devolvidos ao cliente.