## 14.2. Estatísticas utilizadas pelo planejador [#](#PLANNER-STATS)

* [14.2.1. Estatísticas de uma coluna única](planner-stats.md#PLANNER-STATS-SINGLE-COLUMN)
* [14.2.2. Estatísticas extensas](planner-stats.md#PLANNER-STATS-EXTENDED)

### 14.2.1. Estatísticas de uma coluna única [#](#PLANNER-STATS-SINGLE-COLUMN)

Como vimos na seção anterior, o planejador de consultas precisa estimar o número de linhas recuperadas por uma consulta para fazer escolhas adequadas de planos de consulta. Esta seção fornece uma visão rápida das estatísticas que o sistema usa para essas estimativas.

Um componente das estatísticas é o número total de entradas em cada tabela e índice, bem como o número de blocos de disco ocupados por cada tabela e índice. Essas informações são mantidas na tabela `pg_class`(catalog-pg-class.md "52.11. pg_class"), nas colunas `reltuples` e `relpages`. Podemos analisá-las com consultas semelhantes a esta:

```
SELECT relname, relkind, reltuples, relpages
FROM pg_class
WHERE relname LIKE 'tenk1%';

       relname        | relkind | reltuples | relpages
----------------------+---------+-----------+----------
 tenk1                | r       |     10000 |      345
 tenk1_hundred        | i       |     10000 |       11
 tenk1_thous_tenthous | i       |     10000 |       30
 tenk1_unique1        | i       |     10000 |       30
 tenk1_unique2        | i       |     10000 |       30
(5 rows)
```

Aqui podemos ver que `tenk1` contém 10.000 linhas, assim como seus índices, mas os índices (sem surpresa) são muito menores que a tabela.

Por razões de eficiência, `reltuples` e `relpages` não são atualizados em tempo real, e, portanto, geralmente contêm valores um pouco desatualizados. Eles são atualizados por `VACUUM`, `ANALYZE` e alguns comandos DDL, como `CREATE INDEX`. Uma operação de `VACUUM` ou `ANALYZE` que não escaneia toda a tabela (o que é comumente o caso) atualizará incrementalmente o `reltuples` com base na parte da tabela que ela escaneou, resultando em um valor aproximado. Em qualquer caso, o planejador escalará os valores encontrados em `pg_class` para corresponder ao tamanho atual da tabela física, obtendo assim uma aproximação mais próxima.

A maioria das consultas recupera apenas uma fração das linhas em uma tabela, devido às cláusulas `WHERE` que restringem as linhas a serem examinadas. O planejador, portanto, precisa fazer uma estimativa da *seletividade* das cláusulas `WHERE`, ou seja, a fração de linhas que correspondem a cada condição na cláusula `WHERE`. As informações usadas para essa tarefa são armazenadas no catálogo do sistema [[`pg_statistic`](catalog-pg-statistic.md). As entradas em `pg_statistic` são atualizadas pelos comandos `ANALYZE` e `VACUUM ANALYZE`, e são sempre aproximadas, mesmo quando recém-atualizadas.

Em vez de olhar diretamente para `pg_statistic`, é melhor olhar para sua visão `pg_stats`(view-pg-stats.md "53.29. pg_stats") ao examinar as estatísticas manualmente. `pg_stats` é projetado para ser mais facilmente legível. Além disso, `pg_stats` é legível por todos, enquanto `pg_statistic` é legível apenas por um superusuário. (Isso impede que usuários não privilegiados aprendam algo sobre o conteúdo das tabelas de outras pessoas a partir das estatísticas. A visão `pg_stats` é restrita para mostrar apenas linhas sobre tabelas que o usuário atual pode ler.) Por exemplo, podemos fazer:

```
SELECT attname, inherited, n_distinct,
       array_to_string(most_common_vals, E'\n') as most_common_vals
FROM pg_stats
WHERE tablename = 'road';

 attname | inherited | n_distinct |          most_common_vals
---------+-----------+------------+------------------------------------
 name    | f         | -0.5681108 | I- 580                        Ramp+
         |           |            | I- 880                        Ramp+
         |           |            | Sp Railroad                       +
         |           |            | I- 580                            +
         |           |            | I- 680                        Ramp+
         |           |            | I- 80                         Ramp+
         |           |            | 14th                          St  +
         |           |            | I- 880                            +
         |           |            | Mac Arthur                    Blvd+
         |           |            | Mission                       Blvd+
...
 name    | t         |    -0.5125 | I- 580                        Ramp+
         |           |            | I- 880                        Ramp+
         |           |            | I- 580                            +
         |           |            | I- 680                        Ramp+
         |           |            | I- 80                         Ramp+
         |           |            | Sp Railroad                       +
         |           |            | I- 880                            +
         |           |            | State Hwy 13                  Ramp+
         |           |            | I- 80                             +
         |           |            | State Hwy 24                  Ramp+
...
 thepath | f         |          0 |
 thepath | t         |          0 |
(4 rows)
```

Observe que duas linhas são exibidas para a mesma coluna, uma correspondendo à hierarquia completa de herança que começa na tabela `road` (`inherited`=`t`) e outra que inclui apenas a própria tabela `road` (`inherited`=`f`). (Por brevidade, mostramos apenas os primeiros dez valores mais comuns para a coluna `name`.)

A quantidade de informações armazenada em `pg_statistic` por `ANALYZE`, em particular o número máximo de entradas nos arrays `most_common_vals` e `histogram_bounds` para cada coluna, pode ser definida de forma individual para cada coluna usando o comando `ALTER TABLE SET STATISTICS`, ou globalmente definindo a variável de configuração [default_statistics_target](runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET). O limite padrão é atualmente de 100 entradas. Aumentar o limite pode permitir estimativas de planejador mais precisas, particularmente para colunas com distribuições de dados irregulares, ao preço de consumir mais espaço em `pg_statistic` e um tempo ligeiramente maior para calcular as estimativas. Por outro lado, um limite mais baixo pode ser suficiente para colunas com distribuições de dados simples.

Mais detalhes sobre o uso de estatísticas pelo planejador podem ser encontrados em [Capítulo 69](planner-stats-details.md).

### 14.2.2. Estatísticas estendidas [#](#PLANNER-STATS-EXTENDED)

É comum ver consultas lentas executando planos de execução ruins porque várias colunas usadas nas cláusulas da consulta estão correlacionadas. O planejador normalmente assume que várias condições são independentes uma da outra, uma suposição que não se aplica quando os valores das colunas estão correlacionadas. Estatísticas regulares, devido à sua natureza por coluna individual, não podem capturar qualquer conhecimento sobre correlação entre colunas. No entanto, o PostgreSQL tem a capacidade de calcular *estatísticas multivariadas*, que podem capturar tais informações.

Como o número de combinações possíveis de colunas é muito grande, é impraticável calcular estatísticas multivariadas automaticamente. Em vez disso, *objetos de estatísticas estendidos*, mais frequentemente chamados apenas de *objetos de estatísticas*, podem ser criados para instruir o servidor a obter estatísticas em conjuntos de colunas interessantes.

Os objetos de estatísticas são criados usando o comando `CREATE STATISTICS`(sql-createstatistics.md "CREATE STATISTICS"). A criação de tal objeto simplesmente cria uma entrada de catálogo que expressa interesse nas estatísticas. A coleta de dados reais é realizada pelo `ANALYZE` (ou um comando manual, ou auto-análise de fundo). Os valores coletados podem ser examinados no catálogo `pg_statistic_ext_data`(catalog-pg-statistic-ext-data.md "52.53. pg_statistic_ext_data").

`ANALYZE` calcula estatísticas estendidas com base na mesma amostra de linhas da tabela que é utilizada para calcular estatísticas regulares de um único campo. Como o tamanho da amostra é aumentado ao aumentar o objetivo de estatísticas para a tabela ou qualquer uma de suas colunas (como descrito na seção anterior), um objetivo de estatísticas maior normalmente resulta em estatísticas estendidas mais precisas, bem como em mais tempo gasto calculando-as.

Os subtítulos a seguir descrevem os tipos de estatísticas extensas que são atualmente suportados.

#### 14.2.2.1. Dependências Funcionais [#](#PLANNER-STATS-EXTENDED-FUNCTIONAL-DEPS)

O tipo mais simples de estatísticas estendidas rastreia *dependências funcionais*, um conceito usado nas definições dos formatos de normalização de banco de dados. Dizemos que a coluna `b` é funcionalmente dependente da coluna `a` se o conhecimento do valor de `a` for suficiente para determinar o valor de `b`, ou seja, não há duas linhas com o mesmo valor de `a`, mas valores diferentes de `b`. Em um banco de dados totalmente normalizado, as dependências funcionais devem existir apenas em chaves primárias e super-chave. No entanto, na prática, muitos conjuntos de dados não são totalmente normalizados por várias razões; a denormalização intencional por razões de desempenho é um exemplo comum. Mesmo em um banco de dados totalmente normalizado, pode haver correlação parcial entre algumas colunas, que pode ser expressa como dependência funcional parcial.

A existência de dependências funcionais afeta diretamente a precisão das estimativas em certas consultas. Se uma consulta contiver condições em colunas independentes e dependentes, as condições nas colunas dependentes não reduzem ainda mais o tamanho do resultado; mas, sem conhecimento da dependência funcional, o planejador de consultas assumirá que as condições são independentes, resultando em subestimação do tamanho do resultado.

Para informar o planejador sobre as dependências funcionais, `ANALYZE` pode coletar medidas de dependência entre colunas cruzadas. A avaliação do grau de dependência entre todos os conjuntos de colunas seria proibitivamente cara, então a coleta de dados é limitada aos grupos de colunas que aparecem juntas em um objeto estatístico definido com a opção `dependencies`. É aconselhável criar estatísticas `dependencies` apenas para grupos de colunas que estão fortemente correlacionados, para evitar sobrecarga desnecessária tanto em `ANALYZE` quanto no planejamento de consultas posteriores.

Aqui está um exemplo de coleta de estatísticas de dependência funcional:

```
CREATE STATISTICS stts (dependencies) ON city, zip FROM zipcodes;

ANALYZE zipcodes;

SELECT stxname, stxkeys, stxddependencies
  FROM pg_statistic_ext join pg_statistic_ext_data on (oid = stxoid)
  WHERE stxname = 'stts';
 stxname | stxkeys |             stxddependencies
---------+---------+------------------------------------------
 stts    | 1 5     | {"1 => 5": 1.000000, "5 => 1": 0.423130}
(1 row)
```

Aqui pode ser visto que a coluna 1 (código postal) determina totalmente a coluna 5 (cidade), portanto o coeficiente é de 1,0, enquanto a cidade determina o código postal apenas em cerca de 42% dos casos, o que significa que há muitas cidades (58%) que são representadas por mais de um código postal.

Ao calcular a seletividade para uma consulta que envolve colunas funcionalmente dependentes, o planejador ajusta as estimativas de seletividade por condição usando os coeficientes de dependência para não produzir uma subestimação.

##### 14.2.2.1.1. Limitações das Dependências Funcionais [#](#PLANNER-STATS-EXTENDED-FUNCTIONAL-DEPS-LIMITS)

As dependências funcionais são atualmente aplicadas apenas quando se consideram condições de igualdade simples que comparam colunas a valores constantes, e cláusulas `IN` com valores constantes. Elas não são usadas para melhorar as estimativas para condições de igualdade que comparam duas colunas ou comparam uma coluna a uma expressão, nem para cláusulas de intervalo, `LIKE` ou qualquer outro tipo de condição.

Ao estimar com dependências funcionais, o planejador assume que as condições nas colunas envolvidas são compatíveis e, portanto, redundantes. Se forem incompatíveis, a estimativa correta seria zero linhas, mas essa possibilidade não é considerada. Por exemplo, dado uma consulta como

```
SELECT * FROM zipcodes WHERE city = 'San Francisco' AND zip = '94105';
```

o planejador ignorará a cláusula `city`, pois não altera a seletividade, o que é correto. No entanto, ele fará a mesma suposição sobre

```
SELECT * FROM zipcodes WHERE city = 'San Francisco' AND zip = '90210';
```

embora realmente não haverá zero linhas que satisfaçam essa consulta. As estatísticas de dependência funcional não fornecem informações suficientes para concluir isso, no entanto.

Em muitas situações práticas, essa suposição geralmente é satisfeita; por exemplo, pode haver uma GUI na aplicação que permite apenas selecionar valores de cidade e código postal compatíveis para serem usados em uma consulta. Mas se esse não for o caso, as dependências funcionais podem não ser uma opção viável.

#### 14.2.2.2. Contagem N-distinta multivariada [#](#PLANNER-STATS-EXTENDED-N-DISTINCT-COUNTS)

As estatísticas de coluna única armazenam o número de valores distintos em cada coluna. As estimativas do número de valores distintos ao combinar mais de uma coluna (por exemplo, para `GROUP BY a, b`) são frequentemente erradas quando o planejador tem apenas dados estatísticos de coluna única, fazendo com que ele selecione planos ruins.

Para melhorar tais estimativas, o `ANALYZE` pode coletar estatísticas n-distintas para grupos de colunas. Como antes, é impraticável fazer isso para cada possível agrupamento de colunas, então os dados são coletados apenas para aqueles grupos de colunas que aparecem juntos em um objeto de estatísticas definido com a opção `ndistinct`. Os dados serão coletados para cada combinação possível de duas ou mais colunas do conjunto de colunas listadas.

Continuando o exemplo anterior, as contagens n-distintas em uma tabela de códigos postais podem parecer as seguintes:

```
CREATE STATISTICS stts2 (ndistinct) ON city, state, zip FROM zipcodes;

ANALYZE zipcodes;

SELECT stxkeys AS k, stxdndistinct AS nd
  FROM pg_statistic_ext join pg_statistic_ext_data on (oid = stxoid)
  WHERE stxname = 'stts2';
-[ RECORD 1 ]------------------------------------------------------​--
k  | 1 2 5
nd | {"1, 2": 33178, "1, 5": 33178, "2, 5": 27435, "1, 2, 5": 33178}
(1 row)
```

Isso indica que há três combinações de colunas que têm 33178 valores distintos: código postal e estado; código postal e cidade; e código postal, cidade e estado (o fato de que todas elas são iguais é esperado, dado que o código postal sozinho é único nesta tabela). Por outro lado, a combinação de cidade e estado tem apenas 27435 valores distintos.

É aconselhável criar objetos de estatísticas `ndistinct` apenas em combinações de colunas que são realmente usadas para agrupamento, e para as quais a subestimação do número de grupos está resultando em planos ruins. Caso contrário, os ciclos `ANALYZE` são simplesmente desperdiçados.

#### 14.2.2.3. Listas de MCV multivariadas [#](#PLANNER-STATS-EXTENDED-MCV-LISTS)

Outro tipo de estatística armazenada para cada coluna são as listas de valores mais comuns. Isso permite estimativas muito precisas para colunas individuais, mas pode resultar em erros significativos nas consultas com condições em várias colunas.

Para melhorar tais estimativas, o `ANALYZE` pode coletar listas de MCV em combinações de colunas. Da mesma forma que as dependências funcionais e os coeficientes n-distintos, é impraticável fazer isso para cada agrupamento de colunas possível. Ainda mais nesse caso, pois a lista de MCV (ao contrário das dependências funcionais e dos coeficientes n-distintos) armazena os valores comuns das colunas. Portanto, os dados são coletados apenas para aqueles grupos de colunas que aparecem juntos em um objeto estatístico definido com a opção `mcv`.

Continuando o exemplo anterior, a lista MCV para uma tabela de códigos ZIP pode parecer a seguinte (ao contrário de tipos mais simples de estatísticas, é necessária uma função para a inspeção do conteúdo MCV):

```
CREATE STATISTICS stts3 (mcv) ON city, state FROM zipcodes;

ANALYZE zipcodes;

SELECT m.* FROM pg_statistic_ext join pg_statistic_ext_data on (oid = stxoid),
                pg_mcv_list_items(stxdmcv) m WHERE stxname = 'stts3';

 index |         values         | nulls | frequency | base_frequency
-------+------------------------+-------+-----------+----------------
     0 | {Washington, DC}       | {f,f} |  0.003467 |        2.7e-05
     1 | {Apo, AE}              | {f,f} |  0.003067 |        1.9e-05
     2 | {Houston, TX}          | {f,f} |  0.002167 |       0.000133
     3 | {El Paso, TX}          | {f,f} |     0.002 |       0.000113
     4 | {New York, NY}         | {f,f} |  0.001967 |       0.000114
     5 | {Atlanta, GA}          | {f,f} |  0.001633 |        3.3e-05
     6 | {Sacramento, CA}       | {f,f} |  0.001433 |        7.8e-05
     7 | {Miami, FL}            | {f,f} |    0.0014 |          6e-05
     8 | {Dallas, TX}           | {f,f} |  0.001367 |        8.8e-05
     9 | {Chicago, IL}          | {f,f} |  0.001333 |        5.1e-05
   ...
(99 rows)
```

Isso indica que a combinação mais comum de cidade e estado é Washington, com frequência real (na amostra) de cerca de 0,35%. A frequência base da combinação (calculada a partir das frequências simples por coluna) é de apenas 0,0027%, resultando em subestimações de dois ordens de magnitude.

É aconselhável criar objetos de estatísticas de MCV apenas em combinações de colunas que são realmente usadas em condições juntas, e para as quais a subestimação do número de grupos está resultando em planos ruins. Caso contrário, o `ANALYZE` e os ciclos de planejamento serão apenas desperdiçados.