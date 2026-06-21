## 53.10. `pg_hba_file_rules` [#](#VIEW-PG-HBA-FILE-RULES)

The view `pg_hba_file_rules` provides a summary of the contents of the client authentication configuration file, [`pg_hba.conf`](auth-pg-hba-conf.md "20.1. The pg_hba.conf File"). A row appears in this view for each non-empty, non-comment line in the file, with annotations indicating whether the rule could be applied successfully.

This view can be helpful for checking whether planned changes in the authentication configuration file will work, or for diagnosing a previous failure. Note that this view reports on the *current* contents of the file, not on what was last loaded by the server.

By default, the `pg_hba_file_rules` view can be read only by superusers.

**Table 53.10. `pg_hba_file_rules` Columns**



<table border="1" class="table" summary="pg_hba_file_rules Columns">
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
      rule_number
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Number of this rule, if valid, otherwise
     <code class="literal">
      NULL
     </code>
     . This indicates the order in which each rule is considered until a match is found during authentication.
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
     Name of the file containing this rule
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
     Line number of this rule in
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
      type
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Type of connection
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      database
     </code>
     <code class="type">
      text[]
     </code>
    </p>
    <p>
     List of database name(s) to which this rule applies
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      user_name
     </code>
     <code class="type">
      text[]
     </code>
    </p>
    <p>
     List of user and group name(s) to which this rule applies
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      address
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Host name or IP address, or one of
     <code class="literal">
      all
     </code>
     ,
     <code class="literal">
      samehost
     </code>
     , or
     <code class="literal">
      samenet
     </code>
     , or null for local connections
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      netmask
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     IP address mask, or null if not applicable
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      auth_method
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Authentication method
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      options
     </code>
     <code class="type">
      text[]
     </code>
    </p>
    <p>
     Options specified for authentication method, if any
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
     If not null, an error message indicating why this line could not be processed
    </p>
   </td>
  </tr>
 </tbody>
</table>




  

Usually, a row reflecting an incorrect entry will have values for only the `line_number` and `error` fields.

See [Chapter 20](client-authentication.md "Chapter 20. Client Authentication") for more information about client authentication configuration.
