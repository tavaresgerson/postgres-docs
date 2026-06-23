## 9.7. Contagem de Padrões [#](#FUNCTIONS-MATCHING)

* [9.7.1. `LIKE`](functions-matching.md#FUNCTIONS-LIKE)
* [9.7.2. `SIMILAR TO` Expressões Regulares](functions-matching.md#FUNCTIONS-SIMILARTO-REGEXP)
* [9.7.3. Expressões Regulares POSIX](functions-matching.md#FUNCTIONS-POSIX-REGEXP)

Existem três abordagens separadas para correspondência de padrões fornecidas pelo PostgreSQL: o operador SQL tradicional `LIKE`, o operador mais recente `SIMILAR TO` (adicionado no SQL: 1999) e expressões regulares em estilo POSIX. Além dos operadores básicos “esta string corresponde a este padrão?”, funções estão disponíveis para extrair ou substituir substratos correspondentes e para dividir uma string em locais de correspondência.

### DICA

Se você tem necessidades de correspondência de padrões que vão além disso, considere escrever uma função definida pelo usuário em Perl ou Tcl.

### Atenção

Embora a maioria das pesquisas com expressões regulares possa ser executada muito rapidamente, é possível criar expressões regulares que levam quantidades arbitrárias de tempo e memória para processar. Seja cauteloso ao aceitar padrões de pesquisa com expressões regulares de fontes hostis. Se você deve fazê-lo, é aconselhável impor um limite de tempo para a declaração.

As pesquisas que utilizam padrões `SIMILAR TO` apresentam os mesmos riscos de segurança, uma vez que `SIMILAR TO` oferece muitas das mesmas capacidades que as expressões regulares em estilo POSIX.

As pesquisas `LIKE` são muito mais simples do que as outras duas opções e são mais seguras para serem usadas com fontes de padrões possivelmente hostis.

`SIMILAR TO` e as expressões regulares em estilo POSIX não suportam colas não determinísticas. Se necessário, use `LIKE` ou aplique uma outra colocação à expressão para contornar essa limitação.

### 9.7.1. `LIKE` [#](#FUNCTIONS-LIKE)

```
string LIKE pattern [ESCAPE escape-character]
string NOT LIKE pattern [ESCAPE escape-character]
```

A expressão `LIKE` retorna verdadeiro se o *`string`* corresponder ao *`pattern`* fornecido. (Como esperado, a expressão `NOT LIKE` retorna falsa se `LIKE` retornar verdadeiro, e vice-versa. Uma expressão equivalente é `NOT (string LIKE pattern)`.)

Se *`pattern`* não contém sinais percentuais ou sublinhados, então o padrão representa apenas a própria string; nesse caso, `LIKE` age como o operador de igualdade. Um underscore (`_`) em *`pattern`* representa (concorda) qualquer caracter único; um sinal percentual (`%`) corresponde a qualquer sequência de zero ou mais caracteres.

Alguns exemplos:

```
'abc' LIKE 'abc'    true
'abc' LIKE 'a%'     true
'abc' LIKE '_b_'    true
'abc' LIKE 'c'      false
```

A correspondência de padrões `LIKE` suporta colunas não determinísticas (consulte [Seção 23.2.2.4](collation.md#COLLATION-NONDETERMINISTIC)), como colunas que são sensíveis ao caso ou que, por exemplo, ignoram a pontuação. Assim, com uma coluna sensível ao caso, pode-se ter:

```
'AbC' LIKE 'abc' COLLATE case_insensitive    true
'AbC' LIKE 'a%' COLLATE case_insensitive     true
```

Com codificações que ignoram certos caracteres ou que, de forma geral, consideram cadeias de diferentes comprimentos iguais, a semântica pode se tornar um pouco mais complicada. Considere esses exemplos:

```
'.foo.' LIKE 'foo' COLLATE ign_punct    true
'.foo.' LIKE 'f_o' COLLATE ign_punct    true
'.foo.' LIKE '_oo' COLLATE ign_punct    false
```

A forma como o correspondência funciona é que o padrão é dividido em sequências de caracteres com asteriscos e strings sem asteriscos (os asteriscos sendo `_` e `%`). Por exemplo, o padrão `f_o` é dividido em `f, _, o`, o padrão `_oo` é dividido em `_, oo`. A string de entrada corresponde ao padrão se puder ser dividida de tal forma que os asteriscos correspondam a um caractere ou a qualquer número de caracteres, respectivamente, e as partes sem asteriscos sejam iguais sob a collation aplicável. Então, por exemplo, `'.foo.' LIKE 'f_o' COLLATE ign_punct` é verdadeiro porque se pode dividir `.foo.` em `.f, o, o.`, e depois `'.f' = 'f' COLLATE ign_punct`, `'o'` corresponde ao caractere com asterisco `_`, e `'o.' = 'o' COLLATE ign_punct`. Mas `'.foo.' LIKE '_oo' COLLATE ign_punct` é falso porque `.foo.` não pode ser dividido de uma forma que o primeiro caractere seja qualquer caractere e o resto da string seja igual a `oo`. (Nota que o caractere com asterisco de um único caractere sempre corresponde exatamente a um caractere, independentemente da collation. Então, neste exemplo, o `_` corresponderia a `.`, mas depois o resto da string de entrada não corresponderia ao resto do padrão.)

A correspondência de padrões `LIKE` sempre cobre toda a string. Portanto, se deseja-se corresponder a uma sequência em qualquer lugar dentro de uma string, o padrão deve começar e terminar com um sinal de porcentagem.

Para corresponder a um underscore literal ou sinal de porcentagem sem corresponder a outros caracteres, o respectivo caractere em *`pattern`* deve ser precedido pelo caractere de escape. O caractere de escape padrão é a barra invertida, mas um diferente pode ser selecionado usando a cláusula `ESCAPE`. Para corresponder ao próprio caractere de escape, escreva dois caracteres de escape.

Nota

Se você tiver desativado [standard_conforming_strings](runtime-config-compatible.md#GUC-STANDARD-CONFORMING-STRINGS), qualquer barra insira que você escrever em constantes de string literal precisará ser duplicada. Consulte [Seção 4.1.2.1](sql-syntax-lexical.md#SQL-SYNTAX-STRINGS) para mais informações.

Também é possível não selecionar nenhum caractere de escape escrevendo `ESCAPE ''`. Isso efetivamente desativa o mecanismo de escape, o que torna impossível desativar o significado especial dos sinais de sublinhado e porcentagem no padrão.

De acordo com o padrão SQL, omitir `ESCAPE` significa que não há caractere de escape (em vez de padronizar para uma barra invertida), e um valor de comprimento zero `ESCAPE` é desaconselhado. Portanto, o comportamento do PostgreSQL nesse aspecto é ligeiramente não padrão.

A palavra-chave `ILIKE` pode ser usada em vez de `LIKE` para fazer a correspondência não sensível ao caso conforme o local ativo. (Mas isso não suporta colunas não determinísticas.) Isso não está no padrão SQL, mas é uma extensão do PostgreSQL.

O operador `~~` é equivalente a `LIKE`, e `~~*` corresponde a `ILIKE`. Existem também os operadores `!~~` e `!~~*` que representam, respectivamente, `NOT LIKE` e `NOT ILIKE`. Todos esses operadores são específicos do PostgreSQL. Você pode ver esses nomes de operadores no `EXPLAIN` e em lugares semelhantes, já que o analisador realmente traduz `LIKE` et al. para esses operadores.

As expressões `LIKE`, `ILIKE`, `NOT LIKE` e `NOT ILIKE` são geralmente tratadas como operadores na sintaxe do PostgreSQL; por exemplo, elas podem ser usadas em construções como *`expression`* *`operator`* ANY (*`subquery`*) e, embora uma cláusula `ESCAPE` não possa ser incluída lá, em alguns casos obscuros, pode ser necessário usar os nomes dos operadores subjacentes.

Veja também o operador começa com `^@` e a função correspondente `starts_with()`, que são úteis em casos em que simplesmente é necessário corresponder ao início de uma cadeia.

### 9.7.2. `SIMILAR TO` Expressões Regulares [#](#FUNCTIONS-SIMILARTO-REGEXP)

```
string SIMILAR TO pattern [ESCAPE escape-character]
string NOT SIMILAR TO pattern [ESCAPE escape-character]
```

O operador `SIMILAR TO` retorna verdadeiro ou falso, dependendo se seu padrão corresponde à string fornecida. É semelhante ao `LIKE`, exceto que ele interpreta o padrão usando a definição do padrão de expressão regular do padrão SQL. As expressões regulares SQL são uma curiosidade que combina a notação `LIKE` e a notação comum (POSIX) de expressão regular.

Assim como `LIKE`, o operador `SIMILAR TO` só tem sucesso se seu padrão corresponder a toda a string; isso é diferente do comportamento comum das expressões regulares, onde o padrão pode corresponder a qualquer parte da string. Também, assim como `LIKE`, `SIMILAR TO` usa `_` e `%` como caracteres curinga, denotando qualquer caractere único e qualquer string, respectivamente (estes são comparáveis a `.` e `.*` nas expressões regulares POSIX).

Além dessas funcionalidades emprestadas do `LIKE`, o `SIMILAR TO` suporta esses metacaracteres de correspondência de padrões emprestados das expressões regulares POSIX:

* `|` denota alternância (de duas alternativas).
* `*` denota repetição do item anterior zero ou mais vezes.
* `+` denota repetição do item anterior uma ou mais vezes.
* `?` denota repetição do item anterior zero ou uma vez.
* `{`*`m`*`}` denota repetição do item anterior exatamente *`m`* vezes.
* `{`*`m`*`,}` denota repetição do item anterior *`m`* ou mais vezes.
* `{`*`m`*`,`*`n`*`}` denota repetição do item anterior pelo menos *`m`* e não mais do que *`n`* vezes.
* As chaves `()` podem ser usadas para agrupar itens em um único item lógico.
* Uma expressão em chaves `[...]` especifica uma classe de caracteres, assim como nas expressões regulares POSIX.

Observe que o período (`.`) não é um caractere meta para `SIMILAR TO`.

Assim como em `LIKE`, um traço de barra desativa o significado especial de qualquer um desses metacaracteres. Um caractere de escape diferente pode ser especificado com `ESCAPE`, ou a capacidade de escape pode ser desativada escrevendo `ESCAPE ''`.

De acordo com o padrão SQL, omitir `ESCAPE` significa que não há caractere de escape (em vez de padronizar com uma barra invertida), e um valor de comprimento zero `ESCAPE` é desaconselhado. Portanto, o comportamento do PostgreSQL nesse aspecto é ligeiramente não padrão.

Outra extensão não padrão é que, ao seguir o caractere de escape com uma letra ou dígito, é possível acessar as sequências de escape definidas para expressões regulares POSIX; veja [Tabela 9.20](functions-matching.md#POSIX-CHARACTER-ENTRY-ESCAPES-TABLE), [Tabela 9.21](functions-matching.md#POSIX-CLASS-SHORTHAND-ESCAPES-TABLE) e [Tabela 9.22](functions-matching.md#POSIX-CONSTRAINT-ESCAPES-TABLE) abaixo.

Alguns exemplos:

```
'abc' SIMILAR TO 'abc'          true
'abc' SIMILAR TO 'a'            false
'abc' SIMILAR TO '%(b|d)%'      true
'abc' SIMILAR TO '(b|c)%'       false
'-abc-' SIMILAR TO '%\mabc\M%'  true
'xabcy' SIMILAR TO '%\mabc\M%'  false
```

A função `substring` com três parâmetros fornece a extração de uma subcadeia que corresponde a um padrão de expressão regular SQL. A função pode ser escrita de acordo com a sintaxe SQL padrão:

```
substring(string similar pattern escape escape-character)
```

ou usando a sintaxe SQL:1999, que já está obsoleta:

```
substring(string from pattern for escape-character)
```

ou como uma função simples de três argumentos:

```
substring(string, pattern, escape-character)
```

Assim como em `SIMILAR TO`, o padrão especificado deve corresponder a toda a cadeia de dados, caso contrário, a função falha e retorna nulo. Para indicar a parte do padrão para a qual o sub-texto de dados de correspondência é de interesse, o padrão deve conter duas ocorrências do caractere de escape seguido por uma citação dupla (`"`). O texto que corresponde à porção do padrão entre esses separadores é retornado quando a correspondência é bem-sucedida.

Os separadores de aspas duplas de escape, na verdade, dividem o padrão do `substring` em três expressões regulares independentes; por exemplo, uma barra vertical (`|`) em qualquer uma das três seções afeta apenas aquela seção. Além disso, o primeiro e o terceiro desses padrões regulares são definidos para corresponder à menor quantidade possível de texto, não à maior, quando há alguma ambiguidade sobre quanto da string de dados corresponde a qual padrão. (Na linguagem POSIX, os primeiros e terceiros padrões regulares são obrigados a serem não ávidos.)

Como uma extensão do padrão SQL, o PostgreSQL permite que haja apenas um separador de escapamento de dupla-citação, nesse caso, a terceira expressão regular é considerada vazia; ou sem separadores, nesse caso, a primeira e a terceira expressões regulares são consideradas vazias.

Alguns exemplos, com `#"` delimitando a string de retorno:

```
substring('foobar' similar '%#"o_b#"%' escape '#')   oob
substring('foobar' similar '#"o_b#"%' escape '#')    NULL
```

### 9.7.3. Expressões Regulares POSIX [#](#FUNCTIONS-POSIX-REGEXP)

[Tabela 9.16](functions-matching.md#FUNCTIONS-POSIX-TABLE) lista os operadores disponíveis para correspondência de padrões usando expressões regulares POSIX.

**Tabela 9.16. Operadores de correspondência de expressão regular**



<table border="1" class="table" summary="Regular Expression Match Operators">
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
     <code class="type">
      text
     </code>
     <code class="literal">
      ~
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     String corresponde à expressão regular, sensível ao caso
    </p>
    <p>
     <code class="literal">
      'thomas' ~ 't.*ma'
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
     <code class="type">
      text
     </code>
     <code class="literal">
      ~*
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     String corresponde à expressão regular, de forma sensível ao caso
    </p>
    <p>
     <code class="literal">
      'thomas' ~* 'T.*ma'
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
     <code class="type">
      text
     </code>
     <code class="literal">
      !~
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     A cadeia não corresponde à expressão regular, sensível ao caso
    </p>
    <p>
     <code class="literal">
      'thomas' !~ 't.*max'
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
     <code class="type">
      text
     </code>
     <code class="literal">
      !~*
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     A cadeia não corresponde à expressão regular, de forma sensível ao caso
    </p>
    <p>
     <code class="literal">
      'thomas' !~* 'T.*ma'
     </code>
     →
     <code class="returnvalue">
      f
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>










As expressões regulares POSIX oferecem um meio mais poderoso para a correspondência de padrões do que os operadores `LIKE` e `SIMILAR TO`. Muitas ferramentas Unix, como `egrep`, `sed` ou `awk`, utilizam uma linguagem de correspondência de padrões semelhante àquela descrita aqui.

Uma expressão regular é uma sequência de caracteres que é uma definição abreviada de um conjunto de cadeias de caracteres (um *conjunto regular*). Diz-se que uma cadeia de caracteres corresponde a uma expressão regular se ela é um membro do conjunto regular descrito pela expressão regular. Assim como em `LIKE`, os caracteres do padrão correspondem exatamente aos caracteres da cadeia de caracteres, a menos que sejam caracteres especiais na linguagem da expressão regular — mas as expressões regulares usam caracteres especiais diferentes do que `LIKE` faz. Ao contrário dos padrões de `LIKE`, uma expressão regular pode corresponder em qualquer lugar dentro de uma cadeia de caracteres, a menos que a expressão regular seja explicitamente ancorada ao início ou fim da cadeia de caracteres.

Alguns exemplos:

```
'abcd' ~ 'bc'     true
'abcd' ~ 'a.c'    true — dot matches any character
'abcd' ~ 'a.*d'   true — * repeats the preceding pattern item
'abcd' ~ '(b|x)'  true — | means OR, parentheses group
'abcd' ~ '^a'     true — ^ anchors to start of string
'abcd' ~ '^(b|c)' false — would match except for anchoring
```

O padrão da linguagem POSIX é descrito com muito mais detalhes abaixo.

A função `substring` com dois parâmetros, `substring(string from pattern)`, fornece a extração de uma subcadeia que corresponde a um padrão de expressão regular POSIX. Ela retorna nulo se não houver correspondência, caso contrário, a primeira parte do texto que correspondeu ao padrão. Mas se o padrão contiver quaisquer parênteses, a parte do texto que correspondeu à primeira subexpressão entre parênteses (aquela cuja chave esquerda vem primeiro) é devolvida. Você pode colocar parênteses ao redor de toda a expressão se quiser usar parênteses dentro dela sem desencadear essa exceção. Se você precisar de parênteses no padrão antes da subexpressão que você deseja extrair, consulte os parênteses não capturados descritos abaixo.

Alguns exemplos:

```
substring('foobar' from 'o.b')     oob
substring('foobar' from 'o(.)b')   o
```

A função `regexp_count` conta o número de lugares onde um padrão de expressão regular POSIX corresponde a uma string. Ela tem a sintaxe `regexp_count`(*`string`*, *`pattern`* [, *`start`* [, *`flags`* ])). *`pattern`* é procurado em *`string`*, normalmente a partir do início da string, mas se o parâmetro *`start`* for fornecido, então a partir daquele índice de caractere. O parâmetro *`flags`* é uma string de texto opcional que contém zero ou mais códigos de letra únicos que alteram o comportamento da função. Por exemplo, incluir `i` em *`flags`* especifica correspondência insensível ao caso. As bandeiras suportadas são descritas em [Tabela 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE "Table 9.24. ARE Embedded-Option Letters").

Alguns exemplos:

```
regexp_count('ABCABCAXYaxy', 'A.')          3
regexp_count('ABCABCAXYaxy', 'A.', 1, 'i')  4
```

A função `regexp_instr` retorna a posição inicial ou final da *`N`'ª ocorrência de um padrão de expressão regular POSIX em uma string, ou zero se não houver tal ocorrência. Ela tem a sintaxe `regexp_instr`(*`string`*, *`pattern`* [, *`start`* [, *`N`* [, *`endoption`* [, *`flags`* [, *`subexpr`* ]]]). *`pattern`* é pesquisado em *`string`*, normalmente desde o início da string, mas se o parâmetro *`start`* for fornecido, então começando a partir daquele índice de caractere. Se *`N`* for especificado, então o *`N`'ª ocorrência do padrão é localizada, caso contrário, a primeira ocorrência é localizada. Se o parâmetro *`endoption`* for omitido ou especificado como zero, a função retorna a posição do primeiro caractere da ocorrência. Caso contrário, *`endoption`* deve ser um, e a função retorna a posição do caractere que segue a ocorrência. O parâmetro *`flags`* é uma string de texto opcional que contém zero ou mais flags de uma letra que alteram o comportamento da função. As flags suportadas são descritas em [Tabela 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE "Table 9.24. ARE Embedded-Option Letters"). Para um padrão que contém subexpressões entre parênteses, *`subexpr`* é um inteiro que indica qual subexpressão é de interesse: o resultado identifica a posição da substring que corresponde a essa subexpressão. As subexpressões são numeradas na ordem de suas chaves iniciais. Quando *`subexpr`* é omitido ou zero, o resultado identifica a posição de toda a ocorrência, independentemente das subexpressões entre parênteses.

Alguns exemplos:

```
regexp_instr('number of your street, town zip, FR', '[^,]+', 1, 2)
                                   23
regexp_instr(string=>'ABCDEFGHI', pattern=>'(c..)(...)', start=>1, "N"=>1, endoption=>0, flags=>'i', subexpr=>2)
                                   6
```

A função `regexp_like` verifica se ocorre uma correspondência de um padrão de expressão regular POSIX em uma string, retornando booleano verdadeiro ou falso. Ela tem a sintaxe `regexp_like`(*`string`*, *`pattern`* [, *`flags`* ]). O parâmetro *`flags`* é uma string de texto opcional que contém zero ou mais códigos de letra única que alteram o comportamento da função. Os códigos suportados são descritos em [Tabela 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE "Table 9.24. ARE Embedded-Option Letters"). Esta função tem os mesmos resultados que o operador `~` se nenhuma bandeira for especificada. Se apenas a bandeira `i` for especificada, ela tem os mesmos resultados que o operador `~*`.

Alguns exemplos:

```
regexp_like('Hello World', 'world')       false
regexp_like('Hello World', 'world', 'i')  true
```

A função `regexp_match` retorna um array de texto com subdivisões correspondentes dentro do primeiro(s) correspondente(s) de um padrão de expressão regular POSIX em uma string. Ela tem a sintaxe `regexp_match`(*`string`*, *`pattern`* [, *`flags`* ]). Se não houver correspondência, o resultado é `NULL`. Se for encontrada uma correspondência e o *`pattern`* não contém subexpressões entre parênteses, então o resultado é um único elemento de texto contendo a subdivisão que corresponde a todo o padrão. Se for encontrada uma correspondência e o *`pattern`* contém subexpressões entre parênteses, então o resultado é um array de texto cujo *`n`*'o' elemento é a subdivisão que corresponde a *`n`*'o' subexpression entre parênteses do *`pattern`* (não contando as chaves não capturadoras; veja abaixo para detalhes). O parâmetro *`flags`* é uma string de texto opcional que contém zero ou mais flags de uma única letra que alteram o comportamento da função. As flags suportadas são descritas em [Tabela 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE "Table 9.24. ARE Embedded-Option Letters").

Alguns exemplos:

```
SELECT regexp_match('foobarbequebaz', 'bar.*que');
 regexp_match
--------------
 {barbeque}
(1 row)

SELECT regexp_match('foobarbequebaz', '(bar)(beque)');
 regexp_match
--------------
 {bar,beque}
(1 row)
```

### DICA

No caso comum em que você apenas deseja a subcadeia de caracteres correspondente inteira ou `NULL` sem correspondência, a melhor solução é usar `regexp_substr()`. No entanto, `regexp_substr()` existe apenas na versão PostgreSQL 15 e superior. Ao trabalhar em versões mais antigas, você pode extrair o primeiro elemento do resultado de `regexp_match()`, por exemplo:

```
SELECT (regexp_match('foobarbequebaz', 'bar.*que'))[1];
 regexp_match
--------------
 barbeque
(1 row)
```

A função `regexp_matches` retorna um conjunto de arrays de texto com substratos correspondentes dentro das correspondências de um padrão de expressão regular POSIX em uma string. Ela tem a mesma sintaxe que `regexp_match`. Esta função não retorna nenhuma linha se não houver correspondência, uma linha se houver uma correspondência e a bandeira `g` não for dada, ou *`N`* linhas se houver *`N`* correspondências e a bandeira `g` for dada. Cada linha devolvida é um array de texto contendo o inteiro substrato correspondente ou os substratos que correspondem às subexpressões entre parênteses do *`pattern`*, assim como descrito acima para `regexp_match`. `regexp_matches` aceita todas as bandeiras mostradas na [Tabela 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE "Table 9.24. ARE Embedded-Option Letters"), além da bandeira `g` que a comanda a retornar todas as correspondências, não apenas a primeira.

Alguns exemplos:

```
SELECT regexp_matches('foo', 'not there');
 regexp_matches
----------------
(0 rows)

SELECT regexp_matches('foobarbequebazilbarfbonk', '(b[^b]+)(b[^b]+)', 'g');
 regexp_matches
----------------
 {bar,beque}
 {bazil,barf}
(2 rows)
```

### DICA

Na maioria dos casos, `regexp_matches()` deve ser usado com a bandeira `g`, pois, se você só deseja a primeira correspondência, é mais fácil e eficiente usar `regexp_match()`. No entanto, `regexp_match()` existe apenas na versão PostgreSQL 10 e superior. Ao trabalhar em versões mais antigas, um truque comum é colocar uma chamada `regexp_matches()` em um sub-seletor, por exemplo:

```
SELECT col1, (SELECT regexp_matches(col2, '(bar)(beque)')) FROM tab;
```

Isso produz um array de texto se houver uma correspondência, ou `NULL` se não houver, o mesmo que o `regexp_match()` faria. Sem o subseleto, essa consulta não produziria nenhum resultado para as linhas da tabela sem correspondência, o que normalmente não é o comportamento desejado.

A função `regexp_replace` fornece substituição de novo texto para substratos que correspondem a padrões de expressão regular POSIX. Tem a sintaxe `regexp_replace`(*`string`*, *`pattern`*, *`replacement`* [, *`flags`* ]) ou `regexp_replace`(*`string`*, *`pattern`*, *`replacement`*, *`start`* [, *`N`* [, *`flags`* ])). A fonte *`string`* é devolvida inalterada se não houver correspondência ao *`pattern`*. Se houver correspondência, a string *`string`* é devolvida com a string *`replacement`* substituída pelo substrato correspondente. A string *`replacement`* pode conter `\`*`n`*, onde *`n`* é de 1 a 9, para indicar que a substring da fonte que corresponde ao *`n`*'o' subexpressão entre parênteses do padrão deve ser inserida, e pode conter `\&` para indicar que a substring que corresponde ao padrão inteiro deve ser inserida. Escreva `\\` se precisar colocar uma barra insira literal no texto de substituição. *`pattern`* é procurado em *`string`*, normalmente a partir do início da string, mas se o parâmetro *`start`* for fornecido, então a partir daquele índice de caractere. Por padrão, apenas a primeira correspondência do padrão é substituída. Se *`N`* for especificado e maior que zero, então a *`N`*'a' correspondência do padrão é substituída. Se a bandeira `g` for dada, ou se *`N`* for especificado e zero, então todas as correspondências na posição ou após a *`start`* são substituídas. (A bandeira `g` é ignorada quando *`N`* é especificado.) O parâmetro *`flags`* é uma string de texto opcional contendo zero ou mais flags de uma letra que alteram o comportamento da função. As flags suportadas (embora não `g`) são descritas em [Tabela 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE "Table 9.24. ARE Embedded-Option Letters").

Alguns exemplos:

```
regexp_replace('foobarbaz', 'b..', 'X')
                                   fooXbaz
regexp_replace('foobarbaz', 'b..', 'X', 'g')
                                   fooXX
regexp_replace('foobarbaz', 'b(..)', 'X\1Y', 'g')
                                   fooXarYXazY
regexp_replace('A PostgreSQL function', 'a|e|i|o|u', 'X', 1, 0, 'i')
                                   X PXstgrXSQL fXnctXXn
regexp_replace(string=>'A PostgreSQL function', pattern=>'a|e|i|o|u', replacement=>'X', start=>1, "N"=>3, flags=>'i')
                                   A PostgrXSQL function
```

A função `regexp_split_to_table` divide uma string usando um padrão de expressão regular POSIX como delimitador. Ela tem a sintaxe `regexp_split_to_table`(*`string`*, *`pattern`* [, *`flags`* ]). Se não houver correspondência com o *`pattern`*, a função retorna o *`string`*. Se houver pelo menos uma correspondência, para cada correspondência, ela retorna o texto do final da última correspondência (ou do início da string) até o início da correspondência. Quando não houver mais correspondências, ela retorna o texto do final da última correspondência até o final da string. O parâmetro *`flags`* é uma string de texto opcional que contém zero ou mais códigos de letra única que alteram o comportamento da função. `regexp_split_to_table` suporta os códigos descritos na [Tabela 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE "Table 9.24. ARE Embedded-Option Letters").

A função `regexp_split_to_array` se comporta da mesma forma que a `regexp_split_to_table`, exceto que `regexp_split_to_array` retorna seu resultado como um array de `text`. Ela tem a sintaxe `regexp_split_to_array`(*`string`*, *`pattern`* [, *`flags`* ]). Os parâmetros são os mesmos que para `regexp_split_to_table`.

Alguns exemplos:

```
SELECT foo FROM regexp_split_to_table('the quick brown fox jumps over the lazy dog', '\s+') AS foo;
  foo
-------
 the
 quick
 brown
 fox
 jumps
 over
 the
 lazy
 dog
(9 rows)

SELECT regexp_split_to_array('the quick brown fox jumps over the lazy dog', '\s+');
              regexp_split_to_array
-----------------------------------------------
 {the,quick,brown,fox,jumps,over,the,lazy,dog}
(1 row)

SELECT foo FROM regexp_split_to_table('the quick brown fox', '\s*') AS foo;
 foo
-----
 t
 h
 e
 q
 u
 i
 c
 k
 b
 r
 o
 w
 n
 f
 o
 x
(16 rows)
```

Como o último exemplo demonstra, as funções de divisão por padrão de expressão ignoram os correspondências de comprimento zero que ocorrem no início ou no final da string ou imediatamente após uma correspondência anterior. Isso é contrário à definição estrita de correspondência por padrão de expressão que é implementada pelas outras funções de padrão de expressão, mas geralmente é o comportamento mais conveniente na prática. Outros sistemas de software, como o Perl, utilizam definições semelhantes.

A função `regexp_substr` retorna a subcadeia que corresponde a um padrão de expressão regular POSIX, ou `NULL` se não houver correspondência. Ela tem a sintaxe `regexp_substr`(*`string`*, *`pattern`* [, *`start`* [, *`N`* [, *`flags`* [, *`subexpr`* ]]]). *`pattern`* é procurado em *`string`*, normalmente desde o início da cadeia, mas se o parâmetro *`start`* for fornecido, então começando a partir daquele índice de caractere. Se *`N`* for especificado, então o *`N`*'o correspondente do padrão é retornado, caso contrário, o primeiro correspondente é retornado. O parâmetro *`flags`* é uma cadeia de texto opcional que contém zero ou mais flags de uma única letra que alteram o comportamento da função. As flags suportadas são descritas em [Tabela 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE "Table 9.24. ARE Embedded-Option Letters"). Para um padrão que contém subexpressões entre parênteses, *`subexpr`* é um inteiro que indica qual subexpressão é de interesse: o resultado é a subcadeia que corresponde a essa subexpressão. As subexpressões são numeradas na ordem de suas chaves iniciais. Quando *`subexpr`* é omitido ou zero, o resultado é o correspondente inteiro, independentemente das subexpressões entre parênteses.

Alguns exemplos:

```
regexp_substr('number of your street, town zip, FR', '[^,]+', 1, 2)
                                    town zip
regexp_substr('ABCDEFGHI', '(c..)(...)', 1, 1, 'i', 2)
                                   FGH
```

#### 9.7.3.1. Detalhes da expressão regular [#](#POSIX-SYNTAX-DETAILS)

As expressões regulares do PostgreSQL são implementadas usando um pacote de software escrito por Henry Spencer. Grande parte da descrição das expressões regulares abaixo é copiada literalmente do manual dele.

As expressões regulares (ERs), conforme definidas no POSIX 1003.2, vêm em duas formas: ERs *extendidas* ou EREs (aproximadamente as de `egrep`) e ERs *básicas* ou BREs (aproximadamente as de `ed`). O PostgreSQL suporta ambas as formas, e também implementa algumas extensões que não estão no padrão POSIX, mas que se tornaram amplamente utilizadas devido à sua disponibilidade em linguagens de programação como Perl e Tcl. As ERs que usam essas extensões não-POSIX são chamadas de ERs *avançadas* ou AREs nesta documentação. As AREs são quase um conjunto superconjunto exato das EREs, mas as BREs têm várias incompatibilidades de notação (bem como sendo muito mais limitadas). Primeiro descrevemos as formas de ARE e ERE, observando características que se aplicam apenas às AREs, e depois descrevemos como as BREs diferem.

Nota

O PostgreSQL sempre presume que uma expressão regular segue as regras do ARE. No entanto, as regras mais limitadas ERE ou BRE podem ser escolhidas ao prependicar uma opção *incorporada* ao padrão RE, conforme descrito em [Seção 9.7.3.4](functions-matching.md#POSIX-METASYNTAX). Isso pode ser útil para compatibilidade com aplicativos que esperam exatamente as regras do POSIX 1003.2.

Uma expressão regular é definida como uma ou mais *ramos*, separados por `|`. Ela corresponde a qualquer coisa que corresponda a um dos ramos.

Um ramo é zero ou mais *átomos quantificados* ou *restrições*, concatenados. Ele corresponde a uma correspondência para o primeiro, seguido por uma correspondência para o segundo, etc.; um ramo vazio corresponde à string vazia.

Um átomo quantificado é um *átomo* possivelmente seguido por um único *quantificador*. Sem um quantificador, ele corresponde a uma correspondência para o átomo. Com um quantificador, ele pode corresponder a um número determinado de correspondências do átomo. Um *átomo* pode ser qualquer uma das possibilidades mostradas em [Tabela 9.17](functions-matching.md#POSIX-ATOMS-TABLE). Os quantificadores possíveis e seus significados são mostrados em [Tabela 9.18](functions-matching.md#POSIX-QUANTIFIERS-TABLE).

Uma *restrição* corresponde a uma cadeia vazia, mas só corresponde quando condições específicas são atendidas. Uma restrição pode ser usada onde um átomo poderia ser usado, exceto que não pode ser seguida por um quantificador. As restrições simples são mostradas em [Tabela 9.19](functions-matching.md#POSIX-CONSTRAINTS-TABLE); algumas restrições adicionais são descritas mais adiante.

**Tabela 9.17. Átomos de expressão regular**



<table border="1" class="table" summary="Regular Expression Atoms">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Atom
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     (
    </code>
    <em class="replaceable">
     <code>
      re
     </code>
    </em>
    <code class="literal">
     )
    </code>
   </td>
   <td>
    (onde
    <em class="replaceable">
     <code>
      re
     </code>
    </em>
    (qualquer expressão regular) corresponde a uma correspondência para
    <em class="replaceable">
     <code>
      re
     </code>
    </em>
    , com a partida anotada para possível relato
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     (?:
    </code>
    <em class="replaceable">
     <code>
      re
     </code>
    </em>
    <code class="literal">
     )
    </code>
   </td>
   <td>
    como acima, mas a partida não é registrada para relatórios
    <span class="quote">
     “
     <span class="quote">
      não capturador
     </span>
     ”
    </span>
    conjunto de parênteses) (apenas para AREs)
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     .
    </code>
   </td>
   <td>
    corresponda a qualquer caractere único
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     [
    </code>
    <em class="replaceable">
     <code>
      chars
     </code>
    </em>
    <code class="literal">
     ]
    </code>
   </td>
   <td>
    a
    <em class="firstterm">
     expressão de suporte
    </em>
    , correspondendo a qualquer uma das
    <em class="replaceable">
     <code>
      chars
     </code>
    </em>
    (ver
    <a class="xref" href="functions-matching.md#POSIX-BRACKET-EXPRESSIONS" title="9.7.3.2. Bracket Expressions">
     Seção 9.7.3.2
    </a>
    para mais detalhes)
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \
    </code>
    <em class="replaceable">
     <code>
      k
     </code>
    </em>
   </td>
   <td>
    (onde
    <em class="replaceable">
     <code>
      k
     </code>
    </em>
    é um caractere não alfanumérico) corresponda a esse caractere como um caractere comum, por exemplo,
    <code class="literal">
     \\
    </code>
    corresponda a um caractere barra invertida
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \
    </code>
    <em class="replaceable">
     <code>
      c
     </code>
    </em>
   </td>
   <td>
    onde
    <em class="replaceable">
     <code>
      c
     </code>
    </em>
    é alfanumérico (possivelmente seguido por outros caracteres) é um
    <em class="firstterm">
     fugir
    </em>
    , veja
    <a class="xref" href="functions-matching.md#POSIX-ESCAPE-SEQUENCES" title="9.7.3.3. Regular Expression Escapes">
     Seção 9.7.3.3
    </a>
    (Apenas para AREs; em EREs e BREs, isso corresponde a
    <em class="replaceable">
     <code>
      c
     </code>
    </em>
    )
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     {
    </code>
   </td>
   <td>
    quando seguido por outro caractere que não seja um dígito, corresponde ao caractere da brace esquerda
    <code class="literal">
     {
    </code>
    ; quando seguido por um dígito, é o início de um
    <em class="replaceable">
     <code>
      bound
     </code>
    </em>
    (veja abaixo)
   </td>
  </tr>
  <tr>
   <td>
    <em class="replaceable">
     <code>
      x
     </code>
    </em>
   </td>
   <td>
    onde
    <em class="replaceable">
     <code>
      x
     </code>
    </em>
    é um único personagem sem outra significância, que corresponde a esse personagem
   </td>
  </tr>
 </tbody>
</table>










Um RE não pode terminar com uma barra invertida (`\`).

Nota

Se você tiver desativado [standard_conforming_strings](runtime-config-compatible.md#GUC-STANDARD-CONFORMING-STRINGS), qualquer barra insira que você escrever em constantes de string literal precisará ser duplicada. Consulte [Seção 4.1.2.1](sql-syntax-lexical.md#SQL-SYNTAX-STRINGS) para obter mais informações.

**Tabela 9.18. Quantificadores de expressão regular**



<table border="1" class="table" summary="Regular Expression Quantifiers">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Quantifier
   </th>
   <th>
    Jogos
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     *
    </code>
   </td>
   <td>
    uma sequência de 0 ou mais correspondências do átomo
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     +
    </code>
   </td>
   <td>
    uma sequência de 1 ou mais jogos do átomo
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ?
    </code>
   </td>
   <td>
    uma sequência de 0 ou 1 correspondências do átomo
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     {
    </code>
    <em class="replaceable">
     <code>
      m
     </code>
    </em>
    <code class="literal">
     }
    </code>
   </td>
   <td>
    uma sequência de exatamente
    <em class="replaceable">
     <code>
      m
     </code>
    </em>
    jogos do átomo
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     {
    </code>
    <em class="replaceable">
     <code>
      m
     </code>
    </em>
    <code class="literal">
     ,}
    </code>
   </td>
   <td>
    uma sequência de
    <em class="replaceable">
     <code>
      m
     </code>
    </em>
    ou mais partidas do átomo
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     {
    </code>
    <em class="replaceable">
     <code>
      m
     </code>
    </em>
    <code class="literal">
     ,
    </code>
    <em class="replaceable">
     <code>
      n
     </code>
    </em>
    <code class="literal">
     }
    </code>
   </td>
   <td>
    uma sequência de
    <em class="replaceable">
     <code>
      m
     </code>
    </em>
    através
    <em class="replaceable">
     <code>
      n
     </code>
    </em>
    (incluindo) jogos do átomo;
    <em class="replaceable">
     <code>
      m
     </code>
    </em>
    não pode exceder
    <em class="replaceable">
     <code>
      n
     </code>
    </em>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     *?
    </code>
   </td>
   <td>
    versão não gananciosa de
    <code class="literal">
     *
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     +?
    </code>
   </td>
   <td>
    versão não gananciosa de
    <code class="literal">
     +
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ??
    </code>
   </td>
   <td>
    versão não gananciosa de
    <code class="literal">
     ?
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     {
    </code>
    <em class="replaceable">
     <code>
      m
     </code>
    </em>
    <code class="literal">
     }?
    </code>
   </td>
   <td>
    versão não gananciosa de
    <code class="literal">
     {
    </code>
    <em class="replaceable">
     <code>
      m
     </code>
    </em>
    <code class="literal">
     }
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     {
    </code>
    <em class="replaceable">
     <code>
      m
     </code>
    </em>
    <code class="literal">
     ,}?
    </code>
   </td>
   <td>
    versão não gananciosa de
    <code class="literal">
     {
    </code>
    <em class="replaceable">
     <code>
      m
     </code>
    </em>
    <code class="literal">
     ,}
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     {
    </code>
    <em class="replaceable">
     <code>
      m
     </code>
    </em>
    <code class="literal">
     ,
    </code>
    <em class="replaceable">
     <code>
      n
     </code>
    </em>
    <code class="literal">
     }?
    </code>
   </td>
   <td>
    versão não gananciosa de
    <code class="literal">
     {
    </code>
    <em class="replaceable">
     <code>
      m
     </code>
    </em>
    <code class="literal">
     ,
    </code>
    <em class="replaceable">
     <code>
      n
     </code>
    </em>
    <code class="literal">
     }
    </code>
   </td>
  </tr>
 </tbody>
</table>










Os formulários que utilizam `{`*`...`*`}` são conhecidos como *limites*. Os números *`m`* e *`n`* dentro de um limite são inteiros decimais não assinados com valores permitidos de 0 a 255, inclusive.

Os quantificadores (*não-ganídicos*) (disponíveis apenas em AREs) correspondem às mesmas possibilidades que seus equivalentes normais (*ganídicos*) correspondentes, mas preferem o menor número em vez do maior número de correspondências. Veja [Seção 9.7.3.5] para mais detalhes.

Nota

Um quantificador não pode seguir imediatamente outro quantificador, por exemplo, `**` é inválido. Um quantificador não pode iniciar uma expressão ou subexpressão ou seguir `^` ou `|`.

**Tabela 9.19. Restrições de expressão regular**



<table border="1" class="table" summary="Regular Expression Constraints">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Constraint
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     ^
    </code>
   </td>
   <td>
    jogos no início da cadeia
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     $
    </code>
   </td>
   <td>
    jogos no final da string
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     (?=
    </code>
    <em class="replaceable">
     <code>
      re
     </code>
    </em>
    <code class="literal">
     )
    </code>
   </td>
   <td>
    <em class="firstterm">
     olhar positivo para o futuro
    </em>
    correspondências em qualquer ponto
    <em class="replaceable">
     <code>
      re
     </code>
    </em>
    começa (apenas AREs)
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     (?!
    </code>
    <em class="replaceable">
     <code>
      re
     </code>
    </em>
    <code class="literal">
     )
    </code>
   </td>
   <td>
    <em class="firstterm">
     olhar negativo para o futuro
    </em>
    correspondências em qualquer ponto onde não há subdivisão correspondente
    <em class="replaceable">
     <code>
      re
     </code>
    </em>
    começa (apenas AREs)
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     (?&lt;=
    </code>
    <em class="replaceable">
     <code>
      re
     </code>
    </em>
    <code class="literal">
     )
    </code>
   </td>
   <td>
    <em class="firstterm">
     olhar positivo por trás
    </em>
    correspondências em qualquer ponto onde uma subcadeia correspondente
    <em class="replaceable">
     <code>
      re
     </code>
    </em>
    finais (apenas REs)
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     (?&lt;!
    </code>
    <em class="replaceable">
     <code>
      re
     </code>
    </em>
    <code class="literal">
     )
    </code>
   </td>
   <td>
    <em class="firstterm">
     olhar negativo
    </em>
    correspondências em qualquer ponto onde não há subdivisão correspondente
    <em class="replaceable">
     <code>
      re
     </code>
    </em>
    finais (apenas REs)
   </td>
  </tr>
 </tbody>
</table>










As restrições de olhar para frente e para trás não podem conter referências *atrás* (ver [Seção 9.7.3.3] (functions-matching.md#POSIX-ESCAPE-SEQUENCES "9.7.3.3. Regular Expression Escapes")), e todas as chaves de parênteses dentro delas são consideradas não capturadoras.

#### 9.7.3.2. Expressões de Braço [#](#POSIX-BRACKET-EXPRESSIONS)

Uma expressão de *bracket* é uma lista de caracteres fechada entre `[]`. Normalmente, ela corresponde a qualquer único caractere da lista (mas veja abaixo). Se a lista começar com `^`, ela corresponde a qualquer único caractere *não* do resto da lista. Se dois caracteres na lista forem separados por `-`, isso é uma abreviação para a faixa completa de caracteres entre esses dois (incluindo) na sequência de ordenação, por exemplo, `[0-9]` no ASCII corresponde a qualquer dígito decimal. É ilegal que dois intervalos compartilhem um ponto final, por exemplo, `a-c-e`. Os intervalos são muito dependentes da sequência de ordenação, portanto, os programas portáteis devem evitar depender deles.

Para incluir um literal `]` na lista, faça com que seja o primeiro caractere (após `^`, se este for usado). Para incluir um literal `-`, faça com que seja o primeiro ou último caractere, ou o segundo ponto final de uma faixa. Para usar um literal `-` como o primeiro ponto final de uma faixa, envolva-o em `[.` e `.]` para torná-lo um elemento de colocação (veja abaixo). Com exceção desses caracteres, algumas combinações que usam `[` (veja os próximos parágrafos) e escapamentos (apenas em AREs), todos os outros caracteres especiais perdem seu significado especial dentro de uma expressão em chaves. Em particular, `\` não é especial quando segue as regras de ERE ou BRE, embora seja especial (como introduzindo um escapamento) em AREs.

Dentro de uma expressão de colchetes, um elemento de cotação (um caractere, uma sequência de vários caracteres que se cota como se fosse um único caractere, ou um nome de sequência de cotação para qualquer um deles) encerrado em `[.` e `.]` representa a sequência de caracteres desse elemento de cotação. A sequência é tratada como um único elemento da lista da expressão de colchetes. Isso permite que uma expressão de colchetes que contenha um elemento de cotação de vários caracteres corresponda a mais de um caractere, por exemplo, se a sequência de cotação incluir um elemento de cotação `ch`, então o RE `[[.ch.]]*c` corresponderá aos primeiros cinco caracteres de `chchcc`.

Nota

Atualmente, o PostgreSQL não suporta elementos de ordenação de vários caracteres. Esta informação descreve um comportamento possível no futuro.

Dentro de uma expressão de colatância, um elemento de colatância encerrado em `[=` e `=]` é uma *classe de equivalência*, representando as sequências de caracteres de todos os elementos de colatância equivalentes a essa, incluindo a própria. (Se não houver outros elementos de colatância equivalentes, o tratamento é como se os delimitadores internos fossem `[.` e `.]`. Por exemplo, se `o` e `^` são os membros de uma classe de equivalência, então `[[=o=]]`, `[[=^=]]` e `[o^]` são todos sinônimos. Uma classe de equivalência não pode ser um ponto final de uma faixa.

Dentro de uma expressão entre chaves, o nome de uma classe de caracteres encerrada em `[:` e `:]` representa a lista de todos os caracteres pertencentes a essa classe. Uma classe de caracteres não pode ser usada como um ponto final de uma faixa. O padrão POSIX define esses nomes de classes de caracteres: `alnum` (letras e dígitos numéricos), `alpha` (letras), `blank` (espaço e tabulação), `cntrl` (caracteres de controle), `digit` (dígitos numéricos), `graph` (caracteres imprimíveis, exceto espaço), `lower` (letras minúsculas), `print` (caracteres imprimíveis, incluindo espaço), `punct` (ponto de pontuação), `space` (qualquer espaço em branco), `upper` (letras maiúsculas), e `xdigit` (dígitos hexadecimais). O comportamento dessas classes de caracteres padrão é geralmente consistente em todas as plataformas para caracteres no conjunto ASCII de 7 bits. Se um determinado caractere não ASCII é considerado pertencente a uma dessas classes, isso depende da *collation* que é usada para a função ou operador de expressão regular (ver [Seção 23.2](collation.md)), ou, por padrão, da configuração do locale `LC_CTYPE` do banco de dados (ver [Seção 23.1](locale.md)). A classificação de caracteres não ASCII pode variar em plataformas, mesmo em locais com nomes semelhantes. (Mas o locale `C` nunca considera que nenhum caractere não ASCII pertença a nenhuma dessas classes.) Além dessas classes de caracteres padrão, o PostgreSQL define a classe de caracteres `word`, que é a mesma que `alnum` mais o caractere underscore (`_`) e a classe de caracteres `ascii`, que contém exatamente o conjunto ASCII de 7 bits.

Existem dois casos especiais de expressões de colchetes: as expressões de colchetes `[[:<:]]` e `[[:>:]]` são restrições, correspondendo a cadeias vazias no início e no final de uma palavra, respectivamente. Uma palavra é definida como uma sequência de caracteres de palavra que não é precedida nem seguida por caracteres de palavra. Um caractere de palavra é qualquer caractere pertencente à classe de caracteres `word`, ou seja, qualquer letra, dígito ou sublinhado. Esta é uma extensão, compatível com, mas não especificada pelo POSIX 1003.2, e deve ser usada com cautela em software destinado a ser portátil para outros sistemas. As escapadas de restrições descritas abaixo são geralmente preferíveis; elas não são mais padrão, mas são mais fáceis de digitar.

#### 9.7.3.3. Fuertes de expressão regular [#](#POSIX-ESCAPE-SEQUENCES)

*Escapes* são sequências especiais que começam com `\`, seguidas por um caractere alfanumérico. Os escapes vêm em várias variedades: entrada de caracteres, abreviações de classe, escapes de restrição e referências de volta. Um `\`, seguido por um caractere alfanumérico, mas que não constitui uma saída válida, é ilegal em AREs. Em EREs, não há escapes: fora de uma expressão entre chaves, um `\`, seguido por um caractere alfanumérico, simplesmente representa esse caractere como um caractere comum, e dentro de uma expressão entre chaves, `\` é um caractere comum. (Este último é a incompatibilidade real entre EREs e AREs.)

*Evasões de entrada de caracteres* existem para facilitar a especificação de caracteres não imprimíveis e outros caracteres inconvenientes em REs. Eles são mostrados em [Tabela 9.20](functions-matching.md#POSIX-CHARACTER-ENTRY-ESCAPES-TABLE).

*Evasões de abreviação de classe* fornecem abreviações para certas classes de caracteres comumente usadas. Elas são mostradas em [Tabela 9.21](functions-matching.md#POSIX-CLASS-SHORTHAND-ESCAPES-TABLE).

Um *escape de restrição* é uma restrição que corresponde à string vazia se condições específicas forem atendidas, escrita como um escape. Eles são mostrados em [Tabela 9.22](functions-matching.md#POSIX-CONSTRAINT-ESCAPES-TABLE).

Uma *referência de volta* (`\`*`n`*) corresponde à mesma cadeia de caracteres correspondida pela subexpressão anterior entre parênteses especificada pelo número *`n`* (ver [Tabela 9.23](functions-matching.md#POSIX-CONSTRAINT-BACKREF-TABLE "Table 9.23. Regular Expression Back References")). Por exemplo, `([bc])\1` corresponde a `bb` ou `cc`, mas não a `bc` ou `cb`. A subexpressão deve preceder inteiramente a referência de volta no RE. As subexpressões são numeradas na ordem de suas chaves iniciais. As chaves não capturadoras não definem subexpressões. A referência de volta considera apenas os caracteres de cadeia de caracteres correspondidos pela subexpressão referenciada, e não quaisquer restrições contidas nela. Por exemplo, `(^\d)\1` corresponderá a `22`.

**Tabela 9.20. Fuites de entrada de caracteres de expressão regular**



<table border="1" class="table" summary="Regular Expression Character-Entry Escapes">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Escape
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     \a
    </code>
   </td>
   <td>
    caractere de alerta (sino), como em C
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \b
    </code>
   </td>
   <td>
    backspace, como em C
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \B
    </code>
   </td>
   <td>
    sinônimo de barra invertida (
    <code class="literal">
     \
    </code>
    ) para ajudar a reduzir a necessidade de barras inclinadas dobrar
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \c
    </code>
    <em class="replaceable">
     <code>
      X
     </code>
    </em>
   </td>
   <td>
    (onde
    <em class="replaceable">
     <code>
      X
     </code>
    </em>
    (qualquer caractere) o caractere cujos 5 bits de menor ordem são iguais aos da
    <em class="replaceable">
     <code>
      X
     </code>
    </em>
    , e cujos outros bits são todos zero
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \e
    </code>
   </td>
   <td>
    o personagem cujo nome de sequência de correspondência é
    <code class="literal">
     ESC
    </code>
    , ou, caso contrário, o caractere com valor octal
    <code class="literal">
     033
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \f
    </code>
   </td>
   <td>
    forma de alimentação, como em C
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \n
    </code>
   </td>
   <td>
    newline, como em C
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \r
    </code>
   </td>
   <td>
    retorno de carro, como em C
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \t
    </code>
   </td>
   <td>
    semelhante a uma aba horizontal, como em C
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \u
    </code>
    <em class="replaceable">
     <code>
      wxyz
     </code>
    </em>
   </td>
   <td>
    (onde
    <em class="replaceable">
     <code>
      wxyz
     </code>
    </em>
    é exatamente quatro dígitos hexadecimais) o caractere cujo valor hexadecimal é
    <code class="literal">
     0x
    </code>
    <em class="replaceable">
     <code>
      wxyz
     </code>
    </em>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \U
    </code>
    <em class="replaceable">
     <code>
      stuvwxyz
     </code>
    </em>
   </td>
   <td>
    (onde
    <em class="replaceable">
     <code>
      stuvwxyz
     </code>
    </em>
    é exatamente oito dígitos hexadecimais. O caractere cujo valor hexadecimal é
    <code class="literal">
     0x
    </code>
    <em class="replaceable">
     <code>
      stuvwxyz
     </code>
    </em>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \v
    </code>
   </td>
   <td>
    semelhante a uma aba vertical, como em C
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \x
    </code>
    <em class="replaceable">
     <code>
      hhh
     </code>
    </em>
   </td>
   <td>
    (onde
    <em class="replaceable">
     <code>
      hhh
     </code>
    </em>
    é qualquer sequência de dígitos hexadecimais) o caractere cujo valor hexadecimal é
    <code class="literal">
     0x
    </code>
    <em class="replaceable">
     <code>
      hhh
     </code>
    </em>
    (um único caractere, não importa quantos dígitos hexadecimais sejam usados)
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \0
    </code>
   </td>
   <td>
    o caráter cujo valor é
    <code class="literal">
     0
    </code>
    (o byte nulo)
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \
    </code>
    <em class="replaceable">
     <code>
      xy
     </code>
    </em>
   </td>
   <td>
    (onde
    <em class="replaceable">
     <code>
      xy
     </code>
    </em>
    é exatamente dois dígitos óctal, e não é um
    <em class="firstterm">
     referência de volta
    </em>
    ) o personagem cujo valor octal é
    <code class="literal">
     0
    </code>
    <em class="replaceable">
     <code>
      xy
     </code>
    </em>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \
    </code>
    <em class="replaceable">
     <code>
      xyz
     </code>
    </em>
   </td>
   <td>
    (onde
    <em class="replaceable">
     <code>
      xyz
     </code>
    </em>
    é exatamente três dígitos óctal, e não é um
    <em class="firstterm">
     referência de volta
    </em>
    ) o personagem cujo valor octal é
    <code class="literal">
     0
    </code>
    <em class="replaceable">
     <code>
      xyz
     </code>
    </em>
   </td>
  </tr>
 </tbody>
</table>










Os dígitos hexadecimais são `0`-`9`, `a`-`f` e `A`-`F`. Os dígitos óctal são `0`-`7`.

Saídas de entrada de caracteres numéricos que especificam valores fora do intervalo ASCII (0–127) têm significados dependentes do codificação do banco de dados. Quando a codificação é UTF-8, os valores de escape são equivalentes a pontos de código Unicode, por exemplo, `\u1234` significa o caractere `U+1234`. Para outras codificações multibyte, as saídas de entrada de caracteres geralmente especificam apenas a concatenação dos valores de byte para o caractere. Se o valor de escape não corresponder a nenhum caractere legal na codificação do banco de dados, não será gerado nenhum erro, mas nunca corresponderá a nenhum dado.

As escapas de entrada de caracteres são sempre tratadas como caracteres comuns. Por exemplo, `\135` é `]` em ASCII, mas `\135` não termina uma expressão de chaves.

**Tabela 9.21. Evasões abreviadas de classe de expressão regular**



<table border="1" class="table" summary="Regular Expression Class-Shorthand Escapes">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Escape
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     \d
    </code>
   </td>
   <td>
    corresponda a qualquer dígito, como
    <code class="literal">
     [[:digit:]]
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \s
    </code>
   </td>
   <td>
    corresponda a qualquer caractere de espaço em branco, como
    <code class="literal">
     [[:space:]]
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \w
    </code>
   </td>
   <td>
    corresponda a qualquer caractere de palavra, como
    <code class="literal">
     [[:word:]]
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \D
    </code>
   </td>
   <td>
    corresponda a qualquer caractere que não seja um dígito, como
    <code class="literal">
     [^[:digit:]]
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \S
    </code>
   </td>
   <td>
    corresponda a qualquer caractere que não seja espaço em branco, como
    <code class="literal">
     [^[:space:]]
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \W
    </code>
   </td>
   <td>
    corresponda a qualquer caractere não-alfabético, como
    <code class="literal">
     [^[:word:]]
    </code>
   </td>
  </tr>
 </tbody>
</table>










As fórmulas de escape de abreviação de classe também funcionam dentro de expressões de chaves, embora as definições mostradas acima não sejam totalmente sintaticamente válidas nesse contexto. Por exemplo, `[a-c\d]` é equivalente a `[a-c[:digit:]]`.

**Tabela 9.22. Evasões de restrições de expressão regular**



<table border="1" class="table" summary="Regular Expression Constraint Escapes">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Escape
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     \A
    </code>
   </td>
   <td>
    encontra-se apenas no início da cadeia
    <a class="xref" href="functions-matching.md#POSIX-MATCHING-RULES" title="9.7.3.5. Regular Expression Matching Rules">
     Seção 9.7.3.5
    </a>
    para que isso se diferencia de
    <code class="literal">
     ^
    </code>
    )
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \m
    </code>
   </td>
   <td>
    encontra-se apenas no início de uma palavra
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \M
    </code>
   </td>
   <td>
    encontra-se apenas no final de uma palavra
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \y
    </code>
   </td>
   <td>
    encontra-se apenas no início ou no final de uma palavra
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \Y
    </code>
   </td>
   <td>
    correspondência apenas em um ponto que não seja o início ou o fim de uma palavra
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \Z
    </code>
   </td>
   <td>
    encontra-se apenas no final da string (veja
    <a class="xref" href="functions-matching.md#POSIX-MATCHING-RULES" title="9.7.3.5. Regular Expression Matching Rules">
     Seção 9.7.3.5
    </a>
    para que isso se diferencia de
    <code class="literal">
     $
    </code>
    )
   </td>
  </tr>
 </tbody>
</table>










Uma palavra é definida conforme especificado nos padrões de `[[:<:]]` e `[[:>:]]` acima. Fuga de restrição é ilegal dentro das expressões de chaves.

**Tabela 9.23. Referências de expressão regular de volta**



<table border="1" class="table" summary="Regular Expression Back References">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Escape
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     \
    </code>
    <em class="replaceable">
     <code>
      m
     </code>
    </em>
   </td>
   <td>
    (onde
    <em class="replaceable">
     <code>
      m
     </code>
    </em>
    é um dígito não nulo) uma referência de volta ao
    <em class="replaceable">
     <code>
      m
     </code>
    </em>
    "subexpressão
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     \
    </code>
    <em class="replaceable">
     <code>
      mnn
     </code>
    </em>
   </td>
   <td>
    (onde
    <em class="replaceable">
     <code>
      m
     </code>
    </em>
    é um dígito não nulo, e
    <em class="replaceable">
     <code>
      nn
     </code>
    </em>
    são mais dígitos, e o valor decimal
    <em class="replaceable">
     <code>
      mnn
     </code>
    </em>
    não é maior que o número de parênteses de fechamento vistos até agora) uma referência de volta ao
    <em class="replaceable">
     <code>
      mnn
     </code>
    </em>
    "subexpressão
   </td>
  </tr>
 </tbody>
</table>










Nota

Há uma ambiguidade inerente entre as saídas de entrada de caracteres octal e as referências de volta, que é resolvida pelas seguintes heurísticas, conforme mencionado acima. Um zero inicial sempre indica uma saída de escape octal. Um único dígito não nulo, não seguido por outro dígito, é sempre considerado uma referência de volta. Uma sequência de vários dígitos que não começa com um zero é considerada uma referência de volta se vier após uma subexpressão adequada (ou seja, o número está na faixa legal para uma referência de volta), e, caso contrário, é considerada octal.

#### 9.7.3.4. Metasintaxe de expressão regular [#](#POSIX-METASYNTAX)

Além da sintaxe principal descrita acima, existem algumas formas especiais e facilidades sintáticas variadas disponíveis.

Um RE pode começar com um dos dois prefixos especiais de *director*. Se um RE começar com `***:`, o resto do RE é considerado um ARE. (Isso normalmente não tem efeito no PostgreSQL, uma vez que os REs são assumidos como AREs; mas tem efeito se o modo ERE ou BRE tivesse sido especificado pelo parâmetro *`flags`* para uma função de regex.) Se um RE começar com `***=`, o resto do RE é considerado uma string literal, com todos os caracteres considerados caracteres ordinários.

Um RE pode começar com *opções embutidas*: uma sequência `(?`*`xyz`*`)` (onde *`xyz`* é um ou mais caracteres alfabéticos) especifica opções que afetam o resto do RE. Essas opções substituem quaisquer opções previamente determinadas — em particular, elas podem substituir o comportamento de sensibilidade ao caso implícito por um operador regex, ou o parâmetro *`flags`* para uma função regex. As letras de opção disponíveis são mostradas em [Tabela 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE "Table 9.24. ARE Embedded-Option Letters"). Note que essas mesmas letras de opção são usadas nos parâmetros *`flags`* de funções regex.

**Tabela 9.24. Cartas de opção embutidas da ARE**



<table border="1" class="table" summary="ARE Embedded-Option Letters">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Option
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     b
    </code>
   </td>
   <td>
    resto do RE é um BRE
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     c
    </code>
   </td>
   <td>
    correspondência sensível ao caso (supere o tipo do operador)
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     e
    </code>
   </td>
   <td>
    resto de RE é um ERE
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     i
    </code>
   </td>
   <td>
    correspondência não sensível ao caso (consulte
    <a class="xref" href="functions-matching.md#POSIX-MATCHING-RULES" title="9.7.3.5. Regular Expression Matching Rules">
     Seção 9.7.3.5
    </a>
    ) (supere o tipo do operador)
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     m
    </code>
   </td>
   <td>
    sinônimo histórico de
    <code class="literal">
     n
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     n
    </code>
   </td>
   <td>
    correspondência sensível a nova linha (consulte
    <a class="xref" href="functions-matching.md#POSIX-MATCHING-RULES" title="9.7.3.5. Regular Expression Matching Rules">
     Seção 9.7.3.5
    </a>
    )
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     p
    </code>
   </td>
   <td>
    correspondência sensível a novas linhas parciais (consulte
    <a class="xref" href="functions-matching.md#POSIX-MATCHING-RULES" title="9.7.3.5. Regular Expression Matching Rules">
     Seção 9.7.3.5
    </a>
    )
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     q
    </code>
   </td>
   <td>
    o resto de RE é literal (
    <span class="quote">
     “
     <span class="quote">
      citado
     </span>
     ”
    </span>
    ) string, todos os caracteres comuns
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     s
    </code>
   </td>
   <td>
    correspondência não sensível a novas linhas (padrão)
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     t
    </code>
   </td>
   <td>
    sintaxe apertada (padrão; veja abaixo)
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     w
    </code>
   </td>
   <td>
    inverso sensível a nova linha não-espaçada (
    <span class="quote">
     “
     <span class="quote">
      estranho
     </span>
     ”
    </span>
    ) correspondência (ver
    <a class="xref" href="functions-matching.md#POSIX-MATCHING-RULES" title="9.7.3.5. Regular Expression Matching Rules">
     Seção 9.7.3.5
    </a>
    )
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     x
    </code>
   </td>
   <td>
    sintaxe expandida (veja abaixo)
   </td>
  </tr>
 </tbody>
</table>










As opções embutidas entram em vigor no ponto `)` que termina a sequência. Elas podem aparecer apenas no início de um ARE (após o diretor `***:`, se houver).

Além da sintaxe usual (*fechada*) do RE, na qual todos os caracteres são significativos, existe uma sintaxe *expansível*, disponível especificando a opção `x` embutida. Na sintaxe expansível, os caracteres de espaço em branco no RE são ignorados, assim como todos os caracteres entre um `#` e a próxima linha nova (ou o fim do RE). Isso permite a formatação e comentário de um RE complexo. Existem três exceções a essa regra básica:

* um caractere de espaço em branco ou `#` precedido por `\` é mantido
* espaço em branco ou `#` dentro de uma expressão entre chaves é mantido
* espaço em branco e comentários não podem aparecer dentro de símbolos de vários caracteres, como `(?:`

Para esse propósito, os caracteres de espaço em branco, tabulação, nova linha e qualquer caractere que pertença à classe de caracteres *`space`* são em branco.

Finalmente, em uma ARE, as expressões fora de colchetes, a sequência `(?#`*`ttt`*`)` (onde *`ttt`* é qualquer texto que não contenha um `)`) é um comentário, completamente ignorado. Novamente, isso não é permitido entre os caracteres de símbolos de vários caracteres, como `(?:`. Tais comentários são mais um artefato histórico do que uma facilidade útil, e seu uso é desaconselhado; use a sintaxe expandida em vez disso.

*Nenhuma* dessas extensões de sintaxe metassintática está disponível se um diretor inicial `***=` tiver especificado que a entrada do usuário seja tratada como uma string literal e não como um RE.

#### 9.7.3.5. Regras de correspondência por expressão regular [#](#POSIX-MATCHING-RULES)

Caso um RE possa corresponder a mais de uma subcadeia de uma string dada, o RE corresponderá àquela que começa mais cedo na string. Se o RE puder corresponder a mais de uma subcadeia começando nesse ponto, será tomada a correspondência mais longa possível ou a correspondência mais curta possível, dependendo se o RE é *greedy* ou *não-greedy*.

Se um RE é ganancioso ou não é determinado pelas seguintes regras:

* A maioria dos átomos e todas as restrições não possuem atributo de ganância (porque não podem corresponder a quantidades variáveis de texto de qualquer maneira).
* Adicionar chaves ao redor de um RE não altera sua ganância.
* Um átomo quantificado com um quantificador de repetição fixa (`{`*`m`*`}` ou `{`*`m`*`}?`) tem a mesma ganância (possivelmente nenhuma) que o próprio átomo.
* Um átomo quantificado com outros quantificadores normais (incluindo `{`*`m`*`,`*`n`*`}` com *`m`* igual a *`n`*) é ganancioso (prefere a correspondência mais longa).
* Um átomo quantificado com um quantificador não ganancioso (incluindo `{`*`m`*`,`*`n`*`}?` com *`m`* igual a *`n`*) é não ganancioso (prefere a correspondência mais curta).
* Um ramo — ou seja, um RE que não possui o operador `|` de nível superior — tem a mesma ganância que o primeiro átomo quantificado nele que possui um atributo de ganância.
* Um RE composto por duas ou mais ramificações conectadas pelo operador `|` é sempre ganancioso.

As regras acima associam a ganância a atributos não apenas a átomos quantificados individuais, mas também a ramos e REs inteiros que contêm átomos quantificados. O que isso significa é que a correspondência é feita de tal forma que o ramo ou o RE inteiro corresponde à subexpressão mais longa ou mais curta possível *como um todo*. Uma vez determinada a extensão da correspondência total, a parte dela que corresponde a qualquer subexpressão específica é determinada com base no atributo de ganância dessa subexpressão, com subexpressões que começam mais cedo no RE tendo prioridade sobre aquelas que começam mais tarde.

Um exemplo do que isso significa:

```
SELECT SUBSTRING('XY1234Z', 'Y*([0-9]{1,3})');
Result: 123
SELECT SUBSTRING('XY1234Z', 'Y*?([0-9]{1,3})');
Result: 1
```

No primeiro caso, o RE como um todo é ganancioso porque `Y*` é ganancioso. Ele pode corresponder começando no `Y`, e corresponde à cadeia mais longa possível que começa lá, ou seja, `Y123`. A saída é a parte entre parênteses disso, ou `123`. No segundo caso, o RE como um todo é não ganancioso porque `Y*?` é não ganancioso. Ele pode corresponder começando no `Y`, e corresponde à cadeia mais curta possível que começa lá, ou seja, `Y1`. A subexpressão `[0-9]{1,3}` é gananciosa, mas não pode mudar a decisão sobre o comprimento total da correspondência; então ela é forçada a corresponder apenas a `1`.

Em suma, quando um RE contém tanto expressões subexpressões gananciosas quanto não gananciosas, o comprimento total da correspondência é ou o mais longo possível ou o mais curto possível, de acordo com o atributo atribuído ao RE como um todo. Os atributos atribuídos às subexpressões afetam apenas o quanto dessa correspondência eles são permitidos para "comer" em relação uma à outra.

Os quantificadores `{1,1}` e `{1,1}?` podem ser usados para forçar ganância ou falta de ganância, respectivamente, em uma subexpressão ou em um RE inteiro. Isso é útil quando você precisa que o RE inteiro tenha um atributo de ganância diferente do que é deduzido de seus elementos. Como exemplo, suponha que estamos tentando separar uma string que contém alguns dígitos em dígitos e as partes antes e depois deles. Podemos tentar fazer isso assim:

```
SELECT regexp_match('abc01234xyz', '(.*)(\d+)(.*)');
Result: {abc0123,4,xyz}
```

Isso não funcionou: o primeiro `.*` é ganancioso, então ele "come" o máximo que pode, deixando o `\d+` para se ajustar no último possível lugar, o último dígito. Talvez possamos tentar corrigir isso, tornando-o não ganancioso:

```
SELECT regexp_match('abc01234xyz', '(.*?)(\d+)(.*)');
Result: {abc,0,""}
```

Isso também não funcionou, porque agora o RE como um todo é não-gancioso e, portanto, termina a partida como um todo o mais rápido possível. Podemos obter o que queremos, forçando o RE como um todo a ser ganancioso:

```
SELECT regexp_match('abc01234xyz', '(?:(.*?)(\d+)(.*)){1,1}');
Result: {abc,01234,xyz}
```

Controlar a ganância geral do RE separadamente da ganância dos seus componentes permite uma grande flexibilidade no manuseio de padrões de comprimento variável.

Ao decidir o que é uma partida mais longa ou mais curta, as partidas são medidas em caracteres, não em elementos de colagem. Uma string vazia é considerada mais longa do que nenhuma partida. Por exemplo: `bb*` corresponde aos três caracteres do meio de `abbbc`; `(week|wee)(night|knights)` corresponde a todos os dez caracteres de `weeknights`; quando `(.*).*` é correspondido a `abc`, a subexpressão entre parênteses corresponde a todos os três caracteres; e quando `(a*)*` é correspondido a `bc`, tanto o RE inteiro quanto a subexpressão entre parênteses correspondem a uma string vazia.

Se a correspondência independente de caso for especificada, o efeito é como se todas as distinções de caso tivessem desaparecido do alfabeto. Quando um alfabeto que existe em múltiplos casos aparece como um caractere comum fora de uma expressão em chaves, ele é efetivamente transformado em uma expressão em chaves que contém ambos os casos, por exemplo, `x` se torna `[xX]`. Quando aparece dentro de uma expressão em chaves, todas as contrapartes de caso dele são adicionadas à expressão em chaves, por exemplo, `[x]` se torna `[xX]` e `[^x]` se torna `[^xX]`.

Se a correspondência sensível a nova linha for especificada, `.` e expressões de chaves usando `^` nunca corresponderão ao caractere de nova linha (assim, as correspondências não cruzarão linhas, a menos que o RE inclua explicitamente uma nova linha) e `^` e `$` corresponderão à string vazia após e antes de uma nova linha, respectivamente, além de corresponderem no início e no fim da string, respectivamente. Mas as escapadas de classe de caracteres `\A` e `\Z` continuarão a corresponder ao início ou fim da string *apenas*. Além disso, as abreviações de classe de caracteres `\D` e `\W` corresponderão a uma nova linha, independentemente deste modo. (Antes do PostgreSQL 14, elas não correspondiam a novas linhas quando no modo sensível a nova linha. Escreva `[^[:digit:]]` ou `[^[:word:]]` para obter o comportamento antigo.)

Se a correspondência parcial sensível a novas linhas for especificada, isso afeta `.` e expressões de chaves como na correspondência sensível a novas linhas, mas não `^` e `$`.

Se a correspondência inversa sensível a novas linhas for especificada, isso afeta `^` e `$` como na correspondência sensível a novas linhas, mas não `.` e expressões de chaves. Isso não é muito útil, mas é fornecido por simetria.

#### 9.7.3.6. Limites e compatibilidade [#](#POSIX-LIMITS-COMPATIBILITY)

Não há uma limitação específica para o comprimento dos REs nesta implementação. No entanto, os programas destinados a serem altamente portáteis não devem utilizar REs com mais de 256 bytes, pois uma implementação compatível com POSIX pode se recusar a aceitar tais REs.

A única característica dos AREs que é realmente incompatível com os EREs POSIX é que `\` não perde seu significado especial dentro das expressões entre colchetes. Todas as outras características dos AREs usam sintaxe que é ilegal ou tem efeitos indefinidos ou não especificados nos EREs POSIX; a sintaxe `***` dos diretores, da mesma forma, está fora da sintaxe POSIX tanto para BREs quanto para EREs.

Muitas das extensões do ARE foram emprestadas do Perl, mas algumas foram alteradas para limpá-las, e algumas extensões do Perl não estão presentes. As incompatibilidades de destaque incluem `\b`, `\B`, a falta de tratamento especial para uma nova linha final, a adição de expressões de chaves complementares às coisas afetadas por correspondência sensível à nova linha, as restrições em relação a parênteses e referências de volta nas restrições de pré-visualização/pré-visualização e a semântica de correspondência mais longa/mais curta (em vez de correspondência inicial)

#### 9.7.3.7. Expressões Regulares Básicas [#](#POSIX-BASIC-REGEXES)

As BREs diferem das EREs em vários aspectos. Nas BREs, `|`, `+` e `?` são caracteres comuns e não há equivalente para sua funcionalidade. Os delimitadores para limites são `\{` e `\}`, com `{` e `}` sendo, por si sós, caracteres comuns. As chaves para subexpressões aninhadas são `\(` e `\)`, com `(` e `)` sendo, por si sós, caracteres comuns. `^` é um caractere comum, exceto no início do RE ou no início de uma subexpressão entre chaves, `$` é um caractere comum, exceto no final do RE ou no final de uma subexpressão entre chaves, e `*` é um caractere comum se aparecer no início do RE ou no início de uma subexpressão entre chaves (após um possível `^` inicial). Por fim, as referências de volta de um único dígito estão disponíveis, e `\<` e `\>` são sinônimos de `[[:<:]]` e `[[:>:]]`, respectivamente; não há outras escapadas disponíveis nas BREs.

#### 9.7.3.8. Diferenças em relação ao Padrão SQL e ao XQuery [#](#POSIX-VS-XQUERY)

Desde o SQL:2008, o padrão SQL inclui operadores e funções de expressão regular que realizam a correspondência de padrões de acordo com o padrão de expressão regular XQuery:

* `LIKE_REGEX`
* `OCCURRENCES_REGEX`
* `POSITION_REGEX`
* `SUBSTRING_REGEX`
* `TRANSLATE_REGEX`

O PostgreSQL não implementa atualmente esses operadores e funções. Você pode obter uma funcionalidade aproximadamente equivalente em cada caso, conforme mostrado em [Tabela 9.25] ((functions-matching.md#FUNCTIONS-REGEXP-SQL-TABLE "Table 9.25. Regular Expression Functions Equivalencies")). (Várias cláusulas opcionais em ambos os lados foram omitidas nesta tabela.)

**Tabela 9.25. Equivalências de funções de expressão regular**



<table border="1" class="table" summary="Regular Expression Functions Equivalencies">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    SQL standard
   </th>
   <th>
    <span class="productname">
     PostgreSQL
    </span>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     LIKE_REGEX
     <em class="replaceable">
      <code>
       pattern
      </code>
     </em>
    </code>
   </td>
   <td>
    <code class="literal">
     regexp_like(
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     ,
     <em class="replaceable">
      <code>
       pattern
      </code>
     </em>
     )
    </code>
    or
    <code class="literal">
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     ~
     <em class="replaceable">
      <code>
       pattern
      </code>
     </em>
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     OCCURRENCES_REGEX(
     <em class="replaceable">
      <code>
       pattern
      </code>
     </em>
     IN
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     )
    </code>
   </td>
   <td>
    <code class="literal">
     regexp_count(
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     ,
     <em class="replaceable">
      <code>
       pattern
      </code>
     </em>
     )
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     POSITION_REGEX(
     <em class="replaceable">
      <code>
       pattern
      </code>
     </em>
     IN
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     )
    </code>
   </td>
   <td>
    <code class="literal">
     regexp_instr(
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     ,
     <em class="replaceable">
      <code>
       pattern
      </code>
     </em>
     )
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SUBSTRING_REGEX(
     <em class="replaceable">
      <code>
       pattern
      </code>
     </em>
     IN
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     )
    </code>
   </td>
   <td>
    <code class="literal">
     regexp_substr(
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     ,
     <em class="replaceable">
      <code>
       pattern
      </code>
     </em>
     )
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     TRANSLATE_REGEX(
     <em class="replaceable">
      <code>
       pattern
      </code>
     </em>
     IN
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     WITH
     <em class="replaceable">
      <code>
       replacement
      </code>
     </em>
     )
    </code>
   </td>
   <td>
    <code class="literal">
     regexp_replace(
     <em class="replaceable">
      <code>
       string
      </code>
     </em>
     ,
     <em class="replaceable">
      <code>
       pattern
      </code>
     </em>
     ,
     <em class="replaceable">
      <code>
       replacement
      </code>
     </em>
     )
    </code>
   </td>
  </tr>
 </tbody>
</table>










Funções de expressão regular semelhantes às fornecidas pelo PostgreSQL também estão disponíveis em vários outros implementações do SQL, enquanto as funções padrão do SQL não são tão amplamente implementadas. Alguns dos detalhes da sintaxe da expressão regular provavelmente diferirão em cada implementação.

Os operadores e funções padrão do SQL utilizam expressões regulares XQuery, que são bastante próximas à sintaxe ARE descrita acima. As diferenças notáveis entre o recurso de expressão regular baseado em POSIX existente e as expressões regulares XQuery incluem:

* A subtração da classe de caracteres XQuery não é suportada. Um exemplo disso é o uso do seguinte para corresponder apenas a consoantes em inglês: `[a-z-[aeiou]]`.
* As abreviações de classe de caracteres XQuery `\c`, `\C`, `\i` e `\I` não são suportadas.
* Os elementos de classe de caracteres XQuery que usam `\p{UnicodeProperty}` ou o inverso `\P{UnicodeProperty}` não são suportados.
* O POSIX interpreta as classes de caracteres como `\w` (ver [Tabela 9.21](functions-matching.md#POSIX-CLASS-SHORTHAND-ESCAPES-TABLE "Table 9.21. Regular Expression Class-Shorthand Escapes")) de acordo com o local prevalente (que você pode controlar anexando uma cláusula `COLLATE` ao operador ou função). O XQuery especifica essas classes por referência a propriedades de caracteres Unicode, então o comportamento equivalente é obtido apenas com um local que siga as regras Unicode.
* O padrão SQL (não o próprio XQuery) tenta atender a mais variantes de “nova linha” do que o POSIX. As opções de correspondência sensíveis a nova linha descritas acima consideram apenas ASCII NL (`\n`) como uma nova linha, mas o SQL nos faria tratar CR (`\r`), CRLF (`\r\n`) (uma nova linha de estilo Windows) e alguns caracteres exclusivos do Unicode como novas linhas também. Notavelmente, `.` e `\s` devem contar `\r\n` como um caractere e não dois, de acordo com o SQL.
* Das escapadas de entrada de caracteres descritas em [Tabela 9.20](functions-matching.md#POSIX-CHARACTER-ENTRY-ESCAPES-TABLE "Table 9.20. Regular Expression Character-Entry Escapes"), o XQuery suporta apenas `\n`, `\r` e `\t`.
* O XQuery não suporta a sintaxe `[:name:]` para classes de caracteres dentro de expressões de chaves.
* O XQuery não tem restrições de pré-visualização ou pós-visualização, nem nenhuma das escapas de restrição descritas em [Tabela 9.22](functions-matching.md#POSIX-CONSTRAINT-ESCAPES-TABLE "Table 9.22. Regular Expression Constraint Escapes").
* As formas de sintaxe metassintática descritas em [Seção 9.7.3.4](functions-matching.md#POSIX-METASYNTAX "9.7.3.4. Regular Expression Metasyntax") não existem no XQuery.
* As letras de sinalização de expressão regular definidas pelo XQuery estão relacionadas, mas não as mesmas, com as letras de opção para POSIX ([Tabela 9.24](functions-matching.md#POSIX-EMBEDDED-OPTIONS-TABLE "Table 9.24. ARE Embedded-Option Letters")). Embora as opções `i` e `q` se comportem da mesma maneira, outras não:

As opções `s` (permitir que o ponto corresponda a nova linha) e `m` (permitir que `^` e `$` correspondam a novas linhas) do XQuery fornecem acesso aos mesmos comportamentos que as opções `n`, `p` e `w` do POSIX, mas elas *não* correspondem ao comportamento das opções `s` e `m` do POSIX. Observe, em particular, que a correspondência de ponto a nova linha é o comportamento padrão no POSIX, mas não no XQuery. A opção `x` (ignorar espaços em branco no padrão) do XQuery é notavelmente diferente da opção de modo expandido do POSIX. A opção `x` do POSIX também permite que `#` comece um comentário no padrão, e o POSIX não ignorará um caractere de espaço após uma barra invertida.