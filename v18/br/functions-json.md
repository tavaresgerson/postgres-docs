## 9.16. Funções e operadores JSON [#](#FUNCTIONS-JSON)

* [9.16.1. Processamento e criação de dados JSON](functions-json.md#FUNCTIONS-JSON-PROCESSING)
* [9.16.2. A linguagem de caminho SQL/JSON](functions-json.md#FUNCTIONS-SQLJSON-PATH)
* [9.16.3. Funções de consulta SQL/JSON](functions-json.md#SQLJSON-QUERY-FUNCTIONS)
* [9.16.4. JSON_TABLE](functions-json.md#FUNCTIONS-SQLJSON-TABLE)

Esta seção descreve:

* funções e operadores para processamento e criação de dados JSON
* o idioma de caminho SQL/JSON
* as funções de consulta SQL/JSON

Para fornecer suporte nativo aos tipos de dados JSON no ambiente SQL, o PostgreSQL implementa o *modelo de dados SQL/JSON*. Este modelo compreende sequências de itens. Cada item pode conter valores escalares SQL, com um valor nulo SQL/JSON adicional, e estruturas de dados compostas que utilizam arrays e objetos JSON. O modelo é uma formalização do modelo de dados implícito na especificação JSON [RFC 7159](https://datatracker.ietf.org/doc/html/rfc7159).

SQL/JSON permite que você manipule dados JSON juntamente com dados SQL regulares, com suporte a transações, incluindo:

* Carregar dados JSON no banco de dados e armazená-los em colunas regulares do SQL como strings de caracteres ou binárias.
* Gerar objetos e matrizes JSON a partir de dados relacionais.
* Consultar dados JSON usando funções de consulta SQL/JSON e expressões de linguagem de caminho SQL/JSON.

Para saber mais sobre o padrão SQL/JSON, consulte [[sqltr-19075-6]] (biblio.md#SQLTR-19075-6 "SQL Technical Report"). Para detalhes sobre os tipos de JSON suportados no PostgreSQL, consulte [Seção 8.14](datatype-json.md).

### 9.16.1. Processamento e criação de dados JSON [#](#FUNCTIONS-JSON-PROCESSING)

[Tabela 9.47](functions-json.md#FUNCTIONS-JSON-OP-TABLE) mostra os operadores disponíveis para uso com tipos de dados JSON (ver [Seção 8.14](datatype-json.md)). Além disso, os operadores de comparação comuns mostrados em [Tabela 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) estão disponíveis para `jsonb`, embora não para `json`. Os operadores de comparação seguem as regras de ordenação para operações de B-tree descritas em [Seção 8.14.4](datatype-json.md#JSON-INDEXING). Veja também [Seção 9.21](functions-aggregate.md) para a função agregada `json_agg` que agrega valores de registro como JSON, a função agregada `json_object_agg` que agrega pares de valores em um objeto JSON, e seus equivalentes `jsonb`, `jsonb_agg` e `jsonb_object_agg`.

**Tabela 9.47. Operadores `json` e `jsonb`**



<table border="1" class="table" summary="json and jsonb Operators">
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
     <code class="type">
      json
     </code>
     <code class="literal">
      -&gt;
     </code>
     <code class="type">
      integer
     </code>
     →
     <code class="returnvalue">
      json
     </code>
    </p>
    <p class="func_signature">
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      -&gt;
     </code>
     <code class="type">
      integer
     </code>
     →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Extractos
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     'O elemento do array JSON (os elementos do array são indexados a partir de zero, mas os inteiros negativos contam a partir do final).
    </p>
    <p>
     <code class="literal">
      '[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::json -&gt; 2
     </code>
     →
     <code class="returnvalue">
      {"c":"baz"}
     </code>
    </p>
    <p>
     <code class="literal">
      '[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::json -&gt; -3
     </code>
     →
     <code class="returnvalue">
      {"a":"foo"}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      json
     </code>
     <code class="literal">
      -&gt;
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      json
     </code>
    </p>
    <p class="func_signature">
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      -&gt;
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Extrai o campo do objeto JSON com a chave fornecida.
    </p>
    <p>
     <code class="literal">
      '{"a": {"b":"foo"}}'::json -&gt; 'a'
     </code>
     →
     <code class="returnvalue">
      {"b":"foo"}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      json
     </code>
     <code class="literal">
      -&gt;&gt;
     </code>
     <code class="type">
      integer
     </code>
     →
     <code class="returnvalue">
      text
     </code>
    </p>
    <p class="func_signature">
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      -&gt;&gt;
     </code>
     <code class="type">
      integer
     </code>
     →
     <code class="returnvalue">
      text
     </code>
    </p>
    <p>
     Extractos
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     'o elemento do array JSON, como
     <code class="type">
      text
     </code>
     .
    </p>
    <p>
     <code class="literal">
      '[1,2,3]'::json -&gt;&gt; 2
     </code>
     →
     <code class="returnvalue">
      3
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      json
     </code>
     <code class="literal">
      -&gt;&gt;
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      text
     </code>
    </p>
    <p class="func_signature">
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      -&gt;&gt;
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      text
     </code>
    </p>
    <p>
     Extrai o campo do objeto JSON com a chave fornecida, como
     <code class="type">
      text
     </code>
     .
    </p>
    <p>
     <code class="literal">
      '{"a":1,"b":2}'::json -&gt;&gt; 'b'
     </code>
     →
     <code class="returnvalue">
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      json
     </code>
     <code class="literal">
      #&gt;
     </code>
     <code class="type">
      text[]
     </code>
     →
     <code class="returnvalue">
      json
     </code>
    </p>
    <p class="func_signature">
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      #&gt;
     </code>
     <code class="type">
      text[]
     </code>
     →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Extrai o subobjeto JSON no caminho especificado, onde os elementos do caminho podem ser chaves de campo ou índices de matriz.
    </p>
    <p>
     <code class="literal">
      '{"a": {"b": ["foo","bar"]}}'::json #&gt; '{a,b,1}'
     </code>
     →
     <code class="returnvalue">
      "bar"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      json
     </code>
     <code class="literal">
      #&gt;&gt;
     </code>
     <code class="type">
      text[]
     </code>
     →
     <code class="returnvalue">
      text
     </code>
    </p>
    <p class="func_signature">
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      #&gt;&gt;
     </code>
     <code class="type">
      text[]
     </code>
     →
     <code class="returnvalue">
      text
     </code>
    </p>
    <p>
     Extrai o subobjeto JSON no caminho especificado como
     <code class="type">
      text
     </code>
     .
    </p>
    <p>
     <code class="literal">
      '{"a": {"b": ["foo","bar"]}}'::json #&gt;&gt; '{a,b,1}'
     </code>
     →
     <code class="returnvalue">
      bar
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>









### Nota

Os operadores de extração de campo/elemento/caminho retornam NULL, em vez de falhar, se a entrada JSON não tiver a estrutura correta para corresponder à solicitação; por exemplo, se não existir tal chave ou elemento de matriz.

Alguns operadores adicionais existem apenas para `jsonb`, conforme mostrado na [Tabela 9.48](functions-json.md#FUNCTIONS-JSONB-OP-TABLE). [Seção 8.14.4](datatype-json.md#JSON-INDEXING) descreve como esses operadores podem ser usados para pesquisar efetivamente dados indexados de `jsonb`.

**Tabela 9.48. Operadores adicionais do `jsonb`**



<table border="1" class="table" summary="Additional jsonb Operators">
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
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      @&gt;
     </code>
     <code class="type">
      jsonb
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     O primeiro valor JSON contém o segundo? (Veja
     <a class="xref" href="datatype-json.md#JSON-CONTAINMENT" title="8.14.3. jsonb Containment and Existence">
      Seção 8.14.3
     </a>
     para obter detalhes sobre contenção.)
    </p>
    <p>
     <code class="literal">
      '{"a":1, "b":2}'::jsonb @&gt; '{"b":2}'::jsonb
     </code>
     →
     <code class="returnvalue">
      t
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      &lt;@
     </code>
     <code class="type">
      jsonb
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     O primeiro valor JSON está contido no segundo?
    </p>
    <p>
     <code class="literal">
      '{"b":2}'::jsonb &lt;@ '{"a":1, "b":2}'::jsonb
     </code>
     →
     <code class="returnvalue">
      t
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      ?
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     A string de texto existe como uma chave de nível superior ou elemento de matriz dentro do valor JSON?
    </p>
    <p>
     <code class="literal">
      '{"a":1, "b":2}'::jsonb ? 'b'
     </code>
     →
     <code class="returnvalue">
      t
     </code>
    </p>
    <p>
     <code class="literal">
      '["a", "b", "c"]'::jsonb ? 'b'
     </code>
     →
     <code class="returnvalue">
      t
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      ?|
     </code>
     <code class="type">
      text[]
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Algumas das strings na matriz de texto existem como chaves de nível superior ou elementos da matriz?
    </p>
    <p>
     <code class="literal">
      '{"a":1, "b":2, "c":3}'::jsonb ?| array['b', 'd']
     </code>
     →
     <code class="returnvalue">
      t
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      ?&amp;
     </code>
     <code class="type">
      text[]
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Todas as strings na matriz de texto existem como chaves de nível superior ou elementos da matriz?
    </p>
    <p>
     <code class="literal">
      '["a", "b", "c"]'::jsonb ?&amp; array['a', 'b']
     </code>
     →
     <code class="returnvalue">
      t
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      ||
     </code>
     <code class="type">
      jsonb
     </code>
     →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Concatenam dois
     <code class="type">
      jsonb
     </code>
     valores. A concatenação de dois arrays gera um array que contém todos os elementos de cada entrada. A concatenação de dois objetos gera um objeto que contém a união de suas chaves, tomando o valor do segundo objeto quando há chaves duplicadas. Todos os outros casos são tratados convertendo uma entrada que não é um array em um array de um único elemento, e então procedendo como para dois arrays. Não opera recursivamente: apenas a estrutura de array ou objeto de nível superior é montada.
    </p>
    <p>
     <code class="literal">
      '["a", "b"]'::jsonb || '["a", "d"]'::jsonb
     </code>
     →
     <code class="returnvalue">
      ["a", "b", "a", "d"]
     </code>
    </p>
    <p>
     <code class="literal">
      '{"a": "b"}'::jsonb || '{"c": "d"}'::jsonb
     </code>
     →
     <code class="returnvalue">
      {"a": "b", "c": "d"}
     </code>
    </p>
    <p>
     <code class="literal">
      '[1, 2]'::jsonb || '3'::jsonb
     </code>
     →
     <code class="returnvalue">
      [1, 2, 3]
     </code>
    </p>
    <p>
     <code class="literal">
      '{"a": "b"}'::jsonb || '42'::jsonb
     </code>
     →
     <code class="returnvalue">
      [{"a": "b"}, 42]
     </code>
    </p>
    <p>
     Para adicionar um array a outro array como uma única entrada, envolva-o em uma camada adicional de array, por exemplo:
    </p>
    <p>
     <code class="literal">
      '[1, 2]'::jsonb || jsonb_build_array('[3, 4]'::jsonb)
     </code>
     →
     <code class="returnvalue">
      [1, 2, [3, 4]]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      -
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Exclui uma chave (e seu valor) de um objeto JSON ou valores de string correspondentes de um array JSON.
    </p>
    <p>
     <code class="literal">
      '{"a": "b", "c": "d"}'::jsonb - 'a'
     </code>
     →
     <code class="returnvalue">
      {"c": "d"}
     </code>
    </p>
    <p>
     <code class="literal">
      '["a", "b", "c", "b"]'::jsonb - 'b'
     </code>
     →
     <code class="returnvalue">
      ["a", "c"]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      -
     </code>
     <code class="type">
      text[]
     </code>
     →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Exclui todas as chaves ou elementos de array correspondentes do operando esquerdo.
    </p>
    <p>
     <code class="literal">
      '{"a": "b", "c": "d"}'::jsonb - '{a,c}'::text[]
     </code>
     →
     <code class="returnvalue">
      {}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      -
     </code>
     <code class="type">
      integer
     </code>
     →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Exclui o elemento do array com o índice especificado (contando valores negativos a partir do final). Lança um erro se o valor JSON não for um array.
    </p>
    <p>
     <code class="literal">
      '["a", "b"]'::jsonb - 1
     </code>
     →
     <code class="returnvalue">
      ["a"]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      #-
     </code>
     <code class="type">
      text[]
     </code>
     →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Exclui o campo ou o elemento do array no caminho especificado, onde os elementos do caminho podem ser chaves de campo ou índices de array.
    </p>
    <p>
     <code class="literal">
      '["a", {"b":1}]'::jsonb #- '{1,b}'
     </code>
     →
     <code class="returnvalue">
      ["a", {}]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      @?
     </code>
     <code class="type">
      jsonpath
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     O caminho JSON retorna algum item para o valor JSON especificado? (Isso é útil apenas com expressões de caminho JSON padrão de SQL, não
     <a class="link" href="functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS" title="9.16.2.1.1. Boolean Predicate Check Expressions">
      verificação de predicado
     </a>
     , pois esses sempre retornam um valor.)
    </p>
    <p>
     <code class="literal">
      '{"a":[1,2,3,4,5]}'::jsonb @? '$.a[*] ? (@ &gt; 2)'
     </code>
     →
     <code class="returnvalue">
      t
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      jsonb
     </code>
     <code class="literal">
      @@
     </code>
     <code class="type">
      jsonpath
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Retorna o resultado de uma verificação de predicado de caminho JSON para o valor JSON especificado. (Isso é útil apenas com
     <a class="link" href="functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS" title="9.16.2.1.1. Boolean Predicate Check Expressions">
      expressões de verificação de predicado
     </a>
     , não expressões de caminho JSON padrão do SQL, pois ele retornará
     <code class="literal">
      NULL
     </code>
     se o resultado do caminho não for um único valor booleano.)
    </p>
    <p>
     <code class="literal">
      '{"a":[1,2,3,4,5]}'::jsonb @@ '$.a[*] &gt; 2'
     </code>
     →
     <code class="returnvalue">
      t
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>









### Nota

Os operadores `jsonpath` `@?` e `@@` suprimem os seguintes erros: campo ou elemento de matriz de objeto ausente, tipo inesperado de item JSON, erros de data e número. As funções relacionadas ao `jsonpath` descritas abaixo também podem ser informadas para suprimir esses tipos de erros. Esse comportamento pode ser útil ao pesquisar coleções de documentos JSON de estrutura variável.

[Tabela 9.49](functions-json.md#FUNCTIONS-JSON-CREATION-TABLE "Table 9.49. JSON Creation Functions") mostra as funções disponíveis para a construção dos valores de `json` e `jsonb`. Algumas funções nesta tabela têm uma cláusula `RETURNING`, que especifica o tipo de dados retornado. Deve ser um dos tipos `json`, `jsonb`, `bytea`, uma cadeia de caracteres (`text`, `char` ou `varchar`) ou um tipo que pode ser convertido para `json`. Por padrão, o tipo `json` é retornado.

**Tabela 9.49. Funções de criação de JSON**



<table border="1" class="table" summary="JSON Creation Functions">
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
     <code class="function">
      to_json
     </code>
     (
     <code class="type">
      anyelement
     </code>
     ) →
     <code class="returnvalue">
      json
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      to_jsonb
     </code>
     (
     <code class="type">
      anyelement
     </code>
     ) →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Converts any SQL value to
     <code class="type">
      json
     </code>
     or
     <code class="type">
      jsonb
     </code>
     . Arrays and composites are converted recursively to arrays and objects (multidimensional arrays become arrays of arrays in JSON). Otherwise, if there is a cast from the SQL data type to
     <code class="type">
      json
     </code>
     , the cast function will be used to perform the conversion;
     <a class="footnote" href="#ftn.id-1.5.8.22.8.9.2.2.1.1.3.4">
      <sup class="footnote" id="id-1.5.8.22.8.9.2.2.1.1.3.4">
       [a]
      </sup>
     </a>
     otherwise, a scalar JSON value is produced.  For any scalar other than a number, a Boolean, or a null value, the text representation will be used, with escaping as necessary to make it a valid JSON string value.
    </p>
    <p>
     <code class="literal">
      to_json('Fred said "Hi."'::text)
     </code>
     →
     <code class="returnvalue">
      "Fred said \"Hi.\""
     </code>
    </p>
    <p>
     <code class="literal">
      to_jsonb(row(42, 'Fred said "Hi."'::text))
     </code>
     →
     <code class="returnvalue">
      {"f1": 42, "f2": "Fred said \"Hi.\""}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      array_to_json
     </code>
     (
     <code class="type">
      anyarray
     </code>
     [
     <span class="optional">
      ,
      <code class="type">
       boolean
      </code>
     </span>
     ] ) →
     <code class="returnvalue">
      json
     </code>
    </p>
    <p>
     Converts an SQL array to a JSON array.  The behavior is the same as
     <code class="function">
      to_json
     </code>
     except that line feeds will be added between top-level array elements if the optional boolean parameter is true.
    </p>
    <p>
     <code class="literal">
      array_to_json('{{1,5},{99,100}}'::int[])
     </code>
     →
     <code class="returnvalue">
      [[1,5],[99,100]]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_array
     </code>
     ( [
     <span class="optional">
      {
      <em class="replaceable">
       <code>
        value_expression
       </code>
      </em>
      [
      <span class="optional">
       <code class="literal">
        FORMAT JSON
       </code>
      </span>
      ] } [
      <span class="optional">
       , ...
      </span>
      ]
     </span>
     ] [
     <span class="optional">
      {
      <code class="literal">
       NULL
      </code>
      |
      <code class="literal">
       ABSENT
      </code>
      }
      <code class="literal">
       ON NULL
      </code>
     </span>
     ] [
     <span class="optional">
      <code class="literal">
       RETURNING
      </code>
      <em class="replaceable">
       <code>
        data_type
       </code>
      </em>
      [
      <span class="optional">
       <code class="literal">
        FORMAT JSON
       </code>
       [
       <span class="optional">
        <code class="literal">
         ENCODING UTF8
        </code>
       </span>
       ]
      </span>
      ]
     </span>
     ])
    </p>
    <p class="func_signature">
     <code class="function">
      json_array
     </code>
     ( [
     <span class="optional">
      <em class="replaceable">
       <code>
        query_expression
       </code>
      </em>
     </span>
     ] [
     <span class="optional">
      <code class="literal">
       RETURNING
      </code>
      <em class="replaceable">
       <code>
        data_type
       </code>
      </em>
      [
      <span class="optional">
       <code class="literal">
        FORMAT JSON
       </code>
       [
       <span class="optional">
        <code class="literal">
         ENCODING UTF8
        </code>
       </span>
       ]
      </span>
      ]
     </span>
     ])
    </p>
    <p>
     Constructs a JSON array from either a series of
     <em class="replaceable">
      <code>
       value_expression
      </code>
     </em>
     parameters or from the results of
     <em class="replaceable">
      <code>
       query_expression
      </code>
     </em>
     , which must be a SELECT query returning a single column. If
     <code class="literal">
      ABSENT ON NULL
     </code>
     is specified, NULL values are ignored. This is always the case if a
     <em class="replaceable">
      <code>
       query_expression
      </code>
     </em>
     is used.
    </p>
    <p>
     <code class="literal">
      json_array(1,true,json '{"a":null}')
     </code>
     →
     <code class="returnvalue">
      [1, true, {"a":null}]
     </code>
    </p>
    <p>
     <code class="literal">
      json_array(SELECT * FROM (VALUES(1),(2)) t)
     </code>
     →
     <code class="returnvalue">
      [1, 2]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      row_to_json
     </code>
     (
     <code class="type">
      record
     </code>
     [
     <span class="optional">
      ,
      <code class="type">
       boolean
      </code>
     </span>
     ] ) →
     <code class="returnvalue">
      json
     </code>
    </p>
    <p>
     Converts an SQL composite value to a JSON object.  The behavior is the same as
     <code class="function">
      to_json
     </code>
     except that line feeds will be added between top-level elements if the optional boolean parameter is true.
    </p>
    <p>
     <code class="literal">
      row_to_json(row(1,'foo'))
     </code>
     →
     <code class="returnvalue">
      {"f1":1,"f2":"foo"}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_build_array
     </code>
     (
     <code class="literal">
      VARIADIC
     </code>
     <code class="type">
      "any"
     </code>
     ) →
     <code class="returnvalue">
      json
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_build_array
     </code>
     (
     <code class="literal">
      VARIADIC
     </code>
     <code class="type">
      "any"
     </code>
     ) →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Builds a possibly-heterogeneously-typed JSON array out of a variadic argument list.  Each argument is converted as per
     <code class="function">
      to_json
     </code>
     or
     <code class="function">
      to_jsonb
     </code>
     .
    </p>
    <p>
     <code class="literal">
      json_build_array(1, 2, 'foo', 4, 5)
     </code>
     →
     <code class="returnvalue">
      [1, 2, "foo", 4, 5]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_build_object
     </code>
     (
     <code class="literal">
      VARIADIC
     </code>
     <code class="type">
      "any"
     </code>
     ) →
     <code class="returnvalue">
      json
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_build_object
     </code>
     (
     <code class="literal">
      VARIADIC
     </code>
     <code class="type">
      "any"
     </code>
     ) →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Builds a JSON object out of a variadic argument list.  By convention, the argument list consists of alternating keys and values.  Key arguments are coerced to text; value arguments are converted as per
     <code class="function">
      to_json
     </code>
     or
     <code class="function">
      to_jsonb
     </code>
     .
    </p>
    <p>
     <code class="literal">
      json_build_object('foo', 1, 2, row(3,'bar'))
     </code>
     →
     <code class="returnvalue">
      {"foo" : 1, "2" : {"f1":3,"f2":"bar"}}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_object
     </code>
     ( [
     <span class="optional">
      {
      <em class="replaceable">
       <code>
        key_expression
       </code>
      </em>
      {
      <code class="literal">
       VALUE
      </code>
      | ':' }
      <em class="replaceable">
       <code>
        value_expression
       </code>
      </em>
      [
      <span class="optional">
       <code class="literal">
        FORMAT JSON
       </code>
       [
       <span class="optional">
        <code class="literal">
         ENCODING UTF8
        </code>
       </span>
       ]
      </span>
      ] }[
      <span class="optional">
       , ...
      </span>
      ]
     </span>
     ] [
     <span class="optional">
      {
      <code class="literal">
       NULL
      </code>
      |
      <code class="literal">
       ABSENT
      </code>
      }
      <code class="literal">
       ON NULL
      </code>
     </span>
     ] [
     <span class="optional">
      {
      <code class="literal">
       WITH
      </code>
      |
      <code class="literal">
       WITHOUT
      </code>
      }
      <code class="literal">
       UNIQUE
      </code>
      [
      <span class="optional">
       <code class="literal">
        KEYS
       </code>
      </span>
      ]
     </span>
     ] [
     <span class="optional">
      <code class="literal">
       RETURNING
      </code>
      <em class="replaceable">
       <code>
        data_type
       </code>
      </em>
      [
      <span class="optional">
       <code class="literal">
        FORMAT JSON
       </code>
       [
       <span class="optional">
        <code class="literal">
         ENCODING UTF8
        </code>
       </span>
       ]
      </span>
      ]
     </span>
     ])
    </p>
    <p>
     Constructs a JSON object of all the key/value pairs given, or an empty object if none are given.
     <em class="replaceable">
      <code>
       key_expression
      </code>
     </em>
     is a scalar expression defining the
     <acronym class="acronym">
      JSON
     </acronym>
     key, which is converted to the
     <code class="type">
      text
     </code>
     type. It cannot be
     <code class="literal">
      NULL
     </code>
     nor can it belong to a type that has a cast to the
     <code class="type">
      json
     </code>
     type. If
     <code class="literal">
      WITH UNIQUE KEYS
     </code>
     is specified, there must not be any duplicate
     <em class="replaceable">
      <code>
       key_expression
      </code>
     </em>
     . Any pair for which the
     <em class="replaceable">
      <code>
       value_expression
      </code>
     </em>
     evaluates to
     <code class="literal">
      NULL
     </code>
     is omitted from the output if
     <code class="literal">
      ABSENT ON NULL
     </code>
     is specified; if
     <code class="literal">
      NULL ON NULL
     </code>
     is specified or the clause omitted, the key is included with value
     <code class="literal">
      NULL
     </code>
     .
    </p>
    <p>
     <code class="literal">
      json_object('code' VALUE 'P123', 'title': 'Jaws')
     </code>
     →
     <code class="returnvalue">
      {"code" : "P123", "title" : "Jaws"}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_object
     </code>
     (
     <code class="type">
      text[]
     </code>
     ) →
     <code class="returnvalue">
      json
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_object
     </code>
     (
     <code class="type">
      text[]
     </code>
     ) →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Builds a JSON object out of a text array.  The array must have either exactly one dimension with an even number of members, in which case they are taken as alternating key/value pairs, or two dimensions such that each inner array has exactly two elements, which are taken as a key/value pair.  All values are converted to JSON strings.
    </p>
    <p>
     <code class="literal">
      json_object('{a, 1, b, "def", c, 3.5}')
     </code>
     →
     <code class="returnvalue">
      {"a" : "1", "b" : "def", "c" : "3.5"}
     </code>
    </p>
    <p>
     <code class="literal">
      json_object('{{a, 1}, {b, "def"}, {c, 3.5}}')
     </code>
     →
     <code class="returnvalue">
      {"a" : "1", "b" : "def", "c" : "3.5"}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_object
     </code>
     (
     <em class="parameter">
      <code>
       keys
      </code>
     </em>
     <code class="type">
      text[]
     </code>
     ,
     <em class="parameter">
      <code>
       values
      </code>
     </em>
     <code class="type">
      text[]
     </code>
     ) →
     <code class="returnvalue">
      json
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_object
     </code>
     (
     <em class="parameter">
      <code>
       keys
      </code>
     </em>
     <code class="type">
      text[]
     </code>
     ,
     <em class="parameter">
      <code>
       values
      </code>
     </em>
     <code class="type">
      text[]
     </code>
     ) →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     This form of
     <code class="function">
      json_object
     </code>
     takes keys and values pairwise from separate text arrays.  Otherwise it is identical to the one-argument form.
    </p>
    <p>
     <code class="literal">
      json_object('{a,b}', '{1,2}')
     </code>
     →
     <code class="returnvalue">
      {"a": "1", "b": "2"}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json
     </code>
     (
     <em class="replaceable">
      <code>
       expression
      </code>
     </em>
     [
     <span class="optional">
      <code class="literal">
       FORMAT JSON
      </code>
      [
      <span class="optional">
       <code class="literal">
        ENCODING UTF8
       </code>
      </span>
      ]
     </span>
     ] [
     <span class="optional">
      {
      <code class="literal">
       WITH
      </code>
      |
      <code class="literal">
       WITHOUT
      </code>
      }
      <code class="literal">
       UNIQUE
      </code>
      [
      <span class="optional">
       <code class="literal">
        KEYS
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code class="returnvalue">
      json
     </code>
    </p>
    <p>
     Converts a given expression specified as
     <code class="type">
      text
     </code>
     or
     <code class="type">
      bytea
     </code>
     string (in UTF8 encoding) into a JSON value.  If
     <em class="replaceable">
      <code>
       expression
      </code>
     </em>
     is NULL, an
     <acronym class="acronym">
      SQL
     </acronym>
     null value is returned. If
     <code class="literal">
      WITH UNIQUE
     </code>
     is specified, the
     <em class="replaceable">
      <code>
       expression
      </code>
     </em>
     must not contain any duplicate object keys.
    </p>
    <p>
     <code class="literal">
      json('{"a":123, "b":[true,"foo"], "a":"bar"}')
     </code>
     →
     <code class="returnvalue">
      {"a":123, "b":[true,"foo"], "a":"bar"}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_scalar
     </code>
     (
     <em class="replaceable">
      <code>
       expression
      </code>
     </em>
     )
    </p>
    <p>
     Converts a given SQL scalar value into a JSON scalar value. If the input is NULL, an
     <acronym class="acronym">
      SQL
     </acronym>
     null is returned. If the input is number or a boolean value, a corresponding JSON number or boolean value is returned. For any other value, a JSON string is returned.
    </p>
    <p>
     <code class="literal">
      json_scalar(123.45)
     </code>
     →
     <code class="returnvalue">
      123.45
     </code>
    </p>
    <p>
     <code class="literal">
      json_scalar(CURRENT_TIMESTAMP)
     </code>
     →
     <code class="returnvalue">
      "2022-05-10T10:51:04.62128-04:00"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_serialize
     </code>
     (
     <em class="replaceable">
      <code>
       expression
      </code>
     </em>
     [
     <span class="optional">
      <code class="literal">
       FORMAT JSON
      </code>
      [
      <span class="optional">
       <code class="literal">
        ENCODING UTF8
       </code>
      </span>
      ]
     </span>
     ] [
     <span class="optional">
      <code class="literal">
       RETURNING
      </code>
      <em class="replaceable">
       <code>
        data_type
       </code>
      </em>
      [
      <span class="optional">
       <code class="literal">
        FORMAT JSON
       </code>
       [
       <span class="optional">
        <code class="literal">
         ENCODING UTF8
        </code>
       </span>
       ]
      </span>
      ]
     </span>
     ] )
    </p>
    <p>
     Converts an SQL/JSON expression into a character or binary string. The
     <em class="replaceable">
      <code>
       expression
      </code>
     </em>
     can be of any JSON type, any character string type, or
     <code class="type">
      bytea
     </code>
     in UTF8 encoding. The returned type used in
     <code class="literal">
      RETURNING
     </code>
     can be any character string type or
     <code class="type">
      bytea
     </code>
     . The default is
     <code class="type">
      text
     </code>
     .
    </p>
    <p>
     <code class="literal">
      json_serialize('{ "a" : 1 } ' RETURNING bytea)
     </code>
     →
     <code class="returnvalue">
      \x7b20226122203a2031207d20
     </code>
    </p>
   </td>
  </tr>
 </tbody>
 <tbody class="footnotes">
  <tr>
   <td colspan="1">
    <div class="footnote" id="ftn.id-1.5.8.22.8.9.2.2.1.1.3.4">
     <p>
      <a class="para" href="#id-1.5.8.22.8.9.2.2.1.1.3.4">
       <sup class="para">
        [a]
       </sup>
      </a>
      For example, the
      <a class="xref" href="hstore.md" title="F.17. hstore — hstore key/value datatype">
       hstore
      </a>
      extension has a cast from
      <code class="type">
       hstore
      </code>
      to
      <code class="type">
       json
      </code>
      , so that
      <code class="type">
       hstore
      </code>
      values converted via the JSON creation functions will be represented as JSON objects, not as primitive string values.
     </p>
    </div>
   </td>
  </tr>
 </tbody>
</table>









[Tabela 9.50](functions-json.md#FUNCTIONS-SQLJSON-MISC "Table 9.50. SQL/JSON Testing Functions") detalha as facilidades SQL/JSON para testar JSON.

**Tabela 9.50. Funções de teste SQL/JSON**



<table border="1" class="table" summary="SQL/JSON Testing Functions">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Assinatura da função
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
     <em class="replaceable">
      <code>
       expression
      </code>
     </em>
     <code class="literal">
      IS
     </code>
     [
     <span class="optional">
      <code class="literal">
       NOT
      </code>
     </span>
     ]
     <code class="literal">
      JSON
     </code>
     [
     <span class="optional">
      { English: The 2018 FIFA World Cup is the 21st FIFA World Cup and the first to be held in Asia. Portuguese (Brazilian): A Copa do Mundo da FIFA de 2018 é a 21ª Copa do Mundo da FIFA e a primeira a ser realizada na Ásia.
      <code class="literal">
       VALUE
      </code>
      |
      <code class="literal">
       SCALAR
      </code>
      |
      <code class="literal">
       ARRAY
      </code>
      |
      <code class="literal">
       OBJECT
      </code>
      }
     </span>
     ] [
     <span class="optional">
      { English: The 2018 FIFA World Cup is the 21st FIFA World Cup and the first to be held in Asia. Portuguese (Brazilian): A Copa do Mundo da FIFA de 2018 é a 21ª Copa do Mundo da FIFA e a primeira a ser realizada na Ásia.
      <code class="literal">
       WITH
      </code>
      |
      <code class="literal">
       WITHOUT
      </code>
      }
      <code class="literal">
       UNIQUE
      </code>
      [
      <span class="optional">
       <code class="literal">
        KEYS
       </code>
      </span>
      ]
     </span>
     ]
    </p>
    <p>
     Este predicado testa se
     <em class="replaceable">
      <code>
       expression
      </code>
     </em>
     pode ser analisado como JSON, possivelmente de um tipo especificado. Se
     <code class="literal">
      SCALAR
     </code>
     ou
     <code class="literal">
      ARRAY
     </code>
     ou
     <code class="literal">
      OBJECT
     </code>
     é especificado, o teste é se o JSON é ou não desse tipo específico. Se
     <code class="literal">
      WITH UNIQUE KEYS
     </code>
     se especificado, então qualquer objeto no
     <em class="replaceable">
      <code>
       expression
      </code>
     </em>
     também é testado para verificar se ele tem chaves duplicadas.
    </p>
    <p>
    </p>
    <pre class="programlisting">
SELECT js, js IS JSON "json?", js IS JSON SCALAR "scalar?", js IS JSON OBJECT "object?", js IS JSON ARRAY "array?" FROM (VALUES ('123'), ('"abc"'), ('{"a": "b"}'), ('[1,2]'),('abc')) foo(js); js     | json? | scalar? | object? | array? ------------+-------+---------+---------+-------- 123        | t     | t       | f       | f "abc"      | t     | t       | f       | f {"a": "b"} | t     | f       | t       | f [1,2]      | t     | f       | f       | t abc        | f     | f       | f       | f
</pre>
    <p>
    </p>
    <p>
    </p>
    <pre class="programlisting">
SELECT js, js IS JSON OBJECT "object?", js IS JSON ARRAY "array?", js IS JSON ARRAY WITH UNIQUE KEYS "array w. UK?", js IS JSON ARRAY WITHOUT UNIQUE KEYS "array w/o UK?" FROM (VALUES ('[{"a":"1"}, {"b":"2","b":"3"}]')) foo(js); -[ RECORD 1 ]-+-------------------- js            | [{"a":"1"},        +
              |  {"b":"2","b":"3"}]
object?       | f array?        | t array w. UK?  | f array w/o UK? | t
</pre>
    <p>
    </p>
   </td>
  </tr>
 </tbody>
</table>









[Tabela 9.51](functions-json.md#FUNCTIONS-JSON-PROCESSING-TABLE) mostra as funções disponíveis para o processamento dos valores de `json` e `jsonb`.

**Tabela 9.51. Funções de processamento JSON**



<table border="1" class="table" summary="JSON Processing Functions">
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
     <code class="function">
      json_array_elements
     </code>
     (
     <code class="type">
      json
     </code>
     ) →
     <code class="returnvalue">
      setof json
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_array_elements
     </code>
     (
     <code class="type">
      jsonb
     </code>
     ) →
     <code class="returnvalue">
      setof jsonb
     </code>
    </p>
    <p>
     Expands the top-level JSON array into a set of JSON values.
    </p>
    <p>
     <code class="literal">
      select * from json_array_elements('[1,true, [2,false]]')
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
   value ----------- 1 true [2,false]
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_array_elements_text
     </code>
     (
     <code class="type">
      json
     </code>
     ) →
     <code class="returnvalue">
      setof text
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_array_elements_text
     </code>
     (
     <code class="type">
      jsonb
     </code>
     ) →
     <code class="returnvalue">
      setof text
     </code>
    </p>
    <p>
     Expands the top-level JSON array into a set of
     <code class="type">
      text
     </code>
     values.
    </p>
    <p>
     <code class="literal">
      select * from json_array_elements_text('["foo", "bar"]')
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
   value ----------- foo bar
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_array_length
     </code>
     (
     <code class="type">
      json
     </code>
     ) →
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_array_length
     </code>
     (
     <code class="type">
      jsonb
     </code>
     ) →
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Returns the number of elements in the top-level JSON array.
    </p>
    <p>
     <code class="literal">
      json_array_length('[1,2,3,{"f1":1,"f2":[5,6]},4]')
     </code>
     →
     <code class="returnvalue">
      5
     </code>
    </p>
    <p>
     <code class="literal">
      jsonb_array_length('[]')
     </code>
     →
     <code class="returnvalue">
      0
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_each
     </code>
     (
     <code class="type">
      json
     </code>
     ) →
     <code class="returnvalue">
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code class="type">
      text
     </code>
     ,
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code class="type">
      json
     </code>
     )
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_each
     </code>
     (
     <code class="type">
      jsonb
     </code>
     ) →
     <code class="returnvalue">
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code class="type">
      text
     </code>
     ,
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     )
    </p>
    <p>
     Expands the top-level JSON object into a set of key/value pairs.
    </p>
    <p>
     <code class="literal">
      select * from json_each('{"a":"foo", "b":"bar"}')
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
 key | value -----+------- a   | "foo" b   | "bar"
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_each_text
     </code>
     (
     <code class="type">
      json
     </code>
     ) →
     <code class="returnvalue">
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code class="type">
      text
     </code>
     ,
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code class="type">
      text
     </code>
     )
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_each_text
     </code>
     (
     <code class="type">
      jsonb
     </code>
     ) →
     <code class="returnvalue">
      setof record
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code class="type">
      text
     </code>
     ,
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code class="type">
      text
     </code>
     )
    </p>
    <p>
     Expands the top-level JSON object into a set of key/value pairs. The returned
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     s will be of type
     <code class="type">
      text
     </code>
     .
    </p>
    <p>
     <code class="literal">
      select * from json_each_text('{"a":"foo", "b":"bar"}')
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
 key | value -----+------- a   | foo b   | bar
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_extract_path
     </code>
     (
     <em class="parameter">
      <code>
       from_json
      </code>
     </em>
     <code class="type">
      json
     </code>
     ,
     <code class="literal">
      VARIADIC
     </code>
     <em class="parameter">
      <code>
       path_elems
      </code>
     </em>
     <code class="type">
      text[]
     </code>
     ) →
     <code class="returnvalue">
      json
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_extract_path
     </code>
     (
     <em class="parameter">
      <code>
       from_json
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     ,
     <code class="literal">
      VARIADIC
     </code>
     <em class="parameter">
      <code>
       path_elems
      </code>
     </em>
     <code class="type">
      text[]
     </code>
     ) →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Extracts JSON sub-object at the specified path. (This is functionally equivalent to the
     <code class="literal">
      #&gt;
     </code>
     operator, but writing the path out as a variadic list can be more convenient in some cases.)
    </p>
    <p>
     <code class="literal">
      json_extract_path('{"f2":{"f3":1},"f4":{"f5":99,"f6":"foo"}}', 'f4', 'f6')
     </code>
     →
     <code class="returnvalue">
      "foo"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_extract_path_text
     </code>
     (
     <em class="parameter">
      <code>
       from_json
      </code>
     </em>
     <code class="type">
      json
     </code>
     ,
     <code class="literal">
      VARIADIC
     </code>
     <em class="parameter">
      <code>
       path_elems
      </code>
     </em>
     <code class="type">
      text[]
     </code>
     ) →
     <code class="returnvalue">
      text
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_extract_path_text
     </code>
     (
     <em class="parameter">
      <code>
       from_json
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     ,
     <code class="literal">
      VARIADIC
     </code>
     <em class="parameter">
      <code>
       path_elems
      </code>
     </em>
     <code class="type">
      text[]
     </code>
     ) →
     <code class="returnvalue">
      text
     </code>
    </p>
    <p>
     Extracts JSON sub-object at the specified path as
     <code class="type">
      text
     </code>
     . (This is functionally equivalent to the
     <code class="literal">
      #&gt;&gt;
     </code>
     operator.)
    </p>
    <p>
     <code class="literal">
      json_extract_path_text('{"f2":{"f3":1},"f4":{"f5":99,"f6":"foo"}}', 'f4', 'f6')
     </code>
     →
     <code class="returnvalue">
      foo
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_object_keys
     </code>
     (
     <code class="type">
      json
     </code>
     ) →
     <code class="returnvalue">
      setof text
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_object_keys
     </code>
     (
     <code class="type">
      jsonb
     </code>
     ) →
     <code class="returnvalue">
      setof text
     </code>
    </p>
    <p>
     Returns the set of keys in the top-level JSON object.
    </p>
    <p>
     <code class="literal">
      select * from json_object_keys('{"f1":"abc","f2":{"f3":"a", "f4":"b"}}')
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
 json_object_keys ------------------ f1 f2
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_populate_record
     </code>
     (
     <em class="parameter">
      <code>
       base
      </code>
     </em>
     <code class="type">
      anyelement
     </code>
     ,
     <em class="parameter">
      <code>
       from_json
      </code>
     </em>
     <code class="type">
      json
     </code>
     ) →
     <code class="returnvalue">
      anyelement
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_populate_record
     </code>
     (
     <em class="parameter">
      <code>
       base
      </code>
     </em>
     <code class="type">
      anyelement
     </code>
     ,
     <em class="parameter">
      <code>
       from_json
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     ) →
     <code class="returnvalue">
      anyelement
     </code>
    </p>
    <p>
     Expands the top-level JSON object to a row having the composite type of the
     <em class="parameter">
      <code>
       base
      </code>
     </em>
     argument.  The JSON object is scanned for fields whose names match column names of the output row type, and their values are inserted into those columns of the output. (Fields that do not correspond to any output column name are ignored.) In typical use, the value of
     <em class="parameter">
      <code>
       base
      </code>
     </em>
     is just
     <code class="literal">
      NULL
     </code>
     , which means that any output columns that do not match any object field will be filled with nulls.  However, if
     <em class="parameter">
      <code>
       base
      </code>
     </em>
     isn't
     <code class="literal">
      NULL
     </code>
     then the values it contains will be used for unmatched columns.
    </p>
    <p>
     To convert a JSON value to the SQL type of an output column, the following rules are applied in sequence:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist compact" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        A JSON null value is converted to an SQL null in all cases.
       </p>
      </li>
      <li class="listitem">
       <p>
        If the output column is of type
        <code class="type">
         json
        </code>
        or
        <code class="type">
         jsonb
        </code>
        , the JSON value is just reproduced exactly.
       </p>
      </li>
      <li class="listitem">
       <p>
        If the output column is a composite (row) type, and the JSON value is a JSON object, the fields of the object are converted to columns of the output row type by recursive application of these rules.
       </p>
      </li>
      <li class="listitem">
       <p>
        Likewise, if the output column is an array type and the JSON value is a JSON array, the elements of the JSON array are converted to elements of the output array by recursive application of these rules.
       </p>
      </li>
      <li class="listitem">
       <p>
        Otherwise, if the JSON value is a string, the contents of the string are fed to the input conversion function for the column's data type.
       </p>
      </li>
      <li class="listitem">
       <p>
        Otherwise, the ordinary text representation of the JSON value is fed to the input conversion function for the column's data type.
       </p>
      </li>
     </ul>
    </div>
    <p>
    </p>
    <p>
     While the example below uses a constant JSON value, typical use would be to reference a
     <code class="type">
      json
     </code>
     or
     <code class="type">
      jsonb
     </code>
     column laterally from another table in the query's
     <code class="literal">
      FROM
     </code>
     clause.  Writing
     <code class="function">
      json_populate_record
     </code>
     in the
     <code class="literal">
      FROM
     </code>
     clause is good practice, since all of the extracted columns are available for use without duplicate function calls.
    </p>
    <p>
     <code class="literal">
      create type subrowtype as (d int, e text);
     </code>
     <code class="literal">
      create type myrowtype as (a int, b text[], c subrowtype);
     </code>
    </p>
    <p>
     <code class="literal">
      select * from json_populate_record(null::myrowtype, '{"a": 1, "b": ["2", "a b"], "c": {"d": 4, "e": "a  b c"}, "x": "foo"}')
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
 a |   b       |      c ---+-----------+------------- 1 | {2,"a b"} | (4,"a b c")
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      jsonb_populate_record_valid
     </code>
     (
     <em class="parameter">
      <code>
       base
      </code>
     </em>
     <code class="type">
      anyelement
     </code>
     ,
     <em class="parameter">
      <code>
       from_json
      </code>
     </em>
     <code class="type">
      json
     </code>
     ) →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Function for testing
     <code class="function">
      jsonb_populate_record
     </code>
     .  Returns
     <code class="literal">
      true
     </code>
     if the input
     <code class="function">
      jsonb_populate_record
     </code>
     would finish without an error for the given input JSON object; that is, it's valid input,
     <code class="literal">
      false
     </code>
     otherwise.
    </p>
    <p>
     <code class="literal">
      create type jsb_char2 as (a char(2));
     </code>
    </p>
    <p>
     <code class="literal">
      select jsonb_populate_record_valid(NULL::jsb_char2, '{"a": "aaa"}');
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
 jsonb_populate_record_valid ----------------------------- f (1 row)
</pre>
    <p>
     <code class="literal">
      select * from jsonb_populate_record(NULL::jsb_char2, '{"a": "aaa"}') q;
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
ERROR:  value too long for type character(2)
</pre>
    <p>
     <code class="literal">
      select jsonb_populate_record_valid(NULL::jsb_char2, '{"a": "aa"}');
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
 jsonb_populate_record_valid ----------------------------- t (1 row)
</pre>
    <p>
     <code class="literal">
      select * from jsonb_populate_record(NULL::jsb_char2, '{"a": "aa"}') q;
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
 a ---- aa (1 row)
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_populate_recordset
     </code>
     (
     <em class="parameter">
      <code>
       base
      </code>
     </em>
     <code class="type">
      anyelement
     </code>
     ,
     <em class="parameter">
      <code>
       from_json
      </code>
     </em>
     <code class="type">
      json
     </code>
     ) →
     <code class="returnvalue">
      setof anyelement
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_populate_recordset
     </code>
     (
     <em class="parameter">
      <code>
       base
      </code>
     </em>
     <code class="type">
      anyelement
     </code>
     ,
     <em class="parameter">
      <code>
       from_json
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     ) →
     <code class="returnvalue">
      setof anyelement
     </code>
    </p>
    <p>
     Expands the top-level JSON array of objects to a set of rows having the composite type of the
     <em class="parameter">
      <code>
       base
      </code>
     </em>
     argument. Each element of the JSON array is processed as described above for
     <code class="function">
      json[b]_populate_record
     </code>
     .
    </p>
    <p>
     <code class="literal">
      create type twoints as (a int, b int);
     </code>
    </p>
    <p>
     <code class="literal">
      select * from json_populate_recordset(null::twoints, '[{"a":1,"b":2}, {"a":3,"b":4}]')
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
 a | b ---+--- 1 | 2 3 | 4
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_to_record
     </code>
     (
     <code class="type">
      json
     </code>
     ) →
     <code class="returnvalue">
      record
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_to_record
     </code>
     (
     <code class="type">
      jsonb
     </code>
     ) →
     <code class="returnvalue">
      record
     </code>
    </p>
    <p>
     Expands the top-level JSON object to a row having the composite type defined by an
     <code class="literal">
      AS
     </code>
     clause.  (As with all functions returning
     <code class="type">
      record
     </code>
     , the calling query must explicitly define the structure of the record with an
     <code class="literal">
      AS
     </code>
     clause.)  The output record is filled from fields of the JSON object, in the same way as described above for
     <code class="function">
      json[b]_populate_record
     </code>
     .  Since there is no input record value, unmatched columns are always filled with nulls.
    </p>
    <p>
     <code class="literal">
      create type myrowtype as (a int, b text);
     </code>
    </p>
    <p>
     <code class="literal">
      select * from json_to_record('{"a":1,"b":[1,2,3],"c":[1,2,3],"e":"bar","r": {"a": 123, "b": "a b c"}}') as x(a int, b text, c int[], d text, r myrowtype)
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
 a |    b    |    c    | d |       r ---+---------+---------+---+--------------- 1 | [1,2,3] | {1,2,3} |   | (123,"a b c")
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_to_recordset
     </code>
     (
     <code class="type">
      json
     </code>
     ) →
     <code class="returnvalue">
      setof record
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_to_recordset
     </code>
     (
     <code class="type">
      jsonb
     </code>
     ) →
     <code class="returnvalue">
      setof record
     </code>
    </p>
    <p>
     Expands the top-level JSON array of objects to a set of rows having the composite type defined by an
     <code class="literal">
      AS
     </code>
     clause.  (As with all functions returning
     <code class="type">
      record
     </code>
     , the calling query must explicitly define the structure of the record with an
     <code class="literal">
      AS
     </code>
     clause.)  Each element of the JSON array is processed as described above for
     <code class="function">
      json[b]_populate_record
     </code>
     .
    </p>
    <p>
     <code class="literal">
      select * from json_to_recordset('[{"a":1,"b":"foo"}, {"a":"2","c":"bar"}]') as x(a int, b text)
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
 a |  b ---+----- 1 | foo 2 |
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      jsonb_set
     </code>
     (
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     ,
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     <code class="type">
      text[]
     </code>
     ,
     <em class="parameter">
      <code>
       new_value
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        create_if_missing
       </code>
      </em>
      <code class="type">
       boolean
      </code>
     </span>
     ] ) →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Returns
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     with the item designated by
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     replaced by
     <em class="parameter">
      <code>
       new_value
      </code>
     </em>
     , or with
     <em class="parameter">
      <code>
       new_value
      </code>
     </em>
     added if
     <em class="parameter">
      <code>
       create_if_missing
      </code>
     </em>
     is true (which is the default) and the item designated by
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     does not exist. All earlier steps in the path must exist, or the
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     is returned unchanged. As with the path oriented operators, negative integers that appear in the
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     count from the end of JSON arrays. If the last path step is an array index that is out of range, and
     <em class="parameter">
      <code>
       create_if_missing
      </code>
     </em>
     is true, the new value is added at the beginning of the array if the index is negative, or at the end of the array if it is positive.
    </p>
    <p>
     <code class="literal">
      jsonb_set('[{"f1":1,"f2":null},2,null,3]', '{0,f1}', '[2,3,4]', false)
     </code>
     →
     <code class="returnvalue">
      [{"f1": [2, 3, 4], "f2": null}, 2, null, 3]
     </code>
    </p>
    <p>
     <code class="literal">
      jsonb_set('[{"f1":1,"f2":null},2]', '{0,f3}', '[2,3,4]')
     </code>
     →
     <code class="returnvalue">
      [{"f1": 1, "f2": null, "f3": [2, 3, 4]}, 2]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      jsonb_set_lax
     </code>
     (
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     ,
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     <code class="type">
      text[]
     </code>
     ,
     <em class="parameter">
      <code>
       new_value
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        create_if_missing
       </code>
      </em>
      <code class="type">
       boolean
      </code>
      [
      <span class="optional">
       ,
       <em class="parameter">
        <code>
         null_value_treatment
        </code>
       </em>
       <code class="type">
        text
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     If
     <em class="parameter">
      <code>
       new_value
      </code>
     </em>
     is not
     <code class="literal">
      NULL
     </code>
     , behaves identically to
     <code class="literal">
      jsonb_set
     </code>
     . Otherwise behaves according to the value of
     <em class="parameter">
      <code>
       null_value_treatment
      </code>
     </em>
     which must be one of
     <code class="literal">
      'raise_exception'
     </code>
     ,
     <code class="literal">
      'use_json_null'
     </code>
     ,
     <code class="literal">
      'delete_key'
     </code>
     , or
     <code class="literal">
      'return_target'
     </code>
     . The default is
     <code class="literal">
      'use_json_null'
     </code>
     .
    </p>
    <p>
     <code class="literal">
      jsonb_set_lax('[{"f1":1,"f2":null},2,null,3]', '{0,f1}', null)
     </code>
     →
     <code class="returnvalue">
      [{"f1": null, "f2": null}, 2, null, 3]
     </code>
    </p>
    <p>
     <code class="literal">
      jsonb_set_lax('[{"f1":99,"f2":null},2]', '{0,f3}', null, true, 'return_target')
     </code>
     →
     <code class="returnvalue">
      [{"f1": 99, "f2": null}, 2]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      jsonb_insert
     </code>
     (
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     ,
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     <code class="type">
      text[]
     </code>
     ,
     <em class="parameter">
      <code>
       new_value
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        insert_after
       </code>
      </em>
      <code class="type">
       boolean
      </code>
     </span>
     ] ) →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Returns
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     with
     <em class="parameter">
      <code>
       new_value
      </code>
     </em>
     inserted.  If the item designated by the
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     is an array element,
     <em class="parameter">
      <code>
       new_value
      </code>
     </em>
     will be inserted before that item if
     <em class="parameter">
      <code>
       insert_after
      </code>
     </em>
     is false (which is the default), or after it if
     <em class="parameter">
      <code>
       insert_after
      </code>
     </em>
     is true.  If the item designated by the
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     is an object field,
     <em class="parameter">
      <code>
       new_value
      </code>
     </em>
     will be inserted only if the object does not already contain that key. All earlier steps in the path must exist, or the
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     is returned unchanged. As with the path oriented operators, negative integers that appear in the
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     count from the end of JSON arrays. If the last path step is an array index that is out of range, the new value is added at the beginning of the array if the index is negative, or at the end of the array if it is positive.
    </p>
    <p>
     <code class="literal">
      jsonb_insert('{"a": [0,1,2]}', '{a, 1}', '"new_value"')
     </code>
     →
     <code class="returnvalue">
      {"a": [0, "new_value", 1, 2]}
     </code>
    </p>
    <p>
     <code class="literal">
      jsonb_insert('{"a": [0,1,2]}', '{a, 1}', '"new_value"', true)
     </code>
     →
     <code class="returnvalue">
      {"a": [0, 1, "new_value", 2]}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_strip_nulls
     </code>
     (
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code class="type">
      json
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        strip_in_arrays
       </code>
      </em>
      <code class="type">
       boolean
      </code>
     </span>
     ] ) →
     <code class="returnvalue">
      json
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_strip_nulls
     </code>
     (
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        strip_in_arrays
       </code>
      </em>
      <code class="type">
       boolean
      </code>
     </span>
     ] ) →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Deletes all object fields that have null values from the given JSON value, recursively. If
     <em class="parameter">
      <code>
       strip_in_arrays
      </code>
     </em>
     is true (the default is false), null array elements are also stripped. Otherwise they are not stripped. Bare null values are never stripped.
    </p>
    <p>
     <code class="literal">
      json_strip_nulls('[{"f1":1, "f2":null}, 2, null, 3]')
     </code>
     →
     <code class="returnvalue">
      [{"f1":1},2,null,3]
     </code>
    </p>
    <p>
     <code class="literal">
      jsonb_strip_nulls('[1,2,null,3,4]', true)
     </code>
     →
     <code class="returnvalue">
      [1,2,3,4]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      jsonb_path_exists
     </code>
     (
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     ,
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     <code class="type">
      jsonpath
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        vars
       </code>
      </em>
      <code class="type">
       jsonb
      </code>
      [
      <span class="optional">
       ,
       <em class="parameter">
        <code>
         silent
        </code>
       </em>
       <code class="type">
        boolean
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Checks whether the JSON path returns any item for the specified JSON value. (This is useful only with SQL-standard JSON path expressions, not
     <a class="link" href="functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS" title="9.16.2.1.1. Boolean Predicate Check Expressions">
      predicate check expressions
     </a>
     , since those always return a value.) If the
     <em class="parameter">
      <code>
       vars
      </code>
     </em>
     argument is specified, it must be a JSON object, and its fields provide named values to be substituted into the
     <code class="type">
      jsonpath
     </code>
     expression. If the
     <em class="parameter">
      <code>
       silent
      </code>
     </em>
     argument is specified and is
     <code class="literal">
      true
     </code>
     , the function suppresses the same errors as the
     <code class="literal">
      @?
     </code>
     and
     <code class="literal">
      @@
     </code>
     operators do.
    </p>
    <p>
     <code class="literal">
      jsonb_path_exists('{"a":[1,2,3,4,5]}', '$.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max)', '{"min":2, "max":4}')
     </code>
     →
     <code class="returnvalue">
      t
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      jsonb_path_match
     </code>
     (
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     ,
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     <code class="type">
      jsonpath
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        vars
       </code>
      </em>
      <code class="type">
       jsonb
      </code>
      [
      <span class="optional">
       ,
       <em class="parameter">
        <code>
         silent
        </code>
       </em>
       <code class="type">
        boolean
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Returns the SQL boolean result of a JSON path predicate check for the specified JSON value. (This is useful only with
     <a class="link" href="functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS" title="9.16.2.1.1. Boolean Predicate Check Expressions">
      predicate check expressions
     </a>
     , not SQL-standard JSON path expressions, since it will either fail or return
     <code class="literal">
      NULL
     </code>
     if the path result is not a single boolean value.) The optional
     <em class="parameter">
      <code>
       vars
      </code>
     </em>
     and
     <em class="parameter">
      <code>
       silent
      </code>
     </em>
     arguments act the same as for
     <code class="function">
      jsonb_path_exists
     </code>
     .
    </p>
    <p>
     <code class="literal">
      jsonb_path_match('{"a":[1,2,3,4,5]}', 'exists($.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max))', '{"min":2, "max":4}')
     </code>
     →
     <code class="returnvalue">
      t
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      jsonb_path_query
     </code>
     (
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     ,
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     <code class="type">
      jsonpath
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        vars
       </code>
      </em>
      <code class="type">
       jsonb
      </code>
      [
      <span class="optional">
       ,
       <em class="parameter">
        <code>
         silent
        </code>
       </em>
       <code class="type">
        boolean
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code class="returnvalue">
      setof jsonb
     </code>
    </p>
    <p>
     Returns all JSON items returned by the JSON path for the specified JSON value. For SQL-standard JSON path expressions it returns the JSON values selected from
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     . For
     <a class="link" href="functions-json.md#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS" title="9.16.2.1.1. Boolean Predicate Check Expressions">
      predicate check expressions
     </a>
     it returns the result of the predicate check:
     <code class="literal">
      true
     </code>
     ,
     <code class="literal">
      false
     </code>
     , or
     <code class="literal">
      null
     </code>
     . The optional
     <em class="parameter">
      <code>
       vars
      </code>
     </em>
     and
     <em class="parameter">
      <code>
       silent
      </code>
     </em>
     arguments act the same as for
     <code class="function">
      jsonb_path_exists
     </code>
     .
    </p>
    <p>
     <code class="literal">
      select * from jsonb_path_query('{"a":[1,2,3,4,5]}', '$.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max)', '{"min":2, "max":4}')
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
 jsonb_path_query ------------------ 2 3 4
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      jsonb_path_query_array
     </code>
     (
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     ,
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     <code class="type">
      jsonpath
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        vars
       </code>
      </em>
      <code class="type">
       jsonb
      </code>
      [
      <span class="optional">
       ,
       <em class="parameter">
        <code>
         silent
        </code>
       </em>
       <code class="type">
        boolean
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Returns all JSON items returned by the JSON path for the specified JSON value, as a JSON array. The parameters are the same as for
     <code class="function">
      jsonb_path_query
     </code>
     .
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('{"a":[1,2,3,4,5]}', '$.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max)', '{"min":2, "max":4}')
     </code>
     →
     <code class="returnvalue">
      [2, 3, 4]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      jsonb_path_query_first
     </code>
     (
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     ,
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     <code class="type">
      jsonpath
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        vars
       </code>
      </em>
      <code class="type">
       jsonb
      </code>
      [
      <span class="optional">
       ,
       <em class="parameter">
        <code>
         silent
        </code>
       </em>
       <code class="type">
        boolean
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     Returns the first JSON item returned by the JSON path for the specified JSON value, or
     <code class="literal">
      NULL
     </code>
     if there are no results. The parameters are the same as for
     <code class="function">
      jsonb_path_query
     </code>
     .
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_first('{"a":[1,2,3,4,5]}', '$.a[*] ? (@ &gt;= $min &amp;&amp; @ &lt;= $max)', '{"min":2, "max":4}')
     </code>
     →
     <code class="returnvalue">
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      jsonb_path_exists_tz
     </code>
     (
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     ,
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     <code class="type">
      jsonpath
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        vars
       </code>
      </em>
      <code class="type">
       jsonb
      </code>
      [
      <span class="optional">
       ,
       <em class="parameter">
        <code>
         silent
        </code>
       </em>
       <code class="type">
        boolean
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_path_match_tz
     </code>
     (
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     ,
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     <code class="type">
      jsonpath
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        vars
       </code>
      </em>
      <code class="type">
       jsonb
      </code>
      [
      <span class="optional">
       ,
       <em class="parameter">
        <code>
         silent
        </code>
       </em>
       <code class="type">
        boolean
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_path_query_tz
     </code>
     (
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     ,
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     <code class="type">
      jsonpath
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        vars
       </code>
      </em>
      <code class="type">
       jsonb
      </code>
      [
      <span class="optional">
       ,
       <em class="parameter">
        <code>
         silent
        </code>
       </em>
       <code class="type">
        boolean
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code class="returnvalue">
      setof jsonb
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_path_query_array_tz
     </code>
     (
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     ,
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     <code class="type">
      jsonpath
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        vars
       </code>
      </em>
      <code class="type">
       jsonb
      </code>
      [
      <span class="optional">
       ,
       <em class="parameter">
        <code>
         silent
        </code>
       </em>
       <code class="type">
        boolean
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_path_query_first_tz
     </code>
     (
     <em class="parameter">
      <code>
       target
      </code>
     </em>
     <code class="type">
      jsonb
     </code>
     ,
     <em class="parameter">
      <code>
       path
      </code>
     </em>
     <code class="type">
      jsonpath
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        vars
       </code>
      </em>
      <code class="type">
       jsonb
      </code>
      [
      <span class="optional">
       ,
       <em class="parameter">
        <code>
         silent
        </code>
       </em>
       <code class="type">
        boolean
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code class="returnvalue">
      jsonb
     </code>
    </p>
    <p>
     These functions act like their counterparts described above without the
     <code class="literal">
      _tz
     </code>
     suffix, except that these functions support comparisons of date/time values that require timezone-aware conversions.  The example below requires interpretation of the date-only value
     <code class="literal">
      2015-08-02
     </code>
     as a timestamp with time zone, so the result depends on the current
     <a class="xref" href="runtime-config-client.md#GUC-TIMEZONE">
      TimeZone
     </a>
     setting.  Due to this dependency, these functions are marked as stable, which means these functions cannot be used in indexes.  Their counterparts are immutable, and so can be used in indexes; but they will throw errors if asked to make such comparisons.
    </p>
    <p>
     <code class="literal">
      jsonb_path_exists_tz('["2015-08-01 12:00:00-05"]', '$[*] ? (@.datetime() &lt; "2015-08-02".datetime())')
     </code>
     →
     <code class="returnvalue">
      t
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      jsonb_pretty
     </code>
     (
     <code class="type">
      jsonb
     </code>
     ) →
     <code class="returnvalue">
      text
     </code>
    </p>
    <p>
     Converts the given JSON value to pretty-printed, indented text.
    </p>
    <p>
     <code class="literal">
      jsonb_pretty('[{"f1":1,"f2":null}, 2]')
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
[ { "f1": 1, "f2": null }, 2 ]
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      json_typeof
     </code>
     (
     <code class="type">
      json
     </code>
     ) →
     <code class="returnvalue">
      text
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      jsonb_typeof
     </code>
     (
     <code class="type">
      jsonb
     </code>
     ) →
     <code class="returnvalue">
      text
     </code>
    </p>
    <p>
     Returns the type of the top-level JSON value as a text string. Possible types are
     <code class="literal">
      object
     </code>
     ,
     <code class="literal">
      array
     </code>
     ,
     <code class="literal">
      string
     </code>
     ,
     <code class="literal">
      number
     </code>
     ,
     <code class="literal">
      boolean
     </code>
     , and
     <code class="literal">
      null
     </code>
     .

        (The
     <code class="literal">
      null
     </code>
     result should not be confused with an SQL NULL; see the examples.)
    </p>
    <p>
     <code class="literal">
      json_typeof('-123.4')
     </code>
     →
     <code class="returnvalue">
      number
     </code>
    </p>
    <p>
     <code class="literal">
      json_typeof('null'::json)
     </code>
     →
     <code class="returnvalue">
      null
     </code>
    </p>
    <p>
     <code class="literal">
      json_typeof(NULL::json) IS NULL
     </code>
     →
     <code class="returnvalue">
      t
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>






### 9.16.2. A linguagem de caminho SQL/JSON [#](#FUNCTIONS-SQLJSON-PATH)

As expressões de caminho SQL/JSON especificam os itens a serem recuperados de um valor JSON, de forma semelhante às expressões XPath usadas para acesso a conteúdo XML. No PostgreSQL, as expressões de caminho são implementadas como o tipo de dados `jsonpath` e podem usar quaisquer elementos descritos em [Seção 8.14.7](datatype-json.md#DATATYPE-JSONPATH).

As funções e operadores de consulta JSON passam a expressão de caminho fornecida ao *motor de caminho* para avaliação. Se a expressão corresponder aos dados JSON solicitados, o item JSON correspondente ou o conjunto de itens é retornado. Se não houver correspondência, o resultado será `NULL`, `false` ou um erro, dependendo da função. As expressões de caminho são escritas na linguagem de caminho SQL/JSON e podem incluir expressões aritméticas e funções.

Uma expressão de caminho consiste em uma sequência de elementos permitidos pelo tipo de dados `jsonpath`. A expressão de caminho é normalmente avaliada de esquerda para direita, mas você pode usar parênteses para alterar a ordem das operações. Se a avaliação for bem-sucedida, uma sequência de itens JSON é produzida, e o resultado da avaliação é devolvido à função de consulta JSON que completa o cálculo especificado.

Para se referir ao valor JSON que está sendo consultado (o item *context*), use a variável `$` na expressão do caminho. O primeiro elemento de um caminho deve ser sempre `$`. Pode ser seguido por um ou mais [operadores de acesso](datatype-json.md#TYPE-JSONPATH-ACCESSORS "Table 8.25. jsonpath Accessors"), que descem o nível da estrutura JSON nível por nível para recuperar subitens do item de contexto. Cada operador de acesso atua nos resultados da etapa de avaliação anterior, produzindo zero, um ou mais itens de saída de cada item de entrada.

Por exemplo, suponha que você tenha alguns dados JSON de um rastreador de GPS que você gostaria de analisar, como:

```
SELECT '{
  "track": {
    "segments": [
      {
        "location":   [ 47.763, 13.4034 ],
        "start time": "2018-10-14 10:05:14",
        "HR": 73
      },
      {
        "location":   [ 47.706, 13.2635 ],
        "start time": "2018-10-14 10:39:21",
        "HR": 135
      }
    ]
  }
}' AS json \gset
```

(O exemplo acima pode ser copiado e colado no psql para configurar as coisas para os exemplos seguintes. Em seguida, o psql expandirá `:'json'` em uma constante de string com citação adequada que contenha o valor JSON.)

Para recuperar os segmentos de trilha disponíveis, você precisa usar o operador de acesso `.key` para descer através dos objetos JSON circundantes, por exemplo:

```
=> select jsonb_path_query(:'json', '$.track.segments');
                                                                         jsonb_path_query
-----------------------------------------------------------​-----------------------------------------------------------​---------------------------------------------
 [{"HR": 73, "location": [47.763, 13.4034], "start time": "2018-10-14 10:05:14"}, {"HR": 135, "location": [47.706, 13.2635], "start time": "2018-10-14 10:39:21"}]
```

Para recuperar o conteúdo de um array, você normalmente usa o operador `[*]`. O exemplo a seguir retornará as coordenadas de localização para todos os segmentos de faixa disponíveis:

```
=> select jsonb_path_query(:'json', '$.track.segments[*].location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
```

Aqui, começamos com o valor inteiro do entrada JSON (`$`), então o `.track` acessador selecionou o objeto JSON associado à chave do objeto `"track"`, então o `.segments` acessador selecionou o array JSON associado à chave `"segments"` dentro desse objeto, então o `[*]` acessador selecionou cada elemento desse array (produzindo uma série de itens), então o `.location` acessador selecionou o array JSON associado à chave `"location"` dentro de cada um desses objetos. Neste exemplo, cada um desses objetos tinha uma chave `"location"`; mas se algum deles não tivesse, o `.location` acessador simplesmente não teria produzido saída para esse item de entrada.

Para retornar apenas as coordenadas do primeiro segmento, você pode especificar o índice correspondente no operador de acesso `[]`. Lembre-se de que os índices de matriz JSON são relativos ao 0:

```
=> select jsonb_path_query(:'json', '$.track.segments[0].location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
```

O resultado de cada etapa de avaliação de caminho pode ser processado por um ou mais dos operadores e métodos `jsonpath` listados em [Seção 9.16.2.3](functions-json.md#FUNCTIONS-SQLJSON-PATH-OPERATORS). Cada nome de método deve ser precedido por um ponto. Por exemplo, você pode obter o tamanho de um array:

```
=> select jsonb_path_query(:'json', '$.track.segments.size()');
 jsonb_path_query
------------------
 2
```

Mais exemplos de uso dos operadores e métodos `jsonpath` em expressões de caminho aparecem abaixo em [Seção 9.16.2.3](functions-json.md#FUNCTIONS-SQLJSON-PATH-OPERATORS).

Um caminho também pode conter expressões de filtro que funcionam de maneira semelhante à cláusula `WHERE` em SQL. Uma expressão de filtro começa com um ponto de interrogação e fornece uma condição entre parênteses:

```
? (condition)
```

As expressões de filtro devem ser escritas logo após a etapa de avaliação de caminho para a qual elas devem se aplicar. O resultado dessa etapa é filtrado para incluir apenas os itens que satisfazem a condição fornecida. O SQL/JSON define lógica de três valores, então a condição pode produzir `true`, `false` ou `unknown`. O valor `unknown` desempenha o mesmo papel que o SQL `NULL` e pode ser testado com o predicado `is unknown`. Outros passos de avaliação de caminho usam apenas os itens para os quais a expressão de filtro retornou `true`.

As funções e operadores que podem ser usados em expressões de filtro estão listados em [Tabela 9.53](functions-json.md#FUNCTIONS-SQLJSON-FILTER-EX-TABLE). Dentro de uma expressão de filtro, a variável `@` denota o valor que está sendo considerado (ou seja, um resultado da etapa anterior do caminho). Você pode escrever operadores de acesso após `@` para recuperar itens de componentes.

Por exemplo, suponha que você queira recuperar todos os valores de frequência cardíaca superiores a 130. Você pode fazer isso da seguinte forma:

```
=> select jsonb_path_query(:'json', '$.track.segments[*].HR ? (@ > 130)');
 jsonb_path_query
------------------
 135
```

Para obter os horários de início dos segmentos com esses valores, você precisa filtrar os segmentos irrelevantes antes de selecionar os horários de início, para que a expressão de filtro seja aplicada à etapa anterior e o caminho usado na condição seja diferente:

```
=> select jsonb_path_query(:'json', '$.track.segments[*] ? (@.HR > 130)."start time"');
   jsonb_path_query
-----------------------
 "2018-10-14 10:39:21"
```

Você pode usar várias expressões de filtro em sequência, se necessário. O exemplo a seguir seleciona as horas de início de todos os segmentos que contêm locais com coordenadas relevantes e valores de frequência cardíaca elevados:

```
=> select jsonb_path_query(:'json', '$.track.segments[*] ? (@.location[1] < 13.4) ? (@.HR > 130)."start time"');
   jsonb_path_query
-----------------------
 "2018-10-14 10:39:21"
```

Também é permitido usar expressões de filtro em diferentes níveis de encadernação. O exemplo a seguir filtra primeiro todos os segmentos por localização e, em seguida, retorna valores de frequência cardíaca alta para esses segmentos, se disponíveis:

```
=> select jsonb_path_query(:'json', '$.track.segments[*] ? (@.location[1] < 13.4).HR ? (@ > 130)');
 jsonb_path_query
------------------
 135
```

Você também pode aninhar expressões de filtro uma dentro da outra. Esse exemplo retorna o tamanho da faixa se ela contiver quaisquer segmentos com valores de frequência cardíaca alta, ou uma sequência vazia, caso contrário:

```
=> select jsonb_path_query(:'json', '$.track ? (exists(@.segments[*] ? (@.HR > 130))).segments.size()');
 jsonb_path_query
------------------
 2
```

#### 9.16.2.1. Desvios do Padrão SQL [#](#FUNCTIONS-SQLJSON-DEVIATIONS)

A implementação do PostgreSQL do idioma de caminho SQL/JSON tem as seguintes divergências em relação ao padrão SQL/JSON.

##### 9.16.2.1.1. Expressões de verificação de predicado booleano [#](#FUNCTIONS-SQLJSON-CHECK-EXPRESSIONS)

Como uma extensão do padrão SQL, uma expressão de caminho do PostgreSQL pode ser um predicado booleano, enquanto o padrão SQL permite predicados apenas dentro de filtros. Enquanto as expressões de caminho padrão SQL retornam o(s) elemento(s) relevante(s) do valor JSON pesquisado, as expressões de verificação de predicado retornam o único resultado de três valores `jsonb` do predicado: `true`, `false` ou `null`. Por exemplo, poderíamos escrever esta expressão de filtro padrão SQL:

```
=> select jsonb_path_query(:'json', '$.track.segments ?(@[*].HR > 130)');
                                jsonb_path_query
-----------------------------------------------------------​----------------------
 {"HR": 135, "location": [47.706, 13.2635], "start time": "2018-10-14 10:39:21"}
```

A expressão de verificação de predicado semelhante simplesmente retorna `true`, indicando que existe uma correspondência:

```
=> select jsonb_path_query(:'json', '$.track.segments[*].HR > 130');
 jsonb_path_query
------------------
 true
```

### Nota

As expressões de verificação de predicado são necessárias no operador `@@` (e na função `jsonb_path_match`), e não devem ser usadas com o operador `@?` (ou na função `jsonb_path_exists`).

##### 9.16.2.1.2. Interpretação de Expressão Regular [#](#FUNCTIONS-SQLJSON-REGULAR-EXPRESSION-DEVIATION)

Há pequenas diferenças na interpretação dos padrões de expressão regular utilizados nos filtros de `like_regex`, conforme descrito em [Seção 9.16.2.4](functions-json.md#JSONPATH-REGULAR-EXPRESSIONS).

#### 9.16.2.2. Modos estrito e laxo [#](#FUNCTIONS-SQLJSON-STRICT-AND-LAX-MODES)

Quando você consulta dados JSON, a expressão do caminho pode não corresponder à estrutura real dos dados JSON. Uma tentativa de acessar um membro não existente de um objeto ou elemento de um array é definida como um erro estrutural. As expressões de caminho SQL/JSON têm dois modos de tratamento de erros estruturais:

* lax (padrão) — o motor de caminho adapta implicitamente os dados solicitados ao caminho especificado. Quaisquer erros estruturais que não possam ser corrigidos conforme descrito abaixo são suprimidos, não produzindo correspondência.
* strict — se ocorrer um erro estrutural, um erro é gerado.

O modo lax facilita a correspondência de um documento JSON e expressão de caminho quando os dados JSON não correspondem ao esquema esperado. Se um operando não corresponder aos requisitos de uma operação específica, ele pode ser automaticamente envolto como um array SQL/JSON ou desenvolvido convertendo seus elementos em uma sequência SQL/JSON antes de realizar a operação. Além disso, os operadores de comparação desenvolvem automaticamente seus operandos no modo lax, para que você possa comparar arrays SQL/JSON diretamente. Um array de tamanho 1 é considerado igual ao seu único elemento. O desenvolvimento automático não é realizado quando:

* A expressão de caminho contém os métodos `type()` ou `size()` que retornam o tipo e o número de elementos na matriz, respectivamente.
* Os dados JSON solicitados contêm arrays aninhados. Neste caso, apenas o array mais externo é desencapsulado, enquanto todos os arrays internos permanecem inalterados. Assim, o desencapsulamento implícito só pode ir uma etapa abaixo dentro de cada etapa de avaliação de caminho.

Por exemplo, ao consultar os dados do GPS listados acima, você pode abstrair do fato de que eles armazenam um array de segmentos ao usar o modo lax:

```
=> select jsonb_path_query(:'json', 'lax $.track.segments.location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
```

No modo estrito, o caminho especificado deve corresponder exatamente à estrutura do documento JSON pesquisado, portanto, o uso dessa expressão de caminho causará um erro:

```
=> select jsonb_path_query(:'json', 'strict $.track.segments.location');
ERROR:  jsonpath member accessor can only be applied to an object
```

Para obter o mesmo resultado que no modo lax, você precisa desvendar explicitamente o array `segments`:

```
=> select jsonb_path_query(:'json', 'strict $.track.segments[*].location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
```

O comportamento de desenrolar do modo lax pode levar a resultados surpreendentes. Por exemplo, a seguinte consulta que utiliza o acessador `.**` seleciona cada valor `HR` duas vezes:

```
=> select jsonb_path_query(:'json', 'lax $.**.HR');
 jsonb_path_query
------------------
 73
 135
 73
 135
```

Isso acontece porque o acessador `.**` seleciona tanto o array `segments` quanto cada um de seus elementos, enquanto o acessador `.HR` desenrola automaticamente arrays ao usar o modo lax. Para evitar resultados surpreendentes, recomendamos usar o acessador `.**` apenas no modo estrito. A consulta a seguir seleciona cada valor `HR` apenas uma vez:

```
=> select jsonb_path_query(:'json', 'strict $.**.HR');
 jsonb_path_query
------------------
 73
 135
```

A desdobra de arrays também pode levar a resultados inesperados. Considere este exemplo, que seleciona todos os arrays `location`:

```
=> select jsonb_path_query(:'json', 'lax $.track.segments[*].location');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
(2 rows)
```

Como esperado, ele retorna os arrays completos. Mas ao aplicar uma expressão de filtro, os arrays são desenroláveis para avaliar cada item, retornando apenas os itens que correspondem à expressão:

```
=> select jsonb_path_query(:'json', 'lax $.track.segments[*].location ?(@[*] > 15)');
 jsonb_path_query
------------------
 47.763
 47.706
(2 rows)
```

Isso, apesar do fato de que os arrays completos são selecionados pela expressão de caminho. Use o modo estrito para restaurar a seleção dos arrays:

```
=> select jsonb_path_query(:'json', 'strict $.track.segments[*].location ?(@[*] > 15)');
 jsonb_path_query
-------------------
 [47.763, 13.4034]
 [47.706, 13.2635]
(2 rows)
```

#### 9.16.2.3. Operadores e métodos de caminho SQL/JSON [#](#FUNCTIONS-SQLJSON-PATH-OPERATORS)

[Tabela 9.52](functions-json.md#FUNCTIONS-SQLJSON-OP-TABLE) mostra os operadores e métodos disponíveis em `jsonpath`. Observe que, embora os operadores e métodos unários possam ser aplicados a múltiplos valores resultantes de uma etapa anterior do caminho, os operadores binários (adição, etc.) só podem ser aplicados a valores únicos. No modo laxo, os métodos aplicados a uma matriz serão executados para cada valor na matriz. As exceções são `.type()` e `.size()`, que se aplicam à própria matriz.

**Tabela 9.52. Operadores e Métodos `jsonpath`**



<table border="1" class="table" summary="jsonpath Operators and Methods">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Operator/Method
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
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code class="literal">
      +
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        number
       </code>
      </em>
     </code>
    </p>
    <p>
     Addition
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('[2]', '$[0] + 3')
     </code>
     →
     <code class="returnvalue">
      5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="literal">
      +
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        number
       </code>
      </em>
     </code>
    </p>
    <p>
     Unary plus (no operation); unlike addition, this can iterate over multiple values
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('{"x": [2,3,4]}', '+ $.x')
     </code>
     →
     <code class="returnvalue">
      [2, 3, 4]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code class="literal">
      -
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        number
       </code>
      </em>
     </code>
    </p>
    <p>
     Subtraction
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('[2]', '7 - $[0]')
     </code>
     →
     <code class="returnvalue">
      5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="literal">
      -
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        number
       </code>
      </em>
     </code>
    </p>
    <p>
     Negation; unlike subtraction, this can iterate over multiple values
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('{"x": [2,3,4]}', '- $.x')
     </code>
     →
     <code class="returnvalue">
      [-2, -3, -4]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code class="literal">
      *
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        number
       </code>
      </em>
     </code>
    </p>
    <p>
     Multiplication
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('[4]', '2 * $[0]')
     </code>
     →
     <code class="returnvalue">
      8
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code class="literal">
      /
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        number
       </code>
      </em>
     </code>
    </p>
    <p>
     Division
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('[8.5]', '$[0] / 2')
     </code>
     →
     <code class="returnvalue">
      4.2500000000000000
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code class="literal">
      %
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        number
       </code>
      </em>
     </code>
    </p>
    <p>
     Modulo (remainder)
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('[32]', '$[0] % 10')
     </code>
     →
     <code class="returnvalue">
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      type()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        string
       </code>
      </em>
     </code>
    </p>
    <p>
     Type of the JSON item (see
     <code class="function">
      json_typeof
     </code>
     )
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('[1, "2", {}]', '$[*].type()')
     </code>
     →
     <code class="returnvalue">
      ["number", "string", "object"]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      size()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        number
       </code>
      </em>
     </code>
    </p>
    <p>
     Size of the JSON item (number of array elements, or 1 if not an array)
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('{"m": [11, 15]}', '$.m.size()')
     </code>
     →
     <code class="returnvalue">
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      boolean()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        boolean
       </code>
      </em>
     </code>
    </p>
    <p>
     Boolean value converted from a JSON boolean, number, or string
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('[1, "yes", false]', '$[*].boolean()')
     </code>
     →
     <code class="returnvalue">
      [true, true, false]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      string()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        string
       </code>
      </em>
     </code>
    </p>
    <p>
     String value converted from a JSON boolean, number, string, or datetime
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('[1.23, "xyz", false]', '$[*].string()')
     </code>
     →
     <code class="returnvalue">
      ["1.23", "xyz", "false"]
     </code>
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('"2023-08-15 12:34:56"', '$.timestamp().string()')
     </code>
     →
     <code class="returnvalue">
      "2023-08-15T12:34:56"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      double()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        number
       </code>
      </em>
     </code>
    </p>
    <p>
     Approximate floating-point number converted from a JSON number or string
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('{"len": "1.9"}', '$.len.double() * 2')
     </code>
     →
     <code class="returnvalue">
      3.8
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      ceiling()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        number
       </code>
      </em>
     </code>
    </p>
    <p>
     Nearest integer greater than or equal to the given number
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('{"h": 1.3}', '$.h.ceiling()')
     </code>
     →
     <code class="returnvalue">
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      floor()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        number
       </code>
      </em>
     </code>
    </p>
    <p>
     Nearest integer less than or equal to the given number
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('{"h": 1.7}', '$.h.floor()')
     </code>
     →
     <code class="returnvalue">
      1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      abs()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        number
       </code>
      </em>
     </code>
    </p>
    <p>
     Absolute value of the given number
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('{"z": -0.3}', '$.z.abs()')
     </code>
     →
     <code class="returnvalue">
      0.3
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      bigint()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        bigint
       </code>
      </em>
     </code>
    </p>
    <p>
     Big integer value converted from a JSON number or string
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('{"len": "9876543219"}', '$.len.bigint()')
     </code>
     →
     <code class="returnvalue">
      9876543219
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      decimal( [
      <em class="replaceable">
       <code>
        precision
       </code>
      </em>
      [ ,
      <em class="replaceable">
       <code>
        scale
       </code>
      </em>
      ] ] )
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        decimal
       </code>
      </em>
     </code>
    </p>
    <p>
     Rounded decimal value converted from a JSON number or string (
     <code class="literal">
      precision
     </code>
     and
     <code class="literal">
      scale
     </code>
     must be integer values)
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('1234.5678', '$.decimal(6, 2)')
     </code>
     →
     <code class="returnvalue">
      1234.57
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      integer()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        integer
       </code>
      </em>
     </code>
    </p>
    <p>
     Integer value converted from a JSON number or string
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('{"len": "12345"}', '$.len.integer()')
     </code>
     →
     <code class="returnvalue">
      12345
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      number()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        numeric
       </code>
      </em>
     </code>
    </p>
    <p>
     Numeric value converted from a JSON number or string
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('{"len": "123.45"}', '$.len.number()')
     </code>
     →
     <code class="returnvalue">
      123.45
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      datetime()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        datetime_type
       </code>
      </em>
     </code>
     (see note)
    </p>
    <p>
     Date/time value converted from a string
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('["2015-8-1", "2015-08-12"]', '$[*] ? (@.datetime() &lt; "2015-08-2".datetime())')
     </code>
     →
     <code class="returnvalue">
      "2015-8-1"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      datetime(
      <em class="replaceable">
       <code>
        template
       </code>
      </em>
      )
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        datetime_type
       </code>
      </em>
     </code>
     (see note)
    </p>
    <p>
     Date/time value converted from a string using the specified
     <code class="function">
      to_timestamp
     </code>
     template
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('["12:30", "18:40"]', '$[*].datetime("HH24:MI")')
     </code>
     →
     <code class="returnvalue">
      ["12:30:00", "18:40:00"]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      date()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        date
       </code>
      </em>
     </code>
    </p>
    <p>
     Date value converted from a string
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('"2023-08-15"', '$.date()')
     </code>
     →
     <code class="returnvalue">
      "2023-08-15"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      time()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        time without time zone
       </code>
      </em>
     </code>
    </p>
    <p>
     Time without time zone value converted from a string
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('"12:34:56"', '$.time()')
     </code>
     →
     <code class="returnvalue">
      "12:34:56"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      time(
      <em class="replaceable">
       <code>
        precision
       </code>
      </em>
      )
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        time without time zone
       </code>
      </em>
     </code>
    </p>
    <p>
     Time without time zone value converted from a string, with fractional seconds adjusted to the given precision
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('"12:34:56.789"', '$.time(2)')
     </code>
     →
     <code class="returnvalue">
      "12:34:56.79"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      time_tz()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        time with time zone
       </code>
      </em>
     </code>
    </p>
    <p>
     Time with time zone value converted from a string
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('"12:34:56 +05:30"', '$.time_tz()')
     </code>
     →
     <code class="returnvalue">
      "12:34:56+05:30"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      time_tz(
      <em class="replaceable">
       <code>
        precision
       </code>
      </em>
      )
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        time with time zone
       </code>
      </em>
     </code>
    </p>
    <p>
     Time with time zone value converted from a string, with fractional seconds adjusted to the given precision
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('"12:34:56.789 +05:30"', '$.time_tz(2)')
     </code>
     →
     <code class="returnvalue">
      "12:34:56.79+05:30"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      timestamp()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        timestamp without time zone
       </code>
      </em>
     </code>
    </p>
    <p>
     Timestamp without time zone value converted from a string
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('"2023-08-15 12:34:56"', '$.timestamp()')
     </code>
     →
     <code class="returnvalue">
      "2023-08-15T12:34:56"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      timestamp(
      <em class="replaceable">
       <code>
        precision
       </code>
      </em>
      )
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        timestamp without time zone
       </code>
      </em>
     </code>
    </p>
    <p>
     Timestamp without time zone value converted from a string, with fractional seconds adjusted to the given precision
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('"2023-08-15 12:34:56.789"', '$.timestamp(2)')
     </code>
     →
     <code class="returnvalue">
      "2023-08-15T12:34:56.79"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      timestamp_tz()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        timestamp with time zone
       </code>
      </em>
     </code>
    </p>
    <p>
     Timestamp with time zone value converted from a string
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('"2023-08-15 12:34:56 +05:30"', '$.timestamp_tz()')
     </code>
     →
     <code class="returnvalue">
      "2023-08-15T12:34:56+05:30"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      timestamp_tz(
      <em class="replaceable">
       <code>
        precision
       </code>
      </em>
      )
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        timestamp with time zone
       </code>
      </em>
     </code>
    </p>
    <p>
     Timestamp with time zone value converted from a string, with fractional seconds adjusted to the given precision
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('"2023-08-15 12:34:56.789 +05:30"', '$.timestamp_tz(2)')
     </code>
     →
     <code class="returnvalue">
      "2023-08-15T12:34:56.79+05:30"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       object
      </code>
     </em>
     <code class="literal">
      .
     </code>
     <code class="literal">
      keyvalue()
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        array
       </code>
      </em>
     </code>
    </p>
    <p>
     The object's key-value pairs, represented as an array of objects containing three fields:
     <code class="literal">
      "key"
     </code>
     ,
     <code class="literal">
      "value"
     </code>
     , and
     <code class="literal">
      "id"
     </code>
     ;
     <code class="literal">
      "id"
     </code>
     is a unique identifier of the object the key-value pair belongs to
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('{"x": "20", "y": 32}', '$.keyvalue()')
     </code>
     →
     <code class="returnvalue">
      [{"id": 0, "key": "x", "value": "20"}, {"id": 0, "key": "y", "value": 32}]
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>









### Nota

O tipo de resultado dos métodos `datetime()` e `datetime(template)` pode ser `date`, `timetz`, `time`, `timestamptz` ou `timestamp`. Ambos os métodos determinam seu tipo de resultado dinamicamente.

O método `datetime()` tenta sequencialmente alinhar sua string de entrada aos formatos ISO para `date`, `timetz`, `time`, `timestamptz` e `timestamp`. Ele para no primeiro formato correspondente e emite o tipo de dado correspondente.

O método `datetime(template)` determina o tipo de resultado de acordo com os campos utilizados na string de modelo fornecida.

Os métodos `datetime()` e `datetime(template)` utilizam as mesmas regras de análise que a função SQL `to_timestamp` (ver [Seção 9.8](functions-formatting.md)), com três exceções. Primeiro, esses métodos não permitem padrões de modelo não correspondidos. Segundo, apenas os seguintes separadores são permitidos na string de modelo: sinal de menos, ponto, traço (barra), vírgula, apóstrofo, ponto e vírgula, colon e espaço. Terceiro, os separadores na string de modelo devem corresponder exatamente à string de entrada.

Se diferentes tipos de data/hora precisam ser comparados, uma conversão implícita é aplicada. Um valor `date` pode ser convertido para `timestamp` ou `timestamptz`, `timestamp` pode ser convertido para `timestamptz`, e `time` para `timetz`. No entanto, todas, exceto a primeira, dessas conversões dependem do ajuste atual da [TimeZone](runtime-config-client.md#GUC-TIMEZONE), e, portanto, só podem ser realizadas dentro de funções `jsonpath` que são conscientes do fuso horário. Da mesma forma, outros métodos relacionados a data/hora que convertem strings para tipos de data/hora também realizam essa conversão, o que pode envolver o ajuste atual da [TimeZone](runtime-config-client.md#GUC-TIMEZONE). Portanto, essas conversões também só podem ser realizadas dentro de funções `jsonpath` que são conscientes do fuso horário.

[Tabela 9.53](functions-json.md#FUNCTIONS-SQLJSON-FILTER-EX-TABLE) mostra os elementos de expressão de filtro disponíveis.

**Tabela 9.53. Elementos de expressão de filtro `jsonpath`**



<table border="1" class="table" summary="jsonpath Filter Expression Elements">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Predicate/Value
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
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     <code class="literal">
      ==
     </code>
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Equality comparison (this, and the other comparison operators, work on all JSON scalar values)
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('[1, "a", 1, 3]', '$[*] ? (@ == 1)')
     </code>
     →
     <code class="returnvalue">
      [1, 1]
     </code>
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('[1, "a", 1, 3]', '$[*] ? (@ == "a")')
     </code>
     →
     <code class="returnvalue">
      ["a"]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     <code class="literal">
      !=
     </code>
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p class="func_signature">
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     <code class="literal">
      &lt;&gt;
     </code>
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Non-equality comparison
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('[1, 2, 1, 3]', '$[*] ? (@ != 1)')
     </code>
     →
     <code class="returnvalue">
      [2, 3]
     </code>
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('["a", "b", "c"]', '$[*] ? (@ &lt;&gt; "b")')
     </code>
     →
     <code class="returnvalue">
      ["a", "c"]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     <code class="literal">
      &lt;
     </code>
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Less-than comparison
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('[1, 2, 3]', '$[*] ? (@ &lt; 2)')
     </code>
     →
     <code class="returnvalue">
      [1]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     <code class="literal">
      &lt;=
     </code>
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Less-than-or-equal-to comparison
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('["a", "b", "c"]', '$[*] ? (@ &lt;= "b")')
     </code>
     →
     <code class="returnvalue">
      ["a", "b"]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     <code class="literal">
      &gt;
     </code>
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Greater-than comparison
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('[1, 2, 3]', '$[*] ? (@ &gt; 2)')
     </code>
     →
     <code class="returnvalue">
      [3]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     <code class="literal">
      &gt;=
     </code>
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Greater-than-or-equal-to comparison
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('[1, 2, 3]', '$[*] ? (@ &gt;= 2)')
     </code>
     →
     <code class="returnvalue">
      [2, 3]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="literal">
      true
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     JSON constant
     <code class="literal">
      true
     </code>
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('[{"name": "John", "parent": false}, {"name": "Chris", "parent": true}]', '$[*] ? (@.parent == true)')
     </code>
     →
     <code class="returnvalue">
      {"name": "Chris", "parent": true}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="literal">
      false
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     JSON constant
     <code class="literal">
      false
     </code>
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('[{"name": "John", "parent": false}, {"name": "Chris", "parent": true}]', '$[*] ? (@.parent == false)')
     </code>
     →
     <code class="returnvalue">
      {"name": "John", "parent": false}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="literal">
      null
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        value
       </code>
      </em>
     </code>
    </p>
    <p>
     JSON constant
     <code class="literal">
      null
     </code>
     (note that, unlike in SQL, comparison to
     <code class="literal">
      null
     </code>
     works normally)
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('[{"name": "Mary", "job": null}, {"name": "Michael", "job": "driver"}]', '$[*] ? (@.job == null) .name')
     </code>
     →
     <code class="returnvalue">
      "Mary"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       boolean
      </code>
     </em>
     <code class="literal">
      &amp;&amp;
     </code>
     <em class="replaceable">
      <code>
       boolean
      </code>
     </em>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Boolean AND
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('[1, 3, 7]', '$[*] ? (@ &gt; 1 &amp;&amp; @ &lt; 5)')
     </code>
     →
     <code class="returnvalue">
      3
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       boolean
      </code>
     </em>
     <code class="literal">
      ||
     </code>
     <em class="replaceable">
      <code>
       boolean
      </code>
     </em>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Boolean OR
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('[1, 3, 7]', '$[*] ? (@ &lt; 1 || @ &gt; 5)')
     </code>
     →
     <code class="returnvalue">
      7
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="literal">
      !
     </code>
     <em class="replaceable">
      <code>
       boolean
      </code>
     </em>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Boolean NOT
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('[1, 3, 7]', '$[*] ? (!(@ &lt; 5))')
     </code>
     →
     <code class="returnvalue">
      7
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       boolean
      </code>
     </em>
     <code class="literal">
      is unknown
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Tests whether a Boolean condition is
     <code class="literal">
      unknown
     </code>
     .
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('[-1, 2, 7, "foo"]', '$[*] ? ((@ &gt; 0) is unknown)')
     </code>
     →
     <code class="returnvalue">
      "foo"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     <code class="literal">
      like_regex
     </code>
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     [
     <span class="optional">
      <code class="literal">
       flag
      </code>
      <em class="replaceable">
       <code>
        string
       </code>
      </em>
     </span>
     ] →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Tests whether the first operand matches the regular expression given by the second operand, optionally with modifications described by a string of
     <code class="literal">
      flag
     </code>
     characters (see
     <a class="xref" href="functions-json.md#JSONPATH-REGULAR-EXPRESSIONS" title="9.16.2.4. SQL/JSON Regular Expressions">
      Section 9.16.2.4
     </a>
     ).
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('["abc", "abd", "aBdC", "abdacb", "babc"]', '$[*] ? (@ like_regex "^ab.*c")')
     </code>
     →
     <code class="returnvalue">
      ["abc", "abdacb"]
     </code>
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('["abc", "abd", "aBdC", "abdacb", "babc"]', '$[*] ? (@ like_regex "^ab.*c" flag "i")')
     </code>
     →
     <code class="returnvalue">
      ["abc", "aBdC", "abdacb"]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     <code class="literal">
      starts with
     </code>
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Tests whether the second operand is an initial substring of the first operand.
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('["John Smith", "Mary Stone", "Bob Johnson"]', '$[*] ? (@ starts with "John")')
     </code>
     →
     <code class="returnvalue">
      "John Smith"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="literal">
      exists
     </code>
     <code class="literal">
      (
     </code>
     <em class="replaceable">
      <code>
       path_expression
      </code>
     </em>
     <code class="literal">
      )
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Tests whether a path expression matches at least one SQL/JSON item. Returns
     <code class="literal">
      unknown
     </code>
     if the path expression would result in an error; the second example uses this to avoid a no-such-key error in strict mode.
    </p>
    <p>
     <code class="literal">
      jsonb_path_query('{"x": [1, 2], "y": [2, 4]}', 'strict $.* ? (exists (@ ? (@[*] &gt; 2)))')
     </code>
     →
     <code class="returnvalue">
      [2, 4]
     </code>
    </p>
    <p>
     <code class="literal">
      jsonb_path_query_array('{"value": 41}', 'strict $ ? (exists (@.name)) .name')
     </code>
     →
     <code class="returnvalue">
      []
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>






#### 9.16.2.4. Expressões regulares SQL/JSON [#](#JSONPATH-REGULAR-EXPRESSIONS)

As expressões de caminho SQL/JSON permitem que o texto seja correspondido a uma expressão regular com o filtro `like_regex`. Por exemplo, a seguinte consulta de caminho SQL/JSON corresponderia, de forma sensível ao caso, a todas as cadeias em um array que comecem com uma vogal em inglês:

```
$[*] ? (@ like_regex "^[aeiou]" flag "i")
```

A string opcional `flag` pode incluir um ou mais dos caracteres `i` para correspondência sensível ao caso, `m` para permitir que `^` e `$` correspondam a novas linhas, `s` para permitir que `.` corresponda a uma nova linha e `q` para cobrir todo o padrão (reduzindo o comportamento a uma simples correspondência de subcadeia).

O padrão SQL/JSON obtém sua definição para expressões regulares do operador `LIKE_REGEX`, que, por sua vez, utiliza o padrão XQuery. O PostgreSQL atualmente não suporta o operador `LIKE_REGEX`. Portanto, o filtro `like_regex` é implementado usando o motor de expressão regular POSIX descrito em [Seção 9.7.3](functions-matching.md#FUNCTIONS-POSIX-REGEXP). Isso leva a várias discrepâncias menores em relação ao comportamento padrão do SQL/JSON, que são catalogadas em [Seção 9.7.3.8](functions-matching.md#POSIX-VS-XQUERY). No entanto, observe que as incompatibilidades com a letra de sinalização descritas lá não se aplicam ao SQL/JSON, pois traduz as letras de sinalização do XQuery para corresponder ao que o motor POSIX espera.

Tenha em mente que o argumento padrão de `like_regex` é uma string literal de caminho JSON, escrita de acordo com as regras dadas na [Seção 8.14.7](datatype-json.md#DATATYPE-JSONPATH). Isso significa, em particular, que quaisquer barras invertidas que você deseja usar na expressão regular devem ser duplicadas. Por exemplo, para corresponder a valores de string do documento raiz que contenham apenas dígitos:

```
$.* ? (@ like_regex "^\\d+$")
```

### 9.16.3. Funções de consulta SQL/JSON [#](#SQLJSON-QUERY-FUNCTIONS)

As funções SQL/JSON `JSON_EXISTS()`, `JSON_QUERY()` e `JSON_VALUE()` descritas em [Tabela 9.54](functions-json.md#FUNCTIONS-SQLJSON-QUERYING) podem ser usadas para consultar documentos JSON. Cada uma dessas funções aplica um *`path_expression`* (uma consulta de caminho SQL/JSON) a um *`context_item`* (o documento). Veja [Seção 9.16.2](functions-json.md#FUNCTIONS-SQLJSON-PATH) para mais detalhes sobre o que o *`path_expression`* pode conter. O *`path_expression`* também pode referenciar variáveis, cujos valores são especificados com seus respectivos nomes na cláusula `PASSING` que é suportada por cada função. *`context_item`* pode ser um valor `jsonb` ou uma cadeia de caracteres que pode ser convertida com sucesso para `jsonb`.

**Tabela 9.54. Funções de consulta SQL/JSON**



<table border="1" class="table" summary="SQL/JSON Query Functions">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function signature
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
    </p>
    <pre class="synopsis">
<code class="function">JSON_EXISTS</code> (
<em class="replaceable"><code>context_item</code></em>, <em class="replaceable"><code>path_expression</code></em>
[<span class="optional"> <code class="literal">PASSING</code> { <em class="replaceable"><code>value</code></em> <code class="literal">AS</code> <em class="replaceable"><code>varname</code></em> } [<span class="optional">, ...</span>]</span>] [<span class="optional">{ <code class="literal">TRUE</code> | <code class="literal">FALSE</code> |<code class="literal"> UNKNOWN</code> | <code class="literal">ERROR</code> } <code class="literal">ON ERROR</code> </span>]) → <code class="returnvalue">boolean</code>
</pre>
    <p class="func_signature">
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        Returns true if the SQL/JSON
        <em class="replaceable">
         <code>
          path_expression
         </code>
        </em>
        applied to the
        <em class="replaceable">
         <code>
          context_item
         </code>
        </em>
        yields any items, false otherwise.
       </p>
      </li>
      <li class="listitem">
       <p>
        The
        <code class="literal">
         ON ERROR
        </code>
        clause specifies the behavior if an error occurs during
        <em class="replaceable">
         <code>
          path_expression
         </code>
        </em>
        evaluation.  Specifying
        <code class="literal">
         ERROR
        </code>
        will cause an error to be thrown with the appropriate message.  Other options include returning
        <code class="type">
         boolean
        </code>
        values
        <code class="literal">
         FALSE
        </code>
        or
        <code class="literal">
         TRUE
        </code>
        or the value
        <code class="literal">
         UNKNOWN
        </code>
        which is actually an SQL NULL. The default when no
        <code class="literal">
         ON ERROR
        </code>
        clause is specified is to return the
        <code class="type">
         boolean
        </code>
        value
        <code class="literal">
         FALSE
        </code>
        .
       </p>
      </li>
     </ul>
    </div>
    <p>
     Examples:
    </p>
    <p>
     <code class="literal">
      JSON_EXISTS(jsonb '{"key1": [1,2,3]}', 'strict $.key1[*] ? (@ &gt; $x)' PASSING 2 AS x)
     </code>
     →
     <code class="returnvalue">
      t
     </code>
    </p>
    <p>
     <code class="literal">
      JSON_EXISTS(jsonb '{"a": [1,2,3]}', 'lax $.a[5]' ERROR ON ERROR)
     </code>
     →
     <code class="returnvalue">
      f
     </code>
    </p>
    <p>
     <code class="literal">
      JSON_EXISTS(jsonb '{"a": [1,2,3]}', 'strict $.a[5]' ERROR ON ERROR)
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
ERROR:  jsonpath array subscript is out of bounds
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
    </p>
    <pre class="synopsis">
<code class="function">JSON_QUERY</code> (
<em class="replaceable"><code>context_item</code></em>, <em class="replaceable"><code>path_expression</code></em>
[<span class="optional"> <code class="literal">PASSING</code> { <em class="replaceable"><code>value</code></em> <code class="literal">AS</code> <em class="replaceable"><code>varname</code></em> } [<span class="optional">, ...</span>]</span>] [<span class="optional"> <code class="literal">RETURNING</code> <em class="replaceable"><code>data_type</code></em> [<span class="optional"> <code class="literal">FORMAT JSON</code> [<span class="optional"> <code class="literal">ENCODING UTF8</code> </span>] </span>] </span>] [<span class="optional"> { <code class="literal">WITHOUT</code> | <code class="literal">WITH</code> { <code class="literal">CONDITIONAL</code> | [<span class="optional"><code class="literal">UNCONDITIONAL</code></span>] } } [<span class="optional"> <code class="literal">ARRAY</code> </span>] <code class="literal">WRAPPER</code> </span>] [<span class="optional"> { <code class="literal">KEEP</code> | <code class="literal">OMIT</code> } <code class="literal">QUOTES</code> [<span class="optional"> <code class="literal">ON SCALAR STRING</code> </span>] </span>] [<span class="optional"> { <code class="literal">ERROR</code> | <code class="literal">NULL</code> | <code class="literal">EMPTY</code> { [<span class="optional"> <code class="literal">ARRAY</code> </span>] | <code class="literal">OBJECT</code> } | <code class="literal">DEFAULT</code> <em class="replaceable"><code>expression</code></em> } <code class="literal">ON EMPTY</code> </span>] [<span class="optional"> { <code class="literal">ERROR</code> | <code class="literal">NULL</code> | <code class="literal">EMPTY</code> { [<span class="optional"> <code class="literal">ARRAY</code> </span>] | <code class="literal">OBJECT</code> } | <code class="literal">DEFAULT</code> <em class="replaceable"><code>expression</code></em> } <code class="literal">ON ERROR</code> </span>]) → <code class="returnvalue">jsonb</code>
</pre>
    <p class="func_signature">
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        Returns the result of applying the SQL/JSON
        <em class="replaceable">
         <code>
          path_expression
         </code>
        </em>
        to the
        <em class="replaceable">
         <code>
          context_item
         </code>
        </em>
        .
       </p>
      </li>
      <li class="listitem">
       <p>
        By default, the result is returned as a value of type
        <code class="type">
         jsonb
        </code>
        , though the
        <code class="literal">
         RETURNING
        </code>
        clause can be used to return as some other type to which it can be successfully coerced.
       </p>
      </li>
      <li class="listitem">
       <p>
        If the path expression may return multiple values, it might be necessary to wrap those values using the
        <code class="literal">
         WITH WRAPPER
        </code>
        clause to make it a valid JSON string, because the default behavior is to not wrap them, as if
        <code class="literal">
         WITHOUT WRAPPER
        </code>
        were specified. The
        <code class="literal">
         WITH WRAPPER
        </code>
        clause is by default taken to mean
        <code class="literal">
         WITH UNCONDITIONAL WRAPPER
        </code>
        , which means that even a single result value will be wrapped. To apply the wrapper only when multiple values are present, specify
        <code class="literal">
         WITH CONDITIONAL WRAPPER
        </code>
        . Getting multiple values in result will be treated as an error if
        <code class="literal">
         WITHOUT WRAPPER
        </code>
        is specified.
       </p>
      </li>
      <li class="listitem">
       <p>
        If the result is a scalar string, by default, the returned value will be surrounded by quotes, making it a valid JSON value.  It can be made explicit by specifying
        <code class="literal">
         KEEP QUOTES
        </code>
        .  Conversely, quotes can be omitted by specifying
        <code class="literal">
         OMIT QUOTES
        </code>
        . To ensure that the result is a valid JSON value,
        <code class="literal">
         OMIT QUOTES
        </code>
        cannot be specified when
        <code class="literal">
         WITH WRAPPER
        </code>
        is also specified.
       </p>
      </li>
      <li class="listitem">
       <p>
        The
        <code class="literal">
         ON EMPTY
        </code>
        clause specifies the behavior if evaluating
        <em class="replaceable">
         <code>
          path_expression
         </code>
        </em>
        yields an empty set. The
        <code class="literal">
         ON ERROR
        </code>
        clause specifies the behavior if an error occurs when evaluating
        <em class="replaceable">
         <code>
          path_expression
         </code>
        </em>
        , when coercing the result value to the
        <code class="literal">
         RETURNING
        </code>
        type, or when evaluating the
        <code class="literal">
         ON EMPTY
        </code>
        expression if the
        <em class="replaceable">
         <code>
          path_expression
         </code>
        </em>
        evaluation returns an empty set.
       </p>
      </li>
      <li class="listitem">
       <p>
        For both
        <code class="literal">
         ON EMPTY
        </code>
        and
        <code class="literal">
         ON ERROR
        </code>
        , specifying
        <code class="literal">
         ERROR
        </code>
        will cause an error to be thrown with the appropriate message. Other options include returning an SQL NULL, an empty array (
        <code class="literal">
         EMPTY [
         <span class="optional">
          ARRAY
         </span>
         ]
        </code>
        ), an empty object (
        <code class="literal">
         EMPTY OBJECT
        </code>
        ), or a user-specified expression (
        <code class="literal">
         DEFAULT
        </code>
        <em class="replaceable">
         <code>
          expression
         </code>
        </em>
        ) that can be coerced to jsonb or the type specified in
        <code class="literal">
         RETURNING
        </code>
        . The default when
        <code class="literal">
         ON EMPTY
        </code>
        or
        <code class="literal">
         ON ERROR
        </code>
        is not specified is to return an SQL NULL value.
       </p>
      </li>
     </ul>
    </div>
    <p>
     Examples:
    </p>
    <p>
     <code class="literal">
      JSON_QUERY(jsonb '[1,[2,3],null]', 'lax $[*][$off]' PASSING 1 AS off WITH CONDITIONAL WRAPPER)
     </code>
     →
     <code class="returnvalue">
      3
     </code>
    </p>
    <p>
     <code class="literal">
      JSON_QUERY(jsonb '{"a": "[1, 2]"}', 'lax $.a' OMIT QUOTES)
     </code>
     →
     <code class="returnvalue">
      [1, 2]
     </code>
    </p>
    <p>
     <code class="literal">
      JSON_QUERY(jsonb '{"a": "[1, 2]"}', 'lax $.a' RETURNING int[] OMIT QUOTES ERROR ON ERROR)
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
ERROR:  malformed array literal: "[1, 2]" DETAIL:  Missing "]" after array dimensions.
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
    </p>
    <pre class="synopsis">
<code class="function">JSON_VALUE</code> (
<em class="replaceable"><code>context_item</code></em>, <em class="replaceable"><code>path_expression</code></em>
[<span class="optional"> <code class="literal">PASSING</code> { <em class="replaceable"><code>value</code></em> <code class="literal">AS</code> <em class="replaceable"><code>varname</code></em> } [<span class="optional">, ...</span>]</span>] [<span class="optional"> <code class="literal">RETURNING</code> <em class="replaceable"><code>data_type</code></em> </span>] [<span class="optional"> { <code class="literal">ERROR</code> | <code class="literal">NULL</code> | <code class="literal">DEFAULT</code> <em class="replaceable"><code>expression</code></em> } <code class="literal">ON EMPTY</code> </span>] [<span class="optional"> { <code class="literal">ERROR</code> | <code class="literal">NULL</code> | <code class="literal">DEFAULT</code> <em class="replaceable"><code>expression</code></em> } <code class="literal">ON ERROR</code> </span>]) → <code class="returnvalue">text</code>
</pre>
    <p class="func_signature">
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        Returns the result of applying the SQL/JSON
        <em class="replaceable">
         <code>
          path_expression
         </code>
        </em>
        to the
        <em class="replaceable">
         <code>
          context_item
         </code>
        </em>
        .
       </p>
      </li>
      <li class="listitem">
       <p>
        Only use
        <code class="function">
         JSON_VALUE()
        </code>
        if the extracted value is expected to be a single
        <acronym class="acronym">
         SQL/JSON
        </acronym>
        scalar item; getting multiple values will be treated as an error. If you expect that extracted value might be an object or an array, use the
        <code class="function">
         JSON_QUERY
        </code>
        function instead.
       </p>
      </li>
      <li class="listitem">
       <p>
        By default, the result, which must be a single scalar value, is returned as a value of type
        <code class="type">
         text
        </code>
        , though the
        <code class="literal">
         RETURNING
        </code>
        clause can be used to return as some other type to which it can be successfully coerced.
       </p>
      </li>
      <li class="listitem">
       <p>
        The
        <code class="literal">
         ON ERROR
        </code>
        and
        <code class="literal">
         ON EMPTY
        </code>
        clauses have similar semantics as mentioned in the description of
        <code class="function">
         JSON_QUERY
        </code>
        , except the set of values returned in lieu of throwing an error is different.
       </p>
      </li>
      <li class="listitem">
       <p>
        Note that scalar strings returned by
        <code class="function">
         JSON_VALUE
        </code>
        always have their quotes removed, equivalent to specifying
        <code class="literal">
         OMIT QUOTES
        </code>
        in
        <code class="function">
         JSON_QUERY
        </code>
        .
       </p>
      </li>
     </ul>
    </div>
    <p>
     Examples:
    </p>
    <p>
     <code class="literal">
      JSON_VALUE(jsonb '"123.45"', '$' RETURNING float)
     </code>
     →
     <code class="returnvalue">
      123.45
     </code>
    </p>
    <p>
     <code class="literal">
      JSON_VALUE(jsonb '"03:04 2015-02-01"', '$.datetime("HH24:MI YYYY-MM-DD")' RETURNING date)
     </code>
     →
     <code class="returnvalue">
      2015-02-01
     </code>
    </p>
    <p>
     <code class="literal">
      JSON_VALUE(jsonb '[1,2]', 'strict $[$off]' PASSING 1 as off)
     </code>
     →
     <code class="returnvalue">
      2
     </code>
    </p>
    <p>
     <code class="literal">
      JSON_VALUE(jsonb '[1,2]', 'strict $[*]' DEFAULT 9 ON ERROR)
     </code>
     →
     <code class="returnvalue">
      9
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>









### Nota

A expressão *`context_item`* é convertida para `jsonb` por uma conversão implícita se a expressão não estiver já do tipo `jsonb`. No entanto, observe que quaisquer erros de análise que ocorram durante essa conversão são lançados incondicionalmente, ou seja, não são tratados de acordo com a cláusula (especificada ou implícita) `ON ERROR`.

### Nota

`JSON_VALUE()` retorna um NULL SQL se *`path_expression`* retornar um JSON `null`, enquanto `JSON_QUERY()` retorna o JSON `null` como está.

### 9.16.4. JSON_TABLE [#](#FUNCTIONS-SQLJSON-TABLE)

`JSON_TABLE` é uma função SQL/JSON que consulta dados JSON e apresenta os resultados como uma visão relacional, que pode ser acessada como uma tabela SQL regular. Você pode usar `JSON_TABLE` dentro da cláusula `FROM` de um `SELECT`, `UPDATE` ou `DELETE` e como fonte de dados em uma declaração `MERGE`.

Tomando os dados JSON como entrada, `JSON_TABLE` usa uma expressão de caminho JSON para extrair uma parte dos dados fornecidos para ser usada como um *padrão de linha* para a visão construída. Cada valor SQL/JSON dado pelo padrão de linha serve como fonte para uma linha separada na visão construída.

Para dividir o padrão de linha em colunas, `JSON_TABLE` fornece a cláusula `COLUMNS` que define o esquema da visão criada. Para cada coluna, uma expressão de caminho JSON separada pode ser especificada para ser avaliada contra o padrão de linha para obter um valor SQL/JSON que se tornará o valor para a coluna especificada em uma determinada linha de saída.

Os dados JSON armazenados em um nível aninhado do padrão de linha podem ser extraídos usando a cláusula `NESTED PATH`. Cada cláusula `NESTED PATH` pode ser usada para gerar uma ou mais colunas usando os dados de um nível aninhado do padrão de linha. Essas colunas podem ser especificadas usando uma cláusula `COLUMNS` que se assemelha à cláusula COLUMNS de nível superior. As linhas construídas a partir de COLUNAS ANHADAS são chamadas de *linhas filhas* e são unidas contra a linha construída a partir das colunas especificadas na cláusula `COLUMNS` do parentesco para obter a linha na visão final. As colunas próprias das *linhas filhas* podem conter uma especificação `NESTED PATH`, permitindo assim extrair dados localizados em níveis de aninhamento arbitrários. As colunas produzidas por múltiplas `NESTED PATH`s no mesmo nível são consideradas *irmãs* umas das outras e suas linhas após a junção com a linha do parentesco são combinadas usando a UNION.

As linhas produzidas por `JSON_TABLE` são unidas lateralmente à linha que as gerou, então você não precisa unir explicitamente a visão construída com a tabela original que contém dados JSON.

A sintaxe é:

```
JSON_TABLE (
    context_item, path_expression [ AS json_path_name ] [ PASSING { value AS varname } [, ...] ]
    COLUMNS ( json_table_column [, ...] )
    [ { ERROR | EMPTY [ARRAY]} ON ERROR ]
)


where json_table_column is:

  name FOR ORDINALITY
  | name type
        [ FORMAT JSON [ENCODING UTF8]]
        [ PATH path_expression ]
        [ { WITHOUT | WITH { CONDITIONAL | [UNCONDITIONAL] } } [ ARRAY ] WRAPPER ]
        [ { KEEP | OMIT } QUOTES [ ON SCALAR STRING ] ]
        [ { ERROR | NULL | EMPTY { [ARRAY] | OBJECT } | DEFAULT expression } ON EMPTY ]
        [ { ERROR | NULL | EMPTY { [ARRAY] | OBJECT } | DEFAULT expression } ON ERROR ]
  | name type EXISTS [ PATH path_expression ]
        [ { ERROR | TRUE | FALSE | UNKNOWN } ON ERROR ]
  | NESTED [ PATH ] path_expression [ AS json_path_name ] COLUMNS ( json_table_column [, ...] )
```

Cada elemento de sintaxe é descrito abaixo com mais detalhes.

`context_item, path_expression [ AS json_path_name ] [ PASSING { value AS varname } [, ...]]`: O *`context_item` especifica o documento de entrada a ser pesquisado, o *`path_expression` é uma expressão de caminho SQL/JSON que define a consulta, e o *`json_path_name` é um nome opcional para o *`path_expression`*. A cláusula opcional `PASSING` fornece valores de dados para as variáveis mencionadas no *`path_expression`*. O resultado da avaliação dos dados de entrada usando os elementos mencionados é chamado de *padrão de linha*, que é usado como fonte para os valores das linhas na visão construída.

`COLUMNS` ( *`json_table_column`* [, ...] ): A cláusula `COLUMNS` que define o esquema da visão construída. Nesta cláusula, você pode especificar cada coluna a ser preenchida com um valor SQL/JSON obtido aplicando uma expressão de caminho JSON contra o padrão da linha. *`json_table_column`* tem as seguintes variantes:

*`name`* `FOR ORDINALITY` : Adiciona uma coluna de ordinalidade que fornece numeração sequencial de linhas a partir do número 1. Cada `NESTED PATH` (veja abaixo) recebe seu próprio contador para qualquer coluna de ordinalidade aninhada.

`name type [FORMAT JSON [ENCODING UTF8]] [ PATH path_expression ]` : Insere um valor SQL/JSON obtido aplicando *`path_expression`* contra o padrão da linha na linha de saída da visão após a coerência para o especificado *`type`*.

Especificar `FORMAT JSON` torna explícito que você espera que o valor seja um objeto válido `json`. Só faz sentido especificar `FORMAT JSON` se *`type`* é um dos tipos `bpchar`, `bytea`, `character varying`, `name`, `json`, `jsonb`, `text`, ou um domínio sobre esses tipos.

Opcionalmente, você pode especificar as cláusulas `WRAPPER` e `QUOTES` para formatar a saída. Observe que especificar `OMIT QUOTES` substitui `FORMAT JSON` se também for especificado, porque literais não citados não constituem valores válidos de `json`.

Opcionalmente, você pode usar as cláusulas `ON EMPTY` e `ON ERROR` para especificar se deve ser lançado o erro ou retornar o valor especificado quando o resultado da avaliação do caminho JSON estiver vazio e quando ocorrer um erro durante a avaliação do caminho JSON ou quando a coerção do valor SQL/JSON para o tipo especificado, respectivamente. O padrão para ambas é retornar um valor `NULL`.

### Nota

Esta cláusula é internamente convertida e tem a mesma semântica que `JSON_VALUE` ou `JSON_QUERY`. Esta última se o tipo especificado não for um tipo escalar ou se alguma das cláusulas `FORMAT JSON`, `WRAPPER` ou `QUOTES` estiver presente.

*`name`* *`type`* `EXISTS` [ `PATH` *`path_expression` ] :   Insere um valor booleano obtido aplicando *`path_expression`* contra o padrão da linha na linha de saída da visualização, após a coerência para o *`type`* especificado.

O valor corresponde à questão de se a aplicação da expressão `PATH` ao padrão da linha gera algum valor.

O especificado *`type`* deve ter um molde do tipo `boolean`.

Opcionalmente, você pode usar `ON ERROR` para especificar se deve ser lançada a erro ou retornado o valor especificado quando ocorre um erro durante a avaliação do caminho JSON ou quando o valor SQL/JSON é coercido para o tipo especificado. O padrão é retornar um valor booleano `FALSE`.

### Nota

Esta cláusula é internamente convertida e tem a mesma semântica que `JSON_EXISTS`.

`NESTED [ PATH ]` *`path_expression`* [ `AS` *`json_path_name`* ] `COLUMNS` ( *`json_table_column`* [, ...] ) :   Extrai valores SQL/JSON de níveis aninhados do padrão da linha, gera uma ou mais colunas conforme definido pela cláusula `COLUMNS`, e insere os valores SQL/JSON extraídos nessas colunas. A expressão *`json_table_column`* na cláusula `COLUMNS` usa a mesma sintaxe que na cláusula `COLUMNS` pai.

A sintaxe `NESTED PATH` é recursiva, então você pode descer vários níveis aninhados, especificando várias subcláusulas `NESTED PATH` dentro uma da outra. Isso permite desanidar a hierarquia de objetos e arrays JSON em uma única invocação de função, em vez de concatenar várias expressões `JSON_TABLE` em uma declaração SQL.

### Nota

Em cada variante de *`json_table_column`* descrito acima, se a cláusula `PATH` for omitida, a expressão de caminho `$.name` é usada, onde *`name`* é o nome da coluna fornecida.

`AS` *`json_path_name`*: O opcional *`json_path_name`* serve como identificador do *`path_expression`* fornecido. O nome deve ser único e distinto dos nomes das colunas.

{ `ERROR` | `EMPTY` } `ON ERROR`: O opcional `ON ERROR` pode ser usado para especificar como lidar com erros ao avaliar o *`path_expression`* de nível superior. Use `ERROR` se você deseja que os erros sejam lançados e `EMPTY` para retornar uma tabela vazia, ou seja, uma tabela contendo 0 linhas. Observe que esta cláusula não afeta os erros que ocorrem ao avaliar colunas, para os quais o comportamento depende de se a cláusula `ON ERROR` é especificada contra uma coluna dada.

Exemplos

Nos exemplos que se seguem, a tabela a seguir, contendo dados em JSON, será utilizada:

```
CREATE TABLE my_films ( js jsonb );

INSERT INTO my_films VALUES (
'{ "favorites" : [
   { "kind" : "comedy", "films" : [
     { "title" : "Bananas",
       "director" : "Woody Allen"},
     { "title" : "The Dinner Game",
       "director" : "Francis Veber" } ] },
   { "kind" : "horror", "films" : [
     { "title" : "Psycho",
       "director" : "Alfred Hitchcock" } ] },
   { "kind" : "thriller", "films" : [
     { "title" : "Vertigo",
       "director" : "Alfred Hitchcock" } ] },
   { "kind" : "drama", "films" : [
     { "title" : "Yojimbo",
       "director" : "Akira Kurosawa" } ] }
  ] }');
```

A consulta a seguir mostra como usar `JSON_TABLE` para transformar os objetos JSON da tabela `my_films` em uma visão que contenha colunas para as chaves `kind`, `title` e `director` contidas no JSON original, juntamente com uma coluna de ordinalidade:

```
SELECT jt.* FROM
 my_films,
 JSON_TABLE (js, '$.favorites[*]' COLUMNS (
   id FOR ORDINALITY,
   kind text PATH '$.kind',
   title text PATH '$.films[*].title' WITH WRAPPER,
   director text PATH '$.films[*].director' WITH WRAPPER)) AS jt;
```

```
 id |   kind   |             title              |             director
----+----------+--------------------------------+----------------------------------
  1 | comedy   | ["Bananas", "The Dinner Game"] | ["Woody Allen", "Francis Veber"]
  2 | horror   | ["Psycho"]                     | ["Alfred Hitchcock"]
  3 | thriller | ["Vertigo"]                    | ["Alfred Hitchcock"]
  4 | drama    | ["Yojimbo"]                    | ["Akira Kurosawa"]
(4 rows)
```

O que se segue é uma versão modificada da consulta acima para mostrar o uso dos argumentos `PASSING` no filtro especificado na expressão do caminho JSON de nível superior e as várias opções para as colunas individuais:

```
SELECT jt.* FROM
 my_films,
 JSON_TABLE (js, '$.favorites[*] ? (@.films[*].director == $filter)'
   PASSING 'Alfred Hitchcock' AS filter
     COLUMNS (
     id FOR ORDINALITY,
     kind text PATH '$.kind',
     title text FORMAT JSON PATH '$.films[*].title' OMIT QUOTES,
     director text PATH '$.films[*].director' KEEP QUOTES)) AS jt;
```

```
 id |   kind   |  title  |      director
----+----------+---------+--------------------
  1 | horror   | Psycho  | "Alfred Hitchcock"
  2 | thriller | Vertigo | "Alfred Hitchcock"
(2 rows)
```

O que se segue é uma versão modificada da consulta acima para mostrar o uso de `NESTED PATH` para preencher as colunas de título e diretor, ilustrando como elas são unidas às colunas parent id e kind:

```
SELECT jt.* FROM
 my_films,
 JSON_TABLE ( js, '$.favorites[*] ? (@.films[*].director == $filter)'
   PASSING 'Alfred Hitchcock' AS filter
   COLUMNS (
    id FOR ORDINALITY,
    kind text PATH '$.kind',
    NESTED PATH '$.films[*]' COLUMNS (
      title text FORMAT JSON PATH '$.title' OMIT QUOTES,
      director text PATH '$.director' KEEP QUOTES))) AS jt;
```

```
 id |   kind   |  title  |      director
----+----------+---------+--------------------
  1 | horror   | Psycho  | "Alfred Hitchcock"
  2 | thriller | Vertigo | "Alfred Hitchcock"
(2 rows)
```

O que segue é a mesma consulta, mas sem o filtro no caminho raiz:

```
SELECT jt.* FROM
 my_films,
 JSON_TABLE ( js, '$.favorites[*]'
   COLUMNS (
    id FOR ORDINALITY,
    kind text PATH '$.kind',
    NESTED PATH '$.films[*]' COLUMNS (
      title text FORMAT JSON PATH '$.title' OMIT QUOTES,
      director text PATH '$.director' KEEP QUOTES))) AS jt;
```

```
 id |   kind   |      title      |      director
----+----------+-----------------+--------------------
  1 | comedy   | Bananas         | "Woody Allen"
  1 | comedy   | The Dinner Game | "Francis Veber"
  2 | horror   | Psycho          | "Alfred Hitchcock"
  3 | thriller | Vertigo         | "Alfred Hitchcock"
  4 | drama    | Yojimbo         | "Akira Kurosawa"
(5 rows)
```

O que se segue mostra outra consulta que utiliza um objeto diferente `JSON` como entrada. Ela mostra a junção UNION entre os caminhos `$.movies[*]` e `$.books[*]` do `NESTED` e também o uso da coluna `FOR ORDINALITY` nos níveis de `NESTED` (colunas `movie_id`, `book_id` e `author_id`):

```
SELECT * FROM JSON_TABLE (
'{"favorites":
    [{"movies":
      [{"name": "One", "director": "John Doe"},
       {"name": "Two", "director": "Don Joe"}],
     "books":
      [{"name": "Mystery", "authors": [{"name": "Brown Dan"}]},
       {"name": "Wonder", "authors": [{"name": "Jun Murakami"}, {"name":"Craig Doe"}]}]
}]}'::json, '$.favorites[*]'
COLUMNS (
  user_id FOR ORDINALITY,
  NESTED '$.movies[*]'
    COLUMNS (
    movie_id FOR ORDINALITY,
    mname text PATH '$.name',
    director text),
  NESTED '$.books[*]'
    COLUMNS (
      book_id FOR ORDINALITY,
      bname text PATH '$.name',
      NESTED '$.authors[*]'
        COLUMNS (
          author_id FOR ORDINALITY,
          author_name text PATH '$.name'))));
```

```
 user_id | movie_id | mname | director | book_id |  bname  | author_id | author_name
---------+----------+-------+----------+---------+---------+-----------+--------------
       1 |        1 | One   | John Doe |         |         |           |
       1 |        2 | Two   | Don Joe  |         |         |           |
       1 |          |       |          |       1 | Mystery |         1 | Brown Dan
       1 |          |       |          |       2 | Wonder  |         1 | Jun Murakami
       1 |          |       |          |       2 | Wonder  |         2 | Craig Doe
(5 rows)
```
