## 52.27. `pg_inherits` [#](#CATALOG-PG-INHERITS)

O catálogo `pg_inherits` registra informações sobre hierarquias de herança de tabelas e índices. Há uma entrada para cada relação de tabela ou índice pai-filho direto no banco de dados. (A herança indireta pode ser determinada seguindo cadeias de entradas.)

**Tabela 52.27. Colunas `pg_inherits`**



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
      inhrelid
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
     O OID da tabela ou índice da criança
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      inhparent
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
     O OID da tabela ou índice principal
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      inhseqno
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Se houver mais de um progenitor direto para uma tabela de crianças (herança múltipla), este número indica a ordem em que as colunas herdadas devem ser organizadas. A contagem começa em 1.
    </p>
    <p>
     Os índices não podem ter herança múltipla, pois eles só podem herdar quando estão usando particionamento declarativo.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      inhdetachpending
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     <code>
      true
     </code>
     para uma partição que está em processo de ser desativada;
     <code>
      false
     </code>
     otherwise.
    </p>
   </td>
  </tr>
 </tbody>
</table>





