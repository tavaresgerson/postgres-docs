## E.2. Versão 18.3 [#](#RELEASE-18-3)

* [E.2.1. Migração para a Versão 18.3](release-18-3.md#RELEASE-18-3-MIGRATION)
* [E.2.2. Alterações](release-18-3.md#RELEASE-18-3-CHANGES)

**Data de lançamento:** 26/02/2026

Esta versão contém um pequeno número de correções da versão 18.2. Para informações sobre as novas funcionalidades da versão principal 18, consulte [Seção E.5](release-18.md).

### E.2.1. Migração para a Versão 18.3 [#](#RELEASE-18-3-MIGRATION)

Não é necessário fazer um descarte/restauração para aqueles que estão rodando a versão 18.X.

No entanto, se você está atualizando a partir de uma versão anterior à 18.2, consulte [Seção E.3](release-18-2.md).

### E.2.2. Alterações [#](#RELEASE-18-3-CHANGES)

* Consertar falha após a reprodução de um registro de truncação multixid do WAL que foi gerado por uma versão menor anterior (Heikki Linnakangas) [§](https://postgr.es/c/817f74600)

A lógica errada para lidar com a forma como as versões anteriores tratavam o multixid wraparound levou ao fracasso do replay, com mensagens como “não foi possível acessar o status da transação”. Um cenário típico em que isso poderia ocorrer é um servidor de espera da versão menor mais recente consumindo WAL de um servidor primário de uma versão mais antiga.
* Evite a reclamação incorreta de codificação inválida quando `substring()` é aplicado a dados “tostados” (Noah Misch) [§](https://postgr.es/c/6e045e1a6) [§](https://postgr.es/c/d04b34d68) [§](https://postgr.es/c/4174e41b9)

A correção para o CVE-2026-2006 foi muito agressiva e poderia gerar um erro sobre um caracter incompleto em casos que são, na verdade, válidos.
* Erro de revisão na correção para o CVE-2026-2007 (Zsolt Parragi) [§](https://postgr.es/c/041e02e6a)

Se o array de "limites" precisar ser expandido, porque a entrada continha mais trigêmeos do que a suposição inicial, `generate_trgm_only` não retornou o ponteiro de matriz modificado para seu chamador. Isso levaria a saída incorreta de `strict_word_similarity()` e funções relacionadas, ou, em casos raros, a um travamento. O código defeituoso é alcançado se a string de entrada se tornar mais longa quando é convertida para maiúsculas. As únicas instâncias conhecidas disso ocorrem quando um local de ICU é usado com certas codificações de único byte.
* Corrija a marcação de volatilidade de `json_strip_nulls()` e `jsonb_strip_nulls()` (Andrew Dunstan) [§](https://postgr.es/c/2f6ee7b38)

Essas funções sempre foram consideradas imutáveis, mas a refatoração na versão 18 acidentalmente as marcou como estáveis em vez disso. Isso impede seu uso em expressões de índice e pode causar avaliações repetidas desnecessárias em consultas. Esta correção corrige a marcação em clusters de banco de dados recém-inicializados (incluindo clusters que são pg_upgrade'd para 18.3 ou posterior). No entanto, ela não ajudará clusters existentes feitos usando 18.0 a 18.2.

Se esse erro afetar o uso dessas funções, a correção recomendada para um clúster existente é uma atualização manual do catálogo. Como usuário superusuário, realize

```
UPDATE pg_catalog.pg_proc SET provolatile = 'i' WHERE oid IN ('3261','3262');
```

em cada banco de dados afetado. Atualize também `template0` e `template1` para que os bancos de dados feitos no futuro tenham a correção.
* Correção da computação do conjunto de junções externas potencialmente anuláveis para o resultado de uma subconsulta `LATERAL UNION ALL` (Richard Guo) [§](https://postgr.es/c/ed57c207c)

Esse erro pode levar ao omissão dos testes `NOT NULL`, na crença equivocada de que eles eram desnecessários, resultando em saída de consulta errada.
* Evite colisões de nomes entre restrições escritas pelo usuário e restrições `NOT NULL` com nomes automaticamente definidos (Laurenz Albe) [§](https://postgr.es/c/8d9a97e0b)

A partir da versão 18, as restrições `NOT NULL` possuem entradas completas de `pg_constraint`, e, portanto, exigem nomes. A lógica para escolher um nome para uma restrição `NOT NULL` sem nome não conseguiu evitar conflitos com restrições escritas pelo usuário em outros lugares da mesma declaração `CREATE TABLE`.
* Considere corrigir `pg_stat_get_backend_wait_event()` e `pg_stat_get_backend_wait_event_type()` para relatar valores para processos auxiliares (Heikki Linnakangas) [§](https://postgr.es/c/53463b4b2)

Anteriormente, essas funções retornavam NULL para processos auxiliares, mas isso é inconsistente com a visão `pg_stat_activity`.
* Consertar o casting de uma variável de tipo composto para um tipo de domínio ao retornar seu valor de uma função PL/pgSQL (Tom Lane) [§](https://postgr.es/c/ce4b7e3a1)

Se o valor da variável for NULL, resultou em um erro de "busca de cache falhou para o tipo 0".
* Consertar possível referência de ponteiro nulo na função de entrada binária de `contrib/hstore` (Michael Paquier) [§](https://postgr.es/c/4a0843c53)

A função de recebimento do `hstore` travou em entrada contendo chaves duplicadas. Os valores do `hstore` gerados pelo Postgres nunca contariam chaves duplicadas, então esse erro passou despercebido. O travamento poderia ser provocado por dados maliciosos ou corrompidos.