## 52.47. `pg_sequence` [#](#CATALOG-PG-SEQUENCE)

O catálogo `pg_sequence` contém informações sobre sequências. Algumas das informações sobre sequências, como o nome e o esquema, estão em [`pg_class`](catalog-pg-class.md "52.11. pg_class")

**Tabela 52.47. Colunas `pg_sequence`**



<table>
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
     <code>
      seqrelid
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code>
       pg_class
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     O OID do
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code>
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
     <code>
      seqtypid
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code>
       pg_type
      </code>
     </a>
     .
     <code>
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
     <code>
      seqstart
     </code>
     <code>
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
     <code>
      seqincrement
     </code>
     <code>
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
     <code>
      seqmax
     </code>
     <code>
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
     <code>
      seqmin
     </code>
     <code>
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
     <code>
      seqcache
     </code>
     <code>
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
     <code>
      seqcycle
     </code>
     <code>
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





