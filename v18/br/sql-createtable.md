## Crie uma tabela

CREATE TABLE — definir uma nova tabela

## Sinopse

```
CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name ( [
  { column_name data_type [ STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT } ] [ COMPRESSION compression_method ] [ COLLATE collation ] [ column_constraint [ ... ] ]
    | table_constraint
    | LIKE source_table [ like_option ... ] }
    [, ... ]
] )
[ INHERITS ( parent_table [, ... ] ) ]
[ PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] ) ]
[ USING method ]
[ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE tablespace_name ]

CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name
    OF type_name [ (
  { column_name [ WITH OPTIONS ] [ column_constraint [ ... ] ]
    | table_constraint }
    [, ... ]
) ]
[ PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] ) ]
[ USING method ]
[ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE tablespace_name ]

CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name
    PARTITION OF parent_table [ (
  { column_name [ WITH OPTIONS ] [ column_constraint [ ... ] ]
    | table_constraint }
    [, ... ]
) ] { FOR VALUES partition_bound_spec | DEFAULT }
[ PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] ) ]
[ USING method ]
[ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE tablespace_name ]

where column_constraint is:

[ CONSTRAINT constraint_name ]
{ NOT NULL [ NO INHERIT ]  |
  NULL |
  CHECK ( expression ) [ NO INHERIT ] |
  DEFAULT default_expr |
  GENERATED ALWAYS AS ( generation_expr ) [ STORED | VIRTUAL ] |
  GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( sequence_options ) ] |
  UNIQUE [ NULLS [ NOT ] DISTINCT ] index_parameters |
  PRIMARY KEY index_parameters |
  REFERENCES reftable [ ( refcolumn ) ] [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ]
    [ ON DELETE referential_action ] [ ON UPDATE referential_action ] }
[ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ] [ ENFORCED | NOT ENFORCED ]

and table_constraint is:

[ CONSTRAINT constraint_name ]
{ CHECK ( expression ) [ NO INHERIT ] |
  NOT NULL column_name [ NO INHERIT ] |
  UNIQUE [ NULLS [ NOT ] DISTINCT ] ( column_name [, ... ] [, column_name WITHOUT OVERLAPS ] ) index_parameters |
  PRIMARY KEY ( column_name [, ... ] [, column_name WITHOUT OVERLAPS ] ) index_parameters |
  EXCLUDE [ USING index_method ] ( exclude_element WITH operator [, ... ] ) index_parameters [ WHERE ( predicate ) ] |
  FOREIGN KEY ( column_name [, ... ] [, PERIOD column_name ] ) REFERENCES reftable [ ( refcolumn [, ... ] [, PERIOD refcolumn ] ) ]
    [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ] [ ON DELETE referential_action ] [ ON UPDATE referential_action ] }
[ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ] [ ENFORCED | NOT ENFORCED ]

and like_option is:

{ INCLUDING | EXCLUDING } { COMMENTS | COMPRESSION | CONSTRAINTS | DEFAULTS | GENERATED | IDENTITY | INDEXES | STATISTICS | STORAGE | ALL }

and partition_bound_spec is:

IN ( partition_bound_expr [, ...] ) |
FROM ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] )
  TO ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] ) |
WITH ( MODULUS numeric_literal, REMAINDER numeric_literal )

index_parameters in UNIQUE, PRIMARY KEY, and EXCLUDE constraints are:

[ INCLUDE ( column_name [, ... ] ) ]
[ WITH ( storage_parameter [= value] [, ... ] ) ]
[ USING INDEX TABLESPACE tablespace_name ]

exclude_element in an EXCLUDE constraint is:

{ column_name | ( expression ) } [ COLLATE collation ] [ opclass [ ( opclass_parameter = value [, ... ] ) ] ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ]

referential_action in a FOREIGN KEY/REFERENCES constraint is:

{ NO ACTION | RESTRICT | CASCADE | SET NULL [ ( column_name [, ... ] ) ] | SET DEFAULT [ ( column_name [, ... ] ) ] }
```

## Descrição

`CREATE TABLE` criará uma nova tabela, inicialmente vazia, no banco de dados atual. A tabela será de propriedade do usuário que emite o comando.

Se um nome de esquema for fornecido (por exemplo, `CREATE TABLE myschema.mytable ...`) então a tabela é criada no esquema especificado. Caso contrário, ela é criada no esquema atual. As tabelas temporárias existem em um esquema especial, portanto, não pode ser fornecido um nome de esquema ao criar uma tabela temporária. O nome da tabela deve ser distinto do nome de qualquer outra relação (tabela, sequência, índice, visão, visão materializada ou tabela externa) no mesmo esquema.

`CREATE TABLE` também cria automaticamente um tipo de dados que representa o tipo composto correspondente a uma linha da tabela. Portanto, as tabelas não podem ter o mesmo nome que qualquer tipo de dados existente no mesmo esquema.

As cláusulas de restrição opcionais especificam restrições (testes) que as novas ou atualizadas linhas devem satisfazer para que uma operação de inserção ou atualização seja bem-sucedida. Uma restrição é um objeto SQL que ajuda a definir o conjunto de valores válidos na tabela de várias maneiras.

Existem duas maneiras de definir restrições: restrições de tabela e restrições de coluna. Uma restrição de coluna é definida como parte de uma definição de coluna. A definição de restrição de tabela não está ligada a uma coluna específica e pode abranger mais de uma coluna. Cada restrição de coluna também pode ser escrita como uma restrição de tabela; uma restrição de coluna é apenas uma conveniência de notação para uso quando a restrição afeta apenas uma coluna.

Para criar uma tabela, você deve ter o privilégio `USAGE` em todos os tipos de coluna ou o tipo na cláusula `OF`, respectivamente.

## Parâmetros

`TEMPORARY` ou `TEMP` [#](#SQL-CREATETABLE-TEMPORARY): Se especificado, a tabela é criada como uma tabela temporária. As tabelas temporárias são automaticamente descartadas no final de uma sessão, ou opcionalmente no final da transação atual (consulte `ON COMMIT` abaixo). O caminho de pesquisa padrão inclui o esquema temporário primeiro, e, portanto, as tabelas permanentes com nomes idênticos existentes não são escolhidas para novos planos enquanto a tabela temporária existir, a menos que sejam referenciadas com nomes qualificados por esquema. Quaisquer índices criados em uma tabela temporária também são temporários automaticamente.

O daemon [autovacuum][(routine-vacuuming.md#AUTOVACUUM "24.1.6. The Autovacuum Daemon")] não pode acessar e, portanto, não pode realizar a limpeza ou análise de tabelas temporárias. Por esse motivo, as operações adequadas de limpeza e análise devem ser realizadas por meio de comandos SQL de sessão. Por exemplo, se uma tabela temporária será usada em consultas complexas, é aconselhável executar `ANALYZE` na tabela temporária após ela ser preenchida.

Opcionalmente, `GLOBAL` ou `LOCAL` pode ser escrito antes de `TEMPORARY` ou `TEMP`. Isso atualmente não faz diferença no PostgreSQL e é descontinuado; veja [Compatibilidade][(sql-createtable.md#SQL-CREATETABLE-COMPATIBILITY "Compatibility")] abaixo.

`UNLOGGED` [#](#SQL-CREATETABLE-UNLOGGED): Se especificado, a tabela é criada como uma tabela não registrada. Os dados escritos em tabelas não registradas não são escritos no log de antecipação (consulte [Capítulo 28](wal.md "Chapter 28. Reliability and the Write-Ahead Log")), o que as torna consideravelmente mais rápidas do que as tabelas comuns. No entanto, elas não são seguras em caso de falha: uma tabela não registrada é automaticamente truncada após uma falha ou desligamento não limpo. O conteúdo de uma tabela não registrada também não é replicado para servidores de espera. Quaisquer índices criados em uma tabela não registrada também são automaticamente não registrados.

Se isso for especificado, quaisquer sequências criadas juntamente com a tabela não registrada (para colunas de identidade ou serial) também serão criadas como não registradas.

Este formulário não é suportado para tabelas particionadas.

`IF NOT EXISTS` [#](#SQL-CREATETABLE-PARMS-IF-NOT-EXISTS): Não exija um erro se uma relação com o mesmo nome já existir. Neste caso, é emitido um aviso. Observe que não há garantia de que a relação existente seja algo semelhante àquela que teria sido criada.

*`table_name`* [#](#SQL-CREATETABLE-PARMS-TABLE-NAME): O nome (opcionalmente qualificado por esquema) da tabela a ser criada.

`OF type_name` [#](#SQL-CREATETABLE-PARMS-TYPE-NAME): Cria uma *tabela tipificada*, que obtém sua estrutura do tipo composto específico especificado (ou seja, um criado usando [CREATE TYPE](sql-createtype.md "CREATE TYPE")) embora ainda produza um novo tipo composto. A tabela terá uma dependência no tipo referenciado, o que significa que ações alteradas e de eliminação em cascata nesse tipo se propagam para a tabela.

Uma tabela digitada sempre tem os mesmos nomes de colunas e tipos de dados que o tipo a partir do qual é derivada, portanto, você não pode especificar colunas adicionais. Mas o comando `CREATE TABLE` pode adicionar definições padrão e restrições à tabela, além de especificar parâmetros de armazenamento.

*`column_name`* [#](#SQL-CREATETABLE-PARMS-COLUMN-NAME): O nome da coluna a ser criada na nova tabela.

*`data_type`* [#](#SQL-CREATETABLE-PARMS-DATA-TYPE): O tipo de dados da coluna. Isso pode incluir especificadores de matriz. Para mais informações sobre os tipos de dados suportados pelo PostgreSQL, consulte [Capítulo 8](datatype.md "Chapter 8. Data Types").

`COLLATE collation` [#](#SQL-CREATETABLE-PARMS-COLLATE): A cláusula `COLLATE` atribui uma correção de texto à coluna (que deve ser de um tipo de dados correção de texto). Se não for especificado, o tipo de dados da coluna usa a correção de texto padrão.

`STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT }` [#](#SQL-CREATETABLE-PARMS-STORAGE): Este formulário define o modo de armazenamento para a coluna. Isso controla se esta coluna será mantida em linha ou em uma tabela secundária de TOAST, e se os dados devem ser comprimidos ou não. `PLAIN` deve ser usado para valores de comprimento fixo, como `integer` e é em linha, não comprimido. `MAIN` é para dados em linha, comprimíveis. `EXTERNAL` é para dados externos, não comprimidos, e `EXTENDED` é para dados externos, comprimidos. Escrever `DEFAULT` define o modo de armazenamento para o modo padrão para o tipo de dados da coluna. `EXTENDED` é o padrão para a maioria dos tipos de dados que suportam armazenamento não `PLAIN`. O uso de `EXTERNAL` fará com que as operações de subcadeia em valores muito grandes de `text` e `bytea` sejam executadas mais rapidamente, com a penalidade de aumento do espaço de armazenamento. Consulte [Seção 66.2](storage-toast.md "66.2. TOAST") para mais informações.

`COMPRESSION compression_method` [#](#SQL-CREATETABLE-PARMS-COMPRESSION): A cláusula `COMPRESSION` define o método de compressão para a coluna. A compressão é suportada apenas para tipos de dados de largura variável, e é usada apenas quando o modo de armazenamento da coluna é `main` ou `extended`. (Consulte [ALTER TABLE](sql-altertable.md "ALTER TABLE") para informações sobre os modos de armazenamento de coluna.) Definir essa propriedade para uma tabela particionada não tem efeito direto, porque tais tabelas não têm armazenamento próprio, mas o valor configurado será herdado por novas particionamentos. Os métodos de compressão suportados são `pglz` e `lz4`. (`lz4` está disponível apenas se `--with-lz4` foi usado ao construir o PostgreSQL.) Além disso, *`compression_method`* pode ser `default` para especificar explicitamente o comportamento padrão, que é consultar a configuração [default_toast_compression](runtime-config-client.md#GUC-DEFAULT-TOAST-COMPRESSION) no momento da inserção de dados para determinar o método a ser usado.

`INHERITS ( parent_table [, ... ] )` [#](#SQL-CREATETABLE-PARMS-INHERITS): A cláusula opcional `INHERITS` especifica uma lista de tabelas das quais a nova tabela herda automaticamente todas as colunas. As tabelas pai podem ser tabelas comuns ou tabelas estrangeiras.

O uso de `INHERITS` cria uma relação persistente entre a nova tabela de crianças e suas tabelas pai(s). As modificações do esquema das tabelas pai(s) normalmente se propagam para as crianças também, e, por padrão, os dados da tabela de crianças são incluídos em varreduras das tabelas pai(s).

Se o mesmo nome de coluna existir em mais de uma tabela pai, um erro será relatado, a menos que os tipos de dados das colunas correspondam em cada uma das tabelas pai. Se não houver conflito, as colunas duplicadas serão unidas para formar uma única coluna na nova tabela. Se a lista de nomes de coluna da nova tabela contiver um nome de coluna que também seja herdado, o tipo de dados também deve corresponder ao(s) colun(a)a herdado(s), e as definições das colunas serão unidas em uma. Se a nova tabela especificar explicitamente um valor padrão para a coluna, esse valor padrão substituirá quaisquer valores padrão das declarações herdadas da coluna. Caso contrário, quaisquer pais que especifiquem valores padrão para a coluna devem especificar todos os mesmos valores padrão, ou um erro será relatado.

As restrições `CHECK` são unidas de maneira essencialmente a mesma que as colunas: se várias tabelas pai e/ou a nova definição de tabela contiverem restrições `CHECK` com nomes idênticos, essas restrições devem ter todas a mesma expressão de verificação, ou um erro será relatado. As restrições com o mesmo nome e expressão serão unidas em uma cópia. Uma restrição marcada `NO INHERIT` em um pai não será considerada. Observe que uma restrição `CHECK` sem nome na nova tabela nunca será unida, uma vez que um nome único será sempre escolhido para ela.

As configurações da coluna `STORAGE` também são copiadas das tabelas parentais.

Se uma coluna na tabela principal for uma coluna de identidade, essa propriedade não é herdada. Uma coluna na tabela secundária pode ser declarada como coluna de identidade, se desejar.

`PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ opclass ] [, ...] )` [#](#SQL-CREATETABLE-PARMS-PARTITION-BY): A cláusula opcional `PARTITION BY` especifica uma estratégia de partição da tabela. A tabela assim criada é chamada de *tabela particionada*. A lista entre parênteses de colunas ou expressões forma o *chave de partição* para a tabela. Ao usar partição por intervalo ou hash, a chave de partição pode incluir múltiplas colunas ou expressões (até 32, mas esse limite pode ser alterado ao construir o PostgreSQL), mas para partição por lista, a chave de partição deve consistir em uma única coluna ou expressão.

A partição por faixa e a partição por lista exigem uma classe de operador btree, enquanto a partição por hash exige uma classe de operador de hash. Se nenhuma classe de operador for especificada explicitamente, a classe de operador padrão do tipo apropriado será usada; se nenhuma classe de operador padrão existir, um erro será gerado. Quando a partição por hash é usada, a classe de operador usada deve implementar a função de suporte 2 (consulte [Seção 36.16.3] para detalhes).

Uma tabela dividida é dividida em sub-tabelas (chamadas de partições), que são criadas usando comandos separados `CREATE TABLE`. A tabela dividida é em si vazia. Uma linha de dados inserida na tabela é encaminhada para uma partição com base no valor das colunas ou expressões na chave da partição. Se nenhuma partição existente corresponder aos valores da nova linha, um erro será relatado.

Veja [Seção 5.12][(ddl-partitioning.md "5.12. Table Partitioning")] para mais discussão sobre a partição de tabelas.

`PARTITION OF parent_table { FOR VALUES partition_bound_spec | DEFAULT }` [#](#SQL-CREATETABLE-PARTITION): Cria a tabela como uma *partição* da tabela especificado pai. A tabela pode ser criada como uma partição para valores específicos usando `FOR VALUES` ou como uma partição padrão usando `DEFAULT`. Quaisquer índices, restrições e gatilhos definidos pelo usuário em nível de linha que existem na tabela pai são clonados na nova partição.

O *`partition_bound_spec` deve corresponder ao método de particionamento e à chave de particionamento da tabela principal, e não deve sobrepor-se a nenhuma partição existente dessa tabela principal. O formulário com `IN` é usado para particionamento de lista, o formulário com `FROM` e `TO` é usado para particionamento de intervalo, e o formulário com `WITH` é usado para particionamento de hash.

*`partition_bound_expr`* é qualquer expressão sem variáveis (subconsultas, funções de janela, funções agregadas e funções que retornam conjuntos não são permitidas). Seu tipo de dado deve corresponder ao tipo de dado da coluna correspondente à chave de partição. A expressão é avaliada uma vez no momento da criação da tabela, então ela pode até conter expressões voláteis, como `CURRENT_TIMESTAMP`.

Ao criar uma partição de lista, `NULL` pode ser especificado para indicar que a coluna do chave da partição pode ser nula. No entanto, não pode haver mais de uma partição de lista desse tipo para uma tabela-mãe dada. `NULL` não pode ser especificado para partições de intervalo.

Ao criar uma partição de intervalo, o limite inferior especificado com `FROM` é um limite inclusivo, enquanto o limite superior especificado com `TO` é um limite exclusivo. Ou seja, os valores especificados na lista de `FROM` são valores válidos das colunas de chave de partição correspondentes para esta partição, enquanto os da lista de `TO` não são. Note que esta declaração deve ser entendida de acordo com as regras de comparação por linha ([Seção 9.25.5](functions-comparisons.md#ROW-WISE-COMPARISON "9.25.5. Row Constructor Comparison")). Por exemplo, dado `PARTITION BY RANGE (x,y)`, uma fronteira de partição `FROM (1, 2) TO (3, 4)` permite `x=1` com qualquer `y>=2`, `x=2` com qualquer `y` não nulo e `x=3` com qualquer `y<4`.

Os valores especiais `MINVALUE` e `MAXVALUE` podem ser usados ao criar uma partição de intervalo para indicar que não há limite inferior ou superior no valor da coluna. Por exemplo, uma partição definida usando `FROM (MINVALUE) TO (10)` permite quaisquer valores menores que 10, e uma partição definida usando `FROM (10) TO (MAXVALUE)` permite quaisquer valores maiores ou iguais a 10.

Ao criar uma partição de intervalo que envolve mais de uma coluna, também pode fazer sentido usar `MAXVALUE` como parte do limite inferior e `MINVALUE` como parte do limite superior. Por exemplo, uma partição definida usando `FROM (0, MAXVALUE) TO (10, MAXVALUE)` permite quaisquer linhas onde o primeiro coluna da chave de partição é maior que 0 e menor ou igual a 10. Da mesma forma, uma partição definida usando `FROM ('a', MINVALUE) TO ('b', MINVALUE)` permite quaisquer linhas onde a primeira coluna da chave de partição começa com "a".

Observe que, se `MINVALUE` ou `MAXVALUE` for usado para uma coluna de um vínculo de particionamento, o mesmo valor deve ser usado para todas as colunas subsequentes. Por exemplo, `(10, MINVALUE, 0)` não é um vínculo válido; você deve escrever `(10, MINVALUE, MINVALUE)`.

Observe também que alguns tipos de elementos, como `timestamp`, têm uma noção de "infinito", que é apenas outro valor que pode ser armazenado. Isso é diferente de `MINVALUE` e `MAXVALUE`, que não são valores reais que podem ser armazenados, mas sim são maneiras de dizer que o valor é ilimitado. `MAXVALUE` pode ser considerado maior que qualquer outro valor, incluindo "infinito" e `MINVALUE` como sendo menor que qualquer outro valor, incluindo "menos infinito". Assim, a faixa `FROM ('infinity') TO (MAXVALUE)` não é uma faixa vazia; ela permite exatamente um valor ser armazenado — "infinito".

Se `DEFAULT` for especificado, a tabela será criada como a partição padrão da tabela pai. Esta opção não está disponível para tabelas com partição de hash. Um valor de chave de partição que não se encaixe em nenhuma outra partição do pai dado será encaminhado para a partição padrão.

Quando uma tabela tem uma partição existente `DEFAULT` e uma nova partição é adicionada a ela, a partição padrão deve ser verificada para verificar se ela não contém quaisquer linhas que pertencem adequadamente à nova partição. Se a partição padrão contiver um grande número de linhas, isso pode ser lento. O varrimento será ignorado se a partição padrão for uma tabela estrangeira ou se ela tiver uma restrição que comprove que ela não pode conter linhas que devem ser colocadas na nova partição.

Ao criar uma partição hash, um módulo e um resto devem ser especificados. O módulo deve ser um número inteiro positivo, e o resto deve ser um número inteiro não negativo menor que o módulo. Tipicamente, ao configurar inicialmente uma tabela com partição hash, você deve escolher um módulo igual ao número de partições e atribuir a cada tabela o mesmo módulo e um resto diferente (veja os exemplos abaixo). No entanto, não é necessário que cada partição tenha o mesmo módulo, apenas que cada módulo que ocorre entre as partições de uma tabela com partição hash seja um fator do módulo do próximo tamanho maior. Isso permite que o número de partições seja aumentado gradualmente sem precisar mover todos os dados de uma vez. Por exemplo, suponha que você tenha uma tabela com partição hash com 8 partições, cada uma com módulo 8, mas que ache necessário aumentar o número de partições para 16. Você pode separar uma das partições de módulo 8, criar duas novas partições de módulo 16 cobrindo a mesma porção do espaço de chave (uma com um resto igual ao resto da partição separada, e a outra com um resto igual a esse valor mais 8), e repopular essas partições com dados. Em seguida, você pode repetir isso -- talvez em um momento posterior -- para cada partição de módulo 8 até que nenhuma permaneça. Embora isso ainda possa envolver um grande movimento de dados em cada etapa, ainda é melhor do que ter que criar uma tabela inteira nova e mover todos os dados de uma vez.

Uma partição deve ter os mesmos nomes e tipos de coluna da tabela particionada à qual pertence. As modificações nos nomes ou tipos de coluna de uma tabela particionada serão automaticamente propagadas para todas as partições. As restrições `CHECK` serão herdadas automaticamente por todas as partições, mas uma partição individual pode especificar restrições adicionais `CHECK`; restrições adicionais com o mesmo nome e condição que no parâmetro pai serão mescladas com a restrição do parâmetro pai. Os valores padrão podem ser especificados separadamente para cada partição. Mas observe que o valor padrão de uma partição não é aplicado ao inserir uma tupla através de uma tabela particionada.

As linhas inseridas em uma tabela particionada serão automaticamente direcionadas para a partição correta. Se não existir uma partição adequada, ocorrerá um erro.

Operações como `TRUNCATE` que normalmente afetam uma tabela e todas as suas crianças de herança serão aplicadas a todas as partições, mas também podem ser realizadas em uma partição individual.

Observe que a criação de uma partição usando `PARTITION OF` requer a aquisição de um `ACCESS EXCLUSIVE` de bloqueio na tabela particionada pai. Da mesma forma, a remoção de uma partição com `DROP TABLE` requer a aquisição de um `ACCESS EXCLUSIVE` de bloqueio na tabela pai. É possível usar [`ALTER TABLE ATTACH/DETACH PARTITION`](sql-altertable.md "ALTER TABLE") para realizar essas operações com um bloqueio mais fraco, reduzindo assim a interferência em operações concorrentes na tabela particionada.

`LIKE source_table [ like_option ... ]` [#](#SQL-CREATETABLE-PARMS-LIKE): A cláusula `LIKE` especifica uma tabela a partir da qual a nova tabela copia automaticamente todos os nomes de coluna, seus tipos de dados e suas restrições não nulos.

Ao contrário de `INHERITS`, a nova tabela e a tabela original são completamente desacopladas após a conclusão da criação. Alterações na tabela original não serão aplicadas à nova tabela, e não é possível incluir dados da nova tabela em varreduras da tabela original.

Além disso, ao contrário de `INHERITS`, as colunas e restrições copiadas por `LIKE` não são mescladas com colunas e restrições com nomes semelhantes. Se o mesmo nome for especificado explicitamente ou em outra cláusula `LIKE`, um erro é sinalizado.

As cláusulas opcionais *`like_option`* especificam quais propriedades adicionais da tabela original devem ser copiadas. Especificar `INCLUDING` copia a propriedade, omitindo `EXCLUDING` a propriedade. `EXCLUDING` é o padrão. Se várias especificações forem feitas para o mesmo tipo de objeto, a última é usada. As opções disponíveis são:

`INCLUDING COMMENTS` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-COMMENTS) : Os comentários das colunas copiadas, as restrições de verificação, as restrições não nulos, os índices e as estatísticas extensas serão copiados. O comportamento padrão é excluir os comentários, resultando nos objetos correspondentes na nova tabela sem comentários.

`INCLUDING COMPRESSION` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-COMPRESSION) : O método de compressão das colunas será copiado. O comportamento padrão é excluir os métodos de compressão, resultando em colunas com o método de compressão padrão.

`INCLUDING CONSTRAINTS` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-CONSTRAINTS) :   As restrições `CHECK` serão copiadas. Não há distinção entre restrições de coluna e restrições de tabela. As restrições não nulos são sempre copiadas para a nova tabela.

`INCLUDING DEFAULTS` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-DEFAULTS) : As expressões padrão para as definições de colunas copiadas serão copiadas. Caso contrário, as expressões padrão não serão copiadas, resultando em colunas copiadas na nova tabela com valores padrão nulos. Observe que a cópia de valores padrão que chamam funções de modificação de banco de dados, como `nextval`, pode criar uma ligação funcional entre as tabelas original e nova.

`INCLUDING GENERATED` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-GENERATED) :   Todas as expressões de geração, bem como a escolha armazenada/virtual das definições de coluna copiadas serão copiadas. Por padrão, as novas colunas serão colunas regulares de base.

`INCLUDING IDENTITY` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-IDENTITY) :   Todas as especificações de identidade das definições de coluna copiadas serão copiadas. Uma nova sequência é criada para cada coluna de identidade da nova tabela, separada das sequências associadas à tabela antiga.

`INCLUDING INDEXES` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-INDEXES) : Os índices, as restrições `PRIMARY KEY`, `UNIQUE` e `EXCLUDE` da tabela original serão criados na nova tabela. Os nomes dos novos índices e restrições são escolhidos de acordo com as regras padrão, independentemente de como os originais foram nomeados. (Esse comportamento evita possíveis falhas de nome duplicado para os novos índices.)

`INCLUDING STATISTICS` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-STATISTICS) : As estatísticas extensas são copiadas para a nova tabela.

`INCLUDING STORAGE` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-STORAGE) : As configurações das definições das colunas copiadas serão copiadas. O comportamento padrão é excluir as configurações de `STORAGE`, resultando nas colunas copiadas na nova tabela com configurações padrão específicas do tipo. Para mais informações sobre as configurações de `STORAGE`, consulte [Seção 66.2](storage-toast.md "66.2. TOAST").

`INCLUDING ALL` [#](#SQL-CREATETABLE-PARMS-LIKE-OPT-ALL) :   `INCLUDING ALL` é uma forma abreviada que seleciona todas as opções individuais disponíveis. (Poderia ser útil escrever cláusulas individuais `EXCLUDING` após `INCLUDING ALL` para selecionar todas, exceto algumas opções específicas.)

A cláusula `LIKE` também pode ser usada para copiar definições de coluna a partir de visualizações, tabelas externas ou tipos compostos. Opções inapropriadas (por exemplo, `INCLUDING INDEXES` de uma visualização) são ignoradas.

`CONSTRAINT constraint_name` [#](#SQL-CREATETABLE-PARMS-CONSTRAINT): Um nome opcional para uma coluna ou restrição de tabela. Se a restrição for violada, o nome da restrição está presente nas mensagens de erro, então nomes de restrição como `col must be positive` podem ser usados para comunicar informações úteis sobre a restrição para aplicativos de cliente. (As aspas duplas são necessárias para especificar nomes de restrição que contenham espaços.) Se um nome de restrição não for especificado, o sistema gera um nome.

`NOT NULL [ NO INHERIT ]` [#](#SQL-CREATETABLE-PARMS-NOT-NULL): A coluna não pode conter valores nulos.

Uma restrição marcada com `NO INHERIT` não se propagará para as tabelas filhas.

`NULL` [#](#SQL-CREATETABLE-PARMS-NULL): A coluna pode conter valores nulos. Esse é o padrão.

Esta cláusula é fornecida apenas para compatibilidade com bancos de dados SQL não padrão. Seu uso é desencorajado em novas aplicações.

`CHECK ( expression ) [ NO INHERIT ]` [#](#SQL-CREATETABLE-PARMS-CHECK): A cláusula `CHECK` especifica uma expressão que produz um resultado booleano que as novas ou atualizadas linhas devem satisfazer para que uma operação de inserção ou atualização seja bem-sucedida. As expressões que avaliam como VERDADEIRO ou DESCONHECIDO são bem-sucedidas. Se qualquer linha de uma operação de inserção ou atualização produzir um resultado FALSO, uma exceção de erro é levantada e a inserção ou atualização não altera o banco de dados. Uma restrição de verificação especificada como uma restrição de coluna deve referenciar apenas o valor daquela coluna, enquanto uma expressão que aparece em uma restrição de tabela pode referenciar múltiplas colunas.

Atualmente, as expressões `CHECK` não podem conter subconsultas nem referir-se a variáveis que não sejam colunas da linha atual (consulte [Seção 5.5.1][(ddl-constraints.md#DDL-CONSTRAINTS-CHECK-CONSTRAINTS "5.5.1. Check Constraints")]). A coluna do sistema `tableoid` pode ser referenciada, mas não qualquer outra coluna do sistema.

Uma restrição marcada com `NO INHERIT` não se propagará para as tabelas filhas.

Quando uma tabela tiver múltiplas restrições `CHECK`, elas serão testadas para cada linha em ordem alfabética por nome, após a verificação das restrições `NOT NULL`. (As versões do PostgreSQL anteriores a 9.5 não respeitavam qualquer ordem específica de disparo para as restrições `CHECK`.

`DEFAULT default_expr` [#](#SQL-CREATETABLE-PARMS-DEFAULT): A cláusula `DEFAULT` atribui um valor de dados padrão para a coluna cuja definição de coluna ela aparece dentro. O valor é qualquer expressão livre de variáveis (em particular, referências cruzadas para outras colunas na tabela atual não são permitidas). Subconsultas também não são permitidas. O tipo de dados da expressão padrão deve corresponder ao tipo de dados da coluna.

A expressão padrão será usada em qualquer operação de inserção que não especifique um valor para a coluna. Se não houver um padrão para uma coluna, então o padrão é nulo.

`GENERATED ALWAYS AS ( generation_expr ) [ STORED | VIRTUAL ]` [#](#SQL-CREATETABLE-PARMS-GENERATED-STORED): Esta cláusula cria a coluna como uma *coluna gerada*. A coluna não pode ser escrita e, ao ser lida, o resultado da expressão especificada será retornado.

Quando `VIRTUAL` é especificado, a coluna será calculada quando ela for lida e não ocupará nenhum armazenamento. Quando `STORED` é especificado, a coluna será calculada na escrita e será armazenada no disco. `VIRTUAL` é o padrão.

A expressão de geração pode se referir a outras colunas na tabela, mas não a outras colunas geradas. Quaisquer funções e operadores utilizados devem ser imutáveis. Não são permitidas referências a outras tabelas.

Uma coluna gerada virtualmente não pode ter um tipo definido pelo usuário, e a expressão de geração de uma coluna gerada virtualmente não pode fazer referência a funções ou tipos definidos pelo usuário, ou seja, ela pode usar apenas funções ou tipos embutidos. Isso também se aplica indiretamente, como para funções ou tipos que subjazem a operadores ou tipos de conversão. (Essa restrição não existe para colunas geradas armazenadas.)

`GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( sequence_options ) ]` [#](#SQL-CREATETABLE-PARMS-GENERATED-IDENTITY): Esta cláusula cria a coluna como uma coluna de identidade. Ela terá uma sequência implícita anexada a ela e, em linhas recém-inseridas, a coluna terá automaticamente valores da sequência atribuídos a ela. Tal coluna é implicitamente `NOT NULL`.

As cláusulas `ALWAYS` e `BY DEFAULT` determinam como os valores especificados explicitamente pelo usuário são tratados nos comandos `INSERT` e `UPDATE`.

Em um comando `INSERT`, se `ALWAYS` for selecionado, um valor especificado pelo usuário é aceito apenas se a declaração `INSERT` especificar `OVERRIDING SYSTEM VALUE`. Se `BY DEFAULT` for selecionado, então o valor especificado pelo usuário tem precedência. Veja [INSERT](sql-insert.md "INSERT") para detalhes. (No comando `COPY`, os valores especificados pelo usuário são sempre usados, independentemente desta configuração.)

Em um comando `UPDATE`, se `ALWAYS` for selecionado, qualquer atualização da coluna para qualquer valor que não seja `DEFAULT` será rejeitada. Se `BY DEFAULT` for selecionado, a coluna pode ser atualizada normalmente. (Não há cláusula `OVERRIDING` para o comando `UPDATE`.

A cláusula opcional *`sequence_options`* pode ser usada para substituir os parâmetros da sequência. As opções disponíveis incluem as mostradas para [CREATE SEQUENCE](sql-createsequence.md "CREATE SEQUENCE"), além de `SEQUENCE NAME name`, `LOGGED` e `UNLOGGED`, que permitem a seleção do nome e do nível de persistência da sequência. Sem `SEQUENCE NAME`, o sistema escolhe um nome não utilizado para a sequência. Sem `LOGGED` ou `UNLOGGED`, a sequência terá o mesmo nível de persistência que a tabela.

`UNIQUE [ NULLS [ NOT ] DISTINCT ]` (constrangimento de coluna) `UNIQUE [ NULLS [ NOT ] DISTINCT ] ( column_name [, ... ] [, column_name WITHOUT OVERLAPS ] )` [ `INCLUDE ( column_name [, ...])` ] (constrangimento de tabela) [#](#SQL-CREATETABLE-PARMS-UNIQUE): O constrangimento `UNIQUE` especifica que um grupo de uma ou mais colunas de uma tabela pode conter apenas valores únicos. O comportamento de um constrangimento de tabela único é o mesmo que o de um constrangimento de coluna única, com a capacidade adicional de abranger múltiplas colunas. Portanto, o constrangimento exige que quaisquer duas linhas devem diferir em pelo menos uma dessas colunas.

Se a opção `WITHOUT OVERLAPS` for especificada para a última coluna, então essa coluna é verificada quanto a sobreposições em vez de igualdade. Nesse caso, as outras colunas da restrição permitirão duplicatas, desde que as duplicatas não se sobreponham na coluna `WITHOUT OVERLAPS`. (Isso é às vezes chamado de chave temporal, se a coluna for uma faixa de datas ou timestamps, mas o PostgreSQL permite faixas sobre qualquer tipo de base.) Na verdade, tal restrição é aplicada com uma restrição `EXCLUDE` em vez de uma restrição `UNIQUE`. Portanto, por exemplo, `UNIQUE (id, valid_at WITHOUT OVERLAPS)` se comporta como `EXCLUDE USING GIST (id WITH =, valid_at WITH &&)`. A coluna `WITHOUT OVERLAPS` deve ter um tipo de faixa ou multifaixa. Faixas/multifaixas vazias não são permitidas. As colunas não `WITHOUT OVERLAPS` da restrição podem ser qualquer tipo que possa ser comparado quanto à igualdade em um índice GiST. Por padrão, apenas tipos de faixa são suportados, mas você pode usar outros tipos adicionando a extensão [btree_gist](btree-gist.md "F.8. btree_gist — GiST operator classes with B-tree behavior") (que é a maneira esperada de usar esse recurso).

Para fins de restrição única, os valores nulos não são considerados iguais, a menos que `NULLS NOT DISTINCT` seja especificado.

Cada restrição única deve nomear um conjunto de colunas que é diferente do conjunto de colunas nomeado por qualquer outra restrição de chave primária única definida para a tabela. (Caso contrário, as restrições únicas redundantes serão descartadas.)

Ao estabelecer uma restrição exclusiva para uma hierarquia de partição de vários níveis, todas as colunas na chave de partição da tabela alvo particionada, bem como as de todas as suas tabelas particionadas descendentes, devem ser incluídas na definição da restrição.

Adicionar uma restrição exclusiva criará automaticamente um índice btree exclusivo na coluna ou no grupo de colunas utilizadas na restrição. Mas se a restrição incluir uma cláusula `WITHOUT OVERLAPS`, ela usará um índice GiST. O índice criado tem o mesmo nome da restrição exclusiva.

A cláusula opcional `INCLUDE` adiciona a esse índice uma ou mais colunas que são simplesmente "carga": a unicidade não é aplicada nelas, e o índice não pode ser pesquisado com base nessas colunas. No entanto, elas podem ser recuperadas por uma varredura apenas com índice. Note que, embora a restrição não seja aplicada nas colunas incluídas, ela ainda depende delas. Consequentemente, algumas operações nessas colunas (por exemplo, `DROP COLUMN`) podem causar eliminação de restrição e índice em cascata.

`PRIMARY KEY` (constrangimento de coluna) `PRIMARY KEY ( column_name [, ... ] [, column_name WITHOUT OVERLAPS ] )` [ `INCLUDE ( column_name [, ...])` ] (constrangimento de tabela) [#](#SQL-CREATETABLE-PARMS-PRIMARY-KEY): O constrangimento `PRIMARY KEY` especifica que uma coluna ou colunas de uma tabela podem conter apenas valores únicos (não duplicados) e não nulos. Apenas uma chave primária pode ser especificada para uma tabela, seja como um constrangimento de coluna ou um constrangimento de tabela.

A restrição de chave primária deve nomear um conjunto de colunas que é diferente do conjunto de colunas nomeado por qualquer restrição única definida para a mesma tabela. (Caso contrário, a restrição única é redundante e será descartada.)

`PRIMARY KEY` aplica as mesmas restrições de dados que uma combinação de `UNIQUE` e `NOT NULL`. No entanto, identificar um conjunto de colunas como a chave primária também fornece metadados sobre o design do esquema, uma vez que uma chave primária implica que outras tabelas podem confiar nesse conjunto de colunas como um identificador único para as linhas.

Quando colocada em uma mesa dividida, as restrições de `PRIMARY KEY` compartilham as restrições descritas anteriormente para as restrições de `UNIQUE`.

A adição de uma restrição `PRIMARY KEY` criará automaticamente um índice btree único na coluna ou grupo de colunas utilizado na restrição, ou GiST se `WITHOUT OVERLAPS` foi especificado.

A cláusula opcional `INCLUDE` adiciona a esse índice uma ou mais colunas que são simplesmente "carga": a unicidade não é aplicada nelas, e o índice não pode ser pesquisado com base nessas colunas. No entanto, elas podem ser recuperadas por uma varredura apenas com índice. Note que, embora a restrição não seja aplicada nas colunas incluídas, ela ainda depende delas. Consequentemente, algumas operações nessas colunas (por exemplo, `DROP COLUMN`) podem causar eliminação de restrição e índice em cascata.

`EXCLUDE [ USING index_method ] ( exclude_element WITH operator [, ... ] ) index_parameters [ WHERE ( predicate ) ]` [#](#SQL-CREATETABLE-EXCLUDE): A cláusula `EXCLUDE` define uma restrição de exclusão, que garante que, se quaisquer duas linhas forem comparadas nas colunas ou expressões especificadas usando os operadores especificados, não todas essas comparações retornarão `TRUE`. Se todos os operadores especificados testarem a igualdade, isso é equivalente a uma restrição `UNIQUE`, embora uma restrição única comum seja mais rápida. No entanto, as restrições de exclusão podem especificar restrições que são mais gerais do que a simples igualdade. Por exemplo, você pode especificar uma restrição de forma que nenhuma das duas linhas na tabela contenha círculos sobrepostos (consulte [Seção 8.8][(datatype-geometric.md "8.8. Geometric Types")]) usando o operador `&&`. Os operadores são obrigatórios serem compostos.

As restrições de exclusão são implementadas usando um índice que tem o mesmo nome que a restrição, portanto, cada operador especificado deve ser associado a uma classe de operador apropriada (consulte [Seção 11.10][(indexes-opclass.md "11.10. Operator Classes and Operator Families")]) para o método de acesso ao índice *`index_method`*. Cada *`exclude_element`* define uma coluna do índice, portanto, pode especificar opcionalmente uma collation, uma classe de operador, parâmetros de classe de operador e/ou opções de ordenação; essas são descritas completamente em [CREATE INDEX][(sql-createindex.md "CREATE INDEX")].

O método de acesso deve suportar `amgettuple` (consulte [Capítulo 63][(indexam.md "Chapter 63. Index Access Method Interface Definition")]); atualmente, isso significa que o GIN não pode ser usado. Embora seja permitido, não faz muito sentido usar índices B-tree ou de hash com uma restrição de exclusão, porque isso não faz nada que uma restrição única comum não faça melhor. Portanto, na prática, o método de acesso será sempre GiST ou SP-GiST.

O *`predicate` permite que você especifique uma restrição de exclusão em um subconjunto da tabela; internamente, isso cria um índice parcial. Note que os parênteses são necessários ao redor do predicado.

Ao estabelecer uma restrição de exclusão para uma hierarquia de partição de vários níveis, todas as colunas na chave de partição da tabela alvo particionada, bem como as de todas as suas tabelas particionadas descendentes, devem ser incluídas na definição da restrição. Além disso, essas colunas devem ser comparadas usando o operador de igualdade. Essas restrições garantem que linhas potencialmente conflitantes existam na mesma partição. A restrição também pode se referir a outras colunas que não fazem parte de qualquer chave de partição, que podem ser comparadas usando qualquer operador apropriado.

`REFERENCES reftable [ ( refcolumn ) ] [ MATCH matchtype ] [ ON DELETE referential_action ] [ ON UPDATE referential_action ]` (constrangimento de coluna) `FOREIGN KEY ( column_name [, ... ] [, PERIOD column_name ] ) REFERENCES reftable [ ( refcolumn [, ... ] [, PERIOD refcolumn ] ) ] [ MATCH matchtype ] [ ON DELETE referential_action ] [ ON UPDATE referential_action ]` (constrangimento de tabela) [#](#SQL-CREATETABLE-PARMS-REFERENCES): Essas cláusulas especificam um constrangimento de chave estrangeira, que exige que um grupo de uma ou mais colunas da nova tabela contenha apenas valores que correspondem aos valores nas(s) coluna(s) de referência de alguma linha da tabela de referência. Se a lista *`refcolumn`* for omitida, a chave primária do *`reftable`* é usada. Caso contrário, a lista *`refcolumn`* deve se referir às colunas de uma restrição de chave única ou primária não diferível ou ser as colunas de um índice único não parcial.

Se a última coluna estiver marcada com `PERIOD`, ela é tratada de uma maneira especial. Enquanto as colunas que não são `PERIOD` são comparadas quanto à igualdade (e deve haver pelo menos uma delas), a coluna `PERIOD` não é. Em vez disso, a restrição é considerada satisfeita se a tabela referenciada tiver registros correspondentes (com base nas partes não `PERIOD` da chave) cujos valores combinados de `PERIOD` cobrem completamente os do registro de referência. Em outras palavras, a referência deve ter um referente por toda a sua duração. Esta coluna deve ser um tipo de intervalo ou multiintervalo. Além disso, a tabela referenciada deve ter uma chave primária ou restrição única declarada com `WITHOUT OVERLAPS`. Finalmente, se a chave estrangeira tiver a especificação PERIOD *`column_name`*, o *`refcolumn`* correspondente, se presente, também deve ser marcado `PERIOD`. Se a cláusula *`refcolumn`* for omitida e, portanto, a restrição de chave primária da reftable for escolhida, a chave primária deve ter sua coluna final marcada `WITHOUT OVERLAPS`.

Para cada par de coluna de referência e coluna referenciada, se elas forem de um tipo de dados colidível, então as colatações devem ser ambas determinísticas ou, caso contrário, ambas as mesmas. Isso garante que ambas as colunas tenham uma noção consistente de igualdade.

O usuário deve ter a permissão `REFERENCES` na tabela referenciada (seja a tabela inteira ou as colunas específicas referenciadas). A adição de uma restrição de chave estrangeira requer um bloqueio `SHARE ROW EXCLUSIVE` na tabela referenciada. Observe que as restrições de chave estrangeira não podem ser definidas entre tabelas temporárias e tabelas permanentes.

Um valor inserido na(s) coluna(s) de referência é comparado com os valores da(s) tabela(s) referenciada(s) usando o tipo de correspondência fornecido. Existem três tipos de correspondência: `MATCH FULL`, `MATCH PARTIAL` e `MATCH SIMPLE` (que é o padrão). `MATCH FULL` não permitirá que uma coluna de uma chave estrangeira multicoluna seja nula, a menos que todas as colunas da chave estrangeira sejam nulos; se todas forem nulos, a linha não é obrigada a ter uma correspondência na tabela referenciada. `MATCH SIMPLE` permite que qualquer uma das colunas da chave estrangeira seja nula; se alguma delas for nula, a linha não é obrigada a ter uma correspondência na tabela referenciada. `MATCH PARTIAL` ainda não é implementado. (Claro, as restrições `NOT NULL` podem ser aplicadas à(s) coluna(s) de referência para evitar que esses casos ocorram.)

Além disso, quando os dados nas colunas referenciadas são alterados, certas ações são realizadas nos dados das colunas da tabela. A cláusula `ON DELETE` especifica a ação a ser realizada quando uma linha referenciada na tabela referenciada está sendo excluída. Da mesma forma, a cláusula `ON UPDATE` especifica a ação a ser realizada quando uma coluna referenciada na tabela referenciada é atualizada para um novo valor. Se a linha for atualizada, mas a coluna referenciada não for realmente alterada, nenhuma ação é realizada. As ações referenciadas são executadas como parte do comando de alteração de dados, mesmo que a restrição seja adiada. Existem as seguintes ações possíveis para cada cláusula:

`NO ACTION` [#](#SQL-CREATETABLE-PARMS-REFERENCES-REFACT-NO-ACTION) :   Produza um erro se a exclusão ou atualização criaria uma violação de restrição de chave estrangeira. Se a restrição for adiada, esse erro será produzido no momento da verificação da restrição se ainda existir alguma linha de referência. Essa é a ação padrão.

`RESTRICT` [#](#SQL-CREATETABLE-PARMS-REFERENCES-REFACT-RESTRICT) :   Produza um erro se uma linha a ser excluída ou atualizada corresponder a uma linha na tabela de referência. Isso impede a ação mesmo se o estado após a ação não violar a restrição de chave estrangeira. Em particular, impede atualizações de linhas referenciadas para valores que são distintos, mas comparam como iguais. (Mas não impede atualizações "sem efeito" que atualizam uma coluna para o mesmo valor.)

Em uma chave estrangeira temporal, esta opção não é suportada.

`CASCADE` [#](#SQL-CREATETABLE-PARMS-REFERENCES-REFACT-CASCADE) :   Exclua quaisquer linhas que façam referência à linha excluída, ou atualize os valores da(s) coluna(s) de referência para os novos valores das colunas referenciadas, respectivamente.

Em uma chave estrangeira temporal, esta opção não é suportada.

`SET NULL [ ( column_name [, ... ] ) ]` [#](#SQL-CREATETABLE-PARMS-REFERENCES-REFACT-SET-NULL) :   Configure todas as colunas de referência ou um subconjunto especificado das colunas de referência como nulos. Um subconjunto de colunas só pode ser especificado para ações de `ON DELETE`.

Em uma chave estrangeira temporal, esta opção não é suportada.

`SET DEFAULT [ ( column_name [, ... ] ) ]` [#](#SQL-CREATETABLE-PARMS-REFERENCES-REFACT-SET-DEFAULT) :   Defina todas as colunas de referência ou um subconjunto especificado das colunas de referência para seus valores padrão. Um subconjunto de colunas só pode ser especificado para ações de `ON DELETE`. (Deve haver uma linha na tabela referenciada que corresponda aos valores padrão, se não forem nulos, ou a operação falhará.)

Em uma chave estrangeira temporal, esta opção não é suportada.

Se as colunas referenciadas forem alteradas frequentemente, pode ser prudente adicionar um índice à(s) coluna(s) de referência, para que as ações referenciadas associadas à restrição de chave estrangeira possam ser realizadas de forma mais eficiente.

`DEFERRABLE` `NOT DEFERRABLE` [#](#SQL-CREATETABLE-PARMS-DEFERRABLE): Isso controla se a restrição pode ser adiada. Uma restrição que não pode ser adiada será verificada imediatamente após cada comando. A verificação de restrições que podem ser adiadas pode ser adiada até o final da transação (usando o comando `SET CONSTRAINTS`). `NOT DEFERRABLE` é o padrão. Atualmente, apenas as restrições `UNIQUE`, `PRIMARY KEY`, `EXCLUDE` e `REFERENCES` (chave estrangeira) aceitam essa cláusula. As restrições `NOT NULL` e `CHECK` não podem ser adiadas. Note que as restrições adiáveis não podem ser usadas como arbitradores de conflito em uma declaração `INSERT` que inclui uma cláusula `ON CONFLICT`.

`INITIALLY IMMEDIATE` `INITIALLY DEFERRED` [#](#SQL-CREATETABLE-PARMS-INITIALLY): Se uma restrição for adiável, esta cláusula especifica o tempo padrão para verificar a restrição. Se a restrição for `INITIALLY IMMEDIATE`, ela é verificada após cada declaração. Este é o padrão. Se a restrição for `INITIALLY DEFERRED`, ela é verificada apenas no final da transação. O tempo de verificação da restrição pode ser alterado com o comando [`SET CONSTRAINTS`(sql-set-constraints.md "SET CONSTRAINTS")].

`ENFORCED` `NOT ENFORCED` [#](#SQL-CREATETABLE-PARMS-ENFORCED): Quando a restrição é `ENFORCED`, o sistema de banco de dados garantirá que a restrição seja satisfeita, verificando a restrição em momentos apropriados (após cada declaração ou no final da transação, conforme apropriado). Esse é o padrão. Se a restrição for `NOT ENFORCED`, o sistema de banco de dados não verificará a restrição. Então, cabe ao código da aplicação garantir que as restrições sejam satisfeitas. O sistema de banco de dados pode ainda assumir que os dados realmente satisfazem a restrição para decisões de otimização, onde isso não afeta a correção do resultado.

As restrições `NOT ENFORCED` podem ser úteis como documentação se a verificação real da restrição no momento da execução for muito cara.

Atualmente, isso é suportado apenas para chaves estrangeiras e restrições `CHECK`.

`USING method` [#](#SQL-CREATETABLE-METHOD): Esta cláusula opcional especifica o método de acesso à tabela a ser utilizado para armazenar o conteúdo da nova tabela; o método deve ser um método de acesso do tipo `TABLE`. Consulte [Capítulo 62](tableam.md "Chapter 62. Table Access Method Interface Definition") para obter mais informações. Se esta opção não for especificada, o método de acesso à tabela padrão é escolhido para a nova tabela. Consulte [default_table_access_method](runtime-config-client.md#GUC-DEFAULT-TABLE-ACCESS-METHOD) para obter mais informações.

Ao criar uma partição, o método de acesso à tabela é o método de acesso da sua tabela particionada, se definido.

`WITH ( storage_parameter [= value] [, ... ] )` [#](#SQL-CREATETABLE-PARMS-WITH): Esta cláusula especifica parâmetros de armazenamento opcionais para uma tabela ou índice; consulte [Parâmetros de armazenamento](sql-createtable.md#SQL-CREATETABLE-STORAGE-PARAMETERS "Storage Parameters") abaixo para mais informações. Para compatibilidade reversa, a cláusula `WITH` para uma tabela também pode incluir `OIDS=FALSE` para especificar que as linhas da nova tabela não devem conter OIDs (identificadores de objeto), `OIDS=TRUE` não é mais suportado.

`WITHOUT OIDS` [#](#SQL-CREATETABLE-PARMS-WITHOUT-OIDS): Esta é uma sintaxe compatível com versões anteriores para declarar uma tabela `WITHOUT OIDS`, a criação de uma tabela `WITH OIDS` não é mais suportada.

`ON COMMIT` [#](#SQL-CREATETABLE-PARMS-ON-COMMIT): O comportamento das tabelas temporárias no final de um bloco de transação pode ser controlado usando `ON COMMIT`. As três opções são:

`PRESERVE ROWS` [#](#SQL-CREATETABLE-PARMS-ON-COMMIT-PRESERVE-ROWS) : Não se realiza nenhuma ação especial nas extremidades das transações. Esse é o comportamento padrão.

`DELETE ROWS` [#](#SQL-CREATETABLE-PARMS-ON-COMMIT-DELETE-ROWS) : Todos os registros na tabela temporária serão excluídos no final de cada bloco de transação. Essencialmente, um `TRUNCATE` automático é realizado em cada commit. Quando usado em uma tabela particionada, isso não é cascado para suas particionamentos.

`DROP` [#](#SQL-CREATETABLE-PARMS-ON-COMMIT-DROP) : A tabela temporária será descartada no final do bloco atual de transação. Quando usada em uma tabela particionada, essa ação descarta suas particionamentos e, quando usada em tabelas com filhos de herança, descarta os filhos dependentes.

`TABLESPACE tablespace_name` [#](#SQL-CREATETABLE-TABLESPACE): O *`tablespace_name`* é o nome do tablespace no qual a nova tabela deve ser criada. Se não for especificado, [default_tablespace](runtime-config-client.md#GUC-DEFAULT-TABLESPACE) é consultado, ou [temp_tablespaces](runtime-config-client.md#GUC-TEMP-TABLESPACES) se a tabela for temporária. Para tabelas particionadas, uma vez que não é necessário armazenamento para a própria tabela, o tablespace especificado substitui `default_tablespace` como tablespace padrão a ser usado para quaisquer particionações recém-criadas, quando nenhum outro tablespace é especificado explicitamente.

`USING INDEX TABLESPACE tablespace_name` [#](#SQL-CREATETABLE-PARMS-USING-INDEX-TABLESPACE): Esta cláusula permite a seleção do tablespace no qual o índice associado a uma restrição `UNIQUE`, `PRIMARY KEY` ou `EXCLUDE` será criado. Se não for especificado, [default_tablespace](runtime-config-client.md#GUC-DEFAULT-TABLESPACE) é consultado, ou [temp_tablespaces](runtime-config-client.md#GUC-TEMP-TABLESPACES) se a tabela for temporária.

### Parâmetros de Armazenamento

A cláusula `WITH` pode especificar *parâmetros de armazenamento* para tabelas e para índices associados a uma restrição `UNIQUE`, `PRIMARY KEY` ou `EXCLUDE`. Os parâmetros de armazenamento para índices são documentados em [CREATE INDEX](sql-createindex.md "CREATE INDEX"). Os parâmetros de armazenamento atualmente disponíveis para tabelas estão listados abaixo. Para muitos desses parâmetros, como mostrado, há um parâmetro adicional com o mesmo nome prefixado com `toast.`, que controla o comportamento da tabela secundária TOAST da tabela, se houver (consulte [Seção 66.2](storage-toast.md "66.2. TOAST") para mais informações sobre TOAST). Se um valor de parâmetro de tabela for definido e o parâmetro equivalente `toast.` não for, a tabela TOAST usará o valor do parâmetro da tabela. Especificar esses parâmetros para tabelas particionadas não é suportado, mas você pode especificá-los para particionações individuais.

`fillfactor` (`integer`) [#](#RELOPTION-FILLFACTOR): O fator de preenchimento de uma tabela é uma porcentagem entre 10 e 100. 100 (enchimento completo) é o padrão. Quando um fator de preenchimento menor é especificado, as operações `INSERT` preenchem as páginas da tabela apenas até a porcentagem indicada; o espaço restante em cada página é reservado para atualizar as linhas naquela página. Isso dá ao `UPDATE` a chance de colocar a cópia atualizada de uma linha na mesma página que a original, o que é mais eficiente do que colocá-la em uma página diferente, e torna as atualizações de tupla apenas para heap mais prováveis. Para uma tabela cujos registros nunca são atualizados, o enchimento completo é a melhor escolha, mas em tabelas com muitas atualizações, fatores de preenchimento menores são apropriados. Este parâmetro não pode ser definido para tabelas TOAST.

`toast_tuple_target` (`integer`) [#](#RELOPTION-TOAST-TUPLE-TARGET): O toast_tuple_target especifica o comprimento mínimo da tupla exigido antes de tentarmos comprimir e/ou mover valores de coluna longa para as tabelas TOAST, e também é o comprimento alvo que tentamos reduzir abaixo uma vez que o toasting começa. Isso afeta as colunas marcadas como Externa (para mover), Main (para compressão) ou Extendida (para ambas) e aplica-se apenas a novos tuplos. Não há efeito em linhas existentes. Por padrão, este parâmetro é definido para permitir pelo menos 4 tuplos por bloco, o que, com o tamanho padrão do bloco, será de 2040 bytes. Os valores válidos estão entre 128 bytes e (tamanho do bloco - cabeçalho), por padrão 8160 bytes. Alterar este valor pode não ser útil para linhas muito curtas ou muito longas. Note que o ajuste padrão está frequentemente próximo do ótimo, e é possível que ajustar este parâmetro possa ter efeitos negativos em alguns casos. Este parâmetro não pode ser definido para tabelas TOAST.

`parallel_workers` (`integer`) [#](#RELOPTION-PARALLEL-WORKERS): Este define o número de trabalhadores que devem ser utilizados para auxiliar uma varredura paralela desta tabela. Se não definido, o sistema determinará um valor com base no tamanho da relação. O número real de trabalhadores escolhidos pelo planejador ou por declarações de utilidade que utilizam varreduras paralelas pode ser menor, por exemplo, devido à definição de [max_worker_processes](runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES).

`autovacuum_enabled`, `toast.autovacuum_enabled` (`boolean`) [#](#RELOPTION-AUTOVACUUM-ENABLED): Habilita ou desabilita o daemon de autovacuum para uma tabela específica. Se verdadeiro, o daemon de autovacuum realizará operações automáticas de `VACUUM` e/ou `ANALYZE` nesta tabela, seguindo as regras discutidas na [Seção 24.1.6](routine-vacuuming.md#AUTOVACUUM "24.1.6. The Autovacuum Daemon"). Se falso, esta tabela não será autovacuumada, exceto para prevenir o enrolamento de IDs de transação. Consulte [Seção 24.1.5](routine-vacuuming.md#VACUUM-FOR-WRAPAROUND "24.1.5. Preventing Transaction ID Wraparound Failures") para mais informações sobre prevenção de enrolamento. Observe que o daemon de autovacuum não é executado em absoluto (exceto para prevenir o enrolamento de IDs de transação) se o parâmetro [autovacuum](runtime-config-vacuum.md#GUC-AUTOVACUUM) for falso; definir os parâmetros de armazenamento de tabelas individuais não substitui isso. Portanto, raramente há muito sentido em definir explicitamente esse parâmetro de armazenamento para `true`, apenas para `false`.

`vacuum_index_cleanup`, `toast.vacuum_index_cleanup` (`enum`) [#](#RELOPTION-VACUUM-INDEX-CLEANUP): Força ou desabilita a limpeza de índices quando `VACUUM` é executado nesta tabela. O valor padrão é `AUTO`. Com `OFF`, a limpeza de índices é desativada, com `ON` ela é ativada e com `AUTO` uma decisão é tomada dinamicamente, cada vez que `VACUUM` é executado. O comportamento dinâmico permite que `VACUUM` evite a digitalização desnecessária de índices para remover poucos tuplas mortas. Desabilitar todas as limpas de índices forçadamente pode acelerar `VACUUM` de forma significativa, mas também pode levar a índices severamente inflados se as modificações da tabela forem frequentes. O parâmetro `INDEX_CLEANUP` de [`VACUUM`(sql-vacuum.md "VACUUM"), se especificado, substitui o valor desta opção.

`vacuum_truncate`, `toast.vacuum_truncate` (`boolean`) [#](#RELOPTION-VACUUM-TRUNCATE): Valor por tabela para o parâmetro [vacuum_truncate](runtime-config-vacuum.md#GUC-VACUUM-TRUNCATE). O parâmetro `TRUNCATE` de [`VACUUM`(sql-vacuum.md "VACUUM"), se especificado, substitui o valor desta opção.

`autovacuum_vacuum_threshold`, `toast.autovacuum_vacuum_threshold` (`integer`) [#](#RELOPTION-AUTOVACUUM-VACUUM-THRESHOLD): Valor por tabela para o parâmetro [autovacuum_vacuum_threshold](runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-THRESHOLD).

`autovacuum_vacuum_max_threshold`, `toast.autovacuum_vacuum_max_threshold` (`integer`) [#](#RELOPTION-AUTOVACUUM-VACUUM-MAX-THRESHOLD): Valor por tabela para o parâmetro [autovacuum_vacuum_max_threshold](runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-MAX-THRESHOLD).

`autovacuum_vacuum_scale_factor`, `toast.autovacuum_vacuum_scale_factor` (`floating point`) [#](#RELOPTION-AUTOVACUUM-VACUUM-SCALE-FACTOR): Valor por tabela para o parâmetro [autovacuum_vacuum_scale_factor](runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-SCALE-FACTOR).

`autovacuum_vacuum_insert_threshold`, `toast.autovacuum_vacuum_insert_threshold` (`integer`) [#](#RELOPTION-AUTOVACUUM-VACUUM-INSERT-THRESHOLD): Valor por tabela para o parâmetro [autovacuum_vacuum_insert_threshold](runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-INSERT-THRESHOLD). O valor especial de -1 pode ser usado para desabilitar os vacúmens de inserção na tabela.

`autovacuum_vacuum_insert_scale_factor`, `toast.autovacuum_vacuum_insert_scale_factor` (`floating point`) [#](#RELOPTION-AUTOVACUUM-VACUUM-INSERT-SCALE-FACTOR): Valor por tabela para o parâmetro [autovacuum_vacuum_insert_scale_factor](runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-INSERT-SCALE-FACTOR).

`autovacuum_analyze_threshold` (`integer`) [#](#RELOPTION-AUTOVACUUM-ANALYZE-THRESHOLD): Valor por tabela para o parâmetro [autovacuum_analyze_threshold](runtime-config-vacuum.md#GUC-AUTOVACUUM-ANALYZE-THRESHOLD).

`autovacuum_analyze_scale_factor` (`floating point`) [#](#RELOPTION-AUTOVACUUM-ANALYZE-SCALE-FACTOR): Valor por tabela para o parâmetro [autovacuum_analyze_scale_factor](runtime-config-vacuum.md#GUC-AUTOVACUUM-ANALYZE-SCALE-FACTOR).

`autovacuum_vacuum_cost_delay`, `toast.autovacuum_vacuum_cost_delay` (`floating point`) [#](#RELOPTION-AUTOVACUUM-VACUUM-COST-DELAY): Valor por tabela para o parâmetro [autovacuum_vacuum_cost_delay](runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-COST-DELAY).

`autovacuum_vacuum_cost_limit`, `toast.autovacuum_vacuum_cost_limit` (`integer`) [#](#RELOPTION-AUTOVACUUM-VACUUM-COST-LIMIT): Valor por tabela para o parâmetro [autovacuum_vacuum_cost_limit](runtime-config-vacuum.md#GUC-AUTOVACUUM-VACUUM-COST-LIMIT).

`autovacuum_freeze_min_age`, `toast.autovacuum_freeze_min_age` (`integer`) [#](#RELOPTION-AUTOVACUUM-FREEZE-MIN-AGE): Valor por tabela para o parâmetro [vacuum_freeze_min_age](runtime-config-vacuum.md#GUC-VACUUM-FREEZE-MIN-AGE). Observe que o autovacuum ignorará os parâmetros por tabela `autovacuum_freeze_min_age` que forem maiores que metade da configuração de [autovacuum_freeze_max_age](runtime-config-vacuum.md#GUC-AUTOVACUUM-FREEZE-MAX-AGE) definida para o sistema.

`autovacuum_freeze_max_age`, `toast.autovacuum_freeze_max_age` (`integer`) [#](#RELOPTION-AUTOVACUUM-FREEZE-MAX-AGE): Valor por tabela para o parâmetro [autovacuum_freeze_max_age](runtime-config-vacuum.md#GUC-AUTOVACUUM-FREEZE-MAX-AGE). Observe que o autovacuum ignorará os parâmetros por tabela `autovacuum_freeze_max_age` que são maiores que o ajuste de nível de sistema (só pode ser definido menor).

`autovacuum_freeze_table_age`, `toast.autovacuum_freeze_table_age` (`integer`) [#](#RELOPTION-AUTOVACUUM-FREEZE-TABLE-AGE): Valor por tabela para o parâmetro [vacuum_freeze_table_age](runtime-config-vacuum.md#GUC-VACUUM-FREEZE-TABLE-AGE).

`autovacuum_multixact_freeze_min_age`, `toast.autovacuum_multixact_freeze_min_age` (`integer`) [#](#RELOPTION-AUTOVACUUM-MULTIXACT-FREEZE-MIN-AGE): Valor por tabela para o parâmetro [vacuum_multixact_freeze_min_age](runtime-config-vacuum.md#GUC-VACUUM-MULTIXACT-FREEZE-MIN-AGE). Observe que o autovacuum ignorará os parâmetros por tabela `autovacuum_multixact_freeze_min_age` que forem maiores que metade da configuração de [autovacuum_multixact_freeze_max_age](runtime-config-vacuum.md#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE) definida para o sistema.

`autovacuum_multixact_freeze_max_age`, `toast.autovacuum_multixact_freeze_max_age` (`integer`) [#](#RELOPTION-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE): Valor por tabela para o parâmetro [autovacuum_multixact_freeze_max_age](runtime-config-vacuum.md#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE). Observe que o autovacuum ignorará os parâmetros por tabela `autovacuum_multixact_freeze_max_age` que são maiores que o ajuste de nível de sistema (só pode ser definido menor).

`autovacuum_multixact_freeze_table_age`, `toast.autovacuum_multixact_freeze_table_age` (`integer`) [#](#RELOPTION-AUTOVACUUM-MULTIXACT-FREEZE-TABLE-AGE): Valor por tabela para o parâmetro [vacuum_multixact_freeze_table_age](runtime-config-vacuum.md#GUC-VACUUM-MULTIXACT-FREEZE-TABLE-AGE).

`log_autovacuum_min_duration`, `toast.log_autovacuum_min_duration` (`integer`) [#](#RELOPTION-LOG-AUTOVACUUM-MIN-DURATION): Valor por tabela para o parâmetro [log_autovacuum_min_duration](runtime-config-logging.md#GUC-LOG-AUTOVACUUM-MIN-DURATION).

`vacuum_max_eager_freeze_failure_rate`, `toast.vacuum_max_eager_freeze_failure_rate` (`floating point`) [#](#RELOPTION-VACUUM-MAX-EAGER-FREEZE-FAILURE-RATE): Valor por tabela para o parâmetro [taxa de falha de congelamento máximo em vácuo](runtime-config-vacuum.md#GUC-VACUUM-MAX-EAGER-FREEZE-FAILURE-RATE).

`user_catalog_table` (`boolean`) [#](#RELOPTION-USER-CATALOG-TABLE): Declare a tabela como uma tabela de catálogo adicional para fins de replicação lógica. Consulte [Seção 47.6.2] (logicaldecoding-output-plugin.md#LOGICALDECODING-CAPABILITIES "47.6.2. Capabilities") para obter detalhes. Este parâmetro não pode ser definido para tabelas TOAST.

## Notas

O PostgreSQL cria automaticamente um índice para cada restrição única e restrição de chave primária para impor a unicidade. Assim, não é necessário criar um índice explicitamente para colunas de chave primária. (Veja [CREATE INDEX][(sql-createindex.md "CREATE INDEX")] para mais informações.)

As restrições únicas e as chaves primárias não são herdadas na implementação atual. Isso torna a combinação de herança e restrições únicas bastante disfuncional.

Uma tabela não pode ter mais de 1600 colunas. (Na prática, o limite efetivo é geralmente menor devido às restrições de comprimento do tupla.)

## Exemplos

Crie a tabela `films` e a tabela `distributors`:

```
CREATE TABLE films (
    code        char(5) CONSTRAINT firstkey PRIMARY KEY,
    title       varchar(40) NOT NULL,
    did         integer NOT NULL,
    date_prod   date,
    kind        varchar(10),
    len         interval hour to minute
);

CREATE TABLE distributors (
     did    integer PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
     name   varchar(40) NOT NULL CHECK (name <> '')
);
```

Crie uma tabela com um array bidimensional:

```
CREATE TABLE array_int (
    vector  int[][]
);
```

Defina uma restrição de tabela única para a tabela `films`. Restrições de tabela únicas podem ser definidas em uma ou mais colunas da tabela:

```
CREATE TABLE films (
    code        char(5),
    title       varchar(40),
    did         integer,
    date_prod   date,
    kind        varchar(10),
    len         interval hour to minute,
    CONSTRAINT production UNIQUE(date_prod)
);
```

Defina uma restrição de coluna de verificação:

```
CREATE TABLE distributors (
    did     integer CHECK (did > 100),
    name    varchar(40)
);
```

Defina uma restrição de tabela de verificação:

```
CREATE TABLE distributors (
    did     integer,
    name    varchar(40),
    CONSTRAINT con1 CHECK (did > 100 AND name <> '')
);
```

Defina uma restrição de tabela chave primária para a tabela `films`:

```
CREATE TABLE films (
    code        char(5),
    title       varchar(40),
    did         integer,
    date_prod   date,
    kind        varchar(10),
    len         interval hour to minute,
    CONSTRAINT code_title PRIMARY KEY(code,title)
);
```

Defina uma restrição de chave primária para a tabela `distributors`. Os dois exemplos seguintes são equivalentes, o primeiro usando a sintaxe de restrição de tabela, o segundo a sintaxe de restrição de coluna:

```
CREATE TABLE distributors (
    did     integer,
    name    varchar(40),
    PRIMARY KEY(did)
);

CREATE TABLE distributors (
    did     integer PRIMARY KEY,
    name    varchar(40)
);
```

Atribua um valor de constante literal padrão para a coluna `name`, organize para que o valor padrão da coluna `did` seja gerado selecionando o próximo valor de um objeto de sequência e faça o valor padrão de `modtime` ser o momento em que a linha é inserida:

```
CREATE TABLE distributors (
    name      varchar(40) DEFAULT 'Luso Films',
    did       integer DEFAULT nextval('distributors_serial'),
    modtime   timestamp DEFAULT current_timestamp
);
```

Defina duas restrições de coluna `NOT NULL` na tabela `distributors`, uma das quais recebe explicitamente um nome:

```
CREATE TABLE distributors (
    did     integer CONSTRAINT no_null NOT NULL,
    name    varchar(40) NOT NULL
);
```

Defina uma restrição única para a coluna `name`:

```
CREATE TABLE distributors (
    did     integer,
    name    varchar(40) UNIQUE
);
```

O mesmo, especificado como restrição de tabela:

```
CREATE TABLE distributors (
    did     integer,
    name    varchar(40),
    UNIQUE(name)
);
```

Crie a mesma tabela, especificando um fator de preenchimento de 70% tanto para a tabela quanto para seu índice único:

```
CREATE TABLE distributors (
    did     integer,
    name    varchar(40),
    UNIQUE(name) WITH (fillfactor=70)
)
WITH (fillfactor=70);
```

Crie a tabela `circles` com uma restrição de exclusão que impeça que dois círculos se sobreponham:

```
CREATE TABLE circles (
    c circle,
    EXCLUDE USING gist (c WITH &&)
);
```

Crie a tabela `cinemas` no tablespace `diskvol1`:

```
CREATE TABLE cinemas (
        id serial,
        name text,
        location text
) TABLESPACE diskvol1;
```

Crie um tipo composto e uma tabela tipada:

```
CREATE TYPE employee_type AS (name text, salary numeric);

CREATE TABLE employees OF employee_type (
    PRIMARY KEY (name),
    salary WITH OPTIONS DEFAULT 1000
);
```

Crie uma tabela particionada com um intervalo:

```
CREATE TABLE measurement (
    logdate         date not null,
    peaktemp        int,
    unitsales       int
) PARTITION BY RANGE (logdate);
```

Crie uma tabela com várias colunas particionada em uma faixa com chave de particionamento:

```
CREATE TABLE measurement_year_month (
    logdate         date not null,
    peaktemp        int,
    unitsales       int
) PARTITION BY RANGE (EXTRACT(YEAR FROM logdate), EXTRACT(MONTH FROM logdate));
```

Crie uma tabela dividida:

```
CREATE TABLE cities (
    city_id      bigserial not null,
    name         text not null,
    population   bigint
) PARTITION BY LIST (left(lower(name), 1));
```

Crie uma tabela com particionamento por hash:

```
CREATE TABLE orders (
    order_id     bigint not null,
    cust_id      bigint not null,
    status       text
) PARTITION BY HASH (order_id);
```

Crie uma partição de uma tabela com partição de intervalo:

```
CREATE TABLE measurement_y2016m07
    PARTITION OF measurement (
    unitsales DEFAULT 0
) FOR VALUES FROM ('2016-07-01') TO ('2016-08-01');
```

Crie algumas partições de uma tabela com partições de intervalo com várias colunas no chave de partição:

```
CREATE TABLE measurement_ym_older
    PARTITION OF measurement_year_month
    FOR VALUES FROM (MINVALUE, MINVALUE) TO (2016, 11);

CREATE TABLE measurement_ym_y2016m11
    PARTITION OF measurement_year_month
    FOR VALUES FROM (2016, 11) TO (2016, 12);

CREATE TABLE measurement_ym_y2016m12
    PARTITION OF measurement_year_month
    FOR VALUES FROM (2016, 12) TO (2017, 01);

CREATE TABLE measurement_ym_y2017m01
    PARTITION OF measurement_year_month
    FOR VALUES FROM (2017, 01) TO (2017, 02);
```

Crie uma partição de uma tabela com partição de lista:

```
CREATE TABLE cities_ab
    PARTITION OF cities (
    CONSTRAINT city_id_nonzero CHECK (city_id != 0)
) FOR VALUES IN ('a', 'b');
```

Crie uma partição de uma tabela particionada de lista que, por sua vez, seja particionada e, em seguida, adicione uma partição a ela:

```
CREATE TABLE cities_ab
    PARTITION OF cities (
    CONSTRAINT city_id_nonzero CHECK (city_id != 0)
) FOR VALUES IN ('a', 'b') PARTITION BY RANGE (population);

CREATE TABLE cities_ab_10000_to_100000
    PARTITION OF cities_ab FOR VALUES FROM (10000) TO (100000);
```

Crie partições de uma tabela com particionamento de hash:

```
CREATE TABLE orders_p1 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE orders_p2 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE orders_p3 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE orders_p4 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

Crie uma partição padrão:

```
CREATE TABLE cities_partdef
    PARTITION OF cities DEFAULT;
```

## Compatibilidade

O comando `CREATE TABLE` está em conformidade com o padrão SQL, com exceções listadas abaixo.

### Tabelas Temporárias

Embora a sintaxe de `CREATE TEMPORARY TABLE` se assemelhe à do padrão SQL, o efeito não é o mesmo. No padrão, as tabelas temporárias são definidas apenas uma vez e existem automaticamente (com conteúdos vazios) em todas as sessões que as necessitam. O PostgreSQL, por outro lado, exige que cada sessão emita seu próprio comando `CREATE TEMPORARY TABLE` para cada tabela temporária que será usada. Isso permite que diferentes sessões usem o mesmo nome de tabela temporária para diferentes propósitos, enquanto a abordagem do padrão restringe todas as instâncias de um nome de tabela temporária dado a ter a mesma estrutura de tabela.

A definição do comportamento das tabelas temporárias do padrão é amplamente ignorada. O comportamento do PostgreSQL sobre esse ponto é semelhante ao de várias outras bases de dados SQL.

O padrão SQL também distingue entre tabelas temporárias globais e locais, onde uma tabela temporária local tem um conjunto separado de conteúdos para cada módulo SQL dentro de cada sessão, embora sua definição ainda seja compartilhada entre as sessões. Como o PostgreSQL não suporta módulos SQL, essa distinção não é relevante no PostgreSQL.

Por questão de compatibilidade, o PostgreSQL aceitará as palavras-chave `GLOBAL` e `LOCAL` em uma declaração de tabela temporária, mas atualmente elas não têm efeito. O uso dessas palavras-chave é desencorajado, uma vez que versões futuras do PostgreSQL podem adotar uma interpretação mais compatível com padrões de seu significado.

A cláusula `ON COMMIT` para tabelas temporárias também se assemelha ao padrão SQL, mas tem algumas diferenças. Se a cláusula `ON COMMIT` for omitida, o SQL especifica que o comportamento padrão é `ON COMMIT DELETE ROWS`. No entanto, o comportamento padrão no PostgreSQL é `ON COMMIT PRESERVE ROWS`. A opção `ON COMMIT DROP` não existe no SQL.

### Restrições de unicidade não diferidas

Quando uma restrição `UNIQUE` ou `PRIMARY KEY` não é adiável, o PostgreSQL verifica a unicidade imediatamente sempre que uma linha é inserida ou modificada. O padrão SQL diz que a unicidade deve ser aplicada apenas no final da declaração; isso faz diferença quando, por exemplo, um único comando atualiza vários valores de chave. Para obter um comportamento compatível com o padrão, declare a restrição como `DEFERRABLE`, mas não adiada (ou seja, `INITIALLY IMMEDIATE`). Esteja ciente de que isso pode ser significativamente mais lento do que a verificação de unicidade imediata.

### Restrições de verificação de coluna

O padrão SQL diz que as restrições de coluna `CHECK` só podem se referir à coluna à qual se aplicam; apenas as restrições de tabela `CHECK` podem se referir a múltiplas colunas. O PostgreSQL não aplica essa restrição; ele trata as restrições de verificação de coluna e tabela da mesma forma.

### `EXCLUDE` Restrição

O tipo de restrição `EXCLUDE` é uma extensão do PostgreSQL.

### Restrições de Chave Estrangeira

A capacidade de especificar listas de colunas nas ações de chave estrangeira `SET DEFAULT` e `SET NULL` é uma extensão do PostgreSQL.

É uma extensão do PostgreSQL que uma restrição de chave estrangeira pode referenciar colunas de um índice único em vez de colunas de uma chave primária ou restrição única.

### `NULL` “Restrição”

A `NULL` “restrição” (na verdade, uma não-restrição) é uma extensão do PostgreSQL ao padrão SQL que é incluída para compatibilidade com outros sistemas de banco de dados (e para simetria com a restrição `NOT NULL`). Como é o padrão para qualquer coluna, sua presença é simplesmente ruído.

### Nomeação de restrições

O padrão SQL diz que as restrições de tabela e domínio devem ter nomes que sejam únicos no esquema que contém a tabela ou domínio. O PostgreSQL é mais flexível: ele apenas exige que os nomes das restrições sejam únicos nos limites anexados a uma tabela ou domínio específico. No entanto, essa liberdade extra não existe para restrições baseadas em índice (as restrições `UNIQUE`, `PRIMARY KEY` e `EXCLUDE`) porque o índice associado tem o mesmo nome que a restrição, e os nomes dos índices devem ser únicos em todas as relações dentro do mesmo esquema.

### Herança

A herança múltipla via a cláusula `INHERITS` é uma extensão do idioma PostgreSQL. O SQL:1999 e versões posteriores definem a herança simples usando uma sintaxe e semântica diferentes. A herança no estilo SQL:1999 ainda não é suportada pelo PostgreSQL.

### Tabelas de Coluna Zero

O PostgreSQL permite que uma tabela sem colunas seja criada (por exemplo, `CREATE TABLE foo();`). Esta é uma extensão do padrão SQL, que não permite tabelas com zero colunas. Tabelas com zero colunas não são, por si só, muito úteis, mas a não permitir que elas existam cria casos especiais estranhos para `ALTER TABLE DROP COLUMN`, então parece mais limpo ignorar essa restrição especifica.

### Colunas de Identidade Múltiplas

O PostgreSQL permite que uma tabela tenha mais de uma coluna de identidade. O padrão especifica que uma tabela pode ter, no máximo, uma coluna de identidade. Isso é relaxado principalmente para oferecer mais flexibilidade para fazer alterações ou migrações de esquema. Note que o comando `INSERT` suporta apenas uma cláusula de substituição que se aplica a toda a declaração, portanto, ter múltiplas colunas de identidade com comportamentos diferentes não é bem suportado.

### Colunas Geradas

As opções `STORED` e `VIRTUAL` não são padrão, mas também são usadas por outras implementações do SQL. O padrão SQL não especifica o armazenamento de colunas geradas.

### `LIKE` Cláusula

Embora uma cláusula `LIKE` exista no padrão SQL, muitas das opções que o PostgreSQL aceita para ela não estão no padrão, e algumas das opções do padrão não são implementadas pelo PostgreSQL.

### `WITH` Cláusula

A cláusula `WITH` é uma extensão do PostgreSQL; os parâmetros de armazenamento não estão no padrão.

### Espaços de tabelas

O conceito de tablespaces do PostgreSQL não faz parte do padrão. Portanto, as cláusulas `TABLESPACE` e `USING INDEX TABLESPACE` são extensões.

### Tabelas digitadas

As tabelas digitadas implementam um subconjunto do padrão SQL. De acordo com o padrão, uma tabela tipada tem colunas correspondentes ao tipo composto subjacente, bem como uma outra coluna que é a "coluna de autoreferência". O PostgreSQL não suporta colunas de autoreferência explicitamente.

### `PARTITION BY` Cláusula

A cláusula `PARTITION BY` é uma extensão do PostgreSQL.

### `PARTITION OF` Cláusula

A cláusula `PARTITION OF` é uma extensão do PostgreSQL.

## Veja também

[ALTER TABLE](sql-altertable.md "ALTER TABLE"), [DROP TABLE](sql-droptable.md "DROP TABLE"), [CREATE TABLE AS](sql-createtableas.md "CREATE TABLE AS"), [CREATE TABLESPACE](sql-createtablespace.md "CREATE TABLESPACE"), [CREATE TYPE](sql-createtype.md "CREATE TYPE")