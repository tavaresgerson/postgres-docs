## 35.31. `foreign_tables` [#](#INFOSCHEMA-FOREIGN-TABLES)

A vista `foreign_tables` contém todas as tabelas externas definidas no banco de dados atual. Apenas as tabelas externas são mostradas que o usuário atual tem acesso (como proprietário ou com algum privilégio).

**Tabela 35.29. Colunas `foreign_tables`**



<table border="1" class="table" summary="foreign_tables Columns">
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
      foreign_table_catalog
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that the foreign table is defined in (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      foreign_table_schema
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema that contains the foreign table
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      foreign_table_name
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the foreign table
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      foreign_server_catalog
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that the foreign server is defined in (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      foreign_server_name
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the foreign server
    </p>
   </td>
  </tr>
 </tbody>
</table>




