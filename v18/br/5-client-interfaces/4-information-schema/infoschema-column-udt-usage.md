## 35.16. `column_udt_usage` [#](#INFOSCHEMA-COLUMN-UDT-USAGE)

A vista `column_udt_usage` identifica todas as colunas que utilizam tipos de dados de propriedade de um papel atualmente habilitado. Observe que, no PostgreSQL, os tipos de dados integrados se comportam como tipos definidos pelo usuário, portanto, eles também são incluídos aqui. Consulte também [Seção 35.17](infoschema-columns.md) para obter detalhes.

**Tabela 35.14. Colunas `column_udt_usage`**



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
      udt_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that the column data type (the underlying type of the domain, if applicable) is defined in (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      udt_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema that the column data type (the underlying type of the domain, if applicable) is defined in
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      udt_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the column data type (the underlying type of the domain, if applicable)
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
     Name of the column
    </p>
   </td>
  </tr>
 </tbody>
</table>





