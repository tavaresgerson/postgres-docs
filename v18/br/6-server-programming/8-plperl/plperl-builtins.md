## 43.3. Funções embutidas [#](#PLPERL-BUILTINS)

* [43.3.1. Acesso a banco de dados a partir de PL/Perl](plperl-builtins.md#PLPERL-DATABASE)
* [43.3.2. Funções utilitárias em PL/Perl](plperl-builtins.md#PLPERL-UTILITY-FUNCTIONS)

### 43.3.1. Acesso ao banco de dados a partir do PL/Perl [#](#PLPERL-DATABASE)

O acesso ao próprio banco de dados a partir da sua função Perl pode ser feito através das seguintes funções:

`spi_exec_query(query [, limit])`: `spi_exec_query` executa um comando SQL e retorna o conjunto de linhas inteira como uma referência a um array de referências de hash. Se *`limit`* é especificado e é maior que zero, então `spi_exec_query` recupera no máximo *`limit`* linhas, assim como se a consulta incluísse uma cláusula de `LIMIT`. O omitindo *`limit`* ou especificando-o como zero resulta em nenhum limite de linha.

*Você deve usar este comando apenas quando sabe que o conjunto de resultados será relativamente pequeno.* Aqui está um exemplo de uma consulta (comando `SELECT`) com o número máximo de linhas opcional:

```
$rv = spi_exec_query('SELECT * FROM my_table', 5);
```

Isso retorna até 5 linhas da tabela `my_table`. Se `my_table` tiver uma coluna `my_column`, você pode obter esse valor da linha `$i` do resultado da seguinte forma:

```
$foo = $rv->{rows}[$i]->{my_column};
```

O número total de linhas retornadas por uma consulta `SELECT` pode ser acessado da seguinte forma:

```
$nrows = $rv->{processed}
```

Aqui está um exemplo usando um tipo de comando diferente:

```
$query = "INSERT INTO my_table VALUES (1, 'test')"; $rv = spi_exec_query($query);
```

Você pode, então, acessar o status do comando (por exemplo, `SPI_OK_INSERT`) da seguinte forma:

```
$res = $rv->{status};
```

Para obter o número de linhas afetadas, faça:

```
$nrows = $rv->{processed};
```

Aqui está um exemplo completo:

```
CREATE TABLE test ( i int, v varchar );

INSERT INTO test (i, v) VALUES (1, 'first line'); INSERT INTO test (i, v) VALUES (2, 'second line'); INSERT INTO test (i, v) VALUES (3, 'third line'); INSERT INTO test (i, v) VALUES (4, 'immortal');

CREATE OR REPLACE FUNCTION test_munge() RETURNS SETOF test AS $$ my $rv = spi_exec_query('select i, v from test;'); my $status = $rv->{status}; my $nrows = $rv->{processed}; foreach my $rn (0 .. $nrows - 1) { my $row = $rv->{rows}[$rn]; $row->{i} += 200 if defined($row->{i}); $row->{v} =~ tr/A-Za-z/a-zA-Z/ if (defined($row->{v})); return_next($row); } return undef; $$ LANGUAGE plperl;

SELECT * FROM test_munge();
```

`spi_query(command)` `spi_fetchrow(cursor)` `spi_cursor_close(cursor)`: `spi_query` e `spi_fetchrow` trabalham juntos como um par para conjuntos de linhas que podem ser grandes, ou para casos em que você deseja retornar as linhas conforme elas chegam. `spi_fetchrow` funciona *apenas* com `spi_query`. O exemplo a seguir ilustra como você os usa juntos:

```
CREATE TYPE foo_type AS (the_num INTEGER, the_text TEXT);

CREATE OR REPLACE FUNCTION lotsa_md5 (INTEGER) RETURNS SETOF foo_type AS $$ use Digest::MD5 qw(md5_hex); my $file = '/usr/share/dict/words'; my $t = localtime; elog(NOTICE, "opening file $file at $t" ); open my $fh, '<', $file # ooh, it's a file access! or elog(ERROR, "cannot open $file for reading: $!"); my @words = <$fh>; close $fh; $t = localtime; elog(NOTICE, "closed file $file at $t"); chomp(@words); my $row; my $sth = spi_query("SELECT * FROM generate_series(1,$_[0]) AS b(a)"); while (defined ($row = spi_fetchrow($sth))) { return_next({ the_num => $row->{a}, the_text => md5_hex($words[rand @words]) }); } return; $$ LANGUAGE plperlu;

SELECT * from lotsa_md5(500);
```

Normalmente, `spi_fetchrow` deve ser repetido até que ele retorne `undef`, indicando que não há mais linhas a serem lidas. O cursor retornado por `spi_query` é liberado automaticamente quando `spi_fetchrow` retorna `undef`. Se você não deseja ler todas as linhas, em vez disso, chame `spi_cursor_close` para liberar o cursor. A falha em fazer isso resultará em vazamentos de memória.

`spi_prepare(command, argument types)` `spi_query_prepared(plan, arguments)` `spi_exec_prepared(plan [, attributes], arguments)` `spi_freeplan(plan)`: `spi_prepare`, `spi_query_prepared`, `spi_exec_prepared`, e `spi_freeplan` implementam a mesma funcionalidade, mas para consultas preparadas. `spi_prepare` aceita uma string de consulta com suportes de argumento numerados ($1, $2, etc.) e uma lista de string de tipos de argumento:

```
$plan = spi_prepare('SELECT * FROM test WHERE id > $1 AND name = $2', 'INTEGER', 'TEXT');
```

Uma vez que um plano de consulta é preparado por uma chamada a `spi_prepare`, o plano pode ser usado em vez da consulta de string, seja em `spi_exec_prepared`, onde o resultado é o mesmo retornado por `spi_exec_query`, ou em `spi_query_prepared` que retorna um cursor exatamente como o `spi_query` faz, que pode ser passado posteriormente para `spi_fetchrow`. O segundo parâmetro opcional de `spi_exec_prepared` é uma referência de hash de atributos; o único atributo atualmente suportado é `limit`, que define o número máximo de linhas retornadas da consulta. Omitindo `limit` ou especificando-o como zero não resulta em nenhuma limitação de linhas.

A vantagem das consultas preparadas é que é possível usar um plano preparado para mais de uma execução de consulta. Depois que o plano não é mais necessário, ele pode ser liberado com `spi_freeplan`:

```
CREATE OR REPLACE FUNCTION init() RETURNS VOID AS $$ $_SHARED{my_plan} = spi_prepare('SELECT (now() + $1)::date AS now', 'INTERVAL'); $$ LANGUAGE plperl;

CREATE OR REPLACE FUNCTION add_time( INTERVAL ) RETURNS TEXT AS $$ return spi_exec_prepared( $_SHARED{my_plan}, $_[0] )->{rows}->[0]->{now}; $$ LANGUAGE plperl;

CREATE OR REPLACE FUNCTION done() RETURNS VOID AS $$ spi_freeplan( $_SHARED{my_plan}); undef $_SHARED{my_plan}; $$ LANGUAGE plperl;

SELECT init(); SELECT add_time('1 day'), add_time('2 days'), add_time('3 days'); SELECT done();

  add_time  |  add_time  |  add_time ------------+------------+------------ 2005-12-10 | 2005-12-11 | 2005-12-12
```

Observe que o subscrito do parâmetro em `spi_prepare` é definido via $1, $2, $3, etc., então evite declarar strings de consulta em aspas duplas que podem facilmente levar a bugs difíceis de detectar.

Outro exemplo ilustra o uso de um parâmetro opcional em `spi_exec_prepared`:

```
CREATE TABLE hosts AS SELECT id, ('192.168.1.'||id)::inet AS address FROM generate_series(1,3) AS id;

CREATE OR REPLACE FUNCTION init_hosts_query() RETURNS VOID AS $$ $_SHARED{plan} = spi_prepare('SELECT * FROM hosts WHERE address << $1', 'inet'); $$ LANGUAGE plperl;

CREATE OR REPLACE FUNCTION query_hosts(inet) RETURNS SETOF hosts AS $$ return spi_exec_prepared( $_SHARED{plan}, {limit => 2}, $_[0] )->{rows}; $$ LANGUAGE plperl;

CREATE OR REPLACE FUNCTION release_hosts_query() RETURNS VOID AS $$ spi_freeplan($_SHARED{plan}); undef $_SHARED{plan}; $$ LANGUAGE plperl;

SELECT init_hosts_query(); SELECT query_hosts('192.168.1.0/30'); SELECT release_hosts_query();

    query_hosts ----------------- (1,192.168.1.1) (2,192.168.1.2) (2 rows)
```

`spi_commit()` `spi_rollback()`: Comunique ou desfaça a transação atual. Isso só pode ser chamado em um procedimento ou bloco de código anônimo (comando `DO` ) chamado do nível superior. (Observe que não é possível executar os comandos SQL `COMMIT` ou `ROLLBACK` por meio de `spi_exec_query` ou similar. Tem que ser feito usando essas funções.) Após uma transação ser encerrada, uma nova transação é iniciada automaticamente, então não há uma função separada para isso.

Aqui está um exemplo:

```
CREATE PROCEDURE transaction_test1() LANGUAGE plperl AS $$ foreach my $i (0..9) { spi_exec_query("INSERT INTO test1 (a) VALUES ($i)"); if ($i % 2 == 0) { spi_commit(); } else { spi_rollback(); } } $$;

CALL transaction_test1();
```

### 43.3.2. Funções de Utilidade em PL/Perl [#](#PLPERL-UTILITY-FUNCTIONS)

`elog(level, msg)`: Emita uma mensagem de log ou de erro. Os níveis possíveis são `DEBUG`, `LOG`, `INFO`, `NOTICE`, `WARNING` e `ERROR`. `ERROR` leva uma condição de erro; se não for capturada pelo código Perl circundante, o erro se propaga para a consulta que o solicitou, causando o cancelamento da transação ou subtransação atual. Isso é efetivamente o mesmo que o comando Perl `die`. Os outros níveis apenas geram mensagens de diferentes níveis de prioridade. Se mensagens de uma prioridade específica são relatadas ao cliente, escritas no log do servidor ou ambas, é controlado pelas variáveis de configuração [log_min_messages](runtime-config-logging.md#GUC-LOG-MIN-MESSAGES) e [client_min_messages](runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES). Consulte [Capítulo 19](runtime-config.md "Chapter 19. Server Configuration") para mais informações.

`quote_literal(string)`: Retorne a string dada devidamente citada para ser usada como uma string literal em uma string de declaração SQL. As aspas embutidas e barras invertidas são duplicadas corretamente. Note que `quote_literal` retorna undef em caso de entrada undef; se o argumento pode ser undef, `quote_nullable` é frequentemente mais adequado.

`quote_nullable(string)`: Retorne a string dada devidamente citada para ser usada como uma string literal em uma string de declaração SQL; ou, se o argumento for undef, retorne a string não citada "NULL". As aspas embutidas e barras invertidas são duplicadas corretamente.

`quote_ident(string)`: Retorne a string dada devidamente citada para ser usada como um identificador em uma string de declaração SQL. As citações são adicionadas apenas se necessário (ou seja, se a string contém caracteres não identificadores ou seria compactada por caso). As citações embutidas são duplicadas adequadamente.

`decode_bytea(string)`: Retorne os dados binários não escapados representados pelo conteúdo da string fornecida, que deve ser codificado em `bytea`.

`encode_bytea(string)`: Retorne o formulário codificado `bytea` dos conteúdos de dados binários da string fornecida.

`encode_array_literal(array)` `encode_array_literal(array, delimiter)`: Retorna o conteúdo do array referenciado como uma string no formato literal de matriz (consulte [Seção 8.15.2](arrays.md#ARRAYS-INPUT "8.15.2. Array Value Input")). Retorna o valor do argumento inalterado se não for uma referência a uma matriz. O delimitador usado entre os elementos do literal de matriz tem como padrão "`,`" se um delimitador não for especificado ou é indefinido.

`encode_typed_literal(value, typename)`: Converte uma variável Perl para o valor do tipo de dados passado como segundo argumento e retorna uma representação em string desse valor. Manipula corretamente arrays aninhados e valores de tipos compostos.

`encode_array_constructor(array)`: Retorna o conteúdo do array referenciado como uma string no formato do construtor de matriz (consulte [Seção 4.2.12](sql-expressions.md#SQL-SYNTAX-ARRAY-CONSTRUCTORS)). Valores individuais são citados usando `quote_nullable`. Retorna o valor do argumento, citado usando `quote_nullable`, se não for uma referência a um array.

`looks_like_number(string)`: Devolve um valor verdadeiro se o conteúdo da string fornecida parece ser um número, de acordo com Perl, devolve false caso contrário. `Inf` e `Infinity` são considerados números. `Inf` e `Infinity` são considerados números.

`is_array_ref(argument)` :   Devolve um valor verdadeiro se o argumento fornecido pode ser tratado como uma referência de matriz, ou seja, se ref do argumento é `ARRAY` ou `PostgreSQL::InServer::ARRAY`. Devolve false caso contrário.