## Crie publicação

Crie publicação — defina uma nova publicação

## Sinopse

```
CREATE PUBLICATION name
    [ FOR ALL TABLES
      | FOR publication_object [, ... ] ]
    [ WITH ( publication_parameter [= value] [, ... ] ) ]

where publication_object is one of:

    TABLE table_and_columns [, ... ]
    TABLES IN SCHEMA { schema_name | CURRENT_SCHEMA } [, ... ]

and table_and_columns is:

    [ ONLY ] table_name [ * ] [ ( column_name [, ... ] ) ] [ WHERE ( expression ) ]
```

## Descrição

`CREATE PUBLICATION` adiciona uma nova publicação ao banco de dados atual. O nome da publicação deve ser distinto do nome de qualquer publicação existente no banco de dados atual.

Uma publicação é, essencialmente, um grupo de tabelas cujos dados devem ser replicados por meio de replicação lógica. Consulte a [Seção 29.1] para obter detalhes sobre como as publicações se encaixam no conjunto de configuração de replicação lógica.

## Parâmetros

*`name`* [#](#SQL-CREATEPUBLICATION-PARAMS-NAME): O nome da nova publicação.

`FOR TABLE` [#](#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLE): Especifica uma lista de tabelas a serem adicionadas à publicação. Se `ONLY` for especificado antes do nome da tabela, apenas essa tabela será adicionada à publicação. Se `ONLY` não for especificado, a tabela e todas as suas tabelas descendentes (se houver) serão adicionadas. Opcionalmente, `*` pode ser especificado após o nome da tabela para indicar explicitamente que as tabelas descendentes são incluídas. Isso, no entanto, não se aplica a uma tabela dividida. As partições de uma tabela dividida são sempre consideradas implicitamente parte da publicação, portanto, nunca são adicionadas explicitamente à publicação.

Se a cláusula opcional `WHERE` for especificada, ela define uma expressão de *filtro de linha*. As linhas para as quais o *`expression`* avalia como falso ou nulo não serão publicadas. Note que parênteses são necessários ao redor da expressão. Não tem efeito sobre os comandos `TRUNCATE`.

Quando uma lista de colunas é especificada, apenas as colunas nomeadas são replicadas. A lista de colunas pode conter colunas geradas armazenadas também. Se a lista de colunas for omitida, a publicação irá replicar todas as colunas não geradas (incluindo quaisquer adicionadas no futuro) por padrão. Colunas geradas armazenadas também podem ser replicadas se `publish_generated_columns` for definido como `stored`. Especificar uma lista de colunas não tem efeito sobre os comandos `TRUNCATE`. Consulte [Seção 29.5](logical-replication-col-lists.md) para detalhes sobre listas de colunas.

Somente tabelas de base persistentes e tabelas particionadas podem fazer parte de uma publicação. Tabelas temporárias, tabelas não registradas, tabelas externas, visualizações materializadas e visualizações regulares não podem fazer parte de uma publicação.

Especificar uma lista de colunas quando a publicação também publica `FOR TABLES IN SCHEMA` não é suportada.

Quando uma tabela dividida é adicionada a uma publicação, todas as suas partições existentes e futuras são implicitamente consideradas parte da publicação. Portanto, mesmo as operações que são realizadas diretamente em uma partição também são publicadas por meio de publicações das quais seus ancestrais fazem parte.

`FOR ALL TABLES` [#](#SQL-CREATEPUBLICATION-PARAMS-FOR-ALL-TABLES): Marca a publicação como aquela que replica as alterações para todas as tabelas no banco de dados, incluindo tabelas criadas no futuro.

`FOR TABLES IN SCHEMA` [#](#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLES-IN-SCHEMA): Marca a publicação como aquela que replica as alterações para todas as tabelas na lista especificada de esquemas, incluindo tabelas criadas no futuro.

Especificar um esquema quando a publicação também publica uma tabela com uma lista de colunas não é suportado.

Somente as tabelas de base persistentes e as tabelas particionadas presentes no esquema serão incluídas como parte da publicação. Tabelas temporárias, tabelas não registradas, tabelas externas, visualizações materializadas e visualizações regulares do esquema não fazem parte da publicação.

Quando uma tabela dividida é publicada por meio de uma publicação em nível de esquema, todas as suas partições existentes e futuras são implicitamente consideradas parte da publicação, independentemente de serem do esquema de publicação ou não. Portanto, mesmo as operações que são realizadas diretamente em uma partição também são publicadas por meio de publicações das quais seus ancestrais fazem parte.

`WITH ( publication_parameter [= value] [, ... ] )` [#](#SQL-CREATEPUBLICATION-PARAMS-WITH): Esta cláusula especifica parâmetros opcionais para uma publicação. Os seguintes parâmetros são suportados:

`publish` (`string`) [#](#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH) :   Este parâmetro determina quais operações de DML serão publicadas pela nova publicação para os assinantes. O valor é uma lista de operações separadas por vírgula. As operações permitidas são `insert`, `update`, `delete` e `truncate`. O padrão é publicar todas as ações, e, portanto, o valor padrão para esta opção é `'insert, update, delete, truncate'`.

Este parâmetro afeta apenas as operações de DML. Em particular, a sincronização inicial de dados (consulte [Seção 29.9.1](logical-replication-architecture.md#LOGICAL-REPLICATION-SNAPSHOT)) para replicação lógica não leva em conta este parâmetro ao copiar dados de tabela existentes.

`publish_generated_columns` (`enum`) [#](#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-GENERATED-COLUMNS) : Especifica se as colunas geradas presentes nas tabelas associadas à publicação devem ser replicadas. Os valores possíveis são `none` e `stored`.

O padrão é `none`, o que significa que as colunas geradas presentes nas tabelas associadas à publicação não serão replicadas.

Se configurado como `stored`, as colunas geradas armazenadas presentes nas tabelas associadas à publicação serão replicadas.

Nota

Se o assinante tiver uma versão anterior a 18, a sincronização inicial da tabela não copiará as colunas geradas, mesmo que o parâmetro `publish_generated_columns` seja `stored` no editor.

Veja [Seção 29.6](logical-replication-gencols.md) para mais detalhes sobre a replicação lógica de colunas geradas.

`publish_via_partition_root` (`boolean`) [#](#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-VIA-PARTITION-ROOT) :   Este parâmetro controla como as alterações em uma tabela particionada (ou em qualquer uma de suas partições) são publicadas. Quando definido como `true`, as alterações são publicadas usando a identidade e o esquema da tabela particionada raiz. Quando definido como `false` (o padrão), as alterações são publicadas usando a identidade e o esquema das partições individuais onde as alterações ocorreram. Habilitar esta opção permite que as alterações sejam replicadas em uma tabela não particionada ou em uma tabela particionada cuja estrutura de partição difere da do publicador.

Pode haver um caso em que uma assinatura combine várias publicações. Se uma tabela dividida for publicada por qualquer publicação assinada que defina `publish_via_partition_root = true`, as alterações nesta tabela dividida (ou em suas partições) serão publicadas usando a identidade e o esquema desta tabela dividida, em vez da de cada partição individual.

Este parâmetro também afeta a forma como os filtros de linha e as listas de colunas são escolhidos para as partições; veja abaixo para obter detalhes.

Se estiver habilitado, as operações `TRUNCATE` realizadas diretamente em partições não são replicadas.

Ao especificar um parâmetro do tipo `boolean`, a parte *`value`* do `=` pode ser omitida, o que é equivalente a especificar `TRUE`.

## Notas

Se `FOR TABLE`, `FOR ALL TABLES` ou `FOR TABLES IN SCHEMA` não forem especificados, a publicação começa com um conjunto vazio de tabelas. Isso é útil se tabelas ou esquemas devam ser adicionados posteriormente.

A criação de uma publicação não inicia a replicação. Ela apenas define uma lógica de agrupamento e filtragem para futuros assinantes.

Para criar uma publicação, o usuário que faz a solicitação deve ter o privilégio `CREATE` para o banco de dados atual. (É claro que os superusuários ignoram essa verificação.)

Para adicionar uma tabela a uma publicação, o usuário que está fazendo a solicitação deve ter direitos de propriedade sobre a tabela. As cláusulas `FOR ALL TABLES` e `FOR TABLES IN SCHEMA` exigem que o usuário que está fazendo a solicitação seja um superusuário.

As tabelas adicionadas a uma publicação que publica operações `UPDATE` e/ou `DELETE` devem ter `REPLICA IDENTITY` definido. Caso contrário, essas operações serão desativadas nessas tabelas.

Qualquer lista de colunas deve incluir as colunas `REPLICA IDENTITY` para que as operações `UPDATE` ou `DELETE` sejam publicadas. Não há restrições para listas de colunas se a publicação publicar apenas operações `INSERT`.

Uma expressão de filtro de linha (ou seja, a cláusula `WHERE`) deve conter apenas colunas que estejam cobertas pelo `REPLICA IDENTITY`, para que as operações `UPDATE` e `DELETE` sejam publicadas. Para a publicação das operações `INSERT`, qualquer coluna pode ser usada na expressão `WHERE`. O filtro de linha permite expressões simples que não tenham funções definidas pelo usuário, operadores definidos pelo usuário, tipos definidos pelo usuário, colóquios definidos pelo usuário, funções internas não imutáveis ou referências a colunas do sistema.

As colunas geradas que fazem parte de `REPLICA IDENTITY` devem ser publicadas explicitamente, ou seja, listadas na lista de colunas ou habilitando a opção `publish_generated_columns`, para que as operações de `UPDATE` e `DELETE` sejam publicadas.

O filtro de linha em uma tabela se torna redundante se `FOR TABLES IN SCHEMA` for especificado e a tabela pertencer ao esquema referido.

Para tabelas particionadas publicadas, o filtro de linha para cada partição é retirado da tabela particionada publicada se o parâmetro de publicação `publish_via_partition_root` for verdadeiro, ou da própria partição se for falso (o padrão). Veja [Seção 29.4](logical-replication-row-filter.md) para detalhes sobre filtros de linha. Da mesma forma, para tabelas particionadas publicadas, a lista de colunas para cada partição é retirada da tabela particionada publicada se o parâmetro de publicação `publish_via_partition_root` for verdadeiro, ou da própria partição se for falso.

Para um comando `INSERT ... ON CONFLICT`, a publicação publicará a operação que resulta do comando. Dependendo do resultado, ela pode ser publicada como `INSERT` ou `UPDATE`, ou pode não ser publicada em absoluto.

Para um comando `MERGE`, a publicação publicará um `INSERT`, `UPDATE` ou `DELETE` para cada linha inserida, atualizada ou excluída.

`ATTACH` a tabela em uma árvore de partições cujo nó é publicado usando uma publicação com `publish_via_partition_root` definido como `true` não resulta na replicação dos conteúdos existentes da tabela.

Os comandos `COPY ... FROM` são publicados como operações `INSERT`.

As operações de DDL não são publicadas.

A expressão da cláusula `WHERE` é executada com o papel utilizado para a conexão de replicação.

## Exemplos

Crie uma publicação que publique todas as alterações em duas tabelas:

```
CREATE PUBLICATION mypublication FOR TABLE users, departments;
```

Crie uma publicação que publique todas as alterações dos departamentos ativos:

```
CREATE PUBLICATION active_departments FOR TABLE departments WHERE (active IS TRUE);
```

Crie uma publicação que publique todas as alterações em todas as tabelas:

```
CREATE PUBLICATION alltables FOR ALL TABLES;
```

Crie uma publicação que publique apenas as operações `INSERT` em uma tabela:

```
CREATE PUBLICATION insert_only FOR TABLE mydata
    WITH (publish = 'insert');
```

Crie uma publicação que publique todas as alterações para as tabelas `users`, `departments` e todas as alterações para todas as tabelas presentes no esquema `production`:

```
CREATE PUBLICATION production_publication FOR TABLE users, departments, TABLES IN SCHEMA production;
```

Crie uma publicação que publique todas as alterações para todas as tabelas presentes nos esquemas `marketing` e `sales`:

```
CREATE PUBLICATION sales_publication FOR TABLES IN SCHEMA marketing, sales;
```

Crie uma publicação que publique todas as alterações para a tabela `users`, mas replique apenas as colunas `user_id` e `firstname`:

```
CREATE PUBLICATION users_filtered FOR TABLE users (user_id, firstname);
```

## Compatibilidade

`CREATE PUBLICATION` é uma extensão do PostgreSQL.

## Veja também

[ALTERAR PUBLICAÇÃO](sql-alterpublication.md "ALTER PUBLICATION"), [DROP PUBLICAÇÃO](sql-droppublication.md "DROP PUBLICATION"), [CADAQUE SUBSCRIPÇÃO](sql-createsubscription.md "CREATE SUBSCRIPTION"), [ALTERAR SUBSCRIPÇÃO](sql-altersubscription.md "ALTER SUBSCRIPTION")