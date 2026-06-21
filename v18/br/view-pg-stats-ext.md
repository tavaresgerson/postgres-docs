## 53.30. `pg_stats_ext` [#](#VIEW-PG-STATS-EXT)

A vista `pg_stats_ext` fornece acesso a informações sobre cada objeto de estatísticas estendidas no banco de dados, combinando informações armazenadas nos catálogos `pg_statistic_ext`(catalog-pg-statistic-ext.md "52.52. pg_statistic_ext") e `pg_statistic_ext_data`(catalog-pg-statistic-ext-data.md "52.53. pg_statistic_ext_data"). Esta vista permite acesso apenas a linhas de `pg_statistic_ext`(catalog-pg-statistic-ext.md "52.52. pg_statistic_ext") e `pg_statistic_ext_data`(catalog-pg-statistic-ext-data.md "52.53. pg_statistic_ext_data") que correspondem a tabelas que o usuário possui, e, portanto, é seguro permitir acesso de leitura público a esta vista.

`pg_stats_ext` também é projetado para apresentar as informações em um formato mais legível do que os catálogos subjacentes — ao custo de que seu esquema deve ser estendido sempre que novos tipos de estatísticas estendidas são adicionados a [`pg_statistic_ext`](catalog-pg-statistic-ext.md "52.52. pg_statistic_ext").

**Tabela 53.30. Colunas `pg_stats_ext`**



<table border="1" class="table" summary="pg_stats_ext Columns">
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
<code class="structfield">
      schemaname
     </code>
<code class="type">
      name
     </code>
     (references
     <a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
<code class="structname">
       pg_namespace
      </code>
</a>
     .
     <code class="structfield">
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
<code class="structfield">
      tablename
     </code>
<code class="type">
      name
     </code>
     (references
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
<code class="structname">
       pg_class
      </code>
</a>
     .
     <code class="structfield">
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
<code class="structfield">
      statistics_schemaname
     </code>
<code class="type">
      name
     </code>
     (references
     <a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
<code class="structname">
       pg_namespace
      </code>
</a>
     .
     <code class="structfield">
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
<code class="structfield">
      statistics_name
     </code>
<code class="type">
      name
     </code>
     (references
     <a class="link" href="catalog-pg-statistic-ext.md" title="52.52. pg_statistic_ext">
<code class="structname">
       pg_statistic_ext
      </code>
</a>
     .
     <code class="structfield">
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
<code class="structfield">
      statistics_owner
     </code>
<code class="type">
      name
     </code>
     (references
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
<code class="structname">
       pg_authid
      </code>
</a>
     .
     <code class="structfield">
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
<code class="structfield">
      attnames
     </code>
<code class="type">
      name[]
     </code>
     (references
     <a class="link" href="catalog-pg-attribute.md" title="52.7. pg_attribute">
<code class="structname">
       pg_attribute
      </code>
</a>
     .
     <code class="structfield">
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
<code class="structfield">
      exprs
     </code>
<code class="type">
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
<code class="structfield">
      kinds
     </code>
<code class="type">
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
<code class="structfield">
      inherited
     </code>
<code class="type">
      bool
     </code>
     (references
     <a class="link" href="catalog-pg-statistic-ext-data.md" title="52.53. pg_statistic_ext_data">
<code class="structname">
       pg_statistic_ext_data
      </code>
</a>
     .
     <code class="structfield">
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
<code class="structfield">
      n_distinct
     </code>
<code class="type">
      pg_ndistinct
     </code>
</p>
<p>
     N-distinct counts for combinations of column values. If greater than zero, the estimated number of distinct values in the combination. If less than zero, the negative of the number of distinct values divided by the number of rows. (The negated form is used when
     <code class="command">
      ANALYZE
     </code>
     believes that the number of distinct values is likely to increase as the table grows; the positive form is used when the column seems to have a fixed number of possible values.)  For example, -1 indicates a unique combination of columns in which the number of distinct combinations is the same as the number of rows.
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      dependencies
     </code>
<code class="type">
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
<code class="structfield">
      most_common_vals
     </code>
<code class="type">
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
<code class="structfield">
      most_common_val_nulls
     </code>
<code class="type">
      bool[]
     </code>
</p>
<p>
     A list of NULL flags for the most common combinations of values. (Null when
     <code class="structfield">
      most_common_vals
     </code>
     is.)
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      most_common_freqs
     </code>
<code class="type">
      float8[]
     </code>
</p>
<p>
     A list of the frequencies of the most common combinations, i.e., number of occurrences of each divided by total number of rows. (Null when
     <code class="structfield">
      most_common_vals
     </code>
     is.)
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      most_common_base_freqs
     </code>
<code class="type">
      float8[]
     </code>
</p>
<p>
     A list of the base frequencies of the most common combinations, i.e., product of per-value frequencies. (Null when
     <code class="structfield">
      most_common_vals
     </code>
     is.)
    </p>
</td>
</tr>
</tbody>
</table>




  

O número máximo de entradas nos campos da matriz pode ser controlado de forma coluna por coluna usando o comando `ALTER TABLE SET STATISTICS`(sql-altertable.md "ALTER TABLE"), ou globalmente, definindo o parâmetro de tempo de execução [default_statistics_target](runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET).