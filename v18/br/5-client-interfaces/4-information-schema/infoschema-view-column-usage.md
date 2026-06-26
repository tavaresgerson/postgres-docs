## 35.63. `view_column_usage` [#](#INFOSCHEMA-VIEW-COLUMN-USAGE)

A vista `view_column_usage` identifica todas as colunas que são usadas na expressão de consulta de uma vista (a declaração `SELECT` que define a vista). Uma coluna só é incluída se a tabela que contém a coluna for de propriedade de um papel atualmente habilitado.

Nota

As colunas das tabelas do sistema não estão incluídas. Isso deve ser corrigido em algum momento.

**Tabela 35.61. Colunas `view_column_usage`**



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
      view_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that contains the view (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      view_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema that contains the view
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      view_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the view
    </p>
   </td>
  </tr>
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
     Name of the database that contains the table that contains the column that is used by the view (always the current database)
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
     Name of the schema that contains the table that contains the column that is used by the view
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
     Name of the table that contains the column that is used by the view
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
     Name of the column that is used by the view
    </p>
   </td>
  </tr>
 </tbody>
</table>





