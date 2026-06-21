## 53.11. `pg_ident_file_mappings` [#](#VIEW-PG-IDENT-FILE-MAPPINGS)

The view `pg_ident_file_mappings` provides a summary of the contents of the client user name mapping configuration file, [`pg_ident.conf`](auth-username-maps.md "20.2. User Name Maps"). A row appears in this view for each non-empty, non-comment line in the file, with annotations indicating whether the map could be applied successfully.

This view can be helpful for checking whether planned changes in the authentication configuration file will work, or for diagnosing a previous failure. Note that this view reports on the *current* contents of the file, not on what was last loaded by the server.

By default, the `pg_ident_file_mappings` view can be read only by superusers.

**Table 53.11. `pg_ident_file_mappings` Columns**



<table border="1" class="table" summary="pg_ident_file_mappings Columns">
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
      map_number
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Number of this map, in priority order, if valid, otherwise
     <code class="literal">
      NULL
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      file_name
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Name of the file containing this map
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      line_number
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Line number of this map in
     <code class="literal">
      file_name
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      map_name
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Name of the map
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      sys_name
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Detected user name of the client
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      pg_username
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Requested PostgreSQL user name
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      error
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     If not
     <code class="literal">
      NULL
     </code>
     , an error message indicating why this line could not be processed
    </p>
   </td>
  </tr>
 </tbody>
</table>




  

Usually, a row reflecting an incorrect entry will have values for only the `line_number` and `error` fields.

See [Chapter 20](client-authentication.md "Chapter 20. Client Authentication") for more information about client authentication configuration.
