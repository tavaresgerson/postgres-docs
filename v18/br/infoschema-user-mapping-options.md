## 35.61. `user_mapping_options` [#](#INFOSCHEMA-USER-MAPPING-OPTIONS)

A vista `user_mapping_options` contém todas as opções definidas para mapeamentos de usuário no banco de dados atual. Apenas os mapeamentos de usuário são mostrados onde o usuário atual tem acesso ao servidor externo correspondente (por ser o proprietário ou ter algum privilégio).

**Tabela 35.59. Colunas `user_mapping_options`**



<table border="1" class="table" summary="user_mapping_options Columns">
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
      authorization_identifier
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the user being mapped, or
     <code class="literal">
      PUBLIC
     </code>
     if the mapping is public
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
     Name of the database that the foreign server used by this mapping is defined in (always the current database)
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
     Name of the foreign server used by this mapping
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
     Value of the option.  This column will show as null unless the current user is the user being mapped, or the mapping is for
     <code class="literal">
      PUBLIC
     </code>
     and the current user is the server owner, or the current user is a superuser.  The intent is to protect password information stored as user mapping option.
    </p>
   </td>
  </tr>
 </tbody>
</table>





