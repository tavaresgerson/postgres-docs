## 35.19. `constraint_table_usage` [#](#INFOSCHEMA-CONSTRAINT-TABLE-USAGE)

A vista `constraint_table_usage` identifica todas as tabelas no banco de dados atual que são usadas por alguma restrição e que pertencem a um papel atualmente habilitado. (Isso é diferente da vista `table_constraints`, que identifica todas as restrições de tabela juntamente com a tabela em que elas são definidas.) Para uma restrição de chave estrangeira, essa vista identifica a tabela que a chave estrangeira referencia. Para uma restrição de chave única ou primária, essa vista simplesmente identifica a tabela à qual a restrição pertence. As restrições de verificação e as restrições não nulos não são incluídas nesta vista.

**Tabela 35.17. Colunas `constraint_table_usage`**



<table border="1" class="table" summary="constraint_table_usage Columns">
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
      table_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the database that contains the table that is used by some constraint (always the current database)
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
     Name of the schema that contains the table that is used by some constraint
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
     Name of the table that is used by some constraint
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      constraint_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the database that contains the constraint (always the current database)
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      constraint_schema
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the schema that contains the constraint
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      constraint_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the constraint
    </p>
</td>
</tr>
</tbody>
</table>

