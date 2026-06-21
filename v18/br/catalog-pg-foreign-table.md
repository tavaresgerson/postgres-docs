## 52.25. `pg_foreign_table` [#](#CATALOG-PG-FOREIGN-TABLE)

O catálogo `pg_foreign_table` contém informações auxiliares sobre tabelas estrangeiras. Uma tabela estrangeira é representada principalmente por uma entrada [`pg_class`](catalog-pg-class.md "52.11. pg_class"), assim como uma tabela regular. Sua entrada `pg_foreign_table` contém as informações que são pertinentes apenas para tabelas estrangeiras e não para qualquer outro tipo de relação.

**Tabela 52.25. Colunas `pg_foreign_table`**



<table border="1" class="table" summary="pg_foreign_table Columns">
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
      ftrelid
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
<code class="structname">
       pg_class
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>O OID do<a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
<code class="structname">
       pg_class
      </code>
</a>entrada para esta mesa estrangeira</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      ftserver
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
<p>OID do servidor estrangeiro para esta tabela estrangeira</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      ftoptions
     </code>
<code class="type">
      text[]
     </code>
</p>
<p>Opções de mesa estrangeiras, como<span class="quote">“<span class="quote">palavra-chave=valor</span>”</span>cordas</p>
</td>
</tr>
</tbody>
</table>

