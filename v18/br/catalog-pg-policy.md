## 52.38. `pg_policy` [#](#CATALOG-PG-POLICY)

O catálogo `pg_policy` armazena políticas de segurança de nível de linha para tabelas. Uma política inclui o tipo de comando que ela aplica (possivelmente todos os comandos), os papéis aos quais ela se aplica, a expressão que será adicionada como qualificação de barreira de segurança a consultas que incluem a tabela e a expressão que será adicionada como opção `WITH CHECK` para consultas que tentam adicionar novos registros à tabela.

**Tabela 52.38. Colunas `pg_policy`**



<table border="1" class="table" summary="pg_policy Columns">
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
      polname
     </code>
<code class="type">
      name
     </code>
</p>
<p>O nome da política</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      polrelid
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
<p>A tabela à qual a política se aplica</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      polcmd
     </code>
<code class="type">
      char
     </code>
</p>
<p>O tipo de comando ao qual a política é aplicada:<code class="literal">
      r
     </code>para<a class="xref" href="sql-select.md" title="SELECT">
<span class="refentrytitle">SELECIONE</span>
</a>,<code class="literal">
      a
     </code>para<a class="xref" href="sql-insert.md" title="INSERT">
<span class="refentrytitle">INSERT</span>
</a>,<code class="literal">
      w
     </code>para<a class="xref" href="sql-update.md" title="UPDATE">
<span class="refentrytitle">ATUALIZAÇÃO</span>
</a>,<code class="literal">
      d
     </code>para<a class="xref" href="sql-delete.md" title="DELETE">
<span class="refentrytitle">DELETE</span>
</a>ou<code class="literal">
      *
     </code>para todos</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      polpermissive
     </code>
<code class="type">
      bool
     </code>
</p>
<p>A política é permissiva ou restritiva?</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      polroles
     </code>
<code class="type">
      oid[]
     </code>(referências<a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
<code class="structname">
       pg_authid
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>Os papéis aos quais a política é aplicada; zero significa<code class="literal">
      PUBLIC
     </code>(e normalmente aparece sozinho na matriz)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      polqual
     </code>
<code class="type">
      pg_node_tree
     </code>
</p>
<p>A expressão que será adicionada às qualificações da barreira de segurança para consultas que utilizam a tabela</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      polwithcheck
     </code>
<code class="type">
      pg_node_tree
     </code>
</p>
<p>A expressão da árvore que será adicionada às qualificações WITH CHECK para consultas que tentam adicionar linhas à tabela</p>
</td>
</tr>
</tbody>
</table>




  

### Nota

As políticas armazenadas em `pg_policy` são aplicadas apenas quando `pg_class`(catalog-pg-class.md "52.11. pg_class").`relrowsecurity` está definido para sua tabela.