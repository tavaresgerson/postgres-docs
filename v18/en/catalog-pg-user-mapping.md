## 52.65. `pg_user_mapping` [#](#CATALOG-PG-USER-MAPPING)

The catalog `pg_user_mapping` stores the mappings from local user to remote. Access to this catalog is restricted from normal users, use the view [`pg_user_mappings`](view-pg-user-mappings.md "53.36. pg_user_mappings") instead.

**Table 52.66. `pg_user_mapping` Columns**



<table border="1" class="table" summary="pg_user_mapping Columns">
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
      oid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     Row identifier
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      umuser
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code class="structname">
       pg_authid
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     OID of the local role being mapped, or zero if the user mapping is public
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      umserver
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-foreign-server.md" title="52.24. pg_foreign_server">
      <code class="structname">
       pg_foreign_server
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     The OID of the foreign server that contains this mapping
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      umoptions
     </code>
     <code class="type">
      text[]
     </code>
    </p>
    <p>
     User mapping specific options, as
     <span class="quote">
      “
      <span class="quote">
       keyword=value
      </span>
      ”
     </span>
     strings
    </p>
   </td>
  </tr>
 </tbody>
</table>

