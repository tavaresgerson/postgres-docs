## 52.50. `pg_shseclabel` [#](#CATALOG-PG-SHSECLABEL)

O catálogo `pg_shseclabel` armazena rótulos de segurança em objetos de banco de dados compartilhados. Os rótulos de segurança podem ser manipulados com o comando `SECURITY LABEL`(sql-security-label.md "SECURITY LABEL"). Para uma maneira mais fácil de visualizar os rótulos de segurança, consulte [Seção 53.23][(view-pg-seclabels.md "53.23. pg_seclabels")].

Veja também `pg_seclabel` (catalog-pg-seclabel.md "52.46. pg_seclabel"), que realiza uma função semelhante para etiquetas de segurança que envolvem objetos dentro de um único banco de dados.

Ao contrário da maioria dos catálogos de sistema, o `pg_shseclabel` é compartilhado em todos os bancos de dados de um clúster: há apenas uma cópia do `pg_shseclabel` por clúster, não uma por banco de dados.

**Tabela 52.50. Colunas `pg_shseclabel`**



<table border="1" class="table" summary="pg_shseclabel Columns">
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

