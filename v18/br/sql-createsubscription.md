## Crie uma assinatura

Crie uma assinatura — defina uma nova assinatura

## Sinopse

```
CREATE SUBSCRIPTION subscription_name
    CONNECTION 'conninfo'
    PUBLICATION publication_name [, ...]
    [ WITH ( subscription_parameter [= value] [, ... ] ) ]
```

## Descrição

`CREATE SUBSCRIPTION` adiciona uma nova assinatura de replicação lógica. O usuário que cria uma assinatura torna-se o proprietário da assinatura. O nome da assinatura deve ser distinto do nome de qualquer assinatura existente no banco de dados atual.

Uma assinatura representa uma conexão de replicação com o editor. Portanto, além de adicionar definições nos catálogos locais, este comando normalmente cria um slot de replicação no editor.

Será iniciado um trabalhador de replicação lógica para replicar dados para a nova assinatura no momento do commit da transação em que este comando é executado, a menos que a assinatura seja inicialmente desativada.

Para criar uma assinatura, você deve ter os privilégios do papel `pg_create_subscription`, bem como os privilégios `CREATE` no banco de dados atual.

Informações adicionais sobre assinaturas e replicação lógica como um todo estão disponíveis em [Seção 29.2][(logical-replication-subscription.md "29.2. Subscription")] e [Capítulo 29][(logical-replication.md "Chapter 29. Logical Replication")].

## Parâmetros

*`subscription_name`* [#](#SQL-CREATESUBSCRIPTION-PARAMS-NAME): O nome da nova assinatura.

`CONNECTION 'conninfo'` [#](#SQL-CREATESUBSCRIPTION-PARAMS-CONNECTION): A cadeia de conexão libpq que define como se conectar ao banco de dados do editor. Para detalhes, consulte [Seção 32.1.1](libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings").

`PUBLICATION publication_name [, ...]` [#](#SQL-CREATESUBSCRIPTION-PARAMS-PUBLICATION): Nomes das publicações do editor para se inscrever.

`WITH ( subscription_parameter [= value] [, ... ] )` [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH): Esta cláusula especifica parâmetros opcionais para uma assinatura.

Os seguintes parâmetros controlam o que acontece durante a criação da assinatura:

`connect` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-CONNECT) : Especifica se o comando `CREATE SUBSCRIPTION` deve se conectar ao editora. O padrão é `true`. Definir isso como `false` fará com que os valores de `create_slot`, `enabled` e `copy_data` sejam `false`. (Você não pode combinar a definição de `connect` como `false` com a definição de `create_slot`, `enabled` ou `copy_data` como `true`.).

Como não há conexão quando esta opção é `false`, nenhuma tabela é assinada. Para iniciar a replicação, você deve criar manualmente o slot de replicação, habilitar o failover, se necessário, habilitar a assinatura e atualizar a assinatura. Consulte [Seção 29.2.3][(logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT "29.2.3. Examples: Deferred Replication Slot Creation")] para exemplos.

`create_slot` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-CREATE-SLOT) : Especifica se o comando deve criar o slot de replicação no publicador. O padrão é `true`.

Se configurado como `false`, você é responsável por criar a posição do editor de alguma outra forma. Consulte [Seção 29.2.3][(logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT "29.2.3. Examples: Deferred Replication Slot Creation")] para exemplos.

`enabled` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-ENABLED) : Especifica se a assinatura deve ser replicada ativamente ou se deve apenas ser configurada, mas ainda não iniciada. O padrão é `true`.

`slot_name` (`string`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-SLOT-NAME) : Nome do slot de replicação do editor a ser utilizado. O padrão é utilizar o nome da assinatura para o nome do slot.

Definir `slot_name` para `NONE` significa que não haverá um slot de replicação associado à assinatura. Essas assinaturas também devem ter os valores de `enabled` e `create_slot` definidos para `false`. Use isso quando você irá criar o slot de replicação manualmente posteriormente. Consulte [Seção 29.2.3][(logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT "29.2.3. Examples: Deferred Replication Slot Creation")] para exemplos.

Ao definir `slot_name` para um nome válido e `create_slot` para `false`, o valor da propriedade `failover` do slot nomeado pode diferir do parâmetro correspondente `failover` especificado na assinatura. Sempre certifique-se de que a propriedade do slot `failover` corresponda ao parâmetro correspondente da assinatura e vice-versa. Caso contrário, o slot no publicador pode se comportar de maneira diferente do que essas opções de assinatura dizem: por exemplo, o slot no publicador pode ser sincronizado com os stand-by mesmo quando a opção `failover` da assinatura está desativada ou pode ser desativado para sincronização mesmo quando a opção `failover` da assinatura está habilitada.

Os seguintes parâmetros controlam o comportamento de replicação da assinatura após ela ter sido criada:

`binary` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-BINARY) :   Especifica se a assinatura solicitará que o editor envie os dados em formato binário (ao contrário do texto). O padrão é `false`. Qualquer cópia inicial de sincronização de tabela (ver `copy_data`) também utiliza o mesmo formato. O formato binário pode ser mais rápido que o formato de texto, mas é menos portátil em arquiteturas de máquina e versões do PostgreSQL. O formato binário é muito específico para o tipo de dado; por exemplo, não permitirá a cópia de uma coluna `smallint` para uma coluna `integer`, embora isso funcione bem no formato de texto. Mesmo quando esta opção está habilitada, apenas os tipos de dados que possuem funções de envio e recepção binárias serão transferidos em binário. Note que a sincronização inicial requer que todos os tipos de dados tenham funções de envio e recepção binárias, caso contrário, a sincronização falhará (ver [CREATE TYPE](sql-createtype.md "CREATE TYPE") para mais informações sobre funções de envio/recepção).

Ao realizar a replicação entre versões, pode acontecer de o editor ter uma função de envio binário para algum tipo de dado, mas o assinante não ter uma função de recebimento binário para esse tipo. Nesse caso, a transferência de dados falhará e a opção `binary` não poderá ser usada.

Se o editor for uma versão do PostgreSQL anterior à 16, então qualquer sincronização inicial de tabela usará o formato de texto mesmo se `binary = true`.

`copy_data` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-COPY-DATA) : Especifica se os dados pré-existentes nas publicações que estão sendo assinadas devem ser copiados quando a replicação começar. O padrão é `true`.

Se as publicações contiverem cláusulas `WHERE`, isso afetará os dados que serão copiados. Consulte as [Notas][(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-NOTES "Notes")] para obter detalhes.

Veja [Notas][(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-NOTES "Notes")] para obter detalhes sobre como o `copy_data = true` pode interagir com o parâmetro `origin`.

`streaming` (`enum`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-STREAMING) : Especifica se deve habilitar o streaming de transações em andamento para esta assinatura. O valor padrão é `parallel`, o que significa que as alterações recebidas são aplicadas diretamente por um dos trabalhadores de aplicação paralela, se disponível. Se nenhum trabalhador de aplicação paralela estiver disponível para lidar com transações de streaming, as alterações são escritas em arquivos temporários e aplicadas após a transação ser comprometida. Observe que, se ocorrer um erro em um trabalhador de aplicação paralela, o LSN de término da transação remota pode não ser relatado no log do servidor.

### Atenção

Há um risco de impasse quando os esquemas do publicador e do assinante diferem, embora tais casos sejam raros. O trabalhador aplicar está equipado para repetir essas transações automaticamente.

Se configurado como `on`, as alterações recebidas são escritas em arquivos temporários e aplicadas apenas após a transação ser confirmada no editor e recebida pelo assinante.

Se configurado como `off`, todas as transações são totalmente decodificadas no editor e só então enviadas ao assinante como um todo.

`synchronous_commit` (`enum`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-SYNCHRONOUS-COMMIT) :   O valor deste parâmetro substitui a configuração [synchronous_commit](runtime-config-wal.md#GUC-SYNCHRONOUS-COMMIT) nos processos de trabalho de aplicação desta assinatura. O valor padrão é `off`.

É seguro usar `off` para replicação lógica: Se o assinante perder transações devido à falta de sincronização, os dados serão enviados novamente pelo editor.

Um cenário diferente pode ser apropriado ao realizar replicação lógica síncrona. Os trabalhadores da replicação lógica relatam as posições de escrita e esvaziamento ao editor, e ao usar replicação síncrona, o editor irá esperar pelo esvaziamento real. Isso significa que definir `synchronous_commit` para o assinante para `off` quando a assinatura é usada para replicação síncrona pode aumentar a latência para `COMMIT` no editor. Neste cenário, pode ser vantajoso definir `synchronous_commit` para `local` ou superior.

`two_phase` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE) : Especifica se o compromisso de duas fases está habilitado para esta assinatura. O padrão é `false`.

Quando o commit de duas fases é habilitado, as transações preparadas são enviadas ao assinante no momento de `PREPARE TRANSACTION`, e são processadas como transações de duas fases também no assinante. Caso contrário, as transações preparadas são enviadas ao assinante apenas quando são comprometidas, e são então processadas imediatamente pelo assinante.

A implementação do commit em duas fases exige que a replicação tenha concluído com sucesso a fase inicial de sincronização da tabela. Portanto, mesmo quando `two_phase` está habilitado para uma assinatura, o estado interno em duas fases permanece temporariamente “pendente” até que a fase de inicialização seja concluída. Veja a coluna `subtwophasestate` de [`pg_subscription`](catalog-pg-subscription.md "52.54. pg_subscription") para saber o estado real em duas fases.

`disable_on_error` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-DISABLE-ON-ERROR) : Especifica se a assinatura deve ser desativada automaticamente se quaisquer erros forem detectados pelos trabalhadores da assinatura durante a replicação de dados do editor. O padrão é `false`.

`password_required` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-PASSWORD-REQUIRED) :   Se definido como `true`, as conexões com o editor feitas como resultado desta assinatura devem usar autenticação por senha e a senha deve ser especificada como parte da cadeia de conexão. Este ajuste é ignorado quando a assinatura é de propriedade de um superusuário. O padrão é `true`. Somente os superusuários podem definir este valor para `false`.

`run_as_owner` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-RUN-AS-OWNER) : Se verdadeiro, todas as ações de replicação são realizadas como o proprietário da assinatura. Se falso, os trabalhadores de replicação realizarão ações em cada tabela como o proprietário dessa tabela. Esta última configuração é geralmente muito mais segura; para detalhes, consulte [Seção 29.11](logical-replication-security.md "29.11. Security"). O padrão é `false`.

`origin` (`string`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-ORIGIN) :   Especifica se a assinatura solicitará que o editor envie apenas alterações que não tenham origem ou envie alterações independentemente da origem. Definir `origin` para `none` significa que a assinatura solicitará que o editor envie apenas alterações que não tenham origem. Definir `origin` para `any` significa que o editor envia alterações independentemente de sua origem. O padrão é `any`.

Veja [Notas][(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-NOTES "Notes")] para obter detalhes sobre como o `copy_data = true` pode interagir com o parâmetro `origin`.

`failover` (`boolean`) [#](#SQL-CREATESUBSCRIPTION-PARAMS-WITH-FAILOVER) : Especifica se os slots de replicação associados à assinatura estão habilitados para serem sincronizados com os backups, para que a replicação lógica possa ser retomada a partir do novo primário após o failover. O padrão é `false`.

Ao especificar um parâmetro do tipo `boolean`, a parte *`value`* do `=` pode ser omitida, o que é equivalente a especificar `TRUE`.

## Notas

Consulte a [Seção 29.11][(logical-replication-security.md "29.11. Security")] para obter detalhes sobre como configurar o controle de acesso entre a assinatura e a instância de publicação.

Ao criar um intervalo de replicação (o comportamento padrão), `CREATE SUBSCRIPTION` não pode ser executado dentro de um bloco de transação.

Criar uma assinatura que se conecte ao mesmo clúster de banco de dados (por exemplo, para replicar entre bancos de dados no mesmo clúster ou para replicar dentro do mesmo banco de dados) só terá sucesso se o intervalo de replicação não for criado como parte do mesmo comando. Caso contrário, a chamada `CREATE SUBSCRIPTION` ficará pendente. Para fazer isso funcionar, crie o intervalo de replicação separadamente (usando a função `pg_create_logical_replication_slot` com o nome do plugin `pgoutput`) e crie a assinatura usando o parâmetro `create_slot = false`. Veja [Seção 29.2.3][(logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES-DEFERRED-SLOT "29.2.3. Examples: Deferred Replication Slot Creation")] para exemplos. Esta é uma restrição de implementação que pode ser levantada em uma versão futura.

Se houver qualquer tabela na publicação com uma cláusula `WHERE`, as linhas para as quais o *`expression`* seja avaliado como `false` ou `NULL` não serão publicadas. Se a assinatura tiver várias publicações nas quais a mesma tabela foi publicada com diferentes cláusulas `WHERE`, uma linha será publicada se alguma das expressões (referindo a essa operação de publicação) for satisfeita. No caso de diferentes cláusulas `WHERE`, se uma das publicações não tiver nenhuma cláusula `WHERE` (referindo a essa operação de publicação) ou a publicação seja declarada como [`FOR ALL TABLES`](sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-ALL-TABLES) ou [`FOR TABLES IN SCHEMA`](sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLES-IN-SCHEMA), as linhas são sempre publicadas, independentemente da definição das outras expressões. Se o assinante for uma versão do PostgreSQL anterior à 15, então qualquer filtragem de linha é ignorada durante a fase inicial de sincronização de dados. Nesse caso, o usuário pode querer considerar a eliminação de qualquer dado inicialmente copiado que seria incompatível com o posterior filtro. Como a sincronização de dados inicial não leva em conta o parâmetro de publicação [`publish`](sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH) ao copiar dados de tabela existentes, algumas linhas podem ser copiadas que não seriam replicadas usando DML. Consulte [Seção 29.2.2](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES "29.2.2. Examples: Set Up Logical Replication") para exemplos.

As assinaturas que possuem várias publicações nas quais a mesma tabela foi publicada com diferentes listas de colunas não são suportadas.

Permitimos que publicações inexistentes sejam especificadas para que os usuários possam adicioná-las mais tarde. Isso significa que `pg_subscription` (catalog-pg-subscription.md "52.54. pg_subscription") pode ter publicações inexistentes.

Ao usar uma combinação de parâmetros de assinatura de `copy_data = true` e `origin = NONE`, os dados iniciais da tabela de sincronização são copiados diretamente do editor, o que significa que o conhecimento da verdadeira origem desses dados não é possível. Se o editor também tiver assinaturas, os dados copiados da tabela podem ter origem em níveis mais altos. Esse cenário é detectado e um ADVERTÊNCIA é registrado para o usuário, mas o aviso é apenas uma indicação de um problema potencial; é responsabilidade do usuário fazer as verificações necessárias para garantir que os dados copiados tenham realmente a origem desejada ou

Para descobrir quais tabelas podem potencialmente incluir origens não locais (devido a outras assinaturas criadas no editor), tente esta consulta SQL:

```
# substitute <pub-names> below with your publication name(s) to be queried
SELECT DISTINCT PT.schemaname, PT.tablename
FROM pg_publication_tables PT
     JOIN pg_class C ON (C.relname = PT.tablename)
     JOIN pg_namespace N ON (N.nspname = PT.schemaname),
     pg_subscription_rel PS
WHERE C.relnamespace = N.oid AND
      (PS.srrelid = C.oid OR
      C.oid IN (SELECT relid FROM pg_partition_ancestors(PS.srrelid) UNION
                SELECT relid FROM pg_partition_tree(PS.srrelid))) AND
      PT.pubname IN (<pub-names>);
```

## Exemplos

Crie uma assinatura para um servidor remoto que replique as tabelas nas publicações `mypublication` e `insert_only` e comece a replicar imediatamente no commit:

```
CREATE SUBSCRIPTION mysub
         CONNECTION 'host=192.168.1.50 port=5432 user=foo dbname=foodb'
        PUBLICATION mypublication, insert_only;
```

Crie uma assinatura para um servidor remoto que replique tabelas na publicação `insert_only` e que não comece a replicar até que seja habilitada posteriormente.

```
CREATE SUBSCRIPTION mysub
         CONNECTION 'host=192.168.1.50 port=5432 user=foo dbname=foodb'
        PUBLICATION insert_only
               WITH (enabled = false);
```

## Compatibilidade

`CREATE SUBSCRIPTION` é uma extensão do PostgreSQL.

## Veja também

[ALTERAR ABONAMENTO](sql-altersubscription.md "ALTER SUBSCRIPTION"), [DROP SUBSCRIPTION](sql-dropsubscription.md "DROP SUBSCRIPTION"), [CREATE PUBLICATION](sql-createpublication.md "CREATE PUBLICATION"), [ALTERAR PUBLICAÇÃO](sql-alterpublication.md "ALTER PUBLICATION")