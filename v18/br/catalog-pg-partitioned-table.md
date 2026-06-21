## 52.37. `pg_partitioned_table` [#](#CATALOG-PG-PARTITIONED-TABLE)

O catálogo `pg_partitioned_table` armazena informações sobre como as tabelas são divididas.

**Tabela 52.37. Colunas `pg_partitioned_table`**



<table border="1" class="table" summary="pg_partitioned_table Columns">
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
      partrelid
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
     O OID do
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
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
     <code class="structfield">
      partstrat
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Estratégia de partição;
     <code class="literal">
      h
     </code>
     = tabela particionada por hash,
     <code class="literal">
      l
     </code>
     = tabela dividida em listas
     <code class="literal">
      r
     </code>
     = tabela particionada de intervalo
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      partnatts
     </code>
     <code class="type">
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
     <code class="structfield">
      partdefid
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
     O OID do
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
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
     <code class="structfield">
      partattrs
     </code>
     <code class="type">
      int2vector
     </code>
     (referências
     <a class="link" href="catalog-pg-attribute.md" title="52.7. pg_attribute">
      <code class="structname">
       pg_attribute
      </code>
     </a>
     .
     <code class="structfield">
      attnum
     </code>
     )
    </p>
    <p>
     Este é um conjunto de
     <code class="structfield">
      partnatts
     </code>
     valores que indicam quais colunas da tabela fazem parte da chave de partição. Por exemplo, um valor de
     <code class="literal">
      1 3
     </code>
     significaria que as primeiras e as terceiras colunas da tabela compõem a chave de partição. Um zero neste array indica que a coluna correspondente à chave de partição é uma expressão, e não uma simples referência de coluna.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      partclass
     </code>
     <code class="type">
      oidvector
     </code>
     (referências
     <a class="link" href="catalog-pg-opclass.md" title="52.33. pg_opclass">
      <code class="structname">
       pg_opclass
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Para cada coluna na chave de partição, isso contém o OID da classe de operador a ser usada. Veja
     <a class="link" href="catalog-pg-opclass.md" title="52.33. pg_opclass">
      <code class="structname">
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
     <code class="structfield">
      partcollation
     </code>
     <code class="type">
      oidvector
     </code>
     (referências
     <a class="link" href="catalog-pg-collation.md" title="52.12. pg_collation">
      <code class="structname">
       pg_collation
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      partexprs
     </code>
     <code class="type">
      pg_node_tree
     </code>
    </p>
    <p>
     árvores de expressão (em
     <code class="function">
      nodeToString()
     </code>
     (representação) para as colunas de chave de partição que não são referências simples de coluna. Esta é uma lista com um elemento para cada entrada de zero
     <code class="structfield">
      partattrs
     </code>
     Nulo se todas as colunas da chave de partição forem referências simples.
    </p>
   </td>
  </tr>
 </tbody>
</table>





