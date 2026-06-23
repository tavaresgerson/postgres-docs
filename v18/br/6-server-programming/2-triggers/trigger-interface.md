## 37.3. Escrever funções de disparo em C [#](#TRIGGER-INTERFACE)

Esta seção descreve os detalhes de baixo nível da interface para uma função de gatilho. Essas informações são necessárias apenas ao escrever funções de gatilho em C. Se você estiver usando uma linguagem de nível mais alto, essas informações são tratadas automaticamente. Na maioria dos casos, você deve considerar o uso de uma linguagem procedural antes de escrever seus gatilhos em C. A documentação de cada linguagem procedural explica como escrever um gatilho nessa linguagem.

As funções de disparo devem usar a interface do gerenciador de funções da “versão 1”.

Quando uma função é chamada pelo gerenciador de gatilho, não são passados argumentos normais, mas sim um ponteiro de "context" que aponta para uma estrutura `TriggerData`. As funções C podem verificar se foram chamadas pelo gerenciador de gatilho ou não, executando o macro:

```
CALLED_AS_TRIGGER(fcinfo)
```

que se expande para:

```
((fcinfo)->context != NULL && IsA((fcinfo)->context, TriggerData))
```

Se isso for verdade, então é seguro converter `fcinfo->context` para o tipo `TriggerData *` e utilizar a estrutura apontada por `TriggerData`. A função *não* deve alterar a estrutura `TriggerData` ou qualquer um dos dados a que ela aponta.

`struct TriggerData` é definido em `commands/trigger.h`:

```
typedef struct TriggerData
{
    NodeTag          type;
    TriggerEvent     tg_event;
    Relation         tg_relation;
    HeapTuple        tg_trigtuple;
    HeapTuple        tg_newtuple;
    Trigger         *tg_trigger;
    TupleTableSlot  *tg_trigslot;
    TupleTableSlot  *tg_newslot;
    Tuplestorestate *tg_oldtable;
    Tuplestorestate *tg_newtable;
    const Bitmapset *tg_updatedcols;
} TriggerData;
```

onde os membros são definidos da seguinte forma:

`type`: Sempre `T_TriggerData`.

`tg_event`: Descreve o evento para o qual a função é chamada. Você pode usar as seguintes macros para examinar `tg_event`:

`TRIGGER_FIRED_BEFORE(tg_event)` : Retorna verdadeiro se o gatilho foi disparado antes da operação.

`TRIGGER_FIRED_AFTER(tg_event)` : Retorna verdadeiro se o gatilho foi disparado após a operação.

`TRIGGER_FIRED_INSTEAD(tg_event)` : Retorna verdadeiro se o gatilho foi disparado em vez da operação.

`TRIGGER_FIRED_FOR_ROW(tg_event)` : Retorna verdadeiro se o gatilho foi disparado para um evento em nível de linha.

`TRIGGER_FIRED_FOR_STATEMENT(tg_event)` : Retorna verdadeiro se o gatilho foi disparado para um evento de nível de declaração.

`TRIGGER_FIRED_BY_INSERT(tg_event)` : Retorna verdadeiro se o gatilho foi disparado por um comando do `INSERT`.

`TRIGGER_FIRED_BY_UPDATE(tg_event)` : Retorna verdadeiro se o gatilho foi disparado por um comando `UPDATE`.

`TRIGGER_FIRED_BY_DELETE(tg_event)` : Retorna verdadeiro se o gatilho foi disparado por um comando `DELETE`.

`TRIGGER_FIRED_BY_TRUNCATE(tg_event)` : Retorna verdadeiro se o gatilho foi disparado por um comando `TRUNCATE`.

`tg_relation`: Um ponteiro para uma estrutura que descreve a relação que o gatilho disparou. Veja `utils/rel.h` para detalhes sobre essa estrutura. As coisas mais interessantes são `tg_relation->rd_att` (descriptor dos tuplos da relação) e `tg_relation->rd_rel->relname` (nome da relação; o tipo não é `char*`, mas sim `NameData`; use `SPI_getrelname(tg_relation)` para obter um `char*` se você precisar de uma cópia do nome).

`tg_trigtuple`: Um ponteiro para a linha para a qual o gatilho foi disparado. Esta é a linha que está sendo inserida, atualizada ou excluída. Se este gatilho foi disparado para um `INSERT` ou `DELETE`, então isso é o que você deve retornar da função se você não quiser substituir a linha com outra (no caso de `INSERT`) ou pular a operação. Para gatilhos em tabelas externas, os valores das colunas do sistema não são especificados.

`tg_newtuple`: Um ponteiro para a nova versão da linha, se o gatilho foi disparado para um `UPDATE`, e `NULL` se for para um `INSERT` ou um `DELETE`. Isso é o que você deve retornar da função se o evento for um `UPDATE` e você não quiser substituir esta linha por outra diferente ou pular a operação. Para gatilhos em tabelas externas, os valores das colunas do sistema aqui não são especificados.

`tg_trigger`: Um ponteiro para uma estrutura do tipo `Trigger`, definida em `utils/reltrigger.h`:

```
typedef struct Trigger { Oid         tgoid; char       *tgname; Oid         tgfoid; int16       tgtype; char        tgenabled; bool        tgisinternal; bool        tgisclone; Oid         tgconstrrelid; Oid         tgconstrindid; Oid         tgconstraint; bool        tgdeferrable; bool        tginitdeferred; int16       tgnargs; int16       tgnattr; int16      *tgattr; char      **tgargs; char       *tgqual; char       *tgoldtable; char       *tgnewtable; } Trigger;
```

onde `tgname` é o nome do gatilho, `tgnargs` é o número de argumentos em `tgargs`, e `tgargs` é um array de ponteiros para os argumentos especificados na declaração `CREATE TRIGGER`. Os outros membros são apenas para uso interno.

`tg_trigslot`: O espaço contendo `tg_trigtuple`, ou um ponteiro `NULL` se não houver tal tupla.

`tg_newslot`: O espaço contendo `tg_newtuple`, ou um ponteiro `NULL` se não houver tal tupla.

`tg_oldtable`: Um ponteiro para uma estrutura do tipo `Tuplestorestate` contendo zero ou mais linhas no formato especificado por `tg_relation`, ou um ponteiro de `NULL` se não houver relação de transição `OLD TABLE`.

`tg_newtable`: Um ponteiro para uma estrutura do tipo `Tuplestorestate` contendo zero ou mais linhas no formato especificado por `tg_relation`, ou um ponteiro de `NULL` se não houver relação de transição `NEW TABLE`.

`tg_updatedcols`: Para os gatilhos de `UPDATE`, um conjunto de mapas que indica as colunas que foram atualizadas pelo comando de gatilho. As funções de gatilho genérico podem usar isso para otimizar as ações, sem ter que lidar com colunas que não foram alteradas.

Como exemplo, para determinar se uma coluna com o número de atributo `attnum` (1-based) é membro deste conjunto de mapas, chame `bms_is_member(attnum - FirstLowInvalidHeapAttributeNumber, trigdata->tg_updatedcols))`.

Para gatilhos que não sejam os gatilhos `UPDATE`, este será `NULL`.

Para permitir que consultas emitidas através do SPI refiram-se a tabelas de transição, consulte [SPI_register_trigger_data](spi-spi-register-trigger-data.md "SPI_register_trigger_data").

Uma função de gatilho deve retornar um ponteiro `HeapTuple` ou um ponteiro `NULL` (*não* um valor nulo do SQL, ou seja, não configure *`isNull`* como verdadeiro). Tenha cuidado em retornar `tg_trigtuple` ou `tg_newtuple`, conforme apropriado, se você não deseja modificar a linha que está sendo operada.