## 53.18. `pg_publication_tables` [#](#VIEW-PG-PUBLICATION-TABLES)

The view `pg_publication_tables` provides information about the mapping between publications and information of tables they contain. Unlike the underlying catalog [`pg_publication_rel`](catalog-pg-publication-rel.md "52.42. pg_publication_rel"), this view expands publications defined as [`FOR ALL TABLES`](sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-ALL-TABLES) and [`FOR TABLES IN SCHEMA`](sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLES-IN-SCHEMA), so for such publications there will be a row for each eligible table.

**Table 53.18. `pg_publication_tables` Columns**



<table border="1" class="table" summary="pg_publication_tables Columns">
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
      pubname
     </code>
     <code class="type">
      name
     </code>
     (references
     <a class="link" href="catalog-pg-publication.md" title="52.40. pg_publication">
      <code class="structname">
       pg_publication
      </code>
     </a>
     .
     <code class="structfield">
      pubname
     </code>
     )
    </p>
    <p>
     Name of publication
    </p>
   </td>
  </tr>
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
     Name of table
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      attnames
     </code>
     <code class="type">
      name[]
     </code>
     (references
     <a class="link" href="catalog-pg-attribute.md" title="52.7. pg_attribute">
      <code class="structname">
       pg_attribute
      </code>
     </a>
     .
     <code class="structfield">
      attname
     </code>
     )
    </p>
    <p>
     Names of table columns included in the publication. This contains all the columns of the table when the user didn't specify the column list for the table.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rowfilter
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Expression for the table's publication qualifying condition
    </p>
   </td>
  </tr>
 </tbody>
</table>

