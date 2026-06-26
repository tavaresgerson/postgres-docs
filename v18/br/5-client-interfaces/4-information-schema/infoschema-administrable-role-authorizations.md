## 35.4. `administrable_role_​authorizations` [#](#INFOSCHEMA-ADMINISTRABLE-ROLE-AUTHORIZATIONS)

A vista `administrable_role_authorizations` identifica todos os papéis que o usuário atual tem a opção de administrador.

**Tabela 35.2. Colunas `administrable_role_authorizations`**



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
      grantee
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the role to which this role membership was granted (can be the current user, or a different role in case of nested role memberships)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      role_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of a role
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
     Always
     <code>
      YES
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>





