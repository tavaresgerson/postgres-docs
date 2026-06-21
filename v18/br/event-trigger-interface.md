## 38.2. Escrever funções de disparo de eventos em C [#](#EVENT-TRIGGER-INTERFACE)

Esta seção descreve os detalhes de baixo nível da interface para uma função de gatilho de evento. Essas informações são necessárias apenas ao escrever funções de gatilho de evento em C. Se você estiver usando uma linguagem de nível mais alto, essas informações são tratadas automaticamente. Na maioria dos casos, você deve considerar o uso de uma linguagem procedural antes de escrever seus gatilhos de evento em C. A documentação de cada linguagem procedural explica como escrever um gatilho de evento nessa linguagem.

As funções de ativação de eventos devem usar a interface do gerenciador de funções da “versão 1”.

Quando uma função é chamada pelo gerenciador de gatilho de evento, não são passados argumentos normais, mas sim um ponteiro de "context" que aponta para uma estrutura `EventTriggerData`. As funções C podem verificar se foram chamadas pelo gerenciador de gatilho de evento ou não, executando a macro:

```
CALLED_AS_EVENT_TRIGGER(fcinfo)
```

que se expande para:

```
((fcinfo)->context != NULL && IsA((fcinfo)->context, EventTriggerData))
```

Se isso for verdade, então é seguro converter `fcinfo->context` para o tipo `EventTriggerData *` e utilizar a estrutura apontada por `EventTriggerData`. A função *não* deve alterar a estrutura `EventTriggerData` ou qualquer um dos dados a que ela aponta.

`struct EventTriggerData` é definido em `commands/event_trigger.h`:

```
typedef struct EventTriggerData
{
    NodeTag     type;
    const char *event;      /* event name */
    Node       *parsetree;  /* parse tree */
    CommandTag  tag;        /* command tag */
} EventTriggerData;
```

onde os membros são definidos da seguinte forma:

`type`: Sempre `T_EventTriggerData`.

`event`: Descreve o evento para o qual a função é chamada, um dos `"login"`, `"ddl_command_start"`, `"ddl_command_end"`, `"sql_drop"`, `"table_rewrite"`. Consulte [Seção 38.1](event-trigger-definition.md "38.1. Overview of Event Trigger Behavior") para o significado desses eventos.

`parsetree`: Um ponteiro para o árvore de análise do comando. Verifique o código-fonte do PostgreSQL para obter detalhes. A estrutura da árvore de análise está sujeita a alterações sem aviso prévio.

`tag`: O rótulo de comando associado ao evento para o qual o gatilho do evento é executado, por exemplo, `"CREATE FUNCTION"`.

Uma função de gatilho de evento deve retornar um ponteiro `NULL` (*não* um valor nulo do SQL, ou seja, não defina *`isNull`* como verdadeiro).