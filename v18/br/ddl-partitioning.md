## 5.12. Divisão de tabela [#](#DDL-PARTITIONING)

* [5.12.1. Visão geral][(ddl-partitioning.md#DDL-PARTITIONING-OVERVIEW)]
* [5.12.2. Partição declarativa][(ddl-partitioning.md#DDL-PARTITIONING-DECLARATIVE)]
* [5.12.3. Partição usando herança][(ddl-partitioning.md#DDL-PARTITIONING-USING-INHERITANCE)]
* [5.12.4. Remoção de partições][(ddl-partitioning.md#DDL-PARTITION-PRUNING)]
* [5.12.5. Partição e exclusão de restrições][(ddl-partitioning.md#DDL-PARTITIONING-CONSTRAINT-EXCLUSION)]
* [5.12.6. Práticas recomendadas para partição declarativa][(ddl-partitioning.md#DDL-PARTITIONING-DECLARATIVE-BEST-PRACTICES)]

O PostgreSQL suporta a partição básica de tabelas. Esta seção descreve por que e como implementar a partição como parte do projeto do seu banco de dados.

### 5.12.1. Visão geral [#](#DDL-PARTITIONING-OVERVIEW)

A partição refere-se à divisão de uma tabela grande em partes físicas menores. A partição pode oferecer vários benefícios:

* O desempenho da consulta pode ser melhorado drasticamente em certas situações, especialmente quando a maioria das linhas com acesso frequente da tabela está em uma única partição ou em um pequeno número de partições. A partição substitui efetivamente os níveis superiores dos índices, tornando mais provável que as partes usadas frequentemente dos índices se encaixem na memória.
* Quando as consultas ou atualizações acessam uma grande porcentagem de uma única partição, o desempenho pode ser melhorado usando uma varredura sequencial dessa partição em vez de usar um índice, o que exigiria leituras de acesso aleatório espalhadas por toda a tabela.
* Cargas e exclusões em massa podem ser realizadas adicionando ou removendo partições, se o padrão de uso for considerado no projeto de partição. A eliminação de uma partição individual usando `DROP TABLE`, ou fazendo `ALTER TABLE DETACH PARTITION`, é muito mais rápida do que uma operação em massa. Esses comandos também evitam completamente o `VACUUM` de sobrecarga causado por uma `DELETE` em massa.
* Dados raramente usados podem ser migrados para mídias de armazenamento mais baratas e lentas.

Esses benefícios normalmente só valem quando uma tabela seria muito grande de outra forma. O ponto exato em que uma tabela se beneficiará da partição depende do aplicativo, embora uma regra geral seja que o tamanho da tabela deve exceder a memória física do servidor de banco de dados.

O PostgreSQL oferece suporte integrado para as seguintes formas de particionamento:

Particionamento de Faixa [#](#DDL-PARTITIONING-OVERVIEW-RANGE): A tabela é dividida em "faixas" definidas por uma coluna ou conjunto de colunas chave, sem sobreposição entre as faixas de valores atribuídos a diferentes particionamentos. Por exemplo, pode-se particionar por faixas de datas ou por faixas de identificadores para objetos de negócios específicos. Os limites de cada faixa são entendidos como inclusivos no extremo inferior e exclusivos no extremo superior. Por exemplo, se o intervalo de uma particionamento é de `1` a `10`, e o intervalo do próximo é de `10` a `20`, então o valor `10` pertence à segunda particionamento e não à primeira.

Partitionamento de lista [#](#DDL-PARTITIONING-OVERVIEW-LIST): A tabela é particionada, listando explicitamente quais valores de chave aparecem em cada partição.

Partitionamento de Hash [#](#DDL-PARTITIONING-OVERVIEW-HASH): A tabela é dividida especificando um módulo e um resto para cada partição. Cada partição conterá as linhas para as quais o valor de hash da chave da partição dividido pelo módulo especificado produzirá o resto especificado.

Se a sua aplicação precisar usar outros tipos de particionamento que não estão listados acima, métodos alternativos, como herança e vistas `UNION ALL`, podem ser usados em vez disso. Esses métodos oferecem flexibilidade, mas não possuem alguns dos benefícios de desempenho do particionamento declarativo embutido.

### 5.12.2. Partição Declarativa [#](#DDL-PARTITIONING-DECLARATIVE)

O PostgreSQL permite que você declare que uma tabela é dividida em partições. A tabela que é dividida é referida como uma *tabela particionada*. A declaração inclui o *método de particionamento* conforme descrito acima, além de uma lista de colunas ou expressões a serem usadas como *chave de partição*.

A própria tabela dividida é uma tabela “virtual” que não possui armazenamento próprio. Em vez disso, o armazenamento pertence aos *partições*, que são tabelas comuns associadas à tabela dividida. Cada partição armazena um subconjunto dos dados, conforme definido pelos seus *limites de partição*. Todas as linhas inseridas em uma tabela dividida serão encaminhadas para a partição apropriada com base nos valores da(s) coluna(s) chave(s) de partição. A atualização da chave de partição de uma linha fará com que ela seja movida para uma partição diferente, se não mais atender aos limites de partição da sua partição original.

As partições podem ser definidas como tabelas particionadas, resultando em *sub-particionamento*. Embora todas as partições devam ter as mesmas colunas que seu pai particionado, as partições podem ter seus próprios índices, restrições e valores padrão, distintos daqueles das outras partições. Consulte [CREATE TABLE][(sql-createtable.md "CREATE TABLE")] para mais detalhes sobre a criação de tabelas e partições particionadas.

Não é possível transformar uma tabela comum em uma tabela particionada ou vice-versa. No entanto, é possível adicionar uma tabela existente comum ou particionada como uma partição de uma tabela particionada, ou remover uma partição de uma tabela particionada, transformando-a em uma tabela independente; isso pode simplificar e acelerar muitos processos de manutenção. Consulte [ALTER TABLE](sql-altertable.md "ALTER TABLE") para saber mais sobre os subcomandos `ATTACH PARTITION` e `DETACH PARTITION`.

As partições também podem ser [tabuletas estrangeiras][(ddl-foreign-data.md "5.13. Foreign Data")], embora seja necessário bastante cuidado, pois é responsabilidade do usuário que o conteúdo da tabela estrangeira satisfaça a regra de partição. Há outras restrições também. Consulte [CREATE FOREIGN TABLE][(sql-createforeigntable.md "CREATE FOREIGN TABLE")] para obter mais informações.

#### 5.12.2.1. Exemplo [#](#DDL-PARTITIONING-DECLARATIVE-EXAMPLE)

Suponha que estamos construindo um banco de dados para uma grande empresa de sorvete. A empresa mede as temperaturas máximas todos os dias, bem como as vendas de sorvete em cada região. Concetualmente, queremos uma tabela como:

```
CREATE TABLE measurement (
    city_id         int not null,
    logdate         date not null,
    peaktemp        int,
    unitsales       int
);
```

Sabemos que a maioria das consultas acessará apenas os dados da última semana, do mês ou do trimestre, já que o uso principal desta tabela será preparar relatórios online para a gestão. Para reduzir a quantidade de dados antigos que precisam ser armazenados, decidimos manter apenas os dados dos últimos 3 anos. No início de cada mês, removeremos os dados do mês mais antigo. Nesta situação, podemos usar a partição para nos ajudar a atender a todas as nossas diferentes necessidades para a tabela de medições.

Para usar a partição declarativa neste caso, siga os passos a seguir:

1. Crie a tabela `measurement` como uma tabela particionada, especificando a cláusula `PARTITION BY`, que inclui o método de particionamento (`RANGE` neste caso) e a lista de coluna(s) a serem usadas como chave de particionamento.

```
   CREATE TABLE measurement (
       city_id         int not null,
       logdate         date not null,
       peaktemp        int,
       unitsales       int
   ) PARTITION BY RANGE (logdate);
   ``` 2. Crie partições. A definição de cada partição deve especificar limites que correspondam ao método de particionamento e à chave de partição do pai. Observe que especificar limites de forma que os valores da nova partição se sobreponham com os de uma ou mais partições existentes causará um erro.

As partições assim criadas são, em todos os aspectos, tabelas normais do PostgreSQL (ou, possivelmente, tabelas estrangeiras). É possível especificar um espaço de tabelas e parâmetros de armazenamento para cada partição separadamente.

Para o nosso exemplo, cada partição deve conter o valor de um mês de dados, para corresponder ao requisito de excluir um mês de dados de cada vez. Portanto, os comandos podem parecer assim:

   ```
   CREATE TABLE measurement_y2006m02 PARTITION OF measurement
       FOR VALUES FROM ('2006-02-01') TO ('2006-03-01');

   CREATE TABLE measurement_y2006m03 PARTITION OF measurement
       FOR VALUES FROM ('2006-03-01') TO ('2006-04-01');

   ...
   CREATE TABLE measurement_y2007m11 PARTITION OF measurement
       FOR VALUES FROM ('2007-11-01') TO ('2007-12-01');

   CREATE TABLE measurement_y2007m12 PARTITION OF measurement
       FOR VALUES FROM ('2007-12-01') TO ('2008-01-01')
       TABLESPACE fasttablespace;

   CREATE TABLE measurement_y2008m01 PARTITION OF measurement
       FOR VALUES FROM ('2008-01-01') TO ('2008-02-01')
       WITH (parallel_workers = 4)
       TABLESPACE fasttablespace;
   ```

(Lembre-se de que as partições adjacentes podem compartilhar um valor limite, uma vez que os limites superiores de intervalo são tratados como limites exclusivos.)

Se você deseja implementar subpartição, especifique novamente a cláusula `PARTITION BY` nos comandos usados para criar partições individuais, por exemplo:

   ```
   CREATE TABLE measurement_y2006m02 PARTITION OF measurement
       FOR VALUES FROM ('2006-02-01') TO ('2006-03-01')
       PARTITION BY RANGE (peaktemp);
   ```

Após a criação de partições de `measurement_y2006m02`, quaisquer dados inseridos em `measurement` que estejam mapeados para `measurement_y2006m02` (ou dados que estejam diretamente inseridos em `measurement_y2006m02`, o que é permitido desde que a restrição de partição seja atendida) serão redirecionados para uma de suas partições com base na coluna `peaktemp`. A chave de partição especificada pode sobrepor-se à chave de partição do pai, embora se deva ter cuidado ao especificar os limites de uma subpartição de modo que o conjunto de dados que ela aceita constitua um subconjunto do que os próprios limites da partição permitem; o sistema não tenta verificar se isso realmente é o caso.

Inserir dados na tabela principal que não correspondem a uma das partições existentes causará um erro; uma partição apropriada deve ser adicionada manualmente.

Não é necessário criar manualmente restrições de tabela que descrevam as condições de limite de partição para as partições. Tais restrições serão criadas automaticamente. 3. Crie um índice na(s) coluna(s) chave, bem como quaisquer outros índices que você queira, na tabela particionada. (O índice chave não é estritamente necessário, mas na maioria dos cenários é útil.) Isso cria automaticamente um índice correspondente em cada partição, e quaisquer partições que você criar ou anexar posteriormente também terão tal índice. Um índice ou restrição única declarada em uma tabela particionada é "virtual" da mesma maneira que a tabela particionada: os dados reais estão em índices filhos nas tabelas de partição individuais.

4. Certifique-se de que o parâmetro de configuração [enable_partition_pruning](runtime-config-query.md#GUC-ENABLE-PARTITION-PRUNING) não esteja desativado em `postgresql.conf`. Se estiver desativado, as consultas não serão otimizadas conforme desejado.

No exemplo acima, criaria uma nova partição a cada mês, então seria sábio escrever um script que gere o DDL necessário automaticamente.

#### 5.12.2.2. Manutenção de Partições [#](#DDL-PARTITIONING-DECLARATIVE-MAINTENANCE)

Normalmente, o conjunto de partições estabelecido ao definir a tabela inicialmente não é destinado a permanecer estático. É comum querer remover partições que contêm dados antigos e, periodicamente, adicionar novas partições para novos dados. Uma das vantagens mais importantes da partição é justamente permitir que essa tarefa, que de outra forma seria dolorosa, seja executada quase instantaneamente, manipulando a estrutura da partição, em vez de mover fisicamente grandes quantidades de dados.

A opção mais simples para remover dados antigos é descartar a partição que não é mais necessária:

```
DROP TABLE measurement_y2006m02;
```

Isso pode muito rapidamente excluir milhões de registros, pois não precisa excluir individualmente cada registro. No entanto, é importante notar que o comando acima exige a aquisição de um bloqueio `ACCESS EXCLUSIVE` na tabela pai.

Outra opção que é frequentemente preferível é remover a partição da tabela particionada, mas manter o acesso a ela como uma tabela em si mesma. Isso tem duas formas:

```
ALTER TABLE measurement DETACH PARTITION measurement_y2006m02;
ALTER TABLE measurement DETACH PARTITION measurement_y2006m02 CONCURRENTLY;
```

Esses permitem que operações adicionais sejam realizadas nos dados antes de serem descartados. Por exemplo, muitas vezes é um momento útil para fazer backup dos dados usando `COPY`, pg_dump ou ferramentas semelhantes. Também pode ser um momento útil para agregar dados em formatos menores, realizar outras manipulações de dados ou executar relatórios. A primeira forma do comando requer um `ACCESS EXCLUSIVE` bloqueio na tabela pai. Adicionar o qualificador `CONCURRENTLY` como na segunda forma permite que a operação de desacoplamento exija apenas `SHARE UPDATE EXCLUSIVE` bloqueio na tabela pai, mas consulte [`ALTER TABLE ... DETACH PARTITION`(sql-altertable.md#SQL-ALTERTABLE-DETACH-PARTITION) para detalhes sobre as restrições.

Da mesma forma, podemos adicionar uma nova partição para lidar com novos dados. Podemos criar uma partição vazia na tabela particionada, assim como as partições originais foram criadas acima:

```
CREATE TABLE measurement_y2008m02 PARTITION OF measurement
    FOR VALUES FROM ('2008-02-01') TO ('2008-03-01')
    TABLESPACE fasttablespace;
```

Como alternativa à criação de uma nova partição, às vezes é mais conveniente criar uma nova tabela separada da estrutura da partição e anexá-la posteriormente como uma partição. Isso permite que novos dados sejam carregados, verificados e transformados antes de aparecerem na tabela particionada. Além disso, a operação `ATTACH PARTITION` requer apenas um bloqueio `SHARE UPDATE EXCLUSIVE` na tabela particionada, em vez do bloqueio `ACCESS EXCLUSIVE` exigido por `CREATE TABLE ... PARTITION OF`, portanto, é mais amigável para operações concorrentes na tabela particionada; consulte [`ALTER TABLE ... ATTACH PARTITION`](sql-altertable.md#SQL-ALTERTABLE-ATTACH-PARTITION) para detalhes adicionais. A opção [`CREATE TABLE ... LIKE`](sql-createtable.md#SQL-CREATETABLE-PARMS-LIKE) pode ser útil para evitar a repetição tediosa da definição da tabela pai; por exemplo:

```
CREATE TABLE measurement_y2008m02
  (LIKE measurement INCLUDING DEFAULTS INCLUDING CONSTRAINTS)
  TABLESPACE fasttablespace;

ALTER TABLE measurement_y2008m02 ADD CONSTRAINT y2008m02
   CHECK ( logdate >= DATE '2008-02-01' AND logdate < DATE '2008-03-01' );

\copy measurement_y2008m02 from 'measurement_y2008m02'
-- possibly some other data preparation work

ALTER TABLE measurement ATTACH PARTITION measurement_y2008m02
    FOR VALUES FROM ('2008-02-01') TO ('2008-03-01' );
```

Observe que, ao executar o comando `ATTACH PARTITION`, a tabela será verificada para validar a restrição de partição enquanto mantém um bloqueio `ACCESS EXCLUSIVE` naquela partição. Como mostrado acima, é recomendável evitar essa verificação ao criar uma restrição `CHECK` que corresponda à restrição de partição esperada na tabela antes de anexá-la. Uma vez que o `ATTACH PARTITION` esteja concluído, é recomendável descartar a restrição `CHECK` agora redundante. Se a tabela que está sendo anexada for ela mesma uma tabela particionada, então cada uma de suas sub-partições será bloqueada e verificada recursivamente até que seja encontrada uma restrição `CHECK` adequada ou até que as partições de folha sejam alcançadas.

Da mesma forma, se a tabela dividida tiver uma partição `DEFAULT`, recomenda-se criar uma restrição `CHECK` que exclua a restrição da partição a ser anexada. Se isso não for feito, a partição `DEFAULT` será verificada para verificar se não contém registros que devem ser localizados na partição a ser anexada. Essa operação será realizada enquanto se mantém um bloqueio `ACCESS EXCLUSIVE` na partição `DEFAULT`. Se a partição `DEFAULT` for ela mesma uma tabela dividida, cada uma de suas partições será verificada recursivamente da mesma maneira que a tabela a ser anexada, conforme mencionado acima.

Como mencionado anteriormente, é possível criar índices em tabelas particionadas para que sejam aplicados automaticamente em toda a hierarquia. Isso pode ser muito conveniente, pois não apenas todas as partições existentes serão indexadas, mas também quaisquer partições futuras. No entanto, uma limitação ao criar novos índices em tabelas particionadas é que não é possível usar o qualificador `CONCURRENTLY`, o que pode levar a tempos de bloqueio longos. Para evitar isso, você pode usar a tabela particionada `CREATE INDEX ON ONLY`, que cria o novo índice marcado como inválido, impedindo a aplicação automática em partições existentes. Em vez disso, os índices podem então ser criados individualmente em cada partição usando `CONCURRENTLY` e *atados* ao índice particionado no pai usando `ALTER INDEX ... ATTACH PARTITION`. Uma vez que os índices para todas as partições sejam anexados ao índice do pai, o índice do pai será marcado como válido automaticamente. Exemplo:

```
CREATE INDEX measurement_usls_idx ON ONLY measurement (unitsales);

CREATE INDEX CONCURRENTLY measurement_usls_200602_idx
    ON measurement_y2006m02 (unitsales);
ALTER INDEX measurement_usls_idx
    ATTACH PARTITION measurement_usls_200602_idx;
...
```

Essa técnica pode ser usada com as restrições `UNIQUE` e `PRIMARY KEY`; os índices são criados implicitamente quando a restrição é criada. Exemplo:

```
ALTER TABLE ONLY measurement ADD UNIQUE (city_id, logdate);

ALTER TABLE measurement_y2006m02 ADD UNIQUE (city_id, logdate);
ALTER INDEX measurement_city_id_logdate_key
    ATTACH PARTITION measurement_y2006m02_city_id_logdate_key;
...
```

#### 5.12.2.3. Limitações [#](#DDL-PARTITIONING-DECLARATIVE-LIMITATIONS)

As seguintes limitações se aplicam a tabelas particionadas:

* Para criar uma restrição de chave primária ou única em uma tabela particionada, as chaves de particionamento não devem incluir expressões ou chamadas de função, e as colunas da restrição devem incluir todas as colunas das chaves de particionamento. Essa limitação existe porque os índices individuais que compõem a restrição só podem impor diretamente a unicidade dentro de suas próprias particionamentos; portanto, a própria estrutura de particionamento deve garantir que não haja duplicatas em diferentes particionamentos.
* Da mesma forma, uma restrição de exclusão deve incluir todas as colunas das chaves de particionamento. Além disso, a restrição deve comparar essas colunas para igualdade (não, por exemplo, `&&`). Novamente, essa limitação decorre da incapacidade de impor restrições entre particionamentos. A restrição pode incluir colunas adicionais que não fazem parte da chave de particionamento, e pode comparar essas colunas com qualquer operador que você desejar.
* Os gatilhos `BEFORE ROW` em `INSERT` não podem alterar qual particionamento é o destino final para uma nova linha.
* Misturar relações temporárias e permanentes na mesma árvore de particionamento não é permitido. Portanto, se a tabela particionada é permanente, suas particionamentos também devem ser permanentes e, da mesma forma, se a tabela particionada é temporária. Ao usar relações temporárias, todos os membros da árvore de particionamento devem ser da mesma sessão.

As partições individuais são vinculadas à sua tabela particionada usando herança nos bastidores. No entanto, não é possível usar todas as características genéricas da herança com tabelas declarativamente particionadas ou suas partições, conforme discutido abaixo. Notavelmente, uma partição não pode ter nenhum dos pais, exceto a tabela particionada da qual é uma partição, e uma tabela também não pode herdar tanto de uma tabela particionada quanto de uma tabela regular. Isso significa que as tabelas particionadas e suas partições nunca compartilham uma hierarquia de herança com tabelas regulares.

Como uma hierarquia de partição que consiste na tabela particionada e suas partições ainda é uma hierarquia de herança, `tableoid` e todas as regras normais de herança se aplicam conforme descrito em [Seção 5.11][(ddl-inherit.md "5.11. Inheritance")], com algumas exceções:

* As partições não podem ter colunas que não estejam presentes no banco de dados principal. Não é possível especificar colunas ao criar partições com `CREATE TABLE`, e também não é possível adicionar colunas às partições posteriormente usando `ALTER TABLE`. As tabelas podem ser adicionadas como partições com `ALTER TABLE ... ATTACH PARTITION` apenas se suas colunas corresponderem exatamente ao banco de dados principal.
* As restrições `CHECK` e `NOT NULL` de uma tabela particionada são sempre herdadas por todas as suas partições; não é permitido criar restrições `NO INHERIT` desses tipos. Não é possível excluir uma restrição desses tipos se a mesma restrição estiver presente na tabela principal.
* Usar `ONLY` para adicionar ou excluir uma restrição apenas na tabela particionada é suportado, desde que não existam partições. Uma vez que as partições existam, o uso de `ONLY` resultará em um erro para quaisquer restrições, exceto `UNIQUE` e `PRIMARY KEY`. Em vez disso, as restrições próprias das partições podem ser adicionadas e (se não estiverem presentes na tabela principal) excluídas.
* Como uma tabela particionada não tem dados próprios, as tentativas de usar `TRUNCATE` `ONLY` em uma tabela particionada sempre retornarão um erro.

### 5.12.3. Partição usando Herança [#](#DDL-PARTITIONING-USING-INHERITANCE)

Embora a partição declarativa integrada seja adequada para a maioria dos casos de uso comuns, há algumas circunstâncias em que uma abordagem mais flexível pode ser útil. A partição pode ser implementada usando a herança de tabela, que permite várias funcionalidades que não são suportadas pela partição declarativa, como:

* Para o particionamento declarativo, as partições devem ter exatamente o mesmo conjunto de colunas que a tabela particionada, enquanto que com a herança de tabela, as tabelas filhas podem ter colunas extras que não estão presentes no pai.
* A herança de tabela permite a herança múltipla.
* O particionamento declarativo só suporta particionamento de intervalo, lista e hash, enquanto que a herança de tabela permite que os dados sejam divididos da maneira que o usuário escolhe. (Observe, no entanto, que se a exclusão de restrição não for capaz de podar as tabelas filhas de forma eficaz, o desempenho da consulta pode ser ruim.)

#### 5.12.3.1. Exemplo [#](#DDL-PARTITIONING-INHERITANCE-EXAMPLE)

Este exemplo constrói uma estrutura de partição equivalente ao exemplo de partição declarativa acima. Use as seguintes etapas:

1. Crie a tabela "raiz", da qual todas as tabelas "filhos" irão herdar. Esta tabela não conterá dados. Não defina nenhuma restrição de verificação nesta tabela, a menos que você pretenda aplicá-la igualmente a todas as tabelas filhas. Também não há sentido em definir quaisquer índices ou restrições exclusivas nela. Para nosso exemplo, a tabela raiz é a tabela `measurement` conforme definida originalmente:

```
   CREATE TABLE measurement (
       city_id         int not null,
       logdate         date not null,
       peaktemp        int,
       unitsales       int
   );
   ``` 2. Crie várias tabelas "filhas" que cada uma herde da tabela raiz. Normalmente, essas tabelas não adicionarão nenhuma coluna ao conjunto herdado da raiz. Assim como na partição declarativa, essas tabelas são, em todos os aspectos, tabelas normais do PostgreSQL (ou tabelas estrangeiras).

```
   CREATE TABLE measurement_y2006m02 () INHERITS (measurement);
   CREATE TABLE measurement_y2006m03 () INHERITS (measurement);
   ...
   CREATE TABLE measurement_y2007m11 () INHERITS (measurement);
   CREATE TABLE measurement_y2007m12 () INHERITS (measurement);
   CREATE TABLE measurement_y2008m01 () INHERITS (measurement);
   ``` 3. Adicione restrições de tabela não sobrepostas às tabelas filhas para definir os valores de chave permitidos em cada uma.

Exemplos típicos seriam:

   ```
   CHECK ( x = 1 )
   CHECK ( county IN ( 'Oxfordshire', 'Buckinghamshire', 'Warwickshire' ))
   CHECK ( outletID >= 100 AND outletID < 200 )
   ```

Certifique-se de que as restrições garantam que não haja sobreposição entre os valores-chave permitidos em diferentes tabelas filhas. Um erro comum é configurar restrições de intervalo como:

   ```
   CHECK ( outletID BETWEEN 100 AND 200 )
   CHECK ( outletID BETWEEN 200 AND 300 )
   ```

Isso está errado, pois não está claro em qual tabela de crianças o valor da chave 200 pertence. Em vez disso, os intervalos devem ser definidos neste estilo:

```
   CREATE TABLE measurement_y2006m02 (
       CHECK ( logdate >= DATE '2006-02-01' AND logdate < DATE '2006-03-01' )
   ) INHERITS (measurement);

   CREATE TABLE measurement_y2006m03 (
       CHECK ( logdate >= DATE '2006-03-01' AND logdate < DATE '2006-04-01' )
   ) INHERITS (measurement);

   ...
   CREATE TABLE measurement_y2007m11 (
       CHECK ( logdate >= DATE '2007-11-01' AND logdate < DATE '2007-12-01' )
   ) INHERITS (measurement);

   CREATE TABLE measurement_y2007m12 (
       CHECK ( logdate >= DATE '2007-12-01' AND logdate < DATE '2008-01-01' )
   ) INHERITS (measurement);

   CREATE TABLE measurement_y2008m01 (
       CHECK ( logdate >= DATE '2008-01-01' AND logdate < DATE '2008-02-01' )
   ) INHERITS (measurement);
   ``` 4. Para cada tabela de crianças, crie um índice na(s) coluna(s) chave, bem como quaisquer outros índices que você queira.

5. Queremos que nossa aplicação possa dizer `INSERT INTO measurement ...` e que os dados sejam redirecionados para a tabela apropriada. Podemos organizar isso anexando uma função de gatilho adequada à tabela raiz. Se os dados serão adicionados apenas à última criança, podemos usar uma função de gatilho muito simples:

   ```
   CREATE OR REPLACE FUNCTION measurement_insert_trigger()
   RETURNS TRIGGER AS $$
   BEGIN
       INSERT INTO measurement_y2008m01 VALUES (NEW.*);
       RETURN NULL;
   END;
   $$
   LANGUAGE plpgsql;
   ```

Após criar a função, criamos um gatilho que chama a função de gatilho:

   ```
   CREATE TRIGGER insert_measurement_trigger
       BEFORE INSERT ON measurement
       FOR EACH ROW EXECUTE FUNCTION measurement_insert_trigger();
   ```

Devemos redefinir a função de gatilho a cada mês para que ela sempre se insira na tabela atual. A definição do gatilho, no entanto, não precisa ser atualizada.

Podemos querer inserir dados e fazer com que o servidor localize automaticamente a tabela secundária na qual a linha deve ser adicionada. Podemos fazer isso com uma função de gatilho mais complexa, por exemplo:

   ```
   CREATE OR REPLACE FUNCTION measurement_insert_trigger()
   RETURNS TRIGGER AS $$
   BEGIN
       IF ( NEW.logdate >= DATE '2006-02-01' AND
            NEW.logdate < DATE '2006-03-01' ) THEN
           INSERT INTO measurement_y2006m02 VALUES (NEW.*);
       ELSIF ( NEW.logdate >= DATE '2006-03-01' AND
               NEW.logdate < DATE '2006-04-01' ) THEN
           INSERT INTO measurement_y2006m03 VALUES (NEW.*);
       ...
       ELSIF ( NEW.logdate >= DATE '2008-01-01' AND
               NEW.logdate < DATE '2008-02-01' ) THEN
           INSERT INTO measurement_y2008m01 VALUES (NEW.*);
       ELSE
           RAISE EXCEPTION 'Date out of range.  Fix the measurement_insert_trigger() function!';
       END IF;
       RETURN NULL;
   END;
   $$
   LANGUAGE plpgsql;
   ```

A definição do gatilho é a mesma que antes. Observe que cada teste `IF` deve corresponder exatamente à restrição `CHECK` da sua tabela filho.

Embora essa função seja mais complexa do que o caso de um mês, não precisa ser atualizada com tanta frequência, uma vez que os ramos podem ser adicionados antes de serem necessários.

### Nota

Na prática, pode ser melhor verificar o filho mais novo primeiro, se a maioria dos registros for nesse filho. Por simplicidade, mostramos os testes do gatilho na mesma ordem que em outras partes deste exemplo.

Uma abordagem diferente para redirecionar insertos para a tabela infantil apropriada é configurar regras, em vez de um gatilho, na tabela raiz. Por exemplo:

   ```
   CREATE RULE measurement_insert_y2006m02 AS
   ON INSERT TO measurement WHERE
       ( logdate >= DATE '2006-02-01' AND logdate < DATE '2006-03-01' )
   DO INSTEAD
       INSERT INTO measurement_y2006m02 VALUES (NEW.*);
   ...
   CREATE RULE measurement_insert_y2008m01 AS
   ON INSERT TO measurement WHERE
       ( logdate >= DATE '2008-01-01' AND logdate < DATE '2008-02-01' )
   DO INSTEAD
       INSERT INTO measurement_y2008m01 VALUES (NEW.*);
   ```

Uma regra tem um overhead significativamente maior do que um gatilho, mas o overhead é pago uma vez por consulta em vez de uma vez por linha, então esse método pode ser vantajoso para situações de inserção em massa. Na maioria dos casos, no entanto, o método de gatilho oferecerá um melhor desempenho.

Tenha em atenção que `COPY` ignora as regras. Se quiser usar `COPY` para inserir dados, precisará copiar para a tabela correta da criança, em vez de diretamente na raiz. `COPY` aciona gatilhos, portanto, pode usá-lo normalmente se usar a abordagem de gatilho.

Outra desvantagem da abordagem de regras é que não há uma maneira simples de forçar um erro se o conjunto de regras não cobre a data de inserção; os dados irão silenciosamente para a tabela raiz.
6. Certifique-se de que o parâmetro de configuração [constraint_exclusion][(runtime-config-query.md#GUC-CONSTRAINT-EXCLUSION) não esteja desativado em `postgresql.conf`; caso contrário, as tabelas filhas podem ser acessadas desnecessariamente.

Como podemos ver, uma hierarquia de tabela complexa pode exigir uma quantidade substancial de DDL. No exemplo acima, criaria uma nova tabela secundária a cada mês, então pode ser sábio escrever um script que gere o DDL necessário automaticamente.

#### 5.12.3.2. Manutenção para Partição de Herança [#](#DDL-PARTITIONING-INHERITANCE-MAINTENANCE)

Para remover dados antigos rapidamente, basta descartar a tabela secundária que não é mais necessária:

```
DROP TABLE measurement_y2006m02;
```

Para remover a tabela de crianças da tabela de hierarquia de herança, mas manter o acesso a ela como uma tabela em si mesma:

```
ALTER TABLE measurement_y2006m02 NO INHERIT measurement;
```

Para adicionar uma nova tabela de filhos para lidar com novos dados, crie uma tabela de filhos vazia, assim como as crianças originais foram criadas acima:

```
CREATE TABLE measurement_y2008m02 (
    CHECK ( logdate >= DATE '2008-02-01' AND logdate < DATE '2008-03-01' )
) INHERITS (measurement);
```

Como alternativa, pode-se querer criar e povoar a nova tabela de filhos antes de adicioná-la à hierarquia da tabela. Isso pode permitir que os dados sejam carregados, verificados e transformados antes de serem tornados visíveis em consultas na tabela principal.

```
CREATE TABLE measurement_y2008m02
  (LIKE measurement INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
ALTER TABLE measurement_y2008m02 ADD CONSTRAINT y2008m02
   CHECK ( logdate >= DATE '2008-02-01' AND logdate < DATE '2008-03-01' );
\copy measurement_y2008m02 from 'measurement_y2008m02'
-- possibly some other data preparation work
ALTER TABLE measurement_y2008m02 INHERIT measurement;
```

#### 5.12.3.3. **Aviso [#](#DDL-PARTITIONING-INHERITANCE-CAVEATS)

As seguintes advertências se aplicam à partição implementada usando herança:

* Não há uma maneira automática de verificar se todas as restrições do `CHECK` são mutuamente exclusivas. É mais seguro criar código que gere tabelas filhas e crie e/ou modifique objetos associados do que escrever cada uma à mão.
* Índices e restrições de chave estrangeira se aplicam a tabelas individuais e não às suas crianças de herança, portanto, há alguns [[caveats]] que é preciso estar ciente.
* Os esquemas mostrados aqui assumem que os valores da(s) coluna(s) chave de uma linha nunca mudam, ou pelo menos não mudam o suficiente para exigir que ela mude para outra partição. Um `UPDATE` que tente fazer isso falhará devido às restrições do `CHECK`. Se você precisar lidar com tais casos, pode colocar gatilhos de atualização adequados nas tabelas filhas, mas isso torna a gestão da estrutura muito mais complicada.
* Os comandos manuais `VACUUM` e `ANALYZE` processarão automaticamente todas as tabelas filhas de herança. Se isso não for desejável, pode usar a palavra-chave `ONLY`. Um comando como:

  ```
  ANALYZE ONLY measurement;
  ```

apenas processará a tabela raiz.
* as declarações `INSERT` com cláusulas `ON CONFLICT` provavelmente não funcionarão conforme o esperado, pois a ação `ON CONFLICT` é realizada apenas em caso de violações únicas na relação de destino especificada, e não em suas relações filhas.
* serão necessárias gatilhos ou regras para encaminhar as linhas para a tabela filha desejada, a menos que o aplicativo esteja explicitamente ciente do esquema de particionamento. os gatilhos podem ser complicados de escrever e serão muito mais lentos do que o roteamento de tupla realizado internamente pelo particionamento declarativo.

### 5.12.4. Remoção de Partições [#](#DDL-PARTITION-PRUNING)

*O podamento de partição* é uma técnica de otimização de consulta que melhora o desempenho para tabelas declarativamente particionadas. Como exemplo:

```
SET enable_partition_pruning = on;                 -- the default
SELECT count(*) FROM measurement WHERE logdate >= DATE '2008-01-01';
```

Sem poda de partição, a consulta acima examinaria cada uma das partições da tabela `measurement`. Com a poda de partição habilitada, o planejador examinará a definição de cada partição e provará que a partição não precisa ser examinada porque ela não poderia conter quaisquer linhas que cumprissem a cláusula `WHERE` da consulta. Quando o planejador pode provar isso, ele exclui (*prona*) a partição do plano de consulta.

Usando o comando EXPLAIN e o parâmetro de configuração [enable_partition_pruning][(runtime-config-query.md#GUC-ENABLE-PARTITION-PRUNING)], é possível mostrar a diferença entre um plano para o qual as partições foram cortadas e outro para o qual elas não foram. Um plano típico não otimizado para esse tipo de configuração de tabela é:

```
SET enable_partition_pruning = off;
EXPLAIN SELECT count(*) FROM measurement WHERE logdate >= DATE '2008-01-01';
                                    QUERY PLAN
-------------------------------------------------------------------​----------------
 Aggregate  (cost=188.76..188.77 rows=1 width=8)
   ->  Append  (cost=0.00..181.05 rows=3085 width=0)
         ->  Seq Scan on measurement_y2006m02  (cost=0.00..33.12 rows=617 width=0)
               Filter: (logdate >= '2008-01-01'::date)
         ->  Seq Scan on measurement_y2006m03  (cost=0.00..33.12 rows=617 width=0)
               Filter: (logdate >= '2008-01-01'::date)
...
         ->  Seq Scan on measurement_y2007m11  (cost=0.00..33.12 rows=617 width=0)
               Filter: (logdate >= '2008-01-01'::date)
         ->  Seq Scan on measurement_y2007m12  (cost=0.00..33.12 rows=617 width=0)
               Filter: (logdate >= '2008-01-01'::date)
         ->  Seq Scan on measurement_y2008m01  (cost=0.00..33.12 rows=617 width=0)
               Filter: (logdate >= '2008-01-01'::date)
```

Algumas ou todas as partições podem usar varreduras de índice em vez de varreduras sequenciais completas da tabela, mas o ponto aqui é que não há necessidade de varredura das partições mais antigas para responder a essa consulta. Quando habilitamos o rastreamento de partições, obtemos um plano significativamente mais barato que fornecerá a mesma resposta:

```
SET enable_partition_pruning = on;
EXPLAIN SELECT count(*) FROM measurement WHERE logdate >= DATE '2008-01-01';
                                    QUERY PLAN
-------------------------------------------------------------------​----------------
 Aggregate  (cost=37.75..37.76 rows=1 width=8)
   ->  Seq Scan on measurement_y2008m01  (cost=0.00..33.12 rows=617 width=0)
         Filter: (logdate >= '2008-01-01'::date)
```

Observe que o recorte de partição é impulsionado apenas pelas restrições definidas implicitamente pelos chaves de partição, e não pela presença de índices. Portanto, não é necessário definir índices nas colunas da chave. Se um índice precisa ser criado para uma partição específica depende do fato de você esperar que as consultas que digitalizam a partição geralmente digitalizem uma grande parte da partição ou apenas uma pequena parte. Um índice será útil no último caso, mas não no primeiro.

O recorte de partições pode ser realizado não apenas durante o planejamento de uma consulta específica, mas também durante sua execução. Isso é útil, pois pode permitir que mais partições sejam recortadas quando as cláusulas contêm expressões cujos valores não são conhecidos no momento do planejamento da consulta, por exemplo, parâmetros definidos em uma declaração `PREPARE`, usando um valor obtido de uma subconsulta, ou usando um valor parametrizado no lado interno de uma junção de laço aninhado. O recorte de partições durante a execução pode ser realizado em qualquer um dos seguintes momentos:

* Durante a inicialização do plano de consulta. A poda de partições pode ser realizada aqui para valores de parâmetros que são conhecidos durante a fase de inicialização da execução. As partições que são podadas durante esta etapa não aparecerão no `EXPLAIN` ou no `EXPLAIN ANALYZE` da consulta. É possível determinar o número de partições que foram removidas durante esta fase observando a propriedade “Subplans Removedos” no `EXPLAIN` de saída. É importante notar que quaisquer partições removidas pela poda de partições realizada nesta etapa ainda estão bloqueadas no início da execução.
* Durante a execução real do plano de consulta. A poda de partições também pode ser realizada aqui para remover partições usando valores que são conhecidos apenas durante a execução real da consulta. Isso inclui valores de subconsultas e valores de parâmetros de tempo de execução, como os de junções de laço parametrizadas. Como o valor desses parâmetros pode mudar muitas vezes durante a execução da consulta, a poda de partições é realizada sempre que um dos parâmetros de execução sendo usado pela poda de partições muda. Determinar se partições foram podadas durante esta fase requer uma inspeção cuidadosa da propriedade `loops` no `EXPLAIN ANALYZE` de saída. Subplans correspondentes a diferentes partições podem ter diferentes valores para isso, dependendo de quantas vezes cada um deles foi podado durante a execução. Alguns podem ser mostrados como `(never executed)` se foram podados todas as vezes.

A poda de partição pode ser desativada usando a configuração [enable_partition_pruning][(runtime-config-query.md#GUC-ENABLE-PARTITION-PRUNING)].

### 5.12.5. Partição e Exclusão de Restrições [#](#DDL-PARTITIONING-CONSTRAINT-EXCLUSION)

*Exclusão de restrições* é uma técnica de otimização de consulta semelhante à poda de partição. Embora seja utilizada principalmente para partições implementadas usando o método de herança legítimo, ela pode ser usada para outros propósitos, incluindo partições declarativas.

A exclusão de restrições funciona de uma maneira muito semelhante à poda de partições, exceto que ela utiliza as restrições `CHECK` de cada tabela — que lhe dá seu nome — enquanto a poda de partições utiliza os limites de partição da tabela, que existem apenas no caso de partição declarativa. Outra diferença é que a exclusão de restrições é aplicada apenas no momento do plano; não há tentativa de remover as partições no momento da execução.

O fato de a exclusão de restrições usar restrições `CHECK`, o que a torna lenta em comparação com o corte de partições, às vezes pode ser usado como uma vantagem: porque as restrições podem ser definidas mesmo em tabelas declarativamente particionadas, além de seus limites internos de partição, a exclusão de restrições pode ser capaz de omitir partições adicionais do plano de consulta.

A configuração padrão (e recomendada) de [constraint_exclusion][(runtime-config-query.md#GUC-CONSTRAINT-EXCLUSION)] não é nem `on` nem `off`, mas uma configuração intermediária chamada `partition`, que faz com que a técnica seja aplicada apenas em consultas que provavelmente estão funcionando em tabelas particionadas de herança. A configuração `on` faz com que o planejador examine as restrições `CHECK` em todas as consultas, mesmo as simples que provavelmente não se beneficiarão.

As seguintes advertências se aplicam à exclusão de restrições:

* A exclusão de restrições é aplicada apenas durante o planejamento da consulta, ao contrário da poda de partições, que também pode ser aplicada durante a execução da consulta.
* A exclusão de restrições só funciona quando a cláusula `WHERE` da consulta contém constantes (ou parâmetros fornecidos externamente). Por exemplo, uma comparação com uma função não imutável, como `CURRENT_TIMESTAMP`, não pode ser otimizada, pois o planejador não pode saber em qual tabela filho o valor da função pode cair no momento da execução.
* Mantenha as restrições de partição simples, caso contrário, o planejador pode não ser capaz de provar que as tabelas filhas podem não precisar ser visitadas. Use condições de igualdade simples para partição de listas ou testes simples de intervalo para partição de intervalo, como ilustrado nos exemplos anteriores. Uma boa regra é que as restrições de partição devem conter apenas comparações da(s) coluna(s) de partição a constantes usando operadores indexáveis em árvore B, porque apenas as colunas indexáveis em árvore B são permitidas na chave de partição.
* Todas as restrições de todas as crianças da tabela principal são examinadas durante a exclusão de restrições, portanto, um grande número de crianças provavelmente aumentará consideravelmente o tempo de planejamento da consulta. Portanto, a partição com base na herança legítima funcionará bem com até talvez cem tabelas filhas; não tente usar muitas milhares de crianças.

### 5.12.6. Práticas recomendadas para particionamento declarativo [#](#DDL-PARTITIONING-DECLARATIVE-BEST-PRACTICES)

A escolha de como particionar uma tabela deve ser feita com cuidado, pois o desempenho do planejamento e execução de consultas pode ser negativamente afetado por um projeto inadequado.

Uma das decisões de design mais críticas será a coluna ou colunas pelas quais você particionará seus dados. Muitas vezes, a melhor escolha será particionar por coluna ou conjunto de colunas que apareçam com mais frequência nas cláusulas `WHERE` das consultas que serão executadas na tabela particionada. Cláusulas `WHERE` que são compatíveis com as restrições de limite de partição podem ser usadas para eliminar partições desnecessárias. No entanto, você pode ser forçado a tomar outras decisões devido aos requisitos para as restrições `PRIMARY KEY` ou `UNIQUE`. A remoção de dados indesejados também é um fator a considerar ao planejar sua estratégia de particionamento. Uma partição inteira pode ser deslocada rapidamente, portanto, pode ser benéfico projetar a estratégia de partição de tal forma que todos os dados que serão removidos de uma vez estejam localizados em uma única partição.

Escolher o número alvo de partições em que a tabela deve ser dividida também é uma decisão crítica a ser tomada. Não ter partições suficientes pode significar que os índices permanecem muito grandes e que a localização dos dados permanece pobre, o que pode resultar em baixas taxas de acerto de cache. No entanto, dividir a tabela em muitas partições também pode causar problemas. Muitas partições podem significar tempos de planejamento de consulta mais longos e maior consumo de memória durante o planejamento e execução da consulta, conforme descrito abaixo. Ao escolher como dividir sua tabela, também é importante considerar as mudanças que podem ocorrer no futuro. Por exemplo, se você optar por ter uma partição por cliente e atualmente tiver um pequeno número de clientes grandes, considere as implicações se, em vários anos, você se encontrar com um grande número de clientes pequenos. Neste caso, pode ser melhor escolher dividir por `HASH` e escolher um número razoável de partições, em vez de tentar dividir por `LIST` e esperar que o número de clientes não aumente além do que é prático para dividir os dados.

A subdivisão pode ser útil para dividir ainda mais as partições que se espera que se tornem maiores do que outras partições. Outra opção é usar a partição por intervalo com múltiplos colunas no chave de partição. Qualquer uma dessas opções pode facilmente levar a um número excessivo de partições, então é aconselhável ter moderação.

É importante considerar o overhead da partição durante o planejamento e execução da consulta. O planejador de consultas geralmente consegue lidar com hierarquias de partição com até alguns milhares de partições de forma bastante satisfatória, desde que as consultas típicas permitam que o planejador de consultas elimine todos, exceto um pequeno número de partições. Os tempos de planejamento se tornam mais longos e o consumo de memória se torna maior quando mais partições permanecem após o planejador realizar a poda de partições. Outra razão para se preocupar com um grande número de partições é que o consumo de memória do servidor pode crescer significativamente ao longo do tempo, especialmente se muitas sessões afetam um grande número de partições. Isso ocorre porque cada partição requer que seus metadados sejam carregados na memória local de cada sessão que a toca.

Com cargas de trabalho do tipo armazém de dados, pode fazer sentido usar um número maior de partições do que com uma carga de trabalho do tipo OLTP. Geralmente, em armazéns de dados, o tempo de planejamento de consultas é menos uma preocupação, pois a maioria do tempo de processamento é gasto durante a execução da consulta. Com qualquer um desses dois tipos de carga de trabalho, é importante tomar as decisões certas desde cedo, pois a re-partição de grandes quantidades de dados pode ser dolorosamente lenta. Simulações da carga de trabalho pretendida são frequentemente benéficas para otimizar a estratégia de partição. Nunca apenas assuma que mais partições são melhores do que menos partições, nem vice-versa.