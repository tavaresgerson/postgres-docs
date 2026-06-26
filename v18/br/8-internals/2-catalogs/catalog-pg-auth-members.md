## 52.9. `pg_auth_members` [#](#CATALOG-PG-AUTH-MEMBERS)

O catálogo `pg_auth_members` mostra as relações de filiação entre os papéis. Qualquer conjunto não circular de relações é permitido.

Como as identidades dos usuários são globais para o clúster, o `pg_auth_members` é compartilhado em todos os bancos de dados de um clúster: há apenas uma cópia do `pg_auth_members` por clúster, não uma por banco de dados.

**Tabela 52.9. Colunas `pg_auth_members`**



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
      oid
     </code>
     <code>
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
     <code>
      roleid
     </code>
     <code>
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code>
       pg_authid
      </code>
     </a>
     .
     <code>
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
     <code>
      member
     </code>
     <code>
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code>
       pg_authid
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     ID of a role that is a member of
     <code>
      roleid
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      grantor
     </code>
     <code>
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code>
       pg_authid
      </code>
     </a>
     .
     <code>
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
     <code>
      admin_option
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     True if
     <code>
      member
     </code>
     can grant membership in
     <code>
      roleid
     </code>
     to others
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      inherit_option
     </code>
     <code>
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
     <code>
      set_option
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     True if the member can
     <a class="link" href="sql-set-role.md" title="SET ROLE">
      <code>
       SET ROLE
      </code>
     </a>
     to the granted role
    </p>
   </td>
  </tr>
 </tbody>
</table>





