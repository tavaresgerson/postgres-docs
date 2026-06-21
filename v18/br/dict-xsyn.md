## F.13. dict_xsyn — dicionário de busca de sinônimos de texto completo [#](#DICT-XSYN)

* [F.13.1. Configuração](dict-xsyn.md#DICT-XSYN-CONFIG)
* [F.13.2. Uso](dict-xsyn.md#DICT-XSYN-USAGE)

`dict_xsyn` (Dicionário de sinônimos estendido) é um exemplo de um modelo de dicionário de extensão para pesquisa de texto completo. Esse tipo de dicionário substitui as palavras por grupos de seus sinônimos, e, assim, torna possível pesquisar uma palavra usando qualquer um de seus sinônimos.

### F.13.1. Configuração [#](#DICT-XSYN-CONFIG)

Um dicionário `dict_xsyn` aceita as seguintes opções:

* `matchorig` controla se a palavra original é aceita pelo dicionário. O padrão é `true`.
* `matchsynonyms` controla se os sinônimos são aceitos pelo dicionário. O padrão é `false`.
* `keeporig` controla se a palavra original está incluída na saída do dicionário. O padrão é `true`.
* `keepsynonyms` controla se os sinônimos estão incluídos na saída do dicionário. O padrão é `true`.
* `rules` é o nome base do arquivo que contém a lista de sinônimos. Este arquivo deve ser armazenado em `$SHAREDIR/tsearch_data/` (onde `$SHAREDIR` significa o diretório de dados compartilhados da instalação do PostgreSQL). Seu nome deve terminar em `.rules` (que não deve ser incluído no parâmetro `rules`).

O arquivo de regras tem o seguinte formato:

* Cada linha representa um grupo de sinônimos para uma única palavra, que é dada primeiro na linha. Os sinônimos são separados por espaço em branco, assim:

* O sinal de ponto (`#`) é um delimitador de comentário. Ele pode aparecer em qualquer posição em uma linha. O resto da linha será ignorado.

Veja `xsyn_sample.rules`, que está instalado em `$SHAREDIR/tsearch_data/`, como exemplo.

### F.13.2. Uso [#](#DICT-XSYN-USAGE)

A instalação da extensão `dict_xsyn` cria um modelo de busca de texto `xsyn_template` e um dicionário `xsyn` com base nele, com parâmetros padrão. Você pode alterar os parâmetros, por exemplo

```
mydb# ALTER TEXT SEARCH DICTIONARY xsyn (RULES='my_rules', KEEPORIG=false);
ALTER TEXT SEARCH DICTIONARY
```

ou crie novos dicionários com base no modelo.

Para testar o dicionário, você pode tentar

```
mydb=# SELECT ts_lexize('xsyn', 'word');
      ts_lexize
-----------------------
 {syn1,syn2,syn3}

mydb# ALTER TEXT SEARCH DICTIONARY xsyn (RULES='my_rules', KEEPORIG=true);
ALTER TEXT SEARCH DICTIONARY

mydb=# SELECT ts_lexize('xsyn', 'word');
      ts_lexize
-----------------------
 {word,syn1,syn2,syn3}

mydb# ALTER TEXT SEARCH DICTIONARY xsyn (RULES='my_rules', KEEPORIG=false, MATCHSYNONYMS=true);
ALTER TEXT SEARCH DICTIONARY

mydb=# SELECT ts_lexize('xsyn', 'syn1');
      ts_lexize
-----------------------
 {syn1,syn2,syn3}

mydb# ALTER TEXT SEARCH DICTIONARY xsyn (RULES='my_rules', KEEPORIG=true, MATCHORIG=false, KEEPSYNONYMS=false);
ALTER TEXT SEARCH DICTIONARY

mydb=# SELECT ts_lexize('xsyn', 'syn1');
      ts_lexize
-----------------------
 {word}
```

O uso no mundo real envolverá incluí-lo em uma configuração de pesquisa de texto, conforme descrito em [Capítulo 12][(textsearch.md "Chapter 12. Full Text Search")]. Isso pode parecer assim:

```
ALTER TEXT SEARCH CONFIGURATION english
    ALTER MAPPING FOR word, asciiword WITH xsyn, english_stem;
```
