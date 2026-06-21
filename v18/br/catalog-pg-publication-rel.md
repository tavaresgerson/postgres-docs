## 52.42. `pg_publication_rel` [#](#CATALOG-PG-PUBLICATION-REL)

O catálogo `pg_publication_rel` contém a mapeo entre as relações e as publicações no banco de dados. Este é um mapeo de muitos para muitos. Consulte também [Seção 53.18](view-pg-publication-tables.md) para uma visão mais amigável dessa informação.

**Tabela 52.42. Colunas `pg_publication_rel`**



<table border="1" class="table" summary="pg_publication_rel Columns">
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
      prpubid
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-publication.md" title="52.40. pg_publication">
      <code class="structname">
       pg_publication
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Referência à publicação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      prrelid
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
      prqual
     </code>
     <code class="type">
      pg_node_tree
     </code>
    </p>
    <p>
     árvore de expressão (em
     <code class="function">
      nodeToString()
     </code>
     representação) para a condição de publicação da relação. Nulo se não houver nenhuma condição de publicação.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      prattrs
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
     Este é um conjunto de valores que indica quais colunas da tabela fazem parte da publicação. Por exemplo, um valor de
     <code class="literal">
      1 3
     </code>
     significaria que as primeiras e as colunas da terceira tabela são publicadas. Um valor nulo indica que todas as colunas são publicadas.
    </p>
   </td>
  </tr>
 </tbody>
</table>





