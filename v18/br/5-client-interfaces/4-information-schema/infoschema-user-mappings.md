## 35.62. `user_mappings` [#](#INFOSCHEMA-USER-MAPPINGS)

A vista `user_mappings` contém todos os mapeamentos de usuário definidos no banco de dados atual. Apenas os mapeamentos de usuário são mostrados onde o usuário atual tem acesso ao servidor externo correspondente (sendo o proprietário ou tendo algum privilégio).

**Tabela 35.60. Colunas `user_mappings`**



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
      authorization_identifier
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the user being mapped, or
     <code>
      PUBLIC
     </code>
     if the mapping is public
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      foreign_server_catalog
     </code>
     <code>
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
     <code>
      foreign_server_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the foreign server used by this mapping
    </p>
   </td>
  </tr>
 </tbody>
</table>





