## 53.15. `pg_policies` [#](#VIEW-PG-POLICIES)

The view `pg_policies` provides access to useful information about each row-level security policy in the database.

**Table 53.15. `pg_policies` Columns**



<table border="1" class="table" summary="pg_policies Columns">
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
      schemaname
     </code>
     <code class="type">
      name
     </code>
     (references
     <a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
      <code class="structname">
       pg_namespace
      </code>
     </a>
     .
     <code class="structfield">
      nspname
     </code>
     )
    </p>
    <p>
     Name of schema containing table policy is on
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      tablename
     </code>
     <code class="type">
      name
     </code>
     (references
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
       pg_class
      </code>
     </a>
     .
     <code class="structfield">
      relname
     </code>
     )
    </p>
    <p>
     Name of table policy is on
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      policyname
     </code>
     <code class="type">
      name
     </code>
     (references
     <a class="link" href="catalog-pg-policy.md" title="52.38. pg_policy">
      <code class="structname">
       pg_policy
      </code>
     </a>
     .
     <code class="structfield">
      polname
     </code>
     )
    </p>
    <p>
     Name of policy
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      permissive
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Is the policy permissive or restrictive?
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      roles
     </code>
     <code class="type">
      name[]
     </code>
    </p>
    <p>
     The roles to which this policy applies
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      cmd
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     The command type to which the policy is applied
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      qual
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     The expression added to the security barrier qualifications for queries that this policy applies to
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      with_check
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     The expression added to the WITH CHECK qualifications for queries that attempt to add rows to this table
    </p>
   </td>
  </tr>
 </tbody>
</table>

