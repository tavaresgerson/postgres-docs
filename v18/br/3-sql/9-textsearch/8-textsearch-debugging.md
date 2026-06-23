## 12.8. Testar e depurar a pesquisa de texto [#](#TEXTSEARCH-DEBUGGING)

* [12.8.1. Testes de Configuração](textsearch-debugging.md#TEXTSEARCH-CONFIGURATION-TESTING)
* [12.8.2. Testes de Parser](textsearch-debugging.md#TEXTSEARCH-PARSER-TESTING)
* [12.8.3. Testes de Dicionário](textsearch-debugging.md#TEXTSEARCH-DICTIONARY-TESTING)

O comportamento de uma configuração de busca de texto personalizada pode facilmente se tornar confuso. As funções descritas nesta seção são úteis para testar objetos de busca de texto. Você pode testar uma configuração completa ou testar os analisadores e dicionários separadamente.

### 12.8.1. Testes de Configuração [#](#TEXTSEARCH-CONFIGURATION-TESTING)

A função `ts_debug` permite testar facilmente uma configuração de busca de texto.

```
ts_debug([ config regconfig, ] document text,
         OUT alias text,
         OUT description text,
         OUT token text,
         OUT dictionaries regdictionary[],
         OUT dictionary regdictionary,
         OUT lexemes text[])
         returns setof record
```

`ts_debug` exibe informações sobre cada token de *`document`* produzido pelo analisador e processado pelos dicionários configurados. Ele utiliza a configuração especificada por *`config`*, ou `default_text_search_config` se esse argumento for omitido.

`ts_debug` retorna uma linha para cada token identificado no texto pelo analisador. As colunas devolvidas são

* *`alias`* `text` — nome curto do tipo de token
* *`description`* `text` — descrição do tipo de token
* *`token`* `text` — texto do token
* *`dictionaries`* `regdictionary[]` — os dicionários selecionados pela configuração para este tipo de token
* *`dictionary`* `regdictionary` — o dicionário que reconheceu o token, ou `NULL` se nenhum reconheceu
* *`lexemes`* `text[]` — o léxico(s) produzido(s) pelo dicionário que reconheceu o token, ou `NULL` se nenhum reconheceu; um array vazio (`{}`) significa que foi reconhecido como uma palavra parada

Aqui está um exemplo simples:

```
SELECT * FROM ts_debug('english', 'a fat  cat sat on a mat - it ate a fat rats');
   alias   |   description   | token |  dictionaries  |  dictionary  | lexemes
-----------+-----------------+-------+----------------+--------------+---------
 asciiword | Word, all ASCII | a     | {english_stem} | english_stem | {}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | fat   | {english_stem} | english_stem | {fat}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | cat   | {english_stem} | english_stem | {cat}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | sat   | {english_stem} | english_stem | {sat}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | on    | {english_stem} | english_stem | {}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | a     | {english_stem} | english_stem | {}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | mat   | {english_stem} | english_stem | {mat}
 blank     | Space symbols   |       | {}             |              |
 blank     | Space symbols   | -     | {}             |              |
 asciiword | Word, all ASCII | it    | {english_stem} | english_stem | {}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | ate   | {english_stem} | english_stem | {ate}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | a     | {english_stem} | english_stem | {}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | fat   | {english_stem} | english_stem | {fat}
 blank     | Space symbols   |       | {}             |              |
 asciiword | Word, all ASCII | rats  | {english_stem} | english_stem | {rat}
```

Para uma demonstração mais extensa, primeiro criamos uma configuração `public.english` e um dicionário Ispell para o idioma inglês:

```
CREATE TEXT SEARCH CONFIGURATION public.english ( COPY = pg_catalog.english );

CREATE TEXT SEARCH DICTIONARY english_ispell (
    TEMPLATE = ispell,
    DictFile = english,
    AffFile = english,
    StopWords = english
);

ALTER TEXT SEARCH CONFIGURATION public.english
   ALTER MAPPING FOR asciiword WITH english_ispell, english_stem;
```

```
SELECT * FROM ts_debug('public.english', 'The Brightest supernovaes');
   alias   |   description   |    token    |         dictionaries          |   dictionary   |   lexemes
-----------+-----------------+-------------+-------------------------------+----------------+-------------
 asciiword | Word, all ASCII | The         | {english_ispell,english_stem} | english_ispell | {}
 blank     | Space symbols   |             | {}                            |                |
 asciiword | Word, all ASCII | Brightest   | {english_ispell,english_stem} | english_ispell | {bright}
 blank     | Space symbols   |             | {}                            |                |
 asciiword | Word, all ASCII | supernovaes | {english_ispell,english_stem} | english_stem   | {supernova}
```

Neste exemplo, a palavra `Brightest` foi reconhecida pelo analisador como uma `ASCII word` (alias `asciiword`). Para este tipo de token, a lista do dicionário é `english_ispell` e `english_stem`. A palavra foi reconhecida pelo `english_ispell`, que a reduziu ao substantivo `bright`. A palavra `supernovaes` é desconhecida pelo dicionário `english_ispell`, então foi passada para o próximo dicionário, e, felizmente, foi reconhecida (de fato, `english_stem` é um dicionário Snowball que reconhece tudo; é por isso que foi colocada no final da lista do dicionário).

A palavra `The` foi reconhecida pelo dicionário `english_ispell` como uma palavra parada ([Seção 12.6.1](textsearch-dictionaries.md#TEXTSEARCH-STOPWORDS)) e não será indexada. Os espaços também são descartados, uma vez que a configuração não fornece dicionários para eles.

Você pode reduzir a largura da saída, especificando explicitamente quais colunas você deseja ver:

```
SELECT alias, token, dictionary, lexemes
FROM ts_debug('public.english', 'The Brightest supernovaes');
   alias   |    token    |   dictionary   |   lexemes
-----------+-------------+----------------+-------------
 asciiword | The         | english_ispell | {}
 blank     |             |                |
 asciiword | Brightest   | english_ispell | {bright}
 blank     |             |                |
 asciiword | supernovaes | english_stem   | {supernova}
```

### 12.8.2. Testes de Parser [#](#TEXTSEARCH-PARSER-TESTING)

As funções a seguir permitem testar diretamente um analisador de pesquisa de texto.

```
ts_parse(parser_name text, document text,
         OUT tokid integer, OUT token text) returns setof record
ts_parse(parser_oid oid, document text,
         OUT tokid integer, OUT token text) returns setof record
```

`ts_parse` analisa o dado *`document`* e retorna uma série de registros, um para cada token produzido pela análise. Cada registro inclui um `tokid` que mostra o tipo de token atribuído e um `token` que é o texto do token. Por exemplo:

```
SELECT * FROM ts_parse('default', '123 - a number');
 tokid | token
-------+--------
    22 | 123
    12 |
    12 | -
     1 | a
    12 |
     1 | number
```

```
ts_token_type(parser_name text, OUT tokid integer,
              OUT alias text, OUT description text) returns setof record
ts_token_type(parser_oid oid, OUT tokid integer,
              OUT alias text, OUT description text) returns setof record
```

`ts_token_type` retorna uma tabela que descreve cada tipo de token que o analisador especificado pode reconhecer. Para cada tipo de token, a tabela fornece o número inteiro `tokid` que o analisador usa para rotular um token desse tipo, o `alias` que nomeia o tipo de token em comandos de configuração e um breve `description`. Por exemplo:

```
SELECT * FROM ts_token_type('default');
 tokid |      alias      |               description
-------+-----------------+------------------------------------------
     1 | asciiword       | Word, all ASCII
     2 | word            | Word, all letters
     3 | numword         | Word, letters and digits
     4 | email           | Email address
     5 | url             | URL
     6 | host            | Host
     7 | sfloat          | Scientific notation
     8 | version         | Version number
     9 | hword_numpart   | Hyphenated word part, letters and digits
    10 | hword_part      | Hyphenated word part, all letters
    11 | hword_asciipart | Hyphenated word part, all ASCII
    12 | blank           | Space symbols
    13 | tag             | XML tag
    14 | protocol        | Protocol head
    15 | numhword        | Hyphenated word, letters and digits
    16 | asciihword      | Hyphenated word, all ASCII
    17 | hword           | Hyphenated word, all letters
    18 | url_path        | URL path
    19 | file            | File or path name
    20 | float           | Decimal notation
    21 | int             | Signed integer
    22 | uint            | Unsigned integer
    23 | entity          | XML entity
```

### 12.8.3. Testes de dicionário [#](#TEXTSEARCH-DICTIONARY-TESTING)

A função `ts_lexize` facilita o teste do dicionário.

```
ts_lexize(dict regdictionary, token text) returns text[]
```

`ts_lexize` retorna um array de lexemas se o input *`token`* estiver conhecido pelo dicionário, ou um array vazio se o token estiver conhecido pelo dicionário, mas for uma palavra parada, ou `NULL` se for uma palavra desconhecida.

Exemplos:

```
SELECT ts_lexize('english_stem', 'stars');
 ts_lexize
-----------
 {star}

SELECT ts_lexize('english_stem', 'a');
 ts_lexize
-----------
 {}
```

### Nota

A função `ts_lexize` espera um único *token*, não texto. Aqui está um caso em que isso pode ser confuso:

```
SELECT ts_lexize('thesaurus_astro', 'supernovae stars') is null;
 ?column?
----------
 t
```

O dicionário de sinônimos `thesaurus_astro` não conhece a frase `supernovae stars`, mas `ts_lexize` falha, pois não analisa o texto de entrada, mas o trata como um único token. Use `plainto_tsquery` ou `to_tsvector` para testar dicionários de sinônimos, por exemplo:

```
SELECT plainto_tsquery('supernovae stars');
 plainto_tsquery
-----------------
 'sn'
```
