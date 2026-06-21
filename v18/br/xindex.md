## 36.16. Interconexão de extensões a índices [#](#XINDEX)

* [36.16.1. Métodos de índice e classes de operadores](xindex.md#XINDEX-OPCLASS)
* [36.16.2. Estratégias de métodos de índice](xindex.md#XINDEX-STRATEGIES)
* [36.16.3. Rotinas de suporte a métodos de índice](xindex.md#XINDEX-SUPPORT)
* [36.16.4. Um exemplo](xindex.md#XINDEX-EXAMPLE)
* [36.16.5. Classes de operadores e famílias de operadores](xindex.md#XINDEX-OPFAMILY)
* [36.16.6. Dependências do sistema em relação a classes de operadores](xindex.md#XINDEX-OPCLASS-DEPENDENCIES)
* [36.16.7. Ordem dos operadores](xindex.md#XINDEX-ORDERING-OPS)
* [36.16.8. Características especiais das classes de operadores](xindex.md#XINDEX-OPCLASS-FEATURES)

Os procedimentos descritos até agora permitem definir novos tipos, funções e operadores. No entanto, ainda não podemos definir um índice em uma coluna de um novo tipo de dados. Para fazer isso, devemos definir uma *classe de operador* para o novo tipo de dados. Mais tarde nesta seção, ilustraremos esse conceito em um exemplo: uma nova classe de operador para o método de índice de árvore B que armazena e ordena números complexos em ordem de valor absoluto ascendente.

As classes de operador podem ser agrupadas em *famílias de operadores* para mostrar as relações entre classes semanticamente compatíveis. Quando apenas um único tipo de dado está envolvido, uma classe de operador é suficiente, então vamos focar nesse caso primeiro e depois voltar às famílias de operadores.

### 36.16.1. Métodos de índice e classes de operador [#](#XINDEX-OPCLASS)

As classes de operador estão associadas a um método de acesso a índice, como [B-Tree](btree.md "65.1. B-Tree Indexes") ou [GIN](gin.md "65.4. GIN Indexes"). Um método de acesso a índice personalizado pode ser definido com [CREATE ACCESS METHOD](sql-create-access-method.md "CREATE ACCESS METHOD"). Consulte [Capítulo 63](indexam.md "Chapter 63. Index Access Method Interface Definition") para obter detalhes.

As rotinas de um método de índice não sabem diretamente sobre os tipos de dados sobre os quais o método de índice operará. Em vez disso, uma *classe de operador* identifica o conjunto de operações que o método de índice precisa usar para trabalhar com um tipo de dados particular. As classes de operador são chamadas assim porque uma das coisas que elas especificam é o conjunto de operadores da cláusula `WHERE` que podem ser usados com um índice (ou seja, que podem ser convertidos em uma qualificação de varredura de índice). Uma classe de operador também pode especificar algumas *funções de suporte* que são necessárias pelas operações internas do método de índice, mas que não correspondem diretamente a nenhum operador da cláusula `WHERE` que pode ser usado com o índice.

É possível definir múltiplas classes de operador para o mesmo tipo de dados e método de índice. Ao fazer isso, é possível definir múltiplos conjuntos de semântica de indexação para um único tipo de dados. Por exemplo, um índice de árvore B requer que uma ordem de classificação seja definida para cada tipo de dados sobre o qual ele funciona. Pode ser útil para um tipo de dados de número complexo ter uma classe de operador B-tree que classifique os dados pelo valor absoluto complexo, outra que classifique pelo real, e assim por diante. Tipicamente, uma das classes de operador será considerada a mais comumente útil e será marcada como a classe de operador padrão para esse tipo de dados e método de índice.

O mesmo nome de classe de operador pode ser usado para vários métodos de índice diferentes (por exemplo, tanto os métodos de índice B-tree quanto os de índice de hash têm classes de operador com o nome `int4_ops`, mas cada uma dessas classes é uma entidade independente e deve ser definida separadamente.

### 36.16.2. Estratégias de Método de Índice [#](#XINDEX-STRATEGIES)

Os operadores associados a uma classe de operadores são identificados por “números de estratégia”, que servem para identificar a semântica de cada operador no contexto de sua classe de operadores. Por exemplo, as árvores B impõem uma ordem estrita sobre as chaves, menor para maior, e, portanto, operadores como “menor que” e “maior que ou igual a” são interessantes em relação a uma árvore B. Como o PostgreSQL permite que o usuário defina operadores, o PostgreSQL não pode olhar para o nome de um operador (por exemplo, `<` ou `>=`) e dizer que tipo de comparação é. Em vez disso, o método de índice define um conjunto de “estratégias”, que podem ser consideradas como operadores generalizados. Cada classe de operador especifica qual operador real corresponde a cada estratégia para um tipo de dados particular e interpretação da semântica do índice.

O método de índice de árvore B define cinco estratégias, mostradas na Tabela 36.3 ((xindex.md#XINDEX-BTREE-STRAT-TABLE "Table 36.3. B-Tree Strategies")).

**Tabela 36.3. Estratégias de Árvores B**



<table border="1" class="table" summary="B-Tree Strategies">
<colgroup>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>
    Operation
   </th>
<th>
    Strategy Number
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>
    less than
   </td>
<td>
    1
   </td>
</tr>
<tr>
<td>
    less than or equal
   </td>
<td>
    2
   </td>
</tr>
<tr>
<td>
    equal
   </td>
<td>
    3
   </td>
</tr>
<tr>
<td>
    greater than or equal
   </td>
<td>
    4
   </td>
</tr>
<tr>
<td>
    greater than
   </td>
<td>
    5
   </td>
</tr>
</tbody>
</table>




  

Os índices de hash só suportam comparações de igualdade, e, portanto, usam apenas uma estratégia, mostrada em [Tabela 36.4][(xindex.md#XINDEX-HASH-STRAT-TABLE "Table 36.4. Hash Strategies")].

**Tabela 36.4. Estratégias de Hash**



<table border="1" class="table" summary="Hash Strategies">
<colgroup>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>
    Operation
   </th>
<th>
    Strategy Number
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>
    equal
   </td>
<td>
    1
   </td>
</tr>
</tbody>
</table>




  

Os índices GiST são mais flexíveis: não possuem um conjunto fixo de estratégias. Em vez disso, a rotina de suporte à “consistência” de cada classe específica de operadores GiST interpreta os números de estratégia da maneira que bem entender. Como exemplo, várias das classes de operadores de índice GiST embutidos indexam objetos geométricos bidimensionais, fornecendo as estratégias de “R-tree” mostradas em [Tabela 36.5] ((xindex.md#XINDEX-RTREE-STRAT-TABLE "Table 36.5. GiST Two-Dimensional “R-tree” Strategies")). Quatro dessas são testes verdadeiramente bidimensionais (sobreposição, mesmo, contém, contido por); quatro delas consideram apenas a direção X; e as outras quatro fornecem os mesmos testes na direção Y.

**Tabela 36.5. Estratégias de GiST bidimensional “R-tree”**



<table border="1" class="table" summary="GiST Two-Dimensional R-tree Strategies">
<colgroup>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>Operação</th>
<th>
    Strategy Number
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>estranhamente à esquerda</td>
<td>
    1
   </td>
</tr>
<tr>
<td>não se estende ao direito de</td>
<td>
    2
   </td>
</tr>
<tr>
<td>sobreposição</td>
<td>
    3
   </td>
</tr>
<tr>
<td>não se estende à esquerda de</td>
<td>
    4
   </td>
</tr>
<tr>
<td>direito estritamente direito</td>
<td>
    5
   </td>
</tr>
<tr>
<td>mesmo</td>
<td>
    6
   </td>
</tr>
<tr>
<td>contem</td>
<td>
    7
   </td>
</tr>
<tr>
<td>contenida por</td>
<td>
    8
   </td>
</tr>
<tr>
<td>não se estende acima</td>
<td>
    9
   </td>
</tr>
<tr>
<td>estreitamente abaixo</td>
<td>
    10
   </td>
</tr>
<tr>
<td>absolutamente acima</td>
<td>
    11
   </td>
</tr>
<tr>
<td>não se estende abaixo</td>
<td>
    12
   </td>
</tr>
</tbody>
</table>




  

Os índices SP-GiST são semelhantes aos índices GiST em termos de flexibilidade: eles não têm um conjunto fixo de estratégias. Em vez disso, as rotinas de suporte de cada classe de operador interpretam os números de estratégia de acordo com a definição da classe de operador. Como exemplo, os números de estratégia usados pelas classes de operadores embutidas para pontos são mostrados na [Tabela 36.6] [(xindex.md#XINDEX-SPGIST-POINT-STRAT-TABLE "Table 36.6. SP-GiST Point Strategies")].

**Tabela 36.6. Estratégias de Pontos SP-GiST**



<table border="1" class="table" summary="SP-GiST Point Strategies">
<colgroup>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>
    Operation
   </th>
<th>
    Strategy Number
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>
    strictly left of
   </td>
<td>
    1
   </td>
</tr>
<tr>
<td>
    strictly right of
   </td>
<td>
    5
   </td>
</tr>
<tr>
<td>
    same
   </td>
<td>
    6
   </td>
</tr>
<tr>
<td>
    contained by
   </td>
<td>
    8
   </td>
</tr>
<tr>
<td>
    strictly below
   </td>
<td>
    10
   </td>
</tr>
<tr>
<td>
    strictly above
   </td>
<td>
    11
   </td>
</tr>
</tbody>
</table>




  

Os índices GIN são semelhantes aos índices GiST e SP-GiST, na medida em que também não possuem um conjunto fixo de estratégias. Em vez disso, as rotinas de suporte de cada classe de operador interpretam os números de estratégia de acordo com a definição da classe de operador. Como exemplo, os números de estratégia usados pela classe de operadores embutida para arrays são mostrados em [Tabela 36.7] [(xindex.md#XINDEX-GIN-ARRAY-STRAT-TABLE "Table 36.7. GIN Array Strategies")].

**Tabela 36.7. Estratégias do Array GIN**



<table border="1" class="table" summary="GIN Array Strategies">
<colgroup>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>
    Operation
   </th>
<th>
    Strategy Number
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>
    overlap
   </td>
<td>
    1
   </td>
</tr>
<tr>
<td>
    contains
   </td>
<td>
    2
   </td>
</tr>
<tr>
<td>
    is contained by
   </td>
<td>
    3
   </td>
</tr>
<tr>
<td>
    equal
   </td>
<td>
    4
   </td>
</tr>
</tbody>
</table>




  

Os índices BRIN são semelhantes aos índices GiST, SP-GiST e GIN, pois também não possuem um conjunto fixo de estratégias. Em vez disso, as rotinas de suporte de cada classe de operador interpretam os números de estratégia de acordo com a definição da classe de operador. Como exemplo, os números de estratégia usados pelas classes de operador embutidas `Minmax` são mostrados em [Tabela 36.8][(xindex.md#XINDEX-BRIN-MINMAX-STRAT-TABLE "Table 36.8. BRIN Minmax Strategies")].

**Tabela 36.8. Estratégias BRIN Minmax**



<table border="1" class="table" summary="BRIN Minmax Strategies">
<colgroup>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>
    Operation
   </th>
<th>
    Strategy Number
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>
    less than
   </td>
<td>
    1
   </td>
</tr>
<tr>
<td>
    less than or equal
   </td>
<td>
    2
   </td>
</tr>
<tr>
<td>
    equal
   </td>
<td>
    3
   </td>
</tr>
<tr>
<td>
    greater than or equal
   </td>
<td>
    4
   </td>
</tr>
<tr>
<td>
    greater than
   </td>
<td>
    5
   </td>
</tr>
</tbody>
</table>




  

Observe que todos os operadores listados acima retornam valores booleanos. Na prática, todos os operadores definidos como operadores de pesquisa de método de índice devem retornar o tipo `boolean`, uma vez que devem aparecer no nível superior de uma cláusula `WHERE` para serem usados com um índice. (Alguns métodos de acesso a índices também suportam operadores de *ordem*, que normalmente não retornam valores booleanos; essa característica é discutida em [Seção 36.16.7][(xindex.md#XINDEX-ORDERING-OPS "36.16.7. Ordering Operators")].

### 36.16.3. Rotinas de suporte ao método de índice [#](#XINDEX-SUPPORT)

As estratégias geralmente não são informações suficientes para o sistema descobrir como usar um índice. Na prática, os métodos de índice requerem rotinas de suporte adicionais para funcionar. Por exemplo, o método de índice B-tree deve ser capaz de comparar duas chaves e determinar se uma é maior, igual ou menor que a outra. Da mesma forma, o método de índice de hash deve ser capaz de calcular códigos de hash para valores de chave. Essas operações não correspondem a operadores usados em qualificações em comandos SQL; são rotinas administrativas usadas internamente pelos métodos de índice.

Assim como nas estratégias, a classe de operador identifica quais funções específicas devem desempenhar cada um desses papéis para um determinado tipo de dados e interpretação semântica. O método de índice define o conjunto de funções que ele precisa, e a classe de operador identifica as funções corretas a serem usadas, atribuindo-as aos "números de funções de suporte" especificados pelo método de índice.

Além disso, algumas classes de operações permitem que os usuários especifiquem parâmetros que controlam seu comportamento. Cada método de acesso a índice embutido tem uma função de suporte opcional `options`, que define um conjunto de parâmetros específicos da classe de operações.

As árvores B requerem uma função de suporte para comparações e permitem que quatro funções de suporte adicionais sejam fornecidas, conforme opção do autor da classe de operador, conforme mostrado na [Tabela 36.9][(xindex.md#XINDEX-BTREE-SUPPORT-TABLE "Table 36.9. B-Tree Support Functions")]. Os requisitos para essas funções de suporte são explicados mais detalhadamente na [Seção 65.1.3][(btree.md#BTREE-SUPPORT-FUNCS "65.1.3. B-Tree Support Functions")].

**Tabela 36.9. Funções de suporte de árvore B**



<table border="1" class="table" summary="B-Tree Support Functions">
<colgroup>
<col class="col1"/>
<col class="col2"/>
</colgroup>
<thead>
<tr>
<th>Função</th>
<th>
    Support Number
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>Compare duas chaves e retorne um número inteiro menor que zero, zero ou maior que zero, indicando se a primeira chave é menor que, igual a ou maior que a segunda.</td>
<td>
    1
   </td>
</tr>
<tr>
<td>Retorne os endereços das funções de suporte de classificação C-callable (opcional)</td>
<td>
    2
   </td>
</tr>
<tr>
<td>Compare um valor de teste a um valor de base mais/menos um deslocamento e retorne verdadeiro ou falso de acordo com o resultado da comparação (opcional)</td>
<td>
    3
   </td>
</tr>
<tr>
<td>Determine se é seguro para índices que utilizam a classe do operador aplicar a otimização de deduplicação btree (opcional)</td>
<td>
    4
   </td>
</tr>
<tr>
<td>Defina opções específicas para essa classe de operador (opcional)</td>
<td>
    5
   </td>
</tr>
<tr>
<td>Retorne os endereços das funções de suporte de salto C-callable (opcional)</td>
<td>
    6
   </td>
</tr>
</tbody>
</table>




  

Os índices hash exigem uma função de suporte e permitem que duas outras sejam fornecidas, conforme opção do autor da classe de operador, conforme mostrado na [Tabela 36.10] [(xindex.md#XINDEX-HASH-SUPPORT-TABLE "Table 36.10. Hash Support Functions")].

**Tabela 36.10. Funções de suporte de hash**



<table border="1" class="table" summary="Hash Support Functions">
<colgroup>
<col class="col1"/>
<col class="col2"/>
</colgroup>
<thead>
<tr>
<th>Função</th>
<th>
    Support Number
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>Calcule o valor de hash de 32 bits para uma chave</td>
<td>
    1
   </td>
</tr>
<tr>
<td>Calcule o valor de hash de 64 bits para uma chave dada uma sal de 64 bits; se o sal for 0, os 32 bits baixos do resultado devem corresponder ao valor que teria sido calculado pela função 1 (opcional)</td>
<td>
    2
   </td>
</tr>
<tr>
<td>Defina opções específicas para essa classe de operador (opcional)</td>
<td>
    3
   </td>
</tr>
</tbody>
</table>




  

Os índices GiST têm doze funções de suporte, das quais sete são opcionais, conforme mostrado na Tabela 36.11 ((xindex.md#XINDEX-GIST-SUPPORT-TABLE "Table 36.11. GiST Support Functions")). (Para mais informações, consulte a Seção 65.2 ((gist.md "65.2. GiST Indexes"))).

**Tabela 36.11. Funções de Suporte GiST**



<table border="1" class="table" summary="GiST Support Functions">
<colgroup>
<col class="col1"/>
<col class="col2"/>
<col class="col3"/>
</colgroup>
<thead>
<tr>
<th>
    Function
   </th>
<th>Descrição</th>
<th>
    Support Number
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="function">
     consistent
    </code>
</td>
<td>determine se a chave atende ao qualificador da consulta</td>
<td>
    1
   </td>
</tr>
<tr>
<td>
<code class="function">
     union
    </code>
</td>
<td>calcular a união de um conjunto de chaves</td>
<td>
    2
   </td>
</tr>
<tr>
<td>
<code class="function">
     compress
    </code>
</td>
<td>calcular uma representação comprimida de uma chave ou valor a ser indexado (opcional)</td>
<td>
    3
   </td>
</tr>
<tr>
<td>
<code class="function">
     decompress
    </code>
</td>
<td>calcular uma representação descomprimida de uma chave comprimida (opcional)</td>
<td>
    4
   </td>
</tr>
<tr>
<td>
<code class="function">
     penalty
    </code>
</td>
<td>calcular penalidade por inserir uma nova chave em uma subárvore com a chave da subárvore dada</td>
<td>
    5
   </td>
</tr>
<tr>
<td>
<code class="function">
     picksplit
    </code>
</td>
<td>determinar quais entradas de uma página devem ser movidas para a nova página e calcular as chaves de união para as páginas resultantes</td>
<td>
    6
   </td>
</tr>
<tr>
<td>
<code class="function">
     same
    </code>
</td>
<td>comparar duas chaves e retornar verdadeiro se elas forem iguais</td>
<td>
    7
   </td>
</tr>
<tr>
<td>
<code class="function">
     distance
    </code>
</td>
<td>determinar a distância entre a chave e o valor da consulta (opcional)</td>
<td>
    8
   </td>
</tr>
<tr>
<td>
<code class="function">
     fetch
    </code>
</td>
<td>calcular a representação original de uma chave comprimida para varreduras apenas de índice (opcional)</td>
<td>
    9
   </td>
</tr>
<tr>
<td>
<code class="function">
     options
    </code>
</td>
<td>defina opções que sejam específicas para essa classe de operador (opcional)</td>
<td>
    10
   </td>
</tr>
<tr>
<td>
<code class="function">
     sortsupport
    </code>
</td>
<td>fornecer um comparador de classificação para ser usado em construções de índice rápidas (opcional)</td>
<td>
    11
   </td>
</tr>
<tr>
<td>
<code class="function">
     translate_cmptype
    </code>
</td>
<td>traduzir comparar tipos para números de estratégia utilizados pela classe de operador (opcional)</td>
<td>
    12
   </td>
</tr>
</tbody>
</table>




  

Os índices SP-GiST têm seis funções de suporte, uma das quais é opcional, conforme mostrado na Tabela 36.12 ((xindex.md#XINDEX-SPGIST-SUPPORT-TABLE "Table 36.12. SP-GiST Support Functions")). (Para mais informações, consulte a Seção 65.3 ((spgist.md "65.3. SP-GiST Indexes"))).

**Tabela 36.12. Funções de Suporte SP-GiST**



<table border="1" class="table" summary="SP-GiST Support Functions">
<colgroup>
<col class="col1"/>
<col class="col2"/>
<col class="col3"/>
</colgroup>
<thead>
<tr>
<th>
    Function
   </th>
<th>Descrição</th>
<th>
    Support Number
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="function">
     config
    </code>
</td>
<td>fornecer informações básicas sobre a classe do operador</td>
<td>
    1
   </td>
</tr>
<tr>
<td>
<code class="function">
     choose
    </code>
</td>
<td>determine como inserir um novo valor em um par ordenado interno</td>
<td>
    2
   </td>
</tr>
<tr>
<td>
<code class="function">
     picksplit
    </code>
</td>
<td>determine como particionar um conjunto de valores</td>
<td>
    3
   </td>
</tr>
<tr>
<td>
<code class="function">
     inner_consistent
    </code>
</td>
<td>determine quais subpartições precisam ser pesquisadas para uma consulta</td>
<td>
    4
   </td>
</tr>
<tr>
<td>
<code class="function">
     leaf_consistent
    </code>
</td>
<td>determinar se a chave atende ao qualificador da consulta</td>
<td>
    5
   </td>
</tr>
<tr>
<td>
<code class="function">
     options
    </code>
</td>
<td>defina opções que sejam específicas para essa classe de operador (opcional)</td>
<td>
    6
   </td>
</tr>
</tbody>
</table>




  

Os índices GIN têm sete funções de suporte, quatro das quais são opcionais, conforme mostrado na Tabela 36.13 ((xindex.md#XINDEX-GIN-SUPPORT-TABLE "Table 36.13. GIN Support Functions")). (Para mais informações, consulte a Seção 65.4 ((gin.md "65.4. GIN Indexes"))).

**Tabela 36.13. Funções de Suporte GIN**



<table border="1" class="table" summary="GIN Support Functions">
<colgroup>
<col class="col1"/>
<col class="col2"/>
<col class="col3"/>
</colgroup>
<thead>
<tr>
<th>
    Function
   </th>
<th>Descrição</th>
<th>
    Support Number
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="function">
     compare
    </code>
</td>
<td>comparar duas chaves e retornar um número inteiro menor que zero, zero ou maior que zero, indicando se a primeira chave é menor que, igual a ou maior que a segunda</td>
<td>
    1
   </td>
</tr>
<tr>
<td>
<code class="function">
     extractValue
    </code>
</td>
<td>extrair chaves de um valor a ser indexado</td>
<td>
    2
   </td>
</tr>
<tr>
<td>
<code class="function">
     extractQuery
    </code>
</td>
<td>extrair chaves de uma condição de consulta</td>
<td>
    3
   </td>
</tr>
<tr>
<td>
<code class="function">
     consistent
    </code>
</td>
<td>determinar se o valor corresponde à condição da consulta (variante booleana) (opcional se a função de suporte 6 estiver presente)</td>
<td>
    4
   </td>
</tr>
<tr>
<td>
<code class="function">
     comparePartial
    </code>
</td>
<td>comparar a chave parcial da consulta e a chave do índice, e retornar um número inteiro menor que zero, zero ou maior que zero, indicando se o GIN deve ignorar esta entrada do índice, tratar a entrada como uma correspondência ou parar a varredura do índice (opcional)</td>
<td>
    5
   </td>
</tr>
<tr>
<td>
<code class="function">
     triConsistent
    </code>
</td>
<td>determinar se o valor corresponde à condição da consulta (variante ternária) (opcional se a função de suporte 4 estiver presente)</td>
<td>
    6
   </td>
</tr>
<tr>
<td>
<code class="function">
     options
    </code>
</td>
<td>defina opções que sejam específicas para essa classe de operador (opcional)</td>
<td>
    7
   </td>
</tr>
</tbody>
</table>




  

Os índices BRIN têm cinco funções de suporte básicas, uma das quais é opcional, conforme mostrado na [Tabela 36.14][(xindex.md#XINDEX-BRIN-SUPPORT-TABLE "Table 36.14. BRIN Support Functions")]. Algumas versões das funções básicas exigem que funções de suporte adicionais sejam fornecidas. (Para mais informações, consulte [Seção 65.5.3][(brin.md#BRIN-EXTENSIBILITY "65.5.3. Extensibility")].

**Tabela 36.14. Funções de Suporte do BRIN**



<table border="1" class="table" summary="BRIN Support Functions">
<colgroup>
<col class="col1"/>
<col class="col2"/>
<col class="col3"/>
</colgroup>
<thead>
<tr>
<th>
    Function
   </th>
<th>Descrição</th>
<th>
    Support Number
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="function">
     opcInfo
    </code>
</td>
<td>retorne informações internas que descrevam os dados resumidos das colunas indexadas</td>
<td>
    1
   </td>
</tr>
<tr>
<td>
<code class="function">
     add_value
    </code>
</td>
<td>adicionar um novo valor a um conjunto de tuplas de índice resumido existente</td>
<td>
    2
   </td>
</tr>
<tr>
<td>
<code class="function">
     consistent
    </code>
</td>
<td>determinar se o valor corresponde à condição da consulta</td>
<td>
    3
   </td>
</tr>
<tr>
<td>
<code class="function">
     union
    </code>
</td>
<td>calcular a união de dois tuplos resumidos</td>
<td>
    4
   </td>
</tr>
<tr>
<td>
<code class="function">
     options
    </code>
</td>
<td>defina opções que sejam específicas para essa classe de operador (opcional)</td>
<td>
    5
   </td>
</tr>
</tbody>
</table>




  

Ao contrário dos operadores de busca, as funções de suporte retornam o tipo de dados que o método de índice específico espera; por exemplo, no caso da função de comparação para B-trees, um inteiro assinado. O número e os tipos dos argumentos de cada função de suporte também dependem do método de índice. Para B-tree e hash, as funções de suporte de comparação e hashing aceitam os mesmos tipos de dados de entrada que os operadores incluídos na classe de operadores, mas isso não é o caso da maioria das funções de suporte GiST, SP-GiST, GIN e BRIN.

### 36.16.4. Um exemplo [#](#XINDEX-EXAMPLE)

Agora que vimos as ideias, aqui está o exemplo prometido para criar uma nova classe de operadores. (Você pode encontrar uma cópia de trabalho deste exemplo em `src/tutorial/complex.c` e `src/tutorial/complex.sql` na distribuição de código-fonte.) A classe de operadores encapsula operadores que ordenam números complexos em ordem de valor absoluto, então escolhemos o nome `complex_abs_ops`. Primeiro, precisamos de um conjunto de operadores. O procedimento para definir operadores foi discutido em [Seção 36.14][(xoper.md "36.14. User-Defined Operators")]. Para uma classe de operadores em B-trees, os operadores que exigimos são:

* menor que (absoluto) (estratégia 1)  
* menor que ou igual a (absoluto) (estratégia 2)  
* igual (absoluto) (estratégia 3)  
* maior que ou igual a (absoluto) (estratégia 4)  
* maior que (absoluto) (estratégia 5)

A maneira menos propensa a erros de definir um conjunto relacionado de operadores de comparação é escrever primeiro a função de suporte de comparação de árvore B, e depois escrever as outras funções como invólucros de uma linha em torno da função de suporte. Isso reduz as chances de obter resultados inconsistentes para casos de esquina. Seguindo essa abordagem, primeiro escrevemos:

```
#define Mag(c)  ((c)->x*(c)->x + (c)->y*(c)->y)

static int
complex_abs_cmp_internal(Complex *a, Complex *b)
{
    double      amag = Mag(a),
                bmag = Mag(b);

    if (amag < bmag)
        return -1;
    if (amag > bmag)
        return 1;
    return 0;
}
```

Agora, a função menos que parece assim:

```
PG_FUNCTION_INFO_V1(complex_abs_lt);

Datum
complex_abs_lt(PG_FUNCTION_ARGS)
{
    Complex    *a = (Complex *) PG_GETARG_POINTER(0);
    Complex    *b = (Complex *) PG_GETARG_POINTER(1);

    PG_RETURN_BOOL(complex_abs_cmp_internal(a, b) < 0);
}
```

As outras quatro funções diferem apenas na forma como comparam o resultado da função interna com zero.

Em seguida, declaramos as funções e os operadores com base nas funções para SQL:

```
CREATE FUNCTION complex_abs_lt(complex, complex) RETURNS bool
    AS 'filename', 'complex_abs_lt'
    LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR < (
   leftarg = complex, rightarg = complex, procedure = complex_abs_lt,
   commutator = > , negator = >= ,
   restrict = scalarltsel, join = scalarltjoinsel
);
```

É importante especificar os operadores corretos de commutator e negator, bem como as funções de restrição e junção adequadas, caso contrário, o otimizador não poderá fazer uso eficaz do índice.

Outras coisas que merecem ser notadas estão acontecendo aqui:

* Pode haver apenas um operador com o nome, digamos, `=` e que tome o tipo `complex` para ambos os operandos. Neste caso, não temos outro operador `=` para `complex`, mas se estivessemos construindo um tipo de dados prático, provavelmente gostaríamos de `=` ser a operação de igualdade ordinária para números complexos (e não a igualdade dos valores absolutos). Nesse caso, precisaríamos usar algum outro nome de operador para `complex_abs_eq`.
* Embora o PostgreSQL possa lidar com funções que têm o mesmo nome SQL, desde que tenham diferentes tipos de dados de argumentos, o C só pode lidar com uma função global que tenha um nome dado. Portanto, não devemos nomear a função C algo simples como `abs_eq`. Geralmente é uma boa prática incluir o nome do tipo de dados no nome da função em C, para não haver conflito com funções para outros tipos de dados.
* Podíamos ter feito o nome SQL da função `abs_eq`, confiando no PostgreSQL para distingui-la pelos tipos de dados de argumentos de qualquer outra função SQL do mesmo nome. Para manter o exemplo simples, fazemos a função ter os mesmos nomes no nível C e nível SQL.

O próximo passo é o registro da rotina de suporte necessária para as árvores B. O código exemplo C que implementa isso está no mesmo arquivo que contém as funções do operador. É assim que declaramos a função:

```
CREATE FUNCTION complex_abs_cmp(complex, complex)
    RETURNS integer
    AS 'filename'
    LANGUAGE C IMMUTABLE STRICT;
```

Agora que temos os operadores e a rotina de suporte necessários, podemos finalmente criar a classe de operador:

```
CREATE OPERATOR CLASS complex_abs_ops
    DEFAULT FOR TYPE complex USING btree AS
        OPERATOR        1       < ,
        OPERATOR        2       <= ,
        OPERATOR        3       = ,
        OPERATOR        4       >= ,
        OPERATOR        5       > ,
        FUNCTION        1       complex_abs_cmp(complex, complex);
```

E pronto! Agora é possível criar e usar índices de árvore B nas colunas de `complex`.

Poderíamos ter escrito as entradas do operador de forma mais verbose, como:

```
        OPERATOR        1       < (complex, complex) ,
```

Mas não há necessidade de fazer isso quando os operadores utilizam o mesmo tipo de dados que estamos definindo para a classe de operadores.

O exemplo acima assume que você deseja tornar essa nova classe de operador a classe de operador padrão de árvore B para o tipo de dados `complex`. Se você não quiser, basta deixar de fora a palavra `DEFAULT`.

### 36.16.5. Classes e famílias de operadores [#](#XINDEX-OPFAMILY)

Até agora, assumimos implicitamente que uma classe de operador lida apenas com um tipo de dados. Embora certamente possa haver apenas um tipo de dados em uma coluna de índice específica, é frequentemente útil indexar operações que comparam uma coluna indexada a um valor de um tipo de dados diferente. Além disso, se houver uso para um operador de cruzamento de tipos de dados em conexão com uma classe de operador, muitas vezes o outro tipo de dados tem sua própria classe de operador relacionada. É útil tornar as conexões entre as classes relacionadas explícitas, porque isso pode ajudar o planejador a otimizar consultas SQL (particularmente para classes de operador B-tree, uma vez que o planejador contém um grande conhecimento sobre como trabalhar com elas).

Para atender a essas necessidades, o PostgreSQL utiliza o conceito de uma *família de operadores*. Uma família de operadores contém uma ou mais classes de operadores e também pode conter operadores indexáveis e funções de suporte correspondentes que pertencem à família como um todo, mas não a nenhuma classe específica dentro da família. Dizemos que esses operadores e funções são “soltos” dentro da família, em oposição a serem vinculados a uma classe específica. Tipicamente, cada classe de operador contém operadores de um único tipo de dado, enquanto os operadores de vários tipos de dados são soltos na família.

Todos os operadores e funções de uma família de operadores devem ter semântica compatível, onde os requisitos de compatibilidade são definidos pelo método de índice. Você pode, portanto, se perguntar por que se preocupar em destacar subconjuntos específicos da família como classes de operadores; e, de fato, para muitos propósitos, as divisões de classe são irrelevantes e a família é o único agrupamento interessante. A razão para definir classes de operadores é que elas especificam quanto da família é necessário para suportar qualquer índice específico. Se houver um índice usando uma classe de operador, então essa classe de operador não pode ser descartada sem descartar o índice — mas outras partes da família de operadores, a saber, outras classes de operadores e operadores soltos, podem ser descartadas. Assim, uma classe de operador deve ser especificada para conter o conjunto mínimo de operadores e funções que são razoavelmente necessárias para trabalhar com um índice em um tipo de dados específico, e então operadores relacionados, mas não essenciais, podem ser adicionados como membros soltos da família de operadores.

Como exemplo, o PostgreSQL possui uma família de operadores B-tree embutida `integer_ops`, que inclui classes de operadores `int8_ops`, `int4_ops` e `int2_ops` para índices em colunas de `bigint` (`int8`), `integer` (`int4`) e `smallint` (`int2`) respectivamente. A família também contém operadores de comparação de dados cruzados, permitindo que qualquer dois desses tipos sejam comparados, de modo que um índice em um desses tipos possa ser pesquisado usando um valor de comparação de outro tipo. A família pode ser duplicada por essas definições:

```
CREATE OPERATOR FAMILY integer_ops USING btree;

CREATE OPERATOR CLASS int8_ops
DEFAULT FOR TYPE int8 USING btree FAMILY integer_ops AS
  -- standard int8 comparisons
  OPERATOR 1 < ,
  OPERATOR 2 <= ,
  OPERATOR 3 = ,
  OPERATOR 4 >= ,
  OPERATOR 5 > ,
  FUNCTION 1 btint8cmp(int8, int8) ,
  FUNCTION 2 btint8sortsupport(internal) ,
  FUNCTION 3 in_range(int8, int8, int8, boolean, boolean) ,
  FUNCTION 4 btequalimage(oid) ,
  FUNCTION 6 btint8skipsupport(internal) ;

CREATE OPERATOR CLASS int4_ops
DEFAULT FOR TYPE int4 USING btree FAMILY integer_ops AS
  -- standard int4 comparisons
  OPERATOR 1 < ,
  OPERATOR 2 <= ,
  OPERATOR 3 = ,
  OPERATOR 4 >= ,
  OPERATOR 5 > ,
  FUNCTION 1 btint4cmp(int4, int4) ,
  FUNCTION 2 btint4sortsupport(internal) ,
  FUNCTION 3 in_range(int4, int4, int4, boolean, boolean) ,
  FUNCTION 4 btequalimage(oid) ,
  FUNCTION 6 btint4skipsupport(internal) ;

CREATE OPERATOR CLASS int2_ops
DEFAULT FOR TYPE int2 USING btree FAMILY integer_ops AS
  -- standard int2 comparisons
  OPERATOR 1 < ,
  OPERATOR 2 <= ,
  OPERATOR 3 = ,
  OPERATOR 4 >= ,
  OPERATOR 5 > ,
  FUNCTION 1 btint2cmp(int2, int2) ,
  FUNCTION 2 btint2sortsupport(internal) ,
  FUNCTION 3 in_range(int2, int2, int2, boolean, boolean) ,
  FUNCTION 4 btequalimage(oid) ,
  FUNCTION 6 btint2skipsupport(internal) ;

ALTER OPERATOR FAMILY integer_ops USING btree ADD
  -- cross-type comparisons int8 vs int2
  OPERATOR 1 < (int8, int2) ,
  OPERATOR 2 <= (int8, int2) ,
  OPERATOR 3 = (int8, int2) ,
  OPERATOR 4 >= (int8, int2) ,
  OPERATOR 5 > (int8, int2) ,
  FUNCTION 1 btint82cmp(int8, int2) ,

  -- cross-type comparisons int8 vs int4
  OPERATOR 1 < (int8, int4) ,
  OPERATOR 2 <= (int8, int4) ,
  OPERATOR 3 = (int8, int4) ,
  OPERATOR 4 >= (int8, int4) ,
  OPERATOR 5 > (int8, int4) ,
  FUNCTION 1 btint84cmp(int8, int4) ,

  -- cross-type comparisons int4 vs int2
  OPERATOR 1 < (int4, int2) ,
  OPERATOR 2 <= (int4, int2) ,
  OPERATOR 3 = (int4, int2) ,
  OPERATOR 4 >= (int4, int2) ,
  OPERATOR 5 > (int4, int2) ,
  FUNCTION 1 btint42cmp(int4, int2) ,

  -- cross-type comparisons int4 vs int8
  OPERATOR 1 < (int4, int8) ,
  OPERATOR 2 <= (int4, int8) ,
  OPERATOR 3 = (int4, int8) ,
  OPERATOR 4 >= (int4, int8) ,
  OPERATOR 5 > (int4, int8) ,
  FUNCTION 1 btint48cmp(int4, int8) ,

  -- cross-type comparisons int2 vs int8
  OPERATOR 1 < (int2, int8) ,
  OPERATOR 2 <= (int2, int8) ,
  OPERATOR 3 = (int2, int8) ,
  OPERATOR 4 >= (int2, int8) ,
  OPERATOR 5 > (int2, int8) ,
  FUNCTION 1 btint28cmp(int2, int8) ,

  -- cross-type comparisons int2 vs int4
  OPERATOR 1 < (int2, int4) ,
  OPERATOR 2 <= (int2, int4) ,
  OPERATOR 3 = (int2, int4) ,
  OPERATOR 4 >= (int2, int4) ,
  OPERATOR 5 > (int2, int4) ,
  FUNCTION 1 btint24cmp(int2, int4) ,

  -- cross-type in_range functions
  FUNCTION 3 in_range(int4, int4, int8, boolean, boolean) ,
  FUNCTION 3 in_range(int4, int4, int2, boolean, boolean) ,
  FUNCTION 3 in_range(int2, int2, int8, boolean, boolean) ,
  FUNCTION 3 in_range(int2, int2, int4, boolean, boolean) ;
```

Observe que essa definição "sobrecarrega" os números da estratégia do operador e da função de suporte: cada número ocorre várias vezes dentro da família. Isso é permitido desde que cada instância de um número específico tenha tipos de dados de entrada distintos. As instâncias que têm ambos os tipos de entrada iguais ao tipo de entrada de uma classe de operador são os operadores e funções de suporte primários para aquela classe de operador, e na maioria dos casos devem ser declaradas como parte da classe de operador em vez de como membros soltos da família.

Em uma família de operadores de árvore B, todos os operadores da família devem ser compatíveis, conforme detalhado em [Seção 65.1.2][(btree.md#BTREE-BEHAVIOR "65.1.2. Behavior of B-Tree Operator Classes")]. Para cada operador da família, deve haver uma função de suporte com os mesmos dois tipos de dados de entrada que o operador. Recomenda-se que uma família seja completa, ou seja, para cada combinação de tipos de dados, todos os operadores devem ser incluídos. Cada classe de operador deve incluir apenas os operadores não cruzados e a função de suporte para seu tipo de dados.

Para construir uma família de operadores de hash de vários tipos de dados, funções de suporte a hash compatíveis devem ser criadas para cada tipo de dados que é suportado pela família. Aqui, a compatibilidade significa que as funções são garantidas para retornar o mesmo código de hash para quaisquer dois valores que são considerados iguais pelos operadores de igualdade da família, mesmo quando os valores são de tipos diferentes. Isso geralmente é difícil de realizar quando os tipos têm representações físicas diferentes, mas pode ser feito em alguns casos. Além disso, a conversão de um valor de um tipo de dados representado na família de operadores para outro tipo de dados também representado na família de operadores via uma conversão implícita ou binária não deve alterar o valor de hash calculado. Observe que há apenas uma função de suporte por tipo de dados, não uma por operador de igualdade. Recomenda-se que uma família seja completa, ou seja, forneça um operador de igualdade para cada combinação de tipos de dados. Cada classe de operador deve incluir apenas o operador de igualdade não cruzado e a função de suporte para seu tipo de dados.

Os índices GiST, SP-GiST e GIN não têm nenhuma noção explícita de operações entre tipos de dados. O conjunto de operadores suportados é apenas o que as funções de suporte primário para uma determinada classe de operadores podem lidar.

Em BRIN, os requisitos dependem da estrutura que fornece as classes de operador. Para as classes de operador baseadas em `minmax`, o comportamento exigido é o mesmo para as famílias de operadores B-tree: todos os operadores da família devem ser compatíveis, e os casts não devem alterar a ordem de classificação associada.

### Nota

Antes do PostgreSQL 8.3, não havia o conceito de famílias de operadores, e, portanto, quaisquer operadores cruzados de dados que fossem destinados a serem usados com um índice tinham que ser vinculados diretamente à classe de operadores do índice. Embora essa abordagem ainda funcione, ela é desaconselhada porque torna as dependências de um índice muito amplas e porque o planejador pode lidar com comparações de dados cruzados de forma mais eficaz quando ambos os tipos de dados têm operadores na mesma família de operadores.

### 36.16.6. Dependências do sistema em classes de operador [#](#XINDEX-OPCLASS-DEPENDENCIES)

O PostgreSQL utiliza classes de operador para inferir as propriedades dos operadores de mais maneiras do que apenas se eles podem ser usados com índices. Portanto, você pode querer criar classes de operador mesmo que não tenha a intenção de indexar quaisquer colunas do seu tipo de dados.

Em particular, existem recursos do SQL, como `ORDER BY` e `DISTINCT`, que exigem comparação e ordenação de valores. Para implementar esses recursos em um tipo de dados definido pelo usuário, o PostgreSQL procura a classe de operador padrão de árvore B para o tipo de dados. O membro “igual” dessa classe de operador define a noção do sistema de igualdade de valores para `GROUP BY` e `DISTINCT`, e a ordem de ordenação imposta pela classe de operador define a ordem padrão de `ORDER BY`.

Se não houver uma classe de operador B-tree padrão para um tipo de dados, o sistema procurará uma classe de operador de hash padrão. Mas, como esse tipo de classe de operador só fornece igualdade, ela só é capaz de suportar agrupamento, não ordenação.

Quando não há uma classe de operador padrão para um tipo de dados, você receberá erros como “não foi possível identificar um operador de ordenação” se você tentar usar essas funcionalidades do SQL com o tipo de dados.

### Nota

Nas versões do PostgreSQL anteriores à 7.4, as operações de ordenação e agrupamento usariam implicitamente operadores com os nomes `=`, `<` e `>`. O novo comportamento de depender das classes de operadores padrão evita a necessidade de fazer qualquer suposição sobre o comportamento dos operadores com nomes específicos.

É possível ordenar por uma classe de operador de árvore B não padrão especificando o operador de menos que da classe em uma opção `USING`, por exemplo:

```
SELECT * FROM mytable ORDER BY somecol USING ~<~;
```

Alternativamente, especificar o operador de maior que da classe em `USING` seleciona uma ordenação em ordem decrescente.

A comparação de arrays de um tipo definido pelo usuário também depende das semânticas definidas pela classe de operador B-tree padrão do tipo. Se não houver uma classe de operador B-tree padrão, mas houver uma classe de operador hash padrão, então a igualdade de arrays é suportada, mas não comparações de ordenação.

Outra característica do SQL que exige ainda mais conhecimento sobre tipos de dados específicos é a opção de enquadramento `RANGE` *`offset`* `PRECEDING`/`FOLLOWING` para funções de janela (consulte [Seção 4.2.8](sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS "4.2.8. Window Function Calls")). Para uma consulta como

```
SELECT sum(x) OVER (ORDER BY x RANGE BETWEEN 5 PRECEDING AND 10 FOLLOWING)
  FROM mytable;
```

não é suficiente saber como ordenar por `x`; o banco de dados também deve entender como "subtrair 5" ou "acrescentar 10" ao valor da linha atual de `x` do banco de dados para identificar os limites da moldura atual da janela. Comparar os limites resultantes com os valores de `x` de outras linhas é possível usando os operadores de comparação fornecidos pela classe de operador de árvore B que define a ordenação de `ORDER BY` — mas os operadores de adição e subtração não fazem parte da classe de operador, então quais devem ser usados? Tornar essa escolha fixa indesejável, porque diferentes ordens de classificação (diferentes classes de operador de árvore B) podem precisar de comportamento diferente. Portanto, uma classe de operador de árvore B pode especificar uma função de suporte *in_range* que encapsula os comportamentos de adição e subtração que fazem sentido para sua ordem de classificação. Ela pode até fornecer mais de uma função de suporte *in_range*, no caso de haver mais de um tipo de dados que faz sentido usar como o deslocamento em cláusulas de `RANGE`. Se a classe de operador de árvore B associada à cláusula de `ORDER BY` da janela não tiver uma função de suporte *in_range* correspondente, a opção *`offset`* *`PRECEDING`/`FOLLOWING` de `PRECEDING`/`FOLLOWING` não é suportada.

Outro ponto importante é que um operador de igualdade que aparece em uma família de operadores de hash é um candidato para junções de hash, agregação de hash e otimizações relacionadas. A família de operadores de hash é essencial aqui, pois ela identifica a(s) função(ões) de hash a serem usadas.

### 36.16.7. Operadores de encomenda [#](#XINDEX-ORDERING-OPS)

Alguns métodos de acesso ao índice (atualmente, apenas GiST e SP-GiST) suportam o conceito de operadores de *ordem*. O que discutimos até agora são operadores de *busca*. Um operador de busca é aquele para o qual o índice pode ser pesquisado para encontrar todas as linhas que satisfazem `WHERE` *`indexed_column`* *`operator`* *`constant`*. Note que nada é prometido sobre a ordem em que as linhas correspondentes serão devolvidas. Em contraste, um operador de ordem não restringe o conjunto de linhas que podem ser devolvidas, mas, em vez disso, determina sua ordem. Um operador de ordem é aquele para o qual o índice pode ser digitalizado para retornar linhas na ordem representada por `ORDER BY` *`indexed_column`* *`operator`* *`constant`*. A razão para definir operadores de ordem dessa maneira é que eles suportam pesquisas de vizinhança mais próxima, se o operador for um que mede a distância. Por exemplo, uma consulta como

```
SELECT * FROM places ORDER BY location <-> point '(101,456)' LIMIT 10;
```

encontra os dez locais mais próximos a um ponto alvo dado. Um índice GiST na coluna de localização pode fazer isso de forma eficiente porque `<->` é um operador de ordenação.

Embora os operadores de busca tenham que retornar resultados booleanos, os operadores de ordenação geralmente retornam algum outro tipo, como float ou numeric para distâncias. Esse tipo normalmente não é o mesmo que o tipo de dados que está sendo indexado. Para evitar suposições fixas sobre o comportamento de diferentes tipos de dados, a definição de um operador de ordenação é necessária para nomear uma família de operadores de B-tree que especifique a ordem de classificação do tipo de dados resultante. Como foi dito na seção anterior, as famílias de operadores de B-tree definem a noção de ordenação do PostgreSQL, então essa é uma representação natural. Como o operador `<->` retorna `float8`, ele poderia ser especificado em um comando de criação de uma classe de operadores assim:

```
OPERATOR 15    <-> (point, point) FOR ORDER BY float_ops
```

onde `float_ops` é a família de operadores embutida que inclui operações em `float8`. Esta declaração afirma que o índice é capaz de retornar linhas em ordem de valores crescentes do operador `<->`.

### 36.16.8. Características especiais das classes de operador [#](#XINDEX-OPCLASS-FEATURES)

Existem duas características especiais das classes de operador que ainda não discutimos, principalmente porque elas não são úteis com os métodos de índice mais comumente usados.

Normalmente, declarar um operador como membro de uma classe (ou família) de operadores significa que o método de índice pode recuperar exatamente o conjunto de linhas que satisfazem uma condição `WHERE` usando o operador. Por exemplo:

```
SELECT * FROM table WHERE integer_column < 4;
```

pode ser satisfeita exatamente por um índice de árvore B na coluna inteira. Mas há casos em que um índice é útil como um guia inexato para as linhas correspondentes. Por exemplo, se um índice GiST armazena apenas caixas de delimitação para objetos geométricos, então ele não pode exatamente satisfazer uma condição `WHERE` que testa a sobreposição entre objetos não retangulares, como polígonos. Ainda assim, poderíamos usar o índice para encontrar objetos cujas caixas de delimitação se sobrepõem à caixa de delimitação do objeto alvo, e então realizar o teste de sobreposição exata apenas nos objetos encontrados pelo índice. Se este cenário se aplicar, o índice é dito ser “perda” para o operador. As pesquisas de índice perda são implementadas fazendo com que o método de índice retorne um sinalizador *recheck* quando uma linha pode ou não realmente satisfazer a condição da consulta. O sistema central então testa a condição original da consulta na linha recuperada para ver se ela deve ser devolvida como um jogo válido. Esta abordagem funciona se o índice for garantido para retornar todas as linhas necessárias, além de talvez algumas linhas adicionais, que podem ser eliminadas realizando a invocação original do operador. Os métodos de índice que suportam pesquisas perda (atualmente, GiST, SP-GiST e GIN) permitem que as funções de suporte das classes de operadores individuais definam o sinalizador recheck, e assim isso é essencialmente uma característica de classe de operador.

Considere novamente a situação em que estamos armazenando no índice apenas a caixa de delimitação de um objeto complexo, como um polígono. Neste caso, não há muito valor em armazenar todo o polígono na entrada do índice — podemos tão bem armazenar apenas um objeto mais simples do tipo `box`. Esta situação é expressa pela opção `STORAGE` em `CREATE OPERATOR CLASS`: escreveríamos algo como:

```
CREATE OPERATOR CLASS polygon_ops
    DEFAULT FOR TYPE polygon USING gist AS
        ...
        STORAGE box;
```

Atualmente, apenas os métodos de índice GiST, SP-GiST, GIN e BRIN suportam um tipo `STORAGE` que é diferente do tipo de dados da coluna. Os GiST `compress` e `decompress` suportam rotinas que devem lidar com conversão de tipo de dados quando `STORAGE` é usado. O SP-GiST, por sua vez, requer uma função de suporte `compress` para converter para o tipo de armazenamento, quando isso é diferente; se uma opclass de SP-GiST também suporta a recuperação de dados, a conversão inversa deve ser tratada pela função `consistent`. Em GIN, o tipo `STORAGE` identifica o tipo dos valores da “chave”, que normalmente é diferente do tipo da coluna indexada — por exemplo, uma classe de operador para colunas de matriz de inteiros pode ter chaves que são apenas inteiros. As rotinas de suporte `extractValue` e `extractQuery` de GIN são responsáveis por extrair chaves de valores indexados. BRIN é semelhante a GIN: o tipo `STORAGE` identifica o tipo dos valores resumidos armazenados, e os procedimentos de suporte de classes de operador são responsáveis por interpretar os valores resumidos corretamente.