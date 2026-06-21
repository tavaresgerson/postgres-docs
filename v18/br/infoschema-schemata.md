## 35.46. `schemata` [#](#INFOSCHEMA-SCHEMATA)

A vista `schemata` contém todos os esquemas no banco de dados atual que o usuário atual tem acesso (sendo o proprietário ou tendo algum privilégio).

**Tabela 35.44. Colunas `schemata`**



<table border="1" class="table" summary="schemata Columns">
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
      catalog_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the database that the schema is contained in (always the current database)
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      schema_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the schema
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      schema_owner
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the owner of the schema
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      default_character_set_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      default_character_set_schema
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      default_character_set_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      sql_path
     </code>
<code class="type">
      character_data
     </code>
</p>
<p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
</p>
</td>
</tr>
</tbody>
</table>

