## 35.49. `sql_implementation_info` [#](#INFOSCHEMA-SQL-IMPLEMENTATION-INFO)

A tabela `sql_implementation_info` contém informações sobre vários aspectos que são definidos pela implementação, conforme o padrão SQL. Essas informações são destinadas principalmente para uso no contexto da interface ODBC; os usuários de outras interfaces provavelmente encontrarão essas informações pouco úteis. Por esse motivo, os itens de informações de implementação individual não são descritos aqui; você os encontrará na descrição da interface ODBC.

**Tabela 35.47. Colunas `sql_implementation_info`**



<table border="1" class="table" summary="sql_implementation_info Columns">
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
      implementation_info_id
     </code>
     <code class="type">
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
     <code class="structfield">
      implementation_info_name
     </code>
     <code class="type">
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
     <code class="structfield">
      integer_value
     </code>
     <code class="type">
      cardinal_number
     </code>
    </p>
    <p>
     Value of the implementation information item, or null if the value is contained in the column
     <code class="literal">
      character_value
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      character_value
     </code>
     <code class="type">
      character_data
     </code>
    </p>
    <p>
     Value of the implementation information item, or null if the value is contained in the column
     <code class="literal">
      integer_value
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      comments
     </code>
     <code class="type">
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




