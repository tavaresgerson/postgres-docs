## 35.21. `domain_constraints` [#](#INFOSCHEMA-DOMAIN-CONSTRAINTS)

A vista `domain_constraints` contém todas as restrições que pertencem a domínios definidos no banco de dados atual. Apenas os domínios que o usuário atual tem acesso (como proprietário ou com algum privilégio) são mostrados.

**Tabela 35.19. Colunas `domain_constraints`**



<table border="1" class="table" summary="domain_constraints Columns">
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
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      is_deferrable
     </code>
<code class="type">
      yes_or_no
     </code>
</p>
<p>
<code class="literal">
      YES
     </code>
     if the constraint is deferrable,
     <code class="literal">
      NO
     </code>
     if not
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      initially_deferred
     </code>
<code class="type">
      yes_or_no
     </code>
</p>
<p>
<code class="literal">
      YES
     </code>
     if the constraint is deferrable and initially deferred,
     <code class="literal">
      NO
     </code>
     if not
    </p>
</td>
</tr>
</tbody>
</table>

