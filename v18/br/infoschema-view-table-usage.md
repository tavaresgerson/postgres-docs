## 35.65. `view_table_usage` [#](#INFOSCHEMA-VIEW-TABLE-USAGE)

A vista `view_table_usage` identifica todas as tabelas que são usadas na expressão de consulta de uma vista (a declaração `SELECT` que define a vista). Uma tabela só é incluída se essa tabela for de propriedade de um papel atualmente habilitado.

### Nota

As tabelas do sistema não estão incluídas. Isso deve ser corrigido em algum momento.

**Tabela 35.63. Colunas `view_table_usage`**



<table border="1" class="table" summary="view_table_usage Columns">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="catalog_table_entry">
<p class="column_definition">
     Column Type
    </p>
<p>
     Description
    </p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      view_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the database that contains the view (always the current database)
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      view_schema
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the schema that contains the view
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      view_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the view
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      table_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the database that contains the table that is used by the view (always the current database)
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      table_schema
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the schema that contains the table that is used by the view
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      table_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the table that is used by the view
    </p>
</td>
</tr>
</tbody>
</table>

