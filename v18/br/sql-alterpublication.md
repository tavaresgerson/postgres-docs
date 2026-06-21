## ALTERAR PUBLICAÇÃO

ALTERAR PUBLICAÇÃO — alterar a definição de uma publicação

## Sinopse

```
ALTER PUBLICATION name ADD publication_object [, ...]
ALTER PUBLICATION name SET publication_object [, ...]
ALTER PUBLICATION name DROP publication_drop_object [, ...]
ALTER PUBLICATION name SET ( publication_parameter [= value] [, ... ] )
ALTER PUBLICATION name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER PUBLICATION name RENAME TO new_name

where publication_object is one of:

    TABLE table_and_columns [, ... ]
    TABLES IN SCHEMA { schema_name | CURRENT_SCHEMA } [, ... ]

and publication_drop_object is one of:

    TABLE [ ONLY ] table_name [ * ] [, ... ]
    TABLES IN SCHEMA { schema_name | CURRENT_SCHEMA } [, ... ]

and table_and_columns is:

    [ ONLY ] table_name [ * ] [ ( column_name [, ... ] ) ] [ WHERE ( expression ) ]
```

## Descrição

O comando `ALTER PUBLICATION` pode alterar os atributos de uma publicação.

As três primeiras variantes alteram quais tabelas/esquemas fazem parte da publicação. A cláusula `SET` substituirá a lista de tabelas/esquemas na publicação pela lista especificada; as tabelas/esquemas existentes que estavam presentes na publicação serão removidos. As cláusulas `ADD` e `DROP` adicionarão e removerão uma ou mais tabelas/esquemas da publicação. Observe que adicionar tabelas/esquemas a uma publicação que já está assinada exigirá uma ação [[`ALTER SUBSCRIPTION ... REFRESH PUBLICATION`][(sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-REFRESH-PUBLICATION)]] do lado assinante para se tornar efetiva. Observe também que `DROP TABLES IN SCHEMA` não descartará quaisquer tabelas de esquema que foram especificadas usando [[`FOR TABLE`][(sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLE)]]/`ADD TABLE`.

A quarta variante deste comando listado no sinopse pode alterar todas as propriedades de publicação especificadas em [CREATE PUBLICATION](sql-createpublication.md "CREATE PUBLICATION"). As propriedades não mencionadas no comando retêm suas configurações anteriores.

As variantes restantes alteram o proprietário e o nome da publicação.

Você deve ser o proprietário da publicação para usar `ALTER PUBLICATION`. Adicionar uma tabela a uma publicação também requer que você seja o proprietário dessa tabela. Para invocar o `ADD TABLES IN SCHEMA` e `SET TABLES IN SCHEMA` a uma publicação, o usuário invocante deve ser um superusuário. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário, e esse papel deve ter o privilégio `CREATE` no banco de dados. Além disso, o novo proprietário de uma publicação [`FOR ALL TABLES`(sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-ALL-TABLES) ou [`FOR TABLES IN SCHEMA`(sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLES-IN-SCHEMA)]] deve ser um superusuário. No entanto, um superusuário pode alterar a propriedade de uma publicação independentemente dessas restrições.

Adicionar/definir qualquer esquema quando a publicação também publica uma tabela com uma lista de colunas, e vice-versa, não é suportada.

## Parâmetros

*`name`*: O nome de uma publicação existente cuja definição deve ser alterada.

*`table_name`*: Nome de uma tabela existente. Se `ONLY` for especificado antes do nome da tabela, apenas essa tabela será afetada. Se `ONLY` não for especificado, a tabela e todas as suas tabelas descendentes (se houver) serão afetadas. Opcionalmente, `*` pode ser especificado após o nome da tabela para indicar explicitamente que as tabelas descendentes são incluídas.

Opcionalmente, uma lista de colunas pode ser especificada. Consulte [CREATE PUBLICATION](sql-createpublication.md "CREATE PUBLICATION") para obter detalhes. Observe que uma assinatura que tenha várias publicações nas quais a mesma tabela foi publicada com diferentes listas de colunas não é suportada. Consulte [Aviso: Combinando Listas de Colunas de Múltiplas Publicações](logical-replication-col-lists.md#LOGICAL-REPLICATION-COL-LIST-COMBINING "Warning: Combining Column Lists from Multiple Publications") para obter detalhes sobre os problemas potenciais ao alterar listas de colunas.

Se a cláusula opcional `WHERE` for especificada, as linhas para as quais o *`expression`* seja avaliado como falso ou nulo não serão publicadas. Observe que as chaves são necessárias ao redor da expressão. O *`expression`* é avaliado com o papel usado para a conexão de replicação.

*`schema_name`*: Nome de um esquema existente.

`SET ( publication_parameter [= value] [, ... ] )`: Esta cláusula altera os parâmetros de publicação originalmente definidos por [CREATE PUBLICATION](sql-createpublication.md "CREATE PUBLICATION"). Veja mais informações lá.

### Atenção

Alterar o parâmetro `publish_via_partition_root` pode levar à perda ou duplicação de dados no assinante, pois ele altera a identidade e o esquema das tabelas publicadas. Este fato ocorre apenas quando uma tabela raiz de partição é especificada como alvo de replicação.

Esse problema pode ser evitado desistindo de modificar as tabelas de folhas de partição após o `ALTER PUBLICATION ... SET` até que o [(sql-altersubscription.md "ALTER SUBSCRIPTION")](sql-altersubscription.md "ALTER SUBSCRIPTION") seja executado e apenas atualizando com a opção `copy_data = off`.

*`new_owner`*: O nome do usuário do novo proprietário da publicação.

*`new_name`*: O novo nome da publicação.

## Exemplos

Alterar a publicação para publicar apenas edições e atualizações:

```
ALTER PUBLICATION noinsert SET (publish = 'update, delete');
```

Adicione algumas tabelas à publicação:

```
ALTER PUBLICATION mypublication ADD TABLE users (user_id, firstname), departments;
```

Altere o conjunto de colunas publicadas para uma tabela:

```
ALTER PUBLICATION mypublication SET TABLE users (user_id, firstname, lastname), TABLE departments;
```

Adicione os esquemas `marketing` e `sales` à publicação `sales_publication`:

```
ALTER PUBLICATION sales_publication ADD TABLES IN SCHEMA marketing, sales;
```

Adicione as tabelas `users`, `departments` e o esquema `production` à publicação `production_publication`:

```
ALTER PUBLICATION production_publication ADD TABLE users, departments, TABLES IN SCHEMA production;
```

## Compatibilidade

`ALTER PUBLICATION` é uma extensão do PostgreSQL.

## Veja também

[CADASTRAR PUBLICAÇÃO](sql-createpublication.md "CREATE PUBLICATION"), [DROP PUBLICAÇÃO](sql-droppublication.md "DROP PUBLICATION"), [CADASTRAR ASSINATURA](sql-createsubscription.md "CREATE SUBSCRIPTION"), [ALTERAR ASSINATURA](sql-altersubscription.md "ALTER SUBSCRIPTION")