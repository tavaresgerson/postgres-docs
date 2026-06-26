## 35.51. `sql_sizing` [#](#INFOSCHEMA-SQL-SIZING)

A tabela `sql_sizing` contém informações sobre vários limites de tamanho e valores máximos no PostgreSQL. Essas informações são destinadas principalmente para uso no contexto da interface ODBC; os usuários de outras interfaces provavelmente encontrarão essas informações de pouco uso. Por esse motivo, os itens de dimensionamento individual não são descritos aqui; você os encontrará na descrição da interface ODBC.

**Tabela 35.49. Colunas `sql_sizing`**



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
      sizing_id
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     Identifier of the sizing item
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      sizing_name
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Descriptive name of the sizing item
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      supported_value
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     Value of the sizing item, or 0 if the size is unlimited or cannot be determined, or null if the features for which the sizing item is applicable are not supported
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      comments
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Possibly a comment pertaining to the sizing item
    </p>
   </td>
  </tr>
 </tbody>
</table>





