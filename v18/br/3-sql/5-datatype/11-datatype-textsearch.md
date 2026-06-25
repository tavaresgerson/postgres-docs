### 8.11. Tipos de pesquisa de texto [#](#DATATYPE-TEXTSEARCH)

* [8.11.1. `tsvector`](datatype-textsearch.md#DATATYPE-TSVECTOR)
* [8.11.2. `tsquery`](datatype-textsearch.md#DATATYPE-TSQUERY)

O PostgreSQL oferece dois tipos de dados projetados para suportar a pesquisa de texto completo, que é a atividade de procurar por uma coleção de *documentos* em linguagem natural para localizar aqueles que melhor correspondem a uma *consulta*. O tipo `tsvector` representa um documento em uma forma otimizada para pesquisa de texto; o tipo `tsquery` representa de forma semelhante uma consulta de texto. O [Capítulo 12](textsearch.md "Chapter 12. Full Text Search") fornece uma explicação detalhada sobre essa facilidade, e [Seção 9.13](functions-textsearch.md "9.13. Text Search Functions and Operators") resume as funções e operadores relacionados.

#### 8.11.1. `tsvector` [#](#DATATYPE-TSVECTOR)

Um valor `tsvector` é uma lista ordenada de *lexemas* distintos, que são palavras que foram *normalizadas* para mesclar diferentes variantes da mesma palavra (consulte o [Capítulo 12](textsearch.md) para detalhes). A ordenação e a eliminação de duplicatas são feitas automaticamente durante a entrada, como mostrado neste exemplo:

```sql
SELECT 'a fat cat sat on a mat and ate a fat rat'::tsvector;
                      tsvector
----------------------------------------------------
 'a' 'and' 'ate' 'cat' 'fat' 'mat' 'on' 'rat' 'sat'
```

Para representar lexemas que contêm espaços em branco ou pontuação, rode-os com aspas:

```sql
SELECT $$the lexeme '    ' contains spaces$$::tsvector;
                 tsvector
-------------------------------------------
 '    ' 'contains' 'lexeme' 'spaces' 'the'
```

(Usamos aspas com citação em dólares neste exemplo e no próximo para evitar a confusão de ter que colocar aspas duplas dentro das aspas.) Aspas embutidas e barras invertidas devem ser duplicadas:

```sql
SELECT $$the lexeme 'Joe''s' contains a quote$$::tsvector;
                    tsvector
------------------------------------------------
 'Joe''s' 'a' 'contains' 'lexeme' 'quote' 'the'
```

Opcionalmente, inteiros *posições* podem ser anexados a lexemas:

```sql
SELECT 'a:1 fat:2 cat:3 sat:4 on:5 a:6 mat:7 and:8 ate:9 a:10 fat:11 rat:12'::tsvector;
                                  tsvector
-------------------------------------------------------------------​------------
 'a':1,6,10 'and':8 'ate':9 'cat':3 'fat':2,11 'mat':7 'on':5 'rat':12 'sat':4
```

Uma posição normalmente indica a localização da palavra fonte no documento. As informações de posição podem ser usadas para *classificação de proximidade*. Os valores de posição podem variar de 1 a 16383; números maiores são silenciosamente definidos como 16383. Posicionamentos duplicados para o mesmo léxico são descartados.

Lexemas que possuem posições podem ser ainda rotulados com um *peso*, que pode ser `A`, `B`, `C` ou `D`. `D` é o padrão e, portanto, não é mostrado na saída:

```sql
SELECT 'a:1A fat:2B,4C cat:5D'::tsvector;
          tsvector
----------------------------
 'a':1A 'cat':5 'fat':2B,4C
```

Os pesos são normalmente usados para refletir a estrutura do documento, por exemplo, marcando palavras de título de maneira diferente das palavras do corpo. As funções de classificação de pesquisa de texto podem atribuir diferentes prioridades aos diferentes marcadores de peso.

É importante entender que o próprio tipo `tsvector` não realiza nenhuma normalização de palavras; ele assume que as palavras que recebe são normalizadas adequadamente para a aplicação. Por exemplo,

```sql
SELECT 'The Fat Rats'::tsvector;
      tsvector
--------------------
 'Fat' 'Rats' 'The'
```

Para a maioria das aplicações que buscam texto em inglês, as palavras acima seriam consideradas não normalizadas, mas o `tsvector` não se importa. O texto do documento bruto geralmente deve ser passado pelo `to_tsvector` para normalizar as palavras adequadamente para pesquisa:

```sql
SELECT to_tsvector('english', 'The Fat Rats');
   to_tsvector
-----------------
 'fat':2 'rat':3
```

Mais detalhes, veja o capítulo 12 [(textsearch.md "Chapter 12. Full Text Search")].

#### 8.11.2. `tsquery` [#](#DATATYPE-TSQUERY)

Um valor `tsquery` armazena léxicos que devem ser pesquisados e pode combiná-los usando os operadores lógicos `&` (E), `|` (OU) e `!` (NÃO), bem como o operador de busca de frase `<->` (SE SEGUIDO POR). Há também uma variante `<N>` do operador SE SEGUIDO POR, onde *`N`* é uma constante numérica que especifica a distância entre os dois léxicos que estão sendo pesquisados. `<->` é equivalente a `<1>`.

As parênteses podem ser usadas para impor o agrupamento desses operadores. Na ausência de parênteses, `!` (NOT) se liga mais fortemente, `<->` (FOLLOWED BY) em seguida, `&` (E), com `|` (OU) se ligando menos fortemente.

Aqui estão alguns exemplos:

```sql
SELECT 'fat & rat'::tsquery;
    tsquery
---------------
 'fat' & 'rat'

SELECT 'fat & (rat | cat)'::tsquery;
          tsquery
---------------------------
 'fat' & ( 'rat' | 'cat' )

SELECT 'fat & rat & ! cat'::tsquery;
        tsquery
------------------------
 'fat' & 'rat' & !'cat'
```

Opcionalmente, os lexemas em um `tsquery` podem ser rotulados com uma ou mais letras de peso, o que os restringe a corresponder apenas aos lexemas `tsvector` com um desses pesos:

```sql
SELECT 'fat:ab & cat'::tsquery;
    tsquery
------------------
 'fat':AB & 'cat'
```

Além disso, lexemas em um `tsquery` podem ser rotulados com `*` para especificar a correspondência de prefixo:

```sql
SELECT 'super:*'::tsquery;
  tsquery
-----------
 'super':*
```

Essa consulta corresponderá a qualquer palavra em um `tsvector` que comece com “super”.

As citações de regras para lexemas são as mesmas descritas anteriormente para lexemas em `tsvector`; e, como com `tsvector`, qualquer normalização necessária de palavras deve ser feita antes de converter para o tipo `tsquery`. A função `to_tsquery` é conveniente para realizar tal normalização:

```sql
SELECT to_tsquery('Fat:ab & Cats');
    to_tsquery
------------------
 'fat':AB & 'cat'
```

Observe que `to_tsquery` processará prefixos da mesma forma que outras palavras, o que significa que essa comparação retornará verdadeiro:

```sql
SELECT to_tsvector( 'postgraduate' ) @@ to_tsquery( 'postgres:*' );
 ?column?
----------
 t
```

porque `postgres` é derivado para `postgr`:

```sql
SELECT to_tsvector( 'postgraduate' ), to_tsquery( 'postgres:*' );
  to_tsvector  | to_tsquery
---------------+------------
 'postgradu':1 | 'postgr':*
```

que corresponderá à forma reduzida de `postgraduate`.