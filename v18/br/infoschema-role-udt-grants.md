## 35.38. `role_udt_grants` [#](#INFOSCHEMA-ROLE-UDT-GRANTS)

A vista `role_udt_grants` destina-se a identificar privilégios `USAGE` concedidos em tipos definidos pelo usuário, onde o concedente ou o beneficiário é um papel atualmente habilitado. Mais informações podem ser encontradas em `udt_privileges`. A única diferença efetiva entre esta vista e `udt_privileges` é que esta vista omite objetos que foram tornados acessíveis ao usuário atual por meio de uma concessão para `PUBLIC`. Como os tipos de dados não têm privilégios reais no PostgreSQL, mas apenas uma concessão implícita para `PUBLIC`, esta vista está vazia.

**Tabela 35.36. Colunas `role_udt_grants`**



<table border="1" class="table" summary="role_udt_grants Columns">
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
     The name of the role that granted the privilege
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
     The name of the role that the privilege was granted to
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





