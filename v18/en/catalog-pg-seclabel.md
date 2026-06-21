## 52.46. `pg_seclabel` [#](#CATALOG-PG-SECLABEL)

The catalog `pg_seclabel` stores security labels on database objects. Security labels can be manipulated with the [`SECURITY LABEL`](sql-security-label.md "SECURITY LABEL") command. For an easier way to view security labels, see [Section 53.23](view-pg-seclabels.md "53.23. pg_seclabels").

See also [`pg_shseclabel`](catalog-pg-shseclabel.md "52.50. pg_shseclabel"), which performs a similar function for security labels of database objects that are shared across a database cluster.

**Table 52.46. `pg_seclabel` Columns**



<table border="1" class="table" summary="pg_seclabel Columns">
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
      objoid
     </code>
     <code class="type">
      oid
     </code>
     (references any OID column)
    </p>
    <p>
     The OID of the object this security label pertains to
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      classoid
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
       pg_class
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     The OID of the system catalog this object appears in
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      objsubid
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     For a security label on a table column, this is the column number (the
     <code class="structfield">
      objoid
     </code>
     and
     <code class="structfield">
      classoid
     </code>
     refer to
       the table itself).  For all other object types, this column is zero.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      provider
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     The label provider associated with this label.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      label
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     The security label applied to this object.
    </p>
   </td>
  </tr>
 </tbody>
</table>

