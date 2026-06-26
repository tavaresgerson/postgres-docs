## 52.53. `pg_statistic_ext_data` [#](#CATALOG-PG-STATISTIC-EXT-DATA)

O catálogo `pg_statistic_ext_data` contém dados para estatísticas de planejador estendido definidos em [`pg_statistic_ext`](catalog-pg-statistic-ext.md "52.52. pg_statistic_ext"). Cada linha deste catálogo corresponde a um *objeto de estatísticas* criado com [`CREATE STATISTICS`](sql-createstatistics.md "CREATE STATISTICS").

Normalmente, há uma entrada, com `stxdinherit` = `false`, para cada objeto de estatísticas que foi analisado. Se a tabela tiver filhos ou partições de herança, uma segunda entrada com `stxdinherit` = `true` também é criada. Esta linha representa o objeto de estatísticas sobre a árvore de herança, ou seja, estatísticas para os dados que você veria com `SELECT * FROM table*`, enquanto a linha `stxdinherit` = `false` representa os resultados de `SELECT * FROM ONLY table`.

Assim como `pg_statistic` (catalog-pg-statistic.md "52.51. pg_statistic"), `pg_statistic_ext_data` não deve ser legível pelo público, uma vez que o conteúdo pode ser considerado sensível. (Exemplo: a maioria das combinações comuns de valores nas colunas pode ser bastante interessante.) `pg_stats_ext` (view-pg-stats-ext.md "53.30. pg_stats_ext") é uma visão legível publicamente sobre `pg_statistic_ext_data` (após a junção com `pg_statistic_ext` (catalog-pg-statistic-ext.md "52.52. pg_statistic_ext")) que expõe apenas informações sobre as tabelas que o usuário atual possui.

**Tabela 52.53. Colunas `pg_statistic_ext_data`**



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
      stxoid
     </code>
     <code>
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-statistic-ext.md" title="52.52. pg_statistic_ext">
      <code>
       pg_statistic_ext
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Extended statistics object containing the definition for this data
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      stxdinherit
     </code>
     <code>
      bool
     </code>
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
      stxdndistinct
     </code>
     <code>
      pg_ndistinct
     </code>
    </p>
    <p>
     N-distinct counts, serialized as
     <code>
      pg_ndistinct
     </code>
     type
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      stxddependencies
     </code>
     <code>
      pg_dependencies
     </code>
    </p>
    <p>
     Functional dependency statistics, serialized as
     <code>
      pg_dependencies
     </code>
     type
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      stxdmcv
     </code>
     <code>
      pg_mcv_list
     </code>
    </p>
    <p>
     MCV (most-common values) list statistics, serialized as
     <code>
      pg_mcv_list
     </code>
     type
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      stxdexpr
     </code>
     <code>
      pg_statistic[]
     </code>
    </p>
    <p>
     Per-expression statistics, serialized as an array of
     <code>
      pg_statistic
     </code>
     type
    </p>
   </td>
  </tr>
 </tbody>
</table>





