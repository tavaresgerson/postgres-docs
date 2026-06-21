## 52.31. `pg_largeobject_metadata` [#](#CATALOG-PG-LARGEOBJECT-METADATA)

The catalog `pg_largeobject_metadata` holds metadata associated with large objects. The actual large object data is stored in [`pg_largeobject`](catalog-pg-largeobject.md "52.30. pg_largeobject").

**Table 52.31. `pg_largeobject_metadata` Columns**



<table border="1" class="table" summary="pg_largeobject_metadata Columns">
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
      lomowner
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
     Owner of the large object
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      lomacl
     </code>
     <code class="type">
      aclitem[]
     </code>
    </p>
    <p>
     Access privileges; see
     <a class="xref" href="ddl-priv.md" title="5.8. Privileges">
      Section 5.8
     </a>
     for details
    </p>
   </td>
  </tr>
 </tbody>
</table>

