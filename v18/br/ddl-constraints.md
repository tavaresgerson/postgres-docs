## 5.5. Restrições [#](#DDL-CONSTRAINTS)

* [5.5.1. Verificação de restrições](ddl-constraints.md#DDL-CONSTRAINTS-CHECK-CONSTRAINTS)
* [5.5.2. Restrições não nulos](ddl-constraints.md#DDL-CONSTRAINTS-NOT-NULL)
* [5.5.3. Restrições únicas](ddl-constraints.md#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS)
* [5.5.4. Chaves primárias](ddl-constraints.md#DDL-CONSTRAINTS-PRIMARY-KEYS)
* [5.5.5. Chaves estrangeiras](ddl-constraints.md#DDL-CONSTRAINTS-FK)
* [5.5.6. Restrições de exclusão](ddl-constraints.md#DDL-CONSTRAINTS-EXCLUSION)

Os tipos de dados são uma maneira de limitar o tipo de dados que podem ser armazenados em uma tabela. No entanto, para muitas aplicações, a restrição que eles fornecem é muito grosseira. Por exemplo, uma coluna contendo o preço de um produto provavelmente deve aceitar apenas valores positivos. Mas não há um tipo de dado padrão que aceite apenas números positivos. Outro problema é que você pode querer restringir os dados da coluna em relação a outras colunas ou linhas. Por exemplo, em uma tabela contendo informações sobre produtos, deve haver apenas uma linha para cada número de produto.

Para esse fim, o SQL permite que você defina restrições em colunas e tabelas. As restrições lhe dão todo o controle sobre os dados em suas tabelas que você deseja. Se um usuário tentar armazenar dados em uma coluna que violaria uma restrição, um erro é exibido. Isso se aplica mesmo se o valor vier da definição do valor padrão.

### 5.5.1. Verificar restrições [#](#DDL-CONSTRAINTS-CHECK-CONSTRAINTS)

Uma restrição de verificação é o tipo de restrição mais genérico. Ela permite que você especifique que o valor em uma certa coluna deve satisfazer uma expressão booleana (verdadeiro ou falso). Por exemplo, para exigir preços de produtos positivos, você pode usar:

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price > 0)
);
```

Como você pode ver, a definição de restrição vem após o tipo de dados, assim como as definições de valor padrão. Os valores padrão e as restrições podem ser listados em qualquer ordem. Uma restrição de verificação consiste na palavra-chave `CHECK` seguida de uma expressão entre parênteses. A expressão da restrição de verificação deve envolver a coluna assim restringida, caso contrário, a restrição não faria muito sentido.

Você também pode dar um nome separado à restrição. Isso esclarece as mensagens de erro e permite que você faça referência à restrição quando precisar modificá-la. A sintaxe é:

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CONSTRAINT positive_price CHECK (price > 0)
);
```

Para especificar uma restrição nomeada, use a palavra-chave `CONSTRAINT` seguida por um identificador seguido da definição da restrição. (Se você não especificar um nome de restrição dessa forma, o sistema escolhe um nome para você.)

Uma restrição de verificação também pode se referir a várias colunas. Digamos que você armazene um preço normal e um preço com desconto, e que você queira garantir que o preço com desconto seja menor que o preço normal:

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price > 0),
    discounted_price numeric CHECK (discounted_price > 0),
    CHECK (price > discounted_price)
);
```

Os dois primeiros constrangimentos devem parecer familiares. O terceiro usa uma sintaxe nova. Não está anexado a uma coluna específica, em vez disso, aparece como um item separado na lista de colunas separadas por vírgula. As definições de coluna e essas definições de constrangimento podem ser listadas em ordem mista.

Dizemos que as duas primeiras restrições são restrições de coluna, enquanto a terceira é uma restrição de tabela, porque é escrita separadamente de qualquer definição de coluna. As restrições de coluna também podem ser escritas como restrições de tabela, embora o contrário não seja necessariamente possível, uma vez que uma restrição de coluna é suposta referir-se apenas à coluna a que está anexada. (O PostgreSQL não aplica essa regra, mas você deve seguir essa regra se quiser que suas definições de tabela funcionem com outros sistemas de banco de dados.) O exemplo acima também pode ser escrito da seguinte forma:

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
    CHECK (price > 0),
    discounted_price numeric,
    CHECK (discounted_price > 0),
    CHECK (price > discounted_price)
);
```

ou até mesmo:

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price > 0),
    discounted_price numeric,
    CHECK (discounted_price > 0 AND price > discounted_price)
);
```

É uma questão de gosto.

Os nomes podem ser atribuídos às restrições de tabela da mesma maneira que as restrições de coluna:

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
    CHECK (price > 0),
    discounted_price numeric,
    CHECK (discounted_price > 0),
    CONSTRAINT valid_discount CHECK (price > discounted_price)
);
```

Deve-se notar que uma restrição de verificação é atendida se a expressão de verificação avaliar para verdadeiro ou para o valor nulo. Como a maioria das expressões avaliará para o valor nulo se qualquer operando for nulo, elas não impedirão valores nulos nas colunas restritas. Para garantir que uma coluna não contenha valores nulos, a restrição não-nulo descrita na próxima seção pode ser usada.

### Nota

O PostgreSQL não suporta restrições `CHECK` que fazem referência a dados de tabela que não sejam a nova ou a atualização da linha verificada. Embora uma restrição `CHECK` que viole essa regra possa parecer funcionar em testes simples, não pode garantir que o banco de dados não atinja um estado em que a condição da restrição seja falsa (devido a mudanças subsequentes nas outras linhas envolvidas). Isso causaria o fracasso de uma varredura e restauração do banco de dados. A restauração poderia falhar mesmo quando o estado completo do banco de dados é consistente com a restrição, devido a linhas que não são carregadas em uma ordem que satisfará a restrição. Se possível, use as restrições `UNIQUE`, `EXCLUDE` ou `FOREIGN KEY` para expressar restrições entre linhas e entre tabelas.

Se o que você deseja é uma verificação única contra outras linhas na inserção de uma linha, em vez de uma garantia de consistência mantida continuamente, pode-se usar um [trigger] personalizado para implementar isso. (Essa abordagem evita o problema de dump/restore, pois o pg_dump não reinstalará os gatilhos até após a restauração dos dados, de modo que a verificação não será aplicada durante um dump/restore.)

### Nota

O PostgreSQL assume que as condições das restrições `CHECK` são imutáveis, ou seja, elas sempre darão o mesmo resultado para a mesma linha de entrada. Essa suposição é o que justifica o exame das restrições `CHECK` apenas quando as linhas são inseridas ou atualizadas, e não em outros momentos. (O aviso acima sobre não referenciar outros dados da tabela é realmente um caso especial dessa restrição.)

Um exemplo de uma maneira comum de quebrar essa suposição é fazer referência a uma função definida pelo usuário em uma expressão `CHECK`, e depois alterar o comportamento dessa função. O PostgreSQL não proíbe isso, mas não notará se houver linhas na tabela que agora violam a restrição `CHECK`. Isso causaria o fracasso de um próximo dump e restabelecimento do banco de dados. A maneira recomendada de lidar com essa mudança é descartar a restrição (usando `ALTER TABLE`), ajustar a definição da função e adicionar novamente a restrição, verificando-a novamente contra todas as linhas da tabela.

### 5.5.2. Restrições de não nulidade [#](#DDL-CONSTRAINTS-NOT-NULL)

Uma restrição não nula simplesmente especifica que uma coluna não pode assumir o valor nulo. Um exemplo de sintaxe:

```
CREATE TABLE products (
    product_no integer NOT NULL,
    name text NOT NULL,
    price numeric
);
```

Também pode ser especificado um nome explícito de restrição, por exemplo:

```
CREATE TABLE products (
    product_no integer NOT NULL,
    name text CONSTRAINT products_name_not_null NOT NULL,
    price numeric
);
```

Uma restrição não nula é geralmente escrita como uma restrição de coluna. A sintaxe para escrevê-la como uma restrição de tabela é

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
    NOT NULL product_no,
    NOT NULL name
);
```

Mas essa sintaxe não é padrão e é destinada principalmente para uso pelo pg_dump.

Uma restrição não nula é funcionalmente equivalente à criação de uma restrição de verificação `CHECK (column_name IS NOT NULL)`, mas no PostgreSQL, criar uma restrição não nula explícita é mais eficiente.

Claro, uma coluna pode ter mais de uma restrição. Basta escrever as restrições uma após a outra:

```
CREATE TABLE products (
    product_no integer NOT NULL,
    name text NOT NULL,
    price numeric NOT NULL CHECK (price > 0)
);
```

A ordem não importa. Ela não determina necessariamente em que ordem as restrições são verificadas.

No entanto, uma coluna pode ter, no máximo, uma restrição explícita de não nulidade.

A restrição `NOT NULL` tem uma inversão: a restrição `NULL`. Isso não significa que a coluna deve ser nula, o que certamente seria inútil. Em vez disso, isso simplesmente seleciona o comportamento padrão de que a coluna pode ser nula. A restrição `NULL` não está presente no padrão SQL e não deve ser usada em aplicações portáteis. (Foi adicionada apenas ao PostgreSQL para ser compatível com alguns outros sistemas de banco de dados.) Alguns usuários, no entanto, gostam disso porque facilita a alternância da restrição em um arquivo de script. Por exemplo, você poderia começar com:

```
CREATE TABLE products (
    product_no integer NULL,
    name text NULL,
    price numeric NULL
);
```

e, em seguida, insira a palavra-chave `NOT` onde desejar.

### DICA

Na maioria dos projetos de banco de dados, a maioria das colunas deve ser marcada como não nula.

### 5.5.3. Restrições Únicas [#](#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS)

Restrições únicas garantem que os dados contidos em uma coluna ou em um grupo de colunas sejam únicos entre todas as linhas da tabela. A sintaxe é:

```
CREATE TABLE products (
    product_no integer UNIQUE,
    name text,
    price numeric
);
```

quando escrito como uma restrição de coluna, e:

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
    UNIQUE (product_no)
);
```

quando escrito como uma restrição de tabela.

Para definir uma restrição única para um grupo de colunas, escreva-a como uma restrição de tabela com os nomes das colunas separados por vírgulas:

```
CREATE TABLE example (
    a integer,
    b integer,
    c integer,
    UNIQUE (a, c)
);
```

Isso especifica que a combinação de valores nas colunas indicadas é única em toda a tabela, embora nenhuma das colunas precise ser (e, normalmente, não seja) única.

Você pode atribuir seu próprio nome para uma restrição única, da maneira usual:

```
CREATE TABLE products (
    product_no integer CONSTRAINT must_be_different UNIQUE,
    name text,
    price numeric
);
```

Adicionar uma restrição exclusiva criará automaticamente um índice de árvore B exclusivo na coluna ou no grupo de colunas listadas na restrição. Uma restrição de unicidade que cobre apenas algumas linhas não pode ser escrita como uma restrição exclusiva, mas é possível impor tal restrição criando um índice exclusivo [(indexes-partial.md "11.8. Partial Indexes")].

Em geral, uma restrição única é violada se houver mais de uma linha na tabela onde os valores de todas as colunas incluídas na restrição forem iguais. Por padrão, dois valores nulos não são considerados iguais nesta comparação. Isso significa que, mesmo na presença de uma restrição única, é possível armazenar linhas duplicadas que contenham um valor nulo em pelo menos uma das colunas restritas. Esse comportamento pode ser alterado adicionando a cláusula `NULLS NOT DISTINCT`, como

```
CREATE TABLE products (
    product_no integer UNIQUE NULLS NOT DISTINCT,
    name text,
    price numeric
);
```

ou

```
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric,
    UNIQUE NULLS NOT DISTINCT (product_no)
);
```

O comportamento padrão pode ser especificado explicitamente usando `NULLS DISTINCT`. O tratamento padrão nulo em restrições exclusivas é definido pela implementação de acordo com o padrão SQL, e outras implementações têm um comportamento diferente. Portanto, tenha cuidado ao desenvolver aplicativos que devem ser portáveis.

### 5.5.4. Chaves primárias [#](#DDL-CONSTRAINTS-PRIMARY-KEYS)

Uma restrição de chave primária indica que uma coluna ou um grupo de colunas pode ser usado como um identificador único para as linhas na tabela. Isso exige que os valores sejam únicos e não nulos. Portanto, as seguintes duas definições de tabela aceitam os mesmos dados:

```
CREATE TABLE products (
    product_no integer UNIQUE NOT NULL,
    name text,
    price numeric
);
```

```
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
```

As chaves primárias podem abranger mais de uma coluna; a sintaxe é semelhante às restrições únicas:

```
CREATE TABLE example (
    a integer,
    b integer,
    c integer,
    PRIMARY KEY (a, c)
);
```

Adicionar uma chave primária criará automaticamente um índice de árvore B único na coluna ou grupo de colunas listadas na chave primária e fará com que a(s) coluna(s) seja marcada com `NOT NULL`.

Uma tabela pode ter, no máximo, uma chave primária. (Pode haver qualquer número de restrições únicas, que, combinadas com restrições não nulos, são funcionalmente quase a mesma coisa, mas apenas uma pode ser identificada como chave primária.) A teoria da teoria de banco de dados relacional dita que cada tabela deve ter uma chave primária. Esta regra não é aplicada pelo PostgreSQL, mas geralmente é melhor segui-la.

As chaves primárias são úteis tanto para fins de documentação quanto para aplicações de clientes. Por exemplo, um aplicativo de GUI que permite modificar os valores das linhas provavelmente precisa saber a chave primária de uma tabela para ser capaz de identificar as linhas de forma única. Há também várias maneiras pelas quais o sistema de banco de dados faz uso de uma chave primária, se uma tiver sido declarada; por exemplo, a chave primária define as colunas alvo padrão(s) para chaves estrangeiras que fazem referência à sua tabela.

### 5.5.5. Chaves estrangeiras [#](#DDL-CONSTRAINTS-FK)

Uma restrição de chave estrangeira especifica que os valores em uma coluna (ou um grupo de colunas) devem corresponder aos valores que aparecem em alguma linha de outra tabela. Dizemos que isso mantém a *integridade referencial* entre duas tabelas relacionadas.

Digamos que você tenha a tabela de produtos que já usamos várias vezes:

```
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
```

Vamos também assumir que você tem uma tabela que armazena pedidos desses produtos. Queremos garantir que a tabela de pedidos só contenha pedidos de produtos que realmente existem. Então, definimos uma restrição de chave estrangeira na tabela de pedidos que faz referência à tabela de produtos:

```
CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    product_no integer REFERENCES products (product_no),
    quantity integer
);
```

Agora é impossível criar pedidos com entradas `product_no` que não aparecem na tabela de produtos.

Dizemos que, nessa situação, a tabela de pedidos é a tabela de *referência* e a tabela de produtos é a tabela *referenciada*. Da mesma forma, existem colunas de referência e colunas referenciadas.

Você também pode encurtar o comando acima para:

```
CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    product_no integer REFERENCES products,
    quantity integer
);
```

porque, na ausência de uma lista de colunas, a chave primária da tabela referenciada é usada como a(s) coluna(s) referenciada(s).

Você pode atribuir seu próprio nome para uma restrição de chave estrangeira, da maneira usual.

Uma chave estrangeira também pode restringir e referenciar um grupo de colunas. Como de costume, ela precisa ser escrita na forma de restrição de tabela. Aqui está um exemplo de sintaxe fictício:

```
CREATE TABLE t1 (
  a integer PRIMARY KEY,
  b integer,
  c integer,
  FOREIGN KEY (b, c) REFERENCES other_table (c1, c2)
);
```

Claro, o número e o tipo das colunas restritas precisam corresponder ao número e ao tipo das colunas referenciadas.

Às vezes, é útil que a "outra tabela" de uma restrição de chave estrangeira seja a mesma tabela; isso é chamado de chave estrangeira *auto-referencial*. Por exemplo, se você deseja que as linhas de uma tabela representem nós de uma estrutura em árvore, você poderia escrever

```
CREATE TABLE tree (
    node_id integer PRIMARY KEY,
    parent_id integer REFERENCES tree,
    name text,
    ...
);
```

Um nó de nível superior teria NULL `parent_id`, enquanto as entradas que não são NULL `parent_id` seriam restringidas para referenciar linhas válidas da tabela.

Uma tabela pode ter mais de uma restrição de chave estrangeira. Isso é usado para implementar relações de muitos para muitos entre tabelas. Digamos que você tenha tabelas sobre produtos e pedidos, mas agora você quer permitir que um pedido contenha possivelmente muitos produtos (o que a estrutura acima não permitia). Você poderia usar essa estrutura de tabela:

```
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);

CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    shipping_address text,
    ...
);

CREATE TABLE order_items (
    product_no integer REFERENCES products,
    order_id integer REFERENCES orders,
    quantity integer,
    PRIMARY KEY (product_no, order_id)
);
```

Observe que a chave primária se sobrepõe às chaves estrangeiras na última tabela.

Sabemos que as chaves estrangeiras não permitem a criação de pedidos que não se relacionem a nenhum produto. Mas e se um produto for removido após a criação de um pedido que o referencia? O SQL permite que você também lidere com isso. Intuitivamente, temos algumas opções:

* Não permitir a exclusão de um produto referenciado
* Exclua também as ordens
* Alguma outra coisa?

Para ilustrar isso, vamos implementar a seguinte política no exemplo de relação muitos-para-muitos acima: quando alguém deseja remover um produto que ainda é referido por uma ordem (via `order_items`,) não permitimos isso. Se alguém remover uma ordem, os itens da ordem também são removidos:

```
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);

CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    shipping_address text,
    ...
);

CREATE TABLE order_items (
    product_no integer REFERENCES products ON DELETE RESTRICT,
    order_id integer REFERENCES orders ON DELETE CASCADE,
    quantity integer,
    PRIMARY KEY (product_no, order_id)
);
```

A ação padrão `ON DELETE` é `ON DELETE NO ACTION`; não é necessário especiá-la. Isso significa que a exclusão na tabela referenciada pode prosseguir. Mas a restrição de chave estrangeira ainda é necessária para ser satisfeita, então essa operação geralmente resultará em um erro. Mas o controle das restrições de chave estrangeira também pode ser adiado para uma data posterior na transação (não coberto neste capítulo). Nesse caso, a configuração `NO ACTION` permitiria que outros comandos "corrijam" a situação antes de a restrição ser verificada, por exemplo, inserindo outra linha adequada na tabela referenciada ou excluindo as linhas agora pendentes da tabela de referência.

`RESTRICT` é um ajuste mais rigoroso do que `NO ACTION`. Ele impede a exclusão de uma linha referenciada. `RESTRICT` não permite que a verificação seja adiada para uma data posterior na transação.

`CASCADE` especifica que, quando uma linha referenciada é excluída, as linhas que a referenciam também devem ser automaticamente excluídas.

Existem outras duas opções: `SET NULL` e `SET DEFAULT`. Essas opções fazem com que a(s) coluna(s) de referência na(s) linha(s) de referência sejam definidas como nulos ou seus valores padrão, respectivamente, quando a(s) linha(s) referenciada(s) é(são) excluída(s). Observe que isso não a isenta de observar quaisquer restrições. Por exemplo, se uma ação especifica `SET DEFAULT`, mas o valor padrão não satisfaria a restrição da chave estrangeira, a operação falhará.

A escolha apropriada da ação `ON DELETE` depende do tipo de objetos que as tabelas relacionadas representam. Quando a tabela de referência representa algo que é um componente do que é representado pela tabela referenciada e não pode existir de forma independente, então `CASCADE` pode ser apropriado. Se as duas tabelas representam objetos independentes, então `RESTRICT` ou `NO ACTION` é mais apropriado; uma aplicação que realmente deseja excluir ambos os objetos teria que ser explícita sobre isso e executar dois comandos de exclusão. No exemplo acima, os itens da ordem fazem parte de uma ordem, e é conveniente se eles forem excluídos automaticamente se uma ordem for excluída. Mas produtos e ordens são coisas diferentes, e então fazer uma exclusão de um produto automaticamente causar a exclusão de alguns itens da ordem pode ser considerado problemático. As ações `SET NULL` ou `SET DEFAULT` podem ser apropriadas se uma relação de chave estrangeira representa informações opcionais. Por exemplo, se a tabela de produtos contivesse uma referência a um gerente de produtos, e a entrada do gerente de produtos for excluída, então definir o gerente de produtos do produto como nulo ou padrão pode ser útil.

As ações `SET NULL` e `SET DEFAULT` podem receber uma lista de colunas para especificar quais colunas devem ser definidas. Normalmente, todas as colunas da restrição de chave estrangeira são definidas; definir apenas um subconjunto é útil em alguns casos especiais. Considere o seguinte exemplo:

```
CREATE TABLE tenants (
    tenant_id integer PRIMARY KEY
);

CREATE TABLE users (
    tenant_id integer REFERENCES tenants ON DELETE CASCADE,
    user_id integer NOT NULL,
    PRIMARY KEY (tenant_id, user_id)
);

CREATE TABLE posts (
    tenant_id integer REFERENCES tenants ON DELETE CASCADE,
    post_id integer NOT NULL,
    author_id integer,
    PRIMARY KEY (tenant_id, post_id),
    FOREIGN KEY (tenant_id, author_id) REFERENCES users ON DELETE SET NULL (author_id)
);
```

Sem a especificação da coluna, a chave estrangeira também definiria a coluna `tenant_id` como nulo, mas essa coluna ainda é necessária como parte da chave primária.

Análogo ao `ON DELETE`, também existe o `ON UPDATE`, que é invocado quando uma coluna referenciada é alterada (atualizada). As ações possíveis são as mesmas, exceto que listas de colunas não podem ser especificadas para `SET NULL` e `SET DEFAULT`. Neste caso, `CASCADE` significa que os valores atualizados da(s) coluna(s) referenciada(s) devem ser copiados na(s) linha(s) de referência. Há também uma diferença notável entre `ON UPDATE NO ACTION` (o padrão) e `ON UPDATE RESTRICT`. O primeiro permitirá que a atualização prossiga e a restrição de chave estrangeira será verificada contra o estado após a atualização. Este último impedirá que a atualização seja executada, mesmo que o estado após a atualização ainda satisfaça a restrição. Isso impede a atualização de uma linha referenciada para um valor que é distinto, mas compara como igual (por exemplo, uma cadeia de caracteres com uma variante de caso diferente, se um tipo de cadeia de caracteres com uma collation sensível ao caso for usado).

Normalmente, uma linha de referência não precisa satisfazer a restrição de chave estrangeira se qualquer uma de suas colunas de referência for nula. Se `MATCH FULL` for adicionado à declaração da chave estrangeira, uma linha de referência escapa de satisfazer a restrição apenas se todas as suas colunas de referência forem nulos (assim, uma mistura de valores nulos e não nulos é garantida para falhar uma restrição `MATCH FULL`). Se você não deseja que as linhas de referência possam evitar satisfazer a restrição da chave estrangeira, declare a(s) coluna(s) de referência como `NOT NULL`.

Uma chave estrangeira deve fazer referência a colunas que sejam uma chave primária ou forme uma restrição única, ou que sejam colunas de um índice único não parcial. Isso significa que as colunas referenciadas sempre têm um índice para permitir pesquisas eficientes sobre se uma linha de referência tem uma correspondência. Como um `DELETE` de uma linha da tabela referenciada ou um `UPDATE` de uma coluna referenciada exigirá uma varredura da tabela de referência para linhas que correspondam ao valor antigo, muitas vezes é uma boa ideia indexar as colunas de referência também. Como isso nem sempre é necessário e há muitas opções disponíveis sobre como indexar, a declaração de uma restrição de chave estrangeira não cria automaticamente um índice nas colunas de referência.

Mais informações sobre atualização e exclusão de dados estão no [Capítulo 6](dml.md). Veja também a descrição da sintaxe de restrição de chave estrangeira na documentação de referência para [CREATE TABLE](sql-createtable.md).

### 5.5.6. Restrições de Exclusão [#](#DDL-CONSTRAINTS-EXCLUSION)

As restrições de exclusão garantem que, se quaisquer duas linhas forem comparadas nas colunas ou expressões especificadas usando os operadores especificados, pelo menos uma dessas comparações de operador retornará falso ou nulo. A sintaxe é:

```
CREATE TABLE circles (
    c circle,
    EXCLUDE USING gist (c WITH &&)
);
```

Veja também `CREATE TABLE ... CONSTRAINT ... EXCLUDE` (sql-createtable.md#SQL-CREATETABLE-EXCLUDE) para detalhes.

Adicionar uma restrição de exclusão criará automaticamente um índice do tipo especificado na declaração da restrição.