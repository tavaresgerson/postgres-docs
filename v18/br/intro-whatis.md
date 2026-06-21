## 1. O que é PostgreSQL? [#](#INTRO-WHATIS)

O PostgreSQL é um sistema de gerenciamento de banco de dados orientado a objetos (ORDBMS) baseado em [POSTGRES, Versão 4.2][(https://dsf.berkeley.edu/postgres.html)], desenvolvido pelo Departamento de Ciência da Computação da Universidade da Califórnia em Berkeley. O PostgreSQL foi pioneiro em muitos conceitos que só se tornaram disponíveis em alguns sistemas de banco de dados comerciais muito mais tarde.

O PostgreSQL é um descendente de código original de Berkeley de código aberto. Ele suporta uma grande parte do padrão SQL e oferece muitas funcionalidades modernas:

* consultas complexas (sql.md "Part II. The SQL Language")
* chaves estrangeiras (ddl-constraints.md#DDL-CONSTRAINTS-FK "5.5.5. Foreign Keys")
* gatilhos (triggers.md "Chapter 37. Triggers")
* visualizações atualizáveis (sql-createview.md#SQL-CREATEVIEW-UPDATABLE-VIEWS "Updatable Views")
* integridade transacional (transaction-iso.md "13.2. Transaction Isolation")
* controle de concorrência multiversão (mvcc.md "Chapter 13. Concurrency Control")

Além disso, o PostgreSQL pode ser ampliado pelo usuário de várias maneiras, por exemplo, adicionando novos

* [tipos de dados](datatype.md "Chapter 8. Data Types")
* [funções](functions.md "Chapter 9. Functions and Operators")
* [operadores](functions.md "Chapter 9. Functions and Operators")
* [funções agregadas](functions-aggregate.md "9.21. Aggregate Functions")
* [métodos de índice](indexes.md "Chapter 11. Indexes")
* [linguagens procedimentais](server-programming.md "Part V. Server Programming")

E, devido à licença liberal, o PostgreSQL pode ser usado, modificado e distribuído por qualquer pessoa gratuitamente para qualquer propósito, seja privado, comercial ou acadêmico.