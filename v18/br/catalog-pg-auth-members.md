## 52.9. `pg_auth_members` [#](#CATALOG-PG-AUTH-MEMBERS)

O catálogo `pg_auth_members` mostra as relações de filiação entre os papéis. Qualquer conjunto não circular de relações é permitido.

Como as identidades dos usuários são globais para o clúster, o `pg_auth_members` é compartilhado em todos os bancos de dados de um clúster: há apenas uma cópia do `pg_auth_members` por clúster, não uma por banco de dados.

**Tabela 52.9. Colunas `pg_auth_members`**



<table border="1" class="table" summary="pg_auth_members Columns">
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
      oid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     Row identifier
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      roleid
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code class="structname">
       pg_authid
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     ID of a role that has a member
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      member
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code class="structname">
       pg_authid
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     ID of a role that is a member of
     <code class="structfield">
      roleid
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      grantor
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code class="structname">
       pg_authid
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     ID of the role that granted this membership
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      admin_option
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     True if
     <code class="structfield">
      member
     </code>
     can grant membership in
     <code class="structfield">
      roleid
     </code>
     to others
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      inherit_option
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     True if the member automatically inherits the privileges of the granted role
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      set_option
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     True if the member can
     <a class="link" href="sql-set-role.md" title="SET ROLE">
      <code class="command">
       SET ROLE
      </code>
     </a>
     to the granted role
    </p>
   </td>
  </tr>
 </tbody>
</table>





