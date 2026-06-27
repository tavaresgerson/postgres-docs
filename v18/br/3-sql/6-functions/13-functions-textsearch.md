### 9.13. Funções e operadores de pesquisa de texto [#](#FUNCTIONS-TEXTSEARCH)

[Tabela 9.42](functions-textsearch.md#TEXTSEARCH-OPERATORS-TABLE "Table 9.42. Text Search Operators"), [Tabela 9.43](functions-textsearch.md#TEXTSEARCH-FUNCTIONS-TABLE "Table 9.43. Text Search Functions") e [Tabela 9.44](functions-textsearch.md#TEXTSEARCH-FUNCTIONS-DEBUG-TABLE "Table 9.44. Text Search Debugging Functions") resumem as funções e operadores que são fornecidos para a pesquisa de texto completo. Consulte [Capítulo 12](textsearch.md "Chapter 12. Full Text Search") para uma explicação detalhada da facilidade de pesquisa de texto do PostgreSQL.

**Tabela 9.42. Operadores de pesquisa de texto**

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
      tsvector
     </code>
     <code>
      @@
     </code>
     <code>
      tsquery
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p class="func_signature">
     <code>
      tsquery
     </code>
     <code>
      @@
     </code>
     <code>
      tsvector
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     Faz
     <code>
      tsvector
     </code>
     jogo
     <code>
      tsquery
     </code>
     (Os argumentos podem ser apresentados em qualquer ordem.)
    </p>
    <p>
     <code>
      to_tsvector('fat cats ate rats') @@ to_tsquery('cat &amp; rat')
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
      text
     </code>
     <code>
      @@
     </code>
     <code>
      tsquery
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     Texto, após invocação implícita de
     <code>
      to_tsvector()
     </code>
     , jogo
     <code>
      tsquery
     </code>
     ?
    </p>
    <p>
     <code>
      'fat cats ate rats' @@ to_tsquery('cat &amp; rat')
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
      tsvector
     </code>
     <code>
      ||
     </code>
     <code>
      tsvector
     </code>
     →
     <code>
      tsvector
     </code>
    </p>
    <p>
     Concatenam dois
     <code>
      tsvector
     </code>
     s. Se ambos os inputs contiverem posições de léxico, as posições do segundo input são ajustadas conforme necessário.
    </p>
    <p>
     <code>
      'a:1 b:2'::tsvector || 'c:1 d:2 b:3'::tsvector
     </code>
     →
     <code>
      'a':1 'b':2,5 'c':3 'd':4
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      tsquery
     </code>
     <code>
      &amp;&amp;
     </code>
     <code>
      tsquery
     </code>
     →
     <code>
      tsquery
     </code>
    </p>
    <p>
     E os dois ANDs
     <code>
      tsquery
     </code>
     juntos, produzindo uma consulta que corresponde a documentos que correspondem às duas consultas de entrada.
    </p>
    <p>
     <code>
      'fat | rat'::tsquery &amp;&amp; 'cat'::tsquery
     </code>
     →
     <code>
      ( 'fat' | 'rat' ) &amp; 'cat'
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      tsquery
     </code>
     <code>
      ||
     </code>
     <code>
      tsquery
     </code>
     →
     <code>
      tsquery
     </code>
    </p>
    <p>
     ORs dois
     <code>
      tsquery
     </code>
     juntos, produzindo uma consulta que corresponde a documentos que correspondem à consulta de entrada.
    </p>
    <p>
     <code>
      'fat | rat'::tsquery || 'cat'::tsquery
     </code>
     →
     <code>
      'fat' | 'rat' | 'cat'
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      !!
     </code>
     <code>
      tsquery
     </code>
     →
     <code>
      tsquery
     </code>
    </p>
    <p>
     Anula um
     <code>
      tsquery
     </code>
     , produzindo uma consulta que corresponde a documentos que não correspondem à consulta de entrada.
    </p>
    <p>
     <code>
      !! 'cat'::tsquery
     </code>
     →
     <code>
      !'cat'
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      tsquery
     </code>
     <code>
      &lt;-&gt;
     </code>
     <code>
      tsquery
     </code>
     →
     <code>
      tsquery
     </code>
    </p>
    <p>
     Construi uma consulta de frase, que corresponde se as duas consultas de entrada corresponderem em lexemas sucessivos.
    </p>
    <p>
     <code>
      to_tsquery('fat') &lt;-&gt; to_tsquery('rat')
     </code>
     →
     <code>
      'fat' &lt;-&gt; 'rat'
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      tsquery
     </code>
     <code>
      @&gt;
     </code>
     <code>
      tsquery
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     Primeiro
     <code>
      tsquery
     </code>
     contêm o segundo? (Isso considera apenas se todos os lexemas que aparecem em uma consulta aparecem na outra, ignorando os operadores de combinação.)
    </p>
    <p>
     <code>
      'cat'::tsquery @&gt; 'cat &amp; rat'::tsquery
     </code>
     →
     <code>
      f
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      tsquery
     </code>
     <code>
      &lt;@
     </code>
     <code>
      tsquery
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     É o primeiro
     <code>
      tsquery
     </code>
     contido no segundo? (Isso considera apenas se todos os lexemas que aparecem em uma consulta aparecem no outro, ignorando os operadores de combinação.)
    </p>
    <p>
     <code>
      'cat'::tsquery &lt;@ 'cat &amp; rat'::tsquery
     </code>
     →
     <code>
      t
     </code>
    </p>
    <p>
     <code>
      'cat'::tsquery &lt;@ '!cat &amp; rat'::tsquery
     </code>
     →
     <code>
      t
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>

Além desses operadores especializados, os operadores de comparação comuns mostrados na [Tabela 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) estão disponíveis para os tipos `tsvector` e `tsquery`. Estes não são muito úteis para pesquisas de texto, mas permitem, por exemplo, a construção de índices únicos em colunas desses tipos.

**Tabela 9.43. Funções de pesquisa de texto**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
    <p>
     Example(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_to_tsvector
     </code>
     (
     <code>
      text[]
     </code>
     ) →
     <code>
      tsvector
     </code>
    </p>
    <p>
     Converts an array of text strings to a
     <code>
      tsvector
     </code>
     . The given strings are used as lexemes as-is, without further processing.  Array elements must not be empty strings or
     <code>
      NULL
     </code>
     .
    </p>
    <p>
     <code>
      array_to_tsvector('{fat,cat,rat}'::text[])
     </code>
     →
     <code>
      'cat' 'fat' 'rat'
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      get_current_ts_config
     </code>
     ( ) →
     <code>
      regconfig
     </code>
    </p>
    <p>
     Returns the OID of the current default text search configuration (as set by
     <a class="xref" href="runtime-config-client.md#GUC-DEFAULT-TEXT-SEARCH-CONFIG">
      default_text_search_config
     </a>
     ).
    </p>
    <p>
     <code>
      get_current_ts_config()
     </code>
     →
     <code>
      english
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      length
     </code>
     (
     <code>
      tsvector
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns the number of lexemes in the
     <code>
      tsvector
     </code>
     .
    </p>
    <p>
     <code>
      length('fat:2,4 cat:3 rat:5A'::tsvector)
     </code>
     →
     <code>
      3
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      numnode
     </code>
     (
     <code>
      tsquery
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns the number of lexemes plus operators in the
     <code>
      tsquery
     </code>
     .
    </p>
    <p>
     <code>
      numnode('(fat &amp; rat) | cat'::tsquery)
     </code>
     →
     <code>
      5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      plainto_tsquery
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        config
       </code>
      </em>
      <code>
       regconfig
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       query
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      tsquery
     </code>
    </p>
    <p>
     Converts text to a
     <code>
      tsquery
     </code>
     , normalizing words according to the specified or default configuration.  Any punctuation in the string is ignored (it does not determine query operators).  The resulting query matches documents containing all non-stopwords in the text.
    </p>
    <p>
     <code>
      plainto_tsquery('english', 'The Fat Rats')
     </code>
     →
     <code>
      'fat' &amp; 'rat'
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      phraseto_tsquery
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        config
       </code>
      </em>
      <code>
       regconfig
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       query
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      tsquery
     </code>
    </p>
    <p>
     Converts text to a
     <code>
      tsquery
     </code>
     , normalizing words according to the specified or default configuration.  Any punctuation in the string is ignored (it does not determine query operators).  The resulting query matches phrases containing all non-stopwords in the text.
    </p>
    <p>
     <code>
      phraseto_tsquery('english', 'The Fat Rats')
     </code>
     →
     <code>
      'fat' &lt;-&gt; 'rat'
     </code>
    </p>
    <p>
     <code>
      phraseto_tsquery('english', 'The Cat and Rats')
     </code>
     →
     <code>
      'cat' &lt;2&gt; 'rat'
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      websearch_to_tsquery
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        config
       </code>
      </em>
      <code>
       regconfig
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       query
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      tsquery
     </code>
    </p>
    <p>
     Converts text to a
     <code>
      tsquery
     </code>
     , normalizing words according to the specified or default configuration.  Quoted word sequences are converted to phrase tests.  The word
     <span class="quote">
      “
      <span class="quote">
       or
      </span>
      ”
     </span>
     is understood as producing an OR operator, and a dash produces a NOT operator; other punctuation is ignored. This approximates the behavior of some common web search tools.
    </p>
    <p>
     <code>
      websearch_to_tsquery('english', '"fat rat" or cat dog')
     </code>
     →
     <code>
      'fat' &lt;-&gt; 'rat' | 'cat' &amp; 'dog'
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      querytree
     </code>
     (
     <code>
      tsquery
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Produces a representation of the indexable portion of a
     <code>
      tsquery
     </code>
     .  A result that is empty or just
     <code>
      T
     </code>
     indicates a non-indexable query.
    </p>
    <p>
     <code>
      querytree('foo &amp; ! bar'::tsquery)
     </code>
     →
     <code>
      'foo'
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      setweight
     </code>
     (
     <em class="parameter">
      <code>
       vector
      </code>
     </em>
     <code>
      tsvector
     </code>
     ,
     <em class="parameter">
      <code>
       weight
      </code>
     </em>
     <code>
      "char"
     </code>
     ) →
     <code>
      tsvector
     </code>
    </p>
    <p>
     Assigns the specified
     <em class="parameter">
      <code>
       weight
      </code>
     </em>
     to each element of the
     <em class="parameter">
      <code>
       vector
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      setweight('fat:2,4 cat:3 rat:5B'::tsvector, 'A')
     </code>
     →
     <code>
      'cat':3A 'fat':2A,4A 'rat':5A
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      setweight
     </code>
     (
     <em class="parameter">
      <code>
       vector
      </code>
     </em>
     <code>
      tsvector
     </code>
     ,
     <em class="parameter">
      <code>
       weight
      </code>
     </em>
     <code>
      "char"
     </code>
     ,
     <em class="parameter">
      <code>
       lexemes
      </code>
     </em>
     <code>
      text[]
     </code>
     ) →
     <code>
      tsvector
     </code>
    </p>
    <p>
     Assigns the specified
     <em class="parameter">
      <code>
       weight
      </code>
     </em>
     to elements of the
     <em class="parameter">
      <code>
       vector
      </code>
     </em>
     that are listed in
     <em class="parameter">
      <code>
       lexemes
      </code>
     </em>
     . The strings in
     <em class="parameter">
      <code>
       lexemes
      </code>
     </em>
     are taken as lexemes as-is, without further processing.  Strings that do not match any lexeme in
     <em class="parameter">
      <code>
       vector
      </code>
     </em>
     are ignored.
    </p>
    <p>
     <code>
      setweight('fat:2,4 cat:3 rat:5,6B'::tsvector, 'A', '{cat,rat}')
     </code>
     →
     <code>
      'cat':3A 'fat':2,4 'rat':5A,6A
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      strip
     </code>
     (
     <code>
      tsvector
     </code>
     ) →
     <code>
      tsvector
     </code>
    </p>
    <p>
     Removes positions and weights from the
     <code>
      tsvector
     </code>
     .
    </p>
    <p>
     <code>
      strip('fat:2,4 cat:3 rat:5A'::tsvector)
     </code>
     →
     <code>
      'cat' 'fat' 'rat'
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      to_tsquery
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        config
       </code>
      </em>
      <code>
       regconfig
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       query
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      tsquery
     </code>
    </p>
    <p>
     Converts text to a
     <code>
      tsquery
     </code>
     , normalizing words according to the specified or default configuration.  The words must be combined by valid
     <code>
      tsquery
     </code>
     operators.
    </p>
    <p>
     <code>
      to_tsquery('english', 'The &amp; Fat &amp; Rats')
     </code>
     →
     <code>
      'fat' &amp; 'rat'
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      to_tsvector
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        config
       </code>
      </em>
      <code>
       regconfig
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       document
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      tsvector
     </code>
    </p>
    <p>
     Converts text to a
     <code>
      tsvector
     </code>
     , normalizing words according to the specified or default configuration.  Position information is included in the result.
    </p>
    <p>
     <code>
      to_tsvector('english', 'The Fat Rats')
     </code>
     →
     <code>
      'fat':2 'rat':3
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      to_tsvector
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        config
       </code>
      </em>
      <code>
       regconfig
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       document
      </code>
     </em>
     <code>
      json
     </code>
     ) →
     <code>
      tsvector
     </code>
    </p>
    <p class="func_signature">
     <code>
      to_tsvector
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        config
       </code>
      </em>
      <code>
       regconfig
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       document
      </code>
     </em>
     <code>
      jsonb
     </code>
     ) →
     <code>
      tsvector
     </code>
    </p>
    <p>
     Converts each string value in the JSON document to a
     <code>
      tsvector
     </code>
     , normalizing words according to the specified or default configuration.  The results are then concatenated in document order to produce the output.  Position information is generated as though one stopword exists between each pair of string values.  (Beware that
     <span class="quote">
      “
      <span class="quote">
       document order
      </span>
      ”
     </span>
     of the fields of a JSON object is implementation-dependent when the input is
     <code>
      jsonb
     </code>
     ; observe the difference in the examples.)
    </p>
    <p>
     <code>
      to_tsvector('english', '{"aa": "The Fat Rats", "b": "dog"}'::json)
     </code>
     →
     <code>
      'dog':5 'fat':2 'rat':3
     </code>
    </p>
    <p>
     <code>
      to_tsvector('english', '{"aa": "The Fat Rats", "b": "dog"}'::jsonb)
     </code>
     →
     <code>
      'dog':1 'fat':4 'rat':5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      json_to_tsvector
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        config
       </code>
      </em>
      <code>
       regconfig
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       document
      </code>
     </em>
     <code>
      json
     </code>
     ,
     <em class="parameter">
      <code>
       filter
      </code>
     </em>
     <code>
      jsonb
     </code>
     ) →
     <code>
      tsvector
     </code>
    </p>
    <p class="func_signature">
     <code>
      jsonb_to_tsvector
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        config
       </code>
      </em>
      <code>
       regconfig
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       document
      </code>
     </em>
     <code>
      jsonb
     </code>
     ,
     <em class="parameter">
      <code>
       filter
      </code>
     </em>
     <code>
      jsonb
     </code>
     ) →
     <code>
      tsvector
     </code>
    </p>
    <p>
     Selects each item in the JSON document that is requested by the
     <em class="parameter">
      <code>
       filter
      </code>
     </em>
     and converts each one to a
     <code>
      tsvector
     </code>
     , normalizing words according to the specified or default configuration.  The results are then concatenated in document order to produce the output.  Position information is generated as though one stopword exists between each pair of selected items.  (Beware that
     <span class="quote">
      “
      <span class="quote">
       document order
      </span>
      ”
     </span>
     of the fields of a JSON object is implementation-dependent when the input is
     <code>
      jsonb
     </code>
     .) The
     <em class="parameter">
      <code>
       filter
      </code>
     </em>
     must be a
     <code>
      jsonb
     </code>
     array containing zero or more of these keywords:
     <code>
      "string"
     </code>
     (to include all string values),
     <code>
      "numeric"
     </code>
     (to include all numeric values),
     <code>
      "boolean"
     </code>
     (to include all boolean values),
     <code>
      "key"
     </code>
     (to include all keys), or
     <code>
      "all"
     </code>
     (to include all the above). As a special case, the
     <em class="parameter">
      <code>
       filter
      </code>
     </em>
     can also be a simple JSON value that is one of these keywords.
    </p>
    <p>
     <code>
      json_to_tsvector('english', '{"a": "The Fat Rats", "b": 123}'::json, '["string", "numeric"]')
     </code>
     →
     <code>
      '123':5 'fat':2 'rat':3
     </code>
    </p>
    <p>
     <code>
      json_to_tsvector('english', '{"cat": "The Fat Rats", "dog": 123}'::json, '"all"')
     </code>
     →
     <code>
      '123':9 'cat':1 'dog':7 'fat':4 'rat':5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ts_delete
     </code>
     (
     <em class="parameter">
      <code>
       vector
      </code>
     </em>
     <code>
      tsvector
     </code>
     ,
     <em class="parameter">
      <code>
       lexeme
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      tsvector
     </code>
    </p>
    <p>
     Removes any occurrence of the given
     <em class="parameter">
      <code>
       lexeme
      </code>
     </em>
     from the
     <em class="parameter">
      <code>
       vector
      </code>
     </em>
     . The
     <em class="parameter">
      <code>
       lexeme
      </code>
     </em>
     string is treated as a lexeme as-is, without further processing.
    </p>
    <p>
     <code>
      ts_delete('fat:2,4 cat:3 rat:5A'::tsvector, 'fat')
     </code>
     →
     <code>
      'cat':3 'rat':5A
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ts_delete
     </code>
     (
     <em class="parameter">
      <code>
       vector
      </code>
     </em>
     <code>
      tsvector
     </code>
     ,
     <em class="parameter">
      <code>
       lexemes
      </code>
     </em>
     <code>
      text[]
     </code>
     ) →
     <code>
      tsvector
     </code>
    </p>
    <p>
     Removes any occurrences of the lexemes in
     <em class="parameter">
      <code>
       lexemes
      </code>
     </em>
     from the
     <em class="parameter">
      <code>
       vector
      </code>
     </em>
     . The strings in
     <em class="parameter">
      <code>
       lexemes
      </code>
     </em>
     are taken as lexemes as-is, without further processing.  Strings that do not match any lexeme in
     <em class="parameter">
      <code>
       vector
      </code>
     </em>
     are ignored.
    </p>
    <p>
     <code>
      ts_delete('fat:2,4 cat:3 rat:5A'::tsvector, ARRAY['fat','rat'])
     </code>
     →
     <code>
      'cat':3
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ts_filter
     </code>
     (
     <em class="parameter">
      <code>
       vector
      </code>
     </em>
     <code>
      tsvector
     </code>
     ,
     <em class="parameter">
      <code>
       weights
      </code>
     </em>
     <code>
      "char"[]
     </code>
     ) →
     <code>
      tsvector
     </code>
    </p>
    <p>
     Selects only elements with the given
     <em class="parameter">
      <code>
       weights
      </code>
     </em>
     from the
     <em class="parameter">
      <code>
       vector
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      ts_filter('fat:2,4 cat:3b,7c rat:5A'::tsvector, '{a,b}')
     </code>
     →
     <code>
      'cat':3B 'rat':5A
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ts_headline
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        config
       </code>
      </em>
      <code>
       regconfig
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       document
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       query
      </code>
     </em>
     <code>
      tsquery
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        options
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Displays, in an abbreviated form, the match(es) for the
     <em class="parameter">
      <code>
       query
      </code>
     </em>
     in the
     <em class="parameter">
      <code>
       document
      </code>
     </em>
     , which must be raw text not a
     <code>
      tsvector
     </code>
     .  Words in the document are normalized according to the specified or default configuration before matching to the query.  Use of this function is discussed in
     <a class="xref" href="textsearch-controls.md#TEXTSEARCH-HEADLINE" title="12.3.4. Highlighting Results">
      Section 12.3.4
     </a>
     , which also describes the available
     <em class="parameter">
      <code>
       options
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      ts_headline('The fat cat ate the rat.', 'cat')
     </code>
     →
     <code>
      The fat &lt;b&gt;cat&lt;/b&gt; ate the rat.
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ts_headline
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        config
       </code>
      </em>
      <code>
       regconfig
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       document
      </code>
     </em>
     <code>
      json
     </code>
     ,
     <em class="parameter">
      <code>
       query
      </code>
     </em>
     <code>
      tsquery
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        options
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p class="func_signature">
     <code>
      ts_headline
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        config
       </code>
      </em>
      <code>
       regconfig
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       document
      </code>
     </em>
     <code>
      jsonb
     </code>
     ,
     <em class="parameter">
      <code>
       query
      </code>
     </em>
     <code>
      tsquery
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        options
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Displays, in an abbreviated form, match(es) for the
     <em class="parameter">
      <code>
       query
      </code>
     </em>
     that occur in string values within the JSON
     <em class="parameter">
      <code>
       document
      </code>
     </em>
     . See
     <a class="xref" href="textsearch-controls.md#TEXTSEARCH-HEADLINE" title="12.3.4. Highlighting Results">
      Section 12.3.4
     </a>
     for more details.
    </p>
    <p>
     <code>
      ts_headline('{"cat":"raining cats and dogs"}'::jsonb, 'cat')
     </code>
     →
     <code>
      {"cat": "raining &lt;b&gt;cats&lt;/b&gt; and dogs"}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ts_rank
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        weights
       </code>
      </em>
      <code>
       real[]
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       vector
      </code>
     </em>
     <code>
      tsvector
     </code>
     ,
     <em class="parameter">
      <code>
       query
      </code>
     </em>
     <code>
      tsquery
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        normalization
       </code>
      </em>
      <code>
       integer
      </code>
     </span>
     ] ) →
     <code>
      real
     </code>
    </p>
    <p>
     Computes a score showing how well the
     <em class="parameter">
      <code>
       vector
      </code>
     </em>
     matches the
     <em class="parameter">
      <code>
       query
      </code>
     </em>
     .  See
     <a class="xref" href="textsearch-controls.md#TEXTSEARCH-RANKING" title="12.3.3. Ranking Search Results">
      Section 12.3.3
     </a>
     for details.
    </p>
    <p>
     <code>
      ts_rank(to_tsvector('raining cats and dogs'), 'cat')
     </code>
     →
     <code>
      0.06079271
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ts_rank_cd
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        weights
       </code>
      </em>
      <code>
       real[]
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       vector
      </code>
     </em>
     <code>
      tsvector
     </code>
     ,
     <em class="parameter">
      <code>
       query
      </code>
     </em>
     <code>
      tsquery
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        normalization
       </code>
      </em>
      <code>
       integer
      </code>
     </span>
     ] ) →
     <code>
      real
     </code>
    </p>
    <p>
     Computes a score showing how well the
     <em class="parameter">
      <code>
       vector
      </code>
     </em>
     matches the
     <em class="parameter">
      <code>
       query
      </code>
     </em>
     , using a cover density algorithm.  See
     <a class="xref" href="textsearch-controls.md#TEXTSEARCH-RANKING" title="12.3.3. Ranking Search Results">
      Section 12.3.3
     </a>
     for details.
    </p>
    <p>
     <code>
      ts_rank_cd(to_tsvector('raining cats and dogs'), 'cat')
     </code>
     →
     <code>
      0.1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ts_rewrite
     </code>
     (
     <em class="parameter">
      <code>
       query
      </code>
     </em>
     <code>
      tsquery
     </code>
     ,
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code>
      tsquery
     </code>
     ,
     <em class="parameter">
      <code>
       substitute
      </code>
     </em>
     <code>
      tsquery
     </code>
     ) →
     <code>
      tsquery
     </code>
    </p>
    <p>
     Replaces occurrences of
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     with
     <em class="parameter">
      <code>
       substitute
      </code>
     </em>
     within the
     <em class="parameter">
      <code>
       query
      </code>
     </em>
     . See
     <a class="xref" href="textsearch-features.md#TEXTSEARCH-QUERY-REWRITING" title="12.4.2.1. Query Rewriting">
      Section 12.4.2.1
     </a>
     for details.
    </p>
    <p>
     <code>
      ts_rewrite('a &amp; b'::tsquery, 'a'::tsquery, 'foo|bar'::tsquery)
     </code>
     →
     <code>
      'b' &amp; ( 'foo' | 'bar' )
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ts_rewrite
     </code>
     (
     <em class="parameter">
      <code>
       query
      </code>
     </em>
     <code>
      tsquery
     </code>
     ,
     <em class="parameter">
      <code>
       select
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      tsquery
     </code>
    </p>
    <p>
     Replaces portions of the
     <em class="parameter">
      <code>
       query
      </code>
     </em>
     according to target(s) and substitute(s) obtained by executing a
     <code>
      SELECT
     </code>
     command. See
     <a class="xref" href="textsearch-features.md#TEXTSEARCH-QUERY-REWRITING" title="12.4.2.1. Query Rewriting">
      Section 12.4.2.1
     </a>
     for details.
    </p>
    <p>
     <code>
      SELECT ts_rewrite('a &amp; b'::tsquery, 'SELECT t,s FROM aliases')
     </code>
     →
     <code>
      'b' &amp; ( 'foo' | 'bar' )
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      tsquery_phrase
     </code>
     (
     <em class="parameter">
      <code>
       query1
      </code>
     </em>
     <code>
      tsquery
     </code>
     ,
     <em class="parameter">
      <code>
       query2
      </code>
     </em>
     <code>
      tsquery
     </code>
     ) →
     <code>
      tsquery
     </code>
    </p>
    <p>
     Constructs a phrase query that searches for matches of
     <em class="parameter">
      <code>
       query1
      </code>
     </em>
     and
     <em class="parameter">
      <code>
       query2
      </code>
     </em>
     at successive lexemes (same as
     <code>
      &lt;-&gt;
     </code>
     operator).
    </p>
    <p>
     <code>
      tsquery_phrase(to_tsquery('fat'), to_tsquery('cat'))
     </code>
     →
     <code>
      'fat' &lt;-&gt; 'cat'
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      tsquery_phrase
     </code>
     (
     <em class="parameter">
      <code>
       query1
      </code>
     </em>
     <code>
      tsquery
     </code>
     ,
     <em class="parameter">
      <code>
       query2
      </code>
     </em>
     <code>
      tsquery
     </code>
     ,
     <em class="parameter">
      <code>
       distance
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      tsquery
     </code>
    </p>
    <p>
     Constructs a phrase query that searches for matches of
     <em class="parameter">
      <code>
       query1
      </code>
     </em>
     and
     <em class="parameter">
      <code>
       query2
      </code>
     </em>
     that occur exactly
     <em class="parameter">
      <code>
       distance
      </code>
     </em>
     lexemes apart.
    </p>
    <p>
     <code>
      tsquery_phrase(to_tsquery('fat'), to_tsquery('cat'), 10)
     </code>
     →
     <code>
      'fat' &lt;10&gt; 'cat'
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      tsvector_to_array
     </code>
     (
     <code>
      tsvector
     </code>
     ) →
     <code>
      text[]
     </code>
    </p>
    <p>
     Converts a
     <code>
      tsvector
     </code>
     to an array of lexemes.
    </p>
    <p>
     <code>
      tsvector_to_array('fat:2,4 cat:3 rat:5A'::tsvector)
     </code>
     →
     <code>
      {cat,fat,rat}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      unnest
     </code>
     (
     <code>
      tsvector
     </code>
     ) →
     <code>
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       lexeme
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       positions
      </code>
     </em>
     <code>
      smallint[]
     </code>
     ,
     <em class="parameter">
      <code>
       weights
      </code>
     </em>
     <code>
      text
     </code>
     )
    </p>
    <p>
     Expands a
     <code>
      tsvector
     </code>
     into a set of rows, one per lexeme.
    </p>
    <p>
     <code>
      select * from unnest('cat:3 fat:2,4 rat:5A'::tsvector)
     </code>
     →
     <code>
     </code>
    </p>
    <pre class="programlisting">
 lexeme | positions | weights --------+-----------+--------- cat    | {3}       | {D} fat    | {2,4}     | {D,D} rat    | {5}       | {A}
</pre>
    <p>
    </p>
   </td>
  </tr>
 </tbody>
</table>

Nota

Todas as funções de busca de texto que aceitam um argumento opcional `regconfig` usarão a configuração especificada por [default_text_search_config](runtime-config-client.md#GUC-DEFAULT-TEXT-SEARCH-CONFIG) quando esse argumento for omitido.

As funções em [Tabela 9.44](functions-textsearch.md#TEXTSEARCH-FUNCTIONS-DEBUG-TABLE) são listadas separadamente porque geralmente não são usadas em operações de busca de texto no dia a dia. Elas são principalmente úteis para o desenvolvimento e depuração de novas configurações de busca de texto.

**Tabela 9.44. Funções de depuração de pesquisa de texto**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
    <p>
     Example(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ts_debug
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        config
       </code>
      </em>
      <code>
       regconfig
      </code>
      ,
     </span>
     ]
     <em class="parameter">
      <code>
       document
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       alias
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       description
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       token
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       dictionaries
      </code>
     </em>
     <code>
      regdictionary[]
     </code>
     ,
     <em class="parameter">
      <code>
       dictionary
      </code>
     </em>
     <code>
      regdictionary
     </code>
     ,
     <em class="parameter">
      <code>
       lexemes
      </code>
     </em>
     <code>
      text[]
     </code>
     )
    </p>
    <p>
     Extracts and normalizes tokens from the
     <em class="parameter">
      <code>
       document
      </code>
     </em>
     according to the specified or default text search configuration, and returns information about how each token was processed. See
     <a class="xref" href="textsearch-debugging.md#TEXTSEARCH-CONFIGURATION-TESTING" title="12.8.1. Configuration Testing">
      Section 12.8.1
     </a>
     for details.
    </p>
    <p>
     <code>
      ts_debug('english', 'The Brightest supernovaes')
     </code>
     →
     <code>
      (asciiword,"Word, all ASCII",The,{english_stem},english_stem,{}) ...
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ts_lexize
     </code>
     (
     <em class="parameter">
      <code>
       dict
      </code>
     </em>
     <code>
      regdictionary
     </code>
     ,
     <em class="parameter">
      <code>
       token
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      text[]
     </code>
    </p>
    <p>
     Returns an array of replacement lexemes if the input token is known to the dictionary, or an empty array if the token is known to the dictionary but it is a stop word, or NULL if it is not a known word. See
     <a class="xref" href="textsearch-debugging.md#TEXTSEARCH-DICTIONARY-TESTING" title="12.8.3. Dictionary Testing">
      Section 12.8.3
     </a>
     for details.
    </p>
    <p>
     <code>
      ts_lexize('english_stem', 'stars')
     </code>
     →
     <code>
      {star}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ts_parse
     </code>
     (
     <em class="parameter">
      <code>
       parser_name
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       document
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       tokid
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       token
      </code>
     </em>
     <code>
      text
     </code>
     )
    </p>
    <p>
     Extracts tokens from the
     <em class="parameter">
      <code>
       document
      </code>
     </em>
     using the named parser. See
     <a class="xref" href="textsearch-debugging.md#TEXTSEARCH-PARSER-TESTING" title="12.8.2. Parser Testing">
      Section 12.8.2
     </a>
     for details.
    </p>
    <p>
     <code>
      ts_parse('default', 'foo - bar')
     </code>
     →
     <code>
      (1,foo) ...
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ts_parse
     </code>
     (
     <em class="parameter">
      <code>
       parser_oid
      </code>
     </em>
     <code>
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       document
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       tokid
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       token
      </code>
     </em>
     <code>
      text
     </code>
     )
    </p>
    <p>
     Extracts tokens from the
     <em class="parameter">
      <code>
       document
      </code>
     </em>
     using a parser specified by OID. See
     <a class="xref" href="textsearch-debugging.md#TEXTSEARCH-PARSER-TESTING" title="12.8.2. Parser Testing">
      Section 12.8.2
     </a>
     for details.
    </p>
    <p>
     <code>
      ts_parse(3722, 'foo - bar')
     </code>
     →
     <code>
      (1,foo) ...
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ts_token_type
     </code>
     (
     <em class="parameter">
      <code>
       parser_name
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       tokid
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       alias
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       description
      </code>
     </em>
     <code>
      text
     </code>
     )
    </p>
    <p>
     Returns a table that describes each type of token the named parser can recognize. See
     <a class="xref" href="textsearch-debugging.md#TEXTSEARCH-PARSER-TESTING" title="12.8.2. Parser Testing">
      Section 12.8.2
     </a>
     for details.
    </p>
    <p>
     <code>
      ts_token_type('default')
     </code>
     →
     <code>
      (1,asciiword,"Word, all ASCII") ...
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ts_token_type
     </code>
     (
     <em class="parameter">
      <code>
       parser_oid
      </code>
     </em>
     <code>
      oid
     </code>
     ) →
     <code>
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       tokid
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       alias
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       description
      </code>
     </em>
     <code>
      text
     </code>
     )
    </p>
    <p>
     Returns a table that describes each type of token a parser specified by OID can recognize. See
     <a class="xref" href="textsearch-debugging.md#TEXTSEARCH-PARSER-TESTING" title="12.8.2. Parser Testing">
      Section 12.8.2
     </a>
     for details.
    </p>
    <p>
     <code>
      ts_token_type(3722)
     </code>
     →
     <code>
      (1,asciiword,"Word, all ASCII") ...
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ts_stat
     </code>
     (
     <em class="parameter">
      <code>
       sqlquery
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        weights
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] ) →
     <code>
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       word
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       ndoc
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       nentry
      </code>
     </em>
     <code>
      integer
     </code>
     )
    </p>
    <p>
     Executes the
     <em class="parameter">
      <code>
       sqlquery
      </code>
     </em>
     , which must return a single
     <code>
      tsvector
     </code>
     column, and returns statistics about each distinct lexeme contained in the data. See
     <a class="xref" href="textsearch-features.md#TEXTSEARCH-STATISTICS" title="12.4.4. Gathering Document Statistics">
      Section 12.4.4
     </a>
     for details.
    </p>
    <p>
     <code>
      ts_stat('SELECT vector FROM apod')
     </code>
     →
     <code>
      (foo,10,15) ...
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>
