## 60.2. Criando Planos de Escaneamento Personalizados [#](#CUSTOM-SCAN-PLAN)

* [60.2.1. Retornos de chamadas do plano de varredura personalizada](custom-scan-plan.md#CUSTOM-SCAN-PLAN-CALLBACKS)

Um exame personalizado é representado em uma árvore de plano finalizada usando a seguinte estrutura:

```
typedef struct CustomScan
{
    Scan      scan;
    uint32    flags;
    List     *custom_plans;
    List     *custom_exprs;
    List     *custom_private;
    List     *custom_scan_tlist;
    Bitmapset *custom_relids;
    const CustomScanMethods *methods;
} CustomScan;
```

`scan` deve ser inicializado como para qualquer outro scan, incluindo custos estimados, listas de alvos, qualificações, e assim por diante. `flags` é uma máscara de bits com o mesmo significado que em `CustomPath`. `custom_plans` pode ser usado para armazenar nós de `Plan` de crianças. `custom_exprs` deve ser usado para armazenar árvores de expressão que precisarão ser corrigidas por `setrefs.c` e `subselect.c`, enquanto `custom_private` deve ser usado para armazenar outros dados privados que são usados apenas pelo próprio provedor de varredura personalizada. `custom_scan_tlist` pode ser NIL ao digitalizar uma relação base, indicando que a varredura personalizada retorna tuplas de varredura que correspondem ao tipo de linha da relação base. Caso contrário, é uma lista de alvos que descreve as tuplas de varredura reais. `custom_scan_tlist` deve ser fornecido para junções, e pode ser fornecido para varreduras se o provedor de varredura personalizada puder calcular algumas expressões não-Var. `custom_relids` é definido pelo código central no conjunto de relações (índices de tabelas de intervalo) que este nó de varredura lida; exceto quando esta varredura está substituindo uma junção, terá apenas um membro. `methods` deve apontar para um objeto (geralmente alocado estaticamente) que implemente os métodos de varredura personalizados requeridos, que são detalhados mais abaixo.

Quando um `CustomScan` analisa uma única relação, o índice de tabela de intervalo `scan.scanrelid` deve ser a tabela a ser analisada. Quando ele substitui uma junção, o `scan.scanrelid` deve ser zero.

Os planos de árvores devem ser capazes de ser duplicados usando `copyObject`, portanto, todos os dados armazenados nos campos “personalizados” devem consistir em nós que a função pode manipular. Além disso, os provedores de varredura personalizados não podem substituir uma estrutura maior que incorpora um `CustomScan` pela própria estrutura, como seria possível para um `CustomPath` ou `CustomScanState`.

### 60.2.1. Retornos de chamadas do plano de varredura personalizada [#](#CUSTOM-SCAN-PLAN-CALLBACKS)

```
Node *(*CreateCustomScanState) (CustomScan *cscan);
```

Atribua um `CustomScanState` para este `CustomScan`. A alocação real será frequentemente maior do que o necessário para um `CustomScanState` comum, porque muitos provedores desejam incluir isso como o primeiro campo de uma estrutura maior. O valor retornado deve ter a tag do nó e o `methods` definidos apropriadamente, mas outros campos devem ser deixados como zeros nesta etapa; após o `ExecInitCustomScan` realizar a inicialização básica, o callback do `BeginCustomScan` será invocado para dar ao provedor de varredura personalizado a chance de fazer o que for necessário.