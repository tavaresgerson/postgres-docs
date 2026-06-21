## 35.60. `user_defined_types` [#](#INFOSCHEMA-USER-DEFINED-TYPES)

A vista `user_defined_types` atualmente contém todos os tipos compostos definidos no banco de dados atual. Apenas os tipos que o usuário atual tem acesso (como proprietário ou com algum privilégio) são mostrados.

O SQL conhece dois tipos definidos pelo usuário: tipos estruturados (também conhecidos como tipos compostos no PostgreSQL) e tipos distintos (não implementados no PostgreSQL). Para estar à prova do futuro, use a coluna `user_defined_type_category` para diferenciá-los. Outros tipos definidos pelo usuário, como tipos básicos e enums, que são extensões do PostgreSQL, não são mostrados aqui. Para domínios, consulte [Seção 35.23][(infoschema-domains.md "35.23. domains")] em vez disso.

**Tabela 35.58. Colunas `user_defined_types`**



<table border="1" class="table" summary="user_defined_types Columns">
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
      user_defined_type_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the database that contains the type (always the current database)
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      user_defined_type_schema
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the schema that contains the type
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      user_defined_type_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the type
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      user_defined_type_category
     </code>
<code class="type">
      character_data
     </code>
</p>
<p>
     Currently always
     <code class="literal">
      STRUCTURED
     </code>
</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      is_instantiable
     </code>
<code class="type">
      yes_or_no
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
      is_final
     </code>
<code class="type">
      yes_or_no
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
      ordering_form
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
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      ordering_category
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
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      ordering_routine_catalog
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
      ordering_routine_schema
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
      ordering_routine_name
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
      reference_type
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
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      data_type
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
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      character_maximum_length
     </code>
<code class="type">
      cardinal_number
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
      character_octet_length
     </code>
<code class="type">
      cardinal_number
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
      character_set_catalog
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
      character_set_schema
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
      character_set_name
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
      collation_catalog
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
      collation_schema
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
      collation_name
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
      numeric_precision
     </code>
<code class="type">
      cardinal_number
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
      numeric_precision_radix
     </code>
<code class="type">
      cardinal_number
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
      numeric_scale
     </code>
<code class="type">
      cardinal_number
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
      datetime_precision
     </code>
<code class="type">
      cardinal_number
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
      interval_type
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
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      interval_precision
     </code>
<code class="type">
      cardinal_number
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
      source_dtd_identifier
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
      ref_dtd_identifier
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
</tbody>
</table>

