## 65.2. Índices GiST [#](#GIST)

* [65.2.1. Introdução](gist.md#GIST-INTRO)
* [65.2.2. Classes de Operadores Integradas](gist.md#GIST-BUILTIN-OPCLASSES)
* [65.2.3. Extensibilidade](gist.md#GIST-EXTENSIBILITY)
* [65.2.4. Implementação](gist.md#GIST-IMPLEMENTATION)
* [65.2.5. Exemplos](gist.md#GIST-EXAMPLES)

### 65.2.1. Introdução [#](#GIST-INTRO)

GiST significa Árvore de Busca Generalizada. É um método de acesso balanceado, estruturado em árvore, que atua como um modelo base no qual se implementa esquemas de indexação arbitrários. B-trees, R-trees e muitos outros esquemas de indexação podem ser implementados no GiST.

Uma vantagem do GiST é que ele permite o desenvolvimento de tipos de dados personalizados com os métodos de acesso apropriados, por um especialista no domínio do tipo de dados, e não por um especialista em banco de dados.

Algumas das informações aqui derivadas do Projeto de Indexação GiST da Universidade da Califórnia em Berkeley [site na web][(http://gist.cs.berkeley.edu/)] e da tese de Marcel Kornacker, [Métodos de Acesso para Sistemas de Banco de Dados da Próxima Geração][(http://www.sai.msu.su/~megera/postgres/gist/papers/concurrency/access-methods-for-next-generation.pdf.gz)]. A implementação GiST no PostgreSQL é mantida principalmente por Teodor Sigaev e Oleg Bartunov, e há mais informações em seu [site na web][(http://www.sai.msu.su/~megera/postgres/gist/)].

### 65.2.2. Classes de operador embutidas [#](#GIST-BUILTIN-OPCLASSES)

A distribuição principal do PostgreSQL inclui as classes de operadores GiST mostradas na [Tabela 65.1] ((gist.md#GIST-BUILTIN-OPCLASSES-TABLE "Table 65.1. Built-in GiST Operator Classes")). (Alguns dos módulos opcionais descritos em [Apêndice F] ((contrib.md "Appendix F. Additional Supplied Modules and Extensions")) fornecem classes de operadores GiST adicionais.)

**Tabela 65.1. Classes de operadores GiST integrados**



<table border="1" class="table" summary="Built-in GiST Operator Classes">
<colgroup>
<col class="col1"/>
<col class="col2"/>
<col class="col3"/>
</colgroup>
<thead>
<tr>
<th>Nome</th>
<th>Operadores indexáveis</th>
<th>Operadores de encomendas</th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="12" valign="middle">
<code class="literal">
     box_ops
    </code>
</td>
<td>
<code class="literal">
     &lt;&lt; (box, box)
    </code>
</td>
<td rowspan="12" valign="middle">
<code class="literal">
     &lt;-&gt; (box, point)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&lt; (box, box)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&amp; (box, box)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&gt; (box, box)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &gt;&gt; (box, box)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     ~= (box, box)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     @&gt; (box, box)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;@ (box, box)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&lt;| (box, box)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;&lt;| (box, box)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     |&gt;&gt; (box, box)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     |&amp;&gt; (box, box)
    </code>
</td>
</tr>
<tr>
<td rowspan="12" valign="middle">
<code class="literal">
     circle_ops
    </code>
</td>
<td>
<code class="literal">
     &lt;&lt; (circle, circle)
    </code>
</td>
<td rowspan="12" valign="middle">
<code class="literal">
     &lt;-&gt; (circle, point)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&lt; (circle, circle)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&gt; (circle, circle)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &gt;&gt; (circle, circle)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;@ (circle, circle)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     @&gt; (circle, circle)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     ~= (circle, circle)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&amp; (circle, circle)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     |&gt;&gt; (circle, circle)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;&lt;| (circle, circle)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&lt;| (circle, circle)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     |&amp;&gt; (circle, circle)
    </code>
</td>
</tr>
<tr>
<td rowspan="11" valign="middle">
<code class="literal">
     inet_ops
    </code>
</td>
<td>
<code class="literal">
     &lt;&lt; (inet, inet)
    </code>
</td>
<td rowspan="11" valign="middle">
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;&lt;= (inet, inet)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &gt;&gt; (inet, inet)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &gt;&gt;= (inet, inet)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     = (inet, inet)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;&gt; (inet, inet)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt; (inet, inet)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;= (inet, inet)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &gt; (inet, inet)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &gt;= (inet, inet)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&amp; (inet, inet)
    </code>
</td>
</tr>
<tr>
<td rowspan="18" valign="middle">
<code class="literal">
     multirange_ops
    </code>
</td>
<td>
<code class="literal">
     = (anymultirange, anymultirange)
    </code>
</td>
<td rowspan="18" valign="middle">
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&amp; (anymultirange, anymultirange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&amp; (anymultirange, anyrange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     @&gt; (anymultirange, anyelement)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     @&gt; (anymultirange, anymultirange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     @&gt; (anymultirange, anyrange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;@ (anymultirange, anymultirange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;@ (anymultirange, anyrange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;&lt; (anymultirange, anymultirange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;&lt; (anymultirange, anyrange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &gt;&gt; (anymultirange, anymultirange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &gt;&gt; (anymultirange, anyrange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&lt; (anymultirange, anymultirange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&lt; (anymultirange, anyrange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&gt; (anymultirange, anymultirange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&gt; (anymultirange, anyrange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     -|- (anymultirange, anymultirange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     -|- (anymultirange, anyrange)
    </code>
</td>
</tr>
<tr>
<td rowspan="8" valign="middle">
<code class="literal">
     point_ops
    </code>
</td>
<td>
<code class="literal">
     |&gt;&gt; (point, point)
    </code>
</td>
<td rowspan="8" valign="middle">
<code class="literal">
     &lt;-&gt; (point, point)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;&lt; (point, point)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &gt;&gt; (point, point)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;&lt;| (point, point)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     ~= (point, point)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;@ (point, box)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;@ (point, polygon)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;@ (point, circle)
    </code>
</td>
</tr>
<tr>
<td rowspan="12" valign="middle">
<code class="literal">
     poly_ops
    </code>
</td>
<td>
<code class="literal">
     &lt;&lt; (polygon, polygon)
    </code>
</td>
<td rowspan="12" valign="middle">
<code class="literal">
     &lt;-&gt; (polygon, point)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&lt; (polygon, polygon)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&gt; (polygon, polygon)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &gt;&gt; (polygon, polygon)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;@ (polygon, polygon)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     @&gt; (polygon, polygon)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     ~= (polygon, polygon)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&amp; (polygon, polygon)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;&lt;| (polygon, polygon)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&lt;| (polygon, polygon)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     |&amp;&gt; (polygon, polygon)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     |&gt;&gt; (polygon, polygon)
    </code>
</td>
</tr>
<tr>
<td rowspan="18" valign="middle">
<code class="literal">
     range_ops
    </code>
</td>
<td>
<code class="literal">
     = (anyrange, anyrange)
    </code>
</td>
<td rowspan="18" valign="middle">
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&amp; (anyrange, anyrange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&amp; (anyrange, anymultirange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     @&gt; (anyrange, anyelement)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     @&gt; (anyrange, anyrange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     @&gt; (anyrange, anymultirange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;@ (anyrange, anyrange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;@ (anyrange, anymultirange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;&lt; (anyrange, anyrange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &lt;&lt; (anyrange, anymultirange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &gt;&gt; (anyrange, anyrange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &gt;&gt; (anyrange, anymultirange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&lt; (anyrange, anyrange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&lt; (anyrange, anymultirange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&gt; (anyrange, anyrange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     &amp;&gt; (anyrange, anymultirange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     -|- (anyrange, anyrange)
    </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
     -|- (anyrange, anymultirange)
    </code>
</td>
</tr>
<tr>
<td rowspan="2" valign="middle">
<code class="literal">
     tsquery_ops
    </code>
</td>
<td>
<code class="literal">
     &lt;@ (tsquery, tsquery)
    </code>
</td>
<td rowspan="2" valign="middle">
</td>
</tr>
<tr>
<td>
<code class="literal">
     @&gt; (tsquery, tsquery)
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
     @@ (tsvector, tsquery)
    </code>
</td>
<td>
</td>
</tr>
</tbody>
</table>




  

Por razões históricas, a classe de operador `inet_ops` não é a classe padrão para os tipos `inet` e `cidr`. Para usá-la, mencione o nome da classe em `CREATE INDEX`, por exemplo

```
CREATE INDEX ON my_table USING GIST (my_inet_column inet_ops);
```

### 65.2.3. Extensibilidade [#](#GIST-EXTENSIBILITY)

Tradicionalmente, implementar um novo método de acesso a um índice significava muito trabalho difícil. Era necessário entender o funcionamento interno do banco de dados, como o gerenciador de bloqueio e o Log de Anticipação de Escrita. A interface GiST tem um alto nível de abstração, exigindo que o implementador do método de acesso implemente apenas a semântica do tipo de dados a ser acessado. A própria camada GiST cuida da concorrência, do registro e da busca na estrutura de árvore.

Essa extensibilidade não deve ser confundida com a extensibilidade das outras árvores de busca padrão em termos dos dados que elas podem manipular. Por exemplo, o PostgreSQL suporta árvores B extensivas e índices de hash. Isso significa que você pode usar o PostgreSQL para construir uma árvore B ou um índice de hash sobre qualquer tipo de dados que você deseja. Mas as árvores B só suportam predicados de intervalo (`<`, `=`, `>`) e os índices de hash só suportam consultas de igualdade.

Então, se você indexar, por exemplo, uma coleção de imagens com um B-tree do PostgreSQL, você só pode emitir consultas como “is imagex equal to imagey”, “is imagex less than imagey” e “is imagex greater than imagey”. Dependendo de como você define “igual”, “menor que” e “maior que” nesse contexto, isso pode ser útil. No entanto, usando um índice baseado em GiST, você poderia criar maneiras de fazer perguntas específicas do domínio, talvez “encontrar todas as imagens de cavalos” ou “encontrar todas as imagens sobreexpostas”.

Tudo o que é necessário para fazer um método de acesso GiST funcionar é implementar vários métodos definidos pelo usuário, que definem o comportamento das chaves na árvore. Claro que esses métodos têm que ser bastante sofisticados para suportar consultas sofisticadas, mas para todas as consultas padrão (B-trees, R-trees, etc.) eles são relativamente simples. Em resumo, o GiST combina extensibilidade com generalidade, reutilização de código e uma interface limpa.

Um operador de índice para GiST deve fornecer cinco métodos e sete são opcionais. A correção do índice é assegurada pela implementação adequada dos métodos `same`, `consistent` e `union`, enquanto a eficiência (tamanho e velocidade) do índice dependerá dos métodos `penalty` e `picksplit`. Dois métodos opcionais são `compress` e `decompress`, que permitem que um índice tenha dados internos de uma árvore de um tipo diferente dos dados que ele indexa. As folhas devem ser do tipo de dados indexado, enquanto os outros nós da árvore podem ser de qualquer estrutura C (mas você ainda tem que seguir as regras de tipo de dados do PostgreSQL aqui, veja sobre `varlena` para dados de tamanho variável). Se o tipo de dados interno da árvore existir no nível SQL, a opção `STORAGE` do comando `CREATE OPERATOR CLASS` pode ser usada. O oitavo método opcional é `distance`, que é necessário se a classe do operador desejar suportar varreduras ordenadas (pesquisas de vizinhança mais próxima). O nono método opcional `fetch` é necessário se a classe do operador desejar suportar varreduras apenas de índice, exceto quando o método `compress` é omitido. O décimo método opcional `options` é necessário se a classe do operador tiver parâmetros especificados pelo usuário. O décimo primeiro método opcional `sortsupport` é usado para acelerar a construção de um índice GiST. O décimo segundo método opcional `stratnum` é usado para traduzir tipos de comparação (de `src/include/access/cmptype.h`) em números de estratégia usados pela classe do operador. Isso permite que o código central procure operadores para índices de restrição temporal.

`consistent`: Dado uma entrada de índice `p` e um valor de consulta `q`, esta função determina se a entrada de índice é “consistente” com a consulta; ou seja, o predicado “*`indexed_column`* *`indexable_operator`* `q`” poderia ser verdadeiro para qualquer linha representada pela entrada de índice. Para uma entrada de índice de folha, isso é equivalente a testar a condição indexável, enquanto para um nó interno de árvore, isso determina se é necessário escanear a subárvore do índice representado pelo nó de árvore. Quando o resultado é `true`, um `recheck` deve também ser retornado. Isso indica se o predicado é certamente verdadeiro ou apenas possivelmente verdadeiro. Se `recheck` = `false`, então o índice testou a condição do predicado exatamente, enquanto se `recheck` = `true` a linha é apenas uma correspondência candidata. Nesse caso, o sistema avaliará automaticamente o *`indexable_operator`* contra o valor real da linha para ver se é realmente uma correspondência. Essa convenção permite que o GiST suporte tanto estruturas de índice sem perda quanto estruturas de índice com perda.

A declaração SQL da função deve parecer assim:

```
CREATE OR REPLACE FUNCTION my_consistent(internal, data_type, smallint, oid, internal) RETURNS bool AS 'MODULE_PATHNAME' LANGUAGE C STRICT;
```

E o código correspondente no módulo C poderia então seguir este esqueleto:

```
PG_FUNCTION_INFO_V1(my_consistent);

Datum my_consistent(PG_FUNCTION_ARGS) { GISTENTRY  *entry = (GISTENTRY *) PG_GETARG_POINTER(0); data_type  *query = PG_GETARG_DATA_TYPE_P(1); StrategyNumber strategy = (StrategyNumber) PG_GETARG_UINT16(2); /* Oid subtype = PG_GETARG_OID(3); */ bool       *recheck = (bool *) PG_GETARG_POINTER(4); data_type  *key = DatumGetDataType(entry->key); bool        retval;

    /*
      * determine return value as a function of strategy, key and query. *
      * Use GIST_LEAF(entry) to know where you're called in the index tree,
      * which comes handy when supporting the = operator for example (you could
      * check for non empty union() in non-leaf nodes and equality in leaf
      * nodes). */

    *recheck = true;        /* or false if check is exact */

    PG_RETURN_BOOL(retval); }
```

Aqui, `key` é um elemento no índice e `query` o valor que está sendo procurado no índice. O parâmetro `StrategyNumber` indica qual operador da sua classe de operadores está sendo aplicado — ele corresponde a um dos números do operador no comando `CREATE OPERATOR CLASS`.

Dependendo dos operadores que você incluiu na classe, o tipo de dados de `query` pode variar de acordo com o operador, pois será o tipo que está do lado direito do operador, o que pode ser diferente do tipo de dados indexado que aparece do lado esquerdo. (O esqueleto de código acima assume que apenas um tipo é possível; se não for o caso, a obtenção do valor do argumento `query` teria que depender do operador.) Recomenda-se que a declaração SQL da função `consistent` use o tipo de dados indexado da opclass para o argumento `query`, mesmo que o tipo real possa ser algo diferente dependendo do operador.

`union`: Este método consolida as informações na árvore. Dado um conjunto de entradas, esta função gera uma nova entrada de índice que representa todas as entradas fornecidas.

A declaração SQL da função deve parecer assim:

```
CREATE OR REPLACE FUNCTION my_union(internal, internal) RETURNS storage_type AS 'MODULE_PATHNAME' LANGUAGE C STRICT;
```

E o código correspondente no módulo C poderia então seguir este esqueleto:

```
PG_FUNCTION_INFO_V1(my_union);

Datum my_union(PG_FUNCTION_ARGS) { GistEntryVector *entryvec = (GistEntryVector *) PG_GETARG_POINTER(0); GISTENTRY  *ent = entryvec->vector; data_type  *out, *tmp, *old; int         numranges, i = 0;

    numranges = entryvec->n; tmp = DatumGetDataType(ent[0].key); out = tmp;

    if (numranges == 1) { out = data_type_deep_copy(tmp);

        PG_RETURN_DATA_TYPE_P(out); }

    for (i = 1; i < numranges; i++) { old = out; tmp = DatumGetDataType(ent[i].key); out = my_union_implementation(out, tmp); }

    PG_RETURN_DATA_TYPE_P(out); }
```

Como você pode ver, neste esqueleto, estamos lidando com um tipo de dados onde `union(X, Y, Z) = union(union(X, Y), Z)`. É fácil o suficiente para suportar tipos de dados onde isso não é o caso, implementando o algoritmo de união adequado neste método de suporte GiST.

O resultado da função `union` deve ser um valor do tipo de armazenamento do índice, independentemente disso (pode ou não ser diferente do tipo da coluna indexada). A função `union` deve retornar um ponteiro para memória recém-`palloc()`ada. Você não pode simplesmente retornar o valor de entrada como está, mesmo que não haja mudança de tipo.

Como mostrado acima, o primeiro argumento `union` da função `internal` é, na verdade, um ponteiro `GistEntryVector`. O segundo argumento é um ponteiro para uma variável inteira, que pode ser ignorado. (Anteriormente, era necessário que a função `union` armazenasse o tamanho do valor de seu resultado nessa variável, mas isso não é mais necessário.)

`compress`  :  Converte um item de dados em um formato adequado para armazenamento físico em uma página de índice.  Se o método `compress` for omitido, os itens de dados são armazenados no índice sem modificação.

A declaração SQL da função deve parecer assim:

    ```
    CREATE OR REPLACE FUNCTION my_compress(internal) RETURNS internal AS 'MODULE_PATHNAME' LANGUAGE C STRICT;
    ```

E o código correspondente no módulo C poderia então seguir este esqueleto:

    ```
    PG_FUNCTION_INFO_V1(my_compress);

    Datum my_compress(PG_FUNCTION_ARGS) { GISTENTRY  *entry = (GISTENTRY *) PG_GETARG_POINTER(0); GISTENTRY  *retval;

        if (entry->leafkey) { /* replace entry->key with a compressed version */ compressed_data_type *compressed_data = palloc(sizeof(compressed_data_type));

            /* fill *compressed_data from entry->key ... */

            retval = palloc(sizeof(GISTENTRY)); gistentryinit(*retval, PointerGetDatum(compressed_data), entry->rel, entry->page, entry->offset, FALSE); } else { /* typically we needn't do anything with non-leaf entries */ retval = entry; }

        PG_RETURN_POINTER(retval); }
    ```

Você precisa adaptar *`compressed_data_type`* ao tipo específico para o qual você está convertendo, para, claro, comprimir seus nós de folha.

`decompress`: Converte a representação armazenada de um item de dados em um formato que pode ser manipulado pelos outros métodos GiST na classe de operadores.
Se o método `decompress` for omitido, presume-se que os outros métodos GiST possam trabalhar diretamente no formato de dados armazenado.

(`decompress` não é necessariamente o inverso do método `compress`; em particular, se `compress` for perdas, então é impossível para `decompress` reconstruir exatamente os dados originais. `decompress` não é necessariamente equivalente a `fetch`, também, pois os outros métodos GiST podem não requerer a reconstrução completa dos dados.)

A declaração SQL da função deve parecer assim:

    ```
    CREATE OR REPLACE FUNCTION my_decompress(internal) RETURNS internal AS 'MODULE_PATHNAME' LANGUAGE C STRICT;
    ```

E o código correspondente no módulo C poderia então seguir este esqueleto:

    ```
    PG_FUNCTION_INFO_V1(my_decompress);

    Datum my_decompress(PG_FUNCTION_ARGS) { PG_RETURN_POINTER(PG_GETARG_POINTER(0)); }
    ```

O esqueleto acima é adequado para o caso em que não é necessária descompressão. (Mas, claro, omitir o método completamente é ainda mais fácil e é recomendado em tais casos.)

`penalty`: Retorna um valor que indica o "custo" de inserir a nova entrada em um ramo particular da árvore. Os itens serão inseridos pelo caminho do menor `penalty` na árvore. Os valores retornados por `penalty` devem ser não negativos. Se um valor negativo for retornado, ele será tratado como zero.

A declaração SQL da função deve parecer assim:

    ```
    CREATE OR REPLACE FUNCTION my_penalty(internal, internal, internal) RETURNS internal AS 'MODULE_PATHNAME' LANGUAGE C STRICT;  -- in some cases penalty functions need not be strict
    ```

E o código correspondente no módulo C poderia então seguir este esqueleto:

    ```
    PG_FUNCTION_INFO_V1(my_penalty);

    Datum my_penalty(PG_FUNCTION_ARGS) { GISTENTRY  *origentry = (GISTENTRY *) PG_GETARG_POINTER(0); GISTENTRY  *newentry = (GISTENTRY *) PG_GETARG_POINTER(1); float      *penalty = (float *) PG_GETARG_POINTER(2); data_type  *orig = DatumGetDataType(origentry->key); data_type  *new = DatumGetDataType(newentry->key);

        *penalty = my_penalty_implementation(orig, new); PG_RETURN_POINTER(penalty); }
    ```

Por razões históricas, a função `penalty` não apenas retorna um resultado `float`; em vez disso, ela deve armazenar o valor na localização indicada pelo terceiro argumento. O valor de retorno em si é ignorado, embora seja convencional passar de volta o endereço desse argumento.

A função `penalty` é crucial para o bom desempenho do índice. Ela é usada no momento da inserção para determinar qual ramo seguir ao escolher onde adicionar a nova entrada na árvore. No momento da consulta, quanto mais equilibrado o índice, mais rápida a busca.

`picksplit`
:   Quando uma divisão de página de índice é necessária, esta função decide quais entradas na página devem permanecer na página antiga e quais devem ser movidas para a nova página.

A declaração SQL da função deve parecer assim:

    ```
    CREATE OR REPLACE FUNCTION my_picksplit(internal, internal) RETURNS internal AS 'MODULE_PATHNAME' LANGUAGE C STRICT;
    ```

E o código correspondente no módulo C poderia então seguir este esqueleto:

    ```
    PG_FUNCTION_INFO_V1(my_picksplit);

    Datum my_picksplit(PG_FUNCTION_ARGS) { GistEntryVector *entryvec = (GistEntryVector *) PG_GETARG_POINTER(0); GIST_SPLITVEC *v = (GIST_SPLITVEC *) PG_GETARG_POINTER(1); OffsetNumber maxoff = entryvec->n - 1; GISTENTRY  *ent = entryvec->vector; int         i, nbytes; OffsetNumber *left, *right; data_type  *tmp_union; data_type  *unionL; data_type  *unionR; GISTENTRY **raw_entryvec;

        maxoff = entryvec->n - 1; nbytes = (maxoff + 1) * sizeof(OffsetNumber);

        v->spl_left = (OffsetNumber *) palloc(nbytes); left = v->spl_left; v->spl_nleft = 0;

        v->spl_right = (OffsetNumber *) palloc(nbytes); right = v->spl_right; v->spl_nright = 0;

        unionL = NULL; unionR = NULL;

        /* Initialize the raw entry vector. */ raw_entryvec = (GISTENTRY **) malloc(entryvec->n * sizeof(void *)); for (i = FirstOffsetNumber; i <= maxoff; i = OffsetNumberNext(i)) raw_entryvec[i] = &(entryvec->vector[i]);

        for (i = FirstOffsetNumber; i <= maxoff; i = OffsetNumberNext(i)) { int         real_index = raw_entryvec[i] - entryvec->vector;

            tmp_union = DatumGetDataType(entryvec->vector[real_index].key); Assert(tmp_union != NULL);

            /*
             * Choose where to put the index entries and update unionL and unionR
             * accordingly. Append the entries to either v->spl_left or
             * v->spl_right, and care about the counters. */

            if (my_choice_is_left(unionL, curl, unionR, curr)) { if (unionL == NULL) unionL = tmp_union; else unionL = my_union_implementation(unionL, tmp_union);

                *left = real_index; ++left; ++(v->spl_nleft); } else { /*
                 * Same on the right */ } }

        v->spl_ldatum = DataTypeGetDatum(unionL); v->spl_rdatum = DataTypeGetDatum(unionR); PG_RETURN_POINTER(v); }
    ```

Observe que o resultado da função `picksplit` é entregue modificando a estrutura `v` passada. O valor de retorno em si é ignorado, embora seja convencional retornar o endereço de `v`.

Assim como a função `penalty`, a função `picksplit` é crucial para o bom desempenho do índice. Projetar implementações adequadas de `penalty` e `picksplit` é onde reside o desafio de implementar índices GiST bem-sucedidos.

`same`
:   Retorna verdadeiro se duas entradas de índice forem idênticas, falso em caso contrário.
    (Uma "entrada de índice" é um valor do tipo de armazenamento do índice,
    não necessariamente o tipo da coluna indexada original.)

A declaração SQL da função deve parecer assim:

    ```
    CREATE OR REPLACE FUNCTION my_same(storage_type, storage_type, internal) RETURNS internal AS 'MODULE_PATHNAME' LANGUAGE C STRICT;
    ```

E o código correspondente no módulo C poderia então seguir este esqueleto:

    ```
    PG_FUNCTION_INFO_V1(my_same);

    Datum my_same(PG_FUNCTION_ARGS) { prefix_range *v1 = PG_GETARG_PREFIX_RANGE_P(0); prefix_range *v2 = PG_GETARG_PREFIX_RANGE_P(1); bool       *result = (bool *) PG_GETARG_POINTER(2);

        *result = my_eq(v1, v2); PG_RETURN_POINTER(result); }
    ```

Por razões históricas, a função `same` não apenas retorna um resultado booleano; em vez disso, ela deve armazenar a bandeira na localização indicada pelo terceiro argumento. O valor de retorno em si é ignorado, embora seja convencional passar o endereço desse argumento.

`distance`
:   Dado uma entrada de índice `p` e um valor de consulta `q`,
    esta função determina a "distância" da entrada de índice
    em relação ao valor de consulta. Esta função deve ser
    preenchida se a classe de operadores contiver operadores de ordenação.
    Uma consulta que utilize o operador de ordenação será
    implementada ao retornar entradas de índice com os menores
    valores de "distância" primeiro, portanto, os resultados
    devem ser consistentes com a semântica do operador.
    Para uma entrada de índice de folha, o resultado representa
    apenas a distância até a entrada de índice; para um nó interno
    de árvore, o resultado deve ser a menor distância que qualquer
    entrada de filho poderia ter.

A declaração SQL da função deve parecer assim:

    ```
    CREATE OR REPLACE FUNCTION my_distance(internal, data_type, smallint, oid, internal) RETURNS float8 AS 'MODULE_PATHNAME' LANGUAGE C STRICT;
    ```

E o código correspondente no módulo C poderia então seguir este esqueleto:

    ```
    PG_FUNCTION_INFO_V1(my_distance);

    Datum my_distance(PG_FUNCTION_ARGS) { GISTENTRY  *entry = (GISTENTRY *) PG_GETARG_POINTER(0); data_type  *query = PG_GETARG_DATA_TYPE_P(1); StrategyNumber strategy = (StrategyNumber) PG_GETARG_UINT16(2); /* Oid subtype = PG_GETARG_OID(3); */ /* bool *recheck = (bool *) PG_GETARG_POINTER(4); */ data_type  *key = DatumGetDataType(entry->key); double      retval;

        /*
         * determine return value as a function of strategy, key and query. */

        PG_RETURN_FLOAT8(retval); }
    ```

Os argumentos da função `distance` são idênticos aos argumentos da função `consistent`.

Algumas aproximações são permitidas ao determinar a distância, desde que o resultado nunca seja maior que a distância real da entrada. Assim, por exemplo, a distância de uma caixa de delimitação é geralmente suficiente em aplicações geométricas. Para um nó interno de árvore, a distância devolvida não deve ser maior que a distância de qualquer um dos nós filhos. Se a distância devolvida não for exata, a função deve definir `*recheck` como verdadeiro. (Isso não é necessário para nós internos de árvore; para eles, o cálculo é sempre assumido como inexato.) Neste caso, o executor calculará a distância exata após obter o tuple do heap e reorganizar os tuplos, se necessário.

Se a função de distância retornar `*recheck = true` para qualquer nó de folha, o tipo de retorno do operador original de ordenação deve ser `float8` ou `float4`, e os valores dos resultados da função de distância devem ser comparáveis aos do operador original de ordenação, uma vez que o executor ordenará usando os resultados da função de distância e os resultados recálculos do operador de ordenação. Caso contrário, os valores dos resultados da função de distância podem ser quaisquer valores finitos `float8`, desde que a ordem relativa dos valores dos resultados corresponda à ordem retornada pelo operador de ordenação. (A infindidade e a menos infindidade são usadas internamente para lidar com casos como nulos, portanto, não é recomendado que as funções `distance` retornem esses valores.)

`fetch`   Converte a representação de índice comprimido de um item de dados no tipo de dados original, para varreduras apenas de índice. Os dados retornados devem ser uma cópia exata e sem perda do valor originalmente indexado.

A declaração SQL da função deve parecer assim:

    ```
    CREATE OR REPLACE FUNCTION my_fetch(internal) RETURNS internal AS 'MODULE_PATHNAME' LANGUAGE C STRICT;
    ```

O argumento é um ponteiro para uma estrutura `GISTENTRY`. Na entrada, seu campo `key` contém um dado folha não nulo em forma comprimida. O valor de retorno é outra estrutura `GISTENTRY`, cujo campo `key` contém o mesmo dado em sua forma original, não comprimida. Se a função compress do opclass não fizer nada para entradas de folha, o método `fetch` pode retornar o argumento como é. Ou, se o opclass não tiver uma função compress, o método `fetch` também pode ser omitido, uma vez que seria necessariamente uma operação sem efeito.

O código correspondente no módulo C poderia, então, seguir este esqueleto:

    ```
    PG_FUNCTION_INFO_V1(my_fetch);

    Datum my_fetch(PG_FUNCTION_ARGS) { GISTENTRY  *entry = (GISTENTRY *) PG_GETARG_POINTER(0); input_data_type *in = DatumGetPointer(entry->key); fetched_data_type *fetched_data; GISTENTRY  *retval;

        retval = palloc(sizeof(GISTENTRY)); fetched_data = palloc(sizeof(fetched_data_type));

        /*
         * Convert 'fetched_data' into the a Datum of the original datatype. */

        /* fill *retval from fetched_data. */ gistentryinit(*retval, PointerGetDatum(converted_datum), entry->rel, entry->page, entry->offset, FALSE);

        PG_RETURN_POINTER(retval); }
    ```

Se o método de compressão for perda de entradas de folha, a classe de operador não pode suportar varreduras apenas de índice e não deve definir a função `fetch`.

`options`
:   Permite a definição de parâmetros visíveis ao usuário que controlam o comportamento da classe do operador.

A declaração SQL da função deve parecer assim:

    ```
    CREATE OR REPLACE FUNCTION my_options(internal) RETURNS void AS 'MODULE_PATHNAME' LANGUAGE C STRICT;
    ```

A função recebe um ponteiro para uma estrutura `local_relopts`, que precisa ser preenchida com um conjunto de opções específicas para a classe de operador. As opções podem ser acessadas a partir de outras funções de suporte usando as macros `PG_HAS_OPCLASS_OPTIONS()` e `PG_GET_OPCLASS_OPTIONS()`.

Um exemplo de implementação de my_options() e uso de parâmetros é dado abaixo:

    ```
    typedef enum MyEnumType { MY_ENUM_ON, MY_ENUM_OFF, MY_ENUM_AUTO } MyEnumType;

    typedef struct { int32   vl_len_;    /* varlena header (do not touch directly!) */ int     int_param;  /* integer parameter */ double  real_param; /* real parameter */ MyEnumType enum_param; /* enum parameter */ int     str_param;  /* string parameter */ } MyOptionsStruct;

    /* String representation of enum values */ static relopt_enum_elt_def myEnumValues[] = { {"on", MY_ENUM_ON}, {"off", MY_ENUM_OFF}, {"auto", MY_ENUM_AUTO}, {(const char *) NULL}   /* list terminator */ };

    static char *str_param_default = "default";

    /*
     * Sample validator: checks that string is not longer than 8 bytes. */ static void validate_my_string_relopt(const char *value) { if (strlen(value) > 8) ereport(ERROR, (errcode(ERRCODE_INVALID_PARAMETER_VALUE), errmsg("str_param must be at most 8 bytes"))); }

    /*
     * Sample filler: switches characters to lower case. */ static Size fill_my_string_relopt(const char *value, void *ptr) { char   *tmp = str_tolower(value, strlen(value), DEFAULT_COLLATION_OID); int     len = strlen(tmp);

        if (ptr) strcpy(ptr, tmp);

        pfree(tmp); return len + 1; }

    PG_FUNCTION_INFO_V1(my_options);

    Datum my_options(PG_FUNCTION_ARGS) { local_relopts *relopts = (local_relopts *) PG_GETARG_POINTER(0);

        init_local_reloptions(relopts, sizeof(MyOptionsStruct)); add_local_int_reloption(relopts, "int_param", "integer parameter", 100, 0, 1000000, offsetof(MyOptionsStruct, int_param)); add_local_real_reloption(relopts, "real_param", "real parameter", 1.0, 0.0, 1000000.0, offsetof(MyOptionsStruct, real_param)); add_local_enum_reloption(relopts, "enum_param", "enum parameter", myEnumValues, MY_ENUM_ON, "Valid values are: \"on\", \"off\" and \"auto\".", offsetof(MyOptionsStruct, enum_param)); add_local_string_reloption(relopts, "str_param", "string parameter", str_param_default, &validate_my_string_relopt, &fill_my_string_relopt, offsetof(MyOptionsStruct, str_param));

        PG_RETURN_VOID(); }

    PG_FUNCTION_INFO_V1(my_compress);

    Datum my_compress(PG_FUNCTION_ARGS) { int     int_param = 100; double  real_param = 1.0; MyEnumType enum_param = MY_ENUM_ON; char   *str_param = str_param_default;

        /*
         * Normally, when opclass contains 'options' method, then options are always
         * passed to support functions.  However, if you add 'options' method to
         * existing opclass, previously defined indexes have no options, so the
         * check is required. */ if (PG_HAS_OPCLASS_OPTIONS()) { MyOptionsStruct *options = (MyOptionsStruct *) PG_GET_OPCLASS_OPTIONS();

            int_param = options->int_param; real_param = options->real_param; enum_param = options->enum_param; str_param = GET_STRING_RELOPTION(options, str_param); }

        /* the rest implementation of support function */ }
    ```

Como a representação da chave no GiST é flexível, ela pode depender de parâmetros especificados pelo usuário. Por exemplo, o comprimento da assinatura de chave pode ser especificado. Veja `gtsvector_options()` como exemplo.

`sortsupport`  Retorna uma função comparadora para ordenar dados de uma maneira que preserve a localização. É utilizada pelos comandos `CREATE INDEX` e `REINDEX`. A qualidade do índice criado depende de quão bem a ordem de classificação determinada pela função comparadora preserva a localização dos dados de entrada.

O método `sortsupport` é opcional. Se não for fornecido, o `CREATE INDEX` constrói o índice inserindo cada tupla na árvore usando as funções `penalty` e `picksplit`, o que é muito mais lento.

A declaração SQL da função deve parecer assim:

    ```
    CREATE OR REPLACE FUNCTION my_sortsupport(internal) RETURNS void AS 'MODULE_PATHNAME' LANGUAGE C STRICT;
    ```

O argumento é um ponteiro para uma estrutura `SortSupport`. No mínimo, a função deve preencher seu campo comparador. O comparador recebe três argumentos: dois Datums para comparar e um ponteiro para a estrutura `SortSupport`. Os Datums são os dois valores indexados no formato em que são armazenados no índice; ou seja, no formato retornado pelo método `compress`. A API completa é definida em `src/include/utils/sortsupport.h`.

O código correspondente no módulo C poderia, então, seguir este esqueleto:

    ```
    PG_FUNCTION_INFO_V1(my_sortsupport);

    static int my_fastcmp(Datum x, Datum y, SortSupport ssup) { /* establish order between x and y by computing some sorting value z */

      int z1 = ComputeSpatialCode(x); int z2 = ComputeSpatialCode(y);

      return z1 == z2 ? 0 : z1 > z2 ? 1 : -1; }

    Datum my_sortsupport(PG_FUNCTION_ARGS) { SortSupport ssup = (SortSupport) PG_GETARG_POINTER(0);

      ssup->comparator = my_fastcmp; PG_RETURN_VOID(); }
    ```

`translate_cmptype`
:   Dado um valor `CompareType` de
    `src/include/access/cmptype.h`, retorna um número de estratégia
    usado por esta classe de operador para funcionalidade de correspondência. A
    função deve retornar `InvalidStrategy` se a classe de operador não tiver
    estratégia de correspondência.

Isso é usado para restrições de índice temporal (ou seja, `PRIMARY
    KEY` e `UNIQUE`). Se a classe do operador fornecer essa função e ela retornar resultados para `COMPARE_EQ`, ela pode ser usada na(s) parte(s) não `WITHOUT OVERLAPS` de uma restrição de índice.

Essa função de suporte corresponde ao método de acesso ao índice callback
    function `amtranslatecmptype` (ver [Seção 63.2] (index-functions.md "63.2. Index Access Method Functions")). A
    callback function `amtranslatecmptype` para índices GiST simplesmente chama para baixo até a
    função de suporte `translate_cmptype` da respectiva família de operadores, uma vez que o método de acesso ao índice GiST não tem
    números de estratégia fixos em si.

A declaração SQL da função deve parecer assim:

    ```
    CREATE OR REPLACE FUNCTION my_translate_cmptype(integer) RETURNS smallint AS 'MODULE_PATHNAME' LANGUAGE C STRICT;
    ```

E o registro da família do operador deve ter a seguinte aparência:

    ```
    ALTER OPERATOR FAMILY my_opfamily USING gist ADD FUNCTION 12 ("any", "any") my_translate_cmptype(int);
    ```

O código correspondente no módulo C poderia, então, seguir este esqueleto:

    ```
    PG_FUNCTION_INFO_V1(my_translate_cmptype);

    Datum my_translate_cmptype(PG_FUNCTION_ARGS) { CompareType cmptype = PG_GETARG_INT32(0); StrategyNumber ret = InvalidStrategy;

        switch (cmptype) { case COMPARE_EQ: ret = BTEqualStrategyNumber; }

        PG_RETURN_UINT16(ret); }
    ```

Uma função de tradução é fornecida pelo PostgreSQL:
`gist_translate_cmptype_common` é para classes de operador que usam as constantes `RT*StrategyNumber`.
A extensão `btree_gist`
define uma segunda função de tradução,
`gist_translate_cmptype_btree`, para classes de operador que usam
as constantes `BT*StrategyNumber`.

Todos os métodos de suporte GiST são normalmente chamados em contextos de memória de curta duração; ou seja, `CurrentMemoryContext` será redefinido após cada tupla ser processada. Portanto, não é muito importante se preocupar em liberar tudo o que você alocou com palloc. No entanto, em alguns casos, é útil para um método de suporte armazenar dados em chamadas repetidas. Para isso, aloque os dados de vida mais longa em `fcinfo->flinfo->fn_mcxt`, e mantenha um ponteiro para eles em `fcinfo->flinfo->fn_extra`. Esses dados sobreviverão durante a vida da operação de índice (por exemplo, uma única varredura de índice GiST, construção de índice ou inserção de tupla de índice). Tenha cuidado em liberar o valor anterior ao substituir um valor de `fn_extra`, ou o vazamento se acumulará durante a duração da operação.

### 65.2.4. Implementação [#](#GIST-IMPLEMENTATION)

#### 65.2.4.1. Métodos de construção de índices GiST [#](#GIST-BUFFERING-BUILD)

A maneira mais simples de construir um índice GiST é simplesmente inserir todas as entradas, uma por uma. Isso tende a ser lento para índices grandes, porque, se os tuplos do índice estiverem espalhados pelo índice e o índice for grande o suficiente para não caber na cache, será necessário um monte de I/O aleatório. O PostgreSQL suporta dois métodos alternativos para a construção inicial de um índice GiST: modos *ordenado* e *bufferizado*.

O método ordenado só está disponível se cada uma das opclasses usadas pelo índice fornecer uma função `sortsupport`, conforme descrito em [Seção 65.2.3][(gist.md#GIST-EXTENSIBILITY "65.2.3. Extensibility")]. Se elas o fizerem, esse método é geralmente o melhor, então é usado por padrão.

O método com buffer funciona sem inserir tuplas diretamente no índice de imediato. Ele pode reduzir drasticamente a quantidade de I/O aleatório necessária para conjuntos de dados não ordenados. Para conjuntos de dados bem ordenados, o benefício é menor ou inexistente, porque apenas um pequeno número de páginas recebe novas tuplas de cada vez, e essas páginas cabem na cache mesmo que o índice como um todo não o faça.

O método com buffer precisa ser chamado com mais frequência do que o método simples, que consome alguns recursos de CPU extras. Além disso, os buffers precisam de espaço em disco temporário, até o tamanho do índice resultante. O buffer também pode influenciar a qualidade do índice resultante, tanto em direções positivas quanto negativas. Essa influência depende de vários fatores, como a distribuição dos dados de entrada e a implementação da classe de operador.

Se a classificação não for possível, então, por padrão, a construção de um índice GiST muda para o método de buffer quando o tamanho do índice atinge [effective_cache_size][(runtime-config-query.md#GUC-EFFECTIVE-CACHE-SIZE)]. O bufferamento pode ser forçado manualmente ou impedido pelo parâmetro `buffering` no comando CREATE INDEX. O comportamento padrão é bom para a maioria dos casos, mas desligar o bufferamento pode acelerar um pouco a construção se os dados de entrada estiverem ordenados.

### 65.2.5. Exemplos [#](#GIST-EXAMPLES)

A distribuição de fonte do PostgreSQL inclui vários exemplos de métodos de índice implementados usando GiST. O sistema principal atualmente oferece suporte a pesquisa de texto (indexação para `tsvector` e `tsquery`) além da funcionalidade equivalente ao R-Tree para alguns dos tipos de dados geométricos embutidos (veja `src/backend/access/gist/gistproc.c`). Os seguintes módulos `contrib` também contêm classes de operadores GiST:

`btree_gist`
:   funcionalidade equivalente a árvore B para vários tipos de dados

`cube`
:   Indexação para cubos multidimensionais

`hstore`
:   Módulo para armazenar pares (chave, valor)

`intarray`
:   RD-Tree para matriz unidimensional de valores int4

`ltree`
:   Indexação para estruturas semelhantes a árvores

`pg_trgm`
:   Similaridade de texto usando correspondência de trigramas

`seg`
:   Indexação para “faixas de flutuação”