## 52.24. `pg_foreign_server` [#](#CATALOG-PG-FOREIGN-SERVER)

O catálogo `pg_foreign_server` armazena definições de servidores externos. Um servidor externo descreve uma fonte de dados externos, como um servidor remoto. Servidores externos são acessados por meio de wrappers de dados externos.

**Tabela 52.24. Colunas `pg_foreign_server`**



<table border="1" class="table" summary="pg_foreign_server Columns">
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
      srvname
     </code>
<code class="type">
      name
     </code>
</p>
<p>Nome do servidor estrangeiro</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      srvowner
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
<p>Proprietário do servidor estrangeiro</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      srvfdw
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-foreign-data-wrapper.md" title="52.23. pg_foreign_data_wrapper">
<code class="structname">
       pg_foreign_data_wrapper
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>OID do wrapper de dados estrangeiro deste servidor estrangeiro</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      srvtype
     </code>
<code class="type">
      text
     </code>
</p>
<p>Tipo do servidor (opcional)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      srvversion
     </code>
<code class="type">
      text
     </code>
</p>
<p>Versão do servidor (opcional)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      srvacl
     </code>
<code class="type">
      aclitem[]
     </code>
</p>
<p>Privilegios de acesso; veja<a class="xref" href="ddl-priv.md" title="5.8. Privileges">Seção 5.8</a>para detalhes</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      srvoptions
     </code>
<code class="type">
      text[]
     </code>
</p>
<p>Opções específicas para servidores estrangeiros, como<span class="quote">“<span class="quote">palavra-chave=valor</span>”</span>cordas</p>
</td>
</tr>
</tbody>
</table>

