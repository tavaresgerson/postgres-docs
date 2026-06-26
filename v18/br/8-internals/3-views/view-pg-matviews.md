## 53.14. `pg_matviews` [#](#VIEW-PG-MATVIEWS)

A vista `pg_matviews` fornece acesso a informações úteis sobre cada vista materializada no banco de dados.

**Tabela 53.14. Colunas `pg_matviews`**



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
     Nome do esquema que contém a visualização materializada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      matviewname
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
     Nome do visual materializado
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      matviewowner
     </code>
     <code>
      name
     </code>
     (referências
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code>
       pg_authid
      </code>
     </a>
     .
     <code>
      rolname
     </code>
     )
    </p>
    <p>
     Nome do proprietário da visualização materializada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tablespace
     </code>
     <code>
      name
     </code>
     (referências
     <a class="link" href="catalog-pg-tablespace.md" title="52.56. pg_tablespace">
      <code>
       pg_tablespace
      </code>
     </a>
     .
     <code>
      spcname
     </code>
     )
    </p>
    <p>
     Nome do espaço de tabela que contém a visualização materializada (nulo se for o padrão para o banco de dados)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      hasindexes
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Verdadeiro se a visão materializada tiver (ou tiver tido recentemente) algum índice
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      ispopulated
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Verdadeiro se a visualização materializada está atualmente preenchida
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
     Definição de visão materializada (uma reconstruída
     <a class="xref" href="sql-select.md" title="SELECT">
      <span class="refentrytitle">
       SELECIONE
      </span>
     </a>
     (consulta)
    </p>
   </td>
  </tr>
 </tbody>
</table>





