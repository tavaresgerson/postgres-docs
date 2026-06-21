## 35.22. `domain_udt_usage` [#](#INFOSCHEMA-DOMAIN-UDT-USAGE)

A visão `domain_udt_usage` identifica todos os domínios que são baseados em tipos de dados de propriedade de um papel habilitado atualmente. Observe que, no PostgreSQL, os tipos de dados integrados se comportam como tipos definidos pelo usuário, então eles também são incluídos aqui.

**Tabela 35.20. Colunas `domain_udt_usage`**



<table border="1" class="table" summary="domain_udt_usage Columns">
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
      udt_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the database that the domain data type is defined in (always the current database)
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      udt_schema
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the schema that the domain data type is defined in
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      udt_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the domain data type
    </p>
</td>
</tr>
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
     Name of the database that contains the domain (always the current database)
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
     Name of the schema that contains the domain
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
</tbody>
</table>

