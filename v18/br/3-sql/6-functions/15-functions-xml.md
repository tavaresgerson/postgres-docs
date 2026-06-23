## 9.15. Funções XML [#](#FUNCTIONS-XML)

* [9.15.1. Produção de conteúdo XML](functions-xml.md#FUNCTIONS-PRODUCING-XML)
* [9.15.2. Predicados XML](functions-xml.md#FUNCTIONS-XML-PREDICATES)
* [9.15.3. Processamento de XML](functions-xml.md#FUNCTIONS-XML-PROCESSING)
* [9.15.4. Mapeamento de tabelas para XML](functions-xml.md#FUNCTIONS-XML-MAPPING)

As funções e expressões semelhantes a funções descritas nesta seção operam em valores do tipo `xml`. Consulte [Seção 8.13](datatype-xml.md) para informações sobre o tipo `xml`. As expressões semelhantes a funções `xmlparse` e `xmlserialize` para conversão entre os tipos `xml` são documentadas lá, não nesta seção.

O uso da maioria dessas funções exige que o PostgreSQL tenha sido construído com `configure --with-libxml`.

### 9.15.1. Produzir conteúdo XML [#](#FUNCTIONS-PRODUCING-XML)

Um conjunto de funções e expressões semelhantes a funções está disponível para a produção de conteúdo XML a partir de dados SQL. Como tal, são particularmente adequados para formatar os resultados das consultas em documentos XML para processamento em aplicações cliente.

#### 9.15.1.1. `xmltext` [#](#FUNCTIONS-PRODUCING-XML-XMLTEXT)

```
xmltext ( text ) → xml
```

A função `xmltext` retorna um valor XML com um único nó de texto contendo o argumento de entrada como seu conteúdo. Entidades pré-definidas, como o símbolo de amplo (`&`), chaves de ângulo esquerdo e direito (`< >`) e aspas (`""`) são escapadas.

Exemplo:

```
SELECT xmltext('< foo & bar >');
         xmltext
-------------------------
 &lt; foo &amp; bar &gt;
```

#### 9.15.1.2. `xmlcomment` [#](#FUNCTIONS-PRODUCING-XML-XMLCOMMENT)

```
xmlcomment ( text ) → xml
```

A função `xmlcomment` cria um valor XML que contém um comentário XML com o texto especificado como conteúdo. O texto não pode conter “`--`” ou terminar com “`-`”, caso contrário, o resultado não seria um comentário XML válido. Se o argumento for nulo, o resultado será nulo.

Exemplo:

```
SELECT xmlcomment('hello');

  xmlcomment
--------------
 <!--hello-->
```

#### 9.15.1.3. `xmlconcat` [#](#FUNCTIONS-PRODUCING-XML-XMLCONCAT)

```
xmlconcat ( xml [, ...] ) → xml
```

A função `xmlconcat` concatena uma lista de valores individuais XML para criar um único valor que contém um fragmento de conteúdo XML. Os valores nulos são omitidos; o resultado é nulo apenas se não houver argumentos não nulos.

Exemplo:

```
SELECT xmlconcat('<abc/>', '<bar>foo</bar>');

      xmlconcat
----------------------
 <abc/><bar>foo</bar>
```

As declarações XML, se presentes, são combinadas da seguinte forma. Se todos os valores dos argumentos tiverem a mesma declaração de versão XML, essa versão é usada no resultado, caso contrário, nenhuma versão é usada. Se todos os valores dos argumentos tiverem o valor da declaração de standalone “sim”, então esse valor é usado no resultado. Se todos os valores dos argumentos tiverem uma declaração de standalone e pelo menos uma é “não”, então essa é usada no resultado. Caso contrário, o resultado não terá nenhuma declaração standalone. Se o resultado for determinado que requer uma declaração standalone, mas sem declaração de versão, uma declaração de versão com versão 1.0 será usada porque o XML requer uma declaração XML para conter uma declaração de versão. As declarações de codificação são ignoradas e removidas em todos os casos.

Exemplo:

```
SELECT xmlconcat('<?xml version="1.1"?><foo/>', '<?xml version="1.1" standalone="no"?><bar/>');

             xmlconcat
-----------------------------------
 <?xml version="1.1"?><foo/><bar/>
```

#### 9.15.1.4. `xmlelement` [#](#FUNCTIONS-PRODUCING-XML-XMLELEMENT)

```
xmlelement ( NAME name [, XMLATTRIBUTES ( attvalue [ AS attname ] [, ...] ) ] [, content [, ...]] ) → xml
```

A expressão `xmlelement` produz um elemento XML com o nome, atributos e conteúdo fornecidos. Os itens *`name`* e *`attname`* mostrados na sintaxe são identificadores simples, não valores. Os itens *`attvalue`* e *`content`* são expressões, que podem gerar qualquer tipo de dados do PostgreSQL. Os argumentos dentro de `XMLATTRIBUTES` geram atributos do elemento XML; os valores *`content`* são concatenados para formar seu conteúdo.

Exemplos:

```
SELECT xmlelement(name foo);

 xmlelement
------------
 <foo/>

SELECT xmlelement(name foo, xmlattributes('xyz' as bar));

    xmlelement
------------------
 <foo bar="xyz"/>

SELECT xmlelement(name foo, xmlattributes(current_date as bar), 'cont', 'ent');

             xmlelement
-------------------------------------
 <foo bar="2007-01-26">content</foo>
```

Os nomes de elementos e atributos que não são nomes válidos XML são escapados, substituindo os caracteres oficiais pela sequência `_xHHHH_`, onde *`HHHH`* é o ponto de código Unicode do caractere em notação hexadecimal. Por exemplo:

```
SELECT xmlelement(name "foo$bar", xmlattributes('xyz' as "a&b"));

            xmlelement
----------------------------------
 <foo_x0024_bar a_x0026_b="xyz"/>
```

Um nome de atributo explícito não precisa ser especificado se o valor do atributo for uma referência de coluna, nesse caso, o nome da coluna será usado como nome do atributo por padrão. Em outros casos, o atributo deve ser dado um nome explícito. Portanto, este exemplo é válido:

```
CREATE TABLE test (a xml, b xml);
SELECT xmlelement(name test, xmlattributes(a, b)) FROM test;
```

Mas estas não são:

```
SELECT xmlelement(name test, xmlattributes('constant'), a, b) FROM test;
SELECT xmlelement(name test, xmlattributes(func(a, b))) FROM test;
```

O conteúdo de elementos, se especificado, será formatado de acordo com seu tipo de dados. Se o conteúdo for de tipo `xml`, documentos XML complexos podem ser construídos. Por exemplo:

```
SELECT xmlelement(name foo, xmlattributes('xyz' as bar),
                            xmlelement(name abc),
                            xmlcomment('test'),
                            xmlelement(name xyz));

                  xmlelement
----------------------------------------------
 <foo bar="xyz"><abc/><!--test--><xyz/></foo>
```

O conteúdo de outros tipos será formatado em dados de caracteres XML válidos. Isso significa, em particular, que os caracteres <, > e & serão convertidos em entidades. Os dados binários (tipo de dados `bytea`) serão representados em codificação base64 ou hex, dependendo da configuração do parâmetro de configuração [xmlbinary](runtime-config-client.md#GUC-XMLBINARY). O comportamento específico para tipos de dados individuais é esperado para evoluir para alinhar as mapeamentos do PostgreSQL com os especificados em SQL:2006 e posteriores, conforme discutido em [Seção D.3.1.3](xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-CASTS).

#### 9.15.1.5. `xmlforest` [#](#FUNCTIONS-PRODUCING-XML-XMLFOREST)

```
xmlforest ( content [ AS name ] [, ...] ) → xml
```

A expressão `xmlforest` produz uma floresta (sequência) de elementos XML usando os nomes e o conteúdo fornecidos. Quanto à expressão `xmlelement`, cada *`name`* deve ser um identificador simples, enquanto as expressões *`content`* podem ter qualquer tipo de dado.

Exemplos:

```
SELECT xmlforest('abc' AS foo, 123 AS bar);

          xmlforest
------------------------------
 <foo>abc</foo><bar>123</bar>


SELECT xmlforest(table_name, column_name)
FROM information_schema.columns
WHERE table_schema = 'pg_catalog';

                                xmlforest
------------------------------------​-----------------------------------
 <table_name>pg_authid</table_name>​<column_name>rolname</column_name>
 <table_name>pg_authid</table_name>​<column_name>rolsuper</column_name>
 ...
```

Como visto no segundo exemplo, o nome do elemento pode ser omitido se o valor do conteúdo for uma referência de coluna, nesse caso, o nome da coluna é usado por padrão. Caso contrário, um nome deve ser especificado.

Os nomes de elementos que não são nomes válidos XML são escapados, conforme mostrado para `xmlelement` acima. Da mesma forma, os dados de conteúdo são escapados para criar conteúdo XML válido, a menos que já sejam do tipo `xml`.

Observe que florestas XML não são documentos XML válidos se consistirem em mais de um elemento, portanto, pode ser útil envolver as expressões `xmlforest` em `xmlelement`.

#### 9.15.1.6. `xmlpi` [#](#FUNCTIONS-PRODUCING-XML-XMLPI)

```
xmlpi ( NAME name [, content ] ) → xml
```

A expressão `xmlpi` cria uma instrução de processamento de XML. Quanto à expressão `xmlelement`, o *`name`* deve ser um identificador simples, enquanto a expressão *`content`* pode ter qualquer tipo de dado. O *`content`*, se presente, não deve conter a sequência de caracteres `?>`.

Exemplo:

```
SELECT xmlpi(name php, 'echo "hello world";');

            xmlpi
-----------------------------
 <?php echo "hello world";?>
```

#### 9.15.1.7. `xmlroot` [#](#FUNCTIONS-PRODUCING-XML-XMLROOT)

```
xmlroot ( xml, VERSION {text|NO VALUE} [, STANDALONE {YES|NO|NO VALUE} ] ) → xml
```

A expressão `xmlroot` altera as propriedades do nó raiz de um valor XML. Se uma versão for especificada, ela substitui o valor na declaração de versão do nó raiz; se uma configuração independente for especificada, ela substitui o valor na declaração de independência do nó raiz.

```
SELECT xmlroot(xmlparse(document '<?xml version="1.1"?><content>abc</content>'),
               version '1.0', standalone yes);

                xmlroot
----------------------------------------
 <?xml version="1.0" standalone="yes"?>
 <content>abc</content>
```

#### 9.15.1.8. `xmlagg` [#](#FUNCTIONS-XML-XMLAGG)

```
xmlagg ( xml ) → xml
```

A função `xmlagg` é, ao contrário das outras funções descritas aqui, uma função agregada. Ela concatenia os valores de entrada para a chamada da função agregada, muito como a `xmlconcat` faz, exceto que a concatenação ocorre em linhas em vez de em expressões em uma única linha. Consulte [Seção 9.21](functions-aggregate.md) para obter informações adicionais sobre funções agregadas.

Exemplo:

```
CREATE TABLE test (y int, x xml);
INSERT INTO test VALUES (1, '<foo>abc</foo>');
INSERT INTO test VALUES (2, '<bar/>');
SELECT xmlagg(x) FROM test;
        xmlagg
----------------------
 <foo>abc</foo><bar/>
```

Para determinar a ordem da concatenação, pode-se adicionar uma cláusula `ORDER BY` à chamada agregada, conforme descrito em [Seção 4.2.7](sql-expressions.md#SYNTAX-AGGREGATES). Por exemplo:

```
SELECT xmlagg(x ORDER BY y DESC) FROM test;
        xmlagg
----------------------
 <bar/><foo>abc</foo>
```

A abordagem não padrão a seguir era recomendada em versões anteriores e ainda pode ser útil em casos específicos:

```
SELECT xmlagg(x) FROM (SELECT * FROM test ORDER BY y DESC) AS tab;
        xmlagg
----------------------
 <bar/><foo>abc</foo>
```

### 9.15.2. Predicados XML [#](#FUNCTIONS-XML-PREDICATES)

As expressões descritas nesta seção verificam as propriedades dos valores de `xml`.

#### 9.15.2.1. `IS DOCUMENT` [#](#FUNCTIONS-PRODUCING-XML-IS-DOCUMENT)

```
xml IS DOCUMENT → boolean
```

A expressão `IS DOCUMENT` retorna verdadeiro se o valor XML do argumento for um documento XML válido, falso se não for (ou seja, se for um fragmento de conteúdo) ou nulo se o argumento for nulo. Consulte a [Seção 8.13](datatype-xml.md) sobre a diferença entre documentos e fragmentos de conteúdo.

#### 9.15.2.2. `IS NOT DOCUMENT` [#](#FUNCTIONS-PRODUCING-XML-IS-NOT-DOCUMENT)

```
xml IS NOT DOCUMENT → boolean
```

A expressão `IS NOT DOCUMENT` retorna false se o valor XML do argumento for um documento XML válido, true se não for (ou seja, é um fragmento de conteúdo) ou null se o argumento for nulo.

#### 9.15.2.3. `XMLEXISTS` [#](#XML-EXISTS)

```
XMLEXISTS ( text PASSING [BY {REF|VALUE}] xml [BY {REF|VALUE}] ) → boolean
```

A função `xmlexists` avalia uma expressão XPath 1.0 (o primeiro argumento), com o valor XML passado como seu item de contexto. A função retorna false se o resultado dessa avaliação produzir um conjunto de nós vazio, true se produzir qualquer outro valor. A função retorna null se qualquer argumento for nulo. Um valor não nulo passado como item de contexto deve ser um documento XML, não um fragmento de conteúdo ou qualquer valor não XML.

Exemplo:

```
SELECT xmlexists('//town[text() = ''Toronto'']' PASSING BY VALUE '<towns><town>Toronto</town><town>Ottawa</town></towns>');

 xmlexists
------------
 t
(1 row)
```

As cláusulas `BY REF` e `BY VALUE` são aceitas no PostgreSQL, mas são ignoradas, conforme discutido em [Seção D.3.2](xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-POSTGRESQL).

No padrão SQL, a função `xmlexists` avalia uma expressão no idioma de consulta XML, mas o PostgreSQL permite apenas uma expressão XPath 1.0, conforme discutido em [Seção D.3.1](xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-XPATH1).

#### 9.15.2.4. `xml_is_well_formed` [#](#XML-IS-WELL-FORMED)

```
xml_is_well_formed ( text ) → boolean
xml_is_well_formed_document ( text ) → boolean
xml_is_well_formed_content ( text ) → boolean
```

Essas funções verificam se uma string `text` representa um XML bem formado, retornando um resultado booleano. `xml_is_well_formed_document` verifica se um documento bem formado, enquanto `xml_is_well_formed_content` verifica se o conteúdo está bem formado. `xml_is_well_formed` faz o primeiro se o parâmetro de configuração [xmloption](runtime-config-client.md#GUC-XMLOPTION) estiver definido como `DOCUMENT`, ou o segundo se estiver definido como `CONTENT`. Isso significa que `xml_is_well_formed` é útil para verificar se um simples cast para o tipo `xml` terá sucesso, enquanto as outras duas funções são úteis para verificar se as variantes correspondentes de `XMLPARSE` terão sucesso.

Exemplos:

```
SET xmloption TO DOCUMENT;
SELECT xml_is_well_formed('<>');
 xml_is_well_formed
--------------------
 f
(1 row)

SELECT xml_is_well_formed('<abc/>');
 xml_is_well_formed
--------------------
 t
(1 row)

SET xmloption TO CONTENT;
SELECT xml_is_well_formed('abc');
 xml_is_well_formed
--------------------
 t
(1 row)

SELECT xml_is_well_formed_document('<pg:foo xmlns:pg="http://postgresql.org/stuff">bar</pg:foo>');
 xml_is_well_formed_document
-----------------------------
 t
(1 row)

SELECT xml_is_well_formed_document('<pg:foo xmlns:pg="http://postgresql.org/stuff">bar</my:foo>');
 xml_is_well_formed_document
-----------------------------
 f
(1 row)
```

O último exemplo mostra que os verificações incluem se os nomes de espaço são corretamente correspondidos.

### 9.15.3. Processamento de XML [#](#FUNCTIONS-XML-PROCESSING)

Para processar valores de tipo de dados `xml`, o PostgreSQL oferece as funções `xpath` e `xpath_exists`, que avaliam expressões XPath 1.0, e a função de tabela `XMLTABLE`.

#### 9.15.3.1. `xpath` [#](#FUNCTIONS-XML-PROCESSING-XPATH)

```
xpath ( xpath text, xml xml [, nsarray text[] ] ) → xml[]
```

A função `xpath` avalia a expressão XPath 1.0 *`xpath`* (dada como texto) contra o valor XML *`xml`*. Ela retorna um array de valores XML correspondentes ao conjunto de nós produzido pela expressão XPath. Se a expressão XPath retornar um valor escalar em vez de um conjunto de nós, um array de um único elemento é retornado.

O segundo argumento deve ser um documento XML bem formado. Em particular, ele deve ter um único elemento de nó raiz.

O terceiro argumento opcional da função é um array de mapeamentos de namespaces. Esse array deve ser um array `text` bidimensional com o comprimento do segundo eixo igual a 2 (ou seja, deve ser um array de arrays, cada um dos quais consiste exatamente em 2 elementos). O primeiro elemento de cada entrada do array é o nome (alias) do namespace, o segundo o URI do namespace. Não é necessário que os aliases fornecidos neste array sejam os mesmos que os utilizados no próprio documento XML (em outras palavras, tanto no documento XML quanto no contexto da função `xpath`, os aliases são *locais*).

Exemplo:

```
SELECT xpath('/my:a/text()', '<my:a xmlns:my="http://example.com">test</my:a>',
             ARRAY[ARRAY['my', 'http://example.com']]);

 xpath
--------
 {test}
(1 row)
```

Para lidar com namespaces (anônimos) padrão, faça algo como este:

```
SELECT xpath('//mydefns:b/text()', '<a xmlns="http://example.com"><b>test</b></a>',
             ARRAY[ARRAY['mydefns', 'http://example.com']]);

 xpath
--------
 {test}
(1 row)
```

#### 9.15.3.2. `xpath_exists` [#](#FUNCTIONS-XML-PROCESSING-XPATH-EXISTS)

```
xpath_exists ( xpath text, xml xml [, nsarray text[] ] ) → boolean
```

A função `xpath_exists` é uma forma especializada da função `xpath`. Em vez de retornar os valores XML individuais que satisfazem a expressão XPath 1.0, esta função retorna um Booleano que indica se a consulta foi satisfeita ou não (especificamente, se produziu algum valor diferente de um conjunto de nós vazio). Esta função é equivalente ao predicado `XMLEXISTS`, exceto que também oferece suporte para um argumento de mapeamento de namespace.

Exemplo:

```
SELECT xpath_exists('/my:a/text()', '<my:a xmlns:my="http://example.com">test</my:a>',
                     ARRAY[ARRAY['my', 'http://example.com']]);

 xpath_exists
--------------
 t
(1 row)
```

#### 9.15.3.3. `xmltable` [#](#FUNCTIONS-XML-PROCESSING-XMLTABLE)

```
XMLTABLE (
    [ XMLNAMESPACES ( namespace_uri AS namespace_name [, ...] ), ]
    row_expression PASSING [BY {REF|VALUE}] document_expression [BY {REF|VALUE}]
    COLUMNS name { type [PATH column_expression] [DEFAULT default_expression] [NOT NULL | NULL]
                  | FOR ORDINALITY }
            [, ...]
) → setof record
```

A expressão `xmltable` produz uma tabela com base em um valor XML, um filtro XPath para extrair linhas e um conjunto de definições de coluna. Embora sintacticamente se assemelhe a uma função, ela só pode aparecer como uma tabela na cláusula `FROM` de uma consulta.

A cláusula opcional `XMLNAMESPACES` fornece uma lista de definições de namespaces separadas por vírgula, onde cada *`namespace_uri`* é uma expressão de *`text`* e cada *`namespace_name`* é um identificador simples. Especifica os namespaces XML usados no documento e seus aliases. Uma especificação de namespace padrão não é atualmente suportada.

O argumento *`row_expression`* requerido é uma expressão XPath 1.0 (dada como `text`) que é avaliada, passando o valor XML *`document_expression`* como seu item de contexto, para obter um conjunto de nós XML. Esses nós são os que `xmltable` transforma em linhas de saída. Não serão produzidas linhas se o *`document_expression`* for nulo, nem se o *`row_expression`* produzir um conjunto de nós vazio ou qualquer outro valor que não seja um conjunto de nós.

*`document_expression`* fornece o item de contexto para o *`row_expression`. Deve ser um documento XML bem formado; fragmentos/florestas não são aceitos. As cláusulas `BY REF` e `BY VALUE` são aceitas, mas ignoradas, conforme discutido em [Seção D.3.2](xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-POSTGRESQL).

No padrão SQL, a função `xmltable` avalia expressões no idioma de consulta XML, mas o PostgreSQL permite apenas expressões XPath 1.0, conforme discutido em [Seção D.3.1](xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-XPATH1).

A cláusula `COLUMNS` exigida especifica a(s) coluna(s) que serão produzidas na tabela de saída. Veja o resumo da sintaxe acima para o formato. Um nome é necessário para cada coluna, assim como um tipo de dados (a menos que `FOR ORDINALITY` seja especificado, no qual caso o tipo `integer` é implícito). As cláusulas de caminho, padrão e não nulidade são opcionais.

Uma coluna marcada `FOR ORDINALITY` será preenchida com números de linha, começando com 1, na ordem dos nós recuperados do conjunto de nós de resultado do *`row_expression`*. No máximo, uma coluna pode ser marcada `FOR ORDINALITY`.

Nota

O XPath 1.0 não especifica uma ordem para os nós em um conjunto de nós, portanto, o código que depende de uma ordem específica dos resultados será dependente da implementação. Os detalhes podem ser encontrados em [Seção D.3.1.2](xml-limits-conformance.md#XML-XPATH-1-SPECIFICS).

O *`column_expression`* para uma coluna é uma expressão XPath 1.0 que é avaliada para cada linha, com o nó atual do resultado do *`row_expression`* como seu item de contexto, para encontrar o valor da coluna. Se não for fornecido um *`column_expression`*, então o nome da coluna é usado como um caminho implícito.

Se a expressão XPath de uma coluna retornar um valor não XML (que é limitado a string, booleano ou duplo no XPath 1.0) e a coluna tiver um tipo PostgreSQL diferente de `xml`, a coluna será definida como se o valor fosse representado por uma string no tipo PostgreSQL. (Se o valor for booleano, sua representação em string é considerada `1` ou `0` se a categoria do tipo da coluna de saída for numérica, caso contrário, `true` ou `false`).

Se a expressão XPath de uma coluna retornar um conjunto não vazio de nós XML e o tipo do PostgreSQL da coluna for `xml`, a coluna receberá exatamente o resultado da expressão, se for de forma de documento ou de conteúdo. [[8]](#ftn.id-1.5.8.21.7.5.15.2)

Um resultado não XML atribuído a uma coluna de saída `xml` produz conteúdo, um único nó de texto com o valor de cadeia do resultado. Um resultado XML atribuído a uma coluna de qualquer outro tipo não pode ter mais de um nó, ou uma exceção é levantada. Se houver exatamente um nó, a coluna será definida como se o valor de cadeia do nó (conforme definido para a função `string` de XPath 1.0) fosse atribuído ao tipo PostgreSQL.

O valor de cadeia de um elemento XML é a concatenação, em ordem de documento, de todos os nós de texto contidos nesse elemento e em seus descendentes. O valor de cadeia de um elemento sem nós de texto descendentes é uma cadeia vazia (não `NULL`). Quaisquer atributos `xsi:nil` são ignorados. Observe que o nó `text()` composto apenas por espaços em branco entre dois elementos que não são de texto é preservado, e que o espaço em branco inicial em um nó `text()` não é achatado. A função XPath 1.0 `string` pode ser consultada para as regras que definem o valor de cadeia de outros tipos de nós XML e valores não XML.

As regras de conversão apresentadas aqui não são exatamente as do padrão SQL, conforme discutido em [Seção D.3.1.3](xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-CASTS).

Se a expressão de caminho retornar um conjunto de nós vazio (tipicamente, quando não corresponde) para uma determinada linha, a coluna será definida como `NULL`, a menos que um *`default_expression`* seja especificado; então o valor resultante da avaliação dessa expressão é usado.

Um *`default_expression`*, em vez de ser avaliado imediatamente quando o `xmltable` é chamado, é avaliado cada vez que é necessária uma definição para a coluna. Se a expressão se qualificar como estável ou imutável, a avaliação repetida pode ser ignorada. Isso significa que você pode usar funções voláteis como `nextval` em *`default_expression`*.

As colunas podem ser marcadas com `NOT NULL`. Se o *`column_expression`* para uma coluna `NOT NULL` não corresponder a nada e não houver `DEFAULT` ou o *`default_expression` também avaliar como nulo, um erro é relatado.

Exemplos:

```
CREATE TABLE xmldata AS SELECT
xml $$
<ROWS>
  <ROW id="1">
    <COUNTRY_ID>AU</COUNTRY_ID>
    <COUNTRY_NAME>Australia</COUNTRY_NAME>
  </ROW>
  <ROW id="5">
    <COUNTRY_ID>JP</COUNTRY_ID>
    <COUNTRY_NAME>Japan</COUNTRY_NAME>
    <PREMIER_NAME>Shinzo Abe</PREMIER_NAME>
    <SIZE unit="sq_mi">145935</SIZE>
  </ROW>
  <ROW id="6">
    <COUNTRY_ID>SG</COUNTRY_ID>
    <COUNTRY_NAME>Singapore</COUNTRY_NAME>
    <SIZE unit="sq_km">697</SIZE>
  </ROW>
</ROWS>
$$ AS data;

SELECT xmltable.*
  FROM xmldata,
       XMLTABLE('//ROWS/ROW'
                PASSING data
                COLUMNS id int PATH '@id',
                        ordinality FOR ORDINALITY,
                        "COUNTRY_NAME" text,
                        country_id text PATH 'COUNTRY_ID',
                        size_sq_km float PATH 'SIZE[@unit = "sq_km"]',
                        size_other text PATH
                             'concat(SIZE[@unit!="sq_km"], " ", SIZE[@unit!="sq_km"]/@unit)',
                        premier_name text PATH 'PREMIER_NAME' DEFAULT 'not specified');

 id | ordinality | COUNTRY_NAME | country_id | size_sq_km |  size_other  | premier_name
----+------------+--------------+------------+------------+--------------+---------------
  1 |          1 | Australia    | AU         |            |              | not specified
  5 |          2 | Japan        | JP         |            | 145935 sq_mi | Shinzo Abe
  6 |          3 | Singapore    | SG         |        697 |              | not specified
```

O exemplo a seguir mostra a concatenação de múltiplos nós text(), o uso do nome da coluna como filtro XPath e o tratamento de espaços em branco, comentários XML e instruções de processamento:

```
CREATE TABLE xmlelements AS SELECT
xml $$
  <root>
   <element>  Hello<!-- xyxxz -->2a2<?aaaaa?> <!--x-->  bbb<x>xxx</x>CC  </element>
  </root>
$$ AS data;

SELECT xmltable.*
  FROM xmlelements, XMLTABLE('/root' PASSING data COLUMNS element text);
         element
-------------------------
   Hello2a2   bbbxxxCC
```

O exemplo a seguir ilustra como a cláusula `XMLNAMESPACES` pode ser usada para especificar uma lista de namespaces utilizados no documento XML, bem como nas expressões XPath:

```
WITH xmldata(data) AS (VALUES ('
<example xmlns="http://example.com/myns" xmlns:B="http://example.com/b">
 <item foo="1" B:bar="2"/>
 <item foo="3" B:bar="4"/>
 <item foo="4" B:bar="5"/>
</example>'::xml)
)
SELECT xmltable.*
  FROM XMLTABLE(XMLNAMESPACES('http://example.com/myns' AS x,
                              'http://example.com/b' AS "B"),
             '/x:example/x:item'
                PASSING (SELECT data FROM xmldata)
                COLUMNS foo int PATH '@foo',
                  bar int PATH '@B:bar');
 foo | bar
-----+-----
   1 |   2
   3 |   4
   4 |   5
(3 rows)
```

### 9.15.4. Mapeamento de tabelas para XML [#](#FUNCTIONS-XML-MAPPING)

As funções a seguir mapeiam o conteúdo de tabelas relacionais para valores XML. Elas podem ser consideradas como uma funcionalidade de exportação XML:

```
table_to_xml ( table regclass, nulls boolean,
               tableforest boolean, targetns text ) → xml
query_to_xml ( query text, nulls boolean,
               tableforest boolean, targetns text ) → xml
cursor_to_xml ( cursor refcursor, count integer, nulls boolean,
                tableforest boolean, targetns text ) → xml
```

`table_to_xml` mapeia o conteúdo da tabela nomeada, passada como parâmetro *`table`*. O tipo `regclass` aceita strings que identificam tabelas usando a notação usual, incluindo qualificação opcional do esquema e aspas duplas (consulte [Seção 8.19](datatype-oid.md "8.19. Object Identifier Types") para detalhes). `query_to_xml` executa a consulta cujo texto é passado como parâmetro *`query`* e mapeia o conjunto de resultados. `cursor_to_xml` recupera o número indicado de linhas do cursor especificado pelo parâmetro *`cursor`*. Esta variante é recomendada se grandes tabelas precisam ser mapeadas, porque o valor do resultado é construído na memória por cada função.

Se *`tableforest`* for falso, o documento XML resultante terá o seguinte aspecto:

```
<tablename>
  <row>
    <columnname1>data</columnname1>
    <columnname2>data</columnname2>
  </row>

  <row>
    ...
  </row>

  ...
</tablename>
```

Se *`tableforest`* for verdadeiro, o resultado é um fragmento de conteúdo XML que se parece com este:

```
<tablename>
  <columnname1>data</columnname1>
  <columnname2>data</columnname2>
</tablename>

<tablename>
  ...
</tablename>

...
```

Se não houver um nome de tabela disponível, ou seja, ao mapear uma consulta ou um cursor, a string `table` é usada no primeiro formato, `row` no segundo formato.

A escolha entre esses formatos cabe ao usuário. O primeiro formato é um documento XML adequado, que será importante em muitas aplicações. O segundo formato tende a ser mais útil na função `cursor_to_xml` se os valores dos resultados forem reensamblados em um único documento posteriormente. As funções para produzir conteúdo XML discutidas acima, em particular `xmlelement`, podem ser usadas para alterar os resultados conforme o gosto.

Os valores dos dados são mapeados da mesma maneira que descrito para a função `xmlelement` acima.

O parâmetro *`nulls`* determina se os valores nulos devem ser incluídos na saída. Se verdadeiro, os valores nulos nas colunas são representados como:

```
<columnname xsi:nil="true"/>
```

onde `xsi` é o prefixo do namespace XML para o XML Schema Instance. Uma declaração de namespace apropriada será adicionada ao valor do resultado. Se false, as colunas que contêm valores nulos são simplesmente omitidas na saída.

O parâmetro *`targetns`* especifica o namespace XML desejado para o resultado. Se não se deseja um namespace específico, deve-se passar uma string vazia.

As funções a seguir retornam documentos do esquema XML que descrevem as mapeamentos realizados pelas funções correspondentes acima:

```
table_to_xmlschema ( table regclass, nulls boolean,
                     tableforest boolean, targetns text ) → xml
query_to_xmlschema ( query text, nulls boolean,
                     tableforest boolean, targetns text ) → xml
cursor_to_xmlschema ( cursor refcursor, nulls boolean,
                      tableforest boolean, targetns text ) → xml
```

É essencial que os mesmos parâmetros sejam passados para obter mapeamentos de dados XML correspondentes e documentos de esquema XML.

As funções a seguir produzem mapeamentos de dados XML e o esquema XML correspondente em um único documento (ou floresta), vinculados entre si. Elas podem ser úteis quando se deseja resultados autocontidos e autodescritos:

```
table_to_xml_and_xmlschema ( table regclass, nulls boolean,
                             tableforest boolean, targetns text ) → xml
query_to_xml_and_xmlschema ( query text, nulls boolean,
                             tableforest boolean, targetns text ) → xml
```

Além disso, as seguintes funções estão disponíveis para produzir mapeamentos análogos de esquemas inteiros ou de todo o banco de dados atual:

```
schema_to_xml ( schema name, nulls boolean,
                tableforest boolean, targetns text ) → xml
schema_to_xmlschema ( schema name, nulls boolean,
                      tableforest boolean, targetns text ) → xml
schema_to_xml_and_xmlschema ( schema name, nulls boolean,
                              tableforest boolean, targetns text ) → xml

database_to_xml ( nulls boolean,
                  tableforest boolean, targetns text ) → xml
database_to_xmlschema ( nulls boolean,
                        tableforest boolean, targetns text ) → xml
database_to_xml_and_xmlschema ( nulls boolean,
                                tableforest boolean, targetns text ) → xml
```

Essas funções ignoram tabelas que não são legíveis pelo usuário atual. As funções que afetam todo o banco de dados também ignoram esquemas para os quais o usuário atual não tem privilégio de `USAGE` (consulta).

Observe que esses podem gerar uma grande quantidade de dados, que precisam ser acumulados na memória. Ao solicitar mapeamentos de conteúdo de grandes esquemas ou bancos de dados, pode valer a pena considerar mapear as tabelas separadamente, possivelmente até mesmo por meio de um cursor.

O resultado de uma mapeamento de conteúdo de esquema é o seguinte:

```
<schemaname>

table1-mapping

table2-mapping

...

</schemaname>
```

onde o formato de uma tabela de mapeamento depende do parâmetro *`tableforest`*, conforme explicado acima.

O resultado de um mapeamento do conteúdo do banco de dados é o seguinte:

```
<dbname>

<schema1name>
  ...
</schema1name>

<schema2name>
  ...
</schema2name>

...

</dbname>
```

onde o mapeamento do esquema é conforme acima.

Como exemplo de uso da saída produzida por essas funções, o [Exemplo 9.1] (functions-xml.md#XSLT-XML-HTML "Example 9.1. XSLT Stylesheet for Converting SQL/XML Output to HTML") mostra um modelo de estilo XSLT que converte a saída de `table_to_xml_and_xmlschema` em um documento HTML contendo uma representação tabular dos dados da tabela. Da mesma forma, os resultados desses processos podem ser convertidos em outros formatos baseados em XML.

**Exemplo 9.1. Folha de Estilo XSLT para Conversão de Saída SQL/XML para HTML**

```
<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns="http://www.w3.org/1999/xhtml"
>

  <xsl:output method="xml"
      doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
      doctype-public="-//W3C/DTD XHTML 1.0 Strict//EN"
      indent="yes"/>

  <xsl:template match="/*">
    <xsl:variable name="schema" select="//xsd:schema"/>
    <xsl:variable name="tabletypename"
                  select="$schema/xsd:element[@name=name(current())]/@type"/>
    <xsl:variable name="rowtypename"
                  select="$schema/xsd:complexType[@name=$tabletypename]/xsd:sequence/xsd:element[@name='row']/@type"/>

    <html>
      <head>
        <title><xsl:value-of select="name(current())"/></title>
      </head>
      <body>
        <table>
 <tr>
  <xsl:for-each select="$schema/xsd:complexType[@name=$rowtypename]/xsd:sequence/xsd:element/@name">
   <th>
    <xsl:value-of select=".">
    </xsl:value-of>
   </th>
  </xsl:for-each>
 </tr>
 <xsl:for-each select="row">
  <tr>
   <xsl:for-each select="*">
    <td>
     <xsl:value-of select=".">
     </xsl:value-of>
    </td>
   </xsl:for-each>
  </tr>
 </xsl:for-each>
</table>





      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>
```

---

[[8]](#id-1.5.8.21.7.5.15.2) Um resultado que contém mais de um nó de elemento no nível superior, ou texto que não é espaço em branco fora de um elemento, é um exemplo de forma de conteúdo. Um resultado do XPath não pode ser de nenhuma dessas formas, por exemplo, se ele retornar um nó de atributo selecionado do elemento que o contém. Tal resultado será colocado na forma de conteúdo, com cada nó não permitido substituído por seu valor em string, conforme definido para a função do XPath 1.0 `string`.