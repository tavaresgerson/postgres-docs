## 53.18. `pg_publication_tables` [#](#VIEW-PG-PUBLICATION-TABLES)

A vista `pg_publication_tables` fornece informações sobre o mapeamento entre as publicações e as informações das tabelas que elas contêm. Ao contrário do catálogo subjacente `pg_publication_rel`(catalog-pg-publication-rel.md "52.42. pg_publication_rel"), essa vista expande as publicações definidas como `FOR ALL TABLES`(sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-ALL-TABLES) e `FOR TABLES IN SCHEMA`(sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLES-IN-SCHEMA), portanto, para tais publicações, haverá uma linha para cada tabela elegível.

**Tabela 53.18. Colunas `pg_publication_tables`**



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
      pubname
     </code>
     <code>
      name
     </code>
     (referências
     <a class="link" href="catalog-pg-publication.md" title="52.40. pg_publication">
      <code>
       pg_publication
      </code>
     </a>
     .
     <code>
      pubname
     </code>
     )
    </p>
    <p>
     Nome da publicação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      schemaname
     </code>
     <code>
      name
     </code>
     (referências
     <a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
      <code>
       pg_namespace
      </code>
     </a>
     .
     <code>
      nspname
     </code>
     )
    </p>
    <p>
     Nome do esquema que contém a tabela
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tablename
     </code>
     <code>
      name
     </code>
     (referências
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code>
       pg_class
      </code>
     </a>
     .
     <code>
      relname
     </code>
     )
    </p>
    <p>
     Nome da tabela
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attnames
     </code>
     <code>
      name[]
     </code>
     (referências
     <a class="link" href="catalog-pg-attribute.md" title="52.7. pg_attribute">
      <code>
       pg_attribute
      </code>
     </a>
     .
     <code>
      attname
     </code>
     )
    </p>
    <p>
     Nomes das colunas da tabela incluídos na publicação. Isso contém todas as colunas da tabela quando o usuário não especificou a lista de colunas para a tabela.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      rowfilter
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Expressão para a condição de qualificação da publicação da tabela
    </p>
   </td>
  </tr>
 </tbody>
</table>





