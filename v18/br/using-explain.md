## 14.1. Usando `EXPLAIN` [#](#USING-EXPLAIN)

* [14.1.1. `EXPLAIN` Fundamentos](using-explain.md#USING-EXPLAIN-BASICS)
* [14.1.2. `EXPLAIN ANALYZE`](using-explain.md#USING-EXPLAIN-ANALYZE)
* [14.1.3. Observações](using-explain.md#USING-EXPLAIN-CAVEATS)

O PostgreSQL elabora um plano de *consulta* para cada consulta que recebe. Escolher o plano certo para corresponder à estrutura da consulta e às propriedades dos dados é absolutamente crítico para um bom desempenho, então o sistema inclui um *planificador* complexo que tenta escolher bons planos. Você pode usar o comando `EXPLAIN`(sql-explain.md "EXPLAIN") para ver qual plano de consulta o planeificador cria para qualquer consulta. A leitura do plano é uma arte que requer alguma experiência para dominar, mas esta seção tenta cobrir o básico.

Os exemplos desta seção são retirados do banco de dados de teste de regressão após a realização de um `VACUUM ANALYZE`, usando as fontes de desenvolvimento v18. Você deve ser capaz de obter resultados semelhantes se tentar os exemplos por si mesmo, mas seus custos estimados e contagem de linhas podem variar ligeiramente porque as estatísticas do `ANALYZE` são amostras aleatórias e não exatas, e porque os custos são inerentemente dependentes da plataforma.

Os exemplos utilizam o formato de saída padrão de "texto" do `EXPLAIN`, que é compacto e conveniente para que os seres humanos o leiam. Se você quiser alimentar a saída do `EXPLAIN` em um programa para análise adicional, você deve usar um de seus formatos de saída legíveis por máquina (XML, JSON ou YAML) em vez disso.

### 14.1.1. `EXPLAIN` Princípios básicos [#](#USING-EXPLAIN-BASICS)

A estrutura de um plano de consulta é uma árvore de *nós de plano*. Os nós no nível mais baixo da árvore são nós de varredura: eles retornam linhas bruta de uma tabela. Existem diferentes tipos de nós de varredura para diferentes métodos de acesso a tabela: varreduras sequenciais, varreduras de índice e varreduras de índice de bitmap. Também existem fontes de linha não de tabela, como cláusulas `VALUES` e funções que retornam conjuntos em `FROM`, que têm seus próprios tipos de nós de varredura. Se a consulta requer junção, agregação, ordenação ou outras operações nas linhas bruta, então haverá nós adicionais acima dos nós de varredura para realizar essas operações. Novamente, geralmente há mais de uma maneira possível de fazer essas operações, então diferentes tipos de nós podem aparecer aqui também. A saída de `EXPLAIN` tem uma linha para cada nó na árvore de plano, mostrando o tipo de nó básico mais as estimativas de custo que o planejador fez para a execução desse nó de plano. Linhas adicionais podem aparecer, indentadas a partir da linha de resumo do nó, para mostrar propriedades adicionais do nó. A primeira linha (a linha de resumo do nó mais alto) tem o custo total estimado de execução do plano; é esse número que o planejador busca minimizar.

Aqui está um exemplo trivial, apenas para mostrar como fica o resultado:

```
EXPLAIN SELECT * FROM tenk1;

                         QUERY PLAN
-------------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..445.00 rows=10000 width=244)
```

Como esta consulta não tem cláusula `WHERE`, ela deve analisar todas as linhas da tabela, então o planejador escolheu usar um plano de varredura sequencial simples. Os números que são citados entre parênteses são (de esquerda para direita):

* Custo estimado de início. Este é o tempo gasto antes que a fase de saída possa começar, por exemplo, o tempo para fazer a classificação em um nó de classificação.
* Custo total estimado. Isso é declarado sob a suposição de que o nó do plano é executado até o fim, ou seja, todas as linhas disponíveis são recuperadas. Na prática, o nó do pai do nó pode parar antes de ler todas as linhas disponíveis (veja o exemplo `LIMIT` abaixo).
* Número estimado de linhas produzidas por este nó do plano. Novamente, assume-se que o nó é executado até o fim.
* Largura média estimada das linhas produzidas por este nó do plano (em bytes).

Os custos são medidos em unidades arbitrárias determinadas pelos parâmetros de custo do planejador (ver [Seção 19.7.2] [(runtime-config-query.md#RUNTIME-CONFIG-QUERY-CONSTANTS "19.7.2. Planner Cost Constants")]). A prática tradicional é medir os custos em unidades de busca de página de disco; ou seja, [seq_page_cost](runtime-config-query.md#GUC-SEQ-PAGE-COST) é convencionalmente definido como `1.0` e os outros parâmetros de custo são definidos em relação a isso. Os exemplos nesta seção são executados com os parâmetros de custo padrão.

É importante entender que o custo de um nó de nível superior inclui o custo de todos os seus nós filhos. Também é importante perceber que o custo apenas reflete as coisas que o planejador se importa. Em particular, o custo não considera o tempo gasto para converter os valores de saída para formato de texto ou para transmiti-los ao cliente, o que poderia ser fatores importantes no tempo real; mas o planejador ignora esses custos porque não pode alterá-los alterando o plano. (Todo plano correto produzirá o mesmo conjunto de linhas, confiamos.)

O valor `rows` é um pouco complicado, pois não é o número de linhas processadas ou digitalizadas pelo nó do plano, mas sim o número emitido pelo nó. Isso geralmente é menor que o número digitalizado, como resultado da filtragem por quaisquer condições da cláusula `WHERE` que estão sendo aplicadas no nó. Idealmente, a estimativa das linhas de nível superior deve aproximar o número de linhas realmente devolvidas, atualizadas ou excluídas pela consulta.

Voltando ao nosso exemplo:

```
EXPLAIN SELECT * FROM tenk1;

                         QUERY PLAN
-------------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..445.00 rows=10000 width=244)
```

Esses números são derivados de forma muito simples. Se você fizer:

```
SELECT relpages, reltuples FROM pg_class WHERE relname = 'tenk1';
```

você descobrirá que `tenk1` tem 345 páginas de disco e 10000 linhas. O custo estimado é calculado como (páginas de disco lidas * [seq_page_cost](runtime-config-query.md#GUC-SEQ-PAGE-COST)) + (linhas digitalizadas * [cpu_tuple_cost](runtime-config-query.md#GUC-CPU-TUPLE-COST)). Por padrão, `seq_page_cost` é 1,0 e `cpu_tuple_cost` é 0,01, então o custo estimado é (345 * 1,0) + (10000 * 0,01) = 445.

Agora, vamos modificar a consulta para adicionar uma condição `WHERE`:

```
EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 7000;

                         QUERY PLAN
------------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..470.00 rows=7000 width=244)
   Filter: (unique1 < 7000)
```

Observe que a saída `EXPLAIN` mostra a cláusula `WHERE` sendo aplicada como uma condição de “filtro” anexada ao nó do plano Seq Scan. Isso significa que o nó do plano verifica a condição para cada linha que ele examina e produz apenas as que passam na condição. A estimativa de linhas de saída foi reduzida devido à cláusula `WHERE`. No entanto, a varredura ainda terá que visitar todas as 10000 linhas, então o custo não diminuiu; de fato, aumentou um pouco (por 10000 * [cpu_operator_cost][(runtime-config-query.md#GUC-CPU-OPERATOR-COST)], para ser exato) para refletir o tempo extra de CPU gasto verificando a condição `WHERE`.

O número real de linhas que essa consulta selecionaria é de 7000, mas a estimativa do `rows` é apenas aproximada. Se você tentar duplicar essa experiência, é bem possível que você obtenha uma estimativa ligeiramente diferente; além disso, ela pode mudar após cada comando do `ANALYZE`, porque as estatísticas produzidas pelo `ANALYZE` são tiradas de uma amostra aleatória da tabela.

Agora, vamos tornar a condição mais restritiva:

```
EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100;

                                  QUERY PLAN
-------------------------------------------------------------------​-----------
 Bitmap Heap Scan on tenk1  (cost=5.06..224.98 rows=100 width=244)
   Recheck Cond: (unique1 < 100)
   ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0)
         Index Cond: (unique1 < 100)
```

Aqui, o planejador decidiu usar um plano em duas etapas: o nó do plano de criança visita um índice para encontrar as localizações das linhas que correspondem à condição do índice, e então o nó do plano superior realmente recupera essas linhas da própria tabela. Recuperar as linhas separadamente é muito mais caro do que lê-las sequencialmente, mas, como nem todas as páginas da tabela precisam ser visitadas, isso ainda é mais barato do que uma varredura sequencial. (A razão para usar dois níveis de plano é que o nó do plano superior ordena as localizações das linhas identificadas pelo índice em ordem física antes de lê-las, para minimizar o custo das recuperações separadas. O "bitmape" mencionado nos nomes dos nós é o mecanismo que faz a ordenação.)

Agora, vamos adicionar outra condição à cláusula `WHERE`:

```
EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100 AND stringu1 = 'xxx';

                                  QUERY PLAN
-------------------------------------------------------------------​-----------
 Bitmap Heap Scan on tenk1  (cost=5.04..225.20 rows=1 width=244)
   Recheck Cond: (unique1 < 100)
   Filter: (stringu1 = 'xxx'::name)
   ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0)
         Index Cond: (unique1 < 100)
```

A condição adicional `stringu1 = 'xxx'` reduz a estimativa do número de linhas geradas, mas não o custo, porque ainda temos que visitar o mesmo conjunto de linhas. Isso ocorre porque a cláusula `stringu1` não pode ser aplicada como uma condição de índice, uma vez que este índice está apenas na coluna `unique1`. Em vez disso, é aplicado como um filtro nas linhas recuperadas usando o índice. Assim, o custo realmente aumentou ligeiramente para refletir essa verificação extra.

Em alguns casos, o planejador preferirá um plano de varredura de índice “simples”:

```
EXPLAIN SELECT * FROM tenk1 WHERE unique1 = 42;

                                 QUERY PLAN
-------------------------------------------------------------------​----------
 Index Scan using tenk1_unique1 on tenk1  (cost=0.29..8.30 rows=1 width=244)
   Index Cond: (unique1 = 42)
```

Nesse tipo de plano, as linhas da tabela são obtidas em ordem de índice, o que as torna ainda mais caras de ler, mas há tantas poucas que o custo adicional de ordenar as localizações das linhas não vale a pena. Você verá esse tipo de plano com mais frequência em consultas que obtêm apenas uma única linha. Também é frequentemente usado para consultas que têm uma condição `ORDER BY` que corresponde à ordem de índice, porque, então, não é necessário nenhum passo adicional de ordenação para satisfazer a `ORDER BY`. Neste exemplo, adicionar `ORDER BY unique1` usaria o mesmo plano porque o índice já fornece implicitamente a ordem solicitada.

O planejador pode implementar uma cláusula `ORDER BY` de várias maneiras. O exemplo acima mostra que tal cláusula de ordenação pode ser implementada implicitamente. O planejador também pode adicionar uma etapa explícita `Sort`:

```
EXPLAIN SELECT * FROM tenk1 ORDER BY unique1;

                            QUERY PLAN
-------------------------------------------------------------------
 Sort  (cost=1109.39..1134.39 rows=10000 width=244)
   Sort Key: unique1
   ->  Seq Scan on tenk1  (cost=0.00..445.00 rows=10000 width=244)
```

Se uma parte do plano garantir uma ordenação em um prefixo das chaves de classificação necessárias, então o planejador pode decidir, em vez disso, usar uma etapa `Incremental Sort`:

```
EXPLAIN SELECT * FROM tenk1 ORDER BY hundred, ten LIMIT 100;

                                              QUERY PLAN
-------------------------------------------------------------------​-----------------------------
 Limit  (cost=19.35..39.49 rows=100 width=244)
   ->  Incremental Sort  (cost=19.35..2033.39 rows=10000 width=244)
         Sort Key: hundred, ten
         Presorted Key: hundred
         ->  Index Scan using tenk1_hundred on tenk1  (cost=0.29..1574.20 rows=10000 width=244)
```

Comparado aos tipos de classificação regulares, a classificação incremental permite retornar tuplas antes que todo o conjunto de resultados tenha sido classificado, o que permite otimizações, em particular, com consultas `LIMIT`. Também pode reduzir o uso de memória e a probabilidade de derrapagens de classificação para o disco, mas isso ocorre ao custo do aumento do custo de divisão do conjunto de resultados em múltiplos lotes de classificação.

Se houver índices separados em várias das colunas referenciadas em `WHERE`, o planejador pode optar por usar uma combinação de AND ou OR dos índices:

```
EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100 AND unique2 > 9000;

                                     QUERY PLAN
-------------------------------------------------------------------​------------------
 Bitmap Heap Scan on tenk1  (cost=25.07..60.11 rows=10 width=244)
   Recheck Cond: ((unique1 < 100) AND (unique2 > 9000))
   ->  BitmapAnd  (cost=25.07..25.07 rows=10 width=0)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0)
               Index Cond: (unique1 < 100)
         ->  Bitmap Index Scan on tenk1_unique2  (cost=0.00..19.78 rows=999 width=0)
               Index Cond: (unique2 > 9000)
```

Mas isso exige a visitação de ambos os índices, então não é necessariamente uma vantagem em comparação com o uso de apenas um índice e o tratamento da outra condição como um filtro. Se você variar os intervalos envolvidos, verá que o plano muda conforme necessário.

Aqui está um exemplo que mostra os efeitos do `LIMIT`:

```
EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100 AND unique2 > 9000 LIMIT 2;

                                     QUERY PLAN
-------------------------------------------------------------------​------------------
 Limit  (cost=0.29..14.28 rows=2 width=244)
   ->  Index Scan using tenk1_unique2 on tenk1  (cost=0.29..70.27 rows=10 width=244)
         Index Cond: (unique2 > 9000)
         Filter: (unique1 < 100)
```

Esta é a mesma consulta do texto acima, mas adicionamos um `LIMIT` para que nem todas as linhas não precisem ser recuperadas, e o planejador mudou de ideia sobre o que fazer. Observe que o custo total e o número de linhas do nó de Índex de Pesquisa são mostrados como se estivesse executado até o final. No entanto, espera-se que o nó Limite pare após recuperar apenas um quinto dessas linhas, então seu custo total é apenas um quinto do valor, e esse é o custo estimado real da consulta. Este plano é preferido em relação à adição de um nó Limite ao plano anterior, porque o Limite não conseguiu evitar o pagamento do custo inicial do varrimento de bitmap, então o custo total seria algo além de 25 unidades com essa abordagem.

Vamos tentar unir duas tabelas, usando as colunas que discutimos:

```
EXPLAIN SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 10 AND t1.unique2 = t2.unique2;

                                      QUERY PLAN
-------------------------------------------------------------------​-------------------
 Nested Loop  (cost=4.65..118.50 rows=10 width=488)
   ->  Bitmap Heap Scan on tenk1 t1  (cost=4.36..39.38 rows=10 width=244)
         Recheck Cond: (unique1 < 10)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..4.36 rows=10 width=0)
               Index Cond: (unique1 < 10)
   ->  Index Scan using tenk2_unique2 on tenk2 t2  (cost=0.29..7.90 rows=1 width=244)
         Index Cond: (unique2 = t1.unique2)
```

Neste plano, temos um nó de junção com laço aninhado com dois varreduras de tabela como entradas, ou filhos. A indentação das linhas do resumo do nó reflete a estrutura da árvore do plano. O primeiro, ou "externo", filho da junção é uma varredura de bitmap semelhante àquelas que vimos antes. Seu custo e contagem de linhas são os mesmos que obteríamos do `SELECT ... WHERE unique1 < 10`, porque estamos aplicando a cláusula `WHERE` `unique1 < 10` naquele nó. A cláusula `t1.unique2 = t2.unique2` ainda não é relevante, então ela não afeta a contagem de linhas da varredura externa. O nó de junção com laço aninhado executará seu segundo, ou "interno", filho uma vez para cada linha obtida da varredura externa. Os valores das colunas da linha externa atual podem ser inseridos na varredura interna; aqui, o valor `t1.unique2` da linha externa está disponível, então obtemos um plano e custos semelhantes ao que vimos acima para um caso simples de `SELECT ... WHERE t2.unique2 = constant`. (O custo estimado é na verdade um pouco menor do que o que foi visto acima, como resultado da cache que se espera ocorrer durante as varreduras repetidas de índice em `t2`.) Os custos do nó do laço são então definidos com base no custo da varredura externa, mais uma repetição da varredura interna para cada linha externa (10 * 7,90, aqui), mais um pouco de tempo de CPU para o processamento da junção.

Neste exemplo, o número de linhas de saída do join é o mesmo que o produto dos números de linhas dos dois scans, mas isso não é verdade em todos os casos, porque pode haver cláusulas adicionais de `WHERE` que mencionam ambas as tabelas e, portanto, só podem ser aplicadas no ponto de junção, e não em nenhum dos scans de entrada. Aqui está um exemplo:

```
EXPLAIN SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 10 AND t2.unique2 < 10 AND t1.hundred < t2.hundred;

                                         QUERY PLAN
-------------------------------------------------------------------​--------------------------
 Nested Loop  (cost=4.65..49.36 rows=33 width=488)
   Join Filter: (t1.hundred < t2.hundred)
   ->  Bitmap Heap Scan on tenk1 t1  (cost=4.36..39.38 rows=10 width=244)
         Recheck Cond: (unique1 < 10)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..4.36 rows=10 width=0)
               Index Cond: (unique1 < 10)
   ->  Materialize  (cost=0.29..8.51 rows=10 width=244)
         ->  Index Scan using tenk2_unique2 on tenk2 t2  (cost=0.29..8.46 rows=10 width=244)
               Index Cond: (unique2 < 10)
```

A condição `t1.hundred < t2.hundred` não pode ser testada no índice `tenk2_unique2`, então ela é aplicada no nó de junção. Isso reduz o número estimado de linhas de saída do nó de junção, mas não altera nenhum dos scans de entrada.

Observe que, aqui, o planejador escolheu "materializar" a relação interna da junção, colocando um nó de plano Materialize em cima dela. Isso significa que a varredura do índice `t2` será feita apenas uma vez, embora o nó de junção de laço aninhado precise ler esses dados dez vezes, uma vez para cada linha da relação externa. O nó Materialize salva os dados na memória à medida que são lidos e, em seguida, retorna os dados da memória em cada passagem subsequente.

Ao lidar com junções externas, você pode ver nós do plano de junção com condições de “Filtro de junção” e simplesmente “Filtro” anexadas. As condições de Filtro de junção vêm da cláusula `ON` da junção externa, então uma linha que falha na condição do Filtro de junção ainda pode ser emitida como uma linha com extensão nula. Mas uma condição de Filtro simples é aplicada após as regras da junção externa e, portanto, remove as linhas incondicionalmente. Em uma junção interna, não há diferença semântica entre esses tipos de filtros.

Se mudarmos um pouco a seletividade da consulta, podemos obter um plano de junção muito diferente:

```
EXPLAIN SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2;

                                        QUERY PLAN
-------------------------------------------------------------------​-----------------------
 Hash Join  (cost=226.23..709.73 rows=100 width=488)
   Hash Cond: (t2.unique2 = t1.unique2)
   ->  Seq Scan on tenk2 t2  (cost=0.00..445.00 rows=10000 width=244)
   ->  Hash  (cost=224.98..224.98 rows=100 width=244)
         ->  Bitmap Heap Scan on tenk1 t1  (cost=5.06..224.98 rows=100 width=244)
               Recheck Cond: (unique1 < 100)
               ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0)
                     Index Cond: (unique1 < 100)
```

Aqui, o planejador escolheu usar uma junção hash, na qual as linhas de uma tabela são inseridas em uma tabela hash de memória, após o que a outra tabela é examinada e a tabela hash é sondada em busca de correspondências para cada linha. Novamente, observe como a indentação reflete a estrutura do plano: a varredura de bitmap em `tenk1` é a entrada para o nó Hash, que constrói a tabela hash. Isso é então retornado para o nó de junção hash, que lê as linhas de seu plano filho externo e pesquisa a tabela hash para cada uma.

Outro tipo possível de junção é a junção de fusão, ilustrada aqui:

```
EXPLAIN SELECT *
FROM tenk1 t1, onek t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2;

                                        QUERY PLAN
-------------------------------------------------------------------​-----------------------
 Merge Join  (cost=0.56..233.49 rows=10 width=488)
   Merge Cond: (t1.unique2 = t2.unique2)
   ->  Index Scan using tenk1_unique2 on tenk1 t1  (cost=0.29..643.28 rows=100 width=244)
         Filter: (unique1 < 100)
   ->  Index Scan using onek_unique2 on onek t2  (cost=0.28..166.28 rows=1000 width=244)
```

A junção por fusão exige que os dados de entrada sejam ordenados pelas chaves de junção. Neste exemplo, cada entrada é ordenada usando uma varredura de índice para visitar as linhas no ordem correta; mas uma varredura sequencial e uma ordenação também poderiam ser usadas. (A varredura sequencial e a ordenação frequentemente superam uma varredura de índice para ordenar muitas linhas, devido ao acesso não sequencial ao disco exigido pela varredura de índice.)

Uma maneira de analisar planos variantes é forçar o planejador a ignorar qualquer estratégia que ele pensasse que fosse a mais barata, usando as bandeiras de ativação/desativação descritas em [Seção 19.7.1] (Isso é uma ferramenta grosseira, mas útil. Veja também [Seção 14.3] ((explicit-joins.md "14.3. Controlling the Planner with Explicit JOIN Clauses"))). Por exemplo, se não estamos convencidos de que a junção de fusão é o melhor tipo de junção para o exemplo anterior, poderíamos tentar

```
SET enable_mergejoin = off;

EXPLAIN SELECT *
FROM tenk1 t1, onek t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2;

                                        QUERY PLAN
-------------------------------------------------------------------​-----------------------
 Hash Join  (cost=226.23..344.08 rows=10 width=488)
   Hash Cond: (t2.unique2 = t1.unique2)
   ->  Seq Scan on onek t2  (cost=0.00..114.00 rows=1000 width=244)
   ->  Hash  (cost=224.98..224.98 rows=100 width=244)
         ->  Bitmap Heap Scan on tenk1 t1  (cost=5.06..224.98 rows=100 width=244)
               Recheck Cond: (unique1 < 100)
               ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0)
                     Index Cond: (unique1 < 100)
```

que mostra que o planejador acha que a junção hash seria quase 50% mais cara do que a junção de fusão para este caso. Claro, a próxima pergunta é se isso está correto. Podemos investigar isso usando `EXPLAIN ANALYZE`, conforme discutido [abaixo][(using-explain.md#USING-EXPLAIN-ANALYZE "14.1.2. EXPLAIN ANALYZE")].

Ao usar as bandeiras de habilitação/desabilitação para desabilitar tipos de nós de plano, muitas das bandeiras apenas desencorajam o uso do nó de plano correspondente e não impedem completamente a capacidade do planejador de usar o tipo de nó de plano. Isso é por design, para que o planejador ainda mantenha a capacidade de formar um plano para uma consulta específica. Quando o plano resultante contém um nó desabilitado, a saída `EXPLAIN` indicará esse fato.

```
SET enable_seqscan = off;
EXPLAIN SELECT * FROM unit;

                       QUERY PLAN
---------------------------------------------------------
 Seq Scan on unit  (cost=0.00..21.30 rows=1130 width=44)
   Disabled: true
```

Como a tabela `unit` não possui índices, não há outro meio de ler os dados da tabela, portanto, o varredura sequencial é a única opção disponível para o planejador de consulta.

Alguns planos de consulta envolvem *subplanos*, que surgem de sub-`SELECT`s na consulta original. Essas consultas podem, às vezes, ser transformadas em planos de junção comuns, mas quando não podem ser, obtemos planos como:

```
EXPLAIN VERBOSE SELECT unique1
FROM tenk1 t
WHERE t.ten < ALL (SELECT o.ten FROM onek o WHERE o.four = t.four);

                               QUERY PLAN
-------------------------------------------------------------------​------
 Seq Scan on public.tenk1 t  (cost=0.00..586095.00 rows=5000 width=4)
   Output: t.unique1
   Filter: (ALL (t.ten < (SubPlan 1).col1))
   SubPlan 1
     ->  Seq Scan on public.onek o  (cost=0.00..116.50 rows=250 width=4)
           Output: o.ten
           Filter: (o.four = t.four)
```

Este exemplo bastante artificial serve para ilustrar alguns pontos: os valores do nível do plano externo podem ser passados para um subplano (aqui, `t.four` é passado) e os resultados da subseleção estão disponíveis para o plano externo. Esses valores de resultado são mostrados por `EXPLAIN` com notações como `(subplan_name).colN`, que se refere à *`N`'ª coluna de saída do sub`SELECT`.

No exemplo acima, o operador `ALL` executa o subplano novamente para cada linha da consulta externa (que leva em conta o alto custo estimado). Algumas consultas podem usar um *subplano hashado* para evitar isso:

```
EXPLAIN SELECT *
FROM tenk1 t
WHERE t.unique1 NOT IN (SELECT o.unique1 FROM onek o);

                                         QUERY PLAN
-------------------------------------------------------------------​-------------------------
 Seq Scan on tenk1 t  (cost=61.77..531.77 rows=5000 width=244)
   Filter: (NOT (ANY (unique1 = (hashed SubPlan 1).col1)))
   SubPlan 1
     ->  Index Only Scan using onek_unique1 on onek o  (cost=0.28..59.27 rows=1000 width=4)
(4 rows)
```

Aqui, o subplano é executado uma única vez e sua saída é carregada em uma tabela de hash de memória, que é então verificada pelo operador externo `ANY`. Isso exige que o sub-`SELECT` não faça referência a quaisquer variáveis da consulta externa e que o operador de comparação do `ANY` seja compatível com a hashing.

Se, além de não fazer referência a quaisquer variáveis da consulta externa, o sub-`SELECT` não puder retornar mais de uma linha, ele pode ser implementado como um *initplan*:

```
EXPLAIN VERBOSE SELECT unique1
FROM tenk1 t1 WHERE t1.ten = (SELECT (random() * 10)::integer);

                             QUERY PLAN
------------------------------------------------------------​--------
 Seq Scan on public.tenk1 t1  (cost=0.02..470.02 rows=1000 width=4)
   Output: t1.unique1
   Filter: (t1.ten = (InitPlan 1).col1)
   InitPlan 1
     ->  Result  (cost=0.00..0.02 rows=1 width=4)
           Output: ((random() * '10'::double precision))::integer
```

Um initplan é executado apenas uma vez por execução do plano externo, e seus resultados são salvos para reutilização em linhas posteriores do plano externo. Assim, neste exemplo, `random()` é avaliado apenas uma vez e todos os valores de `t1.ten` são comparados com o mesmo inteiro escolhido aleatoriamente. Isso é bastante diferente do que aconteceria sem a construção sub-`SELECT`.

### 14.1.2. `EXPLAIN ANALYZE` [#](#USING-EXPLAIN-ANALYZE)

É possível verificar a precisão das estimativas do planejador usando a opção `EXPLAIN` de `ANALYZE`. Com essa opção, `EXPLAIN` executa a consulta e, em seguida, exibe as contagens verdadeiras de linhas e o tempo de execução acumulado dentro de cada nó do plano, juntamente com as mesmas estimativas que um simples `EXPLAIN` mostra. Por exemplo, podemos obter um resultado como este:

```
EXPLAIN ANALYZE SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 10 AND t1.unique2 = t2.unique2;

                                                           QUERY PLAN
-------------------------------------------------------------------​--------------------------------------------------------------
 Nested Loop  (cost=4.65..118.50 rows=10 width=488) (actual time=0.017..0.051 rows=10.00 loops=1)
   Buffers: shared hit=36 read=6
   ->  Bitmap Heap Scan on tenk1 t1  (cost=4.36..39.38 rows=10 width=244) (actual time=0.009..0.017 rows=10.00 loops=1)
         Recheck Cond: (unique1 < 10)
         Heap Blocks: exact=10
         Buffers: shared hit=3 read=5 written=4
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..4.36 rows=10 width=0) (actual time=0.004..0.004 rows=10.00 loops=1)
               Index Cond: (unique1 < 10)
               Index Searches: 1
               Buffers: shared hit=2
   ->  Index Scan using tenk2_unique2 on tenk2 t2  (cost=0.29..7.90 rows=1 width=244) (actual time=0.003..0.003 rows=1.00 loops=10)
         Index Cond: (unique2 = t1.unique2)
         Index Searches: 10
         Buffers: shared hit=24 read=6
 Planning:
   Buffers: shared hit=15 dirtied=9
 Planning Time: 0.485 ms
 Execution Time: 0.073 ms
```

Observe que os valores de “tempo real” são em milissegundos de tempo real, enquanto as estimativas de `cost` são expressas em unidades arbitrárias; portanto, é improvável que coincidam. O que geralmente é mais importante verificar é se as contagens de linhas estimadas estão razoavelmente próximas da realidade. Neste exemplo, as estimativas estavam todas corretas, mas isso é bastante incomum na prática.

Em alguns planos de consulta, é possível que um nó de subplano seja executado mais de uma vez. Por exemplo, a varredura do índice interno será executada uma vez por linha externa no plano acima com loop aninhado. Nesses casos, o valor `loops` relata o número total de execuções do nó, e os valores de tempo e linhas reais mostrados são médias por execução. Isso é feito para tornar os números comparáveis com a maneira como as estimativas de custo são mostradas. Multiplique pelo valor `loops` para obter o tempo total realmente gasto no nó. No exemplo acima, gastamos um total de 0,030 milissegundos executando as varreduras de índice em `tenk2`.

Em alguns casos, `EXPLAIN ANALYZE` exibe estatísticas adicionais de execução além dos tempos de execução dos nós do plano e dos contagem de linhas. Por exemplo, os nós de Ordenar e Hash fornecem informações adicionais:

```
EXPLAIN ANALYZE SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2 ORDER BY t1.fivethous;

                                                                 QUERY PLAN
-------------------------------------------------------------------​-------------------------------------------------------------------​------
 Sort  (cost=713.05..713.30 rows=100 width=488) (actual time=2.995..3.002 rows=100.00 loops=1)
   Sort Key: t1.fivethous
   Sort Method: quicksort  Memory: 74kB
   Buffers: shared hit=440
   ->  Hash Join  (cost=226.23..709.73 rows=100 width=488) (actual time=0.515..2.920 rows=100.00 loops=1)
         Hash Cond: (t2.unique2 = t1.unique2)
         Buffers: shared hit=437
         ->  Seq Scan on tenk2 t2  (cost=0.00..445.00 rows=10000 width=244) (actual time=0.026..1.790 rows=10000.00 loops=1)
               Buffers: shared hit=345
         ->  Hash  (cost=224.98..224.98 rows=100 width=244) (actual time=0.476..0.477 rows=100.00 loops=1)
               Buckets: 1024  Batches: 1  Memory Usage: 35kB
               Buffers: shared hit=92
               ->  Bitmap Heap Scan on tenk1 t1  (cost=5.06..224.98 rows=100 width=244) (actual time=0.030..0.450 rows=100.00 loops=1)
                     Recheck Cond: (unique1 < 100)
                     Heap Blocks: exact=90
                     Buffers: shared hit=92
                     ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0) (actual time=0.013..0.013 rows=100.00 loops=1)
                           Index Cond: (unique1 < 100)
                           Index Searches: 1
                           Buffers: shared hit=2
 Planning:
   Buffers: shared hit=12
 Planning Time: 0.187 ms
 Execution Time: 3.036 ms
```

O nó de Ordenação mostra o método de ordenação utilizado (em particular, se a ordenação foi em memória ou em disco) e a quantidade de memória ou espaço em disco necessária. O nó de Hash mostra o número de buckets e lotes de hash, bem como a quantidade máxima de memória usada para a tabela de hash. (Se o número de lotes exceder um, também haverá uso de espaço em disco, mas isso não é mostrado.)

Os nós de varredura de índice (assim como os nós de varredura de índice em formato de bitmap e de varredura apenas com índice) mostram uma linha de “Pesquisas de índice” que relata o número total de pesquisas em *todos* os execuções do nó/`loops`:

```
EXPLAIN ANALYZE SELECT * FROM tenk1 WHERE thousand IN (1, 500, 700, 999);
                                                            QUERY PLAN
-------------------------------------------------------------------​---------------------------------------------------------------
 Bitmap Heap Scan on tenk1  (cost=9.45..73.44 rows=40 width=244) (actual time=0.012..0.028 rows=40.00 loops=1)
   Recheck Cond: (thousand = ANY ('{1,500,700,999}'::integer[]))
   Heap Blocks: exact=39
   Buffers: shared hit=47
   ->  Bitmap Index Scan on tenk1_thous_tenthous  (cost=0.00..9.44 rows=40 width=0) (actual time=0.009..0.009 rows=40.00 loops=1)
         Index Cond: (thousand = ANY ('{1,500,700,999}'::integer[]))
         Index Searches: 4
         Buffers: shared hit=8
 Planning Time: 0.029 ms
 Execution Time: 0.034 ms
```

Aqui vemos um nó de Bitmap Index Scan que precisava de 4 pesquisas de índice separadas. O exame teve que pesquisar o índice a partir da página raiz do índice `tenk1_thous_tenthous` uma vez por cada valor de `integer` do `IN` do construtor do predicado. No entanto, o número de pesquisas de índice muitas vezes não terá uma correspondência tão simples com o predicado da consulta:

```
EXPLAIN ANALYZE SELECT * FROM tenk1 WHERE thousand IN (1, 2, 3, 4);
                                                            QUERY PLAN
-------------------------------------------------------------------​---------------------------------------------------------------
 Bitmap Heap Scan on tenk1  (cost=9.45..73.44 rows=40 width=244) (actual time=0.009..0.019 rows=40.00 loops=1)
   Recheck Cond: (thousand = ANY ('{1,2,3,4}'::integer[]))
   Heap Blocks: exact=38
   Buffers: shared hit=40
   ->  Bitmap Index Scan on tenk1_thous_tenthous  (cost=0.00..9.44 rows=40 width=0) (actual time=0.005..0.005 rows=40.00 loops=1)
         Index Cond: (thousand = ANY ('{1,2,3,4}'::integer[]))
         Index Searches: 1
         Buffers: shared hit=2
 Planning Time: 0.029 ms
 Execution Time: 0.026 ms
```

Esta variante da nossa consulta `IN` realizou apenas uma pesquisa de índice. Gastou menos tempo percorrendo o índice (em comparação com a consulta original) porque sua construção `IN` usa valores que correspondem a tuplas de índice armazenadas uma ao lado da outra, na mesma página da folha de índice `tenk1_thous_tenthous`.

A linha "Pesquisa de índice" também é útil com varreduras de índice de árvore B que aplicam a otimização de *varredura de salto* para percorrer de forma mais eficiente um índice:

```
EXPLAIN ANALYZE SELECT four, unique1 FROM tenk1 WHERE four BETWEEN 1 AND 3 AND unique1 = 42;
                                                              QUERY PLAN
-------------------------------------------------------------------​---------------------------------------------------------------
 Index Only Scan using tenk1_four_unique1_idx on tenk1  (cost=0.29..6.90 rows=1 width=8) (actual time=0.006..0.007 rows=1.00 loops=1)
   Index Cond: ((four >= 1) AND (four <= 3) AND (unique1 = 42))
   Heap Fetches: 0
   Index Searches: 3
   Buffers: shared hit=7
 Planning Time: 0.029 ms
 Execution Time: 0.012 ms
```

Aqui vemos um nó de varredura apenas por índice usando `tenk1_four_unique1_idx`, um índice de múltiplas colunas na coluna `four` e `unique1` da tabela `tenk1`. A varredura realiza 3 pesquisas que leem cada uma uma única página de folha do índice: “`four = 1 AND unique1 = 42`”, “`four = 2 AND unique1 = 42`” e “`four = 3 AND unique1 = 42`”. Este índice é geralmente um bom alvo para varredura de salto, pois, conforme discutido em [Seção 11.3][(indexes-multicolumn.md "11.3. Multicolumn Indexes")], sua coluna principal (a coluna `four`) contém apenas 4 valores distintos, enquanto sua segunda/última coluna (a coluna `unique1`) contém muitos valores distintos.

Outro tipo de informação adicional é o número de linhas removidas por uma condição de filtro:

```
EXPLAIN ANALYZE SELECT * FROM tenk1 WHERE ten < 7;

                                               QUERY PLAN
-------------------------------------------------------------------​--------------------------------------
 Seq Scan on tenk1  (cost=0.00..470.00 rows=7000 width=244) (actual time=0.030..1.995 rows=7000.00 loops=1)
   Filter: (ten < 7)
   Rows Removed by Filter: 3000
   Buffers: shared hit=345
 Planning Time: 0.102 ms
 Execution Time: 2.145 ms
```

Esses contagem podem ser particularmente valiosos para condições de filtro aplicadas em nós de junção. A linha "Linhas Removidas" só aparece quando pelo menos uma linha digitalizada, ou um par potencial de junção, no caso de um nó de junção, é rejeitada pela condição do filtro.

Um caso semelhante às condições de filtro ocorre com varreduras de índice "perdas" (lossy). Por exemplo, considere esta busca por polígonos que contenham um ponto específico:

```
EXPLAIN ANALYZE SELECT * FROM polygon_tbl WHERE f1 @> polygon '(0.5,2.0)';

                                              QUERY PLAN
-------------------------------------------------------------------​-----------------------------------
 Seq Scan on polygon_tbl  (cost=0.00..1.09 rows=1 width=85) (actual time=0.023..0.023 rows=0.00 loops=1)
   Filter: (f1 @> '((0.5,2))'::polygon)
   Rows Removed by Filter: 7
   Buffers: shared hit=1
 Planning Time: 0.039 ms
 Execution Time: 0.033 ms
```

O planejador pensa (com toda a razão) que essa tabela de amostra é muito pequena para se preocupar com uma varredura de índice, então temos uma varredura sequencial simples na qual todas as linhas foram rejeitadas pela condição do filtro. Mas se forçarmos a utilização de uma varredura de índice, vemos:

```
SET enable_seqscan TO off;

EXPLAIN ANALYZE SELECT * FROM polygon_tbl WHERE f1 @> polygon '(0.5,2.0)';

                                                        QUERY PLAN
-------------------------------------------------------------------​-------------------------------------------------------
 Index Scan using gpolygonind on polygon_tbl  (cost=0.13..8.15 rows=1 width=85) (actual time=0.074..0.074 rows=0.00 loops=1)
   Index Cond: (f1 @> '((0.5,2))'::polygon)
   Rows Removed by Index Recheck: 1
   Index Searches: 1
   Buffers: shared hit=1
 Planning Time: 0.039 ms
 Execution Time: 0.098 ms
```

Aqui podemos ver que o índice retornou uma linha de candidato, que foi rejeitada por uma revalidação da condição do índice. Isso acontece porque um índice GiST é "perda" para testes de contenção de polígonos: ele realmente retorna as linhas com polígonos que se sobrepõem ao alvo, e então temos que fazer o teste de contenção exato nessas linhas.

`EXPLAIN` tem uma opção `BUFFERS` que fornece detalhes adicionais sobre as operações de I/O realizadas durante o planejamento e execução da consulta dada. Os números dos buffers exibidos mostram o número de buffers não distintos encontrados, lidos, mantidos sujos e escritos para o nó dado e todos os seus nós filhos. A opção `ANALYZE` habilita implicitamente a opção `BUFFERS`. Se isso não for desejado, `BUFFERS` pode ser explicitamente desativado:

```
EXPLAIN (ANALYZE, BUFFERS OFF) SELECT * FROM tenk1 WHERE unique1 < 100 AND unique2 > 9000;

                                                           QUERY PLAN
-------------------------------------------------------------------​--------------------------------------------------------------
 Bitmap Heap Scan on tenk1  (cost=25.07..60.11 rows=10 width=244) (actual time=0.105..0.114 rows=10.00 loops=1)
   Recheck Cond: ((unique1 < 100) AND (unique2 > 9000))
   Heap Blocks: exact=10
   ->  BitmapAnd  (cost=25.07..25.07 rows=10 width=0) (actual time=0.100..0.101 rows=0.00 loops=1)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0) (actual time=0.027..0.027 rows=100.00 loops=1)
               Index Cond: (unique1 < 100)
               Index Searches: 1
         ->  Bitmap Index Scan on tenk1_unique2  (cost=0.00..19.78 rows=999 width=0) (actual time=0.070..0.070 rows=999.00 loops=1)
               Index Cond: (unique2 > 9000)
               Index Searches: 1
 Planning Time: 0.162 ms
 Execution Time: 0.143 ms
```

Tenha em mente que, como o `EXPLAIN ANALYZE` realmente executa a consulta, quaisquer efeitos colaterais ocorrerão como de costume, embora quaisquer resultados que a consulta possa produzir sejam descartados em favor da impressão dos dados do `EXPLAIN`. Se você deseja analisar uma consulta que modifica dados sem alterar suas tabelas, pode desfazer o comando posteriormente, por exemplo:

```
BEGIN;

EXPLAIN ANALYZE UPDATE tenk1 SET hundred = hundred + 1 WHERE unique1 < 100;

                                                           QUERY PLAN
-------------------------------------------------------------------​-------------------------------------------------------------
 Update on tenk1  (cost=5.06..225.23 rows=0 width=0) (actual time=1.634..1.635 rows=0.00 loops=1)
   ->  Bitmap Heap Scan on tenk1  (cost=5.06..225.23 rows=100 width=10) (actual time=0.065..0.141 rows=100.00 loops=1)
         Recheck Cond: (unique1 < 100)
         Heap Blocks: exact=90
         Buffers: shared hit=4 read=2
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0) (actual time=0.031..0.031 rows=100.00 loops=1)
               Index Cond: (unique1 < 100)
               Index Searches: 1
               Buffers: shared read=2
 Planning Time: 0.151 ms
 Execution Time: 1.856 ms

ROLLBACK;
```

Como visto neste exemplo, quando a consulta é um comando `INSERT`, `UPDATE`, `DELETE` ou `MERGE`, o trabalho real de aplicação das alterações da tabela é realizado por um nó de plano de inserção, atualização, exclusão ou fusão de nível superior. Os nós de plano abaixo deste nó realizam o trabalho de localizar as linhas antigas e/ou calcular os novos dados. Assim, acima, vemos o mesmo tipo de varredura de tabela em bitmap que já vimos antes, e sua saída é alimentada para um nó de atualização que armazena as linhas atualizadas. Vale ressaltar que, embora o nó que modifica os dados possa levar uma quantidade considerável de tempo de execução (aqui, está consumindo a maior parte do tempo), o planejador atualmente não adiciona nada às estimativas de custo para contabilizar esse trabalho. Isso ocorre porque o trabalho a ser realizado é o mesmo para todos os planos de consulta corretos, então isso não afeta as decisões de planejamento.

Quando um comando `UPDATE`, `DELETE` ou `MERGE` afeta uma tabela particionada ou uma hierarquia de herança, o resultado pode parecer assim:

```
EXPLAIN UPDATE gtest_parent SET f1 = CURRENT_DATE WHERE f2 = 101;

                                       QUERY PLAN
-------------------------------------------------------------------​---------------------
 Update on gtest_parent  (cost=0.00..3.06 rows=0 width=0)
   Update on gtest_child gtest_parent_1
   Update on gtest_child2 gtest_parent_2
   Update on gtest_child3 gtest_parent_3
   ->  Append  (cost=0.00..3.06 rows=3 width=14)
         ->  Seq Scan on gtest_child gtest_parent_1  (cost=0.00..1.01 rows=1 width=14)
               Filter: (f2 = 101)
         ->  Seq Scan on gtest_child2 gtest_parent_2  (cost=0.00..1.01 rows=1 width=14)
               Filter: (f2 = 101)
         ->  Seq Scan on gtest_child3 gtest_parent_3  (cost=0.00..1.01 rows=1 width=14)
               Filter: (f2 = 101)
```

Neste exemplo, o nó Atualizar precisa considerar três tabelas filhas, mas não a tabela particionada originalmente mencionada (já que ela nunca armazena nenhum dado). Portanto, há três subplanos de varredura de entrada, um para cada tabela. Para maior clareza, o nó Atualizar é anotado para mostrar as tabelas-alvo específicas que serão atualizadas, na mesma ordem que os subplanos correspondentes.

O `Planning time` mostrado pelo `EXPLAIN ANALYZE` é o tempo que levou para gerar o plano de consulta a partir da consulta analisada e otimizá-lo. Não inclui análise ou reescrita.

O `Execution time` mostrado pelo `EXPLAIN ANALYZE` inclui o tempo de início e fim do executor, bem como o tempo para executar quaisquer gatilhos que sejam disparados, mas não inclui tempo de análise, reescrita ou planejamento. O tempo gasto na execução de gatilhos `BEFORE`, se houver, é incluído no tempo para o nó relacionado de Inserir, Atualizar ou Deletar; mas o tempo gasto na execução de gatilhos `AFTER` não é contado lá porque os gatilhos `AFTER` são disparados após a conclusão do plano inteiro. O tempo total gasto em cada gatilho (seja `BEFORE` ou `AFTER`) também é mostrado separadamente. Note que os gatilhos de restrição diferida não serão executados até o final da transação e, portanto, não são considerados de forma alguma pelo `EXPLAIN ANALYZE`.

O tempo mostrado para o nó de nível superior não inclui qualquer tempo necessário para converter os dados de saída da consulta em formato exibível ou para enviá-los ao cliente. Embora o `EXPLAIN ANALYZE` nunca envie os dados ao cliente, ele pode ser orientado a converter os dados de saída da consulta em formato exibível e medir o tempo necessário para isso, especificando a opção `SERIALIZE`. Esse tempo será mostrado separadamente e também está incluído no total `Execution time`.

### 14.1.3. Avisos [#](#USING-EXPLAIN-CAVEATS)

Existem duas maneiras significativas pelas quais os tempos de execução medidos por `EXPLAIN ANALYZE` podem se desviar da execução normal da mesma consulta. Primeiro, uma vez que nenhuma linha de saída é entregue ao cliente, os custos de transmissão de rede não são incluídos. Os custos de conversão de I/O também não são incluídos, a menos que `SERIALIZE` seja especificado. Em segundo lugar, o custo adicional de medição adicionado por `EXPLAIN ANALYZE` pode ser significativo, especialmente em máquinas com chamadas de sistema operacional `gettimeofday()` que operam lentamente. Você pode usar a ferramenta [pg_test_timing][(pgtesttiming.md "pg_test_timing")] para medir o custo de temporização em seu sistema.

Os resultados do `EXPLAIN` não devem ser extrapolados para situações muito diferentes daquela que você está realmente testando; por exemplo, os resultados em uma mesa do tamanho de um brinquedo não podem ser assumidos como aplicáveis a mesas grandes. As estimativas de custo do planejador não são lineares, e, portanto, ele pode escolher um plano diferente para uma mesa maior ou menor. Um exemplo extremo é que, em uma mesa que ocupa apenas uma página de disco, você quase sempre obterá um plano de varredura sequencial, independentemente de índices estarem disponíveis ou não. O planejador percebe que vai levar uma leitura de uma página de disco para processar a tabela de qualquer maneira, então não há valor em gastar leituras adicionais de página para olhar um índice. (Vimos isso acontecendo no exemplo acima do `polygon_tbl`.)

Existem casos em que os valores reais e estimados não se correspondem bem, mas nada realmente está errado. Um desses casos ocorre quando a execução do nó do plano é interrompida precocemente por um efeito `LIMIT` ou semelhante. Por exemplo, na consulta `LIMIT` que usamos anteriormente,

```
EXPLAIN ANALYZE SELECT * FROM tenk1 WHERE unique1 < 100 AND unique2 > 9000 LIMIT 2;

                                                          QUERY PLAN
-------------------------------------------------------------------​------------------------------------------------------------
 Limit  (cost=0.29..14.33 rows=2 width=244) (actual time=0.051..0.071 rows=2.00 loops=1)
   Buffers: shared hit=16
   ->  Index Scan using tenk1_unique2 on tenk1  (cost=0.29..70.50 rows=10 width=244) (actual time=0.051..0.070 rows=2.00 loops=1)
         Index Cond: (unique2 > 9000)
         Filter: (unique1 < 100)
         Rows Removed by Filter: 287
         Index Searches: 1
         Buffers: shared hit=16
 Planning Time: 0.077 ms
 Execution Time: 0.086 ms
```

o custo estimado e o número de linhas para o nó de varredura do índice são mostrados como se ele tivesse sido executado até o final. Mas, na realidade, o nó Limite parou de solicitar linhas depois de receber duas, então o número real de linhas é apenas 2 e o tempo de execução é menos do que o que a estimativa sugere. Isso não é um erro de estimativa, apenas uma discrepância na forma como as estimativas e os valores verdadeiros são exibidos.

As junções de fusão também têm artefatos de medição que podem confundir quem não está atento. Uma junção de fusão parará de ler uma entrada se tiver esgotado a outra entrada e o próximo valor da chave naquela entrada for maior que o último valor da chave da outra entrada; nesse caso, não pode haver mais correspondências e, portanto, não há necessidade de analisar o restante da primeira entrada. Isso resulta em não ler todas as crianças, com resultados como os mencionados para `LIMIT`. Além disso, se a criança externa (primeira) contiver linhas com valores de chave duplicados, a criança interna (segunda) é copiada e reanalisada para a porção de suas linhas que correspondem a esse valor de chave. `EXPLAIN ANALYZE` conta essas emissões repetidas das mesmas linhas internas como se fossem verdadeiras linhas adicionais. Quando há muitos duplicados externos, o número real de linhas relatado para o nó de plano da criança interna pode ser significativamente maior que o número de linhas que estão realmente na relação interna.

Os nós BitmapAnd e BitmapOr sempre relatam seus contos reais de linha como zero, devido a limitações de implementação.

Normalmente, `EXPLAIN` exibirá cada nó de plano criado pelo planejador. No entanto, há casos em que o executor pode determinar que certos nós não precisam ser executados porque não podem produzir quaisquer linhas, com base em valores de parâmetro que não estavam disponíveis no momento do planejamento. (Atualmente, isso só pode acontecer para nós filhos de um nó de Aplicar ou AplicarAppend que está digitalizando uma tabela dividida.) Quando isso acontece, esses nós de plano são omitidos da saída do `EXPLAIN` e uma anotação `Subplans Removed: N` aparece em vez disso.