## 53.29. `pg_stats` [#](#VIEW-PG-STATS)

A vista `pg_stats` fornece acesso às informações armazenadas no catálogo [`pg_statistic`](catalog-pg-statistic.md "52.51. pg_statistic"). Esta vista permite acesso apenas a linhas de [`pg_statistic`](catalog-pg-statistic.md "52.51. pg_statistic") que correspondem a tabelas para as quais o usuário tem permissão para leitura, e, portanto, é seguro permitir acesso público de leitura a esta vista.

`pg_stats` também é projetado para apresentar as informações em um formato mais legível do que o catálogo subjacente — ao custo de que seu esquema deve ser estendido sempre que novos tipos de slots são definidos para `pg_statistic`(catalog-pg-statistic.md "52.51. pg_statistic").

**Tabela 53.29. Colunas `pg_stats`**



<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="catalog_table_entry">
    <p class="column_definition">
     Column Type
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      schemaname
     </code>
     <code>
      name
     </code>
     (references
     <a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
      <code>
       pg_namespace
      </code>
     </a>
     .
     <code>
      nspname
     </code>
     )
    </p>
    <p>
     Name of schema containing table
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tablename
     </code>
     <code>
      name
     </code>
     (references
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code>
       pg_class
      </code>
     </a>
     .
     <code>
      relname
     </code>
     )
    </p>
    <p>
     Name of table
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attname
     </code>
     <code>
      name
     </code>
     (references
     <a class="link" href="catalog-pg-attribute.md" title="52.7. pg_attribute">
      <code>
       pg_attribute
      </code>
     </a>
     .
     <code>
      attname
     </code>
     )
    </p>
    <p>
     Name of column described by this row
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      inherited
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     If true, this row includes values from child tables, not just the values in the specified table
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      null_frac
     </code>
     <code>
      float4
     </code>
    </p>
    <p>
     Fraction of column entries that are null
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      avg_width
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Average width in bytes of column's entries
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      n_distinct
     </code>
     <code>
      float4
     </code>
    </p>
    <p>
     If greater than zero, the estimated number of distinct values in the column.  If less than zero, the negative of the number of distinct values divided by the number of rows.  (The negated form is used when
     <code>
      ANALYZE
     </code>
     believes that the number of distinct values is likely to increase as the table grows; the positive form is used when the column seems to have a fixed number of possible values.)  For example, -1 indicates a unique column in which the number of distinct values is the same as the number of rows.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      most_common_vals
     </code>
     <code>
      anyarray
     </code>
    </p>
    <p>
     A list of the most common values in the column. (Null if no values seem to be more common than any others.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      most_common_freqs
     </code>
     <code>
      float4[]
     </code>
    </p>
    <p>
     A list of the frequencies of the most common values, i.e., number of occurrences of each divided by total number of rows. (Null when
     <code>
      most_common_vals
     </code>
     is.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      histogram_bounds
     </code>
     <code>
      anyarray
     </code>
    </p>
    <p>
     A list of values that divide the column's values into groups of approximately equal population.  The values in
     <code>
      most_common_vals
     </code>
     , if present, are omitted from this histogram calculation.  (This column is null if the column data type does not have a
     <code>
      &lt;
     </code>
     operator or if the
     <code>
      most_common_vals
     </code>
     list accounts for the entire population.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      correlation
     </code>
     <code>
      float4
     </code>
    </p>
    <p>
     Statistical correlation between physical row ordering and logical ordering of the column values.  This ranges from -1 to +1. When the value is near -1 or +1, an index scan on the column will be estimated to be cheaper than when it is near zero, due to reduction of random access to the disk.  (This column is null if the column data type does not have a
     <code>
      &lt;
     </code>
     operator.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      most_common_elems
     </code>
     <code>
      anyarray
     </code>
    </p>
    <p>
     A list of non-null element values most often appearing within values of the column. (Null for scalar types.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      most_common_elem_freqs
     </code>
     <code>
      float4[]
     </code>
    </p>
    <p>
     A list of the frequencies of the most common element values, i.e., the fraction of rows containing at least one instance of the given value. Two or three additional values follow the per-element frequencies; these are the minimum and maximum of the preceding per-element frequencies, and optionally the frequency of null elements. (Null when
     <code>
      most_common_elems
     </code>
     is.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      elem_count_histogram
     </code>
     <code>
      float4[]
     </code>
    </p>
    <p>
     A histogram of the counts of distinct non-null element values within the values of the column, followed by the average number of distinct non-null elements.  (Null for scalar types.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      range_length_histogram
     </code>
     <code>
      anyarray
     </code>
    </p>
    <p>
     A histogram of the lengths of non-empty and non-null range values of a range type column. (Null for non-range types.)
    </p>
    <p>
     This histogram is calculated using the
     <code>
      subtype_diff
     </code>
     range function regardless of whether range bounds are inclusive.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      range_empty_frac
     </code>
     <code>
      float4
     </code>
    </p>
    <p>
     Fraction of column entries whose values are empty ranges. (Null for non-range types.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      range_bounds_histogram
     </code>
     <code>
      anyarray
     </code>
    </p>
    <p>
     A histogram of lower and upper bounds of non-empty and non-null range values. (Null for non-range types.)
    </p>
    <p>
     These two histograms are represented as a single array of ranges, whose lower bounds represent the histogram of lower bounds, and upper bounds represent the histogram of upper bounds.
    </p>
   </td>
  </tr>
 </tbody>
</table>










O número máximo de entradas nos campos da matriz pode ser controlado de forma coluna por coluna usando o comando `ALTER TABLE SET STATISTICS`(sql-altertable.md "ALTER TABLE") ou globalmente, definindo o parâmetro de tempo de execução [default_statistics_target](runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET).