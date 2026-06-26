## 52.37. `pg_partitioned_table` [#](#CATALOG-PG-PARTITIONED-TABLE)

O catálogo `pg_partitioned_table` armazena informações sobre como as tabelas são divididas.

**Tabela 52.37. Colunas `pg_partitioned_table`**



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
      partrelid
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
     entrada para esta tabela dividida
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      partstrat
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     Estratégia de partição;
     <code>
      h
     </code>
     = tabela particionada por hash,
     <code>
      l
     </code>
     = tabela dividida em listas
     <code>
      r
     </code>
     = tabela particionada de intervalo
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      partnatts
     </code>
     <code>
      int2
     </code>
    </p>
    <p>
     O número de colunas na chave de partição
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      partdefid
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
     entrada para a partição padrão desta tabela particionada, ou zero se esta tabela particionada não tiver uma partição padrão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      partattrs
     </code>
     <code>
      int2vector
     </code>
     (referências
     <a class="link" href="catalog-pg-attribute.md" title="52.7. pg_attribute">
      <code>
       pg_attribute
      </code>
     </a>
     .
     <code>
      attnum
     </code>
     )
    </p>
    <p>
     Este é um conjunto de
     <code>
      partnatts
     </code>
     valores que indicam quais colunas da tabela fazem parte da chave de partição. Por exemplo, um valor de
     <code>
      1 3
     </code>
     significaria que as primeiras e as terceiras colunas da tabela compõem a chave de partição. Um zero neste array indica que a coluna correspondente à chave de partição é uma expressão, e não uma simples referência de coluna.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      partclass
     </code>
     <code>
      oidvector
     </code>
     (referências
     <a class="link" href="catalog-pg-opclass.md" title="52.33. pg_opclass">
      <code>
       pg_opclass
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Para cada coluna na chave de partição, isso contém o OID da classe de operador a ser usada. Veja
     <a class="link" href="catalog-pg-opclass.md" title="52.33. pg_opclass">
      <code>
       pg_opclass
      </code>
     </a>
     para obter mais informações.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      partcollation
     </code>
     <code>
      oidvector
     </code>
     (referências
     <a class="link" href="catalog-pg-collation.md" title="52.12. pg_collation">
      <code>
       pg_collation
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Para cada coluna na chave de partição, isso contém o OID da collation a ser usada para a partição, ou zero se a coluna não for de um tipo de dados colidível.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      partexprs
     </code>
     <code>
      pg_node_tree
     </code>
    </p>
    <p>
     árvores de expressão (em
     <code>
      nodeToString()
     </code>
     (representação) para as colunas de chave de partição que não são referências simples de coluna. Esta é uma lista com um elemento para cada entrada de zero
     <code>
      partattrs
     </code>
     Nulo se todas as colunas da chave de partição forem referências simples.
    </p>
   </td>
  </tr>
 </tbody>
</table>





