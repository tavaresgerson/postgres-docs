## 52.19. `pg_description` [#](#CATALOG-PG-DESCRIPTION)

O catálogo `pg_description` armazena descrições opcionais (comentários) para cada objeto do banco de dados. As descrições podem ser manipuladas com o comando [`COMMENT`](sql-comment.md "COMMENT") e visualizadas com os comandos `\d` do psql. As descrições de muitos objetos de sistema embutidos são fornecidas nos conteúdos iniciais de `pg_description`.

Veja também `pg_shdescription` (catalog-pg-shdescription.md "52.49. pg_shdescription"), que realiza uma função semelhante para descrições que envolvem objetos que são compartilhados em um clúster de banco de dados.

**Tabela 52.19. Colunas `pg_description`**



<table border="1" class="table" summary="pg_description Columns">
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
<p>O OID do objeto a que esta descrição se refere</p>
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
<p>Para um comentário em uma coluna de tabela, este é o número da coluna (o<code class="structfield">
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
      description
     </code>
<code class="type">
      text
     </code>
</p>
<p>Texto arbitrário que serve como descrição deste objeto</p>
</td>
</tr>
</tbody>
</table>

