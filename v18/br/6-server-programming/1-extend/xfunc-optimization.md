## 36.11. Informações sobre otimização de funções [#](#XFUNC-OPTIMIZATION)

Por padrão, uma função é apenas uma "caixa preta" sobre a qual o sistema de banco de dados sabe muito pouco sobre o comportamento. No entanto, isso significa que as consultas que utilizam a função podem ser executadas muito menos eficientemente do que poderiam ser. É possível fornecer conhecimento adicional que ajuda o planejador a otimizar as chamadas à função.

Alguns fatos básicos podem ser fornecidos por anotações declarativas fornecidas no comando `CREATE FUNCTION`(sql-createfunction.md "CREATE FUNCTION"). O mais importante desses fatos é a categoria de volatilidade da função ([volatility category](xfunc-volatility.md "36.7. Function Volatility Categories")(`IMMUTABLE`, `STABLE` ou `VOLATILE`)); deve-se sempre ter cuidado em especificar isso corretamente ao definir uma função. A propriedade de segurança paralela (`PARALLEL UNSAFE`, `PARALLEL RESTRICTED` ou `PARALLEL SAFE`) também deve ser especificada se espera-se usar a função em consultas paralelizadas. Também pode ser útil especificar o custo de execução estimado da função e/ou o número de linhas que uma função que retorna um conjunto é estimada para retornar. No entanto, a maneira declarativa de especificar esses dois fatos só permite especificar um valor constante, que muitas vezes é inadequado.

É também possível anexar uma função de suporte de planejador a uma função que pode ser chamada por SQL (chamada de sua função alvo), e, assim, fornecer conhecimento sobre a função alvo que é muito complexa para ser representada declarativamente. As funções de suporte de planejador devem ser escritas em C (embora suas funções alvos possam não ser), então esta é uma característica avançada que poucas pessoas irão usar.

Uma função de suporte de planejador deve ter a assinatura SQL

```
supportfn(internal) returns internal
```

Ele é anexado à sua função-alvo, especificando a cláusula `SUPPORT` ao criar a função-alvo.

Os detalhes das funções de suporte do planejador podem ser encontrados no arquivo `src/include/nodes/supportnodes.h` no código-fonte do PostgreSQL. Aqui, fornecemos apenas uma visão geral do que as funções de suporte do planejador podem fazer. O conjunto de solicitações possíveis para uma função de suporte é extensivo, então pode haver mais coisas possíveis em versões futuras.

Algumas chamadas de função podem ser simplificadas durante o planejamento com base em propriedades específicas da função. Por exemplo, `int4mul(n, 1)` pode ser simplificado para apenas `n`. Esse tipo de transformação pode ser realizado por uma função de suporte de planejamento, fazendo com que ela implemente o tipo de solicitação `SupportRequestSimplify`. A função de suporte será chamada para cada instância de sua função alvo encontrada em uma árvore de análise de consulta. Se ela encontrar que a chamada específica pode ser simplificada em alguma outra forma, ela pode construir e retornar uma árvore de análise representando essa expressão. Isso funcionará automaticamente para operadores com base na função também — no exemplo apenas dado, `n * 1` também seria simplificado para `n`. (Mas note que isso é apenas um exemplo; essa otimização particular não é realmente realizada pelo PostgreSQL padrão.) Não fazemos nenhuma garantia de que o PostgreSQL nunca chamará a função alvo em casos que a função de suporte poderia simplificar. Garanta equivalência rigorosa entre a expressão simplificada e uma execução real da função alvo.

Para funções-alvo que retornam `boolean`, é frequentemente útil estimar a fração de linhas que serão selecionadas por uma cláusula `WHERE` usando essa função. Isso pode ser feito por uma função de suporte que implementa o tipo de solicitação `SupportRequestSelectivity`.

Se o tempo de execução da função alvo depender fortemente de seus inputs, pode ser útil fornecer uma estimativa de custo não constante para ela. Isso pode ser feito por uma função de suporte que implemente o tipo de solicitação `SupportRequestCost`.

Para funções-alvo que retornam conjuntos, é frequentemente útil fornecer uma estimativa não constante para o número de linhas que serão retornadas. Isso pode ser feito por uma função de suporte que implementa o tipo de solicitação `SupportRequestRows`.

Para funções alvo que retornam `boolean`, pode ser possível converter uma chamada de função que aparece em `WHERE` em uma cláusula ou cláusulas de operador indexável. As cláusulas convertidas podem ser exatamente equivalentes à condição da função, ou podem ser um pouco mais fracas (ou seja, podem aceitar alguns valores que a condição da função não aceita). No último caso, a condição de índice é dita *perda de informação*; ainda pode ser usada para escanear um índice, mas a chamada de função terá que ser executada para cada linha devolvida pelo índice para verificar se realmente passa a condição `WHERE` ou não. Para criar tais condições, a função de suporte deve implementar o tipo de solicitação `SupportRequestIndexCondition`.