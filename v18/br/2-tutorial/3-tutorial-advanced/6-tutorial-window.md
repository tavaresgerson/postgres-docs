### 3.5. Funções de janela [#](#TUTORIAL-WINDOW)

Uma *função de janela* realiza um cálculo em um conjunto de linhas de tabela que estão de alguma forma relacionadas à linha atual. Isso é comparável ao tipo de cálculo que pode ser feito com uma função agregada. No entanto, as funções de janela não fazem com que as linhas sejam agrupadas em uma única linha de saída, como as chamadas agregadas não de janela faria. Em vez disso, as linhas retêm suas identidades separadas. Nos bastidores, a função de janela é capaz de acessar mais do que apenas a linha atual do resultado da consulta.

Aqui está um exemplo que mostra como comparar o salário de cada funcionário com o salário médio de seu departamento:

```
SELECT depname, empno, salary, avg(salary) OVER (PARTITION BY depname) FROM empsalary;
```

```
  depname  | empno | salary |          avg
-----------+-------+--------+-----------------------
 develop   |    11 |   5200 | 5020.0000000000000000
 develop   |     7 |   4200 | 5020.0000000000000000
 develop   |     9 |   4500 | 5020.0000000000000000
 develop   |     8 |   6000 | 5020.0000000000000000
 develop   |    10 |   5200 | 5020.0000000000000000
 personnel |     5 |   3500 | 3700.0000000000000000
 personnel |     2 |   3900 | 3700.0000000000000000
 sales     |     3 |   4800 | 4866.6666666666666667
 sales     |     1 |   5000 | 4866.6666666666666667
 sales     |     4 |   4800 | 4866.6666666666666667
(10 rows)
```

As três primeiras colunas de saída vêm diretamente da tabela `empsalary`, e há uma linha de saída para cada linha da tabela. A quarta coluna representa uma média tirada em todas as linhas da tabela que têm o mesmo valor `depname` que a linha atual. (Na verdade, essa é a mesma função que o agregado não-janela `avg`, mas a cláusula `OVER` faz com que ela seja tratada como uma função de janela e calculada em toda a estrutura da janela.)

Uma chamada de função de janela sempre contém uma cláusula `OVER` diretamente após o nome e o(s) argumento(s) da função de janela. É isso que a distingue sintaticamente de uma função normal ou de um agregado não de janela. A cláusula `OVER` determina exatamente como as linhas da consulta são divididas para processamento pela função de janela. A cláusula `PARTITION BY` dentro de `OVER` divide as linhas em grupos, ou partições, que compartilham os mesmos valores da(s) expressão(ões) `PARTITION BY`. Para cada linha, a função de janela é calculada em relação às linhas que caem na mesma partição que a linha atual.

Você também pode controlar a ordem em que as linhas são processadas por funções de janela usando `ORDER BY` dentro de `OVER`. (A janela `ORDER BY` nem precisa corresponder à ordem em que as linhas são exibidas.) Aqui está um exemplo:

```
SELECT depname, empno, salary,
       row_number() OVER (PARTITION BY depname ORDER BY salary DESC)
FROM empsalary;
```

```
  depname  | empno | salary | row_number
-----------+-------+--------+------------
 develop   |     8 |   6000 |          1
 develop   |    10 |   5200 |          2
 develop   |    11 |   5200 |          3
 develop   |     9 |   4500 |          4
 develop   |     7 |   4200 |          5
 personnel |     2 |   3900 |          1
 personnel |     5 |   3500 |          2
 sales     |     1 |   5000 |          1
 sales     |     4 |   4800 |          2
 sales     |     3 |   4800 |          3
(10 rows)
```

Como mostrado aqui, a função de janela `row_number` atribui números sequenciais às linhas dentro de cada partição, na ordem definida pela cláusula `ORDER BY` (com linhas vinculadas numeradas em uma ordem não especificada). `row_number` não precisa de um parâmetro explícito, porque seu comportamento é totalmente determinado pela cláusula `OVER`.

As linhas consideradas por uma função de janela são aquelas da “tabela virtual” produzida pela cláusula `FROM` da consulta, filtrada por suas cláusulas `WHERE`, `GROUP BY` e `HAVING`, se houver. Por exemplo, uma linha removida porque não atende à condição `WHERE` não é vista por nenhuma função de janela. Uma consulta pode conter múltiplas funções de janela que cortam os dados de maneiras diferentes, usando diferentes cláusulas `OVER`, mas todas elas atuam na mesma coleção de linhas definida por essa tabela virtual.

Já vimos que `ORDER BY` pode ser omitido se a ordem das linhas não for importante. Também é possível omitir `PARTITION BY`, nesse caso, há uma única partição contendo todas as linhas.

Existe outro conceito importante associado às funções de janela: para cada linha, há um conjunto de linhas dentro de sua partição chamado de *quadro de janela*. Algumas funções de janela atuam apenas nas linhas do quadro de janela, em vez de na totalidade da partição. Por padrão, se `ORDER BY` for fornecido, o quadro consiste em todas as linhas a partir do início da partição até a linha atual, além de quaisquer linhas subsequentes que sejam iguais à linha atual de acordo com a cláusula `ORDER BY`. Quando `ORDER BY` é omitido, o quadro padrão consiste em todas as linhas na partição. [[5]](#ftn.id-1.4.5.6.9.5) Aqui está um exemplo usando `sum`:

```
SELECT salary, sum(salary) OVER () FROM empsalary;
```

```
 salary |  sum
--------+-------
   5200 | 47100
   5000 | 47100
   3500 | 47100
   4800 | 47100
   3900 | 47100
   4200 | 47100
   4500 | 47100
   4800 | 47100
   6000 | 47100
   5200 | 47100
(10 rows)
```

Como não há `ORDER BY` na cláusula `OVER`, o quadro da janela é o mesmo que a partição, que, por falta de `PARTITION BY`, é toda a tabela; em outras palavras, cada soma é calculada sobre toda a tabela e, assim, obtemos o mesmo resultado para cada linha de saída. Mas se adicionarmos uma cláusula `ORDER BY`, obtemos resultados muito diferentes:

```
SELECT salary, sum(salary) OVER (ORDER BY salary) FROM empsalary;
```

```
 salary |  sum
--------+-------
   3500 |  3500
   3900 |  7400
   4200 | 11600
   4500 | 16100
   4800 | 25700
   4800 | 25700
   5000 | 30700
   5200 | 41100
   5200 | 41100
   6000 | 47100
(10 rows)
```

Aqui, a soma é tirada do primeiro (menor) salário até o atual, incluindo quaisquer duplicados do atual (observe os resultados para os salários duplicados).

As funções de janela são permitidas apenas na lista `SELECT` e na cláusula `ORDER BY` da consulta. Elas são proibidas em outros lugares, como nas cláusulas `GROUP BY`, `HAVING` e `WHERE`. Isso ocorre porque elas são executadas logicamente após o processamento dessas cláusulas. Além disso, as funções de janela são executadas após funções agregadas não de janela. Isso significa que é válido incluir uma chamada de função agregada nos argumentos de uma função de janela, mas não vice-versa.

Se houver a necessidade de filtrar ou agrupar linhas após os cálculos da janela serem realizados, você pode usar um subseleto. Por exemplo:

```
SELECT depname, empno, salary, enroll_date
FROM
  (SELECT depname, empno, salary, enroll_date,
     row_number() OVER (PARTITION BY depname ORDER BY salary DESC, empno) AS pos
     FROM empsalary
  ) AS ss
WHERE pos < 3;
```

A consulta acima mostra apenas as linhas da consulta interna com `row_number` menor que 3 (ou seja, as duas primeiras linhas para cada departamento).

Quando uma consulta envolve várias funções de janela, é possível escrever cada uma delas com uma cláusula `OVER` separada, mas isso é redundante e propenso a erros se o mesmo comportamento de janelação for desejado para várias funções. Em vez disso, cada comportamento de janelação pode ser nomeado em uma cláusula `WINDOW` e então referenciado em `OVER`. Por exemplo:

```
SELECT sum(salary) OVER w, avg(salary) OVER w
  FROM empsalary
  WINDOW w AS (PARTITION BY depname ORDER BY salary DESC);
```

Mais detalhes sobre as funções de janela podem ser encontrados em [Seção 4.2.8](sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS), [Seção 9.22](functions-window.md), [Seção 7.2.5](queries-table-expressions.md#QUERIES-WINDOW) e na página de referência [SELECT](sql-select.md).

---

[[5]](#id-1.4.5.6.9.5) Existem opções para definir o quadro da janela de outras maneiras, mas este tutorial não as abrange. Consulte [Seção 4.2.8](sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS) para obter detalhes.