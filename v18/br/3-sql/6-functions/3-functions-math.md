## 9.3. Funções e operadores matemáticos [#](#FUNCTIONS-MATH)

Operadores matemáticos são fornecidos para muitos tipos do PostgreSQL. Para tipos sem convenções matemáticas padrão (por exemplo, tipos de data/hora), descrevemos o comportamento real nas seções subsequentes.

[Tabela 9.4](functions-math.md#FUNCTIONS-MATH-OP-TABLE "Table 9.4. Mathematical Operators") mostra os operadores matemáticos disponíveis para os tipos numéricos padrão. A menos que indicado de outra forma, os operadores mostrados como aceitando *`numeric_type`* estão disponíveis para todos os tipos `smallint`, `integer`, `bigint`, `numeric`, `real` e `double precision`. Os operadores mostrados como aceitando *`integral_type`* estão disponíveis para os tipos `smallint`, `integer` e `bigint`. Exceto onde indicado, cada forma de um operador retorna o mesmo tipo de dados que seus(s) argumento(s). Chamadas que envolvem vários tipos de dados de argumento, como `integer` `+` `numeric`, são resolvidas usando o tipo que aparece mais tarde nessas listas.

**Tabela 9.4. Operadores Matemáticos**



<table>
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
     <code>
      +
     </code>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     →
     <code>
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
     <code>
      2 + 3
     </code>
     →
     <code>
      5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      +
     </code>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     →
     <code>
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
     <code>
      + 3.5
     </code>
     →
     <code>
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
     <code>
      -
     </code>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     →
     <code>
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
     <code>
      2 - 3
     </code>
     →
     <code>
      -1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      -
     </code>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     →
     <code>
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
     <code>
      - (-4)
     </code>
     →
     <code>
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
     <code>
      *
     </code>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     →
     <code>
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
     <code>
      2 * 3
     </code>
     →
     <code>
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
     <code>
      /
     </code>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     →
     <code>
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
     <code>
      5.0 / 2
     </code>
     →
     <code>
      2.5000000000000000
     </code>
    </p>
    <p>
     <code>
      5 / 2
     </code>
     →
     <code>
      2
     </code>
    </p>
    <p>
     <code>
      (-5) / 2
     </code>
     →
     <code>
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
     <code>
      %
     </code>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        numeric_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Modulo (remainder); available for
     <code>
      smallint
     </code>
     ,
     <code>
      integer
     </code>
     ,
     <code>
      bigint
     </code>
     , and
     <code>
      numeric
     </code>
    </p>
    <p>
     <code>
      5 % 4
     </code>
     →
     <code>
      1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      numeric
     </code>
     <code>
      ^
     </code>
     <code>
      numeric
     </code>
     →
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      double precision
     </code>
     <code>
      ^
     </code>
     <code>
      double precision
     </code>
     →
     <code>
      double precision
     </code>
    </p>
    <p>
     Exponentiation
    </p>
    <p>
     <code>
      2 ^ 3
     </code>
     →
     <code>
      8
     </code>
    </p>
    <p>
     Unlike typical mathematical practice, multiple uses of
     <code>
      ^
     </code>
     will associate left to right by default:
    </p>
    <p>
     <code>
      2 ^ 3 ^ 3
     </code>
     →
     <code>
      512
     </code>
    </p>
    <p>
     <code>
      2 ^ (3 ^ 3)
     </code>
     →
     <code>
      134217728
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      |/
     </code>
     <code>
      double precision
     </code>
     →
     <code>
      double precision
     </code>
    </p>
    <p>
     Square root
    </p>
    <p>
     <code>
      |/ 25.0
     </code>
     →
     <code>
      5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ||/
     </code>
     <code>
      double precision
     </code>
     →
     <code>
      double precision
     </code>
    </p>
    <p>
     Cube root
    </p>
    <p>
     <code>
      ||/ 64.0
     </code>
     →
     <code>
      4
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      @
     </code>
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     →
     <code>
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
     <code>
      @ -5.0
     </code>
     →
     <code>
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
     <code>
      &amp;
     </code>
     <em class="replaceable">
      <code>
       integral_type
      </code>
     </em>
     →
     <code>
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
     <code>
      91 &amp; 15
     </code>
     →
     <code>
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
     <code>
      |
     </code>
     <em class="replaceable">
      <code>
       integral_type
      </code>
     </em>
     →
     <code>
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
     <code>
      32 | 3
     </code>
     →
     <code>
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
     <code>
      #
     </code>
     <em class="replaceable">
      <code>
       integral_type
      </code>
     </em>
     →
     <code>
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
     <code>
      17 # 5
     </code>
     →
     <code>
      20
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ~
     </code>
     <em class="replaceable">
      <code>
       integral_type
      </code>
     </em>
     →
     <code>
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
     <code>
      ~1
     </code>
     →
     <code>
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
     <code>
      &lt;&lt;
     </code>
     <code>
      integer
     </code>
     →
     <code>
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
     <code>
      1 &lt;&lt; 4
     </code>
     →
     <code>
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
     <code>
      &gt;&gt;
     </code>
     <code>
      integer
     </code>
     →
     <code>
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
     <code>
      8 &gt;&gt; 2
     </code>
     →
     <code>
      2
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>










[Tabela 9.5](functions-math.md#FUNCTIONS-MATH-FUNC-TABLE) mostra as funções matemáticas disponíveis. Muitas dessas funções são fornecidas em várias formas com diferentes tipos de argumentos. Exceto onde indicado, qualquer forma dada de uma função retorna o mesmo tipo de dados que seus(s) argumento(s); casos de cruzamento de tipos são resolvidos da mesma maneira como explicado acima para operadores. As funções que trabalham com dados de `double precision` são implementadas principalmente no topo da biblioteca C do sistema hospedeiro; portanto, a precisão e o comportamento em casos de fronteira podem variar dependendo do sistema hospedeiro.

**Tabela 9.5. Funções matemáticas**



<table>
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
     <code>
      abs
     </code>
     (
     <em class="replaceable">
      <code>
       numeric_type
      </code>
     </em>
     )
     <code>
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
     <code>
      abs(-17.4)
     </code>
     →
     <code>
      17.4
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cbrt
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Raiz cúbica
    </p>
    <p>
     <code>
      cbrt(64.0)
     </code>
     →
     <code>
      4
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ceil
     </code>
     (
     <code>
      numeric
     </code>
     )
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      ceil
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Número inteiro mais próximo do argumento ou igual a ele
    </p>
    <p>
     <code>
      ceil(42.2)
     </code>
     →
     <code>
      43
     </code>
    </p>
    <p>
     <code>
      ceil(-42.8)
     </code>
     →
     <code>
      -42
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ceiling
     </code>
     (
     <code>
      numeric
     </code>
     )
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      ceiling
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Número inteiro mais próximo do argumento (mesmo que igual) (o mesmo que
     <code>
      ceil
     </code>
     )
    </p>
    <p>
     <code>
      ceiling(95.3)
     </code>
     →
     <code>
      96
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      degrees
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Converte radianos em graus
    </p>
    <p>
     <code>
      degrees(0.5)
     </code>
     →
     <code>
      28.64788975654116
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      div
     </code>
     (
     <em class="parameter">
      <code>
       y
      </code>
     </em>
     <code>
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       x
      </code>
     </em>
     <code>
      numeric
     </code>
     )
     <code>
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
     <code>
      div(9, 4)
     </code>
     →
     <code>
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      erf
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Função de erro
    </p>
    <p>
     <code>
      erf(1.0)
     </code>
     →
     <code>
      0.8427007929497149
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      erfc
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Função de erro complementar (
     <code>
      1 - erf(x)
     </code>
     , sem perda de precisão para grandes entradas)
    </p>
    <p>
     <code>
      erfc(1.0)
     </code>
     →
     <code>
      0.15729920705028513
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      exp
     </code>
     (
     <code>
      numeric
     </code>
     )
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      exp
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Explicativa (
     <code>
      e
     </code>
     elevado à potência dada)
    </p>
    <p>
     <code>
      exp(1.0)
     </code>
     →
     <code>
      2.7182818284590452
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      factorial
     </code>
     (
     <code>
      bigint
     </code>
     )
     <code>
      numeric
     </code>
    </p>
    <p>
     Fatorial
    </p>
    <p>
     <code>
      factorial(5)
     </code>
     →
     <code>
      120
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      floor
     </code>
     (
     <code>
      numeric
     </code>
     )
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      floor
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Número inteiro mais próximo, menor ou igual ao argumento
    </p>
    <p>
     <code>
      floor(42.8)
     </code>
     →
     <code>
      42
     </code>
    </p>
    <p>
     <code>
      floor(-42.8)
     </code>
     →
     <code>
      -43
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      gamma
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Função gama
    </p>
    <p>
     <code>
      gamma(0.5)
     </code>
     →
     <code>
      1.772453850905516
     </code>
    </p>
    <p>
     <code>
      gamma(6)
     </code>
     →
     <code>
      120
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
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
     <code>
      <em class="replaceable">
       <code>
        numeric_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Mínimo comum múltiplo (o maior número positivo que divide ambos os valores sem deixar resto); retorna
     <code>
      0
     </code>
     se ambos os inputs forem zero; disponível para
     <code>
      integer
     </code>
     ,
     <code>
      bigint
     </code>
     , e
     <code>
      numeric
     </code>
    </p>
    <p>
     <code>
      gcd(1071, 462)
     </code>
     →
     <code>
      21
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
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
     <code>
      <em class="replaceable">
       <code>
        numeric_type
       </code>
      </em>
     </code>
    </p>
    <p>
     Mínimo múltiplo comum (o menor número estritamente positivo que é um múltiplo integral de ambos os inputs); retorna
     <code>
      0
     </code>
     se qualquer uma das entradas for zero; disponível para
     <code>
      integer
     </code>
     ,
     <code>
      bigint
     </code>
     , e
     <code>
      numeric
     </code>
    </p>
    <p>
     <code>
      lcm(1071, 462)
     </code>
     →
     <code>
      23562
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      lgamma
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Logarítmico natural do valor absoluto da função gama
    </p>
    <p>
     <code>
      lgamma(1000)
     </code>
     →
     <code>
      5905.220423209181
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ln
     </code>
     (
     <code>
      numeric
     </code>
     )
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      ln
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Logarítmico natural
    </p>
    <p>
     <code>
      ln(2.0)
     </code>
     →
     <code>
      0.6931471805599453
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      log
     </code>
     (
     <code>
      numeric
     </code>
     )
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      log
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Logaritmo de base 10
    </p>
    <p>
     <code>
      log(100)
     </code>
     →
     <code>
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      log10
     </code>
     (
     <code>
      numeric
     </code>
     )
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      log10
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Logaritmo de base 10 (mesmo que
     <code>
      log
     </code>
     )
    </p>
    <p>
     <code>
      log10(1000)
     </code>
     →
     <code>
      3
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      log
     </code>
     (
     <em class="parameter">
      <code>
       b
      </code>
     </em>
     <code>
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       x
      </code>
     </em>
     <code>
      numeric
     </code>
     )
     <code>
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
     <code>
      log(2.0, 64.0)
     </code>
     →
     <code>
      6.0000000000000000
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      min_scale
     </code>
     (
     <code>
      numeric
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Escala mínima (número de dígitos decimais fracionários) necessária para representar o valor fornecido com precisão
    </p>
    <p>
     <code>
      min_scale(8.4100)
     </code>
     →
     <code>
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
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
     <code>
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
     <code>
      smallint
     </code>
     ,
     <code>
      integer
     </code>
     ,
     <code>
      bigint
     </code>
     , e
     <code>
      numeric
     </code>
    </p>
    <p>
     <code>
      mod(9, 4)
     </code>
     →
     <code>
      1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pi
     </code>
     (  )
     <code>
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
     <code>
      pi()
     </code>
     →
     <code>
      3.141592653589793
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      power
     </code>
     (
     <em class="parameter">
      <code>
       a
      </code>
     </em>
     <code>
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       b
      </code>
     </em>
     <code>
      numeric
     </code>
     )
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      power
     </code>
     (
     <em class="parameter">
      <code>
       a
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       b
      </code>
     </em>
     <code>
      double precision
     </code>
     )
     <code>
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
     <code>
      power(9, 3)
     </code>
     →
     <code>
      729
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      radians
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Converte graus em radianos
    </p>
    <p>
     <code>
      radians(45.0)
     </code>
     →
     <code>
      0.7853981633974483
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      round
     </code>
     (
     <code>
      numeric
     </code>
     )
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      round
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Arredonda para o número inteiro mais próximo. Para
     <code>
      numeric
     </code>
     , os laços são quebrados arredondando para longe de zero. Para
     <code>
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
     <code>
      round(42.4)
     </code>
     →
     <code>
      42
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      round
     </code>
     (
     <em class="parameter">
      <code>
       v
      </code>
     </em>
     <code>
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       s
      </code>
     </em>
     <code>
      integer
     </code>
     )
     <code>
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
     <code>
      round(42.4382, 2)
     </code>
     →
     <code>
      42.44
     </code>
    </p>
    <p>
     <code>
      round(1234.56, -1)
     </code>
     →
     <code>
      1230
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      scale
     </code>
     (
     <code>
      numeric
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Escala do argumento (número de dígitos decimais na parte fracionária)
    </p>
    <p>
     <code>
      scale(8.4100)
     </code>
     →
     <code>
      4
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sign
     </code>
     (
     <code>
      numeric
     </code>
     )
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      sign
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Sinal do argumento (-1, 0 ou +1)
    </p>
    <p>
     <code>
      sign(-8.4)
     </code>
     →
     <code>
      -1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sqrt
     </code>
     (
     <code>
      numeric
     </code>
     )
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      sqrt
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     raiz quadrada
    </p>
    <p>
     <code>
      sqrt(2)
     </code>
     →
     <code>
      1.4142135623730951
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      trim_scale
     </code>
     (
     <code>
      numeric
     </code>
     )
     <code>
      numeric
     </code>
    </p>
    <p>
     Reduz a escala do valor (número de dígitos decimais fracionários) removendo zeros finais
    </p>
    <p>
     <code>
      trim_scale(8.4100)
     </code>
     →
     <code>
      8.41
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      trunc
     </code>
     (
     <code>
      numeric
     </code>
     )
     <code>
      numeric
     </code>
    </p>
    <p class="func_signature">
     <code>
      trunc
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Trunca para inteiro (em direção a zero)
    </p>
    <p>
     <code>
      trunc(42.8)
     </code>
     →
     <code>
      42
     </code>
    </p>
    <p>
     <code>
      trunc(-42.8)
     </code>
     →
     <code>
      -42
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      trunc
     </code>
     (
     <em class="parameter">
      <code>
       v
      </code>
     </em>
     <code>
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       s
      </code>
     </em>
     <code>
      integer
     </code>
     )
     <code>
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
     <code>
      trunc(42.4382, 2)
     </code>
     →
     <code>
      42.43
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      width_bucket
     </code>
     (
     <em class="parameter">
      <code>
       operand
      </code>
     </em>
     <code>
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       low
      </code>
     </em>
     <code>
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       high
      </code>
     </em>
     <code>
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     <code>
      integer
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p class="func_signature">
     <code>
      width_bucket
     </code>
     (
     <em class="parameter">
      <code>
       operand
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       low
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       high
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     <code>
      integer
     </code>
     )
     <code>
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
     <code>
      0
     </code>
     para uma entrada menor que
     <em class="parameter">
      <code>
       low
      </code>
     </em>
     , ou
     <code>
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
     <code>
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
     <code>
      width_bucket(5.35, 0.024, 10.06, 5)
     </code>
     →
     <code>
      3
     </code>
    </p>
    <p>
     <code>
      width_bucket(9, 10, 0, 10)
     </code>
     →
     <code>
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      width_bucket
     </code>
     (
     <em class="parameter">
      <code>
       operand
      </code>
     </em>
     <code>
      anycompatible
     </code>
     ,
     <em class="parameter">
      <code>
       thresholds
      </code>
     </em>
     <code>
      anycompatiblearray
     </code>
     )
     <code>
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
     <code>
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
     <code>
      width_bucket(now(), array['yesterday', 'today', 'tomorrow']::timestamptz[])
     </code>
     →
     <code>
      2
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>










[Tabela 9.6](functions-math.md#FUNCTIONS-MATH-RANDOM-TABLE "Table 9.6. Random Functions") mostra funções para gerar números aleatórios.

**Tabela 9.6. Funções aleatórias**



<table>
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
     <code>
      random
     </code>
     ( )
     <code>
      double precision
     </code>
    </p>
    <p>
     Retorna um valor aleatório no intervalo 0,0 &lt;= x &lt; 1,0
    </p>
    <p>
     <code>
      random()
     </code>
     →
     <code>
      0.897124072839091
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      random
     </code>
     (
     <em class="parameter">
      <code>
       min
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       max
      </code>
     </em>
     <code>
      integer
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p class="func_signature">
     <code>
      random
     </code>
     (
     <em class="parameter">
      <code>
       min
      </code>
     </em>
     <code>
      bigint
     </code>
     ,
     <em class="parameter">
      <code>
       max
      </code>
     </em>
     <code>
      bigint
     </code>
     )
     <code>
      bigint
     </code>
    </p>
    <p class="func_signature">
     <code>
      random
     </code>
     (
     <em class="parameter">
      <code>
       min
      </code>
     </em>
     <code>
      numeric
     </code>
     ,
     <em class="parameter">
      <code>
       max
      </code>
     </em>
     <code>
      numeric
     </code>
     )
     <code>
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
     <code>
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
     <code>
      random(1, 10)
     </code>
     →
     <code>
      7
     </code>
    </p>
    <p>
     <code>
      random(-0.499, 0.499)
     </code>
     →
     <code>
      0.347
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      random_normal
     </code>
     ( [ ] )
     <span class="optional">
      <em class="parameter">
       <code>
        mean
       </code>
      </em>
      <code>
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
       <code>
        double precision
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code>
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
     <code>
      random_normal(0.0, 1.0)
     </code>
     →
     <code>
      0.051285419
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      setseed
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      void
     </code>
    </p>
    <p>
     Define a semente para o subsequente
     <code>
      random()
     </code>
     e
     <code>
      random_normal()
     </code>
     chamadas; o argumento deve estar entre -1,0 e 1,0, inclusive
    </p>
    <p>
     <code>
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



<table>
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
     <code>
      acos
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Cosseno inverso, resulta em radianos
    </p>
    <p>
     <code>
      acos(1)
     </code>
     →
     <code>
      0
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      acosd
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Cosseno inverso, em graus
    </p>
    <p>
     <code>
      acosd(0.5)
     </code>
     →
     <code>
      60
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      asin
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Senos inversos, em radianos
    </p>
    <p>
     <code>
      asin(1)
     </code>
     →
     <code>
      1.5707963267948966
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      asind
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Senos inversos, em graus
    </p>
    <p>
     <code>
      asind(0.5)
     </code>
     →
     <code>
      30
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      atan
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Tangente inversa, resultado em radianos
    </p>
    <p>
     <code>
      atan(1)
     </code>
     →
     <code>
      0.7853981633974483
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      atand
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Tangente inversa, em graus
    </p>
    <p>
     <code>
      atand(1)
     </code>
     →
     <code>
      45
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      atan2
     </code>
     (
     <em class="parameter">
      <code>
       y
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       x
      </code>
     </em>
     <code>
      double precision
     </code>
     )
     <code>
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
     <code>
      atan2(1, 0)
     </code>
     →
     <code>
      1.5707963267948966
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      atan2d
     </code>
     (
     <em class="parameter">
      <code>
       y
      </code>
     </em>
     <code>
      double precision
     </code>
     ,
     <em class="parameter">
      <code>
       x
      </code>
     </em>
     <code>
      double precision
     </code>
     )
     <code>
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
     <code>
      atan2d(1, 0)
     </code>
     →
     <code>
      90
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cos
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Cosseno, argumento em radianos
    </p>
    <p>
     <code>
      cos(0)
     </code>
     →
     <code>
      1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cosd
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Coseno, argumento em graus
    </p>
    <p>
     <code>
      cosd(60)
     </code>
     →
     <code>
      0.5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cot
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Cotangente, argumento em radianos
    </p>
    <p>
     <code>
      cot(0.5)
     </code>
     →
     <code>
      1.830487721712452
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cotd
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Cotangente, argumento em graus
    </p>
    <p>
     <code>
      cotd(45)
     </code>
     →
     <code>
      1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sin
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Sine, argumento em radianos
    </p>
    <p>
     <code>
      sin(1)
     </code>
     →
     <code>
      0.8414709848078965
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sind
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Sine, argumento em graus
    </p>
    <p>
     <code>
      sind(30)
     </code>
     →
     <code>
      0.5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      tan
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Tangente, argumento em radianos
    </p>
    <p>
     <code>
      tan(1)
     </code>
     →
     <code>
      1.5574077246549023
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      tand
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Tangente, argumento em graus
    </p>
    <p>
     <code>
      tand(45)
     </code>
     →
     <code>
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



<table>
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
     <code>
      sinh
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     seno hiperbólico
    </p>
    <p>
     <code>
      sinh(1)
     </code>
     →
     <code>
      1.1752011936438014
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      cosh
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Cosseno hiperbólico
    </p>
    <p>
     <code>
      cosh(0)
     </code>
     →
     <code>
      1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      tanh
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Tangente hiperbólica
    </p>
    <p>
     <code>
      tanh(1)
     </code>
     →
     <code>
      0.7615941559557649
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      asinh
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     seno hiperbólico inverso
    </p>
    <p>
     <code>
      asinh(1)
     </code>
     →
     <code>
      0.881373587019543
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      acosh
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Cosseno hiperbólico inverso
    </p>
    <p>
     <code>
      acosh(1)
     </code>
     →
     <code>
      0
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      atanh
     </code>
     (
     <code>
      double precision
     </code>
     )
     <code>
      double precision
     </code>
    </p>
    <p>
     Tangente hiperbólica inversa
    </p>
    <p>
     <code>
      atanh(0.5)
     </code>
     →
     <code>
      0.5493061443340548
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>





