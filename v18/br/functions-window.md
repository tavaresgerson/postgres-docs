## 9.22. Funções de janela [#](#FUNCTIONS-WINDOW)

As funções de janela fornecem a capacidade de realizar cálculos em conjuntos de linhas relacionadas à linha atual da consulta. Consulte a Seção 3.5 para uma introdução a este recurso, e a Seção 4.2.8 para detalhes de sintaxe.

As funções de janela embutidas estão listadas em [Tabela 9.67](functions-window.md#FUNCTIONS-WINDOW-TABLE). Observe que essas funções *devem* ser invocadas usando a sintaxe da função de janela, ou seja, é necessária uma cláusula `OVER`.

Além dessas funções, qualquer agregado ordinário incorporado ou definido pelo usuário (ou seja, agregados que não são conjuntos ordenados ou conjuntos hipotéticos) pode ser usado como uma função de janela; consulte [Seção 9.21] para uma lista dos agregados incorporados. As funções de agregação atuam como funções de janela apenas quando uma cláusula (functions-aggregate.md "9.21. Aggregate Functions") segue a chamada; caso contrário, atuam como agregados comuns e retornam uma única linha para todo o conjunto.

**Tabela 9.67. Funções de janela de propósito geral**



<table border="1" class="table" summary="General-Purpose Window Functions">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      row_number
     </code>
     () →
     <code class="returnvalue">
      bigint
     </code>
    </p>
    <p>
     Returns the number of the current row within its partition, counting from 1.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      rank
     </code>
     () →
     <code class="returnvalue">
      bigint
     </code>
    </p>
    <p>
     Returns the rank of the current row, with gaps; that is, the
     <code class="function">
      row_number
     </code>
     of the first row in its peer group.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      dense_rank
     </code>
     () →
     <code class="returnvalue">
      bigint
     </code>
    </p>
    <p>
     Returns the rank of the current row, without gaps; this function effectively counts peer groups.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      percent_rank
     </code>
     () →
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Returns the relative rank of the current row, that is (
     <code class="function">
      rank
     </code>
     - 1) / (total partition rows - 1). The value thus ranges from 0 to 1 inclusive.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      cume_dist
     </code>
     () →
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Returns the cumulative distribution, that is (number of partition rows preceding or peers with current row) / (total partition rows). The value thus ranges from 1/
     <em class="parameter">
      <code>
       N
      </code>
     </em>
     to 1.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      ntile
     </code>
     (
     <em class="parameter">
      <code>
       num_buckets
      </code>
     </em>
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Returns an integer ranging from 1 to the argument value, dividing the partition as equally as possible.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      lag
     </code>
     (
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code class="type">
      anycompatible
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        offset
       </code>
      </em>
      <code class="type">
       integer
      </code>
      [
      <span class="optional">
       ,
       <em class="parameter">
        <code>
         default
        </code>
       </em>
       <code class="type">
        anycompatible
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code class="returnvalue">
      anycompatible
     </code>
    </p>
    <p>
     Returns
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     evaluated at the row that is
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     rows before the current row within the partition; if there is no such row, instead returns
     <em class="parameter">
      <code>
       default
      </code>
     </em>
     (which must be of a type compatible with
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     ). Both
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     and
     <em class="parameter">
      <code>
       default
      </code>
     </em>
     are evaluated with respect to the current row.  If omitted,
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     defaults to 1 and
     <em class="parameter">
      <code>
       default
      </code>
     </em>
     to
     <code class="literal">
      NULL
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      lead
     </code>
     (
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code class="type">
      anycompatible
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        offset
       </code>
      </em>
      <code class="type">
       integer
      </code>
      [
      <span class="optional">
       ,
       <em class="parameter">
        <code>
         default
        </code>
       </em>
       <code class="type">
        anycompatible
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code class="returnvalue">
      anycompatible
     </code>
    </p>
    <p>
     Returns
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     evaluated at the row that is
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     rows after the current row within the partition; if there is no such row, instead returns
     <em class="parameter">
      <code>
       default
      </code>
     </em>
     (which must be of a type compatible with
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     ). Both
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     and
     <em class="parameter">
      <code>
       default
      </code>
     </em>
     are evaluated with respect to the current row.  If omitted,
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     defaults to 1 and
     <em class="parameter">
      <code>
       default
      </code>
     </em>
     to
     <code class="literal">
      NULL
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      first_value
     </code>
     (
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code class="type">
      anyelement
     </code>
     ) →
     <code class="returnvalue">
      anyelement
     </code>
    </p>
    <p>
     Returns
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     evaluated at the row that is the first row of the window frame.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      last_value
     </code>
     (
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code class="type">
      anyelement
     </code>
     ) →
     <code class="returnvalue">
      anyelement
     </code>
    </p>
    <p>
     Returns
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     evaluated at the row that is the last row of the window frame.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      nth_value
     </code>
     (
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     <code class="type">
      anyelement
     </code>
     ,
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     <code class="type">
      integer
     </code>
     ) →
     <code class="returnvalue">
      anyelement
     </code>
    </p>
    <p>
     Returns
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     evaluated at the row that is the
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     'th row of the window frame (counting from 1); returns
     <code class="literal">
      NULL
     </code>
     if there is no such row.
    </p>
   </td>
  </tr>
 </tbody>
</table>









Todas as funções listadas em [Tabela 9.67](functions-window.md#FUNCTIONS-WINDOW-TABLE) dependem da ordem de classificação especificada pela cláusula `ORDER BY` da definição associada da janela. As linhas que não são distintas quando consideradas apenas as colunas `ORDER BY` são chamadas de *pares*. As quatro funções de classificação (incluindo `cume_dist`) são definidas de modo que elas forneçam a mesma resposta para todas as linhas de um grupo de pares.

Observe que `first_value`, `last_value` e `nth_value` consideram apenas as linhas dentro do "quadro de janela", que, por padrão, contém as linhas desde o início da partição até o último parceiro da linha atual. Isso provavelmente dará resultados inúteis para `last_value` e, às vezes, também para `nth_value`. Você pode redefinir o quadro adicionando uma especificação de quadro adequada (`RANGE`, `ROWS` ou `GROUPS`) à cláusula `OVER`. Consulte [Seção 4.2.8](sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS "4.2.8. Window Function Calls") para obter mais informações sobre especificações de quadro.

Quando uma função agregada é usada como uma função de janela, ela agrega as linhas dentro do quadro de janela da linha atual. Um agregado usado com `ORDER BY` e a definição padrão do quadro de janela produz um comportamento de tipo "soma em curso", que pode ou não ser o que se deseja. Para obter agregação sobre toda a partição, omita `ORDER BY` ou use `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`. Outras especificações de quadro podem ser usadas para obter outros efeitos.

### Nota

O padrão SQL define uma opção `RESPECT NULLS` ou `IGNORE NULLS` para `lead`, `lag`, `first_value`, `last_value` e `nth_value`. Isso não é implementado no PostgreSQL: o comportamento é sempre o mesmo que o padrão, ou seja, `RESPECT NULLS`. Da mesma forma, a opção `FROM FIRST` ou `FROM LAST` do padrão para `nth_value` não é implementada: apenas o comportamento padrão `FROM FIRST` é suportado. (Você pode obter o resultado de `FROM LAST` ao inverter a ordem do `ORDER BY`.)