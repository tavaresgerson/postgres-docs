### 8.7. Tipos enumerados [#](#DATATYPE-ENUM)

* [8.7.1. Declaração de Tipos Enumerados](datatype-enum.md#DATATYPE-ENUM-DECLARATION)
* [8.7.2. Ordem](datatype-enum.md#DATATYPE-ENUM-ORDERING)
* [8.7.3. Segurança do Tipo](datatype-enum.md#DATATYPE-ENUM-TYPE-SAFETY)
* [8.7.4. Detalhes de Implementação](datatype-enum.md#DATATYPE-ENUM-IMPLEMENTATION-DETAILS)

Os tipos enumerados (enum) são tipos de dados que compreendem um conjunto estático e ordenado de valores. Eles são equivalentes aos tipos `enum` suportados em vários idiomas de programação. Um exemplo de um tipo de enum pode ser os dias da semana ou um conjunto de valores de status para um pedaço de dados.

#### 8.7.1. Declaração de Tipos Enumerados [#](#DATATYPE-ENUM-DECLARATION)

Os tipos de enumeração são criados usando o comando [CREATE TYPE](sql-createtype.md "CREATE TYPE"), por exemplo:

```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');
```

Uma vez criado, o tipo enum pode ser usado em definições de tabela e funções da mesma forma que qualquer outro tipo:

```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');
CREATE TABLE person (
    name text,
    current_mood mood
);
INSERT INTO person VALUES ('Moe', 'happy');
SELECT * FROM person WHERE current_mood = 'happy';
 name | current_mood
------+--------------
 Moe  | happy
(1 row)
```

#### 8.7.2. Pedidos [#](#DATATYPE-ENUM-ORDERING)

A ordem dos valores em um tipo de enum é a ordem em que os valores foram listados quando o tipo foi criado. Todos os operadores de comparação padrão e as funções agregadas relacionadas são suportados para enums. Por exemplo:

```sql
INSERT INTO person VALUES ('Larry', 'sad');
INSERT INTO person VALUES ('Curly', 'ok');
SELECT * FROM person WHERE current_mood > 'sad';
 name  | current_mood
-------+--------------
 Moe   | happy
 Curly | ok
(2 rows)

SELECT * FROM person WHERE current_mood > 'sad' ORDER BY current_mood;
 name  | current_mood
-------+--------------
 Curly | ok
 Moe   | happy
(2 rows)

SELECT name
FROM person
WHERE current_mood = (SELECT MIN(current_mood) FROM person);
 name
-------
 Larry
(1 row)
```

#### 8.7.3. Segurança do tipo [#](#DATATYPE-ENUM-TYPE-SAFETY)

Cada tipo de dado enumerado é separado e não pode ser comparado com outros tipos enumerados. Veja este exemplo:

```sql
CREATE TYPE happiness AS ENUM ('happy', 'very happy', 'ecstatic');
CREATE TABLE holidays (
    num_weeks integer,
    happiness happiness
);
INSERT INTO holidays(num_weeks,happiness) VALUES (4, 'happy');
INSERT INTO holidays(num_weeks,happiness) VALUES (6, 'very happy');
INSERT INTO holidays(num_weeks,happiness) VALUES (8, 'ecstatic');
INSERT INTO holidays(num_weeks,happiness) VALUES (2, 'sad');
ERROR:  invalid input value for enum happiness: "sad"
SELECT person.name, holidays.num_weeks FROM person, holidays
  WHERE person.current_mood = holidays.happiness;
ERROR:  operator does not exist: mood = happiness
```

Se você realmente precisar fazer algo assim, pode escrever um operador personalizado ou adicionar casts explícitos à sua consulta:

```sql
SELECT person.name, holidays.num_weeks FROM person, holidays
  WHERE person.current_mood::text = holidays.happiness::text;
 name | num_weeks
------+-----------
 Moe  |         4
(1 row)
```

#### 8.7.4. Detalhes de implementação [#](#DATATYPE-ENUM-IMPLEMENTATION-DETAILS)

As etiquetas de enum são sensíveis ao caso, então `'happy'` não é a mesma coisa que `'HAPPY'`. O espaço em branco nas etiquetas também é significativo.

Embora os tipos de enum sejam destinados principalmente a conjuntos estáticos de valores, é possível adicionar novos valores a um tipo de enum existente e renomear valores (consulte [ALTER TYPE](sql-altertype.md "ALTER TYPE")). Os valores existentes não podem ser removidos de um tipo de enum, nem a ordem de classificação desses valores pode ser alterada, a menos que o tipo de enum seja descartado e recriado.

Um valor de enum ocupa quatro bytes no disco. O comprimento da etiqueta textual de um valor de enum é limitado pelo ajuste `NAMEDATALEN` compilado no PostgreSQL; em edições padrão, isso significa, no máximo, 63 bytes.

As traduções dos valores de enum internos para rótulos textuais são mantidas no catálogo do sistema `pg_enum`(catalog-pg-enum.md "52.20. pg_enum"). Consultar diretamente esse catálogo pode ser útil.