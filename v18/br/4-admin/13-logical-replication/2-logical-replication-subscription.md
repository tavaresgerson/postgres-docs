## 29.2. Assinatura [#](#LOGICAL-REPLICATION-SUBSCRIPTION)

* [29.2.1. Gerenciamento de Fendas de Replicação](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-SLOT)
* [29.2.2. Exemplos: Configuração de Replicação Lógica](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES)
* [29.2.3. Exemplos: Criação de Fenda de Replicação Adiada](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT)

Uma *subscrição* é o lado descendente da replicação lógica. O nó onde uma subscrição é definida é referido como o *assinante*. Uma subscrição define a conexão com outro banco de dados e o conjunto de publicações (uma ou mais) aos quais ela deseja se submeter.

O banco de dados de assinantes se comporta da mesma maneira que qualquer outra instância do PostgreSQL e pode ser usado como um publicador para outros bancos de dados, definindo suas próprias publicações.

Um nó de assinante pode ter múltiplas assinaturas, se desejar. É possível definir múltiplas assinaturas entre um único par de editor-assinante, e, nesse caso, é necessário ter cuidado para garantir que os objetos de publicação assinados não se sobreponham.

Cada assinatura receberá as alterações por meio de um intervalo de replicação (consulte [Seção 26.2.6](warm-standby.md#STREAMING-REPLICATION-SLOTS)). Pode ser necessário adicionar intervalos de replicação adicionais para a sincronização inicial dos dados pré-existentes da tabela e esses serão descartados no final da sincronização dos dados.

Uma assinatura de replicação lógica pode ser uma reserva para replicação síncrona (consulte [Seção 26.2.8](warm-standby.md#SYNCHRONOUS-REPLICATION)). O nome de reserva é, por padrão, o nome da assinatura. Um nome alternativo pode ser especificado como `application_name` nas informações de conexão da assinatura.

As assinaturas são descartadas pelo `pg_dump` se o usuário atual for um superusuário. Caso contrário, uma mensagem de alerta é escrita e as assinaturas são ignoradas, pois os usuários não superusuários não podem ler todas as informações das assinaturas do catálogo `pg_subscription`.

A assinatura é adicionada usando `CREATE SUBSCRIPTION` e pode ser interrompida/represa a qualquer momento usando o comando `ALTER SUBSCRIPTION` e removida usando `DROP SUBSCRIPTION` e (sql-dropsubscription.md "DROP SUBSCRIPTION").

Quando uma assinatura é cancelada e recriada, as informações de sincronização são perdidas. Isso significa que os dados precisam ser resincronizados posteriormente.

As definições do esquema não são replicadas, e as tabelas publicadas devem existir no assinante. Apenas tabelas regulares podem ser alvo de replicação. Por exemplo, você não pode replicar para uma visão.

As tabelas são correspondidas entre o editor e o assinante usando o nome da tabela totalmente qualificada. A replicação para tabelas com nomes diferentes no assinante não é suportada.

As colunas de uma tabela também são correspondidas pelo nome. A ordem das colunas na tabela do assinante não precisa corresponder à ordem do editor. Os tipos de dados das colunas não precisam corresponder, desde que a representação textual dos dados possa ser convertida para o tipo alvo. Por exemplo, você pode replicar de uma coluna do tipo `integer` para uma coluna do tipo `bigint`. A tabela alvo também pode ter colunas adicionais não fornecidas pela tabela publicada. Quaisquer colunas desse tipo serão preenchidas com o valor padrão conforme especificado na definição da tabela alvo. No entanto, a replicação lógica em formato binário é mais restritiva. Consulte a opção `binary`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-BINARY) de `CREATE SUBSCRIPTION` para detalhes.

### 29.2.1. Gerenciamento de Fissuras de Replicação [#](#LOGICAL-REPLICATION-SUBSCRIPTION-SLOT)

Como mencionado anteriormente, cada assinatura (ativa) recebe alterações de um intervalo de replicação do lado remoto (de publicação).

Os slots de sincronização de tabela adicionais são normalmente transitórios, criados internamente para realizar a sincronização inicial da tabela e descartados automaticamente quando não são mais necessários. Esses slots de sincronização de tabela têm nomes gerados: “`pg_%u_sync_%u_%llu`” (parâmetros: Subscrição *`oid`*, Tabela *`relid`*, identificador do sistema *`sysid`*)

Normalmente, a posição de replicação remota é criada automaticamente quando a assinatura é criada usando `CREATE SUBSCRIPTION` e é descartada automaticamente quando a assinatura é descartada usando `DROP SUBSCRIPTION`. No entanto, em algumas situações, pode ser útil ou necessário manipular a assinatura e a posição de replicação subjacente separadamente. Aqui estão alguns cenários:

* Ao criar uma assinatura, o slot de replicação já existe. Nesse caso, a assinatura pode ser criada usando a opção `create_slot = false` para associar-se ao slot existente.
* Ao criar uma assinatura, o host remoto não é acessível ou em um estado incerto. Nesse caso, a assinatura pode ser criada usando a opção `connect = false`. O host remoto não será contatado de forma alguma. É isso que o pg_dump usa. O slot de replicação remoto então deve ser criado manualmente antes que a assinatura possa ser ativada.
* Ao descartar uma assinatura, o slot de replicação deve ser mantido. Isso pode ser útil quando o banco de dados do assinante está sendo movido para um host diferente e será ativado a partir daí. Nesse caso, desassocie o slot da assinatura usando `ALTER SUBSCRIPTION`(sql-altersubscription.md "ALTER SUBSCRIPTION") antes de tentar descartar a assinatura.
* Ao descartar uma assinatura, o host remoto não é acessível. Nesse caso, desassocie o slot da assinatura usando `ALTER SUBSCRIPTION` antes de tentar descartar a assinatura. Se a instância do banco de dados remoto não existir mais, então nenhuma ação adicional é necessária. No entanto, se a instância do banco de dados remoto estiver apenas inacessível, o slot de replicação (e quaisquer slots de sincronização de tabela ainda restantes) deve então ser descartado manualmente; caso contrário, eles continuariam a reservar o WAL e eventualmente poderiam fazer com que o disco se encha. Esses casos devem ser investigados cuidadosamente.

### 29.2.2. Exemplos: Configuração da replicação lógica [#](#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES)

Crie algumas tabelas de teste no editor.

```
/* pub # */ CREATE TABLE t1(a int, b text, PRIMARY KEY(a));
/* pub # */ CREATE TABLE t2(c int, d text, PRIMARY KEY(c));
/* pub # */ CREATE TABLE t3(e int, f text, PRIMARY KEY(e));
```

Crie as mesmas tabelas no assinante.

```
/* sub # */ CREATE TABLE t1(a int, b text, PRIMARY KEY(a));
/* sub # */ CREATE TABLE t2(c int, d text, PRIMARY KEY(c));
/* sub # */ CREATE TABLE t3(e int, f text, PRIMARY KEY(e));
```

Insira dados nas tabelas do lado do editor.

```
/* pub # */ INSERT INTO t1 VALUES (1, 'one'), (2, 'two'), (3, 'three');
/* pub # */ INSERT INTO t2 VALUES (1, 'A'), (2, 'B'), (3, 'C');
/* pub # */ INSERT INTO t3 VALUES (1, 'i'), (2, 'ii'), (3, 'iii');
```

Crie publicações para as tabelas. As publicações `pub2` e `pub3a` não permitem algumas operações [`publish`](sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH)]. A publicação `pub3b` tem um filtro de linha (consulte [Seção 29.4](logical-replication-row-filter.md "29.4. Row Filters")).

```
/* pub # */ CREATE PUBLICATION pub1 FOR TABLE t1;
/* pub # */ CREATE PUBLICATION pub2 FOR TABLE t2 WITH (publish = 'truncate');
/* pub # */ CREATE PUBLICATION pub3a FOR TABLE t3 WITH (publish = 'truncate');
/* pub # */ CREATE PUBLICATION pub3b FOR TABLE t3 WHERE (e > 5);
```

Crie assinaturas para as publicações. A assinatura `sub3` se inscreve tanto em `pub3a` quanto em `pub3b`. Todas as assinaturas copiarão os dados iniciais por padrão.

```
/* sub # */ CREATE SUBSCRIPTION sub1
/* sub - */ CONNECTION 'host=localhost dbname=test_pub application_name=sub1'
/* sub - */ PUBLICATION pub1;
/* sub # */ CREATE SUBSCRIPTION sub2
/* sub - */ CONNECTION 'host=localhost dbname=test_pub application_name=sub2'
/* sub - */ PUBLICATION pub2;
/* sub # */ CREATE SUBSCRIPTION sub3
/* sub - */ CONNECTION 'host=localhost dbname=test_pub application_name=sub3'
/* sub - */ PUBLICATION pub3a, pub3b;
```

Observe que os dados iniciais da tabela são copiados, independentemente da operação `publish` da publicação.

```
/* sub # */ SELECT * FROM t1;
 a |   b
---+-------
 1 | one
 2 | two
 3 | three
(3 rows)

/* sub # */ SELECT * FROM t2;
 c | d
---+---
 1 | A
 2 | B
 3 | C
(3 rows)
```

Além disso, porque a cópia inicial dos dados ignora a operação `publish`, e porque a publicação `pub3a` não tem filtro de linha, isso significa que a tabela copiada `t3` contém todas as linhas, mesmo quando elas não correspondem ao filtro de linha da publicação `pub3b`.

```
/* sub # */ SELECT * FROM t3;
 e |  f
---+-----
 1 | i
 2 | ii
 3 | iii
(3 rows)
```

Insira mais dados nas tabelas do lado do editor.

```
/* pub # */ INSERT INTO t1 VALUES (4, 'four'), (5, 'five'), (6, 'six');
/* pub # */ INSERT INTO t2 VALUES (4, 'D'), (5, 'E'), (6, 'F');
/* pub # */ INSERT INTO t3 VALUES (4, 'iv'), (5, 'v'), (6, 'vi');
```

Agora, os dados do lado do editor parecem assim:

```
/* pub # */ SELECT * FROM t1;
 a |   b
---+-------
 1 | one
 2 | two
 3 | three
 4 | four
 5 | five
 6 | six
(6 rows)

/* pub # */ SELECT * FROM t2;
 c | d
---+---
 1 | A
 2 | B
 3 | C
 4 | D
 5 | E
 6 | F
(6 rows)

/* pub # */ SELECT * FROM t3;
 e |  f
---+-----
 1 | i
 2 | ii
 3 | iii
 4 | iv
 5 | v
 6 | vi
(6 rows)
```

Observe que, durante a replicação normal, as operações apropriadas do `publish` são usadas. Isso significa que as publicações `pub2` e `pub3a` não replicam o `INSERT`. Além disso, a publicação `pub3b` só replica dados que correspondem ao filtro de linha de `pub3b`. Agora, os dados do lado do assinante parecem assim:

```
/* sub # */ SELECT * FROM t1;
 a |   b
---+-------
 1 | one
 2 | two
 3 | three
 4 | four
 5 | five
 6 | six
(6 rows)

/* sub # */ SELECT * FROM t2;
 c | d
---+---
 1 | A
 2 | B
 3 | C
(3 rows)

/* sub # */ SELECT * FROM t3;
 e |  f
---+-----
 1 | i
 2 | ii
 3 | iii
 6 | vi
(4 rows)
```

### 29.2.3. Exemplos: Criação de intervalo de criação de replicação diferida [#](#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT)

Há alguns casos (por exemplo, [Seção 29.2.1](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-SLOT)) em que, se o slot de replicação remota não foi criado automaticamente, o usuário deve criá-lo manualmente antes que a assinatura possa ser ativada. As etapas para criar o slot e ativar a assinatura são mostradas nos exemplos a seguir. Esses exemplos especificam o plugin padrão de saída de decodificação lógica (`pgoutput`), que é o que a replicação lógica embutida usa.

Primeiro, crie uma publicação para os exemplos a serem usados.

```
/* pub # */ CREATE PUBLICATION pub1 FOR ALL TABLES;
```

Exemplo 1: Onde a assinatura diz `connect = false`

* Crie a assinatura.

```
  /* sub # */ CREATE SUBSCRIPTION sub1
  /* sub - */ CONNECTION 'host=localhost dbname=test_pub'
  /* sub - */ PUBLICATION pub1
  /* sub - */ WITH (connect=false);
  WARNING:  subscription was created, but is not connected
  HINT:  To initiate replication, you must manually create the replication slot, enable the subscription, and refresh the subscription.
```

* No assinante, complete a ativação da assinatura. Após isso, as tabelas de `pub1` começarão a se replicar.

```
/* sub # */ ALTER SUBSCRIPTION sub1 ENABLE;
/* sub # */ ALTER SUBSCRIPTION sub1 REFRESH PUBLICATION;
```

Exemplo 2: Onde a assinatura diz `connect = false`, mas também especifica a opção [`slot_name`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-SLOT-NAME).

* Crie a assinatura.

* Sobre o editor, crie manualmente um slot usando o mesmo nome que foi especificado durante `CREATE SUBSCRIPTION`, por exemplo, "myslot".

* No assinante, os passos restantes para a ativação da assinatura são os mesmos que antes.

```
/* sub # */ ALTER SUBSCRIPTION sub1 ENABLE;
/* sub # */ ALTER SUBSCRIPTION sub1 REFRESH PUBLICATION;
```

Exemplo 3: Onde a assinatura especifica `slot_name = NONE`

* Crie a assinatura. Quando `slot_name = NONE` é necessário também `enabled = false` e `create_slot = false`.

* Sobre o editor, crie manualmente um slot usando qualquer nome, por exemplo, "myslot".

* No assinante, associe a assinatura ao nome de fenda que acabou de ser criado.

* Os passos restantes para ativar a assinatura são os mesmos que antes.

```
/* sub # */ ALTER SUBSCRIPTION sub1 ENABLE;
/* sub # */ ALTER SUBSCRIPTION sub1 REFRESH PUBLICATION;
```
