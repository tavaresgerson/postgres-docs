## 65.1. Índices de B-Tree [#](#BTREE)

* [65.1.1. Introdução][(btree.md#BTREE-INTRO)]
* [65.1.2. Comportamento das classes operadoras de árvore B][(btree.md#BTREE-BEHAVIOR)]
* [65.1.3. Funções de suporte à árvore B][(btree.md#BTREE-SUPPORT-FUNCS)]
* [65.1.4. Implementação][(btree.md#BTREE-IMPLEMENTATION)]

### 65.1.1. Introdução [#](#BTREE-INTRO)

O PostgreSQL inclui uma implementação da estrutura de dados padrão de índice btree (árvore balanceada multidirecionada). Qualquer tipo de dados que pode ser classificado em uma ordem linear bem definida pode ser indexado por um índice btree. A única limitação é que uma entrada de índice não pode exceder aproximadamente um terço de uma página (após a compressão TOAST, se aplicável).

Como cada classe de operador btree impõe uma ordem de classificação em seu tipo de dados, as classes de operador btree (ou, na verdade, famílias de operadores) passaram a ser usadas como a representação e compreensão geral do PostgreSQL sobre a semântica de classificação. Portanto, elas adquiriram algumas características que vão além do que seria necessário apenas para suportar índices btree, e partes do sistema que estão bastante distantes do AM btree as utilizam.

### 65.1.2. Comportamento das classes de operadores de árvore B [#](#BTREE-BEHAVIOR)

Como mostrado na [Tabela 36.3][(xindex.md#XINDEX-BTREE-STRAT-TABLE "Table 36.3. B-Tree Strategies")], uma classe de operador btree deve fornecer cinco operadores de comparação, `<`, `<=`, `=`, `>=` e `>`. Pode-se esperar que `<>` também faça parte da classe de operador, mas não é o caso, porque quase nunca seria útil usar uma cláusula WHERE `<>` em uma pesquisa de índice. (Para alguns propósitos, o planejador trata `<>` como associado a uma classe de operador btree; mas ele encontra esse operador através do link negador do operador `=`, em vez de a partir de `pg_amop`.

Quando vários tipos de dados compartilham uma semântica de classificação quase idêntica, suas classes de operadores podem ser agrupadas em uma família de operadores. Fazer isso é vantajoso porque permite que o planejador faça deduções sobre comparações entre tipos diferentes. Cada classe de operador dentro da família deve conter os operadores de único tipo (e as funções de suporte associadas) para seu tipo de dados de entrada, enquanto os operadores de comparação entre tipos diferentes e as funções de suporte são "soltas" na família. É recomendável que um conjunto completo de operadores entre tipos diferentes seja incluído na família, garantindo assim que o planejador possa representar quaisquer condições de comparação que deduza da transitividade.

Existem algumas suposições básicas que uma família de operadores btree deve satisfazer:

* Um operador `=` deve ser uma relação de equivalência; ou seja, para todos os valores não nulos *`A`*, *`B`*, *`C`* do tipo de dados:

+ *`A`* `=` *`A`* é verdadeiro (*lei reflexiva*)
  + se *`A`* `=` *`B`*, então *`B`* `=` *`A`* (*lei simétrica*)
  + se *`A`* `=` *`B`* e *`B`* `=` *`C`*, então *`A`* `=` *`C`* (*lei transitiva*)
* O operador *`<`* deve ser uma relação de ordenação forte; ou seja, para todos os valores não nulos *`A`*, *`B`*, *`C`*:

+ *`A`* `<` *`A`* é falso (*lei irreflexiva*)
  + se *`A`* `<` *`B`* e *`B`* `<` *`C`*, então *`A`* `<` *`C`* (*lei transitiva*)
* Além disso, a ordem é total; ou seja, para todos os valores não nulos *`A`*, *`B`*:

+ exatamente um dos *`A`* `<` *`B`*, *`A`* `=` *`B`*, e *`B`* `<` *`A`* é verdadeiro (*lei de tricotomia*)

(A lei da tritomia justifica, claro, a definição da função de suporte de comparação.)

Os outros três operadores são definidos em termos de `=` e `<`, da maneira óbvia, e devem agir de forma consistente com eles.

Para uma família de operadores que suporta vários tipos de dados, as leis acima devem ser válidas quando *`A`*, *`B`*, *`C`* são retirados de qualquer tipo de dados na família. As leis transitivas são as mais difíceis de garantir, pois, em situações cruzadas, representam declarações de que os comportamentos de dois ou três operadores diferentes são consistentes. Como exemplo, não funcionaria colocar `float8` e `numeric` na mesma família de operadores, pelo menos não com a semântica atual de que os valores de `numeric` são convertidos em `float8` para comparação com um `float8`. Devido à precisão limitada de `float8`, isso significa que existem valores distintos de `numeric` que serão iguais ao mesmo valor de `float8`, e, portanto, a lei transitiva falharia.

Outra exigência para uma família de múltiplos tipos de dados é que quaisquer conversões implícitas ou de coerência binária que sejam definidas entre os tipos de dados incluídos na família do operador não devem alterar a ordem de classificação associada.

Deve ser bastante claro por que um índice btree requer que essas leis sejam mantidas dentro de um único tipo de dados: sem elas, não há ordenação para organizar as chaves. Além disso, as pesquisas de índice que utilizam uma chave de comparação de um tipo de dados diferente exigem comparações para se comportar de maneira saudável entre dois tipos de dados. As extensões para três ou mais tipos de dados dentro de uma família não são estritamente necessárias pelo próprio mecanismo do índice btree, mas o planejador depende delas para fins de otimização.

### 65.1.3. Funções de suporte a árvore B [#](#BTREE-SUPPORT-FUNCS)

Como mostrado na [Tabela 36.9][(xindex.md#XINDEX-BTREE-SUPPORT-TABLE "Table 36.9. B-Tree Support Functions")], btree define uma função de suporte obrigatória e cinco opcionais. Os seis métodos definidos pelo usuário são:

`order`: Para cada combinação de tipos de dados que uma família de operadores btree oferece operadores de comparação, ela deve fornecer uma função de suporte à comparação, registrada em `pg_amproc` com o número de função de suporte 1 e `amproclefttype`/`amprocrighttype` igual aos tipos de dados esquerda e direita para a comparação (ou seja, os mesmos tipos de dados com os quais os operadores de correspondência estão registrados em `pg_amop`). A função de comparação deve receber dois valores não nulos *`A`* e *`B`* e retornar um valor de `int32` que é `<`, `0`, `0` ou `>` `0` quando *`A`* [[`<`]*`B`, *`A`* [[`=`]*`B`*, ou *`A`* [[`>`]*`B`*, respectivamente. Um resultado nulo é desaconselhado: todos os valores do tipo de dados devem ser comparáveis. Consulte `src/backend/access/nbtree/nbtcompare.c` para exemplos.

Se os valores comparados forem de um tipo de dados compatível, o OID (Identificador de Ordenação) apropriado será passado para a função de suporte à comparação, utilizando o mecanismo padrão `PG_GET_COLLATION()`.

`sortsupport`: Opcionalmente, uma família de operadores btree pode fornecer *suporte para *sort**, funções registradas sob o número de suporte 2. Essas funções permitem a implementação de comparações para fins de ordenação de uma maneira mais eficiente do que simplesmente chamar a função de suporte para comparação. As APIs envolvidas nisso são definidas em `src/include/utils/sortsupport.h`.

`in_range`: Opcionalmente, uma família de operadores btree pode fornecer uma ou mais funções de suporte *in_range*, registradas sob o número de suporte 3. Essas funções não são usadas durante operações de índice btree; em vez disso, elas estendem a semântica da família de operadores para que ela possa suportar cláusulas de janela que contenham os tipos de limite de quadro `RANGE` *`offset`* `PRECEDING` e `RANGE` *`offset`* `FOLLOWING` (ver [Seção 4.2.8](sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS "4.2.8. Window Function Calls")). Fundamentalmente, a informação adicional fornecida é como adicionar ou subtrair um valor de *`offset`* de uma maneira compatível com a ordem de dados da família.

Uma função `in_range` deve ter a assinatura

``` in_range(val type1, base type1, offset type2, sub bool, less bool) returns bool
    ```

*`val`* e *`base`* devem ser do mesmo tipo, que é um dos tipos suportados pela família de operadores (ou seja, um tipo para o qual ela fornece uma ordenação). No entanto, *`offset`* pode ser de um tipo diferente, que pode ser outro que não seja suportado pela família. Um exemplo é que a família embutida `time_ops` fornece uma função `in_range` que tem *`offset`* do tipo `interval`. Uma família pode fornecer funções `in_range` para qualquer um dos seus tipos suportados e um ou mais tipos *`offset`*. Cada função `in_range` deve ser inserida em `pg_amproc` com `amproclefttype` igual a `type1` e `amprocrighttype` igual a `type2`.

A semântica essencial de uma função `in_range` depende dos dois parâmetros de sinalização booleanos. Ela deve adicionar ou subtrair *`base`* e *`offset`*, e então comparar *`val`* com o resultado, conforme segue:

* se `!`*`sub`* e `!`*`less`*, retorne *`val`* `>=` (*`base`* `+` *`offset`*)
* se `!`*`sub`* e *`less`*, retorne *`val`* `<=` (*`base`* `+` *`offset`*)
* se *`sub`* e `!`*`less`*, retorne *`val`* `>=` (*`base`* `-` *`offset`*)
* se *`sub`* e *`less`*, retorne *`val`* `<=` (*`base`* `-` *`offset`*)

Antes de fazer isso, a função deve verificar o sinal de *`offset`*: se for menor que zero, levante o erro `ERRCODE_INVALID_PRECEDING_OR_FOLLOWING_SIZE` (22013) com texto de erro como “tamanho anterior ou posterior inválido na função de janela”. (Isso é exigido pelo padrão SQL, embora famílias de operadores não padronizadas possam optar por ignorar essa restrição, uma vez que parece haver pouca necessidade semântica para isso.) Esse requisito é delegado à função `in_range` para que o código principal não precise entender o que significa “menor que zero” para um determinado tipo de dados.

Uma expectativa adicional é que `in_range` funcione, se possível, evitando lançar um erro se *`base`* `+` *`offset`* ou *`base`* `-` *`offset`* sobrecarregassem. O resultado da comparação correta pode ser determinado mesmo se esse valor estiver fora da faixa do tipo de dados. Observe que, se o tipo de dados incluir conceitos como “infinito” ou “NaN”, pode ser necessário um cuidado extra para garantir que os resultados de `in_range` estejam de acordo com a ordem de classificação normal da família de operadores.

Os resultados da função `in_range` devem ser consistentes com a ordem de classificação imposta pela família de operadores. Para ser preciso, dado quaisquer valores fixos de *`offset`* e *`sub`*, então:

* Se `in_range` com *`less`* = verdadeiro é verdadeiro para alguns *`val1`* e *`base`*, deve ser verdadeiro para todos os *`val2`* `<=` *`val1`* com o mesmo *`base`*.
* Se `in_range` com *`less`* = falso é falso para alguns *`val1`* e *`base`*, deve ser falso para todos os *`val2`* `>=` *`val1`* com o mesmo *`base`*.
* Se `in_range` com *`less`* = verdadeiro é verdadeiro para alguns *`val`* e *`base1`*, deve ser verdadeiro para todos os *`base2`* `>=` *`base1`* com o mesmo *`val`*.
* Se `in_range` com *`less`* = falso é falso para alguns *`val`* e *`base1`*, deve ser falso para todos os *`base2`* `<=` *`base1`* com o mesmo *`val`*.

Afirmações análogas com condições invertidas valem quando *`less`* = false.

Se o tipo que está sendo solicitado (`type1`) for colidível, o OID de colidência apropriado será passado para a função `in_range`, usando o mecanismo padrão PG_GET_COLLATION().

As funções `in_range` não precisam lidar com entradas NULL e, normalmente, serão marcadas como estritas.

`equalimage`: Opcionalmente, uma família de operadores btree pode fornecer funções de suporte `equalimage` (“igualdade implica igualdade de imagem”) registradas sob o número de função de suporte 4. Essas funções permitem que o código principal determine quando é seguro aplicar a otimização de deduplicação btree. Atualmente, as funções `equalimage` são chamadas apenas ao construir ou reconstruir um índice.

Uma função `equalimage` deve ter a assinatura

``` equalimage(opcintype oid) returns bool
    ```

O valor de retorno é uma informação estática sobre uma classe de operador e uma correção. A indicação de que o `order` da função para a classe de operador é garantido para retornar apenas `0` (“os argumentos são iguais”) quando seus argumentos *`A`* e
*`B`* também são intercambiáveis sem perda de informação semântica. Não registrar uma função `equalimage` ou retornar
`false` indica que essa condição não pode ser assumida como válida.

O argumento *`opcintype`* é o
    `pg_type.oid` do tipo de dados que o operador de índice. Esta é uma conveniência que permite a reutilização da mesma função subjacente
    `equalimage` em todas as classes de operador.
    Se *`opcintype`* for um tipo de dados coletável, o OID (Identificador de Ordenação) apropriado será passado para a função
    `equalimage`, usando o mecanismo padrão
    `PG_GET_COLLATION()`.

No que diz respeito à classe do operador, o retorno de
`true` indica que a deduplicação é segura (ou segura para a
coluna de ordenação cujo OID foi passado para sua
`equalimage` função). No entanto, o código principal só considerará a deduplicação segura para um índice quando
*cada* coluna indexada usa uma classe do operador
que registra uma função `equalimage`, e
cada função realmente retorna `true` quando
chamada.

A igualdade de imagem é *quase* a mesma condição que a simples igualdade de bits. Há uma diferença sutil: ao indexar um tipo de dados varlena, a representação no disco de dois pontos de dados iguais em termos de imagem pode não ser igual em termos de bits devido à aplicação inconsistente da compressão TOAST no input.
Formalmente, quando a função `equalimage` de uma classe de operadores retorna `true`, é seguro assumir que a função C `datum_image_eq()` sempre concordará com a função `order` da classe de operadores (desde que o mesmo OID de collation seja passado para ambas as funções `equalimage` e `order`).

O código central não é fundamentalmente capaz de deduzir nada sobre o status de "igualdade implica igualdade de imagem" de uma classe de operadores dentro de uma família de vários tipos de dados com base em detalhes de outras classes de operadores da mesma família. Além disso, não é sensato que uma família de operadores registre uma função de cruzamento `equalimage`, e tentar fazer isso resultará em um erro. Isso ocorre porque o status de "igualdade implica igualdade de imagem" não depende apenas da semântica de classificação/igualdade, que são mais ou menos definidas no nível da família de operadores. Em geral, a semântica que um tipo de dados específico implementa deve ser considerada separadamente.

A convenção seguida pelas classes de operador incluídas na distribuição principal do PostgreSQL é registrar uma função de estoque, a função `equalimage` genérica. A maioria das classes de operador registra `btequalimage()`, o que indica que a deduplicação é segura incondicionalmente. As classes de operador para tipos de dados coletáveis, como `text`, registram `btvarstrequalimage()`, o que indica que a deduplicação é segura com colatâncias determinísticas. A melhor prática para extensões de terceiros é registrar sua própria função personalizada para manter o controle.

`options` Opcionalmente, uma família de operadores de árvore B pode fornecer funções de suporte a opções específicas de classe de operador, registradas sob o número de função de suporte 5. Essas funções definem um conjunto de parâmetros visíveis ao usuário que controlam o comportamento da classe de operador.

Uma função de suporte `options` deve ter a assinatura

    ```
    options(relopts local_relopts *) returns void
    ```

A função recebe um ponteiro para uma estrutura `local_relopts`, que precisa ser preenchida com um conjunto de opções específicas para a classe de operador. As opções podem ser acessadas a partir de outras funções de suporte usando as macros `PG_HAS_OPCLASS_OPTIONS()` e `PG_GET_OPCLASS_OPTIONS()`.

Atualmente, nenhuma classe de operador de B-Tree tem uma função de suporte `options`. O B-Tree não permite representação flexível de chaves como GiST, SP-GiST, GIN e BRIN. Portanto, `options` provavelmente não tem muita aplicação no método atual de acesso ao índice B-Tree. No entanto, essa função de suporte foi adicionada ao B-Tree para uniformidade e provavelmente encontrará usos durante a evolução adicional do B-Tree no PostgreSQL.

`skipsupport`
: Opcionalmente, uma família de operadores btree pode fornecer uma função de *skip* de suporte, registrada sob o número de função de suporte 6. Essas funções dão ao código B-tree uma maneira de iterar por todos os valores possíveis que podem ser representados pelo tipo de entrada subjacente de uma classe de operadores, em ordem do espaço de chave. Isso é usado pelo código principal quando ele aplica a otimização de varredura de skip. As APIs envolvidas nisso são definidas em `src/include/utils/skipsupport.h`.

As classes de operador que não fornecem uma função de suporte para pular ainda são elegíveis para usar varredura de pular. O código principal ainda pode usar sua estratégia de fallback, embora isso possa ser subótimo para alguns tipos discretos. Geralmente não faz sentido (e pode não ser até viável) para classes de operador em tipos contínuos fornecer uma função de suporte para pular.

Não é sensato que uma família de operadores registre uma função de tipo cruzamento, e tentar fazer isso resultará em um erro. Isso ocorre porque a determinação do próximo valor indexável deve ocorrer ao incrementar um valor copiado de um par de índice. Os valores gerados devem ser todos do mesmo tipo de dados subjacente (o tipo de entrada opclass da coluna de índice "escondida").

### 65.1.4. Implementação [#](#BTREE-IMPLEMENTATION)

Esta seção abrange detalhes da implementação do índice B-Tree que podem ser úteis para usuários avançados. Consulte `src/backend/access/nbtree/README` na distribuição de fonte para uma descrição muito mais detalhada, focada nos aspectos internos, da implementação do B-Tree.

#### 65.1.4.1. Estrutura de B-Tree [#](#BTREE-STRUCTURE)

Os índices B-Tree do PostgreSQL são estruturas de árvore multi-nível, onde cada nível da árvore pode ser usado como uma lista de páginas duplamente vinculada. Uma única metapágina é armazenada em uma posição fixa no início do primeiro arquivo de segmento do índice. Todas as outras páginas são páginas de folha ou páginas internas.
Páginas de folha são as páginas no nível mais baixo da árvore. Todos os outros níveis consistem em páginas internas. Cada página de folha contém tuplas que apontam para linhas de tabela. Cada página interna contém tuplas que apontam para o nível seguinte na árvore. Tipicamente, mais de 99% de todas as páginas são páginas de folha. Tanto as páginas internas quanto as páginas de folha usam o formato de página padrão descrito em [Seção 66.6] [(storage-page-layout.md "66.6. Database Page Layout")].

Novas páginas de folha são adicionadas a um índice B-Tree quando uma página de folha existente não consegue acomodar uma tupla de entrada. Uma operação de *divisão de página* faz espaço para itens que originalmente pertenciam à página transbordante, movendo uma parte dos itens para uma nova página. As divisões de página também devem inserir um novo *downlink* na nova página na página pai, o que pode fazer com que o pai se divida por sua vez. As divisões de página "cascam para cima" de forma recursiva. Quando a página raiz finalmente não consegue acomodar um novo downlink, uma operação de *divisão de página de raiz* ocorre. Isso adiciona um novo nível à estrutura da árvore, criando uma nova página raiz que está um nível acima da página raiz original.

#### 65.1.4.2. Remoção do Índice de baixo para cima [#](#BTREE-DELETION)

Os índices B-Tree não são diretamente conscientes de que, sob MVCC, pode haver múltiplas versões existentes da mesma linha de tabela lógica; para um índice, cada tupla é um objeto independente que precisa de sua própria entrada de índice. As tuplas de "mudança de versão" podem, às vezes, acumular e afetar negativamente a latência e o desempenho da consulta. Isso geralmente ocorre com cargas de trabalho `UPDATE`-pesadas, onde a maioria das atualizações individuais não pode aplicar a otimização [HOT]. (storage-hot.md "66.7. Heap-Only Tuples (HOT)])
Mudar o valor de apenas uma coluna coberta por um índice durante uma `UPDATE` *sempre* necessita de um novo conjunto de tuplas de índice — uma para *cada e todo* índice na tabela. Note, em particular, que isso inclui índices que não foram "logicamente modificados" pelo `UPDATE`. Todos os índices precisarão de uma tupla física de índice sucessor que aponte para a versão mais recente na tabela. Cada nova tupla dentro de cada índice geralmente precisará coexistir com a tupla "atualizada" original por um curto período de tempo (tipicamente até pouco depois do `UPDATE` transação
commit).

Os índices B-Tree excluem incrementalmente tuplos do índice de churn de versão realizando passes de *exclusão de índice de baixo para cima*. Cada passagem de exclusão é acionada em reação a uma divisão de página de "churn de versão" antecipada. Isso ocorre apenas com índices que não são logicamente modificados por declarações de `UPDATE`, onde o acúmulo concentrado de versões obsoletas em páginas específicas ocorreria de outra forma. Uma divisão de página geralmente será evitada, embora seja possível que certas heurísticas de nível de implementação não identifiquem e excluam até mesmo uma tupla de índice de lixo (nesse caso, uma passagem de divisão de página ou deduplicação resolve o problema de uma nova tupla de entrada que não cabe em uma página foliar). O número máximo de versões que qualquer varredura de índice deve percorrer (para qualquer linha lógica única) é um contribuinte importante para a responsividade e o desempenho do sistema como um todo. Uma passagem de exclusão de índice de baixo para cima visa tuplas de lixo suspeitas em uma única página foliar com base em *distinções qualitativas* envolvendo linhas lógicas e versões. Isso contrasta com a limpeza de índice "de cima para baixo" realizada pelos trabalhadores do autovacuum, que é acionada quando certos limiares *quantitativos* de nível de tabela são excedidos (ver [Seção 24.1.6][(routine-vacuuming.md#AUTOVACUUM "24.1.6. The Autovacuum Daemon")]).

### Nota

Nem todas as operações de exclusão que são realizadas dentro de índices B-Tree são operações de exclusão de baixo para cima. Há uma categoria distinta de exclusão de tuplas de índice: *exclusão simples de tupla de índice*. Esta é uma operação de manutenção diferida que exclui tuplas de índice que são conhecidas como seguras para serem excluídas (aqueles cujo bit `LP_DEAD` do identificador do item já está definido). Assim como a exclusão de índice de baixo para cima, a exclusão simples de índice ocorre no ponto em que uma divisão de página é antecipada como uma maneira de evitar a divisão.

A eliminação simples é oportunista no sentido de que só pode ocorrer quando os recentes varreduras de índice definem os bits dos itens afetados de passagem.
Antes do PostgreSQL 14, a única categoria de eliminação de B-Tree era a eliminação simples. As principais diferenças entre ela e a eliminação de cima para baixo são que apenas a primeira é oportunisticamente impulsionada pela atividade de varreduras de índice, enquanto apenas a segunda visa especificamente a mudança de versão dos `UPDATE`s que não modificam logicamente as colunas indexadas.

A exclusão de índice de baixo para cima realiza a grande maioria de todas as limpezas de tupla de índice para índices específicos com certos encargos de trabalho.
Isso é esperado com qualquer índice B-Tree que seja sujeito a
mudança significativa de versões de `UPDATE`s que
raramente ou nunca modificam logicamente as colunas que o índice cobre.
O número médio e o pior caso de versões por linha lógica podem ser mantidos baixo puramente por meio de passes de exclusão incremental direcionados.
É bastante possível que o tamanho em disco de certos índices nunca aumente nem mesmo uma única página/bloco, apesar
*constante* de mudanças de versão de
`UPDATE`s. Mesmo assim, uma "limpeza completa" por uma operação de `VACUUM` (tipicamente
executada em um processo de trabalhador de autovazamento) será eventualmente necessária como
parte da *limpeza coletiva* da tabela e
cada um de seus índices.

Ao contrário de `VACUUM`, a exclusão de índices de baixo para cima não oferece garantias fortes sobre a idade do mais antigo tupla do índice de lixo. Nenhum índice pode ser permitido reter tuplas de índice de "lixo flutuante" que se tornaram mortas antes de um ponto de corte conservador compartilhado pela tabela e por todos os seus índices coletivamente. Esta invariável fundamental a nível de tabela torna seguro reciclar TIDs de tabela. É assim que é possível que linhas lógicas distintas reutilizem o mesmo TID ao longo do tempo (embora isso nunca possa acontecer com duas linhas lógicas cujos períodos de vida abrangem o mesmo ciclo `VACUUM`).

#### 65.1.4.3. Deduplicação [#](#BTREE-DEDUPLICATION)

Um duplicado é um tuplo de página de folha (um tuplo que aponta para uma linha de tabela) onde *todos* os colun
ais de chave indexados têm valores que correspondem aos valores da coluna correspondente de pelo menos uma outra tupla de página de folha no mesmo índice. Tuples duplicados são bastante comuns na prática. Os índices B-Tree podem usar uma representação especial, eficiente em termos de espaço, para duplicados quando uma técnica opcional é habilitada: *deduplicação*.

A eliminação de duplicatas funciona periodicamente, unindo grupos de tuplas duplicadas juntas, formando uma única tupla de *lista de postagens* para cada grupo. O(s) valor(es) da chave da coluna aparecem apenas uma vez nessa representação. Isso é seguido por um array ordenado de TIDs que apontam para linhas na tabela. Isso reduz significativamente o tamanho de armazenamento dos índices, onde cada valor (ou cada combinação distinta de valores de coluna) aparece várias vezes em média. A latência das consultas pode ser reduzida significativamente. O desempenho geral das consultas pode aumentar significativamente. O custo operacional do rastreamento de rotina de índices também pode ser reduzido significativamente.

### Nota

A deduplicação de B-Tree é igualmente eficaz com “duplicatas” que contêm um valor NULL, embora os valores NULL nunca sejam iguais entre si de acordo com o membro `=` de qualquer classe de operador de B-Tree. No que diz respeito a qualquer parte da implementação que compreenda a estrutura de B-Tree em disco, NULL é apenas outro valor do domínio de valores indexados.

O processo de deduplicação ocorre de forma preguiçosa, quando um novo item é inserido que não cabe em uma página de folha existente, embora apenas quando a exclusão do par ordenado do índice não conseguiu liberar espaço suficiente para o novo item (tipicamente, a exclusão é considerada brevemente e depois ignorada). Ao contrário dos tuplos da lista de publicação do GIN, os tuplos da lista de publicação do B-Tree não precisam expandir a cada vez que um novo duplicado é inserido; eles são meramente uma representação física alternativa dos conteúdos lógicos originais da página de folha. Esse design prioriza o desempenho consistente com cargas de trabalho mistas de leitura e escrita. A maioria dos aplicativos de cliente verá pelo menos um benefício moderado de desempenho ao usar a deduplicação. A deduplicação é habilitada por padrão.

`CREATE INDEX` e `REINDEX` aplicam a deduplicação para criar tuplos da lista de postagens, embora a estratégia que utilizam seja um pouco diferente. Cada grupo de tuplos comuns encontrados no conjunto de entrada ordenado retirado da tabela é fundido em um tuplo da lista de postagens *antes* de ser adicionado à página atual de folha pendente. Tuplos individuais da lista de postagens são embalados com o maior número possível de TIDs. As páginas de folha são escritas da maneira usual, sem qualquer passagem de deduplicação separada. Essa estratégia é adequada para `CREATE INDEX` e `REINDEX`, porque são operações de lote únicas.

Trabalhos pesados que não se beneficiam da desduplicação devido ao fato de terem poucos ou nenhum valor duplicado nos índices terão uma pequena penalidade de desempenho fixa (a menos que a desduplicação seja explicitamente desativada). O parâmetro de armazenamento `deduplicate_items` pode ser usado para desativar a desduplicação dentro de índices individuais. Nunca há penalidade de desempenho com cargas de trabalho somente de leitura, uma vez que a leitura de tuplas da lista de postagens é pelo menos tão eficiente quanto a leitura da representação padrão de tupla. Desativar a desduplicação geralmente não é útil.

Às vezes, é possível que índices únicos (assim como restrições únicas) utilizem a deduplicação. Isso permite que as páginas de folha "absorvam" temporariamente duplicatas extras de churn de versão. A deduplicação em índices únicos aumenta a eliminação de índice de baixo para cima, especialmente em casos em que uma transação de longa duração mantém um instantâneo que bloqueia a coleta de lixo. O objetivo é comprar tempo para que a estratégia de eliminação de índice de baixo para cima se torne eficaz novamente. Aguardar as divisões de página até que uma única transação de longa duração desapareça naturalmente pode permitir que uma passagem de eliminação de baixo para cima seja bem-sucedida onde uma passagem de eliminação anterior falhou.

### DICA

Uma heurística especial é aplicada para determinar se uma passagem de descaracterização em um índice único deve ocorrer. Ela pode, muitas vezes, pular diretamente para a divisão de uma página de folha, evitando uma penalização de desempenho ao desperdiçar ciclos em passagens de descaracterização inúteis. Se você está preocupado com o custo da descaracterização, considere definir `deduplicate_items = off` seletivamente. Deixar a descaracterização habilitada em índices únicos tem pouca desvantagem.

A eliminação de duplicatas não pode ser usada em todos os casos devido a restrições de nível de implementação. A segurança da eliminação de duplicatas é determinada quando `CREATE INDEX` ou `REINDEX` é executado.

Observe que a deduplicação é considerada insegura e não pode ser usada nos seguintes casos que envolvem diferenças semanticamente significativas entre datas iguais:

* `text`, `varchar` e `char`
não podem usar deduplicação quando uma
* não determinística* é usada. As diferenças de caso e acentos devem ser preservadas entre datas iguais.
* `numeric` não pode usar deduplicação. A escala de exibição numérica deve ser preservada entre datas iguais.
* `jsonb` não pode usar deduplicação, uma vez que a
* `jsonb` classe de operador B-Tree usa
* `numeric` internamente.
* `float4` e `float8` não podem usar
  duplicação. Esses tipos têm representações distintas para
  `-0` e `0`, que, no entanto, são
  consideradas iguais. Essa diferença deve ser
  preservada.

Há uma restrição adicional em nível de implementação que pode ser
removida em uma versão futura do
PostgreSQL:

* Os tipos de contêiner (como tipos compostos, matrizes ou tipos de intervalo) não podem usar deduplicação.

Há uma restrição adicional em nível de implementação que se aplica
independentemente da classe do operador ou da codificação usada:

* Os índices `INCLUDE` nunca podem usar desduplicação.