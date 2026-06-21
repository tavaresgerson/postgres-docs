## 52.41. `pg_publication_namespace` [#](#CATALOG-PG-PUBLICATION-NAMESPACE)

O catálogo `pg_publication_namespace` contém a mapeo entre esquemas e publicações no banco de dados. Este é um mapeo de muitos para muitos.

**Tabela 52.41. Colunas `pg_publication_namespace`**



<table border="1" class="table" summary="pg_publication_namespace Columns">
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
      pnpubid
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
      pnnspid
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
      <code class="structname">
       pg_namespace
      </code>
     </a>
     .
     <code class="structfield">
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





