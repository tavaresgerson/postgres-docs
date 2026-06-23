## EXPLIQUE

EXPLAIN — mostre o plano de execução de uma declaração

## Sinopse

```
EXPLAIN [ ( option [, ...] ) ] statement

where option can be one of:

    ANALYZE [ boolean ]
    VERBOSE [ boolean ]
    COSTS [ boolean ]
    SETTINGS [ boolean ]
    GENERIC_PLAN [ boolean ]
    BUFFERS [ boolean ]
    SERIALIZE [ { NONE | TEXT | BINARY } ]
    WAL [ boolean ]
    TIMING [ boolean ]
    SUMMARY [ boolean ]
    MEMORY [ boolean ]
    FORMAT { TEXT | XML | JSON | YAML }
```

## Descrição

Este comando exibe o plano de execução que o planejador do PostgreSQL gera para a declaração fornecida. O plano de execução mostra como a(s) tabela(s) referenciada(s) pela declaração será(ão) examinada(s) — por varredura sequencial simples, varredura de índice, etc. — e se várias tabelas são referenciadas, quais algoritmos de junção serão usados para reunir as linhas necessárias de cada tabela de entrada.

A parte mais crítica do display é o custo estimado da execução da declaração, que é a estimativa do planejador de quanto tempo levará para executar a declaração (medido em unidades de custo que são arbitrárias, mas convencionalmente significam fetches de página de disco). Na verdade, dois números são mostrados: o custo de inicialização antes que a primeira linha possa ser devolvida e o custo total para devolver todas as linhas. Para a maioria das consultas, o custo total é o que importa, mas em contextos como uma subconsulta em `EXISTS`, o planejador escolherá o menor custo de inicialização em vez do menor custo total (já que o executor parará depois de obter uma linha, de qualquer forma). Além disso, se você limitar o número de linhas a serem devolvidas com uma cláusula `LIMIT`, o planejador faz uma interpolação apropriada entre os custos de ponto final para estimar qual plano é realmente o mais barato.

A opção `ANALYZE` faz com que a declaração seja executada efetivamente, e não apenas planejada. Em seguida, as estatísticas de tempo de execução real são adicionadas ao display, incluindo o tempo total gasto dentro de cada nó do plano (em milissegundos) e o número total de linhas que ele realmente retornou. Isso é útil para verificar se as estimativas do planejador estão próximas da realidade.

### Importante

Tenha em mente que a declaração é realmente executada quando a opção `ANALYZE` é usada. Embora `EXPLAIN` descarte qualquer saída que um `SELECT` retornaria, outros efeitos colaterais da declaração ocorrerão como de costume. Se você deseja usar `EXPLAIN ANALYZE` em uma declaração `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `CREATE TABLE AS` ou `EXECUTE` sem deixar o comando afetar seus dados, use essa abordagem:

```
BEGIN;
EXPLAIN ANALYZE ...;
ROLLBACK;
```

## Parâmetros

`ANALYZE`: Realize o comando e mostre os tempos de execução reais e outras estatísticas. Este parâmetro tem como padrão `FALSE`.

`VERBOSE`: Exibir informações adicionais sobre o plano. Especificamente, incluir a lista das colunas de saída para cada nó na árvore do plano, as tabelas e os nomes das funções qualificadas pelo esquema, sempre rotular as variáveis nas expressões com o alias da tabela de intervalo e sempre imprimir o nome de cada gatilho para o qual as estatísticas são exibidas. O identificador da consulta também será exibido se tiver sido calculado, consulte [compute_query_id](runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID) para mais detalhes. Este parâmetro tem como padrão `FALSE`.

`COSTS`: Inclua informações sobre o custo estimado de início e total de cada nó do plano, bem como o número estimado de linhas e a largura estimada de cada linha. Este parâmetro tem como padrão `TRUE`.

`SETTINGS`: Inclua informações sobre os parâmetros de configuração. Especificamente, inclua opções que afetam o planejamento de consulta com valor diferente do valor padrão embutido. Este parâmetro tem como padrão `FALSE`.

`GENERIC_PLAN`: Permita que a declaração contenha suportes de parâmetros, como `$1`, e gere um plano genérico que não dependa dos valores desses parâmetros. Consulte (sql-prepare.md "PREPARE") para obter detalhes sobre planos genéricos e os tipos de declaração que suportam parâmetros. Este parâmetro não pode ser usado juntamente com `ANALYZE`. O padrão é `FALSE`.

`BUFFERS`: Inclua informações sobre o uso dos buffers. Especificamente, inclua o número de blocos compartilhados encontrados, lidos, mantidos sujos e escritos, o número de blocos locais encontrados, lidos, mantidos sujos e escritos, o número de blocos temporários lidos e escritos, e o tempo gasto lendo e escrevendo blocos de arquivos de dados, blocos locais e blocos de arquivos temporários (em milissegundos), se [track_io_timing](runtime-config-statistics.md#GUC-TRACK-IO-TIMING) está habilitado. Um *encontrado* significa que uma leitura foi evitada porque o bloco foi encontrado já na cache quando necessário. Blocos compartilhados contêm dados de tabelas e índices regulares; blocos locais contêm dados de tabelas e índices temporários; enquanto blocos temporários contêm dados de trabalho de curto prazo usados em ordenamentos, hashes, nós de planos Materialize e casos semelhantes. O número de blocos *mantidos sujos* indica o número de blocos previamente não modificados que foram alterados por esta consulta; enquanto o número de blocos *escritos* indica o número de blocos previamente mantidos sujos expulsos da cache por este backend durante o processamento da consulta. O número de blocos mostrado para um nó de nível superior inclui aqueles usados por todos os seus nós filhos. Em formato de texto, apenas valores não nulos são impressos. As informações dos buffers são incluídas automaticamente quando `ANALYZE` é usado.

`SERIALIZE`: Inclua informações sobre o custo de *serializar* os dados de saída da consulta, ou seja, convertê-los em formato de texto ou binário para enviar ao cliente. Isso pode ser uma parte significativa do tempo necessário para a execução regular da consulta, se os tipos de dados de saída forem caros ou se os valores TOAST devem ser recuperados de armazenamento fora da linha. O comportamento padrão de `EXPLAIN`, `SERIALIZE NONE`, não realiza essas conversões. Se `SERIALIZE TEXT` ou `SERIALIZE BINARY` for especificado, as conversões apropriadas são realizadas e o tempo gasto nessas conversões é medido (a menos que `TIMING OFF` seja especificado). Se a opção `BUFFERS` também for especificada, então quaisquer acessos de buffer envolvidos nas conversões também são contados. Em nenhum caso, no entanto, `EXPLAIN` realmente enviará os dados resultantes ao cliente; portanto, os custos de transmissão de rede não podem ser investigados dessa maneira. A serialização só pode ser habilitada quando `ANALYZE` também é habilitada. Se `SERIALIZE` for escrito sem um argumento, `TEXT` é assumido.

`WAL`: Inclua informações sobre a geração de registros WAL. Especificamente, inclua o número de registros, o número de imagens completas de página (fpi), a quantidade de WAL gerada em bytes e o número de vezes que os buffers do WAL ficaram cheios. Em formato de texto, apenas os valores não nulos são impressos. Este parâmetro só pode ser usado quando `ANALYZE` também está habilitado. Ele tem como padrão `FALSE`.

`TIMING`: Inclua o tempo de inicialização real e o tempo gasto em cada nó no resultado. O overhead de leitura repetida do relógio do sistema pode desacelerar significativamente a consulta em alguns sistemas, portanto, pode ser útil definir este parâmetro para `FALSE` quando apenas forem necessárias contagens reais de linhas, e não tempos exatos. O tempo de execução de toda a declaração é sempre medido, mesmo quando o temporizador de nível de nó é desativado com esta opção. Este parâmetro só pode ser usado quando `ANALYZE` também está habilitado. Ele tem como padrão `TRUE`.

`SUMMARY`: Inclua informações resumidas (por exemplo, informações totalizadas sobre o tempo) após o plano de consulta. As informações resumidas são incluídas por padrão quando o `ANALYZE` é usado, mas, de outra forma, não são incluídas por padrão, mas podem ser ativadas usando esta opção. O tempo de planejamento em `EXPLAIN EXECUTE` inclui o tempo necessário para buscar o plano da cache e o tempo necessário para re-planejar, se necessário.

`MEMORY`: Inclua informações sobre o consumo de memória na fase de planejamento da consulta. Especificamente, inclua a quantidade precisa de armazenamento usada pelas estruturas de memória do planejador, bem como a memória total considerando o sobrecarga de alocação. Este parâmetro tem como padrão `FALSE`.

`FORMAT`: Especifique o formato de saída, que pode ser TEXT, XML, JSON ou YAML. A saída não textual contém as mesmas informações que o formato de saída de texto, mas é mais fácil de ser analisada por programas. Este parâmetro tem como padrão `TEXT`.

*`boolean`*: Especifica se a opção selecionada deve ser ativada ou desativada. Você pode escrever `TRUE`, `ON` ou `1` para ativar a opção, e `FALSE`, `OFF` ou `0` para desativá-la. O valor *`boolean`* também pode ser omitido, no qual caso `TRUE` é assumido.

*`statement`*: Qualquer declaração `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `VALUES`, `EXECUTE`, `DECLARE`, `CREATE TABLE AS` ou `CREATE MATERIALIZED VIEW AS` cujo plano de execução você deseja ver.

## Saídas

O resultado do comando é uma descrição textual do plano selecionado para o *`statement`*, opcionalmente anotado com estatísticas de execução. A [Seção 14.1](using-explain.md "14.1. Using EXPLAIN") descreve as informações fornecidas.

## Notas

Para permitir que o planejador de consultas do PostgreSQL tome decisões razoavelmente informadas ao otimizar consultas, os dados `pg_statistic` devem estar atualizados para todas as tabelas usadas na consulta. Normalmente, o daemon de autovazamento (routine-vacuuming.md#AUTOVACUUM "24.1.6. The Autovacuum Daemon") cuidará disso automaticamente. Mas se uma tabela tiver sofrido mudanças substanciais em seu conteúdo recentemente, você pode precisar fazer um `ANALYZE` manual em vez de esperar que o autovazamento acompanhe as mudanças.

Para medir o custo de execução de cada nó no plano de execução, a implementação atual do `EXPLAIN ANALYZE` adiciona sobrecarga de perfilagem à execução da consulta. Como resultado, executar `EXPLAIN ANALYZE` em uma consulta pode, às vezes, levar significativamente mais tempo do que executar a consulta normalmente. A quantidade de sobrecarga depende da natureza da consulta, bem como da plataforma que está sendo usada. O caso mais grave ocorre para nós do plano que, por si mesmos, requerem muito pouco tempo por execução, e em máquinas que têm chamadas de sistema operacional relativamente lentas para obter o horário do dia.

## Exemplos

Para mostrar o plano para uma consulta simples em uma tabela com uma única coluna `integer` e 10000 linhas:

```
EXPLAIN SELECT * FROM foo;

                       QUERY PLAN
---------------------------------------------------------
 Seq Scan on foo  (cost=0.00..155.00 rows=10000 width=4)
(1 row)
```

Aqui está a mesma consulta, com formatação de saída em JSON:

```
EXPLAIN (FORMAT JSON) SELECT * FROM foo;
           QUERY PLAN
--------------------------------
 [                             +
   {                           +
     "Plan": {                 +
       "Node Type": "Seq Scan",+
       "Relation Name": "foo", +
       "Alias": "foo",         +
       "Startup Cost": 0.00,   +
       "Total Cost": 155.00,   +
       "Plan Rows": 10000,     +
       "Plan Width": 4         +
     }                         +
   }                           +
 ]
(1 row)
```

Se houver um índice e usarmos uma consulta com uma condição indexável `WHERE`, `EXPLAIN` pode mostrar um plano diferente:

```
EXPLAIN SELECT * FROM foo WHERE i = 4;

                         QUERY PLAN
--------------------------------------------------------------
 Index Scan using fi on foo  (cost=0.00..5.98 rows=1 width=4)
   Index Cond: (i = 4)
(2 rows)
```

Aqui está a mesma consulta, mas no formato YAML:

```
EXPLAIN (FORMAT YAML) SELECT * FROM foo WHERE i='4';
          QUERY PLAN
-------------------------------
 - Plan:                      +
     Node Type: "Index Scan"  +
     Scan Direction: "Forward"+
     Index Name: "fi"         +
     Relation Name: "foo"     +
     Alias: "foo"             +
     Startup Cost: 0.00       +
     Total Cost: 5.98         +
     Plan Rows: 1             +
     Plan Width: 4            +
     Index Cond: "(i = 4)"
(1 row)
```

O formato XML é deixado como um exercício para o leitor.

Aqui está o mesmo plano com as estimativas de custos suprimidos:

```
EXPLAIN (COSTS FALSE) SELECT * FROM foo WHERE i = 4;

        QUERY PLAN
----------------------------
 Index Scan using fi on foo
   Index Cond: (i = 4)
(2 rows)
```

Aqui está um exemplo de um plano de consulta para uma consulta que utiliza uma função agregada:

```
EXPLAIN SELECT sum(i) FROM foo WHERE i < 10;

                             QUERY PLAN
-------------------------------------------------------------------​--
 Aggregate  (cost=23.93..23.93 rows=1 width=4)
   ->  Index Scan using fi on foo  (cost=0.00..23.92 rows=6 width=4)
         Index Cond: (i < 10)
(3 rows)
```

Aqui está um exemplo de uso de `EXPLAIN EXECUTE` para exibir o plano de execução de uma consulta preparada:

```
PREPARE query(int, int) AS SELECT sum(bar) FROM test
    WHERE id > $1 AND id < $2
    GROUP BY foo;

EXPLAIN ANALYZE EXECUTE query(100, 200);

                                                       QUERY PLAN
-------------------------------------------------------------------​------------------------------------------------------
 HashAggregate  (cost=10.77..10.87 rows=10 width=12) (actual time=0.043..0.044 rows=10.00 loops=1)
   Group Key: foo
   Batches: 1  Memory Usage: 24kB
   Buffers: shared hit=4
   ->  Index Scan using test_pkey on test  (cost=0.29..10.27 rows=99 width=8) (actual time=0.009..0.025 rows=99.00 loops=1)
         Index Cond: ((id > 100) AND (id < 200))
         Index Searches: 1
         Buffers: shared hit=4
 Planning Time: 0.244 ms
 Execution Time: 0.073 ms
(10 rows)
```

Claro, os números específicos mostrados aqui dependem dos conteúdos reais das tabelas envolvidas. Além disso, é importante notar que os números, e até mesmo a estratégia de consulta selecionada, podem variar entre as versões do PostgreSQL devido às melhorias no planejador. Além disso, o comando `ANALYZE` usa amostragem aleatória para estimar estatísticas de dados; portanto, é possível que as estimativas de custo mudem após uma nova execução do `ANALYZE`, mesmo que a distribuição real dos dados na tabela não tenha mudado.

Observe que o exemplo anterior mostrou um plano "personalizado" para os valores específicos dos parâmetros fornecidos em `EXECUTE`. Também gostaríamos de ver o plano genérico para uma consulta parametrizada, o que pode ser feito com `GENERIC_PLAN`:

```
EXPLAIN (GENERIC_PLAN)
  SELECT sum(bar) FROM test
    WHERE id > $1 AND id < $2
    GROUP BY foo;

                                  QUERY PLAN
-------------------------------------------------------------------​------------
 HashAggregate  (cost=26.79..26.89 rows=10 width=12)
   Group Key: foo
   ->  Index Scan using test_pkey on test  (cost=0.29..24.29 rows=500 width=8)
         Index Cond: ((id > $1) AND (id < $2))
(4 rows)
```

Neste caso, o analisador inferiu corretamente que `$1` e `$2` deveriam ter o mesmo tipo de dados que `id`, portanto, a falta de informações sobre o tipo de parâmetro de `PREPARE` não foi um problema. Em outros casos, pode ser necessário especificar explicitamente os tipos dos símbolos de parâmetro, o que pode ser feito por meio da conversão, por exemplo:

```
EXPLAIN (GENERIC_PLAN)
  SELECT sum(bar) FROM test
    WHERE id > $1::integer AND id < $2::integer
    GROUP BY foo;
```

## Compatibilidade

Não há nenhuma declaração `EXPLAIN` definida no padrão SQL.

A sintaxe a seguir foi usada antes da versão 9.0 do PostgreSQL e ainda é suportada:

```
EXPLAIN [ ANALYZE ] [ VERBOSE ] statement
```

Observe que, nesta sintaxe, as opções devem ser especificadas exatamente na ordem mostrada.

## Veja também

[ANALYZE](sql-analyze.md "ANALYZE")
