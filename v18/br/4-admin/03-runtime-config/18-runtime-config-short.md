## 19.18. Opções Curtas [#](#RUNTIME-CONFIG-SHORT)

Para conveniência, também estão disponíveis opções de linha de comando com uma única letra para alguns parâmetros. Elas são descritas em [Tabela 19.5](runtime-config-short.md#RUNTIME-CONFIG-SHORT-TABLE). Algumas dessas opções existem por razões históricas, e sua presença como uma opção de uma única letra não indica necessariamente um endosso para usar a opção extensivamente.

**Tabela 19.5. Teclado de opção curto**



<table>
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
    <code>
     -B
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    <code>
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
    <code>
     -d
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    <code>
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
    <code>
     -e
    </code>
   </td>
   <td>
    <code>
     datestyle = euro
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     -fb
    </code>
    ,
    <code>
     -fh
    </code>
    ,
    <code>
     -fi
    </code>
    ,
    <code>
     -fm
    </code>
    ,
    <code>
     -fn
    </code>
    ,
    <code>
     -fo
    </code>
    ,
    <code>
     -fs
    </code>
    ,
    <code>
     -ft
    </code>
   </td>
   <td>
    <code>
     enable_bitmapscan = off
    </code>
    ,
    <code>
     enable_hashjoin = off
    </code>
    ,
    <code>
     enable_indexscan = off
    </code>
    ,
    <code>
     enable_mergejoin = off
    </code>
    ,
    <code>
     enable_nestloop = off
    </code>
    ,
    <code>
     enable_indexonlyscan = off
    </code>
    ,
    <code>
     enable_seqscan = off
    </code>
    ,
    <code>
     enable_tidscan = off
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     -F
    </code>
   </td>
   <td>
    <code>
     fsync = off
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     -h
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    <code>
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
    <code>
     -i
    </code>
   </td>
   <td>
    <code>
     listen_addresses = '*'
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     -k
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    <code>
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
    <code>
     -l
    </code>
   </td>
   <td>
    <code>
     ssl = on
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     -N
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    <code>
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
    <code>
     -O
    </code>
   </td>
   <td>
    <code>
     allow_system_table_mods = on
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     -p
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    <code>
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
    <code>
     -P
    </code>
   </td>
   <td>
    <code>
     ignore_system_indexes = on
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     -s
    </code>
   </td>
   <td>
    <code>
     log_statement_stats = on
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     -S
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    <code>
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
    <code>
     -tpa
    </code>
    ,
    <code>
     -tpl
    </code>
    ,
    <code>
     -te
    </code>
   </td>
   <td>
    <code>
     log_parser_stats = on
    </code>
    ,
    <code>
     log_planner_stats = on
    </code>
    ,
    <code>
     log_executor_stats = on
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     -W
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    <code>
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





