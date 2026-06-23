## 9.3. Funções e operadores matemáticos [#](#FUNCTIONS-MATH)

Operadores matemáticos são fornecidos para muitos tipos do PostgreSQL. Para tipos sem convenções matemáticas padrão (por exemplo, tipos de data/hora), descrevemos o comportamento real nas seções subsequentes.

[Tabela 9.4](functions-math.md#FUNCTIONS-MATH-OP-TABLE "Table 9.4. Mathematical Operators") mostra os operadores matemáticos disponíveis para os tipos numéricos padrão. A menos que indicado de outra forma, os operadores mostrados como aceitando *`numeric_type`* estão disponíveis para todos os tipos `smallint`, `integer`, `bigint`, `numeric`, `real` e `double precision`. Os operadores mostrados como aceitando *`integral_type`* estão disponíveis para os tipos `smallint`, `integer` e `bigint`. Exceto onde indicado, cada forma de um operador retorna o mesmo tipo de dados que seus(s) argumento(s). Chamadas que envolvem vários tipos de dados de argumento, como `integer` `+` `numeric`, são resolvidas usando o tipo que aparece mais tarde nessas listas.

**Tabela 9.4. Operadores Matemáticos**



<table border="1" class="table" summary="Mathematical Operators">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Operator
    </p>
    <p>
     Description
    </p>
    <p>
     Example(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     <code class="literal">
      +
     </code>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        numeric_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Addition
    </p>
    <p>
     <code class="literal">
      2 + 3
     </code>
     →
     <code class="returnvalue">
      5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="literal">
      +
     </code>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        numeric_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Unary plus (no operation)
    </p>
    <p>
     <code class="literal">
      + 3.5
     </code>
     →
     <code class="returnvalue">
      3.5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     <code class="literal">
      -
     </code>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        numeric_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Subtraction
    </p>
    <p>
     <code class="literal">
      2 - 3
     </code>
     →
     <code class="returnvalue">
      -1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="literal">
      -
     </code>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        numeric_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Negation
    </p>
    <p>
     <code class="literal">
      - (-4)
     </code>
     →
     <code class="returnvalue">
      4
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     <code class="literal">
      *
     </code>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        numeric_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Multiplication
    </p>
    <p>
     <code class="literal">
      2 * 3
     </code>
     →
     <code class="returnvalue">
      6
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     <code class="literal">
      /
     </code>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        numeric_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Division (for integral types, division truncates the result towards zero)
    </p>
    <p>
     <code class="literal">
      5.0 / 2
     </code>
     →
     <code class="returnvalue">
      2.5000000000000000
     </code>
    </p>
    <p>
     <code class="literal">
      5 / 2
     </code>
     →
     <code class="returnvalue">
      2
     </code>
    </p>
    <p>
     <code class="literal">
      (-5) / 2
     </code>
     →
     <code class="returnvalue">
      -2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     <code class="literal">
      %
     </code>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        numeric_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Modulo (remainder); available for
     <code class="type">
      smallint
     </code>
     ,
     <code class="type">
      integer
     </code>
     ,
     <code class="type">
      bigint
     </code>
     , and
     <code class="type">
      numeric
     </code>
    </p>
    <p>
     <code class="literal">
      5 % 4
     </code>
     →
     <code class="returnvalue">
      1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      numeric
     </code>
     <code class="literal">
      ^
     </code>
     <code class="type">
      numeric
     </code>
     →
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code class="type">
      double precision
     </code>
     <code class="literal">
      ^
     </code>
     <code class="type">
      double precision
     </code>
     →
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Exponentiation
    </p>
    <p>
     <code class="literal">
      2 ^ 3
     </code>
     →
     <code class="returnvalue">
      8
     </code>
    </p>
    <p>
     Unlike typical mathematical practice, multiple uses of
     <code class="literal">
      ^
     </code>
     will associate left to right by default:
    </p>
    <p>
     <code class="literal">
      2 ^ 3 ^ 3
     </code>
     →
     <code class="returnvalue">
      512
     </code>
    </p>
    <p>
     <code class="literal">
      2 ^ (3 ^ 3)
     </code>
     →
     <code class="returnvalue">
      134217728
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="literal">
      |/
     </code>
     <code class="type">
      double precision
     </code>
     →
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Square root
    </p>
    <p>
     <code class="literal">
      |/ 25.0
     </code>
     →
     <code class="returnvalue">
      5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="literal">
      ||/
     </code>
     <code class="type">
      double precision
     </code>
     →
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Cube root
    </p>
    <p>
     <code class="literal">
      ||/ 64.0
     </code>
     →
     <code class="returnvalue">
      4
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="literal">
      @
     </code>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        numeric_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Absolute value
    </p>
    <p>
     <code class="literal">
      @ -5.0
     </code>
     →
     <code class="returnvalue">
      5.0
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       integral_type
      </code>
     </em>
     <code class="literal">
      &amp;
     </code>
     <em class="replaceable">
      <code>
       integral_type
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        integral_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Bitwise AND
    </p>
    <p>
     <code class="literal">
      91 &amp; 15
     </code>
     →
     <code class="returnvalue">
      11
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       integral_type
      </code>
     </em>
     <code class="literal">
      |
     </code>
     <em class="replaceable">
      <code>
       integral_type
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        integral_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Bitwise OR
    </p>
    <p>
     <code class="literal">
      32 | 3
     </code>
     →
     <code class="returnvalue">
      35
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       integral_type
      </code>
     </em>
     <code class="literal">
      #
     </code>
     <em class="replaceable">
      <code>
       integral_type
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        integral_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Bitwise exclusive OR
    </p>
    <p>
     <code class="literal">
      17 # 5
     </code>
     →
     <code class="returnvalue">
      20
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="literal">
      ~
     </code>
     <em class="replaceable">
      <code>
       integral_type
      </code>
     </em>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        integral_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Bitwise NOT
    </p>
    <p>
     <code class="literal">
      ~1
     </code>
     →
     <code class="returnvalue">
      -2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       integral_type
      </code>
     </em>
     <code class="literal">
      &lt;&lt;
     </code>
     <code class="type">
      integer
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        integral_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Bitwise shift left
    </p>
    <p>
     <code class="literal">
      1 &lt;&lt; 4
     </code>
     →
     <code class="returnvalue">
      16
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       integral_type
      </code>
     </em>
     <code class="literal">
      &gt;&gt;
     </code>
     <code class="type">
      integer
     </code>
     →
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        integral_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Bitwise shift right
    </p>
    <p>
     <code class="literal">
      8 &gt;&gt; 2
     </code>
     →
     <code class="returnvalue">
      2
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>










[Tabela 9.5](functions-math.md#FUNCTIONS-MATH-FUNC-TABLE) mostra as funções matemáticas disponíveis. Muitas dessas funções são fornecidas em várias formas com diferentes tipos de argumentos. Exceto onde indicado, qualquer forma dada de uma função retorna o mesmo tipo de dados que seus(s) argumento(s); casos de cruzamento de tipos são resolvidos da mesma maneira como explicado acima para operadores. As funções que trabalham com dados de `double precision` são implementadas principalmente no topo da biblioteca C do sistema hospedeiro; portanto, a precisão e o comportamento em casos de fronteira podem variar dependendo do sistema hospedeiro.

**Tabela 9.5. Funções matemáticas**



<table border="1" class="table" summary="Mathematical Functions">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função
    </p>
    <p>
     Descrição
    </p>
    <p>
     Exemplo(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      abs
     </code>
     (
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     )
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        numeric_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Valor absoluto
    </p>
    <p>
     <code class="literal">
      abs(-17.4)
     </code>
     →
     <code class="returnvalue">
      17.4
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      cbrt
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Raiz cúbica
    </p>
    <p>
     <code class="literal">
      cbrt(64.0)
     </code>
     →
     <code class="returnvalue">
      4
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      ceil
     </code>
     (
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      ceil
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Número inteiro mais próximo do argumento ou igual a ele
    </p>
    <p>
     <code class="literal">
      ceil(42.2)
     </code>
     →
     <code class="returnvalue">
      43
     </code>
    </p>
    <p>
     <code class="literal">
      ceil(-42.8)
     </code>
     →
     <code class="returnvalue">
      -42
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      ceiling
     </code>
     (
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      ceiling
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Número inteiro mais próximo do argumento (mesmo que igual) (o mesmo que
     <code class="function">
      ceil
     </code>
     )
    </p>
    <p>
     <code class="literal">
      ceiling(95.3)
     </code>
     →
     <code class="returnvalue">
      96
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      degrees
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Converte radianos em graus
    </p>
    <p>
     <code class="literal">
      degrees(0.5)
     </code>
     →
     <code class="returnvalue">
      28.64788975654116
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      div
     </code>
     (
     <em class="parameter">
      <code>
       y
      </code>
     </em>
     <code class="type">
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       x
      </code>
     </em>
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p>
     Quociente inteiro de
     <em class="parameter">
      <code>
       y
      </code>
     </em>
     /
     <em class="parameter">
      <code>
       x
      </code>
     </em>
     (truncado em direção a zero)
    </p>
    <p>
     <code class="literal">
      div(9, 4)
     </code>
     →
     <code class="returnvalue">
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      erf
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Função de erro
    </p>
    <p>
     <code class="literal">
      erf(1.0)
     </code>
     →
     <code class="returnvalue">
      0.8427007929497149
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      erfc
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Função de erro complementar (
     <code class="literal">
      1 - erf(x)
     </code>
     , sem perda de precisão para grandes entradas)
    </p>
    <p>
     <code class="literal">
      erfc(1.0)
     </code>
     →
     <code class="returnvalue">
      0.15729920705028513
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      exp
     </code>
     (
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      exp
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Explicativa (
     <code class="literal">
      e
     </code>
     elevado à potência dada)
    </p>
    <p>
     <code class="literal">
      exp(1.0)
     </code>
     →
     <code class="returnvalue">
      2.7182818284590452
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      factorial
     </code>
     (
     <code class="type">
      bigint
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p>
     Fatorial
    </p>
    <p>
     <code class="literal">
      factorial(5)
     </code>
     →
     <code class="returnvalue">
      120
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      floor
     </code>
     (
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      floor
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Número inteiro mais próximo, menor ou igual ao argumento
    </p>
    <p>
     <code class="literal">
      floor(42.8)
     </code>
     →
     <code class="returnvalue">
      42
     </code>
    </p>
    <p>
     <code class="literal">
      floor(-42.8)
     </code>
     →
     <code class="returnvalue">
      -43
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      gamma
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Função gama
    </p>
    <p>
     <code class="literal">
      gamma(0.5)
     </code>
     →
     <code class="returnvalue">
      1.772453850905516
     </code>
    </p>
    <p>
     <code class="literal">
      gamma(6)
     </code>
     →
     <code class="returnvalue">
      120
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      gcd
     </code>
     (
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     ,
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     )
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        numeric_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Mínimo comum múltiplo (o maior número positivo que divide ambos os valores sem deixar resto); retorna
     <code class="literal">
      0
     </code>
     se ambos os inputs forem zero; disponível para
     <code class="type">
      integer
     </code>
     ,
     <code class="type">
      bigint
     </code>
     , e
     <code class="type">
      numeric
     </code>
    </p>
    <p>
     <code class="literal">
      gcd(1071, 462)
     </code>
     →
     <code class="returnvalue">
      21
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      lcm
     </code>
     (
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     ,
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     )
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        numeric_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Mínimo múltiplo comum (o menor número estritamente positivo que é um múltiplo integral de ambos os inputs); retorna
     <code class="literal">
      0
     </code>
     se qualquer uma das entradas for zero; disponível para
     <code class="type">
      integer
     </code>
     ,
     <code class="type">
      bigint
     </code>
     , e
     <code class="type">
      numeric
     </code>
    </p>
    <p>
     <code class="literal">
      lcm(1071, 462)
     </code>
     →
     <code class="returnvalue">
      23562
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      lgamma
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Logarítmico natural do valor absoluto da função gama
    </p>
    <p>
     <code class="literal">
      lgamma(1000)
     </code>
     →
     <code class="returnvalue">
      5905.220423209181
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      ln
     </code>
     (
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      ln
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Logarítmico natural
    </p>
    <p>
     <code class="literal">
      ln(2.0)
     </code>
     →
     <code class="returnvalue">
      0.6931471805599453
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      log
     </code>
     (
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      log
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Logaritmo de base 10
    </p>
    <p>
     <code class="literal">
      log(100)
     </code>
     →
     <code class="returnvalue">
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      log10
     </code>
     (
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      log10
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Logaritmo de base 10 (mesmo que
     <code class="function">
      log
     </code>
     )
    </p>
    <p>
     <code class="literal">
      log10(1000)
     </code>
     →
     <code class="returnvalue">
      3
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      log
     </code>
     (
     <em class="parameter">
      <code>
       b
      </code>
     </em>
     <code class="type">
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       x
      </code>
     </em>
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p>
     Logaritmo de
     <em class="parameter">
      <code>
       x
      </code>
     </em>
     basear
     <em class="parameter">
      <code>
       b
      </code>
     </em>
    </p>
    <p>
     <code class="literal">
      log(2.0, 64.0)
     </code>
     →
     <code class="returnvalue">
      6.0000000000000000
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      min_scale
     </code>
     (
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Escala mínima (número de dígitos decimais fracionários) necessária para representar o valor fornecido com precisão
    </p>
    <p>
     <code class="literal">
      min_scale(8.4100)
     </code>
     →
     <code class="returnvalue">
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      mod
     </code>
     (
     <em class="parameter">
      <code>
       y
      </code>
     </em>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     ,
     <em class="parameter">
      <code>
       x
      </code>
     </em>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     )
     <code class="returnvalue">
      <em class="replaceable">
       <code>
        numeric_type
       </code>
      </em>
     </code>
    </p>
    <p>
     resto
     <em class="parameter">
      <code>
       y
      </code>
     </em>
     /
     <em class="parameter">
      <code>
       x
      </code>
     </em>
     ; disponível para
     <code class="type">
      smallint
     </code>
     ,
     <code class="type">
      integer
     </code>
     ,
     <code class="type">
      bigint
     </code>
     , e
     <code class="type">
      numeric
     </code>
    </p>
    <p>
     <code class="literal">
      mod(9, 4)
     </code>
     →
     <code class="returnvalue">
      1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pi
     </code>
     (  )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Valor aproximado de
     <span class="symbol_font">
      π
     </span>
    </p>
    <p>
     <code class="literal">
      pi()
     </code>
     →
     <code class="returnvalue">
      3.141592653589793
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      power
     </code>
     (
     <em class="parameter">
      <code>
       a
      </code>
     </em>
     <code class="type">
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       b
      </code>
     </em>
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      power
     </code>
     (
     <em class="parameter">
      <code>
       a
      </code>
     </em>
     <code class="type">
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       b
      </code>
     </em>
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     <em class="parameter">
      <code>
       a
      </code>
     </em>
     elevado à potência de
     <em class="parameter">
      <code>
       b
      </code>
     </em>
    </p>
    <p>
     <code class="literal">
      power(9, 3)
     </code>
     →
     <code class="returnvalue">
      729
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      radians
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Converte graus em radianos
    </p>
    <p>
     <code class="literal">
      radians(45.0)
     </code>
     →
     <code class="returnvalue">
      0.7853981633974483
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      round
     </code>
     (
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      round
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Arredonda para o número inteiro mais próximo. Para
     <code class="type">
      numeric
     </code>
     , os laços são quebrados arredondando para longe de zero. Para
     <code class="type">
      double precision
     </code>
     , o comportamento de resolução de empate depende da plataforma, mas
     <span class="quote">
      “
      <span class="quote">
       arredondar para o número par mais próximo
      </span>
      ”
     </span>
     é a regra mais comum.
    </p>
    <p>
     <code class="literal">
      round(42.4)
     </code>
     →
     <code class="returnvalue">
      42
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      round
     </code>
     (
     <em class="parameter">
      <code>
       v
      </code>
     </em>
     <code class="type">
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       s
      </code>
     </em>
     <code class="type">
      integer
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p>
     Rondas
     <em class="parameter">
      <code>
       v
      </code>
     </em>
     para
     <em class="parameter">
      <code>
       s
      </code>
     </em>
     Os decimais são quebrados arredondando-se para longe de zero.
    </p>
    <p>
     <code class="literal">
      round(42.4382, 2)
     </code>
     →
     <code class="returnvalue">
      42.44
     </code>
    </p>
    <p>
     <code class="literal">
      round(1234.56, -1)
     </code>
     →
     <code class="returnvalue">
      1230
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      scale
     </code>
     (
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Escala do argumento (número de dígitos decimais na parte fracionária)
    </p>
    <p>
     <code class="literal">
      scale(8.4100)
     </code>
     →
     <code class="returnvalue">
      4
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      sign
     </code>
     (
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      sign
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Sinal do argumento (-1, 0 ou +1)
    </p>
    <p>
     <code class="literal">
      sign(-8.4)
     </code>
     →
     <code class="returnvalue">
      -1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      sqrt
     </code>
     (
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      sqrt
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     raiz quadrada
    </p>
    <p>
     <code class="literal">
      sqrt(2)
     </code>
     →
     <code class="returnvalue">
      1.4142135623730951
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      trim_scale
     </code>
     (
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p>
     Reduz a escala do valor (número de dígitos decimais fracionários) removendo zeros finais
    </p>
    <p>
     <code class="literal">
      trim_scale(8.4100)
     </code>
     →
     <code class="returnvalue">
      8.41
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      trunc
     </code>
     (
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      trunc
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Trunca para inteiro (em direção a zero)
    </p>
    <p>
     <code class="literal">
      trunc(42.8)
     </code>
     →
     <code class="returnvalue">
      42
     </code>
    </p>
    <p>
     <code class="literal">
      trunc(-42.8)
     </code>
     →
     <code class="returnvalue">
      -42
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      trunc
     </code>
     (
     <em class="parameter">
      <code>
       v
      </code>
     </em>
     <code class="type">
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       s
      </code>
     </em>
     <code class="type">
      integer
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p>
     Trunca
     <em class="parameter">
      <code>
       v
      </code>
     </em>
     para
     <em class="parameter">
      <code>
       s
      </code>
     </em>
     decismais
    </p>
    <p>
     <code class="literal">
      trunc(42.4382, 2)
     </code>
     →
     <code class="returnvalue">
      42.43
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      width_bucket
     </code>
     (
     <em class="parameter">
      <code>
       operand
      </code>
     </em>
     <code class="type">
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       low
      </code>
     </em>
     <code class="type">
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       high
      </code>
     </em>
     <code class="type">
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     <code class="type">
      integer
     </code>
     )
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      width_bucket
     </code>
     (
     <em class="parameter">
      <code>
       operand
      </code>
     </em>
     <code class="type">
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       low
      </code>
     </em>
     <code class="type">
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       high
      </code>
     </em>
     <code class="type">
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     <code class="type">
      integer
     </code>
     )
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Retorna o número do bucket em que
     <em class="parameter">
      <code>
       operand
      </code>
     </em>
     caem em um histograma com
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     piquetes de largura igual que abrangem a faixa
     <em class="parameter">
      <code>
       low
      </code>
     </em>
     para
     <em class="parameter">
      <code>
       high
      </code>
     </em>
     . Os buckets têm limites inferiores inclusivos e limites superiores exclusivos. Retornos
     <code class="literal">
      0
     </code>
     para uma entrada menor que
     <em class="parameter">
      <code>
       low
      </code>
     </em>
     , ou
     <code class="literal">
      <em class="parameter">
       <code>
        count
       </code>
      </em>
      +1
     </code>
     para uma entrada maior ou igual a
     <em class="parameter">
      <code>
       high
      </code>
     </em>
     . Se
     <em class="parameter">
      <code>
       low
      </code>
     </em>
     &gt;
     <em class="parameter">
      <code>
       high
      </code>
     </em>
     , o comportamento é invertido no espelho, com balde
     <code class="literal">
      1
     </code>
     agora sendo a única logo abaixo
     <em class="parameter">
      <code>
       low
      </code>
     </em>
     , e os limites inclusivos estão agora no lado superior.
    </p>
    <p>
     <code class="literal">
      width_bucket(5.35, 0.024, 10.06, 5)
     </code>
     →
     <code class="returnvalue">
      3
     </code>
    </p>
    <p>
     <code class="literal">
      width_bucket(9, 10, 0, 10)
     </code>
     →
     <code class="returnvalue">
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      width_bucket
     </code>
     (
     <em class="parameter">
      <code>
       operand
      </code>
     </em>
     <code class="type">
      anycompatible
     </code>
     ,
     <em class="parameter">
      <code>
       thresholds
      </code>
     </em>
     <code class="type">
      anycompatiblearray
     </code>
     )
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Retorna o número do bucket em que
     <em class="parameter">
      <code>
       operand
      </code>
     </em>
     devolve uma lista de quedas que indicam os limites inferiores inclusivos dos buckets. Devolve
     <code class="literal">
      0
     </code>
     para uma entrada menor que a primeira faixa inferior.
     <em class="parameter">
      <code>
       operand
      </code>
     </em>
     e os elementos da matriz podem ser de qualquer tipo que tenha operadores de comparação padrão.
     <em class="parameter">
      <code>
       thresholds
      </code>
     </em>
     array
     <span class="emphasis">
      <em>
       devem ser classificados
      </em>
     </span>
     , da menor para a maior, ou resultados inesperados serão obtidos.
    </p>
    <p>
     <code class="literal">
      width_bucket(now(), array['yesterday', 'today', 'tomorrow']::timestamptz[])
     </code>
     →
     <code class="returnvalue">
      2
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>










[Tabela 9.6](functions-math.md#FUNCTIONS-MATH-RANDOM-TABLE "Table 9.6. Random Functions") mostra funções para gerar números aleatórios.

**Tabela 9.6. Funções aleatórias**



<table border="1" class="table" summary="Random Functions">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função
    </p>
    <p>
     Descrição
    </p>
    <p>
     Exemplo(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      random
     </code>
     ( )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Retorna um valor aleatório no intervalo 0,0 &lt;= x &lt; 1,0
    </p>
    <p>
     <code class="literal">
      random()
     </code>
     →
     <code class="returnvalue">
      0.897124072839091
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      random
     </code>
     (
     <em class="parameter">
      <code>
       min
      </code>
     </em>
     <code class="type">
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       max
      </code>
     </em>
     <code class="type">
      integer
     </code>
     )
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      random
     </code>
     (
     <em class="parameter">
      <code>
       min
      </code>
     </em>
     <code class="type">
      bigint
     </code>
     ,
     <em class="parameter">
      <code>
       max
      </code>
     </em>
     <code class="type">
      bigint
     </code>
     )
     <code class="returnvalue">
      bigint
     </code>
    </p>
    <p class="func_signature">
     <code class="function">
      random
     </code>
     (
     <em class="parameter">
      <code>
       min
      </code>
     </em>
     <code class="type">
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       max
      </code>
     </em>
     <code class="type">
      numeric
     </code>
     )
     <code class="returnvalue">
      numeric
     </code>
    </p>
    <p>
     Retorna um valor aleatório na faixa
     <em class="parameter">
      <code>
       min
      </code>
     </em>
     &lt;= x &lt;=
     <em class="parameter">
      <code>
       max
      </code>
     </em>
     . Para o tipo
     <code class="type">
      numeric
     </code>
     , o resultado terá o mesmo número de dígitos decimais fracionários que
     <em class="parameter">
      <code>
       min
      </code>
     </em>
     ou
     <em class="parameter">
      <code>
       max
      </code>
     </em>
     , aquela que tiver mais.
    </p>
    <p>
     <code class="literal">
      random(1, 10)
     </code>
     →
     <code class="returnvalue">
      7
     </code>
    </p>
    <p>
     <code class="literal">
      random(-0.499, 0.499)
     </code>
     →
     <code class="returnvalue">
      0.347
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      random_normal
     </code>
     ( [ ] )
     <span class="optional">
      <em class="parameter">
       <code>
        mean
       </code>
      </em>
      <code class="type">
       double precision
      </code>
      [
      <span class="optional">
       ,
       <em class="parameter">
        <code>
         stddev
        </code>
       </em>
       <code class="type">
        double precision
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Retorna um valor aleatório da distribuição normal com os parâmetros fornecidos;
     <em class="parameter">
      <code>
       mean
      </code>
     </em>
     o padrão é 0,0 e
     <em class="parameter">
      <code>
       stddev
      </code>
     </em>
     o padrão é 1,0
    </p>
    <p>
     <code class="literal">
      random_normal(0.0, 1.0)
     </code>
     →
     <code class="returnvalue">
      0.051285419
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      setseed
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      void
     </code>
    </p>
    <p>
     Define a semente para o subsequente
     <code class="literal">
      random()
     </code>
     e
     <code class="literal">
      random_normal()
     </code>
     chamadas; o argumento deve estar entre -1,0 e 1,0, inclusive
    </p>
    <p>
     <code class="literal">
      setseed(0.12345)
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>










As funções `random()` e `random_normal()` listadas na [Tabela 9.6](functions-math.md#FUNCTIONS-MATH-RANDOM-TABLE "Table 9.6. Random Functions") utilizam um gerador de números pseudoaleatórios determinístico. É rápido, mas não é adequado para aplicações criptográficas; consulte o módulo [pgcrypto](pgcrypto.md "F.26. pgcrypto — cryptographic functions") para uma alternativa mais segura. Se `setseed()` for chamado, a série de resultados das chamadas subsequentes a essas funções na sessão atual pode ser repetida reemitindo `setseed()` com o mesmo argumento. Sem qualquer chamada prévia de `setseed()` na mesma sessão, a primeira chamada para qualquer uma dessas funções obtém uma semente de uma fonte dependente da plataforma de bits aleatórios.

[Tabela 9.7](functions-math.md#FUNCTIONS-MATH-TRIG-TABLE) mostra as funções trigonométricas disponíveis. Cada uma dessas funções vem em duas variantes, uma que mede ângulos em radianos e outra que mede ângulos em graus.

**Tabela 9.7. Funções trigonométricas**



<table border="1" class="table" summary="Trigonometric Functions">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função
    </p>
    <p>
     Descrição
    </p>
    <p>
     Exemplo(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      acos
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Cosseno inverso, resulta em radianos
    </p>
    <p>
     <code class="literal">
      acos(1)
     </code>
     →
     <code class="returnvalue">
      0
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      acosd
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Cosseno inverso, em graus
    </p>
    <p>
     <code class="literal">
      acosd(0.5)
     </code>
     →
     <code class="returnvalue">
      60
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      asin
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Senos inversos, em radianos
    </p>
    <p>
     <code class="literal">
      asin(1)
     </code>
     →
     <code class="returnvalue">
      1.5707963267948966
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      asind
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Senos inversos, em graus
    </p>
    <p>
     <code class="literal">
      asind(0.5)
     </code>
     →
     <code class="returnvalue">
      30
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      atan
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Tangente inversa, resultado em radianos
    </p>
    <p>
     <code class="literal">
      atan(1)
     </code>
     →
     <code class="returnvalue">
      0.7853981633974483
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      atand
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Tangente inversa, em graus
    </p>
    <p>
     <code class="literal">
      atand(1)
     </code>
     →
     <code class="returnvalue">
      45
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      atan2
     </code>
     (
     <em class="parameter">
      <code>
       y
      </code>
     </em>
     <code class="type">
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       x
      </code>
     </em>
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Tangente inversa de
     <em class="parameter">
      <code>
       y
      </code>
     </em>
     /
     <em class="parameter">
      <code>
       x
      </code>
     </em>
     , resulta em radianos
    </p>
    <p>
     <code class="literal">
      atan2(1, 0)
     </code>
     →
     <code class="returnvalue">
      1.5707963267948966
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      atan2d
     </code>
     (
     <em class="parameter">
      <code>
       y
      </code>
     </em>
     <code class="type">
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       x
      </code>
     </em>
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Tangente inversa de
     <em class="parameter">
      <code>
       y
      </code>
     </em>
     /
     <em class="parameter">
      <code>
       x
      </code>
     </em>
     , resultando em graus
    </p>
    <p>
     <code class="literal">
      atan2d(1, 0)
     </code>
     →
     <code class="returnvalue">
      90
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      cos
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Cosseno, argumento em radianos
    </p>
    <p>
     <code class="literal">
      cos(0)
     </code>
     →
     <code class="returnvalue">
      1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      cosd
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Coseno, argumento em graus
    </p>
    <p>
     <code class="literal">
      cosd(60)
     </code>
     →
     <code class="returnvalue">
      0.5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      cot
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Cotangente, argumento em radianos
    </p>
    <p>
     <code class="literal">
      cot(0.5)
     </code>
     →
     <code class="returnvalue">
      1.830487721712452
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      cotd
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Cotangente, argumento em graus
    </p>
    <p>
     <code class="literal">
      cotd(45)
     </code>
     →
     <code class="returnvalue">
      1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      sin
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Sine, argumento em radianos
    </p>
    <p>
     <code class="literal">
      sin(1)
     </code>
     →
     <code class="returnvalue">
      0.8414709848078965
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      sind
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Sine, argumento em graus
    </p>
    <p>
     <code class="literal">
      sind(30)
     </code>
     →
     <code class="returnvalue">
      0.5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      tan
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Tangente, argumento em radianos
    </p>
    <p>
     <code class="literal">
      tan(1)
     </code>
     →
     <code class="returnvalue">
      1.5574077246549023
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      tand
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Tangente, argumento em graus
    </p>
    <p>
     <code class="literal">
      tand(45)
     </code>
     →
     <code class="returnvalue">
      1
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>










Nota

Outra maneira de trabalhar com ângulos medidos em graus é usar as funções de transformação de unidade `radians()` e `degrees()`, mostradas anteriormente. No entanto, é preferível usar as funções trigonométricas baseadas em graus, pois dessa forma é evitado o erro de arredondamento para casos especiais, como `sind(30)`.

[Tabela 9.8](functions-math.md#FUNCTIONS-MATH-HYP-TABLE "Table 9.8. Hyperbolic Functions") mostra as funções hiperbólicas disponíveis.

**Tabela 9.8. Funções hiperbólicas**



<table border="1" class="table" summary="Hyperbolic Functions">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função
    </p>
    <p>
     Descrição
    </p>
    <p>
     Exemplo(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      sinh
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     seno hiperbólico
    </p>
    <p>
     <code class="literal">
      sinh(1)
     </code>
     →
     <code class="returnvalue">
      1.1752011936438014
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      cosh
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Cosseno hiperbólico
    </p>
    <p>
     <code class="literal">
      cosh(0)
     </code>
     →
     <code class="returnvalue">
      1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      tanh
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Tangente hiperbólica
    </p>
    <p>
     <code class="literal">
      tanh(1)
     </code>
     →
     <code class="returnvalue">
      0.7615941559557649
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      asinh
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     seno hiperbólico inverso
    </p>
    <p>
     <code class="literal">
      asinh(1)
     </code>
     →
     <code class="returnvalue">
      0.881373587019543
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      acosh
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Cosseno hiperbólico inverso
    </p>
    <p>
     <code class="literal">
      acosh(1)
     </code>
     →
     <code class="returnvalue">
      0
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      atanh
     </code>
     (
     <code class="type">
      double precision
     </code>
     )
     <code class="returnvalue">
      double precision
     </code>
    </p>
    <p>
     Tangente hiperbólica inversa
    </p>
    <p>
     <code class="literal">
      atanh(0.5)
     </code>
     →
     <code class="returnvalue">
      0.5493061443340548
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>





