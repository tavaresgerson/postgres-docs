## 13.3. Bloqueio explícito [#](#EXPLICIT-LOCKING)

* [13.3.1. Lâminas de bloqueio de nível de tabela](explicit-locking.md#LOCKING-TABLES)
* [13.3.2. Lâminas de bloqueio de nível de linha](explicit-locking.md#LOCKING-ROWS)
* [13.3.3. Lâminas de bloqueio de nível de página](explicit-locking.md#LOCKING-PAGES)
* [13.3.4. Deadlocks](explicit-locking.md#LOCKING-DEADLOCKS)
* [13.3.5. Lâminas de aconselhamento](explicit-locking.md#ADVISORY-LOCKS)

O PostgreSQL oferece vários modos de bloqueio para controlar o acesso concorrente aos dados em tabelas. Esses modos podem ser usados para bloqueio controlado por aplicativo em situações em que o MVCC não oferece o comportamento desejado. Além disso, a maioria dos comandos do PostgreSQL adquire automaticamente blocos de modos apropriados para garantir que as tabelas referenciadas não sejam eliminadas ou modificadas de maneiras incompatíveis enquanto o comando é executado. (Por exemplo, `TRUNCATE` não pode ser executado de forma segura concorrente com outras operações na mesma tabela, então ele obtém um `ACCESS EXCLUSIVE` de bloqueio na tabela para impor isso.)

Para examinar uma lista de bloqueios atualmente pendentes em um servidor de banco de dados, use a visão de sistema `pg_locks` (view-pg-locks.md "53.13. pg_locks"). Para obter mais informações sobre o monitoramento do status do subsistema de gerenciamento de bloqueio, consulte [Capítulo 27][(monitoring.md "Chapter 27. Monitoring Database Activity")].

### 13.3.1. Lâminas de bloqueio em nível de tabela [#](#LOCKING-TABLES)

A lista abaixo mostra os modos de bloqueio disponíveis e os contextos em que eles são usados automaticamente pelo PostgreSQL. Você também pode adquirir qualquer um desses blocos explicitamente com o comando [LOCK](sql-lock.md "LOCK"). Lembre-se de que todos esses modos de bloqueio são blocos de nível de tabela, mesmo que o nome contenha a palavra “linha”; os nomes dos modos de bloqueio são históricos. Até certo ponto, os nomes refletem o uso típico de cada modo de bloqueio — mas a semântica é a mesma. A única diferença real entre um modo de bloqueio e outro é o conjunto de modos de bloqueio com os quais cada um deles entra em conflito (veja [Tabela 13.2](explicit-locking.md#TABLE-LOCK-COMPATIBILITY "Table 13.2. Conflicting Lock Modes")). Duas transações não podem manter blocos de modos conflitantes na mesma tabela ao mesmo tempo. (No entanto, uma transação nunca entra em conflito com si mesma. Por exemplo, ela pode adquirir o bloqueio `ACCESS EXCLUSIVE` e, posteriormente, adquirir o bloqueio `ACCESS SHARE` na mesma tabela.) Modos de bloqueio não conflitantes podem ser mantidos simultaneamente por muitas transações. Observe, em particular, que alguns modos de bloqueio são autoconflitantes (por exemplo, um bloqueio `ACCESS EXCLUSIVE` não pode ser mantido por mais de uma transação de cada vez) enquanto outros não são autoconflitantes (por exemplo, um bloqueio `ACCESS SHARE` pode ser mantido por várias transações).

Modos de bloqueio em nível de tabela

`ACCESS SHARE` (`AccessShareLock`): Confere compatibilidade apenas com o modo de bloqueio `ACCESS EXCLUSIVE`.

O comando `SELECT` adquire um bloqueio desse modo em tabelas referenciadas. Em geral, qualquer consulta que leia apenas uma tabela e não a modifique adquire esse modo de bloqueio.

`ROW SHARE` (`RowShareLock`): Conflitos com os modos de bloqueio `EXCLUSIVE` e `ACCESS EXCLUSIVE`.

O comando `SELECT` adquire um bloqueio desse modo em todas as tabelas nas quais uma das opções `FOR UPDATE`, `FOR NO KEY UPDATE`, `FOR SHARE` ou `FOR KEY SHARE` é especificada (ainda que `ACCESS SHARE` bloqueie quaisquer outras tabelas que sejam referenciadas sem qualquer opção explícita de bloqueio `FOR ...`).

`ROW EXCLUSIVE` (`RowExclusiveLock`): Confere incompatibilidade com os modos de bloqueio dos `SHARE`, `SHARE ROW EXCLUSIVE`, `EXCLUSIVE` e `ACCESS EXCLUSIVE`.

Os comandos `UPDATE`, `DELETE`, `INSERT` e `MERGE` adquirem esse modo de bloqueio na tabela alvo (ainda que `ACCESS SHARE` bloqueie quaisquer outras tabelas referenciadas). Em geral, esse modo de bloqueio será adquirido por qualquer comando que *modifique dados* em uma tabela.

`SHARE UPDATE EXCLUSIVE` (`ShareUpdateExclusiveLock`): Confere incompatibilidade com os modos de bloqueio `SHARE UPDATE EXCLUSIVE`, `SHARE`, `SHARE ROW EXCLUSIVE`, `EXCLUSIVE` e `ACCESS EXCLUSIVE`. Este modo protege uma tabela contra mudanças simultâneas no esquema e `VACUUM` é executado.

Adquirida por `VACUUM` (sem `FULL`, `ANALYZE`, `CREATE INDEX CONCURRENTLY`, `CREATE STATISTICS`, `COMMENT ON`, `REINDEX CONCURRENTLY` e certas variantes de [`ALTER INDEX`](sql-alterindex.md "ALTER INDEX") e [`ALTER TABLE`(sql-altertable.md "ALTER TABLE") (para detalhes completos, consulte a documentação desses comandos).

`SHARE` (`ShareLock`): Confere incompatibilidade com os modos de bloqueio de `ROW EXCLUSIVE`, `SHARE UPDATE EXCLUSIVE`, `SHARE ROW EXCLUSIVE`, `EXCLUSIVE` e `ACCESS EXCLUSIVE`. Este modo protege uma tabela contra alterações de dados concorrentes.

Adquirida por `CREATE INDEX` (sem `CONCURRENTLY`).

`SHARE ROW EXCLUSIVE` (`ShareRowExclusiveLock`): Confere incompatibilidade com os modos de bloqueio `ROW EXCLUSIVE`, `SHARE UPDATE EXCLUSIVE`, `SHARE`, `SHARE ROW EXCLUSIVE`, `EXCLUSIVE` e `ACCESS EXCLUSIVE`. Este modo protege uma tabela contra alterações de dados concorrentes e é autoexclusivo, de modo que apenas uma sessão pode mantê-lo de cada vez.

Adquirida pela `CREATE TRIGGER` e algumas formas de [`ALTER TABLE`](sql-altertable.md "ALTER TABLE").

`EXCLUSIVE` (`ExclusiveLock`): Confere incompatibilidade com os modos de bloqueio `ROW SHARE`, `ROW EXCLUSIVE`, `SHARE UPDATE EXCLUSIVE`, `SHARE`, `SHARE ROW EXCLUSIVE`, `EXCLUSIVE` e `ACCESS EXCLUSIVE`. Este modo permite apenas bloqueios `ACCESS SHARE` concorrentes, ou seja, apenas leituras na tabela podem prosseguir em paralelo com uma transação que mantém este modo de bloqueio.

Adquirida por `REFRESH MATERIALIZED VIEW CONCURRENTLY`.

`ACCESS EXCLUSIVE` (`AccessExclusiveLock`): Conflitos com bloqueios de todos os modos (`ACCESS SHARE`, `ROW SHARE`, `ROW EXCLUSIVE`, `SHARE UPDATE EXCLUSIVE`, `SHARE`, `SHARE ROW EXCLUSIVE`, `EXCLUSIVE` e `ACCESS EXCLUSIVE`). Este modo garante que o titular é a única transação a acessar a tabela de qualquer maneira.

Os comandos adquiridos pelos `DROP TABLE`, `TRUNCATE`, `REINDEX`, `CLUSTER`, `VACUUM FULL` e `REFRESH MATERIALIZED VIEW` (sem `CONCURRENTLY`) também adquirem um bloqueio nesse nível. Esse também é o modo de bloqueio padrão para as declarações `ALTER INDEX` e `ALTER TABLE` que não especificam um modo explicitamente.

### DICA

Apenas um bloqueio `ACCESS EXCLUSIVE` bloqueia uma declaração `SELECT` (sem `FOR UPDATE/SHARE`).

Uma vez adquirida, uma bloqueio é normalmente mantida até o final da transação. Mas se um bloqueio é adquirido após a criação de um ponto de salvamento, o bloqueio é liberado imediatamente se o ponto de salvamento for desfeito. Isso está de acordo com o princípio de que `ROLLBACK` cancela todos os efeitos dos comandos desde o ponto de salvamento. O mesmo vale para os bloqueios adquiridos dentro de um bloco de exceção PL/pgSQL: uma fuga de erro do bloco libera os bloqueios adquiridos nele.

**Tabela 13.2. Modos de bloqueio conflitantes**



<table border="1" class="table" summary="Conflicting Lock Modes">
<colgroup>
<col/>
<col class="lockst"/>
<col/>
<col/>
<col/>
<col/>
<col/>
<col/>
<col class="lockend"/>
</colgroup>
<thead>
<tr>
<th rowspan="2">
    Requested Lock Mode
   </th>
<th align="center" colspan="8">
    Existing Lock Mode
   </th>
</tr>
<tr>
<th>
<code class="literal">
     ACCESS SHARE
    </code>
</th>
<th>
<code class="literal">
     ROW SHARE
    </code>
</th>
<th>
<code class="literal">
     ROW EXCL.
    </code>
</th>
<th>
<code class="literal">
     SHARE UPDATE EXCL.
    </code>
</th>
<th>
<code class="literal">
     SHARE
    </code>
</th>
<th>
<code class="literal">
     SHARE ROW EXCL.
    </code>
</th>
<th>
<code class="literal">
     EXCL.
    </code>
</th>
<th>
<code class="literal">
     ACCESS EXCL.
    </code>
</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="literal">
     ACCESS SHARE
    </code>
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
    X
   </td>
</tr>
<tr>
<td>
<code class="literal">
     ROW SHARE
    </code>
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
</tr>
<tr>
<td>
<code class="literal">
     ROW EXCL.
    </code>
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
</tr>
<tr>
<td>
<code class="literal">
     SHARE UPDATE EXCL.
    </code>
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
</tr>
<tr>
<td>
<code class="literal">
     SHARE
    </code>
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
</td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
</tr>
<tr>
<td>
<code class="literal">
     SHARE ROW EXCL.
    </code>
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
</tr>
<tr>
<td>
<code class="literal">
     EXCL.
    </code>
</td>
<td align="center">
</td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
</tr>
<tr>
<td>
<code class="literal">
     ACCESS EXCL.
    </code>
</td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
</tr>
</tbody>
</table>



### 13.3.2. Lås de nível de linha [#](#LOCKING-ROWS)

Além das bloqueadoras de nível de tabela, existem bloqueadoras de nível de linha, que são listadas abaixo com os contextos em que elas são usadas automaticamente pelo PostgreSQL. Veja [Tabela 13.3][(explicit-locking.md#ROW-LOCK-COMPATIBILITY "Table 13.3. Conflicting Row-Level Locks")] para uma tabela completa de conflitos de bloqueadoras de nível de linha. Note que uma transação pode manter bloqueadoras conflitantes na mesma linha, mesmo em subtransações diferentes; mas, além disso, duas transações nunca podem manter bloqueadoras conflitantes na mesma linha. As bloqueadoras de nível de linha não afetam a consulta de dados; elas bloqueiam apenas os *escritores e bloqueadores* da mesma linha. As bloqueadoras de nível de linha são liberadas no final da transação ou durante o rollback do ponto de salvamento, assim como as bloqueadoras de nível de tabela.

Modos de bloqueio de nível de linha

`FOR UPDATE`: `FOR UPDATE` faz com que as linhas recuperadas pela declaração `SELECT` sejam bloqueadas como se estivessem para atualização. Isso impede que elas sejam bloqueadas, modificadas ou excluídas por outras transações até que a transação atual termine. Isso significa que outras transações que tentem `UPDATE`, `DELETE`, `SELECT FOR UPDATE`, `SELECT FOR NO KEY UPDATE`, `SELECT FOR SHARE` ou `SELECT FOR KEY SHARE` dessas linhas serão bloqueadas até que a transação atual termine; por outro lado, `SELECT FOR UPDATE` aguardará uma transação concorrente que tenha executado qualquer um desses comandos na mesma linha, e então bloqueará e retornará a linha atualizada (ou nenhuma linha, se a linha foi excluída). Dentro de uma transação `REPEATABLE READ` ou `SERIALIZABLE`, no entanto, um erro será lançado se uma linha a ser bloqueada tiver sido alterada desde o início da transação. Para uma discussão adicional, consulte [Seção 13.4][(applevel-consistency.md "13.4. Data Consistency Checks at the Application Level")].

O modo de bloqueio `FOR UPDATE` também é adquirido por qualquer `DELETE` em uma linha, e também por um `UPDATE` que modifica os valores de certas colunas. Atualmente, o conjunto de colunas consideradas para o caso `UPDATE` são aquelas que têm um índice único sobre elas que pode ser usado em uma chave estrangeira (assim, índices parciais e índices expressivos não são considerados), mas isso pode mudar no futuro.

`FOR NO KEY UPDATE`: Se comporta de forma semelhante ao `FOR UPDATE`, exceto que o bloqueio adquirido é mais fraco: este bloqueio não impedirá os comandos `SELECT FOR KEY SHARE` que tentam adquirir um bloqueio nas mesmas linhas. Este modo de bloqueio também é adquirido por qualquer `UPDATE` que não adquira um bloqueio `FOR UPDATE`.

`FOR SHARE`: Se comporta de forma semelhante a `FOR NO KEY UPDATE`, exceto que ele adquire um bloqueio compartilhado em vez de um bloqueio exclusivo em cada linha recuperada. Um bloqueio compartilhado bloqueia outras transações de realizar `UPDATE`, `DELETE`, `SELECT FOR UPDATE` ou `SELECT FOR NO KEY UPDATE` nessas linhas, mas não impede que elas realizem `SELECT FOR SHARE` ou `SELECT FOR KEY SHARE`.

`FOR KEY SHARE`: Se comporta de forma semelhante a `FOR SHARE`, exceto que o bloqueio é mais fraco: `SELECT FOR UPDATE` está bloqueado, mas não `SELECT FOR NO KEY UPDATE`. Um bloqueio compartilhado por chave impede que outras transações realizem `DELETE` ou qualquer `UPDATE` que mude os valores da chave, mas não outros `UPDATE`, e também não impede `SELECT FOR NO KEY UPDATE`, `SELECT FOR SHARE`, ou `SELECT FOR KEY SHARE`.

O PostgreSQL não lembra nenhuma informação sobre as linhas modificadas na memória, portanto, não há limite no número de linhas bloqueadas de uma só vez. No entanto, bloquear uma linha pode causar uma escrita em disco, por exemplo, `SELECT FOR UPDATE` modifica as linhas selecionadas para marcar elas como bloqueadas, e assim resultará em escritas em disco.

**Tabela 13.3. Lâminas de bloqueio em nível de linha conflitantes**



<table border="1" class="table" summary="Conflicting Row-Level Locks">
<colgroup>
<col class="col1"/>
<col class="lockst"/>
<col class="col3"/>
<col class="col4"/>
<col class="lockend"/>
</colgroup>
<thead>
<tr>
<th rowspan="2">Modo de bloqueio solicitado</th>
<th colspan="4">
    Current Lock Mode
   </th>
</tr>
<tr>
<th>PARA A PARTIR DA COMPARTILHADA CLÁSSICA</th>
<th>
    FOR SHARE
   </th>
<th>
    FOR NO KEY UPDATE
   </th>
<th>
    FOR UPDATE
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>PARA A PARTIR DA COMPARTILHADA CLÁSSICA</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
    X
   </td>
</tr>
<tr>
<td>PARA PARtilhar</td>
<td align="center">
</td>
<td align="center">
</td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
</tr>
<tr>
<td>SEM ATUALIZAÇÃO DE CHAVE</td>
<td align="center">
</td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
</tr>
<tr>
<td>PARA ATUALIZAÇÃO</td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
<td align="center">
    X
   </td>
</tr>
</tbody>
</table>



### 13.3.3. Lås de nível de página [#](#LOCKING-PAGES)

Além dos bloqueios de tabela e de linha, as permissões de compartilhamento/exclusivas de nível de página são usadas para controlar o acesso de leitura/escrita às páginas de tabela no conjunto de buffers compartilhados. Esses bloqueios são liberados imediatamente após uma linha ser buscada ou atualizada. Normalmente, os desenvolvedores de aplicativos não precisam se preocupar com os bloqueios de nível de página, mas eles são mencionados aqui por completo.

### 13.3.4. Deadlocks [#](#LOCKING-DEADLOCKS)

O uso de bloqueio explícito pode aumentar a probabilidade de *deadlocks*, nos quais duas (ou mais) transações cada uma detém bloqueios que a outra deseja. Por exemplo, se a transação 1 adquire um bloqueio exclusivo na tabela A e depois tenta adquirir um bloqueio exclusivo na tabela B, enquanto a transação 2 já bloqueia exclusivamente a tabela B e agora deseja um bloqueio exclusivo na tabela A, então nenhuma delas pode prosseguir. O PostgreSQL detecta automaticamente situações de deadlocks e as resolve abortando uma das transações envolvidas, permitindo que as outras sejam concluídas. (É difícil prever exatamente qual transação será abortada e não deve ser confiada.)

Observe que deadlocks também podem ocorrer como resultado de bloqueios de nível de linha (e, portanto, podem ocorrer mesmo que o bloqueio explícito não seja usado). Considere o caso em que duas transações concorrentes modificam uma tabela. A primeira transação executa:

```
UPDATE accounts SET balance = balance + 100.00 WHERE acctnum = 11111;
```

Isso obtém um bloqueio de nível de linha na linha com o número de conta especificado. Em seguida, a segunda transação é executada:

```
UPDATE accounts SET balance = balance + 100.00 WHERE acctnum = 22222;
UPDATE accounts SET balance = balance - 100.00 WHERE acctnum = 11111;
```

A primeira declaração `UPDATE` consegue adquirir um bloqueio de nível de linha na linha especificada, então ela consegue atualizar essa linha. No entanto, a segunda declaração `UPDATE` descobre que a linha que está tentando atualizar já foi bloqueada, então ela espera que a transação que adquiriu o bloqueio seja concluída. A transação dois está agora esperando que a transação um seja concluída antes de continuar a execução. Agora, a transação um é executada:

```
UPDATE accounts SET balance = balance - 100.00 WHERE acctnum = 22222;
```

A transação um tenta adquirir um bloqueio de nível de linha na linha especificada, mas não consegue: a transação dois já detém tal bloqueio. Assim, ela espera que a transação dois complete. Assim, a transação um é bloqueada na transação dois, e a transação dois é bloqueada na transação um: uma condição de impasse. O PostgreSQL detectará essa situação e abortará uma das transações.

A melhor defesa contra deadlocks é, geralmente, evitar-os, garantindo que todas as aplicações que utilizam um banco de dados adquiram bloqueios em múltiplos objetos em uma ordem consistente. No exemplo acima, se ambas as transações tivessem atualizado as linhas na mesma ordem, nenhum deadlock teria ocorrido. Também é importante garantir que o primeiro bloqueio adquirido em um objeto em uma transação seja o modo mais restritivo que será necessário para esse objeto. Se não for viável verificar isso antecipadamente, então deadlocks podem ser tratados em tempo real, repetindo as transações que são abortadas devido a deadlocks.

Enquanto não for detectada uma situação de bloqueio, uma transação que busca um bloqueio em nível de tabela ou em nível de linha aguardará indefinidamente a liberação de bloqueios conflitantes. Isso significa que é uma má ideia para aplicativos manterem transações abertas por longos períodos de tempo (por exemplo, enquanto aguardam a entrada do usuário).

### 13.3.5. Rastreadores de segurança [#](#ADVISORY-LOCKS)

O PostgreSQL oferece uma maneira de criar bloqueios que têm significados definidos pela aplicação. Esses são chamados de *bloqueios aconselhados*, porque o sistema não exige seu uso — cabe à aplicação usá-los corretamente. Bloqueios aconselhados podem ser úteis para estratégias de bloqueio que são um ajuste complicado para o modelo MVCC. Por exemplo, um uso comum de bloqueios aconselhados é emular estratégias de bloqueio pessimista típicas dos chamados sistemas de gerenciamento de dados de "arquivo plano". Embora uma bandeira armazenada em uma tabela possa ser usada para o mesmo propósito, os bloqueios aconselhados são mais rápidos, evitam o bloat da tabela e são automaticamente limpos pelo servidor no final da sessão.

Existem duas maneiras de adquirir um bloqueio de consulta em PostgreSQL: em nível de sessão ou em nível de transação. Uma vez adquirido em nível de sessão, um bloqueio de consulta é mantido até que seja explicitamente liberado ou a sessão termine. Ao contrário dos pedidos de bloqueio padrão, os pedidos de bloqueio de consulta em nível de sessão não respeitam a semântica da transação: um bloqueio adquirido durante uma transação que é posteriormente anulada ainda será mantido após o rollback, e, da mesma forma, um desbloqueio é eficaz mesmo que a transação que o solicitou falhe posteriormente. Um bloqueio pode ser adquirido várias vezes pelo processo proprietário; para cada solicitação de bloqueio concluída, deve haver uma solicitação de desbloqueio correspondente antes que o bloqueio seja realmente liberado. Pedidos de bloqueio em nível de transação, por outro lado, se comportam mais como pedidos de bloqueio regulares: eles são liberados automaticamente no final da transação, e não há operação de desbloqueio explícita. Esse comportamento é frequentemente mais conveniente do que o comportamento em nível de sessão para o uso de curto prazo de um bloqueio de consulta. Pedidos de bloqueio em nível de sessão e de transação para o mesmo identificador de bloqueio de consulta se bloquearão uns aos outros da maneira esperada. Se uma sessão já possui um bloqueio de consulta dado, solicitações adicionais dela sempre terão sucesso, mesmo que outras sessões estejam aguardando o bloqueio; essa afirmação é verdadeira independentemente de o bloqueio existente e a nova solicitação estarem em nível de sessão ou de transação.

Como todos os bloqueios em PostgreSQL, uma lista completa de bloqueios consultados atualmente mantidos por qualquer sessão pode ser encontrada na visão do sistema [[`pg_locks`][(view-pg-locks.md "53.13. pg_locks")]].

Tanto os bloqueios de aconselhamento quanto os blocos regulares são armazenados em um pool de memória compartilhada cujo tamanho é definido pelas variáveis de configuração [max_locks_per_transaction](runtime-config-locks.md#GUC-MAX-LOCKS-PER-TRANSACTION) e [max_connections](runtime-config-connection.md#GUC-MAX-CONNECTIONS). É necessário ter cuidado para não esgotar essa memória, pois, caso contrário, o servidor não poderá conceder nenhum bloqueio. Isso impõe um limite superior ao número de blocos de aconselhamento que o servidor pode conceder, tipicamente nas dezenas a centenas de milhares, dependendo da configuração do servidor.

Em certos casos, ao usar métodos de bloqueio de consulta, especialmente em consultas que envolvem cláusulas de ordenação explícita e `LIMIT`, é necessário ter cuidado para controlar os bloqueios adquiridos devido à ordem em que as expressões SQL são avaliadas. Por exemplo:

```
SELECT pg_advisory_lock(id) FROM foo WHERE id = 12345; -- ok
SELECT pg_advisory_lock(id) FROM foo WHERE id > 12345 LIMIT 100; -- danger!
SELECT pg_advisory_lock(q.id) FROM
(
  SELECT id FROM foo WHERE id > 12345 LIMIT 100
) q; -- ok
```

Nas consultas acima, a segunda forma é perigosa porque não é garantido que o `LIMIT` seja aplicado antes da execução da função de bloqueio. Isso pode causar alguns bloqueios que o aplicativo não esperava e, portanto, não seria liberado (até que termine a sessão). Do ponto de vista do aplicativo, esses bloqueios seriam pendentes, embora ainda visíveis em `pg_locks`.

As funções fornecidas para manipular bloqueios de aconselhamento são descritas em [Seção 9.28.10][(functions-admin.md#FUNCTIONS-ADVISORY-LOCKS "9.28.10. Advisory Lock Functions")].