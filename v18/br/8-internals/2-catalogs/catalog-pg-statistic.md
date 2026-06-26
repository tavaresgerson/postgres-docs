## 52.51. `pg_statistic` [#](#CATALOG-PG-STATISTIC)

O catálogo `pg_statistic` armazena dados estatísticos sobre o conteúdo do banco de dados. As entradas são criadas por `ANALYZE` e posteriormente utilizadas pelo planejador de consultas. Observe que todos os dados estatísticos são inerentemente aproximados, mesmo assumindo que estejam atualizados.

Normalmente, há uma entrada, com `stainherit` = `false`, para cada coluna da tabela que foi analisada. Se a tabela tiver filhos por herança ou partições, uma segunda entrada com `stainherit` = `true` também é criada. Esta linha representa as estatísticas da coluna sobre a árvore de herança, ou seja, estatísticas para os dados que você veria com `SELECT column FROM table*`, enquanto a linha `stainherit` = `false` representa os resultados de `SELECT column FROM ONLY table`.

`pg_statistic` também armazena dados estatísticos sobre os valores das expressões de índice. Essas são descritas como se fossem colunas de dados reais; em particular, `starelid` faz referência ao índice. No entanto, não é feita uma entrada para uma coluna de índice comum que não é uma expressão, pois isso seria redundante com a entrada da coluna da tabela subjacente. Atualmente, as entradas para expressões de índice sempre têm `stainherit` = `false`.

Como diferentes tipos de estatísticas podem ser apropriados para diferentes tipos de dados, o `pg_statistic` não é projetado para assumir muito sobre o tipo de estatísticas que armazena. Apenas estatísticas extremamente gerais (como a ausência de dados) recebem colunas dedicadas no `pg_statistic`. Tudo o resto é armazenado em "caixas", que são grupos de colunas associadas cujo conteúdo é identificado por um número de código em uma das colunas da caixa. Para mais informações, consulte `src/include/catalog/pg_statistic.h`.

`pg_statistic` não deve ser legível pelo público, uma vez que até mesmo informações estatísticas sobre o conteúdo de uma tabela podem ser consideradas sensíveis. (Exemplo: os valores mínimo e máximo de uma coluna de salário podem ser bastante interessantes.) `pg_stats`(view-pg-stats.md "53.29. pg_stats") é uma visão legível publicamente sobre `pg_statistic` que expõe apenas informações sobre as tabelas que são legíveis pelo usuário atual.

**Tabela 52.51. Colunas `pg_statistic`**



<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="catalog_table_entry">
    <p class="column_definition">
     Tipo de coluna
    </p>
    <p>
     Descrição
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      starelid
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code>
       pg_class
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     A tabela ou índice ao qual a coluna descrita pertence
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      staattnum
     </code>
     <code>
      int2
     </code>
     (referências
     <a class="link" href="catalog-pg-attribute.md" title="52.7. pg_attribute">
      <code>
       pg_attribute
      </code>
     </a>
     .
     <code>
      attnum
     </code>
     )
    </p>
    <p>
     O número da coluna descrita
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      stainherit
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Se for verdade, as estatísticas incluem valores de tabelas de crianças, não apenas os valores na relação especificada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      stanullfrac
     </code>
     <code>
      float4
     </code>
    </p>
    <p>
     A fração das entradas da coluna que são nulos
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      stawidth
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     A largura média armazenada, em bytes, das entradas não nulos
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      stadistinct
     </code>
     <code>
      float4
     </code>
    </p>
    <p>
     O número de valores de dados distintos e não nulos na coluna. Um valor maior que zero é o número real de valores distintos. Um valor menor que zero é o negativo de um multiplicador para o número de linhas na tabela; por exemplo, uma coluna na qual cerca de 80% dos valores são não nulos e cada valor não nulo aparece aproximadamente duas vezes em média pode ser representado por
     <code>
      stadistinct
     </code>
     = -0,4. Um valor zero significa que o número de valores distintos é desconhecido.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      stakind
      <em class="replaceable">
       <code>
        N
       </code>
      </em>
     </code>
     <code>
      int2
     </code>
    </p>
    <p>
     Um número de código que indica o tipo de estatísticas armazenadas no
     <em class="replaceable">
      <code>
       N
      </code>
     </em>
     th
     <span class="quote">
      “
      <span class="quote">
       jogada
      </span>
      ”
     </span>
     de o
     <code>
      pg_statistic
     </code>
     row.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      staop
      <em class="replaceable">
       <code>
        N
       </code>
      </em>
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-operator.md" title="52.34. pg_operator">
      <code>
       pg_operator
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Um operador costuma derivar as estatísticas armazenadas no
     <em class="replaceable">
      <code>
       N
      </code>
     </em>
     th
     <span class="quote">
      “
      <span class="quote">
       jogada
      </span>
      ”
     </span>
     Por exemplo, um carpete de histograma mostraria o
     <code>
      &lt;
     </code>
     operador que define a ordem de classificação dos dados. Zero se o tipo de estatística não requer um operador.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      stacoll
      <em class="replaceable">
       <code>
        N
       </code>
      </em>
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-collation.md" title="52.12. pg_collation">
      <code>
       pg_collation
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     A agregação usada para derivar as estatísticas armazenadas no
     <em class="replaceable">
      <code>
       N
      </code>
     </em>
     th
     <span class="quote">
      “
      <span class="quote">
       jogada
      </span>
      ”
     </span>
     Por exemplo, um intervalo de histograma para uma coluna colidível mostraria a collation que define a ordem de classificação dos dados. Zero para dados não colidíveis.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      stanumbers
      <em class="replaceable">
       <code>
        N
       </code>
      </em>
     </code>
     <code>
      float4[]
     </code>
    </p>
    <p>
     Estatísticas numéricas do tipo apropriado para o
     <em class="replaceable">
      <code>
       N
      </code>
     </em>
     th
     <span class="quote">
      “
      <span class="quote">
       jogada
      </span>
      ”
     </span>
     , ou nulo se o tipo de slot não envolver valores numéricos
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      stavalues
      <em class="replaceable">
       <code>
        N
       </code>
      </em>
     </code>
     <code>
      anyarray
     </code>
    </p>
    <p>
     Valores de dados de coluna do tipo apropriado para o
     <em class="replaceable">
      <code>
       N
      </code>
     </em>
     th
     <span class="quote">
      “
      <span class="quote">
       jogada
      </span>
      ”
     </span>
     , ou nulo se o tipo de slot não armazenar nenhum valor de dados. Os valores dos elementos de cada matriz são, na verdade, do tipo de dados da coluna específica, ou de um tipo relacionado, como o tipo de elemento de uma matriz, portanto, não há como definir o tipo dessas colunas de forma mais específica do que
     <code>
      anyarray
     </code>
     .
    </p>
   </td>
  </tr>
 </tbody>
</table>





