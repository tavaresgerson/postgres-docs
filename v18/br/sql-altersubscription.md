## ALTERAR ABONAMENTO

ALTERAR SUBSCRIPÇÃO — alterar a definição de uma assinatura

## Sinopse

```
ALTER SUBSCRIPTION name CONNECTION 'conninfo'
ALTER SUBSCRIPTION name SET PUBLICATION publication_name [, ...] [ WITH ( publication_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name ADD PUBLICATION publication_name [, ...] [ WITH ( publication_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name DROP PUBLICATION publication_name [, ...] [ WITH ( publication_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name REFRESH PUBLICATION [ WITH ( refresh_option [= value] [, ... ] ) ]
ALTER SUBSCRIPTION name ENABLE
ALTER SUBSCRIPTION name DISABLE
ALTER SUBSCRIPTION name SET ( subscription_parameter [= value] [, ... ] )
ALTER SUBSCRIPTION name SKIP ( skip_option = value )
ALTER SUBSCRIPTION name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER SUBSCRIPTION name RENAME TO new_name
```

## Descrição

`ALTER SUBSCRIPTION` pode alterar a maioria das propriedades de assinatura que podem ser especificadas em [CREATE SUBSCRIPTION](sql-createsubscription.md "CREATE SUBSCRIPTION").

Você deve possuir a assinatura para usar `ALTER SUBSCRIPTION`. Para renomear uma assinatura ou alterar o proprietário, você deve ter permissão `CREATE` no banco de dados. Além disso, para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário. Se a assinatura tiver `password_required=false`, apenas superusuários podem modificá-la.

Ao atualizar uma publicação, removemos as relações que não fazem mais parte da publicação e também removemos os intervalos de sincronização de tabela, se houver algum. É necessário remover esses intervalos para que os recursos alocados para a assinatura no host remoto sejam liberados. Se, devido a uma falha na rede ou a algum outro erro, o PostgreSQL não conseguir remover os intervalos, um erro será relatado. Para prosseguir nessa situação, o usuário precisa ou repetir a operação ou desassociar o intervalo da assinatura e descartar a assinatura, conforme explicado em [DROP SUBSCRIPTION][(sql-dropsubscription.md "DROP SUBSCRIPTION")].

Os comandos `ALTER SUBSCRIPTION ... REFRESH PUBLICATION`, `ALTER SUBSCRIPTION ... {SET|ADD|DROP} PUBLICATION ...` com a opção `refresh` como `true`, `ALTER SUBSCRIPTION ... SET (failover = true|false)` e `ALTER SUBSCRIPTION ... SET (two_phase = false)` não podem ser executados dentro de um bloco de transação.

Os comandos `ALTER SUBSCRIPTION ... REFRESH PUBLICATION` e `ALTER SUBSCRIPTION ... {SET|ADD|DROP} PUBLICATION ...` com a opção `refresh` como `true` também não podem ser executados quando a subscrição tem o compromisso [`two_phase`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE) habilitado, a menos que [`copy_data`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-COPY-DATA)]] seja `false`. Veja a coluna `subtwophasestate` de [`pg_subscription`(catalog-pg-subscription.md "52.54. pg_subscription") para saber o estado real de duas fases.

## Parâmetros

*`name`* [#](#SQL-ALTERSUBSCRIPTION-PARAMS-NAME): O nome de uma assinatura cujas propriedades devem ser alteradas.

`CONNECTION 'conninfo'` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-CONNECTION): Esta cláusula substitui a cadeia de conexão originalmente definida por [CREATE SUBSCRIPTION](sql-createsubscription.md "CREATE SUBSCRIPTION"). Veja mais informações lá.

`SET PUBLICATION publication_name` `ADD PUBLICATION publication_name` `DROP PUBLICATION publication_name` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-SETADDDROP-PUBLICATION): Esses formulários alteram a lista de publicações assinadas. `SET` substitui toda a lista de publicações por uma nova lista, `ADD` adiciona publicações adicionais à lista de publicações e `DROP` remove as publicações da lista de publicações. Permitimos que publicações não existentes sejam especificadas em `ADD` e `SET` variantes para que os usuários possam adicioná-las mais tarde. Consulte [CREATE SUBSCRIPTION](sql-createsubscription.md "CREATE SUBSCRIPTION") para obter mais informações. Por padrão, este comando também atuará como `REFRESH PUBLICATION`.

*`publication_option`* especifica opções adicionais para esta operação. As opções suportadas são:

`refresh` (`boolean`) :   Quando falso, o comando não tentará atualizar as informações da tabela. O `REFRESH PUBLICATION` deve ser executado separadamente. O padrão é `true`.

Adicionalmente, as opções descritas em `REFRESH PUBLICATION` podem ser especificadas para controlar a operação de atualização implícita.

`REFRESH PUBLICATION` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-REFRESH-PUBLICATION): Pegar informações de tabela faltantes do editor. Isso iniciará a replicação de tabelas que foram adicionadas às publicações subscritas desde [[`CREATE SUBSCRIPTION`]](sql-createsubscription.md "CREATE SUBSCRIPTION") ou da última invocação de `REFRESH PUBLICATION`.

*`refresh_option`* especifica opções adicionais para a operação de atualização. As opções suportadas são:

`copy_data` (`boolean`) : Especifica se os dados pré-existentes nas publicações que estão sendo assinadas devem ser copiados quando a replicação começar. O padrão é `true`.

As tabelas previamente subscritas não são copiadas, mesmo que a cláusula de filtro de linha de uma tabela `WHERE` tenha sido modificada desde então.

Veja [Notas][(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-NOTES "Notes")] para obter detalhes sobre como o `copy_data = true` pode interagir com o parâmetro [`origin`][(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-ORIGIN)].

Consulte o parâmetro `binary` (sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-BINARY) de `CREATE SUBSCRIPTION` para obter detalhes sobre a cópia de dados pré-existentes em formato binário.

`ENABLE` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-ENABLE): Habilita uma assinatura anteriormente desativada, iniciando o trabalhador de replicação lógica no final da transação.

`DISABLE` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE): Desabilita uma assinatura em execução, parando o trabalhador de replicação lógica no final da transação.

`SET ( subscription_parameter [= value] [, ... ] )` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-SET): Esta cláusula altera parâmetros originalmente definidos por [CREATE SUBSCRIPTION](sql-createsubscription.md "CREATE SUBSCRIPTION"). Veja lá para mais informações. Os parâmetros que podem ser alterados são [`slot_name`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-SLOT-NAME), [`synchronous_commit`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-SYNCHRONOUS-COMMIT), [`binary`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-BINARY), [`streaming`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-STREAMING), [`disable_on_error`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-DISABLE-ON-ERROR), [`password_required`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-PASSWORD-REQUIRED), [`run_as_owner`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-RUN-AS-OWNER), [`origin`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-ORIGIN), [`failover`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER), e [`two_phase`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE)]. Apenas um superusuário pode definir `password_required = false`.

Ao alterar os valores das propriedades `slot_name`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-SLOT-NAME), `failover` e `two_phase` do slot nomeado, os parâmetros correspondentes `failover`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER) e `two_phase`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE) especificados na assinatura podem diferir. Ao criar o slot, certifique-se de que as propriedades do slot `failover` e `two_phase` correspondam aos seus parâmetros correspondentes da assinatura. Caso contrário, o slot no editor pode se comportar de maneira diferente do que essas opções de assinatura dizem: por exemplo, o slot no editor pode ser sincronizado com os stand-by mesmo quando a opção [`failover`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER) da assinatura é desativada ou pode ser desativado para sincronização mesmo quando a opção [`failover`](sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER) da assinatura é habilitada.

Os parâmetros `failover`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER) e `two_phase`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE) só podem ser alterados quando a assinatura é desativada.

Ao alterar `two_phase` de (sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE) para `false`, o processo de backend reporta um erro se forem encontradas quaisquer transações preparadas feitas pelo trabalhador de replicação lógica (desde que o parâmetro `two_phase` ainda estivesse em `true`). Você pode resolver as transações preparadas no nó do publicador ou desfazê-las manualmente no assinante, e então tentar novamente. As transações preparadas pelo trabalhador de replicação lógica correspondentes a uma assinatura específica têm o seguinte padrão: “`pg_gid_%u_%u`” (parâmetros: assinatura *`oid`*, ID de transação remota *`xid`*). Para resolver manualmente tais transações, é necessário desfazer todas as transações preparadas com IDs de assinatura correspondentes em seus nomes. As aplicações podem verificar [`pg_prepared_xacts`](view-pg-prepared-xacts.md "53.17. pg_prepared_xacts") para encontrar as transações preparadas necessárias. Após a opção `two_phase` ser alterada de `true` para `false`, o publicador irá replicar as transações novamente quando elas forem comprometidas.

`SKIP ( skip_option = value )` [#](#SQL-ALTERSUBSCRIPTION-PARAMS-SKIP): Ignora a aplicação de todas as alterações da transação remota. Se os dados recebidos violam quaisquer restrições, a replicação lógica será interrompida até que seja resolvida. Ao usar o comando `ALTER SUBSCRIPTION ... SKIP`, o trabalhador de replicação lógica ignora todas as alterações de modificação de dados dentro da transação. Esta opção não tem efeito nas transações que já estão preparadas ao habilitar [`two_phase`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE) no assinante. Após o trabalhador de replicação lógica ter ignorado com sucesso a transação ou terminado uma transação, o LSN (armazenado em `pg_subscription`.`subskiplsn`) é limpo. Consulte [Seção 29.7](logical-replication-conflicts.md "29.7. Conflicts") para os detalhes dos conflitos de replicação lógica.

*`skip_option`* especifica as opções para esta operação. A opção compatível é:

`lsn` (`pg_lsn`) : Especifica o LSN de término da transação remota cujas alterações devem ser ignoradas pelo trabalhador de replicação lógica. O LSN de término é o LSN no qual a transação é comprometida ou preparada. Não é suportada a supressão de subtransações individuais. Definir `NONE` refaz o LSN.

*`new_owner`* [#](#SQL-ALTERSUBSCRIPTION-PARAMS-NEW-OWNER): O nome do usuário do novo proprietário da assinatura.

*`new_name`* [#](#SQL-ALTERSUBSCRIPTION-PARAMS-NEW-NAME): O novo nome da assinatura.

Ao especificar um parâmetro do tipo `boolean`, a parte *`value`* do `=` pode ser omitida, o que é equivalente a especificar `TRUE`.

## Exemplos

Altere a publicação assinada por uma assinatura para `insert_only`:

```
ALTER SUBSCRIPTION mysub SET PUBLICATION insert_only;
```

Desative (pare) a assinatura:

```
ALTER SUBSCRIPTION mysub DISABLE;
```

## Compatibilidade

`ALTER SUBSCRIPTION` é uma extensão do PostgreSQL.

## Veja também

[Crie Assinatura](sql-createsubscription.md "CREATE SUBSCRIPTION"), [Retire Assinatura](sql-dropsubscription.md "DROP SUBSCRIPTION"), [Crie Publicação](sql-createpublication.md "CREATE PUBLICATION"), [Altere Publicação](sql-alterpublication.md "ALTER PUBLICATION")