## 35.29. `foreign_servers` [#](#INFOSCHEMA-FOREIGN-SERVERS)

A vista `foreign_servers` contém todos os servidores externos definidos no banco de dados atual. Apenas os servidores externos que o usuário atual tem acesso (como proprietário ou com algum privilégio) são mostrados.

**Tabela 35.27. Colunas `foreign_servers`**



<table border="1" class="table" summary="foreign_servers Columns">
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
      foreign_server_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the database that the foreign server is defined in (always the current database)
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      foreign_server_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the foreign server
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      foreign_data_wrapper_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the database that contains the foreign-data wrapper used by the foreign server (always the current database)
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      foreign_data_wrapper_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the foreign-data wrapper used by the foreign server
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      foreign_server_type
     </code>
<code class="type">
      character_data
     </code>
</p>
<p>
     Foreign server type information, if specified upon creation
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      foreign_server_version
     </code>
<code class="type">
      character_data
     </code>
</p>
<p>
     Foreign server version information, if specified upon creation
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      authorization_identifier
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the owner of the foreign server
    </p>
</td>
</tr>
</tbody>
</table>

