## 53.14. `pg_matviews` [#](#VIEW-PG-MATVIEWS)

The view `pg_matviews` provides access to useful information about each materialized view in the database.

**Table 53.14. `pg_matviews` Columns**



<table border="1" class="table" summary="pg_matviews Columns">
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
     Name of schema containing materialized view
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      matviewname
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
     Name of materialized view
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      matviewowner
     </code>
     <code class="type">
      name
     </code>
     (references
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code class="structname">
       pg_authid
      </code>
     </a>
     .
     <code class="structfield">
      rolname
     </code>
     )
    </p>
    <p>
     Name of materialized view's owner
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      tablespace
     </code>
     <code class="type">
      name
     </code>
     (references
     <a class="link" href="catalog-pg-tablespace.md" title="52.56. pg_tablespace">
      <code class="structname">
       pg_tablespace
      </code>
     </a>
     .
     <code class="structfield">
      spcname
     </code>
     )
    </p>
    <p>
     Name of tablespace containing materialized view (null if default for database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      hasindexes
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     True if materialized view has (or recently had) any indexes
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      ispopulated
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     True if materialized view is currently populated
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
     Materialized view definition (a reconstructed
     <a class="xref" href="sql-select.md" title="SELECT">
      <span class="refentrytitle">
       SELECT
      </span>
     </a>
     query)
    </p>
   </td>
  </tr>
 </tbody>
</table>

