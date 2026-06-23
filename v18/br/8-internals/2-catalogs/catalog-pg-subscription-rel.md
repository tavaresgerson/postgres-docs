## 52.55. `pg_subscription_rel` [#](#CATALOG-PG-SUBSCRIPTION-REL)

O catálogo `pg_subscription_rel` contém o estado para cada relação replicada em cada assinatura. Esse é um mapeamento de muitos para muitos.

Este catálogo contém apenas tabelas conhecidas pela assinatura após a execução de `CREATE SUBSCRIPTION`(sql-createsubscription.md "CREATE SUBSCRIPTION") ou `ALTER SUBSCRIPTION ... REFRESH PUBLICATION`(sql-altersubscription.md "ALTER SUBSCRIPTION").

**Tabela 52.55. Colunas `pg_subscription_rel`**



<table border="1" class="table" summary="pg_subscription_rel Columns">
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
      srsubid
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-subscription.md" title="52.54. pg_subscription">
      <code class="structname">
       pg_subscription
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      srrelid
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
       pg_class
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      srsubstate
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Código estadual:
     <code class="literal">
      i
     </code>
     = inicializar,
     <code class="literal">
      d
     </code>
     = dados estão sendo copiados,
     <code class="literal">
      f
     </code>
     = cópia de tabela finalizada,
     <code class="literal">
      s
     </code>
     = sincronizada,
     <code class="literal">
      r
     </code>
     = pronto (replicação normal)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      srsublsn
     </code>
     <code class="type">
      pg_lsn
     </code>
    </p>
    <p>
     LSN remoto da mudança do estado utilizado para coordenação de sincronização quando em
     <code class="literal">
      s
     </code>
     ou
     <code class="literal">
      r
     </code>
     estados, caso contrário, nulos
    </p>
   </td>
  </tr>
 </tbody>
</table>





