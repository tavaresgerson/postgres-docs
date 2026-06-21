## 19.18. Opções Curtas [#](#RUNTIME-CONFIG-SHORT)

Para conveniência, também estão disponíveis opções de linha de comando com uma única letra para alguns parâmetros. Elas são descritas em [Tabela 19.5](runtime-config-short.md#RUNTIME-CONFIG-SHORT-TABLE). Algumas dessas opções existem por razões históricas, e sua presença como uma opção de uma única letra não indica necessariamente um endosso para usar a opção extensivamente.

**Tabela 19.5. Teclado de opção curto**



<table border="1" class="table" summary="Short Option Key">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Short Option
   </th>
   <th>
    Equivalent
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="option">
     -B
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    <code class="literal">
     shared_buffers =
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="option">
     -d
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    <code class="literal">
     log_min_messages = DEBUG
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="option">
     -e
    </code>
   </td>
   <td>
    <code class="literal">
     datestyle = euro
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="option">
     -fb
    </code>
    ,
    <code class="option">
     -fh
    </code>
    ,
    <code class="option">
     -fi
    </code>
    ,
    <code class="option">
     -fm
    </code>
    ,
    <code class="option">
     -fn
    </code>
    ,
    <code class="option">
     -fo
    </code>
    ,
    <code class="option">
     -fs
    </code>
    ,
    <code class="option">
     -ft
    </code>
   </td>
   <td>
    <code class="literal">
     enable_bitmapscan = off
    </code>
    ,
    <code class="literal">
     enable_hashjoin = off
    </code>
    ,
    <code class="literal">
     enable_indexscan = off
    </code>
    ,
    <code class="literal">
     enable_mergejoin = off
    </code>
    ,
    <code class="literal">
     enable_nestloop = off
    </code>
    ,
    <code class="literal">
     enable_indexonlyscan = off
    </code>
    ,
    <code class="literal">
     enable_seqscan = off
    </code>
    ,
    <code class="literal">
     enable_tidscan = off
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="option">
     -F
    </code>
   </td>
   <td>
    <code class="literal">
     fsync = off
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="option">
     -h
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    <code class="literal">
     listen_addresses =
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="option">
     -i
    </code>
   </td>
   <td>
    <code class="literal">
     listen_addresses = '*'
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="option">
     -k
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    <code class="literal">
     unix_socket_directories =
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="option">
     -l
    </code>
   </td>
   <td>
    <code class="literal">
     ssl = on
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="option">
     -N
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    <code class="literal">
     max_connections =
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="option">
     -O
    </code>
   </td>
   <td>
    <code class="literal">
     allow_system_table_mods = on
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="option">
     -p
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    <code class="literal">
     port =
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="option">
     -P
    </code>
   </td>
   <td>
    <code class="literal">
     ignore_system_indexes = on
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="option">
     -s
    </code>
   </td>
   <td>
    <code class="literal">
     log_statement_stats = on
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="option">
     -S
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    <code class="literal">
     work_mem =
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="option">
     -tpa
    </code>
    ,
    <code class="option">
     -tpl
    </code>
    ,
    <code class="option">
     -te
    </code>
   </td>
   <td>
    <code class="literal">
     log_parser_stats = on
    </code>
    ,
    <code class="literal">
     log_planner_stats = on
    </code>
    ,
    <code class="literal">
     log_executor_stats = on
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="option">
     -W
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    <code class="literal">
     post_auth_delay =
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
  </tr>
 </tbody>
</table>




