## 53.22. `pg_rules` [#](#VIEW-PG-RULES)

A vista `pg_rules` fornece acesso a informações úteis sobre as regras de reescrita de consultas.

**Tabela 53.22. Colunas `pg_rules`**



<table border="1" class="table" summary="pg_rules Columns">
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
      schemaname
     </code>
     <code class="type">
      name
     </code>
     (referências
     <a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
      <code class="structname">
       pg_namespace
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      tablename
     </code>
     <code class="type">
      name
     </code>
     (referências
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
       pg_class
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      rulename
     </code>
     <code class="type">
      name
     </code>
     (referências
     <a class="link" href="catalog-pg-rewrite.md" title="52.45. pg_rewrite">
      <code class="structname">
       pg_rewrite
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      definition
     </code>
     <code class="type">
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