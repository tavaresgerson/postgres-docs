## 52.55. `pg_subscription_rel` [#](#CATALOG-PG-SUBSCRIPTION-REL)

The catalog `pg_subscription_rel` contains the state for each replicated relation in each subscription. This is a many-to-many mapping.

This catalog only contains tables known to the subscription after running either [`CREATE SUBSCRIPTION`](sql-createsubscription.md "CREATE SUBSCRIPTION") or [`ALTER SUBSCRIPTION ... REFRESH PUBLICATION`](sql-altersubscription.md "ALTER SUBSCRIPTION").

**Table 52.55. `pg_subscription_rel` Columns**



<table border="1" class="table" summary="pg_subscription_rel Columns">
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
      srsubid
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-subscription.md" title="52.54. pg_subscription">
      <code class="structname">
       pg_subscription
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Reference to subscription
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      srrelid
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
       pg_class
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Reference to relation
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      srsubstate
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     State code:
     <code class="literal">
      i
     </code>
     = initialize,
     <code class="literal">
      d
     </code>
     = data is being copied,
     <code class="literal">
      f
     </code>
     = finished table copy,
     <code class="literal">
      s
     </code>
     = synchronized,
     <code class="literal">
      r
     </code>
     = ready (normal replication)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      srsublsn
     </code>
     <code class="type">
      pg_lsn
     </code>
    </p>
    <p>
     Remote LSN of the state change used for synchronization coordination when in
     <code class="literal">
      s
     </code>
     or
     <code class="literal">
      r
     </code>
     states, otherwise null
    </p>
   </td>
  </tr>
 </tbody>
</table>

