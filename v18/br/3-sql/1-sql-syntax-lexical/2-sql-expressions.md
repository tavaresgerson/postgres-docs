#### 4.2. Expressões de Valor [#](#SQL-EXPRESSIONS)

* [4.2.1. Referências de Coluna](sql-expressions.md#SQL-EXPRESSIONS-COLUMN-REFS)
* [4.2.2. Parâmetros Posicionais](sql-expressions.md#SQL-EXPRESSIONS-PARAMETERS-POSITIONAL)
* [4.2.3. Subíndices](sql-expressions.md#SQL-EXPRESSIONS-SUBSCRIPTS)
* [4.2.4. Seleção de Campo](sql-expressions.md#FIELD-SELECTION)
* [4.2.5. Invocações de Operadores](sql-expressions.md#SQL-EXPRESSIONS-OPERATOR-CALLS)
* [4.2.6. Chamadas de Função](sql-expressions.md#SQL-EXPRESSIONS-FUNCTION-CALLS)
* [4.2.7. Expressões Agregadas](sql-expressions.md#SYNTAX-AGGREGATES)
* [4.2.8. Chamadas de Função de Janela](sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS)
* [4.2.9. Casts de Tipo](sql-expressions.md#SQL-SYNTAX-TYPE-CASTS)
* [4.2.10. Expressões de Colaboração](sql-expressions.md#SQL-SYNTAX-COLLATE-EXPRS)
* [4.2.11. Subconsultas Escalares](sql-expressions.md#SQL-SYNTAX-SCALAR-SUBQUERIES)
* [4.2.12. Construtores de Array](sql-expressions.md#SQL-SYNTAX-ARRAY-CONSTRUCTORS)
* [4.2.13. Construtores de Linha](sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS)
* [4.2.14. Regras de Avaliação de Expressões](sql-expressions.md#SYNTAX-EXPRESS-EVAL)

As expressões de valor são usadas em uma variedade de contextos, como na lista de destino do comando `SELECT`, como novos valores de coluna em `INSERT` ou `UPDATE`, ou em condições de busca em vários comandos. O resultado de uma expressão de valor é às vezes chamado de *escalar*, para distingui-la do resultado de uma expressão de tabela (que é uma tabela). Portanto, as expressões de valor também são chamadas de *expressões escalares* (ou até mesmo simplesmente *expressões*). A sintaxe da expressão permite o cálculo de valores a partir de partes primitivas usando operações aritméticas, lógicas, de conjunto e outras.

Uma expressão de valor é uma das seguintes:

* Um valor constante ou literal
* Uma referência de coluna
* Uma referência de parâmetro posicional, no corpo de uma definição de função ou em uma declaração preparada
* Uma expressão subscrita
* Uma expressão de seleção de campo
* Uma invocação de operador
* Uma chamada de função
* Uma expressão agregada
* Uma chamada de função de janela
* Uma cast de tipo
* Uma expressão de collation
* Uma subconsulta escalar
* Um construtor de matriz
* Um construtor de linha
* Outra expressão de valor entre parênteses (usada para agrupar subexpressões e sobrepor a precedência)

Além dessa lista, há vários construtos que podem ser classificados como expressão, mas que não seguem nenhuma regra de sintaxe geral. Esses geralmente têm a semântica de uma função ou operador e são explicados na localização apropriada em [Capítulo 9](functions.md). Um exemplo é a cláusula `IS NULL`.

Já discutimos as constantes em [Seção 4.1.2](sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS). As seções seguintes discutem as opções restantes.

##### 4.2.1. Referências de coluna [#](#SQL-EXPRESSIONS-COLUMN-REFS)

Uma coluna pode ser referenciada na forma:

```
correlation.columnname
```

*`correlation`* é o nome de uma tabela (possivelmente qualificada com o nome de um esquema), ou um alias para uma tabela definida por meio de uma cláusula `FROM`. O nome de correlação e o ponto de separação podem ser omitidos se o nome da coluna for único em todas as tabelas utilizadas na consulta atual. (Veja também [Capítulo 7](queries.md).)

##### 4.2.2. Parâmetros Posicionais [#](#SQL-EXPRESSIONS-PARAMETERS-POSITIONAL)

Uma referência de parâmetro posicional é usada para indicar um valor que é fornecido externamente a uma declaração SQL. Os parâmetros são usados em definições de funções SQL e em consultas preparadas. Algumas bibliotecas de cliente também suportam especificar valores de dados separadamente da string de comando SQL, nesse caso, os parâmetros são usados para referenciar os valores de dados fora da linha. A forma de uma referência de parâmetro é:

```
$number
```

Por exemplo, considere a definição de uma função, `dept`, como:

```
CREATE FUNCTION dept(text) RETURNS dept
    AS $$ SELECT * FROM dept WHERE name = $1 $$
    LANGUAGE SQL;
```

Aqui, o `$1` refere-se ao valor do primeiro argumento da função sempre que a função é invocada.

##### 4.2.3. Subscripts [#](#SQL-EXPRESSIONS-SUBSCRIPTS)

Se uma expressão produzir um valor de um tipo de matriz, então um elemento específico do valor da matriz pode ser extraído escrevendo

```
expression[subscript]
```

ou múltiplos elementos adjacentes (um "corte de matriz") podem ser extraídos escrevendo

```
expression[lower_subscript:upper_subscript]
```

(Aqui, os colchetes `[ ]` devem aparecer literalmente.) Cada *`subscript`* é, por si só, uma expressão, que será arredondada para o valor inteiro mais próximo.

Em geral, o array *`expression`* deve ser entre parênteses, mas os parênteses podem ser omitidos quando a expressão a ser subscrita é apenas uma referência de coluna ou um parâmetro posicional. Além disso, múltiplos subíndices podem ser concatenados quando o array original é multidimensional. Por exemplo:

```
mytable.arraycolumn[4]
mytable.two_d_column[17][34]
$1[10:42]
(arrayfunction(a,b))[42]
```

As chaves na última expressão são necessárias. Consulte [Seção 8.15](arrays.md) para mais informações sobre arrays.

##### 4.2.4. Seleção do campo [#](#FIELD-SELECTION)

Se uma expressão produzir um valor de um tipo composto (tipo de linha), então um campo específico da linha pode ser extraído escrevendo

```
expression.fieldname
```

Em geral, a linha *`expression`* deve ser colocada entre parênteses, mas os parênteses podem ser omitidos quando a expressão a ser selecionada é apenas uma referência de tabela ou um parâmetro posicional. Por exemplo:

```
mytable.mycolumn
$1.somecolumn
(rowfunction(a,b)).col3
```

(Assim, uma referência qualificada de coluna é, na verdade, apenas um caso especial da sintaxe de seleção de campo.) Um caso especial importante é extrair um campo de uma coluna de tabela que é de um tipo composto:

```
(compositecol).somefield
(mytable.compositecol).somefield
```

As chaves de parênteses são necessárias aqui para mostrar que `compositecol` é o nome de uma coluna, não o nome de uma tabela, ou que `mytable` é o nome de uma tabela, não o nome de um esquema, no segundo caso.

Você pode solicitar todos os campos de um valor composto escrevendo `.*`:

```
(compositecol).*
```

Essa notação se comporta de maneira diferente, dependendo do contexto; consulte [Seção 8.16.5](rowtypes.md#ROWTYPES-USAGE) para obter detalhes.

##### 4.2.5. Invocações do Operador [#](#SQL-EXPRESSIONS-OPERATOR-CALLS)

Existem duas possíveis sintaxes para uma invocação de operador:

<table border="0" class="simplelist" summary="Simple list">
 <tr>
  <td>
   <em class="replaceable">
    <code>
     expression
    </code>
   </em>
   <em class="replaceable">
    <code>
     operator
    </code>
   </em>
   <em class="replaceable">
    <code>
     expression
    </code>
   </em>
   (operador binário de infixo)
  </td>
 </tr>
 <tr>
  <td>
   <em class="replaceable">
    <code>
     operator
    </code>
   </em>
   <em class="replaceable">
    <code>
     expression
    </code>
   </em>
   (operador de prefixo unário)
  </td>
 </tr>
</table>

onde o *`operator`* segue as regras de sintaxe do [Seção 4.1.3](sql-syntax-lexical.md#SQL-SYNTAX-OPERATORS), ou é uma das palavras-chave `AND`, `OR` e `NOT`, ou é um nome de operador qualificado na forma:

```
OPERATOR(schema.operatorname)
```

Quais operadores específicos existem e se são unários ou binários depende do que os operadores foram definidos pelo sistema ou pelo usuário. [Capítulo 9] (functions.md "Chapter 9. Functions and Operators") descreve os operadores embutidos.

##### 4.2.6. Chamadas de função [#](#SQL-EXPRESSIONS-FUNCTION-CALLS)

A sintaxe para uma chamada de função é o nome de uma função (possivelmente qualificada com o nome de um esquema), seguido de sua lista de argumentos entre parênteses:

```
function_name ([expression [, expression ... ]] )
```

Por exemplo, o seguinte calcula a raiz quadrada de 2:

```
sqrt(2)
```

A lista de funções embutidas está em [Capítulo 9](functions.md). Outras funções podem ser adicionadas pelo usuário.

Ao emitir consultas em um banco de dados onde alguns usuários desconfiam dos outros, observe as precauções de segurança da [Seção 10.3](typeconv-func.md) ao escrever chamadas de função.

Os argumentos podem ter nomes opcionais. Consulte a Seção 4.3 para obter detalhes. [(sql-syntax-calling-funcs.md "4.3. Calling Functions")]

Nota

Uma função que recebe um único argumento de tipo composto pode ser chamada opcionalmente usando a sintaxe de seleção de campo, e, reciprocamente, a seleção de campo pode ser escrita em estilo funcional. Ou seja, as notações `col(table)` e `table.col` são intercambiáveis. Esse comportamento não é padrão SQL, mas é fornecido no PostgreSQL porque permite o uso de funções para emular “campos calculados”. Para mais informações, consulte [Seção 8.16.5](rowtypes.md#ROWTYPES-USAGE).

##### 4.2.7. Expressões agregadas [#](#SYNTAX-AGGREGATES)

Uma expressão agregada representa a aplicação de uma função agregada nas linhas selecionadas por uma consulta. Uma função agregada reduz múltiplos inputs a um único valor de saída, como a soma ou a média dos inputs. A sintaxe de uma expressão agregada é uma das seguintes:

```
aggregate_name (expression [ , ... ] [ order_by_clause ] ) [ FILTER ( WHERE filter_clause ) ]
aggregate_name (ALL expression [ , ... ] [ order_by_clause ] ) [ FILTER ( WHERE filter_clause ) ]
aggregate_name (DISTINCT expression [ , ... ] [ order_by_clause ] ) [ FILTER ( WHERE filter_clause ) ]
aggregate_name ( * ) [ FILTER ( WHERE filter_clause ) ]
aggregate_name ( [ expression [ , ... ] ] ) WITHIN GROUP ( order_by_clause ) [ FILTER ( WHERE filter_clause ) ]
```

onde *`aggregate_name`* é um agregado previamente definido (possivelmente qualificado com um nome de esquema) e *`expression`* é qualquer expressão de valor que não contenha, por si só, uma expressão de agregado ou uma chamada de função de janela. Os opcionais *`order_by_clause`* e *`filter_clause`* são descritos abaixo.

A primeira forma de expressão agregada invoca o agregado uma vez para cada linha de entrada. A segunda forma é a mesma que a primeira, uma vez que `ALL` é o padrão. A terceira forma invoca o agregado uma vez para cada valor distinto da expressão (ou conjunto distinto de valores, para múltiplas expressões) encontrado nas linhas de entrada. A quarta forma invoca o agregado uma vez para cada linha de entrada; uma vez que nenhum valor de entrada específico é especificado, geralmente é útil apenas para a função agregada `count(*)`. A última forma é usada com funções agregadas de *conjunto ordenado*, que são descritas abaixo.

A maioria das funções agregadas ignora entradas nulos, de modo que as linhas nas quais uma ou mais expressões geram null são descartadas. Isso pode ser assumido, a menos que especificado de outra forma, para todos os agregados embutidos.

Por exemplo, `count(*)` fornece o número total de linhas de entrada; `count(f1)` fornece o número de linhas de entrada nas quais `f1` não é nulo, uma vez que `count` ignora os nulos; e `count(distinct f1)` fornece o número de valores distintos não nulos de `f1`.

Normalmente, as linhas de entrada são alimentadas para a função agregada em uma ordem não especificada. Em muitos casos, isso não importa; por exemplo, `min` produz o mesmo resultado, independentemente da ordem em que recebe as entradas. No entanto, algumas funções agregadas (como `array_agg` e `string_agg`) produzem resultados que dependem da ordem das linhas de entrada. Ao usar uma dessas funções agregadas, o *`order_by_clause`* opcional pode ser usado para especificar a ordem desejada. O *`order_by_clause`* tem a mesma sintaxe que para uma cláusula de nível de consulta `ORDER BY`, conforme descrito em [Seção 7.5](queries-order.md)), exceto que suas expressões são sempre apenas expressões e não podem ser nomes de colunas de saída ou números. Por exemplo:

```
WITH vals (v) AS ( VALUES (1),(3),(4),(3),(2) )
SELECT array_agg(v ORDER BY v DESC) FROM vals;
  array_agg
-------------
 {4,3,3,2,1}
```

Como o `jsonb` só mantém a última chave correspondente, a ordem de suas chaves pode ser significativa:

```
WITH vals (k, v) AS ( VALUES ('key0','1'), ('key1','3'), ('key1','2') )
SELECT jsonb_object_agg(k, v ORDER BY v) FROM vals;
      jsonb_object_agg
----------------------------
 {"key0": "1", "key1": "3"}
```

Ao lidar com funções agregadas de múltiplos argumentos, observe que a cláusula `ORDER BY` vem após todos os argumentos agregados. Por exemplo, escreva o seguinte:

```
SELECT string_agg(a, ',' ORDER BY a) FROM table;
```

não assim:

```
SELECT string_agg(a ORDER BY a, ',') FROM table;  -- incorrect
```

Este último é sintaticamente válido, mas representa uma chamada de uma função agregada de um único argumento com duas chaves `ORDER BY` (a segunda sendo bastante inútil, uma vez que é uma constante).

Se `DISTINCT` for especificado com um *`order_by_clause`*, as expressões `ORDER BY` só podem fazer referência a colunas da lista `DISTINCT`. Por exemplo:

```
WITH vals (v) AS ( VALUES (1),(3),(4),(3),(2) )
SELECT array_agg(DISTINCT v ORDER BY v DESC) FROM vals;
 array_agg
-----------
 {4,3,2,1}
```

Colocar `ORDER BY` na lista de argumentos regular do agregado, conforme descrito até agora, é usado ao ordenar as linhas de entrada para agregados de propósito geral e estatísticos, para os quais a ordenação é opcional. Existe uma subclasse de funções agregadas chamada *agregados de conjunto ordenado* para os quais um *`order_by_clause`* é *requerido*, geralmente porque o cálculo do agregado é sensível apenas em termos de uma ordem específica de suas linhas de entrada. Exemplos típicos de agregados de conjunto ordenado incluem cálculos de classificação e percentil. Para um agregado de conjunto ordenado, o *`order_by_clause`* é escrito dentro de `WITHIN GROUP (...)`, como mostrado na alternativa de sintaxe final acima. As expressões em *`order_by_clause`* são avaliadas uma vez por linha de entrada, assim como os argumentos regulares do agregado, classificadas conforme os requisitos do *`order_by_clause`*, e fornecidas à função agregada como argumentos de entrada. (Isso é diferente do caso de um *`WITHIN GROUP`* não `order_by_clause`, que não é tratado como argumento(s) para a função agregada.) As expressões de argumento que precedem `WITHIN GROUP`, se houver, são chamadas de *argumentos diretos* para diferenciá-las dos *argumentos agregados* listados em *`order_by_clause`*. Ao contrário dos argumentos regulares do agregado, os argumentos diretos são avaliados apenas uma vez por chamada de agregado, não uma vez por linha de entrada. Isso significa que eles podem conter variáveis apenas se essas variáveis forem agrupadas por `GROUP BY`; essa restrição é a mesma se os argumentos diretos não estivessem dentro de uma expressão agregada. Os argumentos diretos são tipicamente usados para coisas como frações de percentil, que só fazem sentido como um único valor por cálculo de agregação. A lista de argumentos diretos pode ser vazia; nesse caso, escreva apenas `()` e não `(*)`. (O PostgreSQL realmente aceitará qualquer uma dessas ortografias, mas apenas a primeira maneira está em conformidade com o padrão SQL.)

Um exemplo de uma chamada de agregado de conjunto ordenado é:

```
SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY income) FROM households;
 percentile_cont
-----------------
           50489
```

que obtém o valor do percentil 50, ou mediana, da coluna `income` da tabela `households`. Aqui, `0.5` é um argumento direto; não faria sentido que a fração de percentil fosse um valor variando entre as linhas.

Se `FILTER` for especificado, então apenas as linhas de entrada para as quais *`filter_clause`* é avaliada como verdadeira são alimentadas na função agregada; outras linhas são descartadas. Por exemplo:

```
SELECT
    count(*) AS unfiltered,
    count(*) FILTER (WHERE i < 5) AS filtered
FROM generate_series(1,10) AS s(i);
 unfiltered | filtered
------------+----------
         10 |        4
(1 row)
```

As funções agregadas predefinidas são descritas em [Seção 9.21](functions-aggregate.md). Outras funções agregadas podem ser adicionadas pelo usuário.

Uma expressão agregada só pode aparecer na lista de resultados ou na cláusula `HAVING` de um comando `SELECT`. É proibido em outras cláusulas, como `WHERE`, porque essas cláusulas são avaliadas logicamente antes de os resultados dos agregados serem formados.

Quando uma expressão agregada aparece em uma subconsulta (ver [Seção 4.2.11] e [Seção 9.24] (sql-expressions.md#SQL-SYNTAX-SCALAR-SUBQUERIES "4.2.11. Scalar Subqueries") e [(functions-subquery.md "9.24. Subquery Expressions")]), o agregado é normalmente avaliado sobre as linhas da subconsulta. Mas uma exceção ocorre se os argumentos do agregado (e *`filter_clause`* se houver algum) contiverem apenas variáveis de nível externo: o agregado pertence então ao nível externo mais próximo, e é avaliado sobre as linhas dessa consulta. A expressão agregada como um todo é então uma referência externa para a subconsulta em que aparece, e atua como uma constante em qualquer avaliação dessa subconsulta. A restrição de aparecer apenas na lista de resultados ou na cláusula `HAVING` se aplica em relação ao nível de consulta ao qual o agregado pertence.

##### 4.2.8. Chamadas de função de janela [#](#SYNTAX-WINDOW-FUNCTIONS)

Uma chamada de função de janela representa a aplicação de uma função semelhante a agregada sobre uma parte das linhas selecionadas por uma consulta. Ao contrário das chamadas de agregação não de janela, essa não está vinculada à agrupamento das linhas selecionadas em uma única linha de saída — cada linha permanece separada na saída da consulta. No entanto, a função de janela tem acesso a todas as linhas que seriam parte do grupo da linha atual de acordo com a especificação de agrupamento (lista `PARTITION BY`) da chamada de função de janela. A sintaxe de uma chamada de função de janela é uma das seguintes:

```
function_name ([expression [, expression ... ]]) [ FILTER ( WHERE filter_clause ) ] OVER window_name
function_name ([expression [, expression ... ]]) [ FILTER ( WHERE filter_clause ) ] OVER ( window_definition )
function_name ( * ) [ FILTER ( WHERE filter_clause ) ] OVER window_name
function_name ( * ) [ FILTER ( WHERE filter_clause ) ] OVER ( window_definition )
```

onde *`window_definition`* tem a sintaxe

```
[ existing_window_name ]
[ PARTITION BY expression [, ...] ]
[ ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS { FIRST | LAST } ] [, ...] ]
[ frame_clause ]
```

O opcional *`frame_clause`* pode ser um dos

```
{ RANGE | ROWS | GROUPS } frame_start [ frame_exclusion ]
{ RANGE | ROWS | GROUPS } BETWEEN frame_start AND frame_end [ frame_exclusion ]
```

onde *`frame_start`* e *`frame_end`* podem ser um dos

```
UNBOUNDED PRECEDING
offset PRECEDING
CURRENT ROW
offset FOLLOWING
UNBOUNDED FOLLOWING
```

e *`frame_exclusion`* pode ser um dos

```
EXCLUDE CURRENT ROW
EXCLUDE GROUP
EXCLUDE TIES
EXCLUDE NO OTHERS
```

Aqui, *`expression`* representa qualquer expressão de valor que não contenha, por si só, chamadas de função de janela.

*`window_name`* é uma referência a uma especificação de janela nomeada definida na cláusula `WINDOW` da consulta. Alternativamente, um *`window_definition`* completo pode ser dado entre parênteses, usando a mesma sintaxe que para definir uma janela nomeada na cláusula `WINDOW`; veja a página de referência [SELECT](sql-select.md "SELECT") para detalhes. Vale ressaltar que `OVER wname` não é exatamente equivalente a `OVER (wname ...)`; este último implica a cópia e modificação da definição da janela, e será rejeitada se a especificação da janela referenciada incluir uma cláusula de quadro.

A cláusula `PARTITION BY` agrupa as linhas da consulta em *partições*, que são processadas separadamente pela função de janela. `PARTITION BY` funciona de maneira semelhante a uma cláusula de nível de consulta `GROUP BY`, exceto que suas expressões são sempre apenas expressões e não podem ser nomes de colunas de saída ou números. Sem `PARTITION BY`, todas as linhas produzidas pela consulta são tratadas como uma única partição. A cláusula `ORDER BY` determina a ordem em que as linhas de uma partição são processadas pela função de janela. Ela funciona de maneira semelhante a uma cláusula de nível de consulta `ORDER BY`, mas também não pode usar nomes de colunas de saída ou números. Sem `ORDER BY`, as linhas são processadas em uma ordem não especificada.

O *`frame_clause` especifica o conjunto de linhas que constituem o *quadro de janela*, que é um subconjunto da partição atual, para aquelas funções de janela que atuam no quadro em vez do conjunto inteiro da partição. O conjunto de linhas no quadro pode variar dependendo da linha atual. O quadro pode ser especificado no modo de `RANGE`, `ROWS` ou `GROUPS`; em cada caso, ele vai do *`frame_start`* ao *`frame_end`*. Se *`frame_end`* for omitido, o final por padrão é `CURRENT ROW`.

Um *`frame_start`* de `UNBOUNDED PRECEDING` significa que o quadro começa com a primeira linha da partição, e, de forma semelhante, um *`frame_end`* de `UNBOUNDED FOLLOWING` significa que o quadro termina com a última linha da partição.

No modo `RANGE` ou `GROUPS`, um *`frame_start`* de `CURRENT ROW` significa que o quadro começa com a primeira *peer* da linha atual (uma linha que a cláusula `ORDER BY` da janela classifica como equivalente à linha atual), enquanto um *`frame_end`* de `CURRENT ROW` significa que o quadro termina com a última linha peer da linha atual. No modo `ROWS`, `CURRENT ROW` simplesmente significa a linha atual.

Nas opções de quadro *`offset`* `PRECEDING` e *`offset` `FOLLOWING` , o *`offset`* deve ser uma expressão que não contenha variáveis, funções agregadas ou funções de janela. O significado do *`offset`* depende do modo do quadro:

* No modo `ROWS`, o *`offset`* deve retornar um inteiro não nulo e não negativo, e a opção significa que o quadro começa ou termina o número especificado de linhas antes ou depois da linha atual.
* No modo `GROUPS`, o *`offset`* deve retornar novamente um inteiro não nulo e não negativo, e a opção significa que o quadro começa ou termina o número especificado de *grupos de pares* antes ou depois do grupo de pares da linha atual, onde um grupo de pares é um conjunto de linhas que são equivalentes na ordem `ORDER BY`. (Deve haver uma cláusula `ORDER BY` na definição da janela para usar o modo `GROUPS`.
* No modo `RANGE`, essas opções exigem que a cláusula `ORDER BY` especifique exatamente uma coluna. O *`offset`* especifica a diferença máxima entre o valor daquela coluna na linha atual e seu valor nas linhas anteriores ou seguintes do quadro. O tipo de dados da expressão *`offset`* varia dependendo do tipo de dados da coluna de ordenação. Para colunas de ordenação numérica, é tipicamente do mesmo tipo que a coluna de ordenação, mas para colunas de ordenação de datas, é um `interval`. Por exemplo, se a coluna de ordenação for do tipo `date` ou `timestamp`, pode-se escrever `RANGE BETWEEN '1 day' PRECEDING AND '10 days' FOLLOWING`. O *`offset`* ainda é necessário ser não nulo e não negativo, embora o significado de “não negativo” dependa de seu tipo de dados.

De qualquer forma, a distância até o final do quadro é limitada pela distância até o final da partição, de modo que, para as linhas próximas às extremidades da partição, o quadro pode conter menos linhas do que em outras partes.

Observe que, tanto no modo `ROWS` quanto no modo `GROUPS`, `0 PRECEDING` e `0 FOLLOWING` são equivalentes a `CURRENT ROW`. Isso normalmente também ocorre no modo `RANGE`, pois há um significado apropriado específico para o tipo de dado de “zero”.

A opção *`frame_exclusion`* permite que as linhas ao redor da linha atual sejam excluídas do quadro, mesmo que elas fossem incluídas de acordo com as opções de início e fim do quadro. `EXCLUDE CURRENT ROW` exclui a linha atual do quadro. `EXCLUDE GROUP` exclui a linha atual e seus pares de ordenação do quadro. `EXCLUDE TIES` exclui quaisquer pares da linha atual do quadro, mas não a própria linha atual. `EXCLUDE NO OTHERS` especifica simplesmente explicitamente o comportamento padrão de não excluir a linha atual ou seus pares.

A opção padrão de enquadramento é `RANGE UNBOUNDED PRECEDING`, que é a mesma que `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. Com `ORDER BY`, isso define o enquadramento para todas as linhas da partição, desde o início até a última linha com o mesmo `ORDER BY` da linha atual. Sem `ORDER BY`, isso significa que todas as linhas da partição são incluídas no enquadramento da janela, uma vez que todas as linhas se tornam pares da linha atual.

As restrições são que *`frame_start`* não pode ser `UNBOUNDED FOLLOWING`, *`frame_end`* não pode ser `UNBOUNDED PRECEDING`, e a opção *`frame_end`* não pode aparecer anteriormente na lista acima de opções de *`frame_start`* e *`frame_end`* do que a opção *`frame_start`* — por exemplo, `RANGE BETWEEN CURRENT ROW AND offset PRECEDING` não é permitido. Mas, por exemplo, `ROWS BETWEEN 7 PRECEDING AND 8 PRECEDING` é permitido, mesmo que ela nunca selecionará quaisquer linhas.

Se `FILTER` for especificado, então apenas as linhas de entrada para as quais o *`filter_clause`* é verdadeiro são alimentadas na função de janela; outras linhas são descartadas. Apenas as funções de janela que são agregados aceitam uma cláusula `FILTER`.

As funções de janela embutidas são descritas em [Tabela 9.67](functions-window.md#FUNCTIONS-WINDOW-TABLE). Outras funções de janela podem ser adicionadas pelo usuário. Além disso, qualquer agregado geral ou estatístico definido pelo usuário ou embutido pode ser usado como uma função de janela. (Os agregados de conjunto ordenado e hipotético atualmente não podem ser usados como funções de janela.)

As sintaxes que utilizam `*` são usadas para chamar funções agregadas sem parâmetros como funções de janela, por exemplo, `count(*) OVER (PARTITION BY x ORDER BY y)`. O asterisco (`*`) não é customariamente usado para funções específicas de janela. As funções específicas de janela não permitem que `DISTINCT` ou `ORDER BY` sejam usadas na lista de argumentos da função.

As chamadas de função de janela são permitidas apenas na lista `SELECT` e na cláusula `ORDER BY` da consulta.

Mais informações sobre as funções de janela podem ser encontradas em [Seção 3.5](tutorial-window.md), [Seção 9.22](functions-window.md) e [Seção 7.2.5](queries-table-expressions.md#QUERIES-WINDOW).

##### 4.2.9. Moldagem por Tipo [#](#SQL-SYNTAX-TYPE-CASTS)

Uma cast de tipo especifica uma conversão de um tipo de dados para outro. O PostgreSQL aceita dois sintaxe equivalentes para casts de tipo:

```
CAST ( expression AS type )
expression::type
```

A sintaxe do `CAST` é conforme com a SQL; a sintaxe com `::` é o uso histórico do PostgreSQL.

Quando um cast é aplicado a uma expressão de valor de um tipo conhecido, ele representa uma conversão de tipo em tempo de execução. O cast só terá sucesso se uma operação de conversão de tipo adequada tiver sido definida. Observe que isso é sutilmente diferente do uso de casts com constantes, conforme mostrado em [Seção 4.1.2.7](sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS-GENERIC). Um cast aplicado a uma literal de string sem modificação representa a atribuição inicial de um tipo a um valor constante literal, e, portanto, terá sucesso para qualquer tipo (se o conteúdo da literal de string for uma sintaxe de entrada aceitável para o tipo de dados).

Uma conversão explícita de tipo geralmente pode ser omitida se não houver ambiguidade quanto ao tipo que uma expressão de valor deve produzir (por exemplo, quando é atribuída a uma coluna de tabela); o sistema aplicará automaticamente uma conversão de tipo nesses casos. No entanto, a conversão automática é realizada apenas para conversões marcadas como "OK para aplicar implicitamente" nos catálogos do sistema. Outras conversões devem ser invocadas com sintaxe de conversão explícita. Essa restrição visa impedir que conversões surpreendentes sejam aplicadas silenciosamente.

Também é possível especificar uma conversão de tipo usando uma sintaxe semelhante a uma função:

```
typename ( expression )
```

No entanto, isso só funciona para tipos cujos nomes também são válidos como nomes de função. Por exemplo, `double precision` não pode ser usado dessa maneira, mas o equivalente `float8` pode. Além disso, os nomes `interval`, `time` e `timestamp` só podem ser usados dessa maneira se forem citados em duplicado, devido a conflitos sintáticos. Portanto, o uso da sintaxe de cast semelhante a uma função leva a inconsistências e provavelmente deve ser evitado.

Nota

A sintaxe semelhante a uma função, na verdade, é apenas uma chamada de função. Quando uma das duas sintaxes padrão de conversão de tempo de execução é usada para realizar uma conversão, ela internamente invoca uma função registrada para realizar a conversão. Por convenção, essas funções de conversão têm o mesmo nome que seu tipo de saída, e, portanto, a “sintaxe semelhante a uma função” não é nada mais do que uma invocação direta da função de conversão subjacente. Obviamente, isso não é algo que uma aplicação portátil deve depender. Para mais detalhes, consulte [CREATE CAST](sql-createcast.md).

##### 4.2.10. Expressões de colagem [#](#SQL-SYNTAX-COLLATE-EXPRS)

A cláusula `COLLATE` substitui a ordenação de uma expressão. Ela é anexada à expressão a que se aplica:

```
expr COLLATE collation
```

onde *`collation`* é um identificador possivelmente qualificado por esquema. A cláusula `COLLATE` vincula-se de forma mais apertada do que os operadores; parênteses podem ser usados quando necessário.

Se nenhuma ordenação for especificada explicitamente, o sistema de banco de dados deriva uma ordenação a partir das colunas envolvidas na expressão, ou ela é definida como a ordenação padrão do banco de dados se nenhuma coluna estiver envolvida na expressão.

Os dois usos comuns da cláusula `COLLATE` são a supressão da ordem de classificação em uma cláusula `ORDER BY`, por exemplo:

```
SELECT a, b, c FROM tbl WHERE ... ORDER BY a COLLATE "C";
```

e a supressão da ordenação de uma chamada de função ou operador que tenha resultados sensíveis ao idioma, por exemplo:

```
SELECT * FROM tbl WHERE a > 'foo' COLLATE "C";
```

Observe que, no último caso, a cláusula `COLLATE` é anexada a um argumento de entrada do operador que se deseja afetar. Não importa qual argumento do operador ou chamada de função a cláusula `COLLATE` esteja anexada, porque a ordenação que é aplicada pelo operador ou função é derivada considerando todos os argumentos, e uma cláusula explícita `COLLATE` substituirá as ordenações de todos os outros argumentos. (Anexar cláusulas `COLLATE` não correspondentes a mais de um argumento, no entanto, é um erro. Para mais detalhes, consulte [Seção 23.2](collation.md).]) Assim, isso dá o mesmo resultado que o exemplo anterior:

```
SELECT * FROM tbl WHERE a COLLATE "C" > 'foo';
```

Mas isso é um erro:

```
SELECT * FROM tbl WHERE (a > 'foo') COLLATE "C";
```

porque tenta aplicar uma ordenação ao resultado do operador `>`, que é do tipo de dados não ordenável `boolean`.

##### 4.2.11. Subconsultas escalares [#](#SQL-SYNTAX-SCALAR-SUBQUERIES)

Uma subconsulta escalar é uma consulta comum `SELECT` entre parênteses que retorna exatamente uma linha com uma coluna. (Veja [Capítulo 7](queries.md) para informações sobre como escrever consultas. A consulta `SELECT` é executada e o único valor retornado é usado na expressão de valor circundante. É um erro usar uma consulta que retorne mais de uma linha ou mais de uma coluna como uma subconsulta escalar. (Mas se, durante uma execução específica, a subconsulta não retornar nenhuma linha, não há erro; o resultado escalar é considerado nulo.) A subconsulta pode referenciar variáveis da consulta circundante, que atuará como constantes durante qualquer avaliação da subconsulta. Veja também [Seção 9.24](functions-subquery.md) para outras expressões que envolvem subconsultas.

Por exemplo, o seguinte encontra a população da maior cidade em cada estado:

```
SELECT name, (SELECT max(pop) FROM cities WHERE cities.state = states.name)
    FROM states;
```

##### 4.2.12. Construtores de matriz [#](#SQL-SYNTAX-ARRAY-CONSTRUCTORS)

Um construtor de matriz é uma expressão que constrói um valor de matriz usando valores para seus elementos membros. Um construtor de matriz simples consiste na palavra-chave `ARRAY`, um parêntese esquerdo `[`, uma lista de expressões (separadas por vírgulas) para os valores dos elementos da matriz e, finalmente, um parêntese direito `]`. Por exemplo:

```
SELECT ARRAY[1,2,3+4];
  array
---------
 {1,2,7}
(1 row)
```

Por padrão, o tipo do elemento da matriz é o tipo comum das expressões de membro, determinado usando as mesmas regras que para os construtos `UNION` ou `CASE` (consulte [Seção 10.5](typeconv-union-case.md)). Você pode ignorar isso explicitamente, lançando o construtor da matriz para o tipo desejado, por exemplo:

```sql
SELECT ARRAY[1,2,22.7]::integer[];
  array
----------
 {1,2,23}
(1 row)
```

Isso tem o mesmo efeito que lançar cada expressão no tipo de elemento da matriz individualmente. Para mais informações sobre conversão, consulte [Seção 4.2.9](sql-expressions.md#SQL-SYNTAX-TYPE-CASTS).

Os valores de matriz multidimensional podem ser construídos mediante a criação de construtores de matriz em camadas. Nas camadas internas, a palavra-chave `ARRAY` pode ser omitida. Por exemplo, estes produzem o mesmo resultado:

```sql
SELECT ARRAY[ARRAY[1,2], ARRAY[3,4]];
     array
---------------
 {{1,2},{3,4}}
(1 row)

SELECT ARRAY[[1,2],[3,4]];
     array
---------------
 {{1,2},{3,4}}
(1 row)
```

Como matrizes multidimensionais devem ser retangulares, os construtores internos no mesmo nível devem produzir submatrizes de dimensões idênticas. Qualquer cast aplicado ao construtor externo `ARRAY` se propaga automaticamente para todos os construtores internos.

Os elementos do construtor de matriz multidimensional podem ser qualquer coisa que produza uma matriz do tipo correto, não apenas um sub-`ARRAY`. Por exemplo:

```sql
CREATE TABLE arr(f1 int[], f2 int[]);

INSERT INTO arr VALUES (ARRAY[[1,2],[3,4]], ARRAY[[5,6],[7,8]]);

SELECT ARRAY[f1, f2, '{{9,10},{11,12}}'::int[]] FROM arr;
                     array
------------------------------------------------
 {{{1,2},{3,4}},{{5,6},{7,8}},{{9,10},{11,12}}}
(1 row)
```

Você pode construir um array vazio, mas, como é impossível ter um array sem tipo, você deve converter explicitamente seu array vazio para o tipo desejado. Por exemplo:

```sql
SELECT ARRAY[]::integer[];
 array
-------
 {}
(1 row)
```

É também possível construir um array a partir dos resultados de uma subconsulta. Nesta forma, o construtor de array é escrito com a palavra-chave `ARRAY` seguida de uma subconsulta entre parênteses (não entre chaves). Por exemplo:

```sql
SELECT ARRAY(SELECT oid FROM pg_proc WHERE proname LIKE 'bytea%');
                              array
------------------------------------------------------------------
 {2011,1954,1948,1952,1951,1244,1950,2005,1949,1953,2006,31,2412}
(1 row)

SELECT ARRAY(SELECT ARRAY[i, i*2] FROM generate_series(1,5) AS a(i));
              array
----------------------------------
 {{1,2},{2,4},{3,6},{4,8},{5,10}}
(1 row)
```

A subconsulta deve retornar uma única coluna. Se a coluna de saída da subconsulta for de um tipo não de matriz, a matriz resultante unidimensional terá um elemento para cada linha no resultado da subconsulta, com um tipo de elemento que corresponda ao da coluna de saída da subconsulta. Se a coluna de saída da subconsulta for de um tipo de matriz, o resultado será uma matriz do mesmo tipo, mas uma dimensão maior; nesse caso, todas as linhas da subconsulta devem produzir matrizes de dimensionalidade idêntica, caso contrário, o resultado não seria retangular.

Os subíndices de um valor de matriz construído com `ARRAY` sempre começam com um. Para mais informações sobre matrizes, consulte [Seção 8.15](arrays.md).

##### 4.2.13. Construtores de linhas [#](#SQL-SYNTAX-ROW-CONSTRUCTORS)

Um construtor de linha é uma expressão que constrói um valor de linha (também chamado de valor composto) usando valores para seus campos membros. Um construtor de linha consiste na palavra-chave `ROW`, um parêntese esquerdo, zero ou mais expressões (separadas por vírgulas) para os valores dos campos da linha e, finalmente, um parêntese direito. Por exemplo:

```sql
SELECT ROW(1,2.5,'this is a test');
```

A palavra-chave `ROW` é opcional quando há mais de uma expressão na lista.

Um construtor de linha pode incluir a sintaxe *`rowvalue`*`.*`, que será expandida para uma lista dos elementos do valor da linha, assim como ocorre quando a sintaxe `.*` é usada no nível superior de uma lista `SELECT` (ver [Seção 8.16.5](rowtypes.md#ROWTYPES-USAGE "8.16.5. Using Composite Types in Queries")). Por exemplo, se a tabela `t` tiver as colunas `f1` e `f2`, estas são as mesmas:

```sql
SELECT ROW(t.*, 42) FROM t;
SELECT ROW(t.f1, t.f2, 42) FROM t;
```

Nota

Antes do PostgreSQL 8.2, a sintaxe `.*` não era expandida em construtores de linha, de modo que escrever `ROW(t.*, 42)` criava uma linha de dois campos cujo primeiro campo era outro valor de linha. O novo comportamento geralmente é mais útil. Se você precisa do comportamento antigo de valores de linha aninhados, escreva o valor da linha interna sem `.*`, por exemplo `ROW(t, 42)`.

Por padrão, o valor criado por uma expressão `ROW` é de um tipo de registro anônimo. Se necessário, ele pode ser convertido para um tipo composto nomeado — seja o tipo de linha de uma tabela, ou um tipo composto criado com `CREATE TYPE AS`. Pode ser necessário um cast explícito para evitar ambiguidade. Por exemplo:

```sql
CREATE TABLE mytable(f1 int, f2 float, f3 text);

CREATE FUNCTION getf1(mytable) RETURNS int AS 'SELECT $1.f1' LANGUAGE SQL;

-- No cast needed since only one getf1() exists
SELECT getf1(ROW(1,2.5,'this is a test'));
 getf1
-------
     1
(1 row)

CREATE TYPE myrowtype AS (f1 int, f2 text, f3 numeric);

CREATE FUNCTION getf1(myrowtype) RETURNS int AS 'SELECT $1.f1' LANGUAGE SQL;

-- Now we need a cast to indicate which function to call:
SELECT getf1(ROW(1,2.5,'this is a test'));
ERROR:  function getf1(record) is not unique

SELECT getf1(ROW(1,2.5,'this is a test')::mytable);
 getf1
-------
     1
(1 row)

SELECT getf1(CAST(ROW(11,'this is a test',2.5) AS myrowtype));
 getf1
-------
    11
(1 row)
```

Os construtores de linha podem ser usados para construir valores compostos a serem armazenados em uma coluna de tabela de tipo composto, ou para serem passados para uma função que aceita um parâmetro composto. Além disso, é possível testar linhas usando os operadores de comparação padrão, conforme descrito em [Seção 9.2](functions-comparison.md), para comparar uma linha contra outra, conforme descrito em [Seção 9.25](functions-comparisons.md), e usá-los em conexão com subconsultas, conforme discutido em [Seção 9.24](functions-subquery.md).

##### 4.2.14. Regras de Avaliação de Expressão [#](#SYNTAX-EXPRESS-EVAL)

A ordem de avaliação das subexpressões não é definida. Em particular, as entradas de um operador ou função não são necessariamente avaliadas de esquerda para direita ou em qualquer outra ordem fixa.

Além disso, se o resultado de uma expressão pode ser determinado pela avaliação de apenas algumas de suas partes, então outras subexpressões podem não ser avaliadas em absoluto. Por exemplo, se alguém escrevesse:

```sql
SELECT true OR somefunc();
```

então `somefunc()` (provavelmente) não seria chamado de forma alguma. O mesmo aconteceria se alguém escrevesse:

```sql
SELECT somefunc() OR true;
```

Observe que isso não é o mesmo que o "curto-circuito" de operadores lógicos de esquerda para direita que se encontra em alguns idiomas de programação.

Como consequência, não é prudente usar funções com efeitos colaterais como parte de expressões complexas. É particularmente perigoso confiar em efeitos colaterais ou na ordem de avaliação nas cláusulas `WHERE` e `HAVING`, uma vez que essas cláusulas são amplamente reprojetadas como parte do desenvolvimento de um plano de execução. As expressões booleanas (combinações de `AND`/`OR`/`NOT` nessas cláusulas) podem ser reorganizadas de qualquer maneira permitida pelas leis da álgebra booleana.

Quando é essencial forçar a ordem de avaliação, pode ser utilizado um `CASE` (consulte a [Seção 9.18](functions-conditional.md)). Por exemplo, essa é uma maneira pouco confiável de tentar evitar a divisão por zero em uma cláusula `WHERE`:

```sql
SELECT ... WHERE x > 0 AND y/x > 1.5;
```

Mas isso é seguro:

```sql
SELECT ... WHERE CASE WHEN x > 0 THEN y/x > 1.5 ELSE false END;
```

Uma construção `CASE` usada dessa maneira derrotará as tentativas de otimização, portanto, deve ser feita apenas quando necessário. (Neste exemplo específico, seria melhor contornar o problema escrevendo `y > 1.5*x` em vez disso.)

`CASE` não é uma solução para todos os problemas, no entanto. Uma limitação da técnica ilustrada acima é que ela não previne a avaliação precoce de subexpressões constantes. Como descrito em [Seção 36.7](xfunc-volatility.md), funções e operadores marcados `IMMUTABLE` podem ser avaliados quando a consulta é planejada, e não quando é executada. Assim, por exemplo

```sql
SELECT CASE WHEN x > 0 THEN x ELSE 1/0 END FROM tab;
```

é provável que resulte em uma falha de divisão por zero, devido ao planejador tentar simplificar a subexpressão constante, mesmo que cada linha da tabela tenha `x > 0`, para que o braço `ELSE` nunca seja inserido no momento da execução.

Embora esse exemplo específico possa parecer bobo, casos relacionados que não envolvem óbvio constantes podem ocorrer em consultas executadas dentro de funções, uma vez que os valores dos argumentos de função e das variáveis locais podem ser inseridos em consultas como constantes para fins de planejamento. Dentro das funções PL/pgSQL, por exemplo, usar uma declaração `IF`-`THEN`-`ELSE` para proteger uma computação arriscada é muito mais seguro do que simplesmente aninhar em uma expressão `CASE`.

Outra limitação do mesmo tipo é que um `CASE` não pode impedir a avaliação de uma expressão agregada contida nele, porque as expressões agregadas são calculadas antes de outras expressões em uma lista `SELECT` ou cláusula `HAVING` serem consideradas. Por exemplo, a seguinte consulta pode causar um erro de divisão por zero, apesar de aparentemente ter protegido contra isso:

```sql
SELECT CASE WHEN min(employees) > 0
            THEN avg(expenses / employees)
       END
    FROM departments;
```

Os agregados `min()` e `avg()` são calculados simultaneamente sobre todas as linhas de entrada, portanto, se qualquer linha tiver `employees` igual a zero, o erro de divisão por zero ocorrerá antes de haver qualquer oportunidade de testar o resultado de `min()`. Em vez disso, use uma cláusula `WHERE` ou `FILTER` para impedir que as linhas de entrada problemáticas cheguem a uma função agregada em primeiro lugar.