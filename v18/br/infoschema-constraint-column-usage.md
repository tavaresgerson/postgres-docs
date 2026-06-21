## 35.18. `constraint_column_usage` [#](#INFOSCHEMA-CONSTRAINT-COLUMN-USAGE)

A vista `constraint_column_usage` identifica todas as colunas no banco de dados atual que são usadas por alguma restrição. Apenas as colunas são mostradas que estão contidas em uma tabela de propriedade de um papel atualmente habilitado. Para uma restrição de verificação, essa vista identifica as colunas que são usadas na expressão de verificação. Para uma restrição de não nulo, essa vista identifica a coluna sobre a qual a restrição é definida. Para uma restrição de chave estrangeira, essa vista identifica as colunas que a chave estrangeira referencia. Para uma restrição de chave única ou primária, essa vista identifica as colunas restritas.

**Tabela 35.16. Colunas `constraint_column_usage`**



<table border="1" class="table" summary="constraint_column_usage Columns">
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
      table_catalog
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that contains the table that contains the column that is used by some constraint (always the current database)
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
     Name of the schema that contains the table that contains the column that is used by some constraint
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
     Name of the table that contains the column that is used by some constraint
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
     Name of the column that is used by some constraint
    </p>
   </td>
  </tr>
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
 </tbody>
</table>





