## 35.56. `triggered_update_columns` [#](#INFOSCHEMA-TRIGGERED-UPDATE-COLUMNS)

Para gatilhos no banco de dados atual que especificam uma lista de colunas (como `UPDATE OF column1, column2`), a visão `triggered_update_columns` identifica essas colunas. Os gatilhos que não especificam uma lista de colunas não são incluídos nesta visão. Apenas as colunas que o usuário atual possui ou tem algum privilégio além de `SELECT` são mostradas.

**Tabela 35.54. Colunas `triggered_update_columns`**



<table border="1" class="table" summary="triggered_update_columns Columns">
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
      trigger_catalog
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that contains the trigger (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      trigger_schema
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema that contains the trigger
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      trigger_name
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the trigger
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      event_object_catalog
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that contains the table that the trigger is defined on (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      event_object_schema
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema that contains the table that the trigger is defined on
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      event_object_table
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the table that the trigger is defined on
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      event_object_column
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the column that the trigger is defined on
    </p>
   </td>
  </tr>
 </tbody>
</table>




