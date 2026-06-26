## 53.13. `pg_locks` [#](#VIEW-PG-LOCKS)

A vista `pg_locks` fornece acesso a informações sobre as chaves de acesso mantidas por processos ativos dentro do servidor de banco de dados. Consulte o [Capítulo 13](mvcc.md) para mais discussão sobre bloqueio.

`pg_locks` contém uma linha por objeto ativo e bloquível, modo de bloqueio solicitado e processo relevante. Assim, o mesmo objeto bloquível pode aparecer várias vezes, se vários processos estiverem segurando ou aguardando blocos nele. No entanto, um objeto que atualmente não tenha blocos nele não aparecerá de forma alguma.

Existem vários tipos distintos de objetos que podem ser bloqueados: relações inteiras (por exemplo, tabelas), páginas individuais de relações, tuplas individuais de relações, IDs de transação (ambos IDs virtuais e permanentes) e objetos gerais do banco de dados (identificados por OID de classe e OID de objeto, da mesma forma que em `pg_description`(catalog-pg-description.md "52.19. pg_description") ou [`pg_depend`](catalog-pg-depend.md)). Além disso, o direito de estender uma relação é representado como um objeto separado que pode ser bloqueado, assim como o direito de atualizar `pg_database`.`datfrozenxid`. Além disso, bloqueios “conselhos” podem ser tomados em números que têm significados definidos pelo usuário.

**Tabela 53.13. Colunas `pg_locks`**



<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="catalog_table_entry">
    <p class="column_definition">
     Tipo de coluna
    </p>
    <p>
     Descrição
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      locktype
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Tipo do objeto que pode ser trancado:
     <code>
      relation
     </code>
     ,
     <code>
      extend
     </code>
     ,
     <code>
      frozenid
     </code>
     ,
     <code>
      page
     </code>
     ,
     <code>
      tuple
     </code>
     ,
     <code>
      transactionid
     </code>
     ,
     <code>
      virtualxid
     </code>
     ,
     <code>
      spectoken
     </code>
     ,
     <code>
      object
     </code>
     ,
     <code>
      userlock
     </code>
     ,
     <code>
      advisory
     </code>
     , ou
     <code>
      applytransaction
     </code>
     . (Veja também
     <a class="xref" href="monitoring-stats.md#WAIT-EVENT-LOCK-TABLE" title="Table 27.11. Wait Events of Type Lock">
      Tabela 27.11
     </a>
     .)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      database
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-database.md" title="52.15. pg_database">
      <code>
       pg_database
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     OID do banco de dados no qual o alvo de bloqueio existe, ou zero se o alvo for um objeto compartilhado, ou nulo se o alvo for um ID de transação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      relation
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code>
       pg_class
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     OID da relação alvo do bloqueio, ou nulo se o alvo não for uma relação ou parte de uma relação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      page
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Número da página alvo do bloqueio dentro da relação, ou nulo se o alvo não for uma página ou tupla da relação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      tuple
     </code>
     <code>
      int2
     </code>
    </p>
    <p>
     Número de tupla almejado pelo bloqueio dentro da página, ou nulo se o alvo não for uma tupla
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      virtualxid
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     ID virtual da transação alvo do bloqueio, ou nulo se o alvo não for um ID de transação virtual; veja
     <a class="xref" href="transactions.md" title="Chapter 67. Transaction Processing">
      Capítulo 67
     </a>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      transactionid
     </code>
     <code>
      xid
     </code>
    </p>
    <p>
     ID da transação alvo do bloqueio, ou nulo se o alvo não for um ID de transação;
     <a class="xref" href="transactions.md" title="Chapter 67. Transaction Processing">
      Capítulo 67
     </a>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      classid
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code>
       pg_class
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     OID do catálogo do sistema que contém o alvo de bloqueio, ou nulo se o alvo não for um objeto de banco de dados geral
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      objid
     </code>
     <code>
      oid
     </code>
     (referência a qualquer coluna OID)
    </p>
    <p>
     OID do alvo de bloqueio dentro do catálogo do sistema, ou nulo se o alvo não for um objeto de banco de dados geral
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      objsubid
     </code>
     <code>
      int2
     </code>
    </p>
    <p>
     Número da coluna almejada pelo bloqueio (o
     <code>
      classid
     </code>
     e
     <code>
      objid
     </code>
     se refere à própria tabela), ou zero se o alvo for algum outro objeto de banco de dados geral, ou nulo se o alvo não for um objeto de banco de dados geral
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      virtualtransaction
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     ID virtual da transação que está mantendo ou aguardando esse bloqueio
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      pid
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     ID do processo do servidor que detém ou aguarda esse bloqueio, ou nulo se o bloqueio for mantido por uma transação preparada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      mode
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Nome do modo de bloqueio mantido ou desejado por este processo (ver
     <a class="xref" href="explicit-locking.md#LOCKING-TABLES" title="13.3.1. Table-Level Locks">
      Seção 13.3.1
     </a>
     e
     <a class="xref" href="transaction-iso.md#XACT-SERIALIZABLE" title="13.2.3. Serializable Isolation Level">
      Seção 13.2.3
     </a>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      granted
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Verdadeiro se a trava é mantida, falso se a trava é aguardada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      fastpath
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Verdadeiro se o bloqueio foi feito por meio do caminho rápido, falso se feito por meio da tabela principal de bloqueio.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      waitstart
     </code>
     <code>
      timestamptz
     </code>
    </p>
    <p>
     O tempo em que o processo do servidor começou a esperar por esse bloqueio, ou nulo se o bloqueio estiver sendo mantido. Note que isso pode ser nulo por um período muito curto de tempo após o início da espera, mesmo que
     <code>
      granted
     </code>
     é
     <code>
      false
     </code>
     .
    </p>
   </td>
  </tr>
 </tbody>
</table>










`granted` é verdadeiro em uma linha que representa um bloqueio mantido pelo processo indicado. Falso indica que este processo está atualmente aguardando para adquirir este bloqueio, o que implica que pelo menos outro processo está segurando ou aguardando um modo de bloqueio conflitante no mesmo objeto bloqueável. O processo em espera dormirá até que o outro bloqueio seja liberado (ou até que uma situação de deadlock seja detectada). Um único processo pode estar aguardando para adquirir no máximo um bloqueio de cada vez.

Durante a execução de uma transação, um processo do servidor mantém um bloqueio exclusivo sobre o ID virtual da transação. Se uma ID permanente é atribuída à transação (o que normalmente acontece apenas se a transação alterar o estado do banco de dados), ela também mantém um bloqueio exclusivo sobre o ID permanente da transação até que ela termine. Quando um processo considera necessário esperar especificamente para que outra transação termine, ele faz isso tentando adquirir um bloqueio compartilhado sobre o ID da outra transação (seja o ID virtual ou permanente, dependendo da situação). Isso só será bem-sucedido quando a outra transação termina e libera seus bloqueios.

Embora os tuplos sejam um tipo de objeto com bloqueio, as informações sobre os bloqueios de nível de linha são armazenadas em disco, não na memória, e, portanto, os bloqueios de nível de linha normalmente não aparecem nessa visualização. Se um processo estiver aguardando um bloqueio de nível de linha, ele geralmente aparecerá na visualização como aguardando o ID de transação permanente do atual detentor desse bloqueio de linha.

Um bloqueio de inserção especulativo consiste em um ID de transação e um token de inserção especulativo. O token de inserção especulativo é exibido na coluna `objid`.

As chaves de bloqueio indicativo podem ser adquiridas em chaves que consistem em um único valor `bigint` ou em dois valores inteiros. Uma chave `bigint` é exibida com sua metade de ordem alta na coluna `classid`, sua metade de ordem baixa na coluna `objid`, e `objsubid` igual a 1. O valor original `bigint` pode ser remontado com a expressão `(classid::bigint << 32) | objid::bigint`. Chaves numéricas são exibidas com a primeira chave na coluna `classid`, a segunda chave na coluna `objid`, e `objsubid` igual a 2. O significado real das chaves cabe ao usuário. As chaves de bloqueio indicativo são locais para cada banco de dados, portanto, a coluna `database` é significativa para um bloqueio indicativo.

Os bloqueios de transação são aplicados no modo paralelo para aplicar a transação na replicação lógica. O ID de transação remota é exibido na coluna `transactionid`. O `objsubid` exibe o subtipo de bloqueio, que é 0 para o bloqueio usado para sincronizar o conjunto de alterações, e 1 para o bloqueio usado para esperar que a transação termine para garantir a ordem de comprometimento.

`pg_locks` oferece uma visão global de todos os bloqueios no clúster de bancos de dados, não apenas aqueles relevantes para o banco de dados atual. Embora sua coluna `relation` possa ser associada contra [`pg_class`](catalog-pg-class.md "52.11. pg_class").`oid` para identificar relações bloqueadas, isso só funcionará corretamente para relações no banco de dados atual (aqueles para os quais a coluna `database` é o OID do banco de dados atual ou zero).

A coluna `pid` pode ser associada à coluna `pid` da visão [`pg_stat_activity`](monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW) para obter mais informações sobre a sessão que está segurando ou aguardando cada bloqueio, por exemplo.

```
SELECT * FROM pg_locks pl LEFT JOIN pg_stat_activity psa
    ON pl.pid = psa.pid;
```

Além disso, se você estiver usando transações preparadas, a coluna `virtualtransaction` pode ser associada à coluna `transaction` da visão [`pg_prepared_xacts`](view-pg-prepared-xacts.md) para obter mais informações sobre transações preparadas que mantêm bloqueios. (Uma transação preparada nunca pode estar esperando por um bloqueio, mas continua mantendo os bloqueios que adquiriu enquanto estava em execução.) Por exemplo:

```
SELECT * FROM pg_locks pl LEFT JOIN pg_prepared_xacts ppx
    ON pl.virtualtransaction = '-1/' || ppx.transaction;
```

Embora seja possível obter informações sobre quais processos bloqueiam quais outros processos ao unir `pg_locks` contra si mesmo, isso é muito difícil de fazer com detalhes. Tal consulta teria que codificar o conhecimento sobre quais modos de bloqueio conflitam com quais outros. Pior ainda, a visão `pg_locks` não expõe informações sobre quais processos estão à frente de quais outros nas filas de espera de bloqueio, nem informações sobre quais processos são trabalhadores paralelos executando em nome de quais outras sessões de cliente. É melhor usar a função `pg_blocking_pids()` (ver [Tabela 9.71](functions-info.md#FUNCTIONS-INFO-SESSION-TABLE)) para identificar quais processos (s) um processo em espera está bloqueado atrás.

A visão `pg_locks` exibe dados tanto do gerente de bloqueio regular quanto do gerente de bloqueio preditivo, que são sistemas separados; além disso, o gerente de bloqueio regular subdivide seus blocos em blocos regulares e *fast-path*. Esses dados não são garantidos como totalmente consistentes. Quando a visão é consultada, os dados dos blocos fast-path (com `fastpath` = `true`) são coletados de cada backend um de cada vez, sem congelar o estado de todo o gerente de bloqueio, portanto, é possível que blocos sejam tomados ou liberados enquanto as informações são coletadas. No entanto, é importante notar que esses blocos não são conhecidos por conflitar com nenhum outro bloqueio atualmente em vigor. Após todas as backends terem sido consultadas quanto aos blocos fast-path, o restante do gerente de bloqueio regular é bloqueado como uma unidade, e um instantâneo consistente de todos os blocos restantes é coletado como uma ação atômica. Após desbloquear o gerente de bloqueio regular, o gerente de bloqueio preditivo é igualmente bloqueado e todos os blocos preditivos são coletados como uma ação atômica. Assim, com exceção dos blocos fast-path, cada gerente de bloqueio entregará um conjunto consistente de resultados, mas como não bloqueamos ambos os geradores de bloqueio simultaneamente, é possível que blocos sejam tomados ou liberados após interrogarmos o gerente de bloqueio regular e antes de interrogarmos o gerente de bloqueio preditivo.

A bloqueadora de bloqueio regular e/ou predatorial pode ter algum impacto no desempenho do banco de dados se essa visão for acessada com muita frequência. Os bloqueios são mantidos apenas pelo tempo mínimo necessário para obter dados dos gestores de bloqueio, mas isso não elimina completamente a possibilidade de um impacto no desempenho.