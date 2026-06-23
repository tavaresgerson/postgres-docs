## 12.4. Recursos adicionais [#](#TEXTSEARCH-FEATURES)

* [12.4.1. Manipulação de documentos](textsearch-features.md#TEXTSEARCH-MANIPULATE-TSVECTOR)
* [12.4.2. Manipulação de consultas](textsearch-features.md#TEXTSEARCH-MANIPULATE-TSQUERY)
* [12.4.3. Gatilhos para atualizações automáticas](textsearch-features.md#TEXTSEARCH-UPDATE-TRIGGERS)
* [12.4.4. Recolha de estatísticas de documentos](textsearch-features.md#TEXTSEARCH-STATISTICS)

Esta seção descreve funções e operadores adicionais que são úteis em conexão com a pesquisa de texto.

### 12.4.1. Manipulação de documentos [#](#TEXTSEARCH-MANIPULATE-TSVECTOR)

[Seção 12.3.1] (textsearch-controls.md#TEXTSEARCH-PARSING-DOCUMENTS "12.3.1. Parsing Documents") mostrou como documentos textuais brutos podem ser convertidos em valores de `tsvector`. O PostgreSQL também fornece funções e operadores que podem ser usados para manipular documentos que já estão na forma de `tsvector`.

`tsvector || tsvector`: O operador de concatenação `tsvector` retorna um vetor que combina os lexemas e as informações posicionais dos dois vetores fornecidos como argumentos. As posições e as etiquetas de peso são mantidas durante a concatenação. As posições que aparecem no vetor da direita são deslocadas pela maior posição mencionada no vetor da esquerda, de modo que o resultado é quase equivalente ao resultado de realizar `to_tsvector` na concatenação das duas strings originais do documento. (A equivalência não é exata, porque quaisquer palavras-chave removidas do final do argumento da esquerda não afetarão o resultado, enquanto que elas teriam afetado as posições dos lexema no argumento da direita se a concatenação textual fosse usada.)

Uma vantagem de usar concatenação na forma vetorial, em vez de concatenar texto antes de aplicar `to_tsvector`, é que você pode usar diferentes configurações para analisar diferentes seções do documento. Além disso, porque a função `setweight` marca todos os lexemas do vetor fornecido da mesma maneira, é necessário analisar o texto e fazer `setweight` antes de concatenar, se você deseja rotular diferentes partes do documento com diferentes pesos.

`setweight(vector tsvector, weight "char") returns tsvector`: `setweight` retorna uma cópia do vetor de entrada na qual cada posição foi rotulada com o dado *`weight`*, seja `A`, `B`, `C` ou `D`. (`D` é o padrão para novos vetores e, como tal, não é exibido na saída.) Essas etiquetas são mantidas quando os vetores são concatenados, permitindo que palavras de diferentes partes de um documento sejam ponderadas de maneira diferente por funções de classificação.

Observe que as etiquetas de peso se aplicam a *posições*, não a *lexemas*. Se o vetor de entrada tiver sido despojado de posições, então `setweight` não faz nada.

`length(vector tsvector) returns integer`: Retorna o número de lexemas armazenados no vetor.

`strip(vector tsvector) returns tsvector`: Retorna um vetor que lista os mesmos lexemas que o vetor fornecido, mas não possui nenhuma informação sobre posição ou peso. O resultado geralmente é muito menor do que um vetor não filtrado, mas também é menos útil. O ranking de relevância não funciona tão bem em vetores filtrados quanto em vetores não filtrados. Além disso, o operador `<->` (SE SEGUIDO POR) `tsquery` nunca corresponderá ao input filtrado, uma vez que não pode determinar a distância entre as ocorrências dos lexemas.

Uma lista completa das funções relacionadas ao `tsvector` está disponível em [Tabela 9.43](functions-textsearch.md#TEXTSEARCH-FUNCTIONS-TABLE).

### 12.4.2. Manipulação de consultas [#](#TEXTSEARCH-MANIPULATE-TSQUERY)

[Seção 12.3.2] (textsearch-controls.md#TEXTSEARCH-PARSING-QUERIES "12.3.2. Parsing Queries") mostrou como consultas textuais bruxas podem ser convertidas em valores de `tsquery`. O PostgreSQL também fornece funções e operadores que podem ser usados para manipular consultas que já estão na forma de `tsquery`.

`tsquery && tsquery`: Retorna a combinação AND das duas consultas fornecidas.

`tsquery || tsquery`: Retorna a combinação OR das duas consultas fornecidas.

`!! tsquery`: Retorna a negação (NOT) da consulta fornecida.

`tsquery <-> tsquery`: Retorna uma consulta que busca uma correspondência para a primeira consulta dada imediatamente seguida por uma correspondência para a segunda consulta dada, usando o operador `<->` (FOLLOWED BY) `tsquery`. Por exemplo:

```
SELECT to_tsquery('fat') <-> to_tsquery('cat | rat'); ?column? ---------------------------- 'fat' <-> ( 'cat' | 'rat' )
```

`tsquery_phrase(query1 tsquery, query2 tsquery [, distance integer ]) returns tsquery`: Retorna uma consulta que busca uma correspondência para a primeira consulta dada, seguida por uma correspondência para a segunda consulta dada, a uma distância de exatamente *`distance`* lexemas, usando o operador `<N>` `tsquery`. Por exemplo:

```
SELECT tsquery_phrase(to_tsquery('fat'), to_tsquery('cat'), 10); tsquery_phrase ------------------ 'fat' <10> 'cat'
```

`numnode(query tsquery) returns integer` Retorna o número de nós (lexemas mais operadores) em um `tsquery`. Esta função é útil para determinar se o *`query`* é significativo (retorna > 0), ou contém apenas palavras de parada (retorna 0). Exemplos:

```
SELECT numnode(plainto_tsquery('the any')); NOTICE:  query contains only stopword(s) or doesn't contain lexeme(s), ignored numnode --------- 0

SELECT numnode('foo & bar'::tsquery); numnode --------- 3
```

`querytree(query tsquery) returns text`: Retorna a parte de um `tsquery` que pode ser usada para pesquisar um índice. Essa função é útil para detectar consultas não indexáveis, por exemplo, aquelas que contêm apenas palavras-chave ou apenas termos negados. Por exemplo:

```
SELECT querytree(to_tsquery('defined')); querytree ----------- 'defin'

SELECT querytree(to_tsquery('!defined')); querytree ----------- T
```

#### 12.4.2.1. Reescrita de consultas [#](#TEXTSEARCH-QUERY-REWRITING)

A família de funções `ts_rewrite` busca um `tsquery` dado para encontrar ocorrências de uma subconsulta alvo e substitui cada ocorrência por uma subconsulta substituta. Em essência, essa operação é uma versão específica do redimensionamento de substratos, específica para `tsquery`. Uma combinação de alvo e substituto pode ser considerada uma *regra de reescrita de consulta*. Uma coleção de tais regras de reescrita pode ser um poderoso auxílio de pesquisa. Por exemplo, você pode expandir a pesquisa usando sinônimos (por exemplo, `new york`, `big apple`, `nyc`, `gotham`) ou restringir a pesquisa para direcionar o usuário para algum tópico quente. Há alguma sobreposição de funcionalidades entre essa característica e os dicionários de sinônimos ([Seção 12.6.4](textsearch-dictionaries.md#TEXTSEARCH-THESAURUS "12.6.4. Thesaurus Dictionary")). No entanto, você pode modificar um conjunto de regras de reescrita em tempo real sem reindexação, enquanto a atualização de um sinônimo requer reindexação para ser eficaz.

`ts_rewrite (query tsquery, target tsquery, substitute tsquery) returns tsquery`: Esta forma de `ts_rewrite` simplesmente aplica uma única regra de reescrita: *`target`* é substituído por *`substitute`* onde quer que apareça em *`query`*. Por exemplo:

```
SELECT ts_rewrite('a & b'::tsquery, 'a'::tsquery, 'c'::tsquery); ts_rewrite ------------ 'b' & 'c'
```

`ts_rewrite (query tsquery, select text) returns tsquery`  :  Esta forma de `ts_rewrite` aceita um início *`query`* e um comando SQL *`select`*, que é dado como uma string de texto. O *`select`* deve gerar duas colunas do tipo `tsquery`. Para cada linha do resultado de *`select`*, as ocorrências do valor da primeira coluna (o alvo) são substituídas pelo valor da segunda coluna (o substituto) dentro do valor atual de *`query`*. Por exemplo:

```
CREATE TABLE aliases (t tsquery PRIMARY KEY, s tsquery); INSERT INTO aliases VALUES('a', 'c');

SELECT ts_rewrite('a & b'::tsquery, 'SELECT t,s FROM aliases'); ts_rewrite ------------ 'b' & 'c'
```

Observe que, quando várias regras de reescrita são aplicadas dessa maneira, a ordem de aplicação pode ser importante; portanto, na prática, você vai querer que a consulta de origem `ORDER BY` tenha uma chave de ordenação.

Vamos considerar um exemplo astronômico da vida real. Vamos expandir a consulta `supernovae` usando regras de reescrita baseadas em tabela:

```
CREATE TABLE aliases (t tsquery primary key, s tsquery); INSERT INTO aliases VALUES(to_tsquery('supernovae'), to_tsquery('supernovae|sn'));

SELECT ts_rewrite(to_tsquery('supernovae & crab'), 'SELECT * FROM aliases'); ts_rewrite --------------------------------- 'crab' & ( 'supernova' | 'sn' )
```

Podemos alterar as regras de reescrita apenas atualizando a tabela:

```
UPDATE aliases SET s = to_tsquery('supernovae|sn & !nebulae') WHERE t = to_tsquery('supernovae');

SELECT ts_rewrite(to_tsquery('supernovae & crab'), 'SELECT * FROM aliases'); ts_rewrite --------------------------------------------- 'crab' & ( 'supernova' | 'sn' & !'nebula' )
```

A reescrita pode ser lenta quando há muitas regras de reescrita, pois ela verifica cada regra em busca de uma possível correspondência. Para descartar regras óbvias que não são candidatas, podemos usar os operadores de contenção para o tipo `tsquery`. No exemplo abaixo, selecionamos apenas aquelas regras que podem corresponder à consulta original:

```
SELECT ts_rewrite('a & b'::tsquery, 'SELECT t,s FROM aliases WHERE ''a & b''::tsquery @> t'); ts_rewrite ------------ 'b' & 'c'
```

### 12.4.3. Gatilhos para Atualizações Automáticas [#](#TEXTSEARCH-UPDATE-TRIGGERS)

### Nota

O método descrito nesta seção foi obsoleto com o uso de colunas geradas armazenadas, conforme descrito em [Seção 12.2.2](textsearch-tables.md#TEXTSEARCH-TABLES-INDEX).

Ao usar uma coluna separada para armazenar a representação `tsvector` dos seus documentos, é necessário criar um gatilho para atualizar a coluna `tsvector` quando as colunas de conteúdo do documento forem alteradas. Duas funções de gatilho integradas estão disponíveis para isso, ou você pode escrever a sua própria.

```
tsvector_update_trigger(tsvector_column_name,​ config_name, text_column_name [, ... ]) tsvector_update_trigger_column(tsvector_column_name,​ config_column_name, text_column_name [, ... ])
```

Essas funções de disparo calculam automaticamente uma coluna `tsvector` a partir de uma ou mais colunas textuais, sob o controle de parâmetros especificados no comando `CREATE TRIGGER`. Um exemplo de seu uso é:

```
CREATE TABLE messages ( title       text, body        text, tsv         tsvector );

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE ON messages FOR EACH ROW EXECUTE FUNCTION tsvector_update_trigger(tsv, 'pg_catalog.english', title, body);

INSERT INTO messages VALUES('title here', 'the body text is here');

SELECT * FROM messages; title    |         body          |            tsv ------------+-----------------------+---------------------------- title here | the body text is here | 'bodi':4 'text':5 'titl':1

SELECT title, body FROM messages WHERE tsv @@ to_tsquery('title & body'); title    |         body ------------+----------------------- title here | the body text is here
```

Tendo criado este gatilho, qualquer alteração em `title` ou `body` será refletida automaticamente em `tsv`, sem que o aplicativo precise se preocupar com isso.

O primeiro argumento de ativação deve ser o nome da coluna `tsvector` a ser atualizada. O segundo argumento especifica a configuração de pesquisa de texto a ser usada para realizar a conversão. Para `tsvector_update_trigger`, o nome da configuração é simplesmente dado como o segundo argumento de ativação. Deve ser qualificada pelo esquema, conforme mostrado acima, para que o comportamento do gatilho não mude com mudanças em `search_path`. Para `tsvector_update_trigger_column`, o segundo argumento de ativação é o nome de outra coluna de tabela, que deve ser do tipo `regconfig`. Isso permite uma seleção por linha da configuração a ser feita. Os argumentos restantes são os nomes das colunas textuais (do tipo `text`, `varchar` ou `char`). Estes serão incluídos no documento na ordem dada. Os valores NULL serão ignorados (mas as outras colunas ainda serão indexadas).

Uma limitação desses gatilhos embutidos é que eles tratam todas as colunas de entrada da mesma forma. Para processar colunas de forma diferente — por exemplo, para pesar o título de forma diferente do corpo — é necessário escrever um gatilho personalizado. Aqui está um exemplo usando PL/pgSQL como a linguagem do gatilho:

```
CREATE FUNCTION messages_trigger() RETURNS trigger AS $$ begin new.tsv := setweight(to_tsvector('pg_catalog.english', coalesce(new.title,'')), 'A') || setweight(to_tsvector('pg_catalog.english', coalesce(new.body,'')), 'D'); return new; end $$ LANGUAGE plpgsql;

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE ON messages FOR EACH ROW EXECUTE FUNCTION messages_trigger();
```

Tenha em mente que é importante especificar o nome da configuração explicitamente ao criar valores de `tsvector` dentro de gatilhos, para que o conteúdo da coluna não seja afetado por alterações em `default_text_search_config`. Se não for feito isso, é provável que isso leve a problemas, como mudanças nos resultados de pesquisa após um dump e restauração.

### 12.4.4. Recolhimento de estatísticas de documentos [#](#TEXTSEARCH-STATISTICS)

A função `ts_stat` é útil para verificar sua configuração e para encontrar candidatos a palavras de parada.

```
ts_stat(sqlquery text, [ weights text, ] OUT word text, OUT ndoc integer, OUT nentry integer) returns setof record
```

*`sqlquery`* é um valor de texto que contém uma consulta SQL que deve retornar uma única coluna `tsvector`. `ts_stat` executa a consulta e retorna estatísticas sobre cada léxico distinto (palavra) contido nos dados de `tsvector`. As colunas devolvidas são

* *`word`* `text` — o valor de um léxico
* *`ndoc`* `integer` — número de documentos (`tsvector`s) em que a palavra ocorreu
* *`nentry`* `integer` — número total de ocorrências da palavra

Se o *`weights`* for fornecido, apenas as ocorrências que tenham um desses pesos serão contadas.

Por exemplo, para encontrar as dez palavras mais frequentes em uma coleção de documentos:

```
SELECT * FROM ts_stat('SELECT vector FROM apod') ORDER BY nentry DESC, ndoc DESC, word LIMIT 10;
```

O mesmo, mas contando apenas as ocorrências de palavras com peso `A` ou `B`:

```
SELECT * FROM ts_stat('SELECT vector FROM apod', 'ab') ORDER BY nentry DESC, ndoc DESC, word LIMIT 10;
```
