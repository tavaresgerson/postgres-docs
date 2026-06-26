## 9.21. Funções agregadas [#](#FUNCTIONS-AGGREGATE)

*As funções agregadas* calculam um único resultado a partir de um conjunto de valores de entrada. As funções agregadas de propósito geral integradas estão listadas em [Tabela 9.62](functions-aggregate.md#FUNCTIONS-AGGREGATE-TABLE), enquanto os agregados estatísticos estão em [Tabela 9.63](functions-aggregate.md#FUNCTIONS-AGGREGATE-STATISTICS-TABLE). As funções agregadas de conjunto ordenado dentro do grupo integrado estão listadas em [Tabela 9.64](functions-aggregate.md#FUNCTIONS-ORDEREDSET-TABLE), enquanto as funções agregadas de conjunto hipotético dentro do grupo integrado estão em [Tabela 9.65](functions-aggregate.md#FUNCTIONS-HYPOTHETICAL-TABLE). As operações de agrupamento, que estão intimamente relacionadas com as funções agregadas, estão listadas em [Tabela 9.66](functions-aggregate.md#FUNCTIONS-GROUPING-TABLE). As considerações de sintaxe especial para funções agregadas são explicadas em [Seção 4.2.7](sql-expressions.md#SYNTAX-AGGREGATES). Consulte [Seção 2.7](tutorial-agg.md) para informações adicionais introdutórias.

As funções agregadas que suportam o *Modo Parcial* são elegíveis para participar em várias otimizações, como agregação paralela.

Embora todos os agregados abaixo aceitem uma cláusula opcional `ORDER BY` (conforme descrito em [Seção 4.2.7](sql-expressions.md#SYNTAX-AGGREGATES)), a cláusula foi adicionada apenas aos agregados cuja saída é afetada pela ordenação.

**Tabela 9.62. Funções agregadas de propósito geral**



<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
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
   </th>
   <th>
    Partial Mode
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      any_value
     </code>
     (
     <code>
      anyelement
     </code>
     ) →
     <code>
      <em class="replaceable">
       <code>
        same as input type
       </code>
      </em>
     </code>
    </p>
    <p>
     Returns an arbitrary value from the non-null input values.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_agg
     </code>
     (
     <code>
      anynonarray
     </code>
     <code>
      ORDER BY
     </code>
     <code>
      input_sort_columns
     </code>
     ) →
     <code>
      anyarray
     </code>
    </p>
    <p>
     Collects all the input values, including nulls, into an array.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      array_agg
     </code>
     (
     <code>
      anyarray
     </code>
     <code>
      ORDER BY
     </code>
     <code>
      input_sort_columns
     </code>
     ) →
     <code>
      anyarray
     </code>
    </p>
    <p>
     Concatenates all the input arrays into an array of one higher dimension.  (The inputs must all have the same dimensionality, and cannot be empty or null.)
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      avg
     </code>
     (
     <code>
      smallint
     </code>
     ) →
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      avg
     </code>
     (
     <code>
      integer
     </code>
     ) →
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      avg
     </code>
     (
     <code>
      bigint
     </code>
     ) →
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      avg
     </code>
     (
     <code>
      numeric
     </code>
     ) →
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      avg
     </code>
     (
     <code>
      real
     </code>
     ) →
     <code>
      double precision
     </code>
    </p>
    <p class="func_signature">
     <code>
      avg
     </code>
     (
     <code>
      double precision
     </code>
     ) →
     <code>
      double precision
     </code>
    </p>
    <p class="func_signature">
     <code>
      avg
     </code>
     (
     <code>
      interval
     </code>
     ) →
     <code>
      interval
     </code>
    </p>
    <p>
     Computes the average (arithmetic mean) of all the non-null input values.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      bit_and
     </code>
     (
     <code>
      smallint
     </code>
     ) →
     <code>
      smallint
     </code>
    </p>
    <p class="func_signature">
     <code>
      bit_and
     </code>
     (
     <code>
      integer
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p class="func_signature">
     <code>
      bit_and
     </code>
     (
     <code>
      bigint
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p class="func_signature">
     <code>
      bit_and
     </code>
     (
     <code>
      bit
     </code>
     ) →
     <code>
      bit
     </code>
    </p>
    <p>
     Computes the bitwise AND of all non-null input values.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      bit_or
     </code>
     (
     <code>
      smallint
     </code>
     ) →
     <code>
      smallint
     </code>
    </p>
    <p class="func_signature">
     <code>
      bit_or
     </code>
     (
     <code>
      integer
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p class="func_signature">
     <code>
      bit_or
     </code>
     (
     <code>
      bigint
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p class="func_signature">
     <code>
      bit_or
     </code>
     (
     <code>
      bit
     </code>
     ) →
     <code>
      bit
     </code>
    </p>
    <p>
     Computes the bitwise OR of all non-null input values.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      bit_xor
     </code>
     (
     <code>
      smallint
     </code>
     ) →
     <code>
      smallint
     </code>
    </p>
    <p class="func_signature">
     <code>
      bit_xor
     </code>
     (
     <code>
      integer
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p class="func_signature">
     <code>
      bit_xor
     </code>
     (
     <code>
      bigint
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p class="func_signature">
     <code>
      bit_xor
     </code>
     (
     <code>
      bit
     </code>
     ) →
     <code>
      bit
     </code>
    </p>
    <p>
     Computes the bitwise exclusive OR of all non-null input values. Can be useful as a checksum for an unordered set of values.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      bool_and
     </code>
     (
     <code>
      boolean
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Returns true if all non-null input values are true, otherwise false.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      bool_or
     </code>
     (
     <code>
      boolean
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Returns true if any non-null input value is true, otherwise false.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      count
     </code>
     (
     <code>
      *
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     Computes the number of input rows.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      count
     </code>
     (
     <code>
      "any"
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     Computes the number of input rows in which the input value is not null.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      every
     </code>
     (
     <code>
      boolean
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     This is the SQL standard's equivalent to
     <code>
      bool_and
     </code>
     .
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      json_agg
     </code>
     (
     <code>
      anyelement
     </code>
     <code>
      ORDER BY
     </code>
     <code>
      input_sort_columns
     </code>
     ) →
     <code>
      json
     </code>
    </p>
    <p class="func_signature">
     <code>
      jsonb_agg
     </code>
     (
     <code>
      anyelement
     </code>
     <code>
      ORDER BY
     </code>
     <code>
      input_sort_columns
     </code>
     ) →
     <code>
      jsonb
     </code>
    </p>
    <p>
     Collects all the input values, including nulls, into a JSON array. Values are converted to JSON as per
     <code>
      to_json
     </code>
     or
     <code>
      to_jsonb
     </code>
     .
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      json_agg_strict
     </code>
     (
     <code>
      anyelement
     </code>
     ) →
     <code>
      json
     </code>
    </p>
    <p class="func_signature">
     <code>
      jsonb_agg_strict
     </code>
     (
     <code>
      anyelement
     </code>
     ) →
     <code>
      jsonb
     </code>
    </p>
    <p>
     Collects all the input values, skipping nulls, into a JSON array. Values are converted to JSON as per
     <code>
      to_json
     </code>
     or
     <code>
      to_jsonb
     </code>
     .
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      json_arrayagg
     </code>
     ( [
     <span class="optional">
      <em class="replaceable">
       <code>
        value_expression
       </code>
      </em>
     </span>
     ] [
     <span class="optional">
      <code>
       ORDER BY
      </code>
      <em class="replaceable">
       <code>
        sort_expression
       </code>
      </em>
     </span>
     ] [
     <span class="optional">
      {
      <code>
       NULL
      </code>
      |
      <code>
       ABSENT
      </code>
      }
      <code>
       ON NULL
      </code>
     </span>
     ] [
     <span class="optional">
      <code>
       RETURNING
      </code>
      <em class="replaceable">
       <code>
        data_type
       </code>
      </em>
      [
      <span class="optional">
       <code>
        FORMAT JSON
       </code>
       [
       <span class="optional">
        <code>
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
     Behaves in the same way as
     <code>
      json_array
     </code>
     but as an aggregate function so it only takes one
     <em class="replaceable">
      <code>
       value_expression
      </code>
     </em>
     parameter. If
     <code>
      ABSENT ON NULL
     </code>
     is specified, any NULL values are omitted. If
     <code>
      ORDER BY
     </code>
     is specified, the elements will appear in the array in that order rather than in the input order.
    </p>
    <p>
     <code>
      SELECT json_arrayagg(v) FROM (VALUES(2),(1)) t(v)
     </code>
     →
     <code>
      [2, 1]
     </code>
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      json_objectagg
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
      <code>
       VALUE
      </code>
      | ':' }
      <em class="replaceable">
       <code>
        value_expression
       </code>
      </em>
      }
     </span>
     ] [
     <span class="optional">
      {
      <code>
       NULL
      </code>
      |
      <code>
       ABSENT
      </code>
      }
      <code>
       ON NULL
      </code>
     </span>
     ] [
     <span class="optional">
      {
      <code>
       WITH
      </code>
      |
      <code>
       WITHOUT
      </code>
      }
      <code>
       UNIQUE
      </code>
      [
      <span class="optional">
       <code>
        KEYS
       </code>
      </span>
      ]
     </span>
     ] [
     <span class="optional">
      <code>
       RETURNING
      </code>
      <em class="replaceable">
       <code>
        data_type
       </code>
      </em>
      [
      <span class="optional">
       <code>
        FORMAT JSON
       </code>
       [
       <span class="optional">
        <code>
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
     Behaves like
     <code>
      json_object
     </code>
     , but as an aggregate function, so it only takes one
     <em class="replaceable">
      <code>
       key_expression
      </code>
     </em>
     and one
     <em class="replaceable">
      <code>
       value_expression
      </code>
     </em>
     parameter.
    </p>
    <p>
     <code>
      SELECT json_objectagg(k:v) FROM (VALUES ('a'::text,current_date),('b',current_date + 1)) AS t(k,v)
     </code>
     →
     <code>
      { "a" : "2022-05-10", "b" : "2022-05-11" }
     </code>
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      json_object_agg
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      "any"
     </code>
     ,
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code>
      "any"
     </code>
     <code>
      ORDER BY
     </code>
     <code>
      input_sort_columns
     </code>
     ) →
     <code>
      json
     </code>
    </p>
    <p class="func_signature">
     <code>
      jsonb_object_agg
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      "any"
     </code>
     ,
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code>
      "any"
     </code>
     <code>
      ORDER BY
     </code>
     <code>
      input_sort_columns
     </code>
     ) →
     <code>
      jsonb
     </code>
    </p>
    <p>
     Collects all the key/value pairs into a JSON object.  Key arguments are coerced to text; value arguments are converted as per
     <code>
      to_json
     </code>
     or
     <code>
      to_jsonb
     </code>
     . Values can be null, but keys cannot.
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      json_object_agg_strict
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      "any"
     </code>
     ,
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code>
      "any"
     </code>
     ) →
     <code>
      json
     </code>
    </p>
    <p class="func_signature">
     <code>
      jsonb_object_agg_strict
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      "any"
     </code>
     ,
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code>
      "any"
     </code>
     ) →
     <code>
      jsonb
     </code>
    </p>
    <p>
     Collects all the key/value pairs into a JSON object.  Key arguments are coerced to text; value arguments are converted as per
     <code>
      to_json
     </code>
     or
     <code>
      to_jsonb
     </code>
     . The
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     can not be null. If the
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     is null then the entry is skipped,
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      json_object_agg_unique
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      "any"
     </code>
     ,
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code>
      "any"
     </code>
     ) →
     <code>
      json
     </code>
    </p>
    <p class="func_signature">
     <code>
      jsonb_object_agg_unique
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      "any"
     </code>
     ,
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code>
      "any"
     </code>
     ) →
     <code>
      jsonb
     </code>
    </p>
    <p>
     Collects all the key/value pairs into a JSON object.  Key arguments are coerced to text; value arguments are converted as per
     <code>
      to_json
     </code>
     or
     <code>
      to_jsonb
     </code>
     . Values can be null, but keys cannot. If there is a duplicate key an error is thrown.
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      json_object_agg_unique_strict
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      "any"
     </code>
     ,
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code>
      "any"
     </code>
     ) →
     <code>
      json
     </code>
    </p>
    <p class="func_signature">
     <code>
      jsonb_object_agg_unique_strict
     </code>
     (
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     <code>
      "any"
     </code>
     ,
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code>
      "any"
     </code>
     ) →
     <code>
      jsonb
     </code>
    </p>
    <p>
     Collects all the key/value pairs into a JSON object.  Key arguments are coerced to text; value arguments are converted as per
     <code>
      to_json
     </code>
     or
     <code>
      to_jsonb
     </code>
     . The
     <em class="parameter">
      <code>
       key
      </code>
     </em>
     can not be null. If the
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     is null then the entry is skipped. If there is a duplicate key an error is thrown.
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      max
     </code>
     (
     <em class="replaceable">
      <code>
       see text
      </code>
     </em>
     ) →
     <code>
      <em class="replaceable">
       <code>
        same as input type
       </code>
      </em>
     </code>
    </p>
    <p>
     Computes the maximum of the non-null input values.  Available for any numeric, string, date/time, or enum type, as well as
     <code>
      bytea
     </code>
     ,
     <code>
      inet
     </code>
     ,
     <code>
      interval
     </code>
     ,
     <code>
      money
     </code>
     ,
     <code>
      oid
     </code>
     ,
     <code>
      pg_lsn
     </code>
     ,
     <code>
      tid
     </code>
     ,
     <code>
      xid8
     </code>
     , and also arrays and composite types containing sortable data types.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      min
     </code>
     (
     <em class="replaceable">
      <code>
       see text
      </code>
     </em>
     ) →
     <code>
      <em class="replaceable">
       <code>
        same as input type
       </code>
      </em>
     </code>
    </p>
    <p>
     Computes the minimum of the non-null input values.  Available for any numeric, string, date/time, or enum type, as well as
     <code>
      bytea
     </code>
     ,
     <code>
      inet
     </code>
     ,
     <code>
      interval
     </code>
     ,
     <code>
      money
     </code>
     ,
     <code>
      oid
     </code>
     ,
     <code>
      pg_lsn
     </code>
     ,
     <code>
      tid
     </code>
     ,
     <code>
      xid8
     </code>
     , and also arrays and composite types containing sortable data types.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      range_agg
     </code>
     (
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code>
      anyrange
     </code>
     ) →
     <code>
      anymultirange
     </code>
    </p>
    <p class="func_signature">
     <code>
      range_agg
     </code>
     (
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code>
      anymultirange
     </code>
     ) →
     <code>
      anymultirange
     </code>
    </p>
    <p>
     Computes the union of the non-null input values.
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      range_intersect_agg
     </code>
     (
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code>
      anyrange
     </code>
     ) →
     <code>
      anyrange
     </code>
    </p>
    <p class="func_signature">
     <code>
      range_intersect_agg
     </code>
     (
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code>
      anymultirange
     </code>
     ) →
     <code>
      anymultirange
     </code>
    </p>
    <p>
     Computes the intersection of the non-null input values.
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      string_agg
     </code>
     (
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code>
      text
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
     ) →
     <code>
      text
     </code>
    </p>
    <p class="func_signature">
     <code>
      string_agg
     </code>
     (
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code>
      bytea
     </code>
     ,
     <em class="parameter">
      <code>
       delimiter
      </code>
     </em>
     <code>
      bytea
     </code>
     <code>
      ORDER BY
     </code>
     <code>
      input_sort_columns
     </code>
     ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Concatenates the non-null input values into a string.  Each value after the first is preceded by the corresponding
     <em class="parameter">
      <code>
       delimiter
      </code>
     </em>
     (if it's not null).
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sum
     </code>
     (
     <code>
      smallint
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p class="func_signature">
     <code>
      sum
     </code>
     (
     <code>
      integer
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p class="func_signature">
     <code>
      sum
     </code>
     (
     <code>
      bigint
     </code>
     ) →
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      sum
     </code>
     (
     <code>
      numeric
     </code>
     ) →
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      sum
     </code>
     (
     <code>
      real
     </code>
     ) →
     <code>
      real
     </code>
    </p>
    <p class="func_signature">
     <code>
      sum
     </code>
     (
     <code>
      double precision
     </code>
     ) →
     <code>
      double precision
     </code>
    </p>
    <p class="func_signature">
     <code>
      sum
     </code>
     (
     <code>
      interval
     </code>
     ) →
     <code>
      interval
     </code>
    </p>
    <p class="func_signature">
     <code>
      sum
     </code>
     (
     <code>
      money
     </code>
     ) →
     <code>
      money
     </code>
    </p>
    <p>
     Computes the sum of the non-null input values.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      xmlagg
     </code>
     (
     <code>
      xml
     </code>
     <code>
      ORDER BY
     </code>
     <code>
      input_sort_columns
     </code>
     ) →
     <code>
      xml
     </code>
    </p>
    <p>
     Concatenates the non-null XML input values (see
     <a class="xref" href="functions-xml.md#FUNCTIONS-XML-XMLAGG" title="9.15.1.8. xmlagg">
      Section 9.15.1.8
     </a>
     ).
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
 </tbody>
</table>










Deve-se notar que, exceto para `count`, essas funções retornam um valor nulo quando nenhuma linha é selecionada. Em particular, `sum` sem nenhuma linha retorna nulo, não zero como se poderia esperar, e `array_agg` retorna nulo em vez de um array vazio quando não há linhas de entrada. A função `coalesce` pode ser usada para substituir zero ou um array vazio por nulo quando necessário.

As funções agregadas `array_agg`, `json_agg`, `jsonb_agg`, `json_agg_strict`, `jsonb_agg_strict`, `json_object_agg`, `jsonb_object_agg`, `json_object_agg_strict`, `jsonb_object_agg_strict`, `json_object_agg_unique`, `jsonb_object_agg_unique`, `json_object_agg_unique_strict`, `jsonb_object_agg_unique_strict`, `string_agg` e `xmlagg`, bem como funções agregadas definidas pelo usuário semelhantes, produzem valores de resultado significativamente diferentes, dependendo da ordem dos valores de entrada. Essa ordem não é especificada por padrão, mas pode ser controlada escrevendo uma cláusula `ORDER BY` dentro da chamada agregada, conforme mostrado em [Seção 4.2.7](sql-expressions.md#SYNTAX-AGGREGATES). Alternativamente, fornecer os valores de entrada de uma subconsulta ordenada geralmente funciona. Por exemplo:

```
SELECT xmlagg(x) FROM (SELECT x FROM test ORDER BY y DESC) AS tab;
```

Cuidado, pois essa abordagem pode falhar se o nível da consulta externa contiver processamento adicional, como uma junção, porque isso pode fazer com que a saída da subconsulta seja reordenada antes de o agregado ser calculado.

Nota

Os agregados booleanos `bool_and` e `bool_or` correspondem aos agregados padrão SQL `every` e `any` ou `some`. O PostgreSQL suporta `every`, mas não `any` ou `some`, porque há uma ambiguidade embutida na sintaxe padrão:

```
SELECT b1 = ANY((SELECT b2 FROM t2 ...)) FROM t1 ...;
```

Aqui `ANY` pode ser considerado como introduzindo uma subconsulta, ou como sendo uma função agregada, se a subconsulta retornar uma única linha com um valor booleano. Assim, o nome padrão não pode ser dado a esses agregados.

Nota

Os usuários acostumados a trabalhar com outros sistemas de gerenciamento de banco de dados SQL podem ficar desapontados com o desempenho do agregado `count` quando aplicado a toda a tabela. Uma consulta como:

```
SELECT count(*) FROM sometable;
```

requerirá um esforço proporcional ao tamanho da tabela: o PostgreSQL precisará analisar toda a tabela ou a totalidade de um índice que inclua todas as linhas da tabela.

[Tabela 9.63](functions-aggregate.md#FUNCTIONS-AGGREGATE-STATISTICS-TABLE "Table 9.63. Aggregate Functions for Statistics") mostra funções agregadas tipicamente usadas na análise estatística. (Essas são separadas apenas para evitar a sobrecarga na lista de agregados mais comumente usados.) As funções mostradas como aceitando *`numeric_type`* estão disponíveis para todos os tipos `smallint`, `integer`, `bigint`, `numeric`, `real` e `double precision`. Onde a descrição menciona *`N`*, isso significa que o número de linhas de entrada para as quais todas as expressões de entrada são não nulos. Em todos os casos, o nulo é retornado se a computação não tiver significado, por exemplo, quando *`N`* é zero.

**Tabela 9.63. Funções agregadas para estatísticas**



<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
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
   </th>
   <th>
    Partial Mode
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      corr
     </code>
     (
     <em class="parameter">
      <code>
       Y
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       X
      </code>
     </em>
     <code>
      double precision
     </code>
     ) →
     <code>
      double precision
     </code>
    </p>
    <p>
     Computes the correlation coefficient.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      covar_pop
     </code>
     (
     <em class="parameter">
      <code>
       Y
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       X
      </code>
     </em>
     <code>
      double precision
     </code>
     ) →
     <code>
      double precision
     </code>
    </p>
    <p>
     Computes the population covariance.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      covar_samp
     </code>
     (
     <em class="parameter">
      <code>
       Y
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       X
      </code>
     </em>
     <code>
      double precision
     </code>
     ) →
     <code>
      double precision
     </code>
    </p>
    <p>
     Computes the sample covariance.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      regr_avgx
     </code>
     (
     <em class="parameter">
      <code>
       Y
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       X
      </code>
     </em>
     <code>
      double precision
     </code>
     ) →
     <code>
      double precision
     </code>
    </p>
    <p>
     Computes the average of the independent variable,
     <code>
      sum(
      <em class="parameter">
       <code>
        X
       </code>
      </em>
      )/
      <em class="parameter">
       <code>
        N
       </code>
      </em>
     </code>
     .
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      regr_avgy
     </code>
     (
     <em class="parameter">
      <code>
       Y
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       X
      </code>
     </em>
     <code>
      double precision
     </code>
     ) →
     <code>
      double precision
     </code>
    </p>
    <p>
     Computes the average of the dependent variable,
     <code>
      sum(
      <em class="parameter">
       <code>
        Y
       </code>
      </em>
      )/
      <em class="parameter">
       <code>
        N
       </code>
      </em>
     </code>
     .
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      regr_count
     </code>
     (
     <em class="parameter">
      <code>
       Y
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       X
      </code>
     </em>
     <code>
      double precision
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     Computes the number of rows in which both inputs are non-null.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      regr_intercept
     </code>
     (
     <em class="parameter">
      <code>
       Y
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       X
      </code>
     </em>
     <code>
      double precision
     </code>
     ) →
     <code>
      double precision
     </code>
    </p>
    <p>
     Computes the y-intercept of the least-squares-fit linear equation determined by the (
     <em class="parameter">
      <code>
       X
      </code>
     </em>
     ,
     <em class="parameter">
      <code>
       Y
      </code>
     </em>
     ) pairs.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      regr_r2
     </code>
     (
     <em class="parameter">
      <code>
       Y
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       X
      </code>
     </em>
     <code>
      double precision
     </code>
     ) →
     <code>
      double precision
     </code>
    </p>
    <p>
     Computes the square of the correlation coefficient.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      regr_slope
     </code>
     (
     <em class="parameter">
      <code>
       Y
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       X
      </code>
     </em>
     <code>
      double precision
     </code>
     ) →
     <code>
      double precision
     </code>
    </p>
    <p>
     Computes the slope of the least-squares-fit linear equation determined by the (
     <em class="parameter">
      <code>
       X
      </code>
     </em>
     ,
     <em class="parameter">
      <code>
       Y
      </code>
     </em>
     ) pairs.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      regr_sxx
     </code>
     (
     <em class="parameter">
      <code>
       Y
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       X
      </code>
     </em>
     <code>
      double precision
     </code>
     ) →
     <code>
      double precision
     </code>
    </p>
    <p>
     Computes the
     <span class="quote">
      “
      <span class="quote">
       sum of squares
      </span>
      ”
     </span>
     of the independent variable,
     <code>
      sum(
      <em class="parameter">
       <code>
        X
       </code>
      </em>
      ^2) - sum(
      <em class="parameter">
       <code>
        X
       </code>
      </em>
      )^2/
      <em class="parameter">
       <code>
        N
       </code>
      </em>
     </code>
     .
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      regr_sxy
     </code>
     (
     <em class="parameter">
      <code>
       Y
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       X
      </code>
     </em>
     <code>
      double precision
     </code>
     ) →
     <code>
      double precision
     </code>
    </p>
    <p>
     Computes the
     <span class="quote">
      “
      <span class="quote">
       sum of products
      </span>
      ”
     </span>
     of independent times dependent variables,
     <code>
      sum(
      <em class="parameter">
       <code>
        X
       </code>
      </em>
      *
      <em class="parameter">
       <code>
        Y
       </code>
      </em>
      ) - sum(
      <em class="parameter">
       <code>
        X
       </code>
      </em>
      ) * sum(
      <em class="parameter">
       <code>
        Y
       </code>
      </em>
      )/
      <em class="parameter">
       <code>
        N
       </code>
      </em>
     </code>
     .
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      regr_syy
     </code>
     (
     <em class="parameter">
      <code>
       Y
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       X
      </code>
     </em>
     <code>
      double precision
     </code>
     ) →
     <code>
      double precision
     </code>
    </p>
    <p>
     Computes the
     <span class="quote">
      “
      <span class="quote">
       sum of squares
      </span>
      ”
     </span>
     of the dependent variable,
     <code>
      sum(
      <em class="parameter">
       <code>
        Y
       </code>
      </em>
      ^2) - sum(
      <em class="parameter">
       <code>
        Y
       </code>
      </em>
      )^2/
      <em class="parameter">
       <code>
        N
       </code>
      </em>
     </code>
     .
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      stddev
     </code>
     (
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     ) →
     <code>
     </code>
     <code>
      double precision
     </code>
     for
     <code>
      real
     </code>
     or
     <code>
      double precision
     </code>
     , otherwise
     <code>
      numeric
     </code>
    </p>
    <p>
     This is a historical alias for
     <code>
      stddev_samp
     </code>
     .
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      stddev_pop
     </code>
     (
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     ) →
     <code>
     </code>
     <code>
      double precision
     </code>
     for
     <code>
      real
     </code>
     or
     <code>
      double precision
     </code>
     , otherwise
     <code>
      numeric
     </code>
    </p>
    <p>
     Computes the population standard deviation of the input values.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      stddev_samp
     </code>
     (
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     ) →
     <code>
     </code>
     <code>
      double precision
     </code>
     for
     <code>
      real
     </code>
     or
     <code>
      double precision
     </code>
     , otherwise
     <code>
      numeric
     </code>
    </p>
    <p>
     Computes the sample standard deviation of the input values.
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      variance
     </code>
     (
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     ) →
     <code>
     </code>
     <code>
      double precision
     </code>
     for
     <code>
      real
     </code>
     or
     <code>
      double precision
     </code>
     , otherwise
     <code>
      numeric
     </code>
    </p>
    <p>
     This is a historical alias for
     <code>
      var_samp
     </code>
     .
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      var_pop
     </code>
     (
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     ) →
     <code>
     </code>
     <code>
      double precision
     </code>
     for
     <code>
      real
     </code>
     or
     <code>
      double precision
     </code>
     , otherwise
     <code>
      numeric
     </code>
    </p>
    <p>
     Computes the population variance of the input values (square of the population standard deviation).
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      var_samp
     </code>
     (
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     ) →
     <code>
     </code>
     <code>
      double precision
     </code>
     for
     <code>
      real
     </code>
     or
     <code>
      double precision
     </code>
     , otherwise
     <code>
      numeric
     </code>
    </p>
    <p>
     Computes the sample variance of the input values (square of the sample standard deviation).
    </p>
   </td>
   <td>
    Yes
   </td>
  </tr>
 </tbody>
</table>










[Tabela 9.64](functions-aggregate.md#FUNCTIONS-ORDEREDSET-TABLE) mostra algumas funções agregadas que utilizam a sintaxe de *conjunto ordenado* agregada. Essas funções são, por vezes, referidas como funções de “distribuição inversa”. A entrada agregada é introduzida por `ORDER BY`, e elas também podem receber um *argumento direto* que não é agregado, mas é calculado apenas uma vez. Todas essas funções ignoram valores nulos na sua entrada agregada. Para aquelas que recebem um *`fraction`* parâmetro, o valor da fração deve estar entre 0 e 1; uma exceção é lançada se não estiver. No entanto, um valor nulo de *`fraction`* simplesmente produz um resultado nulo.

**Tabela 9.64. Funções agregadas de conjunto ordenado**



<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função
    </p>
    <p>
     Descrição
    </p>
   </th>
   <th>
    Partial Mode
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      mode
     </code>
     ()
     <code>
      WITHIN GROUP
     </code>
     (
     <code>
      ORDER BY
     </code>
     <code>
      anyelement
     </code>
     )
     <code>
      anyelement
     </code>
    </p>
    <p>
     Calcula o
     <em class="firstterm">
      modo
     </em>
     , o valor mais frequente do argumento agregado (escolhendo arbitrariamente o primeiro se houver vários valores igualmente frequentes). O argumento agregado deve ser de um tipo ordenável.
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      percentile_cont
     </code>
     (
     <em class="parameter">
      <code>
       fraction
      </code>
     </em>
     <code>
      double precision
     </code>
     )
     <code>
      WITHIN GROUP
     </code>
     (
     <code>
      ORDER BY
     </code>
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p class="func_signature">
     <code>
      percentile_cont
     </code>
     (
     <em class="parameter">
      <code>
       fraction
      </code>
     </em>
     <code>
      double precision
     </code>
     )
     <code>
      WITHIN GROUP
     </code>
     (
     <code>
      ORDER BY
     </code>
     <code>
      interval
     </code>
     )
     <code>
      interval
     </code>
    </p>
    <p>
     Calcula o
     <em class="firstterm">
      percentil contínuo
     </em>
     , um valor correspondente ao especificado
     <em class="parameter">
      <code>
       fraction
      </code>
     </em>
     dentro do conjunto ordenado de valores de argumento agregados. Isso irá interpolar entre itens de entrada adjacentes, se necessário.
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      percentile_cont
     </code>
     (
     <em class="parameter">
      <code>
       fractions
      </code>
     </em>
     <code>
      double precision[]
     </code>
     )
     <code>
      WITHIN GROUP
     </code>
     (
     <code>
      ORDER BY
     </code>
     <code>
      double precision
     </code>
     )
     <code>
      double precision[]
     </code>
    </p>
    <p class="func_signature">
     <code>
      percentile_cont
     </code>
     (
     <em class="parameter">
      <code>
       fractions
      </code>
     </em>
     <code>
      double precision[]
     </code>
     )
     <code>
      WITHIN GROUP
     </code>
     (
     <code>
      ORDER BY
     </code>
     <code>
      interval
     </code>
     )
     <code>
      interval[]
     </code>
    </p>
    <p>
     Calcula múltiplos percentis contínuos. O resultado é um array com as mesmas dimensões que o original.
     <em class="parameter">
      <code>
       fractions
      </code>
     </em>
     parâmetro, com cada elemento não nulo substituído pelo valor correspondente a esse percentil (possivelmente interpolado).
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      percentile_disc
     </code>
     (
     <em class="parameter">
      <code>
       fraction
      </code>
     </em>
     <code>
      double precision
     </code>
     )
     <code>
      WITHIN GROUP
     </code>
     (
     <code>
      ORDER BY
     </code>
     <code>
      anyelement
     </code>
     )
     <code>
      anyelement
     </code>
    </p>
    <p>
     Calcula o
     <em class="firstterm">
      percentil discreto
     </em>
     , o primeiro valor dentro do conjunto ordenado de valores de argumento agregados cuja posição na ordenação é igual ou superior ao especificado
     <em class="parameter">
      <code>
       fraction
      </code>
     </em>
     O argumento agregado deve ser de um tipo ordenável.
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      percentile_disc
     </code>
     (
     <em class="parameter">
      <code>
       fractions
      </code>
     </em>
     <code>
      double precision[]
     </code>
     )
     <code>
      WITHIN GROUP
     </code>
     (
     <code>
      ORDER BY
     </code>
     <code>
      anyelement
     </code>
     )
     <code>
      anyarray
     </code>
    </p>
    <p>
     Calcula múltiplos percentis discretos. O resultado é um array com as mesmas dimensões que o dado original.
     <em class="parameter">
      <code>
       fractions
      </code>
     </em>
     parâmetro, com cada elemento não nulo substituído pelo valor de entrada correspondente a esse percentil. O argumento agregado deve ser de um tipo ordenável.
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
 </tbody>
</table>










Cada um dos agregados do "conjunto hipotético" listados em [Tabela 9.65](functions-aggregate.md#FUNCTIONS-HYPOTHETICAL-TABLE) está associado a uma função de janela com o mesmo nome definida em [Seção 9.22](functions-window.md). Em cada caso, o resultado do agregado é o valor que a função de janela associada teria retornado para a linha "hipotética" construída a partir de *`args`*, se tal linha tivesse sido adicionada ao grupo de filas ordenadas representado por *`sorted_args`*. Para cada uma dessas funções, a lista de argumentos diretos dada em *`args`* deve corresponder ao número e aos tipos dos argumentos agregados dados em *`sorted_args`*. Ao contrário da maioria dos agregados embutidos, esses agregados não são estritos, ou seja, não descartam filas de entrada que contenham nulos. Os valores nulos são ordenados de acordo com a regra especificada na cláusula `ORDER BY`.

**Tabela 9.65. Funções agregadas de conjunto hipotéticas**



<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
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
   </th>
   <th>
    Partial Mode
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      rank
     </code>
     (
     <em class="replaceable">
      <code>
       args
      </code>
     </em>
     )
     <code>
      WITHIN GROUP
     </code>
     (
     <code>
      ORDER BY
     </code>
     <em class="replaceable">
      <code>
       sorted_args
      </code>
     </em>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     Computes the rank of the hypothetical row, with gaps; that is, the row number of the first row in its peer group.
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      dense_rank
     </code>
     (
     <em class="replaceable">
      <code>
       args
      </code>
     </em>
     )
     <code>
      WITHIN GROUP
     </code>
     (
     <code>
      ORDER BY
     </code>
     <em class="replaceable">
      <code>
       sorted_args
      </code>
     </em>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     Computes the rank of the hypothetical row, without gaps; this function effectively counts peer groups.
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      percent_rank
     </code>
     (
     <em class="replaceable">
      <code>
       args
      </code>
     </em>
     )
     <code>
      WITHIN GROUP
     </code>
     (
     <code>
      ORDER BY
     </code>
     <em class="replaceable">
      <code>
       sorted_args
      </code>
     </em>
     ) →
     <code>
      double precision
     </code>
    </p>
    <p>
     Computes the relative rank of the hypothetical row, that is (
     <code>
      rank
     </code>
     - 1) / (total rows - 1). The value thus ranges from 0 to 1 inclusive.
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cume_dist
     </code>
     (
     <em class="replaceable">
      <code>
       args
      </code>
     </em>
     )
     <code>
      WITHIN GROUP
     </code>
     (
     <code>
      ORDER BY
     </code>
     <em class="replaceable">
      <code>
       sorted_args
      </code>
     </em>
     ) →
     <code>
      double precision
     </code>
    </p>
    <p>
     Computes the cumulative distribution, that is (number of rows preceding or peers with hypothetical row) / (total rows).  The value thus ranges from 1/
     <em class="parameter">
      <code>
       N
      </code>
     </em>
     to 1.
    </p>
   </td>
   <td>
    No
   </td>
  </tr>
 </tbody>
</table>










**Tabela 9.66. Operações de Grupos**



<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função
    </p>
    <p>
     Descrição
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      GROUPING
     </code>
     (
     <em class="replaceable">
      <code>
       group_by_expression(s)
      </code>
     </em>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna uma máscara de bits que indica quais
     <code>
      GROUP BY
     </code>
     As expressões não estão incluídas no conjunto atual de agrupamento. Os bits são atribuídos com o argumento mais à direita correspondente ao bit menos significativo; cada bit é 0 se a expressão correspondente estiver incluída nos critérios de agrupamento do conjunto de agrupamento que gera a linha de resultado atual, e 1 se não estiver incluída.
    </p>
   </td>
  </tr>
 </tbody>
</table>










As operações de agrupamento mostradas na [Tabela 9.66](functions-aggregate.md#FUNCTIONS-GROUPING-TABLE) são usadas em conjunto com conjuntos de agrupamento (veja [Seção 7.2.4](queries-table-expressions.md#QUERIES-GROUPING-SETS)) para distinguir as linhas de resultado. Os argumentos da função `GROUPING` não são realmente avaliados, mas devem corresponder exatamente às expressões fornecidas na cláusula `GROUP BY` do nível de consulta associado. Por exemplo:

```
=> SELECT * FROM items_sold;
 make  | model | sales
-------+-------+-------
 Foo   | GT    |  10
 Foo   | Tour  |  20
 Bar   | City  |  15
 Bar   | Sport |  5
(4 rows)

=> SELECT make, model, GROUPING(make,model), sum(sales) FROM items_sold GROUP BY ROLLUP(make,model);
 make  | model | grouping | sum
-------+-------+----------+-----
 Foo   | GT    |        0 | 10
 Foo   | Tour  |        0 | 20
 Bar   | City  |        0 | 15
 Bar   | Sport |        0 | 5
 Foo   |       |        1 | 30
 Bar   |       |        1 | 20
       |       |        3 | 50
(7 rows)
```

Aqui, o valor `grouping` `0` nas quatro primeiras linhas mostra que esses foram agrupados normalmente, em ambas as colunas de agrupamento. O valor `1` indica que `model` não foi agrupado na última duas linhas, e o valor `3` indica que nem `make` nem `model` foi agrupado na última linha (que, portanto, é um agregado sobre todas as linhas de entrada).