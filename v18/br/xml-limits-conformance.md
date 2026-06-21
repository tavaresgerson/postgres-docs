## D.3. Limites e Conformidade XML com SQL/XML [#](#XML-LIMITS-CONFORMANCE)

* [D.3.1. As consultas são restritas ao XPath 1.0](xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-XPATH1)
* [D.3.2. Limites incidentes da implementação](xml-limits-conformance.md#FUNCTIONS-XML-LIMITS-POSTGRESQL)

Revisões significativas das especificações relacionadas ao XML na ISO/IEC 9075-14 (SQL/XML) foram introduzidas com o SQL:2006. A implementação do tipo de dados XML e das funções relacionadas pelo PostgreSQL segue em grande parte a edição anterior de 2003, com algumas empréstimos de edições posteriores. Em particular:

* Onde o padrão atual fornece uma família de tipos de dados XML para armazenar “documento” ou “conteúdo” em variantes não tipadas ou tipadas com o XML Schema, e um tipo `XML(SEQUENCE)` para armazenar peças arbitrárias de conteúdo XML, o PostgreSQL fornece o único tipo `xml`, que pode armazenar “documento” ou “conteúdo”. Não há um equivalente do tipo “sequência” do padrão.
* O PostgreSQL fornece duas funções introduzidas no SQL:2006, mas em variantes que usam a linguagem XPath 1.0, em vez de Consulta XML conforme especificado para elas no padrão.
* O PostgreSQL não suporta as cláusulas `RETURNING CONTENT` ou `RETURNING SEQUENCE`, funções que são definidas para ter essas cláusulas na especificação estão implicitamente retornando conteúdo.

Esta seção apresenta algumas das diferenças resultantes que você pode encontrar.

### D.3.1. As consultas são restritas ao XPath 1.0 [#](#FUNCTIONS-XML-LIMITS-XPATH1)

As funções específicas do PostgreSQL `xpath()` e `xpath_exists()` consultam documentos XML usando o idioma XPath. O PostgreSQL também oferece variantes exclusivas do XPath das funções padrão `XMLEXISTS` e `XMLTABLE`, que oficialmente usam o idioma XQuery. Para todas essas funções, o PostgreSQL depende da biblioteca libxml2, que fornece apenas XPath 1.0.

Existe uma forte conexão entre a linguagem XQuery e as versões 2.0 e posteriores do XPath: qualquer expressão que seja sintaticamente válida e execute com sucesso em ambas produz o mesmo resultado (com uma exceção menor para expressões que contêm referências de caracteres numéricos ou referências de entidades predefinidas, que o XQuery substitui pelo caractere correspondente, enquanto o XPath as deixa em paz). Mas não há essa conexão entre essas linguagens e o XPath 1.0; foi uma linguagem anterior e difere em muitos aspectos.

Há duas categorias de limitação que é preciso ter em mente: a restrição do XQuery para o XPath das funções especificadas no padrão SQL, e a restrição do XPath para a versão 1.0, tanto para o padrão quanto para as funções específicas do PostgreSQL.

#### D.3.1.1. Restrição do XQuery ao XPath [#](#FUNCTIONS-XML-LIMITS-XPATH1-XQUERY-RESTRICTION)

As características do XQuery que vão além das do XPath incluem:

* As expressões XQuery podem construir e retornar novos nós XML, além de todos os valores possíveis do XPath. O XPath pode criar e retornar valores dos tipos atômicos (números, strings, etc.) mas só pode retornar nós XML que já estavam presentes nos documentos fornecidos como entrada para a expressão.
* O XQuery tem construções de controle para iteração, ordenação e agrupamento.
* O XQuery permite a declaração e uso de funções locais.

As versões recentes do XPath começam a oferecer funcionalidades que se sobrepõem a essas (como os estilos funcionais `for-each` e `sort`, funções anônimas e `parse-xml` para criar um nó a partir de uma string), mas tais recursos não estavam disponíveis antes do XPath 3.0.

#### D.3.1.2. Restrição do XPath para 1.0 [#](#XML-XPATH-1-SPECIFICS)

Para os desenvolvedores familiarizados com XQuery e XPath 2.0 ou versões posteriores, o XPath 1.0 apresenta várias diferenças que precisam ser enfrentadas:

* O tipo fundamental de uma expressão XQuery/XPath, o `sequence`, que pode conter nós XML, valores atômicos ou ambos, não existe no XPath 1.0. Uma expressão 1.0 pode produzir apenas um conjunto de nós (contendo zero ou mais nós XML) ou um único valor atômico.
* Ao contrário de uma sequência XQuery/XPath, que pode conter quaisquer itens desejados em qualquer ordem desejada, um conjunto de nós XPath 1.0 não tem ordem garantida e, como qualquer conjunto, não permite múltiplas aparições do mesmo item.

### Nota

A biblioteca libxml2 parece sempre retornar conjuntos de nós ao PostgreSQL com seus membros na mesma ordem relativa que tinham no documento de entrada. Sua documentação não se compromete com esse comportamento, e uma expressão XPath 1.0 não pode controlá-lo.
* Embora o XQuery/XPath forneça todos os tipos definidos no XML Schema e muitos operadores e funções sobre esses tipos, o XPath 1.0 tem apenas conjuntos de nós e os três tipos atômicos `boolean`, `double` e `string`.
* O XPath 1.0 não tem operador condicional. Uma expressão XQuery/XPath como `if ( hat ) then hat/@size else "no hat"` não tem equivalente no XPath 1.0.
* O XPath 1.0 não tem operador de comparação de ordenação para strings. Tanto `"cat" < "dog"` quanto `"cat" > "dog"` são falsos, porque cada um é uma comparação numérica de dois `NaN`s. Em contraste, `=` e `!=` comparam as strings como strings.
* O XPath 1.0 desfaz a distinção entre *comparações de valor* e *comparações gerais*, conforme definidas pelo XQuery/XPath. Tanto `sale/@hatsize = 7` quanto `sale/@customer = "alice"` são comparações quantificadas existencialmente, verdadeiras se houver algum `sale` com o valor dado para o atributo, mas `sale/@taxable = false()` é uma comparação de valor ao *valor booleano efetivo* de um conjunto de nós inteiro. É verdade apenas se nenhum `sale` tiver um atributo `taxable` de forma alguma.
* No modelo de dados XQuery/XPath, um *nó de documento* pode ter forma de documento (ou seja, exatamente um elemento de nível superior, com apenas comentários e instruções de processamento fora dele) ou forma de conteúdo (com essas restrições relaxadas). Seu equivalente no XPath 1.0, o *nó raiz*, só pode estar em forma de documento. Essa é parte da razão pela qual um valor `xml` passado como item de contexto para qualquer função baseada em XPath do PostgreSQL deve estar em forma de documento.

As diferenças destacadas aqui não são todas. No XQuery e nas versões 2.0 e posteriores do XPath, há um modo de compatibilidade XPath 1.0, e as listas do W3C de (https://www.w3.org/TR/2010/REC-xpath-functions-20101214/#xpath1-compatibility) de (https://www.w3.org/TR/xpath20/#id-backwards-compatibility) de (https://www.w3.org/TR/xpath20/#id-backwards-compatibility) de (https://www.w3.org/TR/2010/REC-xpath-functions-20101214/#xpath1-compatibility) que são aplicadas nesse modo oferecem uma descrição mais completa (mas ainda não exaustiva) das diferenças. O modo de compatibilidade não pode tornar as linguagens posteriores exatamente equivalentes ao XPath 1.0.

#### D.3.1.3. Mapeamentos entre tipos de dados SQL e XML e valores [#](#FUNCTIONS-XML-LIMITS-CASTS)

Em SQL:2006 e versões posteriores, ambas as direções de conversão entre os tipos de dados SQL padrão e os tipos do esquema XML são especificadas com precisão. No entanto, as regras são expressas usando os tipos e a semântica do XQuery/XPath, e não têm aplicação direta no modelo de dados diferente do XPath 1.0.

Quando o PostgreSQL mapeia os valores de dados SQL para XML (como no `xmlelement`), ou XML para SQL (como nas colunas de saída do `xmltable`), exceto em alguns casos tratados de forma especial, o PostgreSQL simplesmente assume que a forma de string XPath 1.0 do tipo de dados XML será válida como a forma de entrada de texto do tipo de dados SQL, e vice-versa. Esta regra tem a virtude da simplicidade enquanto produz, para muitos tipos de dados, resultados semelhantes aos mapeamentos especificados no padrão.

Quando a interoperabilidade com outros sistemas é uma preocupação, para alguns tipos de dados, pode ser necessário usar funções de formatação de tipos de dados (como as do [Seção 9.8] [(functions-formatting.md "9.8. Data Type Formatting Functions")]) explicitamente para produzir as mapeamentos padrão.

### D.3.2. Limites Incidentais da Implementação [#](#FUNCTIONS-XML-LIMITS-POSTGRESQL)

Esta seção trata de limites que não são inerentes à biblioteca libxml2, mas que se aplicam à implementação atual no PostgreSQL.

#### D.3.2.1. Apenas o Mecanismo de Passagem `BY VALUE` é suportado [#](#FUNCTIONS-XML-LIMITS-POSTGRESQL-BY-VALUE-ONLY)

O padrão SQL define dois *mecanismos de passagem* que se aplicam ao passar um argumento XML do SQL para uma função XML ou ao receber um resultado: `BY REF`, no qual um valor XML específico retém sua identidade de nó, e `BY VALUE`, no qual o conteúdo do XML é passado, mas a identidade do nó não é preservada. Um mecanismo pode ser especificado antes de uma lista de parâmetros, como o mecanismo padrão para todos eles, ou após qualquer parâmetro, para sobrescrever o padrão.

Para ilustrar a diferença, se *`x`* é um valor XML, essas duas consultas em um ambiente SQL:2006 produziriam verdadeiro e falso, respectivamente:

```
SELECT XMLQUERY('$a is $b' PASSING BY REF x AS a, x AS b NULL ON EMPTY);
SELECT XMLQUERY('$a is $b' PASSING BY VALUE x AS a, x AS b NULL ON EMPTY);
```

O PostgreSQL aceitará `BY VALUE` ou `BY REF` em uma construção `XMLEXISTS` ou `XMLTABLE`, mas ele os ignora. O tipo de dados `xml` contém uma representação serializada de cadeia de caracteres, portanto, não há identidade de nó a ser preservada, e a passagem é sempre efetivamente `BY VALUE`.

#### D.3.2.2. Não é possível passar parâmetros nomeados para consultas [#](#FUNCTIONS-XML-LIMITS-POSTGRESQL-NAMED-PARAMETERS)

As funções baseadas em XPath suportam a passagem de um parâmetro para servir como item de contexto da expressão XPath, mas não suportam a passagem de valores adicionais que devem estar disponíveis para a expressão como parâmetros nomeados.

#### D.3.2.3. Tipo `XML(SEQUENCE)` [#](#FUNCTIONS-XML-LIMITS-POSTGRESQL-NO-XML-SEQUENCE)

O tipo de dados PostgreSQL `xml` só pode conter um valor na forma `DOCUMENT` ou `CONTENT`. Um item de contexto de expressão XQuery/XPath deve ser um único nó XML ou um valor atômico, mas o XPath 1.0 o restringe ainda mais a ser apenas um nó XML, e não tem tipo de nó que permita `CONTENT`. O resultado é que um `DOCUMENT` bem formado é a única forma de valor XML que o PostgreSQL pode fornecer como um item de contexto de XPath.