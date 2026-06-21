## 53.12. `pg_indexes` [#](#VIEW-PG-INDEXES)

A vista `pg_indexes` fornece acesso a informações úteis sobre cada índice no banco de dados.

**Tabela 53.12. Colunas `pg_indexes`**



<table border="1" class="table" summary="pg_indexes Columns">
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
      schemaname
     </code>
<code class="type">
      name
     </code>(referências<a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
<code class="structname">
       pg_namespace
      </code>
</a>
     .
     <code class="structfield">
      nspname
     </code>)</p>
<p>Nome do esquema que contém a tabela e o índice</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      tablename
     </code>
<code class="type">
      name
     </code>(referências<a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
<code class="structname">
       pg_class
      </code>
</a>
     .
     <code class="structfield">
      relname
     </code>)</p>
<p>Nome da tabela para a qual o índice está sendo criado</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      indexname
     </code>
<code class="type">
      name
     </code>(referências<a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
<code class="structname">
       pg_class
      </code>
</a>
     .
     <code class="structfield">
      relname
     </code>)</p>
<p>Nome do índice</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      tablespace
     </code>
<code class="type">
      name
     </code>(referências<a class="link" href="catalog-pg-tablespace.md" title="52.56. pg_tablespace">
<code class="structname">
       pg_tablespace
      </code>
</a>
     .
     <code class="structfield">
      spcname
     </code>)</p>
<p>Nome do espaço de tabela que contém o índice (nulo se for o padrão para o banco de dados)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      indexdef
     </code>
<code class="type">
      text
     </code>
</p>
<p>Definição do índice (reconstruído<a class="xref" href="sql-createindex.md" title="CREATE INDEX">
<span class="refentrytitle">Crie índice</span>
</a>comando)</p>
</td>
</tr>
</tbody>
</table>

