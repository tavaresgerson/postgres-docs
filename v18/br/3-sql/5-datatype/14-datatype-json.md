## 8.14. Tipos de JSON [#](#DATATYPE-JSON)

* [8.14.1. Sintaxe de entrada e saída JSON](datatype-json.md#JSON-KEYS-ELEMENTS)
* [8.14.2. Projeto de documentos JSON](datatype-json.md#JSON-DOC-DESIGN)
* [8.14.3. `jsonb` Contenimento e existência](datatype-json.md#JSON-CONTAINMENT)
* [8.14.4. `jsonb` Indexação](datatype-json.md#JSON-INDEXING)
* [8.14.5. `jsonb` Subscrito](datatype-json.md#JSONB-SUBSCRIPTING)
* [8.14.6. Transformações](datatype-json.md#DATATYPE-JSON-TRANSFORMS)
* [8.14.7. Tipo jsonpath](datatype-json.md#DATATYPE-JSONPATH)

Os tipos de dados JSON são para armazenar dados de JSON (JavaScript Object Notation), conforme especificado em [RFC 7159](https://datatracker.ietf.org/doc/html/rfc7159). Esses dados também podem ser armazenados como `text`, mas os tipos de dados JSON têm a vantagem de impor que cada valor armazenado seja válido de acordo com as regras do JSON. Também existem funções e operadores específicos para JSON disponíveis para dados armazenados nesses tipos de dados; veja [Seção 9.16](functions-json.md).

O PostgreSQL oferece dois tipos para armazenar dados JSON: `json` e `jsonb`. Para implementar mecanismos de consulta eficientes para esses tipos de dados, o PostgreSQL também fornece o tipo de dados `jsonpath`, descrito na [Seção 8.14.7](datatype-json.md#DATATYPE-JSONPATH).

Os tipos de dados `json` e `jsonb` aceitam *quase* conjuntos idênticos de valores como entrada. A principal diferença prática é uma questão de eficiência. O tipo de dados `json` armazena uma cópia exata do texto de entrada, que as funções de processamento devem reparsear em cada execução; enquanto o tipo de dados `jsonb` é armazenado em um formato binário decomposto que o torna ligeiramente mais lento para entrada devido ao custo adicional de conversão, mas significativamente mais rápido para processamento, uma vez que não é necessário reparsear. O `jsonb` também suporta indexação, o que pode ser uma vantagem significativa.

Como o tipo `json` armazena uma cópia exata do texto de entrada, ele preservará o espaço em branco sem significado semântico entre os tokens, bem como a ordem das chaves dentro dos objetos JSON. Além disso, se um objeto JSON dentro do valor contiver a mesma chave mais de uma vez, todas as pares chave/valor são mantidos. (As funções de processamento consideram o último valor como o operacional.) Em contraste, `jsonb` não preserva o espaço em branco, não preserva a ordem das chaves dos objetos e não mantém chaves de objeto duplicadas. Se chaves duplicadas forem especificadas na entrada, apenas o último valor é mantido.

Em geral, a maioria das aplicações deve preferir armazenar dados JSON como `jsonb`, a menos que haja necessidades bastante especializadas, como suposições legadas sobre a ordem das chaves dos objetos.

O RFC 7159 especifica que as strings JSON devem ser codificadas em UTF8. Portanto, não é possível que os tipos JSON se conformem rigidamente à especificação JSON, a menos que a codificação do banco de dados seja UTF8. Tentativas de incluir diretamente caracteres que não podem ser representados na codificação do banco de dados falharão; por outro lado, caracteres que podem ser representados na codificação do banco de dados, mas não em UTF8, serão permitidos.

O RFC 7159 permite que as strings JSON contenham sequências de escape Unicode indicadas por `\uXXXX`. Na função de entrada para o tipo `json`, as escapas Unicode são permitidas, independentemente do codificação do banco de dados, e são verificadas apenas quanto à correção sintática (ou seja, que quatro dígitos hexadecimais sigam `\u`). No entanto, a função de entrada para o tipo `jsonb` é mais rigorosa: ela não permite escapas Unicode para caracteres que não podem ser representados na codificação do banco de dados. O tipo `jsonb` também rejeita `\u0000` (porque isso não pode ser representado no tipo `text` do PostgreSQL), e insiste que qualquer uso de pares de surogato Unicode para designar caracteres fora da Plane Multilíngue Básica Unicode seja correto. As escapas Unicode válidas são convertidas no caractere único equivalente para armazenamento; isso inclui a dobragem de pares de surogato em um único caractere.

Nota

Muitas das funções de processamento de JSON descritas em [Seção 9.16](functions-json.md) irão converter escapamentos Unicode em caracteres regulares, e, portanto, irão lançar os mesmos tipos de erros descritos anteriormente, mesmo que sua entrada seja do tipo `json`[(functions-json.md "9.16. JSON Functions and Operators")]. O fato de que a função de entrada `json` não faça essas verificações pode ser considerada um artefato histórico, embora permita o armazenamento simples (sem processamento) de escapamentos Unicode de JSON em um codificação de banco de dados que não suporte os caracteres representados.

Ao converter uma entrada textual JSON em `jsonb`, os tipos primitivos descritos pelo RFC 7159 são efetivamente mapeados em tipos nativos do PostgreSQL, conforme mostrado na [Tabela 8.23](datatype-json.md#JSON-TYPE-MAPPING-TABLE). Portanto, há algumas restrições adicionais menores sobre o que constitui dados válidos de `jsonb` que não se aplicam ao tipo `json`, nem ao JSON em abstrato, correspondendo a limites sobre o que pode ser representado pelo tipo de dados subjacente. Notavelmente, `jsonb` rejeitará números que estejam fora do intervalo do tipo de dados `numeric` do PostgreSQL, enquanto `json` não o fará. Tais restrições definidas pela implementação são permitidas pelo RFC 7159. No entanto, na prática, tais problemas são muito mais prováveis de ocorrer em outras implementações, pois é comum representar o tipo primitivo `number` do JSON como ponto flutuante de precisão dupla IEEE 754 (que o RFC 7159 antecipa e permite explicitamente). Ao usar JSON como um formato de intercâmbio com tais sistemas, o perigo de perder precisão numérica em comparação com os dados originalmente armazenados pelo PostgreSQL deve ser considerado.

Por outro lado, conforme observado na tabela, há algumas restrições menores no formato de entrada dos tipos primitivos JSON que não se aplicam aos tipos correspondentes do PostgreSQL.

**Tabela 8.23. Tipos primitivos JSON e tipos correspondentes do PostgreSQL**



<table border="1" class="table" summary="JSON Primitive Types and Corresponding PostgreSQL Types">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    JSON primitive type
   </th>
   <th>
    <span class="productname">
     PostgreSQL
    </span>
    type
   </th>
   <th>
    Notas
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="type">
     string
    </code>
   </td>
   <td>
    <code class="type">
     text
    </code>
   </td>
   <td>
    <code class="literal">
     \u0000
    </code>
    é proibido, assim como as escapadas Unicode que representam caracteres não disponíveis no codificação do banco de dados
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     number
    </code>
   </td>
   <td>
    <code class="type">
     numeric
    </code>
   </td>
   <td>
    <code class="literal">
     NaN
    </code>
    e
    <code class="literal">
     infinity
    </code>
    os valores não são permitidos
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     boolean
    </code>
   </td>
   <td>
    <code class="type">
     boolean
    </code>
   </td>
   <td>
    Apenas minúsculas
    <code class="literal">
     true
    </code>
    e
    <code class="literal">
     false
    </code>
    as grafias são aceitas
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     null
    </code>
   </td>
   <td>
    (none)
   </td>
   <td>
    SQL
    <code class="literal">
     NULL
    </code>
    é um conceito diferente
   </td>
  </tr>
 </tbody>
</table>










### 8.14.1. Sintaxe de entrada e saída JSON [#](#JSON-KEYS-ELEMENTS)

A sintaxe de entrada/saída para os tipos de dados JSON é conforme especificado no RFC 7159.

As seguintes expressões são válidas para `json` (ou `jsonb`):

```
-- Simple scalar/primitive value
-- Primitive values can be numbers, quoted strings, true, false, or null
SELECT '5'::json;

-- Array of zero or more elements (elements need not be of same type)
SELECT '[1, 2, "foo", null]'::json;

-- Object containing pairs of keys and values
-- Note that object keys must always be quoted strings
SELECT '{"bar": "baz", "balance": 7.77, "active": false}'::json;

-- Arrays and objects can be nested arbitrarily
SELECT '{"foo": [true, "bar"], "tags": {"a": 1, "b": null}}'::json;
```

Como já mencionado anteriormente, quando um valor JSON é inserido e, em seguida, impresso sem qualquer processamento adicional, `json` exibe o mesmo texto que foi inserido, enquanto `jsonb` não preserva detalhes sem importância semântica, como espaços em branco. Por exemplo, observe as diferenças aqui:

```
SELECT '{"bar": "baz", "balance": 7.77, "active":false}'::json;
                      json
-------------------------------------------------
 {"bar": "baz", "balance": 7.77, "active":false}
(1 row)

SELECT '{"bar": "baz", "balance": 7.77, "active":false}'::jsonb;
                      jsonb
--------------------------------------------------
 {"bar": "baz", "active": false, "balance": 7.77}
(1 row)
```

Um detalhe sem importância semântica que vale a pena notar é que, em `jsonb`, os números serão impressos de acordo com o comportamento do tipo subjacente `numeric`. Na prática, isso significa que os números inseridos com a notação `E` serão impressos sem ela, por exemplo:

```
SELECT '{"reading": 1.230e-5}'::json, '{"reading": 1.230e-5}'::jsonb;
         json          |          jsonb
-----------------------+-------------------------
 {"reading": 1.230e-5} | {"reading": 0.00001230}
(1 row)
```

No entanto, `jsonb` preservará zeros fracionários finais, como visto neste exemplo, embora esses sejam semanticamente insignificantes para fins como verificações de igualdade.

Para a lista de funções e operadores embutidos disponíveis para a construção e processamento de valores JSON, consulte [Seção 9.16](functions-json.md).

### 8.14.2. Projetando documentos JSON [#](#JSON-DOC-DESIGN)

Representar dados como JSON pode ser consideravelmente mais flexível do que o modelo de dados relacional tradicional, o que é convincente em ambientes onde os requisitos são fluidos. É perfeitamente possível que ambas as abordagens coexistem e se complementem dentro da mesma aplicação. No entanto, mesmo para aplicações onde a flexibilidade máxima é desejada, ainda é recomendado que os documentos JSON tenham uma estrutura um tanto fixa. A estrutura geralmente não é imposta (embora seja possível impor algumas regras comerciais declarativamente), mas ter uma estrutura previsível facilita a escrita de consultas que resumem de forma útil um conjunto de “documentos” (pontos de referência) em uma tabela.

Os dados JSON estão sujeitos às mesmas considerações de controle de concorrência que qualquer outro tipo de dados quando armazenados em uma tabela. Embora seja possível armazenar documentos grandes, lembre-se de que qualquer atualização adquire um bloqueio de nível de linha em toda a linha. Considere limitar os documentos JSON a um tamanho gerenciável para diminuir a concorrência de bloqueio entre as transações de atualização. Idealmente, os documentos JSON devem representar cada um um dado atômico que as regras comerciais ditam que não podem razoavelmente ser subdivididos em menores dados que poderiam ser modificados independentemente.

### 8.14.3. `jsonb` Contenimento e Existência [#](#JSON-CONTAINMENT)

Testar o *contenimento* é uma capacidade importante do `jsonb`. Não há um conjunto paralelo de instalações para o tipo `json`. O contenimento verifica se um documento `jsonb` contém outro documento. Esses exemplos retornam verdadeiro, exceto conforme indicado:

```
-- Simple scalar/primitive values contain only the identical value:
SELECT '"foo"'::jsonb @> '"foo"'::jsonb;

-- The array on the right side is contained within the one on the left:
SELECT '[1, 2, 3]'::jsonb @> '[1, 3]'::jsonb;

-- Order of array elements is not significant, so this is also true:
SELECT '[1, 2, 3]'::jsonb @> '[3, 1]'::jsonb;

-- Duplicate array elements don't matter either:
SELECT '[1, 2, 3]'::jsonb @> '[1, 2, 2]'::jsonb;

-- The object with a single pair on the right side is contained
-- within the object on the left side:
SELECT '{"product": "PostgreSQL", "version": 9.4, "jsonb": true}'::jsonb @> '{"version": 9.4}'::jsonb;

-- The array on the right side is not considered contained within the
-- array on the left, even though a similar array is nested within it:
SELECT '[1, 2, [1, 3]]'::jsonb @> '[1, 3]'::jsonb;  -- yields false

-- But with a layer of nesting, it is contained:
SELECT '[1, 2, [1, 3]]'::jsonb @> '[[1, 3]]'::jsonb;

-- Similarly, containment is not reported here:
SELECT '{"foo": {"bar": "baz"}}'::jsonb @> '{"bar": "baz"}'::jsonb;  -- yields false

-- A top-level key and an empty object is contained:
SELECT '{"foo": {"bar": "baz"}}'::jsonb @> '{"foo": {}}'::jsonb;
```

O princípio geral é que o objeto contido deve corresponder ao objeto contendo em termos de estrutura e conteúdo de dados, possivelmente após descartar alguns elementos de matriz que não correspondem ou pares de chave/valor do objeto contendo. Mas lembre-se de que a ordem dos elementos da matriz não é significativa ao fazer uma correspondência de contenção, e os elementos duplicados da matriz são efetivamente considerados apenas uma vez.

Como exceção especial ao princípio geral de que as estruturas devem corresponder, uma matriz pode conter um valor primitivo:

```
-- This array contains the primitive string value:
SELECT '["foo", "bar"]'::jsonb @> '"bar"'::jsonb;

-- This exception is not reciprocal -- non-containment is reported here:
SELECT '"bar"'::jsonb @> '["bar"]'::jsonb;  -- yields false
```

`jsonb` também tem um operador de *existência*, que é uma variação do tema de contenção: ele testa se uma string (dada como um valor `text` ) aparece como uma chave de objeto ou elemento de matriz no nível superior do valor `jsonb`. Esses exemplos retornam verdadeiro, exceto conforme observado:

```
-- String exists as array element:
SELECT '["foo", "bar", "baz"]'::jsonb ? 'bar';

-- String exists as object key:
SELECT '{"foo": "bar"}'::jsonb ? 'foo';

-- Object values are not considered:
SELECT '{"foo": "bar"}'::jsonb ? 'bar';  -- yields false

-- As with containment, existence must match at the top level:
SELECT '{"foo": {"bar": "baz"}}'::jsonb ? 'bar'; -- yields false

-- A string is considered to exist if it matches a primitive JSON string:
SELECT '"foo"'::jsonb ? 'foo';
```

Os objetos JSON são mais adequados do que os arrays para testar a contenção ou existência quando há muitos elementos ou chaves envolvidos, porque, ao contrário dos arrays, eles são otimizados internamente para pesquisa e não precisam ser pesquisados linearmente.

DICA

Como o conteúdo JSON é aninhado, uma consulta apropriada pode ignorar a seleção explícita de subobjetos. Como exemplo, suponha que tenhamos uma coluna `doc` contendo objetos no nível superior, com a maioria dos objetos contendo campos `tags` que contêm matrizes de subobjetos. Esta consulta encontra entradas nas quais subobjetos contendo tanto `"term":"paris"` quanto `"term":"food"` aparecem, ignorando quaisquer chaves desse tipo fora da matriz `tags`:

```
SELECT doc->'site_name' FROM websites
  WHERE doc @> '{"tags":[{"term":"paris"}, {"term":"food"}]}';
```

Se se quisesse, poderia-se fazer a mesma coisa com, por exemplo,

```
SELECT doc->'site_name' FROM websites
  WHERE doc->'tags' @> '[{"term":"paris"}, {"term":"food"}]';
```

mas essa abordagem é menos flexível e, muitas vezes, menos eficiente também.

Por outro lado, o operador de existência JSON não é aninhado: ele só procurará a chave ou o elemento de matriz especificados no nível superior do valor JSON.

Os vários operadores de contenção e existência, juntamente com todos os outros operadores e funções JSON, estão documentados em [Seção 9.16](functions-json.md).

### 8.14.4. `jsonb` Indicadores [#](#JSON-INDEXING)

Os índices GIN podem ser usados para pesquisar eficientemente chaves ou pares chave/valor que ocorrem em um grande número de documentos `jsonb` (datums). Dois "classes de operadores" GIN são fornecidos, oferecendo diferentes compromissos em termos de desempenho e flexibilidade.

A classe de operador GIN padrão para `jsonb` suporta consultas com os operadores key-exists `?`, `?|` e `?&`, o operador de contenção `@>` e os operadores de correspondência `@?` e `@@` do `jsonpath` (Para detalhes sobre a semântica que esses operadores implementam, consulte a [Tabela 9.48](functions-json.md#FUNCTIONS-JSONB-OP-TABLE)). Um exemplo de criação de um índice com essa classe de operador é:

```
CREATE INDEX idxgin ON api USING GIN (jdoc);
```

A classe de operadores GIN não padrão `jsonb_path_ops` não suporta os operadores key-exists, mas suporta `@>`, `@?` e `@@`. Um exemplo de criação de um índice com essa classe de operadores é:

```
CREATE INDEX idxginp ON api USING GIN (jdoc jsonb_path_ops);
```

Considere o exemplo de uma tabela que armazena documentos JSON recuperados de um serviço web de terceiros, com uma definição de esquema documentada. Um documento típico é:

```
{
    "guid": "9c36adc1-7fb5-4d5b-83b4-90356a46061a",
    "name": "Angela Barton",
    "is_active": true,
    "company": "Magnafone",
    "address": "178 Howard Place, Gulf, Washington, 702",
    "registered": "2009-11-07T08:53:22 +08:00",
    "latitude": 19.793713,
    "longitude": 86.513373,
    "tags": [
        "enim",
        "aliquip",
        "qui"
    ]
}
```

Armazenamos esses documentos em uma tabela chamada `api`, em uma coluna `jsonb` chamada `jdoc`. Se um índice GIN for criado nesta coluna, consultas como as seguintes podem utilizar o índice:

```
-- Find documents in which the key "company" has value "Magnafone"
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc @> '{"company": "Magnafone"}';
```

No entanto, o índice não pode ser usado para consultas como as seguintes, porque, embora o operador `?` seja indexável, ele não é aplicado diretamente à coluna indexada `jdoc`:

```
-- Find documents in which the key "tags" contains key or array element "qui"
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc -> 'tags' ? 'qui';
```

Ainda assim, com o uso apropriado de índices de expressão, a consulta acima pode usar um índice. Se a consulta a itens específicos dentro da chave `"tags"` é comum, definir um índice assim pode ser útil:

```
CREATE INDEX idxgintags ON api USING GIN ((jdoc -> 'tags'));
```

Agora, a cláusula `WHERE` `jdoc -> 'tags' ? 'qui'` será reconhecida como uma aplicação do operador indexável `?` à expressão indexada `jdoc -> 'tags'`. (Mais informações sobre índices de expressão podem ser encontradas em [Seção 11.7](indexes-expressional.md).

Outra abordagem para fazer consultas é explorar a contenção, por exemplo:

```
-- Find documents in which the key "tags" contains array element "qui"
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc @> '{"tags": ["qui"]}';
```

Um índice GIN simples na coluna `jdoc` pode suportar essa consulta. Mas observe que tal índice armazenará cópias de todas as chaves e valores na coluna `jdoc`, enquanto o índice de expressão do exemplo anterior armazena apenas dados encontrados sob a chave `tags`. Embora a abordagem de índice simples seja muito mais flexível (já que suporta consultas sobre qualquer chave), os índices de expressão direcionados provavelmente serão menores e mais rápidos de pesquisar do que um índice simples.

Os índices GIN também suportam os operadores `@?` e `@@`, que realizam a correspondência `jsonpath`. Exemplos são

```
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc @? '$.tags[*] ? (@ == "qui")';
```

```
SELECT jdoc->'guid', jdoc->'name' FROM api WHERE jdoc @@ '$.tags[*] == "qui"';
```

Para esses operadores, um índice GIN extrai cláusulas do tipo `accessors_chain == constant` do padrão `jsonpath`, e realiza a busca no índice com base nas chaves e valores mencionados nessas cláusulas. A cadeia de acessores pode incluir os acessores `.key`, `[*]` e `[index]`. A classe de operadores `jsonb_ops` também suporta os acessores `.*` e `.**`, mas a classe de operadores `jsonb_path_ops`

Embora a classe de operadores `jsonb_path_ops` suporte apenas consultas com os operadores `@>`, `@?` e `@@`, ela possui vantagens notáveis de desempenho em relação à classe de operadores padrão `jsonb_ops`. Um índice `jsonb_path_ops` geralmente é muito menor do que um índice `jsonb_ops` sobre os mesmos dados, e a especificidade das pesquisas é melhor, particularmente quando as consultas contêm chaves que aparecem frequentemente nos dados. Portanto, as operações de pesquisa geralmente se saem melhor do que com a classe de operadores padrão.

A diferença técnica entre um índice `jsonb_ops` e um índice GIN `jsonb_path_ops` é que o primeiro cria itens de índice independentes para cada chave e valor nos dados, enquanto o segundo cria itens de índice apenas para cada valor nos dados. [[7]](#ftn.id-1.5.7.22.18.9.3) Basicamente, cada item de índice `jsonb_path_ops` é um hash do valor e da(s) chave(s) que o levam a; por exemplo, para indexar `{"foo": {"bar": "baz"}}`, um único item de índice seria criado incorporando todos os três `foo`, `bar` e `baz` no valor do hash. Assim, uma consulta de contenção que procura essa estrutura resultaria em uma pesquisa de índice extremamente específica; mas não há absolutamente nenhuma maneira de descobrir se `foo` aparece como uma chave. Por outro lado, um índice `jsonb_ops` criaria três itens de índice representando `foo`, `bar` e `baz` separadamente; então, para fazer a consulta de contenção, procuraria linhas que contenham os três itens. Embora os índices GIN possam realizar uma pesquisa AND de forma bastante eficiente, ainda assim será menos específica e mais lenta do que a pesquisa equivalente `jsonb_path_ops`, especialmente se houver um número muito grande de linhas que contenham qualquer um dos três itens de índice.

Uma desvantagem da abordagem `jsonb_path_ops` é que ela não produz entradas de índice para estruturas JSON que não contêm quaisquer valores, como `{"a": {}}`. Se uma busca por documentos que contenham tal estrutura for solicitada, será necessário realizar uma varredura completa do índice, o que é bastante lento. `jsonb_path_ops` é, portanto, pouco adequado para aplicações que realizam frequentemente tais buscas.

`jsonb` também suporta os índices `btree` e `hash`. Esses índices geralmente são úteis apenas se for importante verificar a igualdade de documentos JSON completos. A ordenação `btree` para os `jsonb` datas raramente é de grande interesse, mas, por completo, é:

```
Object > Array > Boolean > Number > String > null

Object with n pairs > object with n - 1 pairs

Array with n elements > array with n - 1 elements
```

com a exceção de que (por razões históricas) um array de nível superior vazio ordena menos que *`null`*. Os objetos com o mesmo número de pares são comparados na ordem:

```
key-1, value-1, key-2 ...
```

Observe que as chaves dos objetos são comparadas em sua ordem de armazenamento; em particular, uma vez que as chaves mais curtas são armazenadas antes das mais longas, isso pode levar a resultados que podem ser pouco intuitivos, como:

```
{ "aa": 1, "c": 1} > {"b": 1, "d": 1}
```

Da mesma forma, os arrays com números iguais de elementos são comparados na ordem:

```
element-1, element-2 ...
```

Os valores primitivos do JSON são comparados usando as mesmas regras de comparação que para o tipo de dados subjacente do PostgreSQL. As cadeias são comparadas usando a collation padrão do banco de dados.

### 8.14.5. Subscrito [#](#JSONB-SUBSCRIPTING)

O tipo de dados `jsonb` suporta expressões de índice em estilo de matriz para extrair e modificar elementos. Valores aninhados podem ser indicados concatenando expressões de índice, seguindo as mesmas regras do argumento `path` na função `jsonb_set`. Se um valor `jsonb` for uma matriz, os índices numéricos começam em zero, e os inteiros negativos contam para trás a partir do último elemento da matriz. Expressões de fatiamento não são suportadas. O resultado de uma expressão de índice é sempre do tipo de dados jsonb.

As declarações `UPDATE` podem usar subscrito na cláusula `SET` para modificar os valores de `jsonb`. Os caminhos de subscrito devem ser percorríveis para todos os valores afetados, na medida em que existam. Por exemplo, o caminho `val['a']['b']['c']` pode ser percorrido até `c` se todos os `val`, `val['a']` e `val['a']['b']` forem objetos. Se qualquer `val['a']` ou `val['a']['b']` não for definido, ele será criado como um objeto vazio e preenchido conforme necessário. No entanto, se qualquer `val` ou um dos valores intermediários for definido como um não-objeto, como uma string, número ou `jsonb` `null`, a travessia não pode prosseguir, então um erro é gerado e a transação é abortada.

Um exemplo de sintaxe de subscrito:

```
-- Extract object value by key
SELECT ('{"a": 1}'::jsonb)['a'];

-- Extract nested object value by key path
SELECT ('{"a": {"b": {"c": 1}}}'::jsonb)['a']['b']['c'];

-- Extract array element by index
SELECT ('[1, "2", null]'::jsonb)[1];

-- Update object value by key. Note the quotes around '1': the assigned
-- value must be of the jsonb type as well
UPDATE table_name SET jsonb_field['key'] = '1';

-- This will raise an error if any record's jsonb_field['a']['b'] is something
-- other than an object. For example, the value {"a": 1} has a numeric value
-- of the key 'a'.
UPDATE table_name SET jsonb_field['a']['b']['c'] = '1';

-- Filter records using a WHERE clause with subscripting. Since the result of
-- subscripting is jsonb, the value we compare it against must also be jsonb.
-- The double quotes make "value" also a valid jsonb string.
SELECT * FROM table_name WHERE jsonb_field['key'] = '"value"';
```

A atribuição via subscrito lida alguns casos de borda de maneira diferente da `jsonb_set`. Quando o valor da fonte `jsonb` é `NULL`, a atribuição via subscrito procederá como se fosse um valor JSON vazio do tipo (objeto ou matriz) implícito pela chave de subscrito:

```
-- Where jsonb_field was NULL, it is now {"a": 1}
UPDATE table_name SET jsonb_field['a'] = '1';

-- Where jsonb_field was NULL, it is now [1]
UPDATE table_name SET jsonb_field[0] = '1';
```

Se um índice for especificado para um array que contém poucos elementos, os elementos `NULL` serão anexados até que o índice seja alcançável e o valor possa ser definido.

```
-- Where jsonb_field was [], it is now [null, null, 2];
-- where jsonb_field was [0], it is now [0, null, 2]
UPDATE table_name SET jsonb_field[2] = '2';
```

Um valor `jsonb` aceitará atribuições a caminhos de subscrito inexistentes, desde que o último elemento existente a ser percorrido seja um objeto ou uma matriz, conforme implícito pelo subscrito correspondente (o elemento indicado pelo último subscrito no caminho não é percorrido e pode ser qualquer coisa). Estruturas de matriz e objeto aninhadas serão criadas, e no primeiro caso, `null` preenchidas, conforme especificado pelo caminho de subscrito até que o valor atribuído possa ser colocado.

```
-- Where jsonb_field was {}, it is now {"a": [{"b": 1}]}
UPDATE table_name SET jsonb_field['a'][0]['b'] = '1';

-- Where jsonb_field was [], it is now [null, {"a": 1}]
UPDATE table_name SET jsonb_field[1]['a'] = '1';
```

### 8.14.6. Transformações [#](#DATATYPE-JSON-TRANSFORMS)

Existem extensões adicionais disponíveis que implementam transformações para o tipo `jsonb` para diferentes linguagens processuais.

As extensões para PL/Perl são chamadas de `jsonb_plperl` e `jsonb_plperlu`. Se você as usar, os valores de `jsonb` são mapeados para arrays, hashes e escalares em Perl, conforme apropriado.

A extensão para PL/Python é chamada de `jsonb_plpython3u`. Se você a usar, os valores de `jsonb` são mapeados para dicionários, listas e escalares em Python, conforme apropriado.

Desses extensões, a `jsonb_plperl` é considerada “confiável”, ou seja, pode ser instalada por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual. O restante requer privilégio de superusuário para instalação.

### 8.14.7. jsonpath Tipo [#](#DATATYPE-JSONPATH)

O tipo `jsonpath` implementa suporte para o idioma de caminho SQL/JSON no PostgreSQL para consultar eficientemente dados JSON. Ele fornece uma representação binária da expressão de caminho SQL/JSON analisada que especifica os itens que devem ser recuperados pelo motor de caminho a partir dos dados JSON para processamento adicional com as funções de consulta SQL/JSON.

A semântica dos predicados e operadores de caminho SQL/JSON geralmente segue a SQL. Ao mesmo tempo, para fornecer uma maneira natural de trabalhar com dados JSON, a sintaxe de caminho SQL/JSON usa algumas convenções do JavaScript:

* Ponto (`.`) é usado para acesso aos membros.
* Colchetes (`[]`) são usados para acesso a arrays.
* Os arrays SQL/JSON são relativos a 0, ao contrário dos arrays regulares SQL que começam a partir do número 1.

Os literais numéricos em expressões de caminho SQL/JSON seguem as regras do JavaScript, que são diferentes tanto do SQL quanto do JSON em alguns detalhes menores. Por exemplo, o caminho SQL/JSON permite `.1` e `1.`, que são inválidos no JSON. Literais de inteiro não decimal e separadores de sublinhado são suportados, por exemplo, `1_000_000`, `0x1EEE_FFFF`, `0o273`, `0b100101`. No caminho SQL/JSON (e em JavaScript, mas não no SQL propriamente dito), não deve haver um separador de sublinhado diretamente após o prefixo de radix.

Uma expressão de caminho SQL/JSON é normalmente escrita em uma consulta SQL como uma literal de cadeia de caracteres SQL, então ela deve ser fechada entre aspas, e quaisquer aspas desejadas dentro do valor devem ser duplicadas (ver [Seção 4.1.2.1] (sql-syntax-lexical.md#SQL-SYNTAX-STRINGS "4.1.2.1. String Constants")). Algumas formas de expressões de caminho requerem literais de cadeia de caracteres dentro delas. Essas literais de cadeia de caracteres incorporadas seguem as convenções do JavaScript/ECMAScript: elas devem ser cercadas por aspas duplas, e escapamentos de barra podem ser usados dentro delas para representar caracteres de difícil digitação. Em particular, a maneira de escrever uma aspas dupla dentro de uma literal de cadeia de caracteres incorporada é `\"`, e para escrever uma barra ela mesma, você deve escrever `\\`. Outras sequências especiais de barra incluem as reconhecidas em strings de JavaScript: `\b`, `\f`, `\n`, `\r`, `\t`, `\v` para vários caracteres de controle ASCII, `\xNN` para um código de caractere escrito com apenas dois dígitos hexadecimais, `\uNNNN` para um caractere Unicode identificado por seu ponto de código de 4 dígitos hexadecimais, e `\u{N...}` para um ponto de código de caractere Unicode escrito com 1 a 6 dígitos hexadecimais.

Uma expressão de caminho consiste em uma sequência de elementos de caminho, que podem ser qualquer um dos seguintes:

* Literais de caminho de tipos primitivos JSON: texto Unicode, numérico, verdadeiro, falso ou nulo.
* Variáveis de caminho listadas em [Tabela 8.24](datatype-json.md#TYPE-JSONPATH-VARIABLES).
* Operadores de acesso listados em [Tabela 8.25](datatype-json.md#TYPE-JSONPATH-ACCESSORS).
* Operadores e métodos `jsonpath` listados em [Seção 9.16.2.3](functions-json.md#FUNCTIONS-SQLJSON-PATH-OPERATORS).
* Parenteses, que podem ser usadas para fornecer expressões de filtro ou definir a ordem de avaliação do caminho.

Para obter detalhes sobre o uso das expressões `jsonpath` com funções de consulta SQL/JSON, consulte [Seção 9.16.2](functions-json.md#FUNCTIONS-SQLJSON-PATH).

**Tabela 8.24. `jsonpath` Variáveis**



<table border="1" class="table" summary="jsonpath Variables">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Variable
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
     $
    </code>
   </td>
   <td>
    Uma variável que representa o valor JSON que está sendo pesquisado
    <em class="firstterm">
     item de contexto
    </em>
    ).
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     $varname
    </code>
   </td>
   <td>
    Uma variável nomeada. Seu valor pode ser definido pelo parâmetro
    <em class="parameter">
     <code>
      vars
     </code>
    </em>
    de várias funções de processamento de JSON;
    <a class="xref" href="functions-json.md#FUNCTIONS-JSON-PROCESSING-TABLE" title="Table 9.51. JSON Processing Functions">
     Tabela 9.51
    </a>
    para obter mais informações.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     @
    </code>
   </td>
   <td>
    Uma variável que representa o resultado da avaliação do caminho em expressões de filtro.
   </td>
  </tr>
 </tbody>
</table>










**Tabela 8.25. `jsonpath` Acessórios**



<table border="1" class="table" summary="jsonpath Accessors">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Operador de Acessórios
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <p>
     <code class="literal">
      .
      <em class="replaceable">
       <code>
        key
       </code>
      </em>
     </code>
    </p>
    <p>
     <code class="literal">
      ."$
      <em class="replaceable">
       <code>
        varname
       </code>
      </em>
      "
     </code>
    </p>
   </td>
   <td>
    <p>
     Accessor de membro que retorna um membro de objeto com a chave especificada. Se o nome da chave corresponder a alguma variável nomeada que comece com
     <code class="literal">
      $
     </code>
     ou não atende às regras do JavaScript para um identificador, ele deve ser fechado entre aspas duplas para torná-lo um literal de string.
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     <code class="literal">
      .*
     </code>
    </p>
   </td>
   <td>
    <p>
     Acededor de membros wildcard que retorna os valores de todos os membros localizados no nível superior do objeto atual.
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     <code class="literal">
      .**
     </code>
    </p>
   </td>
   <td>
    <p>
     Acesso recursivo a membros com wildcard que processa todos os níveis da hierarquia JSON do objeto atual e retorna todos os valores dos membros, independentemente do seu nível de aninhamento. Isso é
     <span class="productname">
      PostgreSQL
     </span>
     extensão do padrão SQL/JSON.
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     <code class="literal">
      .**{
      <em class="replaceable">
       <code>
        level
       </code>
      </em>
      }
     </code>
    </p>
    <p>
     <code class="literal">
      .**{
      <em class="replaceable">
       <code>
        start_level
       </code>
      </em>
      to
      <em class="replaceable">
       <code>
        end_level
       </code>
      </em>
      }
     </code>
    </p>
   </td>
   <td>
    <p>
     Como
     <code class="literal">
      .**
     </code>
     , mas seleciona apenas os níveis especificados da hierarquia JSON. Os níveis de ninho são especificados como inteiros. O nível zero corresponde ao objeto atual. Para acessar o nível de ninho mais baixo, você pode usar o
     <code class="literal">
      last
     </code>
     palavra-chave. Isso é
     <span class="productname">
      PostgreSQL
     </span>
     extensão do padrão SQL/JSON.
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     <code class="literal">
      [
      <em class="replaceable">
       <code>
        subscript
       </code>
      </em>
      , ...]
     </code>
    </p>
   </td>
   <td>
    <p>
     Acesso ao elemento do array.
     <code class="literal">
      <em class="replaceable">
       <code>
        subscript
       </code>
      </em>
     </code>
     pode ser administrada em duas formas:
     <code class="literal">
      <em class="replaceable">
       <code>
        index
       </code>
      </em>
     </code>
     ou
     <code class="literal">
      <em class="replaceable">
       <code>
        start_index
       </code>
      </em>
      to
      <em class="replaceable">
       <code>
        end_index
       </code>
      </em>
     </code>
     A primeira forma retorna um único elemento de array pelo seu índice. A segunda forma retorna uma fatia de array pelo intervalo de índices, incluindo os elementos que correspondem ao fornecido.
     <em class="replaceable">
      <code>
       start_index
      </code>
     </em>
     e
     <em class="replaceable">
      <code>
       end_index
      </code>
     </em>
     .
    </p>
    <p>
     O especificado
     <em class="replaceable">
      <code>
       index
      </code>
     </em>
     pode ser um inteiro, bem como uma expressão que retorna um único valor numérico, que é automaticamente convertido para inteiro. O índice zero corresponde ao primeiro elemento da matriz. Você também pode usar o
     <code class="literal">
      last
     </code>
     palavra-chave para denotar o último elemento da matriz, o que é útil para manipular matrizes de comprimento desconhecido.
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     <code class="literal">
      [*]
     </code>
    </p>
   </td>
   <td>
    <p>
     Elemento de acesso de matriz com sinal de interrogação que retorna todos os elementos da matriz.
    </p>
   </td>
  </tr>
 </tbody>
</table>








---

[[7]](#id-1.5.7.22.18.9.3) Para esse propósito, o termo "valor" inclui elementos de matriz, embora a terminologia do JSON às vezes considere os elementos de matriz distintos dos valores dentro dos objetos.