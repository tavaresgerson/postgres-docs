## 35.35. `role_column_grants` [#](#INFOSCHEMA-ROLE-COLUMN-GRANTS)

A vista `role_column_grants` identifica todos os privilégios concedidos em colunas onde o concedente ou o beneficiário é um papel habilitado atualmente. Mais informações podem ser encontradas em `column_privileges`. A única diferença efetiva entre esta vista e `column_privileges` é que esta vista omite as colunas que foram tornadas acessíveis ao usuário atual por meio de uma concessão para `PUBLIC`.

**Tabela 35.33. Colunas `role_column_grants`**



<table border="1" class="table" summary="role_column_grants Columns">
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
      grantor
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the role that granted the privilege
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      grantee
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the role that the privilege was granted to
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
     Name of the database that contains the table that contains the column (always the current database)
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
     Name of the schema that contains the table that contains the column
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
     Name of the table that contains the column
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
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      privilege_type
     </code>
<code class="type">
      character_data
     </code>
</p>
<p>
     Type of the privilege:
     <code class="literal">
      SELECT
     </code>
     ,
     <code class="literal">
      INSERT
     </code>
     ,
     <code class="literal">
      UPDATE
     </code>
     , or
     <code class="literal">
      REFERENCES
     </code>
</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      is_grantable
     </code>
<code class="type">
      yes_or_no
     </code>
</p>
<p>
<code class="literal">
      YES
     </code>
     if the privilege is grantable,
     <code class="literal">
      NO
     </code>
     if not
    </p>
</td>
</tr>
</tbody>
</table>

