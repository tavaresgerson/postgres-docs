## F.35. pg_trgm — suporte para similaridade de texto usando trigrama [#](#PGTRGM)

* [F.35.1. Conceitos de Trigrama (ou Trigráfico)](pgtrgm.md#PGTRGM-CONCEPTS)
* [F.35.2. Funções e Operadores](pgtrgm.md#PGTRGM-FUNCS-OPS)
* [F.35.3. Parâmetros do GUC](pgtrgm.md#PGTRGM-GUC)
* [F.35.4. Suporte a Índice](pgtrgm.md#PGTRGM-INDEX)
* [F.35.5. Integração de Pesquisa de Texto](pgtrgm.md#PGTRGM-TEXT-SEARCH)
* [F.35.6. Referências](pgtrgm.md#PGTRGM-REFERENCES)
* [F.35.7. Autores](pgtrgm.md#PGTRGM-AUTHORS)

O módulo `pg_trgm` fornece funções e operadores para determinar a similaridade de texto alfanumérico com base na correspondência de trigramas, bem como classes de operadores de índice que suportam a busca rápida por strings semelhantes.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.35.1. Conceitos de Trigrama (ou Trigráfico) [#](#PGTRGM-CONCEPTS)

Um trigrama é um grupo de três caracteres consecutivos tomados de uma cadeia. Podemos medir a semelhança entre duas cadeias contando o número de trigramas que elas compartilham. Essa ideia simples acaba sendo muito eficaz para medir a semelhança de palavras em muitas línguas naturais.

### Nota

`pg_trgm` ignora caracteres não alfanuméricos ao extrair trigramas de uma string. Cada palavra é considerada ter dois espaços prefixados e um espaço sufixado ao determinar o conjunto de trigramas contidos na string. Por exemplo, o conjunto de trigramas na string “`cat`” é “ `c`”, “ `ca`”, “`cat`” e “`at` ”. O conjunto de trigramas na string “`foo|bar`” é “ `f`”, “ `fo`”, “`foo`”, “`oo` ”, “ `b`”, “ `ba`”, “`bar`” e “`ar` ”.

### F.35.2. Funções e Operadores [#](#PGTRGM-FUNCS-OPS)

As funções fornecidas pelo módulo `pg_trgm` são mostradas na [Tabela F.26](pgtrgm.md#PGTRGM-FUNC-TABLE "Table F.26. pg_trgm Functions"), os operadores na [Tabela F.27](pgtrgm.md#PGTRGM-OP-TABLE "Table F.27. pg_trgm Operators").

**Tabela F.26. `pg_trgm` Funções**



<table border="1" class="table" summary="pg_trgm Functions">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      similarity
     </code>
     (
     <code class="type">
      text
     </code>
     ,
     <code class="type">
      text
     </code>
     ) →
     <code class="returnvalue">
      real
     </code>
    </p>
    <p>
     Returns a number that indicates how similar the two arguments are. The range of the result is zero (indicating that the two strings are completely dissimilar) to one (indicating that the two strings are identical).
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      show_trgm
     </code>
     (
     <code class="type">
      text
     </code>
     ) →
     <code class="returnvalue">
      text[]
     </code>
    </p>
    <p>
     Returns an array of all the trigrams in the given string. (In practice this is seldom useful except for debugging.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      word_similarity
     </code>
     (
     <code class="type">
      text
     </code>
     ,
     <code class="type">
      text
     </code>
     ) →
     <code class="returnvalue">
      real
     </code>
    </p>
    <p>
     Returns a number that indicates the greatest similarity between the set of trigrams in the first string and any continuous extent of an ordered set of trigrams in the second string.  For details, see the explanation below.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      strict_word_similarity
     </code>
     (
     <code class="type">
      text
     </code>
     ,
     <code class="type">
      text
     </code>
     ) →
     <code class="returnvalue">
      real
     </code>
    </p>
    <p>
     Same as
     <code class="function">
      word_similarity
     </code>
     , but forces extent boundaries to match word boundaries.  Since we don't have cross-word trigrams, this function actually returns greatest similarity between first string and any continuous extent of words of the second string.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      show_limit
     </code>
     () →
     <code class="returnvalue">
      real
     </code>
    </p>
    <p>
     Returns the current similarity threshold used by the
     <code class="literal">
      %
     </code>
     operator.  This sets the minimum similarity between two words for them to be considered similar enough to be misspellings of each other, for example. (
     <span class="emphasis">
      <em>
       Deprecated
      </em>
     </span>
     ; instead use
     <code class="command">
      SHOW
     </code>
     <code class="varname">
      pg_trgm.similarity_threshold
     </code>
     .)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      set_limit
     </code>
     (
     <code class="type">
      real
     </code>
     ) →
     <code class="returnvalue">
      real
     </code>
    </p>
    <p>
     Sets the current similarity threshold that is used by the
     <code class="literal">
      %
     </code>
     operator.  The threshold must be between 0 and 1 (default is 0.3). Returns the same value passed in. (
     <span class="emphasis">
      <em>
       Deprecated
      </em>
     </span>
     ; instead use
     <code class="command">
      SET
     </code>
     <code class="varname">
      pg_trgm.similarity_threshold
     </code>
     .)
    </p>
   </td>
  </tr>
 </tbody>
</table>









Considere o exemplo a seguir:

```
# SELECT word_similarity('word', 'two words');
 word_similarity
-----------------
             0.8
(1 row)
```

Na primeira cadeia, o conjunto de trigêmeos é `{" w"," wo","wor","ord","rd "}`. Na segunda cadeia, o conjunto ordenado de trigêmeos é `{" t"," tw","two","wo "," w"," wo","wor","ord","rds","ds "}`. A extensão mais semelhante de um conjunto ordenado de trigêmeos na segunda cadeia é `{" w"," wo","wor","ord"}`, e a similaridade é `0.8`.

Essa função retorna um valor que pode ser entendido aproximadamente como a maior semelhança entre a primeira string e qualquer substring da segunda string. No entanto, essa função não adiciona preenchimento aos limites da extensão. Assim, o número de caracteres adicionais presentes na segunda string não é considerado, exceto pelos limites de palavras desalinhados.

Ao mesmo tempo, `strict_word_similarity` seleciona uma extensão de palavras na segunda cadeia. No exemplo acima, `strict_word_similarity` selecionaria a extensão de uma única palavra `'words'`, cujo conjunto de trigêmeos é `{" w"," wo","wor","ord","rds","ds "}`.

```
# SELECT strict_word_similarity('word', 'two words'), similarity('word', 'words');
 strict_word_similarity | similarity
------------------------+------------
               0.571429 |   0.571429
(1 row)
```

Assim, a função `strict_word_similarity` é útil para encontrar a similaridade com palavras inteiras, enquanto `word_similarity` é mais adequada para encontrar a similaridade com partes de palavras.

**Tabela F.27. Operadores `pg_trgm`**



<table border="1" class="table" summary="pg_trgm Operators">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Operador
    </p>
    <p>
     Descrição
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      text
     </code>
     <code class="literal">
      %
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Retornos
     <code class="literal">
      true
     </code>
     se seus argumentos tiverem uma similaridade maior do que o limite de similaridade atual definido por
     <code class="varname">
      pg_trgm.similarity_threshold
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      text
     </code>
     <code class="literal">
      &lt;%
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Retornos
     <code class="literal">
      true
     </code>
     se a semelhança entre o trigrama definido no primeiro argumento e uma extensão contínua de um conjunto de trigramas ordenado no segundo argumento for maior que o limite atual de semelhança de palavra definido por
     <code class="varname">
      pg_trgm.word_similarity_threshold
     </code>
     parameter.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      text
     </code>
     <code class="literal">
      %&gt;
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Comutador do
     <code class="literal">
      &lt;%
     </code>
     operator.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      text
     </code>
     <code class="literal">
      &lt;&lt;%
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Retornos
     <code class="literal">
      true
     </code>
     se seu segundo argumento tiver uma extensão contínua de um conjunto de trigramas ordenado que corresponda a limites de palavra, e sua semelhança com o conjunto de trigramas do primeiro argumento seja maior que o limite atual de semelhança de palavras estrita definido pelo
     <code class="varname">
      pg_trgm.strict_word_similarity_threshold
     </code>
     parameter.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      text
     </code>
     <code class="literal">
      %&gt;&gt;
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Comutador do
     <code class="literal">
      &lt;&lt;%
     </code>
     operator.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      text
     </code>
     <code class="literal">
      &lt;-&gt;
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      real
     </code>
    </p>
    <p>
     Retorna o
     <span class="quote">
      “
      <span class="quote">
       distância
      </span>
      ”
     </span>
     entre os argumentos, ou seja, um menos o
     <code class="function">
      similarity()
     </code>
     value.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      text
     </code>
     <code class="literal">
      &lt;&lt;-&gt;
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      real
     </code>
    </p>
    <p>
     Retorna o
     <span class="quote">
      “
      <span class="quote">
       distância
      </span>
      ”
     </span>
     entre os argumentos, ou seja, um menos o
     <code class="function">
      word_similarity()
     </code>
     value.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      text
     </code>
     <code class="literal">
      &lt;-&gt;&gt;
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      real
     </code>
    </p>
    <p>
     Comutador do
     <code class="literal">
      &lt;&lt;-&gt;
     </code>
     operator.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      text
     </code>
     <code class="literal">
      &lt;&lt;&lt;-&gt;
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      real
     </code>
    </p>
    <p>
     Retorna o
     <span class="quote">
      “
      <span class="quote">
       distância
      </span>
      ”
     </span>
     entre os argumentos, ou seja, um menos o
     <code class="function">
      strict_word_similarity()
     </code>
     value.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      text
     </code>
     <code class="literal">
      &lt;-&gt;&gt;&gt;
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      real
     </code>
    </p>
    <p>
     Comutador do
     <code class="literal">
      &lt;&lt;&lt;-&gt;
     </code>
     operator.
    </p>
   </td>
  </tr>
 </tbody>
</table>






### F.35.3. Parâmetros do GUC [#](#PGTRGM-GUC)

`pg_trgm.similarity_threshold` (`real`) [#](#GUC-PGTRGM-SIMILARITY-THRESHOLD): Define o limite de similaridade atual que é utilizado pelo operador `%`. O limite deve estar entre 0 e 1 (padrão é 0,3).

`pg_trgm.word_similarity_threshold` (`real`) [#](#GUC-PGTRGM-WORD-SIMILARITY-THRESHOLD): Define o limite atual de semelhança de palavras que é utilizado pelos operadores `<%` e `%>`. O limite deve estar entre 0 e 1 (padrão é 0,6).

`pg_trgm.strict_word_similarity_threshold` (`real`) [#](#GUC-PGTRGM-STRICT-WORD-SIMILARITY-THRESHOLD): Define o limite atual de semelhança de palavras estrita que é usado pelos operadores `<<%` e `%>>`. O limite deve estar entre 0 e 1 (padrão é 0,5).

### F.35.4. Suporte ao índice [#](#PGTRGM-INDEX)

O módulo `pg_trgm` fornece classes de operadores de índice GiST e GIN que permitem criar um índice sobre uma coluna de texto para fins de pesquisas de semelhança muito rápidas. Esses tipos de índice suportam os operadores de semelhança descritos acima e, além disso, suportam pesquisas de índice baseadas em trigêmeos para consultas de `LIKE`, `ILIKE`, `~`, `~*` e `=`. As comparações de semelhança são insensíveis ao caso em uma versão padrão do `pg_trgm`. Operadores de desigualdade não são suportados. Note que esses índices podem não ser tão eficientes quanto os índices regulares de árvore B para operadores de igualdade.

Exemplo:

```
CREATE TABLE test_trgm (t text);
CREATE INDEX trgm_idx ON test_trgm USING GIST (t gist_trgm_ops);
```

ou

```
CREATE INDEX trgm_idx ON test_trgm USING GIN (t gin_trgm_ops);
```

`gist_trgm_ops` O opclass GiST aproxima um conjunto de trigramas como uma assinatura de bitmap. Seu parâmetro inteiro opcional `siglen` determina o comprimento da assinatura em bytes. O comprimento padrão é de 12 bytes. Os valores válidos do comprimento da assinatura estão entre 1 e 2024 bytes. assinaturas mais longas levam a uma busca mais precisa (digitalizando uma fração menor do índice e menos páginas de heap), ao custo de um índice maior.

Exemplo de criação de um índice desse tipo com uma extensão de assinatura de 32 bytes:

```
CREATE INDEX trgm_idx ON test_trgm USING GIST (t gist_trgm_ops(siglen=32));
```

Neste ponto, você terá um índice na coluna `t` que você pode usar para pesquisa de similaridade. Uma consulta típica é

```
SELECT t, similarity(t, 'word') AS sml
  FROM test_trgm
  WHERE t % 'word'
  ORDER BY sml DESC, t;
```

Isso retornará todos os valores na coluna de texto que são suficientemente semelhantes a *`word`*, ordenados do melhor correspondente ao pior. O índice será usado para tornar essa operação rápida, mesmo em conjuntos de dados muito grandes.

Uma variante da consulta acima é

```
SELECT t, t <-> 'word' AS dist
  FROM test_trgm
  ORDER BY dist LIMIT 10;
```

Isso pode ser implementado de forma bastante eficiente por índices GiST, mas não por índices GIN. Geralmente, ele supera a primeira formulação quando apenas um pequeno número de correspondências mais próximas é necessário.

Além disso, você pode usar um índice na coluna `t` para similaridade de palavras ou similaridade estrita de palavras. As consultas típicas são:

```
SELECT t, word_similarity('word', t) AS sml
  FROM test_trgm
  WHERE 'word' <% t
  ORDER BY sml DESC, t;
```

e

```
SELECT t, strict_word_similarity('word', t) AS sml
  FROM test_trgm
  WHERE 'word' <<% t
  ORDER BY sml DESC, t;
```

Isso retornará todos os valores na coluna de texto para os quais há uma extensão contínua no conjunto de trigramas ordenado correspondente que é suficientemente semelhante ao conjunto de trigramas de *`word`*, classificado do melhor correspondente ao pior. O índice será usado para tornar essa operação rápida, mesmo em conjuntos de dados muito grandes.

Possíveis variantes das perguntas acima são:

```
SELECT t, 'word' <<-> t AS dist
  FROM test_trgm
  ORDER BY dist LIMIT 10;
```

e

```
SELECT t, 'word' <<<-> t AS dist
  FROM test_trgm
  ORDER BY dist LIMIT 10;
```

Isso pode ser implementado de forma bastante eficiente por índices GiST, mas não por índices GIN.

A partir do PostgreSQL 9.1, esses tipos de índice também suportam pesquisas de índice para `LIKE` e `ILIKE`, por exemplo.

```
SELECT * FROM test_trgm WHERE t LIKE '%foo%bar';
```

A pesquisa de índice funciona extraindo trigramas da string de pesquisa e, em seguida, procurando esses trigramas no índice. Quanto mais trigramas na string de pesquisa, mais eficaz é a pesquisa de índice. Ao contrário das pesquisas baseadas em árvores B, a string de pesquisa não precisa ser ancorada à esquerda.

A partir do PostgreSQL 9.3, esses tipos de índice também suportam pesquisas de índice para correspondências de expressão regular (operadores `~` e `~*`, por exemplo)

```
SELECT * FROM test_trgm WHERE t ~ '(foo|bar)';
```

A pesquisa do índice funciona extraindo trigramas da expressão regular e, em seguida, procurando esses trigramas no índice. Quanto mais trigramas puder ser extraído da expressão regular, mais eficaz será a pesquisa do índice. Ao contrário das pesquisas baseadas em árvores B, a string de pesquisa não precisa ser ancorada à esquerda.

Para as pesquisas tanto do `LIKE` quanto das de expressão regular, lembre-se de que um padrão sem trigramas extraíveis degenerará em uma varredura de índice completo.

A escolha entre a indexação GiST e GIN depende das características de desempenho relativas de GiST e GIN, que são discutidas em outros lugares.

### F.35.5. Integração de pesquisa de texto [#](#PGTRGM-TEXT-SEARCH)

A correspondência de trigramas é uma ferramenta muito útil quando usada em conjunto com um índice de texto completo. Em particular, ela pode ajudar a reconhecer palavras de entrada com erros que não serão correspondidas diretamente pelo mecanismo de pesquisa de texto completo.

O primeiro passo é gerar uma tabela auxiliar contendo todas as palavras únicas nos documentos:

```
CREATE TABLE words AS SELECT word FROM
        ts_stat('SELECT to_tsvector(''simple'', bodytext) FROM documents');
```

onde `documents` é uma tabela que possui um campo de texto `bodytext` que desejamos pesquisar. A razão para usar a configuração `simple` com a função `to_tsvector`, em vez de usar uma configuração específica para o idioma, é que queremos uma lista das palavras originais (não modificadas).

Em seguida, crie um índice de trigrama na coluna de palavra:

```
CREATE INDEX words_idx ON words USING GIN (word gin_trgm_ops);
```

Agora, uma consulta `SELECT` semelhante ao exemplo anterior pode ser usada para sugerir ortografias para palavras mal escritas nos termos de busca do usuário. Um teste extra útil é exigir que as palavras selecionadas também tenham comprimento semelhante à palavra mal escrita.

### Nota

Como a tabela `words` foi gerada como uma tabela separada e estática, ela precisará ser regenerada periodicamente para permanecer razoavelmente atualizada com a coleção de documentos. Manter-a exatamente atualizada geralmente não é necessário.

### F.35.6. Referências [#](#PGTRGM-REFERENCES)

Site de Desenvolvimento GiST <http://www.sai.msu.su/~megera/postgres/gist/>

Site de Desenvolvimento Tsearch2

### F.35.7. Autores [#](#PGTRGM-AUTHORS)

Oleg Bartunov `<oleg@sai.msu.su>`, Moscou, Universidade de Moscou, Rússia

Teodor Sigaev `<teodor@sigaev.ru>`, Moscou, Delta-Soft Ltd., Rússia

Alexander Korotkov `<a.korotkov@postgrespro.ru>`, Moscou, Postgres Professional, Rússia

Documentação: Christopher Kings-Lynne

Este módulo é patrocinado pela Delta-Soft Ltd., Moscou, Rússia.