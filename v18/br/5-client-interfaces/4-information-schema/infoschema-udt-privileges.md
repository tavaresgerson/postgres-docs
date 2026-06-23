## 35.58. `udt_privileges` [#](#INFOSCHEMA-UDT-PRIVILEGES)

A vista `udt_privileges` identifica os privilégios `USAGE` concedidos em tipos definidos pelo usuário para um papel atualmente habilitado ou por um papel atualmente habilitado. Há uma linha para cada combinação de tipo, concedente e beneficiário. Esta vista mostra apenas tipos compostos (consulte [Seção 35.60](infoschema-user-defined-types.md) para saber por quê); consulte [Seção 35.59](infoschema-usage-privileges.md) para privilégios de domínio.

**Tabela 35.56. Colunas `udt_privileges`**



<table border="1" class="table" summary="udt_privileges Columns">
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
      grantor
     </code>
     <code class="type">
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
     <code class="structfield">
      grantee
     </code>
     <code class="type">
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
     <code class="structfield">
      udt_catalog
     </code>
     <code class="type">
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
     <code class="structfield">
      udt_schema
     </code>
     <code class="type">
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
     <code class="structfield">
      udt_name
     </code>
     <code class="type">
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
     <code class="structfield">
      privilege_type
     </code>
     <code class="type">
      character_data
     </code>
    </p>
    <p>
     Always
     <code class="literal">
      TYPE USAGE
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      is_grantable
     </code>
     <code class="type">
      yes_or_no
     </code>
    </p>
    <p>
     <code class="literal">
      YES
     </code>
     if the privilege is grantable,
     <code class="literal">
      NO
     </code>
     if not
    </p>
   </td>
  </tr>
 </tbody>
</table>





