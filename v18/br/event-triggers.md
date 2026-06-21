## Capítulo 38. Gatilhos de evento

**Índice**

* [38.1. Visão geral do comportamento do gatilho de evento](event-trigger-definition.md)

+ [38.1.1. login][(event-trigger-definition.md#EVENT-TRIGGER-LOGIN)]
+ [38.1.2. ddl_command_start][(event-trigger-definition.md#EVENT-TRIGGER-DDL_COMMAND_START)]
+ [38.1.3. ddl_command_end][(event-trigger-definition.md#EVENT-TRIGGER-DDL_COMMAND_END)]
+ [38.1.4. sql_drop][(event-trigger-definition.md#EVENT-TRIGGER-SQL_DROP)]
+ [38.1.5. table_rewrite][(event-trigger-definition.md#EVENT-TRIGGER-TABLE_REWRITE)]
+ [38.1.6. Triggers de Evento em Transações Abortadas][(event-trigger-definition.md#EVENT-TRIGGER-ABORTED-TRANSACTIONS)]
+ [38.1.7. Criando Triggers de Evento][(event-trigger-definition.md#EVENT-TRIGGER-CREATING)]

* [38.2. Funções de disparo de eventos de escrita em C][(event-trigger-interface.md)]
* [38.3. Um exemplo completo de disparo de eventos de escrita][(event-trigger-example.md)]
* [38.4. Um exemplo de disparo de eventos de reescrita de tabela][(event-trigger-table-rewrite-example.md)]
* [38.5. Um exemplo de disparo de eventos de login de banco de dados][(event-trigger-database-login-example.md)]

Para complementar o mecanismo de disparo discutido no [Capítulo 37][(triggers.md "Chapter 37. Triggers")], o PostgreSQL também oferece gatilhos de evento. Ao contrário dos gatilhos regulares, que são anexados a uma única tabela e capturam apenas eventos de DML, os gatilhos de evento são globais para um banco de dados específico e são capazes de capturar eventos de DDL.

Assim como os gatilhos regulares, os gatilhos de evento podem ser escritos em qualquer linguagem procedural que inclua suporte para gatilho de evento, ou em C, mas não em SQL simples.