## F.6. bloom — método de acesso ao índice de filtro bloom [#](#BLOOM)

* [F.6.1. Parâmetros][(bloom.md#BLOOM-PARAMETERS)]
* [F.6.2. Exemplos][(bloom.md#BLOOM-EXAMPLES)]
* [F.6.3. Interface da Classe Operadora][(bloom.md#BLOOM-OPERATOR-CLASS-INTERFACE)]
* [F.6.4. Limitações][(bloom.md#BLOOM-LIMITATIONS)]
* [F.6.5. Autores][(bloom.md#BLOOM-AUTHORS)]

`bloom` fornece um método de acesso ao índice baseado em [Bloom filters][(https://en.wikipedia.org/wiki/Bloom_filter)].

Um filtro Bloom é uma estrutura de dados eficiente em termos de espaço que é usada para testar se um elemento é membro de um conjunto. No caso de um método de acesso a índice, ele permite a rápida exclusão de tuplas que não correspondem, por meio de assinaturas cujas dimensões são determinadas na criação do índice.

Uma assinatura é uma representação perecedora dos(s) atributo(s) indexado(s), e como tal, é propensa a relatar falsos positivos; ou seja, pode ser relatado que um elemento está no conjunto, quando na verdade não está. Portanto, os resultados de busca do índice devem ser sempre verificados novamente usando os valores reais dos atributos da entrada do heap. Assinaturas maiores reduzem as chances de um falso positivo e, assim, reduzem o número de visitas inúteis ao heap, mas, claro, também tornam o índice maior e, portanto, mais lento para ser analisado.

Este tipo de índice é mais útil quando uma tabela tem muitos atributos e as consultas testam combinações arbitrárias deles. Um índice btree tradicional é mais rápido do que um índice bloom, mas pode exigir muitos índices btree para suportar todas as consultas possíveis, quando é necessário apenas um único índice bloom. No entanto, é importante notar que os índices bloom só suportam consultas de igualdade, enquanto os índices btree também podem realizar pesquisas de desigualdade e intervalo.

### F.6.1. Parâmetros [#](#BLOOM-PARAMETERS)

Um índice `bloom` aceita os seguintes parâmetros na sua cláusula `WITH`:

`length`: Comprimento de cada assinatura (entrada de índice) em bits. É arredondado para o múltiplo mais próximo de `16`. O padrão é `80` bits e o máximo é `4096`.

`col1 — col32`: Número de bits gerados para cada coluna de índice. O nome de cada parâmetro refere-se ao número da coluna de índice que ele controla. O padrão é `2` bits e o máximo é `4095`. Os parâmetros para colunas de índice que não são realmente usados são ignorados.

### F.6.2. Exemplos [#](#BLOOM-EXAMPLES)

Este é um exemplo de criação de um índice de floração:

```
CREATE INDEX bloomidx ON tbloom USING bloom (i1,i2,i3)
       WITH (length=80, col1=2, col2=2, col3=4);
```

O índice é criado com um comprimento de assinatura de 80 bits, com os atributos i1 e i2 mapeados para 2 bits e o atributo i3 mapeado para 4 bits. Podíamos ter omitido as especificações `length`, `col1` e `col2`, pois essas têm os valores padrão.

Aqui está um exemplo mais completo da definição e uso do índice bloom, bem como uma comparação com índices equivalente btree. O índice bloom é consideravelmente menor que o índice btree e pode apresentar melhor desempenho.

```
=# CREATE TABLE tbloom AS
   SELECT
     (random() * 1000000)::int as i1,
     (random() * 1000000)::int as i2,
     (random() * 1000000)::int as i3,
     (random() * 1000000)::int as i4,
     (random() * 1000000)::int as i5,
     (random() * 1000000)::int as i6
   FROM
  generate_series(1,10000000);
SELECT 10000000
```

Uma varredura sequencial sobre esta grande tabela leva muito tempo:

```
=# EXPLAIN ANALYZE SELECT * FROM tbloom WHERE i2 = 898732 AND i5 = 123451;
                                              QUERY PLAN
-------------------------------------------------------------------​-----------------------------------
 Seq Scan on tbloom  (cost=0.00..213744.00 rows=250 width=24) (actual time=357.059..357.059 rows=0.00 loops=1)
   Filter: ((i2 = 898732) AND (i5 = 123451))
   Rows Removed by Filter: 10000000
   Buffers: shared hit=63744
 Planning Time: 0.346 ms
 Execution Time: 357.076 ms
(6 rows)
```

Mesmo com o índice btree definido, o resultado ainda será uma varredura sequencial:

```
=# CREATE INDEX btreeidx ON tbloom (i1, i2, i3, i4, i5, i6);
CREATE INDEX
=# SELECT pg_size_pretty(pg_relation_size('btreeidx'));
 pg_size_pretty
----------------
 386 MB
(1 row)
=# EXPLAIN ANALYZE SELECT * FROM tbloom WHERE i2 = 898732 AND i5 = 123451;
                                              QUERY PLAN
-------------------------------------------------------------------​-----------------------------------
 Seq Scan on tbloom  (cost=0.00..213744.00 rows=2 width=24) (actual time=351.016..351.017 rows=0.00 loops=1)
   Filter: ((i2 = 898732) AND (i5 = 123451))
   Rows Removed by Filter: 10000000
   Buffers: shared hit=63744
 Planning Time: 0.138 ms
 Execution Time: 351.035 ms
(6 rows)
```

Ter o índice de floração definido na tabela é melhor do que o btree no manuseio desse tipo de pesquisa:

```
=# CREATE INDEX bloomidx ON tbloom USING bloom (i1, i2, i3, i4, i5, i6);
CREATE INDEX
=# SELECT pg_size_pretty(pg_relation_size('bloomidx'));
 pg_size_pretty
----------------
 153 MB
(1 row)
=# EXPLAIN ANALYZE SELECT * FROM tbloom WHERE i2 = 898732 AND i5 = 123451;
                                                     QUERY PLAN
-------------------------------------------------------------------​--------------------------------------------------
 Bitmap Heap Scan on tbloom  (cost=1792.00..1799.69 rows=2 width=24) (actual time=22.605..22.606 rows=0.00 loops=1)
   Recheck Cond: ((i2 = 898732) AND (i5 = 123451))
   Rows Removed by Index Recheck: 2300
   Heap Blocks: exact=2256
   Buffers: shared hit=21864
   ->  Bitmap Index Scan on bloomidx  (cost=0.00..178436.00 rows=1 width=0) (actual time=20.005..20.005 rows=2300.00 loops=1)
         Index Cond: ((i2 = 898732) AND (i5 = 123451))
         Index Searches: 1
         Buffers: shared hit=19608
 Planning Time: 0.099 ms
 Execution Time: 22.632 ms
(11 rows)
```

Agora, o principal problema com a pesquisa btree é que a btree é ineficiente quando as condições de pesquisa não restringem a(s) coluna(s) do índice principal. Uma estratégia melhor para a btree é criar um índice separado em cada coluna. Então, o planejador escolherá algo como este:

```
=# CREATE INDEX btreeidx1 ON tbloom (i1);
CREATE INDEX
=# CREATE INDEX btreeidx2 ON tbloom (i2);
CREATE INDEX
=# CREATE INDEX btreeidx3 ON tbloom (i3);
CREATE INDEX
=# CREATE INDEX btreeidx4 ON tbloom (i4);
CREATE INDEX
=# CREATE INDEX btreeidx5 ON tbloom (i5);
CREATE INDEX
=# CREATE INDEX btreeidx6 ON tbloom (i6);
CREATE INDEX
=# EXPLAIN ANALYZE SELECT * FROM tbloom WHERE i2 = 898732 AND i5 = 123451;
                                                        QUERY PLAN
-------------------------------------------------------------------​--------------------------------------------------------
 Bitmap Heap Scan on tbloom  (cost=9.29..13.30 rows=1 width=24) (actual time=0.032..0.033 rows=0.00 loops=1)
   Recheck Cond: ((i5 = 123451) AND (i2 = 898732))
   Buffers: shared read=6
   ->  BitmapAnd  (cost=9.29..9.29 rows=1 width=0) (actual time=0.047..0.047 rows=0.00 loops=1)
         Buffers: shared hit=6
         ->  Bitmap Index Scan on btreeidx5  (cost=0.00..4.52 rows=11 width=0) (actual time=0.026..0.026 rows=7.00 loops=1)
               Index Cond: (i5 = 123451)
               Index Searches: 1
               Buffers: shared hit=3
         ->  Bitmap Index Scan on btreeidx2  (cost=0.00..4.52 rows=11 width=0) (actual time=0.007..0.007 rows=8.00 loops=1)
               Index Cond: (i2 = 898732)
               Index Searches: 1
               Buffers: shared hit=3
 Planning Time: 0.264 ms
 Execution Time: 0.047 ms
(15 rows)
```

Embora essa consulta seja muito mais rápida do que com qualquer um dos índices únicos, pagamos uma penalidade no tamanho do índice. Cada um dos índices btree de uma única coluna ocupa 88,5 MB, então o espaço total necessário é de 531 MB, mais de três vezes o espaço usado pelo índice bloom.

### F.6.3. Interface da Classe Operadora [#](#BLOOM-OPERATOR-CLASS-INTERFACE)

Uma classe de operador para índices de flor requer apenas uma função hash para o tipo de dados indexado e um operador de igualdade para a pesquisa. Este exemplo mostra a definição da classe de operador para o tipo de dados `text`:

```
CREATE OPERATOR CLASS text_ops
DEFAULT FOR TYPE text USING bloom AS
    OPERATOR    1   =(text, text),
    FUNCTION    1   hashtext(text);
```

### F.6.4. Limitações [#](#BLOOM-LIMITATIONS)

* Apenas as classes de operador para `int4` e `text` estão incluídas no módulo.
* Apenas o operador `=` é suportado para pesquisa. Mas é possível adicionar suporte para matrizes com operações de união e interseção no futuro.
* O método de acesso `bloom` não suporta índices de `UNIQUE`.
* O método de acesso `bloom` não suporta a pesquisa de valores de `NULL`.

### F.6.5. Autores [#](#BLOOM-AUTHORS)

Teodor Sigaev `<teodor@postgrespro.ru>`, Postgres Professional, Moscou, Rússia

Alexander Korotkov `<a.korotkov@postgrespro.ru>`, Postgres Professional, Moscou, Rússia

Oleg Bartunov `<obartunov@postgrespro.ru>`, Postgres Professional, Moscou, Rússia