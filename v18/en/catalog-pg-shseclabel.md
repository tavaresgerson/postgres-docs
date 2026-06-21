## 52.50. `pg_shseclabel` [#](#CATALOG-PG-SHSECLABEL)

The catalog `pg_shseclabel` stores security labels on shared database objects. Security labels can be manipulated with the [`SECURITY LABEL`](sql-security-label.md "SECURITY LABEL") command. For an easier way to view security labels, see [Section 53.23](view-pg-seclabels.md "53.23. pg_seclabels").

See also [`pg_seclabel`](catalog-pg-seclabel.md "52.46. pg_seclabel"), which performs a similar function for security labels involving objects within a single database.

Unlike most system catalogs, `pg_shseclabel` is shared across all databases of a cluster: there is only one copy of `pg_shseclabel` per cluster, not one per database.

**Table 52.50. `pg_shseclabel` Columns**



<table border="1" class="table" summary="pg_shseclabel Columns">
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

