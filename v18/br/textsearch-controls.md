## 12.3. Controle da pesquisa de texto [#](#TEXTSEARCH-CONTROLS)

* [12.3.1. Análise de documentos](textsearch-controls.md#TEXTSEARCH-PARSING-DOCUMENTS)
* [12.3.2. Análise de consultas](textsearch-controls.md#TEXTSEARCH-PARSING-QUERIES)
* [12.3.3. Classificação dos resultados de pesquisa](textsearch-controls.md#TEXTSEARCH-RANKING)
* [12.3.4. Destaque dos resultados](textsearch-controls.md#TEXTSEARCH-HEADLINE)

Para implementar a pesquisa de texto completo, deve haver uma função para criar um `tsvector` a partir de um documento e um `tsquery` a partir de uma consulta do usuário. Além disso, precisamos retornar os resultados em uma ordem útil, então precisamos de uma função que compare os documentos em relação à sua relevância para a consulta. Também é importante ser capaz de exibir os resultados de forma agradável. O PostgreSQL oferece suporte para todas essas funções.

### 12.3.1. Análise de documentos [#](#TEXTSEARCH-PARSING-DOCUMENTS)

O PostgreSQL fornece a função `to_tsvector` para a conversão de um documento para o tipo de dados `tsvector`.

```
to_tsvector([ config regconfig, ] document text) returns tsvector
```

`to_tsvector` analisa um documento textual em tokens, reduz os tokens a lexema e retorna um `tsvector` que lista os lexema juntamente com suas posições no documento. O documento é processado de acordo com a configuração de busca de texto especificada ou padrão. Aqui está um exemplo simples:

```
SELECT to_tsvector('english', 'a fat  cat sat on a mat - it ate a fat rats');
                  to_tsvector
-----------------------------------------------------
 'ate':9 'cat':3 'fat':2,11 'mat':7 'rat':12 'sat':4
```

No exemplo acima, vemos que o resultado `tsvector` não contém as palavras `a`, `on` ou `it`, a palavra `rats` se tornou `rat`, e o sinal de pontuação `-` foi ignorado.

A função `to_tsvector` chama internamente um analisador que quebra o texto do documento em tokens e atribui um tipo a cada token. Para cada token, uma lista de dicionários ([Seção 12.6](textsearch-dictionaries.md "12.6. Dictionaries")) é consultada, onde a lista pode variar dependendo do tipo do token. O primeiro dicionário que *reconhece* o token emite um ou mais *lexemas* normalizados para representar o token. Por exemplo, `rats` se tornou `rat` porque um dos dicionários reconheceu que a palavra `rats` é uma forma plural de `rat`. Algumas palavras são reconhecidas como *palavras-stop* ([Seção 12.6.1](textsearch-dictionaries.md#TEXTSEARCH-STOPWORDS "12.6.1. Stop Words")), o que as faz ser ignoradas, já que ocorrem com muita frequência para serem úteis na pesquisa. No nosso exemplo, essas são `a`, `on` e `it`. Se nenhum dicionário na lista reconhece o token, ele também é ignorado. Neste exemplo, isso aconteceu com o sinal de pontuação `-`, porque, na verdade, não há dicionários atribuídos para seu tipo de token ([[`Space symbols`]), o que significa que tokens de espaço nunca serão indexados. As escolhas do analisador, dicionários e quais tipos de tokens indexar são determinados pela configuração de busca de texto selecionada ([Seção 12.7](textsearch-configuration.md "12.7. Configuration Example")). É possível ter muitas configurações diferentes no mesmo banco de dados, e configurações predefinidas estão disponíveis para vários idiomas. No nosso exemplo, usamos a configuração padrão `english` para o idioma inglês.

A função `setweight` pode ser usada para marcar as entradas de um `tsvector` com um *peso* dado, onde um peso é uma das letras `A`, `B`, `C` ou `D`. Isso é tipicamente usado para marcar entradas que vêm de diferentes partes de um documento, como título versus corpo. Mais tarde, essas informações podem ser usadas para classificar os resultados de pesquisa.

Como `to_tsvector`(`NULL`) retornará `NULL`, é recomendável usar `coalesce` sempre que um campo possa ser nulo. Aqui está o método recomendado para criar um `tsvector` a partir de um documento estruturado:

```
UPDATE tt SET ti =
    setweight(to_tsvector(coalesce(title,'')), 'A')    ||
    setweight(to_tsvector(coalesce(keyword,'')), 'B')  ||
    setweight(to_tsvector(coalesce(abstract,'')), 'C') ||
    setweight(to_tsvector(coalesce(body,'')), 'D');
```

Aqui, usamos `setweight` para marcar a fonte de cada léxico no `tsvector` final, e depois mesclou os valores marcados de `tsvector` usando o operador de concatenação `tsvector` `||`. ([Seção 12.4.1](textsearch-features.md#TEXTSEARCH-MANIPULATE-TSVECTOR "12.4.1. Manipulating Documents") dá detalhes sobre essas operações.)

### 12.3.2. Análise de consultas [#](#TEXTSEARCH-PARSING-QUERIES)

O PostgreSQL fornece as funções `to_tsquery`, `plainto_tsquery`, `phraseto_tsquery` e `websearch_to_tsquery` para converter uma consulta para o tipo de dados `tsquery`. `to_tsquery` oferece acesso a mais recursos do que `plainto_tsquery` ou `phraseto_tsquery`, mas é menos tolerante em relação à sua entrada. `websearch_to_tsquery` é uma versão simplificada de `to_tsquery` com uma sintaxe alternativa, semelhante àquela usada por motores de busca na web.

```
to_tsquery([ config regconfig, ] querytext text) returns tsquery
```

`to_tsquery` cria um valor `tsquery` a partir de *`querytext`*, que deve consistir em tokens únicos separados por os operadores `tsquery` `&` (E), `|` (OU), `!` (NÃO) e `<->` (SE SEGUIDO POR), possivelmente agrupados usando parênteses. Em outras palavras, a entrada para `to_tsquery` deve seguir as regras gerais para a entrada de `tsquery`, conforme descrito em [Seção 8.11.2](datatype-textsearch.md#DATATYPE-TSQUERY "8.11.2. tsquery"). A diferença é que, enquanto a entrada básica de `tsquery` assume os tokens no seu valor face, `to_tsquery` normaliza cada token em um lexema usando a configuração especificada ou padrão, e descarta quaisquer tokens que são palavras de parada de acordo com a configuração. Por exemplo:

```
SELECT to_tsquery('english', 'The & Fat & Rats');
  to_tsquery
---------------
 'fat' & 'rat'
```

Assim como na entrada básica do `tsquery`, o(s) peso(s) pode(m) ser anexado(s) a cada léxico para restringi-lo(s) a corresponder apenas aos léxicos do `tsvector` desses peso(s). Por exemplo:

```
SELECT to_tsquery('english', 'Fat | Rats:AB');
    to_tsquery
------------------
 'fat' | 'rat':AB
```

Além disso, `*` pode ser anexado a um lexema para especificar a correspondência de prefixo:

```
SELECT to_tsquery('supern:*A & star:A*B');
        to_tsquery
--------------------------
 'supern':*A & 'star':*AB
```

Tal léxico corresponderá a qualquer palavra em um `tsvector` que comece com a cadeia de caracteres fornecida.

`to_tsquery` também pode aceitar frases com aspas simples. Isso é principalmente útil quando a configuração inclui um dicionário de sinônimos que pode ser acionado por essas frases. No exemplo abaixo, um sinônimo contém a regra `supernovae stars : sn`:

```
SELECT to_tsquery('''supernovae stars'' & !crab');
  to_tsquery
---------------
 'sn' & !'crab'
```

Sem aspas, `to_tsquery` gerará um erro de sintaxe para tokens que não são separados por um operador AND, OR ou FOLLOWED BY.

```
plainto_tsquery([ config regconfig, ] querytext text) returns tsquery
```

`plainto_tsquery` transforma o texto não formatado *`querytext`* em um valor `tsquery`. O texto é analisado e normalizado de forma semelhante ao de `to_tsvector`, e em seguida, o operador `&` (E) `tsquery` é inserido entre as palavras que sobreviveram.

Exemplo:

```
SELECT plainto_tsquery('english', 'The Fat Rats');
 plainto_tsquery
-----------------
 'fat' & 'rat'
```

Observe que o `plainto_tsquery` não reconhecerá operadores `tsquery`, rótulos de peso ou rótulos de correspondência de prefixo em sua entrada:

```
SELECT plainto_tsquery('english', 'The Fat & Rats:C');
   plainto_tsquery
---------------------
 'fat' & 'rat' & 'c'
```

Aqui, toda a pontuação de entrada foi descartada.

```
phraseto_tsquery([ config regconfig, ] querytext text) returns tsquery
```

`phraseto_tsquery` se comporta de maneira muito semelhante a `plainto_tsquery`, exceto que insere o operador `<->` (SEGUIDO POR) entre as palavras sobreviventes, em vez do operador `&` (E). Além disso, as palavras paralisantes não são simplesmente descartadas, mas são contabilizadas pela inserção de operadores `<N>` em vez de operadores `<->`. Esta função é útil ao procurar sequências exatas de léxico, uma vez que os operadores SEGUIDO POR verificam a ordem do léxico, não apenas a presença de todos os léxicos.

Exemplo:

```
SELECT phraseto_tsquery('english', 'The Fat Rats');
 phraseto_tsquery
------------------
 'fat' <-> 'rat'
```

Assim como a função `plainto_tsquery`, a função `phraseto_tsquery` não reconhecerá operadores `tsquery`, rótulos de peso ou rótulos de correspondência de prefixo em sua entrada:

```
SELECT phraseto_tsquery('english', 'The Fat & Rats:C');
      phraseto_tsquery
-----------------------------
 'fat' <-> 'rat' <-> 'c'
```

```
websearch_to_tsquery([ config regconfig, ] querytext text) returns tsquery
```

`websearch_to_tsquery` cria um valor `tsquery` a partir de *`querytext`* usando uma sintaxe alternativa na qual o texto simples não formatado é uma consulta válida. Ao contrário de `plainto_tsquery` e `phraseto_tsquery`, ele também reconhece certos operadores. Além disso, essa função nunca apresentará erros de sintaxe, o que permite o uso de entrada bruta fornecida pelo usuário para a pesquisa. A sintaxe a seguir é suportada:

* `unquoted text`: o texto que não está entre aspas será convertido em termos separados por operadores `&`, como se fosse processado por `plainto_tsquery`.
* `"quoted text"`: o texto entre aspas será convertido em termos separados por operadores `<->`, como se fosse processado por `phraseto_tsquery`.
* `OR`: a palavra “ou” será convertida no operador `|`.
* `-`: uma barra será convertida no operador `!`.

Outras pontuações são ignoradas. Assim como `plainto_tsquery` e `phraseto_tsquery`, a função `websearch_to_tsquery` não reconhecerá operadores `tsquery`, rótulos de peso ou rótulos de correspondência de prefixo em sua entrada.

Exemplos:

```
SELECT websearch_to_tsquery('english', 'The fat rats');
 websearch_to_tsquery
----------------------
 'fat' & 'rat'
(1 row)

SELECT websearch_to_tsquery('english', '"supernovae stars" -crab');
       websearch_to_tsquery
----------------------------------
 'supernova' <-> 'star' & !'crab'
(1 row)

SELECT websearch_to_tsquery('english', '"sad cat" or "fat rat"');
       websearch_to_tsquery
-----------------------------------
 'sad' <-> 'cat' | 'fat' <-> 'rat'
(1 row)

SELECT websearch_to_tsquery('english', 'signal -"segmentation fault"');
         websearch_to_tsquery
---------------------------------------
 'signal' & !( 'segment' <-> 'fault' )
(1 row)

SELECT websearch_to_tsquery('english', '""" )( dummy \\ query <->');
 websearch_to_tsquery
----------------------
 'dummi' & 'queri'
(1 row)
```

### 12.3.3. Resultados de pesquisa por classificação [#](#TEXTSEARCH-RANKING)

As tentativas de classificação tentam medir quão relevantes os documentos são para uma consulta específica, para que, quando houver muitas correspondências, os mais relevantes possam ser exibidos primeiro. O PostgreSQL fornece duas funções de classificação predefinidas, que levam em conta informações lexicais, de proximidade e estruturais; ou seja, consideram quão frequentemente os termos da consulta aparecem no documento, quão próximos os termos estão no documento e quão importante é a parte do documento onde eles ocorrem. No entanto, o conceito de relevância é vago e muito específico para cada aplicação. Diferentes aplicações podem exigir informações adicionais para a classificação, por exemplo, o tempo de modificação do documento. As funções de classificação integradas são apenas exemplos. Você pode escrever suas próprias funções de classificação e/ou combinar seus resultados com fatores adicionais para atender às suas necessidades específicas.

As duas funções de classificação atualmente disponíveis são:

`ts_rank([ weights float4[], ] vector tsvector, query tsquery [, normalization integer ]) returns float4`: Classifica vetores com base na frequência de seus lexemas correspondentes.

`ts_rank_cd([ weights float4[], ] vector tsvector, query tsquery [, normalization integer ]) returns float4`: Esta função calcula o ranking de *densidade de cobertura* para o vetor de documento e a consulta dados, conforme descrito em "Ranking de relevância para consultas de um a três termos" de Clarke, Cormack e Tudhope na revista "Information Processing and Management", 1999. A densidade de cobertura é semelhante ao ranking `ts_rank`, exceto que a proximidade dos lexemas que correspondem entre si é considerada.

Essa função requer informações posicionais do léxico para realizar seu cálculo. Portanto, ela ignora quaisquer léxicos "descascados" no `tsvector`. Se não houver léxicos não descascados na entrada, o resultado será zero. (Consulte [Seção 12.4.1] [(textsearch-features.md#TEXTSEARCH-MANIPULATE-TSVECTOR "12.4.1. Manipulating Documents")] para mais informações sobre a função `strip` e informações posicionais nos `tsvector`s.)

Para ambas essas funções, o argumento opcional *`weights`* oferece a capacidade de pesar as instâncias das palavras de forma mais ou menos pesada, dependendo de como elas são rotuladas. Os arrays de peso especificam a importância de cada categoria de palavra, na ordem:

```
{D-weight, C-weight, B-weight, A-weight}
```

Se não forem fornecidos *`weights`*, então esses valores padrão serão utilizados:

```
{0.1, 0.2, 0.4, 1.0}
```

Normalmente, os pesos são usados para marcar palavras de áreas especiais do documento, como o título ou um resumo inicial, para que possam ser tratadas com mais ou menos importância do que as palavras no corpo do documento.

Como um documento mais longo tem maior chance de conter um termo de consulta, é razoável levar em conta o tamanho do documento, por exemplo, um documento de cem palavras com cinco instâncias de uma palavra de busca provavelmente é mais relevante do que um documento de mil palavras com cinco instâncias. Ambas as funções de classificação levam uma opção de número inteiro *`normalization`* que especifica se e como o comprimento do documento deve impactar sua classificação. A opção de número inteiro controla vários comportamentos, então é um pouco de máscara: você pode especificar um ou mais comportamentos usando `|` (por exemplo, `2|4`).

* 0 (o padrão) ignora o comprimento do documento
* 1 divide o rank pelo 1 + o logaritmo do comprimento do documento
* 2 divide o rank pelo comprimento do documento
* 4 divide o rank pela distância harmônica média entre extensões (isso é implementado apenas por `ts_rank_cd`)
* 8 divide o rank pelo número de palavras únicas no documento
* 16 divide o rank pelo 1 + o logaritmo do número de palavras únicas no documento
* 32 divide o rank por si mesmo + 1

Se mais de um bit de bandeira for especificado, as transformações são aplicadas na ordem listada.

É importante notar que as funções de classificação não utilizam nenhuma informação global, portanto, é impossível produzir uma normalização justa para 1% ou 100%, como às vezes desejado. A opção de normalização 32 (`rank/(rank+1)`) pode ser aplicada para escalar todos os rankings na faixa de zero a um, mas, claro, isso é apenas uma mudança cosmética; isso não afetará a ordem dos resultados da pesquisa.

Aqui está um exemplo que seleciona apenas os dez jogos com o maior ranking:

```
SELECT title, ts_rank_cd(textsearch, query) AS rank
FROM apod, to_tsquery('neutrino|(dark & matter)') query
WHERE query @@ textsearch
ORDER BY rank DESC
LIMIT 10;
                     title                     |   rank
-----------------------------------------------+----------
 Neutrinos in the Sun                          |      3.1
 The Sudbury Neutrino Detector                 |      2.4
 A MACHO View of Galactic Dark Matter          |  2.01317
 Hot Gas and Dark Matter                       |  1.91171
 The Virgo Cluster: Hot Plasma and Dark Matter |  1.90953
 Rafting for Solar Neutrinos                   |      1.9
 NGC 4650A: Strange Galaxy and Dark Matter     |  1.85774
 Hot Gas and Dark Matter                       |   1.6123
 Ice Fishing for Cosmic Neutrinos              |      1.6
 Weak Lensing Distorts the Universe            | 0.818218
```

Esse é o mesmo exemplo usando classificação normalizada:

```
SELECT title, ts_rank_cd(textsearch, query, 32 /* rank/(rank+1) */ ) AS rank
FROM apod, to_tsquery('neutrino|(dark & matter)') query
WHERE  query @@ textsearch
ORDER BY rank DESC
LIMIT 10;
                     title                     |        rank
-----------------------------------------------+-------------------
 Neutrinos in the Sun                          | 0.756097569485493
 The Sudbury Neutrino Detector                 | 0.705882361190954
 A MACHO View of Galactic Dark Matter          | 0.668123210574724
 Hot Gas and Dark Matter                       |  0.65655958650282
 The Virgo Cluster: Hot Plasma and Dark Matter | 0.656301290640973
 Rafting for Solar Neutrinos                   | 0.655172410958162
 NGC 4650A: Strange Galaxy and Dark Matter     | 0.650072921219637
 Hot Gas and Dark Matter                       | 0.617195790024749
 Ice Fishing for Cosmic Neutrinos              | 0.615384618911517
 Weak Lensing Distorts the Universe            | 0.450010798361481
```

O ranking pode ser caro, pois exige a consulta ao `tsvector` de cada documento correspondente, que pode ser limitado por I/O e, portanto, lento. Infelizmente, é quase impossível evitar isso, pois as consultas práticas geralmente resultam em um grande número de correspondências.

### 12.3.4. Destaque dos resultados [#](#TEXTSEARCH-HEADLINE)

Para apresentar os resultados da pesquisa, é ideal mostrar uma parte de cada documento e como ele está relacionado à consulta. Geralmente, os motores de busca mostram fragmentos do documento com termos de pesquisa marcados. O PostgreSQL fornece uma função `ts_headline` que implementa essa funcionalidade.

```
ts_headline([ config regconfig, ] document text, query tsquery [, options text ]) returns text
```

`ts_headline` aceita um documento juntamente com uma consulta e retorna um trecho do documento em que os termos da consulta são destacados. Especificamente, a função usará a consulta para selecionar fragmentos de texto relevantes e, em seguida, destacará todas as palavras que aparecem na consulta, mesmo que essas posições das palavras não correspondam às restrições da consulta. A configuração a ser usada para analisar o documento pode ser especificada por *`config`*; se *`config`* é omitido, a configuração `default_text_search_config` é usada.

Se uma string *`options`* for especificada, ela deve consistir em uma lista de separação por vírgula de um ou mais pares *`option`*`=`*`value`*. As opções disponíveis são:

* `MaxWords`, `MinWords` (números inteiros): esses números determinam os cabeçalhos mais longos e mais curtos a serem exibidos. Os valores padrão são 35 e 15.
* `ShortWord` (número inteiro): palavras desse comprimento ou menos serão descartadas no início e no fim de um cabeçalho, a menos que sejam termos de consulta. O valor padrão de três elimina artigos comuns em inglês.
* `HighlightAll` (booleano): se `true` o documento inteiro será usado como cabeçalho, ignorando os três parâmetros anteriores. O valor padrão é `false`.
* `MaxFragments` (número inteiro): número máximo de fragmentos de texto a serem exibidos. O valor padrão de zero seleciona um método de geração de cabeçalho não baseado em fragmentos. Um valor maior que zero seleciona a geração de cabeçalho com base em fragmentos (veja abaixo).
* `StartSel`, `StopSel` (strings): as strings com as quais serão delimitadas as palavras de consulta que aparecem no documento, para as distinguir de outras palavras extraídas. Os valores padrão são “`<b>`” e “`</b>`”, que podem ser adequados para saída HTML (mas veja o aviso abaixo).
* `FragmentDelimiter` (string): quando mais de um fragmento é exibido, os fragmentos serão separados por esta string. O valor padrão é “ `...` ”.

### Aviso: Segurança contra Scripting em Sites Múltiplos (XSS)

A saída de `ts_headline` não é garantida para inclusão direta em páginas da web. Quando `HighlightAll` é `false` (o padrão), algumas tags XML simples são removidas do documento, mas isso não garante a remoção de toda a marcação HTML. Portanto, isso não oferece uma defesa eficaz contra ataques como ataques de script em sites diferentes (XSS), ao trabalhar com entrada não confiável. Para se proteger contra tais ataques, toda a marcação HTML deve ser removida do documento de entrada, ou um purificador de HTML deve ser usado na saída.

Esses nomes de opção são reconhecidos de forma sensível ao caso. Você deve colocar aspas duplas nos valores de cadeia se eles contiverem espaços ou vírgulas.

Na geração de manchetes não baseada em fragmentos, `ts_headline` localiza correspondências para o *`query`* dado e escolhe uma única para exibir, preferindo correspondências que têm mais palavras de consulta dentro do comprimento permitido da manchete. Na geração de manchetes baseada em fragmentos, `ts_headline` localiza as correspondências de consulta e divide cada correspondência em “fragmentos” de não mais de `MaxWords` palavras cada, preferindo fragmentos com mais palavras de consulta, e, quando possível, “esticando” os fragmentos para incluir palavras circundantes. O modo baseado em fragmentos é, portanto, mais útil quando as correspondências de consulta abrangem grandes seções do documento, ou quando é desejável exibir múltiplas correspondências. Em qualquer um dos modos, se não puderem ser identificadas correspondências de consulta, então um único fragmento das primeiras `MinWords` palavras do documento será exibido.

Por exemplo:

```
SELECT ts_headline('english',
  'The most common type of search
is to find all documents containing given query terms
and return them in order of their similarity to the
query.',
  to_tsquery('english', 'query & similarity'));
                        ts_headline
------------------------------------------------------------
 containing given <b>query</b> terms                       +
 and return them in order of their <b>similarity</b> to the+
 <b>query</b>.

SELECT ts_headline('english',
  'Search terms may occur
many times in a document,
requiring ranking of the search matches to decide which
occurrences to display in the result.',
  to_tsquery('english', 'search & term'),
  'MaxFragments=10, MaxWords=7, MinWords=3, StartSel=<<, StopSel=>>');
                        ts_headline
------------------------------------------------------------
 <<Search>> <<terms>> may occur                            +
 many times ... ranking of the <<search>> matches to decide
```

`ts_headline` utiliza o documento original, não um resumo de `tsvector`, portanto, pode ser lento e deve ser usado com cuidado.