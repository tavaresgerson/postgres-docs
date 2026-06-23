## 35.14. `column_options` [#](#INFOSCHEMA-COLUMN-OPTIONS)

A vista `column_options` contém todas as opções definidas para as colunas de tabela estrangeira no banco de dados atual. Apenas as colunas de tabela estrangeira são mostradas que o usuário atual tem acesso (sendo o proprietário ou tendo algum privilégio).

**Tabela 35.12. Colunas `column_options`**



<table border="1" class="table" summary="column_options Columns">
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
      table_catalog
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that contains the foreign table (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      table_schema
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
      table_name
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
      column_name
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the column
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      option_name
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of an option
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      option_value
     </code>
     <code class="type">
      character_data
     </code>
    </p>
    <p>
     Value of the option
    </p>
   </td>
  </tr>
 </tbody>
</table>





