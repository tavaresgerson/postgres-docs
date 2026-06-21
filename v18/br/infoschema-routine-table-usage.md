## 35.44. `routine_table_usage` [#](#INFOSCHEMA-ROUTINE-TABLE-USAGE)

A vista `routine_table_usage` é destinada a identificar todas as tabelas que são utilizadas por uma função ou procedimento. Essas informações atualmente não são rastreadas pelo PostgreSQL.

**Tabela 35.42. Colunas `routine_table_usage`**



<table border="1" class="table" summary="routine_table_usage Columns">
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
      specific_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the database containing the function (always the current database)
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      specific_schema
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the schema containing the function
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      specific_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     The
     <span class="quote">
      “
      <span class="quote">
       specific name
      </span>
      ”
     </span>
     of the function.  See
     <a class="xref" href="infoschema-routines.md" title="35.45. routines">
      Section 35.45
     </a>
     for more information.
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      routine_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the database containing the function (always the current database)
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      routine_schema
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the schema containing the function
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      routine_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the function (might be duplicated in case of overloading)
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
     Name of the database that contains the table that is used by the function (always the current database)
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
     Name of the schema that contains the table that is used by the function
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
     Name of the table that is used by the function
    </p>
</td>
</tr>
</tbody>
</table>

