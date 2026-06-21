## 52.44. `pg_replication_origin` [#](#CATALOG-PG-REPLICATION-ORIGIN)

The `pg_replication_origin` catalog contains all replication origins created. For more on replication origins see [Chapter 48](replication-origins.md "Chapter 48. Replication Progress Tracking").

Unlike most system catalogs, `pg_replication_origin` is shared across all databases of a cluster: there is only one copy of `pg_replication_origin` per cluster, not one per database.

**Table 52.44. `pg_replication_origin` Columns**



<table border="1" class="table" summary="pg_replication_origin Columns">
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
      roident
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     A unique, cluster-wide identifier for the replication origin. Should never leave the system.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      roname
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     The external, user defined, name of a replication origin.
    </p>
   </td>
  </tr>
 </tbody>
</table>

