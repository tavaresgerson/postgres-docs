## 52.46. `pg_seclabel` [#](#CATALOG-PG-SECLABEL)

O catálogo `pg_seclabel` armazena rótulos de segurança em objetos do banco de dados. Os rótulos de segurança podem ser manipulados com o comando `SECURITY LABEL`(sql-security-label.md "SECURITY LABEL"). Para uma maneira mais fácil de visualizar os rótulos de segurança, consulte [Seção 53.23][(view-pg-seclabels.md "53.23. pg_seclabels")].

Veja também `pg_shseclabel` (catalog-pg-shseclabel.md "52.50. pg_shseclabel"), que realiza uma função semelhante para etiquetas de segurança de objetos de banco de dados que são compartilhados em um clúster de banco de dados.

**Tabela 52.46. Colunas `pg_seclabel`**



<table border="1" class="table" summary="pg_seclabel Columns">
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
      objoid
     </code>
<code class="type">
      oid
     </code>(referência a qualquer coluna OID)</p>
<p>O OID do objeto a que este rótulo de segurança se refere</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      classoid
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
<code class="structname">
       pg_class
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>O OID do catálogo do sistema em que esse objeto aparece</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      objsubid
     </code>
<code class="type">
      int4
     </code>
</p>
<p>Para uma etiqueta de segurança em uma coluna de mesa, este é o número da coluna (o<code class="structfield">
      objoid
     </code>e<code class="structfield">
      classoid
     </code>refere-se à própria tabela). Para todos os outros tipos de objeto, essa coluna é zero.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      provider
     </code>
<code class="type">
      text
     </code>
</p>
<p>O fornecedor de rótulos associado a este rótulo.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      label
     </code>
<code class="type">
      text
     </code>
</p>
<p>O rótulo de segurança aplicado a este objeto.</p>
</td>
</tr>
</tbody>
</table>

