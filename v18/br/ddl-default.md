## 5.2. Valores padrão [#](#DDL-DEFAULT)

Uma coluna pode ser atribuída um valor padrão. Quando uma nova linha é criada e não são especificados valores para algumas das colunas, essas colunas serão preenchidas com seus respectivos valores padrão. Um comando de manipulação de dados também pode solicitar explicitamente que uma coluna seja definida com seu valor padrão, sem precisar saber qual é esse valor. (Detalhes sobre comandos de manipulação de dados estão em [Capítulo 6] (dml.md "Chapter 6. Data Manipulation").)

Se nenhum valor padrão for declarado explicitamente, o valor padrão é o valor nulo. Isso geralmente faz sentido, pois um valor nulo pode ser considerado para representar dados desconhecidos.

Em uma definição de tabela, os valores padrão são listados após o tipo de dados da coluna. Por exemplo:

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric DEFAULT 9.99
);
```

O valor padrão pode ser uma expressão, que será avaliada sempre que o valor padrão for inserido (*não* quando a tabela for criada). Um exemplo comum é para uma coluna `timestamp` ter um valor padrão de `CURRENT_TIMESTAMP`, para que ela seja definida no momento da inserção da linha. Outro exemplo comum é gerar um “número de série” para cada linha. No PostgreSQL, isso é tipicamente feito de algo como:

```
CREATE TABLE products (
    product_no integer DEFAULT nextval('products_product_no_seq'),
    ...
);
```

onde a função `nextval()` fornece valores sucessivos de um objeto de *sequência* (ver [Seção 9.17][(functions-sequence.md "9.17. Sequence Manipulation Functions")]). Esse arranjo é suficientemente comum que há um abreviação especial para ele:

```
CREATE TABLE products (
    product_no SERIAL,
    ...
);
```

O abreviação `SERIAL` é discutido mais adiante em [Seção 8.1.4][(datatype-numeric.md#DATATYPE-SERIAL "8.1.4. Serial Types")].