## 35.58. `udt_privileges` [#](#INFOSCHEMA-UDT-PRIVILEGES)

A vista `udt_privileges` identifica os privilégios `USAGE` concedidos em tipos definidos pelo usuário para um papel atualmente habilitado ou por um papel atualmente habilitado. Há uma linha para cada combinação de tipo, concedente e beneficiário. Esta vista mostra apenas tipos compostos (consulte [Seção 35.60](infoschema-user-defined-types.md) para saber por quê); consulte [Seção 35.59](infoschema-usage-privileges.md) para privilégios de domínio.

**Tabela 35.56. Colunas `udt_privileges`**



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
      udt_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database containing the type (always the current database)
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
     Name of the schema containing the type
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
     Name of the type
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
      TYPE USAGE
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





