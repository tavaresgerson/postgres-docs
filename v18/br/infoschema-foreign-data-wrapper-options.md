## 35.26. `foreign_data_wrapper_options` [#](#INFOSCHEMA-FOREIGN-DATA-WRAPPER-OPTIONS)

A vista `foreign_data_wrapper_options` contém todas as opções definidas para os wrappers de dados externos no banco de dados atual. Apenas os wrappers de dados externos que o usuário atual tem acesso (como proprietário ou com algum privilégio) são mostrados.

**Tabela 35.24. Colunas `foreign_data_wrapper_options`**



<table border="1" class="table" summary="foreign_data_wrapper_options Columns">
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
      foreign_data_wrapper_catalog
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that the foreign-data wrapper is defined in (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      foreign_data_wrapper_name
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the foreign-data wrapper
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




