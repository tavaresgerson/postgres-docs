## 19.7. Planejamento de consultas [#](#RUNTIME-CONFIG-QUERY)

* [19.7.1. Configuração do Método de Planejamento](runtime-config-query.md#RUNTIME-CONFIG-QUERY-ENABLE)
* [19.7.2. Constantes de Custo do Planejador](runtime-config-query.md#RUNTIME-CONFIG-QUERY-CONSTANTS)
* [19.7.3. Otimizador de Consulta Genética](runtime-config-query.md#RUNTIME-CONFIG-QUERY-GEQO)
* [19.7.4. Outras Opções do Planejador](runtime-config-query.md#RUNTIME-CONFIG-QUERY-OTHER)

### 19.7.1. Configuração do Método Planejador [#](#RUNTIME-CONFIG-QUERY-ENABLE)

Esses parâmetros de configuração fornecem um método rudimentar para influenciar os planos de consulta escolhidos pelo otimizador de consultas. Se o plano padrão escolhido pelo otimizador para uma consulta específica não for ótimo, uma solução *temporária* é usar um desses parâmetros de configuração para forçar o otimizador a escolher um plano diferente. Melhores maneiras de melhorar a qualidade dos planos escolhidos pelo otimizador incluem ajustar as constantes de custo do planejador (consulte [Seção 19.7.2](runtime-config-query.md#RUNTIME-CONFIG-QUERY-CONSTANTS)], executar manualmente [`ANALYZE`](sql-analyze.md)], aumentar o valor do parâmetro de configuração [default_statistics_target](runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET) e aumentar a quantidade de estatísticas coletadas para colunas específicas usando `ALTER TABLE SET STATISTICS`.

`enable_async_append` (`boolean`) [#](#GUC-ENABLE-ASYNC-APPEND): Habilita ou desabilita o uso de tipos de plano de anexação sensíveis ao async pelo planejador de consulta. O padrão é `on`.

`enable_bitmapscan` (`boolean`) [#](#GUC-ENABLE-BITMAPSCAN): Habilita ou desabilita o uso de tipos de planos de varredura de mapa de bits pelo planejador de consulta. O padrão é `on`.

`enable_distinct_reordering` (`boolean`) [#](#GUC-ENABLE-DISTINCT-REORDERING): Habilita ou desabilita a capacidade do planejador de consulta de reorganizar as chaves DISTINCT para corresponder às chaves de caminho do caminho de entrada. O padrão é `on`.

`enable_gathermerge` (`boolean`) [#](#GUC-ENABLE-GATHERMERGE): Habilita ou desabilita o uso de tipos de plano de junção de coleta pelo planejador de consulta. O padrão é `on`.

`enable_group_by_reordering` (`boolean`) [#](#GUC-ENABLE-GROUPBY-REORDERING): Controla se o planejador de consulta produzirá um plano que fornecerá chaves `GROUP BY` ordenadas na ordem das chaves de um nó filho do plano, como uma varredura de índice. Quando desativado, o planejador de consulta produzirá um plano com chaves `GROUP BY` apenas ordenadas para corresponder à cláusula `ORDER BY`, se houver. Quando ativado, o planejador tentará produzir um plano mais eficiente. O valor padrão é `on`.

`enable_hashagg` (`boolean`) [#](#GUC-ENABLE-HASHAGG): Habilita ou desabilita o uso de tipos de plano de agregação com hash pelo planejador de consulta. O padrão é `on`.

`enable_hashjoin` (`boolean`) [#](#GUC-ENABLE-HASHJOIN): Habilita ou desabilita o uso de tipos de planos de junção de hash pelo planejador de consultas. O padrão é `on`.

`enable_incremental_sort` (`boolean`) [#](#GUC-ENABLE-INCREMENTAL-SORT): Habilita ou desabilita o uso de etapas de classificação incremental pelo planejador de consulta. O padrão é `on`.

`enable_indexscan` (`boolean`) [#](#GUC-ENABLE-INDEXSCAN): Habilita ou desabilita o uso do planejador de consulta dos tipos de plano de varredura de índice e varredura apenas de índice. O padrão é `on`. Veja também [enable_indexonlyscan](runtime-config-query.md#GUC-ENABLE-INDEXONLYSCAN).

`enable_indexonlyscan` (`boolean`) [#](#GUC-ENABLE-INDEXONLYSCAN): Habilita ou desabilita o uso do planejador de consulta de tipos de plano que utilizam apenas índices (consulte [Seção 11.9] (indexes-index-only-scans.md "11.9. Index-Only Scans and Covering Indexes")). O padrão é `on`. A configuração [enable_indexscan](runtime-config-query.md#GUC-ENABLE-INDEXSCAN) também deve ser habilitada para que o planejador de consulta considere varreduras de apenas índices.

`enable_material` (`boolean`) [#](#GUC-ENABLE-MATERIAL): Habilita ou desabilita o uso de materialização pelo planejador de consulta. É impossível suprimir a materialização completamente, mas desligar essa variável impede que o planejador insira nós materializados, exceto nos casos em que isso é necessário para a correção. O padrão é `on`.

`enable_memoize` (`boolean`) [#](#GUC-ENABLE-MEMOIZE): Habilita ou desabilita o uso do planejador de consulta para memorizar planos de cache para o armazenamento de resultados de varreduras parametrizadas em junções de laço aninhado. Esse tipo de plano permite que as varreduras nos planos subjacentes sejam ignoradas quando os resultados dos parâmetros atuais já estão no cache. Resultados menos frequentemente pesquisados podem ser expulsos do cache quando é necessário mais espaço para novas entradas. O padrão é `on`.

`enable_mergejoin` (`boolean`) [#](#GUC-ENABLE-MERGEJOIN): Habilita ou desabilita o uso de tipos de planos de junção por mesclagem pelo planejador de consulta. O padrão é `on`.

`enable_nestloop` (`boolean`) [#](#GUC-ENABLE-NESTLOOP): Habilita ou desabilita o uso de planos de junção de laço aninhado pelo planejador de consulta. É impossível suprimir completamente as junções de laço aninhado, mas desligar essa variável desencoraja o planejador de usá-la se houver outros métodos disponíveis. O padrão é `on`.

`enable_parallel_append` (`boolean`) [#](#GUC-ENABLE-PARALLEL-APPEND): Habilita ou desabilita o uso de tipos de plano de anexação sensíveis a paralelismo pelo planejador de consulta. O padrão é `on`.

`enable_parallel_hash` (`boolean`) [#](#GUC-ENABLE-PARALLEL-HASH): Habilita ou desabilita o uso do planejador de consulta de tipos de plano de junção de hash com hash em paralelo. Não tem efeito se os planos de junção de hash não forem também habilitados. O padrão é `on`.

`enable_partition_pruning` (`boolean`) [#](#GUC-ENABLE-PARTITION-PRUNING): Habilita ou desabilita a capacidade do planejador de consultas de eliminar as partições de uma tabela particionada dos planos de consulta. Isso também controla a capacidade do planejador de gerar planos de consulta que permitam ao executor da consulta remover (ignorar) as partições durante a execução da consulta. O padrão é `on`. Veja [Seção 5.12.4](ddl-partitioning.md#DDL-PARTITION-PRUNING "5.12.4. Partition Pruning") para detalhes.

`enable_partitionwise_join` (`boolean`) [#](#GUC-ENABLE-PARTITIONWISE-JOIN): Habilita ou desabilita o uso do planejador de consulta de junção partição por partição, que permite que uma junção entre tabelas particionadas seja realizada por meio da junção das partições correspondentes. A junção partição atualmente se aplica apenas quando as condições de junção incluem todos os índices de partição, que devem ser do mesmo tipo de dados e ter conjuntos de partições filhas que correspondam um a um. Com este ajuste habilitado, o número de nós cuja utilização de memória é restringida por `work_mem` que aparecem no plano final pode aumentar linearmente de acordo com o número de partições que estão sendo verificadas. Isso pode resultar em um grande aumento no consumo total de memória durante a execução da consulta. O planejamento de consulta também se torna significativamente mais caro em termos de memória e CPU. O valor padrão é `off`.

`enable_partitionwise_aggregate` (`boolean`) [#](#GUC-ENABLE-PARTITIONWISE-AGGREGATE): Habilita ou desabilita o uso do planejador de consulta do agrupamento ou agregação por partição, o que permite que o agrupamento ou agregação em tabelas particionadas sejam realizados separadamente para cada partição. Se a cláusula `GROUP BY` não incluir as chaves de partição, apenas a agregação parcial pode ser realizada por partição, e a finalização deve ser realizada posteriormente. Com este ajuste habilitado, o número de nós cuja utilização de memória é restringida por `work_mem` que aparecem no plano final pode aumentar linearmente de acordo com o número de partições que estão sendo verificadas. Isso pode resultar em um grande aumento no consumo total de memória durante a execução da consulta. O planejamento de consulta também se torna significativamente mais caro em termos de memória e CPU. O valor padrão é `off`.

`enable_presorted_aggregate` (`boolean`) [#](#GUC-ENABLE-PRESORTED-AGGREGATE): Controla se o planejador de consulta produzirá um plano que fornecerá linhas que estão pré-ordenadas na ordem necessária para as funções agregadas `ORDER BY` / `DISTINCT` da consulta. Quando desativado, o planejador de consulta produzirá um plano que sempre exigirá que o executor realize uma ordenação antes de realizar a agregação de cada função agregada que contenha uma cláusula `ORDER BY` ou `DISTINCT`. Quando ativado, o planejador tentará produzir um plano mais eficiente que forneça entrada para as funções agregadas que estão pré-ordenadas na ordem que elas requerem para a agregação. O valor padrão é `on`.

`enable_self_join_elimination` (`boolean`) [#](#GUC-ENABLE-SELF-JOIN-ELIMINATION): Habilita ou desabilita a otimização do planejador de consulta, que analisa a árvore de consulta e substitui as autoconjuntos por varreduras únicas semânticamente equivalentes. Considera apenas tabelas comuns. O padrão é `on`.

`enable_seqscan` (`boolean`) [#](#GUC-ENABLE-SEQSCAN): Habilita ou desabilita o uso de tipos de planos de varredura sequencial pelo planejador de consultas. É impossível suprimir varreduras sequenciais completamente, mas desligar essa variável desencoraja o planejador de usá-las se houver outros métodos disponíveis. O padrão é `on`.

`enable_sort` (`boolean`) [#](#GUC-ENABLE-SORT): Habilita ou desabilita o uso do planejador de consulta de etapas de ordenação explícitas. É impossível suprimir completamente os ordenamentos explícitos, mas desligar essa variável desencoraja o planejador de usá-los se houver outros métodos disponíveis. O padrão é `on`.

`enable_tidscan` (`boolean`) [#](#GUC-ENABLE-TIDSCAN): Habilita ou desabilita o uso dos tipos de plano de varredura TID pelo planejador de consulta. O padrão é `on`.

### 19.7.2. Constantes de custo do planejador [#](#RUNTIME-CONFIG-QUERY-CONSTANTS)

As variáveis de *custo* descritas nesta seção são medidas em uma escala arbitrária. Apenas seus valores relativos importam, portanto, escalá-las todas para cima ou para baixo pelo mesmo fator não resultará em nenhuma mudança nas escolhas do planejador. Por padrão, essas variáveis de custo são baseadas no custo de buscas sequenciais de página; ou seja, `seq_page_cost` é convencionalmente definido como `1.0` e as outras variáveis de custo são definidas com referência a isso. Mas você pode usar uma escala diferente se preferir, como tempos de execução reais em milissegundos em uma máquina específica.

### Nota

Infelizmente, não há um método bem definido para determinar os valores ideais para as variáveis de custo. Eles são melhor tratados como médias sobre toda a mistura de consultas que uma instalação específica receberá. Isso significa que mudá-los com base apenas em alguns experimentos é muito arriscado.

`seq_page_cost` (`floating point`) [#](#GUC-SEQ-PAGE-COST): Define a estimativa do planejador do custo de uma página de disco que faz parte de uma série de buscas sequenciais. O padrão é 1,0. Esse valor pode ser sobrescrito para tabelas e índices em um espaço de tabelas específico, definindo o parâmetro do espaço de tabelas com o mesmo nome (consulte [ALTER TABLESPACE](sql-altertablespace.md "ALTER TABLESPACE")).

`random_page_cost` (`floating point`) [#](#GUC-RANDOM-PAGE-COST): Define a estimativa do planejador do custo de uma página de disco não sequencialmente obtida. O padrão é 4,0. Esse valor pode ser sobrescrito para tabelas e índices em um espaço de tabelas específico, definindo o parâmetro do espaço de tabelas com o mesmo nome (consulte [ALTER TABLESPACE](sql-altertablespace.md "ALTER TABLESPACE")).

Reduzir esse valor em relação a `seq_page_cost` fará com que o sistema prefira varreduras de índice; aumentar esse valor fará com que as varreduras de índice pareçam relativamente mais caras. Você pode aumentar ou diminuir ambos os valores juntos para alterar a importância dos custos de E/S do disco em relação aos custos da CPU, que são descritos pelos seguintes parâmetros.

O acesso aleatório a armazenamento durável normalmente é muito mais caro do que o acesso sequencial quatro vezes. No entanto, uma taxa de taxa menor é usada (4,0) porque se assume que a maioria dos acessos aleatórios ao armazenamento, como leituras indexadas, estão na cache. Além disso, a latência do armazenamento conectado à rede tende a reduzir o custo relativo do acesso aleatório.

Se você acredita que o armazenamento de cache é menos frequente do que o valor padrão reflete, e a latência da rede é mínima, você pode aumentar o random_page_cost para refletir melhor o verdadeiro custo das leituras de armazenamento aleatórias. O armazenamento que tem um custo de leitura aleatória mais alto em relação à seqüencial, como discos magnéticos, também pode ser melhor modelado com um valor mais alto para random_page_cost. Da mesma forma, se seus dados provavelmente estarão completamente em cache, como quando o banco de dados é menor que a memória total do servidor, ou a latência da rede é alta, pode ser apropriado diminuir o random_page_cost.

### DICA

Embora o sistema permita que você defina `random_page_cost` para menos que `seq_page_cost`, não é sensato fazê-lo fisicamente. No entanto, definir-os iguais faz sentido se o banco de dados estiver totalmente cacheado na RAM, uma vez que, nesse caso, não há penalidade por tocar em páginas fora de sequência. Além disso, em um banco de dados fortemente cacheado, você deve diminuir ambos os valores em relação aos parâmetros da CPU, uma vez que o custo de buscar uma página já na RAM é muito menor do que o normal.

`cpu_tuple_cost` (`floating point`) [#](#GUC-CPU-TUPLE-COST): Define a estimativa do planejador do custo do processamento de cada linha durante uma consulta. O padrão é 0,01.

`cpu_index_tuple_cost` (`floating point`) [#](#GUC-CPU-INDEX-TUPLE-COST): Define a estimativa do planejador do custo de processamento de cada entrada de índice durante uma varredura de índice. O padrão é 0,005.

`cpu_operator_cost` (`floating point`) [#](#GUC-CPU-OPERATOR-COST): Define a estimativa do planejador do custo do processamento de cada operador ou função executada durante uma consulta. O padrão é 0,0025.

`parallel_setup_cost` (`floating point`) [#](#GUC-PARALLEL-SETUP-COST): Define a estimativa do planejador do custo de lançamento de processos de trabalhador paralelos. O padrão é 1000.

`parallel_tuple_cost` (`floating point`) [#](#GUC-PARALLEL-TUPLE-COST): Define a estimativa do planejador do custo de transferir uma tupla de um processo de trabalhador paralelo para outro processo. O padrão é 0,1.

`min_parallel_table_scan_size` (`integer`) [#](#GUC-MIN-PARALLEL-TABLE-SCAN-SIZE): Define a quantidade mínima de dados da tabela que deve ser analisada para que uma varredura paralela seja considerada. Para uma varredura sequencial paralela, a quantidade de dados da tabela analisada é sempre igual ao tamanho da tabela, mas quando índices são usados, a quantidade de dados da tabela analisada normalmente será menor. Se este valor for especificado sem unidades, ele é considerado em blocos, ou seja, `BLCKSZ` bytes, tipicamente 8 kB. O padrão é 8 megabytes (`8MB`).

`min_parallel_index_scan_size` (`integer`) [#](#GUC-MIN-PARALLEL-INDEX-SCAN-SIZE): Define a quantidade mínima de dados de índice que devem ser verificados para que uma verificação paralela seja considerada. Observe que uma verificação paralela de índice geralmente não atinge todo o índice; o número de páginas que o planejador acredita que serão realmente atingidas pelo scan é o que é relevante. Este parâmetro também é usado para decidir se um índice específico pode participar de um vácuo paralelo. Veja [VACUUM](sql-vacuum.md "VACUUM"). Se este valor for especificado sem unidades, ele é considerado em blocos, ou seja, `BLCKSZ` bytes, tipicamente 8 kB. O padrão é 512 kilobytes (`512kB`).

`effective_cache_size` (`integer`) [#](#GUC-EFFECTIVE-CACHE-SIZE): Define a suposição do planejador sobre o tamanho efetivo do cache de disco disponível para uma única consulta. Isso é considerado nas estimativas do custo de uso de um índice; um valor mais alto torna mais provável que sejam usados varreduras sequenciais, enquanto um valor mais baixo torna mais provável que sejam usados varreduras sequenciais. Ao definir este parâmetro, você deve considerar tanto os buffers compartilhados do PostgreSQL quanto a porção do cache de disco do kernel que será usada para os arquivos de dados do PostgreSQL, embora alguns dados possam existir em ambos os lugares. Além disso, leve em consideração o número esperado de consultas concorrentes em diferentes tabelas, pois elas terão que compartilhar o espaço disponível. Este parâmetro não afeta o tamanho da memória compartilhada alocada pelo PostgreSQL, nem reserva o cache de disco do kernel; ele é usado apenas para fins de estimativa. O sistema também não assume que os dados permanecem no cache de disco entre as consultas. Se este valor for especificado sem unidades, ele é considerado em blocos, ou seja, `BLCKSZ` bytes, tipicamente 8kB. O padrão é de 4 gigabytes (`4GB`). (Se `BLCKSZ` não for 8kB, o valor padrão é proporcional a ele.)

`jit_above_cost` (`floating point`) [#](#GUC-JIT-ABOVE-COST): Define o custo da consulta acima do qual a compilação JIT é ativada, se habilitada (consulte [Capítulo 30](jit.md "Chapter 30. Just-in-Time Compilation (JIT)). Realizar o planejamento de custos JIT leva tempo, mas pode acelerar a execução da consulta. Definir isso como `-1` desativa a compilação JIT. O padrão é `100000`.

`jit_inline_above_cost` (`floating point`) [#](#GUC-JIT-INLINE-ABOVE-COST): Define o custo da consulta acima do qual a compilação JIT tenta emlinear funções e operadores. O enlinear adiciona tempo de planejamento, mas pode melhorar a velocidade de execução. Não faz sentido definir isso para menos que `jit_above_cost`. Definir isso para `-1` desativa o enlinear. O padrão é `500000`.

`jit_optimize_above_cost` (`floating point`) [#](#GUC-JIT-OPTIMIZE-ABOVE-COST): Define o custo da consulta acima do qual a compilação JIT aplica otimizações caras. Tal otimização adiciona tempo de planejamento, mas pode melhorar a velocidade de execução. Não faz sentido definir isso para menos que `jit_above_cost`, e é improvável que seja benéfico definir isso para mais que `jit_inline_above_cost`. Definir isso para `-1` desativa otimizações caras. O padrão é `500000`.

### 19.7.3. Otimizador de Consulta Genética [#](#RUNTIME-CONFIG-QUERY-GEQO)

O otimizador de consulta genética (GEQO) é um algoritmo que realiza o planejamento de consulta utilizando busca heurística. Isso reduz o tempo de planejamento para consultas complexas (aqueles que unem muitas relações), ao custo de produzir planos que, às vezes, são inferiores aos encontrados pelo algoritmo de busca exhaustiva normal. Para mais informações, consulte [Capítulo 61](geqo.md).

`geqo` (`boolean`) [#](#GUC-GEQO): Habilita ou desabilita a otimização de consultas genéticas. Isso está ativado por padrão. Geralmente, é melhor não desativá-lo em produção; a variável `geqo_threshold` oferece um controle mais granular do GEQO.

`geqo_threshold` (`integer`) [#](#GUC-GEQO-THRESHOLD): Utilize a otimização de consulta genética para planejar consultas com pelo menos esse número de itens `FROM` envolvidos. (Observe que uma construção `FULL OUTER JOIN` é contada como apenas um item `FROM`. O padrão é 12. Para consultas mais simples, geralmente é melhor usar o planejador de pesquisa regular e exaustiva, mas para consultas com muitas tabelas, a pesquisa exaustiva leva muito tempo, muitas vezes mais do que a penalidade de executar um plano subótimo. Assim, um limite no tamanho da consulta é uma maneira conveniente de gerenciar o uso do GEQO.

`geqo_effort` (`integer`) [#](#GUC-GEQO-EFFORT): Controla o equilíbrio entre o tempo de planejamento e a qualidade do plano de consulta no GEQO. Esta variável deve ser um número inteiro na faixa de 1 a 10. O valor padrão é cinco. Valores maiores aumentam o tempo gasto no planejamento de consulta, mas também aumentam a probabilidade de que um plano de consulta eficiente seja escolhido.

`geqo_effort` não faz nada diretamente; ele é usado apenas para calcular os valores padrão para as outras variáveis que influenciam o comportamento do GEQO (descrito abaixo). Se preferir, pode definir os outros parâmetros manualmente.

`geqo_pool_size` (`integer`) [#](#GUC-GEQO-POOL-SIZE): Controla o tamanho do pool utilizado pelo GEQO, ou seja, o número de indivíduos na população genética. Deve ser pelo menos dois, e valores úteis são tipicamente de 100 a 1000. Se definido como zero (a configuração padrão), então um valor adequado é escolhido com base em `geqo_effort` e no número de tabelas na consulta.

`geqo_generations` (`integer`) [#](#GUC-GEQO-GENERATIONS): Controla o número de gerações usadas pelo GEQO, ou seja, o número de iterações do algoritmo. Deve ser pelo menos um, e valores úteis estão na mesma faixa que o tamanho do pool. Se definido como zero (a configuração padrão), então um valor adequado é escolhido com base em `geqo_pool_size`.

`geqo_selection_bias` (`floating point`) [#](#GUC-GEQO-SELECTION-BIAS): Controla a tendência de seleção utilizada pelo GEQO. A tendência de seleção é a pressão seletiva dentro da população. Os valores podem variar de 1,50 a 2,00; o último é o padrão.

`geqo_seed` (`floating point`) [#](#GUC-GEQO-SEED): Controla o valor inicial do gerador de números aleatórios utilizado pelo GEQO para selecionar caminhos aleatórios através do espaço de pesquisa de ordem de junção. O valor pode variar de zero (o padrão) a um. A variação do valor altera o conjunto de caminhos de junção explorados e pode resultar em um melhor ou pior caminho encontrado.

### 19.7.4. Outras opções do planejador [#](#RUNTIME-CONFIG-QUERY-OTHER)

`default_statistics_target` (`integer`) [#](#GUC-DEFAULT-STATISTICS-TARGET): Define o objetivo de estatísticas padrão para as colunas da tabela sem um objetivo específico para a coluna definido via `ALTER TABLE SET STATISTICS`. Valores maiores aumentam o tempo necessário para fazer `ANALYZE`, mas podem melhorar a qualidade das estimativas do planejador. O padrão é 100. Para mais informações sobre o uso de estatísticas pelo planejador de consultas do PostgreSQL, consulte [Seção 14.2](planner-stats.md "14.2. Statistics Used by the Planner").

`constraint_exclusion` (`enum`) [#](#GUC-CONSTRAINT-EXCLUSION): Controla o uso do planejador de consulta de restrições de tabela para otimizar consultas. Os valores permitidos de `constraint_exclusion` são `on` (examinar restrições para todas as tabelas), `off` (nunca examinar restrições), e `partition` (examinar restrições apenas para tabelas de filho de herança e subconsultas `UNION ALL`). `partition` é o ajuste padrão. É frequentemente usado com árvores de herança tradicionais para melhorar o desempenho.

Quando este parâmetro permitir para uma tabela específica, o planejador compara as condições da consulta com as restrições `CHECK` da tabela e omite a varredura de tabelas para as quais as condições contradizem as restrições. Por exemplo:

```
CREATE TABLE parent(key integer, ...); CREATE TABLE child1000(check (key between 1000 and 1999)) INHERITS(parent); CREATE TABLE child2000(check (key between 2000 and 2999)) INHERITS(parent); ... SELECT * FROM parent WHERE key = 2400;
```

Com a exclusão de restrições ativada, este `SELECT` não escaneará `child1000` de forma alguma, melhorando o desempenho.

Atualmente, a exclusão de restrições é habilitada por padrão apenas para casos que são frequentemente usados para implementar a partição de tabelas por meio de árvores de herança. Ativá-la para todas as tabelas impõe um overhead de planejamento extra que é bastante notável em consultas simples, e na maioria das vezes não trará nenhum benefício para consultas simples. Se você não tem tabelas que sejam particionadas usando herança tradicional, você pode preferir desativá-la completamente. (Observe que o recurso equivalente para tabelas particionadas é controlado por um parâmetro separado, [enable_partition_pruning](runtime-config-query.md#GUC-ENABLE-PARTITION-PRUNING)).

Consulte [Seção 5.12.5](ddl-partitioning.md#DDL-PARTITIONING-CONSTRAINT-EXCLUSION) para obter mais informações sobre o uso da exclusão de restrições para implementar a partição.

`cursor_tuple_fraction` (`floating point`) [#](#GUC-CURSOR-TUPLE-FRACTION): Define a estimativa do planejador da fração de linhas de um cursor que será recuperada. O padrão é 0,1. Valores menores nesta configuração inclinam o planejador a usar planos de "início rápido" para cursors, que recuperará as primeiras linhas rapidamente, mas pode levar um longo tempo para obter todas as linhas. Valores maiores colocam mais ênfase no tempo total estimado. No ajuste máximo de 1,0, os cursors são planejados exatamente como consultas regulares, considerando apenas o tempo total estimado e não quão rapidamente as primeiras linhas podem ser entregues.

`from_collapse_limit` (`integer`) [#](#GUC-FROM-COLLAPSE-LIMIT): O planejador irá combinar subconsultas em consultas superiores se a lista resultante do `FROM` não tivesse mais do que esse número de itens. Valores menores reduzem o tempo de planejamento, mas podem gerar planos de consulta inferiores. O padrão é oito. Para mais informações, consulte [Seção 14.3](explicit-joins.md "14.3. Controlling the Planner with Explicit JOIN Clauses").

Definir esse valor como [geqo_threshold](runtime-config-query.md#GUC-GEQO-THRESHOLD) ou mais pode desencadear o uso do planejador GEQO, resultando em planos não ótimos. Veja [Seção 19.7.3](runtime-config-query.md#RUNTIME-CONFIG-QUERY-GEQO).

`jit` (`boolean`) [#](#GUC-JIT): Determina se a compilação JIT pode ser usada pelo PostgreSQL, se disponível (consulte [Capítulo 30](jit.md)]). O padrão é `on`.

`join_collapse_limit` (`integer`) [#](#GUC-JOIN-COLLAPSE-LIMIT): O planejador reescreverá construções explícitas de `JOIN` (exceto `FULL JOIN`s) em listas de itens de `FROM` sempre que uma lista com no máximo esse número de itens resultar. Valores menores reduzem o tempo de planejamento, mas podem gerar planos de consulta inferiores.

Por padrão, essa variável é definida da mesma forma que `from_collapse_limit`, o que é apropriado para a maioria dos usos. Definindo-a como 1, é impedido qualquer reordenação de `JOIN`s explícitos. Assim, a ordem de junção explícita especificada na consulta será a ordem real em que as relações são juncionadas. Como o planejador de consulta nem sempre escolhe a ordem de junção ótima, os usuários avançados podem optar por definir temporariamente essa variável como 1 e, em seguida, especificar explicitamente a ordem de junção que desejam. Para mais informações, consulte [Seção 14.3](explicit-joins.md).

Definir esse valor como [geqo_threshold](runtime-config-query.md#GUC-GEQO-THRESHOLD) ou mais pode desencadear o uso do planejador GEQO, resultando em planos não ótimos. Veja [Seção 19.7.3](runtime-config-query.md#RUNTIME-CONFIG-QUERY-GEQO).

`plan_cache_mode` (`enum`) [#](#GUC-PLAN-CACHE-MODE): As instruções preparadas (ou explicitamente preparadas ou geradas implicitamente, por exemplo, por PL/pgSQL) podem ser executadas usando planos personalizados ou genéricos. Os planos personalizados são feitos novamente para cada execução usando seu conjunto específico de valores de parâmetros, enquanto os planos genéricos não dependem dos valores de parâmetros e podem ser reutilizados em várias execuções. Assim, o uso de um plano genérico economiza tempo de planejamento, mas se o plano ideal depende fortemente dos valores de parâmetros, então um plano genérico pode ser ineficiente. A escolha entre essas opções é normalmente feita automaticamente, mas pode ser sobrescrita com `plan_cache_mode`. Os valores permitidos são `auto` (o padrão), `force_custom_plan` e `force_generic_plan`. Esta configuração é considerada quando um plano armazenado deve ser executado, não quando ele é preparado. Para mais informações, consulte [PREPARE](sql-prepare.md "PREPARE").

`recursive_worktable_factor` (`floating point`) [#](#GUC-RECURSIVE-WORKTABLE-FACTOR): Define a estimativa do planejador do tamanho médio da tabela de trabalho de uma consulta (queries-with.md#QUERIES-WITH-RECURSIVE "7.8.2. Recursive Queries") (consulta recursiva), em múltiplos do tamanho estimado do termo inicial não recursivo da consulta. Isso ajuda o planejador a escolher o método mais apropriado para unir a tabela de trabalho às outras tabelas da consulta. O valor padrão é `10.0`. Um valor menor, como `1.0`, pode ser útil quando a recursão tem baixa "extensão" de um passo para o próximo, como, por exemplo, em consultas de caminho mais curto. As consultas de análise de gráficos podem se beneficiar de valores maiores que o padrão.