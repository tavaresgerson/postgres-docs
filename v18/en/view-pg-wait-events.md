## 53.38. `pg_wait_events` [#](#VIEW-PG-WAIT-EVENTS)

The view `pg_wait_events` provides description about the wait events.

**Table 53.38. `pg_wait_events` Columns**



<table border="1" class="table" summary="pg_wait_events Columns">
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
      type
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Wait event type
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      name
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Wait event name
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      description
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Wait event description
    </p>
   </td>
  </tr>
 </tbody>
</table>

