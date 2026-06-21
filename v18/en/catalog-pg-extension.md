## 52.22. `pg_extension` [#](#CATALOG-PG-EXTENSION)

The catalog `pg_extension` stores information about the installed extensions. See [Section 36.17](extend-extensions.md "36.17. Packaging Related Objects into an Extension") for details about extensions.

**Table 52.22. `pg_extension` Columns**



<table border="1" class="table" summary="pg_extension Columns">
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
      extname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Name of the extension
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      extowner
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
     Owner of the extension
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      extnamespace
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
      <code class="structname">
       pg_namespace
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Schema containing the extension's exported objects
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      extrelocatable
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     True if extension can be relocated to another schema
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      extversion
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Version name for the extension
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      extconfig
     </code>
     <code class="type">
      oid[]
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
     Array of
     <code class="type">
      regclass
     </code>
     OIDs for the extension's configuration table(s), or
     <code class="literal">
      NULL
     </code>
     if none
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      extcondition
     </code>
     <code class="type">
      text[]
     </code>
    </p>
    <p>
     Array of
     <code class="literal">
      WHERE
     </code>
     -clause filter conditions for the extension's configuration table(s), or
     <code class="literal">
      NULL
     </code>
     if none
    </p>
   </td>
  </tr>
 </tbody>
</table>




  

Note that unlike most catalogs with a “namespace” column, `extnamespace` is not meant to imply that the extension belongs to that schema. Extension names are never schema-qualified. Rather, `extnamespace` indicates the schema that contains most or all of the extension's objects. If `extrelocatable` is true, then this schema must in fact contain all schema-qualifiable objects belonging to the extension.
