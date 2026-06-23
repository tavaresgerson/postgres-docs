## 53.28. `pg_shmem_allocations_numa` [#](#VIEW-PG-SHMEM-ALLOCATIONS-NUMA)

O `pg_shmem_allocations_numa` mostra como as alocações de memória compartilhada no segmento principal de memória compartilhada do servidor são distribuídas entre os nós NUMA. Isso inclui tanto a memória alocada pelo PostgreSQL quanto a memória alocada por extensões usando os mecanismos detalhados em [Seção 36.10.11](xfunc-c.md#XFUNC-SHARED-ADDIN). Esta visão exibirá várias linhas para cada um dos segmentos de memória compartilhada, desde que estejam espalhados em vários nós NUMA. Este tipo de visão não deve ser consultada por sistemas de monitoramento, pois é muito lenta e pode acabar alocando memória compartilhada, caso não tenha sido usada anteriormente. A limitação atual para essa visão é que ela não mostrará alocações de memória compartilhada anônima.

Observe que essa visão não inclui a memória alocada usando a infraestrutura de memória compartilhada dinâmica.

### Aviso

Ao determinar o nó NUMA, a visão toca todas as páginas de memória do segmento de memória compartilhada. Isso forçará a alocação da memória compartilhada, se não já tiver sido alocada, e a memória pode ser alocada em um único nó NUMA (dependendo da configuração do sistema).

**Tabela 53.28. Colunas `pg_shmem_allocations_numa`**



<table border="1" class="table" summary="pg_shmem_allocations_numa Columns">
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
      name
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     O nome da alocação de memória compartilhada.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      numa_node
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     ID de
     <acronym class="acronym">
      NUMA
     </acronym>
     nó
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      size
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Tamanho da alocação nesse nó de memória NUMA específico em bytes
    </p>
   </td>
  </tr>
 </tbody>
</table>










Por padrão, a visualização `pg_shmem_allocations_numa` pode ser lida apenas por superusuários ou papéis com privilégios da função `pg_read_all_stats`.