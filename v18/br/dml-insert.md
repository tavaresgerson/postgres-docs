## 6.1. Inserindo Dados [#](#DML-INSERT)

Quando uma tabela é criada, ela não contém dados. A primeira coisa a fazer antes que um banco de dados possa ser muito útil é inserir dados. Os dados são inseridos uma linha de cada vez. Você também pode inserir mais de uma linha em um único comando, mas não é possível inserir algo que não seja uma linha completa. Mesmo que você conheça apenas alguns valores de coluna, uma linha completa deve ser criada.

Para criar uma nova linha, use o comando [INSERT](sql-insert.md). O comando requer o nome da tabela e os valores das colunas. Por exemplo, considere a tabela de produtos do [Capítulo 5](ddl.md):

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric
);
```

Um exemplo de comando para inserir uma linha seria:

```
INSERT INTO products VALUES (1, 'Cheese', 9.99);
```

Os valores dos dados estão listados na ordem em que as colunas aparecem na tabela, separados por vírgulas. Geralmente, os valores dos dados serão literais (constantes), mas expressões escalares também são permitidas.

A sintaxe acima tem o inconveniente de que você precisa saber a ordem das colunas na tabela. Para evitar isso, você também pode listar as colunas explicitamente. Por exemplo, ambos os seguintes comandos têm o mesmo efeito que o acima:

```
INSERT INTO products (product_no, name, price) VALUES (1, 'Cheese', 9.99);
INSERT INTO products (name, price, product_no) VALUES ('Cheese', 9.99, 1);
```

Muitos usuários consideram uma boa prática sempre listar os nomes das colunas.

Se você não tiver valores para todas as colunas, pode omitir algumas delas. Nesse caso, as colunas serão preenchidas com seus valores padrão. Por exemplo:

```
INSERT INTO products (product_no, name) VALUES (1, 'Cheese');
INSERT INTO products VALUES (1, 'Cheese');
```

A segunda forma é uma extensão do PostgreSQL. Ela preenche as colunas da esquerda com tantos valores quanto forem fornecidos, e o restante será predefinido.

Para maior clareza, você também pode solicitar valores padrão explicitamente, para colunas individuais ou para toda a linha:

```
INSERT INTO products (product_no, name, price) VALUES (1, 'Cheese', DEFAULT);
INSERT INTO products DEFAULT VALUES;
```

Você pode inserir várias linhas em um único comando:

```
INSERT INTO products (product_no, name, price) VALUES
    (1, 'Cheese', 9.99),
    (2, 'Bread', 1.99),
    (3, 'Milk', 2.99);
```

Também é possível inserir o resultado de uma consulta (que pode não ter nenhuma linha, uma linha ou muitas linhas):

```
INSERT INTO products (product_no, name, price)
  SELECT product_no, name, price FROM new_products
    WHERE release_date = 'today';
```

Isso fornece todo o poder do mecanismo de consulta SQL ([Capítulo 7](queries.md)) para calcular as linhas a serem inseridas.

### DICA

Ao inserir um monte de dados ao mesmo tempo, considere usar o comando [COPY](sql-copy.md). Não é tão flexível quanto o comando [INSERT](sql-insert.md), mas é mais eficiente. Consulte [Seção 14.4](populate.md) para obter mais informações sobre o desempenho de carregamento em massa.