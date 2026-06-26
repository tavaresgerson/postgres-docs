## F.10. cubo — um tipo de dados cubo multidimensional [#](#CUBE)

* [F.10.1. Sintaxe](cube.md#CUBE-SYNTAX)
* [F.10.2. Precisão](cube.md#CUBE-PRECISION)
* [F.10.3. Uso](cube.md#CUBE-USAGE)
* [F.10.4. Definições Padrão](cube.md#CUBE-DEFAULTS)
* [F.10.5. Notas](cube.md#CUBE-NOTES)
* [F.10.6. Créditos](cube.md#CUBE-CREDITS)

Este módulo implementa um tipo de dados `cube` para representar cubos multidimensionais.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.10.1. Sintaxe [#](#CUBE-SYNTAX)

[Tabela F.1](cube.md#CUBE-REPR-TABLE "Table F.1. Cube External Representations") mostra as representações externas válidas para o tipo `cube`. *`x`*, *`y`*, etc. denotam números em ponto flutuante.

**Tabela F.1. Representações Externas do Cubo**



<table>
 <thead>
  <tr>
   <th>
    Sintaxe Externa
   </th>
   <th>
    Significado
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    Um ponto unidimensional (ou intervalo unidimensional de comprimento zero)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     (
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
     )
    </code>
   </td>
   <td>
    O mesmo que acima
   </td>
  </tr>
  <tr>
   <td>
    <code>
     <em class="replaceable">
      <code>
       x1
      </code>
     </em>
     ,
     <em class="replaceable">
      <code>
       x2
      </code>
     </em>
     ,...,
     <em class="replaceable">
      <code>
       xn
      </code>
     </em>
    </code>
   </td>
   <td>
    Um ponto em um espaço n-dimensional, representado internamente como um cubo de volume zero
   </td>
  </tr>
  <tr>
   <td>
    <code>
     (
     <em class="replaceable">
      <code>
       x1
      </code>
     </em>
     ,
     <em class="replaceable">
      <code>
       x2
      </code>
     </em>
     ,...,
     <em class="replaceable">
      <code>
       xn
      </code>
     </em>
     )
    </code>
   </td>
   <td>
    O mesmo que acima
   </td>
  </tr>
  <tr>
   <td>
    <code>
     (
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
     ),(
     <em class="replaceable">
      <code>
       y
      </code>
     </em>
     )
    </code>
   </td>
   <td>
    Um intervalo unidimensional que começa em
    <em class="replaceable">
     <code>
      x
     </code>
    </em>
    e terminando em
    <em class="replaceable">
     <code>
      y
     </code>
    </em>
    ou vice-versa; a ordem não importa
   </td>
  </tr>
  <tr>
   <td>
    <code>
     [(
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
     ),(
     <em class="replaceable">
      <code>
       y
      </code>
     </em>
     )]
    </code>
   </td>
   <td>
    O mesmo que acima
   </td>
  </tr>
  <tr>
   <td>
    <code>
     (
     <em class="replaceable">
      <code>
       x1
      </code>
     </em>
     ,...,
     <em class="replaceable">
      <code>
       xn
      </code>
     </em>
     ),(
     <em class="replaceable">
      <code>
       y1
      </code>
     </em>
     ,...,
     <em class="replaceable">
      <code>
       yn
      </code>
     </em>
     )
    </code>
   </td>
   <td>
    Um cubo de n dimensões representado por um par de seus cantos opostos diagonalmente
   </td>
  </tr>
  <tr>
   <td>
    <code>
     [(
     <em class="replaceable">
      <code>
       x1
      </code>
     </em>
     ,...,
     <em class="replaceable">
      <code>
       xn
      </code>
     </em>
     ),(
     <em class="replaceable">
      <code>
       y1
      </code>
     </em>
     ,...,
     <em class="replaceable">
      <code>
       yn
      </code>
     </em>
     )]
    </code>
   </td>
   <td>
    O mesmo que acima
   </td>
  </tr>
 </tbody>
</table>










Não importa a ordem em que os cantos opostos de um cubo são inseridos. As funções `cube` trocam automaticamente os valores, se necessário, para criar uma representação interna uniforme “inferior esquerdo — superior direito”. Quando os cantos coincidem, a `cube` armazena apenas um canto juntamente com uma bandeira de “é ponto” para evitar desperdício de espaço.

O espaço em branco é ignorado na entrada, portanto `[(x),(y)]` é o mesmo que `[ ( x ), ( y ) ]`.

### F.10.2. Precisão [#](#CUBE-PRECISION)

Os valores são armazenados internamente como números de ponto flutuante de 64 bits. Isso significa que os números com mais de aproximadamente 16 dígitos significativos serão truncados.

### F.10.3. Uso [#](#CUBE-USAGE)

[Tabela F.2](cube.md#CUBE-OPERATORS-TABLE "Table F.2. Cube Operators") mostra os operadores especializados fornecidos para o tipo `cube`.

**Tabela F.2. Operadores de Cubo**



<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Operador
    </p>
    <p>
     Descrição
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube
     </code>
     <code>
      &amp;&amp;
     </code>
     <code>
      cube
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     Os cubos se sobrepõem?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube
     </code>
     <code>
      @&gt;
     </code>
     <code>
      cube
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     O primeiro cubo contém o segundo?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube
     </code>
     <code>
      &lt;@
     </code>
     <code>
      cube
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     O primeiro cubo está contido no segundo?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube
     </code>
     <code>
      -&gt;
     </code>
     <code>
      integer
     </code>
     →
     <code>
      float8
     </code>
    </p>
    <p>
     Extrai os
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     - a coordenada da (contando de 1) do cubo.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube
     </code>
     <code>
      ~&gt;
     </code>
     <code>
      integer
     </code>
     →
     <code>
      float8
     </code>
    </p>
    <p>
     Extrai os
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     - a coordenada da cuboctaedro, contando da seguinte maneira:
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     = 2
     <em class="parameter">
      <code>
       k
      </code>
     </em>
     - 1 significa limite inferior de
     <em class="parameter">
      <code>
       k
      </code>
     </em>
     -a dimensão,
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     = 2
     <em class="parameter">
      <code>
       k
      </code>
     </em>
     limite superior de
     <em class="parameter">
      <code>
       k
      </code>
     </em>
     -a dimensão. Negativo
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     denota o valor inverso da coordenada positiva correspondente. Este operador é projetado para suporte KNN-GiST.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube
     </code>
     <code>
      &lt;-&gt;
     </code>
     <code>
      cube
     </code>
     →
     <code>
      float8
     </code>
    </p>
    <p>
     Calcula a distância euclidiana entre os dois cubos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube
     </code>
     <code>
      &lt;#&gt;
     </code>
     <code>
      cube
     </code>
     →
     <code>
      float8
     </code>
    </p>
    <p>
     Calcula a distância em táxi (métrica L-1) entre os dois cubos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube
     </code>
     <code>
      &lt;=&gt;
     </code>
     <code>
      cube
     </code>
     →
     <code>
      float8
     </code>
    </p>
    <p>
     Calcula a distância Chebyshev (metrica L-inf) entre os dois cubos.
    </p>
   </td>
  </tr>
 </tbody>
</table>










Além dos operadores acima, os operadores de comparação comuns mostrados na [Tabela 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) estão disponíveis para o tipo `cube`. Esses operadores primeiro comparam as primeiras coordenadas e, se essas forem iguais, comparam as segundas coordenadas, etc. Eles existem principalmente para suportar a classe de operador de índice de árvore b para `cube`, que pode ser útil, por exemplo, se você deseja uma restrição ÚNICA em uma coluna de `cube`. Caso contrário, esse ordenamento não é de grande utilidade prática.

O módulo `cube` também fornece uma classe de operador de índice GiST para valores de `cube`. Um índice GiST de `cube` pode ser usado para pesquisar valores usando os operadores `=`, `&&`, `@>` e `<@` nas cláusulas de `WHERE`.

Além disso, um índice GiST `cube` pode ser usado para encontrar vizinhos mais próximos usando os operadores métricas `<->`, `<#>` e `<=>` em cláusulas `ORDER BY`. Por exemplo, o vizinho mais próximo do ponto 3D (0,5, 0,5, 0,5) pode ser encontrado de forma eficiente com:

```
SELECT c FROM test ORDER BY c <-> cube(array[0.5,0.5,0.5]) LIMIT 1;
```

O operador `~>` também pode ser usado dessa maneira para recuperar eficientemente os primeiros valores ordenados por uma coordenada selecionada. Por exemplo, para obter os primeiros cubos ordenados pela primeira coordenada (canto inferior esquerdo) em ordem ascendente, você pode usar a seguinte consulta:

```
SELECT c FROM test ORDER BY c ~> 1 LIMIT 5;
```

E para obter cubos 2D ordenados pela primeira coordenada do canto superior direito descendo:

```
SELECT c FROM test ORDER BY c ~> 3 DESC LIMIT 5;
```

[Tabela F.3](cube.md#CUBE-FUNCTIONS-TABLE "Table F.3. Cube Functions") mostra as funções disponíveis.

**Tabela F.3. Funções de cubo**



<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função
    </p>
    <p>
     Descrição
    </p>
    <p>
     Exemplo(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube
     </code>
     (
     <code>
      float8
     </code>
     )
     <code>
      cube
     </code>
    </p>
    <p>
     Faz um cubo unidimensional com ambas as coordenadas iguais.
    </p>
    <p>
     <code>
      cube(1)
     </code>
     →
     <code>
      (1)
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube
     </code>
     (
     <code>
      float8
     </code>
     ,
     <code>
      float8
     </code>
     )
     <code>
      cube
     </code>
    </p>
    <p>
     Faz um cubo unidimensional.
    </p>
    <p>
     <code>
      cube(1, 2)
     </code>
     →
     <code>
      (1),(2)
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube
     </code>
     (
     <code>
      float8[]
     </code>
     )
     <code>
      cube
     </code>
    </p>
    <p>
     Faz um cubo de volume zero usando as coordenadas definidas pelo array.
    </p>
    <p>
     <code>
      cube(ARRAY[1,2,3])
     </code>
     →
     <code>
      (1, 2, 3)
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube
     </code>
     (
     <code>
      float8[]
     </code>
     ,
     <code>
      float8[]
     </code>
     )
     <code>
      cube
     </code>
    </p>
    <p>
     Faz um cubo com as coordenadas superior direita e inferior esquerda definidas pelos dois arrays, que devem ter o mesmo comprimento.
    </p>
    <p>
     <code>
      cube(ARRAY[1,2], ARRAY[3,4])
     </code>
     →
     <code>
      (1, 2),(3, 4)
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube
     </code>
     (
     <code>
      cube
     </code>
     ,
     <code>
      float8
     </code>
     )
     <code>
      cube
     </code>
    </p>
    <p>
     Cria um novo cubo ao adicionar uma dimensão a um cubo existente, com os mesmos valores para ambos os pontos finais da nova coordenada. Isso é útil para construir cubos peça por peça a partir de valores calculados.
    </p>
    <p>
     <code>
      cube('(1,2),(3,4)'::cube, 5)
     </code>
     →
     <code>
      (1, 2, 5),(3, 4, 5)
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube
     </code>
     (
     <code>
      cube
     </code>
     ,
     <code>
      float8
     </code>
     ,
     <code>
      float8
     </code>
     )
     <code>
      cube
     </code>
    </p>
    <p>
     Cria um novo cubo adicionando uma dimensão a um cubo existente. Isso é útil para construir cubos peça por peça a partir de valores calculados.
    </p>
    <p>
     <code>
      cube('(1,2),(3,4)'::cube, 5, 6)
     </code>
     →
     <code>
      (1, 2, 5),(3, 4, 6)
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube_dim
     </code>
     (
     <code>
      cube
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o número de dimensões do cubo.
    </p>
    <p>
     <code>
      cube_dim('(1,2),(3,4)')
     </code>
     →
     <code>
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube_ll_coord
     </code>
     (
     <code>
      cube
     </code>
     ,
     <code>
      integer
     </code>
     )
     <code>
      float8
     </code>
    </p>
    <p>
     Retorna o
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     - o valor da coordenada da diagonal que vai do canto inferior esquerdo do cubo.
    </p>
    <p>
     <code>
      cube_ll_coord('(1,2),(3,4)', 2)
     </code>
     →
     <code>
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube_ur_coord
     </code>
     (
     <code>
      cube
     </code>
     ,
     <code>
      integer
     </code>
     )
     <code>
      float8
     </code>
    </p>
    <p>
     Retorna o
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     - o valor da coordenada da terceira dimensão para o canto superior direito do cubo.
    </p>
    <p>
     <code>
      cube_ur_coord('(1,2),(3,4)', 2)
     </code>
     →
     <code>
      4
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube_is_point
     </code>
     (
     <code>
      cube
     </code>
     )
     <code>
      boolean
     </code>
    </p>
    <p>
     Retorna verdadeiro se o cubo for um ponto, ou seja, se as duas arestas definidoras forem iguais.
    </p>
    <p>
     <code>
      cube_is_point(cube(1,1))
     </code>
     →
     <code>
      t
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube_distance
     </code>
     (
     <code>
      cube
     </code>
     ,
     <code>
      cube
     </code>
     )
     <code>
      float8
     </code>
    </p>
    <p>
     Retorna a distância entre dois cubos. Se ambos os cubos forem pontos, esta é a função de distância normal.
    </p>
    <p>
     <code>
      cube_distance('(1,2)', '(3,4)')
     </code>
     →
     <code>
      2.8284271247461903
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube_subset
     </code>
     (
     <code>
      cube
     </code>
     ,
     <code>
      integer[]
     </code>
     )
     <code>
      cube
     </code>
    </p>
    <p>
     Faz um novo cubo a partir de um cubo existente, usando uma lista de índices de dimensão de um array. Pode ser usado para extrair os pontos finais de uma única dimensão, ou para descartar as dimensões, ou para reordená-las conforme desejado.
    </p>
    <p>
     <code>
      cube_subset(cube('(1,3,5),(6,7,8)'), ARRAY[2])
     </code>
     →
     <code>
      (3),(7)
     </code>
    </p>
    <p>
     <code>
      cube_subset(cube('(1,3,5),(6,7,8)'), ARRAY[3,2,1,1])
     </code>
     →
     <code>
      (5, 3, 1, 1),(8, 7, 6, 6)
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube_union
     </code>
     (
     <code>
      cube
     </code>
     ,
     <code>
      cube
     </code>
     )
     <code>
      cube
     </code>
    </p>
    <p>
     Produz a união de dois cubos.
    </p>
    <p>
     <code>
      cube_union('(1,2)', '(3,4)')
     </code>
     →
     <code>
      (1, 2),(3, 4)
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube_inter
     </code>
     (
     <code>
      cube
     </code>
     ,
     <code>
      cube
     </code>
     )
     <code>
      cube
     </code>
    </p>
    <p>
     Produz a interseção de dois cubos.
    </p>
    <p>
     <code>
      cube_inter('(1,2)', '(3,4)')
     </code>
     →
     <code>
      (3, 4),(1, 2)
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cube_enlarge
     </code>
     (
     <em class="parameter">
      <code>
       c
      </code>
     </em>
     <code>
      cube
     </code>
     ,
     <em class="parameter">
      <code>
       r
      </code>
     </em>
     <code>
      double
     </code>
     ,
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     <code>
      integer
     </code>
     )
     <code>
      cube
     </code>
    </p>
    <p>
     Aumenta o tamanho do cubo pelo raio especificado
     <em class="parameter">
      <code>
       r
      </code>
     </em>
     em pelo menos
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     Dimensões. Se o raio for negativo, o cubo é reduzido. Todas as dimensões definidas são alteradas pelo raio.
     <em class="parameter">
      <code>
       r
      </code>
     </em>
     As coordenadas da parte inferior esquerda são diminuídas por
     <em class="parameter">
      <code>
       r
      </code>
     </em>
     e as coordenadas superiores e à direita são aumentadas por
     <em class="parameter">
      <code>
       r
      </code>
     </em>
     . Se uma coordenada inferior esquerda for aumentada para mais do que a coordenada correspondente superior direita (isso só pode acontecer quando
     <em class="parameter">
      <code>
       r
      </code>
     </em>
     &lt; 0) do que ambas as coordenadas estejam definidas em sua média. Se
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     é maior que o número de dimensões definidas e o cubo está sendo ampliado (
     <em class="parameter">
      <code>
       r
      </code>
     </em>
     &gt; 0), então dimensões extras são adicionadas para fazer
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     em conjunto; 0 é usado como o valor inicial para as coordenadas extras. Esta função é útil para criar caixas de delimitação em torno de um ponto para a busca de pontos próximos.
    </p>
    <p>
     <code>
      cube_enlarge('(1,2),(3,4)', 0.5, 3)
     </code>
     →
     <code>
      (0.5, 1.5, -0.5),(3.5, 4.5, 0.5)
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>







### F.10.4. Falhas [#](#CUBE-DEFAULTS)

Essa união:

```
select cube_union('(0,5,2),(2,3,1)', '0');
cube_union
-------------------
(0, 0, 0),(2, 5, 2)
(1 row)
```

não contradiz o senso comum, nem a interseção:

```
select cube_inter('(0,-1),(1,1)', '(-2),(2)');
cube_inter
-------------
(0, 0),(1, 0)
(1 row)
```

Em todas as operações binárias em cubos de dimensões diferentes, o cubo de menor dimensão é assumido como uma projeção cartesiana, ou seja, tendo zeros no lugar das coordenadas omitidas na representação em cadeia. Os exemplos acima são equivalentes a:

```
cube_union('(0,5,2),(2,3,1)','(0,0,0),(0,0,0)');
cube_inter('(0,-1),(1,1)','(-2,0),(2,0)');
```

O seguinte predicado de contenção usa a sintaxe de ponto, enquanto, na verdade, o segundo argumento é representado internamente por uma caixa. Essa sintaxe torna desnecessário definir um tipo de ponto separado e funções para predicados (caixa, ponto).

```
select cube_contains('(0,0),(1,1)', '0.5,0.5');
cube_contains
--------------
t
(1 row)
```

### F.10.5. Notas [#](#CUBE-NOTES)

Para exemplos de uso, veja o teste de regressão `sql/cube.sql`.

Para dificultar que as pessoas quebrem coisas, há um limite de 100 no número de dimensões dos cubos. Isso é definido em `cubedata.h` se você precisar de algo maior.

### F.10.6. Créditos [#](#CUBE-CREDITS)

Autor original: Gene Selkov, Jr. `<selkovjr@mcs.anl.gov>`, Divisão de Matemática e Ciência da Computação, Laboratório Nacional Argonne.

Meu agradecimento é principalmente ao Prof. Joe Hellerstein (<https://dsf.berkeley.edu/jmh/>) por esclarecer o espírito do GiST (<http://gist.cs.berkeley.edu/>) e ao seu antigo aluno Andy Dong por seu exemplo escrito para Illustra. Também estou grato a todos os desenvolvedores do Postgres, presentes e passados, por me permitir criar meu próprio mundo e viver nele sem interrupções. E gostaria de reconhecer minha gratidão ao Argonne Lab e ao Departamento de Energia dos EUA pelos anos de apoio fiel à minha pesquisa de banco de dados.

Mínimas atualizações para este pacote foram feitas por Bruno Wolff III `<bruno@wolff.to>` em agosto/setembro de 2002. Essas atualizações incluem a mudança da precisão de single precision para double precision e a adição de algumas novas funções.

Atualizações adicionais foram feitas por Joshua Reich `<josh@root.net>` em julho de 2006. Essas incluem `cube(float8[], float8[])` e a limpeza do código para usar o protocolo de chamada V1 em vez do protocolo V0 descontinuado.