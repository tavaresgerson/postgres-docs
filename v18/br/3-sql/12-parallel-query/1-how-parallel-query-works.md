## 15.1. Como funciona a consulta paralela [#](#HOW-PARALLEL-QUERY-WORKS)

Quando o otimizador determina que a consulta paralela é a estratégia de execução mais rápida para uma consulta específica, ele criará um plano de consulta que inclui um nó *Gather* ou *Gather Merge*. Aqui está um exemplo simples:

```
EXPLAIN SELECT * FROM pgbench_accounts WHERE filler LIKE '%x%';
                                     QUERY PLAN
-------------------------------------------------------------------​------------------
 Gather  (cost=1000.00..217018.43 rows=1 width=97)
   Workers Planned: 2
   ->  Parallel Seq Scan on pgbench_accounts  (cost=0.00..216018.33 rows=1 width=97)
         Filter: (filler ~~ '%x%'::text)
(4 rows)
```

Em todos os casos, o nó `Gather` ou `Gather Merge` terá exatamente um plano filho, que é a parte do plano que será executada em paralelo. Se o nó `Gather` ou `Gather Merge` estiver no topo da árvore do plano, então toda a consulta será executada em paralelo. Se estiver em algum outro lugar na árvore do plano, então apenas a parte do plano abaixo dele será executada em paralelo. No exemplo acima, a consulta acessa apenas uma tabela, então há apenas um nó de plano, exceto o próprio nó `Gather`; como esse nó de plano é filho do nó `Gather`, ele será executado em paralelo.

[Usando EXPLAIN](using-explain.md), você pode ver o número de trabalhadores escolhidos pelo planejador. Quando o nó `Gather` é alcançado durante a execução da consulta, o processo que está implementando a sessão do usuário solicitará um número de [processos de trabalhador de fundo](bgworker.md) igual ao número de trabalhadores escolhidos pelo planejador. O número de trabalhadores de fundo que o planejador considerará usar é limitado a, no máximo, [max_parallel_workers_per_gather](runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS-PER-GATHER). O número total de trabalhadores de fundo que podem existir em qualquer momento é limitado tanto por [max_worker_processes](runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES) quanto por [max_parallel_workers](runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS). Portanto, é possível que uma consulta paralela seja executada com menos trabalhadores do que o planejado, ou até mesmo sem nenhum trabalhador. O plano ótimo pode depender do número de trabalhadores disponíveis, portanto, isso pode resultar em um desempenho ruim da consulta. Se essa ocorrência for frequente, considere aumentar `max_worker_processes` e `max_parallel_workers` para que mais trabalhadores possam ser executados simultaneamente ou, alternativamente, reduzir `max_parallel_workers_per_gather` para que o planejador solicite menos trabalhadores.

Todo processo de trabalhador de fundo que é iniciado com sucesso para uma consulta paralela dada executará a parte paralela do plano. O líder também executará essa parte do plano, mas tem uma responsabilidade adicional: ele também deve ler todos os tuplos gerados pelos trabalhadores. Quando a parte paralela do plano gera apenas um pequeno número de tuplos, o líder muitas vezes se comporta muito como um trabalhador adicional, acelerando a execução da consulta. Por outro lado, quando a parte paralela do plano gera um grande número de tuplos, o líder pode estar quase inteiramente ocupado lendo os tuplos gerados pelos trabalhadores e realizando quaisquer etapas de processamento adicionais que são necessárias pelos nós do plano acima do nível do nó `Gather` ou do nó `Gather Merge`. Nesses casos, o líder fará muito pouco do trabalho de execução da parte paralela do plano.

Quando o nó no topo da parte paralela do plano é `Gather Merge` em vez de `Gather`, isso indica que cada processo que executa a parte paralela do plano está produzindo tuplas em ordem ordenada e que o líder está realizando uma fusão que preserva a ordem. Em contraste, `Gather` lê tuplas dos trabalhadores na ordem que for conveniente, destruindo qualquer ordem de classificação que possa ter existido.