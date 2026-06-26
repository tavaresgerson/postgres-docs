## 65.3. Índices SP-GiST [#](#SPGIST)

* [65.3.1. Introdução](spgist.md#SPGIST-INTRO)
* [65.3.2. Classes Operadoras Integradas](spgist.md#SPGIST-BUILTIN-OPCLASSES)
* [65.3.3. Extensibilidade](spgist.md#SPGIST-EXTENSIBILITY)
* [65.3.4. Implementação](spgist.md#SPGIST-IMPLEMENTATION)
* [65.3.5. Exemplos](spgist.md#SPGIST-EXAMPLES)

### 65.3.1. Introdução [#](#SPGIST-INTRO)

SP-GiST é uma abreviação para GiST com partição espacial. O SP-GiST suporta árvores de busca com partição, o que facilita o desenvolvimento de uma ampla gama de diferentes estruturas de dados não balanceadas, como quad-trees, k-d trees e radix trees (tries). A característica comum dessas estruturas é que elas dividem repetidamente o espaço de busca em partições que não precisam ter o mesmo tamanho. Pesquisas que estão bem alinhadas com a regra de partição podem ser muito rápidas.

Essas estruturas de dados populares foram originalmente desenvolvidas para uso em memória. Na memória principal, elas são geralmente projetadas como um conjunto de nós dinamicamente alocados ligados por ponteiros. Isso não é adequado para armazenamento direto em disco, pois essas cadeias de ponteiros podem ser bastante longas, o que exigiria muitos acessos ao disco. Em contraste, estruturas de dados baseadas em disco devem ter uma alta ramificação para minimizar o I/O. O desafio abordado pelo SP-GiST é mapear os nós da árvore de busca em páginas de disco de tal forma que uma busca precise acessar apenas algumas páginas de disco, mesmo que percorra muitos nós.

Assim como o GiST, o SP-GiST é projetado para permitir o desenvolvimento de tipos de dados personalizados com os métodos de acesso apropriados, por um especialista no domínio do tipo de dados, e não por um especialista em banco de dados.

Algumas das informações aqui contidas são derivadas do Projeto de Indicação SP-GiST da Universidade Purdue [site web](https://www.cs.purdue.edu/spgist/). A implementação SP-GiST no PostgreSQL é mantida principalmente por Teodor Sigaev e Oleg Bartunov, e há mais informações em seu [site web](http://www.sai.msu.su/~megera/wiki/spgist_dev).

### 65.3.2. Classes de operador embutidas [#](#SPGIST-BUILTIN-OPCLASSES)

A distribuição principal do PostgreSQL inclui as classes de operadores SP-GiST mostradas na [Tabela 65.2](spgist.md#SPGIST-BUILTIN-OPCLASSES-TABLE).

**Tabela 65.2. Classes de operadores SP-GiST integrados**



<table>
 <colgroup>
  <col/>
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
   <th>
    Ordering Operators
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td rowspan="12" valign="middle">
    <code>
     box_ops
    </code>
   </td>
   <td>
    <code>
     &lt;&lt; (box,box)
    </code>
   </td>
   <td rowspan="12" valign="middle">
    <code>
     &lt;-&gt; (box,point)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &amp;&lt; (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &amp;&gt; (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &gt;&gt; (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt;@ (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     @&gt; (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ~= (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &amp;&amp; (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt;&lt;| (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &amp;&lt;| (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     |&amp;&gt; (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     |&gt;&gt; (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="11" valign="middle">
    <code>
     inet_ops
    </code>
   </td>
   <td>
    <code>
     &lt;&lt; (inet,inet)
    </code>
   </td>
   <td rowspan="11" valign="middle">
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt;&lt;= (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &gt;&gt; (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &gt;&gt;= (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     = (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt;&gt; (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt; (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt;= (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &gt; (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &gt;= (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &amp;&amp; (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="6" valign="middle">
    <code>
     kd_point_ops
    </code>
   </td>
   <td>
    <code>
     |&gt;&gt; (point,point)
    </code>
   </td>
   <td rowspan="6" valign="middle">
    <code>
     &lt;-&gt; (point,point)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt;&lt; (point,point)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &gt;&gt; (point,point)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt;&lt;| (point,point)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ~= (point,point)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt;@ (point,box)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="12" valign="middle">
    <code>
     poly_ops
    </code>
   </td>
   <td>
    <code>
     &lt;&lt; (polygon,polygon)
    </code>
   </td>
   <td rowspan="12" valign="middle">
    <code>
     &lt;-&gt; (polygon,point)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &amp;&lt; (polygon,polygon)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &amp;&gt; (polygon,polygon)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &gt;&gt; (polygon,polygon)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt;@ (polygon,polygon)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     @&gt; (polygon,polygon)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ~= (polygon,polygon)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &amp;&amp; (polygon,polygon)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt;&lt;| (polygon,polygon)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &amp;&lt;| (polygon,polygon)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     |&gt;&gt; (polygon,polygon)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     |&amp;&gt; (polygon,polygon)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="6" valign="middle">
    <code>
     quad_point_ops
    </code>
   </td>
   <td>
    <code>
     |&gt;&gt; (point,point)
    </code>
   </td>
   <td rowspan="6" valign="middle">
    <code>
     &lt;-&gt; (point,point)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt;&lt; (point,point)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &gt;&gt; (point,point)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt;&lt;| (point,point)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ~= (point,point)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt;@ (point,box)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="10" valign="middle">
    <code>
     range_ops
    </code>
   </td>
   <td>
    <code>
     = (anyrange,anyrange)
    </code>
   </td>
   <td rowspan="10" valign="middle">
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &amp;&amp; (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     @&gt; (anyrange,anyelement)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     @&gt; (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt;@ (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt;&lt; (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &gt;&gt; (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &amp;&lt; (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &amp;&gt; (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     -|- (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="10" valign="middle">
    <code>
     text_ops
    </code>
   </td>
   <td>
    <code>
     = (text,text)
    </code>
   </td>
   <td rowspan="10" valign="middle">
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt; (text,text)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &lt;= (text,text)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &gt; (text,text)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     &gt;= (text,text)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ~&lt;~ (text,text)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ~&lt;=~ (text,text)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ~&gt;=~ (text,text)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ~&gt;~ (text,text)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ^@ (text,text)
    </code>
   </td>
  </tr>
 </tbody>
</table>










Das duas classes de operadores para o tipo `point`, `quad_point_ops` é o padrão. `kd_point_ops` suporta os mesmos operadores, mas utiliza uma estrutura de dados de índice diferente que pode oferecer melhor desempenho em algumas aplicações.

As classes de operadores `quad_point_ops`, `kd_point_ops` e `poly_ops` suportam o operador de ordenação `<->`, que permite a busca do vizinho k mais próximo (`k-NN`) sobre conjuntos de dados de pontos ou polígonos indexados.

### 65.3.3. Extensibilidade [#](#SPGIST-EXTENSIBILITY)

O SP-GiST oferece uma interface com um alto nível de abstração, exigindo que o desenvolvedor do método de acesso implemente apenas métodos específicos para um determinado tipo de dados. O núcleo SP-GiST é responsável pelo mapeamento eficiente do disco e pela pesquisa na estrutura de árvore. Também cuida das considerações de concorrência e registro.

Os tuplos de folha de uma árvore SP-GiST geralmente contêm valores do mesmo tipo de dados que a coluna indexada, embora também seja possível que eles contenham representações perdidas da coluna indexada. Os tuplos de folha armazenados no nível raiz representarão diretamente o valor original do dado indexado, mas os tuplos de folha em níveis inferiores podem conter apenas um valor parcial, como um sufixo. Nesse caso, as funções de suporte da classe de operadores devem ser capazes de reconstruir o valor original usando informações acumuladas dos tuplos internos que são passados para alcançar o nível de folha.

Quando um índice SP-GiST é criado com colunas `INCLUDE`, os valores dessas colunas também são armazenados em tuplas de folha. As colunas `INCLUDE` não interessam à classe de operadores SP-GiST, portanto, não são discutidas mais detalhadamente aqui.

Os tuplos internos são mais complexos, pois são pontos de ramificação no árvore de busca. Cada tuplo interno contém um conjunto de um ou mais *nós*, que representam grupos de valores de folha semelhantes. Um nó contém um link descendente que leva a outro, um nível mais baixo, tuplo interno, ou a uma lista curta de tuplos de folha que todos estão no mesmo índice. Cada nó normalmente tem um *rótulo* que o descreve; por exemplo, em uma árvore de radix, o rótulo do nó poderia ser o próximo caractere do valor da string. (Alternativamente, uma classe de operadores pode omitir os rótulos dos nós, se trabalha com um conjunto fixo de nós para todos os tuplos internos; veja [Seção 65.3.4.2](spgist.md#SPGIST-NULL-LABELS). Opcionalmente, um tuplo interno pode ter um valor *prefixo* que descreve todos os seus membros. Em uma árvore de radix, isso poderia ser o prefixo comum das strings representadas. O valor do prefixo não é necessariamente um prefixo real, mas pode ser qualquer dado necessário pela classe de operadores; por exemplo, em uma quad-tree, pode armazenar o ponto central com o qual os quatro quadrantes são medidos. Um tuplo interno de quad-tree também conterá então quatro nós correspondentes aos quadrantes ao redor deste ponto central.

Alguns algoritmos de árvores exigem conhecimento do nível (ou profundidade) do conjunto atual, portanto, o núcleo SP-GiST oferece a possibilidade para as classes de operadores gerenciarem o contagem de nível ao descer a árvore. Há também suporte para reconstruir incrementalmente o valor representado quando isso for necessário, e para passar dados adicionais (chamados de *valores de travessia*) durante uma descida da árvore.

Nota

O código-fonte do SP-GiST cuida das entradas nulos. Embora os índices do SP-GiST armazenem entradas para nulos em colunas indexadas, isso é oculto do código da classe do operador de índice: nenhuma entrada de índice nulo ou condições de busca serão passadas para os métodos da classe do operador. (Assume-se que os operadores SP-GiST são estritos e, portanto, não podem ter sucesso para valores nulos.) Valores nulos, portanto, não são discutidos mais aqui.

Há cinco métodos definidos pelo usuário que uma classe de operador de índice para SP-GiST deve fornecer, e dois são opcionais. Todos os cinco métodos obrigatórios seguem a convenção de aceitar dois argumentos `internal`, sendo o primeiro um ponteiro para uma estrutura C que contém valores de entrada para o método de suporte, enquanto o segundo argumento é um ponteiro para uma estrutura C onde os valores de saída devem ser colocados. Quatro dos métodos obrigatórios simplesmente retornam `void`, uma vez que todos os seus resultados aparecem na estrutura de saída; mas `leaf_consistent` retorna um resultado `boolean`. Os métodos não devem modificar nenhum campo das suas estruturas de entrada. Em todos os casos, a estrutura de saída é inicializada com zeros antes de chamar o método definido pelo usuário. O método opcional sexto `compress` aceita um `datum` a ser indexado como o único argumento e retorna um valor adequado para armazenamento físico em um tuplo de folha. O método opcional sétimo `options` aceita um ponteiro `internal` para uma estrutura C, onde os parâmetros específicos da opclass devem ser colocados, e retorna `void`.

Os cinco métodos obrigatórios definidos pelo usuário são:

`config`: Retorna informações estáticas sobre a implementação do índice, incluindo os tipos de ID de dados do tipo de dados de rótulo de prefixo e nó.

A declaração SQL da função deve parecer assim:

```
CREATE FUNCTION my_config(internal, internal) RETURNS void ...
```

O primeiro argumento é um ponteiro para uma `spgConfigIn` C struct, contendo dados de entrada para a função. O segundo argumento é um ponteiro para uma `spgConfigOut` C struct, que a função deve preencher com dados de resultado.

```
typedef struct spgConfigIn { Oid         attType;        /* Data type to be indexed */ } spgConfigIn;

typedef struct spgConfigOut { Oid         prefixType;     /* Data type of inner-tuple prefixes */ Oid         labelType;      /* Data type of inner-tuple node labels */ Oid         leafType;       /* Data type of leaf-tuple values */ bool        canReturnData;  /* Opclass can reconstruct original data */ bool        longValuesOK;   /* Opclass can cope with values > 1 page */ } spgConfigOut;
```

`attType` é passado para suportar classes de operadores de índice polimórfico; para as classes de operadores de dados fixos comuns, ele sempre terá o mesmo valor e, portanto, pode ser ignorado.

Para as classes de operador que não utilizam prefixos, `prefixType` pode ser definido como `VOIDOID`. Da mesma forma, para as classes de operador que não utilizam rótulos de nó, `labelType` pode ser definido como `VOIDOID`. `canReturnData` deve ser definido como verdadeiro se a classe de operador for capaz de reconstruir o valor do índice fornecido originalmente. `longValuesOK` deve ser definido como verdadeiro apenas quando o `attType` tem comprimento variável e a classe de operador é capaz de segmentar valores longos por sufixação repetida (ver [Seção 65.3.4.1] (spgist.md#SPGIST-LIMITS "65.3.4.1. SP-GiST Limits")).

`leafType` deve corresponder ao tipo de armazenamento de índice definido pela entrada de catálogo da classe de operador `opckeytype`. (Observe que `opckeytype` pode ser zero, o que implica que o tipo de armazenamento é o mesmo que o tipo de entrada da classe de operador, que é a situação mais comum). Por razões de compatibilidade reversa, o método `config` pode definir `leafType` para outro valor, e esse valor será usado; mas isso é desaconselhável, uma vez que o conteúdo do índice é então identificado incorretamente nos catálogos. Além disso, é permitido deixar `leafType` não inicializado (zero); isso é interpretado como significando que o tipo de armazenamento de índice derivado de `opckeytype`.

Quando `attType` e `leafType` são diferentes, o método opcional `compress` deve ser fornecido. O método `compress` é responsável pela transformação de dados a serem indexados de `attType` para `leafType`.

`choose`: Escolha um método para inserir um novo valor em um par ordenado interno.

A declaração SQL da função deve parecer assim:

```
CREATE FUNCTION my_choose(internal, internal) RETURNS void ...
```

O primeiro argumento é um ponteiro para uma estrutura `spgChooseIn` C, contendo dados de entrada para a função. O segundo argumento é um ponteiro para uma estrutura `spgChooseOut` C, que a função deve preencher com dados de resultado.

```
typedef struct spgChooseIn { Datum       datum;          /* original datum to be indexed */ Datum       leafDatum;      /* current datum to be stored at leaf */ int         level;          /* current level (counting from zero) */

    /* Data from current inner tuple */ bool        allTheSame;     /* tuple is marked all-the-same? */ bool        hasPrefix;      /* tuple has a prefix? */ Datum       prefixDatum;    /* if so, the prefix value */ int         nNodes;         /* number of nodes in the inner tuple */ Datum      *nodeLabels;     /* node label values (NULL if none) */ } spgChooseIn;

typedef enum spgChooseResultType { spgMatchNode = 1,           /* descend into existing node */ spgAddNode,                 /* add a node to the inner tuple */ spgSplitTuple               /* split inner tuple (change its prefix) */ } spgChooseResultType;

typedef struct spgChooseOut { spgChooseResultType resultType;     /* action code, see above */ union { struct                  /* results for spgMatchNode */ { int         nodeN;      /* descend to this node (index from 0) */ int         levelAdd;   /* increment level by this much */ Datum       restDatum;  /* new leaf datum */ }           matchNode; struct                  /* results for spgAddNode */ { Datum       nodeLabel;  /* new node's label */ int         nodeN;      /* where to insert it (index from 0) */ }           addNode; struct                  /* results for spgSplitTuple */ { /* Info to form new upper-level inner tuple with one child tuple */ bool        prefixHasPrefix;    /* tuple should have a prefix? */ Datum       prefixPrefixDatum;  /* if so, its value */ int         prefixNNodes;       /* number of nodes */ Datum      *prefixNodeLabels;   /* their labels (or NULL for
                                             * no labels) */ int         childNodeN;         /* which node gets child tuple */

            /* Info to form new lower-level inner tuple with all old nodes */ bool        postfixHasPrefix;   /* tuple should have a prefix? */ Datum       postfixPrefixDatum; /* if so, its value */ }           splitTuple; }           result; } spgChooseOut;
```

`datum` é o dado original `spgConfigIn`.`attType` do tipo que deve ser inserido no índice. `leafDatum` é um valor do `spgConfigOut`.`leafType` tipo, que inicialmente é resultado do método `compress` aplicado ao `datum` quando o método `compress` é fornecido, ou o mesmo valor que `datum` caso contrário. `leafDatum` pode mudar em níveis inferiores da árvore se os métodos `choose` ou `picksplit` o mudarem. Quando a busca de inserção atinge uma página de folha, o valor atual de `leafDatum` é o que será armazenado no novo par de folha criado. `level` é o nível do par interno atual, começando em zero para o nível da raiz. `allTheSame` é verdadeiro se o par interno atual está marcado como contendo múltiplos nós equivalentes (ver [Seção 65.3.4.3](spgist.md#SPGIST-ALL-THE-SAME "65.3.4.3. “All-the-Same” Inner Tuples")). `hasPrefix` é verdadeiro se o par interno atual contém um prefixo; se assim for, `prefixDatum` é seu valor. `nNodes` é o número de nós filhos contidos no par interno, e `nodeLabels` é um array de seus valores de rótulo, ou NULL se não houver rótulos.

A função `choose` pode determinar que o novo valor corresponde a um dos nós filhos existentes, ou que um novo nó filho deve ser adicionado, ou que o novo valor é inconsistente com o prefixo do conjunto de tuplas e, portanto, o conjunto de tuplas interno deve ser dividido para criar um prefixo menos restritivo.

Se o novo valor corresponder a um dos nós filhos existentes, defina `resultType` como `spgMatchNode`. Defina `nodeN` como o índice (a partir de zero) desse nó na matriz de nós. Defina `levelAdd` como o incremento em `level` causado pela descida por esse nó, ou deixe-o como zero se a classe do operador não usar níveis. Defina `restDatum` igual a `leafDatum` se a classe do operador não modificar datas de um nível para o próximo, ou, caso contrário, defina-o no valor modificado a ser usado como `leafDatum` no nível seguinte.

Se um novo nó filho precisar ser adicionado, defina `resultType` como `spgAddNode`. Defina `nodeLabel` como o rótulo a ser usado para o novo nó, e defina `nodeN` como o índice (a partir de zero) em que inserir o nó na matriz de nós. Após o nó ter sido adicionado, a função `choose` será chamada novamente com o par interno modificado; Essa chamada deve resultar em um resultado `spgMatchNode`.

Se o novo valor for inconsistente com o prefixo do tuplo, defina `resultType` como `spgSplitTuple`. Essa ação move todos os nós existentes para um novo tuplo interno de nível inferior e substitui o tuplo interno existente por um que tem um único downlink apontando para o novo tuplo interno de nível inferior. Defina `prefixHasPrefix` para indicar se o novo tuplo superior deve ter um prefixo, e, se sim, defina `prefixPrefixDatum` com o valor do prefixo. Esse novo valor de prefixo deve ser suficientemente menos restritivo que o original para aceitar o novo valor indexado. Defina `prefixNNodes` como o número de nós necessários no novo tuplo, e defina `prefixNodeLabels` como um array palloc que contém suas etiquetas, ou como NULL se as etiquetas dos nós não forem necessárias. Observe que o tamanho total do novo tuplo superior não deve ser maior que o tamanho total do tuplo que está sendo substituído; isso restringe as longitudes do novo prefixo e novas etiquetas. Defina `childNodeN` como o índice (de zero) do nó que fará downlink para o novo tuplo interno de nível inferior. Defina `postfixHasPrefix` para indicar se o novo tuplo interno de nível inferior deve ter um prefixo, e, se sim, defina `postfixPrefixDatum` com o valor do prefixo. A combinação desses dois prefixos e a etiqueta do nó (se houver) do downlink deve ter o mesmo significado que o prefixo original, porque não há oportunidade de alterar as etiquetas dos nós que são movidas para o novo tuplo de nível inferior, nem para alterar quaisquer entradas de índice de filhos. Após o nó ter sido dividido, a função `choose` será chamada novamente com o tuplo interno de substituição. Essa chamada pode retornar um resultado `spgAddNode`, se nenhum nó adequado foi criado pela ação `spgSplitTuple`. Eventualmente, `choose` deve retornar `spgMatchNode` para permitir a inserção descer ao próximo nível.

`picksplit`   Decide como criar um novo tupla interna sobre um conjunto de tuplas de folha.

A declaração SQL da função deve parecer assim:

```
CREATE FUNCTION my_picksplit(internal, internal) RETURNS void ...
```

O primeiro argumento é um ponteiro para uma estrutura `spgPickSplitIn` C, que contém dados de entrada para a função. O segundo argumento é um ponteiro para uma estrutura `spgPickSplitOut` C, que a função deve preencher com dados de resultado.

```
typedef struct spgPickSplitIn { int         nTuples;        /* number of leaf tuples */ Datum      *datums;         /* their datums (array of length nTuples) */ int         level;          /* current level (counting from zero) */ } spgPickSplitIn;

typedef struct spgPickSplitOut { bool        hasPrefix;      /* new inner tuple should have a prefix? */ Datum       prefixDatum;    /* if so, its value */

    int         nNodes;         /* number of nodes for new inner tuple */ Datum      *nodeLabels;     /* their labels (or NULL for no labels) */

    int        *mapTuplesToNodes;   /* node index for each leaf tuple */ Datum      *leafTupleDatums;    /* datum to store in each new leaf tuple */ } spgPickSplitOut;
```

`nTuples` é o número de tuplas de folha fornecidas. `datums` é um array de seus valores de dados de `spgConfigOut`.`leafType` tipo. `level` é o nível atual que todas as tuplas de folha compartilham, que se tornará o nível do novo tupla interna.

Defina `hasPrefix` para indicar se o novo tuplo interno deve ter um prefixo, e, se sim, defina `prefixDatum` com o valor do prefixo. Defina `nNodes` para indicar o número de nós que o novo tuplo interno conterá, e defina `nodeLabels` como um array de seus valores de rótulo, ou como NULL se as etiquetas dos nós não forem necessárias. Defina `mapTuplesToNodes` como um array que forneça o índice (a partir de zero) do nó a que cada tuplo de folha deve ser atribuído. Defina `leafTupleDatums` como um array dos valores a serem armazenados nos novos tuplos de folha (estes serão os mesmos que o `datums` de entrada, se a classe do operador não modificar os datums de um nível para o outro). Observe que a função `picksplit` é responsável por alocar os arrays `nodeLabels`, `mapTuplesToNodes` e `leafTupleDatums`.

Se forem fornecidas mais de uma tupla de folhas, espera-se que a função `picksplit` as classifique em mais de um nó; caso contrário, não é possível espalhar as tuplas de folhas em várias páginas, o que é o propósito final dessas operações. Portanto, se a função `picksplit` acabar colocando todas as tuplas de folhas no mesmo nó, o código central do SP-GiST substituirá essa decisão e gerará uma tupla interna na qual as tuplas de folhas são atribuídas randomicamente a vários nós com rótulos idênticos. Tal tupla é marcada `allTheSame` para indicar que isso aconteceu. As funções `choose` e `inner_consistent` devem ter cuidado adequado com tais tuplas internas. Consulte [Seção 65.3.4.3](spgist.md#SPGIST-ALL-THE-SAME) para obter mais informações.

`picksplit` pode ser aplicado a um único tuplo de folha apenas caso o conjunto de função `config` seja definido como verdadeiro e um valor de entrada maior que uma página tenha sido fornecido. Neste caso, o objetivo da operação é remover um prefixo e produzir um novo valor de dado de folha mais curto. A chamada será repetida até que um valor de dado de folha curto o suficiente para caber em uma página seja produzido. Consulte [Seção 65.3.4.1](spgist.md#SPGIST-LIMITS) para obter mais informações.

`inner_consistent` : Retorna um conjunto de nós (ramos) a serem seguidos durante a busca em árvore.

A declaração SQL da função deve parecer assim:

```
CREATE FUNCTION my_inner_consistent(internal, internal) RETURNS void ...
```

O primeiro argumento é um ponteiro para uma estrutura `spgInnerConsistentIn` C, contendo dados de entrada para a função. O segundo argumento é um ponteiro para uma estrutura `spgInnerConsistentOut` C, que a função deve preencher com dados de resultado.

```
typedef struct spgInnerConsistentIn { ScanKey     scankeys;       /* array of operators and comparison values */ ScanKey     orderbys;       /* array of ordering operators and comparison
                                 * values */ int         nkeys;          /* length of scankeys array */ int         norderbys;      /* length of orderbys array */

    Datum       reconstructedValue;     /* value reconstructed at parent */ void       *traversalValue; /* opclass-specific traverse value */ MemoryContext traversalMemoryContext;   /* put new traverse values here */ int         level;          /* current level (counting from zero) */ bool        returnData;     /* original data must be returned? */

    /* Data from current inner tuple */ bool        allTheSame;     /* tuple is marked all-the-same? */ bool        hasPrefix;      /* tuple has a prefix? */ Datum       prefixDatum;    /* if so, the prefix value */ int         nNodes;         /* number of nodes in the inner tuple */ Datum      *nodeLabels;     /* node label values (NULL if none) */ } spgInnerConsistentIn;

typedef struct spgInnerConsistentOut { int         nNodes;         /* number of child nodes to be visited */ int        *nodeNumbers;    /* their indexes in the node array */ int        *levelAdds;      /* increment level by this much for each */ Datum      *reconstructedValues;    /* associated reconstructed values */ void      **traversalValues;        /* opclass-specific traverse values */ double    **distances;              /* associated distances */ } spgInnerConsistentOut;
```

A matriz `scankeys`, de comprimento `nkeys`, descreve a(s) condição(ões) de busca do índice. Essas condições são combinadas com AND — apenas as entradas de índice que as satisfazem são interessantes. (Note que `nkeys` = 0 implica que todas as entradas de índice satisfazem a consulta.) Normalmente, a função consistente só se importa com os campos `sk_strategy` e `sk_argument` de cada entrada da matriz, que, respectivamente, fornecem o operador indexável e o valor de comparação. Em particular, não é necessário verificar `sk_flags` para ver se o valor de comparação é NULL, porque o código do núcleo SP-GiST filtrará tais condições. A matriz `orderbys`, de comprimento `norderbys`, descreve operadores de ordenação (se houver) da mesma maneira. `reconstructedValue` é o valor reconstruído para o tuplo pai; é `(Datum) 0` no nível raiz ou se a `inner_consistent` função não forneceu um valor no nível pai. `traversalValue` é um ponteiro para qualquer dado de travessia passado da chamada anterior de `inner_consistent` no tuplo de índice pai, ou NULL no nível raiz. `traversalMemoryContext` é o contexto de memória no qual armazenar os valores de travessia de saída (veja abaixo). `level` é o nível atual do tuplo interno, começando em zero para o nível raiz. `returnData` é `true` se os dados reconstruídos são necessários para esta consulta; isso só será assim se a `config` função tenha afirmado `canReturnData`. `allTheSame` é verdadeiro se o atual tuplo interno é marcado “tudo o mesmo”; nesse caso, todos os nós têm o mesmo rótulo (se houver) e, portanto, ou todos ou nenhum deles correspondem à consulta (veja [Seção 65.3.4.3](spgist.md#SPGIST-ALL-THE-SAME)). `hasPrefix` é verdadeiro se o atual tuplo interno contém um prefixo; se assim for, `prefixDatum` é seu valor. `nNodes` é o número de nós filhos contidos no tuplo interno, e `nodeLabels` é um array de seus valores de rótulo, ou NULL se os nós não tiverem rótulos.

`nNodes` deve ser definido como o número de nós infantis que precisam ser visitados pela pesquisa, e `nodeNumbers` deve ser definido como um array de seus índices. Se a classe de operador mantém o controle de níveis, defina `levelAdds` como um array dos incrementos de nível requeridos ao descer a cada nó a ser visitado. (Muitas vezes, esses incrementos serão os mesmos para todos os nós, mas isso não é necessariamente o caso, então um array é usado.) Se a reconstrução de valor for necessária, defina `reconstructedValues` como um array dos valores reconstruídos para cada nó infantil a ser visitado; caso contrário, deixe `reconstructedValues` como NULL. Os valores reconstruídos são assumidos como do tipo `spgConfigOut`.`leafType`.

(No entanto, uma vez que o sistema central não fará nada com eles, exceto possivelmente copiá-los, é suficiente que eles tenham as mesmas propriedades de `typlen` e `typbyval` do que `leafType`.). Se a pesquisa ordenada for realizada, defina `distances` como um array de valores de distância de acordo com o array `orderbys` (nós com distâncias mais baixas serão processados primeiro). Deixe como NULL caso contrário. Se é desejado passar informações adicionais fora da banda ("valores de travessia") para níveis mais baixos da pesquisa da árvore, defina `traversalValues` como um array dos valores apropriados de travessia, um para cada nó infantil a ser visitado; caso contrário, deixe `traversalValues` como NULL. Note que a função `inner_consistent` é responsável por pallocar os `nodeNumbers`, `levelAdds`, `distances`, `reconstructedValues`, e `traversalValues` arrays no contexto de memória atual. No entanto, quaisquer valores de travessia de saída apontados pelo array `traversalValues` deverão ser alocados `traversalMemoryContext`. Cada valor de travessia deve ser um único bloco palloc.

`leaf_consistent`: Retorna verdadeiro se um tupla de folha satisfaça uma consulta.

A declaração SQL da função deve parecer assim:

```
CREATE FUNCTION my_leaf_consistent(internal, internal) RETURNS bool ...
```

O primeiro argumento é um ponteiro para uma estrutura `spgLeafConsistentIn` C, contendo dados de entrada para a função. O segundo argumento é um ponteiro para uma estrutura `spgLeafConsistentOut` C, que a função deve preencher com dados de resultado.

```
typedef struct spgLeafConsistentIn { ScanKey     scankeys;       /* array of operators and comparison values */ ScanKey     orderbys;       /* array of ordering operators and comparison
                                 * values */ int         nkeys;          /* length of scankeys array */ int         norderbys;      /* length of orderbys array */

    Datum       reconstructedValue;     /* value reconstructed at parent */ void       *traversalValue; /* opclass-specific traverse value */ int         level;          /* current level (counting from zero) */ bool        returnData;     /* original data must be returned? */

    Datum       leafDatum;      /* datum in leaf tuple */ } spgLeafConsistentIn;

typedef struct spgLeafConsistentOut { Datum       leafValue;        /* reconstructed original data, if any */ bool        recheck;          /* set true if operator must be rechecked */ bool        recheckDistances; /* set true if distances must be rechecked */ double     *distances;        /* associated distances */ } spgLeafConsistentOut;
```

A matriz `scankeys`, de comprimento `nkeys`, descreve a(s) condição(ões) de busca do índice. Essas condições são combinadas com AND — apenas as entradas de índice que satisfazem todas elas satisfazem a consulta. (Observe que `nkeys` = 0 implica que todas as entradas de índice satisfazem a consulta.) Normalmente, a função consistente só se importa com os campos `sk_strategy` e `sk_argument` de cada entrada da matriz, que respectivamente fornecem o operador indexável e o valor de comparação. Em particular, não é necessário verificar `sk_flags` para ver se o valor de comparação é NULL, porque o código do núcleo SP-GiST filtrará tais condições. A matriz `orderbys`, de comprimento `norderbys`, descreve os operadores de ordenação da mesma maneira. `reconstructedValue` é o valor reconstruído para o tuplo pai; é `(Datum) 0` no nível raiz ou se a função `inner_consistent` não forneceu um valor no nível pai. `traversalValue` é um ponteiro para qualquer dado de travessia passado da chamada anterior de `inner_consistent` no tuplo de índice pai, ou NULL no nível raiz. `level` é o nível atual do tuplo folha, começando em zero para o nível raiz. `returnData` é `true` se dados reconstruídos forem necessários para esta consulta; isso só será assim se a função `config` tenha afirmado `canReturnData`. `leafDatum` é o valor da chave de `spgConfigOut`.[[`leafType`] armazenado na tupla atual da folha.

A função deve retornar `true` se o tuplo de folha corresponder à consulta, ou `false` se não corresponder. No caso de `true`, se `returnData` for `true`, então `leafValue` deve ser definido com o valor (do tipo `spgConfigIn`.`attType`) originalmente fornecido para ser indexado para este tuplo de folha. Além disso, `recheck` pode ser definido como `true` se a correspondência for incerta e, portanto, o(s) operador(es) deve(m) ser aplicado(s) novamente ao tuplo real do heap para verificar a correspondência. Se a busca ordenada for realizada, defina `distances` como um array de valores de distância de acordo com a matriz `orderbys`. Deixe-a NULL caso contrário. Se pelo menos uma das distâncias devolvidas não for exata, defina `recheckDistances` como verdadeiro. Neste caso, o executor calculará as distâncias exatas após extrair o tuplo do heap e reorganizará os tuplos, se necessário.

Os métodos opcionais definidos pelo usuário são:

`Datum compress(Datum in)`   Converte um item de dados em um formato adequado para armazenamento físico em uma tupla de folha do índice. Aceita um valor do tipo `spgConfigIn`.`attType` e retorna um valor do tipo `spgConfigOut`.`leafType`. O valor de saída não deve conter um ponteiro TOAST fora da linha.

Nota: o método `compress` é aplicado apenas aos valores a serem armazenados. Os métodos consistentes recebem consulta `scankeys` inalterada, sem transformação usando `compress`.

`options`: Define um conjunto de parâmetros visíveis para o usuário que controlam o comportamento da classe do operador.

A declaração SQL da função deve parecer assim:

```
CREATE OR REPLACE FUNCTION my_options(internal) RETURNS void AS 'MODULE_PATHNAME' LANGUAGE C STRICT;
```

A função recebe um ponteiro para uma estrutura `local_relopts`, que precisa ser preenchida com um conjunto de opções específicas para a classe de operador. As opções podem ser acessadas a partir de outras funções de suporte usando as macros `PG_HAS_OPCLASS_OPTIONS()` e `PG_GET_OPCLASS_OPTIONS()`.

Como a representação da chave no SP-GiST é flexível, ela pode depender de parâmetros especificados pelo usuário.

Todos os métodos de suporte do SP-GiST são normalmente chamados em um contexto de memória de curta duração; ou seja, `CurrentMemoryContext` será redefinido após o processamento de cada tupla. Portanto, não é muito importante se preocupar em liberar tudo o que você pallocou. (O método `config` é uma exceção: ele deve tentar evitar vazamento de memória. Mas, geralmente, o método `config` não precisa fazer nada além de atribuir constantes na estrutura do parâmetro passado.)

Se a coluna indexada for de um tipo de dados coletável, a correção de índice será passada para todos os métodos de suporte, usando o mecanismo padrão `PG_GET_COLLATION()`.

### 65.3.4. Implementação [#](#SPGIST-IMPLEMENTATION)

Esta seção abrange detalhes de implementação e outros truques que são úteis para os implementadores das classes de operadores SP-GiST saberem.

#### 65.3.4.1. Limitações do SP-GiST [#](#SPGIST-LIMITS)

Os tuplos de folhas individuais e os tuplos internos devem caber em uma única página de índice (padrão 8 kB). Portanto, ao indexar valores de tipos de dados de comprimento variável, os valores longos só podem ser suportados por métodos como árvores radix, nas quais cada nível da árvore inclui um prefixo que é curto o suficiente para caber em uma página, e o nível final da folha inclui um sufixo também curto o suficiente para caber em uma página. A classe de operadores deve definir `longValuesOK` para verdadeiro apenas se estiver preparada para garantir que isso aconteça. Caso contrário, o núcleo SP-GiST rejeitará qualquer solicitação para indexar um valor que seja muito grande para caber em uma página de índice.

Da mesma forma, é responsabilidade da classe de operador que os tuplos internos não cresçam demais para caber em uma página de índice; isso limita o número de nós filhos que podem ser usados em um tuplo interno, bem como o tamanho máximo de um valor prefixo.

Outra limitação é que, quando o nó de um tuplo interno aponta para um conjunto de tuplos de folha, esses tuplos devem estar todos na mesma página de índice. (Essa é uma decisão de projeto para reduzir a busca e economizar espaço nos links que unem esses tuplos.) Se o conjunto de tuplos de folha se tornar muito grande para uma página, uma divisão é realizada e um tuplo interno intermediário é inserido. Para resolver o problema, o novo tuplo interno *deve* dividir o conjunto de valores de folha em mais de um grupo de nó. Se a função `picksplit` da classe do operador não conseguir fazer isso, o núcleo SP-GiST recorre a medidas extraordinárias descritas em [Seção 65.3.4.3](spgist.md#SPGIST-ALL-THE-SAME).

Quando `longValuesOK` é verdadeiro, espera-se que os níveis sucessivos da árvore SP-GiST absorvam cada vez mais informações nos prefixos e rótulos dos nós dos tuplos internos, tornando os dados finais menores e menores, de modo que, eventualmente, eles se encaixem em uma página. Para evitar que bugs nas classes de operadores causem loops de inserção infinitos, o núcleo SP-GiST levantará um erro se o dado final não se tornar menor dentro de dez ciclos de chamadas do método `choose`.

#### 65.3.4.2. SP-GiST sem rótulos de nó [#](#SPGIST-NULL-LABELS)

Alguns algoritmos de árvores utilizam um conjunto fixo de nós para cada tupla interna; por exemplo, em uma quad-tree, sempre há exatamente quatro nós correspondentes aos quatro quadrantes ao redor do ponto central da tupla interna. Nesse caso, o código normalmente trabalha com os nós pelo número, e não há necessidade de rótulos explícitos de nó. Para suprimir rótulos de nó (e, assim, economizar espaço), a função `picksplit` pode retornar NULL para o array `nodeLabels`, e da mesma forma, a função `choose` pode retornar NULL para o array `prefixNodeLabels` durante uma ação `spgSplitTuple`. Isso, por sua vez, resultará em `nodeLabels` sendo NULL durante chamadas subsequentes para `choose` e `inner_consistent`. Em princípio, rótulos de nó poderiam ser usados para algumas tuplas internas e omitidos para outras no mesmo índice.

Ao trabalhar com um tuplo interno com nós não rotulados, é um erro que o `choose` retorne `spgAddNode`, uma vez que o conjunto de nós é suposto ser fixo nesses casos.

#### 65.3.4.3. Tuples internos “mesma coisa” [#](#SPGIST-ALL-THE-SAME)

O núcleo SP-GiST pode sobrepor os resultados da função `picksplit` da classe de operadores quando o `picksplit` não consegue dividir os valores fornecidos em pelo menos duas categorias de nós. Quando isso acontece, o novo tuplo interno é criado com vários nós que têm o mesmo rótulo (se houver) que `picksplit` deu ao nó que ele usou, e os valores das folhas são divididos aleatoriamente entre esses nós equivalentes. O sinalizador `allTheSame` é definido no tuplo interno para alertar as funções `choose` e `inner_consistent` de que o tuplo não tem o nó definido que elas podem esperar caso contrário.

Ao lidar com um tuplo `allTheSame`, um resultado de `choose` é interpretado para significar que o novo valor pode ser atribuído a qualquer um dos nós equivalentes; o código principal ignorará o valor fornecido `nodeN` e descerá em um dos nós aleatoriamente (para manter a árvore equilibrada). É um erro para `choose` retornar `spgAddNode`, pois isso tornaria os nós não todos equivalentes; a ação `spgSplitTuple` deve ser usada se o valor a ser inserido não corresponder aos nós existentes.

Ao lidar com um tupla `allTheSame`, a função `inner_consistent` deve retornar todos ou nenhum dos nós como alvos para continuar a busca no índice, uma vez que todos eles são equivalentes. Isso pode ou não exigir código especial, dependendo de quanto a função `inner_consistent` normalmente assume sobre o significado dos nós.

### 65.3.5. Exemplos [#](#SPGIST-EXAMPLES)

A distribuição de fonte do PostgreSQL inclui vários exemplos de classes de operadores de índice para SP-GiST, conforme descrito em [Tabela 65.2](spgist.md#SPGIST-BUILTIN-OPCLASSES-TABLE). Consulte `src/backend/access/spgist/` e `src/backend/utils/adt/` para ver o código.