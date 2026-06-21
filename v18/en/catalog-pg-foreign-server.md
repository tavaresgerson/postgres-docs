## 52.24. `pg_foreign_server` [#](#CATALOG-PG-FOREIGN-SERVER)

The catalog `pg_foreign_server` stores foreign server definitions. A foreign server describes a source of external data, such as a remote server. Foreign servers are accessed via foreign-data wrappers.

**Table 52.24. `pg_foreign_server` Columns**



<table border="1" class="table" summary="pg_foreign_server Columns">
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
      srvname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Name of the foreign server
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      srvowner
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
     Owner of the foreign server
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      srvfdw
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-foreign-data-wrapper.md" title="52.23. pg_foreign_data_wrapper">
      <code class="structname">
       pg_foreign_data_wrapper
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     OID of the foreign-data wrapper of this foreign server
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      srvtype
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Type of the server (optional)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      srvversion
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Version of the server (optional)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      srvacl
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
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      srvoptions
     </code>
     <code class="type">
      text[]
     </code>
    </p>
    <p>
     Foreign server specific options, as
     <span class="quote">
      “
      <span class="quote">
       keyword=value
      </span>
      ”
     </span>
     strings
    </p>
   </td>
  </tr>
 </tbody>
</table>

