## 4.1. Estrutura lexical [#](#SQL-SYNTAX-LEXICAL)

* [4.1.1. Identificadores e Palavras-chave](sql-syntax-lexical.md#SQL-SYNTAX-IDENTIFIERS)
* [4.1.2. Constantes](sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS)
* [4.1.3. Operadores](sql-syntax-lexical.md#SQL-SYNTAX-OPERATORS)
* [4.1.4. Caracteres Especiais](sql-syntax-lexical.md#SQL-SYNTAX-SPECIAL-CHARS)
* [4.1.5. Comentários](sql-syntax-lexical.md#SQL-SYNTAX-COMMENTS)
* [4.1.6. Precedência do Operador](sql-syntax-lexical.md#SQL-PRECEDENCE)

A entrada SQL consiste em uma sequência de *comandos*. Um comando é composto por uma sequência de *tokens*, terminada por um ponto e vírgula (“;”). O fim do fluxo de entrada também termina um comando. Os tokens válidos dependem da sintaxe do comando específico.

Um token pode ser uma *palavra-chave*, um *identificador*, um *identificador citado*, um *literal* (ou constante) ou um símbolo de caractere especial. Os tokens são normalmente separados por espaços em branco (espaço, tabulação, nova linha), mas não precisam ser se não houver ambiguidade (o que geralmente é o caso apenas se um caractere especial estiver adjacente a algum outro tipo de token).

Por exemplo, o seguinte é uma entrada SQL (sintaticamente) válida:

```
SELECT * FROM MY_TABLE;
UPDATE MY_TABLE SET A = 5;
INSERT INTO MY_TABLE VALUES (3, 'hi there');
```

Esta é uma sequência de três comandos, um por linha (embora isso não seja necessário; mais de um comando pode estar em uma linha, e os comandos podem ser úteis divididos em várias linhas).

Além disso, os *comentários* podem ocorrer na entrada SQL. Eles não são tokens, eles são efetivamente equivalentes a espaços em branco.

A sintaxe SQL não é muito consistente em relação ao que os tokens identificam como comandos e quais são operadores ou parâmetros. Os primeiros tokens são geralmente o nome do comando, então, no exemplo acima, geralmente falamos em um comando de “SELECT”, “UPDATE” e “INSERT”. Mas, por exemplo, o comando `UPDATE` sempre requer que um token `SET` apareça em uma certa posição, e esta variação específica de `INSERT` também requer um `VALUES` para ser completa. As regras precisas de sintaxe para cada comando são descritas em [Parte VI](reference.md).

### 4.1.1. Identificadores e Palavras-Chave [#](#SQL-SYNTAX-IDENTIFIERS)

Títulos como `SELECT`, `UPDATE` ou `VALUES` no exemplo acima são exemplos de *palavras-chave*, ou seja, palavras que têm um significado fixo na linguagem SQL. Os títulos `MY_TABLE` e `A` são exemplos de *identificadores*. Eles identificam nomes de tabelas, colunas ou outros objetos de banco de dados, dependendo do comando em que são usados. Portanto, às vezes são simplesmente chamados de “nomes”. Palavras-chave e identificadores têm a mesma estrutura lexical, o que significa que não se pode saber se um título é um identificador ou uma palavra-chave sem conhecer a linguagem. Uma lista completa de palavras-chave pode ser encontrada em [Apêndice C](sql-keywords-appendix.md).

Os identificadores e palavras-chave do SQL devem começar com uma letra (`a`-`z`, mas também letras com acentos gráficos e letras não latinas) ou um underscore (`_`). Os caracteres subsequentes em um identificador ou palavra-chave podem ser letras, underscores, dígitos (`0`-`9`), ou sinais de dólar (`$`). Observe que os sinais de dólar não são permitidos em identificadores de acordo com a letra do padrão SQL, portanto, seu uso pode tornar as aplicações menos portáteis. O padrão SQL não definirá uma palavra-chave que contenha dígitos ou comece ou termine com um underscore, portanto, os identificadores dessa forma são seguros contra possíveis conflitos com futuras extensões do padrão.

O sistema não utiliza mais do que `NAMEDATALEN`-1 bytes de um identificador; nomes mais longos podem ser escritos em comandos, mas serão truncados. Por padrão, `NAMEDATALEN` é 64, então o comprimento máximo do identificador é de 63 bytes. Se esse limite for problemático, ele pode ser aumentado alterando a constante `NAMEDATALEN` em `src/include/pg_config_manual.h`.

Palavras-chave e identificadores não citados são sensíveis a maiúsculas e minúsculas. Portanto:

```
UPDATE MY_TABLE SET A = 5;
```

pode ser escrito de forma equivalente como:

```
uPDaTE my_TabLE SeT a = 5;
```

Uma convenção frequentemente usada é escrever palavras-chave em maiúsculas e nomes em minúsculas, por exemplo:

```
UPDATE my_table SET a = 5;
```

Existe um segundo tipo de identificador: o *identificador delimitado* ou *identificador citado*. É formado ao envolver uma sequência arbitrária de caracteres em aspas duplas (`"`). Um identificador delimitado é sempre um identificador, nunca uma palavra-chave. Portanto, `"select"` pode ser usado para se referir a uma coluna ou tabela chamada “select”, enquanto um `select` não citado seria interpretado como uma palavra-chave e, portanto, provocaria um erro de análise quando usado onde é esperado um nome de tabela ou coluna. O exemplo pode ser escrito com identificadores citados da seguinte forma:

```
UPDATE "my_table" SET "a" = 5;
```

Os identificadores citados podem conter qualquer caractere, exceto o caractere com código zero. (Para incluir uma citação dupla, escreva duas aspas duplas.) Isso permite a construção de nomes de tabela ou colunas que, de outra forma, não seriam possíveis, como aqueles que contêm espaços ou andamentos. A limitação de comprimento ainda se aplica.

Referenciar um identificador também o torna sensível ao caso, enquanto os nomes não referenciados são sempre dobrados para minúsculas. Por exemplo, os identificadores `FOO`, `foo` e `"foo"` são considerados iguais pelo PostgreSQL, mas `"Foo"` e `"FOO"` são diferentes desses três e entre si. (O dobramento de nomes não referenciados para minúsculas no PostgreSQL é incompatível com o padrão SQL, que diz que os nomes não referenciados devem ser dobrados para maiúsculas. Assim, `foo` deve ser equivalente a `"FOO"` e não a `"foo"` de acordo com o padrão. Se você deseja escrever aplicativos portáteis, é aconselhável sempre referenciar um nome específico ou nunca referenciá-lo.)

Uma variante de identificadores citados permite incluir caracteres Unicode escapados identificados por seus pontos de código. Essa variante começa com `U&` (U maiúsculo ou minúsculo seguido de e seguido de um símbolo de amplo) imediatamente antes da citação dupla de abertura, sem espaços entre eles, por exemplo, `U&"foo"`. (Observe que isso cria uma ambiguidade com o operador `&`. Use espaços ao redor do operador para evitar esse problema.) Dentro das citações, caracteres Unicode podem ser especificados em forma escapada escrevendo uma barra invertida seguida pelo número do ponto de código hexadecimal de quatro dígitos ou, alternativamente, uma barra invertida seguida de um sinal de mais seguido de um número de ponto de código hexadecimal de seis dígitos. Por exemplo, o identificador `"data"` poderia ser escrito como

```
U&"d\0061t\+000061"
```

O exemplo a seguir, menos trivial, escreve a palavra russa “slon” (elefante) em letras cirílicas:

```
U&"\0441\043B\043E\043D"
```

Se for desejado um caractere de escape diferente do travessão, ele pode ser especificado usando a cláusula `UESCAPE` após a string, por exemplo:

```
U&"d!0061t!+000061" UESCAPE '!'
```

O caractere de escape pode ser qualquer caractere único, exceto um dígito hexadecimal, o sinal de mais, uma citação única, uma citação dupla ou um caractere de espaço em branco. Note que o caractere de escape é escrito em citações simples, não em duplas, após `UESCAPE`.

Para incluir o caractere de escape no identificador literalmente, escreva-o duas vezes.

Pode-se usar a forma de escape de 4 dígitos ou de 6 dígitos para especificar pares de surogado UTF-16 para compor caracteres com pontos de código maiores que U+FFFF, embora a disponibilidade da forma de 6 dígitos tecnicamente torne isso desnecessário. (Os pares de surogado não são armazenados diretamente, mas são combinados em um único ponto de código.)

Se o codificação do servidor não for UTF-8, o ponto de código Unicode identificado por uma dessas sequências de escape é convertido para a codificação real do servidor; um erro é relatado se isso não for possível.

### 4.1.2. Constantes [#](#SQL-SYNTAX-CONSTANTS)

Existem três tipos de constantes *implicitamente digitadas* no PostgreSQL: strings, strings de bits e números. As constantes também podem ser especificadas com tipos explícitos, o que pode permitir uma representação mais precisa e um tratamento mais eficiente pelo sistema. Essas alternativas são discutidas nas seções a seguir.

#### 4.1.2.1. Constantes de cadeia [#](#SQL-SYNTAX-STRINGS)

Uma constante de cadeia em SQL é uma sequência arbitrária de caracteres limitada por aspas simples (`'`), por exemplo, `'This is a string'`. Para incluir um caractere de aspas simples dentro de uma constante de cadeia, escreva duas aspas simples adjacentes, por exemplo, `'Dianne''s horse'`. Observe que isso *não* é o mesmo que um caractere de aspas duplas (`"`).

Duas constantes de cadeia que são apenas separadas por espaço em branco *com pelo menos uma nova linha* são concatenadas e tratadas efetivamente como se a cadeia tivesse sido escrita como uma constante. Por exemplo:

```
SELECT 'foo'
'bar';
```

é equivalente a:

```
SELECT 'foobar';
```

mas:

```
SELECT 'foo'      'bar';
```

não é sintaxe válida. (Esse comportamento ligeiramente bizarro é especificado pelo SQL; o PostgreSQL está seguindo o padrão.)

#### 4.1.2.2. Constantes de cadeia com escapamentos em estilo C [#](#SQL-SYNTAX-STRINGS-ESCAPE)

O PostgreSQL também aceita constantes de cadeia de "escape", que são uma extensão do padrão SQL. Uma constante de cadeia de escape é especificada escrevendo a letra `E` (maiúscula ou minúscula) logo antes da primeira citação aberta, por exemplo, `E'foo'`. (Ao continuar uma constante de cadeia de escape em linhas, escreva `E` apenas antes da primeira citação aberta.) Dentro de uma cadeia de escape, um caractere barra (`\`) inicia uma sequência de escape *barra de escape* semelhante ao C, na qual a combinação de barra e caracteres subsequentes representa um valor de byte especial, conforme mostrado em [Tabela 4.1](sql-syntax-lexical.md#SQL-BACKSLASH-TABLE).

**Tabela 4.1. Sequências de Escape de Backslash**



<table border="1" class="table" summary="Backslash Escape Sequences">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Backslash Escape Sequence
   </th>
   <th>
    Interpretation
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     \b
    </code>
   </td>
   <td>
    backspace
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \f
    </code>
   </td>
   <td>
    form feed
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \n
    </code>
   </td>
   <td>
    newline
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \r
    </code>
   </td>
   <td>
    carriage return
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \t
    </code>
   </td>
   <td>
    tab
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \
     <em class="replaceable">
      <code>
       o
      </code>
     </em>
    </code>
    ,
    <code class="literal">
     \
     <em class="replaceable">
      <code>
       oo
      </code>
     </em>
    </code>
    ,
    <code class="literal">
     \
     <em class="replaceable">
      <code>
       ooo
      </code>
     </em>
    </code>
    (
    <em class="replaceable">
     <code>
      o
     </code>
    </em>
    = 0–7)
   </td>
   <td>
    octal byte value
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \x
     <em class="replaceable">
      <code>
       h
      </code>
     </em>
    </code>
    ,
    <code class="literal">
     \x
     <em class="replaceable">
      <code>
       hh
      </code>
     </em>
    </code>
    (
    <em class="replaceable">
     <code>
      h
     </code>
    </em>
    = 0–9, A–F)
   </td>
   <td>
    hexadecimal byte value
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \u
     <em class="replaceable">
      <code>
       xxxx
      </code>
     </em>
    </code>
    ,
    <code class="literal">
     \U
     <em class="replaceable">
      <code>
       xxxxxxxx
      </code>
     </em>
    </code>
    (
    <em class="replaceable">
     <code>
      x
     </code>
    </em>
    = 0–9, A–F)
   </td>
   <td>
    16 or 32-bit hexadecimal Unicode character value
   </td>
  </tr>
 </tbody>
</table>









Qualquer outro caractere que siga uma barra invertida é tomado literalmente. Assim, para incluir um caractere de barra invertida, escreva duas barras invertidas (`\\`). Além disso, uma única citação pode ser incluída em uma string de escape escrevendo `\'`, além da maneira normal de `''`.

É sua responsabilidade garantir que as sequências de bytes que você cria, especialmente ao usar escapamentos octal ou hexadecimal, comportem caracteres válidos no conjunto de caracteres do servidor. Uma alternativa útil é usar escapamentos Unicode ou a sintaxe de escapamento Unicode alternativa, explicada em [Seção 4.1.2.3](sql-syntax-lexical.md#SQL-SYNTAX-STRINGS-UESCAPE); então o servidor verificará se a conversão de caracteres é possível.

### Atenção

Se o parâmetro de configuração [standard_conforming_strings](runtime-config-compatible.md#GUC-STANDARD-CONFORMING-STRINGS) for `off`, o PostgreSQL reconhece escapamentos de barra insira em constantes de strings regulares e de escape. No entanto, a partir do PostgreSQL 9.1, o padrão é `on`, o que significa que os escapamentos de barra são reconhecidos apenas em constantes de strings de escape. Esse comportamento é mais compatível com os padrões, mas pode quebrar aplicações que dependem do comportamento histórico, onde os escapamentos de barra eram sempre reconhecidos. Como uma solução, você pode definir esse parâmetro para `off`, mas é melhor migrar para não usar escapamentos de barra. Se você precisar usar um escapamento de barra para representar um caractere especial, escreva a constante de string com `E`.

Além do `standard_conforming_strings`, os parâmetros de configuração [escape_string_warning](runtime-config-compatible.md#GUC-ESCAPE-STRING-WARNING) e [backslash_quote](runtime-config-compatible.md#GUC-BACKSLASH-QUOTE) regem o tratamento de barras inclinadas em constantes de string.

O caractere com o código zero não pode estar em uma constante de string.

#### 4.1.2.3. Constantes de cadeia com escapamentos Unicode [#](#SQL-SYNTAX-STRINGS-UESCAPE)

O PostgreSQL também suporta outro tipo de sintaxe de escape para strings que permite especificar caracteres Unicode arbitrários por ponto de código. Uma constante de cadeia de caracteres de escape Unicode começa com `U&` (letra maiúscula ou minúscula U seguida de e seguido de um símbolo de ampersand) imediatamente antes da citação de abertura, sem espaços entre eles, por exemplo, `U&'foo'`. (Observe que isso cria uma ambiguidade com o operador `&`. Use espaços ao redor do operador para evitar esse problema.) Dentro das citações, os caracteres Unicode podem ser especificados em forma escapada escrevendo uma barra invertida seguida pelo número hexadecimal de quatro dígitos ou, alternativamente, uma barra invertida seguida de um sinal de mais seguido de um número hexadecimal de seis dígitos. Por exemplo, a string `'data'` poderia ser escrita como

```
U&'d\0061t\+000061'
```

O exemplo a seguir, menos trivial, escreve a palavra russa “slon” (elefante) em letras cirílicas:

```
U&'\0441\043B\043E\043D'
```

Se for desejado um caractere de escape diferente do travessão, ele pode ser especificado usando a cláusula `UESCAPE` após a string, por exemplo:

```
U&'d!0061t!+000061' UESCAPE '!'
```

O caractere de fuga pode ser qualquer caractere único, exceto um dígito hexadecimal, o sinal de mais, uma citação única, uma citação dupla ou um caractere de espaço em branco.

Para incluir o caractere de escape na string literalmente, escreva-o duas vezes.

Pode-se usar a forma de escape de 4 dígitos ou de 6 dígitos para especificar pares de surogado UTF-16 para compor caracteres com pontos de código maiores que U+FFFF, embora a disponibilidade da forma de 6 dígitos tecnicamente torne isso desnecessário. (Os pares de surogado não são armazenados diretamente, mas são combinados em um único ponto de código.)

Se o codificação do servidor não for UTF-8, o ponto de código Unicode identificado por uma dessas sequências de escape é convertido para a codificação real do servidor; um erro é relatado se isso não for possível.

Além disso, a sintaxe de escape Unicode para constantes de string só funciona quando o parâmetro de configuração [standard_conforming_strings](runtime-config-compatible.md#GUC-STANDARD-CONFORMING-STRINGS) está ativado. Isso ocorre porque, caso contrário, essa sintaxe poderia confundir os clientes que analisam as declarações SQL ao ponto de poder levar a injeções SQL e problemas de segurança semelhantes. Se o parâmetro estiver definido como desligado, essa sintaxe será rejeitada com uma mensagem de erro.

#### 4.1.2.4. Constantes de cadeia com valores citados em dólares [#](#SQL-SYNTAX-DOLLAR-QUOTING)

Embora a sintaxe padrão para especificar constantes de cadeia seja geralmente conveniente, pode ser difícil de entender quando a cadeia desejada contém muitas aspas simples, uma vez que cada uma delas deve ser duplicada. Para permitir consultas mais legíveis nessas situações, o PostgreSQL fornece outra maneira, chamada “cotação em dólar”, para escrever constantes de cadeia. Uma constante de cadeia cotada em dólar consiste em um sinal de dólar (`$`), um “etiqueta” opcional de zero ou mais caracteres, outro sinal de dólar, uma sequência arbitrária de caracteres que compõe o conteúdo da cadeia, um sinal de dólar, a mesma etiqueta que começou esta citação em dólar e um sinal de dólar. Por exemplo, aqui estão duas maneiras diferentes de especificar a cadeia “Cavalo de Dianne” usando cotação em dólar:

```
$$Dianne's horse$$
$SomeTag$Dianne's horse$SomeTag$
```

Observe que, dentro da string citada em dólares, as aspas podem ser usadas sem necessidade de serem escapadas. De fato, nenhum caractere dentro de uma string citada em dólares é escamado: o conteúdo da string é sempre escrito literalmente. Travessões não são especiais, e nem os sinais de dólar, a menos que sejam parte de uma sequência que corresponda à tag de abertura.

É possível aninhar constantes de cadeia com cotação em dólares escolhendo diferentes tags em cada nível de aninhamento. Isso é mais comumente usado na escrita de definições de funções. Por exemplo:

```
$function$
BEGIN
    RETURN ($1 ~ $q$[\t\r\n\v\\]$q$);
END;
$function$
```

Aqui, a sequência `$q$[\t\r\n\v\\]$q$` representa uma cadeia literal com citação em dólar `[\t\r\n\v\\]`, que será reconhecida quando o corpo da função for executado pelo PostgreSQL. Mas, como a sequência não corresponde ao delimitador de citação em dólar externo `$function$`, são apenas mais caracteres dentro da constante, no que diz respeito à cadeia externa.

A tag, se houver, de uma string citada em dólares segue as mesmas regras que um identificador não citado, exceto que ela não pode conter um sinal de dólar. As tags são sensíveis a maiúsculas e minúsculas, então `$tag$String content$tag$` é correto, mas `$TAG$String content$tag$` não é.

Uma cadeia de caracteres citada em dólares que segue uma palavra-chave ou identificador deve ser separada dela por espaço em branco; caso contrário, o delimitador de citação em dólares seria considerado parte do identificador anterior.

A citação de dólares não faz parte do padrão SQL, mas é frequentemente uma maneira mais conveniente de escrever literais de string complicados do que a sintaxe de citação única compatível com o padrão. É particularmente útil ao representar constantes de string dentro de outras constantes, como muitas vezes é necessário nas definições de funções processuais. Com a sintaxe de citação única, cada barra invertida no exemplo acima teria que ser escrita como quatro barras invertidas, o que seria reduzido a duas barras invertidas na análise da constante de string original, e depois a uma quando a constante de string interna é analisada novamente durante a execução da função.

#### 4.1.2.5. Constantes de cadeia de bits [#](#SQL-SYNTAX-BIT-STRINGS)

As constantes de cadeia de bits parecem constantes de cadeia regulares com `B` (maiúscula ou minúscula) imediatamente antes da citação de abertura (sem espaços em branco intermediários), por exemplo, `B'1001'`. Os únicos caracteres permitidos dentro das constantes de cadeia de bits são `0` e `1`.

Alternativamente, as constantes de cadeia de bits podem ser especificadas em notação hexadecimal, usando um `X` (maiúscula ou minúscula) no início, por exemplo, `X'1FF'`. Essa notação é equivalente a uma constante de cadeia de bits com quatro dígitos binários para cada dígito hexadecimal.

Ambas as formas de constante de cadeia de bits podem ser continuadas em linhas da mesma maneira que as constantes de cadeia de caracteres regulares. A citação de dólar não pode ser usada em uma constante de cadeia de bits.

#### 4.1.2.6. Constantes numéricas [#](#SQL-SYNTAX-CONSTANTS-NUMERIC)

As constantes numéricas são aceitas nessas formas gerais:

```
digits
digits.[digits][e[+-]digits]
[digits].digits[e[+-]digits]
digitse[+-]digits
```

onde *`digits`* é um ou mais dígitos decimais (0 a 9). Pelo menos um dígito deve estar antes ou depois do ponto decimal, se um deles for usado. Pelo menos um dígito deve seguir o marcador de expoente (`e`), se um deles for presente. Não pode haver espaços ou outros caracteres embutidos na constante, exceto por sublinhados, que podem ser usados para agrupamento visual conforme descrito abaixo. Note que qualquer sinal de mais ou menos inicial não é considerado parte da constante; é um operador aplicado à constante.

Esses são alguns exemplos de constantes numéricas válidas:

42 3,5 4. .001 5e2 1,925e-3

Além disso, constantes inteiras não decimais são aceitas nesses formatos:

```
0xhexdigits
0ooctdigits
0bbindigits
```

onde *`hexdigits`* é um ou mais algarismos hexadecimais (0-9, A-F), *`octdigits`* é um ou mais algarismos óctal (0-7), e *`bindigits`* é um ou mais algarismos binários (0 ou 1). Os algarismos hexadecimais e os prefixos de radix podem ser em maiúsculas ou minúsculas. Note que apenas os inteiros podem ter formas não decimais, não números com partes fracionárias.

Esses são alguns exemplos de constantes inteiras não decimais válidas:

0b100101 0B10011001 0o273 0O755 0x42f 0XFFFF

Para agrupamento visual, sublinhados podem ser inseridos entre dígitos. Esses não têm efeito adicional no valor da constante. Por exemplo:

1_500_000_000 0b10001000_00000000 0o_1_755 0xFFFF_FFFF 1.618_034

Sublinhados não são permitidos no início ou no fim de uma constante numérica ou de um grupo de dígitos (ou seja, imediatamente antes ou depois do ponto decimal ou do marcador de expoente), e mais de um sublinhado em uma linha não é permitido.

Uma constante numérica que não contém ponto decimal nem expoente é inicialmente presumida ser do tipo `integer` se seu valor se encaixar no tipo `integer` (32 bits); caso contrário, é presumida ser do tipo `bigint` se seu valor se encaixar no tipo `bigint` (64 bits); caso contrário, é considerada do tipo `numeric`. As constantes que contêm pontos decimais e/ou expoentes são sempre inicialmente presumidas ser do tipo `numeric`.

O tipo de dado inicialmente atribuído a uma constante numérica é apenas um ponto de partida para os algoritmos de resolução de tipo. Na maioria dos casos, a constante será automaticamente coercida para o tipo mais apropriado, dependendo do contexto. Quando necessário, você pode forçar que um valor numérico seja interpretado como um tipo específico, realizando uma conversão. Por exemplo, você pode forçar que um valor numérico seja tratado como o tipo `real` (`float4`) escrevendo:

```
REAL '1.23'  -- string style
1.23::REAL   -- PostgreSQL (historical) style
```

Na verdade, esses são apenas casos especiais das anotações de lançamento gerais discutidas a seguir.

#### 4.1.2.7. Constantes de Outros Tipos [#](#SQL-SYNTAX-CONSTANTS-GENERIC)

Uma constante de um tipo *arbitrário* pode ser inserida usando qualquer uma das seguintes notações:

```
type 'string'
'string'::type
CAST ( 'string' AS type )
```

O texto da constante de cadeia é passado para a rotina de conversão de entrada para o tipo chamado *`type`*. O resultado é uma constante do tipo indicado. O cast de tipo explícito pode ser omitido se não houver ambiguidade quanto ao tipo que a constante deve ser (por exemplo, quando é atribuída diretamente a uma coluna de tabela), no qual caso ela é automaticamente coercida.

A constante de cadeia pode ser escrita usando uma notação SQL regular ou citação em dólar.

Também é possível especificar uma coerção de tipo usando uma sintaxe semelhante a uma função:

```
typename ( 'string' )
```

mas nem todos os nomes de tipo podem ser usados dessa maneira; consulte [Seção 4.2.9](sql-expressions.md#SQL-SYNTAX-TYPE-CASTS) para obter detalhes.

As sintaxes `::`, `CAST()` e de chamada de função também podem ser usadas para especificar conversões de tipo de expressão arbitrária em tempo de execução, conforme discutido em [Seção 4.2.9](sql-expressions.md#SQL-SYNTAX-TYPE-CASTS). Para evitar ambiguidade sintática, a sintaxe `type 'string'` só pode ser usada para especificar o tipo de uma constante literal simples. Outra restrição sobre a sintaxe `type 'string'` é que ela não funciona para tipos de matriz; use `::` ou `CAST()` para especificar o tipo de uma constante de matriz.

A sintaxe `CAST()` é conforme com a SQL. A sintaxe `type 'string'` é uma generalização do padrão: a SQL especifica essa sintaxe apenas para alguns tipos de dados, mas o PostgreSQL permite isso para todos os tipos. A sintaxe com `::` é o uso histórico do PostgreSQL, assim como a sintaxe de chamada de função.

### 4.1.3. Operadores [#](#SQL-SYNTAX-OPERATORS)

Um nome de operador é uma sequência de até `NAMEDATALEN` caracteres (63 por padrão) da lista a seguir:

+ - * / < > = ~ ! @ # % ^ & | ` ?

Existem algumas restrições em relação aos nomes dos operadores, no entanto:

* `--` e `/*` não podem aparecer em qualquer lugar em um nome de operador, pois serão interpretados como o início de um comentário.
* Um nome de operador de vários caracteres não pode terminar em `+` ou `-`, a menos que o nome também contenha pelo menos um desses caracteres:

~ ! @ # % ^ & | ' ?

Por exemplo, `@-` é um nome de operador permitido, mas `*-` não é. Essa restrição permite que o PostgreSQL analise consultas compatíveis com SQL sem exigir espaços entre os tokens.

Ao trabalhar com nomes de operadores que não são padrão para SQL, geralmente você precisará separar operadores adjacentes com espaços para evitar ambiguidade. Por exemplo, se você definiu um operador prefixo chamado `@`, não pode escrever `X*@Y`; você deve escrever `X* @Y` para garantir que o PostgreSQL o leia como dois nomes de operador, não um.

### 4.1.4. Caracteres especiais [#](#SQL-SYNTAX-SPECIAL-CHARS)

Alguns caracteres que não são alfanuméricos têm um significado especial que é diferente de ser um operador. Os detalhes sobre o uso podem ser encontrados no local onde o respectivo elemento de sintaxe é descrito. Esta seção existe apenas para avisar sobre a existência e resumir os propósitos desses caracteres.

Um símbolo de dólar (`$`) seguido por dígitos é usado para representar um parâmetro posicional no corpo de uma definição de função ou uma declaração preparada. Em outros contextos, o símbolo de dólar pode fazer parte de um identificador ou uma constante de cadeia citada por dólar. Parenteses (`()`) têm seu significado usual para agrupar expressões e impor precedência. Em alguns casos, as parenteses são necessárias como parte da sintaxe fixa de um comando SQL específico. Colchetes (`[]`) são usados para selecionar os elementos de um array. Consulte [Seção 8.15](arrays.md "8.15. Arrays") para mais informações sobre arrays. Vírgula (`,`) são usadas em algumas construções sintáticas para separar os elementos de uma lista. O ponto e vírgula (`;`) termina um comando SQL. Não pode aparecer em qualquer lugar dentro de um comando, exceto dentro de uma constante de cadeia ou identificador citado. O colon (`:`) é usado para selecionar “cortes” de arrays. (Veja [Seção 8.15](arrays.md "8.15. Arrays").). Em certos dialetos SQL (como Embedded SQL), o colon é usado para prefixar nomes de variáveis. O asterisco (`*`) é usado em alguns contextos para denotar todos os campos de uma linha de tabela ou valor composto. Também tem um significado especial quando usado como argumento de uma função agregada, ou seja, o agregado não requer nenhum parâmetro explícito. O ponto (`.`) é usado em constantes numéricas e para separar nomes de esquema, tabela e coluna.

### 4.1.5. Comentários [#](#SQL-SYNTAX-COMMENTS)

Um comentário é uma sequência de caracteres que começa com duas barras e se estende até o final da linha, por exemplo:

```
-- This is a standard SQL comment
```

Alternativamente, os comentários em estilo C podem ser usados:

```
/* multiline comment
 * with nesting: /* nested block comment */
 */
```

onde o comentário começa com `/*` e se estende até a ocorrência correspondente de `*/`. Esses comentários de bloco se aninham, conforme especificado no padrão SQL, mas ao contrário do C, para que se possa comentar blocos maiores de código que possam conter comentários de bloco existentes.

Um comentário é removido do fluxo de entrada antes de uma análise sintática adicional e é efetivamente substituído por espaço em branco.

### 4.1.6. Precedência do Operador [#](#SQL-PRECEDENCE)

[Tabela 4.2](sql-syntax-lexical.md#SQL-PRECEDENCE-TABLE "Table 4.2. Operator Precedence (highest to lowest)") mostra a precedência e a associatividade dos operadores no PostgreSQL. A maioria dos operadores tem a mesma precedência e são associativos à esquerda. A precedência e a associatividade dos operadores estão embutidos no analisador. Adicione parênteses se você deseja que uma expressão com vários operadores seja analisada de alguma outra maneira do que o que as regras de precedência implicam.

**Tabela 4.2. Prioridade do operador (da maior para a menor)**



<table border="1" class="table" summary="Operator Precedence (highest to lowest)">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Operator/Element
   </th>
   <th>
    Associativity
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="token">
     .
    </code>
   </td>
   <td>
    left
   </td>
   <td>
    separador de nome de tabela/coluna
   </td>
  </tr>
  <tr>
   <td>
    <code class="token">
     ::
    </code>
   </td>
   <td>
    left
   </td>
   <td>
    <span class="productname">
     PostgreSQL
    </span>
    - tipo de elenco de estilo
   </td>
  </tr>
  <tr>
   <td>
    <code class="token">
     [
    </code>
    <code class="token">
     ]
    </code>
   </td>
   <td>
    left
   </td>
   <td>
    seleção de elemento de matriz
   </td>
  </tr>
  <tr>
   <td>
    <code class="token">
     +
    </code>
    <code class="token">
     -
    </code>
   </td>
   <td>
    right
   </td>
   <td>
    mais um, menos um
   </td>
  </tr>
  <tr>
   <td>
    <code class="token">
     COLLATE
    </code>
   </td>
   <td>
    left
   </td>
   <td>
    seleção de colagem
   </td>
  </tr>
  <tr>
   <td>
    <code class="token">
     AT
    </code>
   </td>
   <td>
    left
   </td>
   <td>
    <code class="literal">
     AT TIME ZONE
    </code>
    ,
    <code class="literal">
     AT LOCAL
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="token">
     ^
    </code>
   </td>
   <td>
    left
   </td>
   <td>
    exponenciação
   </td>
  </tr>
  <tr>
   <td>
    <code class="token">
     *
    </code>
    <code class="token">
     /
    </code>
    <code class="token">
     %
    </code>
   </td>
   <td>
    left
   </td>
   <td>
    multiplicação, divisão, módulo
   </td>
  </tr>
  <tr>
   <td>
    <code class="token">
     +
    </code>
    <code class="token">
     -
    </code>
   </td>
   <td>
    left
   </td>
   <td>
    adição, subtração
   </td>
  </tr>
  <tr>
   <td>
    (any other operator)
   </td>
   <td>
    left
   </td>
   <td>
    todos os outros operadores nativos e definidos pelo usuário
   </td>
  </tr>
  <tr>
   <td>
    <code class="token">
     BETWEEN
    </code>
    <code class="token">
     IN
    </code>
    <code class="token">
     LIKE
    </code>
    <code class="token">
     ILIKE
    </code>
    <code class="token">
     SIMILAR
    </code>
   </td>
   <td>
   </td>
   <td>
    containment de intervalo, pertença de conjunto, correspondência de string
   </td>
  </tr>
  <tr>
   <td>
    <code class="token">
     &lt;
    </code>
    <code class="token">
     &gt;
    </code>
    <code class="token">
     =
    </code>
    <code class="token">
     &lt;=
    </code>
    <code class="token">
     &gt;=
    </code>
    <code class="token">
     &lt;&gt;
    </code>
   </td>
   <td>
   </td>
   <td>
    operadores de comparação
   </td>
  </tr>
  <tr>
   <td>
    <code class="token">
     IS
    </code>
    <code class="token">
     ISNULL
    </code>
    <code class="token">
     NOTNULL
    </code>
   </td>
   <td>
   </td>
   <td>
    <code class="literal">
     IS TRUE
    </code>
    ,
    <code class="literal">
     IS FALSE
    </code>
    ,
    <code class="literal">
     IS NULL
    </code>
    ,
    <code class="literal">
     IS DISTINCT FROM
    </code>
    , etc.
   </td>
  </tr>
  <tr>
   <td>
    <code class="token">
     NOT
    </code>
   </td>
   <td>
    right
   </td>
   <td>
    negação lógica
   </td>
  </tr>
  <tr>
   <td>
    <code class="token">
     AND
    </code>
   </td>
   <td>
    left
   </td>
   <td>
    conjunção lógica
   </td>
  </tr>
  <tr>
   <td>
    <code class="token">
     OR
    </code>
   </td>
   <td>
    left
   </td>
   <td>
    disjunção lógica
   </td>
  </tr>
 </tbody>
</table>









Observe que as regras de precedência do operador também se aplicam a operadores definidos pelo usuário que tenham os mesmos nomes dos operadores internos mencionados acima. Por exemplo, se você definir um operador "+" para algum tipo de dados personalizado, ele terá a mesma precedência que o operador interno "+" interno, independentemente do que o seu fizer.

Quando um nome de operador qualificado por esquema é usado na sintaxe do `OPERATOR`, como, por exemplo, em:

```
SELECT 3 OPERATOR(pg_catalog.+) 4;
```

o `OPERATOR` é considerado ter a precedência padrão mostrada em [Tabela 4.2](sql-syntax-lexical.md#SQL-PRECEDENCE-TABLE)) para “qualquer outro operador”. Isso é verdadeiro, independentemente de qual operador específico aparecer dentro de `OPERATOR()`.

### Nota

As versões do PostgreSQL anteriores a 9.5 utilizavam regras de precedência de operadores ligeiramente diferentes. Em particular, `<=` `>=` e `<>` costumavam ser tratados como operadores genéricos; os testes `IS` costumavam ter uma prioridade mais alta; e `NOT BETWEEN` e construções relacionadas agiam de forma inconsistente, sendo tomadas em alguns casos como tendo a precedência de `NOT` em vez de `BETWEEN`. Essas regras foram alteradas para melhor conformidade com o padrão SQL e para reduzir a confusão decorrente do tratamento inconsistente de construções logicamente equivalentes. Na maioria dos casos, essas mudanças não resultarão em nenhuma mudança comportamental, ou talvez em falhas de "nenhum operador" que podem ser resolvidas adicionando parênteses. No entanto, existem casos especiais em que uma consulta pode mudar o comportamento sem que nenhum erro de análise seja relatado.