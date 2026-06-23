## 7.2. Expressões de tabela [#](#QUERIES-TABLE-EXPRESSIONS)

* [7.2.1. A cláusula `FROM`](queries-table-expressions.md#QUERIES-FROM)
* [7.2.2. A cláusula `WHERE`](queries-table-expressions.md#QUERIES-WHERE)
* [7.2.3. As cláusulas `GROUP BY` e `HAVING`](queries-table-expressions.md#QUERIES-GROUP)
* [7.2.4. `GROUPING SETS`, `CUBE` e `ROLLUP`](queries-table-expressions.md#QUERIES-GROUPING-SETS)
* [7.2.5. Processamento de função de janela](queries-table-expressions.md#QUERIES-WINDOW)

Uma expressão de tabela calcula uma tabela. A expressão de tabela contém uma cláusula `FROM` que é opcionalmente seguida por cláusulas `WHERE`, `GROUP BY` e `HAVING`. Expressões triviais de tabela simplesmente se referem a uma tabela em disco, uma chamada tabela base, mas expressões mais complexas podem ser usadas para modificar ou combinar tabelas base de várias maneiras.

As cláusulas opcionais `WHERE`, `GROUP BY` e `HAVING` na expressão de tabela especificam um pipeline de transformações sucessivas realizadas na tabela derivada na cláusula `FROM`. Todas essas transformações produzem uma tabela virtual que fornece as linhas que são passadas para a lista de seleção para calcular as linhas de saída da consulta.

### 7.2.1. A Cláusula `FROM` [#](#QUERIES-FROM)

A cláusula `FROM`(sql-select.md#SQL-FROM "FROM Clause") deriva uma tabela a partir de uma ou mais outras tabelas, fornecidas em uma lista de referência de tabela separada por vírgula.

```
FROM table_reference [, table_reference [, ...]]
```

Uma referência de tabela pode ser o nome de uma tabela (possível com qualificação de esquema) ou uma tabela derivada, como uma subconsulta, um `JOIN` ou combinações complexas dessas. Se mais de uma referência de tabela estiver listada na cláusula `FROM`, as tabelas são cruzadas (ou seja, o produto cartesiano de suas linhas é formado; veja abaixo). O resultado da lista `FROM` é uma tabela virtual intermediária que pode, então, ser submetida a transformações pelas cláusulas `WHERE`, `GROUP BY` e `HAVING` e, finalmente, é o resultado da expressão geral da tabela.

Quando uma referência de tabela nomeia uma tabela que é a tabela principal de uma hierarquia de herança de tabela, a referência de tabela produz linhas não apenas dessa tabela, mas de todas as suas tabelas descendentes, a menos que a palavra-chave `ONLY` preceeda o nome da tabela. No entanto, a referência produz apenas as colunas que aparecem na tabela nomeada — quaisquer colunas adicionadas em sub-tabelas são ignoradas.

Em vez de escrever `ONLY` antes do nome da tabela, você pode escrever `*` após o nome da tabela para especificar explicitamente que as tabelas descendentes são incluídas. Não há uma razão real para usar essa sintaxe mais, porque a busca de tabelas descendentes é agora sempre o comportamento padrão. No entanto, é suportada para compatibilidade com versões mais antigas.

#### 7.2.1.1. Tabelas unidas [#](#QUERIES-JOIN)

Uma tabela unificada é uma tabela derivada de outras duas (reais ou derivadas) de acordo com as regras do tipo de junção específico. As junções internas, externas e cruzadas estão disponíveis. A sintaxe geral de uma tabela unificada é

```
T1 join_type T2 [ join_condition ]
```

As junções de todos os tipos podem ser encadeadas ou aninhadas: ou *`T1`* e *`T2`* ou ambos podem ser tabelas juncionadas. As chaves de parênteses podem ser usadas em torno das cláusulas de `JOIN` para controlar a ordem de junção. Na ausência de chaves de parênteses, as cláusulas de `JOIN` aninham de esquerda para direita.

**Tipos de Inscrição**

Join cruzado: ``` T1 CROSS JOIN T2
```

Para cada combinação possível de linhas de
*`T1`* e
*`T2`* (ou seja, um produto cartesiano),
a tabela unificada conterá uma
linha composta por todas as colunas de *`T1`*
seguidas por todas as colunas de *`T2`*. Se
as tabelas tiverem N e M linhas respectivamente, a tabela
unificada terá N * M linhas.

`FROM T1 CROSS JOIN
T2` é equivalente a
`FROM T1 INNER JOIN
T2 ON TRUE` (veja abaixo).
É também equivalente a
`FROM T1,
T2`.

Nota

Essa última equivalência não se aplica exatamente quando aparecem mais de duas tabelas, porque `JOIN` se liga mais fortemente do que vírgula. Por exemplo
`FROM T1 CROSS JOIN
T2 INNER JOIN T3
ON condition`
não é o mesmo que
`FROM T1,
T2 INNER JOIN T3
ON condition`
porque o *`condition`* pode
referenciar *`T1`* no primeiro caso, mas não
no segundo.

Conexões qualificadas: ```
T1 { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2 ON boolean_expression
T1 { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2 USING ( join column list )
T1 NATURAL { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2
```

As palavras `INNER` e `OUTER` são opcionais em todas as formas. `INNER` é o padrão; `LEFT`, `RIGHT` e `FULL` implicam uma junção externa.

A condição de junção é especificada na cláusula `ON` ou `USING`, ou implicitamente pela palavra `NATURAL`. A condição de junção determina quais linhas das duas tabelas de origem são consideradas para "combinar", conforme explicado em detalhes abaixo.

Os tipos possíveis de junção qualificada são:

`INNER JOIN` :   Para cada linha R1 de T1, a tabela unificada tem uma linha para cada linha de T2 que satisfaça a condição de junção com R1.

`LEFT OUTER JOIN` :   Primeiro, uma junção interna é realizada. Em seguida, para cada linha de T1 que não satisfaça a condição de junção com qualquer linha de T2, uma linha juncionada é adicionada com valores nulos nas colunas de T2. Assim, a tabela juncionada sempre tem pelo menos uma linha para cada linha de T1.

`RIGHT OUTER JOIN` :   Primeiro, uma junção interna é realizada. Em seguida, para cada linha de T2 que não satisfaça a condição de junção com qualquer linha de T1, uma linha juncionada é adicionada com valores nulos nas colunas de T1. Isso é o contrário de uma junção esquerda: a tabela de resultado sempre terá uma linha para cada linha de T2.

`FULL OUTER JOIN` :   Primeiro, uma junção interna é realizada. Em seguida, para cada linha de T1 que não satisfaça a condição de junção com qualquer linha de T2, uma linha juncionada é adicionada com valores nulos nas colunas de T2. Além disso, para cada linha de T2 que não satisfaça a condição de junção com qualquer linha de T1, uma linha juncionada com valores nulos nas colunas de T1 é adicionada.

A cláusula `ON` é o tipo mais geral de condição de junção: ela aceita uma expressão de valor booleano do mesmo tipo que é usada em uma cláusula `WHERE`. Um par de linhas de *`T1`* e *`T2`* se correspondem se a expressão `ON` for avaliada como verdadeira.

A cláusula `USING` é uma abreviação que permite aproveitar a situação específica em que ambos os lados da junção usam o mesmo nome para a(s) coluna(s) de junção. Ela recebe uma lista de colunas compartilhadas separadas por vírgula e forma uma condição de junção que inclui uma comparação de igualdade para cada uma delas. Por exemplo, a junção de *`T1`* e *`T2`* com `USING (a, b)` produz a condição de junção `ON T1.a = T2.a AND T1.b = T2.b`.

Além disso, a saída de `JOIN USING` suprime colunas redundantes: não há necessidade de imprimir ambas as colunas correspondentes, uma vez que elas devem ter valores iguais. Enquanto `JOIN ON` produz todas as colunas de *`T1`* seguidas por todas as colunas de *`T2`*, `JOIN USING` produz uma coluna de saída para cada um dos pares de colunas listados (na ordem listada), seguidas por quaisquer colunas restantes de *`T1`*, seguidas por quaisquer colunas restantes de *`T2`*.

Finalmente, `NATURAL` é uma forma abreviada de `USING`: ele forma uma lista `USING` composta por todos os nomes de coluna que aparecem em ambas as tabelas de entrada. Como com `USING`, essas colunas aparecem apenas uma vez na tabela de saída. Se não houver nomes de coluna comuns, `NATURAL JOIN` se comporta como `CROSS JOIN`.

Nota

`USING` é razoavelmente seguro em relação a alterações de coluna nas relações unidas, uma vez que apenas as colunas listadas são combinadas. `NATURAL` é consideravelmente mais arriscado, pois quaisquer alterações no esquema em qualquer uma das relações que causem a presença de um novo nome de coluna de correspondência farão com que a junção combine essa nova coluna também.

Para montar isso, vamos supor que temos as tabelas `t1`:

```
 num | name
-----+------
   1 | a
   2 | b
   3 | c
```

e `t2`:

```
 num | value
-----+-------
   1 | xxx
   3 | yyy
   5 | zzz
```

então obtemos os seguintes resultados para as várias junções:

```
=> SELECT * FROM t1 CROSS JOIN t2;
 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
   1 | a    |   3 | yyy
   1 | a    |   5 | zzz
   2 | b    |   1 | xxx
   2 | b    |   3 | yyy
   2 | b    |   5 | zzz
   3 | c    |   1 | xxx
   3 | c    |   3 | yyy
   3 | c    |   5 | zzz
(9 rows)

=> SELECT * FROM t1 INNER JOIN t2 ON t1.num = t2.num;
 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
   3 | c    |   3 | yyy
(2 rows)

=> SELECT * FROM t1 INNER JOIN t2 USING (num);
 num | name | value
-----+------+-------
   1 | a    | xxx
   3 | c    | yyy
(2 rows)

=> SELECT * FROM t1 NATURAL INNER JOIN t2;
 num | name | value
-----+------+-------
   1 | a    | xxx
   3 | c    | yyy
(2 rows)

=> SELECT * FROM t1 LEFT JOIN t2 ON t1.num = t2.num;
 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
   2 | b    |     |
   3 | c    |   3 | yyy
(3 rows)

=> SELECT * FROM t1 LEFT JOIN t2 USING (num);
 num | name | value
-----+------+-------
   1 | a    | xxx
   2 | b    |
   3 | c    | yyy
(3 rows)

=> SELECT * FROM t1 RIGHT JOIN t2 ON t1.num = t2.num;
 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
   3 | c    |   3 | yyy
     |      |   5 | zzz
(3 rows)

=> SELECT * FROM t1 FULL JOIN t2 ON t1.num = t2.num;
 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
   2 | b    |     |
   3 | c    |   3 | yyy
     |      |   5 | zzz
(4 rows)
```

A condição de junção especificada com `ON` também pode conter condições que não se relacionam diretamente com a junção. Isso pode ser útil para algumas consultas, mas precisa ser pensado cuidadosamente. Por exemplo:

```
=> SELECT * FROM t1 LEFT JOIN t2 ON t1.num = t2.num AND t2.value = 'xxx';
 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
   2 | b    |     |
   3 | c    |     |
(3 rows)
```

Observe que, ao colocar a restrição na cláusula `WHERE`, obtém-se um resultado diferente:

```
=> SELECT * FROM t1 LEFT JOIN t2 ON t1.num = t2.num WHERE t2.value = 'xxx';
 num | name | num | value
-----+------+-----+-------
   1 | a    |   1 | xxx
(1 row)
```

Isso ocorre porque uma restrição colocada na cláusula `ON` é processada *antes* do join, enquanto uma restrição colocada na cláusula `WHERE` é processada *depois* do join. Isso não importa com junções internas, mas é muito importante com junções externas.

#### 7.2.1.2. Símbolos de tabela e coluna [#](#QUERIES-TABLE-ALIASES)

Um nome temporário pode ser dado a tabelas e referências complexas de tabela para serem usadas em referências à tabela derivada no restante da consulta. Isso é chamado de *alias de tabela*.

Para criar um alias de tabela, escreva

```
FROM table_reference AS alias
```

ou

```
FROM table_reference alias
```

A palavra-chave `AS` é ruído opcional. *`alias`* pode ser qualquer identificador.

Uma aplicação típica de aliases de tabela é atribuir identificadores curtos a nomes de tabelas longos para manter as cláusulas de junção legíveis. Por exemplo:

```
SELECT * FROM some_very_long_table_name s JOIN another_fairly_long_name a ON s.id = a.num;
```

O alias se torna o novo nome da referência da tabela, na medida em que se refere à consulta atual — não é permitido referir-se à tabela pelo nome original em qualquer outra parte da consulta. Assim, isso não é válido:

```
SELECT * FROM my_table AS m WHERE my_table.a > 5;    -- wrong
```

Os aliases de tabela são principalmente para conveniência de notação, mas é necessário usá-los ao unir uma tabela a si mesma, por exemplo:

```
SELECT * FROM people AS mother JOIN people AS child ON mother.id = child.mother_id;
```

As parênteses são usadas para resolver ambiguidades. No exemplo a seguir, a primeira declaração atribui o alias `b` à segunda instância de `my_table`, mas a segunda declaração atribui o alias ao resultado da junção:

```
SELECT * FROM my_table AS a CROSS JOIN my_table AS b ...
SELECT * FROM (my_table AS a CROSS JOIN my_table) AS b ...
```

Outra forma de aliasing de tabela dá nomes temporários às colunas da tabela, bem como à própria tabela:

```
FROM table_reference [AS] alias ( column1 [, column2 [, ...]] )
```

Se forem especificados menos aliases de coluna do que as colunas que a tabela real possui, as colunas restantes não serão renomeadas. Essa sintaxe é especialmente útil para auto-join ou subconsultas.

Quando um alias é aplicado à saída de uma cláusula `JOIN`, o alias oculta o(s) nome(s) original(is) dentro do `JOIN`. Por exemplo:

```
SELECT a.* FROM my_table AS a JOIN your_table AS b ON ...
```

é válido SQL, mas:

```
SELECT a.* FROM (my_table AS a JOIN your_table AS b ON ...) AS c
```

não é válido; o alias da tabela `a` não é visível fora do alias `c`.

#### 7.2.1.3. Subconsultas [#](#QUERIES-SUBQUERIES)

As subconsultas que especificam uma tabela derivada devem ser fechadas entre parênteses. Elas podem receber um nome de alias de tabela e, opcionalmente, nomes de alias de coluna (como em [Seção 7.2.1.2](queries-table-expressions.md#QUERIES-TABLE-ALIASES)). Por exemplo:

```
FROM (SELECT * FROM table1) AS alias_name
```

Este exemplo é equivalente a `FROM table1 AS alias_name`. Casos mais interessantes, que não podem ser reduzidos a uma simples junção, surgem quando a subconsulta envolve agrupamento ou agregação.

Uma subconsulta também pode ser uma lista `VALUES`:

```
FROM (VALUES ('anne', 'smith'), ('bob', 'jones'), ('joe', 'blow'))
     AS names(first, last)
```

Novamente, um alias de tabela é opcional. Atribuir nomes de alias às colunas da lista `VALUES` é opcional, mas é uma boa prática. Para mais informações, consulte [Seção 7.7](queries-values.md).

De acordo com o padrão SQL, um nome de alias de tabela deve ser fornecido para uma subconsulta. O PostgreSQL permite que `AS` e o alias sejam omitidos, mas escrever um é uma boa prática em código SQL que pode ser exportado para outro sistema.

#### 7.2.1.4. Funções de tabela [#](#QUERIES-TABLEFUNCTIONS)

As funções de tabela são funções que produzem um conjunto de linhas, composto por tipos de dados básicos (tipos escalares) ou tipos de dados compostos (linhas de tabela). Elas são usadas como uma tabela, uma visão ou uma subconsulta na cláusula `FROM` de uma consulta. As colunas devolvidas por funções de tabela podem ser incluídas nas cláusulas `SELECT`, `JOIN` ou `WHERE` da mesma maneira que as colunas de uma tabela, uma visão ou uma subconsulta.

As funções da tabela também podem ser combinadas usando a sintaxe `ROWS FROM`, com os resultados retornados em colunas paralelas; o número de linhas de resultado, neste caso, é o maior resultado da função, com resultados menores preenchidos com valores nulos para corresponder.

```
function_call [WITH ORDINALITY] [[AS] table_alias [(column_alias [, ... ])]]
ROWS FROM( function_call [, ... ] ) [WITH ORDINALITY] [[AS] table_alias [(column_alias [, ... ])]]
```

Se a cláusula `WITH ORDINALITY` for especificada, uma coluna adicional do tipo `bigint` será adicionada às colunas do resultado da função. Esta coluna numera as linhas do conjunto de resultados da função, começando com o número 1. (Esta é uma generalização da sintaxe padrão do SQL para `UNNEST ... WITH ORDINALITY`.). Por padrão, a coluna ordinal é chamada de `ordinality`, mas um nome de coluna diferente pode ser atribuído a ela usando uma cláusula `AS`.

A função especial da tabela `UNNEST` pode ser chamada com qualquer número de parâmetros de matriz, e ela retorna um número correspondente de colunas, como se `UNNEST` ([Seção 9.19](functions-array.md "9.19. Array Functions and Operators")) tivesse sido chamada em cada parâmetro separadamente e combinada usando a construção `ROWS FROM`.

```
UNNEST( array_expression [, ... ] ) [WITH ORDINALITY] [[AS] table_alias [(column_alias [, ... ])]]
```

Se não for especificado um *`table_alias`*, o nome da função é usado como nome da tabela; no caso de um `ROWS FROM()`, o nome da primeira função é usado.

Se não forem fornecidos aliases de coluna, para uma função que retorna um tipo de dados de base, o nome da coluna também é o mesmo que o nome da função. Para uma função que retorna um tipo composto, as colunas de resultado recebem os nomes dos atributos individuais do tipo.

Alguns exemplos:

```
CREATE TABLE foo (fooid int, foosubid int, fooname text);

CREATE FUNCTION getfoo(int) RETURNS SETOF foo AS $$
    SELECT * FROM foo WHERE fooid = $1;
$$ LANGUAGE SQL;

SELECT * FROM getfoo(1) AS t1;

SELECT * FROM foo
    WHERE foosubid IN (
                        SELECT foosubid
                        FROM getfoo(foo.fooid) z
                        WHERE z.fooid = foo.fooid
                      );

CREATE VIEW vw_getfoo AS SELECT * FROM getfoo(1);

SELECT * FROM vw_getfoo;
```

Em alguns casos, é útil definir funções de tabela que possam retornar diferentes conjuntos de colunas dependendo de como são invocadas. Para suportar isso, a função de tabela pode ser declarada como retornando o pseudo-tipo `record` sem parâmetros `OUT`. Quando tal função é usada em uma consulta, a estrutura de linha esperada deve ser especificada na própria consulta, para que o sistema saiba como analisar e planejar a consulta. Essa sintaxe parece assim:

```
function_call [AS] alias (column_definition [, ... ])
function_call AS [alias] (column_definition [, ... ])
ROWS FROM( ... function_call AS (column_definition [, ... ]) [, ... ] )
```

Quando não se utiliza a sintaxe `ROWS FROM()`, a lista *`column_definition`* substitui a lista de aliases de coluna que, de outra forma, poderia ser anexada ao item `FROM`; os nomes nas definições de coluna servem como aliases de coluna. Quando se utiliza a sintaxe `ROWS FROM()`, uma lista *`column_definition`* pode ser anexada a cada função membro separadamente; ou se há apenas uma função membro e nenhuma cláusula `WITH ORDINALITY`, uma lista *`column_definition`* pode ser escrita no lugar de uma lista de aliases de coluna após `ROWS FROM()`.

Considere este exemplo:

```
SELECT *
    FROM dblink('dbname=mydb', 'SELECT proname, prosrc FROM pg_proc')
      AS t1(proname name, prosrc text)
    WHERE proname LIKE 'bytea%';
```

A função [dblink](contrib-dblink-function.md) (parte do módulo [dblink](dblink.md)) executa uma consulta remota. Ela é declarada para retornar `record` porque pode ser usada para qualquer tipo de consulta. O conjunto de colunas reais deve ser especificado na consulta de chamada para que o analisador saiba, por exemplo, para o que `*` deve ser expandido.

Este exemplo usa `ROWS FROM`:

```
SELECT *
FROM ROWS FROM
    (
        json_to_recordset('[{"a":40,"b":"foo"},{"a":"100","b":"bar"}]')
            AS (a INTEGER, b TEXT),
        generate_series(1, 3)
    ) AS x (p, q, s)
ORDER BY p;

  p  |  q  | s
-----+-----+---
  40 | foo | 1
 100 | bar | 2
     |     | 3
```

Ele une duas funções em um único alvo `FROM`. `json_to_recordset()` é instruído a retornar duas colunas, a primeira `integer` e a segunda `text`. O resultado de `generate_series()` é usado diretamente. A cláusula `ORDER BY` ordena os valores das colunas como inteiros.

#### 7.2.1.5. `LATERAL` Subconsultas [#](#QUERIES-LATERAL)

As subconsultas que aparecem em `FROM` podem ser precedidas pela palavra-chave `LATERAL`. Isso permite que elas refiram-se a colunas fornecidas por itens anteriores em `FROM`. (Sem `LATERAL`, cada subconsulta é avaliada de forma independente e, portanto, não pode fazer referência cruzada a qualquer outro item em `FROM`.)

As funções de tabela que aparecem em `FROM` também podem ser precedidas pela palavra-chave `LATERAL`, mas para funções a palavra-chave é opcional; os argumentos da função podem conter referências a colunas fornecidas por itens anteriores em `FROM` em qualquer caso.

Um item `LATERAL` pode aparecer no nível superior na lista `FROM`, ou dentro de uma árvore `JOIN`. Neste último caso, ele também pode se referir a quaisquer itens que estão do lado esquerdo de um `JOIN` que ele esteja do lado direito.

Quando um item `FROM` contém referências cruzadas `LATERAL`, a avaliação é realizada da seguinte forma: para cada linha do item `FROM` que fornece a(s) coluna(s) referenciada(s), ou conjunto de linhas de vários itens `FROM` que fornecem as colunas, o item `LATERAL` é avaliado usando os valores das colunas daquela linha ou conjunto de linhas. As linhas resultantes são unidas, como de costume, com as linhas de que foram calculadas. Isso é repetido para cada linha ou conjunto de linhas da(s) tabela(s) fonte da coluna.

Um exemplo trivial de `LATERAL` é

```
SELECT * FROM foo, LATERAL (SELECT * FROM bar WHERE bar.id = foo.bar_id) ss;
```

Isso não é especialmente útil, pois tem exatamente o mesmo resultado que o mais convencional

```
SELECT * FROM foo, bar WHERE bar.id = foo.bar_id;
```

`LATERAL` é principalmente útil quando a coluna cruzada é necessária para calcular as(s) linha(s) a serem unidas. Uma aplicação comum é fornecer um valor de argumento para uma função que retorna um conjunto. Por exemplo, supondo que `vertices(polygon)` retorne o conjunto de vértices de um polígono, poderíamos identificar vértices próximos uns dos outros de polígonos armazenados em uma tabela com:

```
SELECT p1.id, p2.id, v1, v2
FROM polygons p1, polygons p2,
     LATERAL vertices(p1.poly) v1,
     LATERAL vertices(p2.poly) v2
WHERE (v1 <-> v2) < 10 AND p1.id != p2.id;
```

Essa consulta também poderia ser escrita

```
SELECT p1.id, p2.id, v1, v2
FROM polygons p1 CROSS JOIN LATERAL vertices(p1.poly) v1,
     polygons p2 CROSS JOIN LATERAL vertices(p2.poly) v2
WHERE (v1 <-> v2) < 10 AND p1.id != p2.id;
```

ou em várias outras formulações equivalentes. (Como já mencionado, a palavra-chave `LATERAL` não é necessária neste exemplo, mas a usamos por questão de clareza.)

É frequentemente especialmente útil `LEFT JOIN` para uma subconsulta `LATERAL`, de modo que as linhas de origem apareçam no resultado mesmo que a subconsulta `LATERAL` não produza nenhuma linha para elas. Por exemplo, se `get_product_names()` retorna os nomes dos produtos fabricados por um fabricante, mas alguns fabricantes em nossa tabela atualmente não fabricam nenhum produto, podemos descobrir quais são esses:

```
SELECT m.name
FROM manufacturers m LEFT JOIN LATERAL get_product_names(m.id) pname ON true
WHERE pname IS NULL;
```

### 7.2.2. A cláusula `WHERE` [#](#QUERIES-WHERE)

A sintaxe da cláusula `WHERE`(sql-select.md#SQL-WHERE "WHERE Clause") é

```
WHERE search_condition
```

onde *`search_condition`* é qualquer expressão de valor (ver [Seção 4.2][(sql-expressions.md "4.2. Value Expressions")) que retorna um valor do tipo `boolean`.

Após o processamento da cláusula `FROM` ser concluído, cada linha da tabela virtual derivada é verificada em relação à condição de busca. Se o resultado da condição for verdadeiro, a linha é mantida na tabela de saída; caso contrário (ou seja, se o resultado for falso ou nulo), ela é descartada. A condição de busca geralmente faz referência a pelo menos uma coluna da tabela gerada na cláusula `FROM`; isso não é necessário, mas, caso contrário, a cláusula `WHERE` será bastante inútil.

Nota

A condição de junção de uma junção interna pode ser escrita na cláusula `WHERE` ou na cláusula `JOIN`. Por exemplo, essas expressões de tabela são equivalentes:

```
FROM a, b WHERE a.id = b.id AND b.val > 5
```

e:

```
FROM a INNER JOIN b ON (a.id = b.id) WHERE b.val > 5
```

ou talvez até:

```
FROM a NATURAL JOIN b WHERE b.val > 5
```

Qual desses você usa é principalmente uma questão de estilo. A sintaxe `JOIN` na cláusula `FROM` provavelmente não é tão portátil para outros sistemas de gerenciamento de banco de dados SQL, embora esteja no padrão SQL. Para junções externas, não há escolha: elas devem ser feitas na cláusula `FROM`. A cláusula `ON` ou `USING` de uma junção externa *não* é equivalente a uma condição `WHERE`, porque resulta na adição de linhas (para linhas de entrada não correspondentes) e na remoção de linhas no resultado final.

Aqui estão alguns exemplos de cláusulas `WHERE`:

```
SELECT ... FROM fdt WHERE c1 > 5

SELECT ... FROM fdt WHERE c1 IN (1, 2, 3)

SELECT ... FROM fdt WHERE c1 IN (SELECT c1 FROM t2)

SELECT ... FROM fdt WHERE c1 IN (SELECT c3 FROM t2 WHERE c2 = fdt.c1 + 10)

SELECT ... FROM fdt WHERE c1 BETWEEN (SELECT c3 FROM t2 WHERE c2 = fdt.c1 + 10) AND 100

SELECT ... FROM fdt WHERE EXISTS (SELECT c1 FROM t2 WHERE c2 > fdt.c1)
```

`fdt` é a tabela derivada na cláusula `FROM`. As linhas que não atendem à condição de busca da cláusula `WHERE` são eliminadas de `fdt`. Observe o uso de subconsultas escalares como expressões de valor. Assim como qualquer outra consulta, as subconsultas podem empregar expressões complexas de tabela. Observe também como `fdt` é referenciado nas subconsultas. Qualificar `c1` como `fdt.c1` é necessário apenas se `c1` também é o nome de uma coluna na tabela de entrada derivada da subconsulta. Mas qualificar o nome da coluna adiciona clareza mesmo quando não é necessário. Este exemplo mostra como o escopo de nomeação de coluna de uma consulta externa se estende para suas consultas internas.

### 7.2.3. As cláusulas `GROUP BY` e `HAVING` [#](#QUERIES-GROUP)

Após passar pelo filtro `WHERE`, a tabela de entrada derivada pode ser sujeita a agrupamento, usando a cláusula `GROUP BY`, e eliminação de linhas de grupo usando a cláusula `HAVING`.

```
SELECT select_list
    FROM ...
    [WHERE ...]
    GROUP BY grouping_column_reference [, grouping_column_reference]...
```

A cláusula `GROUP BY`(sql-select.md#SQL-GROUPBY "GROUP BY Clause") é usada para agrupar as linhas de uma tabela que possuem os mesmos valores em todas as colunas listadas. A ordem em que as colunas são listadas não importa. O efeito é combinar cada conjunto de linhas com valores comuns em uma única linha de grupo que representa todas as linhas do grupo. Isso é feito para eliminar a redundância na saída e/ou calcular agregados que se aplicam a esses grupos. Por exemplo:

```
=> SELECT * FROM test1;
 x | y
---+---
 a | 3
 c | 2
 b | 5
 a | 1
(4 rows)

=> SELECT x FROM test1 GROUP BY x;
 x
---
 a
 b
 c
(3 rows)
```

Na segunda consulta, não poderíamos ter escrito `SELECT * FROM test1 GROUP BY x`, porque não há um único valor para a coluna `y` que possa ser associado a cada grupo. As colunas agrupadas podem ser referenciadas na lista de seleção, pois elas têm um único valor em cada grupo.

Em geral, se uma tabela for agrupada, as colunas que não estão listadas em `GROUP BY` não podem ser referenciadas, exceto em expressões agregadas. Um exemplo com expressões agregadas é:

```
=> SELECT x, sum(y) FROM test1 GROUP BY x;
 x | sum
---+-----
 a |   4
 b |   5
 c |   2
(3 rows)
```

Aqui `sum` é uma função agregada que calcula um único valor sobre o grupo inteiro. Mais informações sobre as funções agregadas disponíveis podem ser encontradas em [Seção 9.21](functions-aggregate.md).

### DICA

O agrupamento sem expressões agregadas calcula efetivamente o conjunto de valores distintos em uma coluna. Isso também pode ser alcançado usando a cláusula `DISTINCT` (consulte [Seção 7.3.3](queries-select-lists.md#QUERIES-DISTINCT)).

Aqui está outro exemplo: calcula as vendas totais para cada produto (em vez das vendas totais de todos os produtos):

```
SELECT product_id, p.name, (sum(s.units) * p.price) AS sales
    FROM products p LEFT JOIN sales s USING (product_id)
    GROUP BY product_id, p.name, p.price;
```

Neste exemplo, as colunas `product_id`, `p.name` e `p.price` devem estar na cláusula `GROUP BY`, pois são referenciadas na lista de seleção da consulta (mas veja abaixo). A coluna `s.units` não precisa estar na lista `GROUP BY`, pois é usada apenas em uma expressão agregada (`sum(...)`), que representa as vendas de um produto. Para cada produto, a consulta retorna uma linha resumida sobre todas as vendas do produto.

Se a tabela de produtos estiver configurada de forma que, por exemplo, `product_id` seja a chave primária, então seria suficiente agrupar por `product_id` no exemplo acima, uma vez que o nome e o preço seriam *funcionalmente dependentes* do ID do produto, e, portanto, não haveria ambiguidade sobre qual nome e valor de preço retornar para cada grupo de ID de produto.

Em SQL estrito, `GROUP BY` pode agrupar apenas por colunas da tabela de origem, mas o PostgreSQL estende isso para permitir que `GROUP BY` também agrupe por colunas na lista de seleção. É permitido agrupar por expressões de valor em vez de nomes simples de colunas.

Se uma tabela tiver sido agrupada usando `GROUP BY`, mas apenas certos grupos interessam, a cláusula `HAVING` pode ser usada, de forma semelhante a uma cláusula `WHERE`, para eliminar grupos do resultado. A sintaxe é:

```
SELECT select_list FROM ... [WHERE ...] GROUP BY ... HAVING boolean_expression
```

As expressões na cláusula `HAVING` podem se referir tanto a expressões agrupadas quanto a expressões não agrupadas (que necessariamente envolvem uma função agregada).

Exemplo:

```
=> SELECT x, sum(y) FROM test1 GROUP BY x HAVING sum(y) > 3;
 x | sum
---+-----
 a |   4
 b |   5
(2 rows)

=> SELECT x, sum(y) FROM test1 GROUP BY x HAVING x < 'c';
 x | sum
---+-----
 a |   4
 b |   5
(2 rows)
```

Mais uma vez, um exemplo mais realista:

```
SELECT product_id, p.name, (sum(s.units) * (p.price - p.cost)) AS profit
    FROM products p LEFT JOIN sales s USING (product_id)
    WHERE s.date > CURRENT_DATE - INTERVAL '4 weeks'
    GROUP BY product_id, p.name, p.price, p.cost
    HAVING sum(p.price * s.units) > 5000;
```

No exemplo acima, a cláusula `WHERE` está selecionando linhas por uma coluna que não está agrupada (a expressão é verdadeira apenas para vendas nas últimas quatro semanas), enquanto a cláusula `HAVING` restringe a saída aos grupos com vendas totais brutas acima de

Se uma consulta contiver chamadas a funções agregadas, mas nenhuma cláusula `GROUP BY`, o agrupamento ainda ocorre: o resultado é uma única linha de grupo (ou talvez nenhuma linha, se a única linha for então eliminada por `HAVING`). O mesmo é verdadeiro se contiver uma cláusula `HAVING`, mesmo sem quaisquer chamadas a funções agregadas ou cláusula `GROUP BY`.

### 7.2.4. `GROUPING SETS`, `CUBE` e `ROLLUP` [#](#QUERIES-GROUPING-SETS)

Operações de agrupamento mais complexas do que as descritas acima são possíveis usando o conceito de *conjuntos de agrupamento*. Os dados selecionados pelas cláusulas `FROM` e `WHERE` são agrupados separadamente por cada conjunto de agrupamento especificado, agregados calculados para cada grupo, da mesma forma que para as cláusulas simples `GROUP BY`, e os resultados são então retornados. Por exemplo:

```
=> SELECT * FROM items_sold;
 brand | size | sales
-------+------+-------
 Foo   | L    |  10
 Foo   | M    |  20
 Bar   | M    |  15
 Bar   | L    |  5
(4 rows)

=> SELECT brand, size, sum(sales) FROM items_sold GROUP BY GROUPING SETS ((brand), (size), ());
 brand | size | sum
-------+------+-----
 Foo   |      |  30
 Bar   |      |  20
       | L    |  15
       | M    |  35
       |      |  50
(5 rows)
```

Cada sublista de `GROUPING SETS` pode especificar zero ou mais colunas ou expressões e é interpretada da mesma maneira como se estivesse diretamente na cláusula `GROUP BY`. Um conjunto de agrupamento vazio significa que todas as linhas são agregadas a um único grupo (que é exibido mesmo se não houver linhas de entrada), conforme descrito acima para o caso de funções agregadas sem cláusula `GROUP BY`.

As referências às colunas ou expressões de agrupamento são substituídas por valores nulos nas linhas de resultado para conjuntos de agrupamento nos quais essas colunas não aparecem. Para distinguir qual agrupamento uma determinada linha de saída resultou, consulte [Tabela 9.66](functions-aggregate.md#FUNCTIONS-GROUPING-TABLE).

Uma notação abreviada é fornecida para especificar dois tipos comuns de conjunto de agrupamento. Uma cláusula na forma

```
ROLLUP ( e1, e2, e3, ... )
```

representa a lista dada de expressões e todos os prefixos da lista, incluindo a lista vazia; assim, é equivalente a

```
GROUPING SETS (
    ( e1, e2, e3, ... ),
    ...
    ( e1, e2 ),
    ( e1 ),
    ( )
)
```

Isso é comumente usado para análise de dados hierárquicos; por exemplo, salário total por departamento, divisão e total em toda a empresa.

Uma cláusula na forma

```
CUBE ( e1, e2, ... )
```

representa a lista dada e todos os seus subconjuntos possíveis (ou seja, o conjunto de potência). Assim

```
CUBE ( a, b, c )
```

é equivalente a

```
GROUPING SETS (
    ( a, b, c ),
    ( a, b    ),
    ( a,    c ),
    ( a       ),
    (    b, c ),
    (    b    ),
    (       c ),
    (         )
)
```

Os elementos individuais de uma cláusula `CUBE` ou `ROLLUP` podem ser expressões individuais ou sublistas de elementos entre parênteses. Neste último caso, as sublistas são tratadas como unidades únicas para os fins de geração dos conjuntos de agrupamento individual. Por exemplo:

```
CUBE ( (a, b), (c, d) )
```

é equivalente a

```
GROUPING SETS (
    ( a, b, c, d ),
    ( a, b       ),
    (       c, d ),
    (            )
)
```

e

```
ROLLUP ( a, (b, c), d )
```

é equivalente a

```
GROUPING SETS (
    ( a, b, c, d ),
    ( a, b, c    ),
    ( a          ),
    (            )
)
```

Os construtos `CUBE` e `ROLLUP` podem ser usados diretamente na cláusula `GROUP BY`, ou aninhados dentro de uma cláusula `GROUPING SETS`. Se uma cláusula `GROUPING SETS` for aninhada em outra, o efeito é o mesmo como se todos os elementos da cláusula interna tivessem sido escritos diretamente na cláusula externa.

Se vários itens de agrupamento forem especificados em uma única cláusula `GROUP BY`, a lista final dos conjuntos de agrupamento é o produto cartesiano dos itens individuais. Por exemplo:

```
GROUP BY a, CUBE (b, c), GROUPING SETS ((d), (e))
```

é equivalente a

```
GROUP BY GROUPING SETS (
    (a, b, c, d), (a, b, c, e),
    (a, b, d),    (a, b, e),
    (a, c, d),    (a, c, e),
    (a, d),       (a, e)
)
```

Ao especificar vários itens agrupados juntos, o conjunto final de conjuntos de agrupamento pode conter duplicatas. Por exemplo:

```
GROUP BY ROLLUP (a, b), ROLLUP (a, c)
```

é equivalente a

```
GROUP BY GROUPING SETS (
    (a, b, c),
    (a, b),
    (a, b),
    (a, c),
    (a),
    (a),
    (a, c),
    (a),
    ()
)
```

Se esses duplicados forem indesejados, eles podem ser removidos usando a cláusula `DISTINCT` diretamente no `GROUP BY`. Portanto:

```
GROUP BY DISTINCT ROLLUP (a, b), ROLLUP (a, c)
```

é equivalente a

```
GROUP BY GROUPING SETS (
    (a, b, c),
    (a, b),
    (a, c),
    (a),
    ()
)
```

Isso não é o mesmo que usar `SELECT DISTINCT`, porque as linhas de saída ainda podem conter duplicatas. Se alguma das colunas não agrupadas contiver NULL, ela será indistinguível do NULL usado quando essa mesma coluna é agrupada.

Nota

O construtor `(a, b)` é normalmente reconhecido em expressões como um [construtor de linha](sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS "4.2.13. Row Constructors"). Dentro da cláusula `GROUP BY`, isso não se aplica nos níveis superiores das expressões, e `(a, b)` é analisado como uma lista de expressões, conforme descrito acima. Se, por algum motivo, você *precisa* de um construtor de linha em uma expressão de agrupamento, use `ROW(a, b)`.

### 7.2.5. Processamento de função de janela [#](#QUERIES-WINDOW)

Se a consulta contiver quaisquer funções de janela (consulte [Seção 3.5](tutorial-window.md), [Seção 9.22](functions-window.md) e [Seção 4.2.8](sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS)), essas funções são avaliadas após qualquer agrupamento, agregação e filtragem de `HAVING` ser realizada. Ou seja, se a consulta usa quaisquer agregados, `GROUP BY` ou `HAVING`, então as linhas vistas pelas funções de janela são as linhas de grupo em vez das linhas originais da tabela de `FROM`/`WHERE`.

Quando várias funções de janela são usadas, todas as funções de janela que possuem cláusulas equivalentes `PARTITION BY` e `ORDER BY` em suas definições de janela são garantidas para ver a mesma ordem das linhas de entrada, mesmo que o `ORDER BY` não determine de forma única a ordem. No entanto, não há garantias sobre a avaliação de funções que têm especificações diferentes `PARTITION BY` ou `ORDER BY`. (Nesses casos, geralmente é necessário um passo de ordenação entre as passagens das avaliações de funções de janela, e a ordenação não é garantida para preservar a ordem das linhas que seu `ORDER BY` vê como equivalentes.)

Atualmente, as funções de janela sempre exigem dados pré-ordenados, e, portanto, a saída da consulta será ordenada de acordo com uma das cláusulas `PARTITION BY`/`ORDER BY` das funções de janela. No entanto, não é recomendável confiar nisso. Use uma cláusula explícita de nível superior `ORDER BY` se você quiser ter certeza de que os resultados estão ordenados de uma maneira específica.