## 53.12. `pg_indexes` [#](#VIEW-PG-INDEXES)

A vista `pg_indexes` fornece acesso a informações úteis sobre cada índice no banco de dados.

**Tabela 53.12. Colunas `pg_indexes`**



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
     Nome do esquema que contém a tabela e o índice
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
     Nome da tabela para a qual o índice está sendo criado
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indexname
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
     Nome do índice
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
     Nome do espaço de tabela que contém o índice (nulo se for o padrão para o banco de dados)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      indexdef
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Definição do índice (reconstruído
     <a class="xref" href="sql-createindex.md" title="CREATE INDEX">
      <span class="refentrytitle">
       Crie índice
      </span>
     </a>
     comando)
    </p>
   </td>
  </tr>
 </tbody>
</table>





