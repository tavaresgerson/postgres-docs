## 35.28. `foreign_server_options` [#](#INFOSCHEMA-FOREIGN-SERVER-OPTIONS)

A vista `foreign_server_options` contém todas as opções definidas para servidores externos no banco de dados atual. Apenas os servidores externos que o usuário atual tem acesso (como proprietário ou com algum privilégio) são mostrados.

**Tabela 35.26. Colunas `foreign_server_options`**



<table border="1" class="table" summary="foreign_server_options Columns">
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





