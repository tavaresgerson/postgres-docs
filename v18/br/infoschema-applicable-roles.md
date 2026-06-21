## 35.5. `applicable_roles` [#](#INFOSCHEMA-APPLICABLE-ROLES)

A visão `applicable_roles` identifica todos os papéis cujos privilégios o usuário atual pode usar. Isso significa que há uma cadeia de concessões de papel do usuário atual para o papel em questão. O próprio usuário atual também é um papel aplicável. O conjunto de papéis aplicáveis é geralmente usado para verificação de permissão.

**Tabela 35.3. Colunas `applicable_roles`**



<table border="1" class="table" summary="applicable_roles Columns">
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
      grantee
     </code>
     <code class="type">
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
     <code class="structfield">
      role_name
     </code>
     <code class="type">
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
     if the grantee has the admin option on the role,
     <code class="literal">
      NO
     </code>
     if not
    </p>
   </td>
  </tr>
 </tbody>
</table>




