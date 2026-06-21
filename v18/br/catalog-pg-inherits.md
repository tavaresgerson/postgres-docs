## 52.27. `pg_inherits` [#](#CATALOG-PG-INHERITS)

O catálogo `pg_inherits` registra informações sobre hierarquias de herança de tabelas e índices. Há uma entrada para cada relação de tabela ou índice pai-filho direto no banco de dados. (A herança indireta pode ser determinada seguindo cadeias de entradas.)

**Tabela 52.27. Colunas `pg_inherits`**



<table border="1" class="table" summary="pg_inherits Columns">
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
      inhrelid
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
     O OID da tabela ou índice da criança
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      inhparent
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
     O OID da tabela ou índice principal
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      inhseqno
     </code>
     <code class="type">
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
     <code class="structfield">
      inhdetachpending
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     <code class="literal">
      true
     </code>
     para uma partição que está em processo de ser desativada;
     <code class="literal">
      false
     </code>
     otherwise.
    </p>
   </td>
  </tr>
 </tbody>
</table>




