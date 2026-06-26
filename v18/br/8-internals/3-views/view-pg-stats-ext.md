## 53.30. `pg_stats_ext` [#](#VIEW-PG-STATS-EXT)

A vista `pg_stats_ext` fornece acesso a informações sobre cada objeto de estatísticas estendidas no banco de dados, combinando informações armazenadas nos catálogos `pg_statistic_ext`(catalog-pg-statistic-ext.md "52.52. pg_statistic_ext") e `pg_statistic_ext_data`(catalog-pg-statistic-ext-data.md "52.53. pg_statistic_ext_data"). Esta vista permite acesso apenas a linhas de `pg_statistic_ext`(catalog-pg-statistic-ext.md "52.52. pg_statistic_ext") e `pg_statistic_ext_data`(catalog-pg-statistic-ext-data.md "52.53. pg_statistic_ext_data") que correspondem a tabelas que o usuário possui, e, portanto, é seguro permitir acesso de leitura público a esta vista.

`pg_stats_ext` também é projetado para apresentar as informações em um formato mais legível do que os catálogos subjacentes — ao custo de que seu esquema deve ser estendido sempre que novos tipos de estatísticas estendidas são adicionados a [`pg_statistic_ext`](catalog-pg-statistic-ext.md "52.52. pg_statistic_ext").

**Tabela 53.30. Colunas `pg_stats_ext`**



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
      attnames
     </code>
     <code>
      name[]
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
     Names of the columns included in the extended statistics object
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      exprs
     </code>
     <code>
      text[]
     </code>
    </p>
    <p>
     Expressions included in the extended statistics object
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      kinds
     </code>
     <code>
      char[]
     </code>
    </p>
    <p>
     Types of extended statistics object enabled for this record
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
      n_distinct
     </code>
     <code>
      pg_ndistinct
     </code>
    </p>
    <p>
     N-distinct counts for combinations of column values. If greater than zero, the estimated number of distinct values in the combination. If less than zero, the negative of the number of distinct values divided by the number of rows. (The negated form is used when
     <code>
      ANALYZE
     </code>
     believes that the number of distinct values is likely to increase as the table grows; the positive form is used when the column seems to have a fixed number of possible values.)  For example, -1 indicates a unique combination of columns in which the number of distinct combinations is the same as the number of rows.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      dependencies
     </code>
     <code>
      pg_dependencies
     </code>
    </p>
    <p>
     Functional dependency statistics
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
      text[]
     </code>
    </p>
    <p>
     A list of the most common combinations of values in the columns. (Null if no combinations seem to be more common than any others.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      most_common_val_nulls
     </code>
     <code>
      bool[]
     </code>
    </p>
    <p>
     A list of NULL flags for the most common combinations of values. (Null when
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
      most_common_freqs
     </code>
     <code>
      float8[]
     </code>
    </p>
    <p>
     A list of the frequencies of the most common combinations, i.e., number of occurrences of each divided by total number of rows. (Null when
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
      most_common_base_freqs
     </code>
     <code>
      float8[]
     </code>
    </p>
    <p>
     A list of the base frequencies of the most common combinations, i.e., product of per-value frequencies. (Null when
     <code>
      most_common_vals
     </code>
     is.)
    </p>
   </td>
  </tr>
 </tbody>
</table>










O número máximo de entradas nos campos da matriz pode ser controlado de forma coluna por coluna usando o comando `ALTER TABLE SET STATISTICS`(sql-altertable.md "ALTER TABLE"), ou globalmente, definindo o parâmetro de tempo de execução [default_statistics_target](runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET).