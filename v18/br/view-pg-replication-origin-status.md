## 53.19. `pg_replication_origin_status` [#](#VIEW-PG-REPLICATION-ORIGIN-STATUS)

A visão `pg_replication_origin_status` contém informações sobre o progresso do replay para uma certa origem. Para mais informações sobre origens de replicação, consulte o Capítulo 48 [(replication-origins.md "Chapter 48. Replication Progress Tracking")].

**Tabela 53.19. Colunas `pg_replication_origin_status`**



<table border="1" class="table" summary="pg_replication_origin_status Columns">
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
      local_id
     </code>
<code class="type">
      oid
     </code>
     (references
     <a class="link" href="catalog-pg-replication-origin.md" title="52.44. pg_replication_origin">
<code class="structname">
       pg_replication_origin
      </code>
</a>
     .
     <code class="structfield">
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
<code class="structfield">
      external_id
     </code>
<code class="type">
      text
     </code>
     (references
     <a class="link" href="catalog-pg-replication-origin.md" title="52.44. pg_replication_origin">
<code class="structname">
       pg_replication_origin
      </code>
</a>
     .
     <code class="structfield">
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
<code class="structfield">
      remote_lsn
     </code>
<code class="type">
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
<code class="structfield">
      local_lsn
     </code>
<code class="type">
      pg_lsn
     </code>
</p>
<p>
     This node's LSN at which
     <code class="literal">
      remote_lsn
     </code>
     has been replicated. Used to flush commit records before persisting data to disk when using asynchronous commits.
    </p>
</td>
</tr>
</tbody>
</table>

