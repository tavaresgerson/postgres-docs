## 53.22. `pg_rules` [#](#VIEW-PG-RULES)

A vista `pg_rules` fornece acesso a informações úteis sobre as regras de reescrita de consultas.

**Tabela 53.22. Colunas `pg_rules`**



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
     Nome da tabela para a qual a regra é aplicada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      rulename
     </code>
     <code>
      name
     </code>
     (referências
     <a class="link" href="catalog-pg-rewrite.md" title="52.45. pg_rewrite">
      <code>
       pg_rewrite
      </code>
     </a>
     .
     <code>
      rulename
     </code>
     )
    </p>
    <p>
     Nome da regra
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      definition
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Definição de regra (um comando de criação reconstruído)
    </p>
   </td>
  </tr>
 </tbody>
</table>










A visão `pg_rules` exclui as regras de visões e visões materializadas do `ON SELECT`; essas podem ser vistas em [`pg_views`](view-pg-views.md "53.37. pg_views") e [`pg_matviews`](view-pg-matviews.md "53.14. pg_matviews").