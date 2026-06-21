## 60.1. Criando Caminhos de varredura personalizados [#](#CUSTOM-SCAN-PATH)

* [60.1.1. Retornos de chamadas de caminho de varredura personalizado](custom-scan-path.md#CUSTOM-SCAN-PATH-CALLBACKS)

Um provedor de varredura personalizado normalmente adiciona caminhos para uma relação básica ao definir o seguinte gancho, que é chamado após o código principal ter gerado todos os caminhos de acesso que pode para a relação (exceto os caminhos de Reúso e Reúso Merge, que são feitos após essa chamada, para que possam usar caminhos parciais adicionados pelo gancho):

```
typedef void (*set_rel_pathlist_hook_type) (PlannerInfo *root,
                                            RelOptInfo *rel,
                                            Index rti,
                                            RangeTblEntry *rte);
extern PGDLLIMPORT set_rel_pathlist_hook_type set_rel_pathlist_hook;
```

Embora essa função de gancho possa ser usada para examinar, modificar ou remover caminhos gerados pelo sistema central, um provedor de varredura personalizado geralmente se limita a gerar objetos `CustomPath` e adicioná-los ao `rel` usando `add_path`, ou `add_partial_path`, se forem caminhos parciais. O provedor de varredura personalizado é responsável por inicializar o objeto `CustomPath`, que é declarado da seguinte forma:

```
typedef struct CustomPath
{
    Path      path;
    uint32    flags;
    List     *custom_paths;
    List     *custom_restrictinfo;
    List     *custom_private;
    const CustomPathMethods *methods;
} CustomPath;
```

`path` deve ser inicializado como para qualquer outro caminho, incluindo a estimativa de contagem de linhas, o custo inicial e total, e a ordem de classificação fornecida por este caminho. `flags` é uma máscara de bits, que especifica se o provedor de varredura pode suportar certas capacidades opcionais. `flags` deve incluir `CUSTOMPATH_SUPPORT_BACKWARD_SCAN` se o caminho personalizado puder suportar uma varredura reversa, `CUSTOMPATH_SUPPORT_MARK_RESTORE` se puder suportar marca e restauração, e `CUSTOMPATH_SUPPORT_PROJECTION` se puder realizar projeções. (Se `CUSTOMPATH_SUPPORT_PROJECTION` não for definido, o nó de varredura será solicitado apenas para produzir Vars da relação varrida; enquanto, se essa bandeira for definida, o nó de varredura deve ser capaz de avaliar expressões escalares sobre esses Vars.) Um `custom_paths` opcional é uma lista de nós `Path` usados por este nó de caminho personalizado; estes serão transformados em nós `Plan` pelo planejador. Como descrito abaixo, caminhos personalizados também podem ser criados para relações de junção. Nesse caso, `custom_restrictinfo` deve ser usado para armazenar o conjunto de cláusulas de junção a serem aplicadas à junção que o caminho personalizado substitui. Caso contrário, deve ser NIL. `custom_private` pode ser usado para armazenar os dados privados do caminho personalizado. Os dados privados devem ser armazenados em um formato que possa ser manipulado por `nodeToString`, para que as rotinas de depuração que tentam imprimir o caminho personalizado funcionem conforme o planejado. `methods` deve apontar para um objeto (geralmente alocado estaticamente) que implemente os métodos de caminho personalizado requeridos, que são detalhados abaixo.

Um provedor de caminho de junção personalizado também pode fornecer caminhos de junção. Assim como para relações básicas, esse caminho deve produzir o mesmo resultado que normalmente seria produzido pela junção que ele substitui. Para isso, o provedor de junção deve definir o seguinte gancho e, em seguida, dentro da função do gancho, criar os caminhos `CustomPath` para a relação de junção.

```
typedef void (*set_join_pathlist_hook_type) (PlannerInfo *root,
                                             RelOptInfo *joinrel,
                                             RelOptInfo *outerrel,
                                             RelOptInfo *innerrel,
                                             JoinType jointype,
                                             JoinPathExtraData *extra);
extern PGDLLIMPORT set_join_pathlist_hook_type set_join_pathlist_hook;
```

Esse gancho será invocado repetidamente para a mesma relação de junção, com diferentes combinações de relações internas e externas; é responsabilidade do gancho minimizar o trabalho duplicado.

Observe também que o conjunto de cláusulas de junção a serem aplicadas à junção, que é passado como `extra->restrictlist`, varia dependendo da combinação de relações internas e externas. Um caminho `CustomPath` gerado para o caminho `joinrel` deve conter o conjunto de cláusulas de junção que ele utiliza, que será utilizado pelo planejador para converter o caminho `CustomPath` em um plano, se for selecionado pelo planejador como o melhor caminho para o caminho `joinrel`.

### 60.1.1. Retornos de chamadas de caminho de varredura personalizado [#](#CUSTOM-SCAN-PATH-CALLBACKS)

```
Plan *(*PlanCustomPath) (PlannerInfo *root,
                         RelOptInfo *rel,
                         CustomPath *best_path,
                         List *tlist,
                         List *clauses,
                         List *custom_plans);
```

Converte um caminho personalizado em um plano finalizado. O valor de retorno geralmente será um objeto `CustomScan`, que o callback deve alocar e inicializar. Consulte [Seção 60.2][(custom-scan-plan.md "60.2. Creating Custom Scan Plans")] para mais detalhes.

```
List *(*ReparameterizeCustomPathByChild) (PlannerInfo *root,
                                          List *custom_private,
                                          RelOptInfo *child_rel);
```

Esse callback é chamado durante a conversão de um caminho parametrizado pelo parent mais alto da relação de filho dada `child_rel` para ser parametrizado pela relação de filho. O callback é usado para reparametrizar quaisquer caminhos ou traduzir quaisquer nós de expressão salvos no membro dado `custom_private` de um `CustomPath`. O callback pode usar `reparameterize_path_by_child`, `adjust_appendrel_attrs` ou `adjust_appendrel_attrs_multilevel` conforme necessário.