## 15.2. Quando pode ser usada a consulta paralela? [#](#WHEN-CAN-PARALLEL-QUERY-BE-USED)

Existem vários parâmetros que podem fazer com que o planejador de consultas não gere um plano de consulta paralela sob quaisquer circunstâncias. Para que quaisquer planos de consulta paralela sejam gerados, os seguintes parâmetros devem ser configurados conforme indicado.

* [max_parallel_workers_per_gather](runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS-PER-GATHER) deve ser definido com um valor maior que zero. Este é um caso especial do princípio mais geral de que não deve ser usado mais trabalhadores do que o número configurado via `max_parallel_workers_per_gather`.

Além disso, o sistema não deve estar em modo de usuário único. Como todo o sistema de banco de dados está rodando como um único processo nessa situação, nenhum trabalhador de fundo estará disponível.

Mesmo quando é possível, em geral, gerar planos de consulta paralelos, o planejador não os gerará para uma consulta específica se qualquer um dos seguintes estiver verdadeiro:

* A consulta escreve qualquer dado ou bloqueia qualquer linha de banco de dados. Se uma consulta contiver uma operação que modifique dados, seja no nível superior ou dentro de um CTE, não serão gerados planos paralelos para essa consulta. Como exceção, os seguintes comandos, que criam uma nova tabela e a preenchem, podem usar um plano paralelo para a parte subjacente `SELECT` da consulta:

+ `CREATE TABLE ... AS`
  + `SELECT INTO`
  + `CREATE MATERIALIZED VIEW`
  + `REFRESH MATERIALIZED VIEW`
* A consulta pode ser suspensa durante a execução. Em qualquer situação em que o sistema considere que uma execução parcial ou incremental possa ocorrer, nenhum plano paralelo é gerado. Por exemplo, um cursor criado usando [DECLARE CURSOR](sql-declare.md "DECLARE") nunca usará um plano paralelo. Da mesma forma, um loop PL/pgSQL na forma de `FOR x IN query LOOP .. END LOOP` nunca usará um plano paralelo, porque o sistema de consulta paralela não é capaz de verificar que o código no loop é seguro para execução enquanto a consulta paralela está ativa.
* A consulta usa qualquer função marcada como `PARALLEL UNSAFE`. A maioria das funções definidas pelo sistema são `PARALLEL SAFE`, mas as funções definidas pelo usuário são marcadas como padrão com `PARALLEL UNSAFE`. Veja a discussão de [Seção 15.4](parallel-safety.md "15.4. Parallel Safety").
* A consulta está sendo executada dentro de outra consulta que já é paralela. Por exemplo, se uma função chamada por uma consulta paralela emite uma consulta SQL em si, essa consulta nunca usará um plano paralelo. Esta é uma limitação da implementação atual, mas pode não ser desejável remover essa limitação, pois isso poderia resultar em uma única consulta usando um número muito grande de processos.

Mesmo quando um plano de consulta paralela é gerado para uma consulta específica, há várias circunstâncias em que será impossível executar esse plano em paralelo no momento da execução. Se isso ocorrer, o líder executará a porção do plano abaixo do nó `Gather` inteiramente por si só, quase como se o nó `Gather` não estivesse presente. Isso acontecerá se qualquer uma das seguintes condições for atendida:

* Não é possível obter trabalhadores de segundo plano devido à limitação de que o número total de trabalhadores de segundo plano não pode exceder [max_worker_processes][(runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES)].
* Não é possível obter trabalhadores de segundo plano devido à limitação de que o número total de trabalhadores de segundo plano lançados para fins de consulta paralela não pode exceder [max_parallel_workers][(runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS)].
* O cliente envia uma mensagem Execute com um número de busca não nulo. Consulte a discussão do [protocolo de consulta estendida][(protocol-flow.md#PROTOCOL-FLOW-EXT-QUERY "54.2.3. Extended Query")]. Como o [libpq][(libpq.md "Chapter 32. libpq — C Library")] atualmente não oferece nenhuma maneira de enviar tal mensagem, isso só pode ocorrer ao usar um cliente que não se baseia no libpq. Se isso for uma ocorrência frequente, pode ser uma boa ideia definir [max_parallel_workers_per_gather][(runtime-config-resource.md#GUC-MAX-PARALLEL-WORKERS-PER-GATHER)] em zero em sessões onde é provável, a fim de evitar a geração de planos de consulta que podem ser subótimos quando executados em série.