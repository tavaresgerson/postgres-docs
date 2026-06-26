## 53.20. `pg_replication_slots` [#](#VIEW-PG-REPLICATION-SLOTS)

A visualização `pg_replication_slots` fornece uma lista de todos os slots de replicação que atualmente existem no clúster de banco de dados, juntamente com seu estado atual.

Para mais informações sobre slots de replicação, consulte [Seção 26.2.6](warm-standby.md#STREAMING-REPLICATION-SLOTS) e [Capítulo 47](logicaldecoding.md).

**Tabela 53.20. Colunas `pg_replication_slots`**



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
      slot_name
     </code>
     <code>
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
     <code>
      plugin
     </code>
     <code>
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
     <code>
      slot_type
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     O tipo de slot:
     <code>
      physical
     </code>
     ou
     <code>
      logical
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      datoid
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-database.md" title="52.15. pg_database">
      <code>
       pg_database
      </code>
     </a>
     .
     <code>
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
     <code>
      database
     </code>
     <code>
      name
     </code>
     (referências
     <a class="link" href="catalog-pg-database.md" title="52.15. pg_database">
      <code>
       pg_database
      </code>
     </a>
     .
     <code>
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
     <code>
      temporary
     </code>
     <code>
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
     <code>
      active
     </code>
     <code>
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
     <code>
      active_pid
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     O ID de processo dos dados de transmissão da sessão para este slot.
     <code>
      NULL
     </code>
     se inativo.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      xmin
     </code>
     <code>
      xid
     </code>
    </p>
    <p>
     A transação mais antiga que essa posição precisa manter no banco de dados.
     <code>
      VACUUM
     </code>
     não é possível remover tuplas excluídas por qualquer transação posterior.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      catalog_xmin
     </code>
     <code>
      xid
     </code>
    </p>
    <p>
     A transação mais antiga que afeta os catálogos do sistema é que esse slot precisa do banco de dados para ser mantido.
     <code>
      VACUUM
     </code>
     não é possível remover tuplas de catálogo excluídas por qualquer transação posterior.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      restart_lsn
     </code>
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     O endereço (
     <code>
      LSN
     </code>
     ) do WAL mais antigo que ainda possa ser necessário pelo consumidor deste slot e, portanto, não será removido automaticamente durante os pontos de verificação, a menos que este LSN fique para trás em mais de
     <a class="xref" href="runtime-config-replication.md#GUC-MAX-SLOT-WAL-KEEP-SIZE">
      max_slot_wal_keep_size
     </a>
     a partir do LSN atual.
     <code>
      NULL
     </code>
     se o
     <code>
      LSN
     </code>
     Este slot nunca foi reservado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      confirmed_flush_lsn
     </code>
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     O endereço (
     <code>
      LSN
     </code>
     ) até a qual o consumidor do slot lógico confirmou ter recebido os dados. Os dados correspondentes às transações comprometidas antes disso
     <code>
      LSN
     </code>
     não está mais disponível.
     <code>
      NULL
     </code>
     para slots físicos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      wal_status
     </code>
     <code>
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
        <code>
         reserved
        </code>
        significa que os arquivos reivindicados estão dentro
        <code>
         max_wal_size
        </code>
        .
       </p>
      </li>
      <li class="listitem">
       <p>
        <code>
         extended
        </code>
        significa que
        <code>
         max_wal_size
        </code>
        se o limite é ultrapassado, mas os arquivos ainda são retidos, seja pelo slot de replicação ou pelo
        <code>
         wal_keep_size
        </code>
        .
       </p>
      </li>
      <li class="listitem">
       <p>
        <code>
         unreserved
        </code>
        significa que o slot não retém mais os arquivos WAL necessários e alguns deles devem ser removidos no próximo ponto de verificação. Isso geralmente ocorre quando
        <a class="xref" href="runtime-config-replication.md#GUC-MAX-SLOT-WAL-KEEP-SIZE">
         max_slot_wal_keep_size
        </a>
        está definido para um valor não negativo. Esse estado pode retornar para
        <code>
         reserved
        </code>
        ou
        <code>
         extended
        </code>
        .
       </p>
      </li>
      <li class="listitem">
       <p>
        <code>
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
     <code>
      safe_wal_size
     </code>
     <code>
      int8
     </code>
    </p>
    <p>
     O número de bytes que podem ser escritos no WAL de modo que esse slot não esteja em perigo de entrar no estado "perdido". É NULL para slots perdidos, bem como se
     <code>
      max_slot_wal_keep_size
     </code>
     é
     <code>
      -1
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      two_phase
     </code>
     <code>
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
     <code>
      two_phase_at
     </code>
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     O endereço (
     <code>
      LSN
     </code>
     ) a partir da qual a decodificação de transações preparadas é habilitada.
     <code>
      NULL
     </code>
     para slots lógicos onde
     <code>
      two_phase
     </code>
     é falsa e para slots físicos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      inactive_since
     </code>
     <code>
      timestamptz
     </code>
    </p>
    <p>
     O momento em que o slot se tornou inativo.
     <code>
      NULL
     </code>
     se o horário estiver sendo transmitido atualmente. Se o horário se tornar inválido, esse valor nunca será atualizado. Para horários de espera que estão sendo sincronizados a partir de um servidor primário (cujo
     <code>
      synced
     </code>
     campo é
     <code>
      true
     </code>
     ), o
     <code>
      inactive_since
     </code>
     indica o momento em que a sincronização de faixas (veja
     <a class="xref" href="logicaldecoding-explanation.md#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION" title="47.2.3. Replication Slot Synchronization">
      Seção 47.2.3
     </a>
     ) foi recentemente interrompido.
     <code>
      NULL
     </code>
     se a posição sempre estiver sincronizada. Isso ajuda as posições de espera a rastrear quando a sincronização foi interrompida.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      conflicting
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Verdadeiro se este slot lógico entrou em conflito com a recuperação (e, portanto, foi invalidado). Quando esta coluna estiver verdadeira, verifique
     <code>
      invalidation_reason
     </code>
     coluna para o conflito. Sempre
     <code>
      NULL
     </code>
     para slots físicos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      invalidation_reason
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     A razão da invalidação do slot. É definida tanto para slots lógicos quanto físicos.
     <code>
      NULL
     </code>
     se o slot não for invalido. Os valores possíveis são:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist compact" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        <code>
         wal_removed
        </code>
        significa que o WAL necessário foi removido.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code>
         rows_removed
        </code>
        significa que as linhas necessárias foram removidas. É definido apenas para slots lógicos.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code>
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
        <code>
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
     <code>
      failover
     </code>
     <code>
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
     <code>
      synced
     </code>
     <code>
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





