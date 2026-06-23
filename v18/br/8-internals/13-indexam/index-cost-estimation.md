## 63.6. Funções de Estimativa de Custo do Índice [#](#INDEX-COST-ESTIMATION)

A função `amcostestimate` recebe informações que descrevem um possível varrimento de índice, incluindo listas de cláusulas WHERE e ORDER BY que foram determinadas como utilizáveis com o índice. Ela deve retornar estimativas do custo de acesso ao índice e da seletividade das cláusulas WHERE (ou seja, a fração das linhas da tabela-mãe que serão recuperadas durante o varrimento do índice). Para casos simples, quase todo o trabalho do estimador de custo pode ser feito chamando rotinas padrão no otimizador; o ponto de ter uma função `amcostestimate` é permitir que os métodos de acesso ao índice forneçam conhecimento específico do tipo de índice, caso seja possível melhorar as estimativas padrão.

Cada função `amcostestimate` deve ter a assinatura:

```
void
amcostestimate (PlannerInfo *root,
                IndexPath *path,
                double loop_count,
                Cost *indexStartupCost,
                Cost *indexTotalCost,
                Selectivity *indexSelectivity,
                double *indexCorrelation,
                double *indexPages);
```

Os três primeiros parâmetros são entradas:

*`root`*: As informações do planejador sobre a consulta que está sendo processada.

*`path`*: O caminho de acesso ao índice que está sendo considerado. Todos os campos, exceto os valores de custo e seletividade, são válidos.

*`loop_count`*: O número de repetições do exame de índice que deve ser considerado nas estimativas de custo. Geralmente, esse número será maior que um quando se considera um exame parametrizado para uso no interior de uma junção de laço de nidificação. Observe que as estimativas de custo ainda devem ser para apenas um exame; um *`loop_count`* maior pode significar que é apropriado permitir alguns efeitos de cache em várias análises.

Os últimos cinco parâmetros são saídas por referência:

*`*indexStartupCost`*: Definido como o custo do processamento inicial do índice

*`*indexTotalCost`*: Custo total do processamento do índice

*`*indexSelectivity`*: Definido para indexar seletividade

*`*indexCorrelation`*: Definido para o coeficiente de correlação entre a ordem de varredura do índice e a ordem da tabela subjacente

*`*indexPages`*: Definido como número de páginas de folha de índice

Observe que as funções de estimativa de custo devem ser escritas em C, não em SQL ou em qualquer linguagem procedural disponível, porque elas devem acessar estruturas de dados internas do planejador/opinião.

Os custos de acesso ao índice devem ser calculados usando os parâmetros utilizados por `src/backend/optimizer/path/costsize.c`: um bloco de disco sequencial tem custo `seq_page_cost`, uma busca não sequencial tem custo `random_page_cost`, e o custo de processamento de uma linha de índice geralmente deve ser considerado como `cpu_index_tuple_cost`. Além disso, um múltiplo apropriado de `cpu_operator_cost` deve ser cobrado por quaisquer operadores de comparação invocados durante o processamento do índice (especialmente a avaliação dos próprios indexquals).

Os custos de acesso devem incluir todos os custos de disco e CPU associados à digitalização do próprio índice, mas *não* os custos de recuperação ou processamento das linhas da tabela-mãe que são identificadas pelo índice.

O custo de “inicialização” é a parte do custo total do exame que deve ser gasto antes de podermos começar a extrair a primeira linha. Para a maioria dos índices, isso pode ser considerado zero, mas um tipo de índice com um custo inicial alto pode querer defini-lo como não nulo.

O *`indexSelectivity`* deve ser ajustado para a fração estimada das linhas da tabela-mãe que serão recuperadas durante a varredura do índice. No caso de uma consulta com perda, essa fração será, normalmente, maior do que a fração de linhas que realmente atendem às condições especificadas.

O *`indexCorrelation` deve ser ajustado para a correlação (que varia entre -1,0 e 1,0) entre a ordem do índice e a ordem da tabela. Isso é usado para ajustar a estimativa do custo de obtenção de linhas da tabela principal.

O *`indexPages`* deve ser ajustado para o número de páginas de folha. Isso é usado para estimar o número de trabalhadores para varredura de índice paralela.

Quando *`loop_count`* é maior que um, os números retornados devem ser médias esperadas para qualquer um dos scans do índice.

**Estimativa de Custos**

Um projetista de custos típico procederá da seguinte forma:

1. Estime e retorne a fração das linhas da tabela-mãe que serão visitadas com base nas condições fornecidas. Na ausência de qualquer conhecimento específico do tipo de índice, use a função padrão do otimizador `clauselist_selectivity()`:

2. Estime o número de linhas de índice que serão visitadas durante o varrimento. Para muitos tipos de índice, isso é o mesmo que *`indexSelectivity`* vezes o número de linhas no índice, mas pode ser mais. (Observe que o tamanho do índice em páginas e linhas está disponível na estrutura `path->indexinfo`.)
3. Estime o número de páginas de índice que serão recuperadas durante o varrimento. Isso pode ser apenas *`indexSelectivity`* vezes o tamanho do índice em páginas.
4. Calcule o custo de acesso ao índice. Um estimador genérico pode fazer isso:

```
/*
 * Our generic assumption is that the index pages will be read
 * sequentially, so they cost seq_page_cost each, not random_page_cost.
 * Also, we charge for evaluation of the indexquals at each index row.
 * All the costs are assumed to be paid incrementally during the scan.
 */
cost_qual_eval(&index_qual_cost, path->indexquals, root);
*indexStartupCost = index_qual_cost.startup;
*indexTotalCost = seq_page_cost * numIndexPages +
    (cpu_index_tuple_cost + index_qual_cost.per_tuple) * numIndexTuples;
```

No entanto, o acima não leva em conta a amortização das leituras do índice em varreduras repetidas do índice.
5. Estime a correlação do índice. Para um índice simples ordenado em um único campo, isso pode ser recuperado de pg_statistic. Se a correlação não for conhecida, a estimativa conservadora é zero (sem correlação).

Exemplos de funções de estimativa de custos podem ser encontrados em `src/backend/utils/adt/selfuncs.c`.