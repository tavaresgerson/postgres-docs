## 61.3. Otimização de Consulta Genética (GEQO) no PostgreSQL [#](#GEQO-PG-INTRO)

* [61.3.1. Gerando Planos Possíveis com GEQO][(geqo-pg-intro.md#GEQO-PG-INTRO-GEN-POSSIBLE-PLANS)]
* [61.3.2. Tarefas de Implementação Futura para PostgreSQL GEQO][(geqo-pg-intro.md#GEQO-FUTURE)]

O módulo GEQO aborda o problema de otimização de consultas como se fosse o conhecido problema do vendedor viajante (TSP). Os planos de consulta possíveis são codificados como strings inteiras. Cada string representa a ordem de junção de uma relação da consulta para a próxima. Por exemplo, a árvore de junção

```
   /\
  /\ 2
 /\ 3
4  1
```

é codificado pela string inteira '4-1-3-2', o que significa, primeiro, junção da relação '4' e '1', depois '3', e depois '2', onde 1, 2, 3, 4 são IDs de relação dentro do otimizador do PostgreSQL.

As características específicas da implementação do GEQO no PostgreSQL são:

* Uso de uma GA em estado estável (substituição dos indivíduos menos adequados em uma população, e não substituição de toda a geração) permite a rápida convergência em direção a planos de consulta melhorados. Isso é essencial para o tratamento de consultas com tempo razoável;
* Uso de *recombinação de borda* que é especialmente adequada para manter as perdas de borda baixas para a solução do TSP por meio de uma GA;
* A mutação como operador genético é descontinuada para que não sejam necessários mecanismos de reparo para gerar tours legítimos do TSP.

Algumas partes do módulo GEQO foram adaptadas do algoritmo Genitor de D. Whitley.

O módulo GEQO permite que o otimizador de consultas do PostgreSQL suporte consultas de junção grandes de forma eficaz por meio de uma busca não exaustiva.

### 61.3.1. Gerando Planos Possíveis com GEQO [#](#GEQO-PG-INTRO-GEN-POSSIBLE-PLANS)

O processo de planejamento do GEQO utiliza o código padrão do planejador para gerar planos de varreduras de relações individuais. Em seguida, os planos de junção são desenvolvidos usando a abordagem genética. Como mostrado acima, cada plano de junção candidato é representado por uma sequência na qual as relações de base devem ser junidas. Na etapa inicial, o código do GEQO simplesmente gera algumas sequências de junção possíveis aleatoriamente. Para cada sequência de junção considerada, o código padrão do planejador é invocado para estimar o custo de execução da consulta usando essa sequência de junção. (Para cada etapa da sequência de junção, todas as três estratégias de junção possíveis são consideradas; e todos os planos de varredura de relação inicialmente determinados estão disponíveis. O custo estimado é o mais barato dessas possibilidades.) As sequências de junção com custo estimado mais baixo são consideradas “mais adequadas” do que aquelas com custo mais alto. O algoritmo genético descarta os candidatos menos adequados. Em seguida, novos candidatos são gerados combinando genes de candidatos mais adequados — ou seja, usando porções aleatoriamente escolhidas de sequências de junção de baixo custo conhecidas para criar novas sequências para consideração. Esse processo é repetido até que um número pré-definido de sequências de junção tenham sido consideradas; então, a melhor encontrada em qualquer momento durante a busca é usada para gerar o plano final.

Esse processo é inerentemente não determinístico, devido às escolhas aleatórias feitas durante a seleção inicial da população e à subsequente "mutação" dos melhores candidatos. Para evitar mudanças surpreendentes no plano selecionado, cada execução do algoritmo GEQO reinicia seu gerador de números aleatórios com a configuração atual do parâmetro [[geqo_seed]](runtime-config-query.md#GUC-GEQO-SEED). Enquanto `geqo_seed` e os outros parâmetros do GEQO forem mantidos fixos, o mesmo plano será gerado para uma consulta específica (e outros insumos do planejador, como estatísticas). Para experimentar diferentes caminhos de busca, tente alterar `geqo_seed`.

### 61.3.2. Tarefas de implementação futura para PostgreSQL GEQO [#](#GEQO-FUTURE)

Ainda é necessário trabalhar para melhorar as configurações dos parâmetros do algoritmo genético. Nos arquivos `src/backend/optimizer/geqo/geqo_main.c`, `gimme_pool_size` e `gimme_number_generations`, temos que encontrar um compromisso para as configurações dos parâmetros que satisfaçam duas demandas concorrentes:

* Otimização do plano de consulta * Tempo de computação

Na implementação atual, a adequação de cada sequência de junção de candidatos é estimada ao executar o código padrão de seleção de junção e estimativa de custo do planejador do zero. Na medida em que diferentes candidatos utilizam subsequências semelhantes de junções, uma grande quantidade de trabalho será repetida. Isso pode ser feito significativamente mais rápido ao reter as estimativas de custo para subjunções. O problema é evitar gastar quantias irracionáveis de memória para reter esse estado.

Em um nível mais básico, não está claro que a otimização de consultas com um algoritmo de GA projetado para TSP seja apropriado. No caso do TSP, o custo associado a qualquer subdivisão (tour parcial) é independente do resto do tour, mas isso certamente não é verdade para a otimização de consultas. Portanto, é questionável se a recombinação de borda cruzamento é o procedimento de mutação mais eficaz.