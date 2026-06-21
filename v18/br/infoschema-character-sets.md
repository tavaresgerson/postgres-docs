## 35.7. `character_sets` [#](#INFOSCHEMA-CHARACTER-SETS)

A vista `character_sets` identifica os conjuntos de caracteres disponíveis no banco de dados atual. Como o PostgreSQL não suporta múltiplos conjuntos de caracteres dentro de um único banco de dados, essa vista mostra apenas um, que é o codificação do banco de dados.

Observe como os seguintes termos são utilizados no padrão SQL:

repertório de caracteres: Uma coleção abstrata de caracteres, por exemplo `UNICODE`, `UCS` ou `LATIN1`. Não exposto como um objeto SQL, mas visível nesta visualização.

forma de codificação de caracteres: Uma codificação de algum repertório de caracteres. A maioria dos repertórios de caracteres mais antigos usa apenas uma forma de codificação, e, portanto, não há nomes separados para eles (por exemplo, `LATIN2` é uma forma de codificação aplicável ao repertório `LATIN2`). Mas, por exemplo, o Unicode tem as formas de codificação `UTF8`, `UTF16`, etc. (não todas suportadas pelo PostgreSQL). As formas de codificação não são exibidas como um objeto SQL, mas são visíveis nesta visualização.

conjunto de caracteres: Um objeto SQL nomeado que identifica um repertório de caracteres, um codificação de caracteres e uma ordenação padrão. Um conjunto de caracteres predefinido geralmente teria o mesmo nome que uma forma de codificação, mas os usuários poderiam definir outros nomes. Por exemplo, o conjunto de caracteres `UTF8` geralmente identificaria o repertório de caracteres `UCS`, a forma de codificação `UTF8` e algumas ordenações padrão.

Você pode considerar um "codificação" no PostgreSQL como um conjunto de caracteres ou uma forma de codificação de caracteres. Eles terão o mesmo nome e só podem haver um em um banco de dados.

**Tabela 35.5. Colunas `character_sets`**



<table border="1" class="table" summary="character_sets Columns">
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
      character_set_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Character sets are currently not implemented as schema objects, so this column is null.
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
     Character sets are currently not implemented as schema objects, so this column is null.
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
     Name of the character set, currently implemented as showing the name of the database encoding
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      character_repertoire
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Character repertoire, showing
     <code class="literal">
      UCS
     </code>
     if the encoding is
     <code class="literal">
      UTF8
     </code>
     , else just the encoding name
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      form_of_use
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Character encoding form, same as the database encoding
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      default_collate_catalog
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the database containing the default collation (always the current database, if any collation is identified)
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      default_collate_schema
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the schema containing the default collation
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      default_collate_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>
     Name of the default collation.  The default collation is identified as the collation that matches the
     <code class="literal">
      COLLATE
     </code>
     and
     <code class="literal">
      CTYPE
     </code>
     settings of the current database.  If there is no such collation, then this column and the associated schema and catalog columns are null.
    </p>
</td>
</tr>
</tbody>
</table>

