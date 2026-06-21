## 52.29. `pg_language` [#](#CATALOG-PG-LANGUAGE)

The catalog `pg_language` registers languages in which you can write functions or stored procedures. See [CREATE LANGUAGE](sql-createlanguage.md "CREATE LANGUAGE") and [Chapter 40](xplang.md "Chapter 40. Procedural Languages") for more information about language handlers.

**Table 52.29. `pg_language` Columns**



<table border="1" class="table" summary="pg_language Columns">
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
      lanname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Name of the language
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      lanowner
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
     Owner of the language
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      lanispl
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     This is false for internal languages (such as
     <acronym class="acronym">
      SQL
     </acronym>
     ) and true for user-defined languages.
       Currently,
     <span class="application">
      pg_dump
     </span>
     still uses this to determine which languages need to be dumped, but this might be replaced by a different mechanism in the future.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      lanpltrusted
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     True if this is a trusted language, which means that it is believed not to grant access to anything outside the normal SQL execution environment.  Only superusers can create functions in untrusted languages.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      lanplcallfoid
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     For noninternal languages this references the language handler, which is a special function that is responsible for executing all functions that are written in the particular language. Zero for internal languages.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      laninline
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     This references a function that is responsible for executing
     <span class="quote">
      “
      <span class="quote">
       inline
      </span>
      ”
     </span>
     anonymous code blocks
       (
     <a class="xref" href="sql-do.md" title="DO">
      <span class="refentrytitle">
       DO
      </span>
     </a>
     blocks). Zero if inline blocks are not supported.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      lanvalidator
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     This references a language validator function that is responsible for checking the syntax and validity of new functions when they are created.  Zero if no validator is provided.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      lanacl
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

