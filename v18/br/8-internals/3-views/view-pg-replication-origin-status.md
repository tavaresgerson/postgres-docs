## 53.19. `pg_replication_origin_status` [#](#VIEW-PG-REPLICATION-ORIGIN-STATUS)

A visão `pg_replication_origin_status` contém informações sobre o progresso do replay para uma certa origem. Para mais informações sobre origens de replicação, consulte o [Capítulo 48](replication-origins.md).

**Tabela 53.19. Colunas `pg_replication_origin_status`**



<table>
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
     <code>
      local_id
     </code>
     <code>
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-replication-origin.md" title="52.44. pg_replication_origin">
      <code>
       pg_replication_origin
      </code>
     </a>
     .
     <code>
      roident
     </code>
     )
    </p>
    <p>
     internal node identifier
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      external_id
     </code>
     <code>
      text
     </code>
     (references
     <a class="link" href="catalog-pg-replication-origin.md" title="52.44. pg_replication_origin">
      <code>
       pg_replication_origin
      </code>
     </a>
     .
     <code>
      roname
     </code>
     )
    </p>
    <p>
     external node identifier
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      remote_lsn
     </code>
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     The origin node's LSN up to which data has been replicated.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      local_lsn
     </code>
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     This node's LSN at which
     <code>
      remote_lsn
     </code>
     has been replicated. Used to flush commit records before persisting data to disk when using asynchronous commits.
    </p>
   </td>
  </tr>
 </tbody>
</table>





