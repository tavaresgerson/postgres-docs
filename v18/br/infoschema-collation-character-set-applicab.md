## 35.11. `collation_character_set_​applicability` [#](#INFOSCHEMA-COLLATION-CHARACTER-SET-APPLICAB)

A vista `collation_character_set_applicability` identifica qual conjunto de caracteres os colagens disponíveis são aplicáveis. No PostgreSQL, há apenas um conjunto de caracteres por banco de dados (veja a explicação em [Seção 35.7][(infoschema-character-sets.md "35.7. character_sets")]), então essa vista não fornece muita informação útil.

**Tabela 35.9. Colunas `collation_character_set_applicability`**



<table border="1" class="table" summary="collation_character_set_applicability Columns">
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
      collation_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the database containing the collation (always the current database)
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      collation_schema
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the schema containing the collation
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      collation_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the default collation
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      character_set_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Character sets are currently not implemented as schema objects, so this column is null
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      character_set_schema
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Character sets are currently not implemented as schema objects, so this column is null
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      character_set_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the character set
    </p>
</td>
</tr>
</tbody>
</table>

