## 52.41. `pg_publication_namespace` [#](#CATALOG-PG-PUBLICATION-NAMESPACE)

O catálogo `pg_publication_namespace` contém a mapeo entre esquemas e publicações no banco de dados. Este é um mapeo de muitos para muitos.

**Tabela 52.41. Colunas `pg_publication_namespace`**



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
      pnpubid
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-publication.md" title="52.40. pg_publication">
      <code>
       pg_publication
      </code>
     </a>
     .
     <code>
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
     <code>
      pnnspid
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
      <code>
       pg_namespace
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Referência ao esquema
    </p>
   </td>
  </tr>
 </tbody>
</table>





