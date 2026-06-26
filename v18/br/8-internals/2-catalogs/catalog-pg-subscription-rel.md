## 52.55. `pg_subscription_rel` [#](#CATALOG-PG-SUBSCRIPTION-REL)

O catálogo `pg_subscription_rel` contém o estado para cada relação replicada em cada assinatura. Esse é um mapeamento de muitos para muitos.

Este catálogo contém apenas tabelas conhecidas pela assinatura após a execução de `CREATE SUBSCRIPTION`(sql-createsubscription.md "CREATE SUBSCRIPTION") ou `ALTER SUBSCRIPTION ... REFRESH PUBLICATION`(sql-altersubscription.md "ALTER SUBSCRIPTION").

**Tabela 52.55. Colunas `pg_subscription_rel`**



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
      srsubid
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-subscription.md" title="52.54. pg_subscription">
      <code>
       pg_subscription
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Referência à assinatura
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      srrelid
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code>
       pg_class
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Referência à relação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      srsubstate
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     Código estadual:
     <code>
      i
     </code>
     = inicializar,
     <code>
      d
     </code>
     = dados estão sendo copiados,
     <code>
      f
     </code>
     = cópia de tabela finalizada,
     <code>
      s
     </code>
     = sincronizada,
     <code>
      r
     </code>
     = pronto (replicação normal)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      srsublsn
     </code>
     <code>
      pg_lsn
     </code>
    </p>
    <p>
     LSN remoto da mudança do estado utilizado para coordenação de sincronização quando em
     <code>
      s
     </code>
     ou
     <code>
      r
     </code>
     estados, caso contrário, nulos
    </p>
   </td>
  </tr>
 </tbody>
</table>





