## 35.30. `foreign_table_options` [#](#INFOSCHEMA-FOREIGN-TABLE-OPTIONS)

A vista `foreign_table_options` contém todas as opções definidas para tabelas externas no banco de dados atual. Apenas as tabelas externas que o usuário atual tem acesso (como proprietário ou com algum privilégio) são mostradas.

**Tabela 35.28. Colunas `foreign_table_options`**



<table border="1" class="table" summary="foreign_table_options Columns">
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
      foreign_table_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the database that contains the foreign table (always the current database)
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      foreign_table_schema
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the schema that contains the foreign table
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      foreign_table_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the foreign table
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      option_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of an option
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      option_value
     </code>
<code class="type">
      character_data
     </code>
</p>
<p>
     Value of the option
    </p>
</td>
</tr>
</tbody>
</table>

