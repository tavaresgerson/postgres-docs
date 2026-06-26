## 35.66. `views` [#](#INFOSCHEMA-VIEWS)

A vista `views` contém todas as vistas definidas no banco de dados atual. Apenas as vistas que o usuário atual tem acesso (como proprietário ou com algum privilégio) são mostradas.

**Tabela 35.64. Colunas `views`**



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
     Name of the database that contains the view (always the current database)
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
     Name of the schema that contains the view
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
     Name of the view
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      view_definition
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Query expression defining the view (null if the view is not owned by a currently enabled role)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      check_option
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     <code>
      CASCADED
     </code>
     or
     <code>
      LOCAL
     </code>
     if the view has a
     <code>
      CHECK OPTION
     </code>
     defined on it,
     <code>
      NONE
     </code>
     if not
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      is_updatable
     </code>
     <code>
      yes_or_no
     </code>
    </p>
    <p>
     <code>
      YES
     </code>
     if the view is updatable (allows
     <code>
      UPDATE
     </code>
     and
     <code>
      DELETE
     </code>
     ),
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
      is_insertable_into
     </code>
     <code>
      yes_or_no
     </code>
    </p>
    <p>
     <code>
      YES
     </code>
     if the view is insertable into (allows
     <code>
      INSERT
     </code>
     ),
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
      is_trigger_updatable
     </code>
     <code>
      yes_or_no
     </code>
    </p>
    <p>
     <code>
      YES
     </code>
     if the view has an
     <code>
      INSTEAD OF
     </code>
     <code>
      UPDATE
     </code>
     trigger defined on it,
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
      is_trigger_deletable
     </code>
     <code>
      yes_or_no
     </code>
    </p>
    <p>
     <code>
      YES
     </code>
     if the view has an
     <code>
      INSTEAD OF
     </code>
     <code>
      DELETE
     </code>
     trigger defined on it,
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
      is_trigger_insertable_into
     </code>
     <code>
      yes_or_no
     </code>
    </p>
    <p>
     <code>
      YES
     </code>
     if the view has an
     <code>
      INSTEAD OF
     </code>
     <code>
      INSERT
     </code>
     trigger defined on it,
     <code>
      NO
     </code>
     if not
    </p>
   </td>
  </tr>
 </tbody>
</table>





