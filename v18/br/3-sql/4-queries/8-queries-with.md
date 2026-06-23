## 7.8. `WITH` Consultas (Expressões de Tabela Comum] [#](#QUERIES-WITH)

* [7.8.1. `SELECT` em `WITH`](queries-with.md#QUERIES-WITH-SELECT)
* [7.8.2. Consultas recursivas](queries-with.md#QUERIES-WITH-RECURSIVE)
* [7.8.3. Materialização da expressão de tabela comum](queries-with.md#QUERIES-WITH-CTE-MATERIALIZATION)
* [7.8.4. Declarações que modificam dados em `WITH`](queries-with.md#QUERIES-WITH-MODIFYING)

`WITH` fornece uma maneira de escrever declarações auxiliares para uso em uma consulta maior. Essas declarações, que são frequentemente referidas como Expressões de Tabela Comum ou CTEs, podem ser consideradas como definindo tabelas temporárias que existem apenas para uma consulta. Cada declaração auxiliar em uma cláusula `WITH` pode ser um `SELECT`, `INSERT`, `UPDATE`, `DELETE` ou `MERGE`; e a própria cláusula `WITH` é anexada a uma declaração principal que também pode ser um `SELECT`, `INSERT`, `UPDATE`, `DELETE` ou `MERGE`.

### 7.8.1. `SELECT` em `WITH` [#](#QUERIES-WITH-SELECT)

O valor básico de `SELECT` em `WITH` é de quebrar consultas complicadas em partes mais simples. Um exemplo é:

```
WITH regional_sales AS (
    SELECT region, SUM(amount) AS total_sales
    FROM orders
    GROUP BY region
), top_regions AS (
    SELECT region
    FROM regional_sales
    WHERE total_sales > (SELECT SUM(total_sales)/10 FROM regional_sales)
)
SELECT region,
       product,
       SUM(quantity) AS product_units,
       SUM(amount) AS product_sales
FROM orders
WHERE region IN (SELECT region FROM top_regions)
GROUP BY region, product;
```

que exibe os totais de vendas por produto apenas nas regiões de maior venda. A cláusula `WITH` define duas declarações auxiliares chamadas `regional_sales` e `top_regions`, onde a saída de `regional_sales` é usada em `top_regions` e a saída de `top_regions` é usada na consulta primária `SELECT`. Este exemplo poderia ter sido escrito sem `WITH`, mas precisaríamos de dois níveis de sub`SELECT`s aninhados. É um pouco mais fácil seguir essa maneira.

### 7.8.2. Consultas recursivas [#](#QUERIES-WITH-RECURSIVE)

O modificador opcional `RECURSIVE` transforma `WITH` de uma mera conveniência sintática em uma característica que realiza coisas que não são possíveis de outra forma no SQL padrão. Usando `RECURSIVE`, uma consulta `WITH` pode se referir à própria saída. Um exemplo muito simples é esta consulta para somar os inteiros de 1 até 100:

```
WITH RECURSIVE t(n) AS (
    VALUES (1)
  UNION ALL
    SELECT n+1 FROM t WHERE n < 100
)
SELECT sum(n) FROM t;
```

A forma geral de uma consulta recursiva `WITH` é sempre um *termo não recursivo*, em seguida `UNION` (ou `UNION ALL`), em seguida um *termo recursivo*, onde apenas o termo recursivo pode conter uma referência à própria saída da consulta. Tal consulta é executada da seguinte forma:

**Avaliação de consulta recursiva**

1. Avalie o termo não recursivo. Para `UNION` (mas não `UNION ALL`), descarte as linhas duplicadas. Inclua todas as linhas restantes no resultado da consulta recursiva e também coloque-as em uma *tabela de trabalho* temporária. 2. Enquanto a tabela de trabalho não estiver vazia, repita esses passos:

1. Avalie o termo recursivo, substituindo o conteúdo atual da tabela de trabalho pela autoreferência recursiva. Para `UNION` (mas não `UNION ALL`), descarte as linhas duplicadas e as linhas que dupliquem qualquer linha de resultado anterior. Inclua todas as linhas restantes no resultado da consulta recursiva e, também, coloque-as em uma *tabela intermediária* temporária.
2. Substitua o conteúdo da tabela de trabalho pelo conteúdo da tabela intermediária, em seguida, limpe a tabela intermediária.

Nota

Embora o `RECURSIVE` permita que as consultas sejam especificadas recursivamente, internamente, essas consultas são avaliadas iterativamente.

No exemplo acima, a tabela de trabalho tem apenas uma única linha em cada etapa, e assume os valores de 1 a 100 em etapas consecutivas. No 100º passo, não há saída devido à cláusula `WHERE`, e, portanto, a consulta termina.

As consultas recursivas são tipicamente usadas para lidar com dados hierárquicos ou estruturados em forma de árvore. Um exemplo útil é esta consulta para encontrar todas as subpartes diretas e indiretas de um produto, dado apenas uma tabela que mostra inclusões imediatas:

```
WITH RECURSIVE included_parts(sub_part, part, quantity) AS (
    SELECT sub_part, part, quantity FROM parts WHERE part = 'our_product'
  UNION ALL
    SELECT p.sub_part, p.part, p.quantity * pr.quantity
    FROM included_parts pr, parts p
    WHERE p.part = pr.sub_part
)
SELECT sub_part, SUM(quantity) as total_quantity
FROM included_parts
GROUP BY sub_part
```

#### 7.8.2.1. Ordem de pesquisa [#](#QUERIES-WITH-SEARCH)

Ao calcular uma travessia de árvore usando uma consulta recursiva, você pode querer ordenar os resultados em ordem de primeiro-visitado ou de primeiro-escaneado. Isso pode ser feito calculando uma coluna de ordenação ao lado das outras colunas de dados e usando isso para ordenar os resultados no final. Note que isso não controla realmente em que ordem a avaliação da consulta visita as linhas; isso é sempre dependente da implementação do SQL. Essa abordagem simplesmente fornece uma maneira conveniente de ordenar os resultados posteriormente.

Para criar uma ordem de profundidade, calculamos para cada linha de resultado um array de linhas que visitamos até agora. Por exemplo, considere a seguinte consulta que pesquisa uma tabela `tree` usando um campo `link`:

```
WITH RECURSIVE search_tree(id, link, data) AS (
    SELECT t.id, t.link, t.data
    FROM tree t
  UNION ALL
    SELECT t.id, t.link, t.data
    FROM tree t, search_tree st
    WHERE t.id = st.link
)
SELECT * FROM search_tree;
```

Para adicionar informações de ordenação de profundidade, você pode escrever o seguinte:

```
WITH RECURSIVE search_tree(id, link, data, path) AS (
    SELECT t.id, t.link, t.data, ARRAY[t.id]
    FROM tree t
  UNION ALL
    SELECT t.id, t.link, t.data, path || t.id
    FROM tree t, search_tree st
    WHERE t.id = st.link
)
SELECT * FROM search_tree ORDER BY path;
```

No caso geral, quando mais de um campo precisa ser usado para identificar uma linha, use um array de linhas. Por exemplo, se precisássemos rastrear os campos `f1` e `f2`:

```
WITH RECURSIVE search_tree(id, link, data, path) AS (
    SELECT t.id, t.link, t.data, ARRAY[ROW(t.f1, t.f2)]
    FROM tree t
  UNION ALL
    SELECT t.id, t.link, t.data, path || ROW(t.f1, t.f2)
    FROM tree t, search_tree st
    WHERE t.id = st.link
)
SELECT * FROM search_tree ORDER BY path;
```

### DICA

Omitam a sintaxe `ROW()` no caso comum em que apenas um campo precisa ser rastreado. Isso permite que um array simples, em vez de um array de tipo composto, seja usado, obtendo eficiência.

Para criar uma ordem de largura, você pode adicionar uma coluna que acompanhe a profundidade da pesquisa, por exemplo:

```
WITH RECURSIVE search_tree(id, link, data, depth) AS (
    SELECT t.id, t.link, t.data, 0
    FROM tree t
  UNION ALL
    SELECT t.id, t.link, t.data, depth + 1
    FROM tree t, search_tree st
    WHERE t.id = st.link
)
SELECT * FROM search_tree ORDER BY depth;
```

Para obter uma classificação estável, adicione as colunas de dados como colunas de classificação secundárias.

### DICA

O algoritmo de avaliação de consultas recursivas produz sua saída na ordem de pesquisa de largura, no entanto, essa é uma questão de implementação e talvez não seja seguro confiar nela. A ordem das linhas dentro de cada nível é certamente indefinida, portanto, em qualquer caso, pode ser desejada uma ordenação explícita.

Há sintaxe embutida para calcular uma coluna de ordenação de profundidade ou de largura. Por exemplo:

```
WITH RECURSIVE search_tree(id, link, data) AS (
    SELECT t.id, t.link, t.data
    FROM tree t
  UNION ALL
    SELECT t.id, t.link, t.data
    FROM tree t, search_tree st
    WHERE t.id = st.link
) SEARCH DEPTH FIRST BY id SET ordercol
SELECT * FROM search_tree ORDER BY ordercol;

WITH RECURSIVE search_tree(id, link, data) AS (
    SELECT t.id, t.link, t.data
    FROM tree t
  UNION ALL
    SELECT t.id, t.link, t.data
    FROM tree t, search_tree st
    WHERE t.id = st.link
) SEARCH BREADTH FIRST BY id SET ordercol
SELECT * FROM search_tree ORDER BY ordercol;
```

Essa sintaxe é expandida internamente para algo semelhante às formas escritas à mão acima. A cláusula `SEARCH` especifica se a busca de profundidade ou de largura deve ser desejada, a lista de colunas a serem rastreadas para ordenação e um nome de coluna que conterá os dados de resultado que podem ser usados para ordenação. Essa coluna será implicitamente adicionada às linhas de saída do CTE.

#### 7.8.2.2. Detecção de ciclo [#](#QUERIES-WITH-CYCLE)

Ao trabalhar com consultas recursivas, é importante ter certeza de que a parte recursiva da consulta eventualmente retornará nenhum tupla, caso contrário, a consulta entrará em um loop indefinidamente. Às vezes, usar `UNION` em vez de `UNION ALL` pode realizar isso, descartando as linhas que duplicam as linhas de saída anteriores. No entanto, muitas vezes, um ciclo não envolve linhas de saída que são completamente duplicadas: pode ser necessário verificar apenas um ou alguns campos para ver se o mesmo ponto já foi alcançado antes. O método padrão para lidar com tais situações é calcular um array dos valores já visitados. Por exemplo, considere novamente a seguinte consulta que busca uma tabela `graph` usando um campo `link`:

```
WITH RECURSIVE search_graph(id, link, data, depth) AS (
    SELECT g.id, g.link, g.data, 0
    FROM graph g
  UNION ALL
    SELECT g.id, g.link, g.data, sg.depth + 1
    FROM graph g, search_graph sg
    WHERE g.id = sg.link
)
SELECT * FROM search_graph;
```

Essa consulta irá repetir se as relações `link` contiverem ciclos. Como precisamos de uma saída de “profundidade”, simplesmente alterar `UNION ALL` para `UNION` não eliminaria a repetição. Em vez disso, precisamos reconhecer se chegamos à mesma linha novamente ao seguir um caminho específico de links. Adicionamos duas colunas `is_cycle` e `path` à consulta propensa a ciclos:

```
WITH RECURSIVE search_graph(id, link, data, depth, is_cycle, path) AS (
    SELECT g.id, g.link, g.data, 0,
      false,
      ARRAY[g.id]
    FROM graph g
  UNION ALL
    SELECT g.id, g.link, g.data, sg.depth + 1,
      g.id = ANY(path),
      path || g.id
    FROM graph g, search_graph sg
    WHERE g.id = sg.link AND NOT is_cycle
)
SELECT * FROM search_graph;
```

Além de prevenir ciclos, o valor da matriz é frequentemente útil por si só, representando o "caminho" tomado para alcançar qualquer linha específica.

No caso geral, quando mais de um campo precisa ser verificado para reconhecer um ciclo, use um array de linhas. Por exemplo, se precisássemos comparar os campos `f1` e `f2`:

```
WITH RECURSIVE search_graph(id, link, data, depth, is_cycle, path) AS (
    SELECT g.id, g.link, g.data, 0,
      false,
      ARRAY[ROW(g.f1, g.f2)]
    FROM graph g
  UNION ALL
    SELECT g.id, g.link, g.data, sg.depth + 1,
      ROW(g.f1, g.f2) = ANY(path),
      path || ROW(g.f1, g.f2)
    FROM graph g, search_graph sg
    WHERE g.id = sg.link AND NOT is_cycle
)
SELECT * FROM search_graph;
```

### DICA

Omitam a sintaxe `ROW()` no caso comum em que apenas um campo precisa ser verificado para reconhecer um ciclo. Isso permite que um array simples, em vez de um array de tipo composto, seja usado, ganhando eficiência.

Há sintaxe embutida para simplificar a detecção de ciclos. A consulta acima também pode ser escrita da seguinte forma:

```
WITH RECURSIVE search_graph(id, link, data, depth) AS (
    SELECT g.id, g.link, g.data, 1
    FROM graph g
  UNION ALL
    SELECT g.id, g.link, g.data, sg.depth + 1
    FROM graph g, search_graph sg
    WHERE g.id = sg.link
) CYCLE id SET is_cycle USING path
SELECT * FROM search_graph;
```

e será reescrita internamente para a forma acima. A cláusula `CYCLE` especifica primeiro a lista de colunas a serem rastreadas para detecção de ciclo, em seguida, um nome de coluna que mostrará se um ciclo foi detectado, e, finalmente, o nome de outra coluna que rastreará o caminho. As colunas ciclo e caminho serão implicitamente adicionadas às linhas de saída do CTE.

### DICA

A coluna de ciclo é calculada da mesma maneira que a coluna de ordenação de ordem primeiro, mostrada na seção anterior. Uma consulta pode ter tanto uma cláusula `SEARCH` quanto uma cláusula `CYCLE`, mas uma especificação de pesquisa de ordem primeiro e uma especificação de detecção de ciclo criariam cálculos redundantes, então é mais eficiente apenas usar a cláusula `CYCLE` e ordenar pela coluna de caminho. Se a ordenação de largura primeiro é desejada, então especificar tanto `SEARCH` quanto `CYCLE` pode ser útil.

Um truque útil para testar consultas quando você não tem certeza se elas podem repetir é colocar um `LIMIT` na consulta principal. Por exemplo, esta consulta iria repetir para sempre sem o `LIMIT`:

```
WITH RECURSIVE t(n) AS (
    SELECT 1
  UNION ALL
    SELECT n+1 FROM t
)
SELECT n FROM t LIMIT 100;
```

Isso funciona porque a implementação do PostgreSQL avalia apenas tantas linhas de uma consulta `WITH` quanto são realmente obtidas pela consulta pai. Usar esse truque em produção não é recomendado, porque outros sistemas podem funcionar de maneira diferente. Além disso, geralmente não funcionará se você fizer a consulta externa ordenar os resultados da consulta recursiva ou combiná-los com outra tabela, porque, nesse caso, a consulta externa geralmente tentará obter todas as saídas da consulta `WITH` de qualquer maneira.

### 7.8.3. Materialização da Expressão de Tabela Comum [#](#QUERIES-WITH-CTE-MATERIALIZATION)

Uma propriedade útil das consultas `WITH` é que elas são normalmente avaliadas apenas uma vez por execução da consulta pai, mesmo que sejam referenciadas mais de uma vez pela consulta pai ou pelas consultas `WITH` irmãs. Assim, cálculos caros que são necessários em vários lugares podem ser colocados dentro de uma consulta `WITH`, para evitar trabalho redundante. Outra aplicação possível é prevenir avaliações múltiplas indesejadas de funções com efeitos colaterais. No entanto, o outro lado dessa moeda é que o otimizador não é capaz de empurrar restrições da consulta pai para uma consulta `WITH` com múltiplas referências, pois isso pode afetar todas as utilizações da saída da consulta `WITH` quando ela deve afetar apenas uma. A consulta `WITH` com múltiplas referências será avaliada conforme escrito, sem supressão de linhas que a consulta pai pode descartar posteriormente. (Mas, como mencionado acima, a avaliação pode parar precocemente se as referências à consulta demandarem apenas um número limitado de linhas.)

No entanto, se uma consulta `WITH` for não recursiva e sem efeitos colaterais (ou seja, é uma consulta `SELECT` que não contém funções voláteis), ela pode ser integrada à consulta pai, permitindo a otimização conjunta dos dois níveis de consulta. Por padrão, isso acontece se a consulta pai fizer referência à consulta `WITH` apenas uma vez, mas não se fizer referência à consulta `WITH` mais de uma vez. Você pode alterar essa decisão especificando `MATERIALIZED` para forçar o cálculo separado da consulta `WITH`, ou especificando `NOT MATERIALIZED` para forçá-la a ser integrada à consulta pai. Esta última escolha arrisca o cálculo duplicado da consulta `WITH`, mas ainda pode gerar um ganho líquido se cada uso da consulta `WITH` precisar apenas de uma pequena parte da saída completa da consulta `WITH`.

Um exemplo simples dessas regras é

```
WITH w AS (
    SELECT * FROM big_table
)
SELECT * FROM w WHERE key = 123;
```

Essa consulta `WITH` será preenchida, produzindo o mesmo plano de execução que

```
SELECT * FROM big_table WHERE key = 123;
```

Em particular, se houver um índice em `key`, ele provavelmente será usado para obter apenas as linhas que possuem `key = 123`. Por outro lado, em

```
WITH w AS (
    SELECT * FROM big_table
)
SELECT * FROM w AS w1 JOIN w AS w2 ON w1.key = w2.ref
WHERE w2.key = 123;
```

a consulta `WITH` será materializada, produzindo uma cópia temporária de `big_table` que é então associada a si mesma — sem o benefício de qualquer índice. Essa consulta será executada de forma muito mais eficiente se escrita como

```
WITH w AS NOT MATERIALIZED (
    SELECT * FROM big_table
)
SELECT * FROM w AS w1 JOIN w AS w2 ON w1.key = w2.ref
WHERE w2.key = 123;
```

para que as restrições da consulta principal possam ser aplicadas diretamente aos scans do `big_table`.

Um exemplo em que `NOT MATERIALIZED` poderia ser indesejável é

```
WITH w AS (
    SELECT key, very_expensive_function(val) as f FROM some_table
)
SELECT * FROM w AS w1 JOIN w AS w2 ON w1.f = w2.f;
```

Aqui, a materialização da consulta `WITH` garante que `very_expensive_function` seja avaliado apenas uma vez por linha de tabela, e não duas vezes.

Os exemplos acima mostram apenas o uso do `WITH` com o `SELECT`, mas ele pode ser anexado da mesma maneira ao `INSERT`, `UPDATE`, `DELETE` ou `MERGE`. Em cada caso, ele efetivamente fornece uma ou mais tabelas temporárias que podem ser referenciadas no comando principal.

### 7.8.4. Declarações que modificam dados em `WITH` [#](#QUERIES-WITH-MODIFYING)

Você pode usar declarações que modificam dados (`INSERT`, `UPDATE`, `DELETE` ou `MERGE`) em `WITH`. Isso permite que você realize várias operações diferentes na mesma consulta. Um exemplo é:

```
WITH moved_rows AS (
    DELETE FROM products
    WHERE
        "date" >= '2010-10-01' AND
        "date" < '2010-11-01'
    RETURNING *
)
INSERT INTO products_log
SELECT * FROM moved_rows;
```

Essa consulta efetivamente move as linhas de `products` para `products_log`. O `DELETE` em `WITH` exclui as linhas especificadas de `products`, devolvendo seus conteúdos por meio de sua cláusula `RETURNING`; e, em seguida, a consulta principal lê essa saída e a insere em `products_log`.

Um ponto importante do exemplo acima é que a cláusula `WITH` está anexada ao `INSERT`, e não ao sub-`SELECT` dentro do `INSERT`. Isso é necessário porque as declarações que modificam dados só são permitidas em cláusulas `WITH` que estão anexadas à declaração de nível superior. No entanto, as regras normais de visibilidade `WITH` se aplicam, portanto, é possível referenciar a saída da declaração `WITH` do sub-`SELECT`.

As declarações que modificam dados em `WITH` geralmente têm cláusulas `RETURNING` (veja [Seção 6.4](dml-returning.md)), como mostrado no exemplo acima. É a saída da cláusula `RETURNING`, *não* a tabela-alvo da declaração que modifica dados, que forma a tabela temporária que pode ser referenciada pelo resto da consulta. Se uma declaração que modifica dados em `WITH` não tiver uma cláusula `RETURNING`, então ela não forma nenhuma tabela temporária e não pode ser referenciada no resto da consulta. Tal declaração será executada, não obstante. Um exemplo que não é particularmente útil é:

```
WITH t AS (
    DELETE FROM foo
)
DELETE FROM bar;
```

Esse exemplo removeria todas as linhas das tabelas `foo` e `bar`. O número de linhas afetadas relatadas ao cliente só incluirá as linhas removidas de `bar`.

As referências recursivas em declarações que modificam dados não são permitidas. Em alguns casos, é possível contornar essa limitação referenciando o resultado de um `WITH` recursivo, por exemplo:

```
WITH RECURSIVE included_parts(sub_part, part) AS (
    SELECT sub_part, part FROM parts WHERE part = 'our_product'
  UNION ALL
    SELECT p.sub_part, p.part
    FROM included_parts pr, parts p
    WHERE p.part = pr.sub_part
)
DELETE FROM parts
  WHERE part IN (SELECT part FROM included_parts);
```

Essa consulta removeria todas as subpartes diretas e indiretas de um produto.

As declarações que modificam dados em `WITH` são executadas exatamente uma vez e sempre até o término, independentemente de a consulta primária ler todas (ou qualquer) suas saídas. Observe que isso é diferente da regra para `SELECT` em `WITH`: conforme declarado na seção anterior, a execução de um `SELECT` é realizada apenas até onde a consulta primária exige sua saída.

As sub-declarações em `WITH` são executadas simultaneamente entre si e com a consulta principal. Portanto, ao usar declarações que modificam dados em `WITH`, a ordem em que as atualizações especificadas realmente ocorrem é imprevisível. Todas as declarações são executadas com o mesmo *instantâneo* (ver [Capítulo 13](mvcc.md)), então elas não podem "ver" os efeitos uns dos outros nas tabelas de destino. Isso alivia os efeitos da imprevisibilidade da ordem real das atualizações de linha, e significa que os dados de `RETURNING` são a única maneira de comunicar mudanças entre diferentes sub-declarações de `WITH` e a consulta principal. Um exemplo disso é que em

```
WITH t AS (
    UPDATE products SET price = price * 1.05
    RETURNING *
)
SELECT * FROM products;
```

o valor externo `SELECT` retornaria os preços originais antes da ação do `UPDATE`, enquanto em

```
WITH t AS (
    UPDATE products SET price = price * 1.05
    RETURNING *
)
SELECT * FROM t;
```

o canal externo `SELECT` retornaria os dados atualizados.

Tentar atualizar a mesma linha duas vezes em uma única declaração não é suportado. Apenas uma das modificações ocorre, mas não é fácil (e às vezes não é possível) prever qual delas. Isso também se aplica à exclusão de uma linha que já foi atualizada na mesma declaração: apenas a atualização é realizada. Portanto, você geralmente deve evitar tentar modificar uma única linha duas vezes em uma única declaração. Em particular, evite escrever sub-declarações `WITH` que possam afetar as mesmas linhas alteradas pela declaração principal ou uma sub-declaração irmã. Os efeitos de tal declaração não serão previsíveis.

Atualmente, qualquer tabela usada como alvo de uma declaração que modifique dados em `WITH` não deve ter uma regra condicional, nem uma regra `ALSO` nem uma regra `INSTEAD` que se expanda para múltiplas declarações.