## 13.2. Isolamento de Transações [#](#TRANSACTION-ISO)

* [13.2.1. Nível de Isolamento de Leitura Comprometido](transaction-iso.md#XACT-READ-COMMITTED)
* [13.2.2. Nível de Leitura Repetível](transaction-iso.md#XACT-REPEATABLE-READ)
* [13.2.3. Nível de Isolamento Serializável](transaction-iso.md#XACT-SERIALIZABLE)

O padrão SQL define quatro níveis de isolamento de transação. O mais rigoroso é Serializable, que é definido pelo padrão em um parágrafo que diz que qualquer execução concorrente de um conjunto de transações Serializable é garantida para produzir o mesmo efeito que executá-las uma de cada vez em algum ordem. Os outros três níveis são definidos em termos de fenômenos, resultantes da interação entre transações concorrentes, que não devem ocorrer em cada nível. O padrão observa que, devido à definição de Serializable, nenhum desses fenômenos é possível nesse nível. (Isso dificilmente é surpreendente -- se o efeito das transações deve ser consistente com ter sido executado uma de cada vez, como você poderia ver algum fenômeno causado por interações?)

Os fenômenos que são proibidos em vários níveis são:

leitura suja: uma transação lê dados escritos por uma transação não comprometida concorrente.

não-repetível: Uma transação re lê os dados que já havia lido anteriormente e descobre que os dados foram modificados por outra transação (que foi comprometida desde a leitura inicial).

Phantom read: Uma transação reexecuta uma consulta que retorna um conjunto de linhas que satisfazem uma condição de pesquisa e descobre que o conjunto de linhas que satisfazem a condição mudou devido a outra transação recentemente realizada.

anomalia de serialização: O resultado de comprovar com sucesso um grupo de transações é inconsistente com todas as possíveis ordens de execução dessas transações uma de cada vez.

Os níveis de isolamento de transação implementados no padrão SQL e no PostgreSQL são descritos em [Tabela 13.1](transaction-iso.md#MVCC-ISOLEVEL-TABLE).

**Tabela 13.1. Níveis de Isolamento de Transação**



<table border="1" class="table" summary="Transaction Isolation Levels">
 <colgroup>
  <col/>
  <col/>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Isolation Level
   </th>
   <th>
    Dirty Read
   </th>
   <th>
    Nonrepeatable Read
   </th>
   <th>
    Phantom Read
   </th>
   <th>
    Serialization Anomaly
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    Read uncommitted
   </td>
   <td>
    Permitido, mas não em PG
   </td>
   <td>
    Possible
   </td>
   <td>
    Possible
   </td>
   <td>
    Possible
   </td>
  </tr>
  <tr>
   <td>
    Read committed
   </td>
   <td>
    Não é possível
   </td>
   <td>
    Possible
   </td>
   <td>
    Possible
   </td>
   <td>
    Possible
   </td>
  </tr>
  <tr>
   <td>
    Repeatable read
   </td>
   <td>
    Não é possível
   </td>
   <td>
    Not possible
   </td>
   <td>
    Allowed, but not in PG
   </td>
   <td>
    Possible
   </td>
  </tr>
  <tr>
   <td>
    Serializable
   </td>
   <td>
    Não é possível
   </td>
   <td>
    Not possible
   </td>
   <td>
    Not possible
   </td>
   <td>
    Not possible
   </td>
  </tr>
 </tbody>
</table>










Em PostgreSQL, você pode solicitar qualquer um dos quatro níveis padrão de isolamento de transação, mas internamente, apenas três níveis de isolamento distintos são implementados, ou seja, o modo Não Comitado de Leitura do PostgreSQL se comporta como Leitura Comitada. Isso ocorre porque é a única maneira sensível de mapear os níveis de isolamento padrão para a arquitetura de controle de concorrência multiversão do PostgreSQL.

A tabela também mostra que a implementação de Leitura Repetível do PostgreSQL não permite leituras fantasmas. Isso é aceitável sob o padrão SQL, porque o padrão especifica quais anomalias não devem *ocorrer* em certos níveis de isolamento; garantias mais altas são aceitáveis. O comportamento dos níveis de isolamento disponíveis é detalhado nas seções a seguir.

Para definir o nível de isolamento de transação de uma transação, use o comando [SET TRANSACTION](sql-set-transaction.md "SET TRANSACTION").

### Importante

Alguns tipos de dados e funções do PostgreSQL têm regras especiais em relação ao comportamento transacional. Em particular, as alterações feitas em uma sequência (e, portanto, o contador de uma coluna declarada usando `serial`) são imediatamente visíveis para todas as outras transações e não são revertidas se a transação que fez as alterações abortar. Veja [Seção 9.17](functions-sequence.md) e [Seção 8.1.4](datatype-numeric.md#DATATYPE-SERIAL).

### 13.2.1. Nível de Isolamento de Leitura Comprometido [#](#XACT-READ-COMMITTED)

*Read Committed* é o nível de isolamento padrão no PostgreSQL. Quando uma transação usa esse nível de isolamento, uma consulta `SELECT` (sem uma cláusula `FOR UPDATE/SHARE`) vê apenas dados comprometidos antes do início da consulta; ela nunca vê dados não comprometidos ou alterações comprometidas por transações concorrentes durante a execução da consulta. Na prática, uma consulta `SELECT` vê um instantâneo do banco de dados no momento em que a consulta começa a ser executada. No entanto, `SELECT` vê os efeitos das atualizações anteriores executadas dentro de sua própria transação, mesmo que ainda não estejam comprometidas. Além disso, note que dois comandos consecutivos `SELECT` podem ver dados diferentes, mesmo que estejam dentro de uma única transação, se outras transações comprometem alterações após o início do primeiro `SELECT` e antes do início do segundo `SELECT`.

Os comandos `UPDATE`, `DELETE`, `SELECT FOR UPDATE` e `SELECT FOR SHARE` comportam-se da mesma forma que `SELECT` em termos de busca de linhas alinhadas: eles só encontrarão linhas alinhadas que foram comprometidas no momento da hora de início do comando. No entanto, uma tal linha alinhada pode já ter sido atualizada (ou excluída ou bloqueada) por outra transação concorrente no momento em que é encontrada. Neste caso, o pretendente a atualização irá esperar que a primeira transação de atualização comprometa ou desconsome (se ainda estiver em progresso). Se a primeira atualização desconsome, seus efeitos são negados e a segunda atualização pode proceder com a atualização da linha originalmente encontrada. Se a primeira atualização compromete, a segunda atualização ignorará a linha se a primeira atualização a excluiu, caso contrário, tentará aplicar sua operação à versão atualizada da linha. A condição de busca do comando (a cláusula `WHERE`) é reavaliada para ver se a versão atualizada da linha ainda corresponde à condição de busca. Se sim, a segunda atualização procede com sua operação usando a versão atualizada da linha. No caso de `SELECT FOR UPDATE` e `SELECT FOR SHARE`, isso significa que é a versão atualizada da linha que é bloqueada e devolvida ao cliente.

`INSERT` com uma cláusula `ON CONFLICT DO UPDATE` comporta-se de maneira semelhante. No modo de Commit de Leitura, cada linha proposta para inserção será inserida ou atualizada. A menos que haja erros não relacionados, um desses dois resultados é garantido. Se um conflito se origina em outra transação cujos efeitos ainda não são visíveis para o `INSERT`, a cláusula `UPDATE` afetará essa linha, mesmo que possivelmente *nenhuma* versão dessa linha seja convencionalmente visível ao comando.

`INSERT` com uma cláusula `ON CONFLICT DO NOTHING` pode ter a inserção não prosseguir para uma linha devido ao resultado de outra transação cujos efeitos não são visíveis ao instantâneo `INSERT`. Novamente, isso ocorre apenas no modo de Comprometimento de Leitura.

`MERGE` permite que o usuário especifique várias combinações de subcomandos `INSERT`, `UPDATE` e `DELETE`. Um comando `MERGE` com os subcomandos `INSERT` e `UPDATE` parece semelhante a `INSERT` com uma cláusula `ON CONFLICT DO UPDATE`, mas não garante que `INSERT` ou `UPDATE` ocorrerá. Se `MERGE` tenta um `UPDATE` ou `DELETE` e a linha é atualizada simultaneamente, mas a condição de junção ainda passa para o alvo atual e o tupla atual da fonte, então `MERGE` se comportará da mesma forma que os comandos `UPDATE` ou `DELETE` e realizará sua ação na versão atualizada da linha. No entanto, como `MERGE` pode especificar várias ações e elas podem ser condicionais, as condições para cada ação são reavaliadas na versão atualizada da linha, começando pela primeira ação, mesmo que a ação que originalmente correspondia apareça mais tarde na lista de ações. Por outro lado, se a linha é atualizada simultaneamente de modo que a condição de junção falhe, então `MERGE` avaliará as ações `NOT MATCHED BY SOURCE` e `NOT MATCHED [BY TARGET]` do comando, e executará a primeira delas que tiver sucesso. Se a linha é excluída simultaneamente, então `MERGE` avaliará as ações `NOT MATCHED [BY TARGET]` do comando, e executará a primeira que tiver sucesso. Se `MERGE` tenta um `INSERT` e um índice único está presente e uma linha duplicada é inserida simultaneamente, então é levantado um erro de violação de unicidade; `MERGE` não tenta evitar tais erros reiniciando a avaliação das condições `MATCHED`.

Devido às regras acima, é possível que um comando de atualização veja um instantâneo inconsistente: ele pode ver os efeitos de comandos de atualização concorrentes nas mesmas linhas que está tentando atualizar, mas não vê os efeitos desses comandos em outras linhas do banco de dados. Esse comportamento torna o modo de comprometimento de leitura inadequado para comandos que envolvem condições de busca complexas; no entanto, é perfeito para casos mais simples. Por exemplo, considere a transferência de $100 de uma conta para outra:

```
BEGIN;
UPDATE accounts SET balance = balance + 100.00 WHERE acctnum = 12345;
UPDATE accounts SET balance = balance - 100.00 WHERE acctnum = 7534;
COMMIT;
```

Se outra transação tentar alterar o saldo da conta 7534 simultaneamente, queremos claramente que o segundo extrato comece com a versão atualizada da linha da conta. Como cada comando afeta apenas uma linha predeterminada, permitir que ele veja a versão atualizada da linha não cria nenhuma inconsistência problemática.

O uso mais complexo pode produzir resultados indesejados no modo de leitura com compromisso. Por exemplo, considere um comando `DELETE` que opera em dados que estão sendo adicionados e removidos de seus critérios de restrição por outro comando, por exemplo, suponha que `website` seja uma tabela de duas linhas com `website.hits` igual a `9` e `10`:

```
BEGIN;
UPDATE website SET hits = hits + 1;
-- run from another session:  DELETE FROM website WHERE hits = 10;
COMMIT;
```

O `DELETE` não terá efeito, mesmo que haja uma linha `website.hits = 10` antes e depois do `UPDATE`. Isso ocorre porque o valor da linha pré-atualização `9` é ignorado, e quando o `UPDATE` é concluído e o `DELETE` obtém um bloqueio, o novo valor da linha não é mais `10`, mas sim `11`, que não mais corresponde aos critérios.

Como o modo de leitura comprometida inicia cada comando com um novo instantâneo que inclui todas as transações comprometidas até aquele momento, os comandos subsequentes na mesma transação verão os efeitos da transação concorrente comprometida, de qualquer forma. O ponto em questão acima é se um *único* comando verá uma visão absolutamente consistente do banco de dados ou

A isolação parcial de transação fornecida pelo modo de comprometimento de leitura é adequada para muitas aplicações, e esse modo é rápido e fácil de usar; no entanto, não é suficiente para todos os casos. Aplicações que realizam consultas e atualizações complexas podem exigir uma visão de banco de dados mais consistentemente rigorosa do que o modo de comprometimento de leitura fornece.

### 13.2.2. Nível de isolamento de leitura repetida [#](#XACT-REPEATABLE-READ)

O nível de isolamento *Repeatable Read* só vê dados comprometidos antes do início da transação; ele nunca vê dados não comprometidos ou alterações comprometidas por transações concorrentes durante a execução da transação. (No entanto, cada consulta vê os efeitos das atualizações anteriores executadas dentro de sua própria transação, mesmo que ainda não estejam comprometidas.) Esta é uma garantia mais forte do que a exigida pelo padrão SQL para este nível de isolamento, e previne todos os fenômenos descritos em [Tabela 13.1] ((transaction-iso.md#MVCC-ISOLEVEL-TABLE "Table 13.1. Transaction Isolation Levels")) exceto as anomalias de serialização. Como mencionado acima, isso é especificamente permitido pelo padrão, que descreve apenas as *mínimas* proteções que cada nível de isolamento deve fornecer.

Este nível é diferente de Read Committed porque uma consulta em uma transação de leitura repetitiva vê um instantâneo a partir do início do primeiro enunciado que não controla o transação no *transação*, e não a partir do início do enunciado atual dentro da transação. Assim, os comandos consecutivos `SELECT` dentro de uma *única* transação veem os mesmos dados, ou seja, eles não veem as alterações feitas por outras transações que se comprometem após o início da própria transação.

As aplicações que utilizam esse nível devem estar preparadas para repetir as transações devido a falhas de serialização.

Os comandos `UPDATE`, `DELETE`, `MERGE`, `SELECT FOR UPDATE` e `SELECT FOR SHARE` se comportam da mesma forma que o `SELECT` em termos de busca de linhas-alvo: eles só encontrarão linhas-alvo que foram comprometidas a partir do horário de início da transação. No entanto, uma tal linha-alvo já pode ter sido atualizada (ou excluída ou bloqueada) por outra transação concorrente no momento em que é encontrada. Neste caso, a transação de leitura repetitiva aguardará o primeiro compromisso ou o retorno (se ainda estiver em andamento) da transação atualizadora. Se o primeiro atualizador retornar, então seus efeitos serão negados e a transação de leitura repetitiva pode prosseguir com a atualização da linha originalmente encontrada. Mas se o primeiro atualizador compromet (e de fato atualizou ou excluiu a linha, não apenas a bloqueou) então a transação de leitura repetitiva será revertida com a mensagem

```
ERROR:  could not serialize access due to concurrent update
```

porque uma transação de leitura repetida não pode modificar ou bloquear linhas alteradas por outras transações após a transação de leitura repetida ter começado.

Quando um aplicativo recebe essa mensagem de erro, ele deve abortar a transação atual e tentar novamente a transação inteira desde o início. A segunda vez, a transação verá a alteração previamente comprometida como parte de sua visão inicial do banco de dados, portanto, não há conflito lógico em usar a nova versão da linha como ponto de partida para a atualização da nova transação.

Observe que apenas as transações atualizadas podem precisar ser refeitas; as transações somente de leitura nunca terão conflitos de serialização.

O modo de leitura repetida oferece uma garantia rigorosa de que cada transação vê uma visão completamente estável do banco de dados. No entanto, essa visão não será necessariamente sempre consistente com a execução serial (uma de cada vez) de transações concorrentes do mesmo nível. Por exemplo, mesmo uma transação apenas de leitura neste nível pode ver um registro de controle atualizado para mostrar que um lote foi completado, mas *não* ver um dos registros de detalhe que são logicamente parte do lote, porque leu uma revisão anterior do registro de controle. Tentativas de impor regras de negócios por transações que executam este nível de isolamento provavelmente não funcionarão corretamente sem o uso cuidadoso de bloqueios explícitos para bloquear transações conflitantes.

O nível de isolamento de leitura repetida é implementado usando uma técnica conhecida na literatura acadêmica de banco de dados e em alguns outros produtos de banco de dados como *Snapshot Isolation*. Diferenças de comportamento e desempenho podem ser observadas quando comparadas com sistemas que utilizam uma técnica de bloqueio tradicional que reduz a concorrência. Alguns outros sistemas podem até oferecer Leitura Repetida e Snapshot Isolation como níveis de isolamento distintos com comportamento diferente. Os fenômenos permitidos que distinguem as duas técnicas não foram formalizados pelos pesquisadores de banco de dados até após o desenvolvimento do padrão SQL, e estão fora do escopo deste manual. Para um tratamento completo, consulte [[berenson95]](biblio.md#BERENSON95).

### Nota

Antes da versão 9.1 do PostgreSQL, um pedido para o nível de isolamento de transação Serializable fornecia exatamente o mesmo comportamento descrito aqui. Para manter o comportamento Serializable herdado, o Repeatable Read deve ser solicitado agora.

### 13.2.3. Nível de isolamento serializável [#](#XACT-SERIALIZABLE)

O nível de isolamento *Serializable* oferece o isolamento de transação mais rigoroso. Este nível emula a execução serial de transações para todas as transações comprometidas; como se as transações tivessem sido executadas uma após a outra, seriamente, em vez de concorrentemente. No entanto, como o nível de leitura repetida, as aplicações que usam este nível devem estar preparadas para repetir as transações devido a falhas de serialização. De fato, este nível de isolamento funciona exatamente da mesma forma que o de leitura repetida, exceto que também monitora condições que poderiam fazer com que a execução de um conjunto concorrente de transações serializáveis se comporte de uma maneira inconsistente com todas as possíveis execuções seriadas (uma de cada vez) dessas transações. Esse monitoramento não introduz bloqueio além do presente na leitura repetida, mas há algum custo de monitoramento, e a detecção das condições que poderiam causar uma *anomalia de serialização* acionará uma *falha de serialização*.

Como exemplo, considere uma tabela `mytab`, inicialmente contendo:

```
 class | value
-------+-------
     1 |    10
     1 |    20
     2 |   100
     2 |   200
```

Suponha que a transação serializável A calcule:

```
SELECT SUM(value) FROM mytab WHERE class = 1;
```

e, em seguida, insere o resultado (30) como `value` em uma nova linha com `class` `= 2`. Concomitantemente, a transação serializável B calcula:

```
SELECT SUM(value) FROM mytab WHERE class = 2;
```

e obtém o resultado 300, que ele insere em uma nova linha com `class` `= 1`. Então, ambas as transações tentam confirmar. Se uma das transações estivesse em execução no nível de isolamento de leitura repetida, ambas seriam permitidas para confirmar; mas, como não há ordem serial de execução consistente com o resultado, usando transações serializáveis, uma transação poderá confirmar e a outra será revertida com esta mensagem:

```
ERROR:  could not serialize access due to read/write dependencies among transactions
```

Isso ocorre porque, se A tivesse executado antes de B, B teria calculado a soma de 330, não de 300, e da mesma forma, o outro pedido resultaria em uma soma diferente calculada por A.

Ao confiar em transações Serializable para prevenir anomalias, é importante que quaisquer dados lidos de uma tabela de usuário permanente não sejam considerados válidos até que a transação que os leu tenha sido comprometida com sucesso. Isso é verdade mesmo para transações somente de leitura, exceto que dados lidos dentro de uma *deferível* transação somente de leitura são conhecidos como válidos assim que são lidos, porque tal transação espera até que possa adquirir um instantâneo garantido estar livre de tais problemas antes de começar a ler quaisquer dados. Em todos os outros casos, as aplicações não devem depender dos resultados lidos durante uma transação que é posteriormente abortada; em vez disso, elas devem tentar novamente a transação até que ela seja bem-sucedida.

Para garantir a serializabilidade verdadeira, o PostgreSQL utiliza o *bloqueio de predicado*, o que significa que ele mantém blocos que lhe permitem determinar quando uma escrita teria tido impacto no resultado de uma leitura anterior de uma transação concorrente, se tivesse sido executada primeiro. No PostgreSQL, esses blocos não causam bloqueio e, portanto, *não* podem desempenhar qualquer papel na ocorrência de um impasse. Eles são usados para identificar e marcar dependências entre transações serializáveis concorrentes que, em certas combinações, podem levar a anomalias de serialização. Em contraste, uma transação com compromisso de leitura ou leitura repetida que deseja garantir a consistência dos dados pode precisar retirar um bloqueio de uma tabela inteira, o que poderia bloquear outros usuários que tentam usar essa tabela, ou pode usar `SELECT FOR UPDATE` ou `SELECT FOR SHARE`, que não apenas podem bloquear outras transações, mas causar acesso ao disco.

As bloqueadoras de predicado no PostgreSQL, como na maioria dos outros sistemas de banco de dados, são baseadas nos dados realmente acessados por uma transação. Essas aparecerão na visão do sistema `pg_locks`(view-pg-locks.md "53.13. pg_locks") com um `mode` de `SIReadLock`. Os bloqueios específicos adquiridos durante a execução de uma consulta dependerão do plano usado pela consulta, e múltiplos bloqueios mais detalhados (por exemplo, bloqueios de tupla) podem ser combinados em menos bloqueios mais grosseiros (por exemplo, bloqueios de página) durante o curso da transação para evitar o esgotamento da memória usada para rastrear os bloqueios. Uma transação `READ ONLY` pode ser capaz de liberar suas bloqueadoras SIRead antes da conclusão, se detectar que ainda não podem ocorrer conflitos que poderiam levar a uma anomalia de serialização. De fato, as transações `READ ONLY` muitas vezes serão capazes de estabelecer esse fato no início e evitar a tomada de quaisquer bloqueios de predicado. Se você solicitar explicitamente uma transação `SERIALIZABLE READ ONLY DEFERRABLE`, ela bloqueará até que possa estabelecer esse fato. (Este é o *único* caso em que as transações Serializable bloqueiam, mas as transações Repeatable Read não fazem isso.) Por outro lado, os bloqueios SIRead muitas vezes precisam ser mantidos após o compromisso da transação, até que as transações de escrita e leitura que se sobrepõem sejam concluídas.

O uso consistente de transações serializáveis pode simplificar o desenvolvimento. A garantia de que qualquer conjunto de transações concorrentes serializáveis que tenham sido executadas com sucesso terá o mesmo efeito como se fossem executadas uma de cada vez significa que, se você puder demonstrar que uma única transação, conforme escrita, fará a coisa certa quando executada por si mesma, você pode ter confiança de que ela fará a coisa certa em qualquer combinação de transações serializáveis, mesmo sem qualquer informação sobre o que essas outras transações podem fazer, ou ela não se comprometerá com sucesso. É importante que um ambiente que use essa técnica tenha uma maneira generalizada de lidar com falhas de serialização (que sempre retornam com um valor SQLSTATE de '40001'), porque será muito difícil prever exatamente quais transações podem contribuir para as dependências de leitura/escrita e precisam ser revertidas para prevenir anomalias de serialização. O monitoramento das dependências de leitura/escrita tem um custo, assim como o reinício das transações que são terminadas com uma falha de serialização, mas equilibrado em relação ao custo e ao bloqueio envolvidos no uso de bloqueios explícitos e `SELECT FOR UPDATE` ou `SELECT FOR SHARE`, as transações serializáveis são a melhor escolha de desempenho para alguns ambientes.

Embora o nível de isolamento de transação Serializable do PostgreSQL permita que as transações concorrentes se comprovem se puderem provar que há uma ordem serial de execução que produziria o mesmo efeito, ele nem sempre impede que erros sejam gerados que não ocorreriam em uma execução serial verdadeira. Em particular, é possível observar violações de restrições únicas causadas por conflitos com transações Serializable que se sobrepõem, mesmo após verificar explicitamente que a chave não está presente antes de tentar inseri-la. Isso pode ser evitado garantindo que *todas* as transações Serializable que inserem chaves potencialmente conflitantes verificem explicitamente se podem fazê-lo primeiro. Por exemplo, imagine um aplicativo que pede ao usuário uma nova chave e depois verifica se ela não existe já, tentando selecioná-la primeiro, ou gera uma nova chave selecionando a chave máxima existente e adicionando uma. Se algumas transações Serializable inserirem novas chaves diretamente sem seguir esse protocolo, violações de restrições únicas podem ser relatadas mesmo em casos em que elas não poderiam ocorrer em uma execução serial das transações concorrentes.

Para obter um desempenho ótimo quando se utiliza transações serializáveis para controle de concorrência, é importante considerar esses problemas:

* Declare as transações como `READ ONLY` quando possível.
* Controle o número de conexões ativas, usando um pool de conexões, se necessário. Isso é sempre uma consideração importante de desempenho, mas pode ser particularmente importante em um sistema ocupado que usa transações serializáveis.
* Não coloque mais em uma única transação do que o necessário para fins de integridade.
* Não deixe as conexões pendentes "inativas na transação" por mais tempo do que o necessário. O parâmetro de configuração [idle_in_transaction_session_timeout](runtime-config-client.md#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT) pode ser usado para desconectar automaticamente as sessões que persistem.
* Elimine as bloqueadoras explícitas, `SELECT FOR UPDATE` e `SELECT FOR SHARE`, quando não forem mais necessárias devido às proteções fornecidas automaticamente pelas transações serializáveis.
* Quando o sistema é forçado a combinar várias bloqueadoras de predicado de nível de página em uma única bloqueadora de predicado de nível de relação, porque a tabela de bloqueadora de predicado está sem memória, pode ocorrer um aumento na taxa de falhas de serialização. Você pode evitar isso aumentando [max_pred_locks_per_transaction](runtime-config-locks.md#GUC-MAX-PRED-LOCKS-PER-TRANSACTION), [max_pred_locks_per_relation](runtime-config-locks.md#GUC-MAX-PRED-LOCKS-PER-RELATION) e/ou [max_pred_locks_per_page](runtime-config-locks.md#GUC-MAX-PRED-LOCKS-PER-PAGE).
* Uma varredura sequencial sempre exigirá uma bloqueadora de predicado de nível de relação. Isso pode resultar em um aumento na taxa de falhas de serialização. Pode ser útil incentivar o uso de varreduras de índice, reduzindo [random_page_cost](runtime-config-query.md#GUC-RANDOM-PAGE-COST) e/ou aumentando [cpu_tuple_cost](runtime-config-query.md#GUC-CPU-TUPLE-COST). Certifique-se de pesar qualquer diminuição nos rollback e reinício das transações contra qualquer mudança geral no tempo de execução da consulta.

O nível de isolamento Serializable é implementado usando uma técnica conhecida na literatura acadêmica sobre bancos de dados como Isolamento de Escaneamento Serializável, que se baseia no Isolamento de Escaneamento, adicionando verificações para anomalias de serialização. Algumas diferenças de comportamento e desempenho podem ser observadas quando comparado com outros sistemas que utilizam uma técnica de bloqueio tradicional. Consulte [[ports12]](biblio.md#PORTS12) para informações detalhadas.