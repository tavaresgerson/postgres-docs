## 52.47. `pg_sequence` [#](#CATALOG-PG-SEQUENCE)

O catálogo `pg_sequence` contém informações sobre sequências. Algumas das informações sobre sequências, como o nome e o esquema, estão em [`pg_class`](catalog-pg-class.md "52.11. pg_class")

**Tabela 52.47. Colunas `pg_sequence`**



<table border="1" class="table" summary="pg_sequence Columns">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="catalog_table_entry">
    <p class="column_definition">
     Tipo de coluna
    </p>
    <p>
     Descrição
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      seqrelid
     </code>
     <code class="type">
      oid
     </code>
     (referências
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
     O OID do
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
       pg_class
      </code>
     </a>
     entrada para esta sequência
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      seqtypid
     </code>
     <code class="type">
      oid
     </code>
     (referências
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
     Tipo de dados da sequência
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      seqstart
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Valor inicial da sequência
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      seqincrement
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Valor incremental da sequência
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      seqmax
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Valor máximo da sequência
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      seqmin
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Valor mínimo da sequência
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      seqcache
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Tamanho de cache da sequência
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      seqcycle
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Se a sequência cicla
    </p>
   </td>
  </tr>
 </tbody>
</table>





