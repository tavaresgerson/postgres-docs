## 52.14. `pg_conversion` [#](#CATALOG-PG-CONVERSION)

O catálogo `pg_conversion` descreve as funções de conversão de codificação. Consulte [CREATE CONVERSION](sql-createconversion.md "CREATE CONVERSION") para obter mais informações.

**Tabela 52.14. Colunas `pg_conversion`**



<table border="1" class="table" summary="pg_conversion Columns">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="catalog_table_entry">
<p class="column_definition">Tipo de coluna</p>
<p>Descrição</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      oid
     </code>
<code class="type">
      oid
     </code>
</p>
<p>Identificador da linha</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      conname
     </code>
<code class="type">
      name
     </code>
</p>
<p>Nome de conversão (único dentro de um espaço de nomes)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      connamespace
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
<code class="structname">
       pg_namespace
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>O OID do espaço de nome que contém essa conversão</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      conowner
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
<code class="structname">
       pg_authid
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>Proprietário da conversão</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      conforencoding
     </code>
<code class="type">
      int4
     </code>
</p>
<p>ID de codificação de fonte (<a class="link" href="functions-info.md#PG-ENCODING-TO-CHAR">
<code class="function">
       pg_encoding_to_char()
      </code>
</a>pode traduzir esse número para o nome do codificação)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      contoencoding
     </code>
<code class="type">
      int4
     </code>
</p>
<p>ID de codificação de destino (<a class="link" href="functions-info.md#PG-ENCODING-TO-CHAR">
<code class="function">
       pg_encoding_to_char()
      </code>
</a>pode traduzir esse número para o nome do codificação)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      conproc
     </code>
<code class="type">
      regproc
     </code>(referências<a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
<code class="structname">
       pg_proc
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>Função de conversão</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      condefault
     </code>
<code class="type">
      bool
     </code>
</p>
<p>Verdadeiro se esta for a conversão padrão</p>
</td>
</tr>
</tbody>
</table>

