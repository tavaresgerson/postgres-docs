## 35.39. `role_usage_grants` [#](#INFOSCHEMA-ROLE-USAGE-GRANTS)

A vista `role_usage_grants` identifica privilégios `USAGE` concedidos em vários tipos de objetos, onde o concedente ou o beneficiário é um papel atualmente habilitado. Mais informações podem ser encontradas em `usage_privileges`. A única diferença efetiva entre essa vista e `usage_privileges` é que essa vista omite objetos que foram tornados acessíveis ao usuário atual por meio de uma concessão para `PUBLIC`.

**Tabela 35.37. Colunas `role_usage_grants`**



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
     The name of the role that granted the privilege
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
     The name of the role that the privilege was granted to
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      object_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database containing the object (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      object_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema containing the object, if applicable, else an empty string
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      object_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the object
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      object_type
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     <code>
      COLLATION
     </code>
     or
     <code>
      DOMAIN
     </code>
     or
     <code>
      FOREIGN DATA WRAPPER
     </code>
     or
     <code>
      FOREIGN SERVER
     </code>
     or
     <code>
      SEQUENCE
     </code>
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
      USAGE
     </code>
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





