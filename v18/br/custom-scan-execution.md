## 60.3. Executar varreduras personalizadas [#](#CUSTOM-SCAN-EXECUTION)

* [60.3.1. Chamadas de retorno de execução de varredura personalizada](custom-scan-execution.md#CUSTOM-SCAN-EXECUTION-CALLBACKS)

Quando um `CustomScan` é executado, seu estado de execução é representado por um `CustomScanState`, que é declarado da seguinte forma:

```
typedef struct CustomScanState
{
    ScanState ss;
    uint32    flags;
    const CustomExecMethods *methods;
} CustomScanState;
```

`ss` é inicializado como para qualquer outro estado de varredura, exceto que, se a varredura for para uma junção em vez de uma relação de base, `ss.ss_currentRelation` é deixado NULL. `flags` é uma máscara de bits com o mesmo significado que em `CustomPath` e `CustomScan`. `methods` deve apontar para um objeto (geralmente alocado estaticamente) que implemente os métodos de estado de varredura personalizados necessários, que são detalhados abaixo. Tipicamente, um `CustomScanState`, que não precisa suportar `copyObject`, será na verdade uma estrutura maior que incorpora o acima como seu primeiro membro.

### 60.3.1. Chamadas de retorno de execução de varredura personalizada [#](#CUSTOM-SCAN-EXECUTION-CALLBACKS)

```
void (*BeginCustomScan) (CustomScanState *node,
                         EState *estate,
                         int eflags);
```

Inicialização completa do fornecido `CustomScanState`. Os campos padrão foram inicializados por `ExecInitCustomScan`, mas quaisquer campos privados devem ser inicializados aqui.

```
TupleTableSlot *(*ExecCustomScan) (CustomScanState *node);
```

Pegue o próximo tuplo de varredura. Se houver algum tuplo restante, ele deve preencher `ps_ResultTupleSlot` com o próximo tuplo na direção atual da varredura, e então retornar o slot do tuplo. Se não, `NULL` ou um slot vazio deve ser retornado.

```
void (*EndCustomScan) (CustomScanState *node);
```

Limpe quaisquer dados privados associados ao `CustomScanState`. Esse método é necessário, mas não precisa fazer nada se não houver dados associados, pois eles serão limpos automaticamente.

```
void (*ReScanCustomScan) (CustomScanState *node);
```

Reveja a varredura atual até o início e prepare-se para fazer uma nova varredura da relação.

```
void (*MarkPosCustomScan) (CustomScanState *node);
```

Salve a posição atual do rastreamento para que ela possa ser posteriormente restaurada pelo callback `RestrPosCustomScan`. Este callback é opcional e só precisa ser fornecido se a bandeira `CUSTOMPATH_SUPPORT_MARK_RESTORE` estiver definida.

```
void (*RestrPosCustomScan) (CustomScanState *node);
```

Restaure a posição anterior da varredura conforme salva pelo callback `MarkPosCustomScan`. Este callback é opcional e só precisa ser fornecido se a bandeira `CUSTOMPATH_SUPPORT_MARK_RESTORE` estiver definida.

```
Size (*EstimateDSMCustomScan) (CustomScanState *node,
                               ParallelContext *pcxt);
```

Estime a quantidade de memória compartilhada dinâmica que será necessária para a operação paralela. Isso pode ser maior que a quantidade que será realmente usada, mas não deve ser menor. O valor de retorno é em bytes. Este callback é opcional e só precisa ser fornecido se este provedor de varredura personalizado suportar execução paralela.

```
void (*InitializeDSMCustomScan) (CustomScanState *node,
                                 ParallelContext *pcxt,
                                 void *coordinate);
```

Inicialize a memória compartilhada dinâmica que será necessária para a operação paralela. `coordinate` aponta para uma área de memória compartilhada do tamanho igual ao valor de retorno de `EstimateDSMCustomScan`. Esse callback é opcional e só precisa ser fornecido se esse provedor de varredura personalizado suportar execução paralela.

```
void (*ReInitializeDSMCustomScan) (CustomScanState *node,
                                   ParallelContext *pcxt,
                                   void *coordinate);
```

Reiniicie a memória compartilhada dinâmica necessária para operação paralela quando o nó do plano de varredura personalizada está prestes a ser re-escaneado. Esse callback é opcional e só precisa ser fornecido se esse provedor de varredura personalizada suportar execução paralela. A prática recomendada é que esse callback redimensione apenas o estado compartilhado, enquanto o callback `ReScanCustomScan` redimensione apenas o estado local. Atualmente, esse callback será chamado antes do `ReScanCustomScan`, mas é melhor não confiar nessa ordem.

```
void (*InitializeWorkerCustomScan) (CustomScanState *node,
                                    shm_toc *toc,
                                    void *coordinate);
```

Inicialize o estado local de um trabalhador paralelo com base no conjunto de estado compartilhado configurado pelo líder durante `InitializeDSMCustomScan`. Esse callback é opcional e deve ser fornecido apenas se esse provedor de varredura personalizado suportar execução paralela.

```
void (*ShutdownCustomScan) (CustomScanState *node);
```

Liberte recursos quando é esperado que o nó não seja executado até o final. Isso não é chamado em todos os casos; às vezes, `EndCustomScan` pode ser chamado sem que essa função tenha sido chamada primeiro. Como o segmento DSM usado pelo query paralelo é destruído logo após esse callback ser invocado, os provedores de varredura personalizados que desejam tomar alguma ação antes que o segmento DSM desapareça devem implementar esse método.

```
void (*ExplainCustomScan) (CustomScanState *node,
                           List *ancestors,
                           ExplainState *es);
```

Forneça informações adicionais para `EXPLAIN` de um nó de plano de varredura personalizada. Esse callback é opcional. Os dados comuns armazenados em `ScanState`, como a lista de alvos e a relação de varredura, serão exibidos mesmo sem esse callback, mas o callback permite a exibição de estado adicional e privado.