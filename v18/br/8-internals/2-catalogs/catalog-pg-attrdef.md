## 52.6. `pg_attrdef` [#](#CATALOG-PG-ATTRDEF)

O catálogo `pg_attrdef` armazena expressões padrão de colunas e expressões de geração. As principais informações sobre as colunas são armazenadas em [`pg_attribute`](catalog-pg-attribute.md "52.7. pg_attribute"). Apenas as colunas para as quais uma expressão padrão ou expressão de geração foi explicitamente definida terão uma entrada aqui.

**Tabela 52.6. Colunas `pg_attrdef`**



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
      oid
     </code>
     <code>
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
     <code>
      adrelid
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
     A tabela a que esta coluna pertence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      adnum
     </code>
     <code>
      int2
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
     O número da coluna
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      adbin
     </code>
     <code>
      pg_node_tree
     </code>
    </p>
    <p>
     A expressão padrão ou de geração da coluna, em
     <code>
      nodeToString()
     </code>
     representação. Use
     <code>
      pg_get_expr(adbin, adrelid)
     </code>
     para convertê-lo em uma expressão SQL.
    </p>
   </td>
  </tr>
 </tbody>
</table>





