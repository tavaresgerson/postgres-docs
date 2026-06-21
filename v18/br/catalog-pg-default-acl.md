## 52.17. `pg_default_acl` [#](#CATALOG-PG-DEFAULT-ACL)

O catálogo `pg_default_acl` armazena privilégios iniciais a serem atribuídos a objetos recém-criados.

**Tabela 52.17. Colunas `pg_default_acl`**



<table border="1" class="table" summary="pg_default_acl Columns">
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
      oid
     </code>
<code class="type">
      oid
     </code>
</p>
<p>Identificador da linha</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      defaclrole
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
<p>O OID do papel associado a esta entrada</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      defaclnamespace
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
<code class="structname">
       pg_namespace
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>O OID do espaço de nome associado a esta entrada, ou zero se nenhum</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      defaclobjtype
     </code>
<code class="type">
      char
     </code>
</p>
<p>Tipo de objeto para o qual esta entrada é destinada:<code class="literal">
      r
     </code>= relação (tabela, visualização),<code class="literal">
      S
     </code>= sequência,<code class="literal">
      f
     </code>= função,<code class="literal">
      T
     </code>= tipo,<code class="literal">
      n
     </code>= esquema,<code class="literal">
      L
     </code>= grande objeto</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      defaclacl
     </code>
<code class="type">
      aclitem[]
     </code>
</p>
<p>Privilegios de acesso que esse tipo de objeto deve ter na criação</p>
</td>
</tr>
</tbody>
</table>




  

Uma entrada `pg_default_acl` mostra os privilégios iniciais a serem atribuídos a um objeto pertencente ao usuário indicado. Atualmente, existem dois tipos de entradas: entradas “globais” com `defaclnamespace` = zero e entradas “por esquema” que fazem referência a um esquema específico. Se uma entrada global estiver presente, ela *sobrepõe* os privilégios padrão hard-wired normais para o tipo de objeto. Uma entrada por esquema, se presente, representa privilégios a serem *adicionados* aos privilégios padrão globais ou hard-wired.

Observe que, quando uma entrada de ACL em outro catálogo é nula, ela é considerada para representar os privilégios padrão hard-wired para seu objeto, *não* o que possa estar em `pg_default_acl` no momento. `pg_default_acl` é consultado apenas durante a criação do objeto.