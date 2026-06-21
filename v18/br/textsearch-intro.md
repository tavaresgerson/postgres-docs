## 12.1. Introdução [#](#TEXTSEARCH-INTRO)

* [12.1.1. O que é um documento?](textsearch-intro.md#TEXTSEARCH-DOCUMENT)
* [12.1.2. Contagem básica de texto](textsearch-intro.md#TEXTSEARCH-MATCHING)
* [12.1.3. Configurações](textsearch-intro.md#TEXTSEARCH-INTRO-CONFIGURATIONS)

A pesquisa de texto completo (ou simplesmente *pesquisa de texto*) permite identificar *documentos* em linguagem natural que satisfazem uma *consulta*, e, opcionalmente, classificá-los por relevância em relação à consulta. O tipo de pesquisa mais comum é encontrar todos os documentos que contenham termos de *consulta* específicos e devolvê-los em ordem de *similaridade* com a consulta. As noções de `query` e `similarity` são muito flexíveis e dependem da aplicação específica. A pesquisa mais simples considera `query` como um conjunto de palavras e `similarity` como a frequência de palavras de consulta no documento.

Os operadores de busca textual existem em bancos de dados há anos. O PostgreSQL possui os operadores `~`, `~*`, `LIKE` e `ILIKE` para tipos de dados textuais, mas eles carecem de muitas propriedades essenciais exigidas pelos sistemas de informação modernos:

* Não há suporte linguístico, mesmo para o inglês. As expressões regulares não são suficientes porque não conseguem lidar facilmente com palavras derivadas, por exemplo, `satisfies` e `satisfy`. Você pode perder documentos que contêm `satisfies`, embora você provavelmente queira encontrá-los ao pesquisar `satisfy`. É possível usar `OR` para pesquisar múltiplas formas derivadas, mas isso é tedioso e propenso a erros (algumas palavras podem ter várias mil derivadas).
* Eles não fornecem uma ordenação (classificação) dos resultados da pesquisa, o que os torna ineficazes quando milhares de documentos correspondentes são encontrados.
* Eles tendem a ser lentos porque não há suporte a índice, então eles devem processar todos os documentos para cada pesquisa.

A indexação de texto completo permite que os documentos sejam *pré-processados* e um índice seja salvo para buscas rápidas posteriores. O pré-processamento inclui:

* *Parágrafo de documentos em *tokens*. É útil identificar várias classes de tokens, por exemplo, números, palavras, palavras complexas, endereços de e-mail, para que possam ser processados de maneira diferente. Em princípio, as classes de tokens dependem da aplicação específica, mas para a maioria dos propósitos é adequado usar um conjunto predefinido de classes. O PostgreSQL usa um *parser* para realizar essa etapa. Um parser padrão é fornecido, e parsers personalizados podem ser criados para necessidades específicas.
* *Converter tokens em *lexemas*. Um lexema é uma string, assim como um token, mas foi *normalizado* para que diferentes formas da mesma palavra sejam iguais. Por exemplo, a normalização quase sempre inclui a dobragem de letras maiúsculas para minúsculas, e muitas vezes envolve a remoção de sufixos (como `s` ou `es` em inglês). Isso permite que as pesquisas encontrem formas variantes da mesma palavra, sem ter que inserir tediosamente todas as variantes possíveis. Além disso, essa etapa geralmente elimina *palavras comuns*, que são palavras tão comuns que são inúteis para pesquisas. (Em resumo, então, os tokens são fragmentos brutos do texto do documento, enquanto os lexemas são palavras que são consideradas úteis para indexação e pesquisa.) O PostgreSQL usa *dicionários* para realizar essa etapa. Vários dicionários padrão são fornecidos, e dicionários personalizados podem ser criados para necessidades específicas.
* *Armazenar documentos pré-processados otimizados para pesquisa. Por exemplo, cada documento pode ser representado como uma matriz ordenada de lexemas normalizados. Junto com os lexemas, é frequentemente desejável armazenar informações posicionais para usar para *classificação de proximidade*, para que um documento que contém uma região mais "densa" de palavras de consulta seja atribuído um rank mais alto do que um com palavras de consulta espalhadas.

As dicionários permitem o controle fino sobre como os tokens são normalizados. Com dicionários apropriados, você pode:

* Defina palavras paradas que não devem ser indexadas.
* Mapea sinônimos para uma única palavra usando o Ispell.
* Mapea frases para uma única palavra usando um tesauro.
* Mapea diferentes variações de uma palavra para uma forma canônica usando um dicionário Ispell.
* Mapea diferentes variações de uma palavra para uma forma canônica usando as regras do Snowball stemmer.

Um tipo de dados `tsvector` é fornecido para armazenar documentos pré-processados, juntamente com um tipo `tsquery` para representar consultas processadas ([Seção 8.11](datatype-textsearch.md "8.11. Text Search Types")). Existem muitas funções e operadores disponíveis para esses tipos de dados ([Seção 9.13](functions-textsearch.md "9.13. Text Search Functions and Operators")), dos quais o mais importante é o operador de correspondência `@@`, que introduzimos em [Seção 12.1.2](textsearch-intro.md#TEXTSEARCH-MATCHING "12.1.2. Basic Text Matching")). As pesquisas de texto completo podem ser aceleradas usando índices ([Seção 12.9](textsearch-indexes.md "12.9. Preferred Index Types for Text Search")).

### 12.1.1. O que é um documento? [#](#TEXTSEARCH-DOCUMENT)

Um *documento* é a unidade de busca em um sistema de busca de texto completo; por exemplo, um artigo de revista ou uma mensagem de e-mail. O motor de busca de texto deve ser capaz de analisar documentos e armazenar associações de lexemas (palavras-chave) com seus documentos parentais. Posteriormente, essas associações são usadas para buscar documentos que contenham palavras de consulta.

Para pesquisas no PostgreSQL, um documento é normalmente um campo textual dentro de uma linha de uma tabela de banco de dados, ou possivelmente uma combinação (concatenação) desses campos, talvez armazenada em várias tabelas ou obtida dinamicamente. Em outras palavras, um documento pode ser construído a partir de diferentes partes para indexação e pode não ser armazenado em nenhum lugar como um todo. Por exemplo:

```
SELECT title || ' ' ||  author || ' ' ||  abstract || ' ' || body AS document
FROM messages
WHERE mid = 12;

SELECT m.title || ' ' || m.author || ' ' || m.abstract || ' ' || d.body AS document
FROM messages m, docs d
WHERE m.mid = d.did AND m.mid = 12;
```

### Nota

Na verdade, nesses exemplos de consultas, `coalesce` deve ser usado para evitar que um único atributo `NULL` cause um resultado `NULL` para todo o documento.

Outra possibilidade é armazenar os documentos como arquivos de texto simples no sistema de arquivos. Neste caso, o banco de dados pode ser usado para armazenar o índice de texto completo e executar pesquisas, e um identificador único pode ser usado para recuperar o documento do sistema de arquivos. No entanto, recuperar arquivos de fora do banco de dados requer permissões de superusuário ou suporte a função especial, então isso geralmente é menos conveniente do que manter todos os dados dentro do PostgreSQL. Além disso, manter tudo dentro do banco de dados permite acesso fácil aos metadados do documento para auxiliar na indexação e exibição.

Para fins de pesquisa de texto, cada documento deve ser reduzido ao formato pré-processado `tsvector`. A pesquisa e a classificação são realizadas inteiramente na representação `tsvector` de um documento — o texto original só precisa ser recuperado quando o documento foi selecionado para exibição a um usuário. Por isso, frequentemente falamos do `tsvector` como sendo o documento, mas, claro, é apenas uma representação compacta do documento completo.

### 12.1.2. Correção de texto básico [#](#TEXTSEARCH-MATCHING)

A pesquisa de texto completo no PostgreSQL é baseada no operador de correspondência `@@`, que retorna `true` se um `tsvector` (documento) corresponder a um `tsquery` (consulta). Não importa qual tipo de dados é escrito primeiro:

```
SELECT 'a fat cat sat on a mat and ate a fat rat'::tsvector @@ 'cat & rat'::tsquery;
 ?column?
----------
 t

SELECT 'fat & cow'::tsquery @@ 'a fat cat sat on a mat and ate a fat rat'::tsvector;
 ?column?
----------
 f
```

Como o exemplo acima sugere, um `tsquery` não é apenas texto bruto, assim como um `tsvector` não é. Um `tsquery` contém termos de pesquisa, que devem ser lexemas já normalizados, e pode combinar vários termos usando operadores AND, OR, NOT e FOLLOWED BY. (Para detalhes de sintaxe, consulte [Seção 8.11.2][(datatype-textsearch.md#DATATYPE-TSQUERY "8.11.2. tsquery")]. Há funções `to_tsquery`, `plainto_tsquery` e `phraseto_tsquery` que são úteis na conversão de texto escrito pelo usuário em um `tsquery` adequado, principalmente por normalizar palavras que aparecem no texto. Da mesma forma, `to_tsvector` é usado para analisar e normalizar uma string de documento. Portanto, na prática, uma correspondência de pesquisa de texto ficaria mais assim:

```
SELECT to_tsvector('fat cats ate fat rats') @@ to_tsquery('fat & rat');
 ?column?
----------
 t
```

Observe que essa partida não teria sucesso se fosse escrita como

```
SELECT 'fat cats ate fat rats'::tsvector @@ to_tsquery('fat & rat');
 ?column?
----------
 f
```

já que aqui não ocorrerá normalização da palavra `rats`. Os elementos de um `tsvector` são léxicos, que são assumidos já normalizados, portanto, `rats` não corresponde a `rat`.

O operador `@@` também suporta entrada `text`, permitindo a conversão explícita de uma cadeia de texto para `tsvector` ou `tsquery` para ser ignorada em casos simples. As variantes disponíveis são:

```
tsvector @@ tsquery
tsquery  @@ tsvector
text @@ tsquery
text @@ text
```

Os dois primeiros desses já vimos. O formulário `text` `@@` `tsquery` é equivalente a `to_tsvector(x) @@ y`. O formulário `text` `@@` `text` é equivalente a `to_tsvector(x) @@ plainto_tsquery(y)`.

Dentro de um `tsquery`, o operador `&` (E) especifica que ambos os argumentos devem aparecer no documento para ter uma correspondência. Da mesma forma, o operador `|` (OU) especifica que pelo menos um dos seus argumentos deve aparecer, enquanto o operador `!` (NÃO) especifica que seu argumento deve *não* aparecer para ter uma correspondência. Por exemplo, a consulta `fat & ! rat` corresponde a documentos que contêm `fat`, mas não `rat`.

A busca por frases é possível com a ajuda do operador `<->` (SECUDO DE) `tsquery`, que corresponde apenas se seus argumentos tiverem correspondências adjacentes e na ordem dada. Por exemplo:

```
SELECT to_tsvector('fatal error') @@ to_tsquery('fatal <-> error');
 ?column?
----------
 t

SELECT to_tsvector('error is not fatal') @@ to_tsquery('fatal <-> error');
 ?column?
----------
 f
```

Existe uma versão mais geral do operador FOLLOWED BY na forma `<N>`, onde *`N`* é um número inteiro que representa a diferença entre as posições dos lexemas correspondentes. `<1>` é o mesmo que `<->`, enquanto `<2>` permite que exatamente outro lexema apareça entre os correspondentes, e assim por diante. A função `phraseto_tsquery` faz uso desse operador para construir um `tsquery` que pode corresponder a uma frase de várias palavras quando algumas das palavras são palavras paradas. Por exemplo:

```
SELECT phraseto_tsquery('cats ate rats');
       phraseto_tsquery
-------------------------------
 'cat' <-> 'ate' <-> 'rat'

SELECT phraseto_tsquery('the cats ate the rats');
       phraseto_tsquery
-------------------------------
 'cat' <-> 'ate' <2> 'rat'
```

Um caso especial que às vezes é útil é que `<0>` pode ser usado para exigir que dois padrões correspondam à mesma palavra.

As parênteses podem ser usadas para controlar a formação de operadores `tsquery`. Sem parênteses, `|` se liga menos fortemente, depois `&`, depois `<->` e `!` mais fortemente.

Vale ressaltar que os operadores AND/OR/NOT significam algo sutilmente diferente quando estão dentro dos argumentos de um operador FOLLOWED BY do que quando não estão, porque dentro de FOLLOWED BY a posição exata da correspondência é significativa. Por exemplo, normalmente `!x` corresponde apenas a documentos que não contêm `x` em nenhum lugar. Mas `!x <-> y` corresponde a `y` se não estiver imediatamente após um `x`; uma ocorrência de `x` em outro lugar no documento não impede uma correspondência. Outro exemplo é que `x & y` normalmente exige que `x` e `y` apareçam em algum lugar do documento, mas `(x & y) <-> z` exige que `x` e `y` correspondam no mesmo lugar, imediatamente antes de um `z`. Assim, essa consulta se comporta de maneira diferente de `x <-> z & y <-> z`, que corresponderá a um documento contendo duas sequências separadas `x z` e `y z`. (Esta consulta específica é inútil conforme escrita, uma vez que `x` e `y` não poderiam corresponder no mesmo lugar; mas com situações mais complexas, como padrões de correspondência de prefixo, uma consulta deste tipo poderia ser útil.)

### 12.1.3. Configurações [#](#TEXTSEARCH-INTRO-CONFIGURATIONS)

O que está acima são todos exemplos de busca de texto simples. Como mencionado anteriormente, a funcionalidade de busca de texto completo inclui a capacidade de fazer muitas outras coisas: pular a indexação de determinadas palavras (palavras-chave), processar sinônimos e usar análise sofisticada, por exemplo, analisar com base em mais do que apenas espaço em branco. Essa funcionalidade é controlada por *configurações de busca de texto*. O PostgreSQL vem com configurações predefinidas para muitas línguas, e você pode facilmente criar suas próprias configurações. (O comando `\dF` do psql mostra todas as configurações disponíveis.)

Durante a instalação, uma configuração apropriada é selecionada e [default_text_search_config][(runtime-config-client.md#GUC-DEFAULT-TEXT-SEARCH-CONFIG)] é definida conforme necessário em `postgresql.conf`. Se você estiver usando a mesma configuração de pesquisa de texto para todo o clúster, pode usar o valor em `postgresql.conf`. Para usar diferentes configurações em todo o clúster, mas a mesma configuração em qualquer uma das bases de dados, use `ALTER DATABASE ... SET`. Caso contrário, você pode definir `default_text_search_config` em cada sessão.

Cada função de busca de texto que depende de uma configuração tem um argumento opcional `regconfig`, para que a configuração a ser usada possa ser especificada explicitamente. `default_text_search_config` é usado apenas quando este argumento é omitido.

Para facilitar a construção de configurações personalizadas de busca de texto, uma configuração é construída a partir de objetos de banco de dados mais simples. A facilidade de busca de texto do PostgreSQL fornece quatro tipos de objetos de banco de dados relacionados à configuração:

* *Analizadores de pesquisa de texto* quebram os documentos em tokens e classificam cada token (por exemplo, como palavras ou números).
* *Dicionários de pesquisa de texto* convertem os tokens em forma normalizada e rejeitam palavras paradas.
* *Modelos de pesquisa de texto* fornecem as funções subjacentes aos dicionários. (Um dicionário simplesmente especifica um modelo e um conjunto de parâmetros para o modelo.)
* *Configurações de pesquisa de texto* selecionam um analisador e um conjunto de dicionários a serem usados para normalizar os tokens produzidos pelo analisador.

Os analisadores e modelos de pesquisa de texto são construídos a partir de funções C de nível baixo; portanto, é necessário ter habilidade em programação em C para desenvolvê-los, e privilégios de administrador para instalá-los em um banco de dados. (Existem exemplos de analisadores e modelos de pesquisa de texto adicionais na área `contrib/` da distribuição PostgreSQL.) Como os dicionários e as configurações apenas parametrizam e conectam alguns analisadores e modelos de pesquisa de texto subjacentes, não é necessário privilégio especial para criar um novo dicionário ou configuração. Exemplos de criação de dicionários e configurações personalizadas aparecem mais adiante neste capítulo.