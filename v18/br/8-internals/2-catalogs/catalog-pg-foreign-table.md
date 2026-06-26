## 52.25. `pg_foreign_table` [#](#CATALOG-PG-FOREIGN-TABLE)

O catálogo `pg_foreign_table` contém informações auxiliares sobre tabelas estrangeiras. Uma tabela estrangeira é representada principalmente por uma entrada [`pg_class`](catalog-pg-class.md "52.11. pg_class"), assim como uma tabela regular. Sua entrada `pg_foreign_table` contém as informações que são pertinentes apenas para tabelas estrangeiras e não para qualquer outro tipo de relação.

**Tabela 52.25. Colunas `pg_foreign_table`**



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
      ftrelid
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
     O OID do
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code>
       pg_class
      </code>
     </a>
     entrada para esta mesa estrangeira
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      ftserver
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-foreign-server.md" title="52.24. pg_foreign_server">
      <code>
       pg_foreign_server
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     OID do servidor estrangeiro para esta tabela estrangeira
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      ftoptions
     </code>
     <code>
      text[]
     </code>
    </p>
    <p>
     Opções de mesa estrangeiras, como
     <span class="quote">
      “
      <span class="quote">
       palavra-chave=valor
      </span>
      ”
     </span>
     cordas
    </p>
   </td>
  </tr>
 </tbody>
</table>





