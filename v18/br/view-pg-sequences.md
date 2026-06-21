## 53.24. `pg_sequences` [#](#VIEW-PG-SEQUENCES)

A vista `pg_sequences` fornece acesso a informações úteis sobre cada sequência no banco de dados.

**Tabela 53.24. Colunas `pg_sequences`**



<table border="1" class="table" summary="pg_sequences Columns">
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
     Name of schema containing sequence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      sequencename
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
     Name of sequence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      sequenceowner
     </code>
     <code class="type">
      name
     </code>
     (references
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code class="structname">
       pg_authid
      </code>
     </a>
     .
     <code class="structfield">
      rolname
     </code>
     )
    </p>
    <p>
     Name of sequence's owner
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      data_type
     </code>
     <code class="type">
      regtype
     </code>
     (references
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code class="structname">
       pg_type
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Data type of the sequence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      start_value
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Start value of the sequence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      min_value
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Minimum value of the sequence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      max_value
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Maximum value of the sequence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      increment_by
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Increment value of the sequence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      cycle
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Whether the sequence cycles
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      cache_size
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Cache size of the sequence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      last_value
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     The last sequence value written to disk.  If caching is used, this value can be greater than the last value handed out from the sequence.
    </p>
   </td>
  </tr>
 </tbody>
</table>









A coluna `last_value` será considerada nula se qualquer uma das seguintes condições for verdadeira:

* A sequência ainda não foi lida. * O usuário atual não tem privilégio `USAGE` ou `SELECT` na sequência. * A sequência não está registrada e o servidor está em standby.