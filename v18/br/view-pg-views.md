## 53.37. `pg_views` [#](#VIEW-PG-VIEWS)

A vista `pg_views` fornece acesso a informações úteis sobre cada vista no banco de dados.

**Tabela 53.37. Colunas `pg_views`**



<table border="1" class="table" summary="pg_views Columns">
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
<p>Nome do esquema que contém a visualização</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      viewname
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
<p>Nome da vista</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      viewowner
     </code>
<code class="type">
      name
     </code>(referências<a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
<code class="structname">
       pg_authid
      </code>
</a>
     .
     <code class="structfield">
      rolname
     </code>)</p>
<p>Nome do proprietário da visualização</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      definition
     </code>
<code class="type">
      text
     </code>
</p>
<p>Veja a definição (reconstruída<a class="xref" href="sql-select.md" title="SELECT">
<span class="refentrytitle">SELECIONE</span>
</a>(consulta)</p>
</td>
</tr>
</tbody>
</table>

