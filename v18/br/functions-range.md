## 9.20. Funções e operadores de faixa/multifaixa [#](#FUNCTIONS-RANGE)

Veja [Seção 8.17][(rangetypes.md "8.17. Range Types")] para uma visão geral dos tipos de alcance.

[Tabela 9.58][(functions-range.md#RANGE-OPERATORS-TABLE "Table 9.58. Range Operators")] mostra os operadores especializados disponíveis para tipos de intervalo. [Tabela 9.59][(functions-range.md#MULTIRANGE-OPERATORS-TABLE "Table 9.59. Multirange Operators")] mostra os operadores especializados disponíveis para tipos de multiintervalo. Além desses, os operadores de comparação comuns mostrados em [Tabela 9.1][(functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE "Table 9.1. Comparison Operators")] estão disponíveis para tipos de intervalo e multiintervalo. Os operadores de comparação ordenam primeiro pelos limites inferiores do intervalo e, apenas se esses forem iguais, comparam os limites superiores. Os operadores de multiintervalo comparam cada intervalo até que um deles seja desigual. Isso geralmente não resulta em uma ordem geral útil, mas os operadores são fornecidos para permitir que índices únicos sejam construídos em intervalos.

**Tabela 9.58. Operadores de intervalo**



<table border="1" class="table" summary="Range Operators">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="func_table_entry">
<p class="func_signature">Operador</p>
<p>Descrição</p>
<p>Exemplo(s)</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      @&gt;
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O primeiro intervalo contém o segundo?</p>
<p>
<code class="literal">
      int4range(2,4) @&gt; int4range(2,3)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      @&gt;
     </code>
<code class="type">
      anyelement
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A faixa contém o elemento?</p>
<p>
<code class="literal">
      '[2011-01-01,2011-03-01)'::tsrange @&gt; '2011-01-10'::timestamp
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      &lt;@
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A primeira faixa está contida pela segunda?</p>
<p>
<code class="literal">
      int4range(2,4) &lt;@ int4range(1,7)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyelement
     </code>
<code class="literal">
      &lt;@
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O elemento está contido na faixa?</p>
<p>
<code class="literal">
      42 &lt;@ int4range(1,7)
     </code>→<code class="returnvalue">
      f
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      &amp;&amp;
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>Os intervalos se sobrepõem, ou seja, têm algum elemento em comum?</p>
<p>
<code class="literal">
      int8range(3,7) &amp;&amp; int8range(4,12)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      &lt;&lt;
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A primeira faixa está estritamente à esquerda da segunda?</p>
<p>
<code class="literal">
      int8range(1,10) &lt;&lt; int8range(100,110)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      &gt;&gt;
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A primeira faixa está estritamente à direita da segunda?</p>
<p>
<code class="literal">
      int8range(50,60) &gt;&gt; int8range(20,30)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      &amp;&lt;
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A primeira faixa não se estende à direita da segunda?</p>
<p>
<code class="literal">
      int8range(1,20) &amp;&lt; int8range(18,20)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      &amp;&gt;
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A primeira faixa não se estende à esquerda da segunda?</p>
<p>
<code class="literal">
      int8range(7,20) &amp;&gt; int8range(5,10)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      -|-
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>As faixas são adjacentes?</p>
<p>
<code class="literal">
      numrange(1.1,2.2) -|- numrange(2.2,3.3)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      +
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      anyrange
     </code>
</p>
<p>Calcula a união das faixas. As faixas devem se sobrepor ou estar adjacentes, de modo que a união seja uma única faixa (mas veja<code class="function">
      range_merge()
     </code>
     ).
    </p>
<p>
<code class="literal">
      numrange(5,15) + numrange(10,20)
     </code>→<code class="returnvalue">
      [5,20)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      *
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      anyrange
     </code>
</p>
<p>Calcula a interseção das faixas.</p>
<p>
<code class="literal">
      int8range(5,15) * int8range(10,20)
     </code>→<code class="returnvalue">
      [10,15)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      -
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      anyrange
     </code>
</p>
<p>Calcula a diferença das faixas. A segunda faixa não deve estar contida na primeira de tal forma que a diferença não seja uma única faixa.</p>
<p>
<code class="literal">
      int8range(5,15) - int8range(10,20)
     </code>→<code class="returnvalue">
      [5,10)
     </code>
</p>
</td>
</tr>
</tbody>
</table>




  

**Tabela 9.59. Operadores de múltiplos intervalos**



<table border="1" class="table" summary="Multirange Operators">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="func_table_entry">
<p class="func_signature">Operador</p>
<p>Descrição</p>
<p>Exemplo(s)</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      @&gt;
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O primeiro multirange contém o segundo?</p>
<p>
<code class="literal">
      '{[2,4)}'::int4multirange @&gt; '{[2,3)}'::int4multirange
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      @&gt;
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A multirange contém a faixa?</p>
<p>
<code class="literal">
      '{[2,4)}'::int4multirange @&gt; int4range(2,3)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      @&gt;
     </code>
<code class="type">
      anyelement
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O multirange contém o elemento?</p>
<p>
<code class="literal">
      '{[2011-01-01,2011-03-01)}'::tsmultirange @&gt; '2011-01-10'::timestamp
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      @&gt;
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A faixa contém a faixa múltipla?</p>
<p>
<code class="literal">
      '[2,4)'::int4range @&gt; '{[2,3)}'::int4multirange
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      &lt;@
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A primeira faixa está contida pela segunda?</p>
<p>
<code class="literal">
      '{[2,4)}'::int4multirange &lt;@ '{[1,7)}'::int4multirange
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      &lt;@
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O multirange está contido na faixa?</p>
<p>
<code class="literal">
      '{[2,4)}'::int4multirange &lt;@ int4range(1,7)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      &lt;@
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A faixa está contida na multifaixa?</p>
<p>
<code class="literal">
      int4range(2,4) &lt;@ '{[1,7)}'::int4multirange
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyelement
     </code>
<code class="literal">
      &lt;@
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O elemento está contido na multirange?</p>
<p>
<code class="literal">
      4 &lt;@ '{[1,7)}'::int4multirange
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      &amp;&amp;
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>As multiranges se sobrepõem, ou seja, têm algum elemento em comum?</p>
<p>
<code class="literal">
      '{[3,7)}'::int8multirange &amp;&amp; '{[4,12)}'::int8multirange
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      &amp;&amp;
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A multirange sobrepõe-se à faixa?</p>
<p>
<code class="literal">
      '{[3,7)}'::int8multirange &amp;&amp; int8range(4,12)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      &amp;&amp;
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A faixa se sobrepõe à multifaixa?</p>
<p>
<code class="literal">
      int8range(3,7) &amp;&amp; '{[4,12)}'::int8multirange
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      &lt;&lt;
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A primeira faixa está estritamente à esquerda da segunda?</p>
<p>
<code class="literal">
      '{[1,10)}'::int8multirange &lt;&lt; '{[100,110)}'::int8multirange
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      &lt;&lt;
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A multirange está estritamente à esquerda da faixa?</p>
<p>
<code class="literal">
      '{[1,10)}'::int8multirange &lt;&lt; int8range(100,110)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      &lt;&lt;
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A faixa está estritamente à esquerda da multifaixa?</p>
<p>
<code class="literal">
      int8range(1,10) &lt;&lt; '{[100,110)}'::int8multirange
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      &gt;&gt;
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>É o primeiro direito multirange estritamente o segundo?</p>
<p>
<code class="literal">
      '{[50,60)}'::int8multirange &gt;&gt; '{[20,30)}'::int8multirange
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      &gt;&gt;
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A multirange é estritamente o mesmo que range?</p>
<p>
<code class="literal">
      '{[50,60)}'::int8multirange &gt;&gt; int8range(20,30)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      &gt;&gt;
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A faixa é estritamente à direita da faixa multibanda?</p>
<p>
<code class="literal">
      int8range(50,60) &gt;&gt; '{[20,30)}'::int8multirange
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      &amp;&lt;
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A primeira faixa não se estende à direita da segunda?</p>
<p>
<code class="literal">
      '{[1,20)}'::int8multirange &amp;&lt; '{[18,20)}'::int8multirange
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      &amp;&lt;
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A multirange não se estende para a direita da faixa?</p>
<p>
<code class="literal">
      '{[1,20)}'::int8multirange &amp;&lt; int8range(18,20)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      &amp;&lt;
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A faixa não se estende para a direita da multifaixa?</p>
<p>
<code class="literal">
      int8range(1,20) &amp;&lt; '{[18,20)}'::int8multirange
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      &amp;&gt;
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O primeiro multirange não se estende à esquerda do segundo?</p>
<p>
<code class="literal">
      '{[7,20)}'::int8multirange &amp;&gt; '{[5,10)}'::int8multirange
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      &amp;&gt;
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A multirange não se estende à esquerda da faixa?</p>
<p>
<code class="literal">
      '{[7,20)}'::int8multirange &amp;&gt; int8range(5,10)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      &amp;&gt;
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A faixa não se estende à esquerda da multifaixa?</p>
<p>
<code class="literal">
      int8range(7,20) &amp;&gt; '{[5,10)}'::int8multirange
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      -|-
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>Os multiranges são adjacentes?</p>
<p>
<code class="literal">
      '{[1.1,2.2)}'::nummultirange -|- '{[2.2,3.3)}'::nummultirange
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      -|-
     </code>
<code class="type">
      anyrange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A multirange é adjacente à faixa?</p>
<p>
<code class="literal">
      '{[1.1,2.2)}'::nummultirange -|- numrange(2.2,3.3)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyrange
     </code>
<code class="literal">
      -|-
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A faixa é adjacente à multifaixa?</p>
<p>
<code class="literal">
      numrange(1.1,2.2) -|- '{[2.2,3.3)}'::nummultirange
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      +
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      anymultirange
     </code>
</p>
<p>Calcula a união dos multiintervalos. Os multiintervalos não precisam se sobrepor ou estar adjacentes.</p>
<p>
<code class="literal">
      '{[5,10)}'::nummultirange + '{[15,20)}'::nummultirange
     </code>→<code class="returnvalue">
      {[5,10), [15,20)}
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      *
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      anymultirange
     </code>
</p>
<p>Calcula a interseção dos multiintervalos.</p>
<p>
<code class="literal">
      '{[5,15)}'::int8multirange * '{[10,20)}'::int8multirange
     </code>→<code class="returnvalue">
      {[10,15)}
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anymultirange
     </code>
<code class="literal">
      -
     </code>
<code class="type">
      anymultirange
     </code>→<code class="returnvalue">
      anymultirange
     </code>
</p>
<p>Calcula a diferença dos multiintervalos.</p>
<p>
<code class="literal">
      '{[5,20)}'::int8multirange - '{[10,15)}'::int8multirange
     </code>→<code class="returnvalue">
      {[5,10), [15,20)}
     </code>
</p>
</td>
</tr>
</tbody>
</table>




  

Os operadores de esquerda/direita/adjacente sempre retornam falso quando há uma faixa vazia ou uma faixa múltipla envolvida; ou seja, uma faixa vazia não é considerada antes ou depois de qualquer outra faixa.

Em outros lugares, intervalos vazios e multiintervalos são tratados como a identidade aditiva: qualquer coisa que é unida a um valor vazio é ela mesma. Qualquer coisa menos um valor vazio é ela mesma. Um multiintervalo vazio tem exatamente os mesmos pontos que um intervalo vazio. Cada intervalo contém o intervalo vazio. Cada multiintervalo contém tantas faixas vazias quanto você quiser.

Os operadores de união e diferença de intervalo falharão se o intervalo resultante precisar conter dois sub-intervalos disjuntos, pois tal intervalo não pode ser representado. Existem operadores separados para união e diferença que aceitam parâmetros de multiintervalo e retornam um multiintervalo, e eles não falham mesmo se seus argumentos forem disjuntos. Portanto, se você precisar de uma operação de união ou diferença para intervalos que podem ser disjuntos, você pode evitar erros ao primeiro converter seus intervalos em multiintervalos.

[Tabela 9.60][(functions-range.md#RANGE-FUNCTIONS-TABLE "Table 9.60. Range Functions")] mostra as funções disponíveis para uso com tipos de intervalo. [Tabela 9.61][(functions-range.md#MULTIRANGE-FUNCTIONS-TABLE "Table 9.61. Multirange Functions")] mostra as funções disponíveis para uso com tipos de multiintervalo.

**Tabela 9.60. Funções de intervalo**



<table border="1" class="table" summary="Range Functions">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="func_table_entry">
<p class="func_signature">Função</p>
<p>Descrição</p>
<p>Exemplo(s)</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      lower
     </code>(<code class="type">
      anyrange
     </code>)<code class="returnvalue">
      anyelement
     </code>
</p>
<p>Extrai a menor faixa do intervalo (<code class="literal">
      NULL
     </code>se a faixa estiver vazia ou não tiver limite inferior).</p>
<p>
<code class="literal">
      lower(numrange(1.1,2.2))
     </code>→<code class="returnvalue">
      1.1
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      upper
     </code>(<code class="type">
      anyrange
     </code>)<code class="returnvalue">
      anyelement
     </code>
</p>
<p>Extrai o limite superior da faixa (<code class="literal">
      NULL
     </code>se a faixa estiver vazia ou não tiver limite superior).</p>
<p>
<code class="literal">
      upper(numrange(1.1,2.2))
     </code>→<code class="returnvalue">
      2.2
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      isempty
     </code>(<code class="type">
      anyrange
     </code>)<code class="returnvalue">
      boolean
     </code>
</p>
<p>A faixa está vazia?</p>
<p>
<code class="literal">
      isempty(numrange(1.1,2.2))
     </code>→<code class="returnvalue">
      f
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      lower_inc
     </code>(<code class="type">
      anyrange
     </code>)<code class="returnvalue">
      boolean
     </code>
</p>
<p>A faixa de valores inferior é inclusiva?</p>
<p>
<code class="literal">
      lower_inc(numrange(1.1,2.2))
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      upper_inc
     </code>(<code class="type">
      anyrange
     </code>)<code class="returnvalue">
      boolean
     </code>
</p>
<p>A faixa tem limite superior inclusivo?</p>
<p>
<code class="literal">
      upper_inc(numrange(1.1,2.2))
     </code>→<code class="returnvalue">
      f
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      lower_inf
     </code>(<code class="type">
      anyrange
     </code>)<code class="returnvalue">
      boolean
     </code>
</p>
<p>A faixa não tem limite inferior? (Um limite inferior de<code class="literal">
      -Infinity
     </code>retorna falso.)</p>
<p>
<code class="literal">
      lower_inf('(,)'::daterange)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      upper_inf
     </code>(<code class="type">
      anyrange
     </code>)<code class="returnvalue">
      boolean
     </code>
</p>
<p>A faixa não tem limite superior? (Um limite superior de<code class="literal">
      Infinity
     </code>retorna falso.)</p>
<p>
<code class="literal">
      upper_inf('(,)'::daterange)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      range_merge
     </code>(<code class="type">
      anyrange
     </code>,<code class="type">
      anyrange
     </code>)<code class="returnvalue">
      anyrange
     </code>
</p>
<p>Calcula a menor faixa que inclui ambos os intervalos fornecidos.</p>
<p>
<code class="literal">
      range_merge('[1,2)'::int4range, '[3,4)'::int4range)
     </code>→<code class="returnvalue">
      [1,4)
     </code>
</p>
</td>
</tr>
</tbody>
</table>




  

**Tabela 9.61. Funções multirangedoble**



<table border="1" class="table" summary="Multirange Functions">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="func_table_entry">
<p class="func_signature">Função</p>
<p>Descrição</p>
<p>Exemplo(s)</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      lower
     </code>(<code class="type">
      anymultirange
     </code>)<code class="returnvalue">
      anyelement
     </code>
</p>
<p>Extrai a menor faixa do multirange (<code class="literal">
      NULL
     </code>se a multirange estiver vazia ou não tiver limite inferior).</p>
<p>
<code class="literal">
      lower('{[1.1,2.2)}'::nummultirange)
     </code>→<code class="returnvalue">
      1.1
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      upper
     </code>(<code class="type">
      anymultirange
     </code>)<code class="returnvalue">
      anyelement
     </code>
</p>
<p>Extrai o limite superior do multirange (<code class="literal">
      NULL
     </code>se a multirange estiver vazia ou não tiver limite superior).</p>
<p>
<code class="literal">
      upper('{[1.1,2.2)}'::nummultirange)
     </code>→<code class="returnvalue">
      2.2
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      isempty
     </code>(<code class="type">
      anymultirange
     </code>)<code class="returnvalue">
      boolean
     </code>
</p>
<p>A multirange está vazia?</p>
<p>
<code class="literal">
      isempty('{[1.1,2.2)}'::nummultirange)
     </code>→<code class="returnvalue">
      f
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      lower_inc
     </code>(<code class="type">
      anymultirange
     </code>)<code class="returnvalue">
      boolean
     </code>
</p>
<p>A faixa inferior do multirange é inclusiva?</p>
<p>
<code class="literal">
      lower_inc('{[1.1,2.2)}'::nummultirange)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      upper_inc
     </code>(<code class="type">
      anymultirange
     </code>)<code class="returnvalue">
      boolean
     </code>
</p>
<p>A fronteira superior do multirange é inclusiva?</p>
<p>
<code class="literal">
      upper_inc('{[1.1,2.2)}'::nummultirange)
     </code>→<code class="returnvalue">
      f
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      lower_inf
     </code>(<code class="type">
      anymultirange
     </code>)<code class="returnvalue">
      boolean
     </code>
</p>
<p>O multirange não tem limite inferior? (Um limite inferior de<code class="literal">
      -Infinity
     </code>retorna falso.)</p>
<p>
<code class="literal">
      lower_inf('{(,)}'::datemultirange)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      upper_inf
     </code>(<code class="type">
      anymultirange
     </code>)<code class="returnvalue">
      boolean
     </code>
</p>
<p>O multirange não tem limite superior? (Um limite superior de<code class="literal">
      Infinity
     </code>retorna falso.)</p>
<p>
<code class="literal">
      upper_inf('{(,)}'::datemultirange)
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      range_merge
     </code>(<code class="type">
      anymultirange
     </code>)<code class="returnvalue">
      anyrange
     </code>
</p>
<p>Calcula a menor faixa que inclui toda a faixa múltipla.</p>
<p>
<code class="literal">
      range_merge('{[1,2), [3,4)}'::int4multirange)
     </code>→<code class="returnvalue">
      [1,4)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      multirange
     </code>(<code class="type">
      anyrange
     </code>)<code class="returnvalue">
      anymultirange
     </code>
</p>
<p>Retorna uma faixa múltipla contendo apenas a faixa especificada.</p>
<p>
<code class="literal">
      multirange('[1,2)'::int4range)
     </code>→<code class="returnvalue">
      {[1,2)}
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      unnest
     </code>(<code class="type">
      anymultirange
     </code>)<code class="returnvalue">
      setof anyrange
     </code>
</p>
<p>Expande uma faixa multirangedo em um conjunto de faixas em ordem crescente.</p>
<p>
<code class="literal">
      unnest('{[1,2), [3,4)}'::int4multirange)
     </code>→<code class="returnvalue">
</code>
</p>
<pre class="programlisting">
 [1,2) [3,4)
</pre>
<p>
</p>
</td>
</tr>
</tbody>
</table>




  

As funções `lower_inc`, `upper_inc`, `lower_inf` e `upper_inf` retornam false para uma faixa ou faixa múltipla vazia.