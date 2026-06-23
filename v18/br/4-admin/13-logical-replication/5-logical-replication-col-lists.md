## 29.5. Listas de colunas [#](#LOGICAL-REPLICATION-COL-LISTS)

* [29.5.1. Exemplos](logical-replication-col-lists.md#LOGICAL-REPLICATION-COL-LIST-EXAMPLES)

Cada publicação pode especificar opcionalmente quais colunas de cada tabela são replicadas para os assinantes. A tabela do lado do assinante deve ter, pelo menos, todas as colunas que são publicadas. Se nenhuma lista de colunas for especificada, então todas as colunas do editor são replicadas. Consulte [CREATE PUBLICATION](sql-createpublication.md) para obter detalhes sobre a sintaxe.

A escolha das colunas pode ser baseada em razões comportamentais ou de desempenho. No entanto, não confie nesse recurso para segurança: um assinante malicioso pode obter dados de colunas que não são publicadas especificamente. Se a segurança é uma consideração, as proteções podem ser aplicadas no lado do publicador.

Se não for especificado um elenco de colunas, quaisquer colunas adicionadas à tabela posteriormente serão replicadas automaticamente. Isso significa que ter um elenco de colunas que nomeia todas as colunas não é o mesmo que não ter nenhum elenco de colunas.

Uma lista de colunas pode conter apenas referências simples de coluna. A ordem das colunas na lista não é preservada.

As colunas geradas também podem ser especificadas em uma lista de colunas. Isso permite que as colunas geradas sejam publicadas, independentemente do parâmetro de publicação `publish_generated_columns`(sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-GENERATED-COLUMNS). Veja [Seção 29.6](logical-replication-gencols.md "29.6. Generated Column Replication") para detalhes.

Especificar uma lista de colunas quando a publicação também publica `FOR TABLES IN SCHEMA` (sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLES-IN-SCHEMA) não é suportada.

Para tabelas particionadas, o parâmetro de publicação `publish_via_partition_root`(sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-VIA-PARTITION-ROOT) determina qual lista de colunas é usada. Se `publish_via_partition_root` for `true`, a lista de colunas da tabela raiz particionada é usada. Caso contrário, se `publish_via_partition_root` for `false` (o padrão), a lista de colunas de cada particion é usada.

Se uma publicação publicar operações `UPDATE` ou `DELETE`, qualquer lista de colunas deve incluir as colunas de identidade de replicação da tabela (ver [`REPLICA IDENTITY`](sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY)). Se uma publicação publicar apenas operações `INSERT`, então a lista de colunas pode omitir as colunas de identidade de replicação.

As listas de colunas não têm efeito para o comando `TRUNCATE`.

Durante a sincronização inicial de dados, apenas as colunas publicadas são copiadas. No entanto, se o assinante for de uma versão anterior a 15, todas as colunas da tabela são copiadas durante a sincronização inicial de dados, ignorando quaisquer listas de colunas. Se o assinante for de uma versão anterior a 18, a sincronização inicial da tabela não copiará as colunas geradas, mesmo que elas estejam definidas no editor.

### Aviso: Combinando listas de colunas de várias publicações

Atualmente, não há suporte para assinaturas que compreendem várias publicações onde a mesma tabela foi publicada com diferentes listas de colunas. [CREATE SUBSCRIPTION](sql-createsubscription.md "CREATE SUBSCRIPTION") não permite a criação de tais assinaturas, mas ainda é possível entrar nessa situação ao adicionar ou alterar listas de colunas no lado da publicação após a criação de uma assinatura.

Isso significa que alterar as listas de colunas das tabelas em publicações que já estão assinadas pode resultar em erros sendo lançados no lado do assinante.

Se uma assinatura for afetada por esse problema, a única maneira de retomar a replicação é ajustar uma das listas de colunas do lado da publicação para que todas elas coincidam; e, em seguida, ou recriar a assinatura, ou usar `ALTER SUBSCRIPTION ... DROP PUBLICATION`(sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-SETADDDROP-PUBLICATION) para remover uma das publicações que causam problemas e adicioná-la novamente.

### 29.5.1. Exemplos [#](#LOGICAL-REPLICATION-COL-LIST-EXAMPLES)

Crie uma tabela `t1` a ser usada no exemplo a seguir.

```
/* pub # */ CREATE TABLE t1(id int, a text, b text, c text, d text, e text, PRIMARY KEY(id));
```

Crie uma publicação `p1`. Uma lista de colunas é definida para a tabela `t1` para reduzir o número de colunas que serão replicadas. Observe que a ordem dos nomes das colunas na lista de colunas não importa.

```
/* pub # */ CREATE PUBLICATION p1 FOR TABLE t1 (id, b, a, d);
```

`psql` pode ser usado para mostrar as listas de colunas (se definidas) para cada publicação.

```
/* pub # */ \dRp+
                                         Publication p1
  Owner   | All tables | Inserts | Updates | Deletes | Truncates | Generated columns | Via root
----------+------------+---------+---------+---------+-----------+-------------------+----------
 postgres | f          | t       | t       | t       | t         | none              | f
Tables:
    "public.t1" (id, a, b, d)
```

`psql` pode ser usado para mostrar as listas de colunas (se definidas) para cada tabela.

```
/* pub # */ \d t1
                 Table "public.t1"
 Column |  Type   | Collation | Nullable | Default
--------+---------+-----------+----------+---------
 id     | integer |           | not null |
 a      | text    |           |          |
 b      | text    |           |          |
 c      | text    |           |          |
 d      | text    |           |          |
 e      | text    |           |          |
Indexes:
    "t1_pkey" PRIMARY KEY, btree (id)
Publications:
    "p1" (id, a, b, d)
```

No nó do assinante, crie uma tabela `t1`, que agora precisa apenas de um subconjunto das colunas que estavam na tabela do editor `t1`, e também crie a assinatura `s1` que se inscreve na publicação `p1`.

```
/* sub # */ CREATE TABLE t1(id int, b text, a text, d text, PRIMARY KEY(id));
/* sub # */ CREATE SUBSCRIPTION s1
/* sub - */ CONNECTION 'host=localhost dbname=test_pub application_name=s1'
/* sub - */ PUBLICATION p1;
```

No nó do editor, insira algumas linhas na tabela `t1`.

```
/* pub # */ INSERT INTO t1 VALUES(1, 'a-1', 'b-1', 'c-1', 'd-1', 'e-1');
/* pub # */ INSERT INTO t1 VALUES(2, 'a-2', 'b-2', 'c-2', 'd-2', 'e-2');
/* pub # */ INSERT INTO t1 VALUES(3, 'a-3', 'b-3', 'c-3', 'd-3', 'e-3');
/* pub # */ SELECT * FROM t1 ORDER BY id;
 id |  a  |  b  |  c  |  d  |  e
----+-----+-----+-----+-----+-----
  1 | a-1 | b-1 | c-1 | d-1 | e-1
  2 | a-2 | b-2 | c-2 | d-2 | e-2
  3 | a-3 | b-3 | c-3 | d-3 | e-3
(3 rows)
```

Apenas os dados da lista de colunas da publicação `p1` são replicados.

```
/* sub # */ SELECT * FROM t1 ORDER BY id;
 id |  b  |  a  |  d
----+-----+-----+-----
  1 | b-1 | a-1 | d-1
  2 | b-2 | a-2 | d-2
  3 | b-3 | a-3 | d-3
(3 rows)
```
