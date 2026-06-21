## 35.59. `usage_privileges` [#](#INFOSCHEMA-USAGE-PRIVILEGES)

A visão `usage_privileges` identifica os privilégios `USAGE` concedidos em vários tipos de objetos a um papel atualmente habilitado ou por um papel atualmente habilitado. No PostgreSQL, isso se aplica atualmente a colateias, domínios, wrappers de dados externos, servidores externos e sequências. Há uma linha para cada combinação de objeto, concedente e beneficiário.

Como as colatações não têm privilégios reais no PostgreSQL, essa visão mostra privilégios não grantables implícitos `USAGE` concedidos pelo proprietário para `PUBLIC` para todas as colatações. Os outros tipos de objetos, no entanto, mostram privilégios reais.

No PostgreSQL, as sequências também suportam os privilégios `SELECT` e `UPDATE`, além do privilégio `USAGE`. Estes são não padrão e, portanto, não são visíveis no esquema de informações.

**Tabela 35.57. Colunas `usage_privileges`**



<table border="1" class="table" summary="usage_privileges Columns">
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
      object_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the database containing the object (always the current database)
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      object_schema
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the schema containing the object, if applicable, else an empty string
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      object_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the object
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      object_type
     </code>
<code class="type">
      character_data
     </code>
</p>
<p>
<code class="literal">
      COLLATION
     </code>
     or
     <code class="literal">
      DOMAIN
     </code>
     or
     <code class="literal">
      FOREIGN DATA WRAPPER
     </code>
     or
     <code class="literal">
      FOREIGN SERVER
     </code>
     or
     <code class="literal">
      SEQUENCE
     </code>
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
     Always
     <code class="literal">
      USAGE
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

