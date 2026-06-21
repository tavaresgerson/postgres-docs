## 35.8. `check_constraint_routine_usage` [#](#INFOSCHEMA-CHECK-CONSTRAINT-ROUTINE-USAGE)

A vista `check_constraint_routine_usage` identifica rotinas (funções e procedimentos) que são usadas por uma restrição de verificação. Apenas as rotinas que pertencem a um papel habilitado atualmente são mostradas.

**Tabela 35.6. Colunas `check_constraint_routine_usage`**



<table border="1" class="table" summary="check_constraint_routine_usage Columns">
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
     Name of the database containing the constraint (always the current database)
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
     Name of the schema containing the constraint
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
</tbody>
</table>

