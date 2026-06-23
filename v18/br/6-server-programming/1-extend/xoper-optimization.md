## 36.15. Informações sobre otimização do operador [#](#XOPER-OPTIMIZATION)

* [36.15.1. `COMMUTATOR`](xoper-optimization.md#XOPER-COMMUTATOR)
* [36.15.2. `NEGATOR`](xoper-optimization.md#XOPER-NEGATOR)
* [36.15.3. `RESTRICT`](xoper-optimization.md#XOPER-RESTRICT)
* [36.15.4. `JOIN`](xoper-optimization.md#XOPER-JOIN)
* [36.15.5. `HASHES`](xoper-optimization.md#XOPER-HASHES)
* [36.15.6. `MERGES`](xoper-optimization.md#XOPER-MERGES)

Uma definição de operador do PostgreSQL pode incluir várias cláusulas opcionais que informam ao sistema coisas úteis sobre como o operador se comporta. Essas cláusulas devem ser fornecidas sempre que apropriado, porque elas podem resultar em consideráveis aprimoramentos na execução de consultas que utilizam o operador. Mas se você as fornecer, deve ter certeza de que elas estão corretas! O uso incorreto de uma cláusula de otimização pode resultar em consultas lentas, saída sutilmente errada ou outras Coisas ruins. Você sempre pode deixar de fora uma cláusula de otimização se não tiver certeza; a única consequência é que as consultas podem rodar mais lentamente do que precisam.

Cláusulas de otimização adicionais podem ser adicionadas em versões futuras do PostgreSQL. As descritas aqui são todas as que o lançamento 18.4 entende.

É também possível anexar uma função de suporte ao planejador à função que rege um operador, fornecendo outra maneira de informar ao sistema sobre o comportamento do operador. Consulte [Seção 36.11] para obter mais informações.

### 36.15.1. `COMMUTATOR` [#](#XOPER-COMMUTATOR)

A cláusula `COMMUTATOR`, se fornecida, nomeia um operador que é o commutador do operador que está sendo definido. Dizemos que o operador A é o commutador do operador B se (x A y) é igual a (y B x) para todos os possíveis valores de entrada x, y. Observe que B também é o commutador de A. Por exemplo, os operadores `<` e `>` para um tipo de dados específico geralmente são os commutadores um do outro, e o operador `+` geralmente é comutativo consigo mesmo. Mas o operador `-` geralmente não é comutativo com nada.

O tipo do operador de esquerda do operador comutável é o mesmo que o tipo do operador de direita de seu commutator, e vice-versa. Assim, o nome do operador commutator é tudo o que o PostgreSQL precisa ser dado para procurar o commutator, e isso é tudo o que precisa ser fornecido na cláusula `COMMUTATOR`.

É fundamental fornecer informações sobre commutator para operadores que serão usados em cláusulas de índice e junção, porque isso permite que o otimizador de consulta "inverte" tal cláusula para as formas necessárias para diferentes tipos de plano. Por exemplo, considere uma consulta com uma cláusula WHERE como `tab1.x = tab2.y`, onde `tab1.x` e `tab2.y` são de um tipo definido pelo usuário, e suponha que `tab2.y` esteja indexado. O otimizador não pode gerar uma varredura de índice a menos que possa determinar como inverter a cláusula para `tab2.y = tab1.x`, porque a máquina de varredura de índice espera ver a coluna indexada à esquerda do operador que lhe é dado. O PostgreSQL *não* assumirá simplesmente que essa é uma transformação válida — o criador do operador `=` deve especificar que é válida, marcando o operador com informações sobre commutator.

### 36.15.2. `NEGATOR` [#](#XOPER-NEGATOR)

A cláusula `NEGATOR`, se fornecida, nomeia um operador que é o negador do operador que está sendo definido. Dizemos que o operador A é o negador do operador B se ambos retornarem resultados booleanos e (x A y) seja igual a NOT (x B y) para todos os possíveis inputs x, y. Observe que B também é o negador de A. Por exemplo, `<` e `>=` são um par de negador para a maioria dos tipos de dados. Um operador nunca pode ser validamente seu próprio negador.

Ao contrário dos commutativos, um par de operadores unários poderia ser validamente marcado como negadores um do outro; isso significaria que (A x) é igual a NOT (B x) para todos os x.

O negador de um operador deve ter os mesmos tipos de operandos à esquerda e/ou à direita do operador que será definido, assim como no caso de `COMMUTATOR`, apenas o nome do operador precisa ser dado na cláusula `NEGATOR`.

Fornecer um negador é muito útil para o otimizador de consulta, pois permite que expressões como `NOT (x = y)` sejam simplificadas para `x <> y`. Isso acontece com mais frequência do que você pode imaginar, porque operações `NOT` podem ser inseridas como consequência de outros rearranjos.

### 36.15.3. `RESTRICT` [#](#XOPER-RESTRICT)

A cláusula `RESTRICT`, se fornecida, nomeia uma função de estimativa de seletividade de restrição para o operador. (Observe que esta é um nome de função, não um nome de operador.) As cláusulas `RESTRICT` só fazem sentido para operadores binários que retornam `boolean`. A ideia por trás de um estimulador de seletividade de restrição é adivinhar qual fração das linhas em uma tabela atenderá a uma condição de cláusula `WHERE` da forma:

```
column OP constant
```

para o operador atual e um valor constante específico. Isso auxilia o otimizador ao dar uma ideia de quantas linhas serão eliminadas por cláusulas `WHERE` que têm essa forma. (O que acontece se a constante estiver à esquerda, você pode estar se perguntando? Bem, essa é uma das coisas para as quais o `COMMUTATOR` é...)

Escrever novas funções de estimativa de seletividade de restrição vai muito além do escopo deste capítulo, mas, felizmente, você geralmente pode usar uma das estimativas padrão do sistema para muitos de seus próprios operadores. Estes são os estimativos padrão de restrição:



<table border="0" class="simplelist" summary="Simple list">
 <tr>
  <td>
   <code class="function">
    eqsel
   </code>
   para
   <code class="literal">
    =
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="function">
    neqsel
   </code>
   para
   <code class="literal">
    &lt;&gt;
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="function">
    scalarltsel
   </code>
   para
   <code class="literal">
    &lt;
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="function">
    scalarlesel
   </code>
   para
   <code class="literal">
    &lt;=
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="function">
    scalargtsel
   </code>
   para
   <code class="literal">
    &gt;
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="function">
    scalargesel
   </code>
   para
   <code class="literal">
    &gt;=
   </code>
  </td>
 </tr>
</table>







Você pode frequentemente se safar usando `eqsel` ou `neqsel` para operadores que têm seletividade muito alta ou muito baixa, mesmo que não sejam realmente igualdade ou desigualdade. Por exemplo, os operadores geométricos de aproximadamente igualdade usam `eqsel` na suposição de que eles geralmente corresponderão apenas a uma pequena fração das entradas em uma tabela.

Você pode usar `scalarltsel`, `scalarlesel`, `scalargtsel` e `scalargesel` para comparações em tipos de dados que têm meios sensíveis de serem convertidos em escalares numéricos para comparações de intervalo. Se possível, adicione o tipo de dados aos que são compreendidos pela função `convert_to_scalar()` em `src/backend/utils/adt/selfuncs.c`. (Eventualmente, essa função deve ser substituída por funções por tipo de dado identificadas através de uma coluna do catálogo do sistema `pg_type`; mas isso ainda não aconteceu.) Se você não fizer isso, as coisas ainda funcionarão, mas as estimativas do otimizador não serão tão boas quanto poderiam ser.

Outra função de estimação de seletividade integrada útil é `matchingsel`, que funcionará para quase qualquer operador binário, se as estatísticas padrão de MCV e/ou histograma forem coletadas para o(s) tipo(s) de dados de entrada. Sua estimativa padrão é definida como o dobro da estimativa padrão usada em `eqsel`, tornando-a mais adequada para operadores de comparação que são um pouco menos rigorosos que a igualdade. (Ou você pode chamar a função subjacente `generic_restriction_selectivity`, fornecendo uma estimativa padrão diferente.)

Existem funções adicionais de estimativa de seletividade projetadas para operadores geométricos em `src/backend/utils/adt/geo_selfuncs.c`: `areasel`, `positionsel` e `contsel`. Neste momento, essas são apenas esboços, mas você pode querer usá-las (ou melhor ainda, melhorá-las) de qualquer maneira.

### 36.15.4. `JOIN` [#](#XOPER-JOIN)

A cláusula `JOIN`, se fornecida, nomeia uma função de estimativa de seletividade de junção para o operador. (Observe que esta é um nome de função, não um nome de operador.) As cláusulas `JOIN` só fazem sentido para operadores binários que retornam `boolean`. A ideia por trás de um estimulador de seletividade de junção é adivinhar qual fração das linhas em um par de tabelas atenderá a uma condição de cláusula `WHERE` da forma:

```
table1.column1 OP table2.column2
```

para o operador atual. Assim como a cláusula `RESTRICT`, isso ajuda o otimizador de forma muito substancial, permitindo que ele descubra qual das várias sequências de junção provavelmente exigirá o menor trabalho.

Como antes, este capítulo não fará nenhuma tentativa de explicar como escrever uma função de estimativa de seletividade de junção, mas apenas sugerirá que você use uma das estimativas padrão, se uma for aplicável:



<table border="0" class="simplelist" summary="Simple list">
 <tr>
  <td>
   <code class="function">
    eqjoinsel
   </code>
   para
   <code class="literal">
    =
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="function">
    neqjoinsel
   </code>
   para
   <code class="literal">
    &lt;&gt;
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="function">
    scalarltjoinsel
   </code>
   para
   <code class="literal">
    &lt;
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="function">
    scalarlejoinsel
   </code>
   para
   <code class="literal">
    &lt;=
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="function">
    scalargtjoinsel
   </code>
   para
   <code class="literal">
    &gt;
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="function">
    scalargejoinsel
   </code>
   para
   <code class="literal">
    &gt;=
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="function">
    matchingjoinsel
   </code>
   para operadores de correspondência genéricos
  </td>
 </tr>
 <tr>
  <td>
   <code class="function">
    areajoinsel
   </code>
   para comparações baseadas em áreas 2D
  </td>
 </tr>
 <tr>
  <td>
   <code class="function">
    positionjoinsel
   </code>
   para comparações baseadas na posição 2D
  </td>
 </tr>
 <tr>
  <td>
   <code class="function">
    contjoinsel
   </code>
   para comparações com base em contenção 2D
  </td>
 </tr>
</table>







### 36.15.5. `HASHES` [#](#XOPER-HASHES)

A cláusula `HASHES`, se presente, informa ao sistema que é permitido usar o método de junção de hash para uma junção com base neste operador. `HASHES` só faz sentido para um operador binário que retorna `boolean`, e, na prática, o operador deve representar igualdade para algum tipo de dados ou par de tipos de dados.

A suposição subjacente à junção hash é que o operador de junção só pode retornar verdadeiro para pares de valores à esquerda e à direita que hash para o mesmo código de hash. Se dois valores forem colocados em diferentes buckets de hash, a junção nunca os comparará, assumindo implicitamente que o resultado do operador de junção deve ser falso. Portanto, não faz sentido especificar `HASHES` para operadores que não representam alguma forma de igualdade. Na maioria dos casos, é prático apenas suportar a hashing para operadores que tomam o mesmo tipo de dados em ambos os lados. No entanto, às vezes é possível projetar funções de hash compatíveis para dois ou mais tipos de dados; ou seja, funções que gerarão os mesmos códigos de hash para valores "iguais", mesmo que os valores tenham representações diferentes. Por exemplo, é bastante simples organizar essa propriedade ao hashar inteiros de diferentes larguras.

Para ser marcado `HASHES`, o operador de junção deve aparecer em uma família de operadores de índice de hash. Isso não é exigido ao criar o operador, uma vez que, claro, a família de operadores de referência ainda não poderia existir. Mas as tentativas de usar o operador em junções de hash falharão no tempo de execução se não houver tal família de operadores. O sistema precisa da família de operadores para encontrar as funções de hash específicas para o tipo de dados do(s) tipo(s) de dados de entrada do operador. Claro, você também deve criar funções de hash adequadas antes de poder criar a família de operadores.

É necessário ter cuidado ao preparar uma função hash, porque existem maneiras dependentes da máquina em que ela pode falhar em fazer a coisa certa. Por exemplo, se o seu tipo de dados é uma estrutura na qual pode haver bits de preenchimento desinteressantes, você não pode simplesmente passar toda a estrutura para `hash_any`. (A menos que você escreva seus outros operadores e funções para garantir que os bits não utilizados sejam sempre zero, que é a estratégia recomendada.) Outro exemplo é que em máquinas que atendem ao padrão de ponto flutuante IEEE, zero negativo e zero positivo são valores diferentes (padrões de bits diferentes), mas são definidos para serem comparados como iguais. Se um valor de float pode conter zero negativo, então são necessários passos extras para garantir que ele gere o mesmo valor de hash que o zero positivo.

Um operador que pode ser associado a hash deve ter um commutator (ele mesmo se os dois tipos de dados dos operandos forem os mesmos, ou um operador de igualdade relacionado se forem diferentes) que apareça na mesma família de operadores. Se este não for o caso, podem ocorrer erros no planejador quando o operador é usado. Além disso, é uma boa ideia (mas não é estritamente necessária) para uma família de operadores de hash que suporta vários tipos de dados fornecer operadores de igualdade para cada combinação dos tipos de dados; isso permite uma melhor otimização.

Nota

A função subjacente a um operador que pode ser associado por junção de hash deve ser marcada como imutável ou estável. Se for volátil, o sistema nunca tentará usar o operador para uma junção de hash.

Nota

Se um operador que pode ser associado por hash tiver uma função subjacente marcada como estrita, a função também deve ser completa: ou seja, deve retornar verdadeiro ou falso, nunca nulo, para quaisquer dois inputs não nulos. Se essa regra não for seguida, a otimização de `IN` das operações pode gerar resultados errados. (Especificamente, `IN` pode retornar falso onde a resposta correta, de acordo com o padrão, seria nulo; ou pode gerar um erro que reclama que não foi preparado para um resultado nulo.)

### 36.15.6. `MERGES` [#](#XOPER-MERGES)

A cláusula `MERGES`, se presente, informa ao sistema que é permitido usar o método de junção por fusão para uma junção baseada neste operador. `MERGES` só faz sentido para um operador binário que retorna `boolean`, e, na prática, o operador deve representar igualdade para algum tipo de dados ou par de tipos de dados.

A junção por correspondência é baseada na ideia de ordenar as tabelas da esquerda e da direita e, em seguida, digitalizar-as em paralelo. Portanto, ambos os tipos de dados devem ser capazes de ser totalmente ordenados, e o operador de junção deve ser aquele que só pode ter sucesso para pares de valores que caem no "mesmo lugar" na ordem de classificação. Na prática, isso significa que o operador de junção deve se comportar como igualdade. No entanto, é possível realizar uma junção por correspondência entre dois tipos de dados distintos, desde que eles sejam logicamente compatíveis. Por exemplo, o operador de igualdade `smallint`-versus-`integer` é compatível com junção. Só precisamos de operadores de classificação que levem ambos os tipos de dados a uma sequência logicamente compatível.

Para ser marcado `MERGES`, o operador de junção deve aparecer como membro de igualdade de uma família de operadores de índice `btree`. Isso não é exigido ao criar o operador, uma vez que, claro, a família de operadores de referência ainda não poderia existir. Mas o operador não será realmente usado para junções de fusão, a menos que uma família de operadores correspondente possa ser encontrada. A bandeira `MERGES`, portanto, atua como um aviso ao planejador de que vale a pena procurar uma família de operadores correspondente.

Um operador que pode ser fundido e unido deve ter um commutator (ele mesmo se os dois tipos de dados dos operandos forem os mesmos, ou um operador de igualdade relacionado se forem diferentes) que apareça na mesma família de operadores. Se este não for o caso, podem ocorrer erros no planejador quando o operador é usado. Além disso, é uma boa ideia (mas não é estritamente necessária) para uma família de operadores `btree` que suporta vários tipos de dados fornecer operadores de igualdade para cada combinação dos tipos de dados; isso permite uma melhor otimização.

Nota

A função subjacente a um operador que pode ser fundido e unido deve ser marcada como imutável ou estável. Se for volátil, o sistema nunca tentará usar o operador para uma junção de fusão.