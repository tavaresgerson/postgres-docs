## 53.17. `pg_prepared_xacts` [#](#VIEW-PG-PREPARED-XACTS)

A vista `pg_prepared_xacts` exibe informações sobre as transações que estão atualmente preparadas para o compromisso em duas fases (consulte [PREPARAR TRANSAÇÃO](sql-prepare-transaction.md "PREPARE TRANSACTION") para obter detalhes).

`pg_prepared_xacts` contém uma linha por transação preparada. Uma entrada é removida quando a transação é confirmada ou desfeita.

**Tabela 53.17. Colunas `pg_prepared_xacts`**



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
      transaction
     </code>
     <code>
      xid
     </code>
    </p>
    <p>
     Identificador numérico de transação do pedido de transação preparado
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      gid
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Identificador global da transação que foi atribuído à transação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      prepared
     </code>
     <code>
      timestamptz
     </code>
    </p>
    <p>
     Tempo em que a transação foi preparada para ser confirmada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      owner
     </code>
     <code>
      name
     </code>
     (referências
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code>
       pg_authid
      </code>
     </a>
     .
     <code>
      rolname
     </code>
     )
    </p>
    <p>
     Nome do usuário que executou a transação
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
     Nome do banco de dados em que a transação foi executada
    </p>
   </td>
  </tr>
 </tbody>
</table>










Quando a visualização `pg_prepared_xacts` é acessada, as estruturas de dados do gerenciador de transações interno são temporariamente bloqueadas e uma cópia é feita para que a visualização possa ser exibida. Isso garante que a visualização produza um conjunto consistente de resultados, sem bloquear operações normais por mais tempo do que o necessário. No entanto, pode haver algum impacto no desempenho do banco de dados se essa visualização for frequentemente acessada.