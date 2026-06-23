## REINDEX

REINDEX — reconstruir índices

## Sinopse

```
REINDEX [ ( option [, ...] ) ] { INDEX | TABLE | SCHEMA } [ CONCURRENTLY ] name
REINDEX [ ( option [, ...] ) ] { DATABASE | SYSTEM } [ CONCURRENTLY ] [ name ]

where option can be one of:

    CONCURRENTLY [ boolean ]
    TABLESPACE new_tablespace
    VERBOSE [ boolean ]
```

## Descrição

`REINDEX` reconstrui um índice usando os dados armazenados na tabela do índice, substituindo a cópia antiga do índice. Existem vários cenários em que se pode usar `REINDEX`:

* Um índice tornou-se corrompido e já não contém dados válidos. Embora, em teoria, isso nunca deva acontecer, na prática, os índices podem se corromper devido a erros de software ou falhas de hardware. `REINDEX` fornece um método de recuperação.
* Um índice tornou-se "inchado", ou seja, contém muitas páginas vazias ou quase vazias. Isso pode ocorrer com índices de árvore B no PostgreSQL em determinados padrões de acesso incomuns. `REINDEX` fornece uma maneira de reduzir o consumo de espaço do índice, escrevendo uma nova versão do índice sem as páginas mortas. Consulte [Seção 24.2](routine-reindex.md) para mais informações.
* Você alterou um parâmetro de armazenamento (como fillfactor) para um índice e deseja garantir que a alteração tenha surtido efeito completo.
* Se uma construção de índice falhar com a opção `CONCURRENTLY`, esse índice é deixado como "inválido". Tais índices são inúteis, mas pode ser conveniente usar `REINDEX` para reconstruí-los. Note que apenas `REINDEX INDEX` é capaz de realizar uma construção concorrente em um índice inválido.

## Parâmetros

`INDEX`: Recrie o índice especificado. Esta forma de `REINDEX` não pode ser executada dentro de um bloco de transação quando usada com um índice particionado.

`TABLE`: Recrie todos os índices da tabela especificada. Se a tabela tiver uma tabela secundária "TOAST", ela também será reindexada. Esta forma de `REINDEX` não pode ser executada dentro de um bloco de transação quando usada com uma tabela particionada.

`SCHEMA`: Recrie todos os índices do esquema especificado. Se uma tabela desse esquema tiver uma tabela secundária "TOAST", ela também será reindexada. Os índices em catálogos de sistema compartilhados também são processados. Esta forma de `REINDEX` não pode ser executada dentro de um bloco de transação.

`DATABASE`: Recrie todos os índices dentro do banco de dados atual, exceto os catálogos do sistema. Os índices nos catálogos do sistema não são processados. Esta forma de `REINDEX` não pode ser executada dentro de um bloco de transação.

`SYSTEM`: Recrie todos os índices nos catálogos do sistema dentro do banco de dados atual. Os índices nos catálogos de sistema compartilhados são incluídos. Os índices nas tabelas de usuário não são processados. Esta forma de `REINDEX` não pode ser executada dentro de um bloco de transação.

*`name`*: O nome do índice, tabela ou banco de dados específico que será reindexado. Os nomes de índice e tabela podem ser qualificados pelo esquema. Atualmente, `REINDEX DATABASE` e `REINDEX SYSTEM` só podem reindexar o banco de dados atual. Seu parâmetro é opcional e deve corresponder ao nome do banco de dados atual.

`CONCURRENTLY`: Quando esta opção é usada, o PostgreSQL reconstruirá o índice sem tomar quaisquer bloqueios que impeçam inserções, atualizações ou exclusões concorrentes na tabela; enquanto um reconstrução de índice padrão bloqueia as escritas (mas não as leituras) na tabela até que ela esteja pronta. Há várias advertências a serem consideradas ao usar esta opção — veja [Reconstrução de índices concorrentemente](sql-reindex.md#SQL-REINDEX-CONCURRENTLY) abaixo.

Para tabelas temporárias, `REINDEX` é sempre não concorrente, pois nenhuma outra sessão pode acessá-las, e o reindex não concorrente é mais barato.

`TABLESPACE`: Especifica que os índices serão reconstruídos em um novo espaço de tabelas.

`VERBOSE`: Imprime um relatório de progresso à medida que cada índice é reindexado no nível `INFO`.

*`boolean`*: Especifica se a opção selecionada deve ser ativada ou desativada. Você pode escrever `TRUE`, `ON` ou `1` para ativar a opção e `FALSE`, `OFF` ou `0` para desativá-la. O valor *`boolean`* também pode ser omitido, no qual caso `TRUE` é assumido.

*`new_tablespace`*: O tablespace onde os índices serão reconstruídos.

## Notas

Se você suspeitar que um índice em uma tabela de usuários esteja corrompido, você pode simplesmente reconstruí-lo, ou todos os índices na tabela, usando `REINDEX INDEX` ou `REINDEX TABLE`.

As coisas são mais difíceis se você precisar recuperar de uma corrupção de um índice em uma tabela do sistema. Neste caso, é importante que o sistema não tenha usado nenhum dos índices suspeitos. (De fato, neste tipo de cenário, você pode descobrir que os processos do servidor estão travando imediatamente no início, devido à dependência dos índices corrompidos.) Para recuperar com segurança, o servidor deve ser iniciado com a opção `-P`, que o impede de usar índices para pesquisas no catálogo do sistema.

Uma maneira de fazer isso é desligar o servidor e iniciar um servidor PostgreSQL de usuário único com a opção `-P` incluída em sua linha de comando. Em seguida, `REINDEX DATABASE`, `REINDEX SYSTEM`, `REINDEX TABLE` ou `REINDEX INDEX` pode ser emitido, dependendo de quanto você deseja reconstruir. Se houver dúvida, use `REINDEX SYSTEM` para selecionar a reconstrução de todos os índices do sistema no banco de dados. Em seguida, encerre a sessão do servidor de usuário único e reinicie o servidor regular. Consulte a página de referência [postgres](app-postgres.md) para obter mais informações sobre como interagir com a interface do servidor de usuário único.

Alternativamente, uma sessão regular do servidor pode ser iniciada com `-P` incluído em suas opções de linha de comando. O método para fazer isso varia entre os clientes, mas em todos os clientes baseados em libpq, é possível definir a variável de ambiente `PGOPTIONS` para `-P` antes de iniciar o cliente. Note que, embora este método não exija o bloqueio de outros clientes, ainda pode ser prudente impedir que outros usuários se conectem ao banco de dados danificado até que as reparações tenham sido concluídas.

`REINDEX` é semelhante a uma queda e uma recriação do índice, pois o conteúdo do índice é reconstruído do zero. No entanto, as considerações de bloqueio são bastante diferentes. `REINDEX` bloqueia a escrita, mas não as leituras da tabela pai do índice. Ele também assume um bloqueio `ACCESS EXCLUSIVE` no índice específico que está sendo processado, o que bloqueará leituras que tentam usar esse índice. Em particular, o planejador de consulta tenta assumir um bloqueio `ACCESS SHARE` em todos os índices da tabela, independentemente da consulta, e assim `REINDEX` bloqueia praticamente todas as consultas, exceto algumas consultas preparadas cujo plano foi armazenado na cache e que não usam esse índice específico. Em contraste, `DROP INDEX` assume momentaneamente um bloqueio `ACCESS EXCLUSIVE` na tabela pai, bloqueando tanto a escrita quanto a leitura. Os bloqueios subsequentes `CREATE INDEX` bloqueiam a escrita, mas não as leituras; como o índice não está presente, nenhuma leitura tentará usá-lo, o que significa que não haverá bloqueio, mas as leituras podem ser forçadas a realizar escansos sequenciais caros.

Enquanto o `REINDEX` está em execução, o [search_path](runtime-config-client.md#GUC-SEARCH-PATH) é temporariamente alterado para `pg_catalog, pg_temp`.

Reindexar um único índice ou tabela requer ter o privilégio `MAINTAIN` na tabela. Note que, embora o `REINDEX` em um índice ou tabela particionada exija ter o privilégio `MAINTAIN` na tabela particionada, esses comandos ignoram as verificações de privilégio ao processar as partições individuais. Reindexar um esquema ou banco de dados requer ser o proprietário desse esquema ou banco de dados ou ter privilégios do papel [pg_maintain](predefined-roles.md#PREDEFINED-ROLE-PG-MAINTAIN). Note especificamente que, portanto, é possível que usuários não superusuários reconstruam índices de tabelas de outros usuários. No entanto, como exceção especial, `REINDEX DATABASE`, `REINDEX SCHEMA` e `REINDEX SYSTEM` ignorarão índices em catálogos compartilhados, a menos que o usuário tenha o privilégio `MAINTAIN` no catálogo.

A reindexação de índices particionados ou tabelas particionadas é suportada com `REINDEX INDEX` ou `REINDEX TABLE`, respectivamente. Cada partição da relação particionada especificada é reindexada em uma transação separada. Esses comandos não podem ser usados dentro de um bloco de transação ao trabalhar em uma tabela ou índice particionado.

Ao usar a cláusula `TABLESPACE` com `REINDEX` em um índice particionado ou tabela, apenas as referências do espaço de tabelas das partições de folha são atualizadas. Como os índices particionados não são atualizados, é recomendável usar separadamente `ALTER TABLE ONLY` neles, para que quaisquer novas partições anexadas herdem o novo espaço de tabelas. Em caso de falha, pode não ter movido todos os índices para o novo espaço de tabelas. Refazer o comando reconstruirá todas as partições de folha e moverá os índices que não foram processados anteriormente para o novo espaço de tabelas.

Se `SCHEMA`, `DATABASE` ou `SYSTEM` for usado com `TABLESPACE`, as relações do sistema são ignoradas e um único `WARNING` será gerado. Os índices nas tabelas TOAST são reconstruídos, mas não movidos para o novo espaço de tabela.

### Rebuilding Indexes Concurrently

A reconstrução de um índice pode interferir no funcionamento regular de um banco de dados. Normalmente, o PostgreSQL bloqueia a tabela cuja indexação é reconstruída contra as escritas e realiza a construção completa do índice com uma única varredura da tabela. Outras transações ainda podem ler a tabela, mas se tentarem inserir, atualizar ou excluir linhas na tabela, elas serão bloqueadas até que a reconstrução do índice seja concluída. Isso pode ter um efeito grave se o sistema for um banco de dados de produção em uso. Tabelas muito grandes podem levar muitas horas para serem indexadas, e mesmo para tabelas menores, a reconstrução de um índice pode bloquear escritores por períodos que são inacreditavelmente longos para um sistema de produção.

O PostgreSQL suporta a reconstrução de índices com bloqueio mínimo de escrita. Esse método é invocado especificando a opção `CONCURRENTLY` de `REINDEX`. Quando essa opção é usada, o PostgreSQL deve realizar duas varreduras da tabela para cada índice que precisa ser reconstruído e esperar pelo término de todas as transações existentes que possam potencialmente usar o índice. Esse método requer mais trabalho total do que a reconstrução padrão de índice e leva significativamente mais tempo para ser concluído, pois precisa esperar por transações inacabadas que podem modificar o índice. No entanto, uma vez que permite que operações normais continuem enquanto o índice está sendo reconstruído, esse método é útil para a reconstrução de índices em um ambiente de produção. Claro, o carregamento extra de CPU, memória e I/O imposto pela reconstrução do índice pode desacelerar outras operações.

Os seguintes passos ocorrem em um reindexação concorrente. Cada passo é executado em uma transação separada. Se houver vários índices a serem reconstruídos, cada passo percorre todos os índices antes de passar para o próximo passo.

1. Uma nova definição de índice transitório é adicionada ao catálogo `pg_index`. Esta definição será usada para substituir o índice antigo. Um bloqueio `SHARE UPDATE EXCLUSIVE` no nível de sessão é realizado nos índices que estão sendo reindexados, bem como nas tabelas associadas, para evitar qualquer modificação do esquema durante o processamento.
2. Uma primeira passagem é feita para construir o índice para cada novo índice. Uma vez que o índice é construído, sua bandeira `pg_index.indisready` é alterada para “true” para torná-lo pronto para inserções, tornando-o visível para outras sessões uma vez que a transação que realizou a construção esteja concluída. Essa etapa é realizada em uma transação separada para cada índice.
3. Em seguida, uma segunda passagem é realizada para adicionar tuplas que foram adicionadas enquanto a primeira passagem estava em execução. Essa etapa também é realizada em uma transação separada para cada índice.
4. Todas as restrições que se referem ao índice são alteradas para se referirem à nova definição de índice, e os nomes dos índices são alterados. Neste ponto, `pg_index.indisvalid` é alterado para “true” para o novo índice e para “false” para o antigo, e uma invalidação de cache é realizada, causando a invalidação de todas as sessões que referenciaram o índice antigo.
5. Os índices antigos têm `pg_index.indisready` alterado para “false” para evitar quaisquer novas inserções de tuplas, após esperar que consultas que possam referenciar o índice antigo sejam concluídas.
6. Os índices antigos são descartados. Os bloqueios de sessão `SHARE UPDATE EXCLUSIVE` para os índices e a tabela são liberados.

Se um problema surgir durante a reconstrução dos índices, como uma violação de unicidade em um índice único, o comando `REINDEX` falhará, mas deixará um novo índice “inválido”, além do pré-existente. Esse índice será ignorado para fins de consulta, pois pode ser incompleto; no entanto, ainda consumirá o overhead de atualização. O comando psql `\d` reportará tal índice como `INVALID`:

```
postgres=# \d tab
       Table "public.tab"
 Column |  Type   | Modifiers
--------+---------+-----------
 col    | integer |
Indexes:
    "idx" btree (col)
    "idx_ccnew" btree (col) INVALID
```

Se o índice marcado `INVALID` estiver sufixado com `_ccnew`, então ele corresponde ao índice transitório criado durante a operação concorrente, e o método de recuperação recomendado é descartá-lo usando `DROP INDEX`, então tente `REINDEX CONCURRENTLY` novamente. Se o índice inválido estiver sufixado com `_ccold`, ele corresponde ao índice original que não pôde ser descartado; o método de recuperação recomendado é simplesmente descartar esse índice, uma vez que a reconstrução adequada foi bem-sucedida. Um número não nulo pode ser anexado ao sufixo dos nomes dos índices inválidos para mantê-los únicos, como `_ccnew1`, `_ccold2`, etc.

As construções regulares de índice permitem que outras construções regulares de índice na mesma tabela ocorram simultaneamente, mas apenas uma construção de índice concorrente pode ocorrer em uma tabela de cada vez. Em ambos os casos, nenhum outro tipo de modificação do esquema na tabela é permitido enquanto isso. Outra diferença é que um comando regular `REINDEX TABLE` ou `REINDEX INDEX` pode ser realizado dentro de um bloco de transação, mas `REINDEX CONCURRENTLY` não pode.

Como qualquer transação de longa duração, `REINDEX` em uma tabela pode afetar quais tuplos podem ser removidos por `VACUUM` concorrente em qualquer outra tabela.

`REINDEX SYSTEM` não suporta `CONCURRENTLY` porque os catálogos do sistema não podem ser reindexados simultaneamente.

Além disso, os índices para restrições de exclusão não podem ser reindexados simultaneamente. Se um índice com essa restrição for nomeado diretamente neste comando, um erro será exibido. Se uma tabela ou banco de dados com índices de restrição de exclusão for reindexada simultaneamente, esses índices serão ignorados. É possível reindexar esses índices sem a opção `CONCURRENTLY`.

Cada backend que executa `REINDEX` informará seu progresso na visualização `pg_stat_progress_create_index`. Consulte [Seção 27.4.4](progress-reporting.md#CREATE-INDEX-PROGRESS-REPORTING) para obter detalhes.

## Exemplos

Rebuilt a single index:

```
REINDEX INDEX my_index;
```

Recrie todos os índices na tabela `my_table`:

```
REINDEX TABLE my_table;
```

Recrie todos os índices em um banco de dados específico, sem confiar que os índices do sistema já sejam válidos:

```
$ export PGOPTIONS="-P"
$ psql broken_db
...
broken_db=> REINDEX DATABASE broken_db;
broken_db=> \q
```

Recrie índices para uma tabela, sem bloquear operações de leitura e escrita nas relações envolvidas enquanto o reindexação está em andamento:

```
REINDEX TABLE CONCURRENTLY my_broken_table;
```

## Compatibilidade

Não existe comando `REINDEX` no padrão SQL.

## Veja também

[Crie índice](sql-createindex.md "CREATE INDEX"), [Exclua índice](sql-dropindex.md "DROP INDEX"), [Reindex DB](app-reindexdb.md "reindexdb"), [Seção 27.4.4](progress-reporting.md#CREATE-INDEX-PROGRESS-REPORTING "27.4.4. CREATE INDEX Progress Reporting")