## 53.21. `pg_roles` [#](#VIEW-PG-ROLES)

A vista `pg_roles` fornece acesso a informações sobre os papéis do banco de dados. Esta é simplesmente uma vista legível publicamente de [`pg_authid`](catalog-pg-authid.md "52.8. pg_authid") que apaga o campo de senha.

**Tabela 53.21. Colunas `pg_roles`**



<table border="1" class="table" summary="pg_roles Columns">
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
      rolname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome do papel
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rolsuper
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     O papel tem privilégios de superusuário
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rolinherit
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     O papel herda automaticamente os privilégios dos papéis dos quais é membro
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rolcreaterole
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     O papel pode criar mais papéis
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rolcreatedb
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Role pode criar bancos de dados
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rolcanlogin
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     O papel pode fazer login. Ou seja, esse papel pode ser dado como o identificador de autorização da sessão inicial.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rolreplication
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     O papel é um papel de replicação. Um papel de replicação pode iniciar conexões de replicação e criar e descartar slots de replicação.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rolconnlimit
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Para os papéis que podem fazer login, isso define o número máximo de conexões concorrentes que esse papel pode fazer. -1 significa sem limite.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rolpassword
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Não a senha (sempre é lido como
     <code class="literal">
      ********
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rolvaliduntil
     </code>
     <code class="type">
      timestamptz
     </code>
    </p>
    <p>
     Tempo de expiração da senha (usado apenas para autenticação de senha); nulo se não houver expiração
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      rolbypassrls
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     O papel contorna todas as políticas de segurança de nível de linha, veja
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
     <code class="structfield">
      rolconfig
     </code>
     <code class="type">
      text[]
     </code>
    </p>
    <p>
     Padrões específicos para o papel das variáveis de configuração de tempo de execução
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      oid
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code class="structname">
       pg_authid
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     ID do papel
    </p>
   </td>
  </tr>
 </tbody>
</table>





