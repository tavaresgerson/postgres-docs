## 35.4. `administrable_role_​authorizations` [#](#INFOSCHEMA-ADMINISTRABLE-ROLE-AUTHORIZATIONS)

The view `administrable_role_authorizations` identifies all roles that the current user has the admin option for.

**Table 35.2. `administrable_role_authorizations` Columns**



<table border="1" class="table" summary="administrable_role_authorizations Columns">
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
     Always
     <code class="literal">
      YES
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>

