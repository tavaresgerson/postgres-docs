## 59.1. Funções de Suporte ao Método de Amostragem [#](#TABLESAMPLE-SUPPORT-FUNCTIONS)

A função de manipulação TSM retorna uma estrutura `TsmRoutine` palloc, contendo ponteiros para as funções de suporte descritas abaixo. A maioria das funções é necessária, mas algumas são opcionais, e esses ponteiros podem ser NULL.

```
void
SampleScanGetSampleSize (PlannerInfo *root,
                         RelOptInfo *baserel,
                         List *paramexprs,
                         BlockNumber *pages,
                         double *tuples);
```

Essa função é chamada durante o planejamento. Ela deve estimar o número de páginas de relação que serão lidas durante uma varredura de amostragem e o número de tuplas que serão selecionadas pela varredura. (Por exemplo, essas podem ser determinadas estimando a fração de amostragem e, em seguida, multiplicando os números `baserel->pages` e `baserel->tuples` por isso, garantindo que os resultados sejam arredondados para valores inteiros). A lista `paramexprs` contém a(s) expressão(ões) que são parâmetros para a cláusula `TABLESAMPLE`. Recomenda-se usar `estimate_expression_value()` para tentar reduzir essas expressões a constantes, se seus valores forem necessários para fins de estimativa; mas a função deve fornecer estimativas de tamanho mesmo que não possam ser reduzidas, e não deve falhar mesmo se os valores parecerem inválidos (lembre-se de que são apenas estimativas do que os valores de execução serão). Os parâmetros `pages` e `tuples` são saídas.

```
void
InitSampleScan (SampleScanState *node,
                int eflags);
```

Inicializar para execução de um nó de plano SampleScan. Isso é chamado durante o início do executor. Deve realizar qualquer inicialização necessária antes que o processamento possa começar. O nó `SampleScanState` já foi criado, mas seu campo `tsm_state` é NULL. A função `InitSampleScan` pode pallocar quaisquer dados de estado interno necessários pelo método de amostragem e armazenar um ponteiro para eles em `node->tsm_state`. As informações sobre a tabela a ser analisada são acessíveis através de outros campos do nó `SampleScanState` (mas note que o descritor de varredura `node->ss.ss_currentScanDesc` ainda não está configurado). `eflags` contém bits de sinalização que descrevem o modo operacional do executor para este nó do plano.

Quando `(eflags & EXEC_FLAG_EXPLAIN_ONLY)` é verdadeiro, o exame não será realizado, portanto, essa função deve realizar apenas o mínimo necessário para tornar o estado do nó válido para `EXPLAIN` e `EndSampleScan`.

Essa função pode ser omitida (definir o ponteiro como NULL), nesse caso, o `BeginSampleScan` deve realizar toda a inicialização necessária pelo método de amostragem.

```
void
BeginSampleScan (SampleScanState *node,
                 Datum *params,
                 int nparams,
                 uint32 seed);
```

Comece a execução de uma varredura de amostragem. Isso é chamado pouco antes da primeira tentativa de obter um tuplo, e pode ser chamado novamente se a varredura precisar ser reiniciada. As informações sobre a tabela a ser varrida são acessíveis através dos campos do nó `SampleScanState` (mas note que o descritor de varredura `node->ss.ss_currentScanDesc` ainda não está configurado). O array `params`, com comprimento `nparams`, contém os valores dos parâmetros fornecidos na cláusula `TABLESAMPLE`. Esses terão o número e os tipos especificados na lista `parameterTypes` do método de amostragem, e foram verificados para não serem nulos. `seed` contém uma semente para usar em quaisquer números aleatórios gerados dentro do método de amostragem; é ou um hash derivado do valor `REPEATABLE` se um foi fornecido, ou o resultado de `random()` se não for.

Essa função pode ajustar os campos `node->use_bulkread` e `node->use_pagemode`. Se `node->use_bulkread` for `true`, o que é o padrão, a varredura usará uma estratégia de acesso a buffer que incentiva o reciclagem de buffers após o uso. Pode ser razoável definir isso para `false` se a varredura visitar apenas uma pequena fração das páginas da tabela. Se `node->use_pagemode` for `true`, o que é o padrão, a varredura realizará verificação de visibilidade em uma única passagem para todos os tuplos em cada página visitada. Pode ser razoável definir isso para `false` se a varredura selecionar apenas uma pequena fração dos tuplos em cada página visitada. Isso resultará em menos verificações de visibilidade de tuplos sendo realizadas, embora cada uma delas seja mais cara porque exigirá mais bloqueio.

Se o método de amostragem estiver marcado como `repeatable_across_scans`, ele deve ser capaz de selecionar o mesmo conjunto de tuplas durante uma nova varredura, ou seja, uma nova chamada de `BeginSampleScan` deve levar à seleção das mesmas tuplas que antes (se os parâmetros e a semente do `TABLESAMPLE` não mudarem).

```
BlockNumber
NextSampleBlock (SampleScanState *node, BlockNumber nblocks);
```

Retorna o número de bloco da próxima página a ser analisada, ou `InvalidBlockNumber` se não houver mais páginas a serem analisadas.

Essa função pode ser omitida (definir o ponteiro como NULL), nesse caso, o código central realizará uma varredura sequencial de toda a relação. Tal varredura pode usar varredura sincronizada, de modo que o método de amostragem não possa assumir que as páginas da relação são visitadas na mesma ordem em cada varredura.

```
OffsetNumber
NextSampleTuple (SampleScanState *node,
                 BlockNumber blockno,
                 OffsetNumber maxoffset);
```

Retorna o número de deslocamento do próximo tuplo a ser amostrado na página especificada, ou `InvalidOffsetNumber` se não houver tuplos a serem amostrados. `maxoffset` é o maior número de deslocamento em uso na página.

Nota

`NextSampleTuple` não é explicitamente informado quais dos números de deslocamento na faixa `1 .. maxoffset` realmente contêm tuplas válidas. Isso normalmente não é um problema, uma vez que o código principal ignora solicitações para amostrar tuplas ausentes ou invisíveis; isso não deve resultar em qualquer viés na amostra. No entanto, se necessário, a função pode usar `node->donetuples` para examinar quantas das tuplas que ela retornou foram válidas e visíveis.

Nota

`NextSampleTuple` não deve *não* assumir que `blockno` seja o mesmo número de página retornado pela chamada mais recente de `NextSampleBlock`. Foi retornado por alguma chamada anterior de `NextSampleBlock`, mas o código principal é permitido chamar `NextSampleBlock` antes de realmente digitalizar as páginas, a fim de suportar o pré-enchimento. É OK assumir que, uma vez que a amostragem de uma página dada começa, as chamadas consecutivas de `NextSampleTuple` todas se referem à mesma página até que `InvalidOffsetNumber` seja retornado.

```
void
EndSampleScan (SampleScanState *node);
```

Finalize a varredura e libere os recursos. Normalmente, não é importante liberar memória palloc, mas quaisquer recursos visíveis externamente devem ser limpos. Esta função pode ser omitida (definir o ponteiro como NULL) no caso comum em que tais recursos não existem.