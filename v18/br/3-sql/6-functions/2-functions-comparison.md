## 9.2. Funções e operadores de comparação [#](#FUNCTIONS-COMPARISON)

Os operadores de comparação comuns estão disponíveis, conforme mostrado na [Tabela 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE).

**Tabela 9.1. Operadores de comparação**



<table border="1" class="table" summary="Comparison Operators">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Operador
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <em class="replaceable">
     <code>
      datatype
     </code>
    </em>
    <code class="literal">
     &lt;
    </code>
    <em class="replaceable">
     <code>
      datatype
     </code>
    </em>
    →
    <code class="returnvalue">
     boolean
    </code>
   </td>
   <td>
    Menos de
   </td>
  </tr>
  <tr>
   <td>
    <em class="replaceable">
     <code>
      datatype
     </code>
    </em>
    <code class="literal">
     &gt;
    </code>
    <em class="replaceable">
     <code>
      datatype
     </code>
    </em>
    →
    <code class="returnvalue">
     boolean
    </code>
   </td>
   <td>
    Superior a
   </td>
  </tr>
  <tr>
   <td>
    <em class="replaceable">
     <code>
      datatype
     </code>
    </em>
    <code class="literal">
     &lt;=
    </code>
    <em class="replaceable">
     <code>
      datatype
     </code>
    </em>
    →
    <code class="returnvalue">
     boolean
    </code>
   </td>
   <td>
    Menos ou igual a
   </td>
  </tr>
  <tr>
   <td>
    <em class="replaceable">
     <code>
      datatype
     </code>
    </em>
    <code class="literal">
     &gt;=
    </code>
    <em class="replaceable">
     <code>
      datatype
     </code>
    </em>
    →
    <code class="returnvalue">
     boolean
    </code>
   </td>
   <td>
    Maior que ou igual a
   </td>
  </tr>
  <tr>
   <td>
    <em class="replaceable">
     <code>
      datatype
     </code>
    </em>
    <code class="literal">
     =
    </code>
    <em class="replaceable">
     <code>
      datatype
     </code>
    </em>
    →
    <code class="returnvalue">
     boolean
    </code>
   </td>
   <td>
    Igual
   </td>
  </tr>
  <tr>
   <td>
    <em class="replaceable">
     <code>
      datatype
     </code>
    </em>
    <code class="literal">
     &lt;&gt;
    </code>
    <em class="replaceable">
     <code>
      datatype
     </code>
    </em>
    →
    <code class="returnvalue">
     boolean
    </code>
   </td>
   <td>
    Não igual
   </td>
  </tr>
  <tr>
   <td>
    <em class="replaceable">
     <code>
      datatype
     </code>
    </em>
    <code class="literal">
     !=
    </code>
    <em class="replaceable">
     <code>
      datatype
     </code>
    </em>
    →
    <code class="returnvalue">
     boolean
    </code>
   </td>
   <td>
    Não igual
   </td>
  </tr>
 </tbody>
</table>










Nota

`<>` é a notação SQL padrão para “não igual”. `!=` é um alias, que é convertido para `<>` em uma fase muito inicial do parsing. Portanto, não é possível implementar os operadores `!=` e `<>` que fazem coisas diferentes.

Esses operadores de comparação estão disponíveis para todos os tipos de dados integrados que têm uma ordem natural, incluindo tipos numéricos, de string e de data/hora. Além disso, matrizes, tipos compostos e intervalos podem ser comparados se seus tipos de dados componentes forem comparáveis.

Geralmente é possível comparar valores de tipos de dados relacionados também; por exemplo, `integer` `>` `bigint` funcionarão. Alguns casos desse tipo são implementados diretamente por operadores de comparação "cruzamento de tipos", mas se nenhum operador desse tipo estiver disponível, o analisador fará com que o tipo menos geral seja convertido para o tipo mais geral e aplicará o operador de comparação deste último.

Como mostrado acima, todos os operadores de comparação são operadores binários que retornam valores do tipo `boolean`. Assim, expressões como `1 < 2 < 3` não são válidas (porque não há um operador `<` para comparar um valor booleano com `3`). Use as preditivas `BETWEEN` mostradas abaixo para realizar testes de intervalo.

Existem também alguns predicados de comparação, conforme mostrado na [Tabela 9.2](functions-comparison.md#FUNCTIONS-COMPARISON-PRED-TABLE). Esses se comportam de maneira muito semelhante aos operadores, mas têm uma sintaxe especial exigida pelo padrão SQL.

**Tabela 9.2. Predicados de comparação**



<table border="1" class="table" summary="Comparison Predicates">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Predicado
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
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     <code class="literal">
      BETWEEN
     </code>
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     <code class="literal">
      AND
     </code>
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Entre (incluindo os pontos finais da faixa).
    </p>
    <p>
     <code class="literal">
      2 BETWEEN 1 AND 3
     </code>
     →
     <code class="returnvalue">
      t
     </code>
    </p>
    <p>
     <code class="literal">
      2 BETWEEN 3 AND 1
     </code>
     →
     <code class="returnvalue">
      f
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     <code class="literal">
      NOT BETWEEN
     </code>
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     <code class="literal">
      AND
     </code>
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Não entre (a negação de
     <code class="literal">
      BETWEEN
     </code>
     ).
    </p>
    <p>
     <code class="literal">
      2 NOT BETWEEN 1 AND 3
     </code>
     →
     <code class="returnvalue">
      f
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     <code class="literal">
      BETWEEN SYMMETRIC
     </code>
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     <code class="literal">
      AND
     </code>
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Entre, após a classificação dos dois valores de extremidade.
    </p>
    <p>
     <code class="literal">
      2 BETWEEN SYMMETRIC 3 AND 1
     </code>
     →
     <code class="returnvalue">
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
       datatype
      </code>
     </em>
     <code class="literal">
      NOT BETWEEN SYMMETRIC
     </code>
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     <code class="literal">
      AND
     </code>
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Não entre, após a classificação dos dois valores de extremidade.
    </p>
    <p>
     <code class="literal">
      2 NOT BETWEEN SYMMETRIC 3 AND 1
     </code>
     →
     <code class="returnvalue">
      f
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     <code class="literal">
      IS DISTINCT FROM
     </code>
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Não é igual, tratando o nulo como um valor comparável.
    </p>
    <p>
     <code class="literal">
      1 IS DISTINCT FROM NULL
     </code>
     →
     <code class="returnvalue">
      t
     </code>
     (em vez de
     <code class="literal">
      NULL
     </code>
     )
    </p>
    <p>
     <code class="literal">
      NULL IS DISTINCT FROM NULL
     </code>
     →
     <code class="returnvalue">
      f
     </code>
     (em vez de
     <code class="literal">
      NULL
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     <code class="literal">
      IS NOT DISTINCT FROM
     </code>
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Igual, tratando o nulo como um valor comparável.
    </p>
    <p>
     <code class="literal">
      1 IS NOT DISTINCT FROM NULL
     </code>
     →
     <code class="returnvalue">
      f
     </code>
     (em vez de
     <code class="literal">
      NULL
     </code>
     )
    </p>
    <p>
     <code class="literal">
      NULL IS NOT DISTINCT FROM NULL
     </code>
     →
     <code class="returnvalue">
      t
     </code>
     (em vez de
     <code class="literal">
      NULL
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     <code class="literal">
      IS NULL
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Teste se o valor é nulo.
    </p>
    <p>
     <code class="literal">
      1.5 IS NULL
     </code>
     →
     <code class="returnvalue">
      f
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     <code class="literal">
      IS NOT NULL
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Teste se o valor não é nulo.
    </p>
    <p>
     <code class="literal">
      'null' IS NOT NULL
     </code>
     →
     <code class="returnvalue">
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
       datatype
      </code>
     </em>
     <code class="literal">
      ISNULL
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Teste se o valor é nulo (sintaxe não padrão).
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       datatype
      </code>
     </em>
     <code class="literal">
      NOTNULL
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Teste se o valor não é nulo (sintaxe não padrão).
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      boolean
     </code>
     <code class="literal">
      IS TRUE
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Teste se a expressão booleana produz verdadeiro.
    </p>
    <p>
     <code class="literal">
      true IS TRUE
     </code>
     →
     <code class="returnvalue">
      t
     </code>
    </p>
    <p>
     <code class="literal">
      NULL::boolean IS TRUE
     </code>
     →
     <code class="returnvalue">
      f
     </code>
     (em vez de
     <code class="literal">
      NULL
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      boolean
     </code>
     <code class="literal">
      IS NOT TRUE
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Teste se a expressão booleana gera falso ou desconhecido.
    </p>
    <p>
     <code class="literal">
      true IS NOT TRUE
     </code>
     →
     <code class="returnvalue">
      f
     </code>
    </p>
    <p>
     <code class="literal">
      NULL::boolean IS NOT TRUE
     </code>
     →
     <code class="returnvalue">
      t
     </code>
     (em vez de
     <code class="literal">
      NULL
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      boolean
     </code>
     <code class="literal">
      IS FALSE
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Teste se a expressão booleana gera um valor falso.
    </p>
    <p>
     <code class="literal">
      true IS FALSE
     </code>
     →
     <code class="returnvalue">
      f
     </code>
    </p>
    <p>
     <code class="literal">
      NULL::boolean IS FALSE
     </code>
     →
     <code class="returnvalue">
      f
     </code>
     (em vez de
     <code class="literal">
      NULL
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      boolean
     </code>
     <code class="literal">
      IS NOT FALSE
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Teste se a expressão booleana produz verdadeiro ou desconhecido.
    </p>
    <p>
     <code class="literal">
      true IS NOT FALSE
     </code>
     →
     <code class="returnvalue">
      t
     </code>
    </p>
    <p>
     <code class="literal">
      NULL::boolean IS NOT FALSE
     </code>
     →
     <code class="returnvalue">
      t
     </code>
     (em vez de
     <code class="literal">
      NULL
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      boolean
     </code>
     <code class="literal">
      IS UNKNOWN
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Teste se a expressão booleana gera desconhecido.
    </p>
    <p>
     <code class="literal">
      true IS UNKNOWN
     </code>
     →
     <code class="returnvalue">
      f
     </code>
    </p>
    <p>
     <code class="literal">
      NULL::boolean IS UNKNOWN
     </code>
     →
     <code class="returnvalue">
      t
     </code>
     (em vez de
     <code class="literal">
      NULL
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      boolean
     </code>
     <code class="literal">
      IS NOT UNKNOWN
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Teste se a expressão booleana produz verdadeiro ou falso.
    </p>
    <p>
     <code class="literal">
      true IS NOT UNKNOWN
     </code>
     →
     <code class="returnvalue">
      t
     </code>
    </p>
    <p>
     <code class="literal">
      NULL::boolean IS NOT UNKNOWN
     </code>
     →
     <code class="returnvalue">
      f
     </code>
     (em vez de
     <code class="literal">
      NULL
     </code>
     )
    </p>
   </td>
  </tr>
 </tbody>
</table>










O predicado `BETWEEN` simplifica os testes de intervalo:

```
a BETWEEN x AND y
```

é equivalente a

```
a >= x AND a <= y
```

Observe que `BETWEEN` trata os valores do ponto final como incluídos no intervalo. `BETWEEN SYMMETRIC` é como `BETWEEN`, exceto que não há exigência de que o argumento à esquerda de `AND` seja menor ou igual ao argumento à direita. Se não for, esses dois argumentos são automaticamente trocados, de modo que um intervalo não vazio é sempre implícito.

As várias variantes de `BETWEEN` são implementadas em termos dos operadores de comparação ordinários, e, portanto, funcionarão para qualquer tipo de dados que possa ser comparado.

Nota

O uso de `AND` na sintaxe de `BETWEEN` cria uma ambiguidade com o uso de `AND` como operador lógico. Para resolver isso, apenas um conjunto limitado de tipos de expressão são permitidos como o segundo argumento de uma cláusula de `BETWEEN`. Se você precisar escrever uma subexpressão mais complexa em `BETWEEN`, escreva parênteses ao redor da subexpressão.

Os operadores de comparação comuns retornam nulo (indicando “desconhecido”), não verdadeiro ou falso, quando qualquer um dos inputs é nulo. Por exemplo, `7 = NULL` retorna nulo, assim como `7 <> NULL`. Quando esse comportamento não é adequado, use os predicados `IS [ NOT ] DISTINCT FROM`:

```
a IS DISTINCT FROM b
a IS NOT DISTINCT FROM b
```

Para entradas não nulos, `IS DISTINCT FROM` é o mesmo que o operador `<>`. No entanto, se ambas as entradas forem nulos, ele retorna false, e se apenas uma entrada for nula, ele retorna true. Da mesma forma, `IS NOT DISTINCT FROM` é idêntico a `=` para entradas não nulos, mas ele retorna true quando ambas as entradas forem nulos, e false quando apenas uma entrada for nula. Assim, esses predicados atuam efetivamente como se nulo fosse um valor de dados normal, em vez de “desconhecido”.

Para verificar se um valor é nulo ou não, use os predicados:

```
expression IS NULL
expression IS NOT NULL
```

ou predicados equivalentes, mas não padronizados:

```
expression ISNULL
expression NOTNULL
```

Não escreva `expression = NULL` porque `NULL` não é “igual a” `NULL`. (O valor nulo representa um valor desconhecido, e não se sabe se dois valores desconhecidos são iguais.)

DICA

Algumas aplicações podem esperar que `expression = NULL` retorne verdadeiro se *`expression`* avalia o valor nulo. É altamente recomendável que essas aplicações sejam modificadas para atender ao padrão SQL. No entanto, se isso não puder ser feito, a variável de configuração [transform_null_equals](runtime-config-compatible.md#GUC-TRANSFORM-NULL-EQUALS) está disponível. Se estiver habilitada, o PostgreSQL converterá as cláusulas `x = NULL` para `x IS NULL`.

Se o *`expression`* for de valor de linha, então `IS NULL` é verdadeiro quando a própria expressão de linha é nula ou quando todos os campos da linha são nulos, enquanto `IS NOT NULL` é verdadeiro quando a própria expressão de linha não é nula e todos os campos da linha não são nulos. Devido a esse comportamento, `IS NULL` e `IS NOT NULL` nem sempre retornam resultados inversos para expressões de valor de linha; em particular, uma expressão de valor de linha que contém campos tanto nulos quanto não nulos retornará falso para ambos os testes. Por exemplo:

```
SELECT ROW(1,2.5,'this is a test') = ROW(1, 3, 'not the same');

SELECT ROW(table.*) IS NULL FROM table;  -- detect all-null rows

SELECT ROW(table.*) IS NOT NULL FROM table;  -- detect all-non-null rows

SELECT NOT(ROW(table.*) IS NOT NULL) FROM TABLE; -- detect at least one null in rows
```

Em alguns casos, pode ser preferível escrever *`row`* `IS DISTINCT FROM NULL` ou *`row`* `IS NOT DISTINCT FROM NULL`, que simplesmente verificará se o valor geral da linha é nulo, sem quaisquer testes adicionais nos campos da linha.

Os valores lógicos também podem ser testados usando os predicados

```
boolean_expression IS TRUE
boolean_expression IS NOT TRUE
boolean_expression IS FALSE
boolean_expression IS NOT FALSE
boolean_expression IS UNKNOWN
boolean_expression IS NOT UNKNOWN
```

Esses sempre retornarão verdadeiro ou falso, nunca um valor nulo, mesmo quando o operando é nulo. Uma entrada nulo é tratada como o valor lógico “desconhecido”. Observe que `IS UNKNOWN` e `IS NOT UNKNOWN` são efetivamente iguais a `IS NULL` e `IS NOT NULL`, respectivamente, exceto que a expressão de entrada deve ser do tipo Booleano.

Algumas funções relacionadas à comparação também estão disponíveis, conforme mostrado na [Tabela 9.3](functions-comparison.md#FUNCTIONS-COMPARISON-FUNC-TABLE).

**Tabela 9.3. Funções de comparação**



<table border="1" class="table" summary="Comparison Functions">
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
      num_nonnulls
     </code>
     (
     <code class="literal">
      VARIADIC
     </code>
     <code class="type">
      "any"
     </code>
     )
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Retorna o número de argumentos que não são nulos.
    </p>
    <p>
     <code class="literal">
      num_nonnulls(1, NULL, 2)
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
      num_nulls
     </code>
     (
     <code class="literal">
      VARIADIC
     </code>
     <code class="type">
      "any"
     </code>
     )
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Retorna o número de argumentos nulos.
    </p>
    <p>
     <code class="literal">
      num_nulls(1, NULL, 2)
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





