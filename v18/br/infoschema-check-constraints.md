## 35.9. `check_constraints` [#](#INFOSCHEMA-CHECK-CONSTRAINTS)

A visão `check_constraints` contém todas as restrições de verificação, definidas em uma tabela ou em um domínio, que são de propriedade de um papel habilitado atualmente. (O proprietário da tabela ou do domínio é o proprietário da restrição.)

O padrão SQL considera restrições não nulos como restrições de verificação com uma expressão `CHECK (column_name IS NOT NULL)`. Portanto, as restrições não nulos também estão incluídas aqui e não têm uma visão separada.

**Tabela 35.7. Colunas `check_constraints`**



<table border="1" class="table" summary="check_constraints Columns">
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
     Name of the database containing the constraint (always the current database)
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
     Name of the schema containing the constraint
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
      check_clause
     </code>
     <code class="type">
      character_data
     </code>
    </p>
    <p>
     The check expression of the check constraint
    </p>
   </td>
  </tr>
 </tbody>
</table>




