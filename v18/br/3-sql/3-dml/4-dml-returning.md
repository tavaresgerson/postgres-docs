### 6.4. Retornar dados de linhas modificadas [#](#DML-RETURNING)

Às vezes, é útil obter dados de linhas modificadas enquanto elas estão sendo manipuladas. Os comandos `INSERT`, `UPDATE`, `DELETE` e `MERGE` têm uma cláusula opcional `RETURNING` que suporta isso. O uso de `RETURNING` evita a realização de uma consulta extra ao banco de dados para coletar os dados, e é especialmente valioso quando, de outra forma, seria difícil identificar as linhas modificadas de forma confiável.

Os conteúdos permitidos de uma cláusula `RETURNING` são os mesmos que a lista de saída de um comando `SELECT` (consulte [Seção 7.3](queries-select-lists.md)). Ela pode conter nomes de colunas da tabela de destino do comando, ou expressões de valor usando essas colunas. Uma abreviação comum é `RETURNING *`, que seleciona todas as colunas da tabela de destino em ordem.

Em um `INSERT`, os dados padrão disponíveis para `RETURNING` são as linhas conforme inseridas. Isso não é tão útil em inserções triviais, pois apenas repetiria os dados fornecidos pelo cliente. Mas pode ser muito útil quando se baseia em valores padrão computados. Por exemplo, ao usar uma coluna `serial`(datatype-numeric.md#DATATYPE-SERIAL "8.1.4. Serial Types") para fornecer identificadores únicos, `RETURNING` pode retornar a ID atribuída a uma nova linha:

```
CREATE TABLE users (firstname text, lastname text, id serial primary key);

INSERT INTO users (firstname, lastname) VALUES ('Joe', 'Cool') RETURNING id;
```

A cláusula `RETURNING` também é muito útil com `INSERT ... SELECT`.

Em um `UPDATE`, os dados padrão disponíveis para `RETURNING` são o novo conteúdo da linha modificada. Por exemplo:

```
UPDATE products SET price = price * 1.10
  WHERE price <= 99.99
  RETURNING name, price AS new_price;
```

Em um `DELETE`, os dados padrão disponíveis para `RETURNING` são o conteúdo da linha excluída. Por exemplo:

```
DELETE FROM products
  WHERE obsoletion_date = 'today'
  RETURNING *;
```

Em um `MERGE`, os dados padrão disponíveis para `RETURNING` são o conteúdo da linha de origem mais o conteúdo da linha de destino inserida, atualizada ou excluída. Como é bastante comum que a origem e o destino tenham muitas das mesmas colunas, especificar `RETURNING *` pode levar a muitas colunas duplicadas, portanto, é frequentemente mais útil qualificá-lo para retornar apenas a linha de origem ou de destino. Por exemplo:

```
MERGE INTO products p USING new_products n ON p.product_no = n.product_no
  WHEN NOT MATCHED THEN INSERT VALUES (n.product_no, n.name, n.price)
  WHEN MATCHED THEN UPDATE SET name = n.name, price = n.price
  RETURNING p.*;
```

Em cada um desses comandos, também é possível retornar explicitamente o conteúdo antigo e novo da linha modificada. Por exemplo:

```
UPDATE products SET price = price * 1.10
  WHERE price <= 99.99
  RETURNING name, old.price AS old_price, new.price AS new_price,
            new.price - old.price AS price_change;
```

Neste exemplo, escrever `new.price` é o mesmo que simplesmente escrever `price`, mas isso torna o significado mais claro.

Essa sintaxe para retornar valores antigos e novos está disponível nos comandos `INSERT`, `UPDATE`, `DELETE` e `MERGE`, mas, tipicamente, os valores antigos serão `NULL` para um `INSERT`, e os novos valores serão `NULL` para um `DELETE`. No entanto, há situações em que ainda pode ser útil para esses comandos. Por exemplo, em um `INSERT` com uma cláusula [[`ON CONFLICT DO UPDATE`](sql-insert.md#SQL-ON-CONFLICT)], os valores antigos serão não `NULL` para linhas conflitantes. Da mesma forma, se um `DELETE` é convertido em um `UPDATE` por uma regra de reescrita (sql-createrule.md "CREATE RULE"), os novos valores podem ser não `NULL`.

Se houver gatilhos ([Capítulo 37](triggers.md)) na tabela alvo, os dados disponíveis para `RETURNING` são as linhas modificadas pelos gatilhos. Assim, inspecionar as colunas calculadas por gatilhos é outro caso de uso comum para `RETURNING`.