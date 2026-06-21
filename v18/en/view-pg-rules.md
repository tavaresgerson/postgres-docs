## 53.22. `pg_rules` [#](#VIEW-PG-RULES)

The view `pg_rules` provides access to useful information about query rewrite rules.

**Table 53.22. `pg_rules` Columns**



<table border="1" class="table" summary="pg_rules Columns">
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
     Name of schema containing table
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
     Name of table the rule is for
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rulename
     </code>
     <code class="type">
      name
     </code>
     (references
     <a class="link" href="catalog-pg-rewrite.md" title="52.45. pg_rewrite">
      <code class="structname">
       pg_rewrite
      </code>
     </a>
     .
     <code class="structfield">
      rulename
     </code>
     )
    </p>
    <p>
     Name of rule
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      definition
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Rule definition (a reconstructed creation command)
    </p>
   </td>
  </tr>
 </tbody>
</table>




  

The `pg_rules` view excludes the `ON SELECT` rules of views and materialized views; those can be seen in [`pg_views`](view-pg-views.md "53.37. pg_views") and [`pg_matviews`](view-pg-matviews.md "53.14. pg_matviews").
