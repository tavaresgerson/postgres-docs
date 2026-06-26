## 35.49. `sql_implementation_info` [#](#INFOSCHEMA-SQL-IMPLEMENTATION-INFO)

A tabela `sql_implementation_info` contém informações sobre vários aspectos que são definidos pela implementação, conforme o padrão SQL. Essas informações são destinadas principalmente para uso no contexto da interface ODBC; os usuários de outras interfaces provavelmente encontrarão essas informações pouco úteis. Por esse motivo, os itens de informações de implementação individual não são descritos aqui; você os encontrará na descrição da interface ODBC.

**Tabela 35.47. Colunas `sql_implementation_info`**



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
      implementation_info_id
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Identifier string of the implementation information item
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      implementation_info_name
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Descriptive name of the implementation information item
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      integer_value
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     Value of the implementation information item, or null if the value is contained in the column
     <code>
      character_value
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      character_value
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Value of the implementation information item, or null if the value is contained in the column
     <code>
      integer_value
     </code>
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
     Possibly a comment pertaining to the implementation information item
    </p>
   </td>
  </tr>
 </tbody>
</table>





