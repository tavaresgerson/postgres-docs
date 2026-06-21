## 52.10. `pg_cast` [#](#CATALOG-PG-CAST)

O catálogo `pg_cast` armazena caminhos de conversão de tipos de dados, tanto os pré-definidos quanto os definidos pelo usuário.

Deve-se notar que `pg_cast` não representa todo o tipo de conversão que o sistema sabe como realizar; apenas aquelas que não podem ser deduzidas a partir de alguma regra genérica. Por exemplo, a conversão entre um domínio e seu tipo base não é explicitamente representada em `pg_cast`. Outra exceção importante é que as "conversões de E/S automáticas", as realizadas usando as próprias funções de E/S de um tipo de dados para converter para ou a partir de `text` ou outros tipos de string, não são explicitamente representadas em `pg_cast`.

**Tabela 52.10. Colunas `pg_cast`**



<table border="1" class="table" summary="pg_cast Columns">
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
      castsource
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
<p>OID do tipo de dados de origem</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      casttarget
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
<p>OID do tipo de dados-alvo</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      castfunc
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
<code class="structname">
       pg_proc
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>O OID da função a ser usada para realizar essa conversão. Zero é armazenado se o método de conversão não exigir uma função.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      castcontext
     </code>
<code class="type">
      char
     </code>
</p>
<p>Indica em quais contextos o cast pode ser invocado.<code class="literal">
      e
     </code>significa apenas como um elenco explícito (usando<code class="literal">
      CAST
     </code>ou<code class="literal">
      ::
     </code>
     syntax).
     <code class="literal">
      a
     </code>significa implicitamente na atribuição a uma coluna de destino, bem como explicitamente.<code class="literal">
      i
     </code>significa implicitamente em expressões, bem como em outros casos.</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      castmethod
     </code>
<code class="type">
      char
     </code>
</p>
<p>Indica como o elenco é realizado.<code class="literal">
      f
     </code>significa que a função especificada no<code class="structfield">
      castfunc
     </code>campo é utilizado.<code class="literal">
      i
     </code>significa que as funções de entrada/saída são utilizadas.<code class="literal">
      b
     </code>Isso significa que os tipos são binariamente coeríveis, portanto, nenhuma conversão é necessária.</p>
</td>
</tr>
</tbody>
</table>




  

As funções de cast listadas em `pg_cast` devem sempre receber o tipo de fonte de cast como seu primeiro tipo de argumento e retornar o tipo de destino de cast como seu tipo de resultado. Uma função de cast pode ter até três argumentos. O segundo argumento, se presente, deve ser do tipo `integer`; ele recebe o modificador de tipo associado ao tipo de destino, ou -1 se não houver nenhum. O terceiro argumento, se presente, deve ser do tipo `boolean`; ele recebe `true` se a cast for uma cast explícita, `false` caso contrário.

É legítimo criar uma entrada `pg_cast` na qual os tipos de origem e destino sejam os mesmos, se a função associada receber mais de um argumento. Tais entradas representam "funções de coerção de comprimento" que coagem valores do tipo a serem legais para um valor específico do modificador de tipo.

Quando uma entrada `pg_cast` tem diferentes tipos de origem e destino e uma função que aceita mais de um argumento, ela representa a conversão de um tipo para outro e a aplicação de uma coerção de comprimento em um único passo. Quando não há tal entrada disponível, a coerção para um tipo que utiliza um modificador de tipo envolve dois passos, um para converter entre tipos de dados e um segundo para aplicar o modificador.