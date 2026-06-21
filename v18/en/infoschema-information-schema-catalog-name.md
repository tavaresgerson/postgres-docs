## 35.3. `information_schema_catalog_name` [#](#INFOSCHEMA-INFORMATION-SCHEMA-CATALOG-NAME)

`information_schema_catalog_name` is a table that always contains one row and one column containing the name of the current database (current catalog, in SQL terminology).

**Table 35.1. `information_schema_catalog_name` Columns**



<table border="1" class="table" summary="information_schema_catalog_name Columns">
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
      catalog_name
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that contains this information schema
    </p>
   </td>
  </tr>
 </tbody>
</table>

