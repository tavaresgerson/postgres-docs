## 53.2. `pg_aios` [#](#VIEW-PG-AIOS)

A visão `pg_aios` lista todos os [Tratamento de E/S assíncrono](glossary.md#GLOSSARY-AIO "Asynchronous I/O") que estão atualmente em uso. Um tratamento de E/S é usado para referenciar uma operação de E/S que está sendo preparada, executada ou está em processo de conclusão. `pg_aios` contém uma linha para cada tratamento de E/S.

Essa visão é principalmente útil para desenvolvedores do PostgreSQL, mas também pode ser útil ao ajustar o PostgreSQL.

**Tabela 53.2. Colunas `pg_aios`**



<table border="1" class="table" summary="pg_aios Columns">
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
      pid
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Process ID of the server process that is issuing this I/O.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      io_id
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Identifier of the I/O handle. Handles are reused once the I/O completed (or if the handle is released before I/O is started). On reuse
     <a class="link" href="view-pg-aios.md#VIEW-PG-AIOS-IO-GENERATION">
      <code class="structname">
       pg_aios
      </code>
      .
      <code class="structfield">
       io_generation
      </code>
     </a>
     is incremented.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry" id="VIEW-PG-AIOS-IO-GENERATION">
    <p class="column_definition">
     <code class="structfield">
      io_generation
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Generation of the I/O handle.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      state
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     State of the I/O handle:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        <code class="literal">
         HANDED_OUT
        </code>
        , referenced by code but not yet used
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         DEFINED
        </code>
        , information necessary for execution is known
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         STAGED
        </code>
        , ready for execution
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         SUBMITTED
        </code>
        , submitted for execution
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         COMPLETED_IO
        </code>
        , finished, but result has not yet been processed
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         COMPLETED_SHARED
        </code>
        , shared completion processing completed
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         COMPLETED_LOCAL
        </code>
        , backend local completion processing completed
       </p>
      </li>
     </ul>
    </div>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      operation
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Operation performed using the I/O handle:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        <code class="literal">
         invalid
        </code>
        , not yet known
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         readv
        </code>
        , a vectored read
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         writev
        </code>
        , a vectored write
       </p>
      </li>
     </ul>
    </div>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      off
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Offset of the I/O operation.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      length
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     Length of the I/O operation.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      target
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     What kind of object is the I/O targeting:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist compact" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        <code class="literal">
         smgr
        </code>
        , I/O on relations
       </p>
      </li>
     </ul>
    </div>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      handle_data_len
     </code>
     <code class="type">
      int2
     </code>
    </p>
    <p>
     Length of the data associated with the I/O operation. For I/O to/from
     <a class="xref" href="runtime-config-resource.md#GUC-SHARED-BUFFERS">
      shared_buffers
     </a>
     and
     <a class="xref" href="runtime-config-resource.md#GUC-TEMP-BUFFERS">
      temp_buffers
     </a>
     , this indicates the number of buffers the I/O is operating on.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      raw_result
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Low-level result of the I/O operation, or NULL if the operation has not yet completed.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      result
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     High-level result of the I/O operation:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        <code class="literal">
         UNKNOWN
        </code>
        means that the result of the operation is not yet known.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         OK
        </code>
        means the I/O completed successfully.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         PARTIAL
        </code>
        means that the I/O completed without error, but did not process all data. Commonly callers will need to retry and perform the remainder of the work in a separate I/O.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         WARNING
        </code>
        means that the I/O completed without error, but that execution of the IO triggered a warning. E.g. when encountering a corrupted buffer with
        <a class="xref" href="runtime-config-developer.md#GUC-ZERO-DAMAGED-PAGES">
         zero_damaged_pages
        </a>
        enabled.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         ERROR
        </code>
        means the I/O failed with an error.
       </p>
      </li>
     </ul>
    </div>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      target_desc
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Description of what the I/O operation is targeting.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      f_sync
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Flag indicating whether the I/O is executed synchronously.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      f_localmem
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Flag indicating whether the I/O references process local memory.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      f_buffered
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Flag indicating whether the I/O is buffered I/O.
    </p>
   </td>
  </tr>
 </tbody>
</table>









A visão `pg_aios` é somente de leitura.

Por padrão, a visualização `pg_aios` pode ser lida apenas por superusuários ou papéis com privilégios da função `pg_read_all_stats`.