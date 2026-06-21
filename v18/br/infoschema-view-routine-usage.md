## 35.64. `view_routine_usage` [#](#INFOSCHEMA-VIEW-ROUTINE-USAGE)

A vista `view_routine_usage` identifica todas as rotinas (funções e procedimentos) que são usadas na expressão de consulta de uma vista (a declaração `SELECT` que define a vista). Uma rotina só é incluída se essa rotina pertencer a um papel habilitado atualmente.

**Tabela 35.62. Colunas `view_routine_usage`**



<table border="1" class="table" summary="view_routine_usage Columns">
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
     Name of the database containing the view (always the current database)
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
     Name of the schema containing the view
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
     Name of the view
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      specific_catalog
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database containing the function (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      specific_schema
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema containing the function
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      specific_name
     </code>
     <code class="type">
      sql_identifier
     </code>
    </p>
    <p>
     The
     <span class="quote">
      “
      <span class="quote">
       specific name
      </span>
      ”
     </span>
     of the function.  See
     <a class="xref" href="infoschema-routines.md" title="35.45. routines">
      Section 35.45
     </a>
     for more information.
    </p>
   </td>
  </tr>
 </tbody>
</table>




