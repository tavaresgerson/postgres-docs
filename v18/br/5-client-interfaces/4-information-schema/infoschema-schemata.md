## 35.46. `schemata` [#](#INFOSCHEMA-SCHEMATA)

A vista `schemata` contém todos os esquemas no banco de dados atual que o usuário atual tem acesso (sendo o proprietário ou tendo algum privilégio).

**Tabela 35.44. Colunas `schemata`**



<table>
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
     <code>
      catalog_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that the schema is contained in (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      schema_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      schema_owner
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the owner of the schema
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      default_character_set_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      default_character_set_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      default_character_set_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      sql_path
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
    </p>
   </td>
  </tr>
 </tbody>
</table>





