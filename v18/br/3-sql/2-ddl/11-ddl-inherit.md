### 5.11. Herança [#](#DDL-INHERIT)

* [5.11.1. Observações](ddl-inherit.md#DDL-INHERIT-CAVEATS)

O PostgreSQL implementa a herança de tabelas, que pode ser uma ferramenta útil para os projetistas de banco de dados. (SQL: 1999 e versões posteriores definem uma característica de herança de tipos, que difere em muitos aspectos das características descritas aqui.)

Vamos começar com um exemplo: suponha que estamos tentando construir um modelo de dados para cidades. Cada estado tem muitas cidades, mas apenas uma capital. Queremos ser capazes de recuperar rapidamente a cidade capital de qualquer estado específico. Isso pode ser feito criando duas tabelas, uma para capitais de estado e outra para cidades que não são capitais. No entanto, o que acontece quando queremos solicitar dados sobre uma cidade, independentemente de ela ser uma capital ou não? O recurso de herança pode ajudar a resolver esse problema. Definimos a tabela `capitals` para que ela herde do `cities`:

```
CREATE TABLE cities (
    name            text,
    population      float,
    elevation       int     -- in feet
);

CREATE TABLE capitals (
    state           char(2)
) INHERITS (cities);
```

Neste caso, a tabela `capitals` *herda* todas as colunas da sua tabela pai, `cities`. As capitais dos estados também têm uma coluna extra, `state`, que mostra seu estado.

Em PostgreSQL, uma tabela pode herdar de zero ou mais outras tabelas, e uma consulta pode referenciar todas as linhas de uma tabela ou todas as linhas de uma tabela mais todas as suas tabelas descendentes. Este último comportamento é o padrão. Por exemplo, a seguinte consulta encontra os nomes de todas as cidades, incluindo as capitais dos estados, que estão localizadas em uma elevação superior a 152 metros:

```
SELECT name, elevation
    FROM cities
    WHERE elevation > 500;
```

Dadas as informações da amostra do tutorial do PostgreSQL (consulte a [Seção 2.1](tutorial-sql-intro.md)), isso retorna:

```
   name    | elevation
-----------+-----------
 Las Vegas |      2174
 Mariposa  |      1953
 Madison   |       845
```

Por outro lado, a seguinte consulta encontra todas as cidades que não são capitais estaduais e estão situadas em uma elevação superior a 152 metros:

```
SELECT name, elevation
    FROM ONLY cities
    WHERE elevation > 500;

   name    | elevation
-----------+-----------
 Las Vegas |      2174
 Mariposa  |      1953
```

Aqui, a palavra-chave `ONLY` indica que a consulta deve ser aplicada apenas para `cities`, e não para quaisquer tabelas abaixo de `cities` na hierarquia de herança. Muitos dos comandos que já discutimos — `SELECT`, `UPDATE` e `DELETE` — suportam a palavra-chave `ONLY`.

Você também pode escrever o nome da tabela com um `*` no final para especificar explicitamente que as tabelas descendentes são incluídas:

```
SELECT name, elevation
    FROM cities*
    WHERE elevation > 500;
```

Não é necessário escrever `*`, uma vez que esse comportamento é sempre o padrão. No entanto, essa sintaxe ainda é suportada para compatibilidade com versões mais antigas, onde o padrão pode ser alterado.

Em alguns casos, você pode querer saber de qual tabela uma determinada linha se originou. Há uma coluna de sistema chamada `tableoid` em cada tabela que pode lhe dizer qual é a tabela de origem:

```
SELECT c.tableoid, c.name, c.elevation
FROM cities c
WHERE c.elevation > 500;
```

que retorna:

```
 tableoid |   name    | elevation
----------+-----------+-----------
   139793 | Las Vegas |      2174
   139793 | Mariposa  |      1953
   139798 | Madison   |       845
```

(Se você tentar reproduzir este exemplo, provavelmente obterá diferentes OIDs numéricos.) Ao fazer uma junção com `pg_class`, você pode ver os nomes reais das tabelas:

```
SELECT p.relname, c.name, c.elevation
FROM cities c, pg_class p
WHERE c.elevation > 500 AND c.tableoid = p.oid;
```

que retorna:

```
 relname  |   name    | elevation
----------+-----------+-----------
 cities   | Las Vegas |      2174
 cities   | Mariposa  |      1953
 capitals | Madison   |       845
```

Outra maneira de obter o mesmo efeito é usar o tipo de alias `regclass`, que imprimirá o OID da tabela de forma simbólica:

```
SELECT c.tableoid::regclass, c.name, c.elevation
FROM cities c
WHERE c.elevation > 500;
```

A herança não propaga automaticamente os dados dos comandos `INSERT` ou `COPY` para outras tabelas na hierarquia de herança. No nosso exemplo, a seguinte declaração `INSERT` falhará:

```
INSERT INTO cities (name, population, elevation, state)
VALUES ('Albany', NULL, NULL, 'NY');
```

Podemos esperar que os dados sejam encaminhados de alguma forma para a tabela `capitals`, mas isso não acontece: `INSERT` sempre insere exatamente na tabela especificada. Em alguns casos, é possível redirecionar a inserção usando uma regra (consulte [Capítulo 39](rules.md)). No entanto, isso não ajuda no caso acima, porque a tabela `cities` não contém a coluna `state`, e, portanto, o comando será rejeitado antes que a regra possa ser aplicada.

Todas as restrições de verificação e restrições não nulo em uma tabela pai são automaticamente herdadas por suas crianças, a menos que especificamente especificado de outra forma com cláusulas `NO INHERIT`. Outros tipos de restrições (união, chave primária e restrições de chave estrangeira) não são herdados.

Uma tabela pode herdar de mais de uma tabela pai, no caso, ela tem a união das colunas definidas pelas tabelas pai. Quaisquer colunas declaradas na definição da tabela filha são adicionadas a essas. Se o mesmo nome de coluna aparecer em várias tabelas pai, ou tanto em uma tabela pai quanto na definição da filha, então essas colunas são “fusionadas” para que haja apenas uma coluna desse tipo na tabela filha. Para serem fusionadas, as colunas devem ter os mesmos tipos de dados, caso contrário, um erro é levantado. As restrições de verificação hereditárias e as restrições não nulos são fusionadas de uma maneira semelhante. Assim, por exemplo, uma coluna fusionada será marcada como não nula se alguma das definições de coluna de onde ela veio for marcada como não nula. As restrições de verificação são fusionadas se elas tiverem o mesmo nome, e a fusão falhará se suas condições forem diferentes.

A herança de tabela é tipicamente estabelecida quando a tabela filho é criada, usando a cláusula `INHERITS` da declaração [`CREATE TABLE`](sql-createtable.md "CREATE TABLE"). Alternativamente, uma tabela que já está definida de maneira compatível pode ter uma nova relação de pai adicionada, usando a variante `INHERIT` da [`ALTER TABLE`](sql-altertable.md "ALTER TABLE"). Para fazer isso, a nova tabela filho deve já incluir colunas com os mesmos nomes e tipos que as colunas do pai. Também deve incluir restrições de verificação com os mesmos nomes e expressões de verificação que as do pai. Da mesma forma, um link de herança pode ser removido de uma tabela filho usando a variante `NO INHERIT` da `ALTER TABLE`. Adicionar e remover dinamicamente links de herança como este pode ser útil quando a relação de herança está sendo usada para particionar a tabela (ver [Seção 5.12](ddl-partitioning.md "5.12. Table Partitioning")).

Uma maneira conveniente de criar uma tabela compatível que será posteriormente feita uma nova criança é usar a cláusula `LIKE` em `CREATE TABLE`. Isso cria uma nova tabela com as mesmas colunas que a tabela de origem. Se houver quaisquer restrições `CHECK` definidas na tabela de origem, a opção `INCLUDING CONSTRAINTS` para `LIKE` deve ser especificada, pois a nova criança deve ter restrições que correspondam ao pai para ser considerada compatível.

Uma tabela principal não pode ser excluída enquanto qualquer uma de suas crianças permanecerem. Da mesma forma, as colunas ou restrições de verificação das tabelas de crianças não podem ser excluídas ou alteradas se forem herdadas de qualquer tabela principal. Se você deseja remover uma tabela e todos os seus descendentes, uma maneira fácil é excluir a tabela principal com a opção `CASCADE` (consulte [Seção 5.15](ddl-depend.md)).

`ALTER TABLE` propagará quaisquer alterações nas definições de dados das colunas e nas restrições de verificação na hierarquia de herança. Novamente, a remoção de colunas que dependem de outras tabelas só é possível ao usar a opção `CASCADE`. `ALTER TABLE` segue as mesmas regras para a fusão e rejeição de colunas duplicadas que se aplicam durante `CREATE TABLE`.

As consultas herdadas realizam verificações de permissão de acesso apenas na tabela pai. Assim, por exemplo, conceder a permissão `UPDATE` na tabela `cities` implica em permissão para atualizar linhas na tabela `capitals`, também, quando elas são acessadas através de `cities`. Isso preserva a aparência de que os dados estão (também) na tabela pai. Mas a tabela `capitals` não poderia ser atualizada diretamente sem uma concessão adicional. Da mesma forma, as políticas de segurança de linha da tabela pai (ver [Seção 5.9] (ddl-rowsecurity.md "5.9. Row Security Policies")) são aplicadas às linhas que vêm de tabelas filhas durante uma consulta herdada. As políticas de uma tabela filhas, se houver, são aplicadas apenas quando ela é a tabela explicitamente nomeada na consulta; e, nesse caso, quaisquer políticas anexadas a seus(s) pai(s) são ignoradas.

As tabelas externas (consulte a [Seção 5.13](ddl-foreign-data.md)) também podem fazer parte de hierarquias de herança, seja como tabelas pai ou filho, assim como as tabelas regulares podem. Se uma tabela externa faz parte de uma hierarquia de herança, então quaisquer operações que não sejam suportadas pela tabela externa também não são suportadas na hierarquia como um todo.

#### 5.11.1. Avisos [#](#DDL-INHERIT-CAVEATS)

Observe que nem todos os comandos SQL podem funcionar em hierarquias de herança. Os comandos que são usados para consulta de dados, modificação de dados ou modificação de esquema (por exemplo, `SELECT`, `UPDATE`, `DELETE`, a maioria das variantes de `ALTER TABLE`, mas não `INSERT` ou `ALTER TABLE ... RENAME`) geralmente têm como padrão incluir tabelas de filhos e suportar a notação `ONLY` para excluí-los. A maioria dos comandos que realizam manutenção e ajuste de banco de dados (por exemplo, `REINDEX`) funcionam apenas em tabelas individuais e físicas e não suportam a recursão em hierarquias de herança. No entanto, tanto os comandos `VACUUM` quanto `ANALYZE` têm como padrão incluir tabelas de filhos e a notação `ONLY` é suportada para permitir que elas sejam excluídas. O comportamento respectivo de cada comando individual é documentado em sua página de referência ([Comandos SQL](sql-commands.md "SQL Commands")).

Uma limitação séria do recurso de herança é que os índices (incluindo restrições exclusivas) e as restrições de chave estrangeira só se aplicam a tabelas individuais, e não às suas crianças de herança. Isso é verdadeiro tanto no lado de referência quanto no lado referenciado de uma restrição de chave estrangeira. Assim, em termos do exemplo acima:

* Se declarássemos `cities`.`name` como `UNIQUE` ou uma `PRIMARY KEY`, isso não impediriam que a tabela `capitals` tivesse linhas com nomes que duplicavam as linhas em `cities`. E essas linhas duplicadas apareceriam por padrão em consultas de `cities`. De fato, por padrão, `capitals` não teria nenhuma restrição única, e assim poderia conter várias linhas com o mesmo nome. Você poderia adicionar uma restrição única a `capitals`, mas isso não impedirá a duplicação em comparação com `cities`.
* Da mesma forma, se especificarmos que a coluna de outra tabela `cities`.`name` `REFERENCES` alguma outra tabela, essa restrição não se propagaria automaticamente para `capitals`. Nesse caso, você poderia contornar isso adicionando manualmente a mesma restrição `REFERENCES` a `capitals`.
* Especificar que a coluna de outra tabela `REFERENCES cities(name)` permitiria que a outra tabela contêsse nomes de cidade, mas não nomes de capital. Não há uma boa solução para esse caso.

Algumas funcionalidades não implementadas para hierarquias de herança são implementadas para particionamento declarativo. É necessário grande cuidado ao decidir se a particionamento com herança legítima é útil para sua aplicação.