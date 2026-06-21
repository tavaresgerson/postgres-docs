## 52.40. `pg_publication` [#](#CATALOG-PG-PUBLICATION)

The catalog `pg_publication` contains all publications created in the database. For more on publications see [Section 29.1](logical-replication-publication.md "29.1. Publication").

**Table 52.40. `pg_publication` Columns**



<table border="1" class="table" summary="pg_publication Columns">
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
      oid
     </code>
     <code class="type">
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
     <code class="structfield">
      pubname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Name of the publication
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      pubowner
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code class="structname">
       pg_authid
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Owner of the publication
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      puballtables
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     If true, this publication automatically includes all tables in the database, including any that will be created in the future.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      pubinsert
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     If true,
     <a class="xref" href="sql-insert.md" title="INSERT">
      <span class="refentrytitle">
       INSERT
      </span>
     </a>
     operations are replicated for tables in the publication.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      pubupdate
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     If true,
     <a class="xref" href="sql-update.md" title="UPDATE">
      <span class="refentrytitle">
       UPDATE
      </span>
     </a>
     operations are replicated for tables in the publication.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      pubdelete
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     If true,
     <a class="xref" href="sql-delete.md" title="DELETE">
      <span class="refentrytitle">
       DELETE
      </span>
     </a>
     operations are replicated for tables in the publication.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      pubtruncate
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     If true,
     <a class="xref" href="sql-truncate.md" title="TRUNCATE">
      <span class="refentrytitle">
       TRUNCATE
      </span>
     </a>
     operations are replicated for tables in the publication.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      pubviaroot
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     If true, operations on a leaf partition are replicated using the identity and schema of its topmost partitioned ancestor mentioned in the publication instead of its own.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      pubgencols
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Controls how to handle generated column replication when there is no publication column list:
     <code class="literal">
      n
     </code>
     = generated columns in the tables associated with
       the publication should not be replicated,
     <code class="literal">
      s
     </code>
     = stored generated columns in the tables associated
       with the publication should be replicated.
    </p>
   </td>
  </tr>
 </tbody>
</table>

