## 53.36. `pg_user_mappings` [#](#VIEW-PG-USER-MAPPINGS)

A vista `pg_user_mappings` fornece acesso a informações sobre mapeamentos de usuários. Essa é, essencialmente, uma vista públicamente legível de `pg_user_mapping`(catalog-pg-user-mapping.md "52.65. pg_user_mapping") que exclui o campo de opções se o usuário não tiver direitos para usá-lo.

**Tabela 53.36. Colunas `pg_user_mappings`**



<table border="1" class="table" summary="pg_user_mappings Columns">
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
      umid
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-user-mapping.md" title="52.65. pg_user_mapping">
<code class="structname">
       pg_user_mapping
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>OID do mapeamento de usuários</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      srvid
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-foreign-server.md" title="52.24. pg_foreign_server">
<code class="structname">
       pg_foreign_server
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>O OID do servidor estrangeiro que contém esse mapeamento</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      srvname
     </code>
<code class="type">
      name
     </code>(referências<a class="link" href="catalog-pg-foreign-server.md" title="52.24. pg_foreign_server">
<code class="structname">
       pg_foreign_server
      </code>
</a>
     .
     <code class="structfield">
      srvname
     </code>)</p>
<p>Nome do servidor estrangeiro</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      umuser
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
<code class="structname">
       pg_authid
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>OID do papel local que está sendo mapeado, ou zero se a mapeamento do usuário é público</p>
</td>
</tr>
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
<p>Nome do usuário local a ser mapeado</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      umoptions
     </code>
<code class="type">
      text[]
     </code>
</p>
<p>Mapeamento de opções específicas do usuário, como<span class="quote">“<span class="quote">palavra-chave=valor</span>”</span>cordas</p>
</td>
</tr>
</tbody>
</table>




  

Para proteger as informações de senha armazenadas como uma opção de mapeamento de usuário, a coluna `umoptions` será considerada nula, a menos que uma das seguintes situações se aplique:

* o usuário atual é o usuário que está sendo mapeado e possui o servidor ou possui o privilégio `USAGE` nele
* o usuário atual é o proprietário do servidor e a mapeo é para `PUBLIC`
* o usuário atual é um superusuário