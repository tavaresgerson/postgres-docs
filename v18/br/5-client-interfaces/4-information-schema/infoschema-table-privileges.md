## 35.53. `table_privileges` [#](#INFOSCHEMA-TABLE-PRIVILEGES)

A vista `table_privileges` identifica todos os privilégios concedidos em tabelas ou vistas a um papel atualmente habilitado ou por um papel atualmente habilitado. Há uma linha para cada combinação de tabela, concedente e beneficiário.

**Tabela 35.51. Colunas `table_privileges`**



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
      table_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that contains the table (always the current database)
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
     Name of the schema that contains the table
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
     Name of the table
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
     Type of the privilege:
     <code>
      SELECT
     </code>
     ,
     <code>
      INSERT
     </code>
     ,
     <code>
      UPDATE
     </code>
     ,
     <code>
      DELETE
     </code>
     ,
     <code>
      TRUNCATE
     </code>
     ,
     <code>
      REFERENCES
     </code>
     , or
     <code>
      TRIGGER
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
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      with_hierarchy
     </code>
     <code>
      yes_or_no
     </code>
    </p>
    <p>
     In the SQL standard,
     <code>
      WITH HIERARCHY OPTION
     </code>
     is a separate (sub-)privilege allowing certain operations on table inheritance hierarchies.  In PostgreSQL, this is included in the
     <code>
      SELECT
     </code>
     privilege, so this column shows
     <code>
      YES
     </code>
     if the privilege is
     <code>
      SELECT
     </code>
     , else
     <code>
      NO
     </code>
     .
    </p>
   </td>
  </tr>
 </tbody>
</table>





