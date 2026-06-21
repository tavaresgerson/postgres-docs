## F.48. unaccent — um dicionário de busca de texto que remove diacríticos [#](#UNACCENT)

* [F.48.1. Configuração](unaccent.md#UNACCENT-CONFIGURATION)
* [F.48.2. Uso](unaccent.md#UNACCENT-USAGE)
* [F.48.3. Funções](unaccent.md#UNACCENT-FUNCTIONS)

`unaccent` é um dicionário de busca de texto que remove acentos (sinais diacríticos) dos lexemas. É um dicionário de filtragem, o que significa que sua saída é sempre passada para o próximo dicionário (se houver), ao contrário do comportamento normal dos dicionários. Isso permite o processamento insensível ao acento para busca de texto completo.

A implementação atual do `unaccent` não pode ser usada como um dicionário normalizador para o dicionário `thesaurus`.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.48.1. Configuração [#](#UNACCENT-CONFIGURATION)

Um dicionário `unaccent` aceita as seguintes opções:

* `RULES` é o nome base do arquivo que contém a lista das regras de tradução. Esse arquivo deve ser armazenado em `$SHAREDIR/tsearch_data/` (onde `$SHAREDIR` significa o diretório de dados compartilhados da instalação do PostgreSQL). Seu nome deve terminar em `.rules` (que não deve ser incluído no parâmetro `RULES`).

O arquivo de regras tem o seguinte formato:

* Cada linha representa uma regra de tradução, consistindo em um caractere com acento seguido de um caractere sem acento. A primeira é traduzida para a segunda. Por exemplo,

  ```
  À        A
  Á        A
  Â        A
  Ã        A
  Ä        A
  Å        A
  Æ        AE
  ```

Os dois caracteres devem ser separados por espaço em branco, e qualquer espaço em branco inicial ou final em uma linha é ignorado.
* Alternativamente, se apenas um caractere for dado em uma linha, as instâncias desse caractere são excluídas; isso é útil em linguagens onde acentos são representados por caracteres separados.
* Na verdade, cada "caractere" pode ser qualquer string que não contenha espaço em branco, então os dicionários `unaccent` poderiam ser usados para outras substituições de subcadeia além da remoção de diacríticos.
* Alguns caracteres, como símbolos numéricos, podem exigir espaços em branco em sua regra de tradução. É possível usar aspas duplas ao redor dos caracteres traduzidos neste caso. Uma aspa dupla precisa ser escapada com uma segunda aspa dupla quando incluída no caractere traduzido. Por exemplo:

* Assim como outros arquivos de configuração de busca de texto do PostgreSQL, o arquivo de regras deve ser armazenado com codificação UTF-8. Os dados são automaticamente traduzidos para a codificação do banco de dados atual quando carregados. Quaisquer linhas que contenham caracteres não traduzíveis são ignorados silenciosamente, para que os arquivos de regras possam conter regras que não sejam aplicáveis na codificação atual.

Um exemplo mais completo, que é diretamente útil para a maioria das línguas europeias, pode ser encontrado em `unaccent.rules`, que é instalado em `$SHAREDIR/tsearch_data/` quando o módulo `unaccent` é instalado. Este arquivo de regras traduz caracteres com acentos para os mesmos caracteres sem acentos e também expande as ligaduras na série equivalente de caracteres simples (por exemplo, Æ para AE).

### F.48.2. Uso [#](#UNACCENT-USAGE)

A instalação da extensão `unaccent` cria um modelo de busca de texto `unaccent` e um dicionário `unaccent` com base nele. O dicionário `unaccent` tem o parâmetro de configuração padrão `RULES='unaccent'`, o que o torna imediatamente utilizável com o arquivo padrão `unaccent.rules`. Se desejar, pode alterar o parâmetro, por exemplo

```
mydb=# ALTER TEXT SEARCH DICTIONARY unaccent (RULES='my_rules');
```

ou crie novos dicionários com base no modelo.

Para testar o dicionário, você pode tentar:

```
mydb=# select ts_lexize('unaccent','Hôtel');
 ts_lexize
-----------
 {Hotel}
(1 row)
```

Aqui está um exemplo que mostra como inserir o dicionário `unaccent` em uma configuração de pesquisa de texto:

```
mydb=# CREATE TEXT SEARCH CONFIGURATION fr ( COPY = french );
mydb=# ALTER TEXT SEARCH CONFIGURATION fr
        ALTER MAPPING FOR hword, hword_part, word
        WITH unaccent, french_stem;
mydb=# select to_tsvector('fr','Hôtels de la Mer');
    to_tsvector
-------------------
 'hotel':1 'mer':4
(1 row)

mydb=# select to_tsvector('fr','Hôtel de la Mer') @@ to_tsquery('fr','Hotels');
 ?column?
----------
 t
(1 row)

mydb=# select ts_headline('fr','Hôtel de la Mer',to_tsquery('fr','Hotels'));
      ts_headline
------------------------
 <b>Hôtel</b> de la Mer
(1 row)
```

### F.48.3. Funções [#](#UNACCENT-FUNCTIONS)

A função `unaccent()` remove acentos (sinais diacríticos) de uma cadeia de caracteres dada. Basicamente, é um wrapper em torno de dicionários do tipo `unaccent`, mas pode ser usado fora dos contextos normais de busca de texto.

```
unaccent([dictionary regdictionary, ] string text) returns text
```

Se o argumento *`dictionary`* for omitido, o dicionário de busca de texto denominado `unaccent` e que aparece no mesmo esquema que a própria função `unaccent()` é usado.

Por exemplo:

```
SELECT unaccent('unaccent', 'Hôtel');
SELECT unaccent('Hôtel');
```
