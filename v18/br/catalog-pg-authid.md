## 52.8. `pg_authid` [#](#CATALOG-PG-AUTHID)

O catálogo `pg_authid` contém informações sobre identificadores de autorização de banco de dados ( papéis). Um papel engloba os conceitos de “usuários” e “grupos”. Um usuário é essencialmente apenas um papel com a bandeira `rolcanlogin` definida. Qualquer papel (com ou sem `rolcanlogin`) pode ter outros papéis como membros; veja [`pg_auth_members`](catalog-pg-auth-members.md "52.9. pg_auth_members").

Como este catálogo contém senhas, ele não deve ser legível publicamente. `pg_roles` (view-pg-roles.md "53.21. pg_roles") é uma visualização legível publicamente no `pg_authid` que apaga o campo de senha.

[Capítulo 21](user-manag.md "Chapter 21. Database Roles") contém informações detalhadas sobre gerenciamento de usuários e privilégios.

Como as identidades dos usuários são globais para o clúster, o `pg_authid` é compartilhado em todos os bancos de dados de um clúster: há apenas uma cópia do `pg_authid` por clúster, não uma por banco de dados.

**Tabela 52.8. Colunas `pg_authid`**



<table border="1" class="table" summary="pg_authid Columns">
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
      oid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     Identificador da linha
    </p>
   </td>
  </tr>
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
     Senha criptografada; nulo se não houver. O formato depende da forma de criptografia utilizada.
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
 </tbody>
</table>









Para uma senha criptografada por MD5, a coluna `rolpassword` começará com a string `md5`, seguida por um hash hexadecimal de 32 caracteres MD5. O hash MD5 será a senha do usuário concatenada ao seu nome de usuário. Por exemplo, se o usuário `joe` tiver senha `xyzzy`, o PostgreSQL armazenará o hash md5 de `xyzzyjoe`.

### Aviso

O suporte para senhas criptografadas com MD5 é desatualizado e será removido em uma versão futura do PostgreSQL. Consulte [Seção 20.5](auth-password.md) para obter detalhes sobre a migração para outro tipo de senha.

Se a senha for criptografada com SCRAM-SHA-256, ela tem o seguinte formato:

```
SCRAM-SHA-256$<iteration count>:<salt>$<StoredKey>:<ServerKey>
```

onde *`salt`*, *`StoredKey`* e *`ServerKey`* estão no formato codificado em Base64. Este formato é o mesmo que especificado por [RFC 5803](https://datatracker.ietf.org/doc/html/rfc5803).