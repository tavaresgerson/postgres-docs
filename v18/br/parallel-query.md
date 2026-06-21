## Capítulo 15. Consulta Paralela

**Índice**

* [15.1. Como funciona a consulta paralela](how-parallel-query-works.md)
* [15.2. Quando a consulta paralela pode ser usada?](when-can-parallel-query-be-used.md)
* [15.3. Planos paralelos](parallel-plans.md)

+ [15.3.1. Análises paralelas](parallel-plans.md#PARALLEL-SCANS)
+ [15.3.2. Conjunções paralelas](parallel-plans.md#PARALLEL-JOINS)
+ [15.3.3. Agregação paralela](parallel-plans.md#PARALLEL-AGGREGATION)
+ [15.3.4. Aplicação paralela](parallel-plans.md#PARALLEL-APPEND)
+ [15.3.5. Dicas de plano paralelo](parallel-plans.md#PARALLEL-PLAN-TIPS)

* [15.4. Segurança paralela](parallel-safety.md)

+ [15.4.1. Etiquetagem paralela para funções e agregados](parallel-safety.md#PARALLEL-LABELING)

O PostgreSQL pode elaborar planos de consulta que podem aproveitar múltiplos CPUs para responder a consultas mais rapidamente. Esse recurso é conhecido como consulta paralela. Muitas consultas não podem se beneficiar da consulta paralela, seja devido a limitações da implementação atual ou porque não existe nenhum plano de consulta imaginável que seja mais rápido que o plano de consulta serial. No entanto, para consultas que podem se beneficiar, a aceleração da consulta paralela é frequentemente muito significativa. Muitas consultas podem rodar mais do que o dobro da velocidade quando usando consulta paralela, e algumas consultas podem rodar quatro vezes mais rápido ou até mais. As consultas que tocam uma grande quantidade de dados, mas retornam apenas algumas linhas ao usuário, geralmente se beneficiarão mais. Este capítulo explica alguns detalhes de como a consulta paralela funciona e em quais situações ela pode ser usada para que os usuários que desejam usá-la possam entender o que esperar.