## 53.27. `pg_shmem_allocations` [#](#VIEW-PG-SHMEM-ALLOCATIONS)

A visualização `pg_shmem_allocations` mostra as alocações feitas a partir do segmento principal de memória compartilhada do servidor. Isso inclui tanto a memória alocada pelo PostgreSQL quanto a memória alocada por extensões usando os mecanismos detalhados na [Seção 36.10.11](xfunc-c.md#XFUNC-SHARED-ADDIN).

Observe que essa visão não inclui a memória alocada usando a infraestrutura de memória compartilhada dinâmica.

**Tabela 53.27. Colunas `pg_shmem_allocations`**



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
      name
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     O nome da alocação de memória compartilhada. NULL para memória não utilizada e
     <code>
      &lt;anonymous&gt;
     </code>
     para alocações anônimas.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      off
     </code>
     <code>
      int8
     </code>
    </p>
    <p>
     O deslocamento em que a alocação começa. NULL para alocações anônimas, uma vez que os detalhes relacionados a elas não são conhecidos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      size
     </code>
     <code>
      int8
     </code>
    </p>
    <p>
     Tamanho da alocação em bytes
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      allocated_size
     </code>
     <code>
      int8
     </code>
    </p>
    <p>
     Tamanho da alocação em bytes, incluindo o preenchimento. Para alocações anônimas, não há informações sobre o preenchimento, então
     <code>
      size
     </code>
     e
     <code>
      allocated_size
     </code>
     As colunas sempre serão iguais. O preenchimento não é significativo para memória livre, então as colunas serão iguais nesse caso também.
    </p>
   </td>
  </tr>
 </tbody>
</table>










As alocações anônimas são as alocações que foram feitas diretamente com `ShmemAlloc()`, em vez de através de `ShmemInitStruct()` ou `ShmemInitHash()`.

Por padrão, a visualização `pg_shmem_allocations` pode ser lida apenas por superusuários ou papéis com privilégios da função `pg_read_all_stats`.