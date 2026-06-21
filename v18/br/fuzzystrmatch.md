## F.16. fuzzystrmatch — determinar semelhanças e distância de strings [#](#FUZZYSTRMATCH)

* [F.16.1. Soundex][(fuzzystrmatch.md#FUZZYSTRMATCH-SOUNDEX)
* [F.16.2. Daitch-Mokotoff Soundex][(fuzzystrmatch.md#FUZZYSTRMATCH-DAITCH-MOKOTOFF)
* [F.16.3. Levenshtein][(fuzzystrmatch.md#FUZZYSTRMATCH-LEVENSHTEIN)
* [F.16.4. Metaphone][(fuzzystrmatch.md#FUZZYSTRMATCH-METAPHONE)
* [F.16.5. Double Metaphone][(fuzzystrmatch.md#FUZZYSTRMATCH-DOUBLE-METAPHONE)

O módulo `fuzzystrmatch` oferece várias funções para determinar semelhanças e distância entre strings.

### Atenção

Atualmente, as funções `soundex`, `metaphone`, `dmetaphone` e `dmetaphone_alt` não funcionam bem com codificações multibyte (como UTF-8). Use `daitch_mokotoff` ou `levenshtein` com esses dados.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.16.1. Soundex [#](#FUZZYSTRMATCH-SOUNDEX)

O sistema Soundex é um método de correspondência de nomes com sons semelhantes, convertendo-os no mesmo código. Inicialmente, foi utilizado pelo Censo dos Estados Unidos em 1880, 1900 e 1910. Observe que o Soundex não é muito útil para nomes que não são em inglês.

O módulo `fuzzystrmatch` oferece duas funções para trabalhar com códigos Soundex:

```
soundex(text) returns text
difference(text, text) returns int
```

A função `soundex` converte uma string em seu código Soundex. A função `difference` converte duas strings em seus códigos Soundex e, em seguida, reporta o número de posições de código correspondentes. Como os códigos Soundex têm quatro caracteres, o resultado varia de zero a quatro, com zero sendo sem correspondência e quatro sendo uma correspondência exata. (Assim, a função está mal nomeada — `similarity` teria sido um nome melhor.)

Aqui estão alguns exemplos de uso:

```
SELECT soundex('hello world!');

SELECT soundex('Anne'), soundex('Ann'), difference('Anne', 'Ann');
SELECT soundex('Anne'), soundex('Andrew'), difference('Anne', 'Andrew');
SELECT soundex('Anne'), soundex('Margaret'), difference('Anne', 'Margaret');

CREATE TABLE s (nm text);

INSERT INTO s VALUES ('john');
INSERT INTO s VALUES ('joan');
INSERT INTO s VALUES ('wobbly');
INSERT INTO s VALUES ('jack');

SELECT * FROM s WHERE soundex(nm) = soundex('john');

SELECT * FROM s WHERE difference(s.nm, 'john') > 2;
```

### F.16.2. Daitch-Mokotoff Soundex [#](#FUZZYSTRMATCH-DAITCH-MOKOTOFF)

Assim como o sistema original Soundex, o Daitch-Mokotoff Soundex combina nomes com sons semelhantes convertendo-os no mesmo código. No entanto, o Daitch-Mokotoff Soundex é significativamente mais útil para nomes que não são em inglês do que o sistema original. As principais melhorias em relação ao sistema original incluem:

* O código é baseado nas seis primeiras letras significativas, e não em quatro.
* Uma letra ou combinação de letras é mapeada em dez códigos possíveis, e não em sete.
* Quando duas letras consecutivas têm um único som, elas são codificadas como um único número.
* Quando uma letra ou combinação de letras pode ter diferentes sons, múltiplos códigos são emitidos para cobrir todas as possibilidades.

Esta função gera os códigos Daitch-Mokotoff de somatados para sua entrada:

```
daitch_mokotoff(source text) returns text[]
```

O resultado pode conter um ou mais códigos, dependendo de quantas pronúncias plausíveis houver, portanto, é representado como uma matriz.

Como um código Daitch-Mokotoff de somatônico consiste apenas em 6 dígitos, *`source`* deve ser preferencialmente uma palavra ou um nome.

Aqui estão alguns exemplos:

```
SELECT daitch_mokotoff('George');
 daitch_mokotoff
-----------------
 {595000}

SELECT daitch_mokotoff('John');
 daitch_mokotoff
-----------------
 {160000,460000}

SELECT daitch_mokotoff('Bierschbach');
                      daitch_mokotoff
-----------------------------------------------------------
 {794575,794574,794750,794740,745750,745740,747500,747400}

SELECT daitch_mokotoff('Schwartzenegger');
 daitch_mokotoff
-----------------
 {479465}
```

Para a correspondência de nomes únicos, os arrays de texto retornados podem ser correspondidos diretamente usando o operador `&&`: qualquer sobreposição pode ser considerada uma correspondência. Um índice GIN pode ser usado para eficiência, veja [Seção 65.4](gin.md) e este exemplo:

```
CREATE TABLE s (nm text);
CREATE INDEX ix_s_dm ON s USING gin (daitch_mokotoff(nm)) WITH (fastupdate = off);

INSERT INTO s (nm) VALUES
  ('Schwartzenegger'),
  ('John'),
  ('James'),
  ('Steinman'),
  ('Steinmetz');

SELECT * FROM s WHERE daitch_mokotoff(nm) && daitch_mokotoff('Swartzenegger');
SELECT * FROM s WHERE daitch_mokotoff(nm) && daitch_mokotoff('Jane');
SELECT * FROM s WHERE daitch_mokotoff(nm) && daitch_mokotoff('Jens');
```

Para indexação e correspondência de qualquer número de nomes em qualquer ordem, as funcionalidades de pesquisa de texto completo podem ser usadas. Veja [Capítulo 12](textsearch.md) e este exemplo:

```
CREATE FUNCTION soundex_tsvector(v_name text) RETURNS tsvector
BEGIN ATOMIC
  SELECT to_tsvector('simple',
                     string_agg(array_to_string(daitch_mokotoff(n), ' '), ' '))
  FROM regexp_split_to_table(v_name, '\s+') AS n;
END;

CREATE FUNCTION soundex_tsquery(v_name text) RETURNS tsquery
BEGIN ATOMIC
  SELECT string_agg('(' || array_to_string(daitch_mokotoff(n), '|') || ')', '&')::tsquery
  FROM regexp_split_to_table(v_name, '\s+') AS n;
END;

CREATE TABLE s (nm text);
CREATE INDEX ix_s_txt ON s USING gin (soundex_tsvector(nm)) WITH (fastupdate = off);

INSERT INTO s (nm) VALUES
  ('John Doe'),
  ('Jane Roe'),
  ('Public John Q.'),
  ('George Best'),
  ('John Yamson');

SELECT * FROM s WHERE soundex_tsvector(nm) @@ soundex_tsquery('john');
SELECT * FROM s WHERE soundex_tsvector(nm) @@ soundex_tsquery('jane doe');
SELECT * FROM s WHERE soundex_tsvector(nm) @@ soundex_tsquery('john public');
SELECT * FROM s WHERE soundex_tsvector(nm) @@ soundex_tsquery('besst, giorgio');
SELECT * FROM s WHERE soundex_tsvector(nm) @@ soundex_tsquery('Jameson John');
```

Se for desejado evitar a recálculo dos códigos soundex durante as revisões do índice, pode-se usar um índice em uma coluna separada em vez de um índice em uma expressão. Uma coluna gerada armazenada pode ser usada para isso; veja [Seção 5.4](ddl-generated-columns.md).

### F.16.3. Levenshtein [#](#FUZZYSTRMATCH-LEVENSHTEIN)

Esta função calcula a distância de Levenshtein entre duas strings:

```
levenshtein(source text, target text, ins_cost int, del_cost int, sub_cost int) returns int
levenshtein(source text, target text) returns int
levenshtein_less_equal(source text, target text, ins_cost int, del_cost int, sub_cost int, max_d int) returns int
levenshtein_less_equal(source text, target text, max_d int) returns int
```

Tanto `source` quanto `target` podem ser qualquer string não nula, com um máximo de 255 caracteres. Os parâmetros de custo especificam quanto cobrar por inserção, exclusão ou substituição de um caractere, respectivamente. Você pode omitir os parâmetros de custo, como na segunda versão da função; nesse caso, todos eles têm o valor padrão de 1.

`levenshtein_less_equal` é uma versão acelerada da função Levenshtein para uso quando apenas pequenas distâncias são de interesse. Se a distância real for menor ou igual a `max_d`, então `levenshtein_less_equal` retorna a distância correta; caso contrário, retorna algum valor maior que `max_d`. Se `max_d` for negativo, então o comportamento é o mesmo que `levenshtein`.

Exemplos:

```
test=# SELECT levenshtein('GUMBO', 'GAMBOL');
 levenshtein
-------------
           2
(1 row)

test=# SELECT levenshtein('GUMBO', 'GAMBOL', 2, 1, 1);
 levenshtein
-------------
           3
(1 row)

test=# SELECT levenshtein_less_equal('extensive', 'exhaustive', 2);
 levenshtein_less_equal
------------------------
                      3
(1 row)

test=# SELECT levenshtein_less_equal('extensive', 'exhaustive', 4);
 levenshtein_less_equal
------------------------
                      4
(1 row)
```

### F.16.4. Metafone [#](#FUZZYSTRMATCH-METAPHONE)

Assim como o Soundex, o Metaphone é baseado na ideia de construir um código representativo para uma string de entrada. Duas strings são consideradas semelhantes se tiverem os mesmos códigos.

Esta função calcula o código metafone de uma string de entrada:

```
metaphone(source text, max_output_length int) returns text
```

`source` deve ser uma string não nula com um máximo de 255 caracteres. `max_output_length` define o comprimento máximo do código metafone de saída; se for mais longo, a saída é truncada para esse comprimento.

Exemplo:

```
test=# SELECT metaphone('GUMBO', 4);
 metaphone
-----------
 KM
(1 row)
```

### F.16.5. Metafone Duplo [#](#FUZZYSTRMATCH-DOUBLE-METAPHONE)

O sistema Double Metaphone calcula duas cadeias de "som parecido" para uma cadeia de entrada dada — uma "primária" e uma "alternativa". Na maioria dos casos, elas são as mesmas, mas, especialmente em nomes não em inglês, podem ser um pouco diferentes, dependendo da pronúncia. Essas funções calculam os códigos primário e alternativo:

```
dmetaphone(source text) returns text
dmetaphone_alt(source text) returns text
```

Não há limite de comprimento nas strings de entrada.

Exemplo:

```
test=# SELECT dmetaphone('gumbo');
 dmetaphone
------------
 KMP
(1 row)
```
