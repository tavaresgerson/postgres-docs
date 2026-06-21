## 9.26. Definir funções de retorno [#](#FUNCTIONS-SRF)

Esta seção descreve funções que possivelmente retornam mais de uma linha. As funções mais amplamente utilizadas nesta classe são as funções geradoras de séries, conforme detalhado em [Tabela 9.69][(functions-srf.md#FUNCTIONS-SRF-SERIES "Table 9.69. Series Generating Functions")] e [Tabela 9.70][(functions-srf.md#FUNCTIONS-SRF-SUBSCRIPTS "Table 9.70. Subscript Generating Functions")]. Outras funções mais especializadas que retornam conjuntos são descritas em outros lugares deste manual. Veja [Seção 7.2.1.4][(queries-table-expressions.md#QUERIES-TABLEFUNCTIONS "7.2.1.4. Table Functions")] para formas de combinar múltiplas funções que retornam conjuntos.

**Tabela 9.69. Funções geradoras de série**



<table border="1" class="table" summary="Series Generating Functions">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="func_table_entry">
<p class="func_signature">Função</p>
<p>Descrição</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      generate_series
     </code>(<em class="parameter">
<code>
       start
      </code>
</em>
<code class="type">
      integer
     </code>,<em class="parameter">
<code>
       stop
      </code>
</em>
<code class="type">
      integer
     </code>[<span class="optional">,<em class="parameter">
<code>
        step
       </code>
</em>
<code class="type">
       integer
      </code>
</span>] )<code class="returnvalue">
      setof integer
     </code>
</p>
<p class="func_signature">
<code class="function">
      generate_series
     </code>(<em class="parameter">
<code>
       start
      </code>
</em>
<code class="type">
      bigint
     </code>,<em class="parameter">
<code>
       stop
      </code>
</em>
<code class="type">
      bigint
     </code>[<span class="optional">,<em class="parameter">
<code>
        step
       </code>
</em>
<code class="type">
       bigint
      </code>
</span>] )<code class="returnvalue">
      setof bigint
     </code>
</p>
<p class="func_signature">
<code class="function">
      generate_series
     </code>(<em class="parameter">
<code>
       start
      </code>
</em>
<code class="type">
      numeric
     </code>,<em class="parameter">
<code>
       stop
      </code>
</em>
<code class="type">
      numeric
     </code>[<span class="optional">,<em class="parameter">
<code>
        step
       </code>
</em>
<code class="type">
       numeric
      </code>
</span>] )<code class="returnvalue">
      setof numeric
     </code>
</p>
<p>Gera uma série de valores a partir de<em class="parameter">
<code>
       start
      </code>
</em>para<em class="parameter">
<code>
       stop
      </code>
</em>, com um tamanho de passo de<em class="parameter">
<code>
       step
      </code>
</em>
     .
     <em class="parameter">
<code>
       step
      </code>
</em>o padrão é 1.</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      generate_series
     </code>(<em class="parameter">
<code>
       start
      </code>
</em>
<code class="type">
      timestamp
     </code>,<em class="parameter">
<code>
       stop
      </code>
</em>
<code class="type">
      timestamp
     </code>,<em class="parameter">
<code>
       step
      </code>
</em>
<code class="type">
      interval
     </code>)<code class="returnvalue">
      setof timestamp
     </code>
</p>
<p class="func_signature">
<code class="function">
      generate_series
     </code>(<em class="parameter">
<code>
       start
      </code>
</em>
<code class="type">
      timestamp with time zone
     </code>,<em class="parameter">
<code>
       stop
      </code>
</em>
<code class="type">
      timestamp with time zone
     </code>,<em class="parameter">
<code>
       step
      </code>
</em>
<code class="type">
      interval
     </code>[<span class="optional">,<em class="parameter">
<code>
        timezone
       </code>
</em>
<code class="type">
       text
      </code>
</span>] )<code class="returnvalue">
      setof timestamp with time zone
     </code>
</p>
<p>Gera uma série de valores a partir de<em class="parameter">
<code>
       start
      </code>
</em>para<em class="parameter">
<code>
       stop
      </code>
</em>, com um tamanho de passo de<em class="parameter">
<code>
       step
      </code>
</em>. No formulário que considera a fusão horária, os horários do dia e os ajustes de horário de verão são calculados de acordo com a fusão horária indicada pelo<em class="parameter">
<code>
       timezone
      </code>
</em>argumento, ou o atual<a class="xref" href="runtime-config-client.md#GUC-TIMEZONE">Fuso Horário</a>especificações, se este for omitido.</p>
</td>
</tr>
</tbody>
</table>




  

Quando *`step`* é positivo, zero linhas são retornadas se *`start`* for maior que *`stop`*. Por outro lado, quando *`step`* é negativo, zero linhas são retornadas se *`start`* for menor que *`stop`*. Zero linhas também são retornadas se qualquer entrada for `NULL`. É um erro para *`step`* ser zero. Alguns exemplos seguem:

```
SELECT * FROM generate_series(2,4);
 generate_series
-----------------
               2
               3
               4
(3 rows)

SELECT * FROM generate_series(5,1,-2);
 generate_series
-----------------
               5
               3
               1
(3 rows)

SELECT * FROM generate_series(4,3);
 generate_series
-----------------
(0 rows)

SELECT generate_series(1.1, 4, 1.3);
 generate_series
-----------------
             1.1
             2.4
             3.7
(3 rows)

-- this example relies on the date-plus-integer operator:
SELECT current_date + s.a AS dates FROM generate_series(0,14,7) AS s(a);
   dates
------------
 2004-02-05
 2004-02-12
 2004-02-19
(3 rows)

SELECT * FROM generate_series('2008-03-01 00:00'::timestamp,
                              '2008-03-04 12:00', '10 hours');
   generate_series
---------------------
 2008-03-01 00:00:00
 2008-03-01 10:00:00
 2008-03-01 20:00:00
 2008-03-02 06:00:00
 2008-03-02 16:00:00
 2008-03-03 02:00:00
 2008-03-03 12:00:00
 2008-03-03 22:00:00
 2008-03-04 08:00:00
(9 rows)

-- this example assumes that TimeZone is set to UTC; note the DST transition:
SELECT * FROM generate_series('2001-10-22 00:00 -04:00'::timestamptz,
                              '2001-11-01 00:00 -05:00'::timestamptz,
                              '1 day'::interval, 'America/New_York');
    generate_series
------------------------
 2001-10-22 04:00:00+00
 2001-10-23 04:00:00+00
 2001-10-24 04:00:00+00
 2001-10-25 04:00:00+00
 2001-10-26 04:00:00+00
 2001-10-27 04:00:00+00
 2001-10-28 04:00:00+00
 2001-10-29 05:00:00+00
 2001-10-30 05:00:00+00
 2001-10-31 05:00:00+00
 2001-11-01 05:00:00+00
(11 rows)
```

**Tabela 9.70. Funções geradoras de subscrito**



<table border="1" class="table" summary="Subscript Generating Functions">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="func_table_entry">
<p class="func_signature">Função</p>
<p>Descrição</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      generate_subscripts
     </code>(<em class="parameter">
<code>
       array
      </code>
</em>
<code class="type">
      anyarray
     </code>,<em class="parameter">
<code>
       dim
      </code>
</em>
<code class="type">
      integer
     </code>)<code class="returnvalue">
      setof integer
     </code>
</p>
<p>Gera uma série que compreende os subíndices válidos do<em class="parameter">
<code>
       dim
      </code>
</em>'a dimensão da matriz fornecida.</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      generate_subscripts
     </code>(<em class="parameter">
<code>
       array
      </code>
</em>
<code class="type">
      anyarray
     </code>,<em class="parameter">
<code>
       dim
      </code>
</em>
<code class="type">
      integer
     </code>,<em class="parameter">
<code>
       reverse
      </code>
</em>
<code class="type">
      boolean
     </code>)<code class="returnvalue">
      setof integer
     </code>
</p>
<p>Gera uma série que compreende os subíndices válidos do<em class="parameter">
<code>
       dim
      </code>
</em>'a dimensão da matriz fornecida. Quando<em class="parameter">
<code>
       reverse
      </code>
</em>Se é verdade, retorna a série em ordem inversa.</p>
</td>
</tr>
</tbody>
</table>




  

`generate_subscripts` é uma função de conveniência que gera o conjunto de subíndices válidos para a dimensão especificada da matriz fornecida. São retornadas zero linhas para matrizes que não possuem a dimensão solicitada, ou se qualquer entrada for `NULL`. Alguns exemplos seguem:

```
-- basic usage:
SELECT generate_subscripts('{NULL,1,NULL,2}'::int[], 1) AS s;
 s
---
 1
 2
 3
 4
(4 rows)

-- presenting an array, the subscript and the subscripted
-- value requires a subquery:
SELECT * FROM arrays;
         a
--------------------
 {-1,-2}
 {100,200,300}
(2 rows)

SELECT a AS array, s AS subscript, a[s] AS value
FROM (SELECT generate_subscripts(a, 1) AS s, a FROM arrays) foo;
     array     | subscript | value
---------------+-----------+-------
 {-1,-2}       |         1 |    -1
 {-1,-2}       |         2 |    -2
 {100,200,300} |         1 |   100
 {100,200,300} |         2 |   200
 {100,200,300} |         3 |   300
(5 rows)

-- unnest a 2D array:
CREATE OR REPLACE FUNCTION unnest2(anyarray)
RETURNS SETOF anyelement AS $$
select $1[i][j]
   from generate_subscripts($1,1) g1(i),
        generate_subscripts($1,2) g2(j);
$$ LANGUAGE sql IMMUTABLE;
CREATE FUNCTION
SELECT * FROM unnest2(ARRAY[[1,2],[3,4]]);
 unnest2
---------
       1
       2
       3
       4
(4 rows)
```

Quando uma função na cláusula `FROM` é sufixada por `WITH ORDINALITY`, uma coluna `bigint` é anexada à(s) coluna(s) de saída da função, que começa em 1 e incrementa em 1 para cada linha da(s) coluna(s) de saída da função. Isso é mais útil no caso de funções de conjunto que retornam, como `unnest()`.

```
-- set returning function WITH ORDINALITY:
SELECT * FROM pg_ls_dir('.') WITH ORDINALITY AS t(ls,n);
       ls        | n
-----------------+----
 pg_serial       |  1
 pg_twophase     |  2
 postmaster.opts |  3
 pg_notify       |  4
 postgresql.conf |  5
 pg_tblspc       |  6
 logfile         |  7
 base            |  8
 postmaster.pid  |  9
 pg_ident.conf   | 10
 global          | 11
 pg_xact         | 12
 pg_snapshots    | 13
 pg_multixact    | 14
 PG_VERSION      | 15
 pg_wal          | 16
 pg_hba.conf     | 17
 pg_stat_tmp     | 18
 pg_subtrans     | 19
(19 rows)
```
