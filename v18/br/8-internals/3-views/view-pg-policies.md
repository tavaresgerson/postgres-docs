## 53.15. `pg_policies` [#](#VIEW-PG-POLICIES)

A vista `pg_policies` fornece acesso a informações úteis sobre cada política de segurança de nível de linha no banco de dados.

**Tabela 53.15. Colunas `pg_policies`**



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
     O nome do esquema que contém a política de tabela está em
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
     O nome da política da tabela está em
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      policyname
     </code>
     <code>
      name
     </code>
     (referências
     <a class="link" href="catalog-pg-policy.md" title="52.38. pg_policy">
      <code>
       pg_policy
      </code>
     </a>
     .
     <code>
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
     <code>
      permissive
     </code>
     <code>
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
     <code>
      roles
     </code>
     <code>
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
     <code>
      cmd
     </code>
     <code>
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
     <code>
      qual
     </code>
     <code>
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
     <code>
      with_check
     </code>
     <code>
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





