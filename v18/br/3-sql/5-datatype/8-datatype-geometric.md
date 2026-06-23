## 8.8. Tipos geométricos [#](#DATATYPE-GEOMETRIC)

* [8.8.1. Pontos](datatype-geometric.md#DATATYPE-GEOMETRIC-POINTS)
* [8.8.2. Linhas](datatype-geometric.md#DATATYPE-LINE)
* [8.8.3. Setores de linha](datatype-geometric.md#DATATYPE-LSEG)
* [8.8.4. Caixas](datatype-geometric.md#DATATYPE-GEOMETRIC-BOXES)
* [8.8.5. Caminhos](datatype-geometric.md#DATATYPE-GEOMETRIC-PATHS)
* [8.8.6. Polígonos](datatype-geometric.md#DATATYPE-POLYGON)
* [8.8.7. Círculos](datatype-geometric.md#DATATYPE-CIRCLE)

Os tipos de dados geométricos representam objetos espaciais bidimensionais. [Tabela 8.20](datatype-geometric.md#DATATYPE-GEO-TABLE) mostra os tipos geométricos disponíveis no PostgreSQL.

**Tabela 8.20. Tipos geométricos**



<table border="1" class="table" summary="Geometric Types">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
  <col class="col4"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Name
   </th>
   <th>
    Storage Size
   </th>
   <th>
    Descrição
   </th>
   <th>
    Representation
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="type">
     point
    </code>
   </td>
   <td>
    16 bytes
   </td>
   <td>
    Ponto em um avião
   </td>
   <td>
    (x,y)
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     line
    </code>
   </td>
   <td>
    24 bytes
   </td>
   <td>
    Linha infinita
   </td>
   <td>
    {A,B,C}
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     lseg
    </code>
   </td>
   <td>
    32 bytes
   </td>
   <td>
    Seção de linha finita
   </td>
   <td>
    [(x1,y1),(x2,y2)]
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     box
    </code>
   </td>
   <td>
    32 bytes
   </td>
   <td>
    Caixa retangular
   </td>
   <td>
    (x1,y1),(x2,y2)
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     path
    </code>
   </td>
   <td>
    16+16n bytes
   </td>
   <td>
    Caminho fechado (semelhante a polígono)
   </td>
   <td>
    ((x1,y1),...)
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     path
    </code>
   </td>
   <td>
    16+16n bytes
   </td>
   <td>
    Caminho aberto
   </td>
   <td>
    [(x1,y1),...]
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     polygon
    </code>
   </td>
   <td>
    40+16n bytes
   </td>
   <td>
    Poligonal (semelhante a um caminho fechado)
   </td>
   <td>
    ((x1,y1),...)
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     circle
    </code>
   </td>
   <td>
    24 bytes
   </td>
   <td>
    Círculo
   </td>
   <td>
    &lt;(x,y),r&gt; (center point and radius)
   </td>
  </tr>
 </tbody>
</table>










Em todos esses tipos, as coordenadas individuais são armazenadas como números `double precision` (`float8`).

Um conjunto rico de funções e operadores está disponível para realizar várias operações geométricas, como escala, tradução, rotação e determinação de interseções. Eles são explicados em [Seção 9.11](functions-geometry.md).

### 8.8.1. Pontos [#](#DATATYPE-GEOMETRIC-POINTS)

Os pontos são os blocos de construção fundamentais bidimensionais para tipos geométricos. Os valores do tipo `point` são especificados usando qualquer uma das seguintes sintaxes:

```
( x , y )
  x , y
```

onde *`x`* e *`y`* são as respectivas coordenadas, como números em ponto flutuante.

Os pontos são exibidos usando a primeira sintaxe.

### 8.8.2. Linhas [#](#DATATYPE-LINE)

As linhas são representadas pela equação linear *`A`*x + *`B`*y + *`C`* = 0, onde *`A`* e *`B`* não são ambos iguais a zero. Os valores do tipo `line` são inseridos e saem na seguinte forma:

```
{ A, B, C }
```

Alternativamente, qualquer uma das seguintes formas pode ser usada para entrada:

```
[ ( x1 , y1 ) , ( x2 , y2 ) ]
( ( x1 , y1 ) , ( x2 , y2 ) )
  ( x1 , y1 ) , ( x2 , y2 )
    x1 , y1   ,   x2 , y2
```

onde `(x1,y1)` e `(x2,y2)` são dois pontos diferentes na linha.

### 8.8.3. Segmentos de linha [#](#DATATYPE-LSEG)

Os segmentos de linha são representados por pares de pontos que são os pontos finais do segmento. Os valores do tipo `lseg` são especificados usando qualquer uma das seguintes sintaxes:

```
[ ( x1 , y1 ) , ( x2 , y2 ) ]
( ( x1 , y1 ) , ( x2 , y2 ) )
  ( x1 , y1 ) , ( x2 , y2 )
    x1 , y1   ,   x2 , y2
```

onde `(x1,y1)` e `(x2,y2)` são os pontos finais do segmento de linha.

Os segmentos de linha são produzidos usando a primeira sintaxe.

### 8.8.4. Caixas [#](#DATATYPE-GEOMETRIC-BOXES)

As caixas são representadas por pares de pontos que são cantos opostos da caixa. Os valores do tipo `box` são especificados usando qualquer uma das seguintes sintaxes:

```
( ( x1 , y1 ) , ( x2 , y2 ) )
  ( x1 , y1 ) , ( x2 , y2 )
    x1 , y1   ,   x2 , y2
```

onde `(x1,y1)` e `(x2,y2)` são quaisquer dois cantos opostos da caixa.

As caixas são produzidas usando a segunda sintaxe.

Qualquer dois cantos opostos podem ser fornecidos na entrada, mas os valores serão reorganizados conforme necessário para armazenar os cantos superior direito e inferior esquerdo, nessa ordem.

### 8.8.5. Caminhos [#](#DATATYPE-GEOMETRIC-PATHS)

Os caminhos são representados por listas de pontos conectados. Os caminhos podem ser *abertos*, onde os primeiros e últimos pontos da lista são considerados não conectados, ou *fechados*, onde os primeiros e últimos pontos são considerados conectados.

Os valores do tipo `path` são especificados usando qualquer uma das seguintes sintaxes:

```
[ ( x1 , y1 ) , ... , ( xn , yn ) ]
( ( x1 , y1 ) , ... , ( xn , yn ) )
  ( x1 , y1 ) , ... , ( xn , yn )
  ( x1 , y1   , ... ,   xn , yn )
    x1 , y1   , ... ,   xn , yn
```

onde os pontos são os pontos finais dos segmentos de linha que compõem o caminho. Os colchetes quadrados (`[]`) indicam um caminho aberto, enquanto as parênteses (`()`) indicam um caminho fechado. Quando os colchetes externos são omitidos, como nas terceiras a quinta sintáticas, um caminho fechado é assumido.

Os caminhos são exibidos usando a primeira ou a segunda sintaxe, conforme apropriado.

### 8.8.6. Polígonos [#](#DATATYPE-POLYGON)

Os polígonos são representados por listas de pontos (os vértices do polígono). Os polígonos são muito semelhantes a caminhos fechados; a diferença semântica essencial é que um polígono é considerado para incluir a área dentro dele, enquanto um caminho não é.

Uma diferença importante entre polígonos e caminhos é que a representação armazenada de um polígono inclui sua caixa menor de delimitação. Isso acelera certas operações de busca, embora a computação da caixa de delimitação aumente o overhead ao construir novos polígonos.

Os valores do tipo `polygon` são especificados usando qualquer uma das seguintes sintaxes:

```
( ( x1 , y1 ) , ... , ( xn , yn ) )
  ( x1 , y1 ) , ... , ( xn , yn )
  ( x1 , y1   , ... ,   xn , yn )
    x1 , y1   , ... ,   xn , yn
```

onde os pontos são os pontos finais dos segmentos de linha que compõem a borda do polígono.

Os polígonos são produzidos usando a primeira sintaxe.

### 8.8.7. Círculos [#](#DATATYPE-CIRCLE)

Os círculos são representados por um ponto central e raio. Os valores do tipo `circle` são especificados usando qualquer uma das seguintes sintaxes:

```
< ( x , y ) , r >
( ( x , y ) , r )
  ( x , y ) , r
    x , y   , r
```

onde `(x,y)` é o ponto central e *`r`* é o raio do círculo.

Os círculos são produzidos usando a primeira sintaxe.