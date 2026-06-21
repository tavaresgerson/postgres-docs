## Capítulo 39. O Sistema de Regras

**Índice**

* [39.1. Árvores de Consulta](querytree.md)
* [39.2. Visualizações e o Sistema de Regras](rules-views.md)

+ [39.2.1. Como funcionam as regras do `SELECT`](rules-views.md#RULES-SELECT)
+ [39.2.2. Visualizar regras em declarações não do `SELECT`](rules-views.md#RULES-VIEWS-NON-SELECT)
+ [39.2.3. O poder das visualizações no PostgreSQL](rules-views.md#RULES-VIEWS-POWER)
+ [39.2.4. Atualizando uma visualização](rules-views.md#RULES-VIEWS-UPDATE)

* [39.3. Visões Materializadas](rules-materializedviews.md)
* [39.4. Regras sobre `INSERT`, `UPDATE` e `DELETE`](rules-update.md)

+ [39.4.1. Como funcionam as regras de atualização][(rules-update.md#RULES-UPDATE-HOW)]
+ [39.4.2. Cooperação com visualizações][(rules-update.md#RULES-UPDATE-VIEWS)]

* [39.5. Regras e Privilegios](rules-privileges.md)
* [39.6. Regras e Status de Comando](rules-status.md)
* [39.7. Regras versus Triggers](rules-triggers.md)

Este capítulo discute o sistema de regras no PostgreSQL. Os sistemas de regras de produção são conceitualmente simples, mas há muitos pontos sutis envolvidos na utilização deles.

Alguns outros sistemas de banco de dados definem regras de banco de dados ativas, que geralmente são procedimentos armazenados e gatilhos. No PostgreSQL, esses podem ser implementados usando funções e gatilhos também.

O sistema de regras (mais precisamente, o sistema de regras de reescrita de consultas) é totalmente diferente de procedimentos armazenados e gatilhos. Ele modifica as consultas para levar em consideração as regras, e então passa a consulta modificada para o planejador de consultas para planejamento e execução. É muito poderoso e pode ser usado para muitas coisas, como procedimentos de linguagem de consulta, visualizações e versões. As bases teóricas e o poder desse sistema de regras também são discutidos em [[ston90b]](biblio.md#STON90B) e [[ong90]](biblio.md#ONG90).