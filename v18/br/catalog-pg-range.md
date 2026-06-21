## 52.43. `pg_range` [#](#CATALOG-PG-RANGE)

O catálogo `pg_range` armazena informações sobre os tipos de faixa. Isso é adicional às entradas dos tipos em [`pg_type`](catalog-pg-type.md "52.64. pg_type").

**Tabela 52.43. Colunas `pg_range`**



<table border="1" class="table" summary="pg_range Columns">
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
      rngtypid
     </code>
     <code class="type">
      oid
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
     OID of the range type
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rngsubtype
     </code>
     <code class="type">
      oid
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
     OID of the element type (subtype) of this range type
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rngmultitypid
     </code>
     <code class="type">
      oid
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
     OID of the multirange type for this range type
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rngcollation
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-collation.md" title="52.12. pg_collation">
      <code class="structname">
       pg_collation
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     OID of the collation used for range comparisons, or zero if none
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rngsubopc
     </code>
     <code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-opclass.md" title="52.33. pg_opclass">
      <code class="structname">
       pg_opclass
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     OID of the subtype's operator class used for range comparisons
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rngcanonical
     </code>
     <code class="type">
      regproc
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
     OID of the function to convert a range value into canonical form, or zero if none
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rngsubdiff
     </code>
     <code class="type">
      regproc
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
     OID of the function to return the difference between two element values as
     <code class="type">
      double precision
     </code>
     , or zero if none
    </p>
   </td>
  </tr>
 </tbody>
</table>










`rngsubopc` (mais `rngcollation`, se o tipo de elemento for coletável) determina a ordem de classificação usada pelo tipo de intervalo. `rngcanonical` é usado quando o tipo de elemento é discreto. `rngsubdiff` é opcional, mas deve ser fornecido para melhorar o desempenho dos índices GiST no tipo de intervalo.