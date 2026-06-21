## CRIAR ESTATÍSTICAS

CREATE STATISTICS — defina estatísticas extensas

## Sinopse

```
CREATE STATISTICS [ [ IF NOT EXISTS ] statistics_name ]
    ON ( expression )
    FROM table_name

CREATE STATISTICS [ [ IF NOT EXISTS ] statistics_name ]
    [ ( statistics_kind [, ... ] ) ]
    ON { column_name | ( expression ) }, { column_name | ( expression ) } [, ...]
    FROM table_name
```

## Descrição

`CREATE STATISTICS` criará um novo objeto de estatísticas estendido que rastreará dados sobre a tabela especificada, a tabela externa ou a visão materializada. O objeto de estatísticas será criado no banco de dados atual e será de propriedade do usuário que emite o comando.

O comando `CREATE STATISTICS` tem duas formas básicas. A primeira forma permite a coleta de estatísticas univariáveis para uma única expressão, proporcionando benefícios semelhantes a um índice de expressão sem o overhead da manutenção do índice. Esta forma não permite que o tipo de estatísticas seja especificado, uma vez que os vários tipos de estatísticas se referem apenas a estatísticas multivariáveis. A segunda forma do comando permite a coleta de estatísticas multivariáveis em várias colunas e/ou expressões, especificando opcionalmente quais tipos de estatísticas devem ser incluídos. Esta forma também causará automaticamente a coleta de estatísticas univariáveis em quaisquer expressões incluídas na lista.

Se um nome de esquema for fornecido (por exemplo, `CREATE STATISTICS myschema.mystat ...`) então o objeto de estatísticas é criado no esquema especificado. Caso contrário, ele é criado no esquema atual. Se fornecido, o nome do objeto de estatísticas deve ser distinto do nome de qualquer outro objeto de estatísticas no mesmo esquema.

## Parâmetros

`IF NOT EXISTS`: Não exija um erro se um objeto de estatísticas com o mesmo nome já existir. Neste caso, é emitido um aviso. Observe que apenas o nome do objeto de estatísticas é considerado aqui, não os detalhes de sua definição. O nome do estatística é necessário quando `IF NOT EXISTS` é especificado.

*`statistics_name`*: O nome (opcionalmente qualificado por esquema) do objeto de estatísticas a ser criado. Se o nome for omitido, o PostgreSQL escolhe um nome adequado com base no nome da tabela pai e no(s) nome(s) de coluna(s) e/ou expressão(s) definidos.

*`statistics_kind`*: Um tipo de estatística multivariada a ser computada neste objeto estatístico. Os tipos atualmente suportados são `ndistinct`, que permite estatísticas n-distintas, `dependencies`, que permite estatísticas de dependência funcional, e `mcv`, que permite listas de valores mais comuns. Se esta cláusula for omitida, todos os tipos de estatísticas suportados são incluídos no objeto estatístico. As estatísticas de expressão univariada são construídas automaticamente se a definição estatística incluir expressões complexas, em vez de apenas referências simples de colunas. Para mais informações, consulte [Seção 14.2.2](planner-stats.md#PLANNER-STATS-EXTENDED) e [Seção 69.2](multivariate-statistics-examples.md).

*`column_name`*: O nome de uma coluna de tabela que será coberta pelas estatísticas calculadas. Isso só é permitido ao construir estatísticas multivariadas. Pelo menos dois nomes de coluna ou expressões devem ser especificados, e seu ordem não é significativa.

*`expression`*: Uma expressão que será coberta pelas estatísticas calculadas. Isso pode ser usado para construir estatísticas univariáveis em uma única expressão, ou como parte de uma lista de múltiplos nomes de colunas e/ou expressões para construir estatísticas multivariáveis. No último caso, estatísticas univariáveis separadas são construídas automaticamente para cada expressão na lista.

*`table_name`*: O nome (opcionalmente qualificado por esquema) da tabela que contém a(s) coluna(s) sobre a qual as estatísticas são calculadas; consulte [ANALYZE](sql-analyze.md "ANALYZE") para uma explicação sobre o tratamento de herança e partições.

## Notas

Você deve ser o proprietário de uma tabela para criar um objeto de estatísticas lendo-a. No entanto, uma vez criado, a propriedade do objeto de estatísticas é independente da(s) tabela(s) subjacente(s).

As estatísticas de expressão são por expressão e são semelhantes à criação de um índice na expressão, exceto que elas evitam o custo de manutenção do índice. As estatísticas de expressão são construídas automaticamente para cada expressão na definição do objeto de estatísticas.

Estatísticas estendidas atualmente não são utilizadas pelo planejador para estimativas de seletividade feitas para junções de tabela. Essa limitação provavelmente será removida em uma versão futura do PostgreSQL.

## Exemplos

Crie a tabela `t1` com duas colunas funcionalmente dependentes, ou seja, o conhecimento de um valor na primeira coluna é suficiente para determinar o valor na outra coluna. Em seguida, as estatísticas de dependência funcional são construídas nessas colunas:

```
CREATE TABLE t1 (
    a   int,
    b   int
);

INSERT INTO t1 SELECT i/100, i/500
                 FROM generate_series(1,1000000) s(i);

ANALYZE t1;

-- the number of matching rows will be drastically underestimated:
EXPLAIN ANALYZE SELECT * FROM t1 WHERE (a = 1) AND (b = 0);

CREATE STATISTICS s1 (dependencies) ON a, b FROM t1;

ANALYZE t1;

-- now the row count estimate is more accurate:
EXPLAIN ANALYZE SELECT * FROM t1 WHERE (a = 1) AND (b = 0);
```

Sem estatísticas de dependência funcional, o planejador assumirá que as duas condições `WHERE` são independentes e multiplicará suas seletividades para chegar a uma estimativa de contagem de linhas muito pequena. Com tais estatísticas, o planejador reconhece que as condições `WHERE` são redundantes e não subestima a contagem de linhas.

Crie a tabela `t2` com duas colunas perfeitamente correlacionadas (contendo dados idênticos) e uma lista de MCV nessas colunas:

```
CREATE TABLE t2 (
    a   int,
    b   int
);

INSERT INTO t2 SELECT mod(i,100), mod(i,100)
                 FROM generate_series(1,1000000) s(i);

CREATE STATISTICS s2 (mcv) ON a, b FROM t2;

ANALYZE t2;

-- valid combination (found in MCV)
EXPLAIN ANALYZE SELECT * FROM t2 WHERE (a = 1) AND (b = 1);

-- invalid combination (not found in MCV)
EXPLAIN ANALYZE SELECT * FROM t2 WHERE (a = 1) AND (b = 2);
```

A lista MCV fornece ao planejador informações mais detalhadas sobre os valores específicos que normalmente aparecem na tabela, além de um limite superior para as seletividades de combinações de valores que não aparecem na tabela, permitindo que ela gere melhores estimativas em ambos os casos.

Crie a tabela `t3` com uma única coluna de marca-horário e execute consultas usando expressões nessa coluna. Sem estatísticas extensas, o planejador não tem informações sobre a distribuição dos dados para as expressões e usa estimativas padrão. O planejador também não percebe que o valor da data truncada ao mês é totalmente determinado pelo valor da data truncada ao dia. Em seguida, as estatísticas de expressão e ndistinct são construídas nessas duas expressões:

```
CREATE TABLE t3 (
    a   timestamp
);

INSERT INTO t3 SELECT i FROM generate_series('2020-01-01'::timestamp,
                                             '2020-12-31'::timestamp,
                                             '1 minute'::interval) s(i);

ANALYZE t3;

-- the number of matching rows will be drastically underestimated:
EXPLAIN ANALYZE SELECT * FROM t3
  WHERE date_trunc('month', a) = '2020-01-01'::timestamp;

EXPLAIN ANALYZE SELECT * FROM t3
  WHERE date_trunc('day', a) BETWEEN '2020-01-01'::timestamp
                                 AND '2020-06-30'::timestamp;

EXPLAIN ANALYZE SELECT date_trunc('month', a), date_trunc('day', a)
   FROM t3 GROUP BY 1, 2;

-- build ndistinct statistics on the pair of expressions (per-expression
-- statistics are built automatically)
CREATE STATISTICS s3 (ndistinct) ON date_trunc('month', a), date_trunc('day', a) FROM t3;

ANALYZE t3;

-- now the row count estimates are more accurate:
EXPLAIN ANALYZE SELECT * FROM t3
  WHERE date_trunc('month', a) = '2020-01-01'::timestamp;

EXPLAIN ANALYZE SELECT * FROM t3
  WHERE date_trunc('day', a) BETWEEN '2020-01-01'::timestamp
                                 AND '2020-06-30'::timestamp;

EXPLAIN ANALYZE SELECT date_trunc('month', a), date_trunc('day', a)
   FROM t3 GROUP BY 1, 2;
```

Sem expressões e estatísticas distintas, o planejador não tem informações sobre o número de valores distintos para as expressões, e tem que confiar em estimativas padrão. As condições de igualdade e intervalo são assumidas como tendo seletividade de 0,5%, e o número de valores distintos na expressão é assumido como sendo o mesmo que para a coluna (ou seja, único). Isso resulta em uma subestimação significativa do número de linhas nas duas primeiras consultas. Além disso, o planejador não tem informações sobre a relação entre as expressões, então assume que as duas condições `WHERE` e `GROUP BY` são independentes, e multiplica suas seletividades juntas para chegar a uma superestimação severa do número de grupos na consulta agregada. Isso é exacerbado ainda mais pela falta de estatísticas precisas para as expressões, forçando o planejador a usar uma estimativa distinta padrão para a expressão derivada de distinta para a coluna. Com tais estatísticas, o planejador reconhece que as condições estão correlacionadas, e chega a estimativas muito mais precisas.

## Compatibilidade

Não existe comando `CREATE STATISTICS` no padrão SQL.

## Veja também

[ALTER STATISTICS](sql-alterstatistics.md "ALTER STATISTICS"), [DROP STATISTICS](sql-dropstatistics.md "DROP STATISTICS")