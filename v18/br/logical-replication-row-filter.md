## 29.4. Filtros de linha [#](#LOGICAL-REPLICATION-ROW-FILTER)

* [29.4.1. Regras de filtro de linha](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-RULES)
* [29.4.2. Restrições de expressão](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-RESTRICTIONS)
* [29.4.3. Transformações de atualização](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-TRANSFORMATIONS)
* [29.4.4. Tabelas particionadas](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-PARTITIONED-TABLE)
* [29.4.5. Sincronização inicial de dados](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-INITIAL-DATA-SYNC)
* [29.4.6. Combinando vários filtros de linha](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-COMBINING)
* [29.4.7. Exemplos](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-EXAMPLES)

Por padrão, todos os dados de todas as tabelas publicadas serão replicados para os assinantes apropriados. Os dados replicados podem ser reduzidos usando um *filtro de linha*. Um usuário pode optar por usar filtros de linha por razões comportamentais, de segurança ou de desempenho. Se uma tabela publicada definir um filtro de linha, uma linha será replicada apenas se seus dados satisfazem a expressão do filtro de linha. Isso permite que um conjunto de tabelas seja parcialmente replicado. O filtro de linha é definido por tabela. Use uma cláusula `WHERE` após o nome da tabela para cada tabela publicada que exige que os dados sejam filtrados. A cláusula `WHERE` deve ser fechada entre parênteses. Veja [CREATE PUBLICATION](sql-createpublication.md "CREATE PUBLICATION") para detalhes.

### 29.4.1. Regras de filtro de linha [#](#LOGICAL-REPLICATION-ROW-FILTER-RULES)

Os filtros de linha são aplicados *antes* da publicação das alterações. Se o filtro de linha avaliar `false` ou `NULL`, a linha não será replicada. A expressão da cláusula `WHERE` é avaliada com o mesmo papel usado para a conexão de replicação (ou seja, o papel especificado na cláusula `CONNECTION`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-CONNECTION) do [CREATE SUBSCRIPTION](sql-createsubscription.md "CREATE SUBSCRIPTION")). Os filtros de linha não têm efeito para o comando `TRUNCATE`.

### 29.4.2. Restrições de expressão [#](#LOGICAL-REPLICATION-ROW-FILTER-RESTRICTIONS)

A cláusula `WHERE` permite apenas expressões simples. Não pode conter funções definidas pelo usuário, operadores, tipos e colasções, referências de coluna do sistema ou funções internas não imutáveis.

Se uma publicação publicar operações `UPDATE` ou `DELETE`, a cláusula de filtro de linha `WHERE` deve conter apenas colunas que são cobertas pela identidade da replica (ver [`REPLICA IDENTITY`](sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY)). Se uma publicação publicar apenas operações `INSERT`, a cláusula de filtro de linha `WHERE` pode usar qualquer coluna.

### 29.4.3. ATUALIZAÇÃO Transformações [#](#LOGICAL-REPLICATION-ROW-FILTER-TRANSFORMATIONS)

Sempre que um `UPDATE` é processado, a expressão de filtro de linha é avaliada tanto para a linha antiga quanto para a nova (ou seja, usando os dados antes e depois da atualização). Se ambas as avaliações forem `true`, ela replica a mudança do `UPDATE`. Se ambas as avaliações forem `false`, ela não replica a mudança. Se apenas uma das linhas antiga/nova corresponder à expressão de filtro de linha, o `UPDATE` é transformado em `INSERT` ou `DELETE`, para evitar qualquer inconsistência de dados. A linha do assinante deve refletir o que é definido pela expressão de filtro de linha no editor.

Se a linha antiga satisfazer a expressão do filtro de linha (foi enviada ao assinante), mas a nova não, então, do ponto de vista da consistência dos dados, a linha antiga deve ser removida do assinante. Assim, o `UPDATE` é transformado em um `DELETE`.

Se a linha antiga não satisfazer a expressão do filtro de linha (não foi enviada ao assinante), mas a nova linha o faz, então, do ponto de vista da consistência dos dados, a nova linha deve ser adicionada ao assinante. Assim, o `UPDATE` é transformado em um `INSERT`.

[Tabela 29.1](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-TRANSFORMATIONS-SUMMARY) resume as transformações aplicadas.

**Tabela 29.1. Resumo da transformação de `UPDATE`**



<table border="1" class="table" summary="UPDATE Transformation Summary">
 <colgroup>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Old row
   </th>
   <th>
    New row
   </th>
   <th>
    Transformation
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    no match
   </td>
   <td>
    no match
   </td>
   <td>
    don't replicate
   </td>
  </tr>
  <tr>
   <td>
    no match
   </td>
   <td>
    match
   </td>
   <td>
    <code class="literal">
     INSERT
    </code>
   </td>
  </tr>
  <tr>
   <td>
    match
   </td>
   <td>
    no match
   </td>
   <td>
    <code class="literal">
     DELETE
    </code>
   </td>
  </tr>
  <tr>
   <td>
    match
   </td>
   <td>
    match
   </td>
   <td>
    <code class="literal">
     UPDATE
    </code>
   </td>
  </tr>
 </tbody>
</table>






### 29.4.4. Tabelas Partidas [#](#LOGICAL-REPLICATION-ROW-FILTER-PARTITIONED-TABLE)

Se a publicação contiver uma tabela dividida, o parâmetro de publicação `publish_via_partition_root`(sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-VIA-PARTITION-ROOT) determina qual filtro de linha é usado. Se `publish_via_partition_root` é `true`, o filtro de linha do *root partitioned table* é usado. Caso contrário, se `publish_via_partition_root` é `false` (padrão), cada filtro de linha do *partition* é usado.

### 29.4.5. Sincronização inicial de dados [#](#LOGICAL-REPLICATION-ROW-FILTER-INITIAL-DATA-SYNC)

Se a assinatura exigir a cópia de dados de tabela pré-existentes e uma publicação contiver cláusulas `WHERE`, apenas os dados que satisfazem as expressões de filtro de linha serão copiados para o assinante.

Se a assinatura tiver várias publicações nas quais uma tabela foi publicada com diferentes cláusulas `WHERE`, as linhas que satisfazem *qualquer* das expressões serão copiadas. Consulte [Seção 29.4.6](logical-replication-row-filter.md#LOGICAL-REPLICATION-ROW-FILTER-COMBINING) para obter detalhes.

### Aviso

Como a sincronização de dados inicial não leva em conta o parâmetro `publish`(sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH) ao copiar dados de tabela existentes, algumas linhas podem ser copiadas que não seriam replicadas usando DML. Consulte [Seção 29.9.1](logical-replication-architecture.md#LOGICAL-REPLICATION-SNAPSHOT), e veja [Seção 29.2.2](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-EXAMPLES) para exemplos.

### Nota

Se o assinante estiver em uma versão anterior a 15, a cópia de dados pré-existentes não usa filtros de linha, mesmo que eles estejam definidos na publicação. Isso ocorre porque as versões antigas só podem copiar os dados completos da tabela.

### 29.4.6. Combinando Filtros de Linha Múltiplos [#](#LOGICAL-REPLICATION-ROW-FILTER-COMBINING)

Se a assinatura tiver várias publicações nas quais a mesma tabela foi publicada com diferentes filtros de linha (para a mesma operação `publish`(sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH)), essas expressões são ORed juntas, de modo que as linhas que satisfazem *qualquer* das expressões serão replicadas. Isso significa que todos os outros filtros de linha para a mesma tabela se tornam redundantes se:

* Uma das publicações não tem filtro de linha.
* Uma das publicações foi criada usando `FOR ALL TABLES`(sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-ALL-TABLES). Esta cláusula não permite filtros de linha.
* Uma das publicações foi criada usando `FOR TABLES IN SCHEMA`(sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-FOR-TABLES-IN-SCHEMA) e a tabela pertence ao esquema referido. Esta cláusula não permite filtros de linha.

### 29.4.7. Exemplos [#](#LOGICAL-REPLICATION-ROW-FILTER-EXAMPLES)

Crie algumas tabelas que serão usadas nos exemplos a seguir.

```
/* pub # */ CREATE TABLE t1(a int, b int, c text, PRIMARY KEY(a,c));
/* pub # */ CREATE TABLE t2(d int, e int, f int, PRIMARY KEY(d));
/* pub # */ CREATE TABLE t3(g int, h int, i int, PRIMARY KEY(g));
```

Crie algumas publicações. A publicação `p1` tem uma tabela (`t1`) e essa tabela tem um filtro de linha. A publicação `p2` tem duas tabelas. A tabela `t1` não tem filtro de linha, e a tabela `t2` tem um filtro de linha. A publicação `p3` tem duas tabelas, e ambas têm um filtro de linha.

```
/* pub # */ CREATE PUBLICATION p1 FOR TABLE t1 WHERE (a > 5 AND c = 'NSW');
/* pub # */ CREATE PUBLICATION p2 FOR TABLE t1, t2 WHERE (e = 99);
/* pub # */ CREATE PUBLICATION p3 FOR TABLE t2 WHERE (d = 10), t3 WHERE (g = 10);
```

`psql` pode ser usado para mostrar as expressões de filtro de linha (se definidas) para cada publicação.

```
/* pub # */ \dRp+
                                         Publication p1
  Owner   | All tables | Inserts | Updates | Deletes | Truncates | Generated columns | Via root
----------+------------+---------+---------+---------+-----------+-------------------+----------
 postgres | f          | t       | t       | t       | t         | none              | f
Tables:
    "public.t1" WHERE ((a > 5) AND (c = 'NSW'::text))

                                         Publication p2
  Owner   | All tables | Inserts | Updates | Deletes | Truncates | Generated columns | Via root
----------+------------+---------+---------+---------+-----------+-------------------+----------
 postgres | f          | t       | t       | t       | t         | none              | f
Tables:
    "public.t1"
    "public.t2" WHERE (e = 99)

                                         Publication p3
  Owner   | All tables | Inserts | Updates | Deletes | Truncates | Generated columns | Via root
----------+------------+---------+---------+---------+-----------+-------------------+----------
 postgres | f          | t       | t       | t       | t         | none              | f
Tables:
    "public.t2" WHERE (d = 10)
    "public.t3" WHERE (g = 10)
```

`psql` pode ser usado para mostrar as expressões de filtro de linha (se definidas) para cada tabela. Veja que a tabela `t1` é membro de duas publicações, mas tem um filtro de linha apenas em `p1`. Veja que a tabela `t2` é membro de duas publicações e tem um filtro de linha diferente em cada uma delas.

```
/* pub # */ \d t1
                 Table "public.t1"
 Column |  Type   | Collation | Nullable | Default
--------+---------+-----------+----------+---------
 a      | integer |           | not null |
 b      | integer |           |          |
 c      | text    |           | not null |
Indexes:
    "t1_pkey" PRIMARY KEY, btree (a, c)
Publications:
    "p1" WHERE ((a > 5) AND (c = 'NSW'::text))
    "p2"

/* pub # */ \d t2
                 Table "public.t2"
 Column |  Type   | Collation | Nullable | Default
--------+---------+-----------+----------+---------
 d      | integer |           | not null |
 e      | integer |           |          |
 f      | integer |           |          |
Indexes:
    "t2_pkey" PRIMARY KEY, btree (d)
Publications:
    "p2" WHERE (e = 99)
    "p3" WHERE (d = 10)

/* pub # */ \d t3
                 Table "public.t3"
 Column |  Type   | Collation | Nullable | Default
--------+---------+-----------+----------+---------
 g      | integer |           | not null |
 h      | integer |           |          |
 i      | integer |           |          |
Indexes:
    "t3_pkey" PRIMARY KEY, btree (g)
Publications:
    "p3" WHERE (g = 10)
```

No nó do assinante, crie uma tabela `t1` com a mesma definição que a do editor, e também crie a assinatura `s1` que se inscreve na publicação `p1`.

```
/* sub # */ CREATE TABLE t1(a int, b int, c text, PRIMARY KEY(a,c));
/* sub # */ CREATE SUBSCRIPTION s1
/* sub - */ CONNECTION 'host=localhost dbname=test_pub application_name=s1'
/* sub - */ PUBLICATION p1;
```

Insira algumas linhas. Apenas as linhas que satisfazem a cláusula `t1 WHERE` da publicação `p1` são replicadas.

```
/* pub # */ INSERT INTO t1 VALUES (2, 102, 'NSW');
/* pub # */ INSERT INTO t1 VALUES (3, 103, 'QLD');
/* pub # */ INSERT INTO t1 VALUES (4, 104, 'VIC');
/* pub # */ INSERT INTO t1 VALUES (5, 105, 'ACT');
/* pub # */ INSERT INTO t1 VALUES (6, 106, 'NSW');
/* pub # */ INSERT INTO t1 VALUES (7, 107, 'NT');
/* pub # */ INSERT INTO t1 VALUES (8, 108, 'QLD');
/* pub # */ INSERT INTO t1 VALUES (9, 109, 'NSW');

/* pub # */ SELECT * FROM t1;
 a |  b  |  c
---+-----+-----
 2 | 102 | NSW
 3 | 103 | QLD
 4 | 104 | VIC
 5 | 105 | ACT
 6 | 106 | NSW
 7 | 107 | NT
 8 | 108 | QLD
 9 | 109 | NSW
(8 rows)
```

```
/* sub # */ SELECT * FROM t1;
 a |  b  |  c
---+-----+-----
 6 | 106 | NSW
 9 | 109 | NSW
(2 rows)
```

Atualize alguns dados, onde os valores da linha antiga e nova satisfazem a cláusula `t1 WHERE` da publicação `p1`. O `UPDATE` replica a mudança como normal.

```
/* pub # */ UPDATE t1 SET b = 999 WHERE a = 6;

/* pub # */ SELECT * FROM t1;
 a |  b  |  c
---+-----+-----
 2 | 102 | NSW
 3 | 103 | QLD
 4 | 104 | VIC
 5 | 105 | ACT
 7 | 107 | NT
 8 | 108 | QLD
 9 | 109 | NSW
 6 | 999 | NSW
(8 rows)
```

```
/* sub # */ SELECT * FROM t1;
 a |  b  |  c
---+-----+-----
 9 | 109 | NSW
 6 | 999 | NSW
(2 rows)
```

Atualize alguns dados, onde os valores da linha antiga não satisfaziam a cláusula `t1 WHERE` da publicação `p1`, mas os novos valores da linha a satisfazem. O `UPDATE` é transformado em um `INSERT` e a mudança é replicada. Veja a nova linha no assinante.

```
/* pub # */ UPDATE t1 SET a = 555 WHERE a = 2;

/* pub # */ SELECT * FROM t1;
  a  |  b  |  c
-----+-----+-----
   3 | 103 | QLD
   4 | 104 | VIC
   5 | 105 | ACT
   7 | 107 | NT
   8 | 108 | QLD
   9 | 109 | NSW
   6 | 999 | NSW
 555 | 102 | NSW
(8 rows)
```

```
/* sub # */ SELECT * FROM t1;
  a  |  b  |  c
-----+-----+-----
   9 | 109 | NSW
   6 | 999 | NSW
 555 | 102 | NSW
(3 rows)
```

Atualize alguns dados, onde os valores da linha antiga satisfaziam a cláusula `t1 WHERE` da publicação `p1`, mas os novos valores da linha não a satisfazem. O `UPDATE` é transformado em um `DELETE` e a mudança é replicada. Verifique se a linha é removida do assinante.

```
/* pub # */ UPDATE t1 SET c = 'VIC' WHERE a = 9;

/* pub # */ SELECT * FROM t1;
  a  |  b  |  c
-----+-----+-----
   3 | 103 | QLD
   4 | 104 | VIC
   5 | 105 | ACT
   7 | 107 | NT
   8 | 108 | QLD
   6 | 999 | NSW
 555 | 102 | NSW
   9 | 109 | VIC
(8 rows)
```

```
/* sub # */ SELECT * FROM t1;
  a  |  b  |  c
-----+-----+-----
   6 | 999 | NSW
 555 | 102 | NSW
(2 rows)
```

Os exemplos a seguir mostram como o parâmetro de publicação `publish_via_partition_root`(sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-VIA-PARTITION-ROOT) determina se o filtro de linha da tabela pai ou da tabela filho será usado no caso de tabelas particionadas.

Crie uma tabela particionada no editor.

```
/* pub # */ CREATE TABLE parent(a int PRIMARY KEY) PARTITION BY RANGE(a);
/* pub # */ CREATE TABLE child PARTITION OF parent DEFAULT;
```

Crie as mesmas tabelas no assinante.

```
/* sub # */ CREATE TABLE parent(a int PRIMARY KEY) PARTITION BY RANGE(a);
/* sub # */ CREATE TABLE child PARTITION OF parent DEFAULT;
```

Crie uma publicação `p4`, e, em seguida, assine-a. O parâmetro de publicação `publish_via_partition_root` é definido como verdadeiro. Existem filtros de linha definidos tanto na tabela particionada (`parent`), quanto na partição (`child`).

```
/* pub # */ CREATE PUBLICATION p4 FOR TABLE parent WHERE (a < 5), child WHERE (a >= 5)
/* pub - */ WITH (publish_via_partition_root=true);
```

```
/* sub # */ CREATE SUBSCRIPTION s4
/* sub - */ CONNECTION 'host=localhost dbname=test_pub application_name=s4'
/* sub - */ PUBLICATION p4;
```

Insira alguns valores diretamente nas tabelas `parent` e `child`. Eles se replicam usando o filtro de linha de `parent` (porque `publish_via_partition_root` é verdadeiro).

```
/* pub # */ INSERT INTO parent VALUES (2), (4), (6);
/* pub # */ INSERT INTO child VALUES (3), (5), (7);

/* pub # */ SELECT * FROM parent ORDER BY a;
 a
---
 2
 3
 4
 5
 6
 7
(6 rows)
```

```
/* sub # */ SELECT * FROM parent ORDER BY a;
 a
---
 2
 3
 4
(3 rows)
```

Repita o mesmo teste, mas com um valor diferente para `publish_via_partition_root`. O parâmetro de publicação `publish_via_partition_root` é definido como falso. Um filtro de linha é definido na partição (`child`).

```
/* pub # */ DROP PUBLICATION p4;
/* pub # */ CREATE PUBLICATION p4 FOR TABLE parent, child WHERE (a >= 5)
/* pub - */ WITH (publish_via_partition_root=false);
```

```
/* sub # */ ALTER SUBSCRIPTION s4 REFRESH PUBLICATION;
```

Os insertos no editor são os mesmos que antes. Eles se replicam usando o filtro de linha de `child` (porque `publish_via_partition_root` é falso).

```
/* pub # */ TRUNCATE parent;
/* pub # */ INSERT INTO parent VALUES (2), (4), (6);
/* pub # */ INSERT INTO child VALUES (3), (5), (7);

/* pub # */ SELECT * FROM parent ORDER BY a;
 a
---
 2
 3
 4
 5
 6
 7
(6 rows)
```

```
/* sub # */ SELECT * FROM child ORDER BY a;
 a
---
 5
 6
 7
(3 rows)
```
