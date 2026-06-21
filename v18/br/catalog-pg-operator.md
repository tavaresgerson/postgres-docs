## 52.34. `pg_operator` [#](#CATALOG-PG-OPERATOR)

O catálogo `pg_operator` armazena informações sobre operadores. Consulte [CREATE OPERATOR](sql-createoperator.md "CREATE OPERATOR") e [Seção 36.14](xoper.md "36.14. User-Defined Operators") para obter mais informações.

**Tabela 52.34. Colunas `pg_operator`**



<table border="1" class="table" summary="pg_operator Columns">
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
      oprname
     </code>
<code class="type">
      name
     </code>
</p>
<p>Nome do operador</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      oprnamespace
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
<p>O OID do espaço de nome que contém este operador</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      oprowner
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
<p>Proprietário do operador</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      oprkind
     </code>
<code class="type">
      char
     </code>
</p>
<p>
<code class="literal">
      b
     </code>= operador infix (<span class="quote">“<span class="quote">ambos</span>”</span>), ou<code class="literal">
      l
     </code>= operador prefixo (<span class="quote">“<span class="quote">esquerda</span>”</span>)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      oprcanmerge
     </code>
<code class="type">
      bool
     </code>
</p>
<p>Este operador suporta junções de fusão</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      oprcanhash
     </code>
<code class="type">
      bool
     </code>
</p>
<p>Este operador suporta junções de hash</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      oprleft
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
<code class="structname">
       pg_type
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>Tipo do operando esquerdo (zero para um operador prefixo)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      oprright
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
<code class="structname">
       pg_type
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>Tipo do operador de direita</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      oprresult
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
<code class="structname">
       pg_type
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>Tipo do resultado (zero para ainda não definido<span class="quote">“<span class="quote">casca</span>”</span>operador)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      oprcom
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-operator.md" title="52.34. pg_operator">
<code class="structname">
       pg_operator
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>Comutador deste operador (zero se nenhum)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      oprnegate
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-operator.md" title="52.34. pg_operator">
<code class="structname">
       pg_operator
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>Negador desse operador (zero se nenhum)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      oprcode
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
<p>Função que implementa esse operador (zero para um ainda não definido<span class="quote">“<span class="quote">casca</span>”</span>operador)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      oprrest
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
<p>Função de estimativa de seletividade de restrição para este operador (zero se não houver)</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      oprjoin
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
<p>Função de estimativa de seletividade para este operador (zero se não houver)</p>
</td>
</tr>
</tbody>
</table>

