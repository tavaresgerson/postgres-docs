## 35.50. `sql_parts` [#](#INFOSCHEMA-SQL-PARTS)

A tabela `sql_parts` contém informações sobre quais das várias partes do padrão SQL são suportadas pelo PostgreSQL.

**Tabela 35.48. Colunas `sql_parts`**



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
      feature_id
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     An identifier string containing the number of the part
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      feature_name
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Descriptive name of the part
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      is_supported
     </code>
     <code>
      yes_or_no
     </code>
    </p>
    <p>
     <code>
      YES
     </code>
     if the part is fully supported by the current version of
     <span class="productname">
      PostgreSQL
     </span>
     ,
     <code>
      NO
     </code>
     if not
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      is_verified_by
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Always null, since the
     <span class="productname">
      PostgreSQL
     </span>
     development group does not perform formal testing of feature conformance
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
     Possibly a comment about the supported status of the part
    </p>
   </td>
  </tr>
 </tbody>
</table>





