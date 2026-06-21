## 9.11. Funções e Operadores Geométricos [#](#FUNCTIONS-GEOMETRY)

Os tipos geométricos `point`, `box`, `lseg`, `line`, `path`, `polygon` e `circle` possuem um grande conjunto de funções e operadores de suporte nativo, mostrados em [Tabela 9.36](functions-geometry.md#FUNCTIONS-GEOMETRY-OP-TABLE "Table 9.36. Geometric Operators"), [Tabela 9.37](functions-geometry.md#FUNCTIONS-GEOMETRY-FUNC-TABLE "Table 9.37. Geometric Functions") e [Tabela 9.38](functions-geometry.md#FUNCTIONS-GEOMETRY-CONV-TABLE "Table 9.38. Geometric Type Conversion Functions").

**Tabela 9.36. Operadores geométricos**



<table border="1" class="table" summary="Geometric Operators">
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
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      +
     </code>
<code class="type">
      point
     </code>→<code class="returnvalue">
<em class="replaceable">
<code>
        geometric_type
       </code>
</em>
</code>
</p>
<p>Adicione as coordenadas do segundo<code class="type">
      point
     </code>para aqueles de cada ponto do primeiro argumento, realizando assim a tradução. Disponível para<code class="type">
      point
     </code>,<code class="type">
      box
     </code>,<code class="type">
      path
     </code>,<code class="type">
      circle
     </code>
     .
    </p>
<p>
<code class="literal">
      box '(1,1),(0,0)' + point '(2,0)'
     </code>→<code class="returnvalue">
      (3,1),(2,0)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      path
     </code>
<code class="literal">
      +
     </code>
<code class="type">
      path
     </code>→<code class="returnvalue">
      path
     </code>
</p>
<p>Concatenia dois caminhos abertos (retorna NULL se qualquer um dos caminhos estiver fechado).</p>
<p>
<code class="literal">
      path '[(0,0),(1,1)]' + path '[(2,2),(3,3),(4,4)]'
     </code>→<code class="returnvalue">
      [(0,0),(1,1),(2,2),(3,3),(4,4)]
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      -
     </code>
<code class="type">
      point
     </code>→<code class="returnvalue">
<em class="replaceable">
<code>
        geometric_type
       </code>
</em>
</code>
</p>
<p>Subtrai as coordenadas do segundo<code class="type">
      point
     </code>a partir dos de cada ponto do primeiro argumento, realizando assim a tradução. Disponível para<code class="type">
      point
     </code>,<code class="type">
      box
     </code>,<code class="type">
      path
     </code>,<code class="type">
      circle
     </code>
     .
    </p>
<p>
<code class="literal">
      box '(1,1),(0,0)' - point '(2,0)'
     </code>→<code class="returnvalue">
      (-1,1),(-2,0)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      *
     </code>
<code class="type">
      point
     </code>→<code class="returnvalue">
<em class="replaceable">
<code>
        geometric_type
       </code>
</em>
</code>
</p>
<p>Multiplica cada ponto do primeiro argumento pelo segundo<code class="type">
      point
     </code>(tratando um ponto como um número complexo representado por partes reais e imaginárias, e realizando a multiplicação padrão de números complexos). Se se interpretar o segundo
<code class="type">
      point
     </code>Como um vetor, isso é equivalente a escalar o tamanho do objeto e a distância da origem pelo comprimento do vetor, e rotá-lo no sentido anti-horário em torno da origem pelo ângulo do vetor a partir<em class="replaceable">
<code>
       x
      </code>
</em>eixo. Disponível para<code class="type">
      point
     </code>,<code class="type">
      box
     </code>,<a class="footnote" href="#ftn.FUNCTIONS-GEOMETRY-ROTATION-FN">
<sup class="footnote" id="FUNCTIONS-GEOMETRY-ROTATION-FN">[a]</sup>
</a>
<code class="type">
      path
     </code>,<code class="type">
      circle
     </code>
     .
    </p>
<p>
<code class="literal">
      path '((0,0),(1,0),(1,1))' * point '(3.0,0)'
     </code>→<code class="returnvalue">
      ((0,0),(3,0),(3,3))
     </code>
</p>
<p>
<code class="literal">
      path '((0,0),(1,0),(1,1))' * point(cosd(45), sind(45))
     </code>→<code class="returnvalue">
      ((0,0),​(0.7071067811865475,0.7071067811865475),​(0,1.414213562373095))
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      /
     </code>
<code class="type">
      point
     </code>→<code class="returnvalue">
<em class="replaceable">
<code>
        geometric_type
       </code>
</em>
</code>
</p>
<p>Divide cada ponto do primeiro argumento pelo segundo<code class="type">
      point
     </code>(tratando um ponto como um número complexo representado por partes reais e imaginárias, e realizando a divisão padrão de números complexos). Se se interpretar o segundo
<code class="type">
      point
     </code>Como um vetor, isso é equivalente a escalar o tamanho do objeto e a distância da origem para baixo pelo comprimento do vetor, e rotá-lo no sentido horário em torno da origem pelo ângulo do vetor a partir<em class="replaceable">
<code>
       x
      </code>
</em>eixo. Disponível para<code class="type">
      point
     </code>,<code class="type">
      box
     </code>,<a class="footnoteref" href="functions-geometry.md#ftn.FUNCTIONS-GEOMETRY-ROTATION-FN">
<sup class="footnoteref">[a]</sup>
</a>
<code class="type">
      path
     </code>,<code class="type">
      circle
     </code>
     .
    </p>
<p>
<code class="literal">
      path '((0,0),(1,0),(1,1))' / point '(2.0,0)'
     </code>→<code class="returnvalue">
      ((0,0),(0.5,0),(0.5,0.5))
     </code>
</p>
<p>
<code class="literal">
      path '((0,0),(1,0),(1,1))' / point(cosd(45), sind(45))
     </code>→<code class="returnvalue">
      ((0,0),​(0.7071067811865476,-0.7071067811865476),​(1.4142135623730951,0))
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="literal">
      @-@
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      double precision
     </code>
</p>
<p>Calcula o comprimento total. Disponível para<code class="type">
      lseg
     </code>,<code class="type">
      path
     </code>
     .
    </p>
<p>
<code class="literal">
      @-@ path '[(0,0),(1,0),(1,1)]'
     </code>→<code class="returnvalue">
      2
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="literal">
      @@
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      point
     </code>
</p>
<p>Calcula o ponto central. Disponível para<code class="type">
      box
     </code>,<code class="type">
      lseg
     </code>,<code class="type">
      polygon
     </code>,<code class="type">
      circle
     </code>
     .
    </p>
<p>
<code class="literal">
      @@ box '(2,2),(0,0)'
     </code>→<code class="returnvalue">
      (1,1)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="literal">
      #
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      integer
     </code>
</p>
<p>Retorna o número de pontos. Disponível para<code class="type">
      path
     </code>,<code class="type">
      polygon
     </code>
     .
    </p>
<p>
<code class="literal">
      # path '((1,0),(0,1),(-1,0))'
     </code>→<code class="returnvalue">
      3
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      #
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      point
     </code>
</p>
<p>Calcula o ponto de interseção, ou NULL, se não houver nenhum. Disponível para<code class="type">
      lseg
     </code>,<code class="type">
      line
     </code>
     .
    </p>
<p>
<code class="literal">
      lseg '[(0,0),(1,1)]' # lseg '[(1,0),(0,1)]'
     </code>→<code class="returnvalue">
      (0.5,0.5)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      box
     </code>
<code class="literal">
      #
     </code>
<code class="type">
      box
     </code>→<code class="returnvalue">
      box
     </code>
</p>
<p>Calcula a interseção de duas caixas, ou NULL, se não houver nenhuma.</p>
<p>
<code class="literal">
      box '(2,2),(-1,-1)' # box '(1,1),(-2,-2)'
     </code>→<code class="returnvalue">
      (1,1),(-1,-1)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      ##
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      point
     </code>
</p>
<p>Calcula o ponto mais próximo do primeiro objeto no segundo objeto. Disponível para esses pares de tipos: (<code class="type">
      point
     </code>,<code class="type">
      box
     </code>), (<code class="type">
      point
     </code>,<code class="type">
      lseg
     </code>), (<code class="type">
      point
     </code>,<code class="type">
      line
     </code>), (<code class="type">
      lseg
     </code>,<code class="type">
      box
     </code>), (<code class="type">
      lseg
     </code>,<code class="type">
      lseg
     </code>), (<code class="type">
      line
     </code>,<code class="type">
      lseg
     </code>
     ).
    </p>
<p>
<code class="literal">
      point '(0,0)' ## lseg '[(2,0),(0,2)]'
     </code>→<code class="returnvalue">
      (1,1)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      &lt;-&gt;
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      double precision
     </code>
</p>
<p>Calcula a distância entre os objetos. Disponível para todos os sete tipos geométricos, para todas as combinações de<code class="type">
      point
     </code>com outro tipo geométrico, e para esses pares adicionais de tipos: (<code class="type">
      box
     </code>,<code class="type">
      lseg
     </code>), (<code class="type">
      lseg
     </code>,<code class="type">
      line
     </code>), (<code class="type">
      polygon
     </code>,<code class="type">
      circle
     </code>) (e os casos de commutator).</p>
<p>
<code class="literal">
      circle '&lt;(0,0),1&gt;' &lt;-&gt; circle '&lt;(5,0),1&gt;'
     </code>→<code class="returnvalue">
      3
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      @&gt;
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O primeiro objeto contém o segundo? Disponível para esses pares de tipos: (<code class="literal">
      box
     </code>,<code class="literal">
      point
     </code>), (<code class="literal">
      box
     </code>,<code class="literal">
      box
     </code>), (<code class="literal">
      path
     </code>,<code class="literal">
      point
     </code>), (<code class="literal">
      polygon
     </code>,<code class="literal">
      point
     </code>), (<code class="literal">
      polygon
     </code>,<code class="literal">
      polygon
     </code>), (<code class="literal">
      circle
     </code>,<code class="literal">
      point
     </code>), (<code class="literal">
      circle
     </code>,<code class="literal">
      circle
     </code>
     ).
    </p>
<p>
<code class="literal">
      circle '&lt;(0,0),2&gt;' @&gt; point '(1,1)'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      &lt;@
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O primeiro objeto está contido em ou sobre o segundo? Disponível para esses pares de tipos: (<code class="literal">
      point
     </code>,<code class="literal">
      box
     </code>), (<code class="literal">
      point
     </code>,<code class="literal">
      lseg
     </code>), (<code class="literal">
      point
     </code>,<code class="literal">
      line
     </code>), (<code class="literal">
      point
     </code>,<code class="literal">
      path
     </code>), (<code class="literal">
      point
     </code>,<code class="literal">
      polygon
     </code>), (<code class="literal">
      point
     </code>,<code class="literal">
      circle
     </code>), (<code class="literal">
      box
     </code>,<code class="literal">
      box
     </code>), (<code class="literal">
      lseg
     </code>,<code class="literal">
      box
     </code>), (<code class="literal">
      lseg
     </code>,<code class="literal">
      line
     </code>), (<code class="literal">
      polygon
     </code>,<code class="literal">
      polygon
     </code>), (<code class="literal">
      circle
     </code>,<code class="literal">
      circle
     </code>
     ).
    </p>
<p>
<code class="literal">
      point '(1,1)' &lt;@ circle '&lt;(0,0),2&gt;'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      &amp;&amp;
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>Estes objetos se sobrepõem? (Um ponto em comum torna isso verdadeiro.) Disponível para<code class="type">
      box
     </code>,<code class="type">
      polygon
     </code>,<code class="type">
      circle
     </code>
     .
    </p>
<p>
<code class="literal">
      box '(1,1),(0,0)' &amp;&amp; box '(2,2),(0,0)'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      &lt;&lt;
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O primeiro objeto está estritamente à esquerda do segundo? Disponível para<code class="type">
      point
     </code>,<code class="type">
      box
     </code>,<code class="type">
      polygon
     </code>,<code class="type">
      circle
     </code>
     .
    </p>
<p>
<code class="literal">
      circle '&lt;(0,0),1&gt;' &lt;&lt; circle '&lt;(5,0),1&gt;'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      &gt;&gt;
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O primeiro objeto é estritamente correto em relação ao segundo? Disponível para<code class="type">
      point
     </code>,<code class="type">
      box
     </code>,<code class="type">
      polygon
     </code>,<code class="type">
      circle
     </code>
     .
    </p>
<p>
<code class="literal">
      circle '&lt;(5,0),1&gt;' &gt;&gt; circle '&lt;(0,0),1&gt;'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      &amp;&lt;
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O primeiro objeto não se estende ao direito do segundo? Disponível para<code class="type">
      box
     </code>,<code class="type">
      polygon
     </code>,<code class="type">
      circle
     </code>
     .
    </p>
<p>
<code class="literal">
      box '(1,1),(0,0)' &amp;&lt; box '(2,2),(0,0)'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      &amp;&gt;
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O primeiro objeto não se estende à esquerda do segundo? Disponível para<code class="type">
      box
     </code>,<code class="type">
      polygon
     </code>,<code class="type">
      circle
     </code>
     .
    </p>
<p>
<code class="literal">
      box '(3,3),(0,0)' &amp;&gt; box '(2,2),(0,0)'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      &lt;&lt;|
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O primeiro objeto está estritamente abaixo do segundo? Disponível para<code class="type">
      point
     </code>,<code class="type">
      box
     </code>,<code class="type">
      polygon
     </code>,<code class="type">
      circle
     </code>
     .
    </p>
<p>
<code class="literal">
      box '(3,3),(0,0)' &lt;&lt;| box '(5,5),(3,4)'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      |&gt;&gt;
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O primeiro objeto está estritamente acima do segundo? Disponível para<code class="type">
      point
     </code>,<code class="type">
      box
     </code>,<code class="type">
      polygon
     </code>,<code class="type">
      circle
     </code>
     .
    </p>
<p>
<code class="literal">
      box '(5,5),(3,4)' |&gt;&gt; box '(3,3),(0,0)'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      &amp;&lt;|
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O primeiro objeto não se estende acima do segundo? Disponível para<code class="type">
      box
     </code>,<code class="type">
      polygon
     </code>,<code class="type">
      circle
     </code>
     .
    </p>
<p>
<code class="literal">
      box '(1,1),(0,0)' &amp;&lt;| box '(2,2),(0,0)'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      |&amp;&gt;
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O primeiro objeto não se estende abaixo do segundo? Disponível para<code class="type">
      box
     </code>,<code class="type">
      polygon
     </code>,<code class="type">
      circle
     </code>
     .
    </p>
<p>
<code class="literal">
      box '(3,3),(0,0)' |&amp;&gt; box '(2,2),(0,0)'
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
      box
     </code>
<code class="literal">
      &lt;^
     </code>
<code class="type">
      box
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O primeiro objeto está abaixo do segundo (permite que as bordas se toquem)?</p>
<p>
<code class="literal">
      box '((1,1),(0,0))' &lt;^ box '((2,2),(1,1))'
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
      box
     </code>
<code class="literal">
      &gt;^
     </code>
<code class="type">
      box
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O primeiro objeto está acima do segundo (permite que as bordas se toquem)?</p>
<p>
<code class="literal">
      box '((2,2),(1,1))' &gt;^ box '((1,1),(0,0))'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      ?#
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>Estes objetos se cruzam? Disponível para estes pares de tipos: (<code class="type">
      box
     </code>,<code class="type">
      box
     </code>), (<code class="type">
      lseg
     </code>,<code class="type">
      box
     </code>), (<code class="type">
      lseg
     </code>,<code class="type">
      lseg
     </code>), (<code class="type">
      lseg
     </code>,<code class="type">
      line
     </code>), (<code class="type">
      line
     </code>,<code class="type">
      box
     </code>), (<code class="type">
      line
     </code>,<code class="type">
      line
     </code>), (<code class="type">
      path
     </code>,<code class="type">
      path
     </code>
     ).
    </p>
<p>
<code class="literal">
      lseg '[(-1,0),(1,0)]' ?# box '(2,2),(-2,-2)'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="literal">
      ?-
     </code>
<code class="type">
      line
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p class="func_signature">
<code class="literal">
      ?-
     </code>
<code class="type">
      lseg
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A linha é horizontal?</p>
<p>
<code class="literal">
      ?- lseg '[(-1,0),(1,0)]'
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
      point
     </code>
<code class="literal">
      ?-
     </code>
<code class="type">
      point
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>Os pontos estão alinhados horizontalmente (ou seja, têm a mesma coordenada y)?</p>
<p>
<code class="literal">
      point '(1,0)' ?- point '(0,0)'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="literal">
      ?|
     </code>
<code class="type">
      line
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p class="func_signature">
<code class="literal">
      ?|
     </code>
<code class="type">
      lseg
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A linha é vertical?</p>
<p>
<code class="literal">
      ?| lseg '[(-1,0),(1,0)]'
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
      point
     </code>
<code class="literal">
      ?|
     </code>
<code class="type">
      point
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>Os pontos estão alinhados verticalmente (ou seja, têm a mesma coordenada x)?</p>
<p>
<code class="literal">
      point '(0,1)' ?| point '(0,0)'
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
      line
     </code>
<code class="literal">
      ?-|
     </code>
<code class="type">
      line
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p class="func_signature">
<code class="type">
      lseg
     </code>
<code class="literal">
      ?-|
     </code>
<code class="type">
      lseg
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>As linhas são perpendiculares?</p>
<p>
<code class="literal">
      lseg '[(0,0),(0,1)]' ?-| lseg '[(0,0),(1,0)]'
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
      line
     </code>
<code class="literal">
      ?||
     </code>
<code class="type">
      line
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p class="func_signature">
<code class="type">
      lseg
     </code>
<code class="literal">
      ?||
     </code>
<code class="type">
      lseg
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>As linhas são paralelas?</p>
<p>
<code class="literal">
      lseg '[(-1,0),(1,0)]' ?|| lseg '[(-1,2),(1,2)]'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>
<code class="literal">
      ~=
     </code>
<em class="replaceable">
<code>
       geometric_type
      </code>
</em>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>Estes objetos são os mesmos? Disponível para<code class="type">
      point
     </code>,<code class="type">
      box
     </code>,<code class="type">
      polygon
     </code>,<code class="type">
      circle
     </code>
     .
    </p>
<p>
<code class="literal">
      polygon '((0,0),(1,1))' ~= polygon '((1,1),(0,0))'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
</tbody>
<tbody class="footnotes">
<tr>
<td colspan="1">
<div class="footnote" id="ftn.FUNCTIONS-GEOMETRY-ROTATION-FN">
<p>
<a class="para" href="#FUNCTIONS-GEOMETRY-ROTATION-FN">
<sup class="para">[a]</sup>
</a>
<span class="quote">“<span class="quote">Girando</span>”</span>Uma caixa com esses operadores apenas move seus pontos de canto: a caixa ainda é considerada ter lados paralelos aos eixos. Portanto, o tamanho da caixa não é preservado, como uma verdadeira rotação faria.</p>
</div>
</td>
</tr>
</tbody>
</table>




  

### Atenção

Observe que o operador “igual a”, `~=`, representa a noção usual de igualdade para os tipos `point`, `box`, `polygon` e `circle`. Alguns dos tipos geométricos também têm um operador `=`, mas `=` compara apenas por *áreas* iguais. Os outros operadores de comparação escalar (`<=` e assim por diante), onde disponíveis para esses tipos, também comparam áreas.

### Nota

Antes do PostgreSQL 14, os operadores de comparação ponto acima/abaixo estritamente `point` `<<|` `point` e `point` `|>>` `point` eram respectivamente chamados `<^` e `>^`. Esses nomes ainda estão disponíveis, mas são desaconselhados e, eventualmente, serão removidos.

**Tabela 9.37. Funções Geométrica**



<table border="1" class="table" summary="Geometric Functions">
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
      area
     </code>(<em class="replaceable">
<code>
       geometric_type
      </code>
</em>)<code class="returnvalue">
      double precision
     </code>
</p>
<p>Calcula a área. Disponível para<code class="type">
      box
     </code>,<code class="type">
      path
     </code>,<code class="type">
      circle
     </code>. A<code class="type">
      path
     </code>A entrada deve ser fechada, caso contrário, NULL é retornado. Além disso, se o<code class="type">
      path
     </code>se auto-intersecta, o resultado pode não ter sentido.</p>
<p>
<code class="literal">
      area(box '(2,2),(0,0)')
     </code>→<code class="returnvalue">
      4
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      center
     </code>(<em class="replaceable">
<code>
       geometric_type
      </code>
</em>)<code class="returnvalue">
      point
     </code>
</p>
<p>Calcula o ponto central. Disponível para<code class="type">
      box
     </code>,<code class="type">
      circle
     </code>
     .
    </p>
<p>
<code class="literal">
      center(box '(1,2),(0,0)')
     </code>→<code class="returnvalue">
      (0.5,1)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      diagonal
     </code>(<code class="type">
      box
     </code>)<code class="returnvalue">
      lseg
     </code>
</p>
<p>Extrai a diagonal da caixa como um segmento de linha (mesmo que<code class="function">
      lseg(box)
     </code>
     ).
    </p>
<p>
<code class="literal">
      diagonal(box '(1,2),(0,0)')
     </code>→<code class="returnvalue">
      [(1,2),(0,0)]
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      diameter
     </code>(<code class="type">
      circle
     </code>)<code class="returnvalue">
      double precision
     </code>
</p>
<p>Calcula o diâmetro do círculo.</p>
<p>
<code class="literal">
      diameter(circle '&lt;(0,0),2&gt;')
     </code>→<code class="returnvalue">
      4
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      height
     </code>(<code class="type">
      box
     </code>)<code class="returnvalue">
      double precision
     </code>
</p>
<p>Calcula o tamanho vertical da caixa.</p>
<p>
<code class="literal">
      height(box '(1,2),(0,0)')
     </code>→<code class="returnvalue">
      2
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      isclosed
     </code>(<code class="type">
      path
     </code>)<code class="returnvalue">
      boolean
     </code>
</p>
<p>O caminho está fechado?</p>
<p>
<code class="literal">
      isclosed(path '((0,0),(1,1),(2,0))')
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
      isopen
     </code>(<code class="type">
      path
     </code>)<code class="returnvalue">
      boolean
     </code>
</p>
<p>O caminho está aberto?</p>
<p>
<code class="literal">
      isopen(path '[(0,0),(1,1),(2,0)]')
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
      length
     </code>(<em class="replaceable">
<code>
       geometric_type
      </code>
</em>)<code class="returnvalue">
      double precision
     </code>
</p>
<p>Calcula o comprimento total. Disponível para<code class="type">
      lseg
     </code>,<code class="type">
      path
     </code>
     .
    </p>
<p>
<code class="literal">
      length(path '((-1,0),(1,0))')
     </code>→<code class="returnvalue">
      4
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      npoints
     </code>(<em class="replaceable">
<code>
       geometric_type
      </code>
</em>)<code class="returnvalue">
      integer
     </code>
</p>
<p>Retorna o número de pontos. Disponível para<code class="type">
      path
     </code>,<code class="type">
      polygon
     </code>
     .
    </p>
<p>
<code class="literal">
      npoints(path '[(0,0),(1,1),(2,0)]')
     </code>→<code class="returnvalue">
      3
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      pclose
     </code>(<code class="type">
      path
     </code>)<code class="returnvalue">
      path
     </code>
</p>
<p>Converte o caminho para uma forma fechada.</p>
<p>
<code class="literal">
      pclose(path '[(0,0),(1,1),(2,0)]')
     </code>→<code class="returnvalue">
      ((0,0),(1,1),(2,0))
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      popen
     </code>(<code class="type">
      path
     </code>)<code class="returnvalue">
      path
     </code>
</p>
<p>Converte o caminho para o formulário aberto.</p>
<p>
<code class="literal">
      popen(path '((0,0),(1,1),(2,0))')
     </code>→<code class="returnvalue">
      [(0,0),(1,1),(2,0)]
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      radius
     </code>(<code class="type">
      circle
     </code>)<code class="returnvalue">
      double precision
     </code>
</p>
<p>Calcula o raio do círculo.</p>
<p>
<code class="literal">
      radius(circle '&lt;(0,0),2&gt;')
     </code>→<code class="returnvalue">
      2
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      slope
     </code>(<code class="type">
      point
     </code>,<code class="type">
      point
     </code>)<code class="returnvalue">
      double precision
     </code>
</p>
<p>Calcula a inclinação de uma linha traçada pelos dois pontos.</p>
<p>
<code class="literal">
      slope(point '(0,0)', point '(2,1)')
     </code>→<code class="returnvalue">
      0.5
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      width
     </code>(<code class="type">
      box
     </code>)<code class="returnvalue">
      double precision
     </code>
</p>
<p>Calcula o tamanho horizontal da caixa.</p>
<p>
<code class="literal">
      width(box '(1,2),(0,0)')
     </code>→<code class="returnvalue">
      1
     </code>
</p>
</td>
</tr>
</tbody>
</table>




  

**Tabela 9.38. Funções de conversão de tipo geométrico**



<table border="1" class="table" summary="Geometric Type Conversion Functions">
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
      box
     </code>(<code class="type">
      circle
     </code>)<code class="returnvalue">
      box
     </code>
</p>
<p>Calcula a caixa inscrita dentro do círculo.</p>
<p>
<code class="literal">
      box(circle '&lt;(0,0),2&gt;')
     </code>→<code class="returnvalue">
      (1.414213562373095,1.414213562373095),​(-1.414213562373095,-1.414213562373095)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      box
     </code>(<code class="type">
      point
     </code>)<code class="returnvalue">
      box
     </code>
</p>
<p>Converte ponto em caixa vazia.</p>
<p>
<code class="literal">
      box(point '(1,0)')
     </code>→<code class="returnvalue">
      (1,0),(1,0)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      box
     </code>(<code class="type">
      point
     </code>,<code class="type">
      point
     </code>)<code class="returnvalue">
      box
     </code>
</p>
<p>Converte quaisquer dois pontos de canto em caixa.</p>
<p>
<code class="literal">
      box(point '(0,1)', point '(1,0)')
     </code>→<code class="returnvalue">
      (1,1),(0,0)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      box
     </code>(<code class="type">
      polygon
     </code>)<code class="returnvalue">
      box
     </code>
</p>
<p>Calcula a caixa de delimitação do polígono.</p>
<p>
<code class="literal">
      box(polygon '((0,0),(1,1),(2,0))')
     </code>→<code class="returnvalue">
      (2,1),(0,0)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      bound_box
     </code>(<code class="type">
      box
     </code>,<code class="type">
      box
     </code>)<code class="returnvalue">
      box
     </code>
</p>
<p>Calcula a caixa de delimitação de duas caixas.</p>
<p>
<code class="literal">
      bound_box(box '(1,1),(0,0)', box '(4,4),(3,3)')
     </code>→<code class="returnvalue">
      (4,4),(0,0)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      circle
     </code>(<code class="type">
      box
     </code>)<code class="returnvalue">
      circle
     </code>
</p>
<p>Calcula o menor círculo que envolve a caixa.</p>
<p>
<code class="literal">
      circle(box '(1,1),(0,0)')
     </code>→<code class="returnvalue">
      &lt;(0.5,0.5),0.7071067811865476&gt;
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      circle
     </code>(<code class="type">
      point
     </code>,<code class="type">
      double precision
     </code>)<code class="returnvalue">
      circle
     </code>
</p>
<p>Construa um círculo a partir do centro e do raio.</p>
<p>
<code class="literal">
      circle(point '(0,0)', 2.0)
     </code>→<code class="returnvalue">
      &lt;(0,0),2&gt;
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      circle
     </code>(<code class="type">
      polygon
     </code>)<code class="returnvalue">
      circle
     </code>
</p>
<p>Converte polígono em círculo. O centro do círculo é a média das posições dos pontos do polígono, e o raio é a distância média dos pontos do polígono a partir desse centro.</p>
<p>
<code class="literal">
      circle(polygon '((0,0),(1,3),(2,0))')
     </code>→<code class="returnvalue">
      &lt;(1,1),1.6094757082487299&gt;
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      line
     </code>(<code class="type">
      point
     </code>,<code class="type">
      point
     </code>)<code class="returnvalue">
      line
     </code>
</p>
<p>Converte dois pontos na linha que os une.</p>
<p>
<code class="literal">
      line(point '(-1,0)', point '(1,0)')
     </code>→<code class="returnvalue">
      {0,-1,0}
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      lseg
     </code>(<code class="type">
      box
     </code>)<code class="returnvalue">
      lseg
     </code>
</p>
<p>Extrai a diagonal da caixa como um segmento de linha.</p>
<p>
<code class="literal">
      lseg(box '(1,0),(-1,0)')
     </code>→<code class="returnvalue">
      [(1,0),(-1,0)]
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      lseg
     </code>(<code class="type">
      point
     </code>,<code class="type">
      point
     </code>)<code class="returnvalue">
      lseg
     </code>
</p>
<p>Construi um segmento de linha a partir de dois pontos finais.</p>
<p>
<code class="literal">
      lseg(point '(-1,0)', point '(1,0)')
     </code>→<code class="returnvalue">
      [(-1,0),(1,0)]
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      path
     </code>(<code class="type">
      polygon
     </code>)<code class="returnvalue">
      path
     </code>
</p>
<p>Converte polígono em um caminho fechado com a mesma lista de pontos.</p>
<p>
<code class="literal">
      path(polygon '((0,0),(1,1),(2,0))')
     </code>→<code class="returnvalue">
      ((0,0),(1,1),(2,0))
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      point
     </code>(<code class="type">
      double precision
     </code>,<code class="type">
      double precision
     </code>)<code class="returnvalue">
      point
     </code>
</p>
<p>Construi pontos a partir de suas coordenadas.</p>
<p>
<code class="literal">
      point(23.4, -44.5)
     </code>→<code class="returnvalue">
      (23.4,-44.5)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      point
     </code>(<code class="type">
      box
     </code>)<code class="returnvalue">
      point
     </code>
</p>
<p>Calcula o centro da caixa.</p>
<p>
<code class="literal">
      point(box '(1,0),(-1,0)')
     </code>→<code class="returnvalue">
      (0,0)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      point
     </code>(<code class="type">
      circle
     </code>)<code class="returnvalue">
      point
     </code>
</p>
<p>Calcula o centro do círculo.</p>
<p>
<code class="literal">
      point(circle '&lt;(0,0),2&gt;')
     </code>→<code class="returnvalue">
      (0,0)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      point
     </code>(<code class="type">
      lseg
     </code>)<code class="returnvalue">
      point
     </code>
</p>
<p>Calcula o centro do segmento de linha.</p>
<p>
<code class="literal">
      point(lseg '[(-1,0),(1,0)]')
     </code>→<code class="returnvalue">
      (0,0)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      point
     </code>(<code class="type">
      polygon
     </code>)<code class="returnvalue">
      point
     </code>
</p>
<p>Calcula o centro do polígono (a média das posições dos pontos do polígono).</p>
<p>
<code class="literal">
      point(polygon '((0,0),(1,1),(2,0))')
     </code>→<code class="returnvalue">
      (1,0.3333333333333333)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      polygon
     </code>(<code class="type">
      box
     </code>)<code class="returnvalue">
      polygon
     </code>
</p>
<p>Converte a caixa em um polígono de 4 pontos.</p>
<p>
<code class="literal">
      polygon(box '(1,1),(0,0)')
     </code>→<code class="returnvalue">
      ((0,0),(0,1),(1,1),(1,0))
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      polygon
     </code>(<code class="type">
      circle
     </code>)<code class="returnvalue">
      polygon
     </code>
</p>
<p>Converte o círculo em um polígono de 12 pontos.</p>
<p>
<code class="literal">
      polygon(circle '&lt;(0,0),2&gt;')
     </code>→<code class="returnvalue">
      ((-2,0),​(-1.7320508075688774,0.9999999999999999),​(-1.0000000000000002,1.7320508075688772),​(-1.2246063538223773e-16,2),​(0.9999999999999996,1.7320508075688774),​(1.732050807568877,1.0000000000000007),​(2,2.4492127076447545e-16),​(1.7320508075688776,-0.9999999999999994),​(1.0000000000000009,-1.7320508075688767),​(3.673819061467132e-16,-2),​(-0.9999999999999987,-1.732050807568878),​(-1.7320508075688767,-1.0000000000000009))
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      polygon
     </code>(<code class="type">
      integer
     </code>,<code class="type">
      circle
     </code>)<code class="returnvalue">
      polygon
     </code>
</p>
<p>Converte círculo em<em class="replaceable">
<code>
       n
      </code>
</em>- ponto poligonal.</p>
<p>
<code class="literal">
      polygon(4, circle '&lt;(3,0),1&gt;')
     </code>→<code class="returnvalue">
      ((2,0),​(3,1),​(4,1.2246063538223773e-16),​(3,-1))
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      polygon
     </code>(<code class="type">
      path
     </code>)<code class="returnvalue">
      polygon
     </code>
</p>
<p>Converte o caminho fechado em um polígono com a mesma lista de pontos.</p>
<p>
<code class="literal">
      polygon(path '((0,0),(1,1),(2,0))')
     </code>→<code class="returnvalue">
      ((0,0),(1,1),(2,0))
     </code>
</p>
</td>
</tr>
</tbody>
</table>




  

É possível acessar os dois números de componentes de um `point` como se o ponto fosse um array com índices 0 e 1. Por exemplo, se `t.p` é uma coluna de `point`, então `SELECT p[0] FROM t` recupera a coordenada X e `UPDATE t SET p[1] = ...` altera a coordenada Y. Da mesma forma, um valor do tipo `box` ou `lseg` pode ser tratado como um array de dois valores de `point`.