## 5.1. Fundamentos da tabela [#](#DDL-BASICS)

Uma tabela em um banco de dados relacional é muito semelhante a uma tabela em papel: ela consiste em linhas e colunas. O número e a ordem das colunas são fixos, e cada coluna tem um nome. O número de linhas é variável — reflete quanto dados são armazenados em um momento dado. O SQL não oferece garantias sobre a ordem das linhas em uma tabela. Quando uma tabela é lida, as linhas aparecerão em uma ordem não especificada, a menos que a ordenação seja solicitada explicitamente. Isso é coberto em [Capítulo 7](queries.md). Além disso, o SQL não atribui identificadores únicos às linhas, portanto, é possível ter várias linhas completamente idênticas em uma tabela. Esta é uma consequência do modelo matemático que sustenta o SQL, mas geralmente não é desejável. Mais adiante neste capítulo, veremos como lidar com essa questão.

Cada coluna tem um tipo de dados. O tipo de dados restringe o conjunto de valores possíveis que podem ser atribuídos a uma coluna e atribui semântica aos dados armazenados na coluna, para que possam ser usados para cálculos. Por exemplo, uma coluna declarada como de tipo numérico não aceitará strings de texto arbitrárias, e os dados armazenados em tal coluna podem ser usados para cálculos matemáticos. Por outro lado, uma coluna declarada como de tipo de string de caracteres aceitará quase qualquer tipo de dados, mas não se presta a cálculos matemáticos, embora outras operações, como concatenação de strings, estejam disponíveis.

O PostgreSQL inclui um conjunto considerável de tipos de dados embutidos que se adequam a muitas aplicações. Os usuários também podem definir seus próprios tipos de dados. A maioria dos tipos de dados embutidos tem nomes e semântica óbvias, então nós adiamos uma explicação detalhada para [Capítulo 8](datatype.md). Alguns dos tipos de dados frequentemente usados são `integer` para números inteiros, `numeric` para números possivelmente fracionários, `text` para strings de caracteres, `date` para datas, `time` para valores de hora do dia e `timestamp` para valores que contêm tanto data quanto hora.

Para criar uma tabela, você usa o comando apropriadamente chamado [CREATE TABLE](sql-createtable.md). Neste comando, você especifica pelo menos um nome para a nova tabela, os nomes das colunas e o tipo de dados de cada coluna. Por exemplo:

```
CREATE TABLE my_first_table (
    first_column text,
    second_column integer
);
```

Isso cria uma tabela denominada `my_first_table` com duas colunas. A primeira coluna é denominada `first_column` e tem um tipo de dados de `text`; a segunda coluna tem o nome `second_column` e o tipo `integer`. Os nomes da tabela e das colunas seguem a sintaxe de identificadores explicada em [Seção 4.1.1](sql-syntax-lexical.md#SQL-SYNTAX-IDENTIFIERS). Os nomes dos tipos são geralmente também identificadores, mas há algumas exceções. Note que a lista de colunas é separada por vírgula e cercada por parênteses.

Claro, o exemplo anterior foi muito artificial. Normalmente, você daria nomes às suas tabelas e colunas que indiquem que tipo de dados elas armazenam. Então, vamos analisar um exemplo mais realista:

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric
);
```

(O tipo `numeric` pode armazenar componentes fracionários, como seria típico em valores monetários.)

### DICA

Quando você cria muitas tabelas inter-relacionadas, é prudente escolher um padrão de nomeação consistente para as tabelas e colunas. Por exemplo, há a opção de usar substantivos singulares ou plurais para os nomes das tabelas, ambos favorecidos por algum teórico ou outro.

Há um limite para o número de colunas que uma tabela pode conter. Dependendo dos tipos de coluna, esse limite varia entre 250 e 1600. No entanto, definir uma tabela com tantas colunas é altamente incomum e, muitas vezes, um projeto questionável.

Se você não precisar mais de uma tabela, pode removê-la usando o comando [DROP TABLE](sql-droptable.md "DROP TABLE"). Por exemplo:

```
DROP TABLE my_first_table;
DROP TABLE products;
```

Tentar excluir uma tabela que não existe é um erro. No entanto, é comum em arquivos de script SQL tentar incondicionalmente excluir cada tabela antes de criá-la, ignorando quaisquer mensagens de erro, para que o script funcione, independentemente de a tabela existir ou não. (Se preferir, pode usar a variante `DROP TABLE IF EXISTS` para evitar as mensagens de erro, mas isso não é SQL padrão.)

Se você precisar modificar uma tabela que já existe, consulte a [Seção 5.7](ddl-alter.md) mais adiante neste capítulo.

Com as ferramentas discutidas até agora, você pode criar tabelas totalmente funcionais. O restante deste capítulo trata da adição de recursos à definição da tabela para garantir a integridade dos dados, segurança ou conveniência. Se você está ansioso para preencher suas tabelas com dados agora, pode pular para [Capítulo 6](dml.md) e ler o restante deste capítulo mais tarde.