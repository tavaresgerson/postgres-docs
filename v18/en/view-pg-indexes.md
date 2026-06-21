## 53.12. `pg_indexes` [#](#VIEW-PG-INDEXES)

The view `pg_indexes` provides access to useful information about each index in the database.

**Table 53.12. `pg_indexes` Columns**



<table border="1" class="table" summary="pg_indexes Columns">
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
     Name of schema containing table and index
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
     Name of table the index is for
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      indexname
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
     Name of index
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
     Name of tablespace containing index (null if default for database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      indexdef
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Index definition (a reconstructed
     <a class="xref" href="sql-createindex.md" title="CREATE INDEX">
      <span class="refentrytitle">
       CREATE INDEX
      </span>
     </a>
     command)
    </p>
   </td>
  </tr>
 </tbody>
</table>

