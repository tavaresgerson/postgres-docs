## 53.15. `pg_policies` [#](#VIEW-PG-POLICIES)

A vista `pg_policies` fornece acesso a informações úteis sobre cada política de segurança de nível de linha no banco de dados.

**Tabela 53.15. Colunas `pg_policies`**



<table border="1" class="table" summary="pg_policies Columns">
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
     O nome do esquema que contém a política de tabela está em
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
     O nome da política da tabela está em
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      policyname
     </code>
     <code class="type">
      name
     </code>
     (referências
     <a class="link" href="catalog-pg-policy.md" title="52.38. pg_policy">
      <code class="structname">
       pg_policy
      </code>
     </a>
     .
     <code class="structfield">
      polname
     </code>
     )
    </p>
    <p>
     Nome da política
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      permissive
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     A política é permissiva ou restritiva?
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      roles
     </code>
     <code class="type">
      name[]
     </code>
    </p>
    <p>
     Os papéis aos quais esta política se aplica
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      cmd
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     O tipo de comando ao qual a política é aplicada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      qual
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     A expressão adicionou as qualificações para a barreira de segurança nas consultas que esta política se aplica
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      with_check
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     A expressão adicionada às qualificações WITH CHECK para consultas que tentam adicionar linhas a esta tabela
    </p>
   </td>
  </tr>
 </tbody>
</table>





