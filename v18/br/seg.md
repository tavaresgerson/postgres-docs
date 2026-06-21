## F.39. seg — um tipo de dado para segmentos de linha ou intervalos de ponto flutuante [#](#SEG)

* [F.39.1. Razão](seg.md#SEG-RATIONALE)
* [F.39.2. Sintaxe](seg.md#SEG-SYNTAX)
* [F.39.3. Precisão](seg.md#SEG-PRECISION)
* [F.39.4. Uso](seg.md#SEG-USAGE)
* [F.39.5. Notas](seg.md#SEG-NOTES)
* [F.39.6. Créditos](seg.md#SEG-CREDITS)

Este módulo implementa um tipo de dados `seg` para representar segmentos de linha ou intervalos de ponto flutuante. `seg` pode representar a incerteza nos pontos finais do intervalo, tornando-o especialmente útil para representar medições laboratoriais.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.39.1. **Razão [#](#SEG-RATIONALE)

A geometria das medições geralmente é mais complexa do que a de um ponto em um contínuo numérico. Uma medição geralmente é um segmento desse contínuo com limites um tanto borrosos. As medições aparecem como intervalos devido à incerteza e à aleatoriedade, além do fato de que o valor que está sendo medido pode ser naturalmente um intervalo que indica alguma condição, como a faixa de temperatura de estabilidade de uma proteína.

Usando apenas o senso comum, parece mais conveniente armazenar esses dados como intervalos, em vez de pares de números. Na prática, até mesmo se revela mais eficiente na maioria das aplicações.

Seguindo a linha do senso comum, a nebulosidade dos limites sugere que o uso de tipos de dados numéricos tradicionais leva a uma certa perda de informação. Considere isso: seu instrumento lê 6,50, e você insere essa leitura no banco de dados. O que você obtém ao recuperá-la? Assista:

```
test=> select 6.50 :: float8 as "pH";
 pH
---
6.5
(1 row)
```

No mundo das medições, 6,50 não é o mesmo que 6,5. Às vezes, pode ser criticamente diferente. Os experimentadores geralmente registram (e publicam) os dígitos em que confiam. 6,50 é, na verdade, um intervalo borrado contido dentro de um intervalo maior e ainda mais borrado, 6,5, com seus pontos centrais sendo (provavelmente) a única característica comum que compartilham. Definitivamente, não queremos que itens de dados tão diferentes pareçam os mesmos.

Conclusão? É bom ter um tipo de dados especial que possa registrar os limites de um intervalo com precisão arbitrariamente variável. Variável no sentido de que cada elemento de dados registra sua própria precisão.

Confira isso:

```
test=> select '6.25 .. 6.50'::seg as "pH";
          pH
------------
6.25 .. 6.50
(1 row)
```

### F.39.2. Sintaxe [#](#SEG-SYNTAX)

A representação externa de um intervalo é formada usando um ou dois números de ponto flutuante unidos pelo operador de intervalo (`..` ou `...`). Alternativamente, pode ser especificado como um ponto central mais ou menos com uma desvio. Indicadores de certeza opcionais (`<`, `>` ou `~`) também podem ser armazenados. (Os indicadores de certeza são ignorados por todos os operadores internos, no entanto.) [Tabela F.29](seg.md#SEG-REPR-TABLE "Table F.29. seg External Representations") fornece uma visão geral das representações permitidas; [Tabela F.30](seg.md#SEG-INPUT-EXAMPLES "Table F.30. Examples of Valid seg Input") mostra alguns exemplos.

Em [Tabela F.29](seg.md#SEG-REPR-TABLE), *`x`*, *`y`* e *`delta`* denotam números em ponto flutuante. *`x`* e *`y`*, mas não *`delta`*, podem ser precedidos por um indicador de certeza.

**Tabela F.29. `seg` Representações Externas**



<table border="1" class="table" summary="seg External Representations">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    Valor único (intervalo de comprimento zero)
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
     ..
     <em class="replaceable">
      <code>
       y
      </code>
     </em>
    </code>
   </td>
   <td>
    Intervalo de
    <em class="replaceable">
     <code>
      x
     </code>
    </em>
    para
    <em class="replaceable">
     <code>
      y
     </code>
    </em>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
     (+-)
     <em class="replaceable">
      <code>
       delta
      </code>
     </em>
    </code>
   </td>
   <td>
    Intervalo de
    <em class="replaceable">
     <code>
      x
     </code>
    </em>
    -
    <em class="replaceable">
     <code>
      delta
     </code>
    </em>
    para
    <em class="replaceable">
     <code>
      x
     </code>
    </em>
    +
    <em class="replaceable">
     <code>
      delta
     </code>
    </em>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
     ..
    </code>
   </td>
   <td>
    Intervalo aberto com limite inferior
    <em class="replaceable">
     <code>
      x
     </code>
    </em>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ..
     <em class="replaceable">
      <code>
       x
      </code>
     </em>
    </code>
   </td>
   <td>
    Intervalo aberto com limite superior
    <em class="replaceable">
     <code>
      x
     </code>
    </em>
   </td>
  </tr>
 </tbody>
</table>









**Tabela F.30. Exemplos de entrada válida do `seg`**



<table border="1" class="table" summary="Examples of Valid seg Input">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     5.0
    </code>
   </td>
   <td>
    Cria um segmento de comprimento zero (um ponto, se quiser)
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ~5.0
    </code>
   </td>
   <td>
    Cria um segmento de comprimento zero e registra
    <code class="literal">
     ~
    </code>
    nos dados.
    <code class="literal">
     ~
    </code>
    é ignorado por
    <code class="type">
     seg
    </code>
    operações, mas é preservado como um comentário.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;5.0
    </code>
   </td>
   <td>
    Cria um ponto em 5,0.
    <code class="literal">
     &lt;
    </code>
    é ignorado, mas é preservado como um comentário.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;5.0
    </code>
   </td>
   <td>
    Cria um ponto em 5,0.
    <code class="literal">
     &gt;
    </code>
    é ignorado, mas é preservado como um comentário.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     5(+-)0.3
    </code>
   </td>
   <td>
    Cria um intervalo
    <code class="literal">
     4.7 .. 5.3
    </code>
    . Observe que o
    <code class="literal">
     (+-)
    </code>
    a notação não é preservada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     50 ..
    </code>
   </td>
   <td>
    Tudo o que é maior ou igual a 50
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     .. 0
    </code>
   </td>
   <td>
    Tudo o que é menor ou igual a 0
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     1.5e-2 .. 2E-2
    </code>
   </td>
   <td>
    Cria um intervalo
    <code class="literal">
     0.015 .. 0.02
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     1 ... 2
    </code>
   </td>
   <td>
    O mesmo que
    <code class="literal">
     1...2
    </code>
    , ou
    <code class="literal">
     1 .. 2
    </code>
    , ou
    <code class="literal">
     1..2
    </code>
    (espaços ao redor do operador de intervalo são ignorados)
   </td>
  </tr>
 </tbody>
</table>









Como o operador `...` é amplamente utilizado em fontes de dados, ele é permitido como uma ortografia alternativa do operador `..`. Infelizmente, isso cria uma ambiguidade de análise: não está claro se o limite superior em `0...23` deve ser `23` ou `0.23`. Isso é resolvido exigindo pelo menos um dígito antes do ponto decimal em todos os números na entrada `seg`.

Como uma verificação de sanidade, `seg` rejeita intervalos com a menor extremidade maior que a maior, por exemplo, `5 .. 2`.

### F.39.3. Precisão [#](#SEG-PRECISION)

Os valores de `seg` são armazenados internamente como pares de números em ponto flutuante de 32 bits. Isso significa que os números com mais de 7 dígitos significativos serão truncados.

Os números com 7 dígitos significativos ou menos retêm sua precisão original. Ou seja, se sua consulta retornar 0,00, você terá certeza de que as zeros finais não são artefatos de formatação: eles refletem a precisão dos dados originais. O número de zeros anteriores não afeta a precisão: o valor 0,0067 é considerado ter apenas 2 dígitos significativos.

### F.39.4. Uso [#](#SEG-USAGE)

O módulo `seg` inclui uma classe de operador de índice GiST para valores de `seg`. Os operadores suportados pela classe de operador GiST são mostrados na [Tabela F.31](seg.md#SEG-GIST-OPERATORS).

**Tabela F.31. Operadores GiST Seg**



<table border="1" class="table" summary="Seg GiST Operators">
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
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      seg
     </code>
     <code class="literal">
      &lt;&lt;
     </code>
     <code class="type">
      seg
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     É o primeiro
     <code class="type">
      seg
     </code>
     completamente à esquerda da segunda? [a, b] &lt;&lt; [c, d] é verdadeiro se b &lt; c.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      seg
     </code>
     <code class="literal">
      &gt;&gt;
     </code>
     <code class="type">
      seg
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     É o primeiro
     <code class="type">
      seg
     </code>
     completamente à direita da segunda? [a, b] &gt;&gt; [c, d] é verdadeiro se a &gt; d.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      seg
     </code>
     <code class="literal">
      &amp;&lt;
     </code>
     <code class="type">
      seg
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     O primeiro
     <code class="type">
      seg
     </code>
     Não se estende ao direito do segundo? [a, b] &amp;&lt; [c, d] é verdadeiro se b &lt;= d.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      seg
     </code>
     <code class="literal">
      &amp;&gt;
     </code>
     <code class="type">
      seg
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     O primeiro
     <code class="type">
      seg
     </code>
     não se estenda à esquerda da segunda? [a, b] &amp;&gt; [c, d] é verdadeiro se a &gt;= c.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      seg
     </code>
     <code class="literal">
      =
     </code>
     <code class="type">
      seg
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     São os dois
     <code class="type">
      seg
     </code>
     são iguais?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      seg
     </code>
     <code class="literal">
      &amp;&amp;
     </code>
     <code class="type">
      seg
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Os dois
     <code class="type">
      seg
     </code>
     sobreposição?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      seg
     </code>
     <code class="literal">
      @&gt;
     </code>
     <code class="type">
      seg
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     O primeiro
     <code class="type">
      seg
     </code>
     contêm o segundo?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      seg
     </code>
     <code class="literal">
      &lt;@
     </code>
     <code class="type">
      seg
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     É o primeiro
     <code class="type">
      seg
     </code>
     contido no segundo?
    </p>
   </td>
  </tr>
 </tbody>
</table>









Além dos operadores de comparação acima, os operadores de comparação comuns mostrados em [Tabela 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) estão disponíveis para o tipo `seg`. Esses operadores primeiro comparam (a) com (c), e se esses forem iguais, comparam (b) com (d). Isso resulta em uma classificação razoavelmente boa na maioria dos casos, o que é útil se você quiser usar ORDER BY com esse tipo.

### F.39.5. Notas [#](#SEG-NOTES)

Para exemplos de uso, veja o teste de regressão `sql/seg.sql`.

O mecanismo que converte `(+-)` para faixas regulares não é completamente preciso ao determinar o número de dígitos significativos para os limites. Por exemplo, ele adiciona um dígito extra ao limite inferior se o intervalo resultante incluir uma potência de dez:

```
postgres=> select '10(+-)1'::seg as seg;
      seg
---------
9.0 .. 11             -- should be: 9 .. 11
```

O desempenho de um índice R-tree pode depender muito da ordem inicial dos valores de entrada. Pode ser muito útil ordenar a tabela de entrada na coluna `seg`; veja o script `sort-segments.pl` para um exemplo.

### F.39.6. Créditos [#](#SEG-CREDITS)

Autor original: Gene Selkov, Jr. `<selkovjr@mcs.anl.gov>`, Divisão de Matemática e Ciência da Computação, Laboratório Nacional Argonne.

Meu agradecimento é principalmente ao Prof. Joe Hellerstein (<https://dsf.berkeley.edu/jmh/>) por esclarecer o espírito do GiST (<http://gist.cs.berkeley.edu/>). Também estou grato a todos os desenvolvedores do Postgres, presentes e passados, por me permitir criar meu próprio mundo e viver nele sem interrupções. E gostaria de reconhecer minha gratidão ao Argonne Lab e ao Departamento de Energia dos EUA pelos anos de apoio fiel à minha pesquisa de banco de dados.