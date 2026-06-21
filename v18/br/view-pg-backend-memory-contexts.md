## 53.5. `pg_backend_memory_contexts` [#](#VIEW-PG-BACKEND-MEMORY-CONTEXTS)

A vista `pg_backend_memory_contexts` exibe todos os contextos de memória do processo do servidor vinculado à sessão atual.

`pg_backend_memory_contexts` contém uma linha para cada contexto de memória.

**Tabela 53.5. Colunas `pg_backend_memory_contexts`**



<table border="1" class="table" summary="pg_backend_memory_contexts Columns">
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
     Nome do contexto de memória
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      ident
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Informações de identificação do contexto de memória. Este campo é truncado em 1024 bytes
    </p>
   </td>
  </tr>
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
     Tipo do contexto de memória
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      level
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     O nível de 1 da contexto na hierarquia do contexto de memória. O nível de um contexto também mostra a posição desse contexto na
     <code class="structfield">
      path
     </code>
     column.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      path
     </code>
     <code class="type">
      int4[]
     </code>
    </p>
    <p>
     Conjunto de identificadores numéricos transitórios para descrever a hierarquia do contexto de memória. O primeiro elemento é para
     <code class="literal">
      TopMemoryContext
     </code>
     Os elementos subsequentes contêm pais intermediários e o elemento final contém o identificador do contexto atual.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      total_bytes
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Bytes totais alocados para este contexto de memória
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      total_nblocks
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Número total de blocos alocados para este contexto de memória
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      free_bytes
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Espaço livre em bytes
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      free_chunks
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Número total de blocos livres
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      used_bytes
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Espaço utilizado em bytes
    </p>
   </td>
  </tr>
 </tbody>
</table>









Por padrão, a visualização `pg_backend_memory_contexts` pode ser lida apenas por superusuários ou papéis com os privilégios do papel `pg_read_all_stats`.

Como os contextos de memória são criados e destruídos durante a execução de uma consulta, os identificadores armazenados na coluna `path` podem ser instáveis entre múltiplas invocações da visão na mesma consulta. O exemplo abaixo demonstra um uso eficaz desta coluna e calcula o número total de bytes usados por `CacheMemoryContext` e todos os seus filhos:

```
WITH memory_contexts AS (
    SELECT * FROM pg_backend_memory_contexts
)
SELECT sum(c1.total_bytes)
FROM memory_contexts c1, memory_contexts c2
WHERE c2.name = 'CacheMemoryContext'
AND c1.path[c2.level] = c2.path[c2.level];
```

A expressão de tabela comum (Common Table Expression) ((queries-with.md "7.8. WITH Queries (Common Table Expressions)) é usada para garantir que os IDs de contexto na coluna `path` correspondam entre ambas as avaliações da visualização.