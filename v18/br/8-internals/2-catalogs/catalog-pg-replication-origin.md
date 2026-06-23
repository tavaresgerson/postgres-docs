## 52.44. `pg_replication_origin` [#](#CATALOG-PG-REPLICATION-ORIGIN)

O catálogo `pg_replication_origin` contém todas as origens de replicação criadas. Para mais informações sobre as origens de replicação, consulte o [Capítulo 48](replication-origins.md).

Ao contrário da maioria dos catálogos de sistema, o `pg_replication_origin` é compartilhado em todos os bancos de dados de um clúster: há apenas uma cópia do `pg_replication_origin` por clúster, não uma por banco de dados.

**Tabela 52.44. Colunas `pg_replication_origin`**



<table border="1" class="table" summary="pg_replication_origin Columns">
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
      roident
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     Um identificador único, para todo o conjunto de réplica, para a origem da replicação. Nunca deve sair do sistema.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      roname
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     O nome externo, definido pelo usuário, de uma origem de replicação.
    </p>
   </td>
  </tr>
 </tbody>
</table>





