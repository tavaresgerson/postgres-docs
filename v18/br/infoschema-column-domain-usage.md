## 35.13. `column_domain_usage` [#](#INFOSCHEMA-COLUMN-DOMAIN-USAGE)

A vista `column_domain_usage` identifica todas as colunas (de uma tabela ou de uma vista) que utilizam algum domínio definido no banco de dados atual e que pertence a um papel habilitado atualmente.

**Tabela 35.11. Colunas `column_domain_usage`**



<table border="1" class="table" summary="column_domain_usage Columns">
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
      domain_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the database containing the domain (always the current database)
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      domain_schema
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the schema containing the domain
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      domain_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the domain
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
     Name of the database containing the table (always the current database)
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
     Name of the schema containing the table
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
     Name of the table
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      column_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the column
    </p>
</td>
</tr>
</tbody>
</table>

