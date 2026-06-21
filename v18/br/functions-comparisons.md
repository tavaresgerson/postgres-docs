## 9.25. Comparação de linhas e arrays [#](#FUNCTIONS-COMPARISONS)

* [9.25.1. `IN`](functions-comparisons.md#FUNCTIONS-COMPARISONS-IN-SCALAR)
* [9.25.2. `NOT IN`](functions-comparisons.md#FUNCTIONS-COMPARISONS-NOT-IN)
* [9.25.3. `ANY`/`SOME` (matriz)(functions-comparisons.md#FUNCTIONS-COMPARISONS-ANY-SOME)
* [9.25.4. `ALL` (matriz)(functions-comparisons.md#FUNCTIONS-COMPARISONS-ALL)
* [9.25.5. Comparação do construtor de linhas](functions-comparisons.md#ROW-WISE-COMPARISON)
* [9.25.6. Comparação de tipos compostos](functions-comparisons.md#COMPOSITE-TYPE-COMPARISON)

Esta seção descreve várias construções especializadas para fazer comparações múltiplas entre grupos de valores. Essas formas estão sintaticamente relacionadas às formas de subconsulta da seção anterior, mas não envolvem subconsultas. As formas que envolvem subexpressões de matriz são extensões do PostgreSQL; o restante é compatível com o SQL. Todas as formas de expressão documentadas nesta seção retornam resultados booleanos (verdadeiro/falso).

### 9.25.1. `IN` [#](#FUNCTIONS-COMPARISONS-IN-SCALAR)

```
expression IN (value [, ...])
```

O lado direito é uma lista entre parênteses de expressões. O resultado é "verdadeiro" se o resultado da expressão do lado esquerdo for igual a qualquer uma das expressões do lado direito. Esta é uma notação abreviada para

```
expression = value1
OR
expression = value2
OR
...
```

Observe que, se a expressão da mão esquerda resultar em nulo, ou se não houver valores iguais na mão direita e pelo menos uma expressão da mão direita resultar em nulo, o resultado da construção `IN` será nulo, não falso. Isso está de acordo com as regras normais do SQL para combinações booleanas de valores nulos.

### 9.25.2. `NOT IN` [#](#FUNCTIONS-COMPARISONS-NOT-IN)

```
expression NOT IN (value [, ...])
```

O lado direito é uma lista entre parênteses de expressões. O resultado é "verdadeiro" se o resultado da expressão do lado esquerdo não for igual a todas as expressões do lado direito. Esta é uma notação abreviada para

```
expression <> value1
AND
expression <> value2
AND
...
```

Observe que, se a expressão da mão esquerda resultar em nulo, ou se não houver valores iguais na mão direita e pelo menos uma expressão da mão direita resultar em nulo, o resultado da construção `NOT IN` será nulo, e não verdadeiro, como se poderia esperar ingenuamente. Isso está de acordo com as regras normais do SQL para combinações booleanas de valores nulos.

### DICA

`x NOT IN y` é equivalente a `NOT (x IN y)` em todos os casos. No entanto, valores nulos têm muito mais probabilidade de confundir o novato ao trabalhar com `NOT IN` do que ao trabalhar com `IN`. É melhor expressar sua condição positivamente, se possível.

### 9.25.3. `ANY`/`SOME` (matriz) [#](#FUNCTIONS-COMPARISONS-ANY-SOME)

```
expression operator ANY (array expression)
expression operator SOME (array expression)
```

O lado direito é uma expressão entre parênteses, que deve produzir um valor de matriz. A expressão do lado esquerdo é avaliada e comparada a cada elemento da matriz usando o dado *`operator`*, que deve produzir um resultado booleano. O resultado de `ANY` é “verdadeiro” se qualquer resultado verdadeiro for obtido. O resultado é “falso” se nenhum resultado verdadeiro for encontrado (incluindo o caso em que a matriz tem zero elementos).

Se a expressão de matriz gerar uma matriz nula, o resultado de `ANY` será nulo. Se a expressão da mão esquerda gerar null, o resultado de `ANY` é normalmente nulo (embora um operador de comparação não estrito possa possivelmente gerar um resultado diferente). Além disso, se a matriz da mão direita contiver quaisquer elementos nulos e nenhum resultado de comparação verdadeiro for obtido, o resultado de `ANY` será nulo, não falso (novamente, assumindo um operador de comparação estrito). Isso está de acordo com as regras normais do SQL para combinações booleanas de valores nulos.

`SOME` é sinônimo de `ANY`.

### 9.25.4. `ALL` (matriz) [#](#FUNCTIONS-COMPARISONS-ALL)

```
expression operator ALL (array expression)
```

O lado direito é uma expressão entre parênteses, que deve produzir um valor de matriz. A expressão do lado esquerdo é avaliada e comparada a cada elemento da matriz usando o dado *`operator`*, que deve produzir um resultado booleano. O resultado de `ALL` é “verdadeiro” se todas as comparações produzirem verdadeiro (incluindo o caso em que a matriz tem zero elementos). O resultado é “falso” se qualquer resultado falso for encontrado.

Se a expressão de matriz gerar uma matriz nula, o resultado de `ALL` será nulo. Se a expressão da mão esquerda gerar null, o resultado de `ALL` é normalmente nulo (embora um operador de comparação não estrito possa possivelmente gerar um resultado diferente). Além disso, se a matriz da mão direita contiver quaisquer elementos nulos e não for obtido nenhum resultado de comparação falsa, o resultado de `ALL` será nulo, não verdadeiro (novamente, assumindo um operador de comparação estrito). Isso está de acordo com as regras normais do SQL para combinações booleanas de valores nulos.

### 9.25.5. Comparação do construtor de linhas [#](#ROW-WISE-COMPARISON)

```
row_constructor operator row_constructor
```

Cada lado é um construtor de linha, conforme descrito em [Seção 4.2.13][(sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS "4.2.13. Row Constructors")]. Os dois construtores de linha devem ter o mesmo número de campos. O dado *`operator`* é aplicado a cada par de campos correspondentes. (Como os campos podem ser de tipos diferentes, isso significa que um operador específico diferente pode ser selecionado para cada par.) Todos os operadores selecionados devem ser membros de alguma classe de operador B-tree, ou ser o negador de um membro `=` de uma classe de operador B-tree, o que significa que a comparação de construtor de linha é apenas possível quando o *`operator`* é `=`, `<>`, `<`, `<=`, `>` ou `>=`, ou tem uma semântica semelhante a uma dessas.

Os casos `=` e `<>` funcionam de maneira um pouco diferente dos outros. Duas linhas são consideradas iguais se todos seus membros correspondentes forem não nulos e iguais; as linhas são desiguais se quaisquer membros correspondentes forem não nulos e desiguais; caso contrário, o resultado da comparação das linhas é desconhecido (nulo).

Para os casos de `<`, `<=`, `>` e `>=`, os elementos da linha são comparados de esquerda para direita, parando assim que é encontrado um par desigual ou nulo de elementos. Se qualquer um desses pares de elementos for nulo, o resultado da comparação da linha é desconhecido (nulo); caso contrário, a comparação desse par de elementos determina o resultado. Por exemplo, `ROW(1,2,NULL) < ROW(1,3,0)` produz verdadeiro, não nulo, porque o terceiro par de elementos não é considerado.

```
row_constructor IS DISTINCT FROM row_constructor
```

Esse construtor é semelhante a uma comparação de linha `<>`, mas ele não gera um valor nulo para entradas nulos. Em vez disso, qualquer valor nulo é considerado diferente (distinto) de qualquer valor não nulo, e quaisquer dois nulos são considerados iguais (não distintos). Assim, o resultado será verdadeiro ou falso, nunca nulo.

```
row_constructor IS NOT DISTINCT FROM row_constructor
```

Esse construtor é semelhante a uma comparação de linha `=`, mas não gera um valor nulo para entradas nulos. Em vez disso, qualquer valor nulo é considerado diferente (distinto) de qualquer valor não nulo, e quaisquer dois nulos são considerados iguais (não distintos). Assim, o resultado será sempre verdadeiro ou falso, nunca nulo.

### 9.25.6. Comparação do tipo composto [#](#COMPOSITE-TYPE-COMPARISON)

```
record operator record
```

A especificação SQL exige uma comparação por linha para retornar NULL se o resultado depender da comparação de dois valores NULL ou de um NULL e um não NULL. O PostgreSQL faz isso apenas quando está comparando os resultados de dois construtores de linha (como em [Seção 9.25.5] [(functions-comparisons.md#ROW-WISE-COMPARISON "9.25.5. Row Constructor Comparison")]) ou comparando um construtor de linha com a saída de uma subconsulta (como em [Seção 9.24] [(functions-subquery.md "9.24. Subquery Expressions")]). Em outros contextos onde dois valores de tipo composto são comparados, dois valores de campo NULL são considerados iguais, e um NULL é considerado maior que um não NULL. Isso é necessário para ter um comportamento consistente de ordenação e indexação para tipos compostos.

Cada lado é avaliado e são comparados linha a linha. As comparações de tipos compostos são permitidas quando o *`operator`* é `=`, `<>`, `<`, `<=`, `>` ou `>=`, ou tem uma semântica semelhante a uma dessas. (Para ser específico, um operador pode ser um operador de comparação de linha se for um membro de uma classe de operadores de B-tree, ou é o negador do membro `=` de uma classe de operadores de B-tree.) O comportamento padrão dos operadores acima é o mesmo que para `IS [ NOT ] DISTINCT FROM` para construtores de linha (ver [Seção 9.25.5][(functions-comparisons.md#ROW-WISE-COMPARISON "9.25.5. Row Constructor Comparison")]).

Para auxiliar na correspondência de linhas que incluem elementos sem uma classe de operador B-tree padrão, os seguintes operadores são definidos para comparação de tipos compostos: `*=`, `*<>`, `*<`, `*<=`, `*>` e `*>=`. Esses operadores comparam a representação binária interna das duas linhas. Duas linhas podem ter uma representação binária diferente, mesmo que as comparações das duas linhas com o operador de igualdade sejam verdadeiras. A ordem das linhas sob esses operadores de comparação é determinada, mas não é significativa de outra forma. Esses operadores são usados internamente para visualizações materializadas e podem ser úteis para outros propósitos especializados, como replicação e deduplicação B-Tree (ver [Seção 65.1.4.3] (btree.md#BTREE-DEDUPLICATION "65.1.4.3. Deduplication")). Eles não são destinados a serem úteis em geral para escrever consultas.