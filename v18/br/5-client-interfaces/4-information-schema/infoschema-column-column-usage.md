## 35.12. `column_column_usage` [#](#INFOSCHEMA-COLUMN-COLUMN-USAGE)

A vista `column_column_usage` identifica todas as colunas geradas que dependem de outra coluna base na mesma tabela. Apenas as tabelas de propriedade de um papel habilitado atualmente são incluídas.

**Tabela 35.10. Colunas `column_column_usage`**



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
      table_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database containing the table (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      table_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema containing the table
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      table_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the table
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      column_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the base column that a generated column depends on
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      dependent_column
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the generated column
    </p>
   </td>
  </tr>
 </tbody>
</table>





