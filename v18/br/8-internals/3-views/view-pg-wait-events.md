## 53.38. `pg_wait_events` [#](#VIEW-PG-WAIT-EVENTS)

A vista `pg_wait_events` fornece uma descrição sobre os eventos de espera.

**Tabela 53.38. Colunas `pg_wait_events`**



<table border="1" class="table" summary="pg_wait_events Columns">
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
      type
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Tipo de evento de espera
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      name
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Nome do evento em espera
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      description
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Descrição do evento de espera
    </p>
   </td>
  </tr>
 </tbody>
</table>





