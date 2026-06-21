## 53.35. `pg_user` [#](#VIEW-PG-USER)

A vista `pg_user` fornece acesso a informações sobre os usuários do banco de dados. Esta é simplesmente uma vista legível publicamente do `pg_shadow`(view-pg-shadow.md "53.26. pg_shadow") que apaga o campo de senha.

**Tabela 53.35. Colunas `pg_user`**



<table border="1" class="table" summary="pg_user Columns">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="catalog_table_entry">
<p class="column_definition">Tipo de coluna</p>
<p>Descrição</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      usename
     </code>
<code class="type">
      name
     </code>
</p>
<p>Nome do usuário</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      usesysid
     </code>
<code class="type">
      oid
     </code>
</p>
<p>ID deste usuário</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      usecreatedb
     </code>
<code class="type">
      bool
     </code>
</p>
<p>O usuário pode criar bancos de dados</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      usesuper
     </code>
<code class="type">
      bool
     </code>
</p>
<p>O usuário é um superusuário</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      userepl
     </code>
<code class="type">
      bool
     </code>
</p>
<p>O usuário pode iniciar a replicação em streaming e colocar o sistema no modo de backup e sair dele.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      usebypassrls
     </code>
<code class="type">
      bool
     </code>
</p>
<p>O usuário contorna todas as políticas de segurança de nível de linha, veja<a class="xref" href="ddl-rowsecurity.md" title="5.9. Row Security Policies">Seção 5.9</a>para mais informações.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      passwd
     </code>
<code class="type">
      text
     </code>
</p>
<p>Não a senha (sempre é lido como<code class="literal">
      ********
     </code>)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      valuntil
     </code>
<code class="type">
      timestamptz
     </code>
</p>
<p>Tempo de expiração da senha (usado apenas para autenticação de senha)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      useconfig
     </code>
<code class="type">
      text[]
     </code>
</p>
<p>Padrões de sessão para variáveis de configuração de tempo de execução</p>
</td>
</tr>
</tbody>
</table>

