## 9.19. Funções e operadores de matriz [#](#FUNCTIONS-ARRAY)

[Tabela 9.56](functions-array.md#ARRAY-OPERATORS-TABLE) mostra os operadores especializados disponíveis para tipos de matriz. Além desses, os operadores de comparação comuns mostrados em [Tabela 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) estão disponíveis para matrizes. Os operadores de comparação comparam o conteúdo da matriz elemento a elemento, usando a função de comparação padrão de árvore B para o tipo de dados do elemento, e ordenam com base na primeira diferença. Em matrizes multidimensionais, os elementos são visitados em ordem de linha (a última subexposição varia mais rapidamente). Se o conteúdo de duas matrizes for igual, mas a dimensionalidade for diferente, a primeira diferença na informação de dimensionalidade determina a ordem de classificação.

**Tabela 9.56. Operadores de matriz**



<table border="1" class="table" summary="Array Operators">
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
      anyarray
     </code>
     <code class="literal">
      @&gt;
     </code>
     <code class="type">
      anyarray
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     O primeiro array contém o segundo, ou seja, cada elemento que aparece no segundo array é igual a algum elemento do primeiro array? (Os duplicados não são tratados de forma especial, portanto
     <code class="literal">
      ARRAY[1]
     </code>
     e
     <code class="literal">
      ARRAY[1,1]
     </code>
     são considerados que cada um contém o outro.)
    </p>
    <p>
     <code class="literal">
      ARRAY[1,4,3] @&gt; ARRAY[3,1,3]
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
      anyarray
     </code>
     <code class="literal">
      &lt;@
     </code>
     <code class="type">
      anyarray
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     O primeiro array está contido pelo segundo?
    </p>
    <p>
     <code class="literal">
      ARRAY[2,2,7] &lt;@ ARRAY[1,7,4,2,6]
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
      anyarray
     </code>
     <code class="literal">
      &amp;&amp;
     </code>
     <code class="type">
      anyarray
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Os arrays se sobrepõem, ou seja, têm algum elemento em comum?
    </p>
    <p>
     <code class="literal">
      ARRAY[1,4,3] &amp;&amp; ARRAY[2,1]
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
      anycompatiblearray
     </code>
     <code class="literal">
      ||
     </code>
     <code class="type">
      anycompatiblearray
     </code>
     →
     <code class="returnvalue">
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
     <code class="literal">
      ARRAY[1,2,3] || ARRAY[4,5,6,7]
     </code>
     →
     <code class="returnvalue">
      {1,2,3,4,5,6,7}
     </code>
    </p>
    <p>
     <code class="literal">
      ARRAY[1,2,3] || ARRAY[[4,5,6],[7,8,9.9]]
     </code>
     →
     <code class="returnvalue">
      {{1,2,3},{4,5,6},{7,8,9.9}}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      anycompatible
     </code>
     <code class="literal">
      ||
     </code>
     <code class="type">
      anycompatiblearray
     </code>
     →
     <code class="returnvalue">
      anycompatiblearray
     </code>
    </p>
    <p>
     Concatenia um elemento na frente de uma matriz (que deve estar vazia ou unidimensional).
    </p>
    <p>
     <code class="literal">
      3 || ARRAY[4,5,6]
     </code>
     →
     <code class="returnvalue">
      {3,4,5,6}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      anycompatiblearray
     </code>
     <code class="literal">
      ||
     </code>
     <code class="type">
      anycompatible
     </code>
     →
     <code class="returnvalue">
      anycompatiblearray
     </code>
    </p>
    <p>
     Concatenia um elemento no final de uma matriz (que deve estar vazia ou unidimensional).
    </p>
    <p>
     <code class="literal">
      ARRAY[4,5,6] || 7
     </code>
     →
     <code class="returnvalue">
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



<table border="1" class="table" summary="Array Functions">
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
      array_append
     </code>
     (
     <code class="type">
      anycompatiblearray
     </code>
     ,
     <code class="type">
      anycompatible
     </code>
     ) →
     <code class="returnvalue">
      anycompatiblearray
     </code>
    </p>
    <p>
     Appends an element to the end of an array (same as the
     <code class="type">
      anycompatiblearray
     </code>
     <code class="literal">
      ||
     </code>
     <code class="type">
      anycompatible
     </code>
     operator).
    </p>
    <p>
     <code class="literal">
      array_append(ARRAY[1,2], 3)
     </code>
     →
     <code class="returnvalue">
      {1,2,3}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      array_cat
     </code>
     (
     <code class="type">
      anycompatiblearray
     </code>
     ,
     <code class="type">
      anycompatiblearray
     </code>
     ) →
     <code class="returnvalue">
      anycompatiblearray
     </code>
    </p>
    <p>
     Concatenates two arrays (same as the
     <code class="type">
      anycompatiblearray
     </code>
     <code class="literal">
      ||
     </code>
     <code class="type">
      anycompatiblearray
     </code>
     operator).
    </p>
    <p>
     <code class="literal">
      array_cat(ARRAY[1,2,3], ARRAY[4,5])
     </code>
     →
     <code class="returnvalue">
      {1,2,3,4,5}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      array_dims
     </code>
     (
     <code class="type">
      anyarray
     </code>
     ) →
     <code class="returnvalue">
      text
     </code>
    </p>
    <p>
     Returns a text representation of the array's dimensions.
    </p>
    <p>
     <code class="literal">
      array_dims(ARRAY[[1,2,3], [4,5,6]])
     </code>
     →
     <code class="returnvalue">
      [1:2][1:3]
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      array_fill
     </code>
     (
     <code class="type">
      anyelement
     </code>
     ,
     <code class="type">
      integer[]
     </code>
     [
     <span class="optional">
      ,
      <code class="type">
       integer[]
      </code>
     </span>
     ] ) →
     <code class="returnvalue">
      anyarray
     </code>
    </p>
    <p>
     Returns an array filled with copies of the given value, having dimensions of the lengths specified by the second argument. The optional third argument supplies lower-bound values for each dimension (which default to all
     <code class="literal">
      1
     </code>
     ).
    </p>
    <p>
     <code class="literal">
      array_fill(11, ARRAY[2,3])
     </code>
     →
     <code class="returnvalue">
      {{11,11,11},{11,11,11}}
     </code>
    </p>
    <p>
     <code class="literal">
      array_fill(7, ARRAY[3], ARRAY[2])
     </code>
     →
     <code class="returnvalue">
      [2:4]={7,7,7}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      array_length
     </code>
     (
     <code class="type">
      anyarray
     </code>
     ,
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Returns the length of the requested array dimension. (Produces NULL instead of 0 for empty or missing array dimensions.)
    </p>
    <p>
     <code class="literal">
      array_length(array[1,2,3], 1)
     </code>
     →
     <code class="returnvalue">
      3
     </code>
    </p>
    <p>
     <code class="literal">
      array_length(array[]::int[], 1)
     </code>
     →
     <code class="returnvalue">
      NULL
     </code>
    </p>
    <p>
     <code class="literal">
      array_length(array['text'], 2)
     </code>
     →
     <code class="returnvalue">
      NULL
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      array_lower
     </code>
     (
     <code class="type">
      anyarray
     </code>
     ,
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Returns the lower bound of the requested array dimension.
    </p>
    <p>
     <code class="literal">
      array_lower('[0:2]={1,2,3}'::integer[], 1)
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
      array_ndims
     </code>
     (
     <code class="type">
      anyarray
     </code>
     ) →
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Returns the number of dimensions of the array.
    </p>
    <p>
     <code class="literal">
      array_ndims(ARRAY[[1,2,3], [4,5,6]])
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
      array_position
     </code>
     (
     <code class="type">
      anycompatiblearray
     </code>
     ,
     <code class="type">
      anycompatible
     </code>
     [
     <span class="optional">
      ,
      <code class="type">
       integer
      </code>
     </span>
     ] ) →
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Returns the subscript of the first occurrence of the second argument in the array, or
     <code class="literal">
      NULL
     </code>
     if it's not present. If the third argument is given, the search begins at that subscript. The array must be one-dimensional. Comparisons are done using
     <code class="literal">
      IS NOT DISTINCT FROM
     </code>
     semantics, so it is possible to search for
     <code class="literal">
      NULL
     </code>
     .
    </p>
    <p>
     <code class="literal">
      array_position(ARRAY['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'], 'mon')
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
      array_positions
     </code>
     (
     <code class="type">
      anycompatiblearray
     </code>
     ,
     <code class="type">
      anycompatible
     </code>
     ) →
     <code class="returnvalue">
      integer[]
     </code>
    </p>
    <p>
     Returns an array of the subscripts of all occurrences of the second argument in the array given as first argument. The array must be one-dimensional. Comparisons are done using
     <code class="literal">
      IS NOT DISTINCT FROM
     </code>
     semantics, so it is possible to search for
     <code class="literal">
      NULL
     </code>
     .
     <code class="literal">
      NULL
     </code>
     is returned only if the array is
     <code class="literal">
      NULL
     </code>
     ; if the value is not found in the array, an empty array is returned.
    </p>
    <p>
     <code class="literal">
      array_positions(ARRAY['A','A','B','A'], 'A')
     </code>
     →
     <code class="returnvalue">
      {1,2,4}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      array_prepend
     </code>
     (
     <code class="type">
      anycompatible
     </code>
     ,
     <code class="type">
      anycompatiblearray
     </code>
     ) →
     <code class="returnvalue">
      anycompatiblearray
     </code>
    </p>
    <p>
     Prepends an element to the beginning of an array (same as the
     <code class="type">
      anycompatible
     </code>
     <code class="literal">
      ||
     </code>
     <code class="type">
      anycompatiblearray
     </code>
     operator).
    </p>
    <p>
     <code class="literal">
      array_prepend(1, ARRAY[2,3])
     </code>
     →
     <code class="returnvalue">
      {1,2,3}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      array_remove
     </code>
     (
     <code class="type">
      anycompatiblearray
     </code>
     ,
     <code class="type">
      anycompatible
     </code>
     ) →
     <code class="returnvalue">
      anycompatiblearray
     </code>
    </p>
    <p>
     Removes all elements equal to the given value from the array. The array must be one-dimensional. Comparisons are done using
     <code class="literal">
      IS NOT DISTINCT FROM
     </code>
     semantics, so it is possible to remove
     <code class="literal">
      NULL
     </code>
     s.
    </p>
    <p>
     <code class="literal">
      array_remove(ARRAY[1,2,3,2], 2)
     </code>
     →
     <code class="returnvalue">
      {1,3}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      array_replace
     </code>
     (
     <code class="type">
      anycompatiblearray
     </code>
     ,
     <code class="type">
      anycompatible
     </code>
     ,
     <code class="type">
      anycompatible
     </code>
     ) →
     <code class="returnvalue">
      anycompatiblearray
     </code>
    </p>
    <p>
     Replaces each array element equal to the second argument with the third argument.
    </p>
    <p>
     <code class="literal">
      array_replace(ARRAY[1,2,5,4], 5, 3)
     </code>
     →
     <code class="returnvalue">
      {1,2,3,4}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      array_reverse
     </code>
     (
     <code class="type">
      anyarray
     </code>
     ) →
     <code class="returnvalue">
      anyarray
     </code>
    </p>
    <p>
     Reverses the first dimension of the array.
    </p>
    <p>
     <code class="literal">
      array_reverse(ARRAY[[1,2],[3,4],[5,6]])
     </code>
     →
     <code class="returnvalue">
      {{5,6},{3,4},{1,2}}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      array_sample
     </code>
     (
     <em class="parameter">
      <code>
       array
      </code>
     </em>
     <code class="type">
      anyarray
     </code>
     ,
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
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
     <code class="literal">
      array_sample(ARRAY[1,2,3,4,5,6], 3)
     </code>
     →
     <code class="returnvalue">
      {2,6,1}
     </code>
    </p>
    <p>
     <code class="literal">
      array_sample(ARRAY[[1,2],[3,4],[5,6]], 2)
     </code>
     →
     <code class="returnvalue">
      {{5,6},{1,2}}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      array_shuffle
     </code>
     (
     <code class="type">
      anyarray
     </code>
     ) →
     <code class="returnvalue">
      anyarray
     </code>
    </p>
    <p>
     Randomly shuffles the first dimension of the array.
    </p>
    <p>
     <code class="literal">
      array_shuffle(ARRAY[[1,2],[3,4],[5,6]])
     </code>
     →
     <code class="returnvalue">
      {{5,6},{1,2},{3,4}}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      array_sort
     </code>
     (
     <em class="parameter">
      <code>
       array
      </code>
     </em>
     <code class="type">
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
      <code class="type">
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
       <code class="type">
        boolean
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code class="returnvalue">
      anyarray
     </code>
    </p>
    <p>
     Sorts the first dimension of the array. The sort order is determined by the default sort ordering of the array's element type; however, if the element type is collatable, the collation to use can be specified by adding a
     <code class="literal">
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
     <code class="literal">
      array_sort(ARRAY[[2,4],[2,1],[6,5]])
     </code>
     →
     <code class="returnvalue">
      {{2,1},{2,4},{6,5}}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      array_to_string
     </code>
     (
     <em class="parameter">
      <code>
       array
      </code>
     </em>
     <code class="type">
      anyarray
     </code>
     ,
     <em class="parameter">
      <code>
       delimiter
      </code>
     </em>
     <code class="type">
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
      <code class="type">
       text
      </code>
     </span>
     ] ) →
     <code class="returnvalue">
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
     <code class="literal">
      NULL
     </code>
     , then
     <code class="literal">
      NULL
     </code>
     array entries are represented by that string; otherwise, they are omitted. See also
     <a class="link" href="functions-string.md#FUNCTION-STRING-TO-ARRAY">
      <code class="function">
       string_to_array
      </code>
     </a>
     .
    </p>
    <p>
     <code class="literal">
      array_to_string(ARRAY[1, 2, 3, NULL, 5], ',', '*')
     </code>
     →
     <code class="returnvalue">
      1,2,3,*,5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      array_upper
     </code>
     (
     <code class="type">
      anyarray
     </code>
     ,
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Returns the upper bound of the requested array dimension.
    </p>
    <p>
     <code class="literal">
      array_upper(ARRAY[1,8,3,7], 1)
     </code>
     →
     <code class="returnvalue">
      4
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      cardinality
     </code>
     (
     <code class="type">
      anyarray
     </code>
     ) →
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Returns the total number of elements in the array, or 0 if the array is empty.
    </p>
    <p>
     <code class="literal">
      cardinality(ARRAY[[1,2],[3,4]])
     </code>
     →
     <code class="returnvalue">
      4
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      trim_array
     </code>
     (
     <em class="parameter">
      <code>
       array
      </code>
     </em>
     <code class="type">
      anyarray
     </code>
     ,
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
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
     <code class="literal">
      trim_array(ARRAY[1,2,3,4,5,6], 2)
     </code>
     →
     <code class="returnvalue">
      {1,2,3,4}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      unnest
     </code>
     (
     <code class="type">
      anyarray
     </code>
     ) →
     <code class="returnvalue">
      setof anyelement
     </code>
    </p>
    <p>
     Expands an array into a set of rows. The array's elements are read out in storage order.
    </p>
    <p>
     <code class="literal">
      unnest(ARRAY[1,2])
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
    <pre class="programlisting">
 1 2
</pre>
    <p>
    </p>
    <p>
     <code class="literal">
      unnest(ARRAY[['foo','bar'],['baz','quux']])
     </code>
     →
     <code class="returnvalue">
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
     <code class="function">
      unnest
     </code>
     (
     <code class="type">
      anyarray
     </code>
     ,
     <code class="type">
      anyarray
     </code>
     [
     <span class="optional">
      , ...
     </span>
     ] ) →
     <code class="returnvalue">
      setof anyelement, anyelement [, ... ]
     </code>
    </p>
    <p>
     Expands multiple arrays (possibly of different data types) into a set of rows.  If the arrays are not all the same length then the shorter ones are padded with
     <code class="literal">
      NULL
     </code>
     s.  This form is only allowed in a query's FROM clause; see
     <a class="xref" href="queries-table-expressions.md#QUERIES-TABLEFUNCTIONS" title="7.2.1.4. Table Functions">
      Section 7.2.1.4
     </a>
     .
    </p>
    <p>
     <code class="literal">
      select * from unnest(ARRAY[1,2], ARRAY['foo','bar','baz']) as x(a,b)
     </code>
     →
     <code class="returnvalue">
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