## Crie domínio

CREATE DOMAIN — definir um novo domínio

## Sinopse

```
CREATE DOMAIN name [ AS ] data_type
    [ COLLATE collation ]
    [ DEFAULT expression ]
    [ domain_constraint [ ... ] ]

where domain_constraint is:

[ CONSTRAINT constraint_name ]
{ NOT NULL | NULL | CHECK (expression) }
```

## Descrição

`CREATE DOMAIN` cria um novo domínio. Um domínio é essencialmente um tipo de dados com restrições opcionais (restrições sobre o conjunto de valores permitido). O usuário que define um domínio torna-se seu proprietário.

Se um nome de esquema for fornecido (por exemplo, `CREATE DOMAIN myschema.mydomain ...`) o domínio é criado no esquema especificado. Caso contrário, é criado no esquema atual. O nome do domínio deve ser único entre os tipos e domínios existentes em seu esquema.

Os domínios são úteis para abstrair restrições comuns em campos em um único local para manutenção. Por exemplo, várias tabelas podem conter colunas de endereço de e-mail, todas exigindo a mesma restrição CHECK para verificar a sintaxe do endereço. Defina um domínio em vez de configurar a restrição de cada tabela individualmente.

Para poder criar um domínio, você deve ter o privilégio `USAGE` no tipo subjacente.

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de um domínio a ser criado.

*`data_type`*: O tipo de dados subjacente do domínio. Isso pode incluir especificadores de matriz.

*`collation`*: Uma correção opcional para o domínio. Se não for especificado nenhum tipo de correção, o domínio terá o mesmo comportamento de correção de dados do seu tipo de dados subjacente. O tipo subjacente deve ser correção de dados se `COLLATE` for especificado.

`DEFAULT expression`: A cláusula `DEFAULT` especifica um valor padrão para as colunas do tipo de dados do domínio. O valor é qualquer expressão livre de variáveis (mas subconsultas não são permitidas). O tipo de dados da expressão padrão deve corresponder ao tipo de dados do domínio. Se nenhum valor padrão for especificado, então o valor padrão é o valor nulo.

A expressão padrão será usada em qualquer operação de inserção que não especifique um valor para a coluna. Se um valor padrão for definido para uma coluna específica, ele substituirá qualquer valor padrão associado ao domínio. Por sua vez, o padrão do domínio substituirá qualquer valor padrão associado ao tipo de dados subjacente.

`CONSTRAINT constraint_name`: Um nome opcional para uma restrição. Se não especificado, o sistema gera um nome.

`NOT NULL`: Os valores deste domínio não podem ser nulos (mas veja as notas abaixo).

`NULL`: Os valores deste domínio podem ser nulos. Este é o padrão.

Esta cláusula é destinada apenas à compatibilidade com bancos de dados SQL não padrão. Seu uso é desencorajado em novas aplicações.

As cláusulas `CHECK (expression)`: `CHECK` especificam restrições ou testes de integridade que os valores do domínio devem satisfazer. Cada restrição deve ser uma expressão que produza um resultado booleano. Deve-se usar a palavra-chave `VALUE` para referir-se ao valor que está sendo testado. As expressões que avaliam como VERDADEIRO ou DESCONHECIDO têm sucesso. Se a expressão produzir um resultado FALSO, um erro é relatado e o valor não é permitido ser convertido para o tipo do domínio.

Atualmente, as expressões `CHECK` não podem conter subconsultas nem referir-se a variáveis que não sejam `VALUE`.

Quando um domínio tem múltiplas restrições `CHECK`, elas serão testadas em ordem alfabética por nome. (As versões do PostgreSQL anteriores a 9.5 não respeitavam qualquer ordem específica de disparo para restrições `CHECK`.

## Notas

As restrições de domínio, particularmente `NOT NULL`, são verificadas ao converter um valor para o tipo de domínio. É possível que uma coluna que nominalmente seja do tipo de domínio seja lida como nulo, apesar de existir tal restrição. Por exemplo, isso pode acontecer em uma consulta de junção externa, se a coluna de domínio estiver do lado anulável da junção externa. Um exemplo mais sutil é

```
INSERT INTO tab (domcol) VALUES ((SELECT domcol FROM tab WHERE false));
```

O sub-SELECT escalar vazio produzirá um valor nulo que é considerado do tipo do domínio, portanto, não será aplicada nenhuma verificação adicional de restrição e a inserção terá sucesso.

É muito difícil evitar tais problemas, devido à suposição geral do SQL de que um valor nulo é um valor válido de cada tipo de dado. A melhor prática, portanto, é projetar as restrições de um domínio de modo que um valor nulo seja permitido e, em seguida, aplicar as restrições da coluna `NOT NULL` às colunas do tipo do domínio conforme necessário, em vez de aplicá-las diretamente ao tipo do domínio.

O PostgreSQL assume que as condições das restrições `CHECK` são imutáveis, ou seja, elas sempre darão o mesmo resultado para o mesmo valor de entrada. Essa suposição é o que justifica o exame das restrições `CHECK` apenas quando um valor é convertido pela primeira vez para um tipo de domínio, e não em outros momentos. (Isso é essencialmente o mesmo que o tratamento das restrições da tabela `CHECK`, conforme descrito na [Seção 5.5.1](ddl-constraints.md#DDL-CONSTRAINTS-CHECK-CONSTRAINTS).)

Um exemplo de uma maneira comum de quebrar essa suposição é fazer referência a uma função definida pelo usuário em uma expressão de `CHECK` e, em seguida, alterar o comportamento dessa função. O PostgreSQL não proíbe isso, mas não notará se houver valores armazenados do tipo de domínio que agora violam a restrição `CHECK`. Isso causaria o fracasso de um próximo dump e restabelecimento do banco de dados. A maneira recomendada de lidar com essa mudança é descartar a restrição (usando `ALTER DOMAIN`), ajustar a definição da função e adicionar novamente a restrição, verificando-a novamente contra os dados armazenados.

É também uma boa prática garantir que as expressões do domínio `CHECK` não gerem erros.

## Exemplos

Este exemplo cria o tipo de dados `us_postal_code` e, em seguida, usa o tipo em uma definição de tabela. Um teste de expressão regular é usado para verificar se o valor parece ser um código postal válido dos EUA:

```
CREATE DOMAIN us_postal_code AS TEXT
CHECK(
   VALUE ~ '^\d{5}$'
OR VALUE ~ '^\d{5}-\d{4}$'
);

CREATE TABLE us_snail_addy (
  address_id SERIAL PRIMARY KEY,
  street1 TEXT NOT NULL,
  street2 TEXT,
  street3 TEXT,
  city TEXT NOT NULL,
  postal us_postal_code NOT NULL
);
```

## Compatibilidade

O comando `CREATE DOMAIN` está de acordo com o padrão SQL.

A sintaxe `NOT NULL` neste comando é uma extensão do PostgreSQL. (Uma maneira padrão de escrever o mesmo para tipos de dados não compostos seria `CHECK (VALUE IS NOT NULL)`. No entanto, de acordo com a seção chamada “Notas” (sql-createdomain.md#SQL-CREATEDOMAIN-NOTES "Notes"), essas restrições são melhor evitadas na prática, de qualquer forma.) A “restrição” `NULL` é uma extensão do PostgreSQL (consulte também [Compatibilidade](sql-createtable.md#SQL-CREATETABLE-COMPATIBILITY)).

## Veja também

[ALTERAR DOMÍNIOS](sql-alterdomain.md "ALTER DOMAIN"), [DROP DOMÍNIOS](sql-dropdomain.md "DROP DOMAIN")