## 53.3. `pg_available_extensions` [#](#VIEW-PG-AVAILABLE-EXTENSIONS)

The `pg_available_extensions` view lists the extensions that are available for installation. See also the [`pg_extension`](catalog-pg-extension.md "52.22. pg_extension") catalog, which shows the extensions currently installed.

**Table 53.3. `pg_available_extensions` Columns**



<table border="1" class="table" summary="pg_available_extensions Columns">
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
      name
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Extension name
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      default_version
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Name of default version, or
     <code class="literal">
      NULL
     </code>
     if none is specified
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      installed_version
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Currently installed version of the extension, or
     <code class="literal">
      NULL
     </code>
     if not installed
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      comment
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Comment string from the extension's control file
    </p>
   </td>
  </tr>
 </tbody>
</table>




  

The `pg_available_extensions` view is read-only.
