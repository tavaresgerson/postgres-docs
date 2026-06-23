## 3.6. Herança [#](#TUTORIAL-INHERITANCE)

A herança é um conceito de bancos de dados orientado a objetos. Ela abre novas possibilidades interessantes de projeto de banco de dados.

Vamos criar duas tabelas: uma tabela `cities` e uma tabela `capitals`. Naturalmente, as capitais também são cidades, então você quer alguma maneira de mostrar as capitais implicitamente quando você lista todas as cidades. Se você é realmente inteligente, pode inventar algum esquema como este:

```
CREATE TABLE capitals (
  name       text,
  population real,
  elevation  int,    -- (in ft)
  state      char(2)
);

CREATE TABLE non_capitals (
  name       text,
  population real,
  elevation  int     -- (in ft)
);

CREATE VIEW cities AS
  SELECT name, population, elevation FROM capitals
    UNION
  SELECT name, population, elevation FROM non_capitals;
```

Isso funciona bem no que diz respeito à consulta, mas fica feio quando você precisa atualizar várias linhas, entre outras coisas.

Uma solução melhor é esta:

```
CREATE TABLE cities (
  name       text,
  population real,
  elevation  int     -- (in ft)
);

CREATE TABLE capitals (
  state      char(2) UNIQUE NOT NULL
) INHERITS (cities);
```

Neste caso, uma linha de `capitals` *herda* todas as colunas (`name`, `population` e `elevation`) de seu *padrão*, `cities`. O tipo da coluna `name` é `text`, um tipo nativo do PostgreSQL para strings de caracteres de comprimento variável. A tabela `capitals` tem uma coluna adicional, `state`, que mostra sua abreviação de estado. No PostgreSQL, uma tabela pode herdar de zero ou mais outras tabelas.

Por exemplo, a seguinte consulta encontra os nomes de todas as cidades, incluindo as capitais dos estados, que estão localizadas em uma elevação superior a 152 metros:

```
SELECT name, elevation
  FROM cities
  WHERE elevation > 500;
```

que retorna:

```
   name    | elevation
-----------+-----------
 Las Vegas |      2174
 Mariposa  |      1953
 Madison   |       845
(3 rows)
```

Por outro lado, a seguinte consulta encontra todas as cidades que não são capitais estaduais e estão situadas em uma elevação superior a 152 metros:

```
SELECT name, elevation
    FROM ONLY cities
    WHERE elevation > 500;
```

```
   name    | elevation
-----------+-----------
 Las Vegas |      2174
 Mariposa  |      1953
(2 rows)
```

Aqui, o `ONLY` antes do `cities` indica que a consulta deve ser executada apenas na tabela `cities`, e não em tabelas abaixo do `cities` na hierarquia de herança. Muitos dos comandos que já discutimos — `SELECT`, `UPDATE` e `DELETE` — suportam essa notação `ONLY`.

### Nota

Embora a herança seja frequentemente útil, ela não foi integrada com restrições únicas ou chaves estrangeiras, o que limita sua utilidade. Veja [Seção 5.11] para mais detalhes.