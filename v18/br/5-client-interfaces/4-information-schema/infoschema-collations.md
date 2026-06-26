## 35.10. `collations` [#](#INFOSCHEMA-COLLATIONS)

A vista `collations` contém as colações disponíveis no banco de dados atual.

**Tabela 35.8. Colunas `collations`**



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
      collation_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database containing the collation (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      collation_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema containing the collation
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      collation_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the default collation
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      pad_attribute
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Always
     <code>
      NO PAD
     </code>
     (The alternative
     <code>
      PAD SPACE
     </code>
     is not supported by PostgreSQL.)
    </p>
   </td>
  </tr>
 </tbody>
</table>





