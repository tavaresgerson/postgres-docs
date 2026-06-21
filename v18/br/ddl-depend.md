## 5.15. Rastreamento de dependências [#](#DDL-DEPEND)

Quando você cria estruturas de banco de dados complexas que envolvem muitas tabelas com restrições de chave estrangeira, visualizações, gatilhos, funções, etc., você implicitamente cria uma rede de dependências entre os objetos. Por exemplo, uma tabela com uma restrição de chave estrangeira depende da tabela que ela referencia.

Para garantir a integridade de toda a estrutura do banco de dados, o PostgreSQL garante que você não pode descartar objetos que outros objetos ainda dependem. Por exemplo, ao tentar descartar a tabela de produtos que consideramos no [Seção 5.5.5](ddl-constraints.md#DDL-CONSTRAINTS-FK), com a tabela de pedidos dependendo dela, resultaria em uma mensagem de erro como esta:

```
DROP TABLE products;

ERROR:  cannot drop table products because other objects depend on it
DETAIL:  constraint orders_product_no_fkey on table orders depends on table products
HINT:  Use DROP ... CASCADE to drop the dependent objects too.
```

A mensagem de erro contém um aviso útil: se você não quer se incomodar em excluir todos os objetos dependentes individualmente, você pode executar:

```
DROP TABLE products CASCADE;
```

e todos os objetos dependentes serão removidos, assim como quaisquer objetos que dependam deles, recursivamente. Neste caso, ele não remove a tabela de pedidos, apenas remove a restrição de chave estrangeira. Ele para por aí porque nada depende da restrição de chave estrangeira. (Se você quiser verificar o que `DROP ... CASCADE` fará, execute `DROP` sem `CASCADE` e leia a saída de `DETAIL`.)

Quase todos os comandos `DROP` no PostgreSQL suportam a especificação de `CASCADE`. Claro, a natureza das possíveis dependências varia com o tipo do objeto. Você também pode escrever `RESTRICT` em vez de `CASCADE` para obter o comportamento padrão, que é impedir a eliminação de objetos que qualquer outro objeto depende.

### Nota

De acordo com o padrão SQL, especificar `RESTRICT` ou `CASCADE` é necessário em um comando `DROP`. Nenhum sistema de banco de dados realmente aplica essa regra, mas se o comportamento padrão é `RESTRICT` ou `CASCADE` varia entre os sistemas.

Se um comando `DROP` listar vários objetos, o `CASCADE` é necessário apenas quando há dependências fora do grupo especificado. Por exemplo, ao dizer `DROP TABLE tab1, tab2`, a existência de uma chave estrangeira que faz referência a `tab1` de `tab2` não significaria que `CASCADE` é necessário para ter sucesso.

Para uma função ou procedimento definido pelo usuário cujo corpo é definido como uma literal de string, o PostgreSQL acompanha as dependências associadas às propriedades visíveis externamente da função, como seus tipos de argumento e resultado, mas *não* as dependências que só poderiam ser conhecidas ao examinar o corpo da função. Como exemplo, considere esta situação:

```
CREATE TYPE rainbow AS ENUM ('red', 'orange', 'yellow',
                             'green', 'blue', 'purple');

CREATE TABLE my_colors (color rainbow, note text);

CREATE FUNCTION get_color_note (rainbow) RETURNS text AS
  'SELECT note FROM my_colors WHERE color = $1'
  LANGUAGE SQL;
```

(Veja [Seção 36.5] Funções) para uma explicação das funções do SQL.) O PostgreSQL saberá que a função (xfunc-sql.md "36.5. Query Language (SQL) depende do tipo [[PH_LNK_26]]: a eliminação do tipo forçará a eliminação da função, porque o tipo de seu argumento não seria mais definido. Mas o PostgreSQL não considerará que [[PH_LNK_27]] dependa da tabela [[PH_LNK_28]], e, portanto, não eliminará a função se a tabela for eliminada. Embora haja desvantagens nessa abordagem, também há benefícios. A função ainda é válida em algum sentido se a tabela estiver faltando, embora executá-la causará um erro; criar uma nova tabela com o mesmo nome permitirá que a função funcione novamente.

Por outro lado, para uma função ou procedimento em linguagem SQL cujo corpo é escrito em estilo padrão SQL, o corpo é analisado no momento da definição da função e todas as dependências reconhecidas pelo analisador são armazenadas. Assim, se escrevermos a função acima como

```
CREATE FUNCTION get_color_note (rainbow) RETURNS text
BEGIN ATOMIC
  SELECT note FROM my_colors WHERE color = $1;
END;
```

então a dependência da função na tabela `my_colors` será conhecida e aplicada pela `DROP`.