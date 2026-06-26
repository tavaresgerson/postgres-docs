## 53.9. `pg_group` [#](#VIEW-PG-GROUP)

A vista `pg_group` existe para compatibilidade reversa: ela emula um catálogo que existia no PostgreSQL antes da versão 8.1. Ela mostra os nomes e os membros de todos os papéis que são marcados como não `rolcanlogin`, que é uma aproximação do conjunto de papéis que estão sendo usados como grupos.

**Tabela 53.9. Colunas `pg_group`**



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
      groname
     </code>
     <code>
      name
     </code>
     (references
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code>
       pg_authid
      </code>
     </a>
     .
     <code>
      rolname
     </code>
     )
    </p>
    <p>
     Name of the group
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      grosysid
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
     ID of this group
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      grolist
     </code>
     <code>
      oid[]
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
     An array containing the IDs of the roles in this group
    </p>
   </td>
  </tr>
 </tbody>
</table>





