## 39.3. Visões Materializadas [#](#RULES-MATERIALIZEDVIEWS)

As vistas materializadas no PostgreSQL utilizam o sistema de regras como as vistas, mas persistem os resultados em uma forma semelhante a uma tabela. As principais diferenças entre:

```
CREATE MATERIALIZED VIEW mymatview AS SELECT * FROM mytab;
```

e:

```
CREATE TABLE mymatview AS SELECT * FROM mytab;
```

é que a visão materializada não pode ser posteriormente atualizada diretamente e que a consulta usada para criar a visão materializada é armazenada exatamente da mesma maneira que a consulta de uma visão é armazenada, para que dados frescos possam ser gerados para a visão materializada com:

```
REFRESH MATERIALIZED VIEW mymatview;
```

As informações sobre uma visão materializada nos catálogos do sistema PostgreSQL são exatamente as mesmas que as de uma tabela ou visão. Portanto, para o analisador, uma visão materializada é uma relação, assim como uma tabela ou uma visão. Quando uma visão materializada é referenciada em uma consulta, os dados são retornados diretamente da visão materializada, como de uma tabela; a regra é usada apenas para preencher a visão materializada.

Embora o acesso aos dados armazenados em uma visão materializada seja frequentemente muito mais rápido do que o acesso às tabelas subjacentes diretamente ou através de uma visão, os dados nem sempre são atualizados; no entanto, às vezes, os dados atualizados não são necessários. Considere uma tabela que registra as vendas:

```
CREATE TABLE invoice (
    invoice_no    integer        PRIMARY KEY,
    seller_no     integer,       -- ID of salesperson
    invoice_date  date,          -- date of sale
    invoice_amt   numeric(13,2)  -- amount of sale
);
```

Se as pessoas quiserem poder gravar dados de vendas históricos rapidamente, elas podem querer resumir e talvez não se impor com os dados incompletos para a data atual:

```
CREATE MATERIALIZED VIEW sales_summary AS
  SELECT
      seller_no,
      invoice_date,
      sum(invoice_amt)::numeric(13,2) as sales_amt
    FROM invoice
    WHERE invoice_date < CURRENT_DATE
    GROUP BY
      seller_no,
      invoice_date;

CREATE UNIQUE INDEX sales_summary_seller
  ON sales_summary (seller_no, invoice_date);
```

Essa visão materializada pode ser útil para exibir um gráfico no painel criado para os vendedores. Um trabalho pode ser agendado para atualizar as estatísticas todas as noites usando essa declaração SQL:

```
REFRESH MATERIALIZED VIEW sales_summary;
```

Outro uso de uma visão materializada é permitir acesso mais rápido aos dados trazidos de um sistema remoto por meio de um revestimento de dados estrangeiro. Um exemplo simples usando `file_fdw` está abaixo, com tempos, mas, como este está usando cache no sistema local, a diferença de desempenho em comparação com o acesso a um sistema remoto geralmente seria maior do que o mostrado aqui. Observe que também estamos explorando a capacidade de colocar um índice na visão materializada, enquanto `file_fdw` não suporta índices; essa vantagem pode não se aplicar para outros tipos de acesso a dados estrangeiros.

Configuração:

```
CREATE EXTENSION file_fdw;
CREATE SERVER local_file FOREIGN DATA WRAPPER file_fdw;
CREATE FOREIGN TABLE words (word text NOT NULL)
  SERVER local_file
  OPTIONS (filename '/usr/share/dict/words');
CREATE MATERIALIZED VIEW wrd AS SELECT * FROM words;
CREATE UNIQUE INDEX wrd_word ON wrd (word);
CREATE EXTENSION pg_trgm;
CREATE INDEX wrd_trgm ON wrd USING gist (word gist_trgm_ops);
VACUUM ANALYZE wrd;
```

Agora, vamos verificar a ortografia de uma palavra. Usando diretamente `file_fdw`:

```
SELECT count(*) FROM words WHERE word = 'caterpiler';

 count
-------
     0
(1 row)
```

Com o `EXPLAIN ANALYZE`, vemos:

```
 Aggregate  (cost=21763.99..21764.00 rows=1 width=0) (actual time=188.180..188.181 rows=1.00 loops=1)
   ->  Foreign Scan on words  (cost=0.00..21761.41 rows=1032 width=0) (actual time=188.177..188.177 rows=0.00 loops=1)
         Filter: (word = 'caterpiler'::text)
         Rows Removed by Filter: 479829
         Foreign File: /usr/share/dict/words
         Foreign File Size: 4953699
 Planning time: 0.118 ms
 Execution time: 188.273 ms
```

Se a visão materializada for usada em vez disso, a consulta é muito mais rápida:

```
 Aggregate  (cost=4.44..4.45 rows=1 width=0) (actual time=0.042..0.042 rows=1.00 loops=1)
   ->  Index Only Scan using wrd_word on wrd  (cost=0.42..4.44 rows=1 width=0) (actual time=0.039..0.039 rows=0.00 loops=1)
         Index Cond: (word = 'caterpiler'::text)
         Heap Fetches: 0
         Index Searches: 1
 Planning time: 0.164 ms
 Execution time: 0.117 ms
```

De qualquer forma, a palavra está mal escrita, então vamos procurar o que talvez tenhamos querido. Novamente, usando `file_fdw` e `pg_trgm`:

```
SELECT word FROM words ORDER BY word <-> 'caterpiler' LIMIT 10;

     word
---------------
 cater
 caterpillar
 Caterpillar
 caterpillars
 caterpillar's
 Caterpillar's
 caterer
 caterer's
 caters
 catered
(10 rows)
```

```
 Limit  (cost=11583.61..11583.64 rows=10 width=32) (actual time=1431.591..1431.594 rows=10.00 loops=1)
   ->  Sort  (cost=11583.61..11804.76 rows=88459 width=32) (actual time=1431.589..1431.591 rows=10.00 loops=1)
         Sort Key: ((word <-> 'caterpiler'::text))
         Sort Method: top-N heapsort  Memory: 25kB
         ->  Foreign Scan on words  (cost=0.00..9672.05 rows=88459 width=32) (actual time=0.057..1286.455 rows=479829.00 loops=1)
               Foreign File: /usr/share/dict/words
               Foreign File Size: 4953699
 Planning time: 0.128 ms
 Execution time: 1431.679 ms
```

Usando a visão materializada:

```
 Limit  (cost=0.29..1.06 rows=10 width=10) (actual time=187.222..188.257 rows=10.00 loops=1)
   ->  Index Scan using wrd_trgm on wrd  (cost=0.29..37020.87 rows=479829 width=10) (actual time=187.219..188.252 rows=10.00 loops=1)
         Order By: (word <-> 'caterpiler'::text)
         Index Searches: 1
 Planning time: 0.196 ms
 Execution time: 198.640 ms
```

Se você puder tolerar a atualização periódica dos dados remotos para o banco de dados local, o benefício de desempenho pode ser substancial.