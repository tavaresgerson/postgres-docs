## Crie uma tabela estrangeira

CREATE FOREIGN TABLE — definir uma nova tabela estrangeira

## Sinopse

```
CREATE FOREIGN TABLE [ IF NOT EXISTS ] table_name ( [
  { column_name data_type [ OPTIONS ( option 'value' [, ... ] ) ] [ COLLATE collation ] [ column_constraint [ ... ] ]
    | table_constraint
    | LIKE source_table [ like_option ... ] }
    [, ... ]
] )
[ INHERITS ( parent_table [, ... ] ) ]
  SERVER server_name
[ OPTIONS ( option 'value' [, ... ] ) ]

CREATE FOREIGN TABLE [ IF NOT EXISTS ] table_name
  PARTITION OF parent_table [ (
  { column_name [ WITH OPTIONS ] [ column_constraint [ ... ] ]
    | table_constraint }
    [, ... ]
) ]
{ FOR VALUES partition_bound_spec | DEFAULT }
  SERVER server_name
[ OPTIONS ( option 'value' [, ... ] ) ]

where column_constraint is:

[ CONSTRAINT constraint_name ]
{ NOT NULL [ NO INHERIT ] |
  NULL |
  CHECK ( expression ) [ NO INHERIT ] |
  DEFAULT default_expr |
  GENERATED ALWAYS AS ( generation_expr ) [ STORED | VIRTUAL ] }
[ ENFORCED | NOT ENFORCED ]

and table_constraint is:

[ CONSTRAINT constraint_name ]
{  NOT NULL column_name [ NO INHERIT ] |
   CHECK ( expression ) [ NO INHERIT ] }
[ ENFORCED | NOT ENFORCED ]

and like_option is:

{ INCLUDING | EXCLUDING } { COMMENTS | CONSTRAINTS | DEFAULTS | GENERATED | STATISTICS | ALL }

and partition_bound_spec is:

IN ( partition_bound_expr [, ...] ) |
FROM ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] )
  TO ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] ) |
WITH ( MODULUS numeric_literal, REMAINDER numeric_literal )
```

## Descrição

`CREATE FOREIGN TABLE` cria uma nova tabela estrangeira no banco de dados atual. A tabela será de propriedade do usuário que emite o comando.

Se um nome de esquema for fornecido (por exemplo, `CREATE FOREIGN TABLE myschema.mytable ...`) então a tabela é criada no esquema especificado. Caso contrário, ela é criada no esquema atual. O nome da tabela estrangeira deve ser distinto do nome de qualquer outra relação (tabela, sequência, índice, visão, visão materializada ou tabela estrangeira) no mesmo esquema.

`CREATE FOREIGN TABLE` também cria automaticamente um tipo de dados que representa o tipo composto correspondente a uma linha da tabela estrangeira. Portanto, as tabelas estrangeiras não podem ter o mesmo nome que qualquer tipo de dados existente no mesmo esquema.

Se a cláusula `PARTITION OF` for especificada, a tabela será criada como uma partição de `parent_table` com limites especificados.

Para criar uma tabela estrangeira, você deve ter o privilégio `USAGE` no servidor estrangeiro, bem como o privilégio `USAGE` em todos os tipos de coluna usados na tabela.

## Parâmetros

`IF NOT EXISTS`: Não exija um erro se uma relação com o mesmo nome já existir. Neste caso, é emitido um aviso. Observe que não há garantia de que a relação existente seja algo parecido com a que teria sido criada.

*`table_name`*: O nome (opcionalmente qualificado por esquema) da tabela a ser criada.

*`column_name`*: O nome da coluna que será criada na nova tabela.

*`data_type`*: O tipo de dados da coluna. Isso pode incluir especificadores de matriz. Para mais informações sobre os tipos de dados suportados pelo PostgreSQL, consulte o [Capítulo 8](datatype.md).

`COLLATE collation`: A cláusula `COLLATE` atribui uma correção de texto à coluna (que deve ser de um tipo de dados correção de texto). Se não for especificado, o tipo de dados da coluna usa a correção de texto padrão.

`INHERITS ( parent_table [, ... ] )`: A cláusula opcional `INHERITS` especifica uma lista de tabelas das quais a nova tabela estrangeira herda automaticamente todas as colunas. As tabelas pai podem ser tabelas comuns ou tabelas estrangeiras. Consulte a forma semelhante de [`CREATE TABLE`](sql-createtable.md "CREATE TABLE") para mais detalhes.

`PARTITION OF parent_table { FOR VALUES partition_bound_spec | DEFAULT }`: Este formulário pode ser usado para criar a tabela estrangeira como partição da tabela principal fornecida com os valores especificados para o limite de partição. Consulte o formulário semelhante de [`CREATE TABLE`](sql-createtable.md "CREATE TABLE") para mais detalhes. Note que, atualmente, não é permitido criar a tabela estrangeira como partição da tabela principal se houver índices `UNIQUE` na tabela principal. (Consulte também [`ALTER TABLE ATTACH PARTITION`](sql-altertable.md "ALTER TABLE").)

`LIKE source_table [ like_option ... ]`: A cláusula `LIKE` especifica uma tabela a partir da qual a nova tabela copia automaticamente todos os nomes de coluna, seus tipos de dados e suas restrições não nulos.

Ao contrário de `INHERITS`, a nova tabela e a tabela original são completamente desacopladas após a conclusão da criação. Alterações na tabela original não serão aplicadas à nova tabela, e não é possível incluir dados da nova tabela em varreduras da tabela original.

Além disso, ao contrário de `INHERITS`, as colunas e restrições copiadas por `LIKE` não são mescladas com colunas e restrições com nomes semelhantes. Se o mesmo nome for especificado explicitamente ou em outra cláusula `LIKE`, um erro é sinalizado.

As cláusulas opcionais *`like_option`* especificam quais propriedades adicionais da tabela original devem ser copiadas. Especificar `INCLUDING` copia a propriedade, omitindo `EXCLUDING` a propriedade. `EXCLUDING` é o padrão. Se várias especificações forem feitas para o mesmo tipo de objeto, a última é usada. As opções disponíveis são:

`INCLUDING COMMENTS` : Os comentários das colunas copiadas, restrições e estatísticas extensas serão copiados. O comportamento padrão é excluir comentários, resultando nos objetos correspondentes na nova tabela sem comentários.

`INCLUDING CONSTRAINTS` : As restrições `CHECK` serão copiadas. Não há distinção entre restrições de coluna e restrições de tabela. As restrições não nulos são sempre copiadas para a nova tabela.

`INCLUDING DEFAULTS` : As expressões padrão para as definições de colunas copiadas serão copiadas. Caso contrário, as expressões padrão não serão copiadas, resultando em colunas copiadas na nova tabela com valores padrão nulos. Observe que a cópia de valores padrão que chamam funções de modificação de banco de dados, como `nextval`, pode criar uma ligação funcional entre as tabelas original e nova.

`INCLUDING GENERATED` :   Quaisquer expressões de geração de definições de coluna copiadas serão copiadas. Por padrão, as novas colunas serão colunas regulares de base.

`INCLUDING STATISTICS` : As estatísticas estendidas são copiadas para a nova tabela.

`INCLUDING ALL` :   `INCLUDING ALL` é uma forma abreviada que seleciona todas as opções individuais disponíveis. (Poderia ser útil escrever cláusulas individuais `EXCLUDING` após `INCLUDING ALL` para selecionar todas, exceto algumas opções específicas.)

`CONSTRAINT constraint_name`: Um nome opcional para uma coluna ou restrição de tabela. Se a restrição for violada, o nome da restrição está presente nas mensagens de erro, então nomes de restrição como `col must be positive` podem ser usados para comunicar informações úteis sobre a restrição para aplicativos de cliente. (As aspas duplas são necessárias para especificar nomes de restrição que contenham espaços.) Se um nome de restrição não for especificado, o sistema gera um nome.

`NOT NULL` [ NO INHERIT ]: A coluna não pode conter valores nulos.

Uma restrição marcada com `NO INHERIT` não se propagará para as tabelas filhas.

`NULL`: A coluna pode conter valores nulos. Esse é o padrão.

Esta cláusula é fornecida apenas para compatibilidade com bancos de dados SQL não padrão. Seu uso é desencorajado em novas aplicações.

`CHECK ( expression ) [ NO INHERIT ]`: A cláusula `CHECK` especifica uma expressão que produz um resultado booleano que cada linha da tabela externa deve satisfazer; ou seja, a expressão deve produzir VERDADEIRO ou DESCONHECIDO, nunca FALSO, para todas as linhas da tabela externa. Uma restrição de verificação especificada como uma restrição de coluna deve referenciar apenas o valor daquela coluna, enquanto uma expressão que aparece em uma restrição de tabela pode referenciar múltiplas colunas.

Atualmente, as expressões `CHECK` não podem conter subconsultas nem se referir a variáveis que não sejam colunas da linha atual. A coluna do sistema `tableoid` pode ser referenciada, mas não qualquer outra coluna do sistema.

Uma restrição marcada com `NO INHERIT` não se propagará para as tabelas filhas.

`DEFAULT default_expr`: A cláusula `DEFAULT` atribui um valor de dados padrão para a coluna cuja definição de coluna ela aparece dentro. O valor é qualquer expressão livre de variáveis (subconsultas e referências cruzadas para outras colunas na tabela atual não são permitidas). O tipo de dados da expressão padrão deve corresponder ao tipo de dados da coluna.

A expressão padrão será usada em qualquer operação de inserção que não especifique um valor para a coluna. Se não houver um padrão para uma coluna, então o padrão é nulo.

`GENERATED ALWAYS AS ( generation_expr ) [ STORED | VIRTUAL ]`: Esta cláusula cria a coluna como uma *coluna gerada*. A coluna não pode ser escrita e, ao ser lida, o resultado da expressão especificada será retornado.

Quando `VIRTUAL` é especificado, a coluna será calculada quando ela for lida. (O wrapper de dados externos a verá como um valor nulo em novas linhas e pode optar por armazená-lo como um valor nulo ou ignorá-lo completamente.) Quando `STORED` é especificado, a coluna será calculada na escrita. (O valor calculado será apresentado ao wrapper de dados externos para armazenamento e deve ser retornado na leitura.) `VIRTUAL` é o padrão.

A expressão de geração pode se referir a outras colunas na tabela, mas não a outras colunas geradas. Quaisquer funções e operadores utilizados devem ser imutáveis. Não são permitidas referências a outras tabelas.

*`server_name`*: O nome de um servidor externo existente que será usado para a tabela externa. Para obter detalhes sobre a definição de um servidor, consulte [CREATE SERVER](sql-createserver.md "CREATE SERVER").

`OPTIONS ( option 'value' [, ...] )`: Opções a serem associadas à nova tabela estrangeira ou a uma de suas colunas. Os nomes e valores das opções permitidos são específicos para cada wrapper de dados estrangeiro e são validados usando a função de validação do wrapper de dados estrangeiro. Nomes de opções duplicados não são permitidos (embora seja OK para uma opção de tabela e uma opção de coluna terem o mesmo nome).

## Notas

As restrições em tabelas estrangeiras (como as cláusulas `CHECK` ou `NOT NULL`) não são aplicadas pelo sistema principal do PostgreSQL, e a maioria dos wrappers de dados estrangeiros também não tenta aplicá-las; ou seja, a restrição é simplesmente assumida como verdadeira. Não haveria muito sentido em tal aplicação, pois ela só se aplicaria às linhas inseridas ou atualizadas através da tabela estrangeira, e não às linhas modificadas por outros meios, como diretamente no servidor remoto. Em vez disso, uma restrição anexada a uma tabela estrangeira deve representar uma restrição que está sendo aplicada pelo servidor remoto.

Alguns wrappers de dados estrangeiros de propósito específico podem ser o único mecanismo de acesso aos dados que eles acessam, e, nesse caso, pode ser apropriado que o próprio wrapper de dados estrangeiro realize a aplicação de restrições. Mas você não deve assumir que um wrapper faça isso, a menos que sua documentação diga o contrário.

Embora o PostgreSQL não tente impor restrições em tabelas externas, ele assume que elas são corretas para fins de otimização de consultas. Se houver linhas visíveis na tabela externa que não satisfazem uma restrição declarada, as consultas na tabela podem produzir erros ou respostas incorretas. É responsabilidade do usuário garantir que a definição da restrição corresponda à realidade.

### Atenção

Quando uma tabela estrangeira é usada como uma partição de uma tabela particionada, há uma restrição implícita de que seu conteúdo deve satisfazer a regra de particionamento. Novamente, é responsabilidade do usuário garantir que isso seja verdade, o que é melhor feito instalando uma restrição correspondente no servidor remoto.

Dentro de uma tabela dividida que contém partições de tabela estrangeira, um `UPDATE` que altera o valor da chave de partição pode fazer com que uma linha seja movida de uma partição local para uma partição de tabela estrangeira, desde que o wrapper de dados estrangeiro suporte roteamento de tupla. No entanto, atualmente não é possível mover uma linha de uma partição de tabela estrangeira para outra partição. Um `UPDATE` que exigiria fazer isso falhará devido à restrição de particionamento, assumindo que isso seja adequadamente aplicado pelo servidor remoto.

Considerações semelhantes se aplicam a colunas geradas. Colunas geradas armazenadas são calculadas na inserção ou atualização no servidor PostgreSQL local e entregues ao wrapper de dados externos para gravação no armazenamento de dados externo, mas não é exigido que uma consulta da tabela externa retorne valores para colunas geradas armazenadas que sejam consistentes com a expressão de geração. Novamente, isso pode resultar em resultados de consulta incorretos.

## Exemplos

Crie a tabela estrangeira `films`, que será acessada através do servidor `film_server`:

```
CREATE FOREIGN TABLE films (
    code        char(5) NOT NULL,
    title       varchar(40) NOT NULL,
    did         integer NOT NULL,
    date_prod   date,
    kind        varchar(10),
    len         interval hour to minute
)
SERVER film_server;
```

Crie a tabela estrangeira `measurement_y2016m07`, que será acessada através do servidor `server_07`, como uma partição da tabela de intervalo particionada `measurement`:

```
CREATE FOREIGN TABLE measurement_y2016m07
    PARTITION OF measurement FOR VALUES FROM ('2016-07-01') TO ('2016-08-01')
    SERVER server_07;
```

## Compatibilidade

O comando `CREATE FOREIGN TABLE` está em grande parte em conformidade com o padrão SQL; no entanto, assim como com (sql-createtable.md "CREATE TABLE"), `NULL` e tabelas externas de coluna zero, as restrições são permitidas. A capacidade de especificar valores padrão de coluna também é uma extensão do PostgreSQL. A herança de tabela, na forma definida pelo PostgreSQL, não é padrão. A cláusula `LIKE`, conforme suportada neste comando, não é padrão.

## Veja também

[ALTERAR TABELA EXTERNA](sql-alterforeigntable.md "ALTER FOREIGN TABLE"), [DROP TABELA EXTERNA](sql-dropforeigntable.md "DROP FOREIGN TABLE"), [CADA TABELA CRIAR](sql-createtable.md "CREATE TABLE"), [CRIAR SERVIDOR](sql-createserver.md "CREATE SERVER"), [IMPORTAR SCHEMA EXTERNA](sql-importforeignschema.md "IMPORT FOREIGN SCHEMA")