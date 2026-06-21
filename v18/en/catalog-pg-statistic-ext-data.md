## 52.53. `pg_statistic_ext_data` [#](#CATALOG-PG-STATISTIC-EXT-DATA)

The catalog `pg_statistic_ext_data` holds data for extended planner statistics defined in [`pg_statistic_ext`](catalog-pg-statistic-ext.md "52.52. pg_statistic_ext"). Each row in this catalog corresponds to a *statistics object* created with [`CREATE STATISTICS`](sql-createstatistics.md "CREATE STATISTICS").

Normally there is one entry, with `stxdinherit` = `false`, for each statistics object that has been analyzed. If the table has inheritance children or partitions, a second entry with `stxdinherit` = `true` is also created. This row represents the statistics object over the inheritance tree, i.e., statistics for the data you'd see with `SELECT * FROM table*`, whereas the `stxdinherit` = `false` row represents the results of `SELECT * FROM ONLY table`.

Like [`pg_statistic`](catalog-pg-statistic.md "52.51. pg_statistic"), `pg_statistic_ext_data` should not be readable by the public, since the contents might be considered sensitive. (Example: most common combinations of values in columns might be quite interesting.) [`pg_stats_ext`](view-pg-stats-ext.md "53.30. pg_stats_ext") is a publicly readable view on `pg_statistic_ext_data` (after joining with [`pg_statistic_ext`](catalog-pg-statistic-ext.md "52.52. pg_statistic_ext")) that only exposes information about tables the current user owns.

**Table 52.53. `pg_statistic_ext_data` Columns**



<table border="1" class="table" summary="pg_statistic_ext_data Columns">
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
      stxoid
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-statistic-ext.md" title="52.52. pg_statistic_ext">
      <code class="structname">
       pg_statistic_ext
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      stxdinherit
     </code>
     <code class="type">
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
     <code class="structfield">
      stxdndistinct
     </code>
     <code class="type">
      pg_ndistinct
     </code>
    </p>
    <p>
     N-distinct counts, serialized as
     <code class="structname">
      pg_ndistinct
     </code>
     type
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      stxddependencies
     </code>
     <code class="type">
      pg_dependencies
     </code>
    </p>
    <p>
     Functional dependency statistics, serialized as
     <code class="structname">
      pg_dependencies
     </code>
     type
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      stxdmcv
     </code>
     <code class="type">
      pg_mcv_list
     </code>
    </p>
    <p>
     MCV (most-common values) list statistics, serialized as
     <code class="structname">
      pg_mcv_list
     </code>
     type
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      stxdexpr
     </code>
     <code class="type">
      pg_statistic[]
     </code>
    </p>
    <p>
     Per-expression statistics, serialized as an array of
     <code class="structname">
      pg_statistic
     </code>
     type
    </p>
   </td>
  </tr>
 </tbody>
</table>

