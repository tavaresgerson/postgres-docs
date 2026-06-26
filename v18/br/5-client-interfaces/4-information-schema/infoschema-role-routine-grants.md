## 35.36. `role_routine_grants` [#](#INFOSCHEMA-ROLE-ROUTINE-GRANTS)

A vista `role_routine_grants` identifica todos os privilégios concedidos em funções onde o concedente ou o beneficiário é um papel habilitado atualmente. Mais informações podem ser encontradas em `routine_privileges`. A única diferença efetiva entre esta vista e `routine_privileges` é que esta vista omite funções que foram tornadas acessíveis ao usuário atual por meio de uma concessão para `PUBLIC`.

**Tabela 35.34. Colunas `role_routine_grants`**



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
      grantor
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the role that granted the privilege
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      grantee
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the role that the privilege was granted to
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      specific_catalog
     </code>
     <code>
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
     <code>
      specific_schema
     </code>
     <code>
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
     <code>
      specific_name
     </code>
     <code>
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
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      routine_catalog
     </code>
     <code>
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
     <code>
      routine_schema
     </code>
     <code>
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
     <code>
      routine_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the function (might be duplicated in case of overloading)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      privilege_type
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Always
     <code>
      EXECUTE
     </code>
     (the only privilege type for functions)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      is_grantable
     </code>
     <code>
      yes_or_no
     </code>
    </p>
    <p>
     <code>
      YES
     </code>
     if the privilege is grantable,
     <code>
      NO
     </code>
     if not
    </p>
   </td>
  </tr>
 </tbody>
</table>





