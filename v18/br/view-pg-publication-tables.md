## 53.18. `pg_publication_tables` [#](#VIEW-PG-PUBLICATION-TABLES)

A vista `pg_publication_tables` fornece informações sobre o mapeamento entre as publicações e as informações das tabelas que elas contêm. Ao contrário do catálogo subjacente `pg_publication_rel`(catalog-pg-publication-rel.md "52.42. pg_publication_rel"), essa vista expande as publicações definidas como `FOR ALL TABLES`(sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-ALL-TABLES) e `FOR TABLES IN SCHEMA`(sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLES-IN-SCHEMA), portanto, para tais publicações, haverá uma linha para cada tabela elegível.

**Tabela 53.18. Colunas `pg_publication_tables`**



<table border="1" class="table" summary="pg_publication_tables Columns">
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
      pubname
     </code>
<code class="type">
      name
     </code>(referências<a class="link" href="catalog-pg-publication.md" title="52.40. pg_publication">
<code class="structname">
       pg_publication
      </code>
</a>
     .
     <code class="structfield">
      pubname
     </code>)</p>
<p>Nome da publicação</p>
</td>
</tr>
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
<p>Nome do esquema que contém a tabela</p>
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
<p>Nome da tabela</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      attnames
     </code>
<code class="type">
      name[]
     </code>(referências<a class="link" href="catalog-pg-attribute.md" title="52.7. pg_attribute">
<code class="structname">
       pg_attribute
      </code>
</a>
     .
     <code class="structfield">
      attname
     </code>)</p>
<p>Nomes das colunas da tabela incluídos na publicação. Isso contém todas as colunas da tabela quando o usuário não especificou a lista de colunas para a tabela.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      rowfilter
     </code>
<code class="type">
      text
     </code>
</p>
<p>Expressão para a condição de qualificação da publicação da tabela</p>
</td>
</tr>
</tbody>
</table>

