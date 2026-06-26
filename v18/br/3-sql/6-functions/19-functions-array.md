## 9.19. Funções e operadores de matriz [#](#FUNCTIONS-ARRAY)

[Tabela 9.56](functions-array.md#ARRAY-OPERATORS-TABLE) mostra os operadores especializados disponíveis para tipos de matriz. Além desses, os operadores de comparação comuns mostrados em [Tabela 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) estão disponíveis para matrizes. Os operadores de comparação comparam o conteúdo da matriz elemento a elemento, usando a função de comparação padrão de árvore B para o tipo de dados do elemento, e ordenam com base na primeira diferença. Em matrizes multidimensionais, os elementos são visitados em ordem de linha (a última subexposição varia mais rapidamente). Se o conteúdo de duas matrizes for igual, mas a dimensionalidade for diferente, a primeira diferença na informação de dimensionalidade determina a ordem de classificação.

**Tabela 9.56. Operadores de matriz**



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
      anyarray
     </code>
     <code>
      @&gt;
     </code>
     <code>
      anyarray
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     O primeiro array contém o segundo, ou seja, cada elemento que aparece no segundo array é igual a algum elemento do primeiro array? (Os duplicados não são tratados de forma especial, portanto
     <code>
      ARRAY[1]
     </code>
     e
     <code>
      ARRAY[1,1]
     </code>
     são considerados que cada um contém o outro.)
    </p>
    <p>
     <code>
      ARRAY[1,4,3] @&gt; ARRAY[3,1,3]
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
      anyarray
     </code>
     <code>
      &lt;@
     </code>
     <code>
      anyarray
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     O primeiro array está contido pelo segundo?
    </p>
    <p>
     <code>
      ARRAY[2,2,7] &lt;@ ARRAY[1,7,4,2,6]
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
      anyarray
     </code>
     <code>
      &amp;&amp;
     </code>
     <code>
      anyarray
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     Os arrays se sobrepõem, ou seja, têm algum elemento em comum?
    </p>
    <p>
     <code>
      ARRAY[1,4,3] &amp;&amp; ARRAY[2,1]
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
      anycompatiblearray
     </code>
     <code>
      ||
     </code>
     <code>
      anycompatiblearray
     </code>
     →
     <code>
      anycompatiblearray
     </code>
    </p>
    <p>
     Concatenia os dois arrays. Concatenar um array nulo ou vazio não faz nada; caso contrário, os arrays devem ter o mesmo número de dimensões (como ilustrado no primeiro exemplo) ou diferir em número de dimensões em um (como ilustrado no segundo). Se os arrays não forem do mesmo tipo de elemento, eles serão coeridos para um tipo comum (consulte
     <a class="xref" href="typeconv-union-case.md" title="10.5. UNION, CASE, and Related Constructs">
      Seção 10.5
     </a>
     ).
    </p>
    <p>
     <code>
      ARRAY[1,2,3] || ARRAY[4,5,6,7]
     </code>
     →
     <code>
      {1,2,3,4,5,6,7}
     </code>
    </p>
    <p>
     <code>
      ARRAY[1,2,3] || ARRAY[[4,5,6],[7,8,9.9]]
     </code>
     →
     <code>
      {{1,2,3},{4,5,6},{7,8,9.9}}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      anycompatible
     </code>
     <code>
      ||
     </code>
     <code>
      anycompatiblearray
     </code>
     →
     <code>
      anycompatiblearray
     </code>
    </p>
    <p>
     Concatenia um elemento na frente de uma matriz (que deve estar vazia ou unidimensional).
    </p>
    <p>
     <code>
      3 || ARRAY[4,5,6]
     </code>
     →
     <code>
      {3,4,5,6}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      anycompatiblearray
     </code>
     <code>
      ||
     </code>
     <code>
      anycompatible
     </code>
     →
     <code>
      anycompatiblearray
     </code>
    </p>
    <p>
     Concatenia um elemento no final de uma matriz (que deve estar vazia ou unidimensional).
    </p>
    <p>
     <code>
      ARRAY[4,5,6] || 7
     </code>
     →
     <code>
      {4,5,6,7}
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>










Veja [Seção 8.15](arrays.md) para mais detalhes sobre o comportamento do operador de matriz. Veja [Seção 11.2](indexes-types.md) para mais detalhes sobre quais operadores suportam operações indexadas.

[Tabela 9.57](functions-array.md#ARRAY-FUNCTIONS-TABLE) mostra as funções disponíveis para uso com tipos de matriz. Consulte [Seção 8.15](arrays.md) para mais informações e exemplos de uso dessas funções.

**Tabela 9.57. Funções de matriz**



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
      array_append
     </code>
     (
     <code>
      anycompatiblearray
     </code>
     ,
     <code>
      anycompatible
     </code>
     ) →
     <code>
      anycompatiblearray
     </code>
    </p>
    <p>
     Appends an element to the end of an array (same as the
     <code>
      anycompatiblearray
     </code>
     <code>
      ||
     </code>
     <code>
      anycompatible
     </code>
     operator).
    </p>
    <p>
     <code>
      array_append(ARRAY[1,2], 3)
     </code>
     →
     <code>
      {1,2,3}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_cat
     </code>
     (
     <code>
      anycompatiblearray
     </code>
     ,
     <code>
      anycompatiblearray
     </code>
     ) →
     <code>
      anycompatiblearray
     </code>
    </p>
    <p>
     Concatenates two arrays (same as the
     <code>
      anycompatiblearray
     </code>
     <code>
      ||
     </code>
     <code>
      anycompatiblearray
     </code>
     operator).
    </p>
    <p>
     <code>
      array_cat(ARRAY[1,2,3], ARRAY[4,5])
     </code>
     →
     <code>
      {1,2,3,4,5}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_dims
     </code>
     (
     <code>
      anyarray
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Returns a text representation of the array's dimensions.
    </p>
    <p>
     <code>
      array_dims(ARRAY[[1,2,3], [4,5,6]])
     </code>
     →
     <code>
      [1:2][1:3]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_fill
     </code>
     (
     <code>
      anyelement
     </code>
     ,
     <code>
      integer[]
     </code>
     [
     <span class="optional">
      ,
      <code>
       integer[]
      </code>
     </span>
     ] ) →
     <code>
      anyarray
     </code>
    </p>
    <p>
     Returns an array filled with copies of the given value, having dimensions of the lengths specified by the second argument. The optional third argument supplies lower-bound values for each dimension (which default to all
     <code>
      1
     </code>
     ).
    </p>
    <p>
     <code>
      array_fill(11, ARRAY[2,3])
     </code>
     →
     <code>
      {{11,11,11},{11,11,11}}
     </code>
    </p>
    <p>
     <code>
      array_fill(7, ARRAY[3], ARRAY[2])
     </code>
     →
     <code>
      [2:4]={7,7,7}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_length
     </code>
     (
     <code>
      anyarray
     </code>
     ,
     <code>
      integer
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns the length of the requested array dimension. (Produces NULL instead of 0 for empty or missing array dimensions.)
    </p>
    <p>
     <code>
      array_length(array[1,2,3], 1)
     </code>
     →
     <code>
      3
     </code>
    </p>
    <p>
     <code>
      array_length(array[]::int[], 1)
     </code>
     →
     <code>
      NULL
     </code>
    </p>
    <p>
     <code>
      array_length(array['text'], 2)
     </code>
     →
     <code>
      NULL
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_lower
     </code>
     (
     <code>
      anyarray
     </code>
     ,
     <code>
      integer
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns the lower bound of the requested array dimension.
    </p>
    <p>
     <code>
      array_lower('[0:2]={1,2,3}'::integer[], 1)
     </code>
     →
     <code>
      0
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_ndims
     </code>
     (
     <code>
      anyarray
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns the number of dimensions of the array.
    </p>
    <p>
     <code>
      array_ndims(ARRAY[[1,2,3], [4,5,6]])
     </code>
     →
     <code>
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_position
     </code>
     (
     <code>
      anycompatiblearray
     </code>
     ,
     <code>
      anycompatible
     </code>
     [
     <span class="optional">
      ,
      <code>
       integer
      </code>
     </span>
     ] ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns the subscript of the first occurrence of the second argument in the array, or
     <code>
      NULL
     </code>
     if it's not present. If the third argument is given, the search begins at that subscript. The array must be one-dimensional. Comparisons are done using
     <code>
      IS NOT DISTINCT FROM
     </code>
     semantics, so it is possible to search for
     <code>
      NULL
     </code>
     .
    </p>
    <p>
     <code>
      array_position(ARRAY['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'], 'mon')
     </code>
     →
     <code>
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_positions
     </code>
     (
     <code>
      anycompatiblearray
     </code>
     ,
     <code>
      anycompatible
     </code>
     ) →
     <code>
      integer[]
     </code>
    </p>
    <p>
     Returns an array of the subscripts of all occurrences of the second argument in the array given as first argument. The array must be one-dimensional. Comparisons are done using
     <code>
      IS NOT DISTINCT FROM
     </code>
     semantics, so it is possible to search for
     <code>
      NULL
     </code>
     .
     <code>
      NULL
     </code>
     is returned only if the array is
     <code>
      NULL
     </code>
     ; if the value is not found in the array, an empty array is returned.
    </p>
    <p>
     <code>
      array_positions(ARRAY['A','A','B','A'], 'A')
     </code>
     →
     <code>
      {1,2,4}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_prepend
     </code>
     (
     <code>
      anycompatible
     </code>
     ,
     <code>
      anycompatiblearray
     </code>
     ) →
     <code>
      anycompatiblearray
     </code>
    </p>
    <p>
     Prepends an element to the beginning of an array (same as the
     <code>
      anycompatible
     </code>
     <code>
      ||
     </code>
     <code>
      anycompatiblearray
     </code>
     operator).
    </p>
    <p>
     <code>
      array_prepend(1, ARRAY[2,3])
     </code>
     →
     <code>
      {1,2,3}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_remove
     </code>
     (
     <code>
      anycompatiblearray
     </code>
     ,
     <code>
      anycompatible
     </code>
     ) →
     <code>
      anycompatiblearray
     </code>
    </p>
    <p>
     Removes all elements equal to the given value from the array. The array must be one-dimensional. Comparisons are done using
     <code>
      IS NOT DISTINCT FROM
     </code>
     semantics, so it is possible to remove
     <code>
      NULL
     </code>
     s.
    </p>
    <p>
     <code>
      array_remove(ARRAY[1,2,3,2], 2)
     </code>
     →
     <code>
      {1,3}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_replace
     </code>
     (
     <code>
      anycompatiblearray
     </code>
     ,
     <code>
      anycompatible
     </code>
     ,
     <code>
      anycompatible
     </code>
     ) →
     <code>
      anycompatiblearray
     </code>
    </p>
    <p>
     Replaces each array element equal to the second argument with the third argument.
    </p>
    <p>
     <code>
      array_replace(ARRAY[1,2,5,4], 5, 3)
     </code>
     →
     <code>
      {1,2,3,4}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_reverse
     </code>
     (
     <code>
      anyarray
     </code>
     ) →
     <code>
      anyarray
     </code>
    </p>
    <p>
     Reverses the first dimension of the array.
    </p>
    <p>
     <code>
      array_reverse(ARRAY[[1,2],[3,4],[5,6]])
     </code>
     →
     <code>
      {{5,6},{3,4},{1,2}}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_sample
     </code>
     (
     <em class="parameter">
      <code>
       array
      </code>
     </em>
     <code>
      anyarray
     </code>
     ,
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      anyarray
     </code>
    </p>
    <p>
     Returns an array of
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     items randomly selected from
     <em class="parameter">
      <code>
       array
      </code>
     </em>
     .
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     may not exceed the length of
     <em class="parameter">
      <code>
       array
      </code>
     </em>
     's first dimension. If
     <em class="parameter">
      <code>
       array
      </code>
     </em>
     is multi-dimensional, an
     <span class="quote">
      “
      <span class="quote">
       item
      </span>
      ”
     </span>
     is a slice having a given first subscript.
    </p>
    <p>
     <code>
      array_sample(ARRAY[1,2,3,4,5,6], 3)
     </code>
     →
     <code>
      {2,6,1}
     </code>
    </p>
    <p>
     <code>
      array_sample(ARRAY[[1,2],[3,4],[5,6]], 2)
     </code>
     →
     <code>
      {{5,6},{1,2}}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_shuffle
     </code>
     (
     <code>
      anyarray
     </code>
     ) →
     <code>
      anyarray
     </code>
    </p>
    <p>
     Randomly shuffles the first dimension of the array.
    </p>
    <p>
     <code>
      array_shuffle(ARRAY[[1,2],[3,4],[5,6]])
     </code>
     →
     <code>
      {{5,6},{1,2},{3,4}}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_sort
     </code>
     (
     <em class="parameter">
      <code>
       array
      </code>
     </em>
     <code>
      anyarray
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        descending
       </code>
      </em>
      <code>
       boolean
      </code>
      [
      <span class="optional">
       ,
       <em class="parameter">
        <code>
         nulls_first
        </code>
       </em>
       <code>
        boolean
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code>
      anyarray
     </code>
    </p>
    <p>
     Sorts the first dimension of the array. The sort order is determined by the default sort ordering of the array's element type; however, if the element type is collatable, the collation to use can be specified by adding a
     <code>
      COLLATE
     </code>
     clause to the
     <em class="parameter">
      <code>
       array
      </code>
     </em>
     argument.
    </p>
    <p>
     If
     <em class="parameter">
      <code>
       descending
      </code>
     </em>
     is true then sort in descending order, otherwise ascending order.  If omitted, the default is ascending order. If
     <em class="parameter">
      <code>
       nulls_first
      </code>
     </em>
     is true then nulls appear before non-null values, otherwise nulls appear after non-null values. If omitted,
     <em class="parameter">
      <code>
       nulls_first
      </code>
     </em>
     is taken to have the same value as
     <em class="parameter">
      <code>
       descending
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      array_sort(ARRAY[[2,4],[2,1],[6,5]])
     </code>
     →
     <code>
      {{2,1},{2,4},{6,5}}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_to_string
     </code>
     (
     <em class="parameter">
      <code>
       array
      </code>
     </em>
     <code>
      anyarray
     </code>
     ,
     <em class="parameter">
      <code>
       delimiter
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
        null_string
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
     Converts each array element to its text representation, and concatenates those separated by the
     <em class="parameter">
      <code>
       delimiter
      </code>
     </em>
     string. If
     <em class="parameter">
      <code>
       null_string
      </code>
     </em>
     is given and is not
     <code>
      NULL
     </code>
     , then
     <code>
      NULL
     </code>
     array entries are represented by that string; otherwise, they are omitted. See also
     <a class="link" href="functions-string.md#FUNCTION-STRING-TO-ARRAY">
      <code>
       string_to_array
      </code>
     </a>
     .
    </p>
    <p>
     <code>
      array_to_string(ARRAY[1, 2, 3, NULL, 5], ',', '*')
     </code>
     →
     <code>
      1,2,3,*,5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_upper
     </code>
     (
     <code>
      anyarray
     </code>
     ,
     <code>
      integer
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns the upper bound of the requested array dimension.
    </p>
    <p>
     <code>
      array_upper(ARRAY[1,8,3,7], 1)
     </code>
     →
     <code>
      4
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cardinality
     </code>
     (
     <code>
      anyarray
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns the total number of elements in the array, or 0 if the array is empty.
    </p>
    <p>
     <code>
      cardinality(ARRAY[[1,2],[3,4]])
     </code>
     →
     <code>
      4
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      trim_array
     </code>
     (
     <em class="parameter">
      <code>
       array
      </code>
     </em>
     <code>
      anyarray
     </code>
     ,
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      anyarray
     </code>
    </p>
    <p>
     Trims an array by removing the last
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     elements. If the array is multidimensional, only the first dimension is trimmed.
    </p>
    <p>
     <code>
      trim_array(ARRAY[1,2,3,4,5,6], 2)
     </code>
     →
     <code>
      {1,2,3,4}
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
      anyarray
     </code>
     ) →
     <code>
      setof anyelement
     </code>
    </p>
    <p>
     Expands an array into a set of rows. The array's elements are read out in storage order.
    </p>
    <p>
     <code>
      unnest(ARRAY[1,2])
     </code>
     →
     <code>
     </code>
    </p>
    <pre class="programlisting">
 1 2
</pre>
    <p>
    </p>
    <p>
     <code>
      unnest(ARRAY[['foo','bar'],['baz','quux']])
     </code>
     →
     <code>
     </code>
    </p>
    <pre class="programlisting">
 foo bar baz quux
</pre>
    <p>
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
      anyarray
     </code>
     ,
     <code>
      anyarray
     </code>
     [
     <span class="optional">
      , ...
     </span>
     ] ) →
     <code>
      setof anyelement, anyelement [, ... ]
     </code>
    </p>
    <p>
     Expands multiple arrays (possibly of different data types) into a set of rows.  If the arrays are not all the same length then the shorter ones are padded with
     <code>
      NULL
     </code>
     s.  This form is only allowed in a query's FROM clause; see
     <a class="xref" href="queries-table-expressions.md#QUERIES-TABLEFUNCTIONS" title="7.2.1.4. Table Functions">
      Section 7.2.1.4
     </a>
     .
    </p>
    <p>
     <code>
      select * from unnest(ARRAY[1,2], ARRAY['foo','bar','baz']) as x(a,b)
     </code>
     →
     <code>
     </code>
    </p>
    <pre class="programlisting">
 a |  b ---+----- 1 | foo 2 | bar
   | baz
</pre>
    <p>
    </p>
   </td>
  </tr>
 </tbody>
</table>










Veja também [Seção 9.21](functions-aggregate.md) sobre a função agregada `array_agg` para uso com matrizes.