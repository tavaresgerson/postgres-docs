## 63.1. Estrutura básica da API para índices [#](#INDEX-API)

Cada método de acesso ao índice é descrito por uma linha no catálogo do sistema `pg_am`(catalog-pg-am.md "52.3. pg_am"). A entrada `pg_am` especifica um nome e uma *função de manipulador* para o método de acesso ao índice. Essas entradas podem ser criadas e excluídas usando os comandos SQL [CREATE ACCESS METHOD](sql-create-access-method.md "CREATE ACCESS METHOD") e [DROP ACCESS METHOD](sql-drop-access-method.md "DROP ACCESS METHOD").

Uma função de manipulador de método de acesso a índice deve ser declarada para aceitar um único argumento do tipo `internal` e retornar o pseudo-tipo `index_am_handler`. O argumento é um valor fictício que simplesmente serve para impedir que as funções de manipulador sejam chamadas diretamente a partir de comandos SQL. O resultado da função deve ser uma estrutura palloc'ada do tipo `IndexAmRoutine`, que contém tudo o que o código principal precisa saber para fazer uso do método de acesso a índice. A estrutura `IndexAmRoutine`, também chamada de estrutura *API* do método de acesso, inclui campos que especificam propriedades fixas variadas do método de acesso, como se ele possa suportar índices de múltiplos colunas. Mais importante, ela contém ponteiros para suportar funções do método de acesso, que fazem todo o trabalho real para acessar índices. Essas funções de suporte são funções simples em C e não são visíveis ou chamadas no nível SQL. As funções de suporte são descritas em [Seção 63.2](index-functions.md).

A estrutura `IndexAmRoutine` é definida da seguinte forma:

```
typedef struct IndexAmRoutine
{
    NodeTag     type;

    /*
     * Total number of strategies (operators) by which we can traverse/search
     * this AM.  Zero if AM does not have a fixed set of strategy assignments.
     */
    uint16      amstrategies;
    /* total number of support functions that this AM uses */
    uint16      amsupport;
    /* opclass options support function number or 0 */
    uint16      amoptsprocnum;
    /* does AM support ORDER BY indexed column's value? */
    bool        amcanorder;
    /* does AM support ORDER BY result of an operator on indexed column? */
    bool        amcanorderbyop;
    /* does AM support hashing using API consistent with the hash AM? */
    bool        amcanhash;
    /* do operators within an opfamily have consistent equality semantics? */
    bool        amconsistentequality;
    /* do operators within an opfamily have consistent ordering semantics? */
    bool        amconsistentordering;
    /* does AM support backward scanning? */
    bool        amcanbackward;
    /* does AM support UNIQUE indexes? */
    bool        amcanunique;
    /* does AM support multi-column indexes? */
    bool        amcanmulticol;
    /* does AM require scans to have a constraint on the first index column? */
    bool        amoptionalkey;
    /* does AM handle ScalarArrayOpExpr quals? */
    bool        amsearcharray;
    /* does AM handle IS NULL/IS NOT NULL quals? */
    bool        amsearchnulls;
    /* can index storage data type differ from column data type? */
    bool        amstorage;
    /* can an index of this type be clustered on? */
    bool        amclusterable;
    /* does AM handle predicate locks? */
    bool        ampredlocks;
    /* does AM support parallel scan? */
    bool        amcanparallel;
    /* does AM support parallel build? */
    bool        amcanbuildparallel;
    /* does AM support columns included with clause INCLUDE? */
    bool        amcaninclude;
    /* does AM use maintenance_work_mem? */
    bool        amusemaintenanceworkmem;
    /* does AM summarize tuples, with at least all tuples in the block
     * summarized in one summary */
    bool        amsummarizing;
    /* OR of parallel vacuum flags */
    uint8       amparallelvacuumoptions;
    /* type of data stored in index, or InvalidOid if variable */
    Oid         amkeytype;

    /* interface functions */
    ambuild_function ambuild;
    ambuildempty_function ambuildempty;
    aminsert_function aminsert;
    aminsertcleanup_function aminsertcleanup;   /* can be NULL */
    ambulkdelete_function ambulkdelete;
    amvacuumcleanup_function amvacuumcleanup;
    amcanreturn_function amcanreturn;   /* can be NULL */
    amcostestimate_function amcostestimate;
    amgettreeheight_function amgettreeheight;   /* can be NULL */
    amoptions_function amoptions;
    amproperty_function amproperty;     /* can be NULL */
    ambuildphasename_function ambuildphasename;   /* can be NULL */
    amvalidate_function amvalidate;
    amadjustmembers_function amadjustmembers; /* can be NULL */
    ambeginscan_function ambeginscan;
    amrescan_function amrescan;
    amgettuple_function amgettuple;     /* can be NULL */
    amgetbitmap_function amgetbitmap;   /* can be NULL */
    amendscan_function amendscan;
    ammarkpos_function ammarkpos;       /* can be NULL */
    amrestrpos_function amrestrpos;     /* can be NULL */

    /* interface functions to support parallel index scans */
    amestimateparallelscan_function amestimateparallelscan;    /* can be NULL */
    aminitparallelscan_function aminitparallelscan;    /* can be NULL */
    amparallelrescan_function amparallelrescan;    /* can be NULL */

    /* interface functions to support planning */
    amtranslate_strategy_function amtranslatestrategy;  /* can be NULL */
    amtranslate_cmptype_function amtranslatecmptype;    /* can be NULL */
} IndexAmRoutine;
```

Para ser útil, um método de acesso a índice também deve ter uma ou mais *famílias de operadores* e *classes de operadores* definidas em `pg_opfamily`(catalog-pg-opfamily.md "52.35. pg_opfamily"), [`pg_opclass`](catalog-pg-opclass.md "52.33. pg_opclass"), [`pg_amop`](catalog-pg-amop.md "52.4. pg_amop"), e [`pg_amproc`](catalog-pg-amproc.md). Essas entradas permitem que o planejador determine quais tipos de qualificações de consulta podem ser usadas com índices deste método de acesso. Famílias e classes de operadores são descritas em [Seção 36.16](xindex.md "36.16. Interfacing Extensions to Indexes"), que é material prévio para a leitura deste capítulo.

Um índice individual é definido por uma entrada `pg_class` (catalog-pg-class.md "52.11. pg_class") que o descreve como uma relação física, além de uma entrada `pg_index` (catalog-pg-index.md "52.26. pg_index") que mostra o conteúdo lógico do índice — ou seja, o conjunto de colunas do índice que possui e a semântica dessas colunas, conforme capturado pelas classes de operadores associadas. As colunas do índice (valores de chave) podem ser colunas simples da tabela subjacente ou expressões sobre as linhas da tabela. O método de acesso ao índice normalmente não tem interesse em onde os valores das chaves do índice vêm (sempre são entregues valores de chave pré-computados), mas estará muito interessado nas informações da classe de operadores em `pg_index`. Ambas essas entradas de catálogo podem ser acessadas como parte da estrutura de dados `Relation` que é passada para todas as operações no índice.

Alguns dos campos de bandeira de `IndexAmRoutine` têm implicações não óbvias. Os requisitos de `amcanunique` são discutidos em [Seção 63.5](index-unique-checks.md). O campo de bandeira `amcanmulticol` afirma que o método de acesso suporta índices de coluna com múltiplos chaves, enquanto `amoptionalkey` afirma que permite varreduras onde não é dada nenhuma cláusula de restrição indexável para a primeira coluna de índice. Quando `amcanmulticol` é falso, `amoptionalkey` essencialmente diz se o método de acesso suporta varreduras completos sem nenhuma cláusula de restrição. Métodos de acesso que suportam múltiplas colunas de índice *devem* suportar varreduras que omitem restrições em qualquer ou todas as colunas após a primeira; no entanto, eles são permitidos para exigir que alguma restrição apareça para a primeira coluna de índice, e isso é sinalizado definindo `amoptionalkey` como falso. Uma razão pela qual um AM de índice pode definir `amoptionalkey` falso é se ele não indexar valores nulos. Como a maioria dos operadores indexáveis é estrita e, portanto, não pode retornar verdadeiro para entradas nulos, é, à primeira vista, atraente não armazenar entradas de índice para valores nulos: eles nunca poderiam ser retornados por uma varredura de índice de qualquer maneira. No entanto, esse argumento falha quando uma varredura de índice não tem cláusula de restrição para uma coluna de índice dada. Na prática, isso significa que índices que têm `amoptionalkey` verdadeiro devem indexar nulos, pois o planejador pode decidir usar tal índice sem nenhuma chave de varredura. Uma restrição relacionada é que um método de acesso de índice que suporta múltiplos colunas de índice *deve* suportar indexação de valores nulos em colunas após a primeira, porque o planejador assumirá que o índice pode ser usado para consultas que não restringem essas colunas. Por exemplo, considere um índice em (a,b) e uma consulta com `WHERE a = 4`. O sistema assumirá que o índice pode ser usado para varredura de linhas com `a = 4`, o que está errado se o índice omite linhas onde `b` é nulo. No entanto, está tudo bem omitir linhas onde a primeira coluna indexada é nulo. Um método de acesso de índice que indexa nulos também pode definir `amsearchnulls`, indicando que ele suporta cláusulas `IS NULL` e `IS NOT NULL` como condições de pesquisa.

A bandeira `amcaninclude` indica se o método de acesso suporta colunas "incluídas", ou seja, pode armazenar (sem processamento) colunas adicionais além das colunas chave(s). Os requisitos do parágrafo anterior se aplicam apenas às colunas chave. Em particular, a combinação `amcanmulticol`=`false` e `amcaninclude`=`true` é sensível: isso significa que pode haver apenas uma coluna chave, mas também pode haver colunas incluídas. Além disso, as colunas incluídas devem ser permitidas como nulos, independentemente de `amoptionalkey`.

A bandeira `amsummarizing` indica se o método de acesso resume os tuplos indexados, com granularidade de resumo de pelo menos por bloco. Os métodos de acesso que não apontam para tuplos individuais, mas para faixas de blocos (como BRIN), podem permitir que a otimização HOT continue. Isso não se aplica aos atributos referenciados em predicados de índice, uma atualização de tal atributo sempre desativa o HOT.