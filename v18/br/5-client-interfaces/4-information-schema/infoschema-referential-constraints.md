## 35.34. `referential_constraints` [#](#INFOSCHEMA-REFERENTIAL-CONSTRAINTS)

A vista `referential_constraints` contém todas as restrições referenciais (chave estrangeira) no banco de dados atual. Apenas as restrições que o usuário atual tem acesso de escrita à tabela de referência (sendo o proprietário ou tendo algum privilégio diferente de `SELECT`), são mostradas.

**Tabela 35.32. Colunas `referential_constraints`**



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
      constraint_catalog
     </code>
     <code>
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
     <code>
      constraint_schema
     </code>
     <code>
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
     <code>
      constraint_name
     </code>
     <code>
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
     <code>
      unique_constraint_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that contains the unique or primary key constraint that the foreign key constraint references (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      unique_constraint_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema that contains the unique or primary key constraint that the foreign key constraint references
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      unique_constraint_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the unique or primary key constraint that the foreign key constraint references
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      match_option
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Match option of the foreign key constraint:
     <code>
      FULL
     </code>
     ,
     <code>
      PARTIAL
     </code>
     , or
     <code>
      NONE
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      update_rule
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Update rule of the foreign key constraint:
     <code>
      CASCADE
     </code>
     ,
     <code>
      SET NULL
     </code>
     ,
     <code>
      SET DEFAULT
     </code>
     ,
     <code>
      RESTRICT
     </code>
     , or
     <code>
      NO ACTION
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      delete_rule
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Delete rule of the foreign key constraint:
     <code>
      CASCADE
     </code>
     ,
     <code>
      SET NULL
     </code>
     ,
     <code>
      SET DEFAULT
     </code>
     ,
     <code>
      RESTRICT
     </code>
     , or
     <code>
      NO ACTION
     </code>
     .
    </p>
   </td>
  </tr>
 </tbody>
</table>





