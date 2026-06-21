## Crie índice

CREATE INDEX — definir um novo índice

## Sinopse

```
CREATE [ UNIQUE ] INDEX [ CONCURRENTLY ] [ [ IF NOT EXISTS ] name ] ON [ ONLY ] table_name [ USING method ]
    ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass [ ( opclass_parameter = value [, ... ] ) ] ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...] )
    [ INCLUDE ( column_name [, ...] ) ]
    [ NULLS [ NOT ] DISTINCT ]
    [ WITH ( storage_parameter [= value] [, ... ] ) ]
    [ TABLESPACE tablespace_name ]
    [ WHERE predicate ]
```

## Descrição

`CREATE INDEX` constrói um índice sobre as colunas especificadas da relação especificada, que pode ser uma tabela ou uma visão materializada. Os índices são usados principalmente para melhorar o desempenho do banco de dados (embora o uso inadequado possa resultar em desempenho mais lento).

Os campos chave(s) para o índice são especificados como nomes de coluna, ou, como alternativa, como expressões escritas entre parênteses. Campos múltiplos podem ser especificados se o método de índice suportar índices de múltiplas colunas.

Um campo de índice pode ser uma expressão calculada a partir dos valores de uma ou mais colunas da linha da tabela. Esse recurso pode ser usado para obter acesso rápido aos dados com base em alguma transformação dos dados básicos. Por exemplo, um índice calculado em `upper(col)` permitiria que a cláusula `WHERE upper(col) = 'JIM'` utilizasse um índice.

O PostgreSQL oferece os métodos de índice B-tree, hash, GiST, SP-GiST, GIN e BRIN. Os usuários também podem definir seus próprios métodos de índice, mas isso é bastante complicado.

Quando a cláusula `WHERE` está presente, um *índice parcial* é criado. Um índice parcial é um índice que contém entradas apenas para uma porção de uma tabela, geralmente uma porção que é mais útil para indexação do que o resto da tabela. Por exemplo, se você tem uma tabela que contém ordens faturadas e não faturadas, onde as ordens não faturadas ocupam uma pequena fração da tabela total e, no entanto, é uma seção frequentemente usada, você pode melhorar o desempenho criando um índice apenas nessa porção. Outra aplicação possível é usar `WHERE` com `UNIQUE` para impor a unicidade sobre um subconjunto de uma tabela. Consulte [Seção 11.8](indexes-partial.md) para mais discussão.

A expressão usada na cláusula `WHERE` pode se referir apenas a colunas da tabela subjacente, mas pode usar todas as colunas, não apenas as que estão sendo indexadas. Atualmente, subconsultas e expressões agregadas também são proibidas em `WHERE`. As mesmas restrições se aplicam aos campos de índice que são expressões.

Todas as funções e operadores utilizados em uma definição de índice devem ser "imutáveis", ou seja, seus resultados devem depender apenas de seus argumentos e nunca de qualquer influência externa (como o conteúdo de outra tabela ou a hora atual). Essa restrição garante que o comportamento do índice seja bem definido. Para usar uma função definida pelo usuário em uma expressão de índice ou na cláusula `WHERE`, lembre-se de marcar a função como imutável quando ela for criada.

## Parâmetros

`UNIQUE`: Faz com que o sistema verifique valores duplicados na tabela quando o índice é criado (se os dados já existirem) e cada vez que os dados são adicionados. Tentativas de inserir ou atualizar dados que resultariam em entradas duplicadas gerarão um erro.

Restrições adicionais se aplicam quando índices únicos são aplicados a tabelas particionadas; veja [CREATE TABLE](sql-createtable.md).

`CONCURRENTLY`: Quando esta opção é usada, o PostgreSQL construirá o índice sem tomar quaisquer bloqueios que impeçam inserções, atualizações ou exclusões concorrentes na tabela; enquanto uma construção de índice padrão bloqueia as escritas (mas não as leituras) na tabela até que ela esteja pronta. Há várias advertências a serem consideradas ao usar esta opção — veja [Construção de Índices Concorrentemente](sql-createindex.md#SQL-CREATEINDEX-CONCURRENTLY) abaixo.

Para tabelas temporárias, `CREATE INDEX` é sempre não concorrente, pois nenhuma outra sessão pode acessá-las, e a criação de índices não concorrente é mais barata.

`IF NOT EXISTS`: Não exija um erro se uma relação com o mesmo nome já existir. Neste caso, é emitido um aviso. Observe que não há garantia de que o índice existente seja algo parecido com o que teria sido criado. O nome do índice é necessário quando `IF NOT EXISTS` é especificado.

`INCLUDE`: A cláusula opcional `INCLUDE` especifica uma lista de colunas que serão incluídas no índice como colunas *não-chave*. Uma coluna não-chave não pode ser usada em uma qualificação de pesquisa de varredura de índice, e é ignorada para fins de qualquer restrição de unicidade ou exclusão aplicada pelo índice. No entanto, uma varredura apenas de índice pode retornar o conteúdo de colunas não-chave sem ter que visitar a tabela do índice, uma vez que elas estão disponíveis diretamente a partir da entrada do índice. Assim, a adição de colunas não-chave permite que varreduras apenas de índice sejam usadas para consultas que, de outra forma, não as poderiam usar.

É prudente ser conservador ao adicionar colunas não-chave a um índice, especialmente colunas largas. Se um tuplo de índice exceder o tamanho máximo permitido para o tipo de índice, a inserção de dados falhará. Em qualquer caso, as colunas não-chave duplicam os dados da tabela do índice e aumentam o tamanho do índice, o que pode retardar as pesquisas. Além disso, a desduplicação B-tree nunca é usada com índices que têm uma coluna não-chave.

As colunas listadas na cláusula `INCLUDE` não precisam de classes de operador apropriadas; a cláusula pode incluir colunas cujos tipos de dados não têm classes de operador definidas para um método de acesso dado.

As expressões não são suportadas como colunas incluídas, uma vez que não podem ser usadas em varreduras apenas de índice.

Atualmente, os métodos de acesso aos índices B-tree, GiST e SP-GiST suportam essa funcionalidade. Nesses índices, os valores das colunas listados na cláusula `INCLUDE` são incluídos em tuplos de folha que correspondem a tuplos de pilha, mas não são incluídos em entradas de índice de nível superior usadas para navegação em árvore.

*`name`*: O nome do índice a ser criado. Não é possível incluir o nome do esquema aqui; o índice é sempre criado no mesmo esquema que sua tabela pai. O nome do índice deve ser distinto do nome de qualquer outra relação (tabela, sequência, índice, visão, visão materializada ou tabela externa) nesse esquema. Se o nome for omitido, o PostgreSQL escolhe um nome adequado com base no nome da tabela pai e no(s) nome(s) da coluna(s) indexada(s).

`ONLY`: Indica não recursar na criação de índices em partições, se a tabela estiver particionada. O padrão é recursar.

*`table_name`*: O nome (possivelmente qualificado por esquema) da tabela que será indexada.

*`method`*: O nome do método de índice a ser utilizado. As opções são `btree`, `hash`, `gist`, `spgist`, `gin`, `brin`, ou métodos de acesso instalados pelo usuário, como [bloom](bloom.md "F.6. bloom — bloom filter index access method"). O método padrão é `btree`.

*`column_name`*: O nome de uma coluna da tabela.

*`expression`*: Uma expressão baseada em uma ou mais colunas da tabela. A expressão geralmente deve ser escrita com as chaves ao redor, conforme mostrado na sintaxe. No entanto, as chaves podem ser omitidas se a expressão tiver a forma de uma chamada de função.

*`collation`*: O nome da correção de caracteres a ser usado para o índice. Por padrão, o índice usa a correção de caracteres declarada para a coluna que será indexada ou o resultado da expressão que será indexada. Índices com correções de caracteres não padrão podem ser úteis para consultas que envolvem expressões que usam correções de caracteres não padrão.

*`opclass`*: O nome de uma classe de operador. Veja abaixo para detalhes.

*`opclass_parameter`*: O nome de um parâmetro da classe do operador. Veja abaixo para detalhes.

`ASC`: Especifica o padrão de ordem de classificação ascendente (que é o padrão).

`DESC`: Especifica a ordem de classificação descendente.

`NULLS FIRST`: Especifica que os nulos são ordenados antes dos não nulos. Esse é o padrão quando o `DESC` é especificado.

`NULLS LAST`: Especifica que os nulos são ordenados após os não nulos. Este é o padrão quando `DESC` não é especificado.

`NULLS DISTINCT` `NULLS NOT DISTINCT`: Especifica se, para um índice único, os valores nulos devem ser considerados distintos (não iguais). O padrão é que eles sejam distintos, de modo que um índice único possa conter vários valores nulos em uma coluna.

*`storage_parameter`*: O nome de um parâmetro de armazenamento específico para um método de índice. Consulte [Parâmetros de armazenamento de índice](sql-createindex.md#SQL-CREATEINDEX-STORAGE-PARAMETERS "Index Storage Parameters") abaixo para obter detalhes.

*`tablespace_name`*: O tablespace no qual o índice será criado. Se não especificado, [default_tablespace](runtime-config-client.md#GUC-DEFAULT-TABLESPACE) é consultado, ou [temp_tablespaces](runtime-config-client.md#GUC-TEMP-TABLESPACES) para índices em tabelas temporárias.

*`predicate`*: A expressão de restrição para um índice parcial.

### Parâmetros de Armazenamento do Índice

A cláusula opcional `WITH` especifica *parâmetros de armazenamento* para o índice. Cada método de índice tem seu próprio conjunto de parâmetros de armazenamento permitidos.

Os métodos de índice B-tree, hash, GiST e SP-GiST aceitam todos esse parâmetro:

`fillfactor` (`integer`) [#](#INDEX-RELOPTION-FILLFACTOR): Controla quão cheio o método de índice tentará embalar as páginas de índice. Para árvores B, as páginas de folha são preenchidas com essa porcentagem durante a construção inicial do índice e também quando se estende o índice à direita (adicionando novos valores de chave maiores). Se as páginas posteriormente se tornarem completamente cheias, elas serão divididas, levando à fragmentação da estrutura do índice no disco. As árvores B usam um fator de preenchimento padrão de 90, mas qualquer valor inteiro de 10 a 100 pode ser selecionado.

Os índices B-tree em tabelas onde muitos insertos e/ou atualizações são previstos podem se beneficiar de configurações de fator de preenchimento mais baixas no momento `CREATE INDEX` (após o carregamento em massa na tabela). Os valores na faixa de 50 - 90 podem “suavizar” útil e naturalmente a *taxa* de divisões de página durante o início da vida do índice B-tree (reduzir o fator de preenchimento dessa forma pode até mesmo reduzir o número absoluto de divisões de página, embora esse efeito seja altamente dependente da carga de trabalho). A técnica de exclusão de índice B-tree de baixo para cima descrita em [Seção 65.1.4.2](btree.md#BTREE-DELETION) depende de ter algum espaço “extra” nas páginas para armazenar versões de tupla “extra”, e, portanto, pode ser afetada pelo fator de preenchimento (embora o efeito geralmente não seja significativo).

Em outros casos específicos, pode ser útil aumentar o fillfactor para 100 no momento `CREATE INDEX`, como uma maneira de maximizar a utilização do espaço. Você só deve considerar isso quando estiver completamente seguro de que a tabela é estática (ou seja, que ela nunca será afetada por inserções ou atualizações). Um ajuste do fillfactor de 100, caso contrário, arrisca *danificar* o desempenho: mesmo algumas atualizações ou inserções causarão um súbito surto de divisões de página.

Os outros métodos de índice utilizam o fator de preenchimento de maneiras diferentes, mas aproximadamente análogas; o fator de preenchimento padrão varia entre os métodos.

Os índices de árvore B também aceitam este parâmetro:

`deduplicate_items` (`boolean`) [#](#INDEX-RELOPTION-DEDUPLICATE-ITEMS): Controla o uso da técnica de deduplicação de árvore B descrita em [Seção 65.1.4.3](btree.md#BTREE-DEDUPLICATION "65.1.4.3. Deduplication"). Defina para `ON` ou `OFF` para habilitar ou desabilitar a otimização. ([Seção 19.1](config-setting.md "19.1. Setting Parameters") descreve que são permitidas as ortografias alternativas de `ON` e `OFF`). O padrão é `ON`.

### Nota

Desligar `deduplicate_items` através de `ALTER INDEX` impede que inserções futuras desencadeiem a deduplicação, mas, por si só, não faz com que os tuplos da lista de postagens usem a representação padrão de tupla.

Os índices GiST também aceitam este parâmetro:

`buffering` (`enum`) [#](#INDEX-RELOPTION-BUFFERING): Controla se a técnica de construção com buffer descrita em [Seção 65.2.4.1](gist.md#GIST-BUFFERING-BUILD "65.2.4.1. GiST Index Build Methods") é usada para construir o índice. Com `OFF` o bufferamento está desativado, com `ON` está ativado e com `AUTO` está inicialmente desativado, mas é ativado automaticamente assim que o tamanho do índice atinge [tamanho_cache_efetivo](runtime-config-query.md#GUC-EFFECTIVE-CACHE-SIZE). O padrão é `AUTO`. Note que, se a construção ordenada for possível, ela será usada em vez da construção com buffer, a menos que `buffering=ON` seja especificado.

Os índices GIN aceitam esses parâmetros:

`fastupdate` (`boolean`) [#](#INDEX-RELOPTION-FASTUPDATE): Controla o uso da técnica de atualização rápida descrita em [Seção 65.4.4.1](gin.md#GIN-FAST-UPDATE "65.4.4.1. GIN Fast Update Technique"). `ON` habilita a atualização rápida, `OFF` a desativa. O padrão é `ON`.

### Nota

Desligar `fastupdate` através de `ALTER INDEX` impede que futuras inserções sejam adicionadas à lista de entradas de índice pendentes, mas não apaga as entradas existentes por si só. Você pode `VACUUM` a tabela ou chamar a função `gin_clean_pending_list` posteriormente para garantir que a lista pendente seja esvaziada.

`gin_pending_list_limit` (`integer`) [#](#INDEX-RELOPTION-GIN-PENDING-LIST-LIMIT): Oprime o ajuste global de [gin_pending_list_limit](runtime-config-client.md#GUC-GIN-PENDING-LIST-LIMIT) para este índice. Este valor é especificado em kilobytes.

Os índices BRIN aceitam esses parâmetros:

`pages_per_range` (`integer`) [#](#INDEX-RELOPTION-PAGES-PER-RANGE): Define o número de blocos de tabela que compõem uma faixa de blocos para cada entrada de um índice BRIN (consulte [Seção 65.5.1] para mais detalhes). O padrão é `128`.

`autosummarize` (`boolean`) [#](#INDEX-RELOPTION-AUTOSUMMARIZE): Define se uma execução de resumo está em fila para o intervalo de página anterior sempre que uma inserção for detectada na próxima (consulte [Seção 65.5.1.1] para mais detalhes). O padrão é `off`.

### Construindo índices simultaneamente

Criar um índice pode interferir no funcionamento regular de um banco de dados. Normalmente, o PostgreSQL bloqueia a tabela que será indexada contra escritas e realiza a construção completa do índice com uma única varredura da tabela. Outras transações ainda podem ler a tabela, mas se tentarem inserir, atualizar ou excluir linhas na tabela, elas serão bloqueadas até que a construção do índice seja concluída. Isso pode ter um efeito grave se o sistema for um banco de dados de produção em uso. Tabelas muito grandes podem levar muitas horas para serem indexadas, e mesmo para tabelas menores, a construção de um índice pode bloquear escritores por períodos que são inacreditavelmente longos para um sistema de produção.

O PostgreSQL suporta a construção de índices sem bloquear as escritas. Esse método é invocado especificando a opção `CONCURRENTLY` do `CREATE INDEX`. Quando essa opção é usada, o PostgreSQL deve realizar duas varreduras na tabela e, além disso, deve esperar que todas as transações existentes que possam modificar ou usar o índice terminem. Assim, esse método requer mais trabalho total do que a construção de um índice padrão e leva significativamente mais tempo para ser concluído. No entanto, uma vez que permite que as operações normais continuem enquanto o índice é construído, esse método é útil para adicionar novos índices em um ambiente de produção. Claro, a carga extra de CPU e I/O imposta pela criação do índice pode atrasar outras operações.

Em uma construção de índice concorrente, o índice é, na verdade, inserido como um índice “inválido” nos catálogos do sistema em uma transação, e então ocorrem duas varreduras de tabela em mais duas transações. Antes de cada varredura de tabela, a construção do índice deve esperar por transações existentes que tenham modificado a tabela para terminar. Após a segunda varredura, a construção do índice deve esperar por quaisquer transações que tenham um instantâneo (ver [Capítulo 13](mvcc.md)) que antecipe a segunda varredura para terminar, incluindo transações usadas por qualquer fase de construções de índice concorrentes em outras tabelas, se os índices envolvidos forem parciais ou tiverem colunas que não são referências de coluna simples. Então, finalmente, o índice pode ser marcado como “válido” e pronto para uso, e o comando `CREATE INDEX` termina. Mesmo assim, no entanto, o índice pode não ser imediatamente utilizável para consultas: no pior dos casos, não pode ser usado enquanto existam transações que antecipem o início da construção do índice.

Se um problema surgir durante a digitalização da tabela, como um bloqueio ou uma violação de unicidade em um índice único, o comando `CREATE INDEX` falhará, mas deixará um índice “inválido”. Esse índice será ignorado para fins de consulta, pois pode ser incompleto; no entanto, ainda consumirá o overhead de atualização. O comando psql `\d` reportará tal índice como `INVALID`:

```
postgres=# \d tab
       Table "public.tab"
 Column |  Type   | Collation | Nullable | Default
--------+---------+-----------+----------+---------
 col    | integer |           |          |
Indexes:
    "idx" btree (col) INVALID
```

O método de recuperação recomendado nesses casos é descartar o índice e tentar realizar novamente o `CREATE INDEX CONCURRENTLY`. (Outra possibilidade é reconstruir o índice com `REINDEX INDEX CONCURRENTLY`).

Outro cuidado ao construir um índice único simultaneamente é que a restrição de unicidade já está sendo aplicada contra outras transações quando o segundo varredura da tabela começa. Isso significa que as violações da restrição poderiam ser relatadas em outras consultas antes que o índice se tornasse disponível para uso, ou até mesmo em casos em que a construção do índice eventualmente falhe. Além disso, se uma falha ocorrer na segunda varredura, o índice “inválido” continua a aplicar sua restrição de unicidade posteriormente.

São suportados builds concorrentes de índices de expressão e índices parciais. Erros que ocorrem na avaliação dessas expressões podem causar comportamento semelhante ao descrito acima para violações de restrição única.

As compilações regulares de índice permitem que outras compilações regulares de índice na mesma tabela ocorram simultaneamente, mas apenas uma compilação de índice concorrente pode ocorrer em uma tabela de cada vez. Em qualquer caso, a modificação do esquema da tabela não é permitida enquanto o índice está sendo construído. Outra diferença é que um comando regular `CREATE INDEX` pode ser realizado dentro de um bloco de transação, mas `CREATE INDEX CONCURRENTLY` não pode.

Atualmente, as compilações concorrentes para índices em tabelas particionadas não são suportadas. No entanto, você pode construir o índice em cada partição individualmente e, em seguida, criar o índice particionado de forma não concorrente para reduzir o tempo em que as escritas na tabela particionada serão bloqueadas. Nesse caso, a compilação do índice particionado é uma operação apenas de metadados.

## Notas

Consulte o [Capítulo 11](indexes.md) para obter informações sobre quando os índices podem ser usados, quando não são usados e em quais situações específicas eles podem ser úteis.

Atualmente, apenas os métodos de índices de coluna de múltiplas chaves, B-tree, GiST, GIN e BRIN, suportam índices de coluna de múltiplas chaves. Se pode haver múltiplas colunas de chave, isso é independente de se as colunas `INCLUDE` podem ser adicionadas ao índice. Os índices podem ter até 32 colunas, incluindo as colunas `INCLUDE`. (Esse limite pode ser alterado ao construir o PostgreSQL.) Apenas o B-tree atualmente suporta índices únicos.

Uma classe de operador com parâmetros opcionais pode ser especificada para cada coluna de um índice. A classe de operador identifica os operadores a serem usados pelo índice para aquela coluna. Por exemplo, um índice de árvore B em inteiros de quatro bytes usaria a classe `int4_ops`; essa classe de operador inclui funções de comparação para inteiros de quatro bytes. Na prática, a classe de operador padrão para o tipo de dados da coluna geralmente é suficiente. O ponto principal de ter classes de operador é que, para alguns tipos de dados, pode haver mais de uma ordem significativa. Por exemplo, podemos querer ordenar um tipo de dados de número complexo ou pelo valor absoluto ou pela parte real. Podemos fazer isso definindo duas classes de operador para o tipo de dados e, em seguida, selecionando a classe apropriada ao criar um índice. Mais informações sobre as classes de operador estão em [Seção 11.10](indexes-opclass.md) e em [Seção 36.16](xindex.md).

Quando `CREATE INDEX` é invocado em uma tabela particionada, o comportamento padrão é recurrir a todas as particionamentos para garantir que todas elas tenham índices correspondentes. Cada particionamento é verificado primeiro para determinar se um índice equivalente já existe, e, se existir, esse índice será anexado como índice de particionamento ao índice que está sendo criado, que se tornará seu índice pai. Se não existir nenhum índice correspondente, um novo índice será criado e automaticamente anexado; o nome do novo índice em cada particionamento será determinado como se nenhum nome de índice tivesse sido especificado no comando. Se a opção `ONLY` for especificada, não será feita nenhuma recursão e o índice será marcado como inválido. (`ALTER INDEX ... ATTACH PARTITION` marca o índice como válido, uma vez que todas as particionamentos adquirem índices correspondentes.) No entanto, observe que qualquer particionamento que seja criado no futuro usando `CREATE TABLE ... PARTITION OF` terá automaticamente um índice correspondente, independentemente de `ONLY` ser especificado.

Para métodos de índice que suportam varreduras ordenadas (atualmente, apenas B-tree), as cláusulas opcionais `ASC`, `DESC`, `NULLS FIRST` e/ou `NULLS LAST` podem ser especificadas para modificar a ordem de classificação do índice. Como um índice ordenado pode ser percorrido em ordem direta ou inversa, normalmente não é útil criar um índice de uma coluna `DESC`, pois essa ordem de classificação já está disponível com um índice regular. O valor dessas opções é que índices multicoluna podem ser criados que correspondem à ordem de classificação solicitada por uma consulta de ordem mista, como `SELECT ... ORDER BY x ASC, y DESC`. As opções `NULLS` são úteis se você precisar suportar o comportamento de "nulls sort low" (classificar os nulls como os últimos) em consultas que dependem de índices para evitar etapas de classificação.

O sistema coleta regularmente estatísticas sobre todas as colunas de uma tabela. Os índices não expressos recém-criados podem imediatamente usar essas estatísticas para determinar a utilidade de um índice. Para novos índices de expressão, é necessário executar `ANALYZE` ou esperar que o daemon [autovacuum](routine-vacuuming.md#AUTOVACUUM) analise a tabela para gerar estatísticas para esses índices.

Enquanto o `CREATE INDEX` está em execução, o [search_path](runtime-config-client.md#GUC-SEARCH-PATH) é temporariamente alterado para `pg_catalog, pg_temp`.

Para a maioria dos métodos de índice, a velocidade de criação de um índice depende da configuração de [maintenance_work_mem](runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM). Valores maiores reduzirão o tempo necessário para a criação do índice, desde que você não o torne maior do que a quantidade de memória realmente disponível, o que levaria a máquina a fazer trocas.

O PostgreSQL pode construir índices aproveitando múltiplos CPUs para processar as linhas da tabela mais rapidamente. Esse recurso é conhecido como *construção de índice em paralelo*. Para métodos de índice que suportam a construção de índices em paralelo (atualmente, B-tree, GIN e BRIN), `maintenance_work_mem` especifica a quantidade máxima de memória que pode ser usada por cada operação de construção de índice como um todo, independentemente de quantos processos de trabalho foram iniciados. Geralmente, um modelo de custo determina automaticamente quantas processos de trabalho devem ser solicitados, se houver.

As construções de índice paralelas podem se beneficiar do aumento de `maintenance_work_mem`, onde uma construção de índice serial equivalente verá pouco ou nenhum benefício. Note que `maintenance_work_mem` pode influenciar o número de processos de trabalho solicitados, uma vez que os trabalhadores paralelos devem ter pelo menos uma `32MB` parcela do orçamento total de `maintenance_work_mem`. Deve haver também uma parcela restante de `32MB` para o processo líder. Aumentar [max_parallel_maintenance_workers](runtime-config-resource.md#GUC-MAX-PARALLEL-MAINTENANCE-WORKERS) pode permitir que mais trabalhadores sejam usados, o que reduzirá o tempo necessário para a criação do índice, desde que a construção do índice não esteja já limitada por I/O. Claro, também deve haver capacidade de CPU suficiente que, de outra forma, ficaria inativa.

Definir um valor para `parallel_workers` via [`ALTER TABLE`](sql-altertable.md "ALTER TABLE") controla diretamente quantos processos de trabalhador paralelo serão solicitados por um `CREATE INDEX` contra a tabela. Isso elimina completamente o modelo de custo e impede que `maintenance_work_mem` afete quantos trabalhadores paralelos são solicitados. Definir `parallel_workers` para 0 via `ALTER TABLE` desabilitará a construção de índices paralelos na tabela em todos os casos.

### DICA

Você pode querer redefinir `parallel_workers` após configurá-lo como parte da configuração de uma construção de índice. Isso evita mudanças acidentais nos planos de consulta, uma vez que `parallel_workers` afeta *todas* as varreduras paralelas de tabela.

Enquanto o `CREATE INDEX` com a opção `CONCURRENTLY` suporta compilações paralelas sem restrições especiais, apenas o primeiro varredura da tabela é realizada em paralelo.

Use `DROP INDEX`(sql-dropindex.md "DROP INDEX") para remover um índice.

Como qualquer transação de longa duração, `CREATE INDEX` em uma tabela pode afetar quais tuplos podem ser removidos por `VACUUM` concorrente em qualquer outra tabela.

As versões anteriores do PostgreSQL também tinham um método de índice R-tree. Esse método foi removido porque não tinha vantagens significativas em relação ao método GiST. Se `USING rtree` for especificado, `CREATE INDEX` o interpretará como `USING gist`, para simplificar a conversão de bancos de dados antigos para GiST.

Cada backend que executa `CREATE INDEX` informará seu progresso na visualização `pg_stat_progress_create_index`. Consulte [Seção 27.4.4](progress-reporting.md#CREATE-INDEX-PROGRESS-REPORTING) para obter detalhes.

## Exemplos

Para criar um índice de árvore B único na coluna `title` na tabela `films`:

```
CREATE UNIQUE INDEX title_idx ON films (title);
```

Para criar um índice de árvore B único na coluna `title` com as colunas incluídas `director` e `rating` na tabela `films`:

```
CREATE UNIQUE INDEX title_idx ON films (title) INCLUDE (director, rating);
```

Para criar um índice B-Tree com desduplicação desativada:

```
CREATE INDEX title_idx ON films (title) WITH (deduplicate_items = off);
```

Para criar um índice na expressão `lower(title)`, permitindo pesquisas eficientes que não são sensíveis ao caso:

```
CREATE INDEX ON films ((lower(title)));
```

(Neste exemplo, escolhemos omitir o nome do índice, de modo que o sistema escolha um nome, tipicamente `films_lower_idx`).

Para criar um índice com uma ordem de classificação não padrão:

```
CREATE INDEX title_idx_german ON films (title COLLATE "de_DE");
```

Para criar um índice com uma ordem de classificação não padrão de nulos:

```
CREATE INDEX title_idx_nulls_low ON films (title NULLS FIRST);
```

Para criar um índice com fator de preenchimento não padrão:

```
CREATE UNIQUE INDEX title_idx ON films (title) WITH (fillfactor = 70);
```

Para criar um índice GIN com atualizações rápidas desativadas:

```
CREATE INDEX gin_idx ON documents_table USING GIN (locations) WITH (fastupdate = off);
```

Para criar um índice na coluna `code` na tabela `films` e fazer com que o índice resida no espaço de tabelas `indexspace`:

```
CREATE INDEX code_idx ON films (code) TABLESPACE indexspace;
```

Para criar um índice GiST em um atributo pontual, para que possamos utilizar eficientemente operadores de caixa no resultado da função de conversão:

```
CREATE INDEX pointloc
    ON points USING gist (box(location,location));
SELECT * FROM points
    WHERE box(location,location) && '(0,0),(1,1)'::box;
```

Para criar um índice sem bloquear as escritas na tabela:

```
CREATE INDEX CONCURRENTLY sales_quantity_index ON sales_table (quantity);
```

## Compatibilidade

`CREATE INDEX` é uma extensão de linguagem do PostgreSQL. Não há disposições para índices no padrão SQL.

## Veja também

[ALTERAR ÍNDICE](sql-alterindex.md "ALTER INDEX"), [DROP ÍNDICE](sql-dropindex.md "DROP INDEX"), [REINDEX](sql-reindex.md "REINDEX"), [Seção 27.4.4](progress-reporting.md#CREATE-INDEX-PROGRESS-REPORTING "27.4.4. CREATE INDEX Progress Reporting")