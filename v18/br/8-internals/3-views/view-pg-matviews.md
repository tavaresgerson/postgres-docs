## 53.14. `pg_matviews` [#](#VIEW-PG-MATVIEWS)

A vista `pg_matviews` fornece acesso a informações úteis sobre cada vista materializada no banco de dados.

**Tabela 53.14. Colunas `pg_matviews`**



<table border="1" class="table" summary="pg_matviews Columns">
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
     Nome do esquema que contém a visualização materializada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      matviewname
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
     Nome do visual materializado
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      matviewowner
     </code>
     <code class="type">
      name
     </code>
     (referências
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code class="structname">
       pg_authid
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      tablespace
     </code>
     <code class="type">
      name
     </code>
     (referências
     <a class="link" href="catalog-pg-tablespace.md" title="52.56. pg_tablespace">
      <code class="structname">
       pg_tablespace
      </code>
     </a>
     .
     <code class="structfield">
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
     <code class="structfield">
      hasindexes
     </code>
     <code class="type">
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
     <code class="structfield">
      ispopulated
     </code>
     <code class="type">
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
     <code class="structfield">
      definition
     </code>
     <code class="type">
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





