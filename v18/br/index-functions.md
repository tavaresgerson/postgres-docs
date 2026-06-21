## 63.2. Funções de Método de Acesso ao Índice [#](#INDEX-FUNCTIONS)

As funções de construção e manutenção de índice que um método de acesso a índice deve fornecer no `IndexAmRoutine` são:

```
IndexBuildResult *
ambuild (Relation heapRelation,
         Relation indexRelation,
         IndexInfo *indexInfo);
```

Crie um novo índice. A relação do índice foi criada fisicamente, mas está vazia. Ela deve ser preenchida com qualquer dado fixo que o método de acesso exija, além de entradas para todos os tuplos já existentes na tabela. Normalmente, a função `ambuild` chamará `table_index_build_scan()` para escanear a tabela em busca de tuplos existentes e calcular as chaves que precisam ser inseridas no índice. A função deve retornar uma estrutura palloc que contenha estatísticas sobre o novo índice. A bandeira `amcanbuildparallel` indica se o método de acesso suporta construções de índice paralelas. Quando definida como `true`, o sistema tentará alocar trabalhadores paralelos para a construção. Métodos de acesso que suportam apenas construções de índice não paralelas devem deixar essa bandeira definida como `false`.

```
void
ambuildempty (Relation indexRelation);
```

Crie um índice vazio e escreva-o no ramo de inicialização (`INIT_FORKNUM`) da relação fornecida. Este método é chamado apenas para índices não registrados; o índice vazio escrito no ramo de inicialização será copiado sobre o ramo principal da relação em cada reinício do servidor.

```
bool
aminsert (Relation indexRelation,
          Datum *values,
          bool *isnull,
          ItemPointer heap_tid,
          Relation heapRelation,
          IndexUniqueCheck checkUnique,
          bool indexUnchanged,
          IndexInfo *indexInfo);
```

Insira uma nova tupla em um índice existente. Os arrays `values` e `isnull` fornecem os valores chave a serem indexados, e `heap_tid` é o TID a ser indexado. Se o método de acesso suportar índices únicos (sua bandeira `amcanunique` é verdadeira), então `checkUnique` indica o tipo de verificação de unicidade a ser realizada. Isso varia dependendo se a restrição única é adiável; consulte [Seção 63.5][(index-unique-checks.md "63.5. Index Uniqueness Checks")] para detalhes. Normalmente, o método de acesso só precisa do parâmetro `heapRelation` ao realizar verificação de unicidade (já que, então, terá que olhar no heap para verificar a vitalidade da tupla).

O valor booleano `indexUnchanged` dá uma dica sobre a natureza do tuplo a ser indexado. Quando é verdadeiro, o tuplo é um duplicado de algum tuplo existente no índice. O novo tuplo é uma versão logicamente inalterada do MVCC tuplo. Isso acontece quando ocorre um `UPDATE` que não modifica quaisquer colunas cobertas pelo índice, mas que, no entanto, requer uma nova versão no índice. O AM de índice pode usar essa dica para decidir aplicar a exclusão de índice de baixo para cima em partes do índice onde muitas versões da mesma linha lógica se acumulam. Note que atualizar uma coluna não-chave ou uma coluna que aparece apenas em um predicado de índice parcial não afeta o valor de `indexUnchanged`. O código principal determina o valor `indexUnchanged` de cada tuplo usando uma abordagem de baixo custo que permite tanto falsos positivos quanto falsos negativos. Os AMs de índice não devem tratar `indexUnchanged` como uma fonte autoritária de informações sobre visibilidade ou versionamento de tuplos.

O valor do resultado booleano da função é significativo apenas quando `checkUnique` é `UNIQUE_CHECK_PARTIAL`. Neste caso, um resultado verdadeiro significa que a nova entrada é conhecida como única, enquanto falso significa que pode ser não única (e uma verificação de unicidade diferida deve ser agendada). Para outros casos, é recomendado um resultado constante falso.

Alguns índices podem não indexar todos os tuplos. Se o tuplo não deve ser indexado, `aminsert` deve retornar sem fazer nada.

Se o índice AM desejar armazenar dados em várias inserções sucessivas de índice dentro de uma declaração SQL, pode alocar espaço em `indexInfo->ii_Context` e armazenar um ponteiro para os dados em `indexInfo->ii_AmCache` (que será NULL inicialmente). Se recursos, além da memória, tiverem de ser liberados após as inserções de índice, pode ser fornecida `aminsertcleanup`, que será chamada antes da memória ser liberada.

```
void
aminsertcleanup (Relation indexRelation,
                 IndexInfo *indexInfo);
```

Limpe o estado que foi mantido em inserções sucessivas em `indexInfo->ii_AmCache`. Isso é útil se os dados requerem etapas adicionais de limpeza (por exemplo, liberar buffers presos), e simplesmente liberar a memória não é suficiente.

```
IndexBulkDeleteResult *
ambulkdelete (IndexVacuumInfo *info,
              IndexBulkDeleteResult *stats,
              IndexBulkDeleteCallback callback,
              void *callback_state);
```

Exclua o(s) tupla(s) do índice. Esta é uma operação de "exclusão em massa" que deve ser implementada ao examinar todo o índice e verificar cada entrada para determinar se ela deve ser excluída. A função `callback` passada deve ser chamada, no estilo `callback(TID, callback_state) returns bool`, para determinar se alguma entrada específica do índice, identificada por seu TID referenciado, deve ser excluída. Deve retornar NULL ou uma estrutura palloc'ada contendo estatísticas sobre os efeitos da operação de exclusão. É OK retornar NULL se nenhuma informação precisa ser passada para `amvacuumcleanup`.

Devido ao limite de `maintenance_work_mem`, `ambulkdelete` pode precisar ser chamado mais de uma vez quando muitos tuplos devem ser excluídos. O argumento `stats` é o resultado do chamado anterior para este índice (é NULL para o primeiro chamado dentro de uma operação `VACUUM`). Isso permite que o AM acumule estatísticas em toda a operação. Tipicamente, `ambulkdelete` modificará e retornará a mesma estrutura se o `stats` passado não for nulo.

```
IndexBulkDeleteResult *
amvacuumcleanup (IndexVacuumInfo *info,
                 IndexBulkDeleteResult *stats);
```

Limpe após uma operação `VACUUM` (zero ou mais chamadas `ambulkdelete`). Isso não precisa fazer nada além de retornar estatísticas de índice, mas pode realizar uma limpeza em massa, como recuperar páginas de índice vazias. `stats` é o que a última chamada `ambulkdelete` retornou, ou NULL se `ambulkdelete` não foi chamada porque não foram necessários nenhum tupla a serem excluídos. Se o resultado não for NULL, ele deve ser uma estrutura palloc. As estatísticas que ela contém serão usadas para atualizar `pg_class`, e serão relatadas por `VACUUM` se `VERBOSE` for fornecido. É OK retornar NULL se o índice não foi alterado em absoluto durante a operação `VACUUM`, mas, caso contrário, as estatísticas corretas devem ser retornadas.

`amvacuumcleanup` também será chamado após a conclusão de uma operação `ANALYZE`. Neste caso, `stats` é sempre NULL e qualquer valor de retorno será ignorado. Este caso pode ser distinguido verificando `info->analyze_only`. É recomendável que o método de acesso não faça nada além de limpeza pós-inserção em tal chamada, e que apenas em um processo de trabalhador de autovazamento.

```
bool
amcanreturn (Relation indexRelation, int attno);
```

Verifique se o índice pode suportar [*index-only scans*](indexes-index-only-scans.md "11.9. Index-Only Scans and Covering Indexes") na coluna especificada, retornando o valor original indexado da coluna. O número do atributo é baseado em 1, ou seja, o attno da primeira coluna é 1. Retorna verdadeiro se suportado, caso contrário, falso. Esta função deve sempre retornar verdadeiro para as colunas incluídas (se essas forem suportadas), uma vez que não faz sentido ter uma coluna incluída que não pode ser recuperada. Se o método de acesso não suportar varreduras apenas de índice, o campo `amcanreturn` em sua estrutura `IndexAmRoutine` pode ser definido como NULL.

```
void
amcostestimate (PlannerInfo *root,
                IndexPath *path,
                double loop_count,
                Cost *indexStartupCost,
                Cost *indexTotalCost,
                Selectivity *indexSelectivity,
                double *indexCorrelation,
                double *indexPages);
```

Estime os custos de uma varredura de índice. Essa função é descrita completamente em [Seção 63.6][(index-cost-estimation.md "63.6. Index Cost Estimation Functions")], abaixo.

```
int
amgettreeheight (Relation rel);
```

Calcule a altura de um índice em forma de árvore. Esta informação é fornecida à função `amcostestimate` em `path->indexinfo->tree_height` e pode ser usada para apoiar a estimativa de custo. O resultado não é usado em nenhum outro lugar, portanto, esta função pode ser usada para calcular qualquer tipo de dados (que se encaixe em um número inteiro) sobre o índice que a função de estimativa de custo possa querer saber. Se a computação for cara, pode ser útil armazenar o resultado como parte de `RelationData.rd_amcache`.

```
bytea *
amoptions (ArrayType *reloptions,
           bool validate);
```

Analise e valide o array reloptions para um índice. Isso é chamado apenas quando um array reloptions não nulo existe para o índice. *`reloptions`* é um array `text` contendo entradas na forma de *`name`*`=`*`value`*. A função deve construir um valor `bytea`, que será copiado no campo `rd_options` da entrada relcache do índice. O conteúdo dos dados do valor `bytea` está aberto para o método de acesso definir; a maioria dos métodos de acesso padrão usa a estrutura `StdRdOptions`. Quando *`validate`* é verdadeiro, a função deve reportar uma mensagem de erro adequada se alguma das opções for não reconhecida ou tiver valores inválidos; quando *`validate`* é falso, entradas inválidas devem ser ignoradas silenciosamente. (*`validate`* é falso ao carregar opções já armazenadas em `pg_catalog`; uma entrada inválida só pode ser encontrada se o método de acesso tiver mudado suas regras para opções, e, nesse caso, ignorar entradas obsoletas é apropriado.) É OK retornar NULL se o comportamento padrão é desejado.

```
bool
amproperty (Oid index_oid, int attno,
            IndexAMProperty prop, const char *propname,
            bool *res, bool *isnull);
```

O método `amproperty` permite que os métodos de acesso ao índice sobrescrevam o comportamento padrão do `pg_index_column_has_property` e das funções relacionadas. Se o método de acesso não tiver nenhum comportamento especial para consultas de propriedade de índice, o campo `amproperty` em sua estrutura `IndexAmRoutine` pode ser definido como NULL. Caso contrário, o método `amproperty` será chamado com *`index_oid`* e *`attno`* ambos zero para chamadas de `pg_indexam_has_property`, ou com *`index_oid`* válido e *`attno`* zero para chamadas de `pg_index_has_property`, ou com *`index_oid`* válido e *`attno`* maior que zero para chamadas de `pg_index_column_has_property`. *`prop`* é um valor enum que identifica a propriedade sendo testada, enquanto *`propname`* é o nome original da string da propriedade. Se o código central não reconhecer o nome da propriedade, então *`prop`* é `AMPROP_UNKNOWN`. Os métodos de acesso podem definir nomes de propriedade personalizados, verificando *`propname`* em busca de correspondência (use `pg_strcasecmp` para corresponder, para consistência com o código central); para nomes conhecidos pelo código central, é melhor inspecionar *`prop`*. Se o método `amproperty` retornar `true`, então ele determinou o resultado do teste de propriedade: deve definir `*res` com o valor Booleano a ser retornado, ou definir `*isnull` com `true` para retornar um NULL. (Ambas as variáveis referenciadas são inicializadas com `false` antes da chamada.) Se o método `amproperty` retornar `false`, então o código central prosseguirá com sua lógica normal para determinar o resultado do teste de propriedade.

Os métodos de acesso que suportam testes de operadores de ordenação devem implementar a propriedade `AMPROP_DISTANCE_ORDERABLE`, pois o código principal não sabe como fazer isso e retornará NULL. Também pode ser vantajoso implementar o teste `AMPROP_RETURNABLE`, se isso puder ser feito de forma mais barata do que abrir o índice e chamar `amcanreturn`, que é o comportamento padrão do código principal. O comportamento padrão deve ser satisfatório para todas as outras propriedades padrão.

```
char *
ambuildphasename (int64 phasenum);
```

Retorne o nome textual do número da fase de construção fornecida. Os números das fases são os relatados durante uma construção de índice via a interface `pgstat_progress_update_param`. Os nomes das fases são então exibidos na visualização `pg_stat_progress_create_index`.

```
bool
amvalidate (Oid opclassoid);
```

Valide as entradas do catálogo para a classe de operador especificada, na medida em que o método de acesso possa razoavelmente fazer isso. Por exemplo, isso pode incluir testar se todas as funções de suporte necessárias são fornecidas. A função `amvalidate` deve retornar false se a opclass for inválida. Os problemas devem ser relatados com mensagens `ereport`, tipicamente no nível `INFO`.

```
void
amadjustmembers (Oid opfamilyoid,
                 Oid opclassoid,
                 List *operators,
                 List *functions);
```

Valide os membros propostos de novos operadores e funções de uma família de operadores, na medida em que o método de acesso possa razoavelmente fazer isso, e defina seus tipos de dependência, se o padrão não for satisfatório. Isso é feito durante `CREATE OPERATOR CLASS` e durante `ALTER OPERATOR FAMILY ADD`; no último caso, *`opclassoid`* é `InvalidOid`. Os argumentos de `List` são listas de estruturas `OpFamilyMember`, conforme definido em `amapi.h`. Os testes realizados por essa função são tipicamente um subconjunto dos realizados por `amvalidate`, uma vez que `amadjustmembers` não pode assumir que está vendo um conjunto completo de membros. Por exemplo, seria razoável verificar a assinatura de uma função de suporte, mas não verificar se todas as funções de suporte necessárias são fornecidas. Quaisquer problemas podem ser relatados lançando um erro. Os campos relacionados à dependência das estruturas de `OpFamilyMember` são inicializados pelo código central para criar dependências duras na opclass, se esta é `CREATE OPERATOR CLASS`, ou dependências suaves na opfamily, se esta é `ALTER OPERATOR FAMILY ADD`. `amadjustmembers` pode ajustar esses campos se algum outro comportamento for mais apropriado. Por exemplo, GIN, GiST e SP-GiST sempre definem membros do operador para ter dependências suaves na opfamily, uma vez que a conexão entre um operador e uma opclass é relativamente fraca nesses tipos de índice; portanto, é razoável permitir que os membros do operador sejam adicionados e removidos livremente. Funções de suporte opcionais são tipicamente também dadas dependências suaves, para que possam ser removidas, se necessário.

O propósito de um índice, é claro, é suportar varreduras para tuplas que correspondem a uma condição indexável `WHERE`, frequentemente chamada de *qualificador* ou *chave de varredura*. A semântica da varredura de índice é descrita mais detalhadamente em [Seção 63.3][(index-scanning.md "63.3. Index Scanning")], abaixo. Um método de acesso a índice pode suportar varreduras de índice "simples", varreduras de índice "bitmap" ou ambas. As funções relacionadas à varredura que um método de acesso a índice deve ou pode fornecer são:

```
IndexScanDesc
ambeginscan (Relation indexRelation,
             int nkeys,
             int norderbys);
```

Prepare-se para uma varredura de índice. Os parâmetros `nkeys` e `norderbys` indicam o número de quals e operadores de ordenação que serão usados na varredura; esses podem ser úteis para fins de alocação de espaço. Note que os valores reais das chaves de varredura ainda não são fornecidos. O resultado deve ser uma estrutura palloc. Por razões de implementação, o método de acesso ao índice *deve* criar essa estrutura, chamando `RelationGetIndexScan()`. Na maioria dos casos, `ambeginscan` faz pouco além de fazer esse chamado e, talvez, adquirir bloqueios; as partes interessantes do início da varredura de índice estão em `amrescan`.

```
void
amrescan (IndexScanDesc scan,
          ScanKey keys,
          int nkeys,
          ScanKey orderbys,
          int norderbys);
```

Comece ou reinicie uma varredura de índice, possivelmente com novas chaves de varredura. (Para reiniciar usando chaves previamente passadas, NULL é passado para `keys` e/ou `orderbys`.). Observe que não é permitido que o número de chaves ou operadores de ordem seja maior do que o que foi passado para `ambeginscan`. Na prática, o recurso de reinício é usado quando uma nova tupla externa é selecionada por uma junção de laço aninhado e, portanto, é necessária uma nova comparação de chave, mas a estrutura da chave de varredura permanece a mesma.

```
bool
amgettuple (IndexScanDesc scan,
            ScanDirection direction);
```

Pegue o próximo tuplo no varrimento dado, movendo-se na direção dada (para frente ou para trás no índice). Retorna verdadeiro se um tuplo foi obtido, falso se não houver mais tuplos correspondentes. No caso verdadeiro, o tuplo TID é armazenado na estrutura `scan`. Note que “sucesso” significa apenas que o índice contém uma entrada que corresponde às chaves do varrimento, não que o tuplo necessariamente ainda exista no heap ou passará pelo teste de instantâneo do chamador. No sucesso, `amgettuple` também deve definir `scan->xs_recheck` para verdadeiro ou falso. Falso significa que é certo que a entrada da entrada do índice corresponde às chaves do varrimento. Verdadeiro significa que isso não é certo, e as condições representadas pelas chaves do varrimento devem ser verificadas novamente contra o tuplo do heap após obtê-lo. Esta disposição suporta operadores de índice “perda” (lossy). Note que a verificação será estendida apenas às condições do varrimento; um predicado de índice parcial (se houver) nunca será verificado novamente pelos chamados `amgettuple`.

Se o índice suportar (indexes-index-only-scans.md "11.9. Index-Only Scans and Covering Indexes") (ou seja, `amcanreturn` retornar verdadeiro para qualquer uma de suas colunas), então, em caso de sucesso, a AM também deve verificar `scan->xs_want_itup`, e se isso for verdadeiro, deve retornar os dados originalmente indexados para a entrada do índice. As colunas para as quais `amcanreturn` retornar falso podem ser devolvidas como nulos. Os dados podem ser devolvidos na forma de um ponteiro `IndexTuple` armazenado em `scan->xs_itup`, com descritor de tupla `scan->xs_itupdesc`; ou na forma de um ponteiro `HeapTuple` armazenado em `scan->xs_hitup`, com descritor de tupla `scan->xs_hitupdesc`. (Este último formato deve ser usado ao reconstruir dados que possivelmente não se encaixem em um `IndexTuple`.)) Em qualquer caso, a gestão dos dados referenciados pelo ponteiro é responsabilidade do método de acesso. Os dados devem permanecer válidos pelo menos até o próximo `amgettuple`, `amrescan`, ou `amendscan` para a chamada de varredura.

A função `amgettuple` só precisa ser fornecida se o método de acesso suporte varreduras de índice "simples". Se não for esse o caso, o campo `amgettuple` em sua estrutura `IndexAmRoutine` deve ser definido como NULL.

```
int64
amgetbitmap (IndexScanDesc scan,
             TIDBitmap *tbm);
```

Pegue todos os tuplos no varredura dada e adicione-os ao `TIDBitmap` fornecido pelo chamador (ou seja, o conjunto de IDs de tuplos em qualquer conjunto que já esteja na bitmap). O número de tuplos obtidos é retornado (essa pode ser apenas uma contagem aproximada, por exemplo, alguns AMs não detectam duplicatas). Ao inserir IDs de tuplos na bitmap, `amgetbitmap` pode indicar que uma reverificação das condições de varredura é necessária para IDs específicos de tuplos. Isso é análogo ao parâmetro de saída `xs_recheck`. Nota: na implementação atual, o suporte para essa funcionalidade é confundido com o suporte para o armazenamento não-perda da própria bitmap, e, portanto, os chamados reverificam tanto as condições de varredura quanto o predicado de índice parcial (se houver) para tuplos recheckáveis. No entanto, isso nem sempre é verdade. `amgetbitmap` e `amgettuple` não podem ser usados na mesma varredura de índice; há outras restrições também ao usar `amgetbitmap`, conforme explicado em [Seção 63.3][(index-scanning.md "63.3. Index Scanning")].

A função `amgetbitmap` só precisa ser fornecida se o método de acesso suportar varreduras de índice de "bitmap". Se não for esse o caso, o campo `amgetbitmap` em sua estrutura `IndexAmRoutine` deve ser definido como NULL.

```
void
amendscan (IndexScanDesc scan);
```

Finalize uma varredura e libere recursos. A própria estrutura `scan` não deve ser liberada, mas quaisquer bloqueios ou pinos tomados internamente pelo método de acesso devem ser liberados, assim como qualquer outra memória alocada por `ambeginscan` e outras funções relacionadas à varredura.

```
void
ammarkpos (IndexScanDesc scan);
```

Marcar a posição atual do varrimento. O método de acesso só precisa suportar uma posição de varrimento lembrada por varrimento.

A função `ammarkpos` só precisa ser fornecida se o método de acesso suportar varreduras ordenadas. Se não for esse o caso, o campo `ammarkpos` em sua estrutura `IndexAmRoutine` pode ser definido como NULL.

```
void
amrestrpos (IndexScanDesc scan);
```

Restaure a varredura na posição mais recentemente marcada.

A função `amrestrpos` só precisa ser fornecida se o método de acesso suportar varreduras ordenadas. Se não for esse o caso, o campo `amrestrpos` em sua estrutura `IndexAmRoutine` pode ser definido como NULL.

Além de suportar varreduras de índice comuns, alguns tipos de índice podem querer suportar *varreduras de índice paralelas*, que permitem que vários backends cooperem na realização de uma varredura de índice. O método de acesso ao índice deve organizar as coisas de tal forma que cada processo cooperante retorne um subconjunto dos tuplos que seriam realizados por uma varredura de índice comum, não paralela, mas de tal forma que a união desses subconjuntos seja igual ao conjunto de tuplos que seriam retornados por uma varredura de índice comum, não paralela. Além disso, embora não seja necessário haver qualquer ordem global dos tuplos retornados por uma varredura paralela, a ordem desse subconjunto de tuplos retornados dentro de cada backend cooperante deve corresponder à ordem solicitada. As seguintes funções podem ser implementadas para suportar varreduras de índice paralelas:

```
Size
amestimateparallelscan (Relation indexRelation,
                        int nkeys,
                        int norderbys);
```

Estime e retorne o número de bytes de memória compartilhada dinâmica que o método de acesso precisará para realizar uma varredura paralela. (Este número é adicional, e não substitui, à quantidade de espaço necessário para dados independentes do AM em `ParallelIndexScanDescData`).

Os parâmetros `nkeys` e `norderbys` indicam o número de quals e operadores de ordenação que serão utilizados na varredura; os mesmos valores serão passados para `amrescan`. Observe que os valores reais das chaves de varredura ainda não são fornecidos.

Não é necessário implementar essa função para métodos de acesso que não suportam varreduras paralelas ou para os quais o número de bytes adicionais de armazenamento necessários é zero.

```
void
aminitparallelscan (void *target);
```

Essa função será chamada para inicializar a memória compartilhada dinâmica no início de uma varredura paralela. *`target`* apontará para pelo menos o número de bytes previamente retornados por `amestimateparallelscan`, e essa função pode usar esse espaço para armazenar qualquer dado que desejar.

Não é necessário implementar essa função para métodos de acesso que não suportam varreduras paralelas ou em casos em que o espaço de memória compartilhada necessário não precisa de inicialização.

```
void
amparallelrescan (IndexScanDesc scan);
```

Essa função, se implementada, será chamada quando um varredura de índice paralelo precisar ser recomeçada. Ela deve redefinir qualquer estado compartilhado configurado por `aminitparallelscan` de modo que a varredura seja recomeçada do início.

```
CompareType
amtranslatestrategy (StrategyNumber strategy, Oid opfamily, Oid opcintype);

StrategyNumber
amtranslatecmptype (CompareType cmptype, Oid opfamily, Oid opcintype);
```

Essas funções, se implementadas, serão chamadas pelo planejador e executor para converter entre os valores fixos do `CompareType` e os números específicos da estratégia utilizados pelo método de acesso. Essas funções podem ser implementadas por métodos de acesso que implementem funcionalidades semelhantes aos métodos de acesso internos btree ou hash, e, ao implementar essas traduções, o sistema pode aprender a semântica das operações do método de acesso e pode usá-las em vez de índices btree ou hash em vários lugares. Se a funcionalidade do método de acesso não for semelhante àqueles métodos de acesso internos, essas funções não precisam ser implementadas. Se as funções não forem implementadas, o método de acesso será ignorado para certas decisões do planejador e executor, mas, de outra forma, é totalmente funcional.