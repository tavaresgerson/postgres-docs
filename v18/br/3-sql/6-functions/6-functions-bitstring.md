### 9.6. Funções e operadores de string de bits [#](#FUNCTIONS-BITSTRING)

Esta seção descreve funções e operadores para examinar e manipular strings de bits, ou seja, valores dos tipos `bit` e `bit varying`. (Embora apenas o tipo `bit` seja mencionado nessas tabelas, os valores do tipo `bit varying` podem ser usados de forma intercambiável.) As strings de bits suportam os operadores de comparação usuais mostrados em [Tabela 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE "Table 9.1. Comparison Operators"), bem como os operadores mostrados em [Tabela 9.14](functions-bitstring.md#FUNCTIONS-BIT-STRING-OP-TABLE "Table 9.14. Bit String Operators").

**Tabela 9.14. Operadores de String de Bits**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Operador
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
      bit
     </code>
     <code>
      ||
     </code>
     <code>
      bit
     </code>
     →
     <code>
      bit
     </code>
    </p>
    <p>
     Concatenação
    </p>
    <p>
     <code>
      B'10001' || B'011'
     </code>
     →
     <code>
      10001011
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      bit
     </code>
     <code>
      &amp;
     </code>
     <code>
      bit
     </code>
     →
     <code>
      bit
     </code>
    </p>
    <p>
     E AND (as entradas devem ter a mesma comprimento)
    </p>
    <p>
     <code>
      B'10001' &amp; B'01101'
     </code>
     →
     <code>
      00001
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      bit
     </code>
     <code>
      |
     </code>
     <code>
      bit
     </code>
     →
     <code>
      bit
     </code>
    </p>
    <p>
     XOR (as entradas devem ter a mesma comprimento)
    </p>
    <p>
     <code>
      B'10001' | B'01101'
     </code>
     →
     <code>
      11101
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      bit
     </code>
     <code>
      #
     </code>
     <code>
      bit
     </code>
     →
     <code>
      bit
     </code>
    </p>
    <p>
     XOR (bit a bit) (os inputs devem ter a mesma extensão)
    </p>
    <p>
     <code>
      B'10001' # B'01101'
     </code>
     →
     <code>
      11100
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
     <code>
      bit
     </code>
     →
     <code>
      bit
     </code>
    </p>
    <p>
     Bitwise NOT
    </p>
    <p>
     <code>
      ~ B'10001'
     </code>
     →
     <code>
      01110
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      bit
     </code>
     <code>
      &lt;&lt;
     </code>
     <code>
      integer
     </code>
     →
     <code>
      bit
     </code>
    </p>
    <p>
     Deslocamento lógico à esquerda (comprimento da string é preservado)
    </p>
    <p>
     <code>
      B'10001' &lt;&lt; 3
     </code>
     →
     <code>
      01000
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      bit
     </code>
     <code>
      &gt;&gt;
     </code>
     <code>
      integer
     </code>
     →
     <code>
      bit
     </code>
    </p>
    <p>
     Deslocamento à direita de bits (o comprimento da string é preservado)
    </p>
    <p>
     <code>
      B'10001' &gt;&gt; 2
     </code>
     →
     <code>
      00100
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>

Algumas das funções disponíveis para strings binárias também estão disponíveis para strings de bits, conforme mostrado na [Tabela 9.15](functions-bitstring.md#FUNCTIONS-BIT-STRING-TABLE).

**Tabela 9.15. Funções de String de Bits**

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
      bit_count
     </code>
     (
     <code>
      bit
     </code>
     )
     <code>
      bigint
     </code>
    </p>
    <p>
     Retorna o número de bits definidos na string de bits (também conhecida como
     <span class="quote">
      “
      <span class="quote">
       popcount
      </span>
      ”
     </span>
     ).
    </p>
    <p>
     <code>
      bit_count(B'10111')
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
      bit_length
     </code>
     (
     <code>
      bit
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o número de bits na string de bits.
    </p>
    <p>
     <code>
      bit_length(B'10111')
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
      length
     </code>
     (
     <code>
      bit
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o número de bits na string de bits.
    </p>
    <p>
     <code>
      length(B'10111')
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
      octet_length
     </code>
     (
     <code>
      bit
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o número de bytes na string de bits.
    </p>
    <p>
     <code>
      octet_length(B'1011111011')
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
      overlay
     </code>
     (
     <em class="parameter">
      <code>
       bits
      </code>
     </em>
     <code>
      bit
     </code>
     <code>
      PLACING
     </code>
     <em class="parameter">
      <code>
       newsubstring
      </code>
     </em>
     <code>
      bit
     </code>
     <code>
      FROM
     </code>
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     <code>
      integer
     </code>
     [
     <span class="optional">
      <code>
       FOR
      </code>
      <em class="parameter">
       <code>
        count
       </code>
      </em>
      <code>
       integer
      </code>
     </span>
     ] )
     <code>
      bit
     </code>
    </p>
    <p>
     Substitui a subdivisão de
     <em class="parameter">
      <code>
       bits
      </code>
     </em>
     que começa em
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     'aquele e se estende por
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     bits com
     <em class="parameter">
      <code>
       newsubstring
      </code>
     </em>
     . Se
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     Se for omitido, ele tem como padrão o comprimento de
     <em class="parameter">
      <code>
       newsubstring
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      overlay(B'01010101010101010' placing B'11111' from 2 for 3)
     </code>
     →
     <code>
      0111110101010101010
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      position
     </code>
     (
     <em class="parameter">
      <code>
       substring
      </code>
     </em>
     <code>
      bit
     </code>
     <code>
      IN
     </code>
     <em class="parameter">
      <code>
       bits
      </code>
     </em>
     <code>
      bit
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o primeiro índice de início do especificado
     <em class="parameter">
      <code>
       substring
      </code>
     </em>
     dentro
     <em class="parameter">
      <code>
       bits
      </code>
     </em>
     , ou zero se não estiver presente.
    </p>
    <p>
     <code>
      position(B'010' in B'000001101011')
     </code>
     →
     <code>
      8
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      substring
     </code>
     (
     <em class="parameter">
      <code>
       bits
      </code>
     </em>
     <code>
      bit
     </code>
     [
     <span class="optional">
      <code>
       FROM
      </code>
      <em class="parameter">
       <code>
        start
       </code>
      </em>
      <code>
       integer
      </code>
     </span>
     ] [
     <span class="optional">
      <code>
       FOR
      </code>
      <em class="parameter">
       <code>
        count
       </code>
      </em>
      <code>
       integer
      </code>
     </span>
     ] )
     <code>
      bit
     </code>
    </p>
    <p>
     Extrai a subcadeia de
     <em class="parameter">
      <code>
       bits
      </code>
     </em>
     a partir do
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     'se isso for especificado, e parar após
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     bits, se isso for especificado. Forneça pelo menos um
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     e
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      substring(B'110010111111' from 3 for 2)
     </code>
     →
     <code>
      00
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      get_bit
     </code>
     (
     <em class="parameter">
      <code>
       bits
      </code>
     </em>
     <code>
      bit
     </code>
     ,
     <em class="parameter">
      <code>
       n
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
     Extractos
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     'bit a bit; o primeiro bit (o mais à esquerda) é o bit 0.
    </p>
    <p>
     <code>
      get_bit(B'101010101010101010', 6)
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
      set_bit
     </code>
     (
     <em class="parameter">
      <code>
       bits
      </code>
     </em>
     <code>
      bit
     </code>
     ,
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       newvalue
      </code>
     </em>
     <code>
      integer
     </code>
     )
     <code>
      bit
     </code>
    </p>
    <p>
     Conjunto
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     'bit a bit na sequência de caracteres
     <em class="parameter">
      <code>
       newvalue
      </code>
     </em>
     ; o primeiro bit (o mais à esquerda) é o bit 0.
    </p>
    <p>
     <code>
      set_bit(B'101010101010101010', 6, 0)
     </code>
     →
     <code>
      101010001010101010
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>

Além disso, é possível converter valores inteiros para e a partir do tipo `bit`. A conversão de um inteiro para `bit(n)` copia os bits mais à direita do `n`. A conversão de um inteiro para uma string de bits com largura maior que o próprio inteiro fará extensão de sinal à esquerda. Alguns exemplos:

```sql
44::bit(10)                    0000101100
44::bit(3)                     100
cast(-44 as bit(12))           111111010100
'1110'::bit(4)::integer        14
```

Observe que a conversão para apenas “bit” significa conversão para `bit(1)`, e, portanto, fornecerá apenas o bit menos significativo do inteiro.