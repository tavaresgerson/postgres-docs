## 12.6. Dicionários [#](#TEXTSEARCH-DICTIONARIES)

* [12.6.1. Palavras Particulares](textsearch-dictionaries.md#TEXTSEARCH-STOPWORDS)
* [12.6.2. Dicionário Simples](textsearch-dictionaries.md#TEXTSEARCH-SIMPLE-DICTIONARY)
* [12.6.3. Dicionário de Sinônimos](textsearch-dictionaries.md#TEXTSEARCH-SYNONYM-DICTIONARY)
* [12.6.4. Dicionário de Tesauro](textsearch-dictionaries.md#TEXTSEARCH-THESAURUS)
* [12.6.5. Dicionário Ispell](textsearch-dictionaries.md#TEXTSEARCH-ISPELL-DICTIONARY)
* [12.6.6. Dicionário Snowball](textsearch-dictionaries.md#TEXTSEARCH-SNOWBALL-DICTIONARY)

As dicionários são usados para eliminar palavras que não devem ser consideradas em uma pesquisa (*palavras paradas*), e para *normalizar* as palavras de modo que diferentes formas derivadas da mesma palavra se correspondam. Uma palavra normalizada com sucesso é chamada de *lexema*. Além de melhorar a qualidade da pesquisa, a normalização e a remoção de palavras paradas reduzem o tamanho da representação do `tsvector` de um documento, melhorando, assim, o desempenho. A normalização não tem sempre um significado linguístico e geralmente depende da semântica da aplicação.

Alguns exemplos de normalização:

* Linguística — os dicionários Ispell tentam reduzir as palavras de entrada a uma forma normalizada; os dicionários de stemmer removem as extremidades das palavras
* As localizações de URL podem ser canonicizadas para fazer com que URLs equivalentes correspondam:

+ http://www.pgsql.ru/db/mw/index.html
+ http://www.pgsql.ru/db/mw/
+ http://www.pgsql.ru/db/../db/mw/index.html
* Os nomes de cores podem ser substituídos por seus valores hexadecimais, por exemplo, `red, green, blue, magenta -> FF0000, 00FF00, 0000FF, FF00FF`
* Se forem números de indexação, podemos remover alguns dígitos fracionários para reduzir o intervalo de números possíveis, então, por exemplo, *3.14*159265359, *3.14*15926, *3.14* serão os mesmos após a normalização se apenas dois dígitos forem mantidos após o ponto decimal.

Um dicionário é um programa que aceita um token como entrada e retorna:

* uma matriz de lexemas se o token de entrada é conhecido pelo dicionário (observe que um token pode produzir mais de um lexema)
* um único lexema com a bandeira `TSL_FILTER` definida, para substituir o token original por um novo token a ser passado para dicionários subsequentes (um dicionário que faz isso é chamado de *dicionário de filtragem*)
* uma matriz vazia se o dicionário conhece o token, mas é uma palavra parada
* `NULL` se o dicionário não reconhece o token de entrada

O PostgreSQL oferece dicionários predefinidos para muitas línguas. Também existem vários modelos predefinidos que podem ser usados para criar novos dicionários com parâmetros personalizados. Cada modelo de dicionário predefinido é descrito abaixo. Se nenhum modelo existente for adequado, é possível criar novos; veja a área `contrib/` da distribuição do PostgreSQL para exemplos.

Uma configuração de pesquisa de texto vincula um analisador a um conjunto de dicionários para processar os tokens de saída do analisador. Para cada tipo de token que o analisador pode retornar, uma lista separada de dicionários é especificada pela configuração. Quando um token desse tipo é encontrado pelo analisador, cada dicionário na lista é consultado em ordem, até que algum dicionário o reconheça como uma palavra conhecida. Se for identificado como uma palavra parada, ou se nenhum dicionário reconhece o token, ele será descartado e não será indexado ou pesquisado. Normalmente, o primeiro dicionário que retorna uma saída que não é um `NULL` determina o resultado, e quaisquer dicionários restantes não são consultados; mas um dicionário de filtragem pode substituir a palavra dada por uma palavra modificada, que é então passada para os dicionários subsequentes.

A regra geral para configurar uma lista de dicionários é colocar primeiro o dicionário mais estreito e específico, depois os dicionários mais gerais, terminando com um dicionário muito geral, como um stemmer Snowball ou `simple`, que reconhece tudo. Por exemplo, para uma busca específica de astronomia (configuração `astro_en`), pode-se vincular o tipo de token `asciiword` (palavra ASCII) a um dicionário de sinônimos de termos astronômicos, um dicionário geral de inglês e um stemmer Snowball de inglês:

```
ALTER TEXT SEARCH CONFIGURATION astro_en
    ADD MAPPING FOR asciiword WITH astrosyn, english_ispell, english_stem;
```

Um dicionário de filtragem pode ser colocado em qualquer lugar na lista, exceto no final, onde seria inútil. Dicionários de filtragem são úteis para normalizar parcialmente as palavras para simplificar a tarefa dos dicionários posteriores. Por exemplo, um dicionário de filtragem pode ser usado para remover acentos das letras acentuadas, como feito pelo módulo [unaccent](unaccent.md).

### 12.6.1. Palavras Particulares [#](#TEXTSEARCH-STOPWORDS)

As palavras paradas são palavras que são muito comuns, aparecem em quase todos os documentos e não têm valor de discriminação. Portanto, elas podem ser ignoradas no contexto da pesquisa de texto completo. Por exemplo, todo texto em inglês contém palavras como `a` e `the`, então é inútil armazená-las em um índice. No entanto, as palavras paradas afetam as posições em `tsvector`, que por sua vez afetam o ranking:

```
SELECT to_tsvector('english', 'in the list of stop words');
        to_tsvector
----------------------------
 'list':3 'stop':5 'word':6
```

As posições faltantes 1, 2 e 4 são devido a palavras de parada. As classificações calculadas para documentos com e sem palavras de parada são bastante diferentes:

```
SELECT ts_rank_cd (to_tsvector('english', 'in the list of stop words'), to_tsquery('list & stop'));
 ts_rank_cd
------------
       0.05

SELECT ts_rank_cd (to_tsvector('english', 'list stop words'), to_tsquery('list & stop'));
 ts_rank_cd
------------
        0.1
```

Depende do dicionário específico como ele trata as palavras paradas. Por exemplo, os dicionários `ispell` normalizam as palavras primeiro e depois examinam a lista de palavras paradas, enquanto os `Snowball` stemmers verificam primeiro a lista de palavras paradas. A razão para o comportamento diferente é uma tentativa de diminuir o ruído.

### 12.6.2. Dicionário Simples [#](#TEXTSEARCH-SIMPLE-DICTIONARY)

O modelo de dicionário `simple` opera convertendo o token de entrada para minúsculas e verificando-o contra um arquivo de palavras paradas. Se for encontrado no arquivo, um array vazio é retornado, fazendo com que o token seja descartado. Se não for, a forma minúscula da palavra é retornada como o léxico normalizado. Alternativamente, o dicionário pode ser configurado para relatar palavras não paradas como não reconhecidas, permitindo que elas sejam passadas para o próximo dicionário na lista.

Aqui está um exemplo de definição de dicionário usando o modelo `simple`:

```
CREATE TEXT SEARCH DICTIONARY public.simple_dict (
    TEMPLATE = pg_catalog.simple,
    STOPWORDS = english
);
```

Aqui, `english` é o nome base de um arquivo de palavras paradas. O nome completo do arquivo será `$SHAREDIR/tsearch_data/english.stop`, onde `$SHAREDIR` significa o diretório de dados compartilhados da instalação do PostgreSQL, muitas vezes `/usr/local/share/postgresql` (use `pg_config --sharedir` para determiná-lo se você não está seguro). O formato do arquivo é simplesmente uma lista de palavras, uma por linha. Linhas em branco e espaços finais são ignorados, e as maiúsculas são convertidas para minúsculas, mas nenhum outro processamento é feito nos conteúdos do arquivo.

Agora podemos testar nosso dicionário:

```
SELECT ts_lexize('public.simple_dict', 'YeS');
 ts_lexize
-----------
 {yes}

SELECT ts_lexize('public.simple_dict', 'The');
 ts_lexize
-----------
 {}
```

Também podemos optar por retornar `NULL`, em vez da palavra minúscula, se ela não for encontrada no arquivo de palavras paradas. Esse comportamento é selecionado definindo o parâmetro `Accept` do dicionário como `false`. Continuando o exemplo:

```
ALTER TEXT SEARCH DICTIONARY public.simple_dict ( Accept = false );

SELECT ts_lexize('public.simple_dict', 'YeS');
 ts_lexize
-----------


SELECT ts_lexize('public.simple_dict', 'The');
 ts_lexize
-----------
 {}
```

Com a configuração padrão de `Accept` = `true`, é útil apenas colocar um dicionário `simple` no final de uma lista de dicionários, pois ele nunca passará nenhum token para um dicionário subsequente. Por outro lado, `Accept` = `false` é útil apenas quando há pelo menos um dicionário subsequente.

### Atenção

A maioria dos tipos de dicionários depende de arquivos de configuração, como arquivos de palavras irrelevantes. Esses arquivos *devem* ser armazenados com codificação UTF-8. Eles serão traduzidos para a codificação real do banco de dados, se for diferente, quando forem lidos no servidor.

### Atenção

Normalmente, uma sessão do banco de dados irá ler um arquivo de configuração do dicionário apenas uma vez, quando ele é usado pela primeira vez dentro da sessão. Se você modificar um arquivo de configuração e quiser forçar as sessões existentes a pegar os novos conteúdos, emita um comando `ALTER TEXT SEARCH DICTIONARY` no dicionário. Isso pode ser uma atualização “falsa” que não altera realmente quaisquer valores de parâmetros.

### 12.6.3. Dicionário de sinônimos [#](#TEXTSEARCH-SYNONYM-DICTIONARY)

Este modelo de dicionário é usado para criar dicionários que substituem uma palavra por um sinônimo. As frases não são suportadas (use o modelo de sinônimos ([Seção 12.6.4](textsearch-dictionaries.md#TEXTSEARCH-THESAURUS "12.6.4. Thesaurus Dictionary")) para isso). Um dicionário de sinônimos pode ser usado para superar problemas linguísticos, por exemplo, para evitar que um dicionário de stemmer de inglês reduza a palavra “Paris” para “pari”. É suficiente ter uma linha `Paris paris` no dicionário de sinônimos e colocá-la antes do dicionário `english_stem`. Por exemplo:

```
SELECT * FROM ts_debug('english', 'Paris');
   alias   |   description   | token |  dictionaries  |  dictionary  | lexemes
-----------+-----------------+-------+----------------+--------------+---------
 asciiword | Word, all ASCII | Paris | {english_stem} | english_stem | {pari}

CREATE TEXT SEARCH DICTIONARY my_synonym (
    TEMPLATE = synonym,
    SYNONYMS = my_synonyms
);

ALTER TEXT SEARCH CONFIGURATION english
    ALTER MAPPING FOR asciiword
    WITH my_synonym, english_stem;

SELECT * FROM ts_debug('english', 'Paris');
   alias   |   description   | token |       dictionaries        | dictionary | lexemes
-----------+-----------------+-------+---------------------------+------------+---------
 asciiword | Word, all ASCII | Paris | {my_synonym,english_stem} | my_synonym | {paris}
```

O único parâmetro exigido pelo modelo `synonym` é `SYNONYMS`, que é o nome base do seu arquivo de configuração — `my_synonyms` no exemplo acima. O nome completo do arquivo será `$SHAREDIR/tsearch_data/my_synonyms.syn` (onde `$SHAREDIR` significa o diretório de dados compartilhados da instalação do PostgreSQL). O formato do arquivo é uma linha por palavra a ser substituída, com a palavra seguida de seu sinônimo, separados por espaço em branco. Linhas em branco e espaços finais são ignorados.

O modelo `synonym` também tem um parâmetro opcional `CaseSensitive`, que tem como padrão `false`. Quando `CaseSensitive` é `false`, as palavras no arquivo de sinônimos são dobradas para minúsculas, assim como os tokens de entrada. Quando é `true`, as palavras e tokens não são dobrados para minúsculas, mas são comparados como estão.

Um asterisco (`*`) pode ser colocado no final de um sinônimo no arquivo de configuração. Isso indica que o sinônimo é um prefixo. O asterisco é ignorado quando a entrada é usada em `to_tsvector()`, mas quando é usada em `to_tsquery()`, o resultado será um item de consulta com o marcador de correspondência de prefixo (veja [Seção 12.3.2](textsearch-controls.md#TEXTSEARCH-PARSING-QUERIES)). Por exemplo, suponha que tenhamos essas entradas em `$SHAREDIR/tsearch_data/synonym_sample.syn`:

```
postgres        pgsql
postgresql      pgsql
postgre pgsql
gogle   googl
indices index*
```

Então, teremos esses resultados:

```
mydb=# CREATE TEXT SEARCH DICTIONARY syn (template=synonym, synonyms='synonym_sample');
mydb=# SELECT ts_lexize('syn', 'indices');
 ts_lexize
-----------
 {index}
(1 row)

mydb=# CREATE TEXT SEARCH CONFIGURATION tst (copy=simple);
mydb=# ALTER TEXT SEARCH CONFIGURATION tst ALTER MAPPING FOR asciiword WITH syn;
mydb=# SELECT to_tsvector('tst', 'indices');
 to_tsvector
-------------
 'index':1
(1 row)

mydb=# SELECT to_tsquery('tst', 'indices');
 to_tsquery
------------
 'index':*
(1 row)

mydb=# SELECT 'indexes are very useful'::tsvector;
            tsvector
---------------------------------
 'are' 'indexes' 'useful' 'very'
(1 row)

mydb=# SELECT 'indexes are very useful'::tsvector @@ to_tsquery('tst', 'indices');
 ?column?
----------
 t
(1 row)
```

### 12.6.4. Dicionário Thesaurus [#](#TEXTSEARCH-THESAURUS)

Um dicionário de sinônimos (às vezes abreviado como TZ) é uma coleção de palavras que inclui informações sobre as relações entre palavras e frases, ou seja, termos mais amplos (TA), termos mais restritos (TR), termos preferidos, termos não preferidos, termos relacionados, etc.

Basicamente, um dicionário de sinônimos substitui todos os termos não preferidos por um termo preferido e, opcionalmente, preserva os termos originais para indexação também. A implementação atual do PostgreSQL do dicionário de sinônimos é uma extensão do dicionário de sinônimos com suporte adicional para *frase*. Um dicionário de sinônimos requer um arquivo de configuração do seguinte formato:

```
# this is a comment
sample word(s) : indexed word(s)
more sample word(s) : more indexed word(s)
...
```

onde o símbolo de colon (`:`) atua como delimitador entre uma frase e sua substituição.

Um dicionário de sinônimos usa um *subdicionário* (que é especificado na configuração do dicionário) para normalizar o texto de entrada antes de verificar as correspondências de frases. É possível selecionar apenas um subdicionário. Um erro é relatado se o subdicionário não reconhecer uma palavra. Nesse caso, você deve remover o uso da palavra ou ensinar o subdicionário sobre ela. Você pode colocar um asterisco (`*`) no início de uma palavra indexada para ignorar a aplicação do subdicionário nela, mas todas as palavras de amostra *devem* ser conhecidas pelo subdicionário.

O dicionário de sinônimos escolhe a correspondência mais longa se houver várias frases correspondendo à entrada, e as igualdades são quebradas usando a última definição.

Não é possível especificar palavras específicas de parada reconhecidas pelo subdicionário; em vez disso, use `?` para marcar a localização onde qualquer palavra de parada pode aparecer. Por exemplo, assumindo que `a` e `the` são palavras de parada de acordo com o subdicionário:

```
? one ? two : swsw
```

os códigos `a one the two` e `the one a two`; ambos seriam substituídos por `swsw`.

Como um dicionário de sinônimos tem a capacidade de reconhecer frases, ele deve lembrar seu estado e interagir com o analisador. Um dicionário de sinônimos usa essas atribuições para verificar se deve lidar com a próxima palavra ou parar a acumulação. O dicionário de sinônimos deve ser configurado com cuidado. Por exemplo, se o dicionário de sinônimos é atribuído para lidar apenas com o token `asciiword`, então uma definição de dicionário de sinônimos como `one 7` não funcionará, pois o tipo de token `uint` não é atribuído ao dicionário de sinônimos.

### Atenção

Os tesauros são usados durante a indexação, portanto, qualquer alteração nos parâmetros do dicionário de tesauros *requer* uma reindexação. Para a maioria dos outros tipos de dicionário, pequenas alterações, como adicionar ou remover palavras-chave, não forçam a reindexação.

#### 12.6.4.1. Configuração do Tesauro [#](#TEXTSEARCH-THESAURUS-CONFIG)

Para definir um novo dicionário de sinônimos, use o modelo `thesaurus`. Por exemplo:

```
CREATE TEXT SEARCH DICTIONARY thesaurus_simple (
    TEMPLATE = thesaurus,
    DictFile = mythesaurus,
    Dictionary = pg_catalog.english_stem
);
```

Aqui:

* `thesaurus_simple` é o nome do novo dicionário
* `mythesaurus` é o nome da base do arquivo de configuração do sintagma. (Seu nome completo será `$SHAREDIR/tsearch_data/mythesaurus.ths`, onde `$SHAREDIR` significa o diretório de dados compartilhados da instalação.)
* `pg_catalog.english_stem` é o subdicionário (aqui, um stemmer Snowball English) a ser usado para a normalização do sintagma. Observe que o subdicionário terá sua própria configuração (por exemplo, palavras irrelevantes), que não é mostrada aqui.

Agora é possível vincular o dicionário de sinônimos `thesaurus_simple` aos tipos de token desejados em uma configuração, por exemplo:

```
ALTER TEXT SEARCH CONFIGURATION russian
    ALTER MAPPING FOR asciiword, asciihword, hword_asciipart
    WITH thesaurus_simple;
```

#### 12.6.4.2. Exemplo de tesauros [#](#TEXTSEARCH-THESAURUS-EXAMPLES)

Considere um simples tesauro astronômico `thesaurus_astro`, que contém algumas combinações de palavras astronômicas:

```
supernovae stars : sn
crab nebulae : crab
```

Abaixo, criamos um dicionário e vinculamos alguns tipos de token a um tesauro astronômico e um stemmer em inglês:

```
CREATE TEXT SEARCH DICTIONARY thesaurus_astro (
    TEMPLATE = thesaurus,
    DictFile = thesaurus_astro,
    Dictionary = english_stem
);

ALTER TEXT SEARCH CONFIGURATION russian
    ALTER MAPPING FOR asciiword, asciihword, hword_asciipart
    WITH thesaurus_astro, english_stem;
```

Agora podemos ver como funciona. `ts_lexize` não é muito útil para testar um tesauro, porque trata sua entrada como um único token. Em vez disso, podemos usar `plainto_tsquery` e `to_tsvector`, que irão dividir suas strings de entrada em vários tokens:

```
SELECT plainto_tsquery('supernova star');
 plainto_tsquery
-----------------
 'sn'

SELECT to_tsvector('supernova star');
 to_tsvector
-------------
 'sn':1
```

Em princípio, é possível usar `to_tsquery` se você citar o argumento:

```
SELECT to_tsquery('''supernova star''');
 to_tsquery
------------
 'sn'
```

Observe que `supernova star` corresponde a `supernovae stars` em `thesaurus_astro`, pois especificamos o `english_stem` stemmer na definição do tesauro. O stemmer removido os `e` e `s`.

Para indexar a frase original, bem como a substituta, basta incluí-la na parte direita da definição:

```
supernovae stars : sn supernovae stars

SELECT plainto_tsquery('supernova star');
       plainto_tsquery
-----------------------------
 'sn' & 'supernova' & 'star'
```

### 12.6.5. Dicionário Ispell [#](#TEXTSEARCH-ISPELL-DICTIONARY)

O modelo de dicionário Ispell suporta *dicionários morfológicos*, que podem normalizar muitas formas linguísticas diferentes de uma palavra no mesmo lexema. Por exemplo, um dicionário Ispell em inglês pode corresponder a todas as declinações e conjugações do termo de busca `bank`, por exemplo, `banking`, `banked`, `banks`, `banks'` e `bank's`.

A distribuição padrão do PostgreSQL não inclui nenhum arquivo de configuração do Ispell. Dicionários para um grande número de idiomas estão disponíveis em [Ispell](https://www.cs.hmc.edu/~geoff/ispell.html). Além disso, alguns formatos de arquivo de dicionário mais modernos são suportados — [MySpell](https://en.wikipedia.org/wiki/MySpell) (OO < 2.0.1) and [Hunspell][[PH_LNK_130]] (OO >= 2.0.2). Uma grande lista de dicionários está disponível no [Wiki do OpenOffice](https://wiki.openoffice.org/wiki/Dictionaries).

Para criar um dicionário Ispell, realize as etapas a seguir:

* faça o download dos arquivos de configuração do dicionário. Os arquivos de extensão do OpenOffice têm a extensão `.oxt`. É necessário extrair os arquivos `.aff` e `.dic`, alterar as extensões para `.affix` e `.dict`. Para alguns arquivos de dicionário, também é necessário converter os caracteres para o codificação UTF-8 com comandos (por exemplo, para um dicionário de língua norueguesa):

* copie os arquivos para o diretório `$SHAREDIR/tsearch_data`
* carregue os arquivos no PostgreSQL com o seguinte comando:

```
CREATE TEXT SEARCH DICTIONARY english_hunspell (
    TEMPLATE = ispell,
    DictFile = en_us,
    AffFile = en_us,
    Stopwords = english);
```

Aqui, `DictFile`, `AffFile` e `StopWords` especificam os nomes básicos dos arquivos de dicionário, afixos e palavras-stop. O arquivo de palavras-stop tem o mesmo formato explicado acima para o tipo de dicionário `simple`. O formato dos outros arquivos não é especificado aqui, mas está disponível nos sites mencionados acima.

Os dicionários Ispell geralmente reconhecem um conjunto limitado de palavras, então eles devem ser seguidos por outro dicionário mais amplo; por exemplo, um dicionário Snowball, que reconhece tudo.

O arquivo `.affix` do Ispell tem a seguinte estrutura:

```
prefixes
flag *A:
    .           >   RE      # As in enter > reenter
suffixes
flag T:
    E           >   ST      # As in late > latest
    [^AEIOU]Y   >   -Y,IEST # As in dirty > dirtiest
    [AEIOU]Y    >   EST     # As in gray > grayest
    [^EY]       >   EST     # As in small > smallest
```

E o arquivo `.dict` tem a seguinte estrutura:

```
lapse/ADGRS
lard/DGRS
large/PRTY
lark/MRS
```

O formato do arquivo `.dict` é:

```
basic_form/affix_class_name
```

No arquivo `.affix`, cada sinalizador de afixação é descrito no seguinte formato:

```
condition > [-stripping_letters,] adding_affix
```

Aqui, a condição tem um formato semelhante ao dos padrões de expressão regular. Ela pode usar agrupamentos `[...]` e `[^...]`. Por exemplo, `[AEIOU]Y` significa que a última letra da palavra é `"y"` e a penúltima letra é `"a"`, `"e"`, `"i"`, `"o"` ou `"u"`. `[^EY]` significa que a última letra não é nem `"e"` nem `"y"`.

Os dicionários Ispell suportam a divisão de palavras compostas; um recurso útil. Observe que o arquivo de afixos deve especificar uma bandeira especial usando a declaração `compoundwords controlled` que marca as palavras do dicionário que podem participar da formação de compostos:

```
compoundwords  controlled z
```

Aqui estão alguns exemplos para o idioma norueguês:

```
SELECT ts_lexize('norwegian_ispell', 'overbuljongterningpakkmesterassistent');
   {over,buljong,terning,pakk,mester,assistent}
SELECT ts_lexize('norwegian_ispell', 'sjokoladefabrikk');
   {sjokoladefabrikk,sjokolade,fabrikk}
```

O formato MySpell é um subconjunto do Hunspell. O arquivo `.affix` do Hunspell tem a seguinte estrutura:

```
PFX A Y 1
PFX A   0     re         .
SFX T N 4
SFX T   0     st         e
SFX T   y     iest       [^aeiou]y
SFX T   0     est        [aeiou]y
SFX T   0     est        [^ey]
```

A primeira linha de uma classe de afixação é o cabeçalho. Os campos de uma regra de afixação são listados após o cabeçalho:

* nome do parâmetro (PFX ou SFX) * bandeira (nome da classe de afixação) * remoção de caracteres do início (no prefixo) ou fim (no sufixo) da palavra * adição de afixação * condição que tem um formato semelhante ao formato de expressões regulares.

O arquivo `.dict` parece com o arquivo `.dict` do Ispell:

```
larder/M
lardy/RT
large/RSPMYT
largehearted
```

### Nota

MySpell não suporta palavras compostas. O Hunspell tem um suporte sofisticado para palavras compostas. Atualmente, o PostgreSQL implementa apenas as operações básicas de palavras compostas do Hunspell.

### 12.6.6. Dicionário Snowball [#](#TEXTSEARCH-SNOWBALL-DICTIONARY)

O modelo de dicionário Snowball é baseado em um projeto de Martin Porter, inventor do popular algoritmo de derivação de Porter para a língua inglesa. O Snowball agora fornece algoritmos de derivação para muitas línguas (consulte o site do Snowball [(https://snowballstem.org/)] para mais informações). Cada algoritmo entende como reduzir formas comuns de variantes de palavras a uma ortografia base, ou raiz, dentro de sua língua. Um dicionário Snowball requer um parâmetro `language` para identificar qual derivador usar e, opcionalmente, pode especificar um nome de arquivo `stopword` que fornece uma lista de palavras a serem eliminadas. (As listas padrão de palavras irrelevantes do PostgreSQL também são fornecidas pelo projeto Snowball.) Por exemplo, há uma definição embutida equivalente a

```
CREATE TEXT SEARCH DICTIONARY english_stem (
    TEMPLATE = snowball,
    Language = english,
    StopWords = english
);
```

O formato do arquivo de palavras-chave é o mesmo que já explicado.

Um dicionário Snowball reconhece tudo, independentemente de ser capaz de simplificar a palavra, então ele deve ser colocado no final da lista de dicionários. Não faz sentido tê-lo antes de qualquer outro dicionário, porque um token nunca passará por ele para o próximo dicionário.