## 35.27. `foreign_data_wrappers` [#](#INFOSCHEMA-FOREIGN-DATA-WRAPPERS)

A vista `foreign_data_wrappers` contém todos os wrappers de dados externos definidos no banco de dados atual. Apenas os wrappers de dados externos que o usuário atual tem acesso (como proprietário ou com algum privilégio) são mostrados.

**Tabela 35.25. Colunas `foreign_data_wrappers`**



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
      foreign_data_wrapper_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that contains the foreign-data wrapper (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      foreign_data_wrapper_name
     </code>
     <code>
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
     <code>
      authorization_identifier
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the owner of the foreign server
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      library_name
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     File name of the library that implementing this foreign-data wrapper
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      foreign_data_wrapper_language
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Language used to implement this foreign-data wrapper
    </p>
   </td>
  </tr>
 </tbody>
</table>





