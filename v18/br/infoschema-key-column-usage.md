## 35.32. `key_column_usage` [#](#INFOSCHEMA-KEY-COLUMN-USAGE)

A vista `key_column_usage` identifica todas as colunas no banco de dados atual que são restritas por alguma restrição de chave primária ou chave estrangeira única. As restrições de verificação não são incluídas nesta vista. Apenas as colunas que o usuário atual tem acesso, sendo proprietário ou tendo algum privilégio, são mostradas.

**Tabela 35.30. Colunas `key_column_usage`**



<table border="1" class="table" summary="key_column_usage Columns">
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
      constraint_catalog
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that contains the constraint (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      constraint_schema
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema that contains the constraint
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      constraint_name
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the constraint
    </p>
   </td>
  </tr>
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
     Name of the database that contains the table that contains the column that is restricted by this constraint (always the current database)
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
     Name of the schema that contains the table that contains the column that is restricted by this constraint
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
     Name of the table that contains the column that is restricted by this constraint
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
     Name of the column that is restricted by this constraint
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      ordinal_position
     </code>
     <code class="type">
      cardinal_number
     </code>
    </p>
    <p>
     Ordinal position of the column within the constraint key (count starts at 1)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      position_in_unique_constraint
     </code>
     <code class="type">
      cardinal_number
     </code>
    </p>
    <p>
     For a foreign-key constraint, ordinal position of the referenced column within its unique constraint (count starts at 1); otherwise null
    </p>
   </td>
  </tr>
 </tbody>
</table>




