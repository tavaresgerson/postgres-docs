## 53.20. `pg_replication_slots` [#](#VIEW-PG-REPLICATION-SLOTS)

A visualização `pg_replication_slots` fornece uma lista de todos os slots de replicação que atualmente existem no clúster de banco de dados, juntamente com seu estado atual.

Para mais informações sobre slots de replicação, consulte [Seção 26.2.6](warm-standby.md#STREAMING-REPLICATION-SLOTS) e [Capítulo 47](logicaldecoding.md).

**Tabela 53.20. Colunas `pg_replication_slots`**



<table border="1" class="table" summary="pg_replication_slots Columns">
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
      slot_name
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Um identificador único para o intervalo de replicação em todo o grupo
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      plugin
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     O nome de base do objeto compartilhado que contém o plugin de saída que este slot lógico está usando, ou nulo para slots físicos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      slot_type
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     O tipo de slot:
     <code class="literal">
      physical
     </code>
     ou
     <code class="literal">
      logical
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      datoid
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-database.md" title="52.15. pg_database">
      <code class="structname">
       pg_database
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O OID do banco de dados com o qual este slot está associado, ou nulo. Apenas os slots lógicos têm um banco de dados associado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      database
     </code>
     <code class="type">
      name
     </code>
     (referências
     <a class="link" href="catalog-pg-database.md" title="52.15. pg_database">
      <code class="structname">
       pg_database
      </code>
     </a>
     .
     <code class="structfield">
      datname
     </code>
     )
    </p>
    <p>
     O nome do banco de dados com o qual este slot está associado, ou nulo. Apenas os slots lógicos têm um banco de dados associado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      temporary
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se este for um slot de replicação temporário. Os slots temporários não são salvos em disco e são automaticamente descartados em caso de erro ou quando a sessão tiver terminado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      active
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se este slot está sendo transmitido atualmente
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      active_pid
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     O ID de processo dos dados de transmissão da sessão para este slot.
     <code class="literal">
      NULL
     </code>
     se inativo.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      xmin
     </code>
     <code class="type">
      xid
     </code>
    </p>
    <p>
     A transação mais antiga que essa posição precisa manter no banco de dados.
     <code class="literal">
      VACUUM
     </code>
     não é possível remover tuplas excluídas por qualquer transação posterior.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      catalog_xmin
     </code>
     <code class="type">
      xid
     </code>
    </p>
    <p>
     A transação mais antiga que afeta os catálogos do sistema é que esse slot precisa do banco de dados para ser mantido.
     <code class="literal">
      VACUUM
     </code>
     não é possível remover tuplas de catálogo excluídas por qualquer transação posterior.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      restart_lsn
     </code>
     <code class="type">
      pg_lsn
     </code>
    </p>
    <p>
     O endereço (
     <code class="literal">
      LSN
     </code>
     ) do WAL mais antigo que ainda possa ser necessário pelo consumidor deste slot e, portanto, não será removido automaticamente durante os pontos de verificação, a menos que este LSN fique para trás em mais de
     <a class="xref" href="runtime-config-replication.md#GUC-MAX-SLOT-WAL-KEEP-SIZE">
      max_slot_wal_keep_size
     </a>
     a partir do LSN atual.
     <code class="literal">
      NULL
     </code>
     se o
     <code class="literal">
      LSN
     </code>
     Este slot nunca foi reservado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      confirmed_flush_lsn
     </code>
     <code class="type">
      pg_lsn
     </code>
    </p>
    <p>
     O endereço (
     <code class="literal">
      LSN
     </code>
     ) até a qual o consumidor do slot lógico confirmou ter recebido os dados. Os dados correspondentes às transações comprometidas antes disso
     <code class="literal">
      LSN
     </code>
     não está mais disponível.
     <code class="literal">
      NULL
     </code>
     para slots físicos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      wal_status
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Disponibilidade de arquivos WAL reivindicados por este slot. Os valores possíveis são:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        <code class="literal">
         reserved
        </code>
        significa que os arquivos reivindicados estão dentro
        <code class="varname">
         max_wal_size
        </code>
        .
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         extended
        </code>
        significa que
        <code class="varname">
         max_wal_size
        </code>
        se o limite é ultrapassado, mas os arquivos ainda são retidos, seja pelo slot de replicação ou pelo
        <code class="varname">
         wal_keep_size
        </code>
        .
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         unreserved
        </code>
        significa que o slot não retém mais os arquivos WAL necessários e alguns deles devem ser removidos no próximo ponto de verificação. Isso geralmente ocorre quando
        <a class="xref" href="runtime-config-replication.md#GUC-MAX-SLOT-WAL-KEEP-SIZE">
         max_slot_wal_keep_size
        </a>
        está definido para um valor não negativo. Esse estado pode retornar para
        <code class="literal">
         reserved
        </code>
        ou
        <code class="literal">
         extended
        </code>
        .
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         lost
        </code>
        Isso significa que esse slot não é mais utilizável.
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
      safe_wal_size
     </code>
     <code class="type">
      int8
     </code>
    </p>
    <p>
     O número de bytes que podem ser escritos no WAL de modo que esse slot não esteja em perigo de entrar no estado "perdido". É NULL para slots perdidos, bem como se
     <code class="varname">
      max_slot_wal_keep_size
     </code>
     é
     <code class="literal">
      -1
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      two_phase
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se a posição está habilitada para decodificação de transações preparadas. Sempre falso para posições físicas.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      two_phase_at
     </code>
     <code class="type">
      pg_lsn
     </code>
    </p>
    <p>
     O endereço (
     <code class="literal">
      LSN
     </code>
     ) a partir da qual a decodificação de transações preparadas é habilitada.
     <code class="literal">
      NULL
     </code>
     para slots lógicos onde
     <code class="structfield">
      two_phase
     </code>
     é falsa e para slots físicos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      inactive_since
     </code>
     <code class="type">
      timestamptz
     </code>
    </p>
    <p>
     O momento em que o slot se tornou inativo.
     <code class="literal">
      NULL
     </code>
     se o horário estiver sendo transmitido atualmente. Se o horário se tornar inválido, esse valor nunca será atualizado. Para horários de espera que estão sendo sincronizados a partir de um servidor primário (cujo
     <code class="structfield">
      synced
     </code>
     campo é
     <code class="literal">
      true
     </code>
     ), o
     <code class="structfield">
      inactive_since
     </code>
     indica o momento em que a sincronização de faixas (veja
     <a class="xref" href="logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION" title="47.2.3. Replication Slot Synchronization">
      Seção 47.2.3
     </a>
     ) foi recentemente interrompido.
     <code class="literal">
      NULL
     </code>
     se a posição sempre estiver sincronizada. Isso ajuda as posições de espera a rastrear quando a sincronização foi interrompida.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      conflicting
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se este slot lógico entrou em conflito com a recuperação (e, portanto, foi invalidado). Quando esta coluna estiver verdadeira, verifique
     <code class="structfield">
      invalidation_reason
     </code>
     coluna para o conflito. Sempre
     <code class="literal">
      NULL
     </code>
     para slots físicos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      invalidation_reason
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     A razão da invalidação do slot. É definida tanto para slots lógicos quanto físicos.
     <code class="literal">
      NULL
     </code>
     se o slot não for invalido. Os valores possíveis são:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist compact" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        <code class="literal">
         wal_removed
        </code>
        significa que o WAL necessário foi removido.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         rows_removed
        </code>
        significa que as linhas necessárias foram removidas. É definido apenas para slots lógicos.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         wal_level_insufficient
        </code>
        significa que o primário não tem
        <a class="xref" href="runtime-config-wal.md#GUC-WAL-LEVEL">
         wal_level
        </a>
        suficiente para realizar a decodificação lógica. É definido apenas para slots lógicos.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         idle_timeout
        </code>
        significa que a posição permaneceu inativa por mais tempo do que a configurada
        <a class="xref" href="runtime-config-replication.md#GUC-IDLE-REPLICATION-SLOT-TIMEOUT">
         idle_replication_slot_timeout
        </a>
        duration.
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
      failover
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se este é um slot lógico habilitado para ser sincronizado com os standbys, para que a replicação lógica possa ser retomada a partir do novo primário após o failover. Sempre falso para slots físicos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      synced
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se este é um slot lógico que foi sincronizado a partir de um servidor primário. Em um standby quente, os slots com a coluna sincronizada marcada como verdadeira não podem ser usados para decodificação lógica nem descartados manualmente. O valor desta coluna não tem significado no servidor primário; o valor da coluna no primário é padrão falso para todos os slots, mas pode (se restar de um standby promovido) também ser verdadeiro.
    </p>
   </td>
  </tr>
 </tbody>
</table>




