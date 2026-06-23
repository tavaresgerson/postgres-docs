## SELECIONE

SELECT, TABLE, WITH — recuperar linhas de uma tabela ou visual

## Sinopse

```
[ WITH [ RECURSIVE ] with_query [, ...] ]
SELECT [ ALL | DISTINCT [ ON ( expression [, ...] ) ] ]
    [ { * | expression [ [ AS ] output_name ] } [, ...] ]
    [ FROM from_item [, ...] ]
    [ WHERE condition ]
    [ GROUP BY [ ALL | DISTINCT ] grouping_element [, ...] ]
    [ HAVING condition ]
    [ WINDOW window_name AS ( window_definition ) [, ...] ]
    [ { UNION | INTERSECT | EXCEPT } [ ALL | DISTINCT ] select ]
    [ ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS { FIRST | LAST } ] [, ...] ]
    [ LIMIT { count | ALL } ]
    [ OFFSET start [ ROW | ROWS ] ]
    [ FETCH { FIRST | NEXT } [ count ] { ROW | ROWS } { ONLY | WITH TIES } ]
    [ FOR { UPDATE | NO KEY UPDATE | SHARE | KEY SHARE } [ OF from_reference [, ...] ] [ NOWAIT | SKIP LOCKED ] [...] ]

where from_item can be one of:

    [ ONLY ] table_name [ * ] [ [ AS ] alias [ ( column_alias [, ...] ) ] ]
                [ TABLESAMPLE sampling_method ( argument [, ...] ) [ REPEATABLE ( seed ) ] ]
    [ LATERAL ] ( select ) [ [ AS ] alias [ ( column_alias [, ...] ) ] ]
    with_query_name [ [ AS ] alias [ ( column_alias [, ...] ) ] ]
    [ LATERAL ] function_name ( [ argument [, ...] ] )
                [ WITH ORDINALITY ] [ [ AS ] alias [ ( column_alias [, ...] ) ] ]
    [ LATERAL ] function_name ( [ argument [, ...] ] ) [ AS ] alias ( column_definition [, ...] )
    [ LATERAL ] function_name ( [ argument [, ...] ] ) AS ( column_definition [, ...] )
    [ LATERAL ] ROWS FROM( function_name ( [ argument [, ...] ] ) [ AS ( column_definition [, ...] ) ] [, ...] )
                [ WITH ORDINALITY ] [ [ AS ] alias [ ( column_alias [, ...] ) ] ]
    from_item join_type from_item { ON join_condition | USING ( join_column [, ...] ) [ AS join_using_alias ] }
    from_item NATURAL join_type from_item
    from_item CROSS JOIN from_item

and grouping_element can be one of:

    ( )
    expression
    ( expression [, ...] )
    ROLLUP ( { expression | ( expression [, ...] ) } [, ...] )
    CUBE ( { expression | ( expression [, ...] ) } [, ...] )
    GROUPING SETS ( grouping_element [, ...] )

and with_query is:

    with_query_name [ ( column_name [, ...] ) ] AS [ [ NOT ] MATERIALIZED ] ( select | values | insert | update | delete | merge )
        [ SEARCH { BREADTH | DEPTH } FIRST BY column_name [, ...] SET search_seq_col_name ]
        [ CYCLE column_name [, ...] SET cycle_mark_col_name [ TO cycle_mark_value DEFAULT cycle_mark_default ] USING cycle_path_col_name ]

TABLE [ ONLY ] table_name [ * ]
```

## Descrição

`SELECT` recupera linhas de zero ou mais tabelas. O processamento geral de `SELECT` é o seguinte:

1. Todas as consultas na lista `WITH` são calculadas. Essas efetivamente servem como tabelas temporárias que podem ser referenciadas na lista `FROM`. Uma consulta `WITH` que é referenciada mais de uma vez em `FROM` é calculada apenas uma vez, a menos que seja especificado de outra forma com `NOT MATERIALIZED`. (Veja [Cláusula WITH](sql-select.md#SQL-WITH "WITH Clause") abaixo.)
2. Todos os elementos na lista `FROM` são calculados. (Cada elemento na lista `FROM` é uma tabela real ou virtual.) Se mais de um elemento é especificado na lista `FROM`, eles são cruzados juntos. (Veja [Cláusula FROM](sql-select.md#SQL-FROM "FROM Clause") abaixo.)
3. Se a cláusula `WHERE` for especificada, todas as linhas que não satisfazem a condição são eliminadas do resultado. (Veja [Cláusula WHERE](sql-select.md#SQL-WHERE "WHERE Clause") abaixo.)
4. Se a cláusula `GROUP BY` for especificada, ou se houver chamadas de função agregada, o resultado é combinado em grupos de linhas que correspondem a um ou mais valores, e os resultados das funções agregadas são calculados. Se a cláusula `HAVING` estiver presente, ela elimina grupos que não satisfazem a condição dada. (Veja [Cláusula GROUP BY](sql-select.md#SQL-GROUPBY "GROUP BY Clause") e [HAVING Clause](sql-select.md#SQL-HAVING "HAVING Clause") abaixo.) Embora as colunas de saída da consulta sejam nominalmente calculadas no próximo passo, elas também podem ser referenciadas (pelo nome ou número ordinal) na cláusula `GROUP BY`.
5. As linhas de saída reais são calculadas usando as expressões de saída `SELECT` para cada linha ou grupo de linhas selecionado. (Veja [Lista SELECT](sql-select.md#SQL-SELECT-LIST "SELECT List") abaixo.)
6. `SELECT DISTINCT` elimina linhas duplicadas do resultado. `SELECT DISTINCT ON` elimina linhas que correspondem a todas as expressões especificadas. `SELECT ALL` (o padrão) retornará todas as linhas candidatas, incluindo duplicados. (Veja [Cláusula DISTINCT](sql-select.md#SQL-DISTINCT "DISTINCT Clause") abaixo.)
7. Usando os operadores `UNION`, `INTERSECT`, e `EXCEPT`, a saída de mais de uma declaração `SELECT` pode ser combinada para formar um único conjunto de resultados. O operador `UNION` retorna todas as linhas que estão em uma ou ambas as conjuntos de resultados. O operador `INTERSECT` retorna todas as linhas que estão estritamente em ambos os conjuntos de resultados. O operador `EXCEPT` retorna as linhas que estão no primeiro conjunto de resultados, mas não no segundo. Em todos os três casos, as linhas duplicadas são eliminadas, a menos que `ALL` seja especificado. A palavra de ruído `DISTINCT` pode ser adicionada para especificar explicitamente a eliminação de linhas duplicadas. Note que `DISTINCT` é o comportamento padrão aqui, mesmo que `ALL` seja o comportamento padrão para `SELECT` em si. (Veja [Cláusula UNION](sql-select.md#SQL-UNION "UNION Clause"), [Cláusula INTERSECT](sql-select.md#SQL-INTERSECT "INTERSECT Clause"), e [Cláusula EXCEPT](sql-select.md#SQL-EXCEPT "EXCEPT Clause") abaixo.)
8. Se a cláusula `ORDER BY` for especificada, as linhas retornadas são ordenadas na ordem especificada. Se `ORDER BY` não for dado, as linhas são retornadas na ordem em que o sistema encontra mais rápido para produzir. (Veja [Cláusula ORDER BY](sql-select.md#SQL-ORDERBY "ORDER BY Clause") abaixo.)
9. Se a cláusula `LIMIT` (ou `FETCH FIRST`) ou `OFFSET` for especificada, a declaração `SELECT` retorna apenas um subconjunto das linhas de resultado. (Veja [Cláusula LIMIT](sql-select.md#SQL-LIMIT "LIMIT Clause") abaixo.)
10. Se `FOR UPDATE`, `FOR NO KEY UPDATE`, `FOR SHARE` ou `FOR KEY SHARE` for especificado, a declaração `SELECT` bloqueia as linhas selecionadas contra atualizações concorrentes. (Veja [A Cláusula de Bloqueio](sql-select.md#SQL-FOR-UPDATE-SHARE "The Locking Clause") abaixo.)

Você deve ter o privilégio `SELECT` em cada coluna usada em um comando `SELECT`. O uso de `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` ou `FOR KEY SHARE` também requer privilégio `UPDATE` (pelo menos em uma coluna de cada tabela selecionada).

## Parâmetros

### `WITH` Cláusula

A cláusula `WITH` permite especificar uma ou mais subconsultas que podem ser referenciadas pelo nome na consulta principal. As subconsultas atuam efetivamente como tabelas ou visualizações temporárias durante a duração da consulta principal. Cada subconsulta pode ser uma declaração `SELECT`, `TABLE`, `VALUES`, `INSERT`, `UPDATE`, `DELETE` ou `MERGE`. Ao escrever uma declaração que modifica dados (`INSERT`, `UPDATE`, `DELETE` ou `MERGE`) em `WITH`, é comum incluir uma cláusula `RETURNING`. É o resultado de `RETURNING`, *não* a tabela subjacente que a declaração modifica, que forma a tabela temporária que é lida pela consulta principal. Se `RETURNING` for omitido, a declaração ainda é executada, mas não produz saída, portanto, não pode ser referenciada como uma tabela pela consulta principal.

É necessário especificar um nome (sem qualificação de esquema) para cada consulta `WITH`. Opcionalmente, pode ser especificado uma lista de nomes de colunas; se isso for omitido, os nomes das colunas são inferidos a partir da subconsulta.

Se `RECURSIVE` for especificado, permite que uma subconsulta `SELECT` faça referência a si mesma pelo nome. Tal subconsulta deve ter a forma

```
non_recursive_term UNION [ ALL | DISTINCT ] recursive_term
```

onde a auto-referência recursiva deve aparecer no lado direito do `UNION`. Apenas uma auto-referência recursiva é permitida por consulta. As declarações de modificação de dados recursivas não são suportadas, mas você pode usar os resultados de uma consulta recursiva `SELECT` em uma declaração de modificação de dados. Veja [Seção 7.8](queries-with.md) para um exemplo.

Outro efeito de `RECURSIVE` é que as consultas de `WITH` não precisam ser ordenadas: uma consulta pode referenciar outra que está mais adiante na lista. (No entanto, as referências circulares, ou recursão mútua, não são implementadas.) Sem `RECURSIVE`, as consultas de `WITH` só podem referenciar consultas de `WITH` irmãs que estão mais cedo na lista de `WITH`.

Quando houver várias consultas na cláusula `WITH`, `RECURSIVE` deve ser escrito apenas uma vez, imediatamente após `WITH`. Ela se aplica a todas as consultas na cláusula `WITH`, embora não tenha efeito sobre consultas que não utilizam recursividade ou referências diretas.

A cláusula opcional `SEARCH` calcula uma coluna de *sequência de pesquisa* que pode ser usada para ordenar os resultados de uma consulta recursiva em ordem de largura ou ordem de profundidade. A lista de nomes de colunas fornecida especifica a chave da linha que deve ser usada para acompanhar as linhas visitadas. Uma coluna denominada *`search_seq_col_name`* será adicionada à lista de colunas de resultado da consulta `WITH`. Esta coluna pode ser ordenada na consulta externa para obter a ordenação respectiva. Consulte [Seção 7.8.2.1](queries-with.md#QUERIES-WITH-SEARCH) para exemplos.

A cláusula opcional `CYCLE` é usada para detectar ciclos em consultas recursivas. A lista de nomes de colunas fornecida especifica a chave da linha que deve ser usada para acompanhar as linhas visitadas. Uma coluna denominada *`cycle_mark_col_name`* será adicionada à lista de colunas de resultado da consulta `WITH`. Esta coluna será definida como *`cycle_mark_value`* quando um ciclo tiver sido detectado, caso contrário, como *`cycle_mark_default`*. Além disso, o processamento da união recursiva será interrompido quando um ciclo tiver sido detectado. *`cycle_mark_value`* e *`cycle_mark_default`* devem ser constantes e devem ser coeríveis a um tipo de dados comum, e o tipo de dados deve ter um operador de desigualdade. (O padrão SQL exige que sejam constantes booleanas ou cadeias de caracteres, mas o PostgreSQL não exige isso.) Por padrão, `TRUE` e `FALSE` (do tipo `boolean`) são usados. Além disso, uma coluna denominada *`cycle_path_col_name`* será adicionada à lista de colunas de resultado da consulta `WITH`. Esta coluna é usada internamente para acompanhar as linhas visitadas. Consulte [Seção 7.8.2.2](queries-with.md#QUERIES-WITH-CYCLE "7.8.2.2. Cycle Detection") para exemplos.

Tanto a cláusula `SEARCH` quanto a `CYCLE` são válidas apenas para consultas recursivas `WITH`. O *`with_query`* deve ser um `UNION` (ou `UNION ALL`) de dois comandos `SELECT` (ou equivalentes) (sem `UNION`s aninhados). Se ambas as cláusulas forem usadas, a coluna adicionada pela cláusula `SEARCH` aparece antes das colunas adicionadas pela cláusula `CYCLE`.

A consulta principal e as consultas `WITH` são todas (teoricamente) executadas ao mesmo tempo. Isso implica que os efeitos de uma declaração que modifica dados em `WITH` não podem ser vistos por outras partes da consulta, exceto pela leitura de sua saída `RETURNING`. Se duas dessas declarações que modificam dados tentarem modificar a mesma linha, os resultados não são especificados.

Uma propriedade chave das consultas `WITH` é que elas são normalmente avaliadas apenas uma vez por execução da consulta principal, mesmo que a consulta principal as refira mais de uma vez. Em particular, as declarações que modificam dados são garantidas para serem executadas uma vez e apenas uma vez, independentemente de a consulta principal ler todas ou qualquer uma de suas saídas.

No entanto, uma consulta `WITH` pode ser marcada como `NOT MATERIALIZED` para remover essa garantia. Nesse caso, a consulta `WITH` pode ser integrada à consulta principal, como se fosse uma subconsulta simples `SELECT` na cláusula `FROM` da consulta principal. Isso resulta em cálculos duplicados se a consulta principal se referir a essa consulta `WITH` mais de uma vez; mas se cada uso desse tipo requer apenas algumas linhas do total de saída da consulta `WITH`, a `NOT MATERIALIZED` pode proporcionar uma economia líquida ao permitir que as consultas sejam otimizadas conjuntamente. A `NOT MATERIALIZED` é ignorada se estiver anexada a uma consulta `WITH` que é recursiva ou não é livre de efeitos colaterais (ou seja, não é uma consulta simples `SELECT` que não contém funções voláteis).

Por padrão, uma consulta sem efeitos colaterais `WITH` é incorporada à consulta principal se for usada exatamente uma vez na cláusula `FROM` da consulta principal. Isso permite a otimização conjunta dos dois níveis de consulta em situações em que isso deve ser semanticamente invisível. No entanto, essa incorporação pode ser impedida marcando a consulta `WITH` como `MATERIALIZED`. Isso pode ser útil, por exemplo, se a consulta `WITH` estiver sendo usada como uma barreira de otimização para impedir que o planejador escolha um plano ruim. As versões do PostgreSQL anteriores à v12 nunca fizeram tal incorporação, portanto, consultas escritas para versões mais antigas podem depender de `WITH` para agir como uma barreira de otimização.

Consulte [Seção 7.8](queries-with.md) para obter informações adicionais.

### `FROM` Cláusula

A cláusula `FROM` especifica uma ou mais tabelas de origem para o `SELECT`. Se várias fontes são especificadas, o resultado é o produto cartesiano (cruzamento) de todas as fontes. Mas geralmente, condições de qualificação são adicionadas (via `WHERE`) para restringir as linhas retornadas a um pequeno subconjunto do produto cartesiano.

A cláusula `FROM` pode conter os seguintes elementos:

*`table_name`*: O nome (opcionalmente qualificado por esquema) de uma tabela ou visão existente. Se `ONLY` for especificado antes do nome da tabela, apenas essa tabela será analisada. Se `ONLY` não for especificado, a tabela e todas as suas tabelas descendentes (se houver) serão analisadas. Opcionalmente, `*` pode ser especificado após o nome da tabela para indicar explicitamente que as tabelas descendentes são incluídas.

*`alias`*: Um nome alternativo para o item `FROM` que contém o alias. Um alias é usado para brevidade ou para eliminar ambiguidade em auto-join (onde a mesma tabela é analisada várias vezes). Quando um alias é fornecido, ele oculta completamente o nome real da tabela ou função; por exemplo, dado `FROM foo AS f`, o restante do `SELECT` deve se referir a este item `FROM` como `f` e não `foo`. Se um alias for escrito, uma lista de alias de coluna também pode ser escrita para fornecer nomes alternativos para uma ou mais colunas da tabela.

`TABLESAMPLE sampling_method ( argument [, ...] ) [ REPEATABLE ( seed ) ]`: Uma cláusula `TABLESAMPLE` após um *`table_name`* indica que o *`sampling_method`* especificado deve ser usado para recuperar um subconjunto das linhas naquela tabela. Essa amostragem precede a aplicação de quaisquer outros filtros, como cláusulas `WHERE`. A distribuição padrão do PostgreSQL inclui dois métodos de amostragem, `BERNOULLI` e `SYSTEM`, e outros métodos de amostragem podem ser instalados no banco de dados por meio de extensões.

Os métodos de amostragem `BERNOULLI` e `SYSTEM` aceitam cada um um único *`argument`*, que é a fração da tabela a ser amostrada, expressa como uma porcentagem entre 0 e 100. Este argumento pode ser qualquer expressão com valor de `real`. (Outros métodos de amostragem podem aceitar mais argumentos ou diferentes argumentos.) Esses dois métodos retornam cada um uma amostra aleatoriamente escolhida da tabela que conterá aproximadamente a porcentagem especificada das linhas da tabela. O método `BERNOULLI` digitaliza toda a tabela e seleciona ou ignora linhas individuais de forma independente com a probabilidade especificada. O método `SYSTEM` realiza amostragem de nível de bloco, com cada bloco tendo a chance especificada de ser selecionado; todas as linhas em cada bloco selecionado são devolvidas. O método `SYSTEM` é significativamente mais rápido que o método `BERNOULLI` quando porcentagens de amostragem pequenas são especificadas, mas pode retornar uma amostra menos aleatória da tabela como resultado de efeitos de agrupamento.

A cláusula opcional `REPEATABLE` especifica um número ou expressão *`seed`* a ser usado para gerar números aleatórios dentro do método de amostragem. O valor da semente pode ser qualquer valor de ponto flutuante não nulo. Duas consultas que especificam o mesmo valor da semente e os valores de *`argument`* selecionarán a mesma amostra da tabela, se a tabela não tiver sido alterada durante esse período. Mas valores de semente diferentes geralmente produzirão amostras diferentes. Se `REPEATABLE` não for fornecido, uma nova amostra aleatória será selecionada para cada consulta, com base em uma semente gerada pelo sistema. Note que alguns métodos de amostragem adicionais não aceitam `REPEATABLE`, e sempre produzirão novas amostras em cada uso.

*`select`*: Um sub`SELECT` pode aparecer na cláusula `FROM`. Isso age como se sua saída fosse criada como uma tabela temporária para a duração deste único comando `SELECT`. Note que o sub`SELECT` deve ser cercado por parênteses e um alias pode ser fornecido da mesma maneira que para uma tabela. Um comando [[`VALUES`](sql-values.md)] também pode ser usado aqui.

*`with_query_name`*: Uma consulta `WITH` é referenciada escrevendo seu nome, como se o nome da consulta fosse o nome de uma tabela. (Na verdade, a consulta `WITH` oculta qualquer tabela real com o mesmo nome para os propósitos da consulta primária. Se necessário, você pode referenciar uma tabela real com o mesmo nome qualificando o nome da tabela pelo esquema.) Um alias pode ser fornecido da mesma maneira que para uma tabela.

*`function_name`*: As chamadas de função podem aparecer na cláusula `FROM`. (Isso é especialmente útil para funções que retornam conjuntos de resultados, mas qualquer função pode ser usada.) Isso age como se a saída da função fosse criada como uma tabela temporária durante a duração deste único comando `SELECT`. Se o tipo de resultado da função for composto (incluindo o caso de uma função com vários parâmetros `OUT`, cada atributo se torna uma coluna separada na tabela implícita.

Quando a cláusula opcional `WITH ORDINALITY` é adicionada à chamada de função, uma coluna adicional do tipo `bigint` será anexada à(s) coluna(s) de resultado da função. Essa coluna numera as linhas do conjunto de resultados da função, começando com o número 1. Por padrão, essa coluna é denominada `ordinality`.

Um alias pode ser fornecido da mesma maneira que para uma tabela. Se um alias for escrito, uma lista de alias de coluna também pode ser escrita para fornecer nomes substitutos para um ou mais atributos do tipo de retorno composto da função, incluindo a coluna ordinal se presente.

Várias chamadas de função podem ser combinadas em um único item da cláusula `FROM` ao serem envolvidas por `ROWS FROM( ... )`. A saída de tal item é a concatenação da primeira linha de cada função, em seguida, a segunda linha de cada função, etc. Se algumas das funções produzem menos linhas do que outras, valores nulos são substituídos pelos dados ausentes, de modo que o número total de linhas devolvidas é sempre o mesmo que para a função que produziu as mais linhas.

Se a função tiver sido definida para retornar o tipo de dados `record`, então um alias ou a palavra-chave `AS` deve estar presente, seguida de uma lista de definição de coluna na forma `( column_name data_type [, ... ])`. A lista de definição de coluna deve corresponder ao número e aos tipos de colunas reais retornados pela função.

Ao usar a sintaxe `ROWS FROM( ... )`, se uma das funções requer uma lista de definição de coluna, é preferível colocar a lista de definição de coluna após a chamada de função dentro de `ROWS FROM( ... )`. Uma lista de definição de coluna pode ser colocada após a construção `ROWS FROM( ... )` apenas se houver apenas uma única função e nenhuma cláusula `WITH ORDINALITY`.

Para usar `ORDINALITY` junto com uma lista de definição de coluna, você deve usar a sintaxe `ROWS FROM( ... )` e colocar a lista de definição de coluna dentro de `ROWS FROM( ... )`.

*`join_type`*: Uma das

* `[ INNER ] JOIN` * `LEFT [ OUTER ] JOIN` * `RIGHT [ OUTER ] JOIN` * `FULL [ OUTER ] JOIN`

Para os tipos de junção `INNER` e `OUTER`, uma condição de junção deve ser especificada, ou seja, exatamente um dos `ON join_condition`, `USING (join_column [, ...])` ou `NATURAL`. Veja abaixo o significado.

Uma cláusula `JOIN` combina dois itens `FROM`, que, por conveniência, chamaremos de “tabelas”, embora, na realidade, possam ser qualquer tipo de item `FROM`. Use parênteses, se necessário, para determinar a ordem de ninho. Na ausência de parênteses, os `JOIN`s se aninham de esquerda para direita. Em qualquer caso, o `JOIN` se liga mais fortemente do que as vírgulas que separam os itens da lista `FROM`. Todas as opções de `JOIN` são apenas uma conveniência de notação, uma vez que não fazem nada que você não pudesse fazer com `FROM` e `WHERE` comuns.

`LEFT OUTER JOIN` retorna todas as linhas do produto cartesiano qualificado (ou seja, todas as linhas combinadas que passam pela condição de junção), além de uma cópia de cada linha da tabela da esquerda para a qual não havia nenhuma linha da tabela da direita que passasse pela condição de junção. Essa linha da esquerda é estendida até a largura total da tabela unificada, inserindo valores nulos para as colunas da direita. Note que apenas a condição própria da cláusula `JOIN` é considerada ao decidir quais linhas têm correspondências. As condições externas são aplicadas posteriormente.

Por outro lado, `RIGHT OUTER JOIN` retorna todas as linhas unidas, além de uma linha para cada linha correspondente à direita (extendida com nulos à esquerda). Isso é apenas uma conveniência de notação, pois você poderia convertê-lo em `LEFT OUTER JOIN` ao alternar as tabelas esquerda e direita.

`FULL OUTER JOIN` retorna todas as linhas unidas, além de uma linha para cada linha esquerda não correspondente (extendida com nulos à direita), além de uma linha para cada linha direita não correspondente (extendida com nulos à esquerda).

`ON join_condition`: *`join_condition`* é uma expressão que resulta em um valor do tipo `boolean` (semelhante a uma cláusula `WHERE`) que especifica quais linhas em uma junção são consideradas para corresponder.

`USING ( join_column [, ...] ) [ AS join_using_alias ]`: Uma cláusula na forma de `USING ( a, b, ... )` é uma abreviação para `ON left_table.a = right_table.a AND left_table.b = right_table.b ...`. Além disso, `USING` implica que apenas um dos pares de colunas equivalentes será incluído na saída do join, não ambos.

Se um nome *`join_using_alias`* for especificado, ele fornece um alias de tabela para as colunas de junção. Apenas as colunas de junção listadas na cláusula `USING` podem ser acessadas por este nome. Ao contrário de um *`alias`* regular, isso não oculta os nomes das tabelas unidas do resto da consulta. Além disso, ao contrário de um *`alias`* regular, você não pode escrever uma lista de aliases de coluna — os nomes de saída das colunas de junção são os mesmos que aparecem na lista `USING`.

`NATURAL`: `NATURAL` é uma abreviação para uma lista `USING` que menciona todas as colunas nas duas tabelas que têm nomes correspondentes. Se não houver nomes de colunas comuns, `NATURAL` é equivalente a `ON TRUE`.

`CROSS JOIN`: `CROSS JOIN` é equivalente a `INNER JOIN ON (TRUE)`, ou seja, nenhuma linha é removida por qualificação. Eles produzem um produto cartesiano simples, o mesmo resultado que você obtém ao listar as duas tabelas no nível superior de `FROM`, mas restrito pela condição de junção (se houver).

`LATERAL`: A palavra-chave `LATERAL` pode preceder um sub-`SELECT` item `FROM`. Isso permite que o sub-`SELECT` faça referência a colunas de itens `FROM` que aparecem antes dele na lista `FROM`. (Sem `LATERAL`, cada sub-`SELECT` é avaliado de forma independente e, portanto, não pode fazer referência a nenhum outro item `FROM`.

`LATERAL` também pode preceder um item de chamada de função `FROM`, mas, neste caso, é uma palavra de ruído, porque a expressão da função pode se referir a itens anteriores `FROM` em qualquer caso.

Um item `LATERAL` pode aparecer no nível superior na lista `FROM`, ou dentro de uma árvore `JOIN`. Neste último caso, ele também pode se referir a quaisquer itens que estão do lado esquerdo de um `JOIN` que ele esteja do lado direito.

Quando um item `FROM` contém referências cruzadas `LATERAL`, a avaliação é realizada da seguinte forma: para cada linha do item `FROM` que fornece a(s) coluna(s) referenciada(s), ou conjunto de linhas de vários itens `FROM` que fornecem as colunas, o item `LATERAL` é avaliado usando os valores das colunas daquela linha ou conjunto de linhas. As linhas resultantes são unidas, como de costume, com as linhas de que foram calculadas. Isso é repetido para cada linha ou conjunto de linhas da(s) tabela(s) fonte da coluna.

A(s) tabela(s) de fonte em coluna deve(m) ser `INNER` ou `LEFT` associada(s) ao item `LATERAL`, caso contrário, não haveria um conjunto bem definido de linhas a partir do qual calcular cada conjunto de linhas para o item `LATERAL`. Assim, embora uma construção como `X RIGHT JOIN LATERAL Y` seja sintaticamente válida, ela não é realmente permitida para que *`Y`* faça referência a *`X`*.

### `WHERE` Cláusula

A cláusula opcional `WHERE` tem a forma geral

```
WHERE condition
```

onde *`condition`* é qualquer expressão que avalie um resultado do tipo `boolean`. Qualquer linha que não satisfaça essa condição será eliminada da saída. Uma linha satisfaz a condição se retornar verdadeiro quando os valores reais da linha são substituídos por quaisquer referências de variáveis.

### `GROUP BY` Cláusula

A cláusula opcional `GROUP BY` tem a forma geral

```
GROUP BY [ ALL | DISTINCT ] grouping_element [, ...]
```

`GROUP BY` condensará em uma única linha todas as linhas selecionadas que compartilham os mesmos valores para as expressões agrupadas. Um *`expression`* usado dentro de um *`grouping_element`* pode ser o nome de uma coluna de entrada, ou o nome ou número ordinal de uma coluna de saída (`SELECT` item da lista), ou uma expressão arbitrária formada a partir dos valores das colunas de entrada. Em caso de ambiguidade, um nome de `GROUP BY` será interpretado como o nome de uma coluna de entrada, e não como o nome de uma coluna de saída.

Se algum dos elementos de agrupamento `GROUPING SETS`, `ROLLUP` ou `CUBE` estiver presente como elemento de agrupamento, então a cláusula `GROUP BY` como um todo define um número de *`grouping sets`* independentes. O efeito disso é equivalente à construção de um `UNION ALL` entre subconsultas com os conjuntos de agrupamento individuais como suas cláusulas `GROUP BY`. A cláusula opcional `DISTINCT` remove conjuntos duplicados antes do processamento; ela *não* transforma o `UNION ALL` em um `UNION DISTINCT`. Para mais detalhes sobre o tratamento dos conjuntos de agrupamento, consulte [Seção 7.2.4](queries-table-expressions.md#QUERIES-GROUPING-SETS "7.2.4. GROUPING SETS, CUBE, and ROLLUP").

As funções agregadas, se houver, são calculadas em todas as linhas que compõem cada grupo, produzindo um valor separado para cada grupo. (Se houver funções agregadas, mas sem a cláusula `GROUP BY`, a consulta é tratada como tendo um único grupo que compreende todas as linhas selecionadas.) O conjunto de linhas fornecidas a cada função agregada pode ser filtrado ainda mais anexando uma cláusula `FILTER` à chamada da função agregada; consulte [Seção 4.2.7](sql-expressions.md#SYNTAX-AGGREGATES) para mais informações. Quando houver uma cláusula `FILTER`, apenas as linhas que correspondem a ela são incluídas na entrada para essa função agregada.

Quando `GROUP BY` está presente, ou quaisquer funções agregadas estão presentes, não é válido para as expressões de listas `SELECT` referirem-se a colunas não agrupadas, exceto dentro de funções agregadas ou quando a coluna não agrupada é funcionalmente dependente das colunas agrupadas, pois, caso contrário, haveria mais de um valor possível para retornar para uma coluna não agrupada. Existe uma dependência funcional se as colunas agrupadas (ou um subconjunto delas) forem a chave primária da tabela que contém a coluna não agrupada.

Tenha em mente que todas as funções agregadas são avaliadas antes de avaliar quaisquer expressões “escalares” na cláusula `HAVING` ou na lista `SELECT`. Isso significa, por exemplo, que uma expressão `CASE` não pode ser usada para ignorar a avaliação de uma função agregada; veja [Seção 4.2.14](sql-expressions.md#SYNTAX-EXPRESS-EVAL).

Atualmente, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` e `FOR KEY SHARE` não podem ser especificados com `GROUP BY`.

### `HAVING` Cláusula

A cláusula opcional `HAVING` tem a forma geral

```
HAVING condition
```

onde *`condition`* é o mesmo que especificado para a cláusula `WHERE`.

`HAVING` elimina as linhas do grupo que não satisfazem a condição. `HAVING` é diferente de `WHERE`: `WHERE` filtra as linhas individuais antes da aplicação de `GROUP BY`, enquanto `HAVING` filtra as linhas do grupo criadas por `GROUP BY`. Cada coluna referenciada em *`condition`* deve referenciar de forma inequívoca uma coluna de agrupamento, a menos que a referência apareça dentro de uma função agregada ou a coluna não agrupada dependa funcionalmente dos colunas de agrupamento.

A presença de `HAVING` transforma uma consulta em uma consulta agrupada, mesmo que não haja uma cláusula `GROUP BY`. Isso é o mesmo que acontece quando a consulta contém funções agregadas, mas não há uma cláusula `GROUP BY`. Todas as linhas selecionadas são consideradas para formar um único grupo, e a lista `SELECT` e a cláusula `HAVING` só podem fazer referência a colunas da tabela dentro das funções agregadas. Uma consulta desse tipo emitirá uma única linha se a condição `HAVING` for verdadeira, zero linhas se não for verdadeira.

Atualmente, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` e `FOR KEY SHARE` não podem ser especificados com `HAVING`.

### `WINDOW` Cláusula

A cláusula opcional `WINDOW` tem a forma geral

```
WINDOW window_name AS ( window_definition ) [, ...]
```

onde *`window_name`* é um nome que pode ser referenciado a partir das cláusulas de `OVER` ou definições subsequentes de janela, e *`window_definition`* é

```
[ existing_window_name ]
[ PARTITION BY expression [, ...] ]
[ ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS { FIRST | LAST } ] [, ...] ]
[ frame_clause ]
```

Se um *`existing_window_name`* for especificado, ele deve se referir a uma entrada anterior na lista `WINDOW`; a nova janela copia sua cláusula de particionamento dessa entrada, bem como sua cláusula de ordenação, se houver. Neste caso, a nova janela não pode especificar sua própria cláusula `PARTITION BY`, e pode especificar `ORDER BY` apenas se a janela copiada não tiver uma. A nova janela sempre usa sua própria cláusula de quadro; a janela copiada não deve especificar uma cláusula de quadro.

Os elementos da lista `PARTITION BY` são interpretados de maneira muito semelhante aos elementos de uma cláusula `GROUP BY`(sql-select.md#SQL-GROUPBY "GROUP BY Clause"), exceto que eles são sempre expressões simples e nunca o nome ou o número de uma coluna de saída. Outra diferença é que essas expressões podem conter chamadas de função agregada, que não são permitidas em uma cláusula regular `GROUP BY`. Elas são permitidas aqui porque o windowing ocorre após o agrupamento e agregação.

Da mesma forma, os elementos da lista `ORDER BY` são interpretados de maneira muito semelhante aos elementos de uma cláusula de nível de declaração `ORDER BY`(sql-select.md#SQL-ORDERBY "ORDER BY Clause"), exceto que as expressões são sempre consideradas expressões simples e nunca o nome ou o número de uma coluna de saída.

O opcional *`frame_clause`* define o *quadro de janela* para funções de janela que dependem do quadro (nem todas dependem). O quadro de janela é um conjunto de linhas relacionadas para cada linha da consulta (chamado de *linha atual*). O *`frame_clause`* pode ser um dos

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

Se *`frame_end`* for omitido, ele será predefinido como `CURRENT ROW`. As restrições são que *`frame_start`* não pode ser `UNBOUNDED FOLLOWING`, *`frame_end`* não pode ser `UNBOUNDED PRECEDING`, e a opção *`frame_end`* não pode aparecer anteriormente na lista acima de opções de *`frame_start`* e *`frame_end`* do que a opção *`frame_start`* faz — por exemplo, `RANGE BETWEEN CURRENT ROW AND offset PRECEDING` não é permitido.

A opção padrão de enquadramento é `RANGE UNBOUNDED PRECEDING`, que é a mesma que `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`; ela define o enquadramento como todas as linhas da partição, do início até a última *peer* (uma linha que a cláusula `ORDER BY` da janela considera equivalente à linha atual; todas as linhas são peers se não houver `ORDER BY`). Em geral, `UNBOUNDED PRECEDING` significa que o enquadramento começa com a primeira linha da partição, e da mesma forma, `UNBOUNDED FOLLOWING` significa que o enquadramento termina com a última linha da partição, independentemente de `RANGE`, `ROWS` ou `GROUPS` modo. No modo `ROWS`, `CURRENT ROW` significa que o enquadramento começa ou termina com a linha atual; mas no modo `RANGE` ou `GROUPS`, significa que o enquadramento começa ou termina com o primeiro ou último peer da linha atual na ordem `ORDER BY`. As opções *`offset`* e *`PRECEDING` e *`offset`* `FOLLOWING` variam em significado dependendo do modo de enquadramento. No modo `ROWS`, o *`offset`* é um inteiro que indica que o enquadramento começa ou termina tantas linhas antes ou depois da linha atual. No modo `GROUPS`, o *`offset`* é um inteiro que indica que o enquadramento começa ou termina tantas grupos de peers antes ou depois do grupo de peers da linha atual, onde um *grupo de peers* é um grupo de linhas que são equivalentes de acordo com a cláusula `ORDER BY` da janela. No modo `RANGE`, o uso de uma opção *`offset`* exige que haja exatamente uma coluna `ORDER BY` na definição da janela. Então, o enquadramento contém essas linhas cujo valor da coluna de ordenação é não mais do que *`offset`* menos (para `PRECEDING`) ou mais (para `FOLLOWING`) do valor da coluna de ordenação da linha atual. Nesses casos, o tipo de dados da expressão *`offset`* depende do tipo de dados da coluna de ordenação. Para colunas de ordenação numérica, é tipicamente do mesmo tipo que a coluna de ordenação, mas para colunas de ordenação de datas, é um `interval`. Em todos esses casos, o valor do *`offset`* deve ser não nulo e não negativo. Além disso, embora o *`offset`* não precise ser uma constante simples, ele não pode conter variáveis, funções agregadas ou funções de janela.

A opção *`frame_exclusion`* permite que as linhas ao redor da linha atual sejam excluídas do quadro, mesmo que elas fossem incluídas de acordo com as opções de início e fim do quadro. `EXCLUDE CURRENT ROW` exclui a linha atual do quadro. `EXCLUDE GROUP` exclui a linha atual e seus pares de ordenação do quadro. `EXCLUDE TIES` exclui quaisquer pares da linha atual do quadro, mas não a própria linha atual. `EXCLUDE NO OTHERS` especifica simplesmente explicitamente o comportamento padrão de não excluir a linha atual ou seus pares.

Cuidado, pois o modo `ROWS` pode produzir resultados imprevisíveis se a `ORDER BY` não ordenar as linhas de forma exclusiva. Os modos `RANGE` e `GROUPS` são projetados para garantir que as linhas que são iguais no `ORDER BY` sejam tratadas da mesma forma: todas as linhas de um grupo de pares específico estarão no quadro ou excluídas dele.

O propósito de uma cláusula `WINDOW` é especificar o comportamento das funções *de janela* que aparecem na lista de cláusulas [[PH_LNK_458]] ou `ORDER BY` da consulta. Essas funções podem referenciar as entradas da cláusula (sql-select.md#SQL-ORDERBY "ORDER BY Clause") da cláusula `WINDOW` por nome. Uma entrada de cláusula [[PH_LNK_457]] não precisa ser referenciada em nenhum lugar; no entanto, se não for usada na consulta, ela é simplesmente ignorada. É possível usar funções de janela sem nenhuma cláusula [[PH_LNK_458]] no todo, uma vez que uma chamada de função de janela pode especificar sua definição de janela diretamente em sua cláusula [[PH_LNK_459]]. No entanto, a cláusula [[PH_LNK_460]] economiza digitação quando a mesma definição de janela é necessária para mais de uma função de janela.

Atualmente, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` e `FOR KEY SHARE` não podem ser especificados com `WINDOW`.

As funções de janela são descritas em detalhes em [Seção 3.5](tutorial-window.md), [Seção 4.2.8](sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS) e [Seção 7.2.5](queries-table-expressions.md#QUERIES-WINDOW).

### `SELECT` Lista

A lista `SELECT` (entre as palavras-chave `SELECT` e `FROM`) especifica expressões que formam as linhas de saída da declaração `SELECT`. As expressões podem (e geralmente fazem) se referir a colunas calculadas na cláusula `FROM`.

Assim como em uma tabela, cada coluna de saída de um `SELECT` tem um nome. Em um simples `SELECT`, esse nome é apenas usado para rotular a coluna para exibição, mas quando o `SELECT` é uma subconsulta de uma consulta maior, o nome é visto pela consulta maior como o nome da coluna da tabela virtual produzida pela subconsulta. Para especificar o nome a ser usado para uma coluna de saída, escreva `AS` *`output_name`* após a expressão da coluna. (Você pode omitir `AS`, mas apenas se o nome de saída desejado não corresponder a nenhuma palavra-chave do PostgreSQL (consulte [Apêndice C](sql-keywords-appendix.md)). Para proteção contra possíveis adições de palavras-chave futuras, é recomendável que você escreva sempre `AS` ou coloque aspas duplas no nome de saída.) Se você não especificar um nome de coluna, um nome é escolhido automaticamente pelo PostgreSQL. Se a expressão da coluna for uma simples referência de coluna, o nome escolhido é o mesmo do nome daquela coluna. Em casos mais complexos, pode-se usar o nome de uma função ou tipo, ou o sistema pode recorrer a um nome gerado, como `?column?`.

O nome de uma coluna de saída pode ser usado para se referir ao valor da coluna nas cláusulas `ORDER BY` e `GROUP BY`, mas não nas cláusulas `WHERE` ou `HAVING`; você deve escrever a expressão em vez disso.

Em vez de uma expressão, `*` pode ser escrito na lista de saída como uma abreviação para todas as colunas das linhas selecionadas. Além disso, você pode escrever `table_name.*` como uma abreviação para as colunas que vêm apenas dessa tabela. Nesses casos, não é possível especificar novos nomes com `AS`; os nomes das colunas de saída serão os mesmos dos nomes das colunas da tabela.

De acordo com o padrão SQL, as expressões na lista de saída devem ser calculadas antes de aplicar `DISTINCT`, `ORDER BY` ou `LIMIT`. Isso é obviamente necessário ao usar `DISTINCT`, pois, caso contrário, não fica claro quais valores estão sendo distinguidos. No entanto, em muitos casos, é conveniente se as expressões de saída forem calculadas após `ORDER BY` e `LIMIT`; particularmente se a lista de saída contiver funções voláteis ou caras. Com esse comportamento, a ordem das avaliações das funções é mais intuitiva e não haverá avaliações correspondentes a linhas que nunca aparecem na saída. O PostgreSQL avaliará efetivamente as expressões de saída após o ordenamento e o limite, desde que essas expressões não sejam referenciadas em `DISTINCT`, `ORDER BY` ou `GROUP BY`. (Como exemplo, `SELECT f(x) FROM tab ORDER BY 1` deve claramente avaliar `f(x)` antes do ordenamento.) As expressões de saída que contêm funções que retornam conjuntos são avaliadas efetivamente após o ordenamento e antes do limite, de modo que `LIMIT` atuará para cortar a saída de uma função que retorna um conjunto.

Nota

As versões do PostgreSQL anteriores à 9.6 não forneciam garantias sobre o momento da avaliação de expressões de saída em relação à ordenação e limitação; isso dependia da forma do plano de consulta escolhido.

### `DISTINCT` Cláusula

Se `SELECT DISTINCT` for especificado, todas as linhas duplicadas serão removidas do conjunto de resultados (uma linha será mantida de cada grupo de duplicados). `SELECT ALL` especifica o oposto: todas as linhas serão mantidas; ou seja, é o padrão.

`SELECT DISTINCT ON ( expression [, ...] )` mantém apenas a primeira linha de cada conjunto de linhas onde as expressões fornecidas se equivalem. As expressões `DISTINCT ON` são interpretadas usando as mesmas regras que para `ORDER BY` (veja acima). Observe que a “primeira linha” de cada conjunto é imprevisível, a menos que `ORDER BY` seja usado para garantir que a linha desejada apareça primeiro. Por exemplo:

```
SELECT DISTINCT ON (location) location, time, report
    FROM weather_reports
    ORDER BY location, time DESC;
```

recupera o relatório meteorológico mais recente para cada local. Mas se não tivéssemos usado `ORDER BY` para forçar a ordem decrescente dos valores de tempo para cada local, teríamos recebido um relatório de um tempo imprevisível para cada local.

A(s) expressão(ões) `DISTINCT ON` deve(m) corresponder à(s) expressão(ões) mais à esquerda `ORDER BY`. A cláusula `ORDER BY` normalmente conterá(ão) expressão(ões) adicionais que determinam a precedência desejada das linhas dentro de cada grupo `DISTINCT ON`.

Atualmente, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` e `FOR KEY SHARE` não podem ser especificados com `DISTINCT`.

### `UNION` Cláusula

A cláusula `UNION` tem a seguinte forma geral:

```
select_statement UNION [ ALL | DISTINCT ] select_statement
```

*`select_statement`* é qualquer declaração `SELECT` sem uma cláusula `ORDER BY`, `LIMIT`, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` ou `FOR KEY SHARE`. (`ORDER BY` e `LIMIT` podem ser anexados a uma subexpressão se estiverem contidos entre parênteses. Sem parênteses, essas cláusulas serão consideradas aplicáveis ao resultado do `UNION`, e não à expressão de entrada da direita.)

O operador `UNION` calcula a união de conjuntos das linhas devolvidas pelas declarações envolvidas `SELECT`. Uma linha está na união de conjuntos de dois conjuntos de resultados se ela aparecer em pelo menos um dos conjuntos de resultados. As duas declarações `SELECT` que representam os operandos diretos do `UNION` devem produzir o mesmo número de colunas, e as colunas correspondentes devem ser de tipos de dados compatíveis.

O resultado de `UNION` não contém nenhuma linha duplicada, a menos que a opção `ALL` seja especificada. `ALL` impede a eliminação de duplicatas. (Portanto, `UNION ALL` geralmente é significativamente mais rápido do que `UNION`; use `ALL` quando puder.) `DISTINCT` pode ser escrito para especificar explicitamente o comportamento padrão de eliminação de linhas duplicadas.

Múltiplos operadores `UNION` na mesma declaração `SELECT` são avaliados da esquerda para a direita, a menos que haja indicação em contrário entre parênteses.

Atualmente, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` e `FOR KEY SHARE` não podem ser especificados nem para um resultado de `UNION` ou para qualquer entrada de um `UNION`.

### `INTERSECT` Cláusula

A cláusula `INTERSECT` tem a seguinte forma geral:

```
select_statement INTERSECT [ ALL | DISTINCT ] select_statement
```

*`select_statement`* é qualquer declaração `SELECT` sem uma cláusula `ORDER BY`, `LIMIT`, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` ou `FOR KEY SHARE`.

O operador `INTERSECT` calcula a interseção de conjuntos das linhas devolvidas pelas declarações envolvidas `SELECT`. Uma linha está na interseção de dois conjuntos de resultados se ela aparecer em ambos os conjuntos de resultados.

O resultado de `INTERSECT` não contém nenhuma linha duplicada, a menos que a opção `ALL` seja especificada. Com `ALL`, uma linha que tenha *`m`* duplicados na tabela esquerda e *`n`* duplicados na tabela direita aparecerá min(*`m`*,*`n`*) vezes no conjunto de resultados. `DISTINCT` pode ser escrito para especificar explicitamente o comportamento padrão de eliminação de linhas duplicadas.

Múltiplos operadores `INTERSECT` na mesma declaração `SELECT` são avaliados da esquerda para a direita, a menos que as chaves de parênteses indiquem o contrário. `INTERSECT` se liga mais fortemente do que `UNION`. Isso significa que `A UNION B INTERSECT C` será lido como `A UNION (B INTERSECT C)`.

Atualmente, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` e `FOR KEY SHARE` não podem ser especificados nem para um resultado de `INTERSECT` ou para qualquer entrada de um `INTERSECT`.

### `EXCEPT` Cláusula

A cláusula `EXCEPT` tem a seguinte forma geral:

```
select_statement EXCEPT [ ALL | DISTINCT ] select_statement
```

*`select_statement`* é qualquer declaração `SELECT` sem uma cláusula `ORDER BY`, `LIMIT`, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` ou `FOR KEY SHARE`.

O operador `EXCEPT` calcula o conjunto de linhas que estão no resultado da declaração esquerda `SELECT`, mas não no resultado da declaração direita.

O resultado de `EXCEPT` não contém nenhuma linha duplicada, a menos que a opção `ALL` seja especificada. Com `ALL`, uma linha que tenha *`m`* duplicados na tabela esquerda e *`n`* duplicados na tabela direita aparecerá no máximo (*`m`* até *`n`*,0) vezes no conjunto de resultados. `DISTINCT` pode ser escrito para especificar explicitamente o comportamento padrão de eliminação de linhas duplicadas.

Múltiplos operadores `EXCEPT` na mesma declaração `SELECT` são avaliados da esquerda para a direita, a menos que as chaves de parênteses indiquem o contrário. `EXCEPT` se vincula no mesmo nível que `UNION`.

Atualmente, `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE` e `FOR KEY SHARE` não podem ser especificados nem para um resultado de `EXCEPT` ou para qualquer entrada de um `EXCEPT`.

### `ORDER BY` Cláusula

A cláusula opcional `ORDER BY` tem a seguinte forma geral:

```
ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS { FIRST | LAST } ] [, ...]
```

A cláusula `ORDER BY` faz com que as linhas de resultado sejam ordenadas de acordo com a(s) expressão(ões) especificada(s). Se duas linhas forem iguais de acordo com a expressão mais à esquerda, elas são comparadas de acordo com a próxima expressão e assim por diante. Se forem iguais de acordo com todas as expressões especificadas, elas são devolvidas em uma ordem dependente da implementação.

Cada *`expression`* pode ser o nome ou o número ordinal de uma coluna de saída (item da lista `SELECT`), ou pode ser uma expressão arbitrária formada a partir dos valores das colunas de entrada.

O número ordinal refere-se à posição ordinal (da esquerda para a direita) da coluna de saída. Este recurso permite definir uma ordem com base em uma coluna que não tem um nome único. Isso nunca é absolutamente necessário, pois é sempre possível atribuir um nome a uma coluna de saída usando a cláusula `AS`.

É também possível usar expressões arbitrárias na cláusula `ORDER BY`, incluindo colunas que não aparecem na lista de saída `SELECT`. Assim, a seguinte declaração é válida:

```
SELECT name FROM distributors ORDER BY code;
```

Uma limitação dessa funcionalidade é que uma cláusula `ORDER BY` que se aplica ao resultado de uma cláusula `UNION`, `INTERSECT` ou `EXCEPT` só pode especificar um nome ou número de coluna de saída, não uma expressão.

Se uma expressão `ORDER BY` for um nome simples que corresponda tanto a um nome de coluna de saída quanto a um nome de coluna de entrada, `ORDER BY` a interpretará como o nome da coluna de saída. Isso é o oposto da escolha que `GROUP BY` fará na mesma situação. Essa inconsistência é feita para ser compatível com o padrão SQL.

Opcionalmente, é possível adicionar a palavra-chave `ASC` (ascendente) ou `DESC` (descendente) após qualquer expressão na cláusula `ORDER BY`. Se não for especificado, `ASC` é assumido como padrão. Alternativamente, um nome específico do operador de ordenação pode ser especificado na cláusula `USING`. Um operador de ordenação deve ser um membro de menos-que ou maior-que de alguma família de operadores de B-tree. `ASC` é geralmente equivalente a `USING <` e `DESC` é geralmente equivalente a `USING >`. (Mas o criador de um tipo de dados definido pelo usuário pode definir exatamente qual é a ordem de classificação padrão, e pode corresponder a operadores com outros nomes.)

Se `NULLS LAST` for especificado, os valores nulos são ordenados após todos os valores não nulos; se `NULLS FIRST` for especificado, os valores nulos são ordenados antes de todos os valores não nulos. Se nenhum dos dois for especificado, o comportamento padrão é `NULLS LAST` quando `ASC` é especificado ou implícito, e `NULLS FIRST` quando `DESC` é especificado (assim, o padrão é agir como se os nulos fossem maiores que os não nulos). Quando `USING` for especificado, a ordem padrão dos nulos depende se o operador é um operador de menos que ou maior que.

Observe que as opções de ordenação se aplicam apenas à expressão que as segue; por exemplo, `ORDER BY x, y DESC` não significa a mesma coisa que `ORDER BY x DESC, y DESC`.

Os dados de cadeia de caracteres são ordenados de acordo com a ordenação que se aplica à coluna que está sendo ordenada. Isso pode ser sobrescrito conforme necessário, incluindo uma cláusula `COLLATE` no *`expression`*, por exemplo `ORDER BY mycolumn COLLATE "en_US"`. Para mais informações, consulte [Seção 4.2.10](sql-expressions.md#SQL-SYNTAX-COLLATE-EXPRS "4.2.10. Collation Expressions") e [Seção 23.2](collation.md "23.2. Collation Support").

### `LIMIT` Cláusula

A cláusula `LIMIT` é composta por duas subcláusulas independentes:

```
LIMIT { count | ALL }
OFFSET start
```

O parâmetro *`count`* especifica o número máximo de linhas a serem retornadas, enquanto *`start`* especifica o número de linhas a serem ignoradas antes de começar a retornar as linhas. Quando ambos são especificados, as linhas de *`start`* são ignoradas antes de começar a contar as linhas de *`count`* a serem retornadas.

Se a expressão *`count`* for NULL, ela é tratada como `LIMIT ALL`, ou seja, sem limite. Se *`start`* for NULL, ela é tratada da mesma forma que `OFFSET 0`.

SQL:2008 introduziu uma sintaxe diferente para alcançar o mesmo resultado, que o PostgreSQL também suporta. É:

```
OFFSET start { ROW | ROWS }
FETCH { FIRST | NEXT } [ count ] { ROW | ROWS } { ONLY | WITH TIES }
```

Nessa sintaxe, o valor *`start`* ou *`count`* é exigido pelo padrão para ser uma constante literal, um parâmetro ou um nome de variável; como uma extensão do PostgreSQL, outras expressões são permitidas, mas geralmente precisam ser fechadas entre parênteses para evitar ambiguidade. Se *`count`* é omitido em uma cláusula `FETCH`, ele é predefinido como 1. A opção `WITH TIES` é usada para retornar quaisquer linhas adicionais que se igualem ao último lugar no conjunto de resultados de acordo com a cláusula `ORDER BY`; `ORDER BY` é obrigatório neste caso, e `SKIP LOCKED` não é permitido. `ROW` e `ROWS`, bem como `FIRST` e `NEXT` são palavras de ruído que não influenciam os efeitos dessas cláusulas. De acordo com o padrão, a cláusula `OFFSET` deve vir antes da cláusula `FETCH` se ambas estiverem presentes; mas o PostgreSQL é mais flexível e permite qualquer ordem.

Ao usar `LIMIT`, é uma boa ideia usar uma cláusula `ORDER BY` que restringe as linhas de resultado a uma ordem única. Caso contrário, você obterá um subconjunto imprevisível das linhas da consulta — você pode estar pedindo as décima a vigésima linhas, mas décima a vigésima em que ordem? Você não sabe em que ordem, a menos que especifique `ORDER BY`.

O planejador de consulta leva em consideração `LIMIT` ao gerar um plano de consulta, portanto, é muito provável que você obtenha diferentes planos (que gerem diferentes ordens de linhas) dependendo do que você usa para `LIMIT` e `OFFSET`. Assim, usar diferentes valores de `LIMIT`/`OFFSET` para selecionar diferentes subconjuntos de um resultado de consulta *dará resultados inconsistentes*, a menos que você imponha uma ordem de resultado previsível com `ORDER BY`. Isso não é um bug; é uma consequência inerente do fato de que o SQL não promete entregar os resultados de uma consulta em qualquer ordem específica, a menos que `ORDER BY` seja usado para restringir a ordem.

É até possível que execuções repetidas da mesma consulta `LIMIT` retornem diferentes subconjuntos das linhas de uma tabela, se não houver um `ORDER BY` para impor a seleção de um subconjunto determinístico. Novamente, isso não é um erro; o determinismo dos resultados simplesmente não é garantido nesse caso.

### A Cláusula de Fechamento

`FOR UPDATE`, `FOR NO KEY UPDATE`, `FOR SHARE` e `FOR KEY SHARE` são cláusulas de *bloqueio*; elas afetam a forma como `SELECT` bloqueia as linhas à medida que elas são obtidas da tabela.

A cláusula de bloqueio tem a forma geral

```
FOR lock_strength [ OF from_reference [, ...] ] [ NOWAIT | SKIP LOCKED ]
```

onde *`lock_strength`* pode ser um dos

```
UPDATE
NO KEY UPDATE
SHARE
KEY SHARE
```

*`from_reference`* deve ser uma tabela *`alias`* ou não oculta *`table_name`* referenciada na cláusula *`FROM`. Para mais informações sobre cada modo de bloqueio em nível de linha, consulte [Seção 13.3.2](explicit-locking.md#LOCKING-ROWS "13.3.2. Row-Level Locks").

Para evitar que a operação espere que outras transações sejam confirmadas, use a opção `NOWAIT` ou `SKIP LOCKED`. Com `NOWAIT`, a declaração reporta um erro, em vez de esperar, se uma linha selecionada não puder ser bloqueada imediatamente. Com `SKIP LOCKED`, quaisquer linhas selecionadas que não possam ser bloqueadas imediatamente são ignoradas. Ignorar linhas bloqueadas fornece uma visão inconsistente dos dados, portanto, isso não é adequado para trabalhos de propósito geral, mas pode ser usado para evitar disputa de bloqueio com vários consumidores acessando uma tabela semelhante a uma fila. Note que `NOWAIT` e `SKIP LOCKED` aplicam-se apenas aos(s) bloqueio(s) ao nível da linha — o bloqueio(s) ao nível da tabela requerido(s) `ROW SHARE` ainda é tomado da maneira comum (ver [Capítulo 13](mvcc.md "Chapter 13. Concurrency Control")). Você pode usar [[`LOCK`](sql-lock.md)] com a opção `NOWAIT` primeiro, se você precisar adquirir o bloqueio(s) ao nível da tabela sem esperar.

Se tabelas específicas forem mencionadas em uma cláusula de bloqueio, apenas as linhas provenientes dessas tabelas serão bloqueadas; quaisquer outras tabelas utilizadas no `SELECT` serão simplesmente lidas como de costume. Uma cláusula de bloqueio sem uma lista de tabelas afeta todas as tabelas utilizadas na declaração. Se uma cláusula de bloqueio for aplicada a uma visão ou sub-consulta, ela afeta todas as tabelas utilizadas na visão ou sub-consulta. No entanto, essas cláusulas não se aplicam às consultas `WITH` referenciadas pela consulta primária. Se você deseja que o bloqueio de linha ocorra em uma consulta `WITH`, especifique uma cláusula de bloqueio na consulta `WITH`.

Pode-se escrever várias cláusulas de bloqueio se for necessário especificar um comportamento de bloqueio diferente para diferentes tabelas. Se a mesma tabela for mencionada (ou implicitamente afetada) por mais de uma cláusula de bloqueio, ela é processada como se fosse apenas especificada pela mais forte. Da mesma forma, uma tabela é processada como `NOWAIT` se isso for especificado em qualquer uma das cláusulas que a afetam. Caso contrário, ela é processada como `SKIP LOCKED` se isso for especificado em qualquer uma das cláusulas que a afetam.

As cláusulas de bloqueio não podem ser usadas em contextos onde as linhas retornadas não podem ser identificadas claramente com linhas individuais da tabela; por exemplo, não podem ser usadas com agregação.

Quando uma cláusula de bloqueio aparece no nível superior de uma consulta `SELECT`, as linhas que estão bloqueadas são exatamente aquelas que são devolvidas pela consulta; no caso de uma consulta de junção, as linhas bloqueadas são as que contribuem para as linhas de junção devolvidas. Além disso, as linhas que atenderam às condições da consulta no momento do instantâneo da consulta serão bloqueadas, embora não sejam devolvidas se foram atualizadas após o instantâneo e não atendem mais às condições da consulta. Se um `LIMIT` for usado, o bloqueio para quando o número suficiente de linhas é devolvido para satisfazer o limite (mas note que as linhas ignoradas por `OFFSET` serão bloqueadas). Da mesma forma, se uma cláusula de bloqueio for usada em uma consulta de cursor, apenas as linhas que foram efetivamente obtidas ou ignoradas pelo cursor serão bloqueadas.

Quando uma cláusula de bloqueio aparece em um sub`SELECT`, as linhas bloqueadas são aquelas devolvidas à consulta externa pela subconsulta. Isso pode envolver menos linhas do que a inspeção da subconsulta sozinha sugereria, uma vez que as condições da consulta externa podem ser usadas para otimizar a execução da subconsulta. Por exemplo,

```
SELECT * FROM (SELECT * FROM mytable FOR UPDATE) ss WHERE col1 = 5;
```

bloqueará apenas as linhas que possuem `col1 = 5`, mesmo que essa condição não esteja tecnicamente dentro da subconsulta.

As versões anteriores não conseguiram preservar uma chave que é atualizada por um ponto de salvamento posterior. Por exemplo, este código:

```
BEGIN;
SELECT * FROM mytable WHERE key = 1 FOR UPDATE;
SAVEPOINT s;
UPDATE mytable SET ... WHERE key = 1;
ROLLBACK TO s;
```

não conseguiria preservar o bloqueio `FOR UPDATE` após o `ROLLBACK TO`. Isso foi corrigido na versão 9.3.

### Atenção

É possível que um comando `SELECT` que está sendo executado no nível de isolamento de transação `READ COMMITTED` e usando `ORDER BY` e uma cláusula de bloqueio retorne linhas fora de ordem. Isso ocorre porque o `ORDER BY` é aplicado primeiro. O comando ordena o resultado, mas pode então bloquear ao tentar obter um bloqueio em uma ou mais das linhas. Uma vez que o `SELECT` desbloqueia, alguns dos valores das colunas de ordenação podem ter sido modificados, levando essas linhas a parecerem fora de ordem (embora estejam em ordem em termos dos valores originais das colunas). Isso pode ser contornado conforme necessário, colocando a cláusula `FOR UPDATE/SHARE` em uma sub-consulta, por exemplo.

```
SELECT * FROM (SELECT * FROM mytable FOR UPDATE) ss ORDER BY column1;
```

Observe que isso resultará no bloqueio de todas as linhas de `mytable`, enquanto `FOR UPDATE` no nível superior bloquearia apenas as linhas realmente retornadas. Isso pode resultar em uma diferença significativa de desempenho, especialmente se o `ORDER BY` for combinado com `LIMIT` ou outras restrições. Portanto, essa técnica é recomendada apenas se houver atualizações concorrentes das colunas de ordenação e for necessário um resultado estritamente ordenado.

No nível de isolamento de transação `REPEATABLE READ` ou `SERIALIZABLE`, isso causaria um erro de serialização (com um `SQLSTATE` de `'40001'`), portanto, não há possibilidade de receber linhas fora de ordem nesses níveis de isolamento.

### `TABLE` Comando

O comando

```
TABLE name
```

é equivalente a

```
SELECT * FROM name
```

Ele pode ser usado como um comando de nível superior ou como uma variante de sintaxe que economiza espaço em partes de consultas complexas. Apenas as cláusulas de bloqueio `WITH`, `UNION`, `INTERSECT`, `EXCEPT`, `ORDER BY`, `LIMIT`, `OFFSET`, `FETCH` e `FOR` podem ser usadas com `TABLE`; a cláusula `WHERE` e qualquer forma de agregação não podem ser usadas.

## Exemplos

Para se juntar à tabela `films` com a tabela `distributors`:

```
SELECT f.title, f.did, d.name, f.date_prod, f.kind
    FROM distributors d JOIN films f USING (did);

       title       | did |     name     | date_prod  |   kind
-------------------+-----+--------------+------------+----------
 The Third Man     | 101 | British Lion | 1949-12-23 | Drama
 The African Queen | 101 | British Lion | 1951-08-11 | Romantic
 ...
```

Para somar a coluna `len` de todos os filmes e agrupar os resultados por `kind`:

```
SELECT kind, sum(len) AS total FROM films GROUP BY kind;

   kind   | total
----------+-------
 Action   | 07:34
 Comedy   | 02:58
 Drama    | 14:28
 Musical  | 06:42
 Romantic | 04:38
```

Para somar a coluna `len` de todos os filmes, agrupe os resultados por `kind` e mostre os totais dos grupos que são menos de 5 horas:

```
SELECT kind, sum(len) AS total
    FROM films
    GROUP BY kind
    HAVING sum(len) < interval '5 hours';

   kind   | total
----------+-------
 Comedy   | 02:58
 Romantic | 04:38
```

Os dois exemplos a seguir são formas idênticas de ordenar os resultados individuais de acordo com o conteúdo da segunda coluna (`name`):

```
SELECT * FROM distributors ORDER BY name;
SELECT * FROM distributors ORDER BY 2;

 did |       name
-----+------------------
 109 | 20th Century Fox
 110 | Bavaria Atelier
 101 | British Lion
 107 | Columbia
 102 | Jean Luc Godard
 113 | Luso films
 104 | Mosfilm
 103 | Paramount
 106 | Toho
 105 | United Artists
 111 | Walt Disney
 112 | Warner Bros.
 108 | Westward
```

O próximo exemplo mostra como obter a união das tabelas `distributors` e `actors`, restringindo os resultados aos que começam com a letra W em cada tabela. Apenas as linhas distintas são desejadas, portanto, a palavra-chave `ALL` é omitida.

```
distributors:               actors:
 did |     name              id |     name
-----+--------------        ----+----------------
 108 | Westward               1 | Woody Allen
 111 | Walt Disney            2 | Warren Beatty
 112 | Warner Bros.           3 | Walter Matthau
 ...                         ...

SELECT distributors.name
    FROM distributors
    WHERE distributors.name LIKE 'W%'
UNION
SELECT actors.name
    FROM actors
    WHERE actors.name LIKE 'W%';

      name
----------------
 Walt Disney
 Walter Matthau
 Warner Bros.
 Warren Beatty
 Westward
 Woody Allen
```

Este exemplo mostra como usar uma função na cláusula `FROM`, tanto com uma lista de definição de coluna quanto sem ela:

```
CREATE FUNCTION distributors(int) RETURNS SETOF distributors AS $$
    SELECT * FROM distributors WHERE did = $1;
$$ LANGUAGE SQL;

SELECT * FROM distributors(111);
 did |    name
-----+-------------
 111 | Walt Disney

CREATE FUNCTION distributors_2(int) RETURNS SETOF record AS $$
    SELECT * FROM distributors WHERE did = $1;
$$ LANGUAGE SQL;

SELECT * FROM distributors_2(111) AS (f1 int, f2 text);
 f1  |     f2
-----+-------------
 111 | Walt Disney
```

Aqui está um exemplo de uma função com uma coluna de ordinalidade adicionada:

```
SELECT * FROM unnest(ARRAY['a','b','c','d','e','f']) WITH ORDINALITY;
 unnest | ordinality
--------+----------
 a      |        1
 b      |        2
 c      |        3
 d      |        4
 e      |        5
 f      |        6
(6 rows)
```

Este exemplo mostra como usar uma cláusula simples `WITH`:

```
WITH t AS (
    SELECT random() as x FROM generate_series(1, 3)
  )
SELECT * FROM t
UNION ALL
SELECT * FROM t;
         x
--------------------
  0.534150459803641
  0.520092216785997
 0.0735620250925422
  0.534150459803641
  0.520092216785997
 0.0735620250925422
```

Observe que a consulta `WITH` foi avaliada apenas uma vez, de modo que obtivemos dois conjuntos dos mesmos três valores aleatórios.

Este exemplo usa `WITH RECURSIVE` para encontrar todos os subordinados (diretos ou indiretos) do funcionário Mary, e seu nível de indireção, a partir de uma tabela que mostra apenas subordinados diretos:

```
WITH RECURSIVE employee_recursive(distance, employee_name, manager_name) AS (
    SELECT 1, employee_name, manager_name
    FROM employee
    WHERE manager_name = 'Mary'
  UNION ALL
    SELECT er.distance + 1, e.employee_name, e.manager_name
    FROM employee_recursive er, employee e
    WHERE er.employee_name = e.manager_name
  )
SELECT distance, employee_name FROM employee_recursive;
```

Observe a forma típica de consultas recursivas: uma condição inicial, seguida de `UNION`, seguida pela parte recursiva da consulta. Certifique-se de que a parte recursiva da consulta eventualmente retorne nenhum tuplo, caso contrário, a consulta entrará em um loop indefinidamente. (Veja [Seção 7.8](queries-with.md) para mais exemplos.)

Este exemplo usa `LATERAL` para aplicar uma função de conjunto `get_product_names()` para cada linha da tabela `manufacturers`:

```
SELECT m.name AS mname, pname
FROM manufacturers m, LATERAL get_product_names(m.id) pname;
```

Os fabricantes que atualmente não têm nenhum produto não aparecerão no resultado, pois é uma junção interna. Se quiséssemos incluir os nomes desses fabricantes no resultado, poderíamos fazer:

```
SELECT m.name AS mname, pname
FROM manufacturers m LEFT JOIN LATERAL get_product_names(m.id) pname ON true;
```

## Compatibilidade

Claro, a declaração `SELECT` é compatível com o padrão SQL. Mas há algumas extensões e alguns recursos ausentes.

### Cláusulas omitidas `FROM`

O PostgreSQL permite omitir a cláusula `FROM`. Tem um uso direto para calcular os resultados de expressões simples:

```
SELECT 2+2;

 ?column?
----------
        4
```

Alguns outros bancos de dados SQL não podem fazer isso, exceto introduzindo uma tabela de uma única linha fictícia a partir da qual se pode realizar o `SELECT`.

### Listas vazias `SELECT`

A lista de expressões de saída após `SELECT` pode ser vazia, produzindo uma tabela de resultados com uma coluna em branco. Isso não é sintaxe válida de acordo com o padrão SQL. O PostgreSQL permite que seja consistente ao permitir tabelas com uma coluna em branco. No entanto, uma lista vazia não é permitida quando `DISTINCT` é usado.

### Omitindo a palavra-chave `AS`

No padrão SQL, a palavra-chave opcional `AS` pode ser omitida antes de um nome de coluna de saída sempre que o novo nome de coluna é um nome de coluna válido (ou seja, não é o mesmo que qualquer palavra-chave reservada). O PostgreSQL é um pouco mais restritivo: `AS` é necessário se o novo nome de coluna corresponder a qualquer palavra-chave, reservada ou não. A prática recomendada é usar `AS` ou nomes de colunas de saída com aspas duplas, para evitar qualquer possível conflito contra futuras adições de palavras-chave.

Nos itens `FROM`, tanto o padrão quanto o PostgreSQL permitem que `AS` seja omitido antes de um alias que seja uma palavra-chave não reservada. Mas isso é impraticável para os nomes de colunas de saída, devido a ambiguidades sintáticas.

### Omissão de Sub-`SELECT` Alias em `FROM`

De acordo com o padrão SQL, um sub`SELECT` na lista `FROM` deve ter um alias. No PostgreSQL, esse alias pode ser omitido.

### `ONLY` e Herança

O padrão SQL exige parênteses ao redor do nome da tabela ao escrever `ONLY`, por exemplo `SELECT * FROM ONLY (tab1), ONLY (tab2) WHERE ...`. O PostgreSQL considera esses parênteses como opcionais.

O PostgreSQL permite que um `*` seja escrito no final para especificar explicitamente o comportamento não `ONLY` de incluir tabelas de filhos. O padrão não permite isso.

(Esses pontos se aplicam igualmente a todos os comandos SQL que suportam a opção `ONLY`.

### `TABLESAMPLE` Restrições de cláusula

A cláusula `TABLESAMPLE` é atualmente aceita apenas em tabelas regulares e visualizações materializadas. De acordo com o padrão SQL, ela deve ser possível aplicá-la a qualquer item `FROM`.

### Chamadas de função em `FROM`

O PostgreSQL permite que uma chamada de função seja escrita diretamente como um membro da lista `FROM`. No padrão SQL, seria necessário envolver tal chamada de função em um sub-`SELECT`; ou seja, a sintaxe `FROM func(...) alias` é aproximadamente equivalente a `FROM LATERAL (SELECT func(...)) alias`. Note que `LATERAL` é considerado implícito; isso ocorre porque o padrão exige a semântica `LATERAL` para um item `UNNEST()` em `FROM`. O PostgreSQL trata `UNNEST()` da mesma forma que outras funções que retornam um conjunto.

### Namespace Disponível para `GROUP BY` e `ORDER BY`

No padrão SQL-92, uma cláusula `ORDER BY` só pode usar nomes ou números de colunas de saída, enquanto uma cláusula `GROUP BY` só pode usar expressões baseadas em nomes de colunas de entrada. O PostgreSQL estende cada uma dessas cláusulas para permitir a outra opção também (mas usa a interpretação do padrão se houver ambiguidade). O PostgreSQL também permite que ambas as cláusulas especifiquem expressões arbitrárias. Note que os nomes que aparecem em uma expressão serão sempre tomados como nomes de colunas de entrada, não como nomes de colunas de saída.

SQL:1999 e as versões posteriores utilizam uma definição ligeiramente diferente, que não é totalmente compatível com o SQL-92. Na maioria dos casos, no entanto, o PostgreSQL interpretará uma expressão `ORDER BY` ou `GROUP BY` da mesma maneira que o SQL:1999.

### Dependências Funcionais

O PostgreSQL reconhece a dependência funcional (permitindo que as colunas sejam omitidas em `GROUP BY`) apenas quando a chave primária de uma tabela está incluída na lista em `GROUP BY`. O padrão SQL especifica condições adicionais que devem ser reconhecidas.

### `LIMIT` e `OFFSET`

As cláusulas `LIMIT` e `OFFSET` são sintaxes específicas do PostgreSQL, também utilizadas pelo MySQL. O padrão SQL:2008 introduziu as cláusulas `OFFSET ... FETCH {FIRST|NEXT} ...` para a mesma funcionalidade, conforme mostrado acima em [Cláusula LIMIT](sql-select.md#SQL-LIMIT "LIMIT Clause"). Essa sintaxe também é utilizada pelo IBM DB2. (Aplicações escritas para Oracle frequentemente utilizam uma solução envolvendo a coluna automaticamente gerada `rownum`, que não está disponível no PostgreSQL, para implementar os efeitos dessas cláusulas.)

### `FOR NO KEY UPDATE`, `FOR UPDATE`, `FOR SHARE`, `FOR KEY SHARE`

Embora `FOR UPDATE` apareça no padrão SQL, o padrão permite que ele seja usado apenas como uma opção de `DECLARE CURSOR`. O PostgreSQL permite que ele seja usado em qualquer consulta de `SELECT`, bem como em sub-`SELECT`, mas essa é uma extensão. As variantes de `FOR NO KEY UPDATE`, `FOR SHARE` e `FOR KEY SHARE`, bem como as opções de `NOWAIT` e `SKIP LOCKED`, não aparecem no padrão.

### Declarações que modificam dados em `WITH`

O PostgreSQL permite que `INSERT`, `UPDATE`, `DELETE` e `MERGE` sejam usados como consultas `WITH`. Isso não é encontrado no padrão SQL.

### Cláusulas Não Padronizadas

`DISTINCT ON ( ... )` é uma extensão do padrão SQL.

`ROWS FROM( ... )` é uma extensão do padrão SQL.

As opções `MATERIALIZED` e `NOT MATERIALIZED` do `WITH` são extensões do padrão SQL.