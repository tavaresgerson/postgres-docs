## 52.6. `pg_attrdef` [#](#CATALOG-PG-ATTRDEF)

O catálogo `pg_attrdef` armazena expressões padrão de colunas e expressões de geração. As principais informações sobre as colunas são armazenadas em [`pg_attribute`](catalog-pg-attribute.md "52.7. pg_attribute"). Apenas as colunas para as quais uma expressão padrão ou expressão de geração foi explicitamente definida terão uma entrada aqui.

**Tabela 52.6. Colunas `pg_attrdef`**



<table border="1" class="table" summary="pg_attrdef Columns">
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
      adrelid
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
     A tabela a que esta coluna pertence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      adnum
     </code>
     <code class="type">
      int2
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
     O número da coluna
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      adbin
     </code>
     <code class="type">
      pg_node_tree
     </code>
    </p>
    <p>
     A expressão padrão ou de geração da coluna, em
     <code class="function">
      nodeToString()
     </code>
     representação. Use
     <code class="literal">
      pg_get_expr(adbin, adrelid)
     </code>
     para convertê-lo em uma expressão SQL.
    </p>
   </td>
  </tr>
 </tbody>
</table>





