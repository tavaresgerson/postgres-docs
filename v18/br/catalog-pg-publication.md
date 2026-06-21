## 52.40. `pg_publication` [#](#CATALOG-PG-PUBLICATION)

O catálogo `pg_publication` contém todas as publicações criadas no banco de dados. Para mais informações sobre publicações, consulte [Seção 29.1][(logical-replication-publication.md "29.1. Publication")].

**Tabela 52.40. Colunas `pg_publication`**



<table border="1" class="table" summary="pg_publication Columns">
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
      pubname
     </code>
<code class="type">
      name
     </code>
</p>
<p>Nome da publicação</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      pubowner
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
<p>Proprietário da publicação</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      puballtables
     </code>
<code class="type">
      bool
     </code>
</p>
<p>Se for verdade, essa publicação inclui automaticamente todas as tabelas no banco de dados, incluindo aquelas que serão criadas no futuro.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      pubinsert
     </code>
<code class="type">
      bool
     </code>
</p>
<p>Se for verdade,<a class="xref" href="sql-insert.md" title="INSERT">
<span class="refentrytitle">INSERT</span>
</a>As operações são replicadas para tabelas na publicação.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      pubupdate
     </code>
<code class="type">
      bool
     </code>
</p>
<p>Se for verdade,<a class="xref" href="sql-update.md" title="UPDATE">
<span class="refentrytitle">ATUALIZAÇÃO</span>
</a>As operações são replicadas para tabelas na publicação.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      pubdelete
     </code>
<code class="type">
      bool
     </code>
</p>
<p>Se for verdade,<a class="xref" href="sql-delete.md" title="DELETE">
<span class="refentrytitle">DELETE</span>
</a>As operações são replicadas para tabelas na publicação.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      pubtruncate
     </code>
<code class="type">
      bool
     </code>
</p>
<p>Se for verdade,<a class="xref" href="sql-truncate.md" title="TRUNCATE">
<span class="refentrytitle">TRUNCATE</span>
</a>As operações são replicadas para tabelas na publicação.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      pubviaroot
     </code>
<code class="type">
      bool
     </code>
</p>
<p>Se for verdade, as operações em uma partição de folha são replicadas usando a identidade e o esquema de seu ancestral particionado mais alto mencionado na publicação, em vez do seu próprio.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      pubgencols
     </code>
<code class="type">
      char
     </code>
</p>
<p>Controla como lidar com a replicação de coluna gerada quando não há uma lista de colunas de publicação:<code class="literal">
      n
     </code>= as colunas geradas nas tabelas associadas à publicação não devem ser replicadas,<code class="literal">
      s
     </code>= as colunas geradas armazenadas nas tabelas associadas à publicação devem ser replicadas.</p>
</td>
</tr>
</tbody>
</table>

