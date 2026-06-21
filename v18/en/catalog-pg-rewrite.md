## 52.45. `pg_rewrite` [#](#CATALOG-PG-REWRITE)

The catalog `pg_rewrite` stores rewrite rules for tables and views.

**Table 52.45. `pg_rewrite` Columns**



<table border="1" class="table" summary="pg_rewrite Columns">
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
      rulename
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Rule name
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      ev_class
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
     The table this rule is for
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      ev_type
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Event type that the rule is for: 1 =
     <a class="xref" href="sql-select.md" title="SELECT">
      <span class="refentrytitle">
       SELECT
      </span>
     </a>
     , 2 =
     <a class="xref" href="sql-update.md" title="UPDATE">
      <span class="refentrytitle">
       UPDATE
      </span>
     </a>
     , 3 =
     <a class="xref" href="sql-insert.md" title="INSERT">
      <span class="refentrytitle">
       INSERT
      </span>
     </a>
     , 4 =
     <a class="xref" href="sql-delete.md" title="DELETE">
      <span class="refentrytitle">
       DELETE
      </span>
     </a>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      ev_enabled
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Controls in which
     <a class="xref" href="runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE">
      session_replication_role
     </a>
     modes the rule fires.
     <code class="literal">
      O
     </code>
     = rule fires in
     <span class="quote">
      “
      <span class="quote">
       origin
      </span>
      ”
     </span>
     and
     <span class="quote">
      “
      <span class="quote">
       local
      </span>
      ”
     </span>
     modes,
     <code class="literal">
      D
     </code>
     = rule is disabled,
     <code class="literal">
      R
     </code>
     = rule fires in
     <span class="quote">
      “
      <span class="quote">
       replica
      </span>
      ”
     </span>
     mode,
     <code class="literal">
      A
     </code>
     = rule fires always.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      is_instead
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     True if the rule is an
     <code class="literal">
      INSTEAD
     </code>
     rule
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      ev_qual
     </code>
     <code class="type">
      pg_node_tree
     </code>
    </p>
    <p>
     Expression tree (in the form of a
     <code class="function">
      nodeToString()
     </code>
     representation) for the
       rule's qualifying condition
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      ev_action
     </code>
     <code class="type">
      pg_node_tree
     </code>
    </p>
    <p>
     Query tree (in the form of a
     <code class="function">
      nodeToString()
     </code>
     representation) for the
       rule's action
    </p>
   </td>
  </tr>
 </tbody>
</table>




  

### Note

`pg_class.relhasrules` must be true if a table has any rules in this catalog.
