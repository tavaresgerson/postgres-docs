## 53.31. `pg_stats_ext_exprs` [#](#VIEW-PG-STATS-EXT-EXPRS)

A vista `pg_stats_ext_exprs` fornece acesso a informações sobre todas as expressões incluídas em objetos de estatísticas extensas, combinando informações armazenadas nos catálogos `pg_statistic_ext`(catalog-pg-statistic-ext.md "52.52. pg_statistic_ext") e `pg_statistic_ext_data`(catalog-pg-statistic-ext-data.md "52.53. pg_statistic_ext_data"). Esta vista permite acesso apenas a linhas de `pg_statistic_ext`(catalog-pg-statistic-ext.md "52.52. pg_statistic_ext") e `pg_statistic_ext_data`(catalog-pg-statistic-ext-data.md "52.53. pg_statistic_ext_data") que correspondem a tabelas que o usuário possui, e, portanto, é seguro permitir acesso de leitura público a esta vista.

`pg_stats_ext_exprs` também é projetado para apresentar as informações em um formato mais legível do que os catálogos subjacentes — ao custo de que seu esquema deve ser estendido sempre que a estrutura das estatísticas em `pg_statistic_ext` muda.

**Tabela 53.31. Colunas `pg_stats_ext_exprs`**



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
     Name of table the statistics object is defined on
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      statistics_schemaname
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
     Name of schema containing extended statistics object
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      statistics_name
     </code>
     <code>
      name
     </code>
     (references
     <a class="link" href="catalog-pg-statistic-ext.md" title="52.52. pg_statistic_ext">
      <code>
       pg_statistic_ext
      </code>
     </a>
     .
     <code>
      stxname
     </code>
     )
    </p>
    <p>
     Name of extended statistics object
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      statistics_owner
     </code>
     <code>
      name
     </code>
     (references
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code>
       pg_authid
      </code>
     </a>
     .
     <code>
      rolname
     </code>
     )
    </p>
    <p>
     Owner of the extended statistics object
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      expr
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Expression included in the extended statistics object
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
     (references
     <a class="link" href="catalog-pg-statistic-ext-data.md" title="52.53. pg_statistic_ext_data">
      <code>
       pg_statistic_ext_data
      </code>
     </a>
     .
     <code>
      stxdinherit
     </code>
     )
    </p>
    <p>
     If true, the stats include values from child tables, not just the values in the specified relation
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
     Fraction of expression entries that are null
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
     Average width in bytes of expression's entries
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
     If greater than zero, the estimated number of distinct values in the expression.  If less than zero, the negative of the number of distinct values divided by the number of rows.  (The negated form is used when
     <code>
      ANALYZE
     </code>
     believes that the number of distinct values is likely to increase as the table grows; the positive form is used when the expression seems to have a fixed number of possible values.)  For example, -1 indicates a unique expression in which the number of distinct values is the same as the number of rows.
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
     A list of the most common values in the expression. (Null if no values seem to be more common than any others.)
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
     A list of values that divide the expression's values into groups of approximately equal population.  The values in
     <code>
      most_common_vals
     </code>
     , if present, are omitted from this histogram calculation.  (This expression is null if the expression data type does not have a
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
     Statistical correlation between physical row ordering and logical ordering of the expression values.  This ranges from -1 to +1. When the value is near -1 or +1, an index scan on the expression will be estimated to be cheaper than when it is near zero, due to reduction of random access to the disk.  (This expression is null if the expression's data type does not have a
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
     A list of non-null element values most often appearing within values of the expression. (Null for scalar types.)
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
     A histogram of the counts of distinct non-null element values within the values of the expression, followed by the average number of distinct non-null elements.  (Null for scalar types.)
    </p>
   </td>
  </tr>
 </tbody>
</table>










O número máximo de entradas nos campos da matriz pode ser controlado de forma coluna por coluna usando o comando `ALTER TABLE SET STATISTICS`(sql-altertable.md "ALTER TABLE"), ou globalmente, definindo o parâmetro de tempo de execução [default_statistics_target](runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET).