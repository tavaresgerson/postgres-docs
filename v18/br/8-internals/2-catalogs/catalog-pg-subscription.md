## 52.54. `pg_subscription` [#](#CATALOG-PG-SUBSCRIPTION)

O catálogo `pg_subscription` contém todas as assinaturas de replicação lógica existentes. Para mais informações sobre replicação lógica, consulte o [Capítulo 29](logical-replication.md).

Ao contrário da maioria dos catálogos de sistema, o `pg_subscription` é compartilhado em todos os bancos de dados de um clúster: há apenas uma cópia do `pg_subscription` por clúster, não uma por banco de dados.

O acesso à coluna `subconninfo` é revogado para usuários normais, pois ela pode conter senhas em texto simples.

**Tabela 52.54. Colunas `pg_subscription`**



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
      oid
     </code>
     <code>
      oid
     </code>
    </p>
    <p>
     Identificador da linha
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      subdbid
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
     OID do banco de dados no qual a assinatura reside
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      subskiplsn
     </code>
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     Finalize o LSN da transação cujas alterações devem ser ignoradas, se houver um LSN válido; caso contrário
     <code>
      0/0
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      subname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome da assinatura
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      subowner
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code>
       pg_authid
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Proprietário da assinatura
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      subenabled
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, a assinatura está habilitada e deve estar replicando
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      subbinary
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, a assinatura solicitará que o editor envie dados em formato binário.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      substream
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     Controla como lidar com o streaming de transações em andamento:
     <code>
      f
     </code>
     = não permitir o streaming de transações em andamento,
     <code>
      t
     </code>
     = transferir as alterações das transações em andamento para o disco e aplicá-las de uma vez, após a transação ser confirmada no editor e recebida pelo assinante,
     <code>
      p
     </code>
     = aplicar as alterações diretamente usando um trabalhador de aplicação paralela, se disponível (mesmo que
     <code>
      t
     </code>
     se nenhum trabalhador estiver disponível)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      subtwophasestate
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     Códigos estaduais para modo de duas fases:
     <code>
      d
     </code>
     = deficiente,
     <code>
      p
     </code>
     = em espera de ativação,
     <code>
      e
     </code>
     = ativado
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      subdisableonerr
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, a assinatura será desativada se um de seus funcionários detectar um erro
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      subpasswordrequired
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, a assinatura exigirá que você especifique uma senha para autenticação.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      subrunasowner
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, a assinatura será executada com as permissões do proprietário da assinatura.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      subfailover
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, os slots de replicação associados (ou seja, o slot principal e os slots de sincronização de tabela) no banco de dados upstream são habilitados para serem sincronizados com os standbys
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      subconninfo
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Chave de conexão para o banco de dados upstream
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      subslotname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome do slot de replicação no banco de dados upstream (também utilizado para o nome da origem de replicação local); nulo representa
     <code>
      NONE
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      subsynccommit
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     O
     <code>
      synchronous_commit
     </code>
     ambiente para os trabalhadores da assinatura utilizarem
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      subpublications
     </code>
     <code>
      text[]
     </code>
    </p>
    <p>
     Matriz de nomes de publicações assinadas. Essas publicações de referência são definidas no banco de dados anterior. Para mais informações sobre publicações, consulte
     <a class="xref" href="logical-replication-publication.md" title="29.1. Publication">
      Seção 29.1
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      suborigin
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     O valor de origem deve ser ou
     <code>
      none
     </code>
     ou
     <code>
      any
     </code>
     O padrão é
     <code>
      any
     </code>
     . Se
     <code>
      none
     </code>
     , a assinatura solicitará que o editor envie apenas alterações que não tenham origem. Se
     <code>
      any
     </code>
     , o editor envia as alterações independentemente de sua origem.
    </p>
   </td>
  </tr>
 </tbody>
</table>





