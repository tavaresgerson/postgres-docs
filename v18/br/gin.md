## 65.4. Índices GIN [#](#GIN)

* [65.4.1. Introdução](gin.md#GIN-INTRO)
* [65.4.2. Classes de Operadores Integradas](gin.md#GIN-BUILTIN-OPCLASSES)
* [65.4.3. Extensibilidade](gin.md#GIN-EXTENSIBILITY)
* [65.4.4. Implementação](gin.md#GIN-IMPLEMENTATION)
* [65.4.5. Dicas e Truques do GIN](gin.md#GIN-TIPS)
* [65.4.6. Limitações](gin.md#GIN-LIMIT)
* [65.4.7. Exemplos](gin.md#GIN-EXAMPLES)

### 65.4.1. Introdução [#](#GIN-INTRO)

GIN significa Índice Invertido Generalizado. O GIN é projetado para lidar com casos em que os itens a serem indexados são valores compostos, e as consultas que serão manipuladas pelo índice precisam procurar valores de elementos que apareçam dentro dos itens compostos. Por exemplo, os itens podem ser documentos, e as consultas podem ser buscas por documentos que contenham palavras específicas.

Usamos a palavra *item* para se referir a um valor composto que deve ser indexado, e a palavra *chave* para se referir a um valor de elemento. O GIN sempre armazena e busca por chaves, não por valores de item em si.

Um índice GIN armazena um conjunto de pares (chave, lista de postagem), onde uma *lista de postagem* é um conjunto de IDs de linha nos quais a chave ocorre. O mesmo ID de linha pode aparecer em múltiplas listas de postagem, uma vez que um item pode conter mais de uma chave. Cada valor da chave é armazenado apenas uma vez, portanto, um índice GIN é muito compacto para casos em que a mesma chave aparece muitas vezes.

GIN é generalizada no sentido de que o código do método de acesso GIN não precisa conhecer as operações específicas que ele acelera. Em vez disso, ele usa estratégias personalizadas definidas para tipos de dados particulares. A estratégia define como as chaves são extraídas dos itens indexados e das condições de consulta, e como determinar se uma linha que contém alguns dos valores da chave em uma consulta realmente satisfaz a consulta.

Uma vantagem do GIN é que ele permite o desenvolvimento de tipos de dados personalizados com os métodos de acesso apropriados, por um especialista no domínio do tipo de dados, e não por um especialista em banco de dados. Esta é uma vantagem muito semelhante ao uso do GiST.

A implementação do GIN no PostgreSQL é mantida principalmente por Teodor Sigaev e Oleg Bartunov. Há mais informações sobre o GIN em seu [site](http://www.sai.msu.su/~megera/wiki/Gin).

### 65.4.2. Classes de operador embutidas [#](#GIN-BUILTIN-OPCLASSES)

A distribuição principal do PostgreSQL inclui as classes de operadores GIN mostradas na [Tabela 65.3] ((gin.md#GIN-BUILTIN-OPCLASSES-TABLE "Table 65.3. Built-in GIN Operator Classes")). (Alguns dos módulos opcionais descritos em [Apêndice F] ((contrib.md "Appendix F. Additional Supplied Modules and Extensions")) fornecem classes adicionais de operadores GIN.)

**Tabela 65.3. Classes de operadores GIN integrados**



<table border="1" class="table" summary="Built-in GIN Operator Classes">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Name
   </th>
   <th>
    Indexable Operators
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td rowspan="4" valign="middle">
    <code class="literal">
     array_ops
    </code>
   </td>
   <td>
    <code class="literal">
     &amp;&amp; (anyarray,anyarray)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     @&gt; (anyarray,anyarray)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;@ (anyarray,anyarray)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     = (anyarray,anyarray)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="6" valign="middle">
    <code class="literal">
     jsonb_ops
    </code>
   </td>
   <td>
    <code class="literal">
     @&gt; (jsonb,jsonb)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     @? (jsonb,jsonpath)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     @@ (jsonb,jsonpath)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ? (jsonb,text)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ?| (jsonb,text[])
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ?&amp; (jsonb,text[])
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="3" valign="middle">
    <code class="literal">
     jsonb_path_ops
    </code>
   </td>
   <td>
    <code class="literal">
     @&gt; (jsonb,jsonb)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     @? (jsonb,jsonpath)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     @@ (jsonb,jsonpath)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     tsvector_ops
    </code>
   </td>
   <td>
    <code class="literal">
     @@ (tsvector,tsquery)
    </code>
   </td>
  </tr>
 </tbody>
</table>









Das duas classes de operadores para o tipo `jsonb`, `jsonb_ops` é o padrão. `jsonb_path_ops` suporta menos operadores, mas oferece melhor desempenho para aqueles operadores. Veja [Seção 8.14.4](datatype-json.md#JSON-INDEXING) para detalhes.

### 65.4.3. Extensibilidade [#](#GIN-EXTENSIBILITY)

A interface GIN possui um alto nível de abstração, exigindo que o implementador do método de acesso implemente apenas a semântica do tipo de dados a ser acessado. A própria camada GIN cuida da concorrência, do registro e da busca na estrutura de árvore.

Tudo o que é necessário para fazer um método de acesso GIN funcionar é implementar alguns métodos definidos pelo usuário, que definem o comportamento das chaves na árvore e as relações entre as chaves, itens indexados e consultas indexáveis. Em suma, o GIN combina extensibilidade com generalidade, reutilização de código e uma interface limpa.

Um operador de classe para GIN deve fornecer dois métodos:

`Datum *extractValue(Datum itemValue, int32 *nkeys, bool **nullFlags)`: Retorna um array palloc de chaves dado um item a ser indexado. O número de chaves retornadas deve ser armazenado em `*nkeys`. Se alguma das chaves puder ser nula, também pallocue um array de campos `*nkeys` `bool`, armazene seu endereço em `*nullFlags` e defina esses flags nulos conforme necessário. `*nullFlags` pode ser deixado em `NULL` (seu valor inicial) se todas as chaves forem não nulos. O valor de retorno pode ser `NULL` se o item não contiver chaves.

`Datum *extractQuery(Datum query, int32 *nkeys, StrategyNumber n, bool **pmatch, Pointer **extra_data, bool **nullFlags, int32 *searchMode)`: Retorna um array palloc de chaves dado um valor a ser pesquisado; ou seja, `query` é o valor do lado direito de um operador indexável, cujo lado esquerdo é a coluna indexada. `n` é o número de estratégia do operador dentro da classe de operadores (ver [Seção 36.16.2](xindex.md#XINDEX-STRATEGIES)). Frequentemente, `extractQuery` precisará consultar `n` para determinar o tipo de dados de `query` e o método que ele deve usar para extrair os valores das chaves. O número de chaves retornadas deve ser armazenado em `*nkeys`. Se alguma das chaves puder ser nula, também pallocue um array de campos `*nkeys` `bool`, armazene seu endereço em `*nullFlags` e defina esses flags nulos conforme necessário. `*nullFlags` pode ser deixado `NULL` (seu valor inicial) se todas as chaves forem não nulos. O valor de retorno pode ser `NULL` se o `query` não contiver chaves.

`searchMode` é um argumento de saída que permite que `extractQuery` especifique detalhes sobre como a pesquisa será realizada. Se `*searchMode` estiver definido como `GIN_SEARCH_MODE_DEFAULT` (que é o valor com o qual é inicializado antes da chamada), apenas os itens que correspondem a pelo menos uma das chaves retornadas são considerados correspondências candidatas. Se `*searchMode` estiver definido como `GIN_SEARCH_MODE_INCLUDE_EMPTY`, então, além dos itens que contêm pelo menos uma chave correspondente, os itens que não contêm nenhuma chave são considerados correspondências candidatas. (Este modo é útil para implementar operadores de subconjunto, por exemplo.) Se `*searchMode` estiver definido como `GIN_SEARCH_MODE_ALL`, então todos os itens não nulos no índice são considerados correspondências candidatas, independentemente de corresponderem a alguma das chaves retornadas. (Este modo é muito mais lento do que as outras duas opções, pois requer a varredura essencialmente de todo o índice, mas pode ser necessário implementar casos de esquina corretamente. Um operador que precisa deste modo na maioria dos casos provavelmente não é um bom candidato para uma classe de operador GIN.) Os símbolos a serem usados para definir este modo estão definidos em `access/gin.h`.

`pmatch` é um argumento de saída para uso quando a correspondência parcial é suportada. Para usá-lo, `extractQuery` deve alocar um array de `*nkeys` `bool`s e armazenar seu endereço em `*pmatch`. Cada elemento do array deve ser definido como verdadeiro se a chave correspondente exigir correspondência parcial, falso se não. Se `*pmatch` estiver definido como `NULL`, então o GIN assume que a correspondência parcial não é necessária. A variável é inicializada em `NULL` antes da chamada, então este argumento pode simplesmente ser ignorado por classes de operador que não suportam correspondência parcial.

`extra_data` é um argumento de saída que permite que `extractQuery` passe dados adicionais para os métodos `consistent` e `comparePartial`. Para usá-lo, `extractQuery` deve alocar um array de ponteiros `*nkeys` e armazenar seu endereço em `*extra_data`, e em seguida, armazenar o que quiser nos ponteiros individuais. A variável é inicializada em `NULL` antes da chamada, então este argumento pode simplesmente ser ignorado por classes de operador que não requerem dados adicionais. Se `*extra_data` estiver definido, o array inteiro é passado para o método `consistent`, e o elemento apropriado para o método `comparePartial`.

Uma classe de operador também deve fornecer uma função para verificar se um item indexado corresponde à consulta. Ela vem em dois sabores, uma função booleana `consistent` e uma função ternária `triConsistent`. `triConsistent` cobre a funcionalidade de ambos, portanto, fornecer apenas `triConsistent` é suficiente. No entanto, se a variante booleana for significativamente mais barata de calcular, pode ser vantajosa fornecer ambas. Se apenas a variante booleana for fornecida, algumas otimizações que dependem de refutar itens de índice antes de obter todas as chaves são desativadas.

`bool consistent(bool check[], StrategyNumber n, Datum query, int32 nkeys, Pointer extra_data[], bool *recheck, Datum queryKeys[], bool nullFlags[])`: Retorna verdadeiro se um item indexado satisfazer o operador de consulta com o número de estratégia `n` (ou pode satisfê-lo, se a indicação de recheck for retornada). Esta função não tem acesso direto ao valor do item indexado, uma vez que o GIN não armazena itens explicitamente. O que está disponível é conhecimento sobre quais valores de chave extraídos da consulta aparecem em um dado item indexado. A matriz `check` tem comprimento `nkeys`, que é o mesmo número de chaves previamente retornadas por `extractQuery` para este `query` de dados. Cada elemento da matriz `check` é verdadeiro se o item indexado contém a chave correspondente, ou seja, se (check[i] == true) o i-ésimo chave do array de resultados `extractQuery` está presente no item indexado. O dado original `query` é passado caso o método `consistent` precise consultá-lo, assim como as matrizes `queryKeys[]` e `nullFlags[]` previamente retornadas por `extractQuery`. `extra_data` é a matriz de dados extra retornada por `extractQuery`, ou `NULL` se nenhuma.

Quando o `extractQuery` retorna uma chave nula no `queryKeys[]`, o elemento correspondente no `check[]` é verdadeiro se o item indexado contém uma chave nula; ou seja, a semântica do `check[]` é como a do `IS NOT DISTINCT FROM`. A função `consistent` pode examinar o elemento correspondente no `nullFlags[]` se precisar distinguir entre uma correspondência de valor regular e uma correspondência nula.

Em caso de sucesso, `*recheck` deve ser definido como verdadeiro se o tuplo do heap precisar ser refeito em relação ao operador da consulta, ou como falso se o teste do índice for exato. Ou seja, um valor de retorno falso garante que o tuplo do heap não corresponda à consulta; um valor de retorno verdadeiro com `*recheck` definido como falso garante que o tuplo do heap corresponda à consulta; e um valor de retorno verdadeiro com `*recheck` definido como verdadeiro significa que o tuplo do heap pode corresponder à consulta, portanto, ele precisa ser obtido e refeito, avaliando o operador da consulta diretamente contra o item originalmente indexado.

`GinTernaryValue triConsistent(GinTernaryValue check[], StrategyNumber n, Datum query, int32 nkeys, Pointer extra_data[], Datum queryKeys[], bool nullFlags[])`: `triConsistent` é semelhante a `consistent`, mas, em vez de Booleans no vetor `check`, há três valores possíveis para cada chave: `GIN_TRUE`, `GIN_FALSE` e `GIN_MAYBE`. `GIN_FALSE` e `GIN_TRUE` têm o mesmo significado que os valores regulares de Booleanos, enquanto `GIN_MAYBE` significa que a presença daquela chave não é conhecida. Quando os valores de `GIN_MAYBE` estão presentes, a função deve retornar apenas `GIN_TRUE` se o item certamente corresponder, independentemente de o item de índice conter as chaves de consulta correspondentes. Da mesma forma, a função deve retornar `GIN_FALSE` apenas se o item não corresponder, independentemente de conter as chaves de `GIN_MAYBE`. Se o resultado depende das entradas de `GIN_MAYBE`, ou seja, a correspondência não pode ser confirmada ou refutada com base nas chaves de consulta conhecidas, a função deve retornar `GIN_MAYBE`.

Quando não houver valores de `GIN_MAYBE` no vetor `check`, um valor de retorno de `GIN_MAYBE` é equivalente a definir a bandeira `recheck` na função booleana `consistent`.

Além disso, o GIN deve ter uma maneira de ordenar os valores-chave armazenados no índice. A classe de operador pode definir a ordem de classificação especificando um método de comparação:

`int compare(Datum a, Datum b)`: Compara duas chaves (itens não indexados!) e retorna um inteiro menor que zero, zero ou maior que zero, indicando se a primeira chave é menor que, igual a ou maior que a segunda. Chaves nulos nunca são passadas para esta função.

Como alternativa, se a classe de operador não fornecer um método `compare`, o GIN procurará a classe de operador btree padrão para o tipo de dados da chave do índice e usará sua função de comparação. É recomendável especificar a função de comparação em uma classe de operador GIN que é destinada a apenas um tipo de dados, pois a busca pela classe de operador btree custa alguns ciclos. No entanto, as classes de operador GIN polimórficas (como `array_ops`) geralmente não podem especificar uma única função de comparação.

Uma classe de operador para GIN pode, opcionalmente, fornecer os seguintes métodos:

`int comparePartial(Datum partial_key, Datum key, StrategyNumber n, Pointer extra_data)`: Compare uma chave de consulta de correspondência parcial a uma chave de índice. Retorna um inteiro cujo sinal indica o resultado: menos que zero significa que a chave de índice não corresponde à consulta, mas a varredura do índice deve continuar; zero significa que a chave de índice corresponde à consulta; maior que zero indica que a varredura do índice deve parar porque não há mais correspondências possíveis. O número de estratégia `n` do operador que gerou a consulta de correspondência parcial é fornecido, caso suas semânticas sejam necessárias para determinar quando interromper a varredura. Além disso, `extra_data` é o elemento correspondente da matriz de dados extras feita por `extractQuery`, ou `NULL` se nenhum. Chaves nulos nunca são passadas para esta função.

`void options(local_relopts *relopts)`: Define um conjunto de parâmetros visíveis pelo usuário que controlam o comportamento da classe do operador.

A função `options` é passada um ponteiro para uma estrutura `local_relopts`, que precisa ser preenchida com um conjunto de opções específicas da classe do operador. As opções podem ser acessadas a partir de outras funções de suporte usando as macros `PG_HAS_OPCLASS_OPTIONS()` e `PG_GET_OPCLASS_OPTIONS()`.

Como a extração de chaves de valores indexados e a representação da chave no GIN são flexíveis, elas podem depender de parâmetros especificados pelo usuário.

Para suportar consultas de "jogo parcial", uma classe de operador deve fornecer o método `comparePartial` e seu método `extractQuery` deve definir o parâmetro `pmatch` quando uma consulta de jogo parcial for encontrada. Veja [Seção 65.4.4.2](gin.md#GIN-PARTIAL-MATCH) para detalhes.

Os tipos de dados reais dos vários valores `Datum` mencionados acima variam dependendo da classe do operador. Os valores dos itens passados para `extractValue` são sempre do tipo de entrada da classe do operador, e todos os valores chave devem ser do tipo `STORAGE` da classe. O tipo do argumento `query` passado para `extractQuery`, `consistent` e `triConsistent` é o que for o tipo de entrada do membro da classe identificado pelo número da estratégia. Isso não precisa ser o mesmo que o tipo indexado, desde que os valores chave do tipo correto possam ser extraídos dele. No entanto, é recomendável que as declarações SQL dessas três funções de suporte usem o tipo de dados indexado da opclass para o argumento `query`, mesmo que o tipo real possa ser algo diferente dependendo do operador.

### 65.4.4. Implementação [#](#GIN-IMPLEMENTATION)

Internamente, um índice GIN contém um índice de árvore B construído sobre chaves, onde cada chave é um elemento de um ou mais itens indexados (um membro de uma matriz, por exemplo) e onde cada tupla em uma página de folha contém ou um ponteiro para uma árvore B de ponteiros de pilha (uma "árvore de publicação"), ou uma simples lista de ponteiros de pilha (uma "lista de publicação") quando a lista é pequena o suficiente para caber em uma única tupla de índice juntamente com o valor da chave. [Figura 65.1](gin.md#GIN-INTERNALS-FIGURE) ilustra esses componentes de um índice GIN.

A partir do PostgreSQL 9.1, valores de chave nulos podem ser incluídos no índice. Além disso, os nulos de marcador são incluídos no índice para itens indexados que são nulos ou não contêm chaves de acordo com `extractValue`. Isso permite que pesquisas que devem encontrar itens vazios façam isso.

Os índices GIN de múltiplas colunas são implementados construindo uma única árvore B sobre valores compostos (número de coluna, valor da chave). Os valores da chave para diferentes colunas podem ser de diferentes tipos.

**Figura 65.1. Interiores do GIN**



#### 65.4.4.1. Técnica de Atualização Rápida GIN [#](#GIN-FAST-UPDATE)

Atualizar um índice GIN tende a ser lento devido à natureza intrínseca dos índices invertidos: inserir ou atualizar uma linha em um heap pode causar muitas inserções no índice (uma para cada chave extraída do item indexado). O GIN é capaz de adiar grande parte desse trabalho, inserindo novos tuplos em uma lista temporária e não ordenada de entradas pendentes. Quando a tabela é aspirada ou autoanalisada, ou quando a função `gin_clean_pending_list` é chamada, ou se a lista pendente se torna maior que [gin_pending_list_limit](runtime-config-client.md#GUC-GIN-PENDING-LIST-LIMIT), as entradas são movidas para a estrutura de dados principal do GIN usando as mesmas técnicas de inserção em massa usadas durante a criação inicial do índice. Isso melhora muito a velocidade de atualização do índice GIN, mesmo contando o sobrecarga adicional do vácuo. Além disso, o trabalho de sobrecarga pode ser feito por um processo em segundo plano em vez de no processamento de consultas em primeiro plano.

A principal desvantagem dessa abordagem é que as pesquisas devem percorrer a lista de entradas pendentes, além de pesquisar o índice regular, e, portanto, uma grande lista de entradas pendentes irá desacelerar significativamente as pesquisas. Outra desvantagem é que, embora a maioria das atualizações seja rápida, uma atualização que faça com que a lista pendente se torne "demasiado grande" implicará em um ciclo de limpeza imediata e, portanto, será muito mais lenta do que outras atualizações. O uso adequado do autovacuum pode minimizar ambos esses problemas.

Se o tempo de resposta consistente for mais importante do que a velocidade de atualização, o uso de entradas pendentes pode ser desativado desligando o parâmetro de armazenamento `fastupdate` para um índice GIN. Consulte [CREATE INDEX](sql-createindex.md "CREATE INDEX") para obter detalhes.

#### 65.4.4.2. Algoritmo de correspondência parcial [#](#GIN-PARTIAL-MATCH)

O GIN pode suportar consultas de "jogo parcial", nas quais a consulta não determina uma correspondência exata para uma ou mais chaves, mas as possíveis correspondências estão dentro de uma faixa razoavelmente estreita de valores de chave (dentro do pedido de classificação de chave determinado pelo método de suporte `compare`). O método `extractQuery`, em vez de retornar um valor de chave a ser correspondido exatamente, retorna um valor de chave que é o limite inferior da faixa a ser pesquisada, e define a bandeira `pmatch` como verdadeira. A faixa de chave é então varrida usando o método `comparePartial`. O `comparePartial` deve retornar zero para uma chave de índice correspondente, menos de zero para uma não correspondência que ainda está dentro da faixa a ser pesquisada, ou maior que zero se a chave de índice estiver além da faixa que poderia corresponder.

### 65.4.5. Dicas e truques do GIN [#](#GIN-TIPS)

Criar vs. inserir: A inserção em um índice GIN pode ser lenta devido à probabilidade de muitas chaves serem inseridas para cada item. Portanto, para inserções em massa em uma tabela, é aconselhável descartar o índice GIN e recriá-lo após terminar a inserção em massa.

Quando o `fastupdate` está habilitado para GIN (consulte [Seção 65.4.4.1](gin.md#GIN-FAST-UPDATE) para detalhes), a penalidade é menor do que quando não está habilitado. Mas, para atualizações muito grandes, ainda pode ser melhor descartar e recriar o índice.

[maintenance_work_mem](runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM): O tempo de construção de um índice GIN é muito sensível ao ajuste `maintenance_work_mem`; não vale a pena economizar memória de trabalho durante a criação do índice.

[gin_pending_list_limit](runtime-config-client.md#GUC-GIN-PENDING-LIST-LIMIT): Durante uma série de inserções em um índice GIN existente que tem `fastupdate` habilitado, o sistema limpará a lista de entradas pendentes sempre que a lista crescer maior que `gin_pending_list_limit`. Para evitar flutuações no tempo de resposta observado, é desejável que a limpeza da lista pendente ocorra em segundo plano (ou seja, via autovacuum). As operações de limpeza de plano de fundo podem ser evitadas aumentando `gin_pending_list_limit` ou tornando o autovacuum mais agressivo. No entanto, aumentar o limite da operação de limpeza significa que, se uma limpeza de plano de fundo ocorrer, levará ainda mais tempo.

`gin_pending_list_limit` pode ser sobrescrito para índices GIN individuais alterando os parâmetros de armazenamento, o que permite que cada índice GIN tenha seu próprio limite de limpeza. Por exemplo, é possível aumentar o limite apenas para o índice GIN que pode ser atualizado intensamente, e diminuí-lo de outra forma.

[gin_fuzzy_search_limit](runtime-config-client.md#GUC-GIN-FUZZY-SEARCH-LIMIT): O principal objetivo do desenvolvimento dos índices GIN era criar suporte para pesquisas de texto completo altamente escaláveis no PostgreSQL, e muitas vezes há situações em que uma pesquisa de texto completo retorna um conjunto muito grande de resultados. Além disso, isso geralmente acontece quando a consulta contém palavras muito frequentes, de modo que o grande conjunto de resultados nem é útil. Como ler muitos tuplos do disco e ordená-los pode levar muito tempo, isso é inaceitável para produção. (Observe que a própria pesquisa de índice é muito rápida.)

Para facilitar a execução controlada dessas consultas, o GIN tem um limite suave configurável no número de linhas devolvidas: o parâmetro de configuração [[`gin_fuzzy_search_limit`]. Ele é definido como 0 (significando sem limite) por padrão. Se um limite não nulo for definido, então o conjunto devolvido é um subconjunto do conjunto de resultados completo, escolhido aleatoriamente.

“Soft” significa que o número real de resultados retornados pode diferir um pouco do limite especificado, dependendo da consulta e da qualidade do gerador de números aleatórios do sistema.

De acordo com a experiência, valores em milhares (por exemplo, 5000 a 20000) funcionam bem.

### 65.4.6. Limitações [#](#GIN-LIMIT)

O GIN assume que os operadores indexáveis são estritos. Isso significa que `extractValue` não será chamado em absoluto em um valor de item nulo (em vez disso, uma entrada de índice de marcador é criada automaticamente), e `extractQuery` também não será chamado em um valor de consulta nulo (em vez disso, a consulta é presumida insatisfatível). No entanto, é importante notar que valores de chave nulos contidos em um item ou valor de consulta compostos não nulos são suportados.

### 65.4.7. Exemplos [#](#GIN-EXAMPLES)

A distribuição principal do PostgreSQL inclui as classes de operadores GIN mostradas anteriormente na [Tabela 65.3] (gin.md#GIN-BUILTIN-OPCLASSES-TABLE "Table 65.3. Built-in GIN Operator Classes"). Os seguintes módulos `contrib` também contêm classes de operadores GIN:

`btree_gin`: Funcionalidade equivalente a árvore B para vários tipos de dados

`hstore`: Módulo para armazenar pares (chave, valor)

`intarray`: Suporte aprimorado para `int[]`

`pg_trgm`: Similaridade de texto usando correspondência de trigêmeos