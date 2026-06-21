## 35.55. `transforms` [#](#INFOSCHEMA-TRANSFORMS)

A vista `transforms` contém informações sobre as transformações definidas no banco de dados atual. Mais precisamente, ela contém uma linha para cada função contida em uma transformação (a função “de SQL” ou “para SQL”).

**Tabela 35.53. Colunas `transforms`**



<table border="1" class="table" summary="transforms Columns">
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
     Name of the database that contains the type the transform is for (always the current database)
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
     Name of the schema that contains the type the transform is for
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
     Name of the type the transform is for
    </p>
</td>
</tr>
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
      group_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     The SQL standard allows defining transforms in
     <span class="quote">
      “
      <span class="quote">
       groups
      </span>
      ”
     </span>
     , and selecting a group at run time.  PostgreSQL does not support this. Instead, transforms are specific to a language.  As a compromise, this field contains the language the transform is for.
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      transform_type
     </code>
<code class="type">
      character_data
     </code>
</p>
<p>
<code class="literal">
      FROM SQL
     </code>
     or
     <code class="literal">
      TO SQL
     </code>
</p>
</td>
</tr>
</tbody>
</table>

