## 53.35. `pg_user` [#](#VIEW-PG-USER)

A vista `pg_user` fornece acesso a informações sobre os usuários do banco de dados. Esta é simplesmente uma vista legível publicamente do `pg_shadow`(view-pg-shadow.md "53.26. pg_shadow") que apaga o campo de senha.

**Tabela 53.35. Colunas `pg_user`**



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
      usename
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome do usuário
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      usesysid
     </code>
     <code>
      oid
     </code>
    </p>
    <p>
     ID deste usuário
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      usecreatedb
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     O usuário pode criar bancos de dados
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      usesuper
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     O usuário é um superusuário
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      userepl
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     O usuário pode iniciar a replicação em streaming e colocar o sistema no modo de backup e sair dele.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      usebypassrls
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     O usuário contorna todas as políticas de segurança de nível de linha, veja
     <a class="xref" href="ddl-rowsecurity.md" title="5.9. Row Security Policies">
      Seção 5.9
     </a>
     para mais informações.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      passwd
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Não a senha (sempre é lido como
     <code>
      ********
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      valuntil
     </code>
     <code>
      timestamptz
     </code>
    </p>
    <p>
     Tempo de expiração da senha (usado apenas para autenticação de senha)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      useconfig
     </code>
     <code>
      text[]
     </code>
    </p>
    <p>
     Padrões de sessão para variáveis de configuração de tempo de execução
    </p>
   </td>
  </tr>
 </tbody>
</table>





