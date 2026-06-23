## 10.2. Operadores [#](#TYPECONV-OPER)

O operador específico que é referido por uma expressão de operador é determinado usando o procedimento a seguir. Observe que esse procedimento é indiretamente afetado pela precedência dos operadores envolvidos, uma vez que isso determinará quais subexpressões serão consideradas como os inputs dos quais os operadores são. Consulte [Seção 4.1.6] para obter mais informações. [(sql-syntax-lexical.md#SQL-PRECEDENCE "4.1.6. Operator Precedence")]

**Resolução do tipo de operador**

1. Selecione os operadores a serem considerados do catálogo do sistema `pg_operator`. Se um nome de operador não qualificado pelo esquema foi usado (o caso usual), os operadores considerados são aqueles com o nome correspondente e o número de argumentos que são visíveis no caminho de pesquisa atual (ver [Seção 5.10.3](ddl-schemas.md#DDL-SCHEMAS-PATH)). Se um nome de operador qualificado foi fornecido, apenas os operadores no esquema especificado são considerados.

1. Se o caminho de busca encontrar vários operadores com tipos de argumentos idênticos, apenas o que aparece mais cedo no caminho é considerado. Operadores com tipos de argumentos diferentes são considerados em pé de igualdade, independentemente da posição no caminho de busca.
2. Verifique se um operador aceita exatamente os tipos de argumentos de entrada. Se existir (pode haver apenas uma correspondência exata no conjunto de operadores considerados), use-o. A falta de uma correspondência exata cria um perigo de segurança ao chamar, via nome qualificado [[9]](#ftn.OP-QUALIFIED-SECURITY) (não típico), qualquer operador encontrado em um esquema que permita que usuários não confiáveis criem objetos. Nessas situações, realize uma conversão de argumentos para forçar uma correspondência exata.

1. Se um dos argumentos de uma invocação de operador binário for do tipo `unknown`, então presuma que é o mesmo tipo que o outro argumento para esta verificação. As invocações que envolvem dois `unknown` de entrada ou um operador prefixo com uma entrada `unknown` nunca encontrarão uma correspondência nesta etapa.
2. Se um dos argumentos de uma invocação de operador binário for do tipo `unknown` e o outro for de um tipo de domínio, verifique a seguir se há um operador que aceite exatamente o tipo de base do domínio em ambos os lados; se sim, use-o.
3. Procure a melhor correspondência.

1. Descarte os operadores candidatos para os quais os tipos de entrada não correspondem e não podem ser convertidos (usando uma conversão implícita) para corresponder. Os literais `unknown` são assumidos como convertidos para qualquer coisa para esse propósito. Se apenas um candidato permanecer, use-o; caso contrário, continue para o próximo passo.
2. Se qualquer argumento de entrada estiver de um tipo de domínio, trate-o como sendo do tipo base do domínio para todos os passos subsequentes. Isso garante que os domínios atuem como seus tipos base para fins de resolução de operadores ambíguos.
3. Analise todos os candidatos e mantenha aqueles com os mais exatos correspondências nos tipos de entrada. Mantenha todos os candidatos se nenhum deles tiver correspondências exatas. Se apenas um candidato permanecer, use-o; caso contrário, continue para o próximo passo.
4. Analise todos os candidatos e mantenha aqueles que aceitam tipos preferidos (da categoria de tipo do tipo de dados de entrada) nas posições mais onde a conversão de tipo será necessária. Mantenha todos os candidatos se nenhum deles aceitar tipos preferidos. Se apenas um candidato permanecer, use-o; caso contrário, continue para o próximo passo.
5. Se quaisquer argumentos de entrada forem `unknown`, verifique as categorias de tipo aceitas nessas posições de argumento pelos candidatos restantes. Em cada posição, selecione a categoria `string` se algum candidato aceitar essa categoria. (Esse viés em direção à string é apropriado, pois um literal de tipo desconhecido parece uma string.) Caso contrário, se todos os candidatos restantes aceitarem a mesma categoria de tipo, selecione essa categoria; caso contrário, falhe porque a escolha correta não pode ser deduzida sem mais pistas. Agora, descarte os candidatos que não aceitam a categoria de tipo selecionada. Além disso, se algum candidato aceitar um tipo preferido nessa categoria, descarte os candidatos que aceitam tipos não preferidos para esse argumento. Mantenha todos os candidatos se nenhum deles sobreviver a esses testes. Se apenas um candidato permanecer, use-o; caso contrário, continue para o próximo passo.
6. Se houver tanto `unknown` quanto argumentos de tipo conhecido, e todos os argumentos de tipo conhecido tiverem o mesmo tipo, assuma que os argumentos `unknown` também são desse tipo, e verifique quais candidatos podem aceitar esse tipo nas posições de argumento `unknown`. Se exatamente um candidato passar esse teste, use-o. Caso contrário, falhe.

Alguns exemplos seguem.

**Exemplo 10.1. Resolução do tipo do operador raiz quadrada**

Existe apenas um operador de raiz quadrada (prefixo `|/`) definido no catálogo padrão, e ele recebe um argumento do tipo `double precision`. O scanner atribui um tipo inicial de `integer` ao argumento nesta expressão de consulta:

```
SELECT |/ 40 AS "square root of 40";
 square root of 40
-------------------
 6.324555320336759
(1 row)
```

Então, o analisador faz uma conversão de tipo no operando e a consulta é equivalente a:

```
SELECT |/ CAST(40 AS double precision) AS "square root of 40";
```



**Exemplo 10.2. Resolução do tipo do operador de concatenação de strings**

Uma sintaxe semelhante a uma cadeia é usada para trabalhar com tipos de cadeia e para trabalhar com tipos de extensão complexos. As cadeias com tipo não especificado são correspondidas com candidatos prováveis de operador.

Um exemplo com um argumento não especificado:

```
SELECT text 'abc' || 'def' AS "text and unknown";

 text and unknown
------------------
 abcdef
(1 row)
```

Neste caso, o analisador verifica se há um operador que está tomando `text` para ambos os argumentos. Como há, ele assume que o segundo argumento deve ser interpretado como tipo `text`.

Aqui está uma concatenação de dois valores de tipos não especificados:

```
SELECT 'abc' || 'def' AS "unspecified";

 unspecified
-------------
 abcdef
(1 row)
```

Neste caso, não há nenhuma pista inicial para qual tipo usar, uma vez que nenhum tipo é especificado na consulta. Portanto, o analisador procura todos os operadores candidatos e descobre que há candidatos que aceitam entradas de categoria de string e categoria de string-bit. Como a categoria de string é preferida quando disponível, essa categoria é selecionada, e então o tipo preferido para strings, `text`, é usado como o tipo específico para resolver os literais de tipo desconhecido.



**Exemplo 10.3. Resolução do tipo de operador de valor absoluto e negação**

O catálogo de operadores do PostgreSQL tem várias entradas para o operador prefixo `@`, todos os quais implementam operações de valor absoluto para vários tipos de dados numéricos. Uma dessas entradas é para o tipo `float8`, que é o tipo preferido na categoria numérica. Portanto, o PostgreSQL usará essa entrada quando confrontado com uma entrada `unknown`:

```
SELECT @ '-4.5' AS "abs";
 abs
-----
 4.5
(1 row)
```

Aqui, o sistema implicitamente resolveu o literal de tipo desconhecido como tipo `float8` antes de aplicar o operador escolhido. Podemos verificar que `float8` e não algum outro tipo foi usado:

```
SELECT @ '-4.5e500' AS "abs";

ERROR:  "-4.5e500" is out of range for type double precision
```

Por outro lado, o operador prefixo `~` (negação bit a bit) é definido apenas para tipos de dados inteiros, não para `float8`. Portanto, se tentarmos um caso semelhante com `~`, obtemos:

```
SELECT ~ '20' AS "negation";

ERROR:  operator is not unique: ~ "unknown"
HINT:  Could not choose a best candidate operator. You might need to add
explicit type casts.
```

Isso acontece porque o sistema não consegue decidir qual dos vários operadores possíveis do `~` deve ser preferido. Podemos ajudá-lo com um cast explícito:

```
SELECT ~ CAST('20' AS int8) AS "negation";

 negation
----------
      -21
(1 row)
```



**Exemplo 10.4. Resolução do operador de inclusão de matriz**

Aqui está outro exemplo de resolução de um operador com uma entrada conhecida e uma entrada desconhecida:

```
SELECT array[1,2] <@ '{1,2,3}' as "is subset";

 is subset
-----------
 t
(1 row)
```

O catálogo de operadores do PostgreSQL tem várias entradas para o operador infix `<@`, mas os únicos dois que possivelmente podem aceitar uma matriz de inteiros no lado esquerdo são a inclusão de matriz (`anyarray` `<@` `anyarray`) e a inclusão de intervalo (`anyelement` `<@` `anyrange`). Como nenhum desses pseudotípicos polimórficos (ver [Seção 8.21](datatype-pseudo.md "8.21. Pseudo-Types")) é considerado preferido, o analisador não pode resolver a ambiguidade com base nisso. No entanto, [Passo 3.f](typeconv-oper.md#OP-RESOL-LAST-UNKNOWN "Step 3.f") diz que ele deve assumir que o literal de tipo desconhecido é do mesmo tipo que os outros inputs, ou seja, matriz de inteiros. Agora, apenas um dos dois operadores pode corresponder, então a inclusão de matriz é selecionada. (Se tivesse sido selecionada a inclusão de intervalo, teríamos obtido um erro, porque a string não tem o formato certo para ser um literal de intervalo.)



**Exemplo 10.5. Operador personalizado em um tipo de domínio**

Os usuários às vezes tentam declarar operadores aplicando apenas a um tipo de domínio. Isso é possível, mas não é tão útil quanto parece, porque as regras de resolução de operadores são projetadas para selecionar operadores que se aplicam ao tipo de base do domínio. Como exemplo, considere

```
CREATE DOMAIN mytext AS text CHECK(...);
CREATE FUNCTION mytext_eq_text (mytext, text) RETURNS boolean AS ...;
CREATE OPERATOR = (procedure=mytext_eq_text, leftarg=mytext, rightarg=text);
CREATE TABLE mytable (val mytext);

SELECT * FROM mytable WHERE val = 'foo';
```

Essa consulta não usará o operador personalizado. O analisador primeiro verificará se há um operador `mytext` `=` `mytext` ([Passo 2.a](typeconv-oper.md#OP-RESOL-EXACT-UNKNOWN "Step 2.a")) e, como não há, então considerará o tipo de base do domínio `text`, e verificará se há um operador `text` `=` `text` ([Passo 2.b](typeconv-oper.md#OP-RESOL-EXACT-DOMAIN "Step 2.b")) e, como há, então resolve o literal do tipo `unknown` como `text` e usa o operador `text` `=` `text`. A única maneira de fazer com que o operador personalizado seja usado é ao converter explicitamente o literal:

```
SELECT * FROM mytable WHERE val = text 'foo';
```

para que o operador `mytext` `=` `text` seja encontrado imediatamente de acordo com a regra de correspondência exata. Se as regras de melhor correspondência forem alcançadas, elas discriminam ativamente contra operadores em tipos de domínio. Se não forem, tal operador criaria muitos falhas de operador ambíguo, porque as regras de conversão sempre consideram um domínio como convertivelmente para ou a partir de seu tipo base, e assim o operador de domínio seria considerado utilizável nos mesmos casos que um operador com o mesmo nome no tipo base.



---

[[9]](#OP-QUALIFIED-SECURITY) O perigo não surge com um nome não qualificado por esquema, porque um caminho de pesquisa que contém esquemas que permitem que usuários não confiáveis criem objetos não é um padrão de uso seguro de esquema (ddl-schemas.md#DDL-SCHEMAS-PATTERNS "5.10.6. Usage Patterns").