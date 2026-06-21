## 61.2. Algoritmos Genéticos [#](#GEQO-INTRO2)

O algoritmo genético (AG) é um método heurístico de otimização que opera por meio de busca aleatória. O conjunto de soluções possíveis para o problema de otimização é considerado como uma *população* de *indivíduos*. O grau de adaptação de um indivíduo ao seu ambiente é especificado por sua *aptidão*.

As coordenadas de um indivíduo no espaço de busca são representadas por *cromossomos*, em essência, um conjunto de cadeias de caracteres. Um *gene* é uma subseção de um cromossomo que codifica o valor de um único parâmetro que está sendo otimizado. As codificações típicas para um gene podem ser *binária* ou *inteira*.

Através da simulação das operações evolutivas *recombinação*, *mutação* e *seleção*, são encontradas novas gerações de pontos de busca que apresentam uma aptidão média superior à de seus ancestrais. [Figura 61.1] (geqo-intro2.md#GEQO-FIGURE "Figure 61.1. Structure of a Genetic Algorithm") ilustra esses passos.

**Figura 61.1. Estrutura de um Algoritmo Genético**



De acordo com a FAQ comp.ai.genetic, não se pode enfatizar o suficiente que uma GA não é uma busca pura aleatória para uma solução de um problema. Uma GA utiliza processos estocásticos, mas o resultado é claramente não aleatório (melhor do que aleatório).