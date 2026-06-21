## Capítulo 41. PL/pgSQL — Linguagem Procedimental SQL

**Índice**

* [41.1. Visão geral](plpgsql-overview.md)

+ [41.1.1. Vantagens de usar PL/pgSQL](plpgsql-overview.md#PLPGSQL-ADVANTAGES)
+ [41.1.2. Tipos de dados de argumentos e resultados suportados](plpgsql-overview.md#PLPGSQL-ARGS-RESULTS)

* [41.2. Estrutura do PL/pgSQL](plpgsql-structure.md)
* [41.3. Declarações](plpgsql-declarations.md)

+ [41.3.1. Declaração de Parâmetros de Função](plpgsql-declarations.md#PLPGSQL-DECLARATION-PARAMETERS)
+ [41.3.2. `ALIAS`](plpgsql-declarations.md#PLPGSQL-DECLARATION-ALIAS)
+ [41.3.3. Copiar Tipos](plpgsql-declarations.md#PLPGSQL-DECLARATION-TYPE)
+ [41.3.4. Tipos de Linha](plpgsql-declarations.md#PLPGSQL-DECLARATION-ROWTYPES)
+ [41.3.5. Tipos de Registro](plpgsql-declarations.md#PLPGSQL-DECLARATION-RECORDS)
+ [41.3.6. Colaboração de Variáveis PL/pgSQL](plpgsql-declarations.md#PLPGSQL-DECLARATION-COLLATION)

* [41.4. Expressões](plpgsql-expressions.md)
* [41.5. Declarações Básicas](plpgsql-statements.md)

+ [41.5.1. Atribuição][(plpgsql-statements.md#PLPGSQL-STATEMENTS-ASSIGNMENT)]
+ [41.5.2. Executar comandos SQL][(plpgsql-statements.md#PLPGSQL-STATEMENTS-GENERAL-SQL)]
+ [41.5.3. Executar um comando com um resultado de uma única linha][(plpgsql-statements.md#PLPGSQL-STATEMENTS-SQL-ONEROW)]
+ [41.5.4. Executar comandos dinâmicos][(plpgsql-statements.md#PLPGSQL-STATEMENTS-EXECUTING-DYN)]
+ [41.5.5. Obter o status do resultado][(plpgsql-statements.md#PLPGSQL-STATEMENTS-DIAGNOSTICS)]
+ [41.5.6. Não fazer nada][(plpgsql-statements.md#PLPGSQL-STATEMENTS-NULL)]

* [41.6. Estruturas de controle](plpgsql-control-structures.md)

+ [41.6.1. Retorno de uma função](plpgsql-control-structures.md#PLPGSQL-STATEMENTS-RETURNING)
+ [41.6.2. Retorno de um procedimento](plpgsql-control-structures.md#PLPGSQL-STATEMENTS-RETURNING-PROCEDURE)
+ [41.6.3. Chamada de um procedimento](plpgsql-control-structures.md#PLPGSQL-STATEMENTS-CALLING-PROCEDURE)
+ [41.6.4. Condicionais](plpgsql-control-structures.md#PLPGSQL-CONDITIONALS)
+ [41.6.5. Loops simples](plpgsql-control-structures.md#PLPGSQL-CONTROL-STRUCTURES-LOOPS)
+ [41.6.6. Iteração por resultados de consulta](plpgsql-control-structures.md#PLPGSQL-RECORDS-ITERATING)
+ [41.6.7. Iteração por arrays](plpgsql-control-structures.md#PLPGSQL-FOREACH-ARRAY)
+ [41.6.8. Captura de erros](plpgsql-control-structures.md#PLPGSQL-ERROR-TRAPPING)
+ [41.6.9. Obtenção de informações sobre a localização de execução](plpgsql-control-structures.md#PLPGSQL-CALL-STACK)

* [41.7. Cursor][(plpgsql-cursors.md)]

+ [41.7.1. Declarando variáveis de cursor][(plpgsql-cursors.md#PLPGSQL-CURSOR-DECLARATIONS)]
+ [41.7.2. Abrir cursors][(plpgsql-cursors.md#PLPGSQL-CURSOR-OPENING)]
+ [41.7.3. Usando cursors][(plpgsql-cursors.md#PLPGSQL-CURSOR-USING)]
+ [41.7.4. Percorrendo o resultado de um cursor][(plpgsql-cursors.md#PLPGSQL-CURSOR-FOR-LOOP)]

* [41.8. Gerenciamento de Transações](plpgsql-transactions.md)
* [41.9. Erros e Mensagens](plpgsql-errors-and-messages.md)

+ [41.9.1. Relatando Erros e Mensagens](plpgsql-errors-and-messages.md#PLPGSQL-STATEMENTS-RAISE)
+ [41.9.2. Verificando Afirmações](plpgsql-errors-and-messages.md#PLPGSQL-STATEMENTS-ASSERT)

* [41.10. Funções de gatilho][(plpgsql-trigger.md)]

+ [41.10.1. Descodificadores em Mudanças de Dados](plpgsql-trigger.md#PLPGSQL-DML-TRIGGER)
+ [41.10.2. Descodificadores em Eventos](plpgsql-trigger.md#PLPGSQL-EVENT-TRIGGER)

* [41.11. PL/pgSQL sob o manto][(plpgsql-implementation.md)]

+ [41.11.1. Substituição de variáveis](plpgsql-implementation.md#PLPGSQL-VAR-SUBST)
+ [41.11.2. Caching de plano](plpgsql-implementation.md#PLPGSQL-PLAN-CACHING)

* [41.12. Dicas para o desenvolvimento em PL/pgSQL][(plpgsql-development-tips.md)]

+ [41.12.1. Tratamento de aspas](plpgsql-development-tips.md#PLPGSQL-QUOTE-TIPS)
+ [41.12.2. Verificações adicionais de tempo de compilação e tempo de execução](plpgsql-development-tips.md#PLPGSQL-EXTRA-CHECKS)

* [41.13. Portando de Oracle PL/SQL](plpgsql-porting.md)

+ [41.13.1. Exemplos de Portando][(plpgsql-porting.md#PLPGSQL-PORTING-EXAMPLES)
+ [41.13.2. Outras Coisas a Observar][(plpgsql-porting.md#PLPGSQL-PORTING-OTHER)
+ [41.13.3. Apêndice][(plpgsql-porting.md#PLPGSQL-PORTING-APPENDIX)