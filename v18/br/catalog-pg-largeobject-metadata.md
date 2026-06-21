## 52.31. `pg_largeobject_metadata` [#](#CATALOG-PG-LARGEOBJECT-METADATA)

O catálogo `pg_largeobject_metadata` contém metadados associados a objetos grandes. Os dados reais dos objetos grandes são armazenados em `pg_largeobject`(catalog-pg-largeobject.md "52.30. pg_largeobject").

**Tabela 52.31. Colunas `pg_largeobject_metadata`**



<table border="1" class="table" summary="pg_largeobject_metadata Columns">
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
      lomowner
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
<p>Proprietário do grande objeto</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      lomacl
     </code>
<code class="type">
      aclitem[]
     </code>
</p>
<p>Privilegios de acesso; veja<a class="xref" href="ddl-priv.md" title="5.8. Privileges">Seção 5.8</a>para detalhes</p>
</td>
</tr>
</tbody>
</table>

