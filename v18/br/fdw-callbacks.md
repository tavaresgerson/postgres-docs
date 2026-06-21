## 58.2. Rotinas de chamada de retorno do Wrapper de dados estrangeiro [#](#FDW-CALLBACKS)

* [58.2.1. Rotinas FDW para Escaneamento de Tabelas Estrangeiras](fdw-callbacks.md#FDW-CALLBACKS-SCAN)
* [58.2.2. Rotinas FDW para Escaneamento de Conexões Estrangeiras](fdw-callbacks.md#FDW-CALLBACKS-JOIN-SCAN)
* [58.2.3. Rotinas FDW para Planejamento do Processamento Pós-Escaneio/Conexão](fdw-callbacks.md#FDW-CALLBACKS-UPPER-PLANNING)
* [58.2.4. Rotinas FDW para Atualização de Tabelas Estrangeiras](fdw-callbacks.md#FDW-CALLBACKS-UPDATE)
* [58.2.5. Rotinas FDW para `TRUNCATE`](fdw-callbacks.md#FDW-CALLBACKS-TRUNCATE)
* [58.2.6. Rotinas FDW para Bloqueio de Linhas](fdw-callbacks.md#FDW-CALLBACKS-ROW-LOCKING)
* [58.2.7. Rotinas FDW para `EXPLAIN`](fdw-callbacks.md#FDW-CALLBACKS-EXPLAIN)
* [58.2.8. Rotinas FDW para `ANALYZE`](fdw-callbacks.md#FDW-CALLBACKS-ANALYZE)
* [58.2.9. Rotinas FDW para `IMPORT FOREIGN SCHEMA`](fdw-callbacks.md#FDW-CALLBACKS-IMPORT)
* [58.2.10. Rotinas FDW para Execução Paralela](fdw-callbacks.md#FDW-CALLBACKS-PARALLEL)
* [58.2.11. Rotinas FDW para Execução Assíncrona](fdw-callbacks.md#FDW-CALLBACKS-ASYNC)
* [58.2.12. Rotinas FDW para Reparametrização de Caminhos](fdw-callbacks.md#FDW-CALLBACKS-REPARAMETERIZE-PATHS)

A função handler de FDW retorna uma estrutura `FdwRoutine` palloc, contendo ponteiros para as funções de callback descritas abaixo. As funções relacionadas à varredura são necessárias, o restante é opcional.

O tipo de estrutura `FdwRoutine` é declarado em `src/include/foreign/fdwapi.h`, que pode ser consultado para obter detalhes adicionais.

### 58.2.1. Rotinas FDW para varredura de tabelas estrangeiras [#](#FDW-CALLBACKS-SCAN)

```
void
GetForeignRelSize(PlannerInfo *root,
                  RelOptInfo *baserel,
                  Oid foreigntableid);
```

Obtenha estimativas do tamanho da relação para uma tabela estrangeira. Isso é feito no início do planejamento de uma consulta que digitaliza uma tabela estrangeira. `root` é a informação global do planejador sobre a consulta; `baserel` é a informação do planejador sobre essa tabela; e `foreigntableid` é o OID `pg_class` da tabela estrangeira. (`foreigntableid` pode ser obtido das estruturas de dados do planejador, mas é passado explicitamente para economizar esforço.)

Essa função deve atualizar `baserel->rows` para ser o número esperado de linhas devolvidas pelo varrimento da tabela, após contabilizar o filtro realizado pelos quals de restrição. O valor inicial de `baserel->rows` é apenas uma estimativa constante padrão, que deve ser substituída, se possível. A função também pode optar por atualizar `baserel->width` se puder calcular uma melhor estimativa da largura média do resultado da linha. (O valor inicial é baseado nos tipos de dados das colunas e nos valores de largura média das colunas medidos pelo último `ANALYZE`. Além disso, essa função pode atualizar `baserel->tuples` se puder calcular uma melhor estimativa do total de linhas da tabela externa. (O valor inicial é do `pg_class`.`reltuples` que representa o total de linhas vistas pelo último `ANALYZE`; será `-1` se nenhuma `ANALYZE` tiver sido feita nesta tabela externa.)

Veja [Seção 58.4](fdw-planning.md) para informações adicionais.

```
void
GetForeignPaths(PlannerInfo *root,
                RelOptInfo *baserel,
                Oid foreigntableid);
```

Crie possíveis caminhos de acesso para uma varredura em uma tabela estrangeira. Isso é chamado durante o planejamento da consulta. Os parâmetros são os mesmos que para `GetForeignRelSize`, que já foi chamado.

Essa função deve gerar pelo menos um caminho de acesso (nó `ForeignPath`) para uma varredura na tabela estrangeira e deve chamar `add_path` para adicionar cada um desses caminhos ao `baserel->pathlist`. Recomenda-se usar `create_foreignscan_path` para construir os nós `ForeignPath`. A função pode gerar múltiplos caminhos de acesso, por exemplo, um caminho que tenha `pathkeys` válido para representar um resultado pré-ordenado. Cada caminho de acesso deve conter estimativas de custo e pode conter qualquer informação privada do FDW necessária para identificar o método de varredura pretendido.

Veja [Seção 58.4](fdw-planning.md) para informações adicionais.

```
ForeignScan *
GetForeignPlan(PlannerInfo *root,
               RelOptInfo *baserel,
               Oid foreigntableid,
               ForeignPath *best_path,
               List *tlist,
               List *scan_clauses,
               Plan *outer_plan);
```

Crie um nó de plano `ForeignScan` a partir do caminho de acesso externo selecionado. Isso é chamado no final do planejamento da consulta. Os parâmetros são os mesmos que para `GetForeignRelSize`, além do `ForeignPath` selecionado (anteriormente produzido por `GetForeignPaths`, `GetForeignJoinPaths` ou `GetForeignUpperPaths`), a lista de destino a ser emitida pelo nó do plano, as cláusulas de restrição a serem aplicadas pelo nó do plano e o subplano externo do `ForeignScan`, que é usado para rechecks realizados por `RecheckForeignScan`. (Se o caminho for para uma junção em vez de uma relação de base, `foreigntableid` é `InvalidOid`.

Essa função deve criar e retornar um nó do plano `ForeignScan`; é recomendável usar `make_foreignscan` para construir o nó `ForeignScan`.

Veja [Seção 58.4](fdw-planning.md) para informações adicionais.

```
void
BeginForeignScan(ForeignScanState *node,
                 int eflags);
```

Comece a executar uma varredura externa. Isso é chamado durante o início do executor. Ele deve realizar qualquer inicialização necessária antes que a varredura possa começar, mas não iniciar a execução da varredura real (que deve ser feita na primeira chamada para `IterateForeignScan`). O nó `ForeignScanState` já foi criado, mas seu campo `fdw_state` ainda está NULL. As informações sobre a tabela a ser varrida são acessíveis através do nó `ForeignScanState` (particularmente, do nó subjacente `ForeignScan`, que contém qualquer informação privada do FDW fornecida por `GetForeignPlan`). `eflags` contém bits de sinalização que descrevem o modo operacional do executor para este nó do plano.

Observe que, quando `(eflags & EXEC_FLAG_EXPLAIN_ONLY)` é verdadeiro, essa função não deve realizar nenhuma ação externamente visível; ela deve apenas fazer o mínimo necessário para tornar o estado do nó válido para `ExplainForeignScan` e `EndForeignScan`.

```
TupleTableSlot *
IterateForeignScan(ForeignScanState *node);
```

Pegue uma linha da fonte estrangeira, devolvendo-a em um slot de tabela de tupla (o `ScanTupleSlot` do nó deve ser usado para esse propósito). Devolva NULL se não houver mais linhas disponíveis. A infraestrutura do slot de tabela de tupla permite que uma tupla física ou virtual seja devolvida; na maioria dos casos, a segunda opção é preferível em termos de desempenho. Note que isso é chamado em um contexto de memória de curta duração que será redefinido entre as invocações. Crie um contexto de memória em `BeginForeignScan` se você precisar de armazenamento de maior duração, ou use o `es_query_cxt` do `EState` do nó.

As linhas devolvidas devem corresponder à lista de referência `fdw_scan_tlist`, se uma foi fornecida, caso contrário, devem corresponder ao tipo de linha da tabela estrangeira que está sendo examinada. Se você optar por otimizar a obtenção de colunas que não são necessárias, deve inserir nulos nessas posições de coluna, caso contrário, gere uma lista `fdw_scan_tlist` com essas colunas omitidas.

Observe que o executor do PostgreSQL não se importa se as linhas devolvidas violam quaisquer restrições definidas na tabela estrangeira — mas o planejador se importa, e pode otimizar consultas incorretamente se houver linhas visíveis na tabela estrangeira que não satisfazem uma restrição declarada. Se uma restrição for violada quando o usuário declarou que a restrição deve ser verdadeira, pode ser apropriado gerar um erro (assim como você precisaria fazer no caso de um desajuste de tipo de dados).

```
void
ReScanForeignScan(ForeignScanState *node);
```

Reinicie a varredura do início. Observe que quaisquer parâmetros que dependem da varredura podem ter valores alterados, portanto, a nova varredura não necessariamente retornará exatamente as mesmas linhas.

```
void
EndForeignScan(ForeignScanState *node);
```

Finalize a varredura e libere os recursos. Normalmente, não é importante liberar a memória palloc, mas, por exemplo, arquivos e conexões a servidores remotos devem ser limpos.

### 58.2.2. Rotinas FDW para varredura de junções estrangeiras [#](#FDW-CALLBACKS-JOIN-SCAN)

Se um FDW suportar a realização de junções estrangeiras remotamente (em vez de buscar os dados de ambas as tabelas e realizar a junção localmente), ele deve fornecer essa função de callback:

```
void
GetForeignJoinPaths(PlannerInfo *root,
                    RelOptInfo *joinrel,
                    RelOptInfo *outerrel,
                    RelOptInfo *innerrel,
                    JoinType jointype,
                    JoinPathExtraData *extra);
```

Crie possíveis caminhos de acesso para uma junção de duas (ou mais) tabelas estrangeiras que todas pertençam ao mesmo servidor estrangeiro. Esta função opcional é chamada durante o planejamento da consulta. Assim como `GetForeignPaths`, esta função deve gerar `ForeignPath` caminho(s) para o `joinrel` fornecido (use `create_foreign_join_path` para construí-los) e chamar `add_path` para adicionar esses caminhos ao conjunto de caminhos considerados para a junção. Mas, ao contrário de `GetForeignPaths`, não é necessário que esta função tenha sucesso em criar pelo menos um caminho, uma vez que caminhos envolvendo junção local são sempre possíveis.

Observe que essa função será invocada repetidamente para a mesma relação de junção, com diferentes combinações de relações internas e externas; é responsabilidade do FDW minimizar o trabalho duplicado.

Observe também que o conjunto de cláusulas de junção a serem aplicadas à junção, que é passado como `extra->restrictlist`, varia dependendo da combinação de relações internas e externas. Um caminho `ForeignPath` gerado para o `joinrel` deve conter o conjunto de cláusulas de junção que ele usa, que será usado pelo planejador para converter o caminho `ForeignPath` em um plano, se for selecionado pelo planejador como o melhor caminho para o `joinrel`.

Se for escolhido um caminho `ForeignPath` para a junção, ele representará todo o processo de junção; os caminhos gerados para as tabelas de componentes e as junções subsidiárias não serão utilizados. O processamento subsequente do caminho de junção procede da mesma forma que o de um caminho que analisa uma única tabela estrangeira. Uma diferença é que o `scanrelid` do nó do plano resultante `ForeignScan` deve ser definido como zero, uma vez que não há uma relação única que ele represente; em vez disso, o campo `fs_relids` do nó `ForeignScan` representa o conjunto de relações que foram juncionadas. (Este último campo é configurado automaticamente pelo código do planejador principal e não precisa ser preenchido pelo FDW.) Outra diferença é que, como a lista de colunas para uma junção remota não pode ser encontrada nos catálogos do sistema, o FDW deve preencher `fdw_scan_tlist` com uma lista apropriada de nós `TargetEntry`, representando o conjunto de colunas que ele fornecerá no momento da execução nos tuplos que retorna.

### Nota

Começando com o PostgreSQL 16, `fs_relids` inclui os índices rangetable das junções externas, se houver sido envolvida alguma delas nessa junção. O novo campo `fs_base_relids` inclui apenas índices de relação de base, e, portanto, imita a semântica antiga do `fs_relids`.

Veja [Seção 58.4](fdw-planning.md) para informações adicionais.

### 58.2.3. Rotinas FDW para o planejamento do processamento pós-scan/joinamento [#](#FDW-CALLBACKS-UPPER-PLANNING)

Se um FDW suportar a realização de processamento remoto pós-análise/junção, como agregação remota, ele deve fornecer essa função de callback:

```
void
GetForeignUpperPaths(PlannerInfo *root,
                     UpperRelationKind stage,
                     RelOptInfo *input_rel,
                     RelOptInfo *output_rel,
                     void *extra);
```

Crie possíveis caminhos de acesso para o processamento de *relação superior*, que é o termo do planejador para todo o processamento de consultas pós-scan/join, como agregação, funções de janela, ordenação e atualizações de tabela. Esta função opcional é chamada durante o planejamento da consulta. Atualmente, ela é chamada apenas se todas as relações de base envolvidas na consulta pertencem ao mesmo FDW. Esta função deve gerar `ForeignPath` caminhos para qualquer processamento pós-scan/join que o FDW saiba como realizar remotamente (use `create_foreign_upper_path` para construí-los) e chamar `add_path` para adicionar esses caminhos à relação superior indicada. Como com `GetForeignJoinPaths`, não é necessário que esta função tenha sucesso em criar quaisquer caminhos, uma vez que caminhos envolvendo processamento local são sempre possíveis.

O parâmetro `stage` identifica qual etapa pós-scan/junção está sendo considerada atualmente. `output_rel` é a relação superior que deve receber caminhos representando o cálculo desta etapa, e `input_rel` é a relação que representa a entrada para esta etapa. O parâmetro `extra` fornece detalhes adicionais, atualmente, ele é definido apenas para `UPPERREL_PARTIAL_GROUP_AGG` ou `UPPERREL_GROUP_AGG`, nesse caso, ele aponta para uma estrutura `GroupPathExtraData`; ou para `UPPERREL_FINAL`, nesse caso, ele aponta para uma estrutura `FinalPathExtraData`. (Nota que os caminhos `output_rel` adicionados não teriam, normalmente, nenhuma dependência direta dos caminhos do `input_rel`, uma vez que seu processamento é esperado para ser feito externamente. No entanto, examinar caminhos gerados anteriormente para a etapa de processamento anterior pode ser útil para evitar trabalho de planejamento redundante.)

Veja [Seção 58.4](fdw-planning.md) para informações adicionais.

### 58.2.4. Rotinas FDW para Atualização de Tabelas Estrangeiras [#](#FDW-CALLBACKS-UPDATE)

Se um FDW suportar tabelas estrangeiras graváveis, ele deve fornecer algumas ou todas as seguintes funções de callback, dependendo das necessidades e capacidades do FDW:

```
void
AddForeignUpdateTargets(PlannerInfo *root,
                        Index rtindex,
                        RangeTblEntry *target_rte,
                        Relation target_relation);
```

As operações `UPDATE` e `DELETE` são realizadas contra linhas previamente obtidas pelas funções de varredura de tabela. O FDW pode precisar de informações adicionais, como um ID de linha ou os valores das colunas da chave primária, para garantir que possa identificar a linha exata a ser atualizada ou excluída. Para isso, essa função pode adicionar colunas de destino ocultas ou "desnecessárias" adicionais à lista de colunas que devem ser recuperadas da tabela estrangeira durante uma `UPDATE` ou `DELETE`.

Para fazer isso, construa um `Var` representando um valor extra que você precisa e passe-o para `add_row_identity_var`, juntamente com um nome para a coluna de lixo. (Você pode fazer isso mais de uma vez se várias colunas forem necessárias). Você deve escolher um nome de coluna de lixo distinto para cada `Var` diferente que você precisa, exceto que `Var`s que são idênticos, exceto pelo campo `varno`, podem e devem compartilhar um nome de coluna. O sistema central usa os nomes de coluna de lixo `tableoid` para a coluna `tableoid` de uma tabela, `ctid` ou `ctidN` para `ctid`, `wholerow` para uma coluna de linha inteira `Var` marcada com `vartype` = `RECORD`, e `wholerowN` para uma coluna de linha inteira `Var` com `vartype` igual ao tipo de linha declarado da tabela. Reutilize esses nomes quando puder (o planejador combinará solicitações duplicadas para colunas de lixo idênticas). Se você precisar de outro tipo de coluna de lixo além dessas, pode ser sábio escolher um nome prefixado com o nome da sua extensão, para evitar conflitos com outros FDWs.

Se o ponteiro `AddForeignUpdateTargets` estiver definido como `NULL`, não serão adicionadas expressões de alvo extras. (Isso tornará impossível implementar operações `DELETE`, embora `UPDATE` ainda possa ser viável se o FDW depender de uma chave primária inalterável para identificar as linhas.)

```
List *
PlanForeignModify(PlannerInfo *root,
                  ModifyTable *plan,
                  Index resultRelation,
                  int subplan_index);
```

Realize quaisquer ações de planejamento adicionais necessárias para uma inserção, atualização ou exclusão em uma tabela externa. Esta função gera as informações privadas do FDW que serão anexadas ao nó do plano `ModifyTable` que realiza a ação de atualização. Essas informações privadas devem ter a forma de um `List`, e serão entregues ao `BeginForeignModify` durante a fase de execução.

`root` é a informação global do planejador sobre a consulta. `plan` é o nó do plano `ModifyTable`, que é completo, exceto pelo campo `fdwPrivLists`. `resultRelation` identifica a tabela estrangeira alvo por seu índice de tabela de intervalo. `subplan_index` identifica qual alvo do nó `ModifyTable` este é, contando a partir de zero; use isso se você quiser indexar em subestruturas de relação por alvo do nó `plan`.

Veja [Seção 58.4](fdw-planning.md) para informações adicionais.

Se o ponteiro `PlanForeignModify` estiver configurado como `NULL`, não são realizadas ações adicionais de tempo de plano, e a lista `fdw_private` entregue a `BeginForeignModify` será NIL.

```
void
BeginForeignModify(ModifyTableState *mtstate,
                   ResultRelInfo *rinfo,
                   List *fdw_private,
                   int subplan_index,
                   int eflags);
```

Comece a executar uma operação de modificação de tabela estrangeira. Essa rotina é chamada durante o início do executor. Ela deve realizar qualquer inicialização necessária antes das modificações reais da tabela. Posteriormente, `ExecForeignInsert/ExecForeignBatchInsert`, `ExecForeignUpdate` ou `ExecForeignDelete` serão chamados para tuplas a serem inseridas, atualizadas ou excluídas.

`mtstate` é o estado geral do nó de plano `ModifyTable` que está sendo executado; dados globais sobre o plano e o estado de execução estão disponíveis por meio dessa estrutura. `rinfo` é a estrutura `ResultRelInfo` que descreve a tabela estrangeira de destino. (O campo `ri_FdwState` de `ResultRelInfo` está disponível para o FDW armazenar qualquer estado privado que ele precise para essa operação.) `fdw_private` contém os dados privados gerados por `PlanForeignModify`, se houver. `subplan_index` identifica qual alvo do nó de plano `ModifyTable` é este. `eflags` contém bits de sinalização que descrevem o modo operacional do executor para esse nó de plano.

Observe que, quando `(eflags & EXEC_FLAG_EXPLAIN_ONLY)` é verdadeiro, essa função não deve realizar nenhuma ação externamente visível; ela deve apenas fazer o mínimo necessário para tornar o estado do nó válido para `ExplainForeignModify` e `EndForeignModify`.

Se o ponteiro `BeginForeignModify` estiver definido como `NULL`, nenhuma ação é realizada durante o início do executor.

```
TupleTableSlot *
ExecForeignInsert(EState *estate,
                  ResultRelInfo *rinfo,
                  TupleTableSlot *slot,
                  TupleTableSlot *planSlot);
```

Insira um tuplo na tabela estrangeira. `estate` é o estado de execução global para a consulta. `rinfo` é a estrutura `ResultRelInfo` que descreve a tabela estrangeira alvo. `slot` contém o tuplo a ser inserido; ele corresponderá à definição do tipo de linha da tabela estrangeira. `planSlot` contém o tuplo que foi gerado pelo subplano do nó de plano `ModifyTable`; ele difere de `slot` em possivelmente conter colunas adicionais de "lixo". (O `planSlot` é tipicamente de pouca importância para os casos de `INSERT`, mas é fornecido por completo.)

O valor de retorno é um slot que contém os dados que foram realmente inseridos (isso pode diferir dos dados fornecidos, por exemplo, como resultado de ações de gatilho), ou NULL se nenhuma linha foi realmente inserida (novamente, tipicamente como resultado de gatilhos). O `slot` passado pode ser reutilizado para esse propósito.

Os dados no slot retornado são usados apenas se a declaração `INSERT` tiver uma cláusula `RETURNING` ou envolver uma visão `WITH CHECK OPTION`; ou se a tabela estrangeira tiver um gatilho `AFTER ROW`. Os gatilhos exigem todas as colunas, mas o FDW pode optar por otimizar, ignorando o retorno de algumas ou todas as colunas, dependendo do conteúdo da cláusula `RETURNING` ou das restrições `WITH CHECK OPTION`. Independentemente disso, alguns slots devem ser retornados para indicar sucesso, ou o número de linhas relatado da consulta estará errado.

Se o ponteiro `ExecForeignInsert` estiver definido como `NULL`, as tentativas de inserção na tabela estrangeira falharão com uma mensagem de erro.

Observe que essa função também é chamada ao inserir tuplas roteadas em uma partição de tabela estrangeira ou ao executar `COPY FROM` em uma tabela estrangeira, nesse caso, ela é chamada de uma maneira diferente daquela do caso `INSERT`. Veja as funções de callback descritas abaixo que permitem que o FDW suporte isso.

```
TupleTableSlot **
ExecForeignBatchInsert(EState *estate,
                       ResultRelInfo *rinfo,
                       TupleTableSlot **slots,
                       TupleTableSlot **planSlots,
                       int *numSlots);
```

Insira vários tuplos em massa na tabela estrangeira. Os parâmetros são os mesmos para `ExecForeignInsert`, exceto que `slots` e `planSlots` contêm vários tuplos e `*numSlots` especifica o número de tuplos nesses arrays.

O valor de retorno é um array de slots que contém os dados que foram realmente inseridos (isso pode diferir dos dados fornecidos, por exemplo, como resultado de ações de gatilho). O `slots` passado pode ser reutilizado para esse propósito. O número de tuplas inseridas com sucesso é retornado em `*numSlots`.

Os dados no slot retornado são usados apenas se a declaração `INSERT` envolver uma visão `WITH CHECK OPTION`; ou se a tabela estrangeira tiver um gatilho `AFTER ROW`. Os gatilhos exigem todas as colunas, mas o FDW pode optar por otimizar, ignorando o retorno de algumas ou todas as colunas, dependendo do conteúdo das restrições `WITH CHECK OPTION`.

Se o ponteiro `ExecForeignBatchInsert` ou `GetForeignModifyBatchSize` estiver definido como `NULL`, as tentativas de inserção na tabela estrangeira usarão `ExecForeignInsert`. Esta função não é usada se o `INSERT` tiver a cláusula `RETURNING`.

Observe que essa função também é chamada ao inserir tuplas roteadas em uma partição de tabela estrangeira ou ao executar `COPY FROM` em uma tabela estrangeira, nesse caso, ela é chamada de uma maneira diferente daquela do caso `INSERT`. Veja as funções de callback descritas abaixo que permitem que o FDW suporte isso.

```
int
GetForeignModifyBatchSize(ResultRelInfo *rinfo);
```

Informe o número máximo de tuplas que uma única chamada do `ExecForeignBatchInsert` pode lidar para a tabela estrangeira especificada. O executor passa no máximo o número dado de tuplas para o `ExecForeignBatchInsert`. O `rinfo` é a estrutura `ResultRelInfo` que descreve a tabela estrangeira alvo. Espera-se que o FDW forneça uma opção de servidor estrangeiro e/ou tabela estrangeira para o usuário definir esse valor, ou algum valor pré-codificado.

Se o ponteiro `ExecForeignBatchInsert` ou `GetForeignModifyBatchSize` estiver definido como `NULL`, as tentativas de inserção na tabela estrangeira usarão `ExecForeignInsert`.

```
TupleTableSlot *
ExecForeignUpdate(EState *estate,
                  ResultRelInfo *rinfo,
                  TupleTableSlot *slot,
                  TupleTableSlot *planSlot);
```

Atualize um tuplo na tabela estrangeira. `estate` é o estado de execução global para a consulta. `rinfo` é a estrutura `ResultRelInfo` que descreve a tabela estrangeira alvo. `slot` contém os novos dados para o tuplo; ele corresponderá à definição do tipo de linha da tabela estrangeira. `planSlot` contém o tuplo que foi gerado pelo subplano do nó de plano `ModifyTable`. Ao contrário de `slot`, este tuplo contém apenas os novos valores das colunas alteradas pela consulta, portanto, não confie nos números de atributos da tabela estrangeira para indexar em `planSlot`. Além disso, `planSlot` geralmente contém colunas adicionais de “lixo”. Em particular, quaisquer colunas de lixo que foram solicitadas por `AddForeignUpdateTargets` estarão disponíveis neste slot.

O valor de retorno é um slot que contém a linha conforme ela foi realmente atualizada (isso pode diferir dos dados fornecidos, por exemplo, como resultado de ações de gatilho), ou NULL se nenhuma linha foi realmente atualizada (novamente, tipicamente como resultado de gatilhos). O `slot` passado pode ser reutilizado para esse propósito.

Os dados no slot retornado são usados apenas se a declaração `UPDATE` tiver uma cláusula `RETURNING` ou envolver uma visão `WITH CHECK OPTION`; ou se a tabela estrangeira tiver um gatilho `AFTER ROW`. Os gatilhos exigem todas as colunas, mas o FDW pode optar por otimizar, ignorando o retorno de algumas ou todas as colunas, dependendo do conteúdo da cláusula `RETURNING` ou das restrições `WITH CHECK OPTION`. Independentemente disso, alguns slots devem ser retornados para indicar sucesso, ou o número de linhas relatado da consulta estará errado.

Se o ponteiro `ExecForeignUpdate` estiver definido como `NULL`, as tentativas de atualizar a tabela externa falharão com uma mensagem de erro.

```
TupleTableSlot *
ExecForeignDelete(EState *estate,
                  ResultRelInfo *rinfo,
                  TupleTableSlot *slot,
                  TupleTableSlot *planSlot);
```

Exclua um tuplo da tabela estrangeira. `estate` é o estado de execução global para a consulta. `rinfo` é a estrutura `ResultRelInfo` que descreve a tabela estrangeira alvo. `slot` não contém nada útil após a chamada, mas pode ser usado para armazenar a tupla retornada. `planSlot` contém a tupla que foi gerada pelo subplano do nó de plano `ModifyTable`; em particular, ela carregará quaisquer colunas desnecessárias que foram solicitadas por `AddForeignUpdateTargets`. A(s) coluna(s) desnecessária(s) deve(m) ser usada(s) para identificar a tupla a ser excluída.

O valor de retorno é um slot que contém a linha que foi excluída, ou NULL se nenhuma linha foi excluída (tipicamente como resultado de gatilhos). O `slot` passado pode ser usado para armazenar o tuplo a ser retornado.

Os dados no slot retornado são usados apenas se a consulta `DELETE` tiver uma cláusula `RETURNING` ou se a tabela externa tiver um gatilho `AFTER ROW`. Os gatilhos exigem todas as colunas, mas o FDW pode optar por otimizar, ignorando o retorno de algumas ou todas as colunas, dependendo do conteúdo da cláusula `RETURNING`. Independentemente disso, alguns slots devem ser retornados para indicar sucesso, ou o número de linhas relatado pela consulta estará errado.

Se o ponteiro `ExecForeignDelete` estiver definido como `NULL`, as tentativas de excluir dados da tabela externa falharão com uma mensagem de erro.

```
void
EndForeignModify(EState *estate,
                 ResultRelInfo *rinfo);
```

Finalize a atualização da tabela e libere os recursos. Normalmente, não é importante liberar a memória palloc, mas, por exemplo, arquivos e conexões a servidores remotos devem ser limpos.

Se o ponteiro `EndForeignModify` estiver definido como `NULL`, nenhuma ação é realizada durante o desligamento do executor.

Os tuplos inseridos em uma tabela particionada por `INSERT` ou `COPY FROM` são encaminhados para as partições. Se um FDW suportar partições de tabela estrangeira roteáveis, ele também deve fornecer as seguintes funções de callback. Essas funções também são chamadas quando `COPY FROM` é executado em uma tabela estrangeira.

```
void
BeginForeignInsert(ModifyTableState *mtstate,
                   ResultRelInfo *rinfo);
```

Comece a executar uma operação de inserção em uma tabela estrangeira. Essa rotina é chamada logo antes da primeira tupla ser inserida na tabela estrangeira, em ambos os casos, quando é a partição escolhida para o roteamento de tuplas e o alvo especificado em um comando `COPY FROM`. Ela deve realizar qualquer inicialização necessária antes da inserção real. Posteriormente, `ExecForeignInsert` ou `ExecForeignBatchInsert` será chamado(s) para as tuplas serem inseridas na tabela estrangeira.

`mtstate` é o estado geral do nó do plano `ModifyTable` que está sendo executado; dados globais sobre o plano e o estado de execução estão disponíveis por meio dessa estrutura. `rinfo` é a estrutura `ResultRelInfo` que descreve a tabela estrangeira de destino. (O campo `ri_FdwState` de `ResultRelInfo` está disponível para o FDW armazenar qualquer estado privado que ele precise para essa operação.)

Quando isso é chamado por um comando `COPY FROM`, os dados globais relacionados ao plano em `mtstate` não são fornecidos e o parâmetro `planSlot` de `ExecForeignInsert` subsequentemente chamado para cada tupla inserida é `NULL`, seja a tabela estrangeira a partição escolhida para o roteamento da tupla ou o alvo especificado no comando.

Se o ponteiro `BeginForeignInsert` estiver definido como `NULL`, não será realizada nenhuma ação para a inicialização.

Observe que, se o FDW não suportar partições de tabela estrangeira roteáveis e/ou executar `COPY FROM` em tabelas estrangeiras, essa função ou `ExecForeignInsert/ExecForeignBatchInsert` subsequentemente chamada deve lançar o erro conforme necessário.

```
void
EndForeignInsert(EState *estate,
                 ResultRelInfo *rinfo);
```

Finalize a operação de inserção e libere os recursos. Normalmente, não é importante liberar a memória palloc, mas, por exemplo, arquivos e conexões a servidores remotos devem ser limpos.

Se o ponteiro `EndForeignInsert` estiver definido como `NULL`, não será tomada nenhuma ação para a terminação.

```
int
IsForeignRelUpdatable(Relation rel);
```

Relatório que indica quais operações a tabela estrangeira especificada suporta. O valor de retorno deve ser uma máscara de bits de números de eventos de regra que indicam quais operações são suportadas pela tabela estrangeira, usando a enumeração `CmdType`; ou seja, `(1 << CMD_UPDATE) = 4` para `UPDATE`, `(1 << CMD_INSERT) = 8` para `INSERT` e `(1 << CMD_DELETE) = 16` para `DELETE`.

Se o ponteiro `IsForeignRelUpdatable` estiver definido como `NULL`, as tabelas estrangeiras são assumidas como inseríveis, atualizáveis ou deletabilizáveis se o FDW fornecer `ExecForeignInsert`, `ExecForeignUpdate` ou `ExecForeignDelete`, respectivamente. Esta função é necessária apenas se o FDW suportar algumas tabelas que são atualizáveis e outras que não são. (Mesmo assim, é permitido lançar um erro na rotina de execução em vez de verificar nesta função. No entanto, esta função é usada para determinar a atualizabilidade para exibição nas visualizações do `information_schema`.)

Algumas inserções, atualizações e exclusões em tabelas externas podem ser otimizadas implementando um conjunto alternativo de interfaces. As interfaces comuns para inserções, atualizações e exclusões buscam linhas do servidor remoto e, em seguida, modificam essas linhas uma de cada vez. Em alguns casos, essa abordagem linha por linha é necessária, mas pode ser ineficiente. Se for possível para o servidor externo determinar quais linhas devem ser modificadas sem realmente recuperá-las, e se não houver estruturas locais que afetarão a operação (triggers locais em nível de linha, colunas geradas armazenadas ou restrições `WITH CHECK OPTION` de vistas parentais), então é possível organizar as coisas de modo que toda a operação seja realizada no servidor remoto. As interfaces descritas abaixo tornam isso possível.

```
bool
PlanDirectModify(PlannerInfo *root,
                 ModifyTable *plan,
                 Index resultRelation,
                 int subplan_index);
```

Decida se é seguro executar uma modificação direta no servidor remoto. Se sim, retorne `true` após realizar as ações de planejamento necessárias para isso. Caso contrário, retorne `false`. Esta função opcional é chamada durante o planejamento da consulta. Se essa função tiver sucesso, `BeginDirectModify`, `IterateDirectModify` e `EndDirectModify` serão chamados na etapa de execução, em vez disso. Caso contrário, a modificação da tabela será executada usando as funções de atualização de tabela descritas acima. Os parâmetros são os mesmos que para `PlanForeignModify`.

Para executar a modificação direta no servidor remoto, essa função deve reescrever o subplano-alvo com um nó de plano `ForeignScan` que execute a modificação direta no servidor remoto. Os campos `operation` e `resultRelation` do `ForeignScan` devem ser definidos apropriadamente. `operation` deve ser definido para a enumeração `CmdType` correspondente ao tipo de declaração (ou seja, `CMD_UPDATE` para `UPDATE`, `CMD_INSERT` para `INSERT` e `CMD_DELETE` para `DELETE`), e o argumento `resultRelation` deve ser copiado para o campo `resultRelation`.

Veja [Seção 58.4](fdw-planning.md) para informações adicionais.

Se o ponteiro `PlanDirectModify` estiver configurado para `NULL`, não serão realizadas tentativas de execução de uma modificação direta no servidor remoto.

```
void
BeginDirectModify(ForeignScanState *node,
                  int eflags);
```

Prepare-se para executar uma modificação direta no servidor remoto. Isso é feito durante o início do executor. Deve realizar qualquer inicialização necessária antes da modificação direta (que deve ser feita na primeira chamada para `IterateDirectModify`). O nó `ForeignScanState` já foi criado, mas seu campo `fdw_state` ainda está NULL. As informações sobre a tabela a ser modificada são acessíveis através do nó `ForeignScanState` (em particular, do nó subjacente `ForeignScan`, que contém qualquer informação privada do FDW fornecida por `PlanDirectModify`). `eflags` contém bits de sinalização que descrevem o modo operacional do executor para este nó do plano.

Observe que, quando `(eflags & EXEC_FLAG_EXPLAIN_ONLY)` é verdadeiro, essa função não deve realizar nenhuma ação externamente visível; ela deve apenas fazer o mínimo necessário para tornar o estado do nó válido para `ExplainDirectModify` e `EndDirectModify`.

Se o ponteiro `BeginDirectModify` estiver definido como `NULL`, não serão realizadas tentativas de execução de uma modificação direta no servidor remoto.

```
TupleTableSlot *
IterateDirectModify(ForeignScanState *node);
```

Quando a consulta `INSERT`, `UPDATE` ou `DELETE` não possui uma cláusula `RETURNING`, retorne NULL após uma modificação direta no servidor remoto. Quando a consulta possui a cláusula, obtenha um resultado contendo os dados necessários para o cálculo `RETURNING`, retornando-o em um slot de tabela de tupla (o `ScanTupleSlot` do nó deve ser usado para esse propósito). Os dados que foram realmente inseridos, atualizados ou excluídos devem ser armazenados em `node->resultRelInfo->ri_projectReturning->pi_exprContext->ecxt_scantuple`. Retorne NULL se não houver mais linhas disponíveis. Note que isso é chamado em um contexto de memória de curta duração que será redefinido entre as invocações. Crie um contexto de memória em `BeginDirectModify` se você precisar de armazenamento de maior duração, ou use o `es_query_cxt` do `EState` do nó.

As linhas devolvidas devem corresponder à lista de referência `fdw_scan_tlist`, se uma foi fornecida, caso contrário, devem corresponder ao tipo de linha da tabela estrangeira que está sendo atualizada. Se você optar por otimizar a obtenção de colunas que não são necessárias para o cálculo `RETURNING`, você deve inserir nulos nessas posições de coluna, caso contrário, gere uma lista `fdw_scan_tlist` com essas colunas omitidas.

Se a consulta tiver ou não a cláusula, o número de linhas relatado da consulta deve ser incrementado pelo próprio FDW. Quando a consulta não tiver a cláusula, o FDW também deve incrementar o número de linhas para o nó `ForeignScanState` no caso `EXPLAIN ANALYZE`.

Se o ponteiro `IterateDirectModify` estiver configurado para `NULL`, não serão realizadas tentativas de execução de uma modificação direta no servidor remoto.

```
void
EndDirectModify(ForeignScanState *node);
```

Limpe após uma modificação direta no servidor remoto. Normalmente, não é importante liberar a memória palloc, mas, por exemplo, os arquivos e conexões ao servidor remoto devem ser limpos.

Se o ponteiro `EndDirectModify` estiver configurado como `NULL`, não serão realizadas tentativas de execução de uma modificação direta no servidor remoto.

### 58.2.5. Rotinas FDW para `TRUNCATE` [#](#FDW-CALLBACKS-TRUNCATE)

```
void
ExecForeignTruncate(List *rels,
                    DropBehavior behavior,
                    bool restart_seqs);
```

Retorne tabelas estrangeiras. Essa função é chamada quando [TRUNCATE](sql-truncate.md) é executada em uma tabela estrangeira. `rels` é uma lista de estruturas de dados `Relation` de tabelas estrangeiras a serem truncadas.

`behavior` é ou `DROP_RESTRICT` ou `DROP_CASCADE`, indicando que a opção `RESTRICT` ou `CASCADE` foi solicitada no comando original `TRUNCATE`, respectivamente.

Se `restart_seqs` é `true`, o comando original `TRUNCATE` solicitava o comportamento `RESTART IDENTITY`, caso contrário, o comportamento `CONTINUE IDENTITY` era solicitado.

Observe que as opções `ONLY` especificadas no comando original `TRUNCATE` não são passadas para `ExecForeignTruncate`. Esse comportamento é semelhante às funções de callback dos comandos `SELECT`, `UPDATE` e `DELETE` em uma tabela estrangeira.

`ExecForeignTruncate` é invocado uma vez por servidor estrangeiro para o qual as tabelas estrangeiras devem ser truncadas. Isso significa que todas as tabelas estrangeiras incluídas em `rels` devem pertencer ao mesmo servidor.

Se o ponteiro `ExecForeignTruncate` estiver definido como `NULL`, as tentativas de truncar tabelas externas falharão com uma mensagem de erro.

### 58.2.6. Rotinas FDW para bloqueio de linhas [#](#FDW-CALLBACKS-ROW-LOCKING)

Se uma FDW desejar suportar o *bloqueio tardio da linha* (conforme descrito em [Seção 58.5](fdw-row-locking.md)), ela deve fornecer as seguintes funções de callback:

```
RowMarkType
GetForeignRowMarkType(RangeTblEntry *rte,
                      LockClauseStrength strength);
```

Relatório sobre qual opção de marcação de linha deve ser usada para uma tabela estrangeira. `rte` é o nó `RangeTblEntry` para a tabela e `strength` descreve a força de bloqueio solicitada pela cláusula relevante `FOR UPDATE/SHARE`, se houver. O resultado deve ser um membro do tipo de enum `RowMarkType`.

Essa função é chamada durante o planejamento da consulta para cada tabela estrangeira que aparece em uma consulta de `UPDATE`, `DELETE` ou `SELECT FOR UPDATE/SHARE` e que não é o alvo de `UPDATE` ou `DELETE`.

Se o ponteiro `GetForeignRowMarkType` estiver definido como `NULL`, a opção `ROW_MARK_COPY` é sempre usada. (Isso implica que `RefetchForeignRow` nunca será chamado, portanto, não precisa ser fornecida também.)

Veja [Seção 58.5](fdw-row-locking.md) para mais informações.

```
void
RefetchForeignRow(EState *estate,
                  ExecRowMark *erm,
                  Datum rowid,
                  TupleTableSlot *slot,
                  bool *updated);
```

Recupere um slot de tupla da tabela estrangeira, após bloqueá-lo, se necessário. `estate` é o estado de execução global para a consulta. `erm` é a estrutura `ExecRowMark` que descreve a tabela estrangeira alvo e o tipo de bloqueio de linha (se houver) a ser adquirido. `rowid` identifica a tupla a ser recuperada. `slot` não contém nada útil após a chamada, mas pode ser usado para armazenar a tupla devolvida. `updated` é um parâmetro de saída.

Essa função deve armazenar o tuplo no slot fornecido, ou limpá-lo se o bloqueio da linha não puder ser obtido. O tipo de bloqueio da linha a ser adquirido é definido por `erm->markType`, que é o valor previamente retornado por `GetForeignRowMarkType`. (`ROW_MARK_REFERENCE` significa apenas refazer o tuplo sem adquirir qualquer bloqueio, e `ROW_MARK_COPY` nunca será visto por essa rotina.)

Além disso, `*updated` deve ser definido como `true` se o que foi obtido foi uma versão atualizada do tuplo, e não a mesma versão obtida anteriormente. (Se o FDW não puder ter certeza sobre isso, sempre é recomendado retornar `true`.)

Observe que, por padrão, a falha em adquirir um bloqueio de linha deve resultar no lançamento de um erro; retornar com um slot vazio é apropriado apenas se a opção `SKIP LOCKED` for especificada por `erm->waitPolicy`.

O `rowid` é o valor `ctid` previamente lido para a linha que será recuperada novamente. Embora o valor `rowid` seja passado como um `Datum`, atualmente ele só pode ser um `tid`. A API da função é escolhida na esperança de que seja possível permitir outros tipos de dados para os IDs de linha no futuro.

Se o ponteiro `RefetchForeignRow` estiver definido como `NULL`, as tentativas de recuperar novamente as linhas falharão com uma mensagem de erro.

Veja [Seção 58.5](fdw-row-locking.md) para mais informações.

```
bool
RecheckForeignScan(ForeignScanState *node,
                   TupleTableSlot *slot);
```

Verifique novamente se um conjunto previamente retornado ainda corresponde aos qualificadores relevantes do exame e junção, e, se possível, forneça uma versão modificada do conjunto. Para wrappers de dados externos que não realizam empurrão de junção, geralmente será mais conveniente definir isso como `NULL` e, em vez disso, definir `fdw_recheck_quals` apropriadamente. Quando as junções externas são empurradas, no entanto, não é suficiente reaplicar os controles relevantes para todas as tabelas de base ao conjunto do resultado, mesmo que todos os atributos necessários estejam presentes, porque a falha em corresponder a algum qualificador pode resultar em alguns atributos ficarem em NULL, em vez de nenhum conjunto ser retornado. `RecheckForeignScan` pode reverificar os qualificadores e retornar verdadeiro se ainda estiverem satisfeitos e falso caso contrário, mas também pode armazenar um conjunto de substituição no slot fornecido.

Para implementar o join pushdown, um repositório de dados externo normalmente constrói um plano de junção local alternativo que é usado apenas para rechecks; este se tornará o subplano externo do `ForeignScan`. Quando é necessário um recheck, este subplano pode ser executado e o tuplo resultante pode ser armazenado no slot. Este plano não precisa ser eficiente, uma vez que nenhuma tabela base retornará mais de uma linha; por exemplo, ele pode implementar todos os junções como laços aninhados. A função `GetExistingLocalJoinPath` pode ser usada para procurar caminhos existentes para um caminho de junção local adequado, que pode ser usado como o plano de junção local alternativo. `GetExistingLocalJoinPath` busca um caminho não parametrizado na lista de caminhos da relação de junção especificada. (Se não encontrar tal caminho, ele retorna NULL, e, nesse caso, um repositório de dados externo pode construir o caminho local por si mesmo ou pode optar por não criar caminhos de acesso para essa junção.)

### 58.2.7. Rotinas FDW para `EXPLAIN` [#](#FDW-CALLBACKS-EXPLAIN)

```
void
ExplainForeignScan(ForeignScanState *node,
                   ExplainState *es);
```

Imprima saída adicional de `EXPLAIN` para uma varredura de tabela estrangeira. Esta função pode chamar `ExplainPropertyText` e funções relacionadas para adicionar campos à saída de `EXPLAIN`. Os campos de bandeira em `es` podem ser usados para determinar o que deve ser impresso, e o estado do nó de `ForeignScanState` pode ser inspecionado para fornecer estatísticas de execução no caso de `EXPLAIN ANALYZE`.

Se o ponteiro `ExplainForeignScan` estiver definido como `NULL`, nenhuma informação adicional será impressa durante o `EXPLAIN`.

```
void
ExplainForeignModify(ModifyTableState *mtstate,
                     ResultRelInfo *rinfo,
                     List *fdw_private,
                     int subplan_index,
                     struct ExplainState *es);
```

Imprima saída adicional de `EXPLAIN` para uma atualização de tabela estrangeira. Esta função pode chamar `ExplainPropertyText` e funções relacionadas para adicionar campos à saída de `EXPLAIN`. Os campos de sinalização em `es` podem ser usados para determinar o que deve ser impresso, e o estado do nó de `ModifyTableState` pode ser inspecionado para fornecer estatísticas de execução no caso de `EXPLAIN ANALYZE`. Os quatro primeiros argumentos são os mesmos para `BeginForeignModify`.

Se o ponteiro `ExplainForeignModify` estiver configurado como `NULL`, nenhuma informação adicional será impressa durante o `EXPLAIN`.

```
void
ExplainDirectModify(ForeignScanState *node,
                    ExplainState *es);
```

Imprima uma saída adicional `EXPLAIN` para uma modificação direta no servidor remoto. Esta função pode chamar `ExplainPropertyText` e funções relacionadas para adicionar campos à saída `EXPLAIN`. Os campos de sinalização em `es` podem ser usados para determinar o que deve ser impresso, e o estado do nó `ForeignScanState` pode ser inspecionado para fornecer estatísticas de execução no caso de `EXPLAIN ANALYZE`.

Se o ponteiro `ExplainDirectModify` estiver configurado para `NULL`, nenhuma informação adicional será impressa durante o `EXPLAIN`.

### 58.2.8. Rotinas FDW para `ANALYZE` [#](#FDW-CALLBACKS-ANALYZE)

```
bool
AnalyzeForeignTable(Relation relation,
                    AcquireSampleRowsFunc *func,
                    BlockNumber *totalpages);
```

Essa função é chamada quando [ANALYZE](sql-analyze.md) é executada em uma tabela estrangeira. Se o FDW puder coletar estatísticas para essa tabela estrangeira, deve retornar `true`, e fornecer um ponteiro para uma função que coletará linhas de amostra da tabela em *`func`*, além do tamanho estimado da tabela em páginas em *`totalpages`*. Caso contrário, retorne `false`.

Se o FDW não suportar a coleta de estatísticas para quaisquer tabelas, o ponteiro `AnalyzeForeignTable` pode ser definido como `NULL`.

Se fornecida, a função de coleta de amostra deve ter a assinatura

```
int
AcquireSampleRowsFunc(Relation relation,
                      int elevel,
                      HeapTuple *rows,
                      int targrows,
                      double *totalrows,
                      double *totaldeadrows);
```

Uma amostra aleatória de até *`targrows`* linhas deve ser coletada da tabela e armazenada no array fornecido pelo solicitante *`rows`*. O número real de linhas coletadas deve ser retornado. Além disso, armazene estimativas dos números totais de linhas vivas e mortas na tabela nos parâmetros de saída *`totalrows`* e *`totaldeadrows`*. (Defina *`totaldeadrows`* como zero se o FDW não tiver nenhum conceito de linhas mortas.)

### 58.2.9. Rotinas FDW para `IMPORT FOREIGN SCHEMA` [#](#FDW-CALLBACKS-IMPORT)

```
List *
ImportForeignSchema(ImportForeignSchemaStmt *stmt, Oid serverOid);
```

Obtenha uma lista de comandos de criação de tabelas estrangeiras. Esta função é chamada ao executar [IMPORT FOREIGN SCHEMA](sql-importforeignschema.md), e é passada a árvore de análise para essa declaração, bem como o OID do servidor estrangeiro a ser usado. Ela deve retornar uma lista de strings em C, cada uma das quais deve conter um comando [CREATE FOREIGN TABLE](sql-createforeigntable.md). Essas strings serão analisadas e executadas pelo servidor principal.

Dentro da estrutura `ImportForeignSchemaStmt`, `remote_schema` é o nome do esquema remoto a partir do qual as tabelas devem ser importadas. `list_type` identifica como filtrar os nomes das tabelas: `FDW_IMPORT_SCHEMA_ALL` significa que todas as tabelas no esquema remoto devem ser importadas (neste caso, `table_list` está vazio), `FDW_IMPORT_SCHEMA_LIMIT_TO` significa incluir apenas as tabelas listadas em `table_list`, e `FDW_IMPORT_SCHEMA_EXCEPT` significa excluir as tabelas listadas em `table_list`. `options` é uma lista de opções usadas para o processo de importação. Os significados das opções cabem ao FDW. Por exemplo, um FDW pode usar uma opção para definir se os atributos `NOT NULL` das colunas devem ser importados. Essas opções não precisam ter nada a ver com as suportadas pelo FDW como opções de objeto de banco de dados.

O FDW pode ignorar o campo `local_schema` do `ImportForeignSchemaStmt`, porque o servidor principal inserirá automaticamente esse nome nos comandos `CREATE FOREIGN TABLE` analisados.

O FDW também não precisa se preocupar em implementar o filtro especificado por `list_type` e `table_list`, pois o servidor principal ignorará automaticamente quaisquer comandos retornados para tabelas excluídas de acordo com essas opções. No entanto, muitas vezes é útil evitar o trabalho de criar comandos para tabelas excluídas. A função `IsImportableForeignTable()` pode ser útil para testar se um nome de tabela estrangeira específico passará pelo filtro.

Se o FDW não suportar a importação de definições de tabela, o ponteiro `ImportForeignSchema` pode ser definido como `NULL`.

### 58.2.10. Rotinas FDW para Execução Paralela [#](#FDW-CALLBACKS-PARALLEL)

Um nó `ForeignScan` pode, opcionalmente, suportar execução paralela. Um `ForeignScan` paralelo será executado em vários processos e deve retornar cada linha exatamente uma vez em todos os processos cooperantes. Para isso, os processos podem coordenar por meio de blocos de memória compartilhada dinâmica de tamanho fixo. Essa memória compartilhada não é garantida para ser mapeada no mesmo endereço em todos os processos, portanto, não deve conter ponteiros. As seguintes funções são todas opcionais, mas a maioria é necessária se a execução paralela deve ser suportada.

```
bool
IsForeignScanParallelSafe(PlannerInfo *root, RelOptInfo *rel,
                          RangeTblEntry *rte);
```

Teste se uma varredura pode ser realizada em um trabalhador paralelo. Esta função será chamada apenas quando o planejador acreditar que um plano paralelo seja possível e deve retornar verdadeiro se for seguro que a varredura possa ser executada em um trabalhador paralelo. Geralmente, isso não será o caso se a fonte de dados remota tiver semântica de transação, a menos que a conexão do trabalhador com os dados possa de alguma forma ser feita para compartilhar o mesmo contexto de transação que o líder.

Se essa função não for definida, presume-se que a varredura deve ocorrer dentro do líder paralelo. Observe que retornar verdadeiro não significa que a varredura em si pode ser feita em paralelo, apenas que a varredura pode ser realizada dentro de um trabalhador paralelo. Portanto, pode ser útil definir esse método mesmo quando a execução paralela não é suportada.

```
Size
EstimateDSMForeignScan(ForeignScanState *node, ParallelContext *pcxt);
```

Estime a quantidade de memória compartilhada dinâmica que será necessária para a operação paralela. Isso pode ser maior que a quantidade que será realmente usada, mas não deve ser menor. O valor de retorno é em bytes. Esta função é opcional e pode ser omitida se não for necessária; mas se for omitida, as próximas três funções também devem ser omitidas, porque nenhuma memória compartilhada será alocada para uso do FDW.

```
void
InitializeDSMForeignScan(ForeignScanState *node, ParallelContext *pcxt,
                         void *coordinate);
```

Inicialize a memória compartilhada dinâmica que será necessária para a operação paralela. `coordinate` aponta para uma área de memória compartilhada do tamanho igual ao valor de retorno de `EstimateDSMForeignScan`. Esta função é opcional e pode ser omitida se não for necessária.

```
void
ReInitializeDSMForeignScan(ForeignScanState *node, ParallelContext *pcxt,
                           void *coordinate);
```

Reiniicie a memória compartilhada dinâmica necessária para operação paralela quando o nó do plano de varredura externa estiver prestes a ser re-escaneado. Esta função é opcional e pode ser omitida se não for necessária. A prática recomendada é que esta função reescreva apenas o estado compartilhado, enquanto a função `ReScanForeignScan` reescreve apenas o estado local. Atualmente, esta função será chamada antes de `ReScanForeignScan`, mas é melhor não confiar nessa ordem.

```
void
InitializeWorkerForeignScan(ForeignScanState *node, shm_toc *toc,
                            void *coordinate);
```

Inicialize o estado local de um trabalhador paralelo com base no estado compartilhado configurado pelo líder durante `InitializeDSMForeignScan`. Essa função é opcional e pode ser omitida se não for necessária.

```
void
ShutdownForeignScan(ForeignScanState *node);
```

Liberte recursos quando é esperado que o nó não seja executado até o final. Isso não é chamado em todos os casos; às vezes, `EndForeignScan` pode ser chamado sem que essa função tenha sido chamada primeiro. Como o segmento DSM usado pelo query paralelo é destruído logo após esse callback ser invocado, os wrappers de dados externos que desejam realizar alguma ação antes que o segmento DSM desapareça devem implementar esse método.

### 58.2.11. Rotinas FDW para Execução Assíncrona [#](#FDW-CALLBACKS-ASYNC)

Um nó `ForeignScan` pode, opcionalmente, suportar execução assíncrona conforme descrito em `src/backend/executor/README`. As seguintes funções são todas opcionais, mas são todas necessárias se a execução assíncrona deve ser suportada.

```
bool
IsForeignPathAsyncCapable(ForeignPath *path);
```

Teste se um caminho dado `ForeignPath` pode escanear a relação externa subjacente de forma assíncrona. Esta função só será chamada no final do planejamento da consulta quando o caminho dado for uma criança direta de um caminho `AppendPath` e quando o planejador acredita que a execução assíncrona melhora o desempenho, e deve retornar verdadeiro se o caminho dado for capaz de escanear a relação externa de forma assíncrona.

Se essa função não for definida, presume-se que o caminho fornecido varra a relação estrangeira usando `IterateForeignScan`. (Isso implica que as funções de callback descritas abaixo nunca serão chamadas, portanto, elas não precisam ser fornecidas também.)

```
void
ForeignAsyncRequest(AsyncRequest *areq);
```

Produza um tuplo de forma assíncrona a partir do nó `ForeignScan`. `areq` é a estrutura `AsyncRequest` que descreve o nó `ForeignScan` e o nó `Append` pai que solicitou o tuplo a partir dele. Esta função deve armazenar o tuplo no slot especificado por `areq->result`, e definir `areq->request_complete` para `true`; ou se precisar esperar por um evento externo ao servidor principal, como I/O de rede, e não puder produzir nenhum tuplo imediatamente, defina a bandeira para `false`, e defina `areq->callback_pending` para `true` para o nó `ForeignScan` receber um callback das funções de callback descritas abaixo. Se não houver mais tuplos disponíveis, defina o slot para NULL ou um slot vazio, e a bandeira `areq->request_complete`. É recomendável usar `ExecAsyncRequestDone` ou `ExecAsyncRequestPending` para definir os parâmetros de saída no slot `areq`.

```
void
ForeignAsyncConfigureWait(AsyncRequest *areq);
```

Configure um evento de descritor de arquivo para o qual o nó `ForeignScan` deseja esperar. Esta função será chamada apenas quando o nó `ForeignScan` tiver a bandeira `areq->callback_pending` definida e deve adicionar o evento ao `as_eventset` do nó `Append` pai descrito pelo nó `areq`. Consulte os comentários para `ExecAsyncConfigureWait` em `src/backend/executor/execAsync.c` para informações adicionais. Quando o evento de descritor de arquivo ocorrer, `ForeignAsyncNotify` será chamado.

```
void
ForeignAsyncNotify(AsyncRequest *areq);
```

Processar um evento relevante que ocorreu, em seguida, produzir um tuplo de forma assíncrona a partir do nó `ForeignScan`. Esta função deve definir os parâmetros de saída no `areq` da mesma forma que `ForeignAsyncRequest`.

### 58.2.12. Rotinas FDW para Reparametrização de Caminhos [#](#FDW-CALLBACKS-REPARAMETERIZE-PATHS)

```
List *
ReparameterizeForeignPathByChild(PlannerInfo *root, List *fdw_private,
                                 RelOptInfo *child_rel);
```

Essa função é chamada durante a conversão de um caminho parametrizado pelo parente mais alto da relação de filho dada `child_rel` para ser parametrizado pela relação de filho. A função é usada para reparametrizar quaisquer caminhos ou traduzir quaisquer nós de expressão salvos no membro dado `fdw_private` de um `ForeignPath`. O callback pode usar `reparameterize_path_by_child`, `adjust_appendrel_attrs` ou `adjust_appendrel_attrs_multilevel` conforme necessário.