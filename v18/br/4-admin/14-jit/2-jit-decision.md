## 30.2. Quando usar JIT? [#](#JIT-DECISION)

A compilação JIT é benéfica principalmente para consultas que dependem da CPU por um longo período. Frequentemente, essas serão consultas analíticas. Para consultas curtas, o custo adicional de realizar a compilação JIT geralmente será maior do que o tempo que pode ser economizado.

Para determinar se a compilação JIT deve ser usada, o custo total estimado de uma consulta (ver [Capítulo 69](planner-stats-details.md) e [Seção 19.7.2](runtime-config-query.md#RUNTIME-CONFIG-QUERY-CONSTANTS)) é utilizado. O custo estimado da consulta é comparado com o valor de [jit_above_cost](runtime-config-query.md#GUC-JIT-ABOVE-COST). Se o custo for maior, a compilação JIT será realizada. Em seguida, são necessárias duas decisões adicionais. Primeiramente, se o custo estimado for maior que o valor de [jit_inline_above_cost](runtime-config-query.md#GUC-JIT-INLINE-ABOVE-COST), as funções e operadores curtas usados na consulta serão inlinhados. Em segundo lugar, se o custo estimado for maior que o valor de [jit_optimize_above_cost](runtime-config-query.md#GUC-JIT-OPTIMIZE-ABOVE-COST), otimizações caras são aplicadas para melhorar o código gerado. Cada uma dessas opções aumenta o custo da compilação JIT, mas pode reduzir consideravelmente o tempo de execução da consulta.

Essas decisões baseadas nos custos serão tomadas no momento do planejamento, e não no momento da execução. Isso significa que, quando as declarações preparadas estão em uso e um plano genérico é usado (consulte [PREPARE](sql-prepare.md)), os valores dos parâmetros de configuração em vigor no momento da preparação controlam as decisões, e não os ajustes no momento da execução.

Nota

Se [jit][(runtime-config-query.md#GUC-JIT) estiver definido como `off`, ou se nenhuma implementação JIT estiver disponível (por exemplo, porque o servidor foi compilado sem `--with-llvm`, o JIT não será executado, mesmo que isso seja benéfico com base nos critérios acima. Definir [jit][(runtime-config-query.md#GUC-JIT) como `off` tem efeitos tanto no tempo de planejamento quanto na execução.

[EXPLAIN](sql-explain.md "EXPLAIN") pode ser usado para verificar se o JIT é usado ou não. Como exemplo, aqui está uma consulta que não está usando JIT:

```
=# EXPLAIN ANALYZE SELECT SUM(relpages) FROM pg_class;
                                                 QUERY PLAN
-------------------------------------------------------------------​------------------------------------------
 Aggregate  (cost=16.27..16.29 rows=1 width=8) (actual time=0.303..0.303 rows=1.00 loops=1)
   Buffers: shared hit=14
   ->  Seq Scan on pg_class  (cost=0.00..15.42 rows=342 width=4) (actual time=0.017..0.111 rows=356.00 loops=1)
         Buffers: shared hit=14
 Planning Time: 0.116 ms
 Execution Time: 0.365 ms
```

Dada o custo do plano, é totalmente razoável que não tenha sido usado o JIT; o custo do JIT teria sido maior do que as possíveis economias. Ajustar os limites de custo levará ao uso do JIT:

```
=# SET jit_above_cost = 10;
SET
=# EXPLAIN ANALYZE SELECT SUM(relpages) FROM pg_class;
                                                 QUERY PLAN
-------------------------------------------------------------------​------------------------------------------
 Aggregate  (cost=16.27..16.29 rows=1 width=8) (actual time=6.049..6.049 rows=1.00 loops=1)
   Buffers: shared hit=14
   ->  Seq Scan on pg_class  (cost=0.00..15.42 rows=342 width=4) (actual time=0.019..0.052 rows=356.00 loops=1)
         Buffers: shared hit=14
 Planning Time: 0.133 ms
 JIT:
   Functions: 3
   Options: Inlining false, Optimization false, Expressions true, Deforming true
   Timing: Generation 1.259 ms (Deform 0.000 ms), Inlining 0.000 ms, Optimization 0.797 ms, Emission 5.048 ms, Total 7.104 ms
 Execution Time: 7.416 ms
```

Como é visível aqui, o JIT foi usado, mas o inline e a otimização cara não foram. Se [jit_inline_above_cost](runtime-config-query.md#GUC-JIT-INLINE-ABOVE-COST) ou [jit_optimize_above_cost](runtime-config-query.md#GUC-JIT-OPTIMIZE-ABOVE-COST) também fossem reduzidos, isso mudaria.