## 52.54. `pg_subscription` [#](#CATALOG-PG-SUBSCRIPTION)

O catálogo `pg_subscription` contém todas as assinaturas de replicação lógica existentes. Para mais informações sobre replicação lógica, consulte o [Capítulo 29](logical-replication.md).

Ao contrário da maioria dos catálogos de sistema, o `pg_subscription` é compartilhado em todos os bancos de dados de um clúster: há apenas uma cópia do `pg_subscription` por clúster, não uma por banco de dados.

O acesso à coluna `subconninfo` é revogado para usuários normais, pois ela pode conter senhas em texto simples.

**Tabela 52.54. Colunas `pg_subscription`**



<table border="1" class="table" summary="pg_subscription Columns">
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
      oid
     </code>
     <code class="type">
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
     <code class="structfield">
      subdbid
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
     OID do banco de dados no qual a assinatura reside
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      subskiplsn
     </code>
     <code class="type">
      pg_lsn
     </code>
    </p>
    <p>
     Finalize o LSN da transação cujas alterações devem ser ignoradas, se houver um LSN válido; caso contrário
     <code class="literal">
      0/0
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      subname
     </code>
     <code class="type">
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
     <code class="structfield">
      subowner
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code class="structname">
       pg_authid
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      subenabled
     </code>
     <code class="type">
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
     <code class="structfield">
      subbinary
     </code>
     <code class="type">
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
     <code class="structfield">
      substream
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Controla como lidar com o streaming de transações em andamento:
     <code class="literal">
      f
     </code>
     = não permitir o streaming de transações em andamento,
     <code class="literal">
      t
     </code>
     = transferir as alterações das transações em andamento para o disco e aplicá-las de uma vez, após a transação ser confirmada no editor e recebida pelo assinante,
     <code class="literal">
      p
     </code>
     = aplicar as alterações diretamente usando um trabalhador de aplicação paralela, se disponível (mesmo que
     <code class="literal">
      t
     </code>
     se nenhum trabalhador estiver disponível)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      subtwophasestate
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Códigos estaduais para modo de duas fases:
     <code class="literal">
      d
     </code>
     = deficiente,
     <code class="literal">
      p
     </code>
     = em espera de ativação,
     <code class="literal">
      e
     </code>
     = ativado
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      subdisableonerr
     </code>
     <code class="type">
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
     <code class="structfield">
      subpasswordrequired
     </code>
     <code class="type">
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
     <code class="structfield">
      subrunasowner
     </code>
     <code class="type">
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
     <code class="structfield">
      subfailover
     </code>
     <code class="type">
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
     <code class="structfield">
      subconninfo
     </code>
     <code class="type">
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
     <code class="structfield">
      subslotname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome do slot de replicação no banco de dados upstream (também utilizado para o nome da origem de replicação local); nulo representa
     <code class="literal">
      NONE
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      subsynccommit
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     O
     <code class="varname">
      synchronous_commit
     </code>
     ambiente para os trabalhadores da assinatura utilizarem
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      subpublications
     </code>
     <code class="type">
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
     <code class="structfield">
      suborigin
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     O valor de origem deve ser ou
     <code class="literal">
      none
     </code>
     ou
     <code class="literal">
      any
     </code>
     O padrão é
     <code class="literal">
      any
     </code>
     . Se
     <code class="literal">
      none
     </code>
     , a assinatura solicitará que o editor envie apenas alterações que não tenham origem. Se
     <code class="literal">
      any
     </code>
     , o editor envia as alterações independentemente de sua origem.
    </p>
   </td>
  </tr>
 </tbody>
</table>




