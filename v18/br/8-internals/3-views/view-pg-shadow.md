## 53.26. `pg_shadow` [#](#VIEW-PG-SHADOW)

A vista `pg_shadow` existe para compatibilidade reversa: ela emula um catálogo que existia no PostgreSQL antes da versão 8.1. Ela mostra as propriedades de todos os papéis que estão marcados como `rolcanlogin` em [`pg_authid`](catalog-pg-authid.md "52.8. pg_authid").

O nome decorre do fato de que essa tabela não deve ser legível pelo público, uma vez que contém senhas. `pg_user` (view-pg-user.md "53.35. pg_user") é uma visualização legível publicamente sobre `pg_shadow` que apaga o campo de senha.

**Tabela 53.26. Colunas `pg_shadow`**



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
     (referências
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code>
       pg_authid
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
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
     Senha criptografada; nulo se não houver. Veja
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code>
       pg_authid
      </code>
     </a>
     para obter detalhes sobre como as senhas criptografadas são armazenadas.
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





