## 15.3. Planos paralelos [#](#PARALLEL-PLANS)

* [15.3.1. Estradas paralelas](parallel-plans.md#PARALLEL-SCANS)
* [15.3.2. Conexões paralelas](parallel-plans.md#PARALLEL-JOINS)
* [15.3.3. Agregação paralela](parallel-plans.md#PARALLEL-AGGREGATION)
* [15.3.4. Aplicação paralela](parallel-plans.md#PARALLEL-APPEND)
* [15.3.5. Dicas de plano paralelo](parallel-plans.md#PARALLEL-PLAN-TIPS)

Como cada trabalhador executa a porção paralela do plano até o fim, não é possível simplesmente tomar um plano de consulta comum e executá-lo usando vários trabalhadores. Cada trabalhador produzirá uma cópia completa do conjunto de resultados de saída, portanto, a consulta não correrá mais rápido do que o normal, mas produzirá resultados incorretos. Em vez disso, a porção paralela do plano deve ser o que é conhecido internamente pelo otimizador de consultas como um *plano parcial*; ou seja, deve ser construído de modo que cada processo que executa o plano gere apenas um subconjunto das linhas de saída, de tal forma que cada linha de saída necessária seja garantida para ser gerada exatamente por um dos processos cooperativos. Geralmente, isso significa que a varredura na tabela de condução da consulta deve ser uma varredura consciente de paralelo.

### 15.3.1. Análises paralelas [#](#PARALLEL-SCANS)

Os seguintes tipos de varreduras de tabela sensíveis ao paralelismo são atualmente suportados.

* Em uma *varredura sequencial paralela*, os blocos da tabela serão divididos em faixas e compartilhados entre os processos cooperantes. Cada processo trabalhador completará a varredura de sua faixa específica de blocos antes de solicitar uma faixa adicional de blocos.
* Em uma *varredura de heap de bitmap paralela*, um processo é escolhido como líder. Esse processo realiza uma varredura em um ou mais índices e constrói uma bitmap indicando quais blocos da tabela precisam ser visitados. Esses blocos são então divididos entre os processos cooperantes, como em uma varredura sequencial paralela. Em outras palavras, a varredura do heap é realizada em paralelo, mas a varredura do índice subjacente não é.
* Em uma *varredura de índice paralela* ou *varredura apenas de índice paralela*, os processos cooperantes se revezam lendo dados do índice. Atualmente, varreduras de índice paralelas são suportadas apenas para índices btree. Cada processo reivindicará um único bloco de índice e fará a varredura e retornará todos os tuplos referenciados por esse bloco; outros processos podem, ao mesmo tempo, estar retornando tuplos de um bloco de índice diferente. Os resultados de uma varredura btree paralela são retornados em ordem ordenada dentro de cada processo trabalhador.

Outros tipos de varredura, como varreduras de índices não de btree, podem suportar varreduras paralelas no futuro.

### 15.3.2. Conexões paralelas [#](#PARALLEL-JOINS)

Assim como em um plano não paralelo, a tabela de condução pode ser associada a uma ou mais outras tabelas usando um loop aninhado, junção hash ou junção de fusão. O lado interno da junção pode ser qualquer tipo de plano não paralelo que seja de outra forma suportado pelo planejador, desde que seja seguro executar dentro de um trabalhador paralelo. Dependendo do tipo de junção, o lado interno também pode ser um plano paralelo.

* Em uma junção de *loop aninhado*, o lado interno é sempre não paralelo. Embora seja executado na íntegra, isso é eficiente se o lado interno for uma varredura de índice, porque os tuplos externos e, portanto, os loops que procuram valores no índice são divididos entre os processos cooperativos.
* Em uma *junção de *merge*, o lado interno é sempre um plano não paralelo e, portanto, executado na íntegra. Isso pode ser ineficiente, especialmente se uma ordenação precisar ser realizada, porque o trabalho e os dados resultantes são duplicados em cada processo cooperativo.
* Em uma *junção de *hash* (sem o prefixo "paralelo"), o lado interno é executado na íntegra por todos os processos cooperativos para construir cópias idênticas da tabela hash. Isso pode ser ineficiente se a tabela hash for grande ou o plano for caro. Em uma *junção de *hash paralela*, o lado interno é um *hash paralelo* que divide o trabalho de construção de uma tabela hash compartilhada entre os processos cooperativos.

### 15.3.3. Aglomeração Paralela [#](#PARALLEL-AGGREGATION)

O PostgreSQL suporta agregação paralela ao agregação em duas etapas. Primeiro, cada processo que participa da parte paralela da consulta realiza uma etapa de agregação, produzindo um resultado parcial para cada grupo do qual esse processo está ciente. Isso é refletido no plano como um nó `Partial Aggregate`. Em segundo lugar, os resultados parciais são transferidos para o líder via `Gather` ou `Gather Merge`. Finalmente, o líder re-agrega os resultados em todos os trabalhadores para produzir o resultado final. Isso é refletido no plano como um nó `Finalize Aggregate`.

Como o nó `Finalize Aggregate` funciona no processo líder, as consultas que produzem um número relativamente grande de grupos em comparação ao número de linhas de entrada aparecerão menos favoráveis ao planejador de consultas. Por exemplo, no pior cenário, o número de grupos vistos pelo nó `Finalize Aggregate` pode ser tão grande quanto o número de linhas de entrada que foram vistas por todos os processos de trabalho na etapa `Partial Aggregate`. Para esses casos, é claro que não haverá nenhum benefício de desempenho ao usar agregação paralela. O planejador de consultas leva isso em consideração durante o processo de planejamento e é improvável que escolha agregação paralela nesse cenário.

A agregação paralela não é suportada em todas as situações. Cada agregado deve ser [seguro](parallel-safety.md) para o paralelismo e deve ter uma função de combinação. Se o agregado tiver um estado de transição do tipo `internal`, deve ter funções de serialização e deserialização. Consulte [CREATE AGGREGATE](sql-createaggregate.md) para mais detalhes. A agregação paralela não é suportada se qualquer chamada de função agregada contiver a cláusula `DISTINCT` ou `ORDER BY` e também não é suportada para agregados de conjuntos ordenados ou quando a consulta envolve `GROUPING SETS`. Pode ser usada apenas quando todas as junções envolvidas na consulta também fazem parte da porção paralela do plano.

### 15.3.4. Apêndice paralelo [#](#PARALLEL-APPEND)

Sempre que o PostgreSQL precisa combinar linhas de várias fontes em um único conjunto de resultados, ele usa um nó de plano `Append` ou `MergeAppend`. Isso geralmente acontece ao implementar `UNION ALL` ou ao digitalizar uma tabela particionada. Esses nós podem ser usados em planos paralelos da mesma forma que em qualquer outro plano. No entanto, em um plano paralelo, o planejador pode, em vez disso, usar um nó `Parallel Append`.

Quando um nó `Append` é usado em um plano paralelo, cada processo executará os planos filhos na ordem em que aparecem, de modo que todos os processos participantes cooperem para executar o primeiro plano filho até que ele esteja completo e, em seguida, passem para o segundo plano em torno do mesmo tempo. Quando, em vez disso, é usado um `Parallel Append`, o executor, em vez disso, espalhará os processos participantes o mais uniformemente possível em seus planos filhos, de modo que vários planos filhos sejam executados simultaneamente. Isso evita a contenção e também evita pagar o custo inicial de um plano filho nos processos que nunca o executam.

Além disso, ao contrário de um nó `Append` comum, que só pode ter filhos parciais quando usado em um plano paralelo, um nó `Parallel Append` pode ter planos de filhos tanto parciais quanto não parciais. Os filhos não parciais serão analisados por apenas um único processo, pois analisar-os mais de uma vez produziria resultados duplicados. Portanto, os planos que envolvem a adição de vários conjuntos de resultados podem alcançar paralelismo grosseiro mesmo quando planos parciais eficientes não estão disponíveis. Por exemplo, considere uma consulta contra uma tabela particionada que só pode ser implementada de forma eficiente usando um índice que não suporte varreduras paralelas. O planejador pode optar por um `Parallel Append` de planos regulares `Index Scan`; cada varredura de índice individual teria que ser executada até o término por um único processo, mas diferentes varreduras poderiam ser realizadas ao mesmo tempo por diferentes processos.

[enable_parallel_append](runtime-config-query.md#GUC-ENABLE-PARALLEL-APPEND) pode ser usado para desabilitar este recurso.

### 15.3.5. Dicas para o Plano Paralelo [#](#PARALLEL-PLAN-TIPS)

Se uma consulta que se espera que faça isso não produzir um plano paralelo, você pode tentar reduzir [parallel_setup_cost](runtime-config-query.md#GUC-PARALLEL-SETUP-COST) ou [parallel_tuple_cost](runtime-config-query.md#GUC-PARALLEL-TUPLE-COST). Claro, este plano pode se mostrar mais lento do que o plano serial que o planejador preferiu, mas isso nem sempre será o caso. Se você não obtiver um plano paralelo mesmo com valores muito pequenos desses ajustes (por exemplo, após configurá-los ambos para zero), pode haver algum motivo pelo qual o planejador de consultas não consegue gerar um plano paralelo para sua consulta. Consulte [Seção 15.2](when-can-parallel-query-be-used.md "15.2. When Can Parallel Query Be Used?") e [Seção 15.4](parallel-safety.md "15.4. Parallel Safety") para informações sobre por que isso pode ser o caso.

Ao executar um plano paralelo, você pode usar `EXPLAIN (ANALYZE, VERBOSE)` para exibir estatísticas por trabalhador para cada nó do plano. Isso pode ser útil para determinar se o trabalho está sendo distribuído de forma uniforme entre todos os nós do plano e, de forma mais geral, para entender as características de desempenho do plano.